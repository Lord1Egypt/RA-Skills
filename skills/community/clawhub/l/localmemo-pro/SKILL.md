---
slug: localmemo-pro
name: localmemo-pro
version: "2.0.0"
displayName: 本地长记忆
summary: 零API零云依赖的本地向量记忆：离线可用、隐私不出域、embedding缓存省成本。
license: MIT
description: |-
  面向隐私敏感与离线场景的本地向量记忆系统。基于 LanceDB + 纯本地 embedding（Ollama/nomic-embed-text），实现零外部 API 调用、零数据出域、完全离线可用的语义记忆检索。

  核心能力包括本地 embedding 引擎（Ollama nomic-embed-text，毫秒级延迟）、LanceDB 向量库（本地 SQLite 存储）、embedding 结果缓存（避免重复计算）、WAL 写前日志、三层冷热分层、资源占用控制（内存上限/压缩/清理）、一键初始化与维护命令。

  适用场景：隐私敏感行业（医疗/金融/法律）、离线/弱网环境、个人知识库、合规要求数据不出域的企业 Agent、希望零 API 成本运行的独立开发者。

  差异化：相比云端 embedding 方案，本系统完全本地运行零 API 费用、数据永不离开本机、离线可用；相比简单文件记忆，提供向量语义检索召回更准；新增 embedding 缓存避免重复计算、资源占用控制防止内存膨胀、模型选择指南平衡质量与速度。指令精简分层，降低 token 消耗。

  触发关键词：本地记忆、向量记忆、离线记忆、隐私记忆、embedding、LanceDB、Ollama、nomic、本地向量、local memory
tags:
- 智能代理
- 记忆管理
- 本地存储
tools:
- read
- exec
---

# 本地长记忆（LocalMemo Pro）

**零 API、零云端、零数据出域**的本地向量记忆系统。基于 Ollama + LanceDB，在本地完成 embedding 生成与语义检索，适合隐私敏感、离线、成本敏感场景。

## 痛点与对策速查

| 用户痛点 | 发生场景 | 本系统对策 |
|:---|:---|:---|
| 数据隐私担忧 | 云端 embedding 数据出域 | 纯本地 Ollama embedding，数据不出本机 |
| API 费用高 | 云端 embedding 按 token 收费 | 本地 nomic-embed-text 完全免费 |
| 离线不可用 | 无网络时记忆系统瘫痪 | 本地运行，完全离线可用 |
| 重复计算浪费 | 相同文本反复生成 embedding | embedding 结果缓存，命中即返回 |
| 内存膨胀 | 向量库无限增长占满内存 | 资源占用控制 + 压缩 + 清理 |
| 质量担忧 | 本地模型不如云端 | 提供模型选择指南，质量够用且可切换 |
| 部署复杂 | 本地栈搭建门槛高 | 一键初始化 + 详细故障排查 |

## 本地 vs 云端对比

| 对比维度 | 云端 API（OpenAI） | 本地方案（Ollama） |
|:---|:---|:---|
| 费用 | 按 token 收费 | 完全免费 |
| 延迟 | 网络往返 100-500ms | 本地 10-50ms |
| 隐私 | 数据出域 | 完全本地 |
| 离线 | 不可用 | 完全可用 |
| 质量 | text-embedding-3-large | nomic-embed-text（足够） |
| 资源占用 | 零本地资源 | 需 2-4GB 内存 |
| 部署难度 | 仅需 API Key | 需安装 Ollama |

**结论**：个人/小团队/隐私场景用本地；追求极致质量且不敏感数据用云端。

## 架构

```text
┌───────────────────────────────────────────────────────────────┐
│                   LOCALMEMO PRO 本地架构                        │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  L1 热内存     SESSION-STATE.md    活跃任务上下文（抗压缩）     │
│      ↓                                                         │
│  L2 温向量     LanceDB            本地向量检索（embedding缓存）│
│      ↓         ↑ embedding 由 Ollama 本地生成                  │
│  L3 冷存储     Git-Notes          结构化决策（永久）           │
│      ↓                                                         │
│  L4 精选归档   MEMORY.md + daily/ 人类可读长期记忆             │
│                                                                │
│  全程零外部 API · 零数据出域 · 离线可用                        │
└───────────────────────────────────────────────────────────────┘
```

## 快速开始（3 步）

### 第 1 步：安装本地 embedding 引擎

```bash
# 安装 Ollama
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: 从 https://ollama.com/download 下载安装包

# 拉取 embedding 模型（约 274MB）
ollama pull nomic-embed-text

# 验证
ollama --version
```

### 第 2 步：初始化记忆系统

```bash
cd skills/localmemo-pro
npm install
node bin/init.js
```

初始化创建：
- `SESSION-STATE.md` — 热内存
- `MEMORY.md` — 长期记忆
- `memory/` — 每日日志目录
- `memory/vectors/` — LanceDB 向量数据库
- `memory/cache/` — embedding 缓存目录

