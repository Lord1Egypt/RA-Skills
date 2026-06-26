"""PAO系统安装程序"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


class Installer:
    def __init__(self):
        self.install_dir = Path.home() / ".pao"
        self.config_dir = Path.home() / ".config" / "pao"

    def install(self):
        print("🚀 PAO系统安装程序")
        print("=" * 50)

        # 检查Python版本
        if sys.version_info < (3, 9):
            print("❌ 需要 Python 3.9 或更高版本")
            return False

        print(f"📦 安装目录: {self.install_dir}")
        print(f"⚙️ 配置目录: {self.config_dir}")

        # 创建目录
        self._create_directories()

        # 安装依赖
        self._install_dependencies()

        # 复制配置文件
        self._copy_config()

        print()
        print("✅ 安装完成!")
        print(f"运行 'python -m pao' 启动系统")
        return True

    def _create_directories(self):
        """创建必要的目录"""
        print("📁 创建目录结构...")
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _install_dependencies(self):
        """安装依赖"""
        print("📚 安装依赖...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True
            )
        except subprocess.CalledProcessError:
            print("⚠️ 依赖安装失败，请手动运行: pip install -r requirements.txt")

    def _copy_config(self):
        """复制配置文件"""
        print("📋 复制配置文件...")
        config_template = self.install_dir / "config_template.json"
        if not config_template.exists():
            config_template.write_text('{"device_name": "PAO-Device", "port": 8080}')

    def uninstall(self):
        """卸载系统"""
        print("🗑️ 正在卸载PAO系统...")
        shutil.rmtree(self.install_dir, ignore_errors=True)
        shutil.rmtree(self.config_dir, ignore_errors=True)
        print("✅ 卸载完成")


if __name__ == "__main__":
    installer = Installer()
    if "--uninstall" in sys.argv:
        installer.uninstall()
    else:
        installer.install()
