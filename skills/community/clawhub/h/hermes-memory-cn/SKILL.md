---
name: hermes-memory
description: >-
  给AI装一个「人脑级」记忆系统。它能记住你说过的一切重要信息，下次聊天自动想起来。
  不用云端、不用API Key、不花一分钱——全部数据存在你自己的电脑上。
  说「记住这个」它就记住，问「我上次说了什么」它就找到。自动整理、自动遗忘过时信息。
  适合：想让自己的AI助手拥有长期记忆的用户。
  触发词：记忆、记住、之前说过、上次聊到、搜索记忆、忘了什么。
---

# Hermes-Memory 本地向量记忆系统

**你的AI助手是不是每次聊天都像失忆了？** 这个skill就是解决这个问题的。

Hermes-Memory 给AI装上了长期记忆：记住你的偏好、持仓、策略、教训……下次聊天自动关联上下文，就像跟一个老朋友说话一样。

### 为什么用它？
- **完全本地，隐私零风险** —— 数据存在你电脑上的SQLite文件里，不传任何云端
- **零成本** —— 不需要API Key，不需要付费服务，本地embedding模型免费跑
- **中文优化** —— 专用中文向量模型，搜索准确率远超英文通用模型
- **开箱即用** —— 安装依赖后直接使用，不需要额外启动数据库服务（不像Qdrant/Milvus那样需要单独部署）
- **越用越聪明** —— 自动去重、自动衰减过时记忆、实体关系图谱越建越丰富
- **类型自由定制** —— 内置交易、策略、教训等类型，也可以随时自定义任何新类型

### 和其他方案对比

#### vs 纯文本记忆（MEMORY.md / 每日笔记）
纯文本是大部分AI助手的默认方案——把记忆写在Markdown文件里，每次对话让AI自己翻。

| 维度 | Hermes-Memory | 纯文本记忆 |
|---|---|---|
| 查找方式 | **语义搜索**（"我之前说过什么止损规则"→精准命中） | 关键词匹配或全文翻阅 |
| 记忆容量 | 千条级，搜索毫秒级 | 几百条就开始乱、遗漏 |
| 去重 | 向量相似度>0.95自动合并 | 手动检查，重复越积越多 |
| 过期处理 | 自动衰减+归档 | 永远在文件里，越堆越旧 |
| 结构化 | 按类型/实体/关系组织 | 平铺在一个大文件里 |
| 实体关系 | 多跳图谱（某股→板块→策略→教训） | 无 |
| Token消耗 | 只搜索需要的记忆，按需加载 | 每次要把整个文件喂给AI |

**一句话：** 纯文本适合记10条备忘；Hermes-Memory适合构建一个真正可用的知识库。

#### vs AGENTS.md 内置记忆逻辑
很多用户会在AGENTS.md里写一段记忆规则，让AI自己维护Markdown文件。这个方案能用，但有几个本质限制：

| 维度 | Hermes-Memory | AGENTS.md规则+Markdown |
|---|---|---|
| 存储引擎 | SQLite + 向量索引 + FTS5 | 纯文本文件 |
| 搜索能力 | 向量语义搜索 + 全文搜索 + 关系查询 | 只能靠AI逐行读文件 |
| 可靠性 | **确定性**——CLI命令执行即写入，不依赖AI"记得去写" | **不确定**——AI可能忘写、写错格式、漏写 |
| 写入触发 | CLI工具一键写入（memdb.py add / memory_tool.py check） | 依赖AI每次对话后主动执行，无强制保证 |
| 跨会话 | SQLite文件是唯一真相源，任何session读取一致 | 多个daily note + MEMORY.md，容易不一致 |
| 关系推理 | 实体图谱支持多跳查询（"跟这只股票相关的所有教训"） | 无结构化关系，全靠AI自己关联 |
| 自动维护 | decay归档+去重+export，cron一条命令搞定 | 需要AI手动整理文件，容易堆积垃圾 |
| 可扩展性 | 类型自定义、关系自由扩展 | 文件越大AI越容易遗漏 |

**核心差异：** AGENTS.md记忆规则是"靠AI自觉"——提示词让它记，但执行没有保证。Hermes-Memory是"工具保证"——CLI命令执行就写入，搜索就返回，不依赖AI的注意力。

#### vs 云端向量库（Qdrant / Milvus / Pinecone）

