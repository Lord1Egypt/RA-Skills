---
name: kes-sqlalchemy
name_for_command: kes-sqlalchemy
description: KingbaseES Python 框架集成指南。当用户提到 SQLAlchemy、Django、Python ORM、alembic 迁移金仓时，必须使用此技能。
---

# KingbaseES Python 框架集成指南

本技能指导用户完成 KingbaseES 与 Python 框架的集成，涵盖 SQLAlchemy 和 Django。

## ksycopg2 基础

### 安装

```bash
pip install ksycopg2
```

支持 Python 2.7 和 Python 3.5 ~ 3.13。

### 系统依赖

ksycopg2 依赖 `libkci` 库，需配置环境变量：

```bash
export LD_LIBRARY_PATH=$KINGBASE_HOME/lib:$LD_LIBRARY_PATH
```

### 基本使用

```python
import ksycopg2

conn = ksycopg2.connect(
    database="test",
    user="SYSTEM",
    password="123456",
    host="127.0.0.1",
    port="54321"
)
cur = conn.cursor()
cur.execute("SELECT version()")
print(cur.fetchone()[0])
cur.close()
conn.close()
```

### DSN 连接

```python
conn = ksycopg2.connect("host=127.0.0.1 port=54321 dbname=test user=SYSTEM password=123456")
```

### 高可用连接

```python
conn = ksycopg2.connect(
    host="primary,standby",
    port="54321",
    dbname="test",
    user="SYSTEM",
    password="123456",
    target_session_attrs="read-write"
)
```

## SQLAlchemy

### 配置

```python
from sqlalchemy import create_engine

engine = create_engine("kingbase://SYSTEM:123456@127.0.0.1:54321/test")
```

### ORM 使用

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)

Base.metadata.create_all(engine)
```

## Django

### 数据库配置

在 `settings.py` 中配置。注意：Django 默认不支持 KingbaseES，需使用第三方后端或配置为 PostgreSQL 兼容模式。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.kingbase',
        'NAME': 'test',
        'USER': 'SYSTEM',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '54321',
    }
}
```

### 注意事项

- 验证 Django ORM 生成的 SQL 与 KingbaseES 语法兼容
- 迁移命令可能需要调整
