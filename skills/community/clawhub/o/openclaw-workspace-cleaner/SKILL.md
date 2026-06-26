---
name: workspace-cleaner
description: "优化 OpenClaw 工作区基础文件（AGENTS/MEMORY/SOUL/TOOLS/IDENTITY/USER），减少上下文噪音。执行前必须列出优化方案并获得确认。"
metadata: {"openclaw":{"emoji":"🧹","requires":{"anyBins":[]}}}
---

# workspace-cleaner

优化 OpenClaw 工作区的基础文件结构，减少每次对话的上下文注入量。

**核心原则**：只保留当前有用的内容，无用内容移到深度存储或删除。不创造噪音。

---

## 优化流程

### STEP 1 — 分析当前文件

读取所有 bootstrap 文件，评估每个 section 的：
- **实际使用频率**：这个内容实际被用到过吗？
- **冗余程度**：是否与其他文件重复？
- **归属层次**：热缓存（MEMORY.md）还是深度存储（memory/）？

bootstrap 文件清单：
```
MEMORY.md     — 热缓存，当前最需要的信息
SOUL.md       — Agent 灵魂定义，风格/行为准则
AGENTS.md     — 行为协议，工具规范，飞书协议
TOOLS.md      — 本地工具笔记，skill 覆盖不到的配置
IDENTITY.md   — 身份定义（name/emoji/platform）
USER.md       — 用户信息（多用户系统下应极简）
BOOTSTRAP.md  — 首次运行引导（已完成使命应删除）
```

### STEP 2 — 制定优化方案

分析后，列出优化方案，**必须包含**：

```
待优化项：
1. [文件] [问题] → [处理方式]
2. ...

预计变化：
- [文件]：[原大小] → [新大小]
- 总计：减少约 [%]

优化后文件结构：
[简单树状图]
```

### STEP 3 — 确认后执行

**必须得到用户确认后才能执行修改**。列出方案后停下来，等待用户说"可以"或"执行"。

收到确认后：
1. 执行文件修改
2. 将移出的内容归档到 `memory/` 对应目录
3. 删除 BOOTSTRAP.md（如有）
4. 汇报结果

### STEP 4 — 写日记

将本次优化过程记录到 `memory/daily/YYYY-MM-DD.md`：
```
## 上下文精简
- [文件A]：[原大小] → [新大小]
- [文件B]：[原大小] → [新大小]
归档：移出的内容 → [目标路径]
```

---

## 优化判断标准

### 应移出的内容

| 类型 | 判断 | 目标位置 |
|------|------|---------|
| 静态 People 表 | contacts skill 已有 | `memory/contacts/contacts.d/` |
| 静态 Terms 表 | glossary 已有 | `memory/glossary.md` |
| 技术细节/架构 | 按需查阅 | `memory/knowledge/` |
| 环境配置 | 变化少 | `memory/context/` |
| 失败教训 | 经验累积 | `memory/post-mortems.md` |
| 与 AGENTS 重复内容 | AGENTS 已有 | 删除 |

### 应删除的内容

- **未使用过的规则**：晋升/降级具体频率、Supersede 机制、项目关闭规则（从未实际执行过）
- **重复内容**：MEMORY/AGENTS/SOUL 三处重复的 Preferences/Protocols
- **与 Skills 重复的流程**：MEMORY/AGENTS 里记录的操作流程，如果已有对应 Skill，则精简或删除该部分（Skills 本身已有完整指引，热缓存里不需要重复）
- **失效文件**：BOOTSTRAP.md（首次运行后失效）
- **占位符**：未填实的 `[描述你的个性]` 类内容

### 保留在热缓存的

- 当前项目状态（Projects 表）
- 当前 Skills 清单（精简版）
- 报告投递配置（飞书群 ID 等）
- 必要的 TODO（影响行为的关键事项）

### 精简原则

- **不写精确规则**：无法追踪的频率（如"一周使用3次以上"）删掉
- **不写重复内容**：已在 AGENTS.md 的内容，MEMORY.md 不重复
- **各负其责**：项目内容放各自项目目录，不堆在 MEMORY.md

---

## 深度存储目录结构

```
memory/
├── daily/           — 每日日记
├── glossary.md      — 术语解码
├── people/          — 人物档案（结构化）
├── contacts/        — 通讯录（contacts skill）
├── knowledge/        — 技术知识
│   ├── fw-*.md      — 飞书相关
│   ├── pat-*.md     — 模式/反模式
│   ├── sys-*.md     — 系统架构
│   └── ref-*.md     — 参考资料
├── context/         — 环境上下文
├── post-mortems.md  — 失败教训
└── services/        — 服务记录
```

---

## 归档要求

将内容移到深度存储时：
1. 检查目标文件是否已存在
2. 如已存在，在末尾追加（不覆盖）
3. 如不存在，创建新文件（带标题和日期）

**注意**：不要跨目录修改其他 agent 的文件，只能修改自己的工作区。

---

## 安全约束

- **只改自己的工作区**：每个 agent 只能修改自己的 workspace，不能改别人
- **不修改其他 agent 的 skills**：改自己目录的 skills
- **不删除他人的 memory 内容**：归档自己的，不碰别人的
