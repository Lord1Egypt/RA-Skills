#!/usr/bin/env python3
"""
Bootstrap Extra Files - 本地链接钩子

功能：在安装时检查环境变量，将本地私有文件夹的内容链接到当前工作区。
不执行任何网络操作，不暴露任何敏感信息。

环境变量：
- CNB_PRIVATE_WORKSPACE: 指向本地私有配置目录的路径

使用方法：
1. 用户设置环境变量：export CNB_PRIVATE_WORKSPACE="/path/to/private/config"
2. 安装技能后，此钩子自动将私有目录链接到工作区
"""

import os
import shutil
from pathlib import Path


def get_private_workspace() -> Path | None:
    """获取私有工作区路径"""
    private_path = os.getenv('CNB_PRIVATE_WORKSPACE')
    if private_path:
        return Path(private_path).expanduser().absolute()
    return None


def link_private_files(private_dir: Path, target_dir: Path) -> list[str]:
    """
    将私有目录的文件链接到目标目录
    
    Args:
        private_dir: 私有目录路径
        target_dir: 目标目录路径
        
    Returns:
        已链接的文件列表
    """
    linked_files = []
    
    if not private_dir.exists():
        print(f"⚠️ 私有目录不存在: {private_dir}")
        return linked_files
    
    for item in private_dir.iterdir():
        if item.is_file():
            target = target_dir / item.name
            if not target.exists():
                try:
                    # 优先使用软链接，失败则复制
                    target.symlink_to(item)
                    linked_files.append(item.name)
                    print(f"✅ 已链接: {item.name}")
                except OSError:
                    # 不支持软链接时使用复制
                    shutil.copy2(item, target)
                    linked_files.append(item.name)
                    print(f"✅ 已复制: {item.name}")
            else:
                print(f"⏭️ 跳过已存在: {item.name}")
        elif item.is_dir():
            # 目录也链接
            target = target_dir / item.name
            if not target.exists():
                try:
                    target.symlink_to(item)
                    linked_files.append(f"{item.name}/")
                    print(f"✅ 已链接目录: {item.name}/")
                except OSError:
                    shutil.copytree(item, target)
                    linked_files.append(f"{item.name}/")
                    print(f"✅ 已复制目录: {item.name}/")
    
    return linked_files


def main():
    """主函数"""
    print("=" * 50)
    print("🔧 Bootstrap Extra Files - 本地链接钩子")
    print("=" * 50)
    
    # 获取私有工作区路径
    private_workspace = get_private_workspace()
    
    if not private_workspace:
        print("ℹ️ 未设置 CNB_PRIVATE_WORKSPACE 环境变量")
        print("   如需使用私有配置，请设置：")
        print("   export CNB_PRIVATE_WORKSPACE='/path/to/private/config'")
        return 0
    
    print(f"📁 私有目录: {private_workspace}")
    
    # 获取当前工作区（技能目录）
    skill_dir = Path(__file__).parent.parent
    print(f"📁 目标目录: {skill_dir}")
    
    # 链接文件
    linked = link_private_files(private_workspace, skill_dir)
    
    print("=" * 50)
    if linked:
        print(f"✅ 完成！已链接 {len(linked)} 个项目")
        for f in linked:
            print(f"   - {f}")
    else:
        print("ℹ️ 未链接任何文件")
    
    return 0


if __name__ == "__main__":
    exit(main())
