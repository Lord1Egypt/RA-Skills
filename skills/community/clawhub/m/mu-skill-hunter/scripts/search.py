#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mu-skill-hunter: 四源 Skill 搜索脚本
来源：GitHub API + ClawHub + SkillHub（HTTP API） + Skills.sh（HTTP API + Vercel OIDC）
优先级：HTTP API > CLI 回退
"""
import sys
import os
import json
import urllib.request
import urllib.parse
import subprocess
import argparse

# 自动从 ~/.bashrc 加载 GITHUB_TOKEN（新 session 未 source 时兜底）
if not os.environ.get("GITHUB_TOKEN"):
    try:
        bashrc = os.path.expanduser("~/.bashrc")
        with open(bashrc) as f:
            for line in f:
                if line.strip().startswith("export GITHUB_TOKEN="):
                    val = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["GITHUB_TOKEN"] = val
                    break
    except Exception:
        pass
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def _find_skillhub_bin():
    """查找 skillhub CLI 二进制路径（默认装在 ~/.local/bin）"""
    # 先尝试 PATH 中查找
    import shutil
    bin_path = shutil.which("skillhub")
    if bin_path:
        return bin_path
    # 回退到常见安装路径
    for candidate in [
        os.path.expanduser("~/.local/bin/skillhub"),
        "/usr/local/bin/skillhub",
        "/opt/homebrew/bin/skillhub",
    ]:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def github_search(query, min_stars=0, language="", limit=10, updated_within=365):
    """搜索 GitHub 仓库"""
    import time
    from datetime import datetime, timedelta

    q = query
    if language:
        q += f" language:{language}"
    if min_stars:
        q += f" stars:>={min_stars}"
    if updated_within < 365:
        since = (datetime.now() - timedelta(days=updated_within)).strftime("%Y-%m-%d")
        q += f" pushed:>={since}"

    params = urllib.parse.urlencode({
        "q": q,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 30)
    })
    url = f"https://api.github.com/search/repositories?{params}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "mu-skill-hunter"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            items = data.get("items", [])
            results = []
            for item in items[:limit]:
                results.append({
                    "source": "GitHub",
                    "name": item["full_name"],
                    "description": item.get("description") or "",
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "language": item.get("language") or "",
                    "updated": item.get("updated_at", "")[:10],
                    "url": item.get("html_url", ""),
                    "license": (item.get("license") or {}).get("spdx_id", ""),
                })
            return results, None
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return [], "GitHub API 速率限制（建议配置 GITHUB_TOKEN）"
        return [], f"GitHub API 错误: {e.code}"
    except Exception as e:
        return [], f"GitHub 搜索失败: {e}"


def clawhub_inspect(slug):
    """拉取单个 Skill 的 Summary + 下载量"""
    try:
        import json as _json
        result = subprocess.run(
            ["npx", "--yes", "clawhub", "inspect", slug, "--json"],
            capture_output=True, text=True, timeout=10
        )
        # 过滤掉 stderr 输出（- Fetching skill 提示行）
        json_text = "\n".join(l for l in result.stdout.splitlines() if not l.startswith("-"))
        data = _json.loads(json_text)
        skill = data.get("skill", {})
        summary = skill.get("summary", "")
        downloads = skill.get("stats", {}).get("downloads", 0)
        return summary, downloads
    except Exception:
        pass
    return "", 0


def clawhub_inspect_batch(slugs, timeout_per=10):
    """并行 inspect 多个 ClawHub slug"""
    procs = []
    for slug in slugs:
        try:
            p = subprocess.Popen(
                ["npx", "--yes", "clawhub", "inspect", slug, "--json"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            procs.append((slug, p))
        except Exception:
            continue

    results = {}
    for slug, p in procs:
        try:
            stdout, _ = p.communicate(timeout=timeout_per)
            json_text = "\n".join(l for l in stdout.splitlines() if not l.startswith("-"))
            data = json.loads(json_text)
            skill = data.get("skill", {})
            results[slug] = (skill.get("summary", ""), skill.get("stats", {}).get("downloads", 0))
        except (subprocess.TimeoutExpired, Exception):
            try:
                p.kill()
                p.wait()
            except Exception:
                pass
            results[slug] = ("", 0)
    return results


def clawhub_search(query, limit=10):
    """搜索 ClawHub（并行 inspect）"""
    try:
        result = subprocess.run(
            ["npx", "--yes", "clawhub", "search", query],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return [], f"clawhub 搜索失败: {result.stderr[:200]}"
        lines = result.stdout.strip().split("\n")
        slugs = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("-") or line.startswith("Install"):
                continue
            parts = line.split()
            if parts:
                slugs.append(parts[0])
        # 并行 inspect 补充 Summary + 下载量
        inspect_data = clawhub_inspect_batch(slugs[:limit], timeout_per=10)
        results = []
        for slug in slugs[:limit]:
            description, downloads = inspect_data.get(slug, ("", 0))
            results.append({
                "source": "ClawHub",
                "name": slug,
                "description": description,
                "downloads": downloads,
                "stars": 0,
                "url": f"https://clawhub.ai/skills/{slug}",
            })
        return results, None
    except FileNotFoundError:
        return [], "clawhub CLI 未安装（运行: npm i -g clawhub）"
    except subprocess.TimeoutExpired:
        return [], "clawhub 搜索超时"
    except Exception as e:
        return [], f"clawhub 搜索失败: {e}"


def skillhub_search(query, limit=10):
    """搜索 SkillHub（腾讯 Skill 商店，国内加速+合规）
    优先使用公开 HTTP API（无需鉴权），CLI 作为回退
    API: GET https://api.skillhub.cn/api/skills?keyword=<query>&sortBy=score&pageSize=<N>
    CLI: skillhub search <query> --json
    CLI 安装: curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash -s -- --cli-only
    """
    # 优先使用 HTTP API（公开，无需鉴权）
    try:
        params = urllib.parse.urlencode({
            "keyword": query,
            "sortBy": "score",
            "pageSize": str(min(limit, 20)),
        })
        url = f"https://api.skillhub.cn/api/skills?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "mu-skill-hunter"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            items = data.get("data", {}).get("skills", [])
            results = []
            for item in items[:limit]:
                slug = item.get("slug", "")
                # 优先用中文描述，取第一行
                desc = item.get("description_zh", "") or item.get("description", "")
                desc_parts = desc.split("\n") if desc else []
                short_desc = desc_parts[0][:120] if desc_parts else ""
                downloads = item.get("downloads", 0)
                installs = item.get("installs", 0)
                results.append({
                    "source": "SkillHub",
                    "name": slug,
                    "display_name": item.get("name", slug),
                    "description": short_desc,
                    "version": "",  # API 不返回版本
                    "downloads": downloads,
                    "installs": installs,
                    "stars": 0,
                    "category": item.get("category", ""),
                    "url": f"https://skillhub.cn/skills/{slug}",
                    "install_cmd": f"skillhub install {slug} --dir <skills目录>",
                })
            return results, None
    except Exception as api_err:
        api_err_msg = str(api_err)
    
    # CLI 回退
    bin_path = _find_skillhub_bin()
    if not bin_path:
        return [], f"SkillHub API 不可用（{api_err_msg}），CLI 未安装（安装: curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash -s -- --cli-only）"
    try:
        result = subprocess.run(
            [bin_path, "search", query, "--json", "--search-limit", str(min(limit, 20))],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return [], f"skillhub 搜索失败: {result.stderr[:200]}"
        data = json.loads(result.stdout)
        items = data.get("results", [])
        results = []
        for item in items[:limit]:
            desc = item.get("description", "")
            desc_parts = desc.split("\n")
            short_desc = desc_parts[0][:120] if desc_parts else desc[:120]
            slug = item.get("slug", "")
            results.append({
                "source": "SkillHub",
                "name": slug,
                "display_name": item.get("name", slug),
                "description": short_desc,
                "version": item.get("version", ""),
                "downloads": 0,
                "stars": 0,
                "url": f"https://skillhub.cn/skills/{slug}",
                "install_cmd": f"skillhub install {slug} --dir <skills目录>",
            })
        return results, None
    except subprocess.TimeoutExpired:
        return [], "skillhub 搜索超时"
    except json.JSONDecodeError as e:
        return [], f"skillhub 响应解析失败: {e}"
    except Exception as e:
        return [], f"skillhub 搜索失败: {e}"


def skillssh_search(query, limit=10):
    """搜索 Skills.sh（通过 npx skills find CLI，无需鉴权）
    Skills.sh HTTP API 需内部鉴权（401），但 CLI 完全公开可用。
    CLI: npx skills find <query>  或  npm i -g skills && skills find <query>
    安装: npx skills add <owner/repo@skill>
    """
    try:
        result = subprocess.run(
            ["npx", "--yes", "skills", "find", query],
            capture_output=True, text=True, timeout=30,
            input="n\n"  # 跳过交互提示
        )
        if result.returncode != 0:
            return [], f"skills CLI 搜索失败: {result.stderr[:200]}"

        import re
        ansi_re = re.compile(r'\x1b\[[0-9;]*m')
        clean = ansi_re.sub('', result.stdout)
        lines = clean.strip().split("\n")
        results = []
        current_slug = None
        current_installs = 0
        for line in lines:
            line = line.strip()
            if not line or '██' in line or line.startswith('Install'):
                continue
            # 匹配 "owner/repo@skill  123.4K installs" 格式
            m = re.match(r'([\w._-]+/[\w._-]+)@([\w._-]+)\s+([\d.]+[KMB]?)\s*installs?', line)
            if m:
                owner_repo = m.group(1)
                skill = m.group(2)
                installs_str = m.group(3)
                current_slug = f"{owner_repo}@{skill}"
                current_installs = _parse_installs_str(installs_str)
                continue
            # 匹配 URL 行 "└ https://skills.sh/..."
            m_url = re.search(r'https://skills\.sh/([\w._/-]+)', line)
            if m_url and current_slug:
                url = f"https://skills.sh/{m_url.group(1)}"
                display = current_slug.split('@')[-1] if '@' in current_slug else current_slug
                results.append({
                    "source": "Skills.sh",
                    "name": current_slug,
                    "display_name": display,
                    "description": "",
                    "installs": current_installs,
                    "downloads": current_installs,
                    "stars": 0,
                    "url": url,
                    "install_url": "",
                    "install_cmd": f"npx skills add {current_slug.replace('@', ' --skill ')}",
                })
                current_slug = None
                if len(results) >= limit:
                    break
        return results[:limit], None
    except FileNotFoundError:
        return [], "skills CLI 未安装（运行: npm i -g skills）"
    except subprocess.TimeoutExpired:
        return [], "skills CLI 搜索超时"
    except Exception as e:
        return [], f"Skills.sh 搜索失败: {e}"


def _parse_installs_str(s):
    """解析 Skills.sh CLI 输出的安装量（如 '95.4K' → 95400）"""
    s = s.strip().upper()
    try:
        if s.endswith('K'):
            return int(float(s[:-1]) * 1000)
        elif s.endswith('M'):
            return int(float(s[:-1]) * 1000000)
        elif s.endswith('B'):
            return int(float(s[:-1]) * 1000000000)
        else:
            return int(float(s))
    except ValueError:
        return 0


def format_results(gh_results, ch_results, ss_results, sh_results, gh_err, ch_err, ss_err, sh_err):
    lines = []

    if gh_results:
        lines.append(f"\n## 🐙 GitHub ({len(gh_results)} 个结果)")
        lines.append(f"{'排名':<4} {'项目':<40} {'⭐Stars':<10} {'语言':<12} {'更新':<12}")
        lines.append("-" * 80)
        for i, r in enumerate(gh_results, 1):
            stars = f"{r['stars']:,}"
            lines.append(f"{i:<4} {r['name']:<40} {stars:<10} {r.get('language',''):<12} {r.get('updated',''):<12}")
            if r.get("description"):
                lines.append(f"     📝 {r['description'][:70]}")
            lines.append(f"     🔗 {r['url']}")
    elif gh_err:
        lines.append(f"\n⚠️ GitHub: {gh_err}")

    if ch_results:
        lines.append(f"\n## 🦀 ClawHub ({len(ch_results)} 个结果)")
        for i, r in enumerate(ch_results, 1):
            downloads = r.get('downloads', 0)
            dl_str = f" ｜ ⬇️{downloads:,}次下载" if downloads else ""
            lines.append(f"{i}. {r['name']}{dl_str}")
            if r.get("description"):
                lines.append(f"   📝 {r['description']}")
            lines.append(f"   🔗 {r['url']}")
    elif ch_err:
        lines.append(f"\n⚠️ ClawHub: {ch_err}")

    if sh_results:
        lines.append(f"\n## 🐉 SkillHub ({len(sh_results)} 个结果)")
        for i, r in enumerate(sh_results, 1):
            ver_str = f" ｜ v{r.get('version','')}" if r.get("version") else ""
            dl_str = ""
            if r.get("downloads"):
                dl_str = f" ｜ ⬇️{r['downloads']}次下载"
            elif r.get("installs"):
                dl_str = f" ｜ 📦{r['installs']}次安装"
            lines.append(f"{i}. {r['name']}{ver_str}{dl_str}")
            if r.get("category"):
                lines.append(f"   🏷️ 分类: {r['category']}")
            if r.get("description"):
                lines.append(f"   📝 {r['description']}")
            lines.append(f"   🔗 {r['url']}")
            if r.get("install_cmd"):
                lines.append(f"   📦 {r['install_cmd']}")
    elif sh_err:
        lines.append(f"\n⚠️ SkillHub: {sh_err}")

    if ss_results:
        lines.append(f"\n## 🛠️ Skills.sh ({len(ss_results)} 个结果)")
        for i, r in enumerate(ss_results, 1):
            inst_str = f" ｜ 📦{r.get('installs',0)}次安装" if r.get("installs") else ""
            lines.append(f"{i}. {r['name']}{inst_str}")
            lines.append(f"   🔗 {r['url']}")
            if r.get("install_cmd"):
                lines.append(f"   📦 {r['install_cmd']}")
    elif ss_err:
        lines.append(f"\n⚠️ Skills.sh: {ss_err}")

    if not gh_results and not ch_results and not ss_results and not sh_results:
        lines.append("\n❌ 四个平台均未找到相关结果，建议换个关键词试试。")

    if not GITHUB_TOKEN:
        lines.append("\n💡 提示：配置 GITHUB_TOKEN 可提升 GitHub 搜索速率（60次/h → 5000次/h）")
        lines.append("   申请地址：https://github.com/settings/tokens（只需 public_repo 只读权限）")
        lines.append("   配置方式：export GITHUB_TOKEN=\"你的token\"")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="mu-skill-hunter 四源搜索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--language", default="", help="编程语言筛选")
    parser.add_argument("--min-stars", type=int, default=0, help="最小 stars 数")
    parser.add_argument("--limit", type=int, default=10, help="每源返回数量")
    parser.add_argument("--updated-within", type=int, default=365, help="最近N天更新")
    parser.add_argument("--source", choices=["all", "github", "clawhub", "skillhub", "skillssh"], default="all")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    gh_results, gh_err = [], None
    ch_results, ch_err = [], None
    ss_results, ss_err = [], None
    sh_results, sh_err = [], None

    if args.source in ("all", "github"):
        gh_results, gh_err = github_search(
            args.query, args.min_stars, args.language, args.limit, args.updated_within
        )
    if args.source in ("all", "clawhub"):
        ch_results, ch_err = clawhub_search(args.query, args.limit)
    if args.source in ("all", "skillhub"):
        sh_results, sh_err = skillhub_search(args.query, args.limit)
    if args.source in ("all", "skillssh"):
        ss_results, ss_err = skillssh_search(args.query, args.limit)

    if args.json:
        print(json.dumps({
            "github": {"results": gh_results, "error": gh_err},
            "clawhub": {"results": ch_results, "error": ch_err},
            "skillhub": {"results": sh_results, "error": sh_err},
            "skillssh": {"results": ss_results, "error": ss_err},
        }, ensure_ascii=False, indent=2))
    else:
        header = f"# 🎯 Skill 猎手搜索结果：\"{args.query}\"\n"
        print(header + format_results(gh_results, ch_results, ss_results, sh_results, gh_err, ch_err, ss_err, sh_err))


if __name__ == "__main__":
    main()
