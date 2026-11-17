#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""invest_skill_copilot · 功能目录同步引擎（双源可降级）

读取 invest-skill 仓库，解析全部 Skill 资产，重建两份本地快照：
  - references/capability-catalog.md  【功能目录】有哪些能力（随 commit 更新）
  - references/repo-spec-digest.md    【规范摘要】要守哪些纪律（相对稳定）

双源优先级（命中即止，继承仓库四级降级的"失败向下、如实标注"精神）：
  1. Gitee 主源：https://gitee.com/warwickInv/invest-skill
  2. GitHub 镜像：https://github.com/chenxyzcyxpp/invest-skill
  两源 commit 可能不同（镜像非实时逐 commit 同步），故快照同时记录 repo_source + repo_commit；
  --check 以"当前可达源 + 其 commit"与快照比对，换源不会误判为"有更新"。

设计纪律（继承仓库 GATEWAY_REFERENCE.md 第 5 节）：
  - 远端不可达 / 解析失败 → 保留上一版快照、明确报错、不猜测、不清空。
  - 权威字段取自各 skill 的 manifest.yaml。

CLI:
  python repo_sync.py --check                 只检测是否有更新（changed/unchanged，含所用源）
  python repo_sync.py --sync                  按优先级选源，拉取并重建两份快照
  python repo_sync.py --sync --diff           同步并打印变更（新增/移除/升版）
  python repo_sync.py --offline --catalog     离线只读本地功能目录并打印
  python repo_sync.py --source github         强制指定源（gitee/github/auto，默认 auto）
  python repo_sync.py --local-repo /path      用本地已克隆仓库同步（离线/加速）
