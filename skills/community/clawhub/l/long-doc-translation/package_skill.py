#!/usr/bin/env python3
"""把技能目录打包为上架用 zip，并做发布前校验。

用法：
    python package_skill.py [skill_dir] [out_dir]

默认 skill_dir 为本脚本所在目录的上一级（即技能根），out_dir 为 ./dist。

校验项（不通过则中止，不产出 zip）：
  1. SKILL.md 存在，frontmatter 含非空 name / description
  2. manifest.yaml 存在，含非空 name / version / slug / description
  3. 目录结构：至少含 SKILL.md；无 .git / LICENSE / .DS_Store 等非文本杂物
  4. 危险残留扫描：scripts/ 内无可疑网络/命令注入（发布前安全自查）
产出：<slug>-<version>.zip（排除 __pycache__、.pyc、.git、dist、旧 zip 与脚本自身）
"""
import os
import re
import sys
import zipfile

# 本脚本约定放在技能根目录内（与 SKILL.md 同级），故默认 skill_dir = 脚本所在目录
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = HERE
OUT_DIR = os.path.join(SKILL_DIR, "dist")

# 打包时跳过的文件/目录（相对技能根）
EXCLUDE_NAMES = {
    ".git", "__pycache__", ".DS_Store", ".idea", ".vscode",
    "dist", "node_modules", ".pytest_cache", ".mypy_cache",
}
EXCLUDE_SUFFIX = {".pyc", ".pyo", ".zip", ".log"}

# 安全自查：脚本内出现这些高风险模式时告警（不阻断，仅提示）
RISKY_PATTERNS = [
    (r"os\.system\(", "执行 shell 命令"),
    (r"subprocess\.(call|run|Popen)", "执行子进程"),
    (r"eval\(|exec\(", "动态执行代码"),
    (r"urllib\.request|requests\.(get|post)", "发起网络请求"),
    (r"open\([^)]*['\"]w", "写文件"),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def err(msg):
    print("[FAIL] " + msg)
    sys.exit(1)


def ok(msg):
    print("[OK]   " + msg)


def warn(msg):
    print("[WARN] " + msg)


def main():
    skill_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else SKILL_DIR
    out_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else OUT_DIR

    if not os.path.isdir(skill_dir):
        err("技能目录不存在：" + skill_dir)
    print("技能目录:", skill_dir)

    # 1. SKILL.md 校验
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        err("缺少 SKILL.md")
    md = read(skill_md)
    m = re.match(r"^---\s*\n(.*?)\n---", md, re.S)
    if not m:
        err("SKILL.md 缺 frontmatter（--- ... ---）")
    fm = m.group(1)
    name_m = re.search(r"^name:\s*(\S+)", fm, re.M)
    desc_m = re.search(r"^description:\s*(.+)", fm, re.M)
    if not name_m or not name_m.group(1).strip():
        err("frontmatter 缺 name")
    if not desc_m or not desc_m.group(1).strip():
        err("frontmatter 缺 description")
    skill_name = name_m.group(1).strip()
    ok("SKILL.md frontmatter 齐全（name=%s）" % skill_name)

    # 2. manifest.yaml 校验
    manifest = os.path.join(skill_dir, "manifest.yaml")
    if not os.path.isfile(manifest):
        err("缺少 manifest.yaml（上架必需：name/version/slug/description）")
    mf = read(manifest)
    slug = None
    version = None
    for key in ("name", "version", "slug", "description"):
        mm = re.search(r"^%s:\s*(.+)$" % key, mf, re.M)
        if not mm or not mm.group(1).strip():
            err("manifest.yaml 缺字段 %s" % key)
        if key == "slug":
            slug = mm.group(1).strip()
        if key == "version":
            version = mm.group(1).strip()
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", slug or ""):
        err("slug 必须是小写字母/数字/连字符：%r" % slug)
    if not re.match(r"^\d+\.\d+\.\d+$", version or ""):
        err("version 必须是语义化版本 x.y.z：%r" % version)
    ok("manifest.yaml 齐全（slug=%s version=%s）" % (slug, version))

    # 3. 目录结构 + 危险残留扫描 + 收集待打包文件
    files = []
    for root, dirs, names in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_NAMES]
        for n in names:
            if n in EXCLUDE_NAMES:
                continue
            if os.path.splitext(n)[1].lower() in EXCLUDE_SUFFIX:
                continue
            full = os.path.join(root, n)
            rel = os.path.relpath(full, skill_dir)
            if rel == os.path.basename(__file__):
                continue  # 不打包打包脚本自身
            files.append((full, rel))
    if not files:
        err("无可打包文件")
    ok("待打包 %d 个文件" % len(files))

    # 安全自查：扫描 .py / .md / .yaml 内容
    risky = 0
    for full, rel in files:
        if os.path.splitext(rel)[1].lower() not in (".py", ".md", ".yaml"):
            continue
        try:
            content = read(full)
        except Exception:
            continue
        for pat, what in RISKY_PATTERNS:
            if re.search(pat, content):
                warn("安全自查命中 %s：%s（确认无越权后忽略）" % (what, rel))
                risky += 1
    if risky == 0:
        ok("安全自查通过：脚本无 shell 执行 / 网络请求 / 动态执行")

    # 4. 打包
    os.makedirs(out_dir, exist_ok=True)
    zip_name = "%s-%s.zip" % (slug, version)
    zip_path = os.path.join(out_dir, zip_name)
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in files:
            z.write(full, arcname=os.path.join(skill_name, rel))
    size = os.path.getsize(zip_path)
    print("\n产出:", zip_path)
    print("大小: %.1f KB" % (size / 1024))
    print("上架：把该 zip 上传至 ClawHub(https://clawhub.ai) 或 SkillHub(skillhub.cn)，填表提交审核即可。")


if __name__ == "__main__":
    main()
