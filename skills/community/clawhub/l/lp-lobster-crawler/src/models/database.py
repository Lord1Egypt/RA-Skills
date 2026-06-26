"""数据库连接与初始化。"""

import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """ORM 基类。"""
    pass


def get_db_path() -> str:
    """获取数据库文件路径。"""
    return os.environ.get("DB_PATH", "data/lobster.db")


def get_engine(db_path: str | None = None):
    """创建 SQLAlchemy Engine。

    Args:
        db_path: 数据库文件路径，为 None 时从环境变量读取。
    """
    path = db_path or get_db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{path}", echo=False)

    # 启用 SQLite 外键约束
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def init_db(db_path: str | None = None) -> Session:
    """初始化数据库：建表并返回 Session。

    Args:
        db_path: 数据库文件路径。

    Returns:
        一个可用的 Session 实例。
    """
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return session_factory()


def get_session(db_path: str | None = None) -> Session:
    """获取数据库 Session。

    Args:
        db_path: 数据库文件路径。

    Returns:
        一个可用的 Session 实例。
    """
    engine = get_engine(db_path)
    session_factory = sessionmaker(bind=engine)
    return session_factory()