| 维度 | Hermes-Memory | 云端向量库 |
|---|---|---|
| 部署难度 | pip install即可 | 需要启动独立服务或注册云服务 |
| 隐私安全 | ✅ 完全本地 | ⚠️ 需自建或信任第三方 |
| 成本 | 免费 | 云服务按量计费 / 自建服务器成本 |
| 大规模性能 | 千条级优秀 | 百万级优秀 |
| 中文支持 | ✅ 专用中文模型 | ⚠️ 需额外配置embedding |

**一句话：** 个人使用千条级别，Hermes-Memory更简单更安全；企业级百万条数据，上云端方案。

## 快速开始

所有命令必须用 Python 3.12+（支持OpenSSL 3.0+），macOS推荐 `/opt/homebrew/bin/python3.12`。

```bash
# 搜索记忆（语义搜索，支持中文）
python3 scripts/memdb.py search "止损策略" --limit 5

# 添加记忆
python3 scripts/memdb.py add "内容" --type portfolio --entity 某科技股

# 智能检测关键词并写入
python3 scripts/memory_tool.py check "用户说的内容"

# 建立实体关系
python3 scripts/memdb.py relate "某科技股" "属于" "医药板块"

# 查看实体关系（支持多跳）
python3 scripts/memdb.py relations "某科技股" --depth 2

# 统计
python3 scripts/memdb.py stats
```

## 记忆类型

类型完全开放，可自由扩展。以下是内置推荐类型：

### 通用类型
| type | 用途 | 示例 |
|------|------|------|
| preference | 用户偏好 | 数据源用东财、回复用中文 |
| user-profile | 用户画像 | 用户基本信息和背景 |
| fact | 事实/决策 | 用户的重要决定 |
| note | 笔记 | 其他 |
| lesson | 教训（带severity） | 缺乏风控导致亏损 |

### 交易/投资类型（内置，可按需使用）
| type | 用途 | 示例 |
|------|------|------|
| portfolio | 持仓变动 | 买入某科技股、清仓某消费股 |
| strategy | 策略规则 | 主线共振策略买点、情绪周期L4 |
| market-view | 大盘/板块判断 | 大盘缩量反弹，半导体主线 |
| trade-plan | 交易计划 | 某股跌破MA20则止损 |
| stock-note | 个股研究笔记 | 某股：行业龙头，产能扩张期 |
| watchlist | 关注标的 | 关注某股回调至20日线 |
| review | 复盘结论 | 本周操作：胜率40%，亏损来自追高 |

**自定义类型：** `--type` 参数接受任意字符串，无需预定义。根据你的使用场景自由创造类型：
```bash
# 程序员用户可能用
type=bugfix type=architecture type=deploy

# 创作者用户可能用
type=idea type=draft type=publish

# 学生用户可能用
type=course type=exam type=schedule
```

## 实时写入规则

每次回复用户后，检查是否有值得长期记住的信息：

**关键词触发（用 memory_tool.py check）：**
- 买了/卖了/加仓/减仓/清仓/建仓/止盈/止损 → portfolio
- 新策略/改策略/情绪周期/买点卖点 → strategy
- 纠正我/不对/错误/教训/踩坑 → lesson
- 以后用/记住/偏好/改用 → preference

**LLM判断（直接用 memdb.py add）：**
- 隐含信息（用户随口提到的新方向、生活变化）→ fact
- 重要决策 → fact
- **根据对话领域自适应选择类型**，不限于上表
- **遇到新模式可创造新类型**，`--type` 无白名单限制

**判断标准：** 这条信息1周后还有用吗？是→写入，否→跳过。

## 实体关系图谱

写入记忆时，主动建立实体间关联：

```bash
# 股票→板块
python3 scripts/memdb.py relate "某科技股" "属于" "医药板块"
# 策略→组件
python3 scripts/memdb.py relate "主线共振策略" "包含" "买点规则"
# 教训→应用
python3 scripts/memdb.py relate "某股亏损" "教训应用于" "止损规则"
```

## 自动维护

- **衰减：** `memdb.py decay --days 30` 标记30天未更新的记忆为expired
- **归档：** `memdb.py archive` 将expired记忆移入archive表
- **导出：** `memdb.py export --dir ./entities` 同步Markdown可读备份
- **导入：** `memdb.py import --dir ./entities` 从Markdown导入