### 第 3 步：使用记忆工具

```bash
# 存储
node bin/memory.js store "用户喜欢深色模式" --importance 0.9 --category preference

# 搜索
node bin/memory.js search "用户界面偏好"

# 统计
node bin/memory.js stats

# 遗忘
node bin/memory.js forget --query "深色模式"
```

## Embedding 缓存机制（差异化核心）

相同文本反复生成 embedding 是本地系统的主要性能瓶颈。本系统实现 embedding 缓存：

```text
文本 → SHA256(文本) → 查缓存目录
                          ├─ 命中 → 直接返回向量（<1ms）
                          └─ 未命中 → Ollama 生成 → 写入缓存（10-50ms）
```

| 操作 | 无缓存耗时 | 有缓存耗时 | 命中率（典型） |
|:---|:---|:---|:---|
| 存储记忆 | 30-50ms | <1ms（命中）/ 30-50ms（未命中） | 70-90% |
| 检索记忆 | 30-50ms × N | <1ms × N（命中） | 60-80% |

### 缓存配置

```json
{
  "embeddingCache": {
    "enabled": true,
    "path": "./memory/cache",
    "maxSizeMb": 500,
    "ttlDays": 90,
    "compression": true
  }
}
```

缓存达到上限时自动 LRU 淘汰最久未用的 embedding。

## 模型选择指南

| 模型 | 大小 | 维度 | 质量 | 速度 | 推荐场景 |
|:---|:---|:---|:---|:---|:---|
| nomic-embed-text | 274MB | 768 | 中高 | 快 | 通用推荐 |
| bge-m3 | 1.2GB | 1024 | 高 | 中 | 多语言/高质量需求 |
| mxbai-embed-large | 670MB | 1024 | 高 | 中 | 英文高质量 |
| all-MiniLM-L6 | 90MB | 384 | 中 | 极快 | 资源受限设备 |

**推荐**：默认用 nomic-embed-text（质量/速度/大小均衡）。资源紧张用 all-MiniLM-L6，质量优先用 bge-m3。

## WAL 写前日志协议

**原则：先写状态，再回复用户。** 保证崩溃/压缩时不丢上下文。

| 触发条件 | 写入位置 | 写入时机 |
|:---|:---|:---|
| 用户表达偏好 | SESSION-STATE.md + memory store | 回复前 |
| 用户做出决策 | SESSION-STATE.md + Git-Notes | 回复前 |
| 用户给出期限 | SESSION-STATE.md | 回复前 |
| 用户纠正错误 | SESSION-STATE.md + lessons.md | 回复前 |

## 资源占用控制（差异化核心）

本地系统最大风险：向量库无限增长导致内存/CPU/磁盘膨胀。

### 三级资源控制

| 级别 | 触发条件 | 控制措施 |
|:---|:---|:---|
| 轻度 | 向量数 > 10000 | 自动压缩低重要性向量 |
| 中度 | 磁盘 > 500MB | 归档 90 天前记忆到文件 |
| 重度 | 磁盘 > 1GB | 告警 + 停止写入（仅检索） |

### 维护命令

```bash
# 查看资源占用
node bin/memory.js stats --detailed

# 压缩向量库
node bin/memory.js compact

# 清理旧记忆
node bin/memory.js cleanup --before 30d

# 去重
node bin/memory.js dedup

# 导出备份
node bin/memory.js backup ./backups/memory-$(date +%Y%m%d).zip

# 清理 embedding 缓存
node bin/memory.js cache-clean --older-than 30d
```

## Agent 配置集成

在 Agent 配置文件中启用本地记忆插件：

```json
{
  "plugins": {
    "entries": {
      "localmemo-pro": {
        "enabled": true,
        "config": {
          "ollamaUrl": "http://localhost:11434",
          "embeddingModel": "nomic-embed-text",
          "dbPath": "./memory/vectors",
          "cachePath": "./memory/cache",
          "autoRecall": true,
          "autoCapture": false,
          "maxMemoryMb": 500,
          "minImportance": 0.5
        }
      }
    }
  }
}
```

启用后自动提供工具：
- `memory_recall` — 搜索相关记忆
- `memory_store` — 存储重要信息
- `memory_forget` — 删除记忆

## 代理行为指令

### 会话开始时

1. 读取 SESSION-STATE.md（热内存）
2. 执行 memory_recall 搜索相关历史
3. 检查 memory/YYYY-MM-DD.md 近期活动

### 对话进行中

| 情境 | 动作 |
|:---|:---|
| 用户给出具体细节 | 先写 SESSION-STATE.md，再回复 |
| 重要决策 | memory_store 存储 |
| 表达偏好 | memory_store --importance 0.9 --category preference |
| 出现错误 | 写入 lessons.md |

### 会话结束时

