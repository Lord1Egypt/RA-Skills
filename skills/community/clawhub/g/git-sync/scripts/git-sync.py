#!/usr/bin/env python3
"""
git-sync.py v2.12.0 - 完整 Python 版 git-sync
跨平台兼容（Windows/Linux/macOS），不依赖 rsync
用法: python git-sync.py <skill-name> [--skip-scan]
"""
import os
import sys
import json
import shutil
import subprocess
import argparse
import builtins

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR, SKILLS_ROOT as SKILLS_DIR,
    WORK_REPO, DIST_DIR, MANIFEST_FILE, README_FILE, GIT_CREDENTIALS,
    SCAN_OUT_PREFIX,
)

# ── 编码安全 ─────────────────────────────────────────────
# Windows Git Bash (GBK) 下 print(emoji) 直接崩，
# 模块级替换 print 为安全版本，避免挨个改 30+ 处调用。
_original_print = builtins.print
def _safe_print(*args, **kwargs):
    try:
        _original_print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = [str(a).encode("ascii", errors="replace").decode("ascii") for a in args]
        _original_print(*safe_args, **kwargs)
builtins.print = _safe_print
import tempfile
from pathlib import Path
from datetime import datetime


# ── 强制 UTF-8 输出（Windows 终端兼容）────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── 路径配置 ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()

# ZIP 打包排除模式（支持 *.ext, dir/, 精确名）
EXCLUDE_PATTERNS = [
    "*.bak", "__pycache__/", "*.pyc", ".git/", ".mcp.json",
    "node_modules/", ".DS_Store", "Thumbs.db",
    "nul", "NUL",  # Windows 保留设备名，在目录中无法删除且 copytree 崩溃
]

# ── 颜色输出 ──────────────────────────────────────────────────────────────────
class C:
    R = "\033[0;31m"; G = "\033[0;32m"; Y = "\033[1;33m"
    B = "\033[0;34m"; C = "\033[0;36m"; W = "\033[1;37m"; N = "\033[0m"

LOG_BUFFER = []  # 全局日志缓冲

def log(step, total, msg, level="info"):
    tag = {"info":"[i]","ok":"[OK]","warn":"[!]","err":"[X]","skip":"[-]"}.get(level,"[i]")
    LOG_BUFFER.append(f"[{step}/{total}] {tag} {msg}")

def _git_env(base_env: dict = None) -> dict:
    """
    构造一个完全静默的 git 环境变量字典。
    用 GIT_CONFIG_COUNT 注入 credential.helper=（空=禁用），
    优先级高于所有配置文件，覆盖所有子进程（含 Python 脚本内调 git）。
    """
    env = base_env.copy() if base_env else os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    return env

QUIET_MODE = False  # 静默模式标记

def run_python(script: Path, *args, capture=False, check=True):
    """运行 scripts/ 下的 Python 辅助脚本"""
    env = _git_env()
    env["PYTHONUTF8"] = "1"
    cmd = [sys.executable, str(script), *[str(a) for a in args]]
    # 静默模式下强制捕获子进程输出
    if QUIET_MODE:
        capture = True
    return subprocess.run(cmd, capture_output=capture, encoding="utf-8",
                         check=check, env=env,
                         stdin=subprocess.DEVNULL)

def run_git(*args, workdir=None, check=True):
    """
    运行 git 命令，完全静默不弹 UI。
    用 _git_env() 注入 GIT_CONFIG_COUNT，彻底阻止所有子进程弹窗。
    """
    env = _git_env()
    si = None
    if os.name == "nt":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
    cmd = ["git",
           "-c", "credential.helper=",
           "-c", "credential.https://gitee.com.provider=",
           "-c", "credential.https://github.com.provider=",
           *[str(a) for a in args]]
    try:
        return subprocess.run(cmd, cwd=str(workdir or WORK_REPO),
                             capture_output=True, encoding="utf-8",
                             check=check, env=env, timeout=120,
                             stdin=subprocess.DEVNULL,
                             startupinfo=si)
    except subprocess.TimeoutExpired:
        ret = subprocess.CompletedProcess(args=cmd, returncode=-1,
                                          stdout='', stderr='TIMEOUT')
        return ret

# ── 步骤 1：检查维护清单 ─────────────────────────────────────────────────────
def step_manifest(skill_name: str, version: str, repo_name="workbuddy-skills"):
    log(1, 8, "检查维护清单...")
    manifest_py = SCRIPT_DIR / "manifest.py"
    if not manifest_py.exists():
        log(1, 8, "manifest.py 不存在，跳过", "skip")
        return
    # manifest.py 用 exit code 2 表示 NOT_FOUND，不能用 check=True
    r = run_python(manifest_py, "check", repo_name, skill_name,
                   capture=True, check=False)
    status = r.stdout.strip()
    if status == "NOT_FOUND":
        log(1, 8, "不在清单中，自动添加...", "warn")
        run_python(manifest_py, "add", repo_name, skill_name,
                   check=False)
    elif status == "FOUND:not-uploaded":
        log(1, 8, "在清单中，未上传（正常）", "ok")
    else:
        log(1, 8, "在清单中，已上传", "ok")

