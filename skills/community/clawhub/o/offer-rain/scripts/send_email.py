import smtplib
import mimetypes
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formatdate, make_msgid
from email import encoders
from pathlib import Path

# 所需配置集
CONFIGS_NEEDED = [
    "smtp_server",
    "smtp_port",
    "sender",
    "password",
    "receiver",
    "subject",
    "body",
    "attachment_path",
    "attachment_name"
    ]


def parse_arguments():
    """解析命令行参数。"""
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Send an email")
    parser.add_argument("--config", help="Path to the JSON configuration file")
    # 可选覆盖项：命令行显式传则覆盖 JSON 中的同名字段
    parser.add_argument("--smtp-server", help="SMTP 服务器地址")
    parser.add_argument("--smtp-port", type=int, help="SMTP 端口")
    parser.add_argument("--sender", help="发件人邮箱")
    parser.add_argument("--password", help="发件人密码/授权码")
    parser.add_argument("--receiver", help="收件人邮箱")
    parser.add_argument("--subject", help="邮件主题")
    parser.add_argument("--body", help="邮件正文")
    parser.add_argument("--attachment-path", help="附件路径")
    parser.add_argument("--attachment-name", help="附件重命名")
    return parser.parse_args()


def parse_json(json_path):
    """读取并校验 JSON 配置。"""
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 校验
    if not all(key in data for key in CONFIGS_NEEDED):
        missing_keys = [key for key in CONFIGS_NEEDED if key not in data]
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")
    return data


def sanitize_attachment_name(name):
    """清洗 display name，避免 header injection 与非法字符。"""
    if not name:
        return name
    # 去掉 CR/LF（防 header 注入）和双引号（防属性值逃逸）
    cleaned = name.replace("\r", "").replace("\n", "").replace('"', "")
    # 截断过长文件名（部分邮件服务器限制 255 字符）
    return cleaned[:255] if len(cleaned) > 255 else cleaned


# CLI 覆盖 JSON：CLI 显式传入的字段优先级更高
def merge_config(json_config, cli_args):
    """CLI 显式传入的字段覆盖 JSON 中同名字段。"""
    # argparse Namespace → dict，只保留非 None 字段（未传即为 None）
    overrides = {k: v for k, v in vars(cli_args).items() if v is not None and k != "config"}
    return {**json_config, **overrides}


def create_email(sender, receiver, subject, body, attachment_path, attachment_name=None):
    """构建带附件的邮件对象。"""
    # 创建 multipart 邮件对象
    msg = MIMEMultipart()

    # 构建邮件基本信息
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = Header(subject, "utf-8")
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="163.com")

    # 添加正文
    body_part = MIMEText(body, "plain", "utf-8")
    msg.attach(body_part)

    # 添加附件（自动推导 MIME 类型，未知类型降级为 octet-stream）
    with open(attachment_path, "rb") as f:
        file_data = f.read()
    mime_type, _ = mimetypes.guess_type(attachment_path)
    if mime_type is None:
        maintype, subtype = "application", "octet-stream"
    else:
        maintype, subtype = mime_type.split("/", 1)

    # display name：CLI/JSON 显式传入 > 磁盘文件名
    display_name = sanitize_attachment_name(
        attachment_name or Path(attachment_path).name
    )

    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(file_data)
    encoders.encode_base64(attachment)

    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=Header(display_name, "utf-8").encode(),
    )
    msg.attach(attachment)
    return msg


def send_email(smtp_server, smtp_port, sender, password, receiver, msg, timeout=10):
    """通过 SMTP SSL 发送邮件。"""
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=timeout) as server:
            server.login(sender, password)
            server.sendmail(sender, [receiver], msg.as_string())
        print("邮件发送成功")
    except (smtplib.SMTPException, OSError) as e:
        print(f"发送失败: {e}")
        raise


def main():
    """加载配置并发送邮件。"""
    args = parse_arguments()

    try:
        config_dict = parse_json(args.config)
        # CLI 显式传入的字段覆盖 JSON
        config_dict = merge_config(config_dict, args)
        smtp_server = config_dict["smtp_server"]
        smtp_port = config_dict["smtp_port"]
        sender = config_dict["sender"]
        password = config_dict["password"]
        receiver = config_dict["receiver"]
        subject = config_dict["subject"]
        body = config_dict["body"]
        attachment_path = config_dict["attachment_path"]
        attachment_name = config_dict["attachment_name"]

        msg = create_email(sender, receiver, subject, body, attachment_path, attachment_name)
        send_email(smtp_server, smtp_port, sender, password, receiver, msg)
    except (ValueError, FileNotFoundError) as e:
        # JSONDecodeError 是 ValueError 的子类，一并被捕获
        print(f"配置/文件错误: {e}")
        return 1
    except smtplib.SMTPException as e:
        print(f"SMTP 错误: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
