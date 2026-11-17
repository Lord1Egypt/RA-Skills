# Python 项目结构参考（KingbaseES）

标准的 Python + FastAPI + SQLAlchemy 项目布局，适用于 KingbaseES 集成。

## 目录结构

```
myapp/
├── pyproject.toml
├── requirements.txt
├── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 应用入口
│   ├── config.py                # 配置管理
│   ├── database.py              # KingbaseES 连接
│   ├── models/
│   │   ├── __init__.py
│   │   └── employee.py          # SQLAlchemy ORM 模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── employee.py          # Pydantic 模式
│   ├── api/
│   │   ├── __init__.py
│   │   └── employees.py         # API 路由
│   ├── services/
│   │   ├── __init__.py
│   │   └── employee_service.py  # 业务逻辑
│   └── repositories/
│       ├── __init__.py
│       └── employee_repo.py     # 数据访问
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── 001_init.py
│       └── 002_add_index.py
├── tests/
│   ├── __init__.py
│   └── test_employees.py
└── README.md
```

## requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
ksycopg2==9.0.0
alembic==1.13.0
pydantic==2.5.3
```

## 数据库连接 (database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "kingbase://SYSTEM:123456@localhost:54321/test"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## config.py 示例

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "kingbase://SYSTEM:123456@localhost:54321/test"
    app_name: str = "My KingbaseES App"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```
