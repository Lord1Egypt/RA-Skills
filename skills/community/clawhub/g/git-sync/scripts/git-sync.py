#!/usr/bin/env python3
"""
git-sync.py v2.32.0 - 完整 Python 版 git-sync
跨平台兼容（Windows/Linux/macOS），不依赖 rsync
用法: python git-sync.py <skill-name>
"""
import os
import sys
import json
import re
import shutil
import subprocess
import argparse
import builtins
import textwrap

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR, SKILLS_ROOT as SKILLS_DIR,
    WORK_REPO, DIST_DIR, MANIFEST_FILE, README_FILE, GIT_CREDENTIALS,
    SCAN_OUT_PREFIX, CONFIG_FILE,
    TEMP_DIR,
    temp_scan_path, temp_scan_decisions_path,
    temp_filter_scan_path, temp_filter_decisions_path,
    resume_state_path,
    get_work_repo, get_repo_config, get_repo_name,
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

# ZIP 打包排除模式（仅保留 Windows 保留设备名，其余由 LLM 动态判断）
EXCLUDE_PATTERNS = [
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

# ── LLM 决策让位状态管理（v2.43.0 让位式握手）──────────────────────────────
# 设计：skill-standardization 的 sys.exit(2) 让位模式。
# git-sync 遇到 LLM 决策点时不再进程内轮询占用控制权（旧版会卡死），
# 而是写 resume 状态文件 + sys.exit(3) 让位，把控制权交还调用方（AI 助手）。
# 调用方写决策文件后重跑 `python git-sync.py <name>`，main() 检测 resume
# 状态跳过已完成步骤，从当前环节继续（断点续跑）。
EXIT_DECISION_WAIT = 3   # 让位退出码：等待 LLM 决策文件

def _save_resume(name: str, phase: str, **extra) -> Path:
    """记录让位前卡在哪个环节 + 恢复上下文。返回状态文件路径。"""
    import time as _t
    state = {"name": name, "phase": phase, "ts": _t.strftime("%Y-%m-%d %H:%M:%S")}
    state.update(extra)
    p = resume_state_path(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def _load_resume(name: str):
    """读取 resume 状态；不存在或损坏返回 None。"""
    p = resume_state_path(name)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

def _clear_resume(name: str):
    """决策消费成功后清理 resume 状态。"""
    p = resume_state_path(name)
    p.unlink(missing_ok=True)

# ── 步骤 1：检查维护清单 ─────────────────────────────────────────────────────
def step_manifest(skill_name: str, version: str, repo_name=None):
    log(1, 8, "检查维护清单...")
    if repo_name is None:
        repo_name = get_repo_name("skill")  # v2.37.0 动态仓库名
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
def step_version_compare(skill_name: str, local_ver: str, work_repo_subdir: str = "skills/unknown") -> str:
    log(2, 8, "版本号对比（仓库 vs 本地源文件）...")
    # 先查 _meta.json（skill），再查 __init__.py（agent）
    repo_meta = WORK_REPO / work_repo_subdir / "_meta.json"
    repo_ver = ""
    if repo_meta.exists():
        try: repo_ver = json.load(open(repo_meta, encoding="utf-8"))["version"]
        except: pass
    else:
        # agent：找 work_repo 下任意 __init__.py 中含 __version__ 的
        import re
        repo_dir = WORK_REPO / work_repo_subdir
        for init_f in sorted(repo_dir.rglob("__init__.py")):
            if init_f.parent == repo_dir:
                continue
            try:
                txt = init_f.read_text(encoding="utf-8")
                m = re.search(r'__version__\s*=\s*"([^"]+)"', txt)
                if m:
                    repo_ver = m.group(1)
                    break
            except Exception:
                continue
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
    # 简单版本比较（支持 -beta、-rc 等预发布后缀）
    def _parse_version(v):
        """解析版本号为 (数字部分list, 预发布后缀)"""
        base = v.split("-")[0]
        parts = base.split(".")
        nums = []
        for p in parts:
            digit = ""
            for ch in p:
                if ch.isdigit():
                    digit += ch
                else:
                    break
            nums.append(int(digit) if digit else 0)
        # 提取预发布后缀：去掉数字部分后剩下的部分
        suffix = ""
        for p in parts:
            digit_end = 0
            for ch in p:
                if ch.isdigit():
                    digit_end += 1
                else:
                    break
            suffix += p[digit_end:] if digit_end < len(p) else ""
        suffix += v[len(base):] if len(v) > len(base) else ""  # -beta 部分
        return nums, suffix

    def ver_lt(a, b):
        an, asfx = _parse_version(a)
        bn, bsfx = _parse_version(b)
        if an != bn:
            return an < bn
        # 数字部分相同 → 有后缀 < 无后缀（beta < release）
        if asfx and not bsfx:
            return True
        if not asfx and bsfx:
            return False
        return asfx < bsfx
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
        # v2.37.0 多仓库：遍历所有仓库查找项目
        for _repo_name, _repo_data in mf.get("repos", {}).items():
            _items = _repo_data.get("items", {})
            if skill_name in _items:
                manifest_ver = _items[skill_name].get("version", "")
                break
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

def sync_files(skill_name: str, skills_dir: Path, work_repo: Path,
               allowed_files: set = None, subdir: str = None):
    """用 Python 逐个复制文件。只复制 allowed_files 集合中的文件（全部保留时传 None）

    v2.45.0 修复：目标子目录不再硬编码 'skills/' 前缀。
    仓库结构由 manifest/config 的 repo_path 决定（顶层或 skills/ 子目录），
    调用方通过 subdir 传入；不传时回退到顶层（技能名在仓库根）。
    """
    src = skills_dir / skill_name
    dst = work_repo / (subdir or skill_name)
    # v2.47.0 同步保险丝（P0-1）：allow 集合与源树零交集 -> 拒绝清空目标目录。
    # 此前 allow 决策异常（空 allow）时 rmtree 照常执行，工作仓被整目录删除
    # 并推送到双平台（2026-10-02 structured-writer 3.1.10 事故根因）。
    if allowed_files is not None:
        src_files = {str(p.relative_to(src)).replace("\\", "/")
                     for p in src.rglob("*") if p.is_file()}
        matched = src_files & set(allowed_files)
        if not matched:
            log(4, 8, f"保险丝触发：allow 集合（{len(allowed_files)} 项）与源树"
                      f"（{len(src_files)} 个文件）零交集，拒绝清空 {dst}，"
                      f"请检查文件过滤决策", "err")
            raise SystemExit(2)
    if dst.exists():
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    file_count = 0
    for item in src.rglob("*"):
        if item.name.lower() == "nul":
            continue
        if item.is_file():
            try:
                rel = item.relative_to(src)
                rel_str = str(rel).replace("\\", "/")
                # LLM 文件过滤：仅复制允许列表中的文件
                if allowed_files is not None and rel_str not in allowed_files:
                    continue
                dst_file = dst / rel
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_file)
                file_count += 1
            except (OSError, shutil.Error):
                pass
    # 二次保险：清理残留的 __pycache__
    for root, dirs, _ in os.walk(dst):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(Path(root) / d, ignore_errors=True)
    count = sum(1 for _ in dst.rglob("*") if _.is_file())
    log(4, 8, f"已同步 {count} 个文件到 {dst}", "ok")
    return dst

# ── 步骤 4.5：敏感信息扫描 ────────────────────────────────────────────────
def step_sensitive_scan(skill_name: str, repo_skill_dir: Path):
    """
    扫描并脱敏敏感信息。
    返回 desensitized_files: set（脱敏涉及的文件相对路径集合）
    """
    desensitized_files = set()
    log("4.5", 8, "扫描敏感信息...")
    scan_py = SCRIPT_DIR / "sensitive_scan.py"
    if not scan_py.exists():
        log("4.5", 8, "sensitive_scan.py 不存在，跳过", "skip")
        return desensitized_files

    scan_out = temp_scan_path(skill_name)
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
            match = str(f.get("match", ""))
            if len(match) > 40:
                match = match[:40] + "…"
            print(f"      [{severity}] 第 {line} 行 {label} 原文：{match!r} → 替换为：{replace}")
        if len(finds) > 5:
            print(f"      ... 还有 {len(finds) - 5} 处未显示")

    # ── 检查是否已有 LLM 决策 ─────────────────────────────────────────────
    decisions = temp_scan_decisions_path(skill_name)
    if decisions.exists():
        # v2.47.0 陈旧决策守卫（P0-2）：决策必须覆盖本次扫描发现的全部文件，
        # 值必须合法（keep/sanitize/custom）。不满足 = 陈旧/损坏决策 -> 清除后
        # 重新让位，绝不静默应用。此前 apply 遍历 decisions 而非 findings，
        # 扫描新增的敏感文件会被静默放过直接上公共仓。
        try:
            dec_data = json.load(decisions.open(encoding="utf-8"))
        except Exception:
            dec_data = None
        finding_files = {e["file"] for e in d}
        dec_keys = set()
        dec_vals_ok = True
        if isinstance(dec_data, dict):
            for k, v in dec_data.items():
                if str(k).startswith("__"):
                    continue
                dec_keys.add(k)
                if not (v in ("keep", "sanitize")
                        or (isinstance(v, dict) and v.get("mode"))):
                    dec_vals_ok = False
        else:
            dec_vals_ok = False
        stale = (not isinstance(dec_data, dict) or not dec_vals_ok
                 or bool(finding_files - dec_keys))
        if stale:
            log("4.5", 8, "决策文件与本次扫描不匹配（陈旧/损坏/覆盖不全），已清除并重新让位", "err")
            for m in sorted(finding_files - dec_keys)[:5]:
                print(f"      缺决策: {m}")
            decisions.unlink(missing_ok=True)
        else:
            log("4.5", 8, "发现 LLM 决策文件，执行脱敏...", "info")
            desensitized_files = set()
            for e in d:
                desensitized_files.add(repo_skill_dir / e["file"])
            run_python(scan_py, "apply", str(repo_skill_dir),
                       "--decisions", str(decisions),
                       "--scan-result", str(scan_out))
            print(f"  ✅ 决策已执行，涉及 {len(desensitized_files)} 个文件")
            scan_out.unlink(missing_ok=True)
            decisions.unlink(missing_ok=True)
            _clear_resume(skill_name)
            return desensitized_files

    # ── 无决策文件 → 打印发现 + 引导 → 等 LLM 写 decision → 自动继续 ──
    print(f"\n{'='*60}")
    print(f"  ⏳ 等待 LLM 完成敏感信息脱敏决策")
    print(f"{'='*60}")
    print(f"项目: {skill_name}")
    print(f"目标路径: {repo_skill_dir}")
    print(f"发现敏感信息：共 {len(d)} 个文件，{total_findings} 处")
    print()
    print("## 敏感信息发现详情")
    for e in d:
        file_rel = e["file"]
        finds = e.get("findings", [])
        if not finds:
            continue
        print(f"  📄 {file_rel}（{len(finds)} 处）")
        for f in finds[:5]:
            label = f.get("label", "敏感信息")
            severity = f.get("severity", "")
            line = f.get("line", "?")
            replace = f.get("replace", "[redacted]")
            match = str(f.get("match", ""))
            if len(match) > 40:
                match = match[:40] + "…"
            print(f"      [{severity}] 第 {line} 行 {label} 原文：{match!r} → 替换为：{replace}")
        if len(finds) > 5:
            print(f"      ... 还有 {len(finds) - 5} 处未显示")
    print()
    print("#" * 60)
    print("## 脱敏决策引导")
    print("逐文件判断是否应脱敏。以下类型建议脱敏：")
    print("- 个人邮箱、手机号、身份证号")
    print("- API Token、密钥、密码")
    print("- 内网 IP、本地绝对路径（含用户名）")
    print("- 私钥内容（PEM 格式）")
    print()
    print("以下情况可保留（keep）：")
    print("- 公开署名（如 LICENSE/README 中的 wUwproject）")
    print("- 开源项目的公开联系邮箱")
    print("- 文档中的示例路径或占位信息")
    print()
    print("## 写入决策文件")
    print(f"决策文件路径: {decisions}")
    print('JSON 格式：{"相对路径": "keep"|"sanitize"}')
    print('示例：{"README.md": "keep", "config.json": "sanitize"}')
    print('⚠️  Write 工具可能写文件不落地，建议用 Bash: echo \'{"README.md":"keep"}\' > file')
    print()
    # 生成辅助决策脚本
    helper_script = TEMP_DIR / f"write_sensitive_decision_{skill_name}.py"
    helper_content = (
        f'"""\ngit-sync 敏感扫描决策写入器\n'
        f'扫描文件：{json.dumps(str(scan_out))}\n'
        f'决策输出：{json.dumps(str(decisions))}\n'
        f'"""\n'
        f'import json, sys\n'
        f'# 直接读扫描文件，避免把 JSON 嵌入源码（Windows 路径 \\U 转义爆炸）\n'
        f'scan = json.load(open({json.dumps(str(scan_out))}, encoding="utf-8"))\n'
        f'keep_list = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []\n'
        f'decisions = {{e["file"]: ("keep" if e["file"] in keep_list else "sanitize") for e in scan}}\n'
        f'with open({json.dumps(str(decisions))}, "w", encoding="utf-8") as f:\n'
        f'    json.dump(decisions, f, indent=2, ensure_ascii=False)\n'
        f'ok = sum(1 for v in decisions.values() if v == "keep")\n'
        f'san = sum(1 for v in decisions.values() if v == "sanitize")\n'
        f'print(f"决策已写入 ({{ok}} 保留 / {{san}} 脱敏)")'
    )
    helper_script.parent.mkdir(parents=True, exist_ok=True)
    helper_script.write_text(helper_content, encoding="utf-8")
    print(f"辅助脚本已生成：")
    print(f"  # 全部脱敏（默认）：")
    print(f"  python {helper_script}")
    print(f"  # 保留指定文件，其余脱敏：")
    print(f"  python {helper_script} '[\"README.md\"]'")
    print(f"  # 保留多个文件：")
    print(f"  python {helper_script} '[\"README.md\",\"LICENSE\"]'")
    print(f"等待决策文件写入后自动继续...")
    print("#" * 60)

    # ── 让位式握手（v2.43.0）：不再进程内轮询，写 resume + 退出让权 ──
    # 旧版在此 while 轮询 120s 占用控制权，AI 助手无法并行写决策文件 → 卡死。
    # 现在保存断点状态后立即退出（exit 3），调用方写决策文件后重跑续跑。
    # 重跑时决策文件已存在 → 走函数开头 if decisions.exists() 分支执行脱敏。
    print(f"  ⏸️  已让位（exit {EXIT_DECISION_WAIT}）：请写入决策文件后重跑")
    print(f"      python {sys.argv[0]} {skill_name}")
    print(f"      将从脱敏环节继续，不会从头开始。")
    _save_resume(skill_name, "sensitive_scan",
                 repo_skill_dir=str(repo_skill_dir))
    sys.exit(EXIT_DECISION_WAIT)

# ── 步骤 5：更新 README.md ─────────────────────────────────────────────────
def step_update_readme(repo_name=None, work_repo=None):
    log(5, 8, "更新 README.md...")
    if repo_name is None:
        repo_name = get_repo_name("skill")  # v2.37.0 动态仓库名
    if work_repo is None:
        work_repo = WORK_REPO
    readme = Path(work_repo) / "README.md"
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

def step_commit_and_push(skill_name: str, version: str, work_repo_subdir: str = "skills/unknown"):
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
    run_git("add", f"{work_repo_subdir}/")
    run_git("add", "README.md", check=False)

    # commit
    r = run_git("diff", "--cached", "--quiet", check=False)
    if r.returncode == 0:
        log(6, 8, "没有变更需要提交（远端已与本地一致，按成功处理）", "skip")
        return True, True

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
                                  repo_name=None):
    if repo_name is None:
        repo_name = get_repo_name("skill")  # v2.37.0 动态仓库名
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
def step_pack_zip(skill_name: str, version: str, skills_dir: Path):
    log(7, 8, "生成 ZIP 安装包...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    # 防止 version 本身已带 v 前缀导致双 v
    safe_ver = version[1:] if version.startswith("v") else version
    zip_name = f"{skill_name}-v{safe_ver}.zip"
    zip_file = DIST_DIR / zip_name

    # 打包前敏感扫描（强制，不可跳过）
    log("7.5", 8, "打包前敏感信息扫描（强制）...")
    zip_source = skills_dir / skill_name
    scan_py = SCRIPT_DIR / "sensitive_scan.py"
    if scan_py.exists():
        scan_out_zip = temp_scan_path(f"{skill_name}_zip")
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
            decisions_zip = temp_scan_decisions_path(f"{skill_name}_zip")
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

# ── 文件筛除过滤器 ──────────────────────────────
# 由执行者（LLM/Agent）审核源文件列表后写入 decision JSON。
# 无 decision 文件时打印文件列表并阻断，不静默跳过。

def step_llm_file_filter(name: str, src_dir: Path) -> set:
    """扫描源文件 → 写扫描文件 → 打印审查指令 → 等待 WorkBuddy 写入决策文件"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    filter_scan = temp_filter_scan_path(name)
    filter_decisions = temp_filter_decisions_path(name)

    # 收集源文件树
    tree = []
    for f in sorted(src_dir.rglob("*")):
        if f.is_file() and f.name.lower() not in ("nul", "nul "):
            rel = str(f.relative_to(src_dir)).replace("\\", "/")
            size = f.stat().st_size
            tree.append({"path": rel, "size": size})

    # Python 扫描：找规则文件 + 汇总文件树
    rules_content = ""
    for pattern in ["**/blueprint*", "**/*rules*", "**/blueprints/*"]:
        for rf in sorted(src_dir.glob(pattern)):
            if rf.is_file() and rf.suffix in (".md", ".txt", ".yaml", ".yml", ".json"):
                try:
                    text = rf.read_text(encoding="utf-8")[:2000]
                    rel = str(rf.relative_to(src_dir)).replace("\\", "/")
                    rules_content += f"\n--- {rel} ---\n{text}\n"
                except: pass

    report = {
        "project": name,
        "root": str(src_dir),
        "total_files": len(tree),
        "files": tree,
        "project_rules": rules_content[:3000],
        "guidelines": (
            "请审查以上文件列表，结合 project_rules（项目自身规则文件）和以下通用规则，\n"
            "判断哪些文件应该一起发布到公开的代码仓库。\n\n"
            f"项目类型：{'API Skill' if 'slug' in str(src_dir) else 'AI Agent'}\n\n"
            "通用排除参考：\n"
            "- 缓存目录（__pycache__/, .cache/, .mypy_cache/, .pytest_cache/）\n"
            "- 构建产物（dist/, build/, .egg-info/, *.pyc, *.pyo）\n"
            "- 依赖目录（node_modules/, .venv/, .tox/）\n"
            "- 大体积模型权重/data（*.pt, *.pth, *.gguf, data/models/, data/kb/, *.db, *.sqlite）\n"
            "- 个人配置/凭证（config.json, .env, *.token, credentials*）\n"
            "- IDE/系统文件（.vscode/, .idea/, .DS_Store, Thumbs.db）\n"
            "- 日志/临时文件（*.log, *.tmp, *.bak）\n"
            "- .git/ 排除，.gitignore 可保留\n\n"
            "确认以下核心文件被保留：\n"
            "- 所有 .py 代码文件\n"
            "- 文档（README.md, SKILL.md, references/ 下的文档）\n"
            "- 配置文件（_meta.json, requirements.txt, setup.py）\n"
            "- 许可证（LICENSE）\n\n"
            "请以 JSON 返回应保留的文件路径列表：\n"
            "{\"allow\": [\"path/to/file1.py\", \"path/to/file2.py\"]}"
        )
    }
    filter_scan.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if filter_decisions.exists():
        try:
            decisions = json.loads(filter_decisions.read_text(encoding="utf-8"))
            allowed = set(decisions.get("allow", []))
            cnt = len(allowed)
            log("3.7", 8, f"LLM 文件过滤器：{cnt}/{len(tree)} 个文件通过", "ok")
            filter_scan.unlink(missing_ok=True)
            filter_decisions.unlink(missing_ok=True)
            _clear_resume(name)
            return allowed
        except Exception as e:
            log("3.7", 8, f"LLM 决策解析失败: {e}，默认保留所有文件", "warn")
            filter_scan.unlink(missing_ok=True)
            filter_decisions.unlink(missing_ok=True)
            return set(rel for d in tree for rel in [d["path"]])
    else:
        # ── 无决策文件 → 打印文件列表 + 引导 → 等 LLM 写 decision → 自动继续 ──
        print(f"\n{'='*60}")
        print(f"  ⏳ 等待 LLM 完成文件筛除审核")
        print(f"{'='*60}")
        print(f"项目: {name}")
        print(f"源路径: {src_dir}")
        print(f"文件总数: {len(tree)}")
        print()
        print("## 项目规则")
        print(rules_content[:2000] if rules_content else "（无）")
        print()
        print("## 文件列表")
        for e in tree:
            print(f"  {e['path']} ({e['size']}B)")
        print()
        print("#" * 60)
        print("## 文件筛除引导")
        print("- 缓存目录: __pycache__/, .cache/, .mypy_cache/, .pytest_cache/")
        print("- 构建产物: dist/, build/, .egg-info/, *.pyc, *.pyo")
        print("- 依赖目录: node_modules/, .venv/, .tox/")
        print("- 大体积数据: *.pt, *.pth, *.gguf, data/models/, data/kb/, *.db, *.sqlite")
        print("- 个人配置: config.json, .env, *.token, credentials*")
        print("- IDE/系统: .vscode/, .idea/, .DS_Store, Thumbs.db")
        print("- 日志/临时: *.log, *.tmp, *.bak")
        print()
        print("## 写入决策文件")
        print(f"请运行以下命令来写入决策文件：")
        helper_script = TEMP_DIR / f"write_filter_decision_{name}.py"
        helper_content = (
            f'"""\ngit-sync 文件筛除决策写入器\n'
            f'扫描文件：{json.dumps(str(filter_scan))}\n'
            f'决策输出：{json.dumps(str(filter_decisions))}\n'
            f'"""\n'
            f'import json, sys\n'
            f'# 直接读扫描文件，避免把 JSON 嵌入源码（Windows 路径 \\U 转义爆炸）\n'
            f'scan = json.load(open({json.dumps(str(filter_scan))}, encoding="utf-8"))\n'
            f'exclude = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []\n'
            f'allow = [e["path"] for e in scan["files"] if e["path"] not in exclude]\n'
            f'decisions = {{"allow": allow, "exclude": exclude}}\n'
            f'with open({json.dumps(str(filter_decisions))}, "w", encoding="utf-8") as f:\n'
            f'    json.dump(decisions, f, indent=2, ensure_ascii=False)\n'
            f'print(f"决策已写入 ({{len(allow)}} 个文件，排除 {{len(exclude)}} 个)")'
        )
        helper_script.parent.mkdir(parents=True, exist_ok=True)
        helper_script.write_text(helper_content, encoding="utf-8")
        print(f"  python {helper_script} '[\"path/to/exclude1\",\"path/to/exclude2\"]'")
        print(f"  如果无需排除，传入空数组：")
        print(f"  python {helper_script} '[]'")
        print("#" * 60)
        print(f"决策文件路径: {filter_decisions}")
        print(f"写入格式: {{\"allow\": [\"path1\", \"path2\"], \"exclude\": [...]}}")
        print()
        # ── 让位式握手（v2.43.0）：不再进程内轮询，写 resume + 退出让权 ──
        # 旧版在此 while 轮询 120s 占用控制权，AI 助手无法并行写决策文件 → 卡死。
        # 现在保存断点状态后立即退出（exit 3），调用方写决策文件后重跑续跑。
        # 重跑时决策文件已存在 → 走函数开头 if filter_decisions.exists() 分支。
        print(f"  ⏸️  已让位（exit {EXIT_DECISION_WAIT}）：请写入决策文件后重跑")
        print(f"      python {sys.argv[0]} {name}")
        print(f"      将从文件筛除环节继续，不会从头开始。")
        _save_resume(name, "file_filter", src_dir=str(src_dir))
        sys.exit(EXIT_DECISION_WAIT)

