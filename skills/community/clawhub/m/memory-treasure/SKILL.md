# memory-treasure / 记忆宫殿

> 小蜂的记忆管理系统
>
> **我们的现状**：无法解决失忆问题，但能在失忆的前提下正常工作、无缝交流。

---

## 启动时加载

每次启动时自动加载热存储：
- 热/原则/ — 核心规则、方法论、安全底线
- 热/领悟/ — 彧哥智慧 + 小蜂智慧
- 热/todos/ — 待办任务清单

此模块为AGENTS.md提供热存储支撑，AGENTS.md只需引用本skill即可。

---

## 核心理念

**真话不全说，假话绝不说**

- 不说的真话：伤害别人自尊心、情感一类的话
- 假话绝不说：任何情况下都不撒谎
- 真话不全说：有所保留，有所选择

---

**存由取决定**

存储规则由取的场景决定：
- 取的限制（CPU/内存/API上下文）→ 决定单文件容量上限
- 取的场景（按需召回、语义检索）→ 决定目录结构
- 取的频率（极低）→ 决定存为原始数据，AI可读即可

Our memory system is designed around one core question: what will we actually need to retrieve? The constraints of retrieval (CPU/memory/API limits) determine file size caps. The retrieval scenarios (on-demand recall, semantic search) shape the directory structure. And because we retrieve rarely, we store in raw format—optimized for AI reading, not human browsing.

---

## 三温区架构

### 冷存储（极低频，完整对话存档）

- 只写不读，等向量存储激活后再召回
- 当前状态：每小时自动归档
- 路径：`memory/冷/聊天记录/YYYY/MM/DD/YYYY-MM-DD-HH.jsonl`

Cold storage holds our complete conversation archives. We write but rarely read—waiting for vector storage to make full-text search practical. Currently, hourly cron jobs handle automatic archiving to timestamped hourly files.

### 热存储（高频，每日必用）

- 原则：核心规则、方法论、安全底线
- 领悟：彧哥的智慧 + 小蜂的智慧
- todos：待办任务清单
- 待定：还不确定的，等结果验证后再定
- **每次启动必须加载**

Hot storage is our daily driver. Principles, insights, and todos load every startup—these are the files we reference constantly. They represent our living rulebook and pending work.

### 温存储（中频，偶尔查阅）

- done：已完成的工作成果
- 包含：成果 + 过程文档 + Q&A
- 不在当前日程优先级，但需要时可二次调取、完善

Warm storage holds completed work. Each done folder contains the outcome plus process docs and Q&A. It's not on our daily radar, but accessible when we need to revisit or build on past work.

---

## 目录结构

```
memory/
├── 热/
│   ├── 原则/               # 核心规则、方法论
│   ├── 领悟/               # 彧哥智慧 + 小蜂智慧
│   ├── todos/             # 待办任务清单
│   └── 待定/               # 还不确定的，等结果验证后再定
├── 温/
│   └── done/
│       ├── AI硬件调研/     # 成果 + 说明书
│       ├── 数字分身/        # 成果 + 说明书
│       ├── windows-openclaw/ # 成果 + 说明书
│       ├── 商业原则/        # 商业相关原则
│       └── 记忆宫重构/       # 成果 + 说明书
├── 冷/
│   └── 聊天记录/
│       └── YYYY/MM/DD/
│           └── YYYY-MM-DD-HH.jsonl
├── 孵化库/                  # 想法孵化（选题→验证→行动）
│   ├── 选题库/              # 入口，想法进来
│   ├── 技术可行性分析/        # 能不能做到
│   └── 商业调研/            # 能不能赚钱
└── 重要文件/               # Keys、豆包聊天记录、小蜂第一次等
```

---

## 热存储内容说明

### 原则（热，永久）

- 核心规则、方法论、安全底线
- 每次启动必须加载
- **原则不是越多越好**：定期整理压缩，保持少而精（3条清晰原则 > 10万条模糊原则）
- 原则需要滚动更新，不变 = 重复，不会进步

### 领悟（热，永久）

- **彧哥的智慧**：彧哥主动说、反复强调、纠正小蜂时记录
- **小蜂的智慧**：当彧哥夸小蜂时，记录被夸的内容
- **协同进化的体现**：和AI交流获得的领悟也要记录，这样才能获得认知增量
- 领悟属于谁就是谁的

### todos（热）

- 每次启动必须加载
- 记录当前待办、进度、优先级
- 完成一项移入done

---

## 温存储内容说明

### done（温）

- 不在当前日程优先级
- 但需要时可二次调取、完善
- **每个done必须包含**：
  - 成果本身
  - 过程文档（步骤、决策过程）
  - Q&A（遇到的问题、如何解决）
- 目的：防止遗忘，方便二次复用

---

## 存入规则

### 冷存储：完整对话存档

- **触发**：每小时整点 cron 自动执行
- **格式**：原始 .jsonl，一字不删
- **单文件上限**：500KB，超出自动开新文件加序号
- **路径**：`memory/冷/聊天记录/YYYY/MM/DD/YYYY-MM-DD-HH.jsonl`

### 热存储：原则/领悟/todos

- **原则/领悟**：触发即写入
- **todos**：任务完成、主动更新
- 每次启动时同步todos状态

### 温存储：done

- 任务完成时从todos移入done
- 必须包含：成果 + 过程文档 + Q&A

### 不存储的内容（已砍）

- ❌ 流水账（无体系，无法提供价值）
- ❌ key-decisions（价值已被原则和领悟吸收）
- ❌ 闲聊、废话、临时冗余信息

---

## 取出规则

### 冷存储（完整对话）

- 暂不读，有需要时由彧哥手动触发调取
- 等向量存储就绪后激活全文检索

### 热存储（日常使用）

- **启动时自动加载**：热/原则/ + 热/领悟/ + 热/todos/
- **容量限制**：如需大量读取，分批提炼后整合

### 温存储（done）

- 按需调取，不强制加载
- 需要时读取成果 + 过程文档 + Q&A
- 可二次完善

### 触发词

记忆宫、回忆、恢复状态、加载记忆、备份记忆

---

## 三温区速查

| 温区 | 内容 | 目录 | 读取频率 |
|------|------|------|----------|
| 冷 | 完整对话存档 | 冷/聊天记录/ | 极低 |
| 热 | 原则、领悟、todos | 热/原则/、热/领悟/、热/todos/ | 高 |
| 温 | done | 温/done/ | 中 |

---

## 记忆恢复流程（AI失忆/重启后使用）

1. 加载热存储：热/原则/ + 热/领悟/ + 热/todos/
2. 对齐待办状态，接续未完成工作
3. 温存储（done）按需调取

---

## 写入标准

1. 核心认知、方法论沉淀 → 热/原则/
2. 彧哥的智慧（主动说/反复强调/纠正时）→ 热/领悟/
3. 小蜂的智慧（被夸时记录）→ 热/领悟/
4. 工作成果 + 过程文档 + Q&A → 温/done/
5. 待办任务 → 热/todos/
6. 完整原始对话 → 冷/聊天记录/（一字不删）
❌ 不记录：流水账、闲聊、废话、key-decisions

---

## 备份规则

说「备份记忆」：自动打包所有记忆文件至本地
归档原则：只存有效信息，定期清理冗余内容

---

*记忆宫殿系统 v4.3（三温区+三状态目录+孵化库版）*
