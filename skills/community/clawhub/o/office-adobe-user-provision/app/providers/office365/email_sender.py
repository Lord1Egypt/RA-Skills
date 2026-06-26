"""
邮件发送模块
使用 SMTP 发送邮件（支持飞书邮箱）
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

logger = logging.getLogger(__name__)


class EmailSender:
    """使用 SMTP 发送邮件"""
    
    def __init__(self, smtp_config: dict):
        """
        初始化 EmailSender
        
        Args:
            smtp_config: SMTP 配置字典，包含 host, port, username, password, use_ssl
        """
        self.smtp_host = smtp_config.get('smtp_host')
        self.smtp_port = smtp_config.get('smtp_port', 465)
        self.smtp_username = smtp_config.get('smtp_username')
        self.smtp_password = smtp_config.get('smtp_password')
        self.smtp_use_ssl = smtp_config.get('smtp_use_ssl', True)
    
    def send_email(self, from_email: str, to_recipients: list, subject: str, body: str,
                   bcc_recipients: list = None, body_type: str = 'html') -> bool:
        """
        发送邮件
        
        Args:
            from_email: 发件人邮箱
            to_recipients: 收件人列表
            subject: 邮件主题
            body: 邮件正文
            bcc_recipients: 密送列表（可选）
            body_type: 正文类型，'html' 或 'plain'，默认为 'html'
        
        Returns:
            bool: 发送成功返回 True
        """
        if not self.smtp_host or not self.smtp_username or not self.smtp_password:
            logger.error("SMTP 配置不完整，无法发送邮件")
            raise ValueError("SMTP 配置不完整")
        
        try:
            # 创建邮件对象
            msg = MIMEMultipart('alternative')
            msg['From'] = from_email
            msg['To'] = ', '.join(to_recipients)
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加邮件正文
            content_type = 'html' if body_type.lower() == 'html' else 'plain'
            msg.attach(MIMEText(body, content_type, 'utf-8'))
            
            # 添加密送（BCC）
            if bcc_recipients:
                msg['Bcc'] = ', '.join(bcc_recipients)
            
            # 连接 SMTP 服务器并发送
            logger.info(f"连接 SMTP 服务器: {self.smtp_host}:{self.smtp_port}")
            
            if self.smtp_use_ssl:
                # 使用 SSL
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                # 使用 STARTTLS
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            
            # 登录
            server.login(self.smtp_username, self.smtp_password)
            
            # 发送邮件（收件人 + 密送）
            all_recipients = to_recipients + (bcc_recipients if bcc_recipients else [])
            server.sendmail(from_email, all_recipients, msg.as_string())
            server.quit()
            
            logger.info(f"成功发送邮件: 从 {from_email} 到 {to_recipients}")
            if bcc_recipients:
                logger.info(f"密送: {bcc_recipients}")
            
            return True
            
        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            raise


def convert_email_domain(email: str, target_domain: str) -> str:
    """
    转换邮箱域名
    
    Args:
        email: 原始邮箱地址（如 testuser01@example.partner.onmschina.cn）
        target_domain: 目标域名（必需，如 example.com）
    
    Returns:
        str: 转换后的邮箱地址（如 testuser01@example.com）
    """
    if '@' not in email:
        return email
    
    username = email.split('@')[0]
    return f"{username}@{target_domain}"

