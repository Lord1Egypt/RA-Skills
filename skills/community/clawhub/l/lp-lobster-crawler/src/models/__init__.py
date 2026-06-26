"""数据模型模块。"""

from .database import Base, get_engine, get_session, init_db
from .novel import Chapter, Episode, Novel

__all__ = ["Base", "Chapter", "Episode", "Novel", "get_engine", "get_session", "init_db"]
