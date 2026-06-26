# Changelog / 更新日志

> **版本号规则：** Feature 分支不更新版本号，合并到 main 时统一递增版本号

---

## v2.0.0 (2026-03-14)

### English
- 🎨 feat: Add three-level cascade search (keyword → vector → raw text)
  - Level 1: Keyword search (existing)
  - Level 2: Vector semantic search (HuggingFace bge-base-zh-v1.5)
  - Level 3: Raw text search
  - Automatic fallback: upper level no results → next level
- 🧠 feat: Add embedding.py - Vector semantic search module
  - Support HuggingFace local models (recommended)
  - Support Ollama local models
  - Support MiniMax API
  - Default model: BAAI/bge-base-zh-v1.5 (768 dimensions)
- 🔧 feat: Add vector management commands
  - `vector status` - View vector index status
  - `vector test` - Test vector generation
  - `vector reindex` - Batch regenerate vectors
- ✨ feat: Add --embed flag to add command for vector generation
- 📝 docs: Update AGENTS.md with three-level search and proactive trigger
- 🐛 fix: Fix score display bug in search results
- ♻️ refactor: Remove Hook (Agent now intelligently decides when to search)
  - No more auto-search on session start
  - Agent judges based on user question content

### 中文
- 🎨 feat: 添加三级级联搜索（关键词 → 向量 → 原文）
  - 第1层：关键词搜索（现有）
  - 第2层：向量语义搜索（HuggingFace bge-base-zh-v1.5）
  - 第3层：原文全文搜索
  - 自动降级：上层无结果时自动使用下一层
- 🧠 feat: 添加 embedding.py - 向量语义搜索模块
  - 支持 HuggingFace 本地模型（推荐）
  - 支持 Ollama 本地模型
  - 支持 MiniMax API
  - 默认模型：BAAI/bge-base-zh-v1.5（768维）
- 🔧 feat: 添加向量管理命令
  - `vector status` - 查看向量索引状态
  - `vector test` - 测试向量生成
  - `vector reindex` - 批量重新生成向量
- ✨ feat: add 命令添加 --embed 参数支持向量生成
- 📝 docs: 更新 AGENTS.md，添加三级搜索和智能触发
- 🐛 fix: 修复搜索结果分数显示 bug
- ♻️ refactor: 删除 Hook（由 Agent 智能判断是否搜索）
  - 不再自动搜索
  - Agent 根据问题内容判断

---

## v1.0.10 (2026-03-13)

### English
- 🎨 feat: Add three-level cascade search (keyword → vector → raw text)
  - Level 1: Keyword search (existing)
  - Level 2: Vector semantic search (HuggingFace bge-base-zh-v1.5)
  - Level 3: Raw text search
  - Automatic fallback: upper level no results → next level
- 🧠 feat: Add embedding.py - Vector semantic search module
  - Support HuggingFace local models (recommended)
  - Support Ollama local models
  - Support MiniMax API
  - Default model: BAAI/bge-base-zh-v1.5 (768 dimensions)
- 🔧 feat: Add vector management commands
  - `vector status` - View vector index status
  - `vector test` - Test vector generation
  - `vector reindex` - Batch regenerate vectors
- ✨ feat: Add --embed flag to add command for vector generation
- 📝 docs: Update AGENTS.md with three-level search and proactive trigger
- 🐛 fix: Fix score display bug in search results
- ♻️ refactor: Remove Hook (Agent now intelligently decides when to search)
  - No more auto-search on session start
  - Agent judges based on user question content

### 中文
- 🎨 feat: 添加三级级联搜索（关键词 → 向量 → 原文）
  - 第1层：关键词搜索（现有）
  - 第2层：向量语义搜索（HuggingFace bge-base-zh-v1.5）
  - 第3层：原文全文搜索
  - 自动降级：上层无结果时自动使用下一层
- 🧠 feat: 添加 embedding.py - 向量语义搜索模块
  - 支持 HuggingFace 本地模型（推荐）
  - 支持 Ollama 本地模型
  - 支持 MiniMax API
  - 默认模型：BAAI/bge-base-zh-v1.5（768维）
- 🔧 feat: 添加向量管理命令
  - `vector status` - 查看向量索引状态
  - `vector test` - 测试向量生成
  - `vector reindex` - 批量重新生成向量
- ✨ feat: add 命令添加 --embed 参数支持向量生成
- 📝 docs: 更新 AGENTS.md，添加三级搜索和智能触发
- 🐛 fix: 修复搜索结果分数显示 bug
- ♻️ refactor: 删除 Hook（由 Agent 智能判断是否搜索）
  - 不再自动搜索
  - Agent 根据问题内容判断

---

## v1.0.10 (2026-03-13)

### English
- 📝 docs: Update AGENTS.md and install.sh with proactive search rules
  - Add memory search order: memory-indexer first
  - Add proactive search triggers: "找找", "为什么", "之前", "记得"
  - Search automatically when user mentions historical context
- 🔧 fix: update.sh now supports auto-update of OpenClaw config files (AGENTS.md, MEMORY.md, HEARTBEAT.md) and Hooks
  - Add --skip-config option to skip config update
  - Add --skip-hooks option to skip hooks update
  - Auto-update soft links, config files and Hooks
  - Add help info and color output
- 📊 feat: Add memory_detect.py - Compression risk detection
  - Detect memory directory size and estimate context usage
  - Show risk level: safe/warning/critical
  - Provide recommendations based on risk level
- 📊 feat: Add memory_stats.py - Usage statistics
  - Show memory file count, size, keywords count
  - List recent modified files with stars
- 📦 feat: Add memory_snapshot.py - Snapshot management
  - Create/restore snapshots before compression
  - Auto-snapshot when risk level reaches threshold
  - Support listing and restoring snapshots

### 中文
- 📝 docs: 更新 AGENTS.md 和 install.sh，添加主动搜索规则
  - 添加记忆搜索顺序：memory-indexer 最先
  - 添加主动搜索触发词："找找"、"为什么"、"之前"、"记得"
  - 用户提到历史相关内容时自动搜索
- 🔧 fix: update.sh 现在支持自动更新 OpenClaw 配置文件（AGENTS.md, MEMORY.md, HEARTBEAT.md）和 Hooks
  - 添加 --skip-config 选项跳过配置更新
  - 添加 --skip-hooks 选项跳过 Hook 更新
  - 自动更新软链接、配置文件和 Hooks
  - 添加帮助信息和彩色输出
- 📊 feat: 添加 memory_detect.py - 压缩风险检测
  - 检测 memory 目录大小，估算上下文使用量
  - 显示风险等级：safe/warning/critical
  - 根据风险等级提供建议
- 📊 feat: 添加 memory_stats.py - 使用统计
  - 显示 memory 文件数量、大小、关键词数
  - 列出最近修改的文件及星标状态
- 📦 feat: 添加 memory_snapshot.py - 快照管理
  - 压缩前创建/恢复快照
  - 当风险等级达到阈值时自动快照
  - 支持列出和恢复快照

---

## v1.0.9 (2026-03-13)

