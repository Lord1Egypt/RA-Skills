#!/usr/bin/env python3
"""
多 Agent 项目构建器 - 项目生成脚本
一键生成完整的多 Agent 项目模板结构
"""

import os
import sys
import shutil
from pathlib import Path


def get_templates_dir() -> Path:
    """获取模板目录路径"""
    return Path(__file__).parent.parent / "templates"


def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("  多 Agent 项目构建器")
    print("=" * 60)
    print()


def create_project_structure(project_dir: Path):
    """创建项目目录结构"""
    print(f"📁 项目目录: {project_dir}")
    print()
    print("📁 创建目录结构...")

    # 主目录
    project_dir.mkdir(parents=True, exist_ok=True)

    # 输出目录
    outputs_dir = project_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    # 各个阶段的输出目录
    phases = ["01-requirements", "02-research", "03-architecture",
              "04-implementation", "05-testing"]
    for phase in phases:
        (outputs_dir / phase).mkdir(exist_ok=True)


def copy_template_files(project_dir: Path, templates_dir: Path):
    """复制模板文件到项目目录"""
    print("📄 复制模板文件...")

    # 复制配置文件
    config_src = templates_dir / "PROJECT_CONFIG.yaml"
    config_dst = project_dir / "PROJECT_CONFIG.yaml"
    shutil.copy2(config_src, config_dst)

    # 复制执行指南
    guide_src = templates_dir / "EXECUTION_GUIDE.md"
    guide_dst = project_dir / "EXECUTION_GUIDE.md"
    shutil.copy2(guide_src, guide_dst)

    # 复制 README
    readme_src = templates_dir / "README.md"
    readme_dst = project_dir / "README.md"
    shutil.copy2(readme_src, readme_dst)

    # 创建 .gitignore
    gitignore = project_dir / ".gitignore"
    gitignore.write_text("""# Outputs
outputs/

# Temporary files
*.tmp
*.swp
*.swo
*~

# IDE
.vscode/
.idea/
*.iml

# OS
.DS_Store
Thumbs.db
""")


def print_success(project_dir: Path):
    """打印成功消息"""
    print()
    print("=" * 60)
    print("  ✅ 项目创建成功！")
    print("=" * 60)
    print()
    print("下一步:")
    print(f"  1. 进入项目目录:")
    print(f"     cd {project_dir}")
    print()
    print(f"  2. 编辑项目配置:")
    print(f"     打开 PROJECT_CONFIG.yaml，修改项目名称、描述等")
    print()
    print(f"  3. 在 Hermes 中开始执行:")
    print(f"     参考 EXECUTION_GUIDE.md 中的说明")
    print()
    print("项目结构:")
    print(f"  {project_dir.name}/")
    print(f"  ├── PROJECT_CONFIG.yaml    # 项目配置")
    print(f"  ├── EXECUTION_GUIDE.md     # 执行指南")
    print(f"  ├── README.md              # 项目说明")
    print(f"  ├── .gitignore             # Git 忽略")
    print(f"  └── outputs/               # 输出目录")
    print(f"      ├── 01-requirements/   # 需求分析")
    print(f"      ├── 02-research/       # 技术调研")
    print(f"      ├── 03-architecture/   # 架构设计")
    print(f"      ├── 04-implementation/ # 代码实现")
    print(f"      └── 05-testing/        # 测试报告")
    print()


def main():
    print_banner()

    # 获取项目目录
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = input("请输入项目名称: ").strip()
        if not project_name:
            print("❌ 项目名称不能为空")
            sys.exit(1)

    project_dir = Path.cwd() / project_name

    # 检查目录是否已存在
    if project_dir.exists():
        response = input(f"⚠️  目录 {project_name} 已存在，是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("操作已取消")
            sys.exit(0)
        shutil.rmtree(project_dir)

    # 获取模板目录
    templates_dir = get_templates_dir()
    if not templates_dir.exists():
        print(f"❌ 模板目录不存在: {templates_dir}")
        sys.exit(1)

    # 创建项目
    create_project_structure(project_dir)
    copy_template_files(project_dir, templates_dir)
    print_success(project_dir)


if __name__ == "__main__":
    main()
