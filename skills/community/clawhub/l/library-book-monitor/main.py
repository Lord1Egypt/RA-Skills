#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图书馆借书查询系统
- 查询书籍可借状态
- 定时监控不可借书籍
- 可借时提醒用户
"""

import sys
import io
import argparse

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from config import Config
from book_manager import BookManager, Book
from scheduler import BookMonitor


def add_book(
    config: Config,
    title: str = "",
    isbn: str = "",
    author: str = "",
    monitor: bool = False,
):
    """添加书籍"""
    book_manager = BookManager(config.storage.get("book_list_file", "book_list.json"))

    book = Book(title=title, isbn=isbn, author=author)
    book.monitor = monitor

    book_id, is_new = book_manager.add_book(book)
    if is_new:
        print(f"[OK] 已添加书籍: {book.title}")
    else:
        print(f"[OK] 书籍已存在，已更新: {book.title}")
    print(f"   书籍ID: {book_id}")
    print(f"   监控状态: {'开启' if monitor else '关闭'}")


def list_books(config: Config):
    """列出所有书籍"""
    book_manager = BookManager(config.storage.get("book_list_file", "book_list.json"))
    books = book_manager.get_all_books()

    if not books:
        print("书单为空")
        return

    print(f"\n书单 ({len(books)} 本书):")
    print("-" * 80)

    for i, book in enumerate(books, 1):
        status = "[可借]" if book.available else "[不可借]"
        monitor = "[监控中]" if book.monitor else "       "

        print(f"\n{i}. {monitor} {status} {book.title}")
        print(f"   ID: {book.book_id}")
        if book.author:
            print(f"   作者: {book.author}")
        if book.isbn:
            print(f"   ISBN: {book.isbn}")
        if book.locations:
            print(f"   馆藏位置 ({len(book.locations)} 处):")
            for j, loc in enumerate(book.locations, 1):
                print(f"     {j}. {loc}")
        if book.last_checked:
            print(f"   最后检查: {book.last_checked}")
    print("-" * 80)


def remove_book(config: Config, book_id: str):
    """移除书籍"""
    book_manager = BookManager(config.storage.get("book_list_file", "book_list.json"))

    if book_manager.remove_book(book_id):
        print(f"[OK] 已移除书籍: {book_id}")
    else:
        print(f"[ERROR] 未找到书籍: {book_id}")


def toggle_monitor(config: Config, book_id: str):
    """切换监控状态"""
    book_manager = BookManager(config.storage.get("book_list_file", "book_list.json"))
    status = book_manager.toggle_monitor(book_id)

    if status is not None:
        book = book_manager.get_book(book_id)
        print(f"[OK] {book.title} 监控状态: {'开启' if status else '关闭'}")
    else:
        print(f"[ERROR] 未找到书籍: {book_id}")


def check_now(config: Config):
    """立即检查所有书籍"""
    monitor = BookMonitor(config)
    monitor.check_all_books()


def start_monitor(config: Config):
    """启动监控"""
    monitor = BookMonitor(config)
    monitor.start()


def main():
    parser = argparse.ArgumentParser(
        description="图书馆借书查询系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py add --title "Python编程" --author "Guido" --monitor
  python main.py list
  python main.py check
  python main.py monitor
        """,
    )

    subparsers = parser.add_subparsers(title="命令", dest="command")

    # 添加书籍
    add_parser = subparsers.add_parser("add", help="添加书籍")
    add_parser.add_argument("--title", "-t", default="", help="书名")
    add_parser.add_argument("--isbn", "-i", default="", help="ISBN")
    add_parser.add_argument("--author", "-a", default="", help="作者")
    add_parser.add_argument("--monitor", "-m", action="store_true", help="开启监控")

    # 列出书籍
    subparsers.add_parser("list", help="列出所有书籍")

    # 移除书籍
    remove_parser = subparsers.add_parser("remove", help="移除书籍")
    remove_parser.add_argument("book_id", help="书籍ID")

    # 切换监控
    monitor_parser = subparsers.add_parser("toggle", help="切换书籍监控状态")
    monitor_parser.add_argument("book_id", help="书籍ID")

    # 立即检查
    subparsers.add_parser("check", help="立即检查所有书籍状态")

    # 启动监控
    subparsers.add_parser("monitor", help="启动定时监控")

    args = parser.parse_args()

    # 加载配置
    try:
        config = Config()
    except FileNotFoundError as e:
        print(f"[ERROR] 错误: {e}")
        print("请复制 config.yaml.example 到 config.yaml 并修改配置")
        sys.exit(1)

    # 执行命令
    if args.command == "add":
        if not any([args.title, args.isbn, args.author]):
            print("[ERROR] 请至少提供书名、ISBN或作者之一")
            sys.exit(1)
        add_book(config, args.title, args.isbn, args.author, args.monitor)

    elif args.command == "list":
        list_books(config)

    elif args.command == "remove":
        remove_book(config, args.book_id)

    elif args.command == "toggle":
        toggle_monitor(config, args.book_id)

    elif args.command == "check":
        check_now(config)

    elif args.command == "monitor":
        start_monitor(config)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
