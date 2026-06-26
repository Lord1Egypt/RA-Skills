#!/usr/bin/env python3
"""
构建智能数据采集器安装包
"""

import subprocess
import sys
import shutil
from pathlib import Path


def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(f"输出: {result.stdout[:500]}...")
    
    if result.stderr:
        print(f"错误: {result.stderr[:500]}...")
    
    if result.returncode != 0:
        print(f"命令失败，退出码: {result.returncode}")
    
    return result


def clean_build_dirs():
    """清理构建目录"""
    print("\n1. 清理构建目录...")
    
    dirs_to_clean = [
        "build",
        "dist",
        "*.egg-info",
        "output",
        "__pycache__",
        "**/__pycache__",
    ]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                print(f"  删除目录: {path}")
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                print(f"  删除文件: {path}")
                path.unlink(missing_ok=True)


def run_tests():
    """运行测试"""
    print("\n2. 运行测试...")
    
    result = run_command("pytest tests/ -v")
    
    if result.returncode != 0:
        print("❌ 测试失败!")
        return False
    
    print("✅ 测试通过!")
    return True


def check_code_quality():
    """检查代码质量"""
    print("\n3. 检查代码质量...")
    
    # 检查flake8
    print("  运行flake8...")
    result = run_command("flake8 src/ --max-line-length=88 --extend-ignore=E203,W503")
    
    if result.returncode != 0:
        print("⚠️  flake8发现代码风格问题")
    else:
        print("✅  flake8检查通过")
    
    # 检查类型提示
    print("  运行mypy...")
    result = run_command("mypy src/ --ignore-missing-imports")
    
    if result.returncode != 0:
        print("⚠️  mypy发现类型问题")
    else:
        print("✅  mypy检查通过")
    
    return True


def build_package():
    """构建安装包"""
    print("\n4. 构建安装包...")
    
    # 构建源码包和wheel包
    result = run_command("python -m build")
    
    if result.returncode != 0:
        print("❌ 构建失败!")
        return False
    
    # 检查构建结果
    dist_dir = Path("dist")
    if dist_dir.exists():
        packages = list(dist_dir.glob("*"))
        print(f"✅ 构建完成! 生成 {len(packages)} 个包:")
        for pkg in packages:
            size = pkg.stat().st_size
            print(f"   - {pkg.name} ({size:,} 字节)")
    
    return True


def create_skill_package():
    """创建OpenClaw技能包"""
    print("\n5. 创建OpenClaw技能包...")
    
    # 创建技能包目录
    skill_dir = Path("skill_package")
    skill_dir.mkdir(exist_ok=True)
    
    # 复制必要文件
    files_to_copy = [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "requirements.txt",
    ]
    
    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            dst = skill_dir / file_name
            shutil.copy2(src, dst)
            print(f"  复制: {file_name}")
    
    # 复制源代码
    src_dir = skill_dir / "src"
    if src_dir.exists():
        shutil.rmtree(src_dir)
    shutil.copytree("src", src_dir)
    print("  复制: src/")
    
    # 复制示例和配置
    examples_dir = skill_dir / "examples"
    if examples_dir.exists():
        shutil.rmtree(examples_dir)
    shutil.copytree("examples", examples_dir)
    print("  复制: examples/")
    
    config_dir = skill_dir / "config"
    if config_dir.exists():
        shutil.rmtree(config_dir)
    shutil.copytree("config", config_dir)
    print("  复制: config/")
    
    # 创建技能清单
    print("  创建技能清单...")
    try:
        import sys
        sys.path.insert(0, str(Path(".").absolute()))
        
        from src.data_harvester.openclaw_integration import SkillManifest
        
        manifest = SkillManifest()
        manifest.save(skill_dir / "skill_manifest")
        
        print("✅ 技能包创建完成!")
        print(f"  技能包位置: {skill_dir}")
        print(f"  技能名称: {manifest.name}")
        print(f"  技能版本: {manifest.version}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建技能包失败: {e}")
        return False


def main():
    """主函数"""
    print("智能数据采集器 - 构建脚本")
    print("=" * 60)
    
    # 确保在项目根目录
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"项目目录: {project_root}")
    
    # 执行构建步骤
    try:
        clean_build_dirs()
        
        if not run_tests():
            print("❌ 测试失败，停止构建")
            return 1
        
        check_code_quality()
        
        if not build_package():
            print("❌ 构建失败")
            return 1
        
        if not create_skill_package():
            print("⚠️ 技能包创建失败，但主构建成功")
        
        print(f"\n{'='*60}")
        print("🎉 构建完成!")
        print(f"{'='*60}")
        
        print("\n可用的发布文件:")
        
        # 列出dist目录
        dist_dir = Path("dist")
        if dist_dir.exists():
            for pkg in sorted(dist_dir.glob("*")):
                if pkg.is_file():
                    print(f"  📦 {pkg.relative_to(project_root)}")
        
        # 列出技能包
        skill_dir = Path("skill_package")
        if skill_dir.exists():
            print(f"  🦞 {skill_dir.relative_to(project_root)}/ (OpenClaw技能包)")
        
        print("\n下一步:")
        print("  1. 测试安装包: pip install dist/openclaw-data-harvester-*.whl")
        print("  2. 上传到PyPI: twine upload dist/*")
        print("  3. 发布到OpenClaw技能商店")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 构建过程出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import os
    sys.exit(main())