# ── 新步骤：PyPI / ClawHub / SkillHub / Release ──────────────────────────

def _normalize_version(version: str) -> str:
    """将版本号转为 PEP 440 格式（统一用于所有外部输出）
    1.7.0       → 1.7.0
    1.7.0b1     → 1.7.0b1 (已是 PEP 440)
    1.7.0-beta  → 1.7.0b1

    2026-09-17 定稿：版本方案只有 x.y.z 与 x.y.zbn 两种，b 是唯一支持的
    预发布形式；rc/alpha/dev 已废弃，携带这类后缀的一律按非标准后缀剥除——
    剥完与正式版同号会在 PyPI 撞号报错，宁可撞号也不误发。
    """
    v = version.lower().strip()
    # 已是 PEP 440 的 b 后缀（x.y.zbn）→ 保持不变
    if re.search(r'\.\d+b\d+$', v):
        return version  # 原样返回（保持大小写等）
    # 已经是标准 semver x.y.z → 保持不变
    if re.search(r'^\d+\.\d+\.\d+$', v):
        return version
    # 连字符/下划线的 b 后缀转 PEP 440: x.y.z-beta → x.y.zb1
    m = re.search(r'[-_.]?b(?:eta)?(\d*)$', v)
    if m:
        num = m.group(1) or '1'
        return v[:m.start()] + 'b' + num
    # 其余后缀（含已废弃的 rc/alpha/dev，有无分隔符均算）→ 剥掉；
    # 连写形态（1.7.0alpha2）原样发上 PyPI 会被解析成预发布而错标状态，剥成
    # 正式版同号在 PyPI 撞号报错——宁可撞号也不误发。
    v = re.sub(r'[-_.]?[a-z]+\d*$', '', v).rstrip('.')
    return v


