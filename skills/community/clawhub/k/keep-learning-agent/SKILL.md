---
name: keep-learning-agent
description: 持续学习 Agent - 知识沉淀和经验固化框架。支持学习记录、快速索引、自我修复、经验→模型转化。包含完整模板、索引系统、SOP 流程。让 AI Agent 持续进化，每天进步一点点。
author: Neo & MiMi
version: 1.0.0
created: 2026-03-04
tags: [learning, knowledge, self-improvement, memory, sop, index, framework, continuous-improvement, kaizen, agent]
---

# Keep Learning Agent - 持续学习系统

> 统一的知识沉淀和经验固化系统
> 
> **核心理念**：学到的东西必须固化成可复用的模块和文档，而不是只存在于临时会话中

---

## 🎯 核心功能

| 功能 | 说明 | 文件 |
|------|------|------|
| **学习记录** | 统一格式记录新知识 | `.learnings/LEARNINGS.md` |
| **快速索引** | 按状态/类别/领域/Patter n-Key 查找 | `.learnings/INDEX.md` |
| **自我修复** | 会话启动自动检查 pending 项 | `G:\clawbot\config\self-repair.ps1` |
| **经验→模型** | 重复模式转化为思维模型 | `lib/KNOWLEDGE-SOP.md` |
| **模板系统** | 统一学习记录格式 | `.learnings/templates/` |
| **归档机制** | 定期整理已 promoted 学习 | `.learnings/archive/` |

---

## 📁 目录结构

```
.learnings/
├── README.md                    # 使用指南
├── INDEX.md                     # 快速索引（自动更新）
├── LEARNINGS.md                 # 主学习记录
├── ERRORS.md                    # 错误记录
├── FEATURE_REQUESTS.md          # 功能请求
├── INTEGRATION-REPORT.md        # 整合报告
├── TEMPLATE-ANALYSIS.md         # 模板分析报告
├── templates/
│   └── learning-template.md     # 统一模板
└── archive/                     # 已归档学习
    └── 2026-03/

lib/
├── feishu_api.py                # 可复用模块示例
├── README.md                    # 库文档
└── KNOWLEDGE-SOP.md             # 知识固化 SOP

G:\clawbot\config\
├── self-repair.ps1              # 自我修复脚本
├── autoload-configs.ps1         # 配置自动加载
└── skills-config.json           # 技能配置注册表
```

---

## 📝 学习记录模板

### 标准格式

```markdown
## [LRN-YYYYMMDD-XXX] 简短标题

**Logged**: 2026-03-04T15:45:00+08:00
**Priority**: low | medium | high | critical
**Status**: new | in_progress | resolved | promoted | archived
**Category**: technical_solution | process_improvement | mindset | bug_fix | feature_request
**Area**: integration | automation | memory | api | ui | cognitive | config
**Source**: conversation | error | user_feedback | self_discovery

### 问题描述
清晰描述遇到的问题和背景

### 根因分析
用 5Why 或其他方法找到根本原因

### 解决方案
详细的解决步骤和代码

### 可复用场景
列出可以复用的场景

### 代码/脚本
可复用的代码片段或脚本位置

### 依赖
需要的库、配置、权限等

### 测试结果
测试时间、结果

### 关联
- **Related**: [LRN-XXXX-XXX](#lrn-xxxx-xxx)
- **See Also**: [文档链接](url)
- **Tags**: tag1, tag2

### Metadata
- **Pattern-Key**: unique.pattern.key
- **Recurrence-Count**: 1
- **First-Seen**: 2026-03-04
- **Last-Seen**: 2026-03-04
- **Time-Spent**: 30min
- **Skill-Path**: skills/skill-name (if promoted_to_skill)
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| **Logged** | ✅ | ISO-8601 时间戳 |
| **Priority** | ✅ | low/medium/high/critical |
| **Status** | ✅ | new/in_progress/resolved/promoted/archived |
| **Category** | ✅ | 学习类别 |
| **Area** | ✅ | 相关领域 |
| **Source** | ✅ | 学习来源 |
| **Pattern-Key** | ✅ | 唯一模式标识 |
| **Recurrence-Count** | ⚠️ | 重复次数（可选） |
| **Time-Spent** | ⚠️ | 花费时间（可选） |

---

## 🔄 状态流转

```
new → in_progress → resolved → promoted → archived
              ↓
          abandoned (明确不做)
