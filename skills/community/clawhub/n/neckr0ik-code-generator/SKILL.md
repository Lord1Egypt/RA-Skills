---
name: neckr0ik-code-generator
version: 1.0.0
description: Generate boilerplate code for common patterns. Creates project scaffolds, CRUD operations, API clients, database models, tests. Use when you need to quickly scaffold code.
---

# Code Generator

Generate production-ready boilerplate code instantly.

## What This Does

- **Project Scaffolds** — Python, Node.js, Go, Rust project structure
- **CRUD Operations** — Create, Read, Update, Delete boilerplate
- **API Clients** — REST and GraphQL client generators
- **Database Models** — SQLAlchemy, Prisma, TypeORM models
- **Test Templates** — Unit tests, integration tests, mocks
- **Config Files** — Docker, CI/CD, linting, formatting

## Quick Start

```bash
# Generate a new Python project
neckr0ik-code-generator scaffold python my-project

# Generate CRUD operations for a model
neckr0ik-code-generator crud User --fields "name,email,created_at"

# Generate an API client
neckr0ik-code-generator api-client --spec https://api.example.com/openapi.json

# Generate tests
neckr0ik-code-generator tests --source ./src --type unit
```

## Supported Languages

| Language | Scaffold | CRUD | API | Models | Tests |
|----------|----------|------|-----|--------|-------|
| Python | ✅ | ✅ | ✅ | ✅ SQLAlchemy | ✅ pytest |
| TypeScript | ✅ | ✅ | ✅ | ✅ Prisma/TypeORM | ✅ Jest |
| Go | ✅ | ✅ | ✅ | ✅ GORM | ✅ testing |
| Rust | ✅ | ✅ | ✅ | ✅ Diesel | ✅ cargo test |
| Node.js | ✅ | ✅ | ✅ | ✅ Mongoose | ✅ Jest |

## Commands

### scaffold

Create new project structure.

```bash
neckr0ik-code-generator scaffold <language> <name> [options]

Options:
  --template <name>    Template variant (api, web, cli, library)
  --features <list>    Comma-separated features (auth, database, tests, ci)
  --output <dir>       Output directory
```

### crud

Generate CRUD operations.

```bash
neckr0ik-code-generator crud <ModelName> [options]

Options:
  --fields <list>      Comma-separated field definitions (name:type)
  --language <lang>    Target language (default: python)
  --database <type>    Database type (sql, mongodb, postgresql)
  --output <dir>       Output directory
```

### api-client

Generate API client from spec.

```bash
neckr0ik-code-generator api-client [options]

Options:
  --spec <url>         OpenAPI spec URL or file
  --language <lang>    Target language (default: python)
  --output <dir>       Output directory
```

### model

Generate database model.

```bash
neckr0ik-code-generator model <ModelName> [options]

Options:
  --fields <list>      Comma-separated field definitions
  --orm <name>         ORM (sqlalchemy, prisma, typeorm, gorm)
  --migrations         Generate migration files
  --output <dir>       Output directory
```

### test

Generate test templates.

```bash
neckr0ik-code-generator test [options]

Options:
  --source <dir>       Source directory to analyze
  --type <type>        Test type (unit, integration, e2e)
  --framework <name>   Test framework (pytest, jest, testing)
  --output <dir>       Output directory
```

### config

Generate configuration files.

```bash
neckr0ik-code-generator config <type> [options]

Types:
  docker       Dockerfile and docker-compose
  ci           CI/CD pipeline (GitHub Actions, GitLab CI)
  lint         Linting config (eslint, ruff, golangci-lint)
  format       Formatting config (prettier, black, gofmt)

Options:
  --language <lang>   Target language
  --output <dir>       Output directory
```

## Generated Code Quality

- **Type-safe** — Full type annotations where supported
- **Documented** — Docstrings and comments
- **Tested** — Example tests included
- **Modern** — Latest patterns and best practices
- **Clean** — Readable, maintainable code

## Example: Python CRUD

```python
# Generated: user_crud.py

from typing import List, Optional
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate

class UserCRUD:
    """CRUD operations for User model."""

    def create(self, db: Session, user: UserCreate) -> User:
        """Create a new user."""
        db_user = User(
            name=user.name,
            email=user.email,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get(self, db: Session, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get multiple users."""
        return db.query(User).offset(skip).limit(limit).all()

    def update(self, db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
        """Update a user."""
        db_user = self.get(db, user_id)
        if db_user:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    def delete(self, db: Session, user_id: int) -> bool:
        """Delete a user."""
        db_user = self.get(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
```

## Use Cases

- **New Projects** — Start with production-ready structure
- **Rapid Prototyping** — Generate boilerplate, focus on logic
- **Code Reviews** — Generate consistent code patterns
- **Learning** — Study generated code for best practices

## Templates

Templates are stored in `references/templates/`:
- `python/api/` — Python FastAPI project
- `python/cli/` — Python CLI tool
- `typescript/api/` — Node.js Express API
- `typescript/web/` — React + TypeScript web app
- `go/api/` — Go REST API
- `rust/cli/` — Rust CLI tool

## See Also

- `references/templates/` — Code templates
- `scripts/generator.py` — Main generator