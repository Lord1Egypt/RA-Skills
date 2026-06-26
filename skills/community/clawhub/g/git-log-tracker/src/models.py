from sqlalchemy import Column, Integer, Text, text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Commit(Base):
    __tablename__ = "commits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    commit_hash = Column(Text, nullable=False, unique=True)
    short_hash = Column(Text, nullable=False)
    author_name = Column(Text, nullable=False)
    author_email = Column(Text, nullable=False)
    author_ts = Column(Text, nullable=False)
    committer_name = Column(Text)
    committer_email = Column(Text)
    commit_subject = Column(Text, nullable=False)
    commit_body = Column(Text)
    branch = Column(Text)
    repo_path = Column(Text, nullable=False)
    repo_name = Column(Text, nullable=False)
    parent_hashes = Column(Text)
    recorded_at = Column(Text, nullable=False, server_default=text("datetime('now')"))