def _pypi_dev_status(pypi_ver: str) -> str:
    """开发状态（2026-09-17 定稿）：
    主版本号 <1 → Beta（0.x 即初始开发阶段，与后缀无关）；
    主版本号 ≥1 → 纯 x.y.z 为 Production/Stable，跟随 b（x.y.zbn）为 Beta。
    rc/alpha/dev 等形式已废弃，不参与判别。"""
    m = re.match(r'^(\d+)', pypi_ver.strip())
    major = int(m.group(1)) if m else 0
    is_beta = major < 1 or bool(re.search(r'\d+b\d+$', pypi_ver, re.I))
    return "4 - Beta" if is_beta else "5 - Production/Stable"


def step_pypi_publish(name: str, version: str, src_dir: Path):
    """发布到 PyPI（隔离构建，包含 pyproject.toml + long_description 修复）"""
    log(8, 8, f"发布 {name} 到 PyPI...")
    pypi_name = f"{name}-ldxs"
    # 标准化版本号为 PEP 440
    pypi_ver = _normalize_version(version)
    # 开发状态：x<1 → Beta；x≥1 纯 x.y.z → Stable、x.y.zbn → Beta（2026-09-17 定稿）
    dev_status = _pypi_dev_status(pypi_ver)
    build_dir = Path(tempfile.gettempdir()) / f"pypi_build_{name}_{version}"
    if build_dir.exists(): shutil.rmtree(build_dir)
    # Windows 保留设备名（nul/con/prn/aux）与常规缓存/版本库一并排除，避免 copytree 失败
    shutil.copytree(src_dir, build_dir,
                    ignore=shutil.ignore_patterns("__pycache__","*.pyc","dist","build","*.egg-info",
                                                  "nul","con","prn","aux","NUL","CON","PRN","AUX",
                                                  ".git",".gitignore"))
    from pathlib import Path as _P

    # 检测包目录名
    pkg_dir = None
    for d in [name.replace("-", "_"), name]:
        if (build_dir / d).is_dir() and (build_dir / d / "__init__.py").exists():
            pkg_dir = d; break
    if not pkg_dir:
        for d in build_dir.iterdir():
            if d.is_dir() and not d.name.startswith(".") and d.name not in ("scripts","references","data","__pycache__"):
                if (d / "__init__.py").exists(): pkg_dir = d.name; break
    if not pkg_dir:
        log(8, 8, "PyPI 构建：build 目录中找不到含 __init__.py 的包目录，"
                  "fail-closed 终止（v2.47.0 起不再回退硬编码 rag_assistant）", "err")
        shutil.rmtree(build_dir, ignore_errors=True)
        return

    # setup.py 模板中 {BS} 需要反斜杠变量（v2.45.1 修复：原实现漏定义 BS 导致 NameError）
    BS = chr(92)

    # 作者元数据：被发布项目自己的 pyproject [project].authors 优先（PEP 621，项目权威源），
    # 回退 config.json author/email（本地用户配置，与 git commit 同一字段，单一来源），
    # 再回退空串（PyPI 合法）。v2.47.0：删除原硬编码的作者名与邮箱——
    # 工具源码不得含个人信息，作者身份属于被发布项目而非发布工具。
    # 注意读 src_dir：build_dir 的 pyproject.toml 随后会被覆盖为 build-system-only。
    AUTHOR_STR, AUTHOR_EMAIL = "", ""
    try:
        import tomllib as _toml
        _pp = src_dir / "pyproject.toml"
        if _pp.exists():
            _auth = (_toml.loads(_pp.read_text(encoding="utf-8")).get("project", {}) or {}).get("authors") or []
            if _auth:
                AUTHOR_STR = (_auth[0] or {}).get("name", "") or ""
                AUTHOR_EMAIL = (_auth[0] or {}).get("email", "") or ""
    except Exception:
        pass
    if not AUTHOR_STR:
        try:
            _cfg_p = Path(__file__).resolve().parent.parent.parent / ".standardization" / "git-sync" / "data" / "config.json"
            _cfg = json.loads(_cfg_p.read_text(encoding="utf-8"))
            AUTHOR_STR = _cfg.get("author", "") or ""
            AUTHOR_EMAIL = _cfg.get("email", "") or ""
        except Exception:
            pass

    # pyproject.toml（防止 setuptools>=61 Dynamic description bug）
    _P(str(build_dir / "pyproject.toml")).write_text(textwrap.dedent(f"""\
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"
"""), encoding="utf-8")

    # setup.py（动态读取版本号 + long_description：README 粘合当前版本 CHANGELOG）
    _P(str(build_dir / "setup.py")).write_text(textwrap.dedent(f'''\
import os, re
from setuptools import setup
BS=chr(92)
init_p=os.path.join(os.path.dirname(__file__),"{pkg_dir}","__init__.py")
V="{pypi_ver}"
if os.path.exists(init_p):
    with open(init_p) as f:
        for l in f:
            if l.startswith("__version__"): V=l.split('"')[1]; break
req_p=os.path.join(os.path.dirname(__file__),"requirements.txt")
REQ=[]
if os.path.exists(req_p):
    with open(req_p) as f: REQ=[l.strip() for l in f if l.strip() and not l.startswith("#")]
    REQ=[r for r in REQ if not r.startswith("langchain")]
readme_p=os.path.join(os.path.dirname(__file__),"README.md")
LD="{name}"
if os.path.exists(readme_p):
    with open(readme_p,encoding="utf-8") as f: LD=f.read()
# 粘合当前版本的 CHANGELOG 区块到 long_description（更新说明）
changelog_p=os.path.join(os.path.dirname(__file__),"CHANGELOG.md")
if os.path.exists(changelog_p):
    with open(changelog_p,encoding="utf-8") as f: _cl=f.read()
    _esc=re.escape(V)
    _m=re.search(r"##{BS}s*\[?v?"+_esc+r"\]?[^{BS}n]*{BS}n.*?(?={BS}n##{BS}s|{BS}Z)",_cl,re.DOTALL)
    if _m:
        _vc=_m.group(0).strip()
        LD += "{BS}n{BS}n---{BS}n{BS}n## 更新说明{BS}n{BS}n" + _vc
setup(name="{pypi_name}",version=V,description="{name} — AI Agent",
      long_description=LD,long_description_content_type="text/markdown",
      author="{AUTHOR_STR}",author_email="{AUTHOR_EMAIL}",
      url="https://github.com/Ldxs001/maby_agent",
      project_urls={{"GitHub": "https://github.com/Ldxs001/maby_agent",
                     "Gitee": "https://gitee.com/wUwproject/maby_agent",
                     "Documentation": "https://github.com/Ldxs001/maby_agent#readme"}},
      packages=["{pkg_dir}"],include_package_data=True,
      python_requires=">=3.10",install_requires=REQ,
      entry_points={{"console_scripts":["{pypi_name}=main:main"]}},
      classifiers=["Development Status :: {dev_status}","Intended Audience :: Developers",
                   "License :: OSI Approved :: Apache Software License",
                   "Programming Language :: Python :: 3",
                   "Topic :: Scientific/Engineering :: Artificial Intelligence"])
'''), encoding="utf-8")
    # MANIFEST.in 补充 CHANGELOG.md（粘合内容需要它在源码包/构建环境中存在）
    _P(str(build_dir / "MANIFEST.in")).write_text(
        f"include requirements.txt\ninclude README.md\ninclude CHANGELOG.md\ninclude LICENSE\ninclude setup.py\ninclude main.py\n"
        f"graft {pkg_dir}/\nprune __pycache__\nprune *.pyc\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "build", "--wheel", "--no-isolation"],
                       cwd=str(build_dir), capture_output=True, text=True)
    if r.returncode != 0:
        log(8, 8, f"PyPI 构建失败: {r.stderr[:2000]}", "err")
        shutil.rmtree(build_dir, ignore_errors=True); return
    # 从 .pypirc 取 token
    token = ""
    pypirc = Path.home() / ".pypirc"
    if pypirc.exists():
        for line in pypirc.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("password"):
                token = line.split("=", 1)[1].strip()
                break
    if not token: token = os.environ.get("PYPI_TOKEN","")
    if not token:
        log(8,8,"未找到 PyPI token（.pypirc / PYPI_TOKEN）","err")
        shutil.rmtree(build_dir,ignore_errors=True); return
    # wheel 文件名以 dist 实际产物为准——setup.py 运行时会按 __init__.py 字面量
    # 覆盖版本号，与 pypi_ver（清单/提交用）可能不同，按固定名找会静默漏传
    dist = build_dir / "dist"
    whls = sorted(dist.glob("*.whl")) if dist.is_dir() else []
    if whls:
        r = subprocess.run([sys.executable,"-m","twine","upload","--disable-progress",str(whls[0]),"-u","__token__","-p",token],
                          capture_output=True,text=True,cwd=str(build_dir))
        if r.returncode==0: log(8,8,f"PyPI: https://pypi.org/project/{pypi_name}/ （{whls[0].name}）","ok")
        else: log(8,8,f"PyPI 上传失败: {(r.stdout+r.stderr)[-500:]}","err")
    else:
        log(8,8,"dist 下没有 wheel，跳过上传","err")
    shutil.rmtree(build_dir,ignore_errors=True)

