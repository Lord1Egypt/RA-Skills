#!/usr/bin/env python3
"""
IMAP IDLE 邮件监听脚本（QQ邮箱原生协议适配版）
完全参考IMAP IDLE RFC2177标准 + 参考文章的EXISTS监听逻辑
核心：监听服务器EXISTS数量变化，原生IDLE推送机制
"""

import sys
import io
import imaplib
import email
import json
import time
import ssl
from datetime import datetime
from pathlib import Path
from email.header import decode_header
from typing import Optional, Dict, List

# 修复 Windows 控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 必须安装 imap-tools（兼容原生IMAP命令，支持EXISTS监听）
try:
    from imap_tools import MailBox, AND, MailMessage
    import imaplib
except ImportError:
    print("错误: 请先安装 imap-tools -> pip install imap-tools")
    sys.exit(1)

# ============ 配置项（参考文章优化，贴合IMAP标准） ============
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993
EMAIL = "email@qq.com"
PASSWORD = "******"  # QQ邮箱授权码
# 核心超时配置（参考文章：IMAP服务器30分钟断连，心跳29分钟）
HEARTBEAT_TIMEOUT = 29 * 60  # 29分钟心跳保活（原生IDLE保活）
CHECK_TIMEOUT = 60  # 60秒主动检查（QQ邮箱适配，双重保障）
RECONNECT_DELAY = 5  # 重连延迟
MAX_NOTIFICATIONS = 100  # 最大保留通知数

# 路径配置（跨平台兼容）
BASE_DIR = Path(__file__).parent
NOTIFY_FILE = BASE_DIR.parent / "workspace" / "mail_notifications.json"
LOG_FILE = BASE_DIR / "imap_idle.log"

# ============ 工具函数（保留原有稳定逻辑） ============
def decode_email_header(header_value: str) -> str:
    """解码邮件头，解决中文乱码"""
    if not header_value:
        return ""
    decoded_parts = decode_header(header_value)
    result = []
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(encoding or 'utf-8', errors='replace'))
            except:
                result.append(part.decode('utf-8', errors='replace'))
        else:
            result.append(str(part))
    return ''.join(result)

def log(msg: str, to_console: bool = True):
    """日志写入文件 + 控制台输出，带时间戳"""
    log_msg = f"[{datetime.now().isoformat()}] {msg}"
    if to_console:
        print(log_msg)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{log_msg}\n")
    except Exception as e:
        print(f"日志写入失败: {e}")

