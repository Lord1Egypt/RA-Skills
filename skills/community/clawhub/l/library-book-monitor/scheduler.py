import schedule
import time
from typing import Optional
from datetime import datetime
from config import Config
from book_manager import BookManager, Book
from library_scraper import LibraryScraper, ShenzhenLibraryScraper
from notifier import NotificationManager


class BookMonitor:
    """书籍监控器"""

    def __init__(self, config: Config):
        self.config = config
        self.book_manager = BookManager(
            config.storage.get("book_list_file", "book_list.json")
        )
        self.scraper = self._init_scraper()
        self.notifier = NotificationManager(config.notification)
        self.running = False

    def _init_scraper(self) -> LibraryScraper:
        """初始化爬虫"""
        library_name = self.config.library.get("name", "").lower()

        if "深圳" in library_name or "shenzhen" in library_name:
            return ShenzhenLibraryScraper(self.config.library)
        else:
            # 默认使用深圳图书馆爬虫
            print(f"使用默认爬虫: 深圳图书馆")
            return ShenzhenLibraryScraper(self.config.library)

    def check_all_books(self):
        """检查所有书籍状态"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查书籍状态...")

        books = self.book_manager.get_all_books()
        if not books:
            print("书单为空，跳过检查")
            return

        updated_count = 0
        available_count = 0

        for book in books:
            try:
                updated_book, status_changed = self.scraper.update_book_status(book)
                self.book_manager.update_book(updated_book)

                # 显示详细信息
                status = "[可借]" if updated_book.available else "[不可借]"
                print(f"\n  {updated_book.title} {status}")
                if updated_book.author:
                    print(f"    作者: {updated_book.author}")
                if updated_book.isbn:
                    print(f"    ISBN: {updated_book.isbn}")
                if updated_book.locations:
                    print(f"    馆藏位置 ({len(updated_book.locations)} 处):")
                    for i, loc in enumerate(updated_book.locations, 1):
                        print(f"      {i}. {loc}")
                if updated_book.last_checked:
                    print(f"    最后检查: {updated_book.last_checked}")

                if status_changed and updated_book.available:
                    # 状态变为可借，发送提醒
                    print(f"\n    [通知] {updated_book.title} 现在可借了！")
                    if updated_book.monitor:
                        self.notifier.send_book_available(updated_book)
                        available_count += 1

                updated_count += 1

            except Exception as e:
                print(f"\n  - 检查 {book.title} 时出错: {e}")

        print(f"\n检查完成！更新了 {updated_count} 本书，{available_count} 本新书可借")

    def check_monitoring_books(self):
        """仅检查正在监控的书籍"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 检查监控中的书籍...")

        books = self.book_manager.get_monitoring_books()
        if not books:
            print("没有正在监控的书籍")
            return

        for book in books:
            try:
                updated_book, status_changed = self.scraper.update_book_status(book)
                self.book_manager.update_book(updated_book)

                if status_changed and updated_book.available:
                    print(f"\n[通知] {updated_book.title} 现在可借了！")
                    self.notifier.send_book_available(updated_book)

            except Exception as e:
                print(f"\n检查 {book.title} 时出错: {e}")

    def start(self):
        """启动定时任务"""
        if not self.config.scheduler.get("enabled", True):
            print("定时任务未启用")
            return

        interval = self.config.scheduler.get("interval_minutes", 30)
        print(f"启动定时监控，每 {interval} 分钟检查一次...")

        # 先立即执行一次
        self.check_all_books()

        # 设置定时任务
        schedule.every(interval).minutes.do(self.check_monitoring_books)

        self.running = True
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n监控已停止")

    def stop(self):
        """停止监控"""
        self.running = False
