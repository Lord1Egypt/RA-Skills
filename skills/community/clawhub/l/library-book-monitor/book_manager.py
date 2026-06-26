import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class Book:
    """书籍类"""

    def __init__(
        self,
        title: str = "",
        isbn: str = "",
        author: str = "",
        book_id: Optional[str] = None,
    ):
        self.book_id = book_id or self._generate_id()
        self.title = title
        self.isbn = isbn
        self.author = author
        self.available: bool = False
        self.locations: List[str] = []
        self.last_checked: Optional[str] = None
        self.monitor: bool = False

    def _generate_id(self) -> str:
        """生成书籍ID"""
        import uuid

        return str(uuid.uuid4())[:8]

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "isbn": self.isbn,
            "author": self.author,
            "available": self.available,
            "locations": self.locations,
            "last_checked": self.last_checked,
            "monitor": self.monitor,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """从字典创建书籍对象"""
        book = cls(
            title=data.get("title", ""),
            isbn=data.get("isbn", ""),
            author=data.get("author", ""),
            book_id=data.get("book_id"),
        )
        book.available = data.get("available", False)
        book.locations = data.get("locations", [])
        book.last_checked = data.get("last_checked")
        book.monitor = data.get("monitor", False)
        return book


class BookManager:
    """书单管理器"""

    def __init__(self, file_path: str = "book_list.json"):
        self.file_path = Path(file_path)
        self.books: Dict[str, Book] = {}
        self._load_books()

    def _load_books(self):
        """加载书单"""
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for book_data in data.get("books", []):
                        book = Book.from_dict(book_data)
                        self.books[book.book_id] = book
            except (json.JSONDecodeError, KeyError):
                pass

    def _save_books(self):
        """保存书单"""
        data = {"books": [book.to_dict() for book in self.books.values()]}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_book(self, book: Book) -> Tuple[str, bool]:
        """添加书籍，已存在则更新
        返回: (book_id, is_new)
        """
        # 检查是否已存在相同书籍（通过ISBN或标题+作者）
        existing_book = self._find_existing_book(book)
        if existing_book:
            # 更新现有书籍
            existing_book.title = book.title or existing_book.title
            existing_book.isbn = book.isbn or existing_book.isbn
            existing_book.author = book.author or existing_book.author
            existing_book.monitor = book.monitor  # 监控状态按新的设置
            self._save_books()
            return existing_book.book_id, False  # 不是新的

        # 添加新书籍
        self.books[book.book_id] = book
        self._save_books()
        return book.book_id, True  # 是新的

    def _find_existing_book(self, book: Book) -> Optional[Book]:
        """查找是否已存在相同书籍"""
        for existing_book in self.books.values():
            # 如果有ISBN，优先用ISBN匹配
            if book.isbn and existing_book.isbn == book.isbn:
                return existing_book
            # 否则用标题匹配
            if book.title and existing_book.title == book.title:
                return existing_book
        return None

    def remove_book(self, book_id: str) -> bool:
        """移除书籍"""
        if book_id in self.books:
            del self.books[book_id]
            self._save_books()
            return True
        return False

    def get_book(self, book_id: str) -> Optional[Book]:
        """获取书籍"""
        return self.books.get(book_id)

    def get_all_books(self) -> List[Book]:
        """获取所有书籍"""
        return list(self.books.values())

    def get_monitoring_books(self) -> List[Book]:
        """获取正在监控的书籍"""
        return [book for book in self.books.values() if book.monitor]

    def update_book(self, book: Book):
        """更新书籍信息"""
        if book.book_id in self.books:
            self.books[book.book_id] = book
            self._save_books()

    def toggle_monitor(self, book_id: str) -> Optional[bool]:
        """切换监控状态"""
        book = self.get_book(book_id)
        if book:
            book.monitor = not book.monitor
            self._save_books()
            return book.monitor
        return None
