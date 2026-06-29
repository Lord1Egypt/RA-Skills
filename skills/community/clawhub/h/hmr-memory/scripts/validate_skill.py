#!/usr/bin/env python3
"""
validate_skill.py — 校验 OpenClaw skill 是否符合 AgentSkills 规范

检查项：
  1. SKILL.md 存在且有合法 YAML frontmatter
  2. frontmatter 必需字段 name / description
  3. metadata（如有）是合法单行 JSON
  4. frontmatter 全部为单行 key（OpenClaw 解析器要求）
  5. package.json 存在且为合法 JSON
  6. SKILL.md 与 package.json 版本号一致
  7. 安全检查：无真实密钥泄漏、无 shell 命令指示、无未替换占位符

退出码 0 = 全部通过；非 0 = 有问题（CI 会失败）
"""

import re
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []


def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)


# ── 1. SKILL.md 存在 + frontmatter ────────────────────────────────────────
skill_md = ROOT / "SKILL.md"
if not skill_md.exists():
    err("SKILL.md 不存在")
    print("\n".join(errors)); sys.exit(1)

content = skill_md.read_text(encoding="utf-8")
m = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
if not m:
    err("SKILL.md 缺少合法的 YAML frontmatter（必须以 --- 开头和结尾）")
    print("\n".join(errors)); sys.exit(1)

frontmatter = m.group(1)

# ── 2. 必需字段 ────────────────────────────────────────────────────────────
if not re.search(r'^name:\s*\S+', frontmatter, re.M):
    err("frontmatter 缺少必需字段: name")
if not re.search(r'^description:\s*\S+', frontmatter, re.M):
    err("frontmatter 缺少必需字段: description")

# 提取 name 供后续比对
name_match = re.search(r'^name:\s*(\S+)', frontmatter, re.M)
skill_name = name_match.group(1) if name_match else None

# 提取 version
ver_match = re.search(r'^version:\s*(\S+)', frontmatter, re.M)
skill_version = ver_match.group(1) if ver_match else None

# ── 3. metadata 单行 JSON ─────────────────────────────────────────────────
meta_match = re.search(r'^metadata:\s*(.+)$', frontmatter, re.M)
if meta_match:
    raw = meta_match.group(1).strip()
    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        err(f"metadata 不是合法的单行 JSON: {e}")

# ── 4. 全部单行 key（不允许 YAML 多行值/缩进块）────────────────────────────
for i, line in enumerate(frontmatter.split("\n"), 1):
    if not line.strip():
        continue
    # 顶层 key 行必须含冒号；缩进行（多行值）不允许
    if line.startswith((" ", "\t")):
        err(f"frontmatter 第 {i} 行是缩进/多行值，OpenClaw 只支持单行 key: {line!r}")
    elif ":" not in line:
        err(f"frontmatter 第 {i} 行不是合法 key: value 形式: {line!r}")

# ── 5. package.json ────────────────────────────────────────────────────────
pkg_path = ROOT / "package.json"
pkg = None
if not pkg_path.exists():
    err("package.json 不存在（ClawHub 发布需要）")
else:
    try:
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"package.json 不是合法 JSON: {e}")

# ── 6. 版本号一致 ──────────────────────────────────────────────────────────
if pkg and skill_version:
    pkg_version = pkg.get("version")
    if pkg_version != skill_version:
        err(f"版本号不一致: SKILL.md={skill_version} vs package.json={pkg_version}")

# name 一致
if pkg and skill_name:
    if pkg.get("name") != skill_name:
        warn(f"name 不一致: SKILL.md={skill_name} vs package.json={pkg.get('name')}")

# ── 7. 安全检查 ────────────────────────────────────────────────────────────
all_text = content
for p in [ROOT / "README.md", ROOT / "README_EN.md", pkg_path]:
    if p.exists():
        all_text += "\n" + p.read_text(encoding="utf-8")

# 7a. 真实密钥泄漏（sk- 后跟长串）
for km in re.finditer(r'sk-[A-Za-z0-9]{20,}', all_text):
    err(f"疑似真实 API Key 泄漏: {km.group(0)[:12]}...")

# 7b. 未替换占位符
if "your-org" in all_text:
    warn("仍含占位符 'your-org'，发布前请替换为真实 GitHub 用户名/组织名")

# 7c. SKILL.md 不应指示 agent 运行 shell（安全规范）
shell_patterns = [r'\bexec\b', r'\bsubprocess\b', r'rm -rf', r'curl .* \| .*sh', r'\bbash -c\b']
for sp in shell_patterns:
    if re.search(sp, content):
        warn(f"SKILL.md 含疑似 shell 执行指示 ({sp})，请确认是否安全（恶意 skill 常见特征）")

# 7d. package.json 安全声明
if pkg and "agentSkill" in pkg:
    a = pkg["agentSkill"]
    if a.get("shellCommands") is not False:
        warn("package.json 未声明 shellCommands: false")
    if a.get("secrets") is not False:
        warn("package.json 未声明 secrets: false")

# ── 输出结果 ───────────────────────────────────────────────────────────────
print("=" * 56)
print(" OpenClaw Skill 合规校验")
print("=" * 56)
print(f" skill 名称:  {skill_name}")
print(f" 版本:        {skill_version}")
print("-" * 56)

if warnings:
    print(f"\n⚠️  {len(warnings)} 个警告:")
    for w in warnings:
        print(f"   - {w}")

if errors:
    print(f"\n❌ {len(errors)} 个错误（必须修复）:")
    for e in errors:
        print(f"   - {e}")
    print("\n校验失败。")
    sys.exit(1)
else:
    print("\n✅ 所有必需检查通过！")
    if warnings:
        print("   （有警告但不阻塞，发布前建议处理）")
    sys.exit(0)
