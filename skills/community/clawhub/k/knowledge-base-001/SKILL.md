# Knowledge Base Skill

> ⚠️ **首次使用必读** ⚠️
>
> 安装后请立即运行初始化脚本，自动安装依赖并创建知识库目录：
> ```bash
> python3 scripts/init.py
> ```
> 不运行这一步，后续所有功能都无法正常工作。

一套完整的文档转换与知识库管理工具。自动将各类文档转换为 Markdown，按内容智能分类，建立本地可检索的私人知识库。

## 功能

1. **文档转换**：集成 Microsoft MarkItDown，支持 PDF、Word、PPT、Excel、HTML、EPUB、图片等格式转为 Markdown
2. **自动分类**：基于内容关键词智能分类，支持自定义分类
3. **关键词提取**：使用 jieba 中文分词 + TF-IDF 提取关键词，建立检索索引
4. **本地检索**：基于关键词、标题、摘要、内容的全文检索
5. **向量检索**：基于 chromadb 的语义搜索
6. **自动导入**：监控目录自动导入新文件
7. **批量导入**：递归扫描目录批量导入
8. **飞书打通**：接收飞书文件消息自动导入
9. **知识库管理**：文档增删改查、分类管理、统计信息
10. **降低 Token 消耗**：文档内容存储于本地，仅在检索时按需加载，不占用 Memory

## 支持的文件格式

- PDF、DOCX、PPTX、XLSX/XLS
- HTML、EPUB、TXT、CSV、JSON、XML
- 图片（EXIF + OCR）
- ZIP（遍历内容）
- 更多格式详见 [MarkItDown 文档](https://github.com/microsoft/markitdown)

## 依赖（自动安装）

首次使用自动检测并安装依赖，无需手动配置：

- `markitdown[all]` — 文档转换核心
- `jieba` — 中文分词
- `chromadb` — 向量检索（首次使用向量功能时自动安装）

如需手动安装：
```bash
pip install markitdown[all] jieba chromadb
```

## 目录结构

```
~/.openclaw/workspace/knowledge-base/
├── .index.json          # 索引文件（元数据、关键词、摘要）
├── .chroma/             # 向量数据库
├── 学术论文/
├── 技术文档/
├── 工作资料/
├── 读书笔记/
├── 项目文档/
├── 参考资料/
└── 未分类/
```

## 使用方式

### 初始化知识库

```bash
python3 scripts/init.py
```

### 1. 单文件导入

```bash
python3 scripts/kb_cli.py ingest <文件路径>
python3 scripts/kb_cli.py ingest ~/Downloads/report.pdf --category 技术文档
```

### 2. 批量导入

递归扫描整个目录，批量导入所有支持的文件：

```bash
python3 scripts/batch_ingest.py ~/Documents/我的资料
python3 scripts/batch_ingest.py ~/Downloads --no-recursive  # 不递归子目录
python3 scripts/batch_ingest.py ~/Documents --dry-run       # 预览模式
```

### 3. 自动导入（监控模式）

持续监控 `/tmp/openclaw/` 目录（飞书文件下载目录），新文件自动导入：

```bash
# 单次扫描
python3 scripts/auto_ingest.py --once

# 持续监控（每30秒扫描一次）
python3 scripts/auto_ingest.py --watch

# 自定义间隔
python3 scripts/auto_ingest.py --watch --interval 60
```

**飞书自动导入建议**：
将监控脚本加入 OpenClaw cron job，每分钟自动扫描：
```json
{
  "schedule": { "kind": "cron", "expr": "*/1 * * * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 python3 ~/.openclaw/workspace/skills/knowledge-base/scripts/auto_ingest.py --once"
  },
  "sessionTarget": "isolated"
}
```

### 4. 关键词检索

```bash
python3 scripts/kb_cli.py search "机器学习"
python3 scripts/kb_cli.py search "神经网络" --category 技术文档 --limit 5
```

### 5. 向量语义检索

首次使用前需构建索引：

```bash
# 构建/更新向量索引
python3 scripts/vector_index.py build

# 强制重建
python3 scripts/vector_index.py build --force

# 语义搜索
python3 scripts/vector_index.py search "深度学习在图像处理中的应用"
python3 scripts/vector_index.py search "神经网络" --limit 5 --category 技术文档
```

### 6. 列出文档

```bash
python3 scripts/kb_cli.py list
python3 scripts/kb_cli.py list --category 学术论文
```

### 7. 查看文档详情

```bash
python3 scripts/kb_cli.py get <doc_id>
```

### 8. 删除文档

```bash
python3 scripts/kb_cli.py delete <doc_id>
```

### 9. 管理分类

```bash
python3 scripts/kb_cli.py add-category "旅行攻略"
```

### 10. 查看统计

```bash
python3 scripts/kb_cli.py stats
```

## 飞书文件自动处理

当用户通过飞书发送文件时：

1. 文件会被下载到 `/tmp/openclaw/` 目录
2. 运行 `python3 scripts/auto_ingest.py --once` 自动导入
3. 或直接调用 `feishu_im_bot_image` 下载后手动导入

示例 workflow：
```
用户发送 PDF → 检测到文件消息
  → 调用 feishu_im_bot_image 下载到 /tmp/openclaw/
  → 调用 auto_ingest.py 导入知识库
  → 返回导入结果给用户
```

## 核心脚本

| 脚本 | 功能 |
|---|---|
| `scripts/kb_manager.py` | 核心引擎（Python API） |
| `scripts/kb_cli.py` | 单文件操作 CLI |
| `scripts/batch_ingest.py` | 批量导入 |
| `scripts/auto_ingest.py` | 自动监控导入 |
| `scripts/vector_index.py` | 向量索引与语义搜索 |
| `scripts/init.py` | 初始化与依赖安装 |

## 设计原则

- **零配置开箱即用**：自动安装依赖，默认分类，自动处理
- **内容优先**：按内容而非文件名分类
- **本地优先**：所有数据本地存储，无需外部服务
- **检索高效**：关键词索引 + 向量语义检索双层架构
- **降低负担**：文档内容不进 Memory，需要时再读
- **中文友好**：jieba 分词 + 中文停用词过滤
- **自动化**：支持监控模式和批量导入，减少手动操作

## 技术栈

- **文档转换**：Microsoft MarkItDown
- **中文分词**：jieba + TF-IDF
- **向量检索**：ChromaDB（默认 embedding）
- **索引存储**：JSON 文件索引
- **存储格式**：Markdown + YAML 头部

## 许可证

MIT