# ── 步骤 2：版本号对比 ───────────────────────────────────────────────────────
def step_version_compare(skill_name: str, local_ver: str) -> str:
    log(2, 8, "版本号对比（仓库 vs 本地源文件）...")
    repo_meta = WORK_REPO / "skills" / skill_name / "_meta.json"
    repo_ver = ""
    if repo_meta.exists():
        try:
            repo_ver = json.load(open(repo_meta, encoding="utf-8"))["version"]
        except Exception:
            pass
    # 统一去掉 v 前缀
    def _strip_v(s):
        return s[1:] if s.startswith("v") else s

    repo_ver = _strip_v(repo_ver) if repo_ver else ""
    local_ver = _strip_v(local_ver)

    print(f"  仓库版本: {repo_ver or '（无）'}")
    print(f"  本地源文件版本: {local_ver}")

    if not repo_ver:
        log(2, 8, "仓库无版本记录，正常同步", "ok")
        return "normal"
    if repo_ver == local_ver:
        log(2, 8, f"版本相同 ({local_ver})，跳过文件同步", "skip")
        return "skip_sync"
    # 简单版本比较
    def ver_lt(a, b):
        na = [int(x) for x in a.split(".")]
        nb = [int(x) for x in b.split(".")]
        return na < nb
    if ver_lt(repo_ver, local_ver):
        log(2, 8, "仓库版本 < 本地版本，正常升级", "ok")
        return "normal"
    else:
        log(2, 8, f"版本异常：仓库({repo_ver}) > 本地({local_ver})", "err")
        print("  请手动处理版本冲突后重试。")
        sys.exit(1)

# ── 步骤 3：_meta.json 标准化校验 ──────────────────────────────────────────
def step_normalize_meta(meta_file: Path, skill_name: str, version: str):
    log(3, 8, "同步 _meta.json 版本号（保留所有字段）...")
    normalize_py = SCRIPT_DIR / "normalize_meta.py"
    if not normalize_py.exists():
        log(3, 8, "normalize_meta.py 不存在，跳过", "skip")
        return
    desc = get_meta_desc(meta_file)
    run_python(normalize_py, str(meta_file), skill_name, version, desc)

# ── 步骤 3.5：SKILL.md 规范化审查（只读扫描，不修改、不阻断） ────────────────────────────────────────
# ── 步骤 3.5：轻量审计（只读，不修改、不阻断） ─────────────────────────────────────
def step_skill_audit(skill_name: str, skills_dir: Path, manifest_file: Path,
                     desensitized_files=None, repo_skill_dir=None):
    """
    轻量审计：只检查版本一致性和 R-23（脚本引用一致性）。
    只读不修改，不输出修复建议，不触发修复。
    返回 audit_result dict 用于最终报告。
    """
    audit_result = {"summary": {"errors": 0, "warns": 0}, "results": [], "verdict": "pass"}

    skill_md = skills_dir / skill_name / "SKILL.md"
    if not skill_md.exists():
        print("  ⚠️  审计结论：SKILL.md 不存在，跳过")
        return audit_result

    md_text = skill_md.read_text(encoding="utf-8")
    md_lines = md_text.splitlines()

    # ── 检查1：版本一致性（SKILL.md vs _meta.json vs manifest） ──
    md_ver = ""
    for line in md_lines:
        if line.startswith("version:"):
            md_ver = line.split(":", 1)[1].strip()
            break

    meta_file = skills_dir / skill_name / "_meta.json"
    meta_ver = ""
    if meta_file.exists():
        try:
            m = json.loads(meta_file.read_text(encoding="utf-8"))
            meta_ver = m.get("version", "")
        except Exception:
            pass

    manifest_ver = ""
    try:
        mf = json.loads(manifest_file.read_text(encoding="utf-8"))
        items = mf.get("repos", {}).get("workbuddy-skills", {}).get("items", {})
        manifest_ver = items.get(skill_name, {}).get("version", "")
    except Exception:
        pass

    version_errors = []
    if md_ver and meta_ver and md_ver != meta_ver:
        version_errors.append(f"SKILL.md({md_ver}) != _meta.json({meta_ver})")
    if md_ver and manifest_ver and md_ver != manifest_ver:
        version_errors.append(f"SKILL.md({md_ver}) != manifest({manifest_ver})")

    if version_errors:
        audit_result["summary"]["errors"] += len(version_errors)
        for ve in version_errors:
            audit_result["results"].append({
                "rule_id": "R-version",
                "passed": False, "skipped": False,
                "detail": ve
            })

    # ── 检查2：R-23 脚本引用一致性 ────────────────────────
    import re
    md_script_refs = set()
    for line in md_lines:
        m = re.search(r'["\']([^"\']+\.py)["\']', line)
        if m:
            script_path = m.group(1)
            script_name = script_path.replace("\\", "/").split("/")[-1]
            md_script_refs.add(script_name)

    scripts_dir = skills_dir / skill_name / "scripts"
    r23_errors = []
    if scripts_dir.exists():
        actual_scripts = {f.name for f in scripts_dir.iterdir() if f.is_file() and f.suffix == ".py"}
        for ref in md_script_refs:
            if ref not in actual_scripts:
                r23_errors.append(f"MD 引用了不存在的脚本: {ref}")

    if r23_errors:
        audit_result["summary"]["errors"] += len(r23_errors)
        for err in r23_errors:
            audit_result["results"].append({
                "rule_id": "R-23",
                "passed": False, "skipped": False,
                "detail": err
            })

    # ── 检查3：脱敏状态（直接读取 step_sensitive_scan 的执行结果） ──
    # desensitized_files 是 set，非 None 表示执行了扫描（无论是否有结果）
    desensitization_info = {
        "scanned": desensitized_files is not None,
        "sanitized": desensitized_files is not None and len(desensitized_files) > 0,
        "sanitized_files": sorted(str(f) for f in (desensitized_files or []))
    }
    audit_result["desensitization"] = desensitization_info

    # ── 检查4：文件筛选状态（确认 EXCLUDE_PATTERNS 已生效） ──
    filter_info = {
        "exclude_patterns": EXCLUDE_PATTERNS,
        "status": "active"
    }
    # git-sync 本身通过 _ignore_patterns() 和 clean_zip_source.py 保证筛选
    # 审计只需确认 EXCLUDE_PATTERNS 非空即可，不重复遍历目录
    audit_result["filter"] = filter_info

    # ── 定 verdict ──────────────────────────────────────────────
    if audit_result["summary"]["errors"] > 0:
        audit_result["verdict"] = "fail"
    elif audit_result["summary"]["warns"] > 0:
        audit_result["verdict"] = "warn"
    else:
        audit_result["verdict"] = "pass"

    # ── 输出结论（只输出结论，不展开细节）────────────────────
    errors = audit_result["summary"]["errors"]
    warns  = audit_result["summary"]["warns"]
    verdict = audit_result["verdict"]
    if verdict == "pass":
        print(f"  ✅ 审计结论：PASS（ERROR={errors}, WARN={warns}）")
    elif verdict == "warn":
        print(f"  ⚠️  审计结论：WARN（ERROR={errors}, WARN={warns}）—— 建议优化，不阻断同步")
    else:
        print(f"  ❌ 审计结论：FAIL（ERROR={errors}, WARN={warns}）—— 仅记录，不阻断同步")

    return audit_result

