#!/usr/bin/env python3
"""
PAO 系统安装脚本
安装依赖和配置系统
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def print_header(text: str) -> None:
    """打印标题"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)


def print_success(text: str) -> None:
    """打印成功消息"""
    print(f"✅ {text}")


def print_warning(text: str) -> None:
    """打印警告消息"""
    print(f"⚠️  {text}")


def print_error(text: str) -> None:
    """打印错误消息"""
    print(f"❌ {text}")


def check_python_version() -> bool:
    """检查Python版本"""
    print_header("检查Python版本")
    
    required_version = (3, 9)
    current_version = sys.version_info[:2]
    
    print(f"当前Python版本: {sys.version}")
    print(f"要求Python版本: {required_version[0]}.{required_version[1]}+")
    
    if current_version >= required_version:
        print_success(f"Python版本满足要求")
        return True
    else:
        print_error(f"Python版本不满足要求，需要 {required_version[0]}.{required_version[1]}+")
        return False


def check_os() -> str:
    """检查操作系统"""
    print_header("检查操作系统")
    
    system = platform.system()
    release = platform.release()
    
    print(f"操作系统: {system} {release}")
    
    if system in ["Windows", "Linux", "Darwin"]:
        print_success("操作系统支持")
    else:
        print_warning(f"操作系统 {system} 可能不完全支持")
    
    return system


def install_dependencies() -> bool:
    """安装依赖"""
    print_header("安装Python依赖")
    
    # 检查是否有pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print_error("pip未安装，请先安装pip")
        return False
    
    # 安装依赖
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print_error(f"依赖文件不存在: {requirements_file}")
        return False
    
    print(f"安装依赖文件: {requirements_file}")
    
    try:
        # 使用当前Python解释器安装
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print_success("依赖安装完成")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error("依赖安装失败")
        print(e.stderr)
        return False


def setup_configuration() -> bool:
    """设置配置"""
    print_header("设置配置")
    
    config_dir = Path.home() / ".pao"
    
    try:
        # 创建配置目录
        config_dir.mkdir(parents=True, exist_ok=True)
        print_success(f"创建配置目录: {config_dir}")
        
        # 复制示例配置（如果不存在）
        example_config = Path(__file__).parent / "config.example.yaml"
        config_file = config_dir / "config.yaml"
        
        if example_config.exists() and not config_file.exists():
            shutil.copy2(example_config, config_file)
            print_success(f"创建配置文件: {config_file}")
        elif config_file.exists():
            print_success(f"配置文件已存在: {config_file}")
        else:
            print_warning(f"示例配置文件不存在: {example_config}")
            # 创建默认配置
            create_default_config(config_file)
        
        # 创建数据目录
        data_dir = config_dir / "data"
        data_dir.mkdir(exist_ok=True)
        print_success(f"创建数据目录: {data_dir}")
        
        # 创建日志目录
        log_dir = config_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        print_success(f"创建日志目录: {log_dir}")
        
        return True
        
    except Exception as e:
        print_error(f"设置配置失败: {e}")
        return False


def create_default_config(config_file: Path) -> None:
    """创建默认配置"""
    default_config = """# PAO 系统配置
# 自动生成的默认配置

device_name: "pao-{username}"
version: "0.1.0"

# 网络配置
network:
  mode: "lan_only"
  discovery_port: 8765
  data_port: 8766
  max_connections: 10
  connection_timeout: 30
  heartbeat_interval: 60

# 安全配置
security:
  privacy_level: "standard"
  encryption_enabled: true
  require_authentication: true

# 存储配置
storage:
  data_dir: "{data_dir}"
  max_storage_mb: 1024
  backup_enabled: true

# 记忆系统配置
memory:
  enable_persistent_memory: true
  memory_ttl_days: 30
  max_memory_items: 10000

# 日志配置
logging:
  level: "INFO"
  enable_file_logging: true
  log_dir: "{log_dir}"

# 功能开关
enable_discovery: true
enable_sync: true
enable_memory_sharing: true
enable_skill_evolution: false
enable_context_awareness: false

# 高级设置
auto_start: false
debug_mode: false
developer_mode: false
"""
    
    # 替换变量
    import getpass
    username = getpass.getuser()
    data_dir = str(Path.home() / ".pao" / "data").replace("\\", "/")
    log_dir = str(Path.home() / ".pao" / "logs").replace("\\", "/")
    
    config_content = default_config.format(
        username=username,
        data_dir=data_dir,
        log_dir=log_dir
    )
    
    config_file.write_text(config_content, encoding="utf-8")
    print_success(f"创建默认配置文件: {config_file}")


def setup_logging() -> bool:
    """设置日志系统"""
    print_header("设置日志系统")
    
    try:
        # 导入日志配置
        sys.path.insert(0, str(Path(__file__).parent))
        
        from src.core.config import ConfigManager
        config_manager = ConfigManager()
        config_manager.setup_logging()
        
        print_success("日志系统设置完成")
        return True
        
    except Exception as e:
        print_error(f"设置日志系统失败: {e}")
        return False