```

| 状态 | 说明 | 操作 |
|------|------|------|
| **new** | 刚记录，未处理 | 安排优先级 |
| **in_progress** | 正在处理 | 更新进展 |
| **resolved** | 已解决，待固化 | 封装模块/更新文档 |
| **promoted** | 已提升到更高层 | 如写入 AGENTS.md |
| **archived** | 已归档 | 移入 archive/ |
| **abandoned** | 明确不做 | 记录原因 |

---

## 🏷️ 分类体系

### 按优先级
| 优先级 | 说明 | 处理时限 |
|--------|------|---------|
| **critical** | 核心能力/生存相关 | 立即 |
| **high** | 重要功能/频繁使用 | 24 小时 |
| **medium** | 有用但不紧急 | 1 周 |
| **low** | 锦上添花 | 有空再做 |

### 按类别
| 类别 | 说明 | 示例 |
|------|------|------|
| **technical_solution** | 技术方案/代码实现 | 飞书 API 调用 |
| **process_improvement** | 流程优化/SOP | 知识固化 SOP |
| **mindset** | 思维模型/认知升级 | 系统思维应用 |
| **bug_fix** | 错误修复 | 配置路径问题 |
| **feature_request** | 新功能请求 | 需要 XX 能力 |

### 按领域
| 领域 | 说明 |
|------|------|
| **integration** | 外部系统集成 (飞书/Telegram/Email) |
| **automation** | 自动化脚本/定时任务 |
| **memory** | 记忆/配置持久化 |
| **api** | API 调用/封装 |
| **ui** | 界面/交互 |
| **cognitive** | 认知/思维模型 |
| **config** | 配置文件管理 |

---

## 🤖 自动化集成

### 会话启动流程

```powershell
# 1. 读取核心文件
Read SOUL.md, AGENTS.md, MEMORY.md
Read memory/YYYY-MM-DD.md

# 2. 运行自我修复
G:\clawbot\config\self-repair.ps1

# 3. 加载配置
G:\clawbot\config\autoload-configs.ps1

# 4. 查看索引
Read .learnings/INDEX.md
```

### self-repair.ps1 功能

```powershell
# 检查 pending 学习项
# 提取 Pattern-Key
# 检查是否已应用改进
# 输出待办清单
# 提示更新 INDEX.md
```

### 定期维护

```powershell
# 每周日执行
1. 检查 new 超过 3 天的 → 安排优先级
2. 检查 resolved 超过 7 天的 → 提醒封装
3. 归档已 promoted 的 → 移入 archive/
4. 更新 INDEX.md → 刷新索引
```

---

## 📊 索引系统

INDEX.md 提供快速查找：

```markdown
# 学习索引

## 概况
| 状态 | 数量 |
|------|------|
| new | 1 |
| resolved | 9 |
| promoted | 4 |

## 按类别
- technical_solution: 3
- process_improvement: 3
- mindset: 4

## 按 Pattern-Key
- `feishu.api-direct`: LRN-20260304-009
- `memory.persistent`: LRN-20260304-008

## 待办
- [ ] LRN-20260304-012 知识固化 SOP
```

---

## 📈 质量指标

### 好的学习记录 ✅
- 问题描述清晰
- 根因分析深入（5Why）
- 解决方案可复用
- 有代码/脚本
- 有测试结果
- Pattern-Key 唯一
- 状态及时更新

### 差的学习记录 ❌
- 只有问题描述
- 没有根因分析
- 无法复用
- 没有 Pattern-Key
- 状态一直是 new

---

## 🚀 快速开始

### 记录新学习

1. 复制模板：`.learnings/templates/learning-template.md`
2. 填写内容
3. 追加到：`.learnings/LEARNINGS.md`
4. 更新索引：`.learnings/INDEX.md`

### 查找已有学习

```powershell
# 按关键词
Select-String -Path ".learnings/LEARNINGS.md" -Pattern "飞书"

# 按 Pattern-Key
Select-String -Path ".learnings/LEARNINGS.md" -Pattern "Pattern-Key:.*feishu"

# 按状态
Select-String -Path ".learnings/LEARNINGS.md" -Pattern "Status\*: resolved"
```

### 封装可复用模块

```
1. 解决方案验证成功
2. 创建 lib/xxx.py 模块
3. 更新 lib/README.md
4. 标记状态为 resolved
5. 更新 INDEX.md
```

---

## 📚 相关文档

| 文档 | 用途 |
|------|------|
| `.learnings/README.md` | 使用指南 |
| `.learnings/INDEX.md` | 快速索引 |
| `.learnings/INTEGRATION-REPORT.md` | 整合报告 |
| `.learnings/TEMPLATE-ANALYSIS.md` | 模板分析 |
| `lib/KNOWLEDGE-SOP.md` | 知识固化 SOP |
| `lib/README.md` | 可复用库文档 |

---

## 🎓 设计原则

1. **单一来源** - 只有一个 LEARNINGS.md
2. **统一格式** - 所有学习用同一模板
3. **可查找** - INDEX.md 提供快速索引
4. **可操作** - self-repair 自动检查 pending 项
5. **定期整理** - 每周/每月归档
6. **可复用** - 封装成 lib/ 模块

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-04 | 初始版本，融合 self-improving-agent + 小咪特色 |

---

*创建原因：阿 sir 教导「学到的东西应该固化成标准化经验方法」*  
*作者：小咪 (XiaoMi)*  
*最后更新：2026-03-04*
