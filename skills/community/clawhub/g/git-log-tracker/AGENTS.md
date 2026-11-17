<!-- kinema-tdd-injector: injected -->
<!-- generated at: 2026-06-01 | packages: src (Python) -->

# 研发自动化测试规范 (CLAUDE.md)

> 适用对象：Claude Code 编码代理 + 前后端研发团队
> 由 `kinema-tdd-injector` skill 生成

---

## 1. 核心原则

本项目采用 **三阶测试体系**，按运行环境隔离：

| 阶段       | src 目录                            | 执行者          | 外部依赖          |
| -------- | ------------------ | ------------ | ------------- |
| 单元测试     | `tests/unit/src/`            | Agent 自动 / 本地 | ❌ 无           |
| 开发环境集成测试 | `tests/dev-integration/src/` | Agent 自动 / 本地 | ❌ 无（Mock / MSW） |
| 测试环境集成测试 | `tests/testenv-integration/src/` | **用户手动**     | ✅ 真实数据库       |


---

## 2. 测试路径三层命名规则

测试路径由三层组合而成，**逐层强制**：

| 层 | 规则 |
| - | - |
| **阶段层** | 测试根必为 `tests/unit/`、`tests/dev-integration/`、`tests/testenv-integration/` |
| **包层** | 阶段根的下一级必为仓库顶层应用包名（本项目：`src/`）。新增顶层应用包时**必须**在所有阶段根下同步建立同名目录 |
| **模块层** | 包名目录下的子目录与该包源码内部结构 **1:1 对齐**，不得压缩或省略中间目录 |

### 2.1 源码根直接镜像

本项目为 **flat src 布局**：源码模块平铺在 `src/` 下（无内层应用包目录），测试树直接镜像 `src/` 内的结构，**不再多套一层目录**：

```
src/db.py      → tests/unit/src/test_db.py        ✅
src/models.py  → tests/unit/src/test_models.py    ✅
src/cli.py     → tests/unit/src/test_cli.py       ✅
```

若将来 `src/` 下出现子包（如 `src/service/`），按 §2.2 规则继续镜像：`src/service/task_service.py → tests/unit/src/service/test_task_service.py`。`src/migrations/` 下的迁移脚本按 §7.3 排除，不强制测试。

### 2.2 文件命名规则

| 语言 | 源 | 测试 |
| - | - | - |
| **Python** | `<pkg-source-root>/<path>/<module>.py` | `tests/<阶段>/<pkg>/<path>/test_<module>.py` |
| **TS/TSX** | `<pkg-source-root>/<path>/<Name>.ts(x)` | `tests/<阶段>/<pkg>/<path>/<Name>.test.ts(x)` |

**强制约束**：
- Python 测试名 = `test_` + **完整**源文件名（包括 `_router` / `_service` / `_dao` 等后缀），不许缩写、不许用功能名替代
- TS 测试名 = **原始大小写**源文件名 + `.test`（PascalCase 组件保持 PascalCase，camelCase hook 保持 camelCase）
- Python 与 TS 命名规范不同，是为了贴合各自社区工具链（pytest 默认匹配 `test_*`、vitest 默认匹配 `*.test.*`）

### 2.3 归属判定原则

测试归到哪个子目录，**只看源文件物理位置**，与功能语义、模块名含义无关：

- `models/fts.py`（FTS 是搜索功能） → `models/`，**不归** `service/` 或 `search/`
- 包根 `main.py`（FastAPI 入口等） → 包根 `tests/<阶段>/<pkg>/test_main.py`
- `core/lifespan.py`（启动钩子） → `core/`

### 2.4 测试文件拆分规则（C+D 组合）

测试**原则上单文件**，用 `class`（Python）/ `describe`（TS）分组：

```python
# tests/unit/src/service/test_task_service.py
class TestCreate: ...
class TestQuery: ...
class TestDelete: ...
```

若单测试文件超过 **800 行**仍难维护，**先考虑拆源码**（源文件已职责过载），源码拆完测试自动 1:1 跟随。**禁止单独拆测试文件而源码不动**。

### 2.5 测试数据文件

非测试代码的辅助数据（JSON / CSV / SQL dump / 图片）一律放 `tests/data/`，按所属测试路径再镜像：

```
tests/data/src/service/task_service/large_input.json
```

- `tests/data/` 不放任何 `*.py` / `*.ts` 测试代码
- 超大 fixture（GB 级 sample）走 LFS 或外部存储，**不进 git**

---

## 3. Agent 自动行为规范

### 3.1 完成以下任务后，必须自动运行测试

- bug 修复后
- 新功能开发完成
- 重构导致接口变更

### 3.2 自动运行的命令序列

**后端**（工作目录：`src/`）：

```bash
cd src
uv run pytest ../tests/unit/src/ -v
uv run pytest ../tests/dev-integration/src/ -v
```


**激活规则**：一律使用 `uv run`（自动管理 venv），**禁止**在命令前添加 `source .venv/bin/activate` 或 `.venv\Scripts\Activate.ps1`。

**准入规则**：自动触发的阶段必须 **100% 通过** + 覆盖率达标，否则不得提交代码。

### 3.3 测试环境集成测试（不自动运行）

代码提交并部署到测试服务器后，Agent 应**生成以下指令并提示用户手动执行**：

```
✅ 代码已推送。请在测试服务器上手动执行后端冒烟测试：

  cd src && uv run pytest ../tests/testenv-integration/src/ -v
```

Agent **不得**自行执行 `tests/testenv-integration/` 下的任何测试（本地无数据库连接权限，必然报错）。

---

## 4. 网络边界规则

**原则**：**进程内（in-process）随便用，进程外（out-of-process）一律禁。**

**磁盘写入不计入"进程外 I/O"** —— 文件读写、本地 SQLite 文件、临时目录都属于进程内允许范围。

### 4.1 允禁对照表

| 行为 | unit | dev-integration | testenv-integration |
| - | - | - | - |
| `fastapi.TestClient` / `httpx.ASGITransport` | ✅ | ✅ | ✅ |
| `unittest.mock` / `pytest-mock` | ✅ | ✅ | ✅ |
| MSW（前端进程内拦截） | ✅ | ✅ | — |
| 文件读写 / 临时目录 | ✅ | ✅ | ✅ |
| SQLite `:memory:` | ✅ | ✅ | ✅ |
| SQLite 本地文件 | ✅ | ✅ | ✅ |
| 连真实数据库（MySQL/PG 等远程） | ❌ | ❌ | ✅ |
| 真实 HTTP 出栈（requests/urllib/未 mock httpx） | ❌ | ❌ | ✅ |
| DNS 解析非 localhost | ❌ | ❌ | ✅ |
| subprocess 启动网络服务 | ❌ | ❌ | ✅ |

---

## 5. 依赖声明

### 5.1 声明源（唯一手改入口）

- **后端**：`src/pyproject.toml` 的 `[project.dependencies]` 与 `[project.optional-dependencies]`

### 5.2 派生锁定文件（命令生成，禁止手改）

| 文件 | 用途 |
| - | - |
| `src/requirements.txt` | 主依赖 pin 版本（pip 兼容兜底） |
| `src/requirements-test.txt` | test+dev 组 pin 版本 |
| `src/uv.lock` | uv 完整解析锁 |

**全部 lockfile 必须 commit 进 git。**

### 5.3 改后端依赖的流程

1. 编辑 `src/pyproject.toml`
2. 在 `src/` 下重生派生文件：
   ```bash
   uv pip compile pyproject.toml -o requirements.txt
   uv pip compile pyproject.toml --extra test --extra dev -o requirements-test.txt
   uv lock
   ```
3. 将 `pyproject.toml` + 两份 `requirements*.txt` + `uv.lock` 一并 commit

**禁止**：跳过 step 2、单独手改 `requirements*.txt`、用 `pip freeze` 凑 requirements。

### 5.4 环境初始化

```bash
cd src && uv pip install -e ".[test,dev]"
```

---

## 6. Conftest / Fixture 治理（方案 B）

### 6.1 Fixture 分层

| 文件 | 职责 |
| - | - |
| `tests/conftest.py` | **跨阶段通用数据 fixture**：`mock_<entity>` 系列（ORM-shape MagicMock，字段统一） |
| `tests/unit/src/conftest.py` | unit 特化：`mock_session`（基础 AsyncMock） |
| `tests/dev-integration/src/conftest.py` | dev-integration 特化：`mock_db_session`、`client_with_mock_db`（TestClient + dependency override） |
| `tests/testenv-integration/src/conftest.py` | testenv-integration 特化：`real_db_session` 等真库 fixture |

### 6.2 Fixture 命名约定

- **跨阶段同语义 fixture 必须同名**（如 `mock_task` 不再有 `mock_task_row` 双胞胎）
- 阶段特化的会话/客户端 fixture 可以分别命名（`mock_session` vs `mock_db_session` 反映了不同上下文的真实差异）

### 6.3 Fixture 定义位置

- **默认**：所有 fixture 定义在对应层的 `conftest.py`
- **例外**：仅当某 fixture **只服务一个测试文件**时，允许在该测试文件内 inline `@pytest.fixture`
- **禁止**：在测试文件内定义需跨文件共享的 fixture（应上提到 conftest）

---

## 7. 覆盖率门槛

### 7.1 阈值

| 范围 | 总覆盖率 | 每文件兜底 |
| - | - | - |
| 后端 | ≥ 80% | ≥ 50% |

### 7.2 计入测试阶段

- **计入**：`unit/` + `dev-integration/`
- **不计入**：`testenv-integration/`（本地跑不了，CI 也未必连得上真库）

### 7.3 排除文件

- 后端：`src/__init__.py` 及各子包 `__init__.py`、未来的 alembic 迁移脚本

### 7.4 强制点：本地 git hook（双触发）

| Hook | 触发 | 跑什么 |
| - | - | - |
| `pre-commit` | 每次 `git commit` | 快速通道：lint + 单元测试（≤ 10s） |
| `pre-push` | 每次 `git push` | 全套：单元 + 集成 + 覆盖率校验 |

**禁止**用 `git commit --no-verify` / `git push --no-verify` 绕过，除非已修复底层问题。

hook 脚本镜像位于 `scripts/git-hooks/`，由 `init_env` 软链到 `.git/hooks/`，否则新 clone 的同事不会自动获得 hook。

---

## 8. 各阶段测试编写规范

### 8.1 单元测试（阶段一）

- **时机**：编码前或编码中（TDD 优先）
- **工具**：`pytest` + `unittest.mock` / `pytest-mock`；前端 `vitest` + `@testing-library/react`
- **禁止**：任何进程外 I/O（详见 §4）

按以下三层从底向上验证：

#### 8.1.1 模型 / 函数层

```python
# tests/unit/src/models/test_task.py
from src.models import Task

class TestTaskModel:
    def test_table_name(self):
        assert Task.__tablename__ == "tasks"
```

#### 8.1.2 服务层逻辑

```python
# tests/unit/src/service/test_task_service.py
from unittest.mock import MagicMock
from src.service.task_service import TaskService

class TestCreate:
    def test_create_returns_task(self):
        service = TaskService(dao=MagicMock())
        ...
```

#### 8.1.3 接口层契约（TestClient + 全 mock Service）

```python
# tests/unit/src/api/test_task_router.py
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@patch("src.service.task_service.TaskService.get_task")
def test_get_task_endpoint(mock_service):
    mock_service.return_value = {"id": "t001", "title": "X"}
    response = client.get("/tasks/t001")
    assert response.status_code == 200
```

### 8.2 开发环境集成测试（阶段二）

- **时机**：模块开发完成、提交前
- **工具**：`pytest` + `unittest.mock.patch` 拦截 DAO 层；或 TestClient + dependency override
- **测什么**：Controller → Service → DAO 完整调用链路

### 8.3 测试环境集成测试（阶段三）

- **时机**：代码部署到测试服务器后
- **工具**：`pytest`，直连测试数据库（无 Mock）
- **测什么**：真实 SQL、ORM 映射、事务回滚、唯一索引约束
- **运行方式**：用户在测试服务器手动执行

---

## 9. 快速参考

```bash
# 后端开发中（Agent 自动触发）
cd src
uv run pytest ../tests/unit/src/ -v
uv run pytest ../tests/dev-integration/src/ -v


# 部署后冒烟（用户手动，在测试服务器）
cd src && uv run pytest ../tests/testenv-integration/src/ -v
```

---

## 10. Commit Message 规范

### 10.1 标题格式

格式：`<type>(<scope>): <subject>`

**type**：`feat`（新功能）/ `fix`（修补 bug）/ `docs`（文档）/ `style`（格式）/ `refactor`（重构）/ `test`（测试）/ `chore`（构建/工具）

**scope**：模块级（如 `api`、`dao`、`service`、`models`、`schemas`、`core`、`utils`）或跨模块（用逗号，如 `api, service`）

**subject**：
- 使用**中文**
- 结尾不加句号
- 简洁明确

### 10.2 正文

- 与标题空一行
- **中文**详述，列表用 `-` 或 `*`
- 复杂提交分小标题：主要改进 / 影响范围 / 变更细节

### 10.3 脚注

AI 辅助完成需署名：

```
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