def step_clawhub_publish(name: str, version: str):
    # v2.37.0 多仓库：skill 仓库根下直接是技能目录
    sd = get_work_repo("skill") / name
    if not sd.is_dir(): print("  ❌ 技能目录不存在"); return
    meta = json.loads((sd/"_meta.json").read_text(encoding="utf-8"))
    slug = meta.get("slug",name)
    cmd = f'npx clawhub publish "{sd}" --slug "{slug}" --name "{meta.get("displayName",name)}" --version "{version}" --changelog "v{version}"'
    if meta.get("tags"):
        cmd += ' --tags "' + ",".join(meta["tags"]) + '"'
    r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if r.returncode==0 or "ok" in r.stdout.lower(): print(f"  ✅ ClawHub: {slug}")
    else: print(f"  ⚠️  ClawHub: {(r.stdout+r.stderr)[-300:]}")

def step_skillhub_publish(name: str, version: str):
    # v2.37.0 多仓库：skill 仓库根下直接是技能目录
    sd = get_work_repo("skill") / name
    if not sd.is_dir(): print("  ❌ 技能目录不存在"); return
    cli = Path.home() / ".skillhub" / "skills_store_cli.py"
    if not cli.exists(): print("  ❌ SkillHub CLI 不存在"); return
    r = subprocess.run([sys.executable,str(cli),"publish",str(sd),"--version",version,"--changelog",f"v{version}"],
                      capture_output=True,text=True)
    if r.returncode==0: print(f"  ✅ SkillHub: {name} v{version}")
    else: print(f"  ⚠️  SkillHub: {(r.stdout+r.stderr)[-400:]}")

