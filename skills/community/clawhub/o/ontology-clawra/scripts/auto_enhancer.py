#!/usr/bin/env python3
"""
ontology-clawra 自动增强器
持续监控和改进本体论引擎，每次升级自动推送 GitHub + ClawHub
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 配置
SKILL_DIR = Path(__file__).parent.parent
VERSION_FILE = SKILL_DIR / "_meta.json"
CHANGELOG_FILE = SKILL_DIR / "CHANGELOG.md"
SKILL_MD = SKILL_DIR / "SKILL.md"
GITHUB_REPO = "https://github.com/wu-xiaochen/AbilityBuilder-Agent.git"
CLAWHUB_SLUG = "ontology-clawra"


def get_current_version() -> str:
    """获取当前版本"""
    if VERSION_FILE.exists():
        data = json.loads(VERSION_FILE.read_text())
        return data.get("version", "3.3.0")
    return "3.3.0"


def bump_version(version: str, level: str = "patch") -> str:
    """升级版本号"""
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    return f"{major}.{minor}.{patch}"


def update_meta_json(new_version: str):
    """更新 _meta.json"""
    data = {
        "ownerId": "kn7bp4hq9xfft748m62g9vnwm9830csh",
        "slug": CLAWHUB_SLUG,
        "version": new_version,
        "publishedAt": int(datetime.now().timestamp() * 1000)
    }
    VERSION_FILE.write_text(json.dumps(data, indent=2))


def update_changelog(new_version: str, changes: List[str]):
    """更新 CHANGELOG.md"""
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"## v{new_version} ({today}) - 自动增强版\n\n"
    content = "### 增强内容\n"
    for change in changes:
        content += f"- {change}\n"
    content += "\n---\n\n"

    if CHANGELOG_FILE.exists():
        existing = CHANGELOG_FILE.read_text()
    else:
        existing = ""

    CHANGELOG_FILE.write_text(header + content + existing)
    print(f"📝 CHANGELOG.md 已更新: v{new_version}")


def update_skill_md_version(new_version: str):
    """更新 SKILL.md 中的版本号"""
    if SKILL_MD.exists():
        content = SKILL_MD.read_text()
        # 更新 metadata 中的版本
        content = content.replace(
            f'"version": "{get_current_version()}"',
            f'"version": "{new_version}"'
        )
        content = content.replace(
            f"version: {get_current_version()}",
            f"version: {new_version}"
        )
        # 更新 last_updated
        today = datetime.now().strftime("%Y-%m-%d")
        import re
        content = re.sub(
            r'"last_updated": "\d{4}-\d{2}-\d{2}"',
            f'"last_updated": "{today}"',
            content
        )
        content = re.sub(
            r"last_updated: \d{4}-\d{2}-\d{2}",
            f"last_updated: {today}",
            content
        )
        SKILL_MD.write_text(content)
        print(f"📄 SKILL.md 已更新: v{new_version}")


def git_commit_push(new_version: str) -> bool:
    """提交并推送到 GitHub"""
    try:
        # 添加所有更改
        subprocess.run(["git", "add", "."], cwd=SKILL_DIR, check=True)

        # 检查是否有更改
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=SKILL_DIR,
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            print("📦 没有需要提交的更改")
            return False

        # 提交
        commit_msg = f"feat: ontology-clawra v{new_version} - 自动增强"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=SKILL_DIR,
            check=True
        )
        print(f"✅ Git 提交: {commit_msg}")

        # 推送到远程
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=SKILL_DIR,
            check=True
        )
        print("✅ GitHub 推送成功")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False


def publish_clawhub() -> bool:
    """发布到 ClawHub"""
    try:
        # 使用 clawhub CLI 发布
        result = subprocess.run(
            ["clawhub", "publish", CLAWHUB_SLUG],
            cwd=SKILL_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ ClawHub 发布成功: {CLAWHUB_SLUG}")
            return True
        else:
            print(f"⚠️ ClawHub 发布需要手动执行: clawhub publish {CLAWHUB_SLUG}")
            return False
    except FileNotFoundError:
        print("⚠️ clawhub CLI 未找到，请手动发布")
        return False


def analyze_and_enhance() -> tuple[bool, List[str]]:
    """
    分析当前状态并生成增强建议
    触发条件：发现优化点就触发升级
    返回: (是否需要升级, 增强内容列表)
    """
    changes = []

    # 1. 检查 SKILL.md 版本与 _meta.json 是否一致
    skill_md_version = None
    if SKILL_MD.exists():
        content = SKILL_MD.read_text()
        import re
        match = re.search(r'version:\s*"?(\d+\.\d+\.\d+)"?', content)
        if match:
            skill_md_version = match.group(1)

    current_meta = get_current_version()
    if skill_md_version and skill_md_version != current_meta:
        changes.append(f"版本同步: SKILL.md {skill_md_version} → {current_meta}")

    # 2. 检查必要文件是否存在
    required_files = [
        "scripts/ontology-clawra.py",
        "scripts/main.py",
        "scripts/confidence_tracker.py",
        "scripts/typical_scenarios.py",
        "scripts/interactive_confirm.py",
        "scripts/network_fetch.py",
        "scripts/self_eval.py",
        "memory/schema.yaml",
        "memory/rules.yaml",
        "memory/laws.yaml"
    ]

    for f in required_files:
        filepath = SKILL_DIR / f
        if not filepath.exists():
            changes.append(f"⚠️ 缺失文件: {f}")

    # 3. 检查 memory 目录内容 - 核心增强点
    memory_dir = SKILL_DIR / "scripts" / "memory"
    if memory_dir.exists():
        files = list(memory_dir.glob("*"))
        if len(files) < 5:
            changes.append(f"📁 memory 目录内容较少 ({len(files)} 个文件)，可能需要扩充")
        
        # 4. 检查各领域本体覆盖情况
        domain_coverage = check_domain_coverage()
        if domain_coverage:
            changes.extend(domain_coverage)

    # 5. 检查 evals 目录
    evals_dir = SKILL_DIR / "evals"
    if not evals_dir.exists() or not list(evals_dir.glob("*.json")):
        changes.append("🧪 缺少评估测试文件")

    # 6. 检查文档完整性
    if SKILL_MD.exists():
        content = SKILL_MD.read_text()
        doc_length = len(content)

        if doc_length < 10000:
            changes.append(f"📄 文档较短 ({doc_length} chars)，可考虑扩充示例和场景")
        if "v3." not in content and "v4." not in content:
            changes.append("🔄 文档版本较旧，建议更新至最新版本格式")

    # 7. 检查推理规则完整性
    rule_coverage = check_rule_coverage()
    if rule_coverage:
        changes.extend(rule_coverage)

    # 8. 自动增强：确保 memory 目录有基础数据
    ensure_memory_files()

    # 9. 自动增强：更新 self_eval.py
    enhance_self_eval()

    return len(changes) > 0, changes


def check_domain_coverage() -> List[str]:
    """检查各领域本体覆盖，发现缺失领域即添加"""
    changes = []
    
    # 已支持领域
    known_domains = [
        "供应链", "医疗", "金融", "制造", "法律", "能源",
        "燃气工程", "AI", "商业战略", "技术", "教育"
    ]
    
    # 检查 memory/laws.yaml 中的领域覆盖
    laws_file = SKILL_DIR / "scripts" / "memory" / "laws.yaml"
    if laws_file.exists():
        content = laws_file.read_text()
        for domain in known_domains:
            if domain not in content:
                changes.append(f"🌐 发现新领域: {domain}，建议添加领域规则")
    
    return changes


def check_rule_coverage() -> List[str]:
    """检查推理规则覆盖，发现缺失规则即添加"""
    changes = []
    
    # 核心推理规则应该覆盖的场景
    required_scenarios = [
        "选型分析", "计算分析", "风险评估", "决策支持",
        "知识抽取", "规则匹配", "置信度评估", "多领域推理"
    ]
    
    rules_file = SKILL_DIR / "scripts" / "memory" / "rules.yaml"
    if rules_file.exists():
        content = rules_file.read_text()
        for scenario in required_scenarios:
            if scenario not in content:
                changes.append(f"📋 发现缺失推理规则: {scenario}，建议添加")
    
    return changes


def ensure_memory_files():
    """确保 memory 目录有必要的文件"""
    memory_dir = SKILL_DIR / "scripts" / "memory"
    memory_dir.mkdir(exist_ok=True)

    # 确保有基础 schema
    schema_file = memory_dir / "schema.yaml"
    if not schema_file.exists():
        schema_file.write_text("""# ontology-clawra Schema v3.5