def _ignore_patterns(path, names):
    ignored = set()
    for name in names:
        for pat in EXCLUDE_PATTERNS:
            if pat.startswith("*"):
                if name.endswith(pat[1:]):
                    ignored.add(name); break
            elif pat.endswith("/"):
                if (Path(path) / name).is_dir() and name == pat.rstrip("/"):
                    ignored.add(name); break
            else:
                if name == pat:
                    ignored.add(name); break
    return ignored

def sync_files(skill_name: str, skills_dir: Path, work_repo: Path):
    """用 Python 逐个复制文件（替代 shutil.copytree，避免 Windows 保留设备名问题）"""
    src = skills_dir / skill_name
    dst = work_repo / "skills" / skill_name
    if dst.exists():
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    file_count = 0
    for item in src.rglob("*"):
        # Windows 保留设备名：在 Windows 上 os.path.exists('nul') 始终返回 True
        # 即使目录中根本没有这个文件。Path.rglob 遍历时如果构造出 'nul' 路径
        # is_file() 会返回 False（设备不是文件），但 shutil.copy2 会崩溃
        if item.name.lower() == "nul":
            continue
        if item.is_file():
            try:
                rel = item.relative_to(src)
                dst_file = dst / rel
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_file)
                file_count += 1
            except (OSError, shutil.Error):
                pass  # 跳过无法复制的文件
    # 二次保险：清理残留的 __pycache__
    for root, dirs, _ in os.walk(dst):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(Path(root) / d, ignore_errors=True)
    count = sum(1 for _ in dst.rglob("*") if _.is_file())
    log(4, 8, f"已同步 {count} 个文件到 {dst}", "ok")
    return dst

# ── 步骤 4.5：敏感信息扫描 ────────────────────────────────────────────────
def step_sensitive_scan(skill_name: str, repo_skill_dir: Path,
                        skip_scan: bool = False):
    """
    扫描并脱敏敏感信息。
    返回 desensitized_files: set（脱敏涉及的文件相对路径集合）
    """
    desensitized_files = set()
    log("4.5", 8, "扫描敏感信息...")
    if skip_scan:
        log("4.5", 8, "已跳过敏感信息扫描（--skip-scan）", "skip")
        return desensitized_files
    scan_py = SCRIPT_DIR / "sensitive_scan.py"
    if not scan_py.exists():
        log("4.5", 8, "sensitive_scan.py 不存在，跳过", "skip")
        return desensitized_files

    scan_out = SCRIPT_DIR / f".sensitive_scan_{skill_name}.json"
    run_python(scan_py, "scan", str(repo_skill_dir),
               "--output", str(scan_out))

    if not scan_out.exists() or scan_out.stat().st_size == 0:
        log("4.5", 8, "未发现敏感信息", "ok")
        scan_out.unlink(missing_ok=True)
        return desensitized_files

    # ── 打印扫描结果详情 ──────────────────────────────────────────────────
    d = json.load(scan_out.open(encoding="utf-8"))
    total_findings = sum(len(e.get("findings", [])) for e in d)
    if total_findings == 0:
        log("4.5", 8, "未发现敏感信息", "ok")
        scan_out.unlink(missing_ok=True)
        return desensitized_files
    print(f"  ⚠️  发现敏感信息：共 {len(d)} 个文件，{total_findings} 处")
    for e in d:
        file_rel = e["file"]       # 已是相对路径，如 "references/faq.md"
        finds = e.get("findings", [])
        if not finds:
            continue
        print(f"  📄 {file_rel}（{len(finds)} 处）")
        for f in finds[:5]:          # 每文件最多显示 5 条
            label = f.get("label", "敏感信息")
            severity = f.get("severity", "")
            line = f.get("line", "?")
            replace = f.get("replace", "[redacted]")
            print(f"      [{severity}] 第 {line} 行 {label} → 替换为：{replace}")
        if len(finds) > 5:
            print(f"      ... 还有 {len(finds) - 5} 处未显示")

    # ── HOOK-BLOCK：等待 LLM 判断 ─────────────────────────────────────────
    # 扫描结果已保存到 scan_out，LLM 需审阅后手动创建决策文件
    decisions = SCRIPT_DIR / f".sensitive_scan_{skill_name}.json.decisions.json"
    print(f"\n{'='*60}")
    print(f"[HOOK-BLOCK] 发现 {total_findings} 处潜在敏感信息，需 LLM 判断")
    print(f"{'='*60}")
    print(f"  扫描结果: {scan_out}")
    print(f"  请审阅上方 findings，逐个判断是否需要脱敏。")
    print(f"  判断原则：邮箱/token/内网IP → 脱敏；公开署名/代名/示例路径 → 跳过")
    print(f"")
    print(f"  确认后，创建决策文件: {decisions}")
    print(f"  决策文件格式: [{{\"file\":\"<相对路径>\",\"field\":\"<匹配文本>\",\"action\":\"sanitize|skip\"}},...]")
    print(f"  创建后重新运行 git-sync 继续。")
    print(f"{'='*60}\n")
    sys.exit(1)  # HOOK-BLOCK：阻断管道

