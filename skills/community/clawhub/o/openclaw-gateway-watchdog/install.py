# -*- coding: utf-8 -*-
"""
OpenClaw Gateway Watchdog 安装脚本
自动配置开机自启
"""

import os
import sys
import subprocess
import platform

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "gateway_monitor.py")
PYTHON_CMD = sys.executable

def install_windows():
    """Windows 开机自启"""
    task_name = "OpenClawGatewayWatchdog"
    
    # 检查是否已存在
    result = subprocess.run(
        ["schtasks", "/query", "/tn", task_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"❌ 任务 '{task_name}' 已存在，要重新安装请先卸载")
        return False
    
    # 创建任务计划
    cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{PYTHON_CMD}" "{MAIN_SCRIPT}"',
        "/sc", "minute",
        "/mo", "1",
        "/rl", "limited",
        "/f"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Windows 开机自启安装成功！")
        print(f"   任务名: {task_name}")
        print(f"   检查频率: 每 1 分钟")
        return True
    else:
        print(f"❌ 安装失败: {result.stderr}")
        return False

def uninstall_windows():
    """Windows 卸载"""
    task_name = "OpenClawGatewayWatchdog"
    
    result = subprocess.run(
        ["schtasks", "/delete", "/tn", task_name, "/f"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 卸载成功！")
        return True
    else:
        print(f"❌ 卸载失败: {result.stderr}")
        return False

def install_linux():
    """Linux 开机自启 (systemd)"""
    service_name = "gateway-watchdog"
    service_file = f"/etc/systemd/system/{service_name}.service"
    
    if os.path.exists(service_file):
        print(f"❌ 服务已存在，要重新安装请先卸载")
        return False
    
    service_content = f"""[Unit]
Description=OpenClaw Gateway Watchdog
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'root')}
WorkingDirectory={SCRIPT_DIR}
ExecStart={PYTHON_CMD} {MAIN_SCRIPT}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    try:
        # 写入服务文件（需要 sudo）
        print(f"请手动创建服务文件: {service_file}")
        print("内容如下:")
        print("-" * 40)
        print(service_content)
        print("-" * 40)
        print("然后运行:")
        print(f"  sudo systemctl enable {service_name}")
        print(f"  sudo systemctl start {service_name}")
        return True
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False

def install_macos():
    """macOS 开机自启 (launchd)"""
    plist_name = "com.openclaw.gateway-watchdog.plist"
    plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}")
    
    if os.path.exists(plist_path):
        print(f"❌ plist 已存在，要重新安装请先卸载")
        return False
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{plist_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON_CMD}</string>
        <string>{MAIN_SCRIPT}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
    
    try:
        os.makedirs(os.path.dirname(plist_path), exist_ok=True)
        with open(plist_path, "w") as f:
            f.write(plist_content)
        
        print(f"✅ macOS 开机自启安装成功！")
        print(f"   plist: {plist_path}")
        print("然后运行:")
        print(f"  launchctl load {plist_path}")
        return True
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False

def install_crontab():
    """Linux/macOS 备选方案：crontab"""
    print("添加 crontab 开机自启...")
    print(f"请运行: @reboot {PYTHON_CMD} {MAIN_SCRIPT}")
    return True

def main():
    print("=" * 50)
    print("OpenClaw Gateway Watchdog 安装向导")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ["uninstall", "remove", "delete"]:
            system = platform.system()
            if system == "Windows":
                uninstall_windows()
            else:
                print("❌ 仅支持 Windows 卸载")
            return
    
    system = platform.system()
    print(f"\n检测到系统: {system}")
    print()
    
    print("1. 安装开机自启")
    print("2. 卸载开机自启")
    print("3. 直接运行（测试用）")
    print("4. 查看状态")
    print("0. 退出")
    print()
    
    choice = input("请选择 [1-4, 0]: ").strip()
    
    if choice == "1":
        if system == "Windows":
            install_windows()
        elif system == "Linux":
            install_linux()
        elif system == "Darwin":
            install_macos()
        else:
            print(f"❌ 不支持的系统: {system}")
    elif choice == "2":
        if system == "Windows":
            uninstall_windows()
        else:
            print("❌ 仅支持 Windows 卸载")
    elif choice == "3":
        print("运行 Watchdog（按 Ctrl+C 停止）...")
        print("提示: 使用 nohup python gateway_monitor.py & 后台运行")
        import gateway_monitor
        try:
            gateway_monitor.main()
        except KeyboardInterrupt:
            print("\n已停止")
    elif choice == "4":
        if system == "Windows":
            result = subprocess.run(
                ["schtasks", "/query", "/tn", "OpenClawGatewayWatchdog"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Watchdog 已安装")
                print(result.stdout)
            else:
                print("❌ Watchdog 未安装")
        else:
            print("请使用 ps aux | grep gateway_monitor 查看")
    elif choice == "0":
        print("退出")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
