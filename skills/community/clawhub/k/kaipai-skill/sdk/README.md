# Kaipai AI SDK

面向美图开拍算法能力的 Python SDK：拉配置、上传 OSS、消费权益、提交任务、轮询结果。适合在脚本、服务或 Agent 里嵌入调用。

---

## 1. 安装

在项目根目录（包含 `sdk/` 的那一层）执行：

```bash
pip install requests alibabacloud-oss-v2
```

代码里使用本 SDK 时，需保证 **Python 能找到 `sdk` 包**，任选其一即可：

- 在仓库根目录运行，并把根目录加入模块搜索路径，例如：  
  `export PYTHONPATH="/path/to/repo/root:$PYTHONPATH"`  
  或与下文 CLI 一样在根目录执行 `python3 -c "from sdk import SkillClient"`。
- 若你在其他项目中引用，可将本仓库根目录加入 `PYTHONPATH`，或自行用 `pyproject.toml` / `setup.cfg` 做可编辑安装。

---

## 2. 凭证与安全

| 方式 | 说明 |
|------|------|
| **推荐** | `export MT_AK=...` 和 `export MT_SK=...`（或写入 `.env` 后由你的启动方式注入） |
| 不推荐 | 在命令行写 `--ak` / `--sk`：会出现在 `ps`、shell 历史里 |

初始化失败时会抛出 `ValueError: AK and SK required`。

---

## 3. 命令行（`sdk/cli.py`）

在**仓库根目录**执行，使 `sdk` 可被导入：

```bash
cd /path/to/action-web-skill   # 换成你的仓库根路径
export MT_AK="你的 AK"
export MT_SK="你的 SK"
```

### 3.1 常用命令

| 子命令 | 作用 |
|--------|------|
| `run-task` | 一站式：下载（若 `--input` 为 URL）→ 上传 → 消费 → 提交 → 轮询 |
| `query-task` | 用已有 `task_id` 继续查状态（适合异步任务断线续查） |
| `list-tasks` | 打印当前配置里可用的任务预设（名称与参数模板） |

### 3.2 示例

```bash
# 跑一个图片任务（本地文件）
python3 sdk/cli.py run-task --task eraser_watermark --input ./photo.jpg

# 输入为公网 URL
python3 sdk/cli.py run-task --task eraser_watermark --input "https://example.com/in.jpg"

# 覆盖/补充任务参数（JSON 字符串，会与预设里的 params 深度合并）
python3 sdk/cli.py run-task --task eraser_watermark --input ./photo.jpg \
  --params '{"parameter":{"rsp_media_type":"url"}}'

# 异步任务提交后拿到 task_id，稍后续查
python3 sdk/cli.py query-task --task-id "<full_task_id>"

# 查看有哪些 --task 名称可用
python3 sdk/cli.py list-tasks
```

### 3.3 输出与退出码

- **标准输出**：一条 JSON（UTF-8，`ensure_ascii=False`）。
- **退出码**：成功为 `0`，失败为 `1`。成功判定为：无 `error`、非 `skill_status: failed`，且存在有效结果（例如 `output_urls` 非空，或 `data.status` 为已完成的业务状态）。

配额类错误会输出形如 `{"error":"quota_error","code":...,"message":...}`。

### 3.4 与 `scripts/kaipai_ai.py` 的区别

仓库里的 `scripts/kaipai_ai.py` 是**功能更全**的 Agent/运维 CLI（如 `resolve-input`、`notify`、`history` 等）。**本目录的 `sdk/cli.py` 是精简入口**，只覆盖 `run-task` / `query-task` / `list-tasks`，适合快速联调或最小依赖场景。

---

## 4. Python 代码

### 4.1 最小示例（`SkillClient`）

```python
import os
from sdk import SkillClient

# 使用环境变量 MT_AK / MT_SK
client = SkillClient()

# 或显式传入（注意不要把真实密钥写进仓库）
# client = SkillClient(ak="...", sk="...", region="cn-north-4")

result = client.execute(
    task_name="eraser_watermark",
    source="/path/to/image.jpg",  # 或 "https://..."
)

# 成功时通常会有 output_urls、task_id，以及网关返回的 data/meta
urls = result.get("output_urls") or []
print("task_id:", result.get("task_id"))
print("first url:", urls[0] if urls else None)
```

### 4.2 异步：拿到 `task_id` 再轮询

长任务会先进入异步，可在提交后立即得到 `task_id`，再用 `query` 轮询到结束：

```python
def on_submitted(task_id: str) -> None:
    print("submitted:", task_id)

result = client.execute(
    task_name="some_long_task",
    source="/path/to/video.mp4",
    on_async_submitted=on_submitted,
)
# execute 内部会一直轮询直到结束或失败；若你希望完全自己轮询，需改用更底层 API（见下）
```

仅续查状态时：

```python
result = client.query("已有 task_id")
```

### 4.3 只上传并消费权益（不提交算法）

```python
media_url, context = client.prepare_and_consume(
    source="/path/to/file.jpg",
    task_name="eraser_watermark",
)
# 再用 client.api.invoke_task(...) 自行组参提交（进阶）
```

### 4.4 用 `TaskRunner` 统一入口

与直接 `SkillClient` 等价，便于注入同一 client 或统一区域：

```python
from sdk import TaskRunner

runner = TaskRunner()  # 同样读 MT_AK / MT_SK
out = runner.run("eraser_watermark", "/path/to/in.jpg", params=None)
later = runner.resume("task_id_here")
```

### 4.5 进阶：`AiApi` / `WapiClient`

- `client.api`：`AiApi`，负责 token、上传、`submit_task` / `invoke_task`、轮询等。
- `client.wapi`：`WapiClient`，签名访问配置、消费等 HTTP 接口。

需要自定义 `invoke` 表、区域或连接参数时，可看 `sdk/core/config.py` 与环境变量（如 `MT_AI_*`）。

---

## 5. 环境变量参考

| 变量 | 含义 |
|------|------|
| `MT_AK` / `MT_SK` | 开拍 API 访问密钥（必填其一方式：环境变量或 `SkillClient(ak=, sk=)`） |
| `MT_AI_PROGRESS` | 设为 `0` / `false` / `off` 可关闭进度日志（stderr） |
| `MT_AI_URL_MAX_BYTES` 等 | 见 `sdk/core/config.py`，控制 URL 下载大小与超时 |

---

## 6. 返回结构怎么读

- **成功（网关原始成功体）**：常见字段包括 `data`、`meta`、`output_urls`（SDK 附加）、`task_id`（若能解析）。不要只依赖 `skill_status == "completed"`（简化 CLI 已按多种形态判断成功）。
- **失败**：可能出现 `error`、`skill_status: "failed"`，以及 `detail` / `agent_instruction` 等说明，便于日志与排障。

若需强类型封装，可使用 `sdk.core.models` 中的 `TaskResult` 等（按你的业务再映射）。

---

## 版本

与 `sdk/__init__.py` 中 `__version__` 一致（当前为 **1.2.2**）。