# ── 步骤 5：更新 README.md ─────────────────────────────────────────────────
def step_update_readme(repo_name="workbuddy-skills"):
    log(5, 8, "更新 README.md...")
    readme = WORK_REPO / "README.md"
    if not readme.exists():
        log(5, 8, "README.md 不存在，跳过", "skip")
        return
    update_py = SCRIPT_DIR / "update_readme.py"
    if not update_py.exists():
        log(5, 8, "update_readme.py 不存在，跳过", "skip")
        return
    run_python(update_py, repo_name, str(readme))
    log(5, 8, "README.md 已更新", "ok")

# ── 步骤 6：提交并推送到双平台 ────────────────────────────────────────────
def _detect_remote(url_pattern: str) -> str:
    """根据 URL 关键字检测远程名，找不到返回空字符串"""
    r = run_git("remote", "-v",
                 workdir=WORK_REPO, check=False)
    for line in r.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and url_pattern in parts[1]:
            return parts[0]
    return ""

def _get_cred_url(host: str) -> str:
    """从 ~/.git-credentials 读取含凭证的 URL，精确匹配 host"""
    cred_file = Path.home() / ".git-credentials"
    if not cred_file.exists():
        return ""
    best = ""
    for line in cred_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        # 精确匹配：解析凭证 URL 的 host，与 target host 对比
        from urllib.parse import urlparse
        try:
            line_host = urlparse(line).hostname or ""
        except Exception:
            continue
        if line_host == host:
            best = line
            break  # 精确匹配，直接用
    return best

def _classify_push_error(remote_name: str, stderr: str, stdout: str) -> str:
    """
    将 git push/pull 的原始错误输出归类为人类可读的中文描述。
    防止 LLM 误读原始错误码（如 443 超时误判为"网络正常"）。
    返回统一格式的错误描述字符串。
    """
    raw = (stderr or stdout or "").lower()
    # ── 网络类错误 ──
    if "timed out" in raw or "timeout" in raw or "443" in raw:
        return f"⏱️ 网络超时：{remote_name} 连接超时（可能被墙），请检查网络或重试"
    if "could not resolve host" in raw or "name or service not known" in raw:
        return f"🌐 DNS 解析失败：{remote_name} 域名无法解析，请检查网络"
    if "connection refused" in raw:
        return f"🔒 连接被拒绝：{remote_name} 拒绝了连接"
    if "connection reset by peer" in raw:
        return f"🔌 连接被重置：{remote_name} 连接被对端重置"
    if "network is unreachable" in raw or "no route to host" in raw:
        return f"📡 网络不可达：{remote_name} 无法访问，请检查网络连接"
    if "couldn't connect to server" in raw or "cannot connect" in raw:
        return f"🔗 无法连接到服务器：{remote_name}"
    # ── 认证类错误 ──
    if "permission denied" in raw and "publickey" in raw:
        return f"🔑 SSH 密钥认证失败：{remote_name} 拒绝了公钥，请检查 SSH 配置"
    if "authentication failed" in raw or "auth failed" in raw:
        return f"🔑 认证失败：{remote_name} 用户名或密码/Token 错误"
    if "could not read from remote repository" in raw:
        return f"📂 无法读取远程仓库：{remote_name}，请检查仓库地址和权限"
    if "access denied" in raw or "access denied" in raw:
        return f"🚫 访问被拒绝：{remote_name} 无此仓库的访问权限"
    # ── 协议/远程拒绝类错误 ──
    if "rejected" in raw and "fetch first" in raw or "non-fast-forward" in raw:
        return f"🔄 推送被拒绝：{remote_name} 远程仓库有未拉取的更新，请 pull --rebase 后重试"
    if "rejected" in raw and "push" in raw:
        return f"🚫 推送被拒绝：{remote_name} 拒绝推送，请检查分支权限或冲突"
    if "couldn't find remote ref" in raw:
        return f"🔍 远程分支不存在：{remote_name} 的 {branch} 分支不存在"
    # ── 回退：保留原始错误的前 200 字符 ──
    truncated = (stderr or stdout or "未知错误").strip()
    if len(truncated) > 200:
        truncated = truncated[:200] + "..."
    return f"❌ 推送失败：{remote_name} - {truncated}"