def step_release_create(name: str, typ: str, version: str):
    """创建 GitHub + Gitee Release，源码包由平台自动生成"""
    log(9,8,f"创建 Release: {name} v{version}...")

    # v2.37.0 多仓库：从 repos 配置按类型读取仓库名
    try:
        _cfg = json.load(open(CONFIG_FILE, encoding="utf-8"))
        _rc = _cfg.get("repos", {}).get("maby_skills" if typ=="skill" else "maby_agent", {})
        _g = _rc.get("gitee", {})
        _h = _rc.get("github", {})
        GITEE = f"{_g.get('user','wUwproject')}/{_g.get('repo','maby_skills')}"
        GITHUB = f"{_h.get('user','Ldxs001')}/{_h.get('repo','maby_skills')}"
    except:
        GITEE = "wUwproject/maby_skills"
        GITHUB = "Ldxs001/maby_skills"

    _rel_repo = get_work_repo(typ)
    tag = f"v{version}" if typ=="agent" else f"{name}-v{version}"
    subprocess.run(["git","tag",tag],cwd=str(_rel_repo),capture_output=True)
    # 推送 PyPI 触发 tag（GitHub Actions Trusted Publisher 用）
    pypi_tag = f"pypi/{typ}/{name}/{version}"
    subprocess.run(["git","tag",pypi_tag],cwd=str(_rel_repo),capture_output=True)
    for rm in ["gitee","origin"]:
        subprocess.run(["git","push",rm,tag],cwd=str(_rel_repo),capture_output=True,timeout=30)
        subprocess.run(["git","push",rm,pypi_tag],cwd=str(_rel_repo),capture_output=True,timeout=30)
    # GitHub token 三级来源：config.github_token → git credential fill（credential.helper，SSH 远端时唯一可用）→ origin HTTPS URL 内嵌
    token = ""
    try:
        token = json.load(open(CONFIG_FILE)).get("github_token", "") or ""
    except: pass
    if not token:
        try:
            cr = subprocess.run(["git","credential","fill"],
                                input="protocol=https\nhost=github.com\n\n",
                                capture_output=True,text=True,timeout=15)
            for ln in cr.stdout.splitlines():
                if ln.startswith("password="):
                    token = ln.split("=",1)[1].strip(); break
        except: pass
    if not token:
        rmt = subprocess.run(["git","remote","get-url","origin"],cwd=str(_rel_repo),
                             capture_output=True,text=True).stdout.strip()
        if ":" in rmt and "@" in rmt:
            tp = rmt.split("//")[1].split("@")[0]
            if ":" in tp: token = tp.split(":")[1]
    gitee_token = ""
    try:
        gitee_token = json.load(open(CONFIG_FILE)).get("gitee_token", "")
    except: pass

    # GitHub Release
    if token:
        b = json.dumps({"tag_name":tag,"name":f"{name} v{version}",
                        "body":f"## {name} v{version}\n\n由 git-sync 自动发布",
                        "draft":False,"prerelease":False})
        r = subprocess.run(["curl","-s","-X","POST",
                         f"https://api.github.com/repos/{GITHUB}/releases",
                         "-H",f"Authorization: token {token}","-H","Content-Type: application/json","-d",b],
                        capture_output=True,text=True)
        try:
            u = json.loads(r.stdout)
            if "id" in u:
                log(9,8,f"GitHub: {u.get('html_url','')}","ok")
            elif "already_exists" in r.stdout:
                log(9,8,f"GitHub Release 已存在（tag: {tag}）","info")
            else:
                log(9,8,f"GitHub Release 创建失败: {(r.stdout or r.stderr)[:200]}","err")
        except:
            log(9,8,f"GitHub Release 响应异常: {(r.stdout or r.stderr)[:200]}","err")
    else:
        log(9,8,f"GitHub Release 跳过：无可用 token（config.github_token / git credential / URL 内嵌均未命中），仅推送 tag: {tag}","err")

    # Gitee Release
    if gitee_token:
        b = json.dumps({"access_token":gitee_token,"tag_name":tag,
                        "target_commitish":"main","name":f"{name} v{version}",
                        "body":f"## {name} v{version}\n\n由 git-sync 自动发布",
                        "prerelease":False})
        r = subprocess.run(["curl","-s","-X","POST",
                         f"https://gitee.com/api/v5/repos/{GITEE}/releases",
                         "-H","Content-Type: application/json;charset=UTF-8","-d",b],
                        capture_output=True,text=True)
        try:
            u = json.loads(r.stdout)
            if "id" in u:
                log(9,8,f"Gitee: https://gitee.com/{GITEE}/releases/{tag}","ok")
            else:
                log(9,8,f"Gitee 发行版已存在或跳过","info")
        except:
            log(9,8,f"Gitee 发行版 tag 已推送","warn")