def parse_html_to_text(html_content: str, max_length: int = 500) -> str:
    """使用 BeautifulSoup 解析 HTML 为可读纯文本"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除脚本和样式元素
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取纯文本
        text = soup.get_text(separator=' ', strip=True)
        
        # 清理多余空白
        import re
        text = re.sub(r'\s+', ' ', text)  # 多个空格变一个
        text = re.sub(r'\n+', '\n', text)  # 多个换行变一个
        
        return text[:max_length]
    except Exception as e:
        # 降级到简单正则
        import re
        return re.sub('<[^<]+?>', '', html_content)[:max_length]

def get_email_info(msg: MailMessage) -> Dict:
    """提取邮件核心信息，做解码处理"""
    subject = decode_email_header(msg.subject) if msg.subject else "(无主题)"
    from_name = decode_email_header(msg.from_values.name) if msg.from_values.name else ""
    from_email = msg.from_values.email or ""
    
    # 获取邮件正文（优先纯文本，其次 HTML 解析）
    body_text = ""
    try:
        if msg.text:
            # 有纯文本内容
            body_text = msg.text[:500]
        elif msg.html:
            # 有 HTML 内容，解析为纯文本
            body_text = parse_html_to_text(msg.html, 500)
    except Exception as e:
        body_text = "(获取正文失败)"
    
    return {
        'subject': subject,
        'from': {'name': from_name, 'email': from_email},
        'date': msg.date_str or datetime.now().isoformat(),
        'received_at': datetime.now().isoformat(),
        'uid': msg.uid,  # 保留UID，用于去重
        'body': body_text
    }

# 飞书配置（从 openclaw.json 获取）
FEISHU_APP_ID = "******"
FEISHU_APP_SECRET = "******"
FEISHU_USER_ID = "******" 
def get_feishu_token() -> Optional[str]:
    """获取飞书 access token"""
    import urllib.request
    try:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = json.dumps({
            "app_id": FEISHU_APP_ID,
            "app_secret": FEISHU_APP_SECRET
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result['tenant_access_token']
            else:
                log(f"❌ 获取飞书token失败: {result.get('msg')}")
                return None
    except Exception as e:
        log(f"❌ 飞书API请求失败: {e}")
        return None

def send_to_feishu(email_info: Dict):
    """发送邮件通知到飞书"""
    try:
        token = get_feishu_token()
        if not token:
            log("❌ 无法发送飞书通知：获取token失败")
            return
        
        # 构造卡片消息
        subject = email_info['subject']
        from_name = email_info['from']['name'] or email_info['from']['email']
        from_email = email_info['from']['email']
        body = email_info.get('body', '')[:200].replace('\n', ' ')
        
        card_content = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "📧 新邮件通知"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": f"**来自:** {from_name}"}
                },
                {
                    "tag": "div", 
                    "text": {"tag": "plain_text", "content": f"**邮箱:** {from_email}"}
                },
                {
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": f"**主题:** {subject}"}
                },
                {
                    "tag": "div",
                    "text": {"tag": "plain_text", "content": f"**摘要:** {body}"}
                }
            ]
        }
        
        # 发送消息
        import urllib.request
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        data = json.dumps({
            "receive_id": FEISHU_USER_ID,
            "msg_type": "interactive",
            "content": json.dumps(card_content)
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                log(f"✅ 飞书通知发送成功: {subject}")
            else:
                log(f"❌ 飞书发送失败: {result.get('msg')}")
                
    except Exception as e:
        log(f"❌ 发送飞书通知异常: {e}")

def load_notifications() -> List[Dict]:
    """加载已保存的邮件通知"""
    if NOTIFY_FILE.exists():
        try:
            with open(NOTIFY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log(f"加载通知失败: {e}")
            return []
    return []

def save_notifications(notifications: List[Dict]):
    """保存通知，自动创建目录"""
    try:
        NOTIFY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"保存通知失败: {e}")

def add_notification(email_info: Dict):
    """添加新通知，基于UID严格去重"""
    notifications = load_notifications()
    # 按UID去重（比主题+发件人更精准，原生IMAP标识）
    for item in notifications:
        if item.get('uid') == email_info.get('uid'):
            return
    # 新邮件放最前面，保留最新100条
    notifications.insert(0, email_info)
    notifications = notifications[:MAX_NOTIFICATIONS]
    save_notifications(notifications)
    log(f"📧 新邮件触发: {email_info['from']['name']} <{email_info['from']['email']}> - {email_info['subject']}")
    
    # 发送到飞书
    send_to_feishu(email_info)

# ============ 核心：原生IMAP协议校验（参考文章CAPABILITY检查） ============
def check_idle_support(mailbox: MailBox) -> bool:
    """
    校验邮箱是否支持IDLE模式（参考文章第一步：CAPABILITY命令查询）
    QQ邮箱返回的CAPABILITY应包含IDLE，否则直接退出
    """
    try:
        # 执行原生IMAP的CAPABILITY命令
        result = mailbox.client.capability()
        
        # 将整个结果转成字符串来解析
        result_str = str(result)
        log(f"✅ 服务器CAPABILITY返回: {result_str}")
        
        # 检查是否包含 IDLE
        if 'IDLE' in result_str.upper():
            log("✅ 检测到IDLE模式支持，符合QQ邮箱原生特性")
            return True
        else:
            log("❌ 服务器不支持IDLE模式")
            return False
    except Exception as e:
        log(f"❌ 校验IDLE支持失败: {e}")
        return False

# ============ 核心：监听EXISTS数量变化（参考文章IDLE原生机制） ============
def qq_imap_idle_listener():
    """
    QQ邮箱IDLE主监听逻辑，完全参考文章：
    1. 原生IDLE模式监听EXISTS邮件总数变化
    2. 29分钟心跳保活（避免IMAP服务器30分钟断连）
    3. 60秒主动检查（QQ邮箱适配，解决IDLE假死）
    4. 按UID+EXISTS双判断，避免漏检/重检
    """
    last_exists = 0  # 记录上一次的EXISTS数量（文章核心监听项）
    last_uid = None  # 记录上一次的最新UID（双重保障）
    login_time = time.time()  # 记录登录时间，用于心跳检测

    while True:
        mailbox = None
        try:
            # 1. 建立SSL连接，指定超时（贴合原生IMAP）
            log(f"\n📡 开始连接 QQ邮箱 IMAP服务器: {IMAP_SERVER}:{IMAP_PORT}")
            mailbox = MailBox(IMAP_SERVER, IMAP_PORT, timeout=60)
            # 登录并选择收件箱（分开调用，imap-tools API）
            mailbox.login(EMAIL, PASSWORD)
            mailbox.folder.set('INBOX')  # 选择 INBOX 文件夹
            login_time = time.time()  # 重置登录时间
            log("✅ 邮箱登录成功，已选择INBOX收件箱")

            # 2. 校验IDLE支持（参考文章第一步）
            if not check_idle_support(mailbox):
                time.sleep(RECONNECT_DELAY)
                continue

            # 3. 获取初始EXISTS数量和最新UID（初始化基准）
            # 执行原生IMAP SELECT命令，获取邮件数量
            status, response = mailbox.client.select('INBOX', readonly=True)
            if status == 'OK' and response:
                # QQ邮箱返回的是纯数字 [b'1374']，不是 "1374 EXISTS"
                try:
                    last_exists = int(response[0])
                except:
                    last_exists = 0
            
            # 获取最新邮件UID
            all_msgs = list(mailbox.fetch(limit=1, reverse=True, headers_only=True))
            last_uid = all_msgs[0].uid if all_msgs else None
            log(f"✅ 初始化完成 | 初始邮件数量: {last_exists} | 初始最新UID: {last_uid or '无'}")

            # 4. 进入IDLE主循环（参考文章的IdleLoop设计）
            log(f"🚀 进入IDLE监听模式 | 心跳保活: {HEARTBEAT_TIMEOUT//60}分钟 | 主动检查: {CHECK_TIMEOUT}秒")
            log(f"🔍 原生IDLE机制：监听UID变化，有新邮件会触发服务器主动推送")
            while True:
                # 双超时机制：优先60秒主动检查（QQ适配），兜底29分钟心跳（原生保活）
                idle_resp = mailbox.idle.wait(timeout=CHECK_TIMEOUT)
                # 打印IDLE原始响应，方便排查（可看到变化）
                if idle_resp:
                    log(f"⬇️  收到服务器IDLE原始推送: {[r.decode('utf-8', errors='replace') for r in idle_resp]}")

                # 重新获取当前邮件数量和最新UID
                current_exists = 0
                status, response = mailbox.client.select('INBOX', readonly=True)
                if status == 'OK' and response:
                    try:
                        current_exists = int(response[0])
                    except:
                        current_exists = 0
                
                # 获取最新邮件UID
                current_msgs = list(mailbox.fetch(limit=1, reverse=True, headers_only=True))
                current_uid = current_msgs[0].uid if current_msgs else None
                
                log(f"📊 邮件检测 | 数量: {last_exists} -> {current_exists} | UID: {last_uid} -> {current_uid}")

                # 5. 核心判断：UID 变化 → 有新邮件（比 EXISTS 更可靠）
                if current_uid and current_uid != last_uid:
                    log(f"🔥 检测到UID变化，判定有新邮件到达！")
                    # 获取最新的一封邮件（只取1封，避免重复）
                    new_msgs = list(mailbox.fetch(limit=1, reverse=True))
                    for msg in new_msgs:
                        if msg.uid and msg.uid != last_uid:
                            email_info = get_email_info(msg)
                            add_notification(email_info)
                            last_uid = msg.uid  # 立即更新，避免重复
                    last_exists = current_exists
                # 处理数量减少（邮件被删除/移走），重置基准
                elif current_exists < last_exists:
                    log(f"ℹ️  检测到邮件数量减少，邮件被删除/移走，重置基准")
                    last_exists = current_exists
                    last_uid = None  # 重置UID，重新获取

                # 6. 心跳保活：检查是否需要刷新IDLE（避免30分钟断连）
                if (time.time() - login_time) > HEARTBEAT_TIMEOUT:
                    log(f"💓 心跳保活触发：已连接{HEARTBEAT_TIMEOUT//60}分钟，重新建立IDLE连接")
                    break

        except imaplib.IMAP4.abort as e:
            # IMAP服务器主动断连（30分钟超时），正常重连
            log(f"ℹ️  IMAP服务器主动断连（符合30分钟超时规则）: {e}")
        except imaplib.IMAP4.error as e:
            # 登录/命令错误，重连
            log(f"❌ IMAP命令执行错误: {e}")
        except Exception as e:
            # 其他未知错误，打印详细栈信息
            log(f"❌ 监听异常: {e}，错误类型: {type(e).__name__}")
        finally:
            # 确保连接正常关闭，避免资源泄漏
            if mailbox:
                try:
                    mailbox.logout()
                    log("✅ 邮箱连接已正常关闭")
                except:
                    pass
            # 重连前延迟
            if last_exists or last_uid:
                log(f"⏳ {RECONNECT_DELAY}秒后重新建立IDLE连接...\n")
                time.sleep(RECONNECT_DELAY)

# ============ 主函数 ============
def main():
    log("===== QQ邮箱IMAP IDLE监听脚本启动（原生协议适配版） =====")
    log(f"📌 参考IMAP IDLE RFC2177标准 + 原生EXISTS监听机制")
    try:
        qq_imap_idle_listener()
    except KeyboardInterrupt:
        log("===== 用户手动终止，脚本正常退出 =====")
    except SystemExit:
        log("===== 脚本初始化失败，退出 =====")
    except Exception as e:
        log(f"===== 脚本异常退出: {e} =====")

if __name__ == '__main__':
    main()