def _resolve_push_url(remote_name: str) -> tuple:
    """
    解析远程 URL，优先使用 URL 内嵌凭证，其次从 ~/.git-credentials 查找。
    返回 (cred_url: str, raw_url: str, error: str)
    cred_url 为带凭证的可推送 URL；error 非空时表示无法解析。
    """
    r = run_git("remote", "get-url", remote_name,
                 workdir=WORK_REPO, check=False)
    if r.returncode != 0:
        return "", "", f"获取 remote URL 失败: {r.stderr.strip()}"
    raw_url = r.stdout.strip()

    from urllib.parse import urlparse
    parsed = urlparse(raw_url)

    # ★ v2.23.2: 检测 SSH URL — SSH 用 key 认证，不需要 credential 注入
    # SSH 格式: git@host:path (urlparse 无 scheme/hostname) 或 ssh://git@host/path (scheme=ssh)
    _is_ssh = (
        parsed.scheme == 'ssh' or
        (not parsed.scheme and '@' in raw_url and ':' in raw_url)
    )
    if _is_ssh:
        return raw_url, raw_url, ""

    host = parsed.hostname or ""

    # 情况1：URL 已内嵌凭证（如 https://user:[email-redacted]/path）
    if parsed.password:
        return raw_url, raw_url, ""

    # 情况2：从 ~/.git-credentials 查找
    cred_url = _get_cred_url(host)
    if cred_url:
        # 补全路径（凭证 URL 可能只有主机名）
        parsed_cred = urlparse(cred_url)
        if not parsed_cred.path or parsed_cred.path == '/':
            parsed_raw = urlparse(raw_url)
            cred_url = f"{parsed_cred.scheme}://{parsed_cred.netloc}{parsed_raw.path}"
        return cred_url, raw_url, ""

    # 情况3：都没有
    return "", raw_url, f"找不到 {host} 的凭证（remote URL 未内嵌 token，~/.git-credentials 中也无该 host 条目）"


def _push_with_cred_url(remote_name: str, branch: str = "main") -> tuple:
    """
    用凭证嵌入 URL 直接 push，完全绕开 CredentialHelperSelector。
    返回 (success: bool, error_msg: str)
    """
    cred_url, raw_url, error = _resolve_push_url(remote_name)
    if error:
        return False, error

    # 临时覆盖 remote URL（含凭证），push 完立刻恢复
    run_git("remote", "set-url", remote_name, cred_url,
             workdir=WORK_REPO, check=False)
    try:
        r = run_git("push", remote_name, branch,
                     workdir=WORK_REPO, check=False)
        if r.returncode == 0:
            return True, ""
        error_msg = _classify_push_error(remote_name, r.stderr, r.stdout)
        return False, error_msg
    finally:
        run_git("remote", "set-url", remote_name, raw_url,
                 workdir=WORK_REPO, check=False)

def _pull_with_cred_url(remote_name: str, branch: str = "main") -> tuple:
    """用凭证嵌入 URL 直接 pull，完全绕开 CredentialHelperSelector"""
    cred_url, raw_url, error = _resolve_push_url(remote_name)
    if error:
        return False, error

    run_git("remote", "set-url", remote_name, cred_url,
             workdir=WORK_REPO, check=False)
    try:
        r = run_git("pull", remote_name, branch, "--rebase",
                     workdir=WORK_REPO, check=False)
        if r.returncode != 0:
            error_msg = _classify_push_error(remote_name, r.stderr, r.stdout)
            return False, error_msg
        return True, ""
    finally:
        run_git("remote", "set-url", remote_name, raw_url,
                 workdir=WORK_REPO, check=False)