1. 更新 SESSION-STATE.md 最终状态
2. 重要内容移至 MEMORY.md
3. 创建/更新 memory/YYYY-MM-DD.md

## 真实场景示例

### 场景 1：医疗隐私场景

```text
用户："记录患者对青霉素过敏"
→ 本地 embedding 生成（数据不出域）
→ memory_store："患者青霉素过敏" importance=1.0 category=medical
→ 存储在本地 LanceDB，符合 HIPAA 合规

后续查询：
  memory_recall query="患者过敏史"
  → 本地检索，零数据外传
```

### 场景 2：离线开发场景

```text
环境：飞机上无网络，本地开发

用户："上次我们怎么解决 CORS 问题的？"
→ memory_recall query="CORS 跨域解决"
→ 本地 Ollama 生成 query embedding（离线）
→ LanceDB 本地检索
→ 召回："CORS 用代理中间件解决，配置在 middleware/cors.js"
→ 无需网络即可回忆历史决策
```

### 场景 3：成本敏感场景

```text
独立开发者，月 API 预算 $0

存储 1000 条记忆：
  云端方案：embedding 费用约 $0.5-1/月
  本地方案：$0（一次性模型下载 274MB）

检索 100 次/天：
  云端方案：embedding 费用约 $0.3/月
  本地方案：$0（embedding 缓存命中后 <1ms）

年度节省：约 $10-15
```

## 常见问题 FAQ

**Q1：本地 embedding 质量够用吗？**
A：nomic-embed-text 在 MTEB 基准上表现接近 text-embedding-3-small，对个人/小规模记忆库完全够用。如需更高质量可切换 bge-m3。

**Q2：Ollama 占多少内存？**
A：nomic-embed-text 运行时约 2-4GB 内存。资源紧张可用 all-MiniLM-L6（约 500MB）。

**Q3：embedding 缓存会占多少磁盘？**
A：每条记忆的 embedding 约 3KB（768 维 float32）。10000 条记忆约 30MB，缓存上限可配置（默认 500MB）。

**Q4：能和云端方案混用吗？**
A：可以。重要记忆用云端高质量 embedding，日常用本地。但需注意维度一致性，建议统一用一种。

**Q5：向量库损坏怎么办？**
A：定期 `node bin/memory.js backup` 备份。损坏后从备份恢复，或从 MEMORY.md + daily/ 重建（记忆内容仍在文件中）。

## 故障排查

| 现象 | 排查步骤 | 解决方案 |
|:---|:---|:---|
| Ollama 连接失败 | `curl http://localhost:11434/api/tags` | `ollama serve` 启动服务 |
| 模型未找到 | `ollama list` | `ollama pull nomic-embed-text` |
| 向量搜索无结果 | `node bin/memory.js stats` | 确认已存储记忆；检查 dbPath |
| 内存占用过高 | `node bin/memory.js stats --detailed` | 运行 compact + cleanup |
| embedding 速度慢 | 检查缓存命中率 | 确认 cache.enabled=true |
| 磁盘满 | 检查 vectors/ 和 cache/ 大小 | 清理缓存 + 归档旧记忆 |
| 检索质量差 | 检查 minScore 设置 | 降低 minScore 到 0.25；换更大模型 |

## 文件结构

```text
workspace/
├── SESSION-STATE.md          # 热内存
├── MEMORY.md                 # 精选长期记忆
├── memory/
│   ├── vectors/              # LanceDB 向量库
│   ├── cache/                # embedding 缓存
│   ├── 2026-07-18.md         # 每日日志
│   ├── lessons.md            # 教训记录
│   └── topics/               # 主题文件
├── bin/
│   ├── init.js               # 初始化脚本
│   └── memory.js             # 记忆管理 CLI
└── localmemo-config.json     # 配置文件
```

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Node.js**：16+（运行记忆管理脚本）
- **内存**：建议 8GB+（Ollama 运行需 2-4GB）
- **磁盘**：建议 2GB+ 可用空间

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---|:---|:---|:---|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| Ollama | 本地推理引擎 | 必需 | https://ollama.com/install |
| nomic-embed-text | embedding 模型 | 必需 | `ollama pull nomic-embed-text` |
| LanceDB | 向量数据库 | 必需 | `npm install vectordb` |
| Git | 版本控制 | 可选 | 用于 Git-Notes 冷存储 |

### API Key 配置
- **本 Skill 核心功能无需任何 API Key**
- 完全本地运行，零外部 API 调用
- 如需可选的云端备份功能，另行配置对应服务 Key

### 可用性分类
- **分类**：MD+EXEC（Markdown 指令 + exec 命令行执行）
- **说明**：基于 Markdown 的 AI Skill 驱动 Agent 执行本地记忆管理。核心记忆协议纯 Markdown 可工作；向量检索、embedding 生成需 Ollama + LanceDB 环境。
