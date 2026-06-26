#!/usr/bin/env python3
"""
KooCLI 安装脚本
下载并安装华为云命令行工具 KooCLI

支持平台: Linux-x64, Linux-arm64, Windows, macOS
"""

import os
import sys
import platform
import urllib.request
import tarfile
import zipfile
import shutil
import subprocess
from pathlib import Path


# KooCLI 下载地址模板
# 官方下载源：https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/
DOWNLOAD_URLS = {
    "Linux-x86_64": "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-amd64.tar.gz",
    "Linux-aarch64": "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-arm64.tar.gz",
    "Windows-amd64": "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-windows-amd64.zip",
    "Windows-x86_64": "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-windows-amd64.zip",
    "Darwin-x86_64": "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-mac-amd64.tar.gz",
    "Darwin-arm64": "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-mac-arm64.tar.gz",
}

# 默认安装目录
DEFAULT_INSTALL_DIR = "/usr/local/bin" if sys.platform != "win32" else os.path.expandvars(r"%LOCALAPPDATA%\hcloud")


def get_platform_key():
    """获取当前平台的下载键"""
    system = platform.system()
    machine = platform.machine()
    
    # 标准化机器架构名称
    if machine in ("x86_64", "AMD64", "amd64"):
        machine = "x86_64"
    elif machine in ("aarch64", "arm64", "ARM64"):
        machine = "aarch64"
    
    key = f"{system}-{machine}"
    
    if key not in DOWNLOAD_URLS:
        # 尝试备用键
        if system == "Linux" and machine == "x86_64":
            key = "Linux-x86_64"
        elif system == "Linux" and machine == "aarch64":
            key = "Linux-aarch64"
    
    return key


def download_file(url: str, dest: Path) -> bool:
    """下载文件"""
    print(f"📥 正在下载: {url}")
    print(f"📁 保存到: {dest}")
    
    try:
        # 创建目标目录
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # 下载文件
        urllib.request.urlretrieve(url, dest)
        
        # 检查文件大小
        size = dest.stat().st_size
        print(f"✅ 下载完成，文件大小: {size / 1024 / 1024:.2f} MB")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def extract_archive(archive_path: Path, dest_dir: Path) -> bool:
    """解压归档文件"""
    print(f"📦 正在解压到: {dest_dir}")
    
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        if archive_path.suffix == ".gz" or archive_path.name.endswith(".tar.gz"):
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(dest_dir)
        elif archive_path.suffix == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zf:
                zf.extractall(dest_dir)
        else:
            print(f"❌ 不支持的压缩格式: {archive_path.suffix}")
            return False
        
        print("✅ 解压完成")
        return True
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False


def install_hcloud(extract_dir: Path, install_dir: Path) -> bool:
    """安装 hcloud 到系统路径"""
    # 查找 hcloud 可执行文件
    hcloud_name = "hcloud" if sys.platform != "win32" else "hcloud.exe"
    
    # 在解压目录中查找
    hcloud_src = None
    for root, dirs, files in os.walk(extract_dir):
        if hcloud_name in files:
            hcloud_src = Path(root) / hcloud_name
            break
    
    if not hcloud_src:
        print(f"❌ 未找到 {hcloud_name} 可执行文件")
        return False
    
    # 目标路径
    install_dir.mkdir(parents=True, exist_ok=True)
    hcloud_dest = install_dir / hcloud_name
    
    try:
        # 复制文件
        shutil.copy2(hcloud_src, hcloud_dest)
        
        # 设置执行权限
        if sys.platform != "win32":
            os.chmod(hcloud_dest, 0o755)
        
        print(f"✅ 已安装到: {hcloud_dest}")
        return True
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False


def verify_installation() -> bool:
    """验证安装"""
    print("\n🔍 验证安装...")
    
    try:
        result = subprocess.run(
            ["hcloud", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ KooCLI 已正确安装")
            print(f"   版本信息: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️ hcloud 命令执行异常: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ hcloud 命令未找到，可能需要添加到 PATH")
        return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 KooCLI 安装脚本")
    print("=" * 60)
    
    # 获取平台信息
    platform_key = get_platform_key()
    print(f"\n🖥️ 当前平台: {platform.system()} {platform.machine()}")
    print(f"   平台键: {platform_key}")
    
    if platform_key not in DOWNLOAD_URLS:
        print(f"❌ 不支持的平台: {platform_key}")
        print(f"   支持的平台: {list(DOWNLOAD_URLS.keys())}")
        sys.exit(1)
    
    # 获取下载 URL
    download_url = DOWNLOAD_URLS[platform_key]
    
    # 解析命令行参数
    install_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_INSTALL_DIR)
    
    print(f"📂 安装目录: {install_dir}")
    
    # 创建临时目录
    temp_dir = Path("/tmp/koocli_install") if sys.platform != "win32" else Path(os.environ.get("TEMP", ".")) / "koocli_install"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 确定下载文件名
    if download_url.endswith(".tar.gz"):
        archive_name = "hcloud.tar.gz"
    elif download_url.endswith(".zip"):
        archive_name = "hcloud.zip"
    else:
        archive_name = "hcloud_archive"
    
    archive_path = temp_dir / archive_name
    extract_dir = temp_dir / "extracted"
    
    try:
        # 1. 下载
        if not download_file(download_url, archive_path):
            sys.exit(1)
        
        # 2. 解压
        if not extract_archive(archive_path, extract_dir):
            sys.exit(1)
        
        # 3. 安装
        if not install_hcloud(extract_dir, install_dir):
            sys.exit(1)
        
        # 4. 验证
        if verify_installation():
            print("\n" + "=" * 60)
            print("🎉 KooCLI 安装成功！")
            print("=" * 60)
            print("\n使用方法:")
            print("  hcloud --help          查看帮助")
            print("  hcloud configure set   配置 AK/SK")
            print("  hcloud ECS NovaListServers  查询 ECS 列表")
        
    finally:
        # 清理临时文件
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"\n🧹 已清理临时文件")


if __name__ == "__main__":
    main()