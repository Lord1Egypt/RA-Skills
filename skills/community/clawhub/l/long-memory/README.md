<div align="center">

# 🧠 Long Memory

**Enterprise-grade Full Conversation Memory System for AI Agents**

[![Version](https://img.shields.io/badge/version-6.0-blue)]()
[![Python](https://img.shields.io/badge/Python-3.10+-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()
[![Tests](https://img.shields.io/badge/tests-37%20passed-success)]()
[![Scripts](https://img.shields.io/badge/scripts-31-orange)]()

*File system = unlimited external storage. Context window = limited RAM.*
*All conversations archived forever, retrieved on demand, never forgotten.*

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 为什么需要 Long Memory？

AI 助手每次对话都是全新的——它不记得昨天聊了什么，上周做了什么决定。Long Memory 解决这个问题：

- ✅ **全量保存**：每一条用户消息、助手回复、思考过程，一字不落
- ✅ **按需检索**：不用加载全部历史，语义搜索秒级返回
- ✅ **永不遗忘**：文件系统存储，不受上下文窗口限制
- ✅ **企业级可靠**：并发安全、完整性校验、自动备份、操作审计

### 核心能力

```
写入层：归档 / Session捕获 / 结构化模板 / 批量导入
整理层：摘要 / 蒸馏 / 标签优化 / 清理归档
检索层：关键词 / TF-IDF / 语义搜索(零依赖) / Embedding向量搜索 / SQLite / 标签+话题+时间组合 / 智能推荐
分析层：统计 / 时间线 / 关联图谱 / 情感分析 / 遗忘曲线 / 人物关系
质量层：评分 / 完整性校验 / 矛盾检测 / 健康仪表盘
基建层：文件锁 / 内存索引 / SQLite引擎 / TF-IDF / 近义词扩展 / 配置管理 / 定时调度 / 多用户隔离
安全层：隐私加密 / 敏感扫描 / 操作审计 / 自动备份
输出层：CLI(34命令) / REST API / HTML报告 / JSON·MD·TXT导出
```

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/ZYuanJia/long-memory.git
cd long-memory

# 归档一段对话
python3 scripts/cli.py archive --session webchat --topic "项目讨论" --tags "工作,技术"

# 搜索历史记忆
python3 scripts/cli.py search -q "性能优化" --days 30

# 生成每日摘要
python3 scripts/cli.py summary

# 查看记忆健康状态
python3 scripts/cli.py health
```

### CLI 命令（31个）

#### 📝 记录
| 命令 | 说明 |
|------|------|
| `archive` | 归档对话 |
| `capture` | 捕获 Session 历史 |
| `import` | 批量导入 Markdown/JSON/文本 |
| `template create meeting` | 用模板创建会议纪要 |

#### 🔍 检索（三级搜索引擎）
| 命令 | 说明 | 依赖 |
|------|------|------|
| `search` | 关键词+标签+话题+时间组合搜索 | 无 |
| `semantic` | TF-IDF + 近义词语义搜索（推荐） | 无 |
| `tfidf` | TF-IDF 向量搜索 | 无 |
| `embedding` | 深度语义搜索（sentence-transformers） | pip install sentence-transformers |
| `sqlite` | SQLite 高性能存储+查询 | 无 |
| `recommend` | 基于当前对话智能推荐历史 | 无 |
| `timeline` | 话题时间线 | 无 |

#### 📊 分析
| 命令 | 说明 |
|------|------|
| `stats` | 记忆统计 |
| `graph` | 记忆关联图谱 |
| `persons` | 人物关系图谱 |
| `emotion` | 情感分析 |
| `forgetting` | 艾宾浩斯遗忘曲线 |

#### ✅ 质量
| 命令 | 说明 |
|------|------|
| `quality` | 质量评分（0-100） |
| `integrity` | 文件完整性校验 |
| `contradictions` | 记忆矛盾检测 |
| `health` | 综合健康仪表盘 |

#### 🔧 维护
| 命令 | 说明 |
|------|------|
| `summary` | 每日摘要 |
| `distill` | 周蒸馏 |
| `tags` | 标签体系优化 |
| `clean` | 清理旧记忆 |
| `index` | 索引管理 |
| `backup` | Git 自动备份 |
| `scheduler` | 定时任务调度 |

#### 🔒 安全 & 导出
| 命令 | 说明 |
|------|------|
| `privacy encrypt/decrypt` | 加密/解密 |
| `privacy scan` | 敏感内容扫描 |
| `export` | 导出 JSON/Markdown/纯文本 |
| `report` | HTML 可视化报告 |
| `api` | 启动 REST API 服务 |
| `users` | 多用户管理 |
| `log` | 操作审计日志 |
| `config` | 配置验证与迁移 |
| `changelog` | 版本变更记录 |
| `benchmark` | 性能基准测试 |
| `sqlite` | SQLite 初始化/导入/统计/搜索 |

### 文件结构

```
long-memory/
├── SKILL.md                    # Skill 定义（OpenClaw 格式）
├── long-memory.json            # 配置文件
├── .gitignore
├── scripts/
│   ├── cli.py                  # 统一 CLI 入口（31个子命令）
│   ├── lib/
│   │   └── filelock.py         # 文件锁（并发安全）
│   ├── archive_conversation.py # 对话归档
│   ├── capture_session.py      # Session 捕获
│   ├── generate_summary.py     # 每日摘要
│   ├── distill_week.py         # 周蒸馏
│   ├── search_memory.py        # 组合搜索
│   ├── tfidf_search.py         # TF-IDF 语义搜索
│   ├── smart_recommend.py      # 智能推荐
│   ├── topic_timeline.py       # 话题时间线
│   ├── memory_graph.py         # 关联图谱
│   ├── person_graph.py         # 人物关系
│   ├── emotion_analyzer.py     # 情感分析
│   ├── forgetting_curve.py     # 遗忘曲线
│   ├── memory_stats.py         # 统计
│   ├── quality_check.py        # 质量评分
│   ├── detect_contradictions.py# 矛盾检测
│   ├── integrity_check.py      # 完整性校验
│   ├── health_dashboard.py     # 健康仪表盘
│   ├── index_manager.py        # 索引管理
│   ├── auto_backup.py          # 自动备份
│   ├── tag_optimizer.py        # 标签优化
│   ├── clean_old.py            # 旧记忆清理
│   ├── export_memory.py        # 导出
│   ├── import_memory.py        # 导入
│   ├── memory_templates.py     # 结构化模板
│   ├── scheduler.py            # 定时任务
│   ├── user_manager.py         # 多用户管理
│   ├── privacy.py              # 隐私加密
│   ├── html_report.py          # HTML 报告
│   ├── api_server.py           # REST API
│   ├── operation_log.py        # 操作日志
│   ├── config_manager.py       # 配置管理
│   ├── changelog.py            # 变更记录
│   ├── recent_context.py       # 上下文预加载
│   └── benchmark.py            # 性能测试
└── tests/
    └── test_long_memory.py     # 37 个 pytest 用例
```

### 测试

```bash
cd long-memory
python3 -m pytest tests/ -v
# 37 passed
```

### 企业级特性

| 特性 | 实现 |
|------|------|
| 并发安全 | `fcntl` 文件锁，多进程写入不冲突 |
| 索引加速 | 内存索引 + SQLite + TF-IDF + 语义搜索 |
| 完整性校验 | SHA256 校验和，自动修复 |
| 自动备份 | Git commit + push |
| 质量评分 | 7条规则，0-100分量化 |
| 遗忘曲线 | 艾宾浩斯模型，检索优先级加权 |
| 情感分析 | 中文情感词典，情绪变化追踪 |
| 隐私加密 | AES-256，敏感内容自动扫描 |
| 多用户隔离 | 独立记忆空间 |
| 定时调度 | 蒸馏/备份/清理自动执行 |
| REST API | 7个 HTTP 接口 |
| 配置化 | JSON 配置文件 + 版本迁移 |
| 操作审计 | JSONL 操作日志 |

### 配置

编辑 `long-memory.json`：

```json
{
  "version": "5.0",
  "archive_days": 90,
  "max_memory_md_size": 8000,
  "auto_backup": {
    "enabled": false,
    "git_remote": null,
    "interval_hours": 6
  },
  "quality": {
    "auto_flag_low_quality": true
  }
}
```

### REST API

```bash
# 启动服务
python3 scripts/cli.py api --port 8765

# 接口
GET  /api/health          # 健康检查
GET  /api/stats           # 统计信息
GET  /api/conversations   # 对话列表
GET  /api/search?q=xxx    # 搜索
GET  /api/topics          # 话题列表
GET  /api/tags            # 标签列表
POST /api/conversations   # 创建对话
```

### 许可证

MIT License

### 致谢

Built with ❤️ for [OpenClaw](https://github.com/openclaw/openclaw) ecosystem.

---

## English

### Why Long Memory?

AI assistants start fresh every conversation — they don't remember yesterday's chat, last week's decisions. Long Memory fixes this:

- ✅ **Full archival**: Every user message, assistant reply, and thought process — nothing lost
- ✅ **On-demand retrieval**: Semantic search returns relevant memories in milliseconds
- ✅ **Never forget**: File-system storage, not limited by context window size
- ✅ **Enterprise-grade**: Concurrency-safe, integrity-checked, auto-backed, fully audited

### Architecture

```
Write:    Archive / Session Capture / Templates / Batch Import
Organize: Summaries / Distillation / Tag Optimization / Cleanup
Search:   Keyword / TF-IDF Semantic / Tag+Topic+Time / Smart Recommend
Analyze:  Stats / Timeline / Graph / Emotion / Forgetting Curve / People
Quality:  Scoring / Integrity Check / Contradiction Detection / Health Dashboard
Infra:    File Locks / Indexing / Config / Scheduler / Multi-user
Security: Encryption / Sensitive Scan / Audit Log / Auto Backup
Output:   CLI (31 commands) / REST API / HTML Report / JSON·MD·TXT Export
```

### Quick Start

```bash
git clone https://github.com/ZYuanJia/long-memory.git
cd long-memory

# Archive a conversation
python3 scripts/cli.py archive --session webchat --topic "project discussion" --tags "work,tech"

# Search memories
python3 scripts/cli.py search -q "performance optimization" --days 30

# Generate daily summary
python3 scripts/cli.py summary

# Check memory health
python3 scripts/cli.py health
```

### 31 CLI Commands

#### 📝 Recording
| Command | Description |
|---------|-------------|
| `archive` | Archive conversations |
| `capture` | Capture session history |
| `import` | Batch import Markdown/JSON/text |
| `template create meeting` | Create from structured template |

#### 🔍 Search (3-Tier Engine)
| Command | Description | Deps |
|---------|-------------|------|
| `search` | Combined keyword+tag+topic+time search | None |
| `semantic` | TF-IDF + synonym expansion (recommended) | None |
| `tfidf` | TF-IDF vector search | None |
| `embedding` | Deep semantic search (sentence-transformers) | pip install sentence-transformers |
| `sqlite` | SQLite high-performance storage & query | None |
| `recommend` | Smart recommendations based on context | None |
| `timeline` | Topic timeline | None |

#### 📊 Analysis
| Command | Description |
|---------|-------------|
| `stats` | Memory statistics |
| `graph` | Memory association graph |
| `persons` | People relationship graph |
| `emotion` | Emotion analysis |
| `forgetting` | Ebbinghaus forgetting curve |

#### ✅ Quality
| Command | Description |
|---------|-------------|
| `quality` | Quality score (0-100) |
| `integrity` | File integrity check |
| `contradictions` | Memory contradiction detection |
| `health` | Comprehensive health dashboard |

#### 🔧 Maintenance
| Command | Description |
|---------|-------------|
| `sqlite` | SQLite init/import/stats/search |

| `summary` | Daily summary |
| `distill` | Weekly distillation |
| `tags` | Tag system optimization |
| `clean` | Clean old memories |
| `index` | Index management |
| `backup` | Git auto backup |
| `scheduler` | Scheduled task manager |

#### 🔒 Security & Export
| Command | Description |
|---------|-------------|
| `benchmark` | Performance benchmark |
| `sqlite` | SQLite init/import/stats/search |

| `privacy encrypt/decrypt` | Encrypt/decrypt memories |
| `privacy scan` | Sensitive content scan |
| `export` | Export JSON/Markdown/Plain text |
| `report` | HTML visual report |
| `api` | Start REST API server |
| `users` | Multi-user management |
| `log` | Audit log |
| `config` | Config validation & migration |
| `changelog` | Version changelog |
| `benchmark` | Performance benchmark |

### Test

```bash
cd long-memory
python3 -m pytest tests/ -v
# 37 passed
```

### Enterprise Features

| Feature | Implementation |
|---------|---------------|
| Concurrency Safety | `fcntl` file locks |
| Index Acceleration | SQLite + TF-IDF + Semantic search (zero-dep) |
| Integrity Check | SHA256 checksums with auto-repair |
| Auto Backup | Git commit + push |
| Quality Scoring | 7 rules, 0-100 score |
| Forgetting Curve | Ebbinghaus model for retrieval priority |
| Emotion Analysis | Chinese sentiment lexicon |
| Privacy Encryption | AES-256 + sensitive content scanning |
| Multi-user | Isolated memory spaces |
| Scheduler | Auto distill/backup/cleanup |
| REST API | 7 HTTP endpoints |
| Configuration | JSON config + version migration |
| Audit Trail | JSONL operation logs |

### REST API

```bash
# Start server
python3 scripts/cli.py api --port 8765

# Endpoints
GET  /api/health          # Health check
GET  /api/stats           # Statistics
GET  /api/conversations   # List conversations
GET  /api/search?q=xxx    # Search
GET  /api/topics          # List topics
GET  /api/tags            # List tags
POST /api/conversations   # Create conversation
```

### License

MIT License

### Credits

Built with ❤️ for the [OpenClaw](https://github.com/openclaw/openclaw) ecosystem.
