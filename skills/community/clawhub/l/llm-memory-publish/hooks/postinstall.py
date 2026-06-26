#!/usr/bin/env python3
"""
Post-install Hook - 安装后自动拉取私有增强包

触发时机：技能安装完成后自动执行
功能：
1. 检测系统架构（x64/ARM64）
2. 从 CNB 仓库克隆私有包
3. 部署到正确位置
4. 记录安装日志

安全说明：
- 仅在用户明确安装技能后执行
- 不访问任何外部 API（仅 Git 克隆）
- 不修改系统配置
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


def log(message: str, level: str = "INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def detect_architecture() -> str:
    """检测系统架构"""
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "x64"
    elif machine in ["aarch64", "arm64"]:
        return "arm64"
    else:
        log(f"未知架构: {machine}, 默认使用 x64", "WARN")
        return "x64"


def get_skill_dir() -> Path:
    """获取技能目录"""
    # 从环境变量或默认路径获取
    skill_dir = os.environ.get("OPENCLAW_SKILL_DIR")
    if skill_dir:
        return Path(skill_dir)
    
    # 默认路径
    return Path.home() / ".openclaw" / "workspace" / "skills" / "llm-memory-integration"


def get_privileged_url() -> str:
    """获取私有包 URL"""
    return "https://cnb.cool/llm-memory-integrat/llm.git"


def clone_privileged_package(target_dir: Path, arch: str) -> bool:
    """
    克隆私有增强包
    
    Args:
        target_dir: 目标目录
        arch: 系统架构
    
    Returns:
        bool: 是否成功
    """
    url = get_privileged_url()
    
    log(f"开始克隆私有增强包...")
    log(f"  URL: {url}")
    log(f"  架构: {arch}")
    log(f"  目标: {target_dir}")
    
    try:
        # 如果目标目录已存在，先删除
        if target_dir.exists():
            log(f"目标目录已存在，删除旧版本...")
            shutil.rmtree(target_dir)
        
        # 克隆仓库
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            log(f"克隆失败: {result.stderr}", "ERROR")
            return False
        
        log(f"克隆成功！")
        return True
        
    except subprocess.TimeoutExpired:
        log("克隆超时（120秒）", "ERROR")
        return False
    except Exception as e:
        log(f"克隆异常: {e}", "ERROR")
        return False


def verify_privileged_package(target_dir: Path) -> bool:
    """
    验证私有包完整性
    
    Args:
        target_dir: 私有包目录
    
    Returns:
        bool: 是否有效
    """
    required_files = [
        "README.md",
        "hybrid_memory_search.py",
        "smart_memory_update.py"
    ]
    
    for file in required_files:
        if not (target_dir / file).exists():
            log(f"缺少必需文件: {file}", "WARN")
            return False
    
    log("私有包验证通过")
    return True


def write_install_log(skill_dir: Path, arch: str, success: bool):
    """写入安装日志"""
    log_file = skill_dir / ".privileged_install.log"
    
    with open(log_file, "w") as f:
        f.write(f"timestamp: {datetime.now().isoformat()}\n")
        f.write(f"architecture: {arch}\n")
        f.write(f"success: {success}\n")
        f.write(f"version: 1.0.0\n")


def main():
    """主函数"""
    log("=" * 60)
    log("LLM Memory Integration - Post-install Hook")
    log("=" * 60)
    
    # 1. 检测架构
    arch = detect_architecture()
    log(f"检测到系统架构: {arch}")
    
    # 2. 获取路径
    skill_dir = get_skill_dir()
    privileged_dir = skill_dir / "src" / "privileged"
    
    log(f"技能目录: {skill_dir}")
    log(f"私有包目录: {privileged_dir}")
    
    # 3. 克隆私有包
    success = clone_privileged_package(privileged_dir, arch)
    
    if success:
        # 4. 验证
        if verify_privileged_package(privileged_dir):
            log("✅ 私有增强包安装成功！")
            log("   现在可以使用高性能向量搜索功能")
        else:
            log("⚠️  私有包验证失败，将使用安全实现", "WARN")
            success = False
    else:
        log("⚠️  私有包安装失败，将使用安全实现", "WARN")
        log("   您可以稍后手动安装: https://cnb.cool/llm-memory-integrat/llm")
    
    # 5. 写入日志
    write_install_log(skill_dir, arch, success)
    
    log("=" * 60)
    log("Post-install Hook 完成")
    log("=" * 60)
    
    # 返回状态码（0=成功，1=失败但继续）
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