### English
- 🎨 feat: Add memory_compact.py - Memory files compact script
  - Backup memory/*.md to memory-indexer
  - Compact large files to ~10KB
  - Support command line arguments: --memory-dir, --indexer-dir, --max-size
- ⚙️ config: AGENTS.md startup flow updated to search memory using user_id
- 🔄 integration: heartbeat now auto-runs memory_compact.py
- 🔧 fix: Keyword extraction now filters technical IDs (UUID, hex strings, base64, etc.)
- 🔧 fix: Improved subcommand help messages with examples
- 🐛 fix: memory_compact.py now supports custom paths via command line arguments
- 🐛 fix: session_backup.py now supports custom paths via command line arguments
- 🔧 fix: Keyword extraction now filters GitHub tokens (ghp_xxx, gho_xxx, etc.) and other common API tokens

### 中文
- 🎨 feat: 新增 memory_compact.py - Memory 文件精简脚本
  - 备份 memory/*.md 到 memory-indexer
  - 精简大文件到 ~10KB
  - 支持命令行参数: --memory-dir, --indexer-dir, --max-size
- ⚙️ config: AGENTS.md 启动流程更新为使用 user_id 搜索记忆
- 🔄 integration: heartbeat 新增自动执行 memory_compact.py
- 🔧 fix: 关键词提取现在会过滤技术性 ID（UUID、hex 字符串、base64 等）
- 🔧 fix: 改进子命令帮助信息，添加使用示例
- 🐛 fix: memory_compact.py 现在支持通过命令行参数指定自定义路径
- 🐛 fix: session_backup.py 现在支持通过命令行参数指定自定义路径
- 🔧 fix: 关键词提取现在会过滤 GitHub Token（ghp_xxx, gho_xxx 等）和其他常见 API Token

---

## v1.0.8 (2026-03-13)

### English
- 🔧 fix: session_backup.py improved message extraction, filter System: and JSON metadata, keep only real user messages
- ✨ feat: memory-indexer.py supports --keywords parameter to customize keyword extraction count

### 中文
- 🔧 fix: session_backup.py 改进消息提取，过滤 System: 和 JSON 元数据，只保留真正的用户消息
- ✨ feat: memory-indexer.py 支持 --keywords 参数自定义关键词提取数量

---

## v1.0.5 (2026-03-12)

### English
- ⚙️ config: install.sh now includes Hook installation (memory-indexer-on-new)
- 📖 docs: README added manual Hook installation instructions
- 🔄 integration: install.sh automatically copies Hook to ~/.openclaw/hooks/

### 中文
- ⚙️ config: install.sh 新增 Hook 安装（memory-indexer-on-new）
- 📖 docs: README 添加手动安装 Hook 说明
- 🔄 integration: install.sh 自动复制 Hook 到 ~/.openclaw/hooks/

---

## v1.0.5 (2026-03-12)

### English
- 🎨 feat: Add `hooks/memory-indexer-on-new` - OpenClaw hook for auto-searching memories on new conversation
  - Location: `~/.openclaw/hooks/memory-indexer-on-new/`
  - Listens for `/new` command, automatically calls memory-indexer to search
  - Enabled by default, takes effect after gateway restart
- 🔄 integration: Session backup now runs via heartbeat (not cron - the cron task was misconfigured)
- 🐛 fix: Removed erroneous cron task "session精简" which only sent a message without executing the script

### 中文
- 🎨 feat: 新增 `hooks/memory-indexer-on-new` - 新对话自动搜索记忆的 OpenClaw Hook
  - 位置：`~/.openclaw/hooks/memory-indexer-on-new/`
  - 监听 `/new` 命令，自动调用 memory-indexer 搜索相关记忆
  - 默认启用，gateway 重启后生效
- 🔄 integration: Session 备份改为通过 heartbeat 执行（而非 cron，原 cron 任务配置错误）
- 🐛 fix: 删除错误的 cron 任务"session精简"（只发消息不执行脚本）

---

## v1.0.4 (2026-03-12)

### English
- ⚙️ config: install.sh MEMORY rule added "auto-search memory when new session starts"

### 中文
- ⚙️ config: install.sh MEMORY 规则新增"新会话开始时自动搜索记忆"

---

## v1.0.3 (2026-03-12)

### English
- 📖 docs: 添加"为什么要精简 Session Memory"说明文档
- 🔄 integration: README 说明 session_backup.py 用途和效果

### 中文
- 📖 docs: 添加"为什么要精简 Session Memory"说明文档
- 🔄 integration: README 说明 session_backup.py 用途和效果

---

## v1.0.3 (2026-03-12)

### English
- 🎨 feat: 添加 session_backup.py - 会话备份与精简脚本
- 🔄 integration: heartbeat 自动备份会话内容到 indexer，精简原文件到 10KB

### 中文
- 🎨 feat: 添加 session_backup.py - 会话备份与精简脚本
- 🔄 integration: heartbeat 自动备份会话内容到 indexer，精简原文件到 10KB

---

## v1.0.2 (2026-03-12)

### English
- 🎨 feat: install.sh auto-configures MEMORY.md and HEARTBEAT.md rules
- 🔄 integration: One-click install completes all OpenClaw configurations

### 中文
- 🎨 feat: install.sh 自动配置 MEMORY.md 和 HEARTBEAT.md 规则
- 🔄 integration: 一键安装自动完成所有 OpenClaw 配置

---

## v1.0.1 (2026-03-12)

### English
- 🐛 fix: Fix duplicate search results display bug
- 📁 refactor: Move index data directory to skills/memory-indexer/data/

### 中文
- 🐛 fix: 修复搜索结果重复显示的 bug
- 📁 refactor: 索引数据目录移到 skills/memory-indexer/data/

---

## v1.0.0 (2026-03-12)

### English
- ✅ Initial release
- ✅ Automatic keyword extraction (jieba Chinese segmentation)
- ✅ Keyword index system
- ✅ Multi-keyword search (AND/OR mode)
- ✅ Related discovery
- ✅ Timeline view
- ✅ Proactive recall
- ✅ Memory summary
- ✅ Important memory star
- ✅ Incremental sync
- ✅ Cleanup invalid indexes
- ✅ Importable API
- ✅ Install/update scripts

### 中文
- ✅ 首次发布
- ✅ 自动关键词提取（jieba 中文分词）
- ✅ 关键词索引系统
- ✅ 多关键词搜索（AND/OR 模式）
- ✅ 关联发现
- ✅ 时间线视图
- ✅ 主动提醒
- ✅ 记忆摘要
- ✅ 重要记忆标记
- ✅ 增量同步
- ✅ 失效清理
- ✅ 可导入 API
- ✅ 安装/更新脚本