# ── 主流程 ────────────────────────────────────────────────────────────────────
def main():
    # v2.37.0 多仓库：按类型动态切换仓库路径（须在函数内首次使用前声明）
    global WORK_REPO, README_FILE
    global QUIET_MODE
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
    parser.add_argument("name", nargs="?", default="",
                        help="项目名称（自动检测 skill/agent）")
    parser.add_argument("--skip-market", action="store_true", help="跳过市场/PyPI 发布")
    parser.add_argument("--market-only", action="store_true", help="只发市场/PyPI，不发 git")
    parser.add_argument("--pypi", action="store_true", help="发布到 PyPI（仅 agent）")
    parser.add_argument("--release", action="store_true", help="创建 Release")
    args = parser.parse_args()

    name = args.name
    skip_market = args.skip_market
    market_only = args.market_only
    do_pypi = args.pypi
    do_release = args.release

    # ── all 模式 ──────────────────────────────────────────────
    if name == "all":
        for sd in sorted(SKILLS_DIR.iterdir()):
            if sd.is_dir() and (sd / "_meta.json").exists():
                subprocess.run([sys.executable, __file__, sd.name] + sys.argv[2:],
                              capture_output=not QUIET_MODE)
        for ad in sorted((get_work_repo("agent")).iterdir()):
            if ad.is_dir() and any(f.name == "__init__.py" and "__version__" in f.read_text(encoding="utf-8", errors="ignore") for f in ad.rglob("__init__.py")):
                subprocess.run([sys.executable, __file__, ad.name] + sys.argv[2:],
                              capture_output=not QUIET_MODE)
        return

    if not name:
        print(f"用法: python {sys.argv[0]} <name> [--skip-market] [--market-only] [--pypi] [--release]")
        print("       python {sys.argv[0]} all")
        sys.exit(1)

    # ── 类型检测（支持 config.source_overrides 覆盖源路径）──
    is_skill = False
    is_agent = False
    override_dir = None
    # ── 优先从 manifest 读取 source_path / repo_path ──────────
    manifest_found = False
    try:
        mf = json.load(open(MANIFEST_FILE, encoding="utf-8"))
        for repo_name, repo_data in mf.get("repos", {}).items():
            item = repo_data.get("items", {}).get(name)
            if item and isinstance(item, dict):
                mf_src = item.get("source_path", "")
                mf_repo = item.get("repo_path", "")
                if mf_src and Path(mf_src).is_dir():
                    src_dir = Path(mf_src)
                    # v2.37.0 多仓库：repo_path 为仓库根下相对路径（无 skills//agent/ 前缀）
                    work_repo_subdir = mf_repo or name
                    is_skill = (src_dir / "_meta.json").exists()
                    # agent 检测：找任意 __init__.py 中含 __version__ 的
                    is_agent = any(
                        f.name == "__init__.py" and "__version__" in f.read_text(encoding="utf-8", errors="ignore")
                        for f in src_dir.rglob("__init__.py") if f.parent != src_dir
                    ) if not is_skill else False
                    typ = "skill" if is_skill else ("agent" if is_agent else item.get("type", "unknown"))
                    manifest_found = True
                    break
    except Exception:
        pass

    # ── 无 manifest 映射 → source_overrides → 硬编码回退 ──
    if not manifest_found:
        try:
            cfg = json.load(open(CONFIG_FILE, encoding="utf-8"))
            overrides = cfg.get("source_overrides", {})
            if name in overrides:
                override_dir = Path(overrides[name])
                if override_dir.is_dir():
                    if (override_dir / "_meta.json").exists():
                        is_skill, typ, src_dir, work_repo_subdir = True, "skill", override_dir, name
                    elif any(
                        f.name == "__init__.py" and "__version__" in f.read_text(encoding="utf-8", errors="ignore")
                        for f in override_dir.rglob("__init__.py") if f.parent != override_dir
                    ):
                        # agent 通用识别（任意子目录 __init__.py 含 __version__；不再硬编码 rag_assistant）
                        is_agent, typ, src_dir, work_repo_subdir = True, "agent", override_dir, name
                    else:
                        print(f"❌ source_overrides 路径存在但无法识别类型: {override_dir}")
                        sys.exit(1)
        except Exception:
            pass

    if not manifest_found and not override_dir:
        skill_dir = SKILLS_DIR / name
        agent_dir = get_work_repo("agent") / name
        is_skill = (skill_dir / "_meta.json").exists()
        is_agent = any(
            f.name == "__init__.py" and "__version__" in f.read_text(encoding="utf-8", errors="ignore")
            for f in agent_dir.rglob("__init__.py")
        ) if agent_dir.is_dir() else False
        if is_skill:
            typ = "skill"
            src_dir = skill_dir
            work_repo_subdir = name
        elif is_agent:
            typ = "agent"
            src_dir = agent_dir
            work_repo_subdir = name
        else:
            print(f"❌ 未找到项目: {name}（不在 skills/、maby_agent/、manifest 也不在 source_overrides）")
            sys.exit(1)
    print(f"  类型: {typ}")

    # v2.37.0 多仓库：按类型切换全局 WORK_REPO / README_FILE
    WORK_REPO = get_work_repo(typ)
    README_FILE = WORK_REPO / "README.md"

    # ── 读取版本号 ────────────────────────────────────────────
    version = ""
    if is_skill:
        meta_file = skill_dir / "_meta.json"
        if meta_file.exists():
            try:
                version = json.loads(meta_file.read_text(encoding="utf-8"))["version"]
            except Exception:
                pass
    else:
        # agent 版本：优先取与智能体同名的包目录（podcast-maker → podcast_maker/）；
        # 回退扫描跳过 _ 开头过程目录与虚拟环境——源目录里的 _smoke 等残留
        # 自带第三方包的 __init__.py（含 __version__），会污染版本号（v1.15.0 事故）
        import re
        pkg_name = name.replace("-", "_")
        inits = sorted(src_dir.rglob("__init__.py"))
        def _junk(f):
            return any(p.startswith("_") or p in (".venv", "venv", "site-packages")
                       for p in f.relative_to(src_dir).parts[:-1])
        ordered = [f for f in inits if f.parent.name in (pkg_name, name)]
        ordered += [f for f in inits if f not in ordered and not _junk(f)]
        for init_f in ordered:
            if init_f.parent == src_dir:
                continue
            try:
                txt = init_f.read_text(encoding="utf-8")
                m = re.search(r'__version__\s*=\s*"([^"]+)"', txt)
                if m:
                    version = m.group(1)
                    break
            except Exception:
                continue
    if not version:
        print("❌ 无法读取版本号")
        sys.exit(1)
    # 全局归一化版本号为 PEP 440 格式（所有外部输出统一）
    version = _normalize_version(version)

    # ── market-only 模式（直接输出，不走 LOG_BUFFER）───────────────
    if market_only:
        if is_skill:
            print(f"  发布 {name} 到 ClawHub...")
            step_clawhub_publish(name, version)
            print(f"  发布 {name} 到 SkillHub...")
            step_skillhub_publish(name, version)
        elif do_pypi:
            # market-only 模式：仓库副本应在上一次完整同步时已就位
            step_pypi_publish(name, version, WORK_REPO / work_repo_subdir)
        if do_release:
            step_release_create(name, typ, version)
        # log() 只写 LOG_BUFFER 不打印，此处必须显式输出，否则 market-only 全程静默
        for line in LOG_BUFFER:
            print(line)
        return

    # ── 断点续跑检测（v2.43.0 让位式握手）──────────────────────────────
    # LLM 决策让位（exit 3）后调用方写决策文件并重跑，此处跳过已完成步骤：
    #   resume.phase == "file_filter"      → 跳过 manifest/version/normalize，
    #                                        直接进文件过滤消费（决策文件已存在）
    #   resume.phase == "sensitive_scan"   → 跳过 manifest/version/normalize/
    #                                        文件过滤/同步，直接用已同步目录
    #                                        从脱敏环节继续
    resume = _load_resume(name)
    resume_phase = resume.get("phase") if resume else None
    resumed = resume_phase is not None
    if resumed:
        log(4, 8, f"断点续跑：跳过前置步骤，从 {resume_phase} 环节继续", "ok")

    # 静默执行各步骤，收集日志
    QUIET_MODE = True
    import contextlib
    with open(os.devnull, 'w', encoding='utf-8') as _null:
        with contextlib.redirect_stdout(_null), contextlib.redirect_stderr(_null):
            if not resumed:
                step_manifest(name, version, repo_name=get_repo_name(typ))
                compare_result = step_version_compare(name, version, work_repo_subdir)

                if is_skill:
                    step_normalize_meta(meta_file, name, version)

            # 步骤 4：同步文件（版本相同时跳过；断点续跑时已同步过）
            if not resumed:
                skipped_sync = (compare_result == "skip_sync")
            else:
                skipped_sync = False
            if skipped_sync:
                log(4, 8, "跳过文件同步（版本相同）", "skip")
                repo_skill_dir = WORK_REPO / work_repo_subdir
            elif resume_phase == "sensitive_scan":
                # 脱敏断点：文件已在首次运行同步完毕，直接用 resume 记录的目标目录
                repo_skill_dir = Path(resume["repo_skill_dir"])
                log(4, 8, f"文件已同步，直接使用: {repo_skill_dir}", "ok")
            else:
                log(4, 8, "同步文件到工作仓库...")
                # ── LLM 交互：恢复 stdout 以便 WorkBuddy 看到输出并写决策文件 ──
                # file_filter 断点重跑时决策文件已存在，step_llm_file_filter
                # 直接消费返回，不会再次让位。
                _saved_out = sys.stdout
                sys.stdout = sys.__stdout__ if sys.__stdout__ else _saved_out
                try:
                    allowed = step_llm_file_filter(name, src_dir)
                finally:
                    sys.stdout = _saved_out
                if is_skill:
                    repo_skill_dir = sync_files(name, SKILLS_DIR, WORK_REPO, allowed,
                                                subdir=work_repo_subdir)
                else:
                    dst = WORK_REPO / work_repo_subdir
                    if dst.exists(): shutil.rmtree(dst)
                    os.makedirs(dst, exist_ok=True)
                    file_count = 0
                    for item in src_dir.rglob("*"):
                        if item.name.lower() == "nul": continue
                        if item.is_file():
                            try:
                                rel = item.relative_to(src_dir)
                                rel_str = str(rel).replace("\\", "/")
                                if rel_str not in allowed: continue
                                (dst / rel).parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(item, dst / rel)
                                file_count += 1
                            except: pass
                    count = sum(1 for _ in dst.rglob("*") if _.is_file())
                    repo_skill_dir = dst
                    log(4, 8, f"已同步 {count} 个文件", "ok")

            # ── LLM 交互：敏感扫描同样恢复 stdout ──
            _saved_out = sys.stdout
            sys.stdout = sys.__stdout__ if sys.__stdout__ else _saved_out
            try:
                desensitized_files = step_sensitive_scan(name, repo_skill_dir)
            finally:
                sys.stdout = _saved_out
            # README 更新：按当前类型对应的仓库生成
            step_update_readme(repo_name=get_repo_name(typ), work_repo=WORK_REPO)

            gitee_ok, github_ok = step_commit_and_push(name, version, work_repo_subdir)
            step_update_manifest_uploaded(name, version, gitee_ok, github_ok,
                                          repo_name=get_repo_name(typ))

            # 审计（仅 skill）
            audit_result = {}
            if is_skill:
                audit_result = step_skill_audit(
                    name, SKILLS_DIR, MANIFEST_FILE,
                    desensitized_files=desensitized_files,
                    repo_skill_dir=repo_skill_dir
                )

            # ZIP + index（仅 skill）
            zip_file = None
            if is_skill:
                zip_file = step_pack_zip(name, version, SKILLS_DIR)
                step_build_index()

    # ── 市场/PyPI 发布（同步完成后运行，直接输出）─────────────────────
    # PyPI（agent）只受 --pypi 控制，不受 --skip-market 影响（skip-market 仅跳过 ClawHub/SkillHub）
    if not skip_market:
        if is_skill:
            print(f"\n  发布 {name} 到 ClawHub...")
            step_clawhub_publish(name, version)
            print(f"  发布 {name} 到 SkillHub...")
            step_skillhub_publish(name, version)
    if is_agent and do_pypi:
        # 构建源用仓库精选副本（allowlist 过滤后），不再用源目录——
        # 源目录可能含海量过程文件（如 podcast-maker/_smoke 8.4G），会全量拷进构建
        step_pypi_publish(name, version, repo_skill_dir)
    # ── Release（同步完成后）────────────────────────────────────────
    if do_release:
        step_release_create(name, typ, version)

    # ── 打印步骤日志 ─────────────────────────────────────────────────
    QUIET_MODE = False
    for line in LOG_BUFFER:
        print(line)

    # ── 固定格式输出报告 ─────────────────────────────────────────────
    print()
    print("=" * 60)
    print(f"  git-sync 执行报告：{name} v{version}")
    print("=" * 60)

    # 表格 1：推送情况
    print()
    print(f"{'平台':<10} {'状态':<10} {'版本':<12}")
    print("-" * 32)
    gitee_ver = version if gitee_ok else "未推送"
    github_ver = version if github_ok else "未推送"
    # 跳过文件同步时，状态优先显示"⏭️ 跳过"，但推送成功时仍显示"✅ 成功"
    if skipped_sync and not gitee_ok:
        gitee_status = "⏭️ 跳过"
    else:
        gitee_status = "✅ 成功" if gitee_ok else "❌ 失败"
    if skipped_sync and not github_ok:
        github_status = "⏭️ 跳过"
    else:
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
            print(f"  ❌ 脱敏状态：未扫描（脱敏是强制安全门禁，不允许跳过）")

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
        print("  审计结论：跳过（agent 无 SKILL.md，SKILL.md 审计不适用）")

    # ZIP 路径
    if zip_file:
        print(f"ZIP 包：{zip_file}")
        print(f"HTML 索引：{DIST_DIR / 'index.html'}")

    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