def step_commit_and_push(skill_name: str, version: str):
    log(6, 8, "提交并推送...")
    if not WORK_REPO.exists():
        log(6, 8, f"工作仓库不存在: {WORK_REPO}", "err")
        return False, False

    # git config — 从 config.json 读取提交者信息
    import json as _json
    _cfg_path = Path(__file__).resolve().parent.parent.parent / ".standardization" / "git-sync" / "data" / "config.json"
    try:
        _cfg = _json.loads(_cfg_path.read_text(encoding="utf-8"))
    except Exception:
        _cfg = {}
    git_user = _cfg.get("author", "[username-redacted]")
    git_email = _cfg.get("email", "[email-redacted]")
    run_git("config", "user.email", git_email, check=False)
    run_git("config", "user.name",  git_user,  check=False)

    # add
    run_git("add", f"skills/{skill_name}/")
    run_git("add", "README.md", check=False)

    # commit
    r = run_git("diff", "--cached", "--quiet", check=False)
    if r.returncode == 0:
        log(6, 8, "没有变更需要提交", "skip")
        return False, False

    msg = f"feat: sync {skill_name} v{version}"
    run_git("commit", "-m", msg)
    log(6, 8, f"已提交: {msg}", "ok")

    # 自动检测远程名
    remote_gitee  = _detect_remote("gitee.com")
    remote_github = _detect_remote("github.com")

    # push to Gitee（不再提前 pull，避免远程旧版本覆盖本地修改）
    gitee_ok = False
    if remote_gitee:
        log(6, 8, f"推送到码云 (remote: {remote_gitee})...", "info")
        ok, err = _push_with_cred_url(remote_gitee, "main")
        # push 失败时：pull --rebase 再重试一次
        if not ok:
            log(6, 8, f"首次推送失败，尝试 pull --rebase 后重试：{err}", "warn")
            _pull_with_cred_url(remote_gitee, "main")
            ok, err = _push_with_cred_url(remote_gitee, "main")
        if ok:
            log(6, 8, "码云推送成功", "ok")
            gitee_ok = True
        else:
            log(6, 8, f"码云推送失败: {err}", "err")
    else:
        log(6, 8, "未找到码云远程，跳过", "warn")

    # push to GitHub（不再提前 pull，避免远程旧版本覆盖本地修改）
    github_ok = False
    if remote_github:
        log(6, 8, f"推送到 GitHub (remote: {remote_github})...", "info")
        ok, err = _push_with_cred_url(remote_github, "main")
        # push 失败时：pull --rebase 再重试一次
        if not ok:
            log(6, 8, f"首次推送失败，尝试 pull --rebase 后重试：{err}", "warn")
            _pull_with_cred_url(remote_github, "main")
            ok, err = _push_with_cred_url(remote_github, "main")
        if ok:
            log(6, 8, "GitHub 推送成功", "ok")
            github_ok = True
        else:
            log(6, 8, f"GitHub 推送失败: {err}", "err")
    else:
        log(6, 8, "未找到 GitHub 远程，跳过", "warn")

    return gitee_ok, github_ok

# ── 步骤 6.7：更新清单中的上传状态 ──────────────────────────────────────
def step_update_manifest_uploaded(skill_name: str, version: str,
                                  gitee_ok: bool, github_ok: bool,
                                  repo_name="workbuddy-skills"):
    manifest_py = SCRIPT_DIR / "manifest.py"
    if not manifest_py.exists():
        return
    if gitee_ok:
        run_python(manifest_py, "version", repo_name, skill_name, version,
                   "--platform", "gitee")
        run_python(manifest_py, "set-uploaded", repo_name, skill_name,
                   "--platform", "gitee")
        log("6.7", 8, f"清单已更新 [码云]: {skill_name} → {version}", "ok")
    else:
        log("6.7", 8, "码云推送失败，保持 not-uploaded (gitee)", "warn")
    if github_ok:
        run_python(manifest_py, "version", repo_name, skill_name, version,
                   "--platform", "github")
        run_python(manifest_py, "set-uploaded", repo_name, skill_name,
                   "--platform", "github")
        log("6.7", 8, f"清单已更新 [GitHub]: {skill_name} → {version}", "ok")
    else:
        log("6.7", 8, "GitHub 推送失败，保持 not-uploaded (github)", "warn")

