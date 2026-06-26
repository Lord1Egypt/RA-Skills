# 🧠 Memory System

支持 embedding 模型处理的多后端记忆系统，支持共享记忆用于 agent 间通信。

> **默认行为**：所有记忆默认存储为**私人记忆**。共享记忆需要明确指定（如 `memory shared add`）。

## 特性

- **可选 Embedding 处理** - 使用 sentence-transformers 进行语义搜索
- **四种存储后端** - 本地文件 / GitHub / Gitee / SQLite
- **标签分类** - 支持标签组织记忆
- **记忆分组** - 用分组组织记忆
- **批量操作** - 批量删除、添加标签
- **语义搜索** - 基于向量相似度搜索
- **共享记忆** - Agent 之间共享的记忆
- **导入导出** - JSON 格式备份

## 安装依赖

```bash
pip install sentence-transformers scikit-learn pyyaml numpy
```

## 快速开始

### Python API

```python
from memory_system import MemoryManager

# 初始化（本地存储）
mm = MemoryManager(backend='local')

# 添加记忆
mm.add("用户喜欢深色主题", tags=["偏好", "UI"])

# 搜索记忆
results = mm.search("用户主题设置")

# 列出所有记忆
entries = mm.list()

# 按标签筛选
entries = mm.list(tags=["偏好"])
```

### 使用 Embedding

```python
mm = MemoryManager(backend='local', use_embedding=True)

# 添加（自动生成向量）
mm.add("用户工作日早上9点到公司")

# 语义搜索
results = mm.search("用户什么时候上班")
```

### 私人记忆 vs 共享记忆

| 类型 | 存储位置 | 访问者 | 使用场景 |
|------|---------|--------|---------|
| **私人记忆** | `./memory_data/` | 仅当前 agent | 用户个人信息、私人偏好、个人笔记 |
| **共享记忆** | `./shared_memory/` | 所有 agent | 团队决策、协作任务、跨 agent 信息 |

**判断原则**：只有"需要其他 agent 知道"时才放共享记忆，其他默认私人。

```python
# 私人记忆 - 用户说"记住..."
mm.add("用户叫张三")  # 私人

# 共享记忆 - 用户说"告诉其他 agent..."
smm.add("团队决定用 React", agent_id="agent_a")  # 共享
```

### 共享记忆 (Agent 间通信)

```python
from memory_system import SharedMemoryManager

# 初始化共享记忆管理器（本地存储）
smm = SharedMemoryManager(backend='local', shared_path='./shared_memory')

# 使用 GitHub 存储（独立仓库）
smm = SharedMemoryManager(
    backend='github',
    shared_path='owner/shared-repo',
    token_env='SHARED_GITHUB_TOKEN'
)

# 使用 Gitee 存储
smm = SharedMemoryManager(
    backend='gitee',
    shared_path='owner/shared-repo',
    token_env='SHARED_GITEE_TOKEN'
)

# 添加共享记忆（标记来源 agent）
smm.add("用户今天反馈了一个 bug", agent_id='agent_b')

# 列出所有共享记忆
shared_entries = smm.list()

# 按 agent 筛选
agent_entries = smm.get_by_agent('agent_b')

# 搜索共享记忆
results = smm.search("用户反馈")
```

### 使用 GitHub 存储

```bash
export GITHUB_TOKEN="your_token_here"
```

```python
mm = MemoryManager(
    backend='github',
    repo='your-username/your-repo',
    branch='main',
    base_path='memory/'
)
```

### 使用 Gitee 存储

```bash
export GITEE_TOKEN="your_token_here"
```

```python
mm = MemoryManager(
    backend='gitee',
    repo='your-username/your-repo',
    branch='master',
    base_path='memory/'
)
```

### 使用 SQLite 存储（高性能）

```python
mm = MemoryManager(backend='sqlite', base_path='./memory.db')
```

CLI:
```bash
python3 memory_cli.py --backend sqlite add "记忆内容"
```

> SQLite 比本地文件存储更快，适合大量记忆场景。


```python
from memory_system import MemoryManager, MemorySummarizer, ConversationMemoryProcessor

# 初始化 - 模型自动从 OpenClaw 配置读取
mm = MemoryManager(backend='local', use_embedding=True)
summarizer = MemorySummarizer()  # 自动检测 OpenClaw 模型
processor = ConversationMemoryProcessor(mm, summarizer, auto_save=True)

# 对话历史
conversation = """
用户: 我喜欢深色主题
助手: 已为您切换到深色主题
用户: 页面加载有点慢
助手: 已优化图片压缩
用户: 我用 Mac 工作
助手: 了解，已记录您使用 Mac
"""

# 提炼并自动保存
memories = processor.process(conversation, context="用户偏好调查")

# 打印结果
for m in memories:
    print(f"- {m.content} [{m.tags}]")
```

> 💡 模型自动从 OpenClaw 配置读取，无需单独配置。如果需要指定：
> ```python
> summarizer = MemorySummarizer(model='gpt-4', provider='openai')
> ```

CLI 用法：

```bash
# 从文件提炼对话
python3 memory_cli.py summarize --file conversation.txt --context "用户偏好调查" --save

# 直接传入对话
python3 memory_cli.py summarize --conversation "用户: 我喜欢深色主题" --save

# 使用本地模型
python3 memory_cli.py summarize --file dialog.txt --provider ollama --model llama3 --save
```

## CLI 使用

```bash
cd memory_system

# 添加记忆
python3 memory_cli.py add "用户反馈页面加载慢" --tags "bug,性能"

# 列出所有记忆
python3 memory_cli.py list

# 按标签筛选
python3 memory_cli.py list --tags bug

# 搜索
python3 memory_cli.py search "页面性能问题"

# 带 embedding 搜索
python3 memory_cli.py -e search "加载慢"

# 查看单条记忆
python3 memory_cli.py get abc123...

# 删除记忆
python3 memory_cli.py delete abc123...

# 导出
python3 memory_cli.py export -o backup.json

# 导入
python3 memory_cli.py import backup.json

# 批量操作
python3 memory_cli.py batch-add-tags abc123,def456 --tags "新标签1,新标签2"
python3 memory_cli.py batch-remove-tags abc123 --tags "旧标签"
python3 memory_cli.py batch-delete abc123,def456 --force

# 记忆分组
python3 memory_cli.py add "工作记忆" --tags "工作" --group "工作相关"
python3 memory_cli.py group list
python3 memory_cli.py group show "工作相关"
python3 memory_cli.py group add "项目A" abc123,def456
python3 memory_cli.py group remove abc123
python3 memory_cli.py group delete "项目A"

# 重建所有 embedding
python3 memory_cli.py rebuild-embeds

# 更新单条 embedding
python3 memory_cli.py update-embed abc123...

# 指定后端
python3 memory_cli.py -b github list

# 启用 embedding
python3 memory_cli.py -e add "新记忆内容" --tags "test"

# 提炼对话并保存
python3 memory_cli.py summarize --file conversation.txt --context "用户调查" --save

# 分页查看记忆
python3 memory_cli.py list --limit 10 --offset 0
python3 memory_cli.py list --limit 5 --offset 10
```

### 共享记忆 CLI

```bash
# 添加共享记忆（默认本地）
python3 memory_cli.py shared add "共享信息" --agent "agent_a" --tags "共享"

# 使用 GitHub 存储
python3 memory_cli.py shared add "共享信息" --agent "agent_a" --shared-backend github --shared-path "owner/shared-repo"

# 使用 Gitee 存储
python3 memory_cli.py shared add "共享信息" --agent "agent_a" --shared-backend gitee --shared-path "owner/shared-repo"

# 列出所有共享记忆
python3 memory_cli.py shared list

# 按 agent 筛选
python3 memory_cli.py shared list --agent agent_a

# 按标签筛选
python3 memory_cli.py shared list --tags 共享

# 搜索共享记忆
python3 memory_cli.py -e shared search "共享信息"

# 查看单条共享记忆
python3 memory_cli.py shared get abc123...

# 删除共享记忆
python3 memory_cli.py shared delete abc123...
```

### 记忆维护 CLI

```bash
# 生成维护报告
python3 memory_cli.py maintenance report

# 审查旧记忆（7天前的）
python3 memory_cli.py maintenance review --days 7

# 查找相似记忆（仅列出，不删除）
python3 memory_cli.py maintenance consolidate --threshold 0.85

# 扩展短记忆
python3 memory_cli.py maintenance expand <memory_id> --context "相关上下文"

# 列出标记为过时的记忆
python3 memory_cli.py maintenance outdated --list

# 标记某条记忆为过时（需用户确认后手动删除）
python3 memory_cli.py maintenance outdated --mark <memory_id> --reason "已过期"

# 取消过时标记
python3 memory_cli.py maintenance outdated --unmark <memory_id>

# 推荐无标签记忆的标签
python3 memory_cli.py maintenance suggest-tags
python3 memory_cli.py maintenance suggest-tags --limit 5
```

### 记忆模板 CLI

```bash
# 查看所有模板
python3 memory_cli.py template list

# 查看模板详情
python3 memory_cli.py template show task

# 使用模板创建记忆
python3 memory_cli.py template use task --field title="完成报告" --field priority="高" --field status="进行中"
```

> ⚠️ **安全设计**：合并和删除都需要用户手动确认，不会自动删除任何记忆。


## 配置文件

`config.yaml`:

```yaml
STORAGE_BACKEND: "local"

USE_EMBEDDING: false
EMBEDDING_MODEL: "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM: 384

storage:
  local:
    base_path: "./memory_data"
  github:
    repo: "owner/repo"
    branch: "main"
    token_env: "GITHUB_TOKEN"
    base_path: "memory/"
  gitee:
    repo: "owner/repo"
    branch: "master"
    token_env: "GITEE_TOKEN"
    base_path: "memory/"

DEFAULT_TOP_K: 5
SIMILARITY_THRESHOLD: 0.7

# 共享记忆设置（可选独立仓库）
SHARED_MEMORY_ENABLED: true
SHARED_MEMORY_BACKEND: "github"  # github | gitee | local
SHARED_MEMORY_PATH: "./shared_memory"

# 共享记忆独立仓库配置
shared_storage:
  github:
    repo: "shared-owner/shared-repo"
    branch: "main"
    token_env: "SHARED_GITHUB_TOKEN"
    base_path: "shared/"
  gitee:
    repo: "shared-owner/shared-repo"
    branch: "master"
    token_env: "SHARED_GITEE_TOKEN"
    base_path: "shared/"
```

## 项目结构

```
memory_system/
├── __init__.py
├── config.py          # 配置加载
├── exceptions.py     # 异常类
├── memory_manager.py  # 核心管理器
├── shared_memory.py   # 共享记忆管理器
├── summarizer.py      # LLM 对话提炼
├── maintenance.py     # 记忆维护
├── templates.py       # 记忆模板
├── embedding.py       # Embedding 处理
├── cli.py             # CLI 接口
├── memory             # CLI 入口脚本
├── config.yaml        # 配置文件
└── storage/
    ├── __init__.py
    ├── base.py        # 存储基类
    ├── local.py       # 本地存储
    ├── github.py      # GitHub 存储
    ├── gitee.py       # Gitee 存储
    └── sqlite.py      # SQLite 存储
```

## API 文档

### MemoryManager

| 方法 | 说明 |
|------|------|
| `add(content, tags, metadata, group)` | 添加记忆（支持分组） |
| `get(entry_id)` | 获取单条记忆 |
| `delete(entry_id)` | 删除记忆 |
| `list(tags, limit, offset)` | 列出记忆（支持分页） |
| `count(tags)` | 统计记忆数量 |
| `batch_delete(ids)` | 批量删除 |
| `batch_add_tags(ids, tags)` | 批量添加标签 |
| `batch_remove_tags(ids, tags)` | 批量移除标签 |
| `search(query, tags, top_k, threshold)` | 搜索记忆 |
| `update_embedding(entry_id)` | 更新单条 embedding |
| `rebuild_all_embeddings()` | 重建所有 embedding |
| `list_groups()` | 列出所有分组 |
| `get_by_group(group)` | 获取分组中的记忆 |
| `add_to_group(ids, group)` | 添加记忆到分组 |
| `remove_from_group(ids)` | 从分组移除记忆 |
| `delete_group(group, delete_memories)` | 删除分组 |
| `export_json(filepath)` | 导出 JSON |
| `import_json(filepath)` | 导入 JSON |

### SharedMemoryManager

| 方法 | 说明 |
|------|------|
| `add(content, agent_id, tags, metadata)` | 添加共享记忆 |
| `get(entry_id)` | 获取共享记忆 |
| `delete(entry_id)` | 删除共享记忆 |
| `list(tags, limit, offset)` | 列出共享记忆（支持分页） |
| `search(query, tags, top_k, threshold)` | 搜索共享记忆 |
| `get_by_agent(agent_id)` | 获取指定 agent 的所有共享记忆 |
| `export_all()` | 导出所有共享记忆 |

### MemorySummarizer

| 方法 | 说明 |
|------|------|
| `summarize(conversation, context, max_memories)` | 提炼对话生成记忆 |

### ConversationMemoryProcessor

| 方法 | 说明 |
|------|------|
| `process(conversation, context, tags)` | 处理对话并生成记忆 |

### MemoryMaintenance

| 方法 | 说明 |
|------|------|
| `run_review(older_than_days, max_memories)` | 审查旧记忆，列出问题 |
| `consolidate_similar(threshold)` | 查找相似记忆，仅列出不删除 |
| `consolidate_and_merge(keep_id, drop_id, confirm)` | 合并两条记忆（需 confirm=True） |
| `expand_summary(memory_id, context)` | 扩展短记忆 |
| `mark_outdated(memory_id, reason)` | 标记过时（仅标记，需手动删除） |
| `unmark_outdated(memory_id)` | 取消过时标记 |
| `list_outdated()` | 列出所有标记为过时的记忆 |
| `generate_report()` | 生成维护报告 |
| `suggest_tags_llm(content)` | LLM 智能推荐标签 |
| `suggest_tags_for_memories(limit, use_llm)` | 批量推荐无标签记忆的标签 |

### MemoryTemplates

| 方法 | 说明 |
|------|------|
| `list_templates()` | 列出所有模板 |
| `get_template(name)` | 获取模板详情 |
| `generate_from_template(name, fields)` | 从模板生成记忆内容 |

> ⚠️ 所有删除操作都需要用户手动执行 `memory delete <id>`


### MemoryEntry

```python
{
    "id": "abc123...",       # 唯一 ID
    "content": "记忆内容",
    "timestamp": "2026-03-26T13:00:00",
    "tags": ["标签1", "标签2"],
    "embedding": [0.1, 0.2, ...],  # 可选
    "metadata": {},           # 可选
    "is_shared": false       # 是否共享
}
```