def run_tests() -> bool:
    """运行测试"""
    print_header("运行测试")
    
    test_dir = Path(__file__).parent / "tests"
    
    if not test_dir.exists():
        print_warning("测试目录不存在，跳过测试")
        return True
    
    try:
        # 运行pytest
        cmd = [sys.executable, "-m", "pytest", str(test_dir), "-v"]
        
        print(f"执行测试命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("测试通过")
            print(result.stdout)
            return True
        else:
            print_error("测试失败")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print_error(f"运行测试失败: {e}")
        return False


def create_shortcuts() -> None:
    """创建快捷方式"""
    print_header("创建快捷方式")
    
    system = platform.system()
    
    if system == "Windows":
        create_windows_shortcut()
    elif system == "Linux":
        create_linux_shortcut()
    elif system == "Darwin":
        create_macos_shortcut()
    else:
        print_warning(f"不支持为 {system} 创建快捷方式")


def create_windows_shortcut() -> None:
    """创建Windows快捷方式"""
    try:
        import winshell
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "PAO System.lnk")
        
        target = sys.executable
        w_dir = str(Path(__file__).parent)
        icon = str(Path(__file__).parent / "assets" / "pao.ico")
        
        # 如果图标不存在，使用默认图标
        if not os.path.exists(icon):
            icon = None
        
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = target
            shortcut.arguments = str(Path(__file__).parent / "pao.py") + " start"
            shortcut.working_directory = w_dir
            if icon:
                shortcut.icon_location = (icon, 0)
            shortcut.description = "PAO System - Personal AI Operating System"
        
        print_success(f"创建桌面快捷方式: {shortcut_path}")
        
    except ImportError:
        print_warning("无法创建Windows快捷方式，需要安装winshell库")
    except Exception as e:
        print_warning(f"创建Windows快捷方式失败: {e}")


def create_linux_shortcut() -> None:
    """创建Linux快捷方式"""
    try:
        desktop_file = Path.home() / ".local" / "share" / "applications" / "pao-system.desktop"
        
        desktop_file.parent.mkdir(parents=True, exist_ok=True)
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=PAO System
Comment=Personal AI Operating System
Exec={sys.executable} {Path(__file__).parent / 'pao.py'} start
Path={Path(__file__).parent}
Icon={Path(__file__).parent / 'assets' / 'pao.png'}
Terminal=true
Categories=Utility;Network;
"""
        
        desktop_file.write_text(desktop_content, encoding="utf-8")
        os.chmod(desktop_file, 0o755)
        
        print_success(f"创建桌面应用: {desktop_file}")
        
    except Exception as e:
        print_warning(f"创建Linux快捷方式失败: {e}")


def create_macos_shortcut() -> None:
    """创建macOS快捷方式"""
    print_warning("macOS快捷方式创建需要手动配置")
    print("请将以下命令添加到终端配置文件:")
    print(f"alias pao='{sys.executable} {Path(__file__).parent / 'pao.py'}'")


def show_completion_message() -> None:
    """显示完成消息"""
    print_header("安装完成")
    
    print("\n🎉 PAO 系统安装完成！")
    print("\n下一步:")
    print("1. 启动系统: python pao.py start")
    print("2. 运行演示: python pao.py demo")
    print("3. 查看配置: python pao.py config show")
    print("\n快速开始:")
    print("  cd pao-system")
    print("  python pao.py demo")
    print("\n文档:")
    print("  查看 README.md 获取更多信息")
    
    # 显示配置位置
    config_dir = Path.home() / ".pao"
    print(f"\n配置文件位置: {config_dir}")


def main() -> None:
    """主函数"""
    print("PAO 系统安装程序")
    print("版本: 0.1.0")
    print()
    
    # 检查是否在项目目录中
    project_root = Path(__file__).parent
    if not (project_root / "src").exists():
        print_error("请在PAO系统项目目录中运行此脚本")
        print(f"当前目录: {project_root}")
        sys.exit(1)
    
    # 执行安装步骤
    steps = [
        ("检查Python版本", check_python_version),
        ("检查操作系统", check_os),
        ("安装依赖", install_dependencies),
        ("设置配置", setup_configuration),
        ("设置日志系统", setup_logging),
        ("运行测试", run_tests),
        ("创建快捷方式", create_shortcuts),
    ]
    
    all_success = True
    
    for step_name, step_func in steps:
        success = step_func()
        if not success:
            print_warning(f"步骤 '{step_name}' 失败")
            # 对于非关键步骤，继续执行
            if step_name in ["检查Python版本", "安装依赖"]:
                all_success = False
                break
    
    if all_success:
        show_completion_message()
    else:
        print_error("安装过程中出现错误")
        print("请检查上述错误信息并重试")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print_error(f"安装过程中出现未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)