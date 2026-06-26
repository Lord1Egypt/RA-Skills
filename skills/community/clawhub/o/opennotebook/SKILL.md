---
name: opennotebook
description: OpenNotebook 知识管理平台客户端。支持笔记本、源文件、笔记、AI搜索、转换管道等操作。首次使用请配置 OPENNOTEBOOK_BASE_URL 和 OPENNOTEBOOK_API_KEY。
user-invokable: true
metadata: { "openclaw": { "emoji": "📘",  "requires": { "bins": ["python3"], "env":["OPENNOTEBOOK_BASE_URL", "OPENNOTEBOOK_API_KEY"]} } }
---

# OpenNotebook

OpenNotebook 知识管理平台客户端，支持完整的 API 操作。

所有 API 调用已封装到 `opennotebook.py` 脚本中。

## 配置

配置文件：`~/.openclaw/opennotebook.env`

```bash
OPENNOTEBOOK_BASE_URL=http://localhost:8000
OPENNOTEBOOK_API_KEY=your-api-key
```

## 快速开始

```bash
# 检查连接状态
python3 opennotebook.py health

# 列出笔记本
python3 opennotebook.py notebooks list

# 创建笔记本
python3 opennotebook.py notebooks create --name "我的笔记本" --description "描述"

# 上传文件作为源
python3 opennotebook.py sources upload --file /path/to/file.pdf --notebook <id>

# 搜索知识库
python3 opennotebook.py search query "机器学习" --limit 10

# 创建笔记
python3 opennotebook.py notes create --content "内容" --title "标题" --notebook <id>
```

## 可用命令

### 笔记本 (notebooks)

```bash
python3 opennotebook.py notebooks list [--archived] [--order-by <field>]
python3 opennotebook.py notebooks get --id <notebook_id>
python3 opennotebook.py notebooks create --name <name> [--description <desc>]
python3 opennotebook.py notebooks update --id <id> [--name <name>] [--archived]
python3 opennotebook.py notebooks delete --id <id> [--delete-sources]
```

### 源文件 (sources)

```bash
python3 opennotebook.py sources list [--notebook <id>] [--limit 50] [--offset 0]
python3 opennotebook.py sources get --id <source_id>
python3 opennotebook.py sources upload --file <path> [--notebook <id>] [--title <title>]
python3 opennotebook.py sources create-url --url <url> --notebook <id>
python3 opennotebook.py sources create-text --content <text> --notebook <id>
python3 opennotebook.py sources status --id <source_id>
python3 opennotebook.py sources retry --id <source_id>
python3 opennotebook.py sources delete --id <id>
```

### 笔记 (notes)

```bash
python3 opennotebook.py notes list [--notebook <id>]
python3 opennotebook.py notes get --id <note_id>
python3 opennotebook.py notes create --content <content> [--title <title>] [--notebook <id>]
python3 opennotebook.py notes update --id <id> [--content <content>] [--title <title>]
python3 opennotebook.py notes delete --id <id>
```

### 搜索 (search)

```bash
python3 opennotebook.py search query <query> [--limit 10] [--sources] [--notes]
python3 opennotebook.py search ask --question <question> --strategy-model <id> --answer-model <id> --final-model <id>
```

### 转换 (transformations)

```bash
python3 opennotebook.py transformations list
python3 opennotebook.py transformations get --id <id>
python3 opennotebook.py transformations execute --id <id> --input <text> --model <model_id>
```

### 模型 (models)

```bash
python3 opennotebook.py models list [--type <type>]
python3 opennotebook.py models defaults
python3 opennotebook.py models providers
python3 opennotebook.py models sync [--provider <name>]
python3 opennotebook.py models test --id <model_id>
```

### 嵌入 (embeddings)

```bash
python3 opennotebook.py embeddings embed --id <item_id> --type <source|note|insight>
python3 opennotebook.py embeddings rebuild --mode <full|incremental>
python3 opennotebook.py embeddings status --command-id <id>
```

### 聊天 (chat)

```bash
python3 opennotebook.py chat sessions
python3 opennotebook.py chat create-session
python3 opennotebook.py chat execute --session <id> --message <message>
```

### 播客 (podcasts)

```bash
python3 opennotebook.py podcasts episodes
python3 opennotebook.py podcasts get --id <episode_id>
python3 opennotebook.py podcasts audio --id <episode_id> --output <file>
```

## 在 Agent 中使用

推荐在 Python 代码中直接导入使用：

```python
import sys
sys.path.insert(0, '/root/.openclaw/skills/opennotebook')
from opennotebook_client import OpenNotebookClient

client = OpenNotebookClient()

# 列出笔记本
notebooks = client.notebooks.list()

# 搜索
results = client.search.query("关键词")

# 上传文件
source = client.sources.upload("/path/to/file.pdf", notebook_id=notebooks[0]["id"])
```

## API 参考

详细 API 文档请参考 [api_reference.md](api_reference.md)。