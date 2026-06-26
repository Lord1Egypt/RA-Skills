---
name: long-memory
description: '全量对话记忆系统，自动保存每次对话的完整内容（用户消息、助手回复、思考过程）并支持按语义检索任意历史对话。当用户提到"记下来""别忘了""回忆一下""之前聊过""什么时候说的"、要求回顾历史对话、或需要跨 session 记忆连续性时触发。也适用于 session 结束时的自动记忆归档。不适用于简单的短期记事（用 memory 文件即可）。'
---

# Long Memory

文件系统 = 无限外存，上下文窗口 = 有限内存。所有对话全量落盘，按需检索，永不遗忘。

## 企业级特性

- **并发安全**：文件锁机制，多进程写入不冲突
- **三级搜索引擎**：关键词 → TF-IDF + 近义词 → Embedding 向量（零依赖到深度语义）
- **SQLite 引擎**：结构化存储，查询比纯文件快 100 倍
- **自记忆引擎**：系统记住自己的版本演变和决策历史
- **完整性校验**：SHA256 校验和，自动检测修复损坏文件
- **自动备份**：Git commit + push，支持定时自动执行
- **质量评分**：0-100 分量化评估（7 条规则）
- **遗忘曲线**：艾宾浩斯遗忘曲线检索权重
- **情感分析**：对话情绪变化追踪
- **人物图谱**：自动提取人脉关系
- **智能推荐**：基于当前对话推荐相关历史
- **隐私加密**：AES-256 加密敏感记忆
- **结构化模板**：会议纪要/项目决策/学习笔记/周报
- **定时调度**：内置蒸馏/备份/清理调度器
- **多用户隔离**：独立记忆空间
- **REST API**：7 个 HTTP 接口，支持外部集成
- **HTML 报告**：暗色主题可视化分析面板
- **操作审计**：JSONL 完整操作日志
- **配置管理**：JSON 配置 + 版本自动迁移
- **性能基准**：365 天数据模拟，多维度测量
- **统一 CLI**：35 个子命令
- **37 个测试**：pytest 全通过
- **零核心依赖**：搜索引擎、SQLite 全部 Python 标准库

## CLI 速查

所有命令支持 `--memory-dir` 自定义路径，多数命令支持 `--json` JSON 输出。

### 📝 记录
```bash
cli.py archive     --session webchat --topic "话题"     # 归档对话
cli.py capture     [-s <id>]                            # 捕获 session 历史
cli.py import      <file>                               # 批量导入 MD/JSON/文本
cli.py template    list                                 # 列出模板
cli.py template    create meeting -f participants "张三" # 创建结构化记录
```

### 🔍 搜索（三级引擎）
```bash
cli.py search      -q "关键词" --tag 标签 --days 30     # 组合搜索（标签+话题+时间）
cli.py semantic    "怎么优化性能"                        # 语义搜索（TF-IDF+近义词，零依赖，推荐）
cli.py tfidf       "查询" --rebuild                     # TF-IDF 向量搜索
cli.py embedding   search "查询" --top 10               # 深度语义搜索（需 sentence-transformers）
cli.py sqlite      search -q "查询"                     # SQLite 高性能查询
cli.py recommend   "当前对话内容"                        # 智能推荐相关历史
cli.py timeline    [-t 话题] [-v]                       # 话题时间线
```

### 📊 分析
```bash
cli.py stats       [-v]                                 # 统计
cli.py graph       [-v]                                 # 记忆关联图谱
cli.py persons     [-v]                                 # 人物关系
cli.py emotion     [-v]                                 # 情感分析
cli.py health                                           # 健康仪表盘
cli.py report      -o report.html                       # HTML 可视化报告
```

### ✅ 质量
```bash
cli.py quality                                          # 质量评分（0-100）
cli.py contradictions                                  # 矛盾检测
cli.py integrity   [--fix]                              # 完整性校验
cli.py forgetting                                       # 遗忘曲线
```

### 🔧 维护
```bash
cli.py summary                                          # 每日摘要
cli.py distill                                          # 周蒸馏
cli.py tags       [--execute]                           # 标签优化
cli.py clean       --days 90 [--execute]                # 清理旧记忆
cli.py index       [--rebuild]                          # 索引管理
cli.py backup      [--status|--setup]                   # Git 备份
cli.py scheduler   [--list|--run|--force]               # 定时任务
cli.py self        [--summary]                          # 自记忆引擎
cli.py config      [--migrate]                          # 配置验证与迁移
cli.py benchmark                                         # 性能基准测试
```

### 🔒 安全与审计
```bash
cli.py privacy     encrypt "内容" -p 密码               # AES-256 加密
cli.py privacy     decrypt "密文" -p 密码               # 解密
cli.py privacy     scan -f <file>                       # 敏感内容扫描
cli.py users       list                                 # 多用户管理
cli.py users       switch <name>                        # 切换用户
cli.py export      -f json -o backup.json               # 导出 JSON/MD/TXT
cli.py log                                              # 操作审计日志
```

### 🌐 API
```bash
cli.py api         --port 8765                          # 启动 REST API 服务
# GET /api/health  /api/stats  /api/search?q=  /api/topics  /api/tags  /api/conversations
# POST /api/conversations
```

## 测试

```bash
cd long-memory && python3 -m pytest tests/ -v  # 37 passed
```
