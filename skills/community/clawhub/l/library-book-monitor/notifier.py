from typing import List
from book_manager import Book


class Notifier:
    """提醒器基类"""

    def send(self, message: str):
        """发送提醒"""
        raise NotImplementedError("子类必须实现 send 方法")

    def send_book_available(self, book: Book):
        """发送书籍可借提醒"""
        message = self._format_available_message(book)
        self.send(message)

    def _format_available_message(self, book: Book) -> str:
        """格式化书籍可借消息"""
        locations_str = (
            "\n  - ".join(book.locations) if book.locations else "暂无位置信息"
        )
        return f"""
[书籍可借提醒]

书名: {book.title}
作者: {book.author}
ISBN: {book.isbn}
可借状态: [可借]
馆藏位置:
  - {locations_str}

查询时间: {book.last_checked}
""".strip()


class ConsoleNotifier(Notifier):
    """控制台提醒器"""

    def send(self, message: str):
        print("\n" + "=" * 50)
        print(message)
        print("=" * 50 + "\n")


class EmailNotifier(Notifier):
    """邮件提醒器"""

    def __init__(self, config: dict):
        self.config = config
        self.smtp_server = config.get("smtp_server", "")
        self.smtp_port = config.get("smtp_port", 587)
        self.sender = config.get("sender", "")
        self.password = config.get("password", "")
        self.recipients = config.get("recipients", [])

    def send(self, message: str):
        if not all([self.smtp_server, self.sender, self.password, self.recipients]):
            print("邮件配置不完整，跳过邮件发送")
            return

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = ", ".join(self.recipients)
            msg["Subject"] = "[图书馆] 书籍可借提醒"

            msg.attach(MIMEText(message, "plain", "utf-8"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            print("邮件提醒发送成功")
        except Exception as e:
            print(f"邮件发送失败: {e}")


class NotificationManager:
    """提醒管理器"""

    def __init__(self, config: dict):
        self.config = config
        self.notifiers: List[Notifier] = []
        self._init_notifiers()

    def _init_notifiers(self):
        """初始化提醒器"""
        methods = self.config.get("methods", ["console"])

        if "console" in methods:
            self.notifiers.append(ConsoleNotifier())

        if "email" in methods and "email" in self.config:
            self.notifiers.append(EmailNotifier(self.config["email"]))

    def send(self, message: str):
        """通过所有渠道发送提醒"""
        for notifier in self.notifiers:
            notifier.send(message)

    def send_book_available(self, book: Book):
        """发送书籍可借提醒"""
        for notifier in self.notifiers:
            notifier.send_book_available(book)