# ── 步骤 7：生成 ZIP 安装包 ───────────────────────────────────────────────
def step_pack_zip(skill_name: str, version: str, skills_dir: Path,
                   skip_scan: bool = False):
    log(7, 8, "生成 ZIP 安装包...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    # 防止 version 本身已带 v 前缀导致双 v
    safe_ver = version[1:] if version.startswith("v") else version
    zip_name = f"{skill_name}-v{safe_ver}.zip"
    zip_file = DIST_DIR / zip_name

    # 打包前敏感扫描
    log("7.5", 8, "打包前敏感信息扫描...")
    zip_source = skills_dir / skill_name
    if not skip_scan:
        scan_py = SCRIPT_DIR / "sensitive_scan.py"
        if scan_py.exists():
            scan_out_zip = SCRIPT_DIR / f".sensitive_scan_{skill_name}_zip.json"
            run_python(scan_py, "scan", str(zip_source),
                       "--output", str(scan_out_zip))
            if scan_out_zip.exists() and scan_out_zip.stat().st_size > 0:
                log("7.5", 8, "发现敏感信息，将在副本中脱敏...", "warn")
                tmp_dir = Path(tempfile.gettempdir()) / f".tmp_zip_{os.getpid()}"
                if tmp_dir.exists(): shutil.rmtree(tmp_dir)
                tmp_dir.mkdir(parents=True)
                dst_tmp = tmp_dir / skill_name
                # 逐个复制（跳过 nul 等 Windows 保留设备名）
                os.makedirs(dst_tmp, exist_ok=True)
                for item in zip_source.rglob("*"):
                    if item.name.lower() in ("nul", "nul "):
                        continue
                    if item.is_file():
                        try:
                            rel = item.relative_to(zip_source)
                            dst_item = dst_tmp / rel
                            dst_item.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, dst_item)
                        except (OSError, shutil.Error):
                            pass
                # 脱敏
                decisions_zip = scan_out_zip.with_suffix(".json.decisions.json")
                make_py = SCRIPT_DIR / "make_all_sanitize.py"
                if make_py.exists():
                    r = run_python(make_py, str(scan_out_zip), capture=True)
                    if r and r.stdout:
                        Path(decisions_zip).write_text(r.stdout, encoding="utf-8")
                if decisions_zip.exists():
                    run_python(scan_py, "apply", str(dst_tmp),
                               "--decisions", str(decisions_zip),
                               "--scan-result", str(scan_out_zip))
                zip_source = dst_tmp
                scan_out_zip.unlink(missing_ok=True)
                decisions_zip.unlink(missing_ok=True)
            else:
                scan_out_zip.unlink(missing_ok=True)
                log("7.5", 8, "未发现敏感信息", "ok")
        else:
            log("7.5", 8, "sensitive_scan.py 不存在，跳过", "skip")
    else:
        log("7.5", 8, "已跳过（--skip-scan）", "skip")

    # 清理 ZIP 源目录中的临时文件
    clean_py = SCRIPT_DIR / "clean_zip_source.py"
    if clean_py.exists():
        run_python(clean_py, str(zip_source), check=False)

    # 调用 pack_zip.py 打包
    pack_py = SCRIPT_DIR / "pack_zip.py"
    if pack_py.exists():
        run_python(pack_py, str(zip_source), str(zip_file))
    else:
        # 内置打包逻辑
        import zipfile
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in zip_source.rglob("*"):
                if f.is_file():
                    arcname = f.relative_to(zip_source.parent)
                    zf.write(f, arcname)
    log(7, 8, f"ZIP 已生成: {zip_file}", "ok")

    # 清理旧包：每个技能保留最近 5 个版本
    try:
        import re as _re
        from collections import defaultdict as _dd
        _skill_zips = _dd(list)
        for _f in DIST_DIR.iterdir():
            if _f.name == 'index.html':
                continue
            _m = _re.match(r'^(.+)-v?(\d+\.\d+\.\d+)\.zip$', _f.name)
            if _m and _m.group(1) == skill_name:
                _ver = tuple(int(x) for x in _m.group(2).split('.'))
                _skill_zips[skill_name].append((_ver, _f))
        for _name, _versions in _skill_zips.items():
            _versions.sort(key=lambda x: x[0], reverse=True)
            if len(_versions) > 5:
                for _v in _versions[5:]:
                    _v[1].unlink(missing_ok=True)
                    log(7, 8, f"  清理旧包: {_v[1].name}")
    except Exception:
        pass  # 清理失败不阻断主流程

    # 清理临时目录（仅在定义了 tmp_dir 时）
    if 'tmp_dir' in locals() and tmp_dir.exists():
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return zip_file

# ── 步骤 8：刷新 index.html ────────────────────────────────────────────────
def step_build_index():
    log(8, 8, "刷新 .dist/index.html...")
    build_py = SCRIPT_DIR / "build_index.py"
    if not build_py.exists():
        log(8, 8, "build_index.py 不存在，跳过", "skip")
        return
    run_python(build_py, str(DIST_DIR))
    log(8, 8, "index.html 已刷新", "ok")

# ── 辅助：读取 description ───────────────────────────────────────────────────
def get_meta_desc(meta_file: Path) -> str:
    get_desc_py = SCRIPT_DIR / "get_meta_desc.py"
    if get_desc_py.exists():
        r = run_python(get_desc_py, str(meta_file), capture=True)
        return r.stdout.strip()
    return ""

