# -*- coding: utf-8 -*-
"""
OpenClaw Gateway Watchdog
Gateway 监控脚本，支持自动重启和钉钉通知
"""

import os
import sys
import time
import json
import hmac
import base64
import urllib.parse
import urllib.request
import subprocess
import platform
from datetime import datetime, timezone, timedelta

# ==================== 配置区域 ====================
# 优先使用同目录下的 config.py
import os
import sys

_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
if os.path.exists(_config_file):
    sys.path.insert(0, os.path.dirname(_config_file))
    try:
        import config
        WEBHOOK = getattr(config, 'WEBHOOK', "")
        SECRET = getattr(config, 'SECRET', "")
        CHECK_INTERVAL = getattr(config, 'CHECK_INTERVAL', 60)
        GATEWAY_PORT = getattr(config, 'GATEWAY_PORT', 18789)
        GATEWAY_URL = getattr(config, 'GATEWAY_URL', f"http://127.0.0.1:{GATEWAY_PORT}/")
        NOTIFY_ON_STARTUP = getattr(config, 'NOTIFY_ON_STARTUP', True)
        NOTIFY_ON_DOWN = getattr(config, 'NOTIFY_ON_DOWN', True)
        NOTIFY_ON_RECOVERY = getattr(config, 'NOTIFY_ON_RECOVERY', True)
        NOTIFY_ON_FAILED = getattr(config, 'NOTIFY_ON_FAILED', True)
        NOTIFY_DAILY = getattr(config, 'NOTIFY_DAILY', True)
        LOG_FILE = getattr(config, 'LOG_FILE', os.path.join(os.path.expanduser("~"), ".openclaw", "gateway-watchdog.log"))
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        WEBHOOK = ""
        SECRET = ""
        CHECK_INTERVAL = 60
        GATEWAY_PORT = 18789
        GATEWAY_URL = f"http://127.0.0.1:{GATEWAY_PORT}/"
        NOTIFY_ON_STARTUP = True
        NOTIFY_ON_DOWN = True
        NOTIFY_ON_RECOVERY = True
        NOTIFY_ON_FAILED = True
        NOTIFY_DAILY = True
        LOG_FILE = os.path.join(os.path.expanduser("~"), ".openclaw", "gateway-watchdog.log")
else:
    # 钉钉配置
    WEBHOOK = ""  # 钉钉 Webhook URL
    SECRET = ""   # 钉钉加签密钥

    # 监控配置
    CHECK_INTERVAL = 60      # 检查间隔（秒）
    GATEWAY_PORT = 18789    # Gateway 端口
    GATEWAY_URL = f"http://127.0.0.1:{GATEWAY_PORT}/"

    # 通知配置
    NOTIFY_ON_STARTUP = True    # 启动时报平安
    NOTIFY_ON_DOWN = True       # 掉线时通知
    NOTIFY_ON_RECOVERY = True   # 恢复时通知
    NOTIFY_ON_FAILED = True     # 重启失败时通知
    NOTIFY_DAILY = True         # 每天报平安

    # 日志文件
    LOG_FILE = os.path.join(os.path.expanduser("~"), ".openclaw", "gateway-watchdog.log")
# =================================================

# 北京时间
def beijing_now():
    return datetime.now(timezone(timedelta(hours=8)))

def log(msg):
    """记录日志"""
    timestamp = beijing_now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def send_dingtalk(text):
    """发送钉钉通知"""
    if not WEBHOOK or not SECRET:
        log("钉钉未配置，跳过通知")
        return
    
    timestamp = int(time.time() * 1000)
    sign_str = f"{timestamp}\n{SECRET}"
    
    # HMAC-SHA256 签名
    hmac_obj = hmac.new(SECRET.encode("utf-8"), sign_str.encode("utf-8"), digestmod="sha256")
    sign = base64.b64encode(hmac_obj.digest()).decode("utf-8")
    sign = urllib.parse.quote(sign)
    
    url = f"{WEBHOOK}&timestamp={timestamp}&sign={sign}"
    
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("errcode") == 0:
                log("钉钉通知发送成功")
            else:
                log(f"钉钉通知发送失败: {result.get('errmsg')}")
    except Exception as e:
        log(f"钉钉通知发送失败: {e}")