"""
import argparse
import re
import shutil
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# 双源定义：优先级从高到低。raw 模板用于单文件读取（Step 0 正文引用）。
SOURCES = [
    {
        "key": "gitee",
        "label": "Gitee 主源",
        "git": "https://gitee.com/warwickInv/invest-skill.git",
        "web": "https://gitee.com/warwickInv/invest-skill",
        "raw": "https://gitee.com/warwickInv/invest-skill/raw/main/{path}",
    },
    {
        "key": "github",
        "label": "GitHub 镜像",
        "git": "https://github.com/chenxyzcyxpp/invest-skill.git",
        "web": "https://github.com/chenxyzcyxpp/invest-skill",
        "raw": "https://raw.githubusercontent.com/chenxyzcyxpp/invest-skill/main/{path}",
    },
]
SOURCE_BY_KEY = {s["key"]: s for s in SOURCES}

CATEGORIES = {
    "macro_event": "宏观 & 事件类",
    "subject_analysis": "标的分析类",
    "market_review": "行情复盘类",
    "quant_strategy": "量化策略类",
    "subjective_strategy": "主观策略类",
}
RUNTIME_DESC = {
    "llm_prompt": "纯提示词（加载即用）",
    "script_based": "脚本驱动（可复现）",
    "base_skill": "已包装为 BaseSkill",
}
SCRIPTS_DIR = Path(__file__).resolve().parent
PKG_DIR = SCRIPTS_DIR.parent
REF_DIR = PKG_DIR / "references"
CATALOG = REF_DIR / "capability-catalog.md"
DIGEST = REF_DIR / "repo-spec-digest.md"

HEAD_RE = re.compile(r"^([0-9a-f]{40})\s+HEAD", re.M)
ASSET_HEADING = re.compile(r"^###\s+[\d.]+\s+(.+?)\s+·\s+([A-Za-z0-9_]+)\s*$", re.M)


def now_bjt():
    tz = timezone(timedelta(hours=8))
    return datetime.now(timezone.utc).astimezone(tz).strftime("%Y-%m-%d %H:%M UTC+8")


def run(cmd, cwd=None, timeout=60):
    import subprocess
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def source_head(src):
    """返回 (commit, error)；失败 commit=None。"""
    code, out, err = run(["git", "ls-remote", src["git"], "HEAD"], timeout=45)
    if code != 0:
        return None, err
    m = HEAD_RE.search(out)
    return (m.group(1), "") if m else (None, "HEAD 未解析到 commit")


def pick_source(pref="auto"):
    """按优先级探测源，返回 (src, commit, tried)；全部失败返回 (None, None, tried)。"""
    order = SOURCES if pref == "auto" else [SOURCE_BY_KEY[pref]]
    tried = []
    for src in order:
        commit, err = source_head(src)
        if commit:
            return src, commit, tried
        tried.append(f"{src['key']}: {err.strip()[:80]}")
    return None, None, tried


def read_snapshot_meta():
    """从快照读 (source_key, commit)；兼容旧版只有 commit 的快照（视为 gitee）。"""
    if not CATALOG.exists():
        return None, None
    text = CATALOG.read_text(encoding="utf-8")
    m_src = re.search(r"repo_source:\s*(\w+)", text)
    m_com = re.search(r"repo_commit:\s*([0-9a-f]{40})", text)
    return (m_src.group(1) if m_src else "gitee"), (m_com.group(1) if m_com else None)


def ensure_repo(src, local_repo=None):
    """返回 (repo_path, is_temp, commit)。本地仓库优先；否则浅克隆指定源。"""
    if local_repo:
        repo = Path(local_repo).resolve()
        if not (repo / "skills").is_dir():
            raise RuntimeError(f"本地仓库路径无效（缺 skills/）: {repo}")
        code, out, _ = run(["git", "rev-parse", "HEAD"], cwd=str(repo))
        return repo, False, (out if code == 0 else None)
    tmp = Path(tempfile.mkdtemp(prefix="repo_sync_"))
    code, out, err = run(["git", "clone", "--depth", "1", src["git"], str(tmp)], timeout=120)
    if code != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError(f"克隆 {src['label']} 失败: {err}")
    code, out, _ = run(["git", "rev-parse", "HEAD"], cwd=str(tmp))
    return tmp, True, (out if code == 0 else None)


def parse_asset_features(assets_text):
    """从 ASSETS.md 抽取 {skill_id: 功能一句话}。"""
    feats = {}
    for m in ASSET_HEADING.finditer(assets_text):
        sid = m.group(2)
        block = assets_text[m.end(): m.end() + 1400]
        fm = re.search(r"\*\*功能\*\*：(.*)", block)
        if fm:
            txt = re.sub(r"\s+", " ", fm.group(1)).strip()
            feats[sid] = txt[:160] + ("…" if len(txt) > 160 else "")
    return feats


def scan_skills(repo: Path, feats):
    """扫描 skills/<category>/<id>/manifest.yaml，返回能力列表。"""
    skills = []
    skill_root = repo / "skills"
    for cat_dir in sorted(skill_root.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name in {"base", "scripts"} or cat_dir.name.startswith("__"):
            continue
        category = cat_dir.name
        for sid_dir in sorted(cat_dir.iterdir()):
            if not sid_dir.is_dir() or sid_dir.name.startswith("__"):
                continue
            sid = sid_dir.name
            manifest = sid_dir / "manifest.yaml"
            name, version, runtime, desc = sid, "", "llm_prompt", ""
            if manifest.exists() and yaml:
                try:
                    obj = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
                    name = str(obj.get("skill_name") or name)
                    version = str(obj.get("version") or "")
                    runtime = str(obj.get("runtime") or "llm_prompt")
                    desc = str(obj.get("description") or "").strip().replace("\n", " ")
                except Exception:
                    desc = ""
            feature = feats.get(sid) or desc or "（仓库未提供功能简介）"
            skills.append({
                "id": sid, "name": name, "category": category,
                "runtime": runtime, "version": version,
                "path": f"skills/{category}/{sid}/",
                "feature": re.sub(r"\s+", " ", feature).strip(),
            })
    return skills


def write_catalog(skills, src, commit):
    lines = [
        "# invest-skill 功能目录（capability-catalog）",
        "",
        "> 由 `scripts/repo_sync.py` 自动生成，请勿手工编辑。",
        f"> repo_source: {src['key']}（{src['label']}）",
        f"> repo_url: {src['web']}",
        f"> repo_commit: {commit}",
        f"> synced_at: {now_bjt()}",
        f"> 能力总数：{len(skills)}",
        "",
        "本目录是 invest_skill_copilot 的场景路由清单：用户任意投研意图先在此匹配技能，",
        "再按 `methodology-map.md` 内化对应方法论。仓库新增/升版 skill 后随 commit 自动重建。",
        "双源可降级：Gitee 主源不可达时自动切换 GitHub 镜像；换源会触发重建（两源 commit 可能不同）。",
        "",
    ]
    for cat, label in CATEGORIES.items():
        group = [s for s in skills if s["category"] == cat]
        if not group:
            continue
        lines += [f"## {label}（`{cat}/`）", "", "| Skill ID | 名称 | 形态 | 版本 | 一句话能力 |", "|---|---|---|---|---|"]
        for s in group:
            rt = RUNTIME_DESC.get(s["runtime"], s["runtime"])
            lines.append(f"| `{s['id']}` | {s['name']} | {rt} | {s['version'] or '—'} | {s['feature']} |")
        lines.append("")
    lines += [
        "---", "", "## 路由说明",
        "- 命中具体 skill 后，**必须连同其 `references/` 一起读**（仓库 README 警告：只读 SKILL.md 会输出残缺）。",
        "- 本表只反映仓库登记在 `skills/<category>/<id>/manifest.yaml` 的能力；骨架占位（如基金类）在分析时明确告知暂不支持。",
        "- 数据来源纪律见 `repo-spec-digest.md` 与 `data-discipline.md`。", "",
    ]
    CATALOG.write_text("\n".join(lines), encoding="utf-8")


def write_digest(repo: Path, skills, src, commit):
    lines = [
        "# invest-skill 规范摘要（repo-spec-digest）", "",
        "> 由 `scripts/repo_sync.py` 自动生成，请勿手工编辑。",
        f"> repo_source: {src['key']}（{src['label']}）",
        f"> repo_commit: {commit}",
        f"> synced_at: {now_bjt()}",
        "> 用途：分析时快速内化仓库数据纪律与护栏；细节以仓库原文为准。", "",
        "## 一、防幻觉护栏（最高优先级红线，源自 GATEWAY_REFERENCE.md 第 5 节）",
        "1. 不编造：取数失败/字段缺失/源无数据一律标注 N/A，严禁生成数字、结论或引用。",
        "2. 可溯源：每个字段标注 data_source 与获取时间；区分实测数据与模型推断。",
        "3. 降级留痕：记录从哪级、因何、切到哪级、最终命中来源（gateway_trace）。",
        "4. 明确报错：全源失败返回 error，不回退过期缓存、不返回占位值。",
        "5. 事实与结论分离：推断须显式标注为观点。",
        "6. 局部失败不阻断：某维度缺失显式标注，其余照常输出，不掩盖缺口。", "",
        "## 二、四级数据源降级链（命中即止，顺序不可跳级）",
        "1. Tushare（需 TUSHARE_TOKEN，全品类）→ 2. Akshare（免 token，主降级）→",
        "3. Baostock（免 token，财务兜底）→ 4. 东方财富/腾讯网页源（基础行情兜底）。",
        "全部失败 → 明确报错。关键字段至少取一个次级源交叉校验（价格>1%/比率>5% 标 conflict）。",
        "字段缺失不插值、不估算。", "",
        "## 三、场景—方法论映射（权威明细见 methodology-map.md）",
        "个股诊断→五维分析；对比→对比分析；选股→量化选股；行业→行业速报；",
        "产业链→主题产业链；政策→政策解读；舆情→舆情风险；抄底→底部信号；",
        "宏观→宏观分析；热点→市场热点；收评→每日收评；隔夜→隔夜外围复盘。", "",
        "## 四、仓库读取双源（Gitee 主 → GitHub 镜像备）",
        f"- 主源：{SOURCES[0]['web']}",
        f"- 镜像：{SOURCES[1]['web']}",
        "- 主源不可达自动切镜像；两源 commit 可能不同，以实际命中的源为准。", "",
        "## 五、当前仓库 Skill 清单（按功能目录）", "",
    ]
    for s in skills:
        lines.append(f"- `{s['id']}`（{s['name']}，{s['runtime']}）：{s['feature']}")
    if (repo / "skills" / "base" / "GATEWAY_REFERENCE.md").exists():
        lines += ["", "> 完整护栏与网关契约原文：`skills/base/GATEWAY_REFERENCE.md`（仓库内）。"]
    lines.append("")
    DIGEST.write_text("\n".join(lines), encoding="utf-8")


def diff_catalog(old_text, new_skills):
    if not old_text:
        return ["（首次生成，无历史快照）"]
    old_ids = set(re.findall(r"^\| `([a-z0-9_]+)` \|", old_text, re.M))
    old_versions = dict(re.findall(r"^\| `([a-z0-9_]+)` \|.*?\| ([\d.]+) \|", old_text, re.M))
    new_ids = {s["id"] for s in new_skills}
    added = sorted(new_ids - old_ids)
    removed = sorted(old_ids - new_ids)
    bumped = []
    for s in new_skills:
        ov = old_versions.get(s["id"])
        if ov and s["version"] and ov != s["version"]:
            bumped.append(f"{s['id']}: {ov} → {s['version']}")
    return [
        f"新增 skill：{', '.join(added) if added else '无'}",
        f"移除 skill：{', '.join(removed) if removed else '无'}",
        f"升版：{'; '.join(bumped) if bumped else '无'}",
    ]


def do_check(args):
    src, commit, tried = pick_source(args.source)
    if src is None:
        print("unknown: 所有源均不可达（无法检测更新）")
        for t in tried:
            print(f"  - {t}")
        return 3
    old_src, old_commit = read_snapshot_meta()
    if old_src == src["key"] and old_commit == commit:
        print(f"unchanged: [{src['key']}] {commit[:8]}")
        return 0
    print(f"changed: [{src['key']}] {commit[:8]}（本地快照 [{old_src}] {old_commit[:8] if old_commit else '无'}）")
    return 2


def do_sync(args):
    old_text = CATALOG.read_text(encoding="utf-8") if CATALOG.exists() else ""
    if args.local_repo:
        # 本地仓库：源按用户指定或默认主源标记，commit 取本地 HEAD
        src = SOURCE_BY_KEY[args.source] if args.source != "auto" else SOURCES[0]
        repo, is_temp, commit = ensure_repo(src, args.local_repo)
    else:
        src, commit, tried = pick_source(args.source)
        if src is None:
            sys.stderr.write("[error] 所有源均不可达，放弃同步（保留旧快照）：\n")
            for t in tried:
                sys.stderr.write(f"  - {t}\n")
            return 1
        repo, is_temp, commit = ensure_repo(src)
    if not commit:
        sys.stderr.write("[error] 无法确定仓库 commit，放弃同步（保留旧快照）。\n")
        return 1
    feats = parse_asset_features((repo / "ASSETS.md").read_text(encoding="utf-8"))
    skills = scan_skills(repo, feats)
    if not skills:
        sys.stderr.write("[error] 未解析到任何 skill，放弃同步（保留旧快照）。\n")
        if is_temp:
            shutil.rmtree(repo, ignore_errors=True)
        return 1
    REF_DIR.mkdir(parents=True, exist_ok=True)
    write_catalog(skills, src, commit)
    write_digest(repo, skills, src, commit)
    print(f"synced: [{src['key']}] commit={commit[:8]} skills={len(skills)}")
    print("快照：capability-catalog.md / repo-spec-digest.md 已重建")
    if args.diff:
        print("--- 本次变更 ---")
        for line in diff_catalog(old_text, skills):
            print(line)
    if is_temp:
        shutil.rmtree(repo, ignore_errors=True)
    return 0


def do_offline_catalog():
    if not CATALOG.exists():
        sys.stderr.write("[error] 本地无功能目录快照，请先联网同步。\n")
        return 1
    print(CATALOG.read_text(encoding="utf-8"))
    return 0


def main():
    ap = argparse.ArgumentParser(description="invest-skill 功能目录同步引擎（双源可降级）")
    ap.add_argument("--check", action="store_true", help="只检测是否有更新（含所用源）")
    ap.add_argument("--sync", action="store_true", help="按优先级选源并重建两份快照")
    ap.add_argument("--diff", action="store_true", help="同步时打印变更")
    ap.add_argument("--offline", action="store_true", help="离线只读本地快照")
    ap.add_argument("--catalog", action="store_true", help="配合 --offline 打印功能目录")
    ap.add_argument("--source", choices=["auto", "gitee", "github"], default="auto", help="源选择，默认 auto（Gitee 优先，失败切 GitHub 镜像）")
    ap.add_argument("--local-repo", default=None, help="用本地已克隆仓库同步（离线/加速）")
    args = ap.parse_args()
    if yaml is None and (args.sync or not args.check and not args.offline):
        sys.stderr.write("[error] 需要 pyyaml：pip install pyyaml\n")
        return 1
    if args.check:
        return do_check(args)
    if args.sync:
        return do_sync(args)
    if args.offline and args.catalog:
        return do_offline_catalog()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