# ── 主流程 ────────────────────────────────────────────────────────────────────
def main():
    # ── 0. 彻底阻止 CredentialHelperSelector 弹窗 ──────────────────────
    # 方案：在最早时机固化 credential.helper 配置，所有后续 git 命令直接继承
    # 同时用 GIT_CREDENTIAL_HELPER 环境变量双重保险
    import subprocess as _sp

    _env = os.environ.copy()
    _env["GIT_TERMINAL_PROMPT"] = "0"
    # 写入 repo 级配置（最高优先级，覆盖全局）
    _sp.run(
        ["git", "config", "credential.helper", "store"],
        cwd=str(WORK_REPO), capture_output=True, check=False, env=_env
    )
    # 写入全局配置（防止 repo 级失败）
    _sp.run(
        ["git", "config", "--global", "credential.helper", "store"],
        capture_output=True, check=False, env=_env
    )
    # 确保 .git-credentials 文件存在（避免 store helper 报错）
    _cred = Path.home() / ".git-credentials"
    if not _cred.exists():
        try:
            _cred.write_text("", encoding="utf-8")
        except Exception:
            pass
    # ────────────────────────────────────────────────────────────────────────

    parser = argparse.ArgumentParser(description="git-sync.py v2.12.0")
    parser.add_argument("skill_name", nargs="?", default="",
                        help="技能名称（如 skill-standardization）")
    parser.add_argument("--skip-scan", action="store_true",
                        help="跳过敏感信息扫描")
    args = parser.parse_args()

    skill_name = args.skill_name
    skip_scan  = args.skip_scan

    if not skill_name:
        print(f"用法: python {sys.argv[0]} <skill-name> [--skip-scan]")
        sys.exit(1)

    # 强制从 _meta.json 读取版本号，禁止 LLM 手动传参
    meta_file = SKILLS_DIR / skill_name / "_meta.json"
    version = ""
    if meta_file.exists():
        try:
            version = json.load(open(meta_file, encoding="utf-8"))["version"]
        except Exception:
            pass
    if not version:
        print("❌ 无法从 _meta.json 读取版本号，拒绝同步")
        sys.exit(1)

    # 静默执行各步骤，收集日志
    global QUIET_MODE
    QUIET_MODE = True
    import contextlib
    with open(os.devnull, 'w', encoding='utf-8') as _null:
        with contextlib.redirect_stdout(_null), contextlib.redirect_stderr(_null):
            step_manifest(skill_name, version)
            compare_result = step_version_compare(skill_name, version)
            step_normalize_meta(meta_file, skill_name, version)

            # 步骤 4：同步文件（版本相同时跳过）
            skipped_sync = (compare_result == "skip_sync")
            if skipped_sync:
                log(4, 8, "跳过文件同步（版本相同）", "skip")
                repo_skill_dir = WORK_REPO / "skills" / skill_name
            else:
                log(4, 8, "同步文件到工作仓库...")
                repo_skill_dir = sync_files(skill_name, SKILLS_DIR, WORK_REPO)

            desensitized_files = step_sensitive_scan(skill_name, repo_skill_dir, skip_scan)
            step_update_readme()

            gitee_ok, github_ok = step_commit_and_push(skill_name, version)
            step_update_manifest_uploaded(skill_name, version, gitee_ok, github_ok)

            # 审计放在 manifest 更新之后
            audit_result = step_skill_audit(
                skill_name, SKILLS_DIR, MANIFEST_FILE,
                desensitized_files=desensitized_files,
                repo_skill_dir=repo_skill_dir
            )

            zip_file = step_pack_zip(skill_name, version, SKILLS_DIR, skip_scan)
            step_build_index()

    # ── 打印步骤日志 ─────────────────────────────────────────────────
    QUIET_MODE = False
    for line in LOG_BUFFER:
        print(line)

    # ── 固定格式输出报告 ─────────────────────────────────────────────
    print()
    print("=" * 60)
    print(f"  git-sync 执行报告：{skill_name} v{version}")
    print("=" * 60)

    # 表格 1：推送情况
    print()
    print(f"{'平台':<10} {'状态':<10} {'版本':<12}")
    print("-" * 32)
    gitee_ver = version if gitee_ok else "未推送"
    github_ver = version if github_ok else "未推送"
    # 跳过文件同步时，状态显示"⏭️ 跳过"而非"✅ 成功"
    if skipped_sync:
        gitee_status = "⏭️ 跳过"
        github_status = "⏭️ 跳过"
    else:
        gitee_status = "✅ 成功" if gitee_ok else "❌ 失败"
        github_status = "✅ 成功" if github_ok else "❌ 失败"
    print(f"{'码云':<10} {gitee_status:<10} {gitee_ver:<12}")
    print(f"{'GitHub':<10} {github_status:<10} {github_ver:<12}")

    # 审计报告
    print()
    print("─── 轻量审计报告 ──────────────────────────────────")
    if audit_result:
        a_errors = audit_result.get("summary", {}).get("errors", 0)
        a_warns  = audit_result.get("summary", {}).get("warns", 0)
        a_verdict = audit_result.get("verdict", "?")
        print(f"  审计结论：{a_verdict}（ERROR={a_errors}, WARN={a_warns}）")

        # 1. 版本一致性
        version_results = [r for r in audit_result.get("results", []) if r.get("rule_id") == "R-version"]
        if version_results:
            print("  ❌ 版本一致性：失败")
            for vr in version_results:
                print(f"     - {vr.get('detail', '')}")
        else:
            print("  ✅ 版本一致性：PASS")

        # 2. R-23 MD/PY 引用一致性
        r23_results = [r for r in audit_result.get("results", []) if r.get("rule_id") == "R-23"]
        if r23_results:
            print("  ❌ MD/PY 引用一致性（R-23）：失败")
            for r23 in r23_results[:5]:
                print(f"     - {r23.get('detail', '')}")
        else:
            print("  ✅ MD/PY 引用一致性（R-23）：PASS")

        # 3. 脱敏状态
        d_info = audit_result.get("desensitization", {})
        if d_info.get("sanitized"):
            files_str = ", ".join(list(d_info.get("sanitized_files", []))[:3])
            print(f"  ✅ 脱敏状态：已脱敏")
            if files_str:
                print(f"    涉及文件：{files_str}{'...' if len(list(d_info.get('sanitized_files', []))) > 3 else ''}")
        elif d_info.get("scanned"):
            print(f"  ⚠️  脱敏状态：未脱敏（发现 {d_info.get('findings_count', 0)} 处）")
        else:
            print(f"  ✅ 脱敏状态：未扫描（--skip-scan）")

        # 4. 文件筛选状态（三档）
        f_info = audit_result.get("filter", {})
        violations = f_info.get("violations", [])
        f_error = f_info.get("error", False) or f_info.get("status") == "error"
        if f_error:
            print(f"  ❌  文件筛选状态：检查失败")
        elif violations:
            print(f"  ⚠️  文件筛选状态：有 {len(violations)} 个不应打包的文件")
            for v in violations[:5]:
                print(f"     - {v}")
        else:
            print(f"  ✅ 文件筛选状态：干净（无多余文件）")
    else:
        print("  审计结论：未执行或执行失败")

    # ZIP 路径
    print()
    print(f"ZIP 包：{zip_file}")
    print(f"HTML 索引：{DIST_DIR / 'index.html'}")

    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