def check_gateway():
    """检查 Gateway 是否在运行"""
    try:
        req = urllib.request.Request(GATEWAY_URL)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return True
    except Exception:
        pass
    return False

def kill_gateway_processes():
    """杀掉 Gateway 相关进程"""
    system = platform.system()
    
    if system == "Windows":
        try:
            subprocess.run(["taskkill", "/F", "/IM", "node.exe"], 
                          capture_output=True, timeout=10)
        except Exception:
            pass
    else:  # Linux/Mac
        try:
            # 杀掉所有 node 进程（谨慎使用）
            subprocess.run(["pkill", "-f", "openclaw"], 
                          capture_output=True, timeout=10)
        except Exception:
            pass

def start_gateway():
    """启动 Gateway（使用 --force 强制重启）"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # 使用 --force 强制重启
            subprocess.Popen(
                ["openclaw", "gateway", "--force"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
        else:
            subprocess.Popen(
                ["openclaw", "gateway", "--force"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        return True
    except Exception as e:
        log(f"启动 Gateway 失败: {e}")
        return False

def get_last_check_time():
    """获取上次检查时间（用于每日报平安）"""
    config_file = os.path.join(os.path.expanduser("~"), ".openclaw", "watchdog-config.json")
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                return json.load(f).get("last_daily_notify", 0)
    except Exception:
        pass
    return 0

def save_last_check_time():
    """保存检查时间"""
    config_file = os.path.join(os.path.expanduser("~"), ".openclaw", "watchdog-config.json")
    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "w") as f:
            json.dump({"last_daily_notify": int(time.time())}, f)
    except Exception:
        pass

def should_send_daily():
    """判断是否应该发送每日报平安"""
    last = get_last_check_time()
    now = int(time.time())
    
    # 每天 9 点发送
    current_hour = beijing_now().hour
    
    # 距离上次通知超过 20 小时 且 当前是 8-10 点
    if now - last > 20 * 3600 and 8 <= current_hour <= 10:
        return True
    return False

def main():
    """主函数"""
    log("=" * 50)
    log("OpenClaw Gateway Watchdog 启动")
    log("=" * 50)
    
    # 启动时发送通知
    if NOTIFY_ON_STARTUP:
        send_dingtalk("🦞 [小溪] Gateway Watchdog 已启动！监控中...")
    
    consecutive_failures = 0
    
    while True:
        try:
            if check_gateway():
                log("Gateway is running - OK")
                consecutive_failures = 0
                
                # 每日报平安
                if NOTIFY_DAILY and should_send_daily():
                    send_dingtalk("☀️ [小溪] Gateway 今天也在正常运行！")
                    save_last_check_time()
            else:
                consecutive_failures += 1
                log(f"Gateway is DOWN! (连续失败: {consecutive_failures})")
                
                if NOTIFY_ON_DOWN:
                    send_dingtalk("⚠️ [报警] Gateway 掉线了！正在尝试重启...")
                
                # 杀掉旧进程
                kill_gateway_processes()
                time.sleep(2)
                
                # 启动 Gateway
                start_gateway()
                time.sleep(5)
                
                # 检查是否成功
                if check_gateway():
                    log("Gateway 重启成功")
                    if NOTIFY_ON_RECOVERY:
                        send_dingtalk("✅ [小溪] Gateway 重启成功！")
                else:
                    log("Gateway 重启失败")
                    if NOTIFY_ON_FAILED:
                        send_dingtalk("❌ [报警] Gateway 重启失败！需要人工干预！")
                    
                    # 失败后等待更长时间再重试
                    time.sleep(60)
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            log("收到退出信号，Watchdog 停止")
            break
        except Exception as e:
            log(f"发生错误: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