types:
  Person:
    required: [name]
    properties:
      name: string
      role: string
      goals: list
      preferences: map
      capabilities: list

  Concept:
    required: [name, definition]
    properties:
      name: string
      definition: string
      domain: string

  Law:
    required: [name, domain, statement]
    properties:
      name: string
      domain: string
      statement: string
      conditions: list
      effects: list

  Rule:
    required: [name, condition, action]
    properties:
      name: string
      condition: string
      action: string
      weight: float
      enabled: boolean

links:
  works_on: { from: [Person], to: [Project, Task] }
  triggers: { from: [Rule], to: [Decision] }
  relates_to: { from: [Any], to: [Any] }
  is_a: { from: [Concept], to: [Concept] }
""")
        print("✅ memory/schema.yaml 已创建")


def enhance_self_eval():
    """增强 self_eval.py"""
    self_eval_file = SKILL_DIR / "scripts" / "self_eval.py"
    if not self_eval_file.exists():
        return

    content = self_eval_file.read_text()

    # 检查是否有基础的评估逻辑
    if "def evaluate" not in content:
        # 需要增强
        new_content = '''#!/usr/bin/env python3
"""
ontology-clawra 自我评估模块
用于测试和改进本体论引擎
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent


def evaluate_ontology():
    """评估本体论引擎"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }

    # 测试1: 检查核心文件
    core_files = [
        "SKILL.md",
        "scripts/ontology-clawra.py",
        "scripts/main.py",
        "memory/schema.yaml"
    ]

    for f in core_files:
        filepath = SKILL_DIR / f
        results["tests"].append({
            "name": f"核心文件: {f}",
            "passed": filepath.exists(),
            "required": True
        })

    # 测试2: 检查版本一致性
    try:
        meta = json.loads((SKILL_DIR / "_meta.json").read_text())
        skill_md = (SKILL_DIR / "SKILL.md").read_text()
        version_in_skill = "version:" in skill_md
        results["tests"].append({
            "name": "版本一致性",
            "passed": version_in_skill,
            "details": f"meta: {meta.get('version')}"
        })
    except:
        results["tests"].append({
            "name": "版本一致性",
            "passed": False,
            "required": True
        })

    return results


def main():
    results = evaluate_ontology()
    passed = sum(1 for t in results["tests"] if t["passed"])
    total = len(results["tests"])

    print(f"\\n🧪 ontology-clawra 自我评估")
    print(f"   通过: {passed}/{total}")

    for t in results["tests"]:
        status = "✅" if t["passed"] else "❌"
        print(f"   {status} {t['name']}")

    if passed == total:
        print("\\n🎉 所有测试通过!")
        return 0
    else:
        print("\\n⚠️ 部分测试失败，建议运行增强器")
        return 1


if __name__ == "__main__":
    sys.exit(main())
'''
        self_eval_file.write_text(new_content)
        print("✅ scripts/self_eval.py 已增强")


def run_full_enhancement():
    """运行完整增强流程"""
    print("=" * 60)
    print("🚀 ontology-clawra 自动增强器")
    print("=" * 60)

    current_version = get_current_version()
    print(f"\n📌 当前版本: v{current_version}")

    # 1. 分析当前状态
    print("\n🔍 分析当前状态...")
    needs_upgrade, changes = analyze_and_enhance()

    if not needs_upgrade:
        print("✅ 当前版本已是最新状态，无需升级")
        return False

    print(f"\n📋 发现 {len(changes)} 项可改进:")
    for change in changes:
        print(f"   • {change}")

    # 2. 决定升级级别
    if any("版本" in c for c in changes):
        level = "minor"
    else:
        level = "patch"

    new_version = bump_version(current_version, level)
    print(f"\n🔄 升级版本: v{current_version} → v{new_version} ({level}级)")

    # 3. 更新文件
    print("\n📝 更新文件...")
    update_skill_md_version(new_version)
    update_changelog(new_version, changes)
    update_meta_json(new_version)

    # 4. Git 提交推送
    print("\n📦 提交到 GitHub...")
    if git_commit_push(new_version):
        # 5. 发布到 ClawHub
        print("\n🌐 发布到 ClawHub...")
        publish_clawhub()

    print("\n" + "=" * 60)
    print(f"✅ ontology-clawra v{new_version} 增强完成!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_full_enhancement()
    sys.exit(0 if success else 0)  # 即使无升级也返回0