推荐Cron每晚23点执行：decay → export → stats。

## CLI完整参考

```bash
# ── 记忆操作 ──
python3 scripts/memdb.py add "内容" --type <type> [--entity <实体>] [--severity high|medium|low] [--source manual|conversation|cron]
python3 scripts/memdb.py search "查询" [--type <type>] [--status active|expired] [--entity <实体>] [--limit N] [--format text|json]
python3 scripts/memdb.py list [--type <type>] [--status active] [--limit N]
python3 scripts/memdb.py relate "实体A" "关系" "实体B"
python3 scripts/memdb.py relations "实体" [--depth 1|2|3] [--direction from|to|both]
python3 scripts/memdb.py unrelate "实体A" "关系" "实体B"
python3 scripts/memdb.py decay [--days 30]
python3 scripts/memdb.py archive
python3 scripts/memdb.py export --dir <目录>
python3 scripts/memdb.py import --dir <目录>
python3 scripts/memdb.py stats

# ── Skill进化 ──
python3 scripts/skill_evolve.py record "操作模式" --tags "标签1,标签2"
python3 scripts/skill_evolve.py detect
python3 scripts/skill_evolve.py draft <pattern_id> [--name "skill-name"]
python3 scripts/skill_evolve.py promote <pattern_id> --name "skill-name"
python3 scripts/skill_evolve.py list
```

## 详细文档

- **安装指南：** 见 [references/install.md](references/install.md)
- **AGENTS.md集成：** 见 [references/integration.md](references/integration.md)

## Skill进化系统

受 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的闭环学习启发，hermes-memory-cn 增加了自动模式检测和skill提炼能力。

### 工作流
```
完成多步骤任务 → skill_evolve.py record → 向量检测相似模式
                                                ↓
                          同一模式出现≥3次 → 自动通知候选
                                                ↓
                          skill_evolve.py draft → 生成草案到 skill_drafts/
                                                ↓
                          用户审核 → skill_evolve.py promote → 正式skill
```

### 命令
```bash
# 记录操作模式
python3 scripts/skill_evolve.py record "步骤1→步骤2→步骤3" --tags "标签"

# 检测候选
python3 scripts/skill_evolve.py detect

# 生成草案
python3 scripts/skill_evolve.py draft <id> --name "skill-name"

# 确认升级
python3 scripts/skill_evolve.py promote <id> --name "skill-name"

# 查看所有模式
python3 scripts/skill_evolve.py list
```

### 与 Hermes Agent 对比

| 维度 | Hermes Agent | Hermes Memory CN |
|------|-------------|-----------------|
| **定位** | 完整Agent框架（自研内核+工具+消息平台） | 专注记忆层的工程优化 |
| **记忆存储** | Markdown(3600字符硬上限) | SQLite+向量DB(千条级) |
| **检索方式** | FTS5+LLM摘要 | 向量语义搜索+FTS5+关系图谱 |
| **容量管理** | 硬上限强制精简 | 自动衰减+去重+归档 |
| **skill进化** | ✅ 自动沉淀（成熟） | ✅ 模式检测+草案生成（新增） |
| **冻结注入** | ✅ 保护prefix cache | ❌ 无 |
| **中文优化** | 无 | 专用text2vec-base-chinese |
| **实体关系** | 无 | 多跳图谱查询 |
| **部署门槛** | 低（一个CLI） | 中（需装embedding模型） |

**关系定位：** Hermes Agent 定义了"AI应该有长期记忆"的范式——反思循环、跨session持久化、skill自动沉淀。Hermes Memory CN 继承这个理念，在记忆存储层做了工程升级：从Markdown到向量数据库，从关键词搜索到语义检索，从几十条到千条级。两者互补，不是替代关系。

## 架构

```
用户对话 → LLM判断/关键词触发 → memdb.py add/relate → SQLite + 向量DB
                                                        ↓
                        Cron每晚 ← decay + export ← entities/ Markdown备份
```

**技术栈：**
- 存储层：SQLite（结构化数据）+ sqlite-vec（向量索引）+ FTS5（全文搜索）
- Embedding：text2vec-base-chinese（768维，本地运行，MPS加速）
- 关系层：relations表（实体关系图谱，支持多跳BFS查询）
- 去重：向量余弦相似度 >0.95 自动合并
