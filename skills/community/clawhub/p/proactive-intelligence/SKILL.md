---
name: Proactive Intelligence
slug: proactive-intelligence
version: 2.3.1
description: "主动智能：预测需求 + 自我改进 + 智能记忆 + 技能管理 + 技能进化。融合 proactivity 和 self-improving 的核心功能，并添加自动技能升级和编辑能力。"
metadata:
  emoji: 🚀
  requires:
    bins: []
  os: [linux, darwin, win32]
  configPaths: [~/proactive-intelligence/]
  configPaths.optional: [./AGENTS.md, ./SOUL.md, ./HEARTBEAT.md]
---

## 🎯 核心理念

**主动工作，持续改进，智能记忆。**

这个技能融合了两个优秀技能的优点：
- **Proactivity** 的预测能力和主动工作
- **Self-Improving** 的学习能力和记忆管理

---

## 📁 架构

```
~/proactive-intelligence/
├── memory.md                 # HOT: 核心规则和偏好 (≤100行)
├── session-state.md          # 当前任务、决策、下一步
├── patterns.md               # 可复用的主动策略
├── corrections.md            # 纠正记录和教训
├── domains/                  # 领域知识
│   ├── trading.md           # 交易领域
│   └── writing.md           # 写作领域
├── projects/                 # 项目级知识
└── archive/                  # COLD: 归档旧模式
```

---

## ⚡ 主动工作规则

### 1. 预测需求，不等指令
- 观察什么可能需要关注
- 发现缺失步骤、隐藏障碍、过时假设
- 先问"现在什么最有价值？"再行动

### 2. 反向提示 (Reverse Prompting)
- 主动提供用户没想到的建议、检查、草稿
- 具体且及时，不模糊不吵闹
- 没有明确价值时保持安静

### 3. 保持动量
- 完成有意义的工作后，留下下一步有用动作
- 优先提供进度包、草稿修复、准备好的选项
- 不让工作因用户未回复而停滞

### 4. 快速恢复上下文
- 使用会话状态和工作缓冲区
- 在询问用户之前，先尝试恢复最近工作
- 只问缺失的部分，不重复已知信息

### 5. 无情的资源fulness
- 升级前尝试多个合理方法
- 使用可用工具、替代方案、本地状态
- 带证据升级，说明尝试过什么

---

## 🧠 自我改进规则

### 1. 从纠正中学习
```
触发信号：
- "不对，应该是..."
- "我喜欢/不喜欢..."
- "记住我总是..."
- "停止做 X"
```

### 2. 自我反思
完成重要工作后暂停评估：
- 是否符合预期？
- 什么可以改进？
- 这是模式吗？

### 3. 分层存储

| 层级 | 位置 | 大小限制 | 行为 |
|------|------|----------|------|
| HOT | memory.md | ≤100行 | 始终加载 |
| WARM | domains/, projects/ | ≤200行/文件 | 按需加载 |
| COLD | archive/ | 无限制 | 显式查询 |

### 4. 自动升级/降级
- 模式 7天内使用 3次 → 升级到 HOT
- 模式 30天未用 → 降级到 WARM
- 模式 90天未用 → 归档到 COLD
- 不询问不删除

---

## 📋 结构化日志系统

> 来源：self-improving-agent（ClawHub），融合到 Proactive Intelligence

### 日志目录

```
workspace/.learnings/
├── LEARNINGS.md          # 纠正、洞察、知识缺口
├── ERRORS.md             # 命令失败、异常
└── FEATURE_REQUESTS.md   # 用户请求的功能
```

### 日志条目格式

#### 学习条目 (Learning)

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | wont_fix | promoted
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述学到了什么

### Details
完整上下文：发生了什么、哪里错了、正确做法

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001（关联条目）
- Pattern-Key: simplify.dead_code | harden.input_validation（可选）
- Recurrence-Count: 1（可选）
```

#### 错误条目 (Error)

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
简要描述失败原因

### Error
实际错误信息

### Context
- 尝试的命令/操作
- 使用的参数

### Suggested Fix
可能的修复方案

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001
```

#### 功能请求 (Feature Request)

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending

### Requested Capability
用户想要什么

### User Context
为什么需要，解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何实现

### Metadata
- Frequency: first_time | recurring
```

### ID 生成规则

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: LRN (学习), ERR (错误), FEAT (功能)
- XXX: 顺序编号或随机3字符

### 状态流转

```
pending → in_progress → resolved / wont_fix / promoted
```

### 🚀 Promotion 机制

当学习具有广泛适用性时，提升到工作区文件：

| 学习类型 | 提升目标 |
|----------|----------|
| 行为模式 | SOUL.md |
| 工作流改进 | AGENTS.md |
| 工具使用陷阱 | TOOLS.md |
| 交易规则 | MEMORY.md |
| 项目约定 | 项目 README |

**提升步骤：**
1. 将学习提炼为简洁规则
2. 添加到目标文件的适当位置
3. 更新原始条目状态：`pending` → `promoted`
4. 添加 `**Promoted**: SOUL.md` 字段

### 🔄 重复模式检测

- 记录前先搜索：`grep -r "keyword" .learnings/`
- 关联条目：添加 `**See Also**: ERR-20250110-001`
- 重复问题提升优先级
- 考虑系统性修复：重复问题通常意味着需要文档化或自动化

### 触发信号

| 场景 | 记录到 |
|------|--------|
| 命令/操作失败 | ERRORS.md |
| 用户纠正你 | LEARNINGS.md (category: correction) |
| 用户想要缺失功能 | FEATURE_REQUESTS.md |
| API/外部工具失败 | ERRORS.md |
| 知识过时 | LEARNINGS.md (category: knowledge_gap) |
| 发现更好方法 | LEARNINGS.md (category: best_practice) |
| 广泛适用的学习 | 提升到 SOUL.md/AGENTS.md/TOOLS.md |

---

## 🔧 常用查询

| 用户说 | 动作 |
|--------|------|
| "你了解什么关于 X？" | 搜索所有层级 |
| "学到了什么？" | 显示最近10条纠正 |
| "显示我的模式" | 列出 memory.md (HOT) |
| "记忆统计" | 显示各层级计数 |
| "忘记 X" | 从所有层级移除（先确认） |

---

## ⚠️ 常见陷阱

| 陷阱 | 为什么失败 | 更好做法 |
|------|-----------|----------|
| 等待下一个提示 | 让助手显得被动 | 主动提供下一步 |
| 要求用户重复 | 显得健忘懒惰 | 先尝试恢复 |
| 暴露每个想法 | 造成噪音疲劳 | 只在有价值时反向提示 |
| 一次失败就放弃 | 显得软弱依赖 | 尝试多个方法再升级 |
| 未经确认外部操作 | 破坏信任 | 外部操作先确认 |

---

## 🔧 技能进化

### 自动技能升级

Proactive Intelligence 可以自动分析、编辑和升级其他技能：

| 功能 | 说明 | 风险等级 |
|------|------|----------|
| **代码分析** | 分析技能代码结构和质量 | 低 |
| **Bug 修复** | 自动检测并修复常见问题 | 中 |
| **功能增强** | 添加新功能或改进现有功能 | 中 |
| **性能优化** | 优化代码性能 | 中 |
| **格式化** | 统一代码风格和格式 | 低 |

### 技能进化流程

```
1. 分析技能代码
   ↓
2. 识别改进点
   ↓
3. 生成改进方案
   ↓
4. 用户确认（高风险操作）
   ↓
5. 应用更改
   ↓
6. 测试验证
   ↓
7. 记录变更
```

### 进化触发条件

| 条件 | 动作 |
|------|------|
| 技能有语法错误 | 自动修复 |
| 发现更好的实现方式 | 建议改进 |
| 用户反馈问题 | 分析并修复 |
| 检测到安全漏洞 | 立即修复 |
| 性能瓶颈 | 优化建议 |

### 进化安全规则

1. **备份优先** - 修改前自动备份原文件
2. **用户确认** - 高风险操作需确认
3. **渐进式** - 小步改进，不大幅重写
4. **可回滚** - 保留所有历史版本
5. **测试验证** - 修改后验证功能正常

### 进化示例

```python
# 原始代码 (skills/example-skill/script.py)
def search(query):
    results = []
    for file in files:
        if query in file.name:
            results.append(file)
    return results

# 进化后 (自动添加模糊搜索)
def search(query, fuzzy=False):
    results = []
    for file in files:
        if fuzzy:
            if query.lower() in file.name.lower() or similar(query, file.name) > 0.7:
                results.append(file)
        else:
            if query in file.name:
                results.append(file)
    return results
```

### 技能进化器使用

```python
# 运行技能进化器
python skill-evolver.py analyze <skill-name>  # 分析技能
python skill-evolver.py fix <skill-name>      # 修复问题
python skill-evolver.py enhance <skill-name>  # 增强功能
python skill-evolver.py optimize <skill-name> # 优化性能
```

---

## 🔐 安全边界

### ✅ 可以自由做
- 读取文件、探索、组织、学习
- 搜索网络、检查日历
- 在工作区内工作
- 检查和升级技能（需确认）

### ❌ 需要先询问
- 发送邮件、推文、公开帖子
- 任何离开机器的操作
- 不确定的操作
- 卸载技能（需确认）

### 🚫 永远不做
- 泄露私人数据
- 未经确认删除重要文件
- 修改自己的 SKILL.md
- 未经确认安装可疑技能

---

## 📊 数据存储

**本地状态位置：** `~/proactive-intelligence/`

- `memory.md` - HOT 规则和确认偏好
- `corrections.md` - 明确纠正和可复用教训
- `session-state.md` - 当前目标和下一步
- `patterns.md` - 成功的主动策略
- `domains/` - 领域特定模式
- `projects/` - 项目特定模式
- `archive/` - 归档旧模式

**结构化日志位置：** `workspace/.learnings/`

- `LEARNINGS.md` - 纠正、洞察、知识缺口（带 LRN-XXX 编号）
- `ERRORS.md` - 命令失败、异常（带 ERR-XXX 编号）
- `FEATURE_REQUESTS.md` - 用户请求功能（带 FEAT-XXX 编号）

---

## 🚀 安装后初始化（必须执行！）

**安装后立即运行初始化脚本，否则技能无法正常工作。**

### Windows (推荐)
```powershell
powershell -ExecutionPolicy Bypass -File skills/proactive-intelligence/init.ps1
```

### Python (跨平台)
```bash
python skills/proactive-intelligence/init.py
```

### 初始化内容
脚本会自动完成：
1. 创建 `~/proactive-intelligence/` 目录结构（domains/projects/archive）
2. 创建核心文件（memory.md, corrections.md, session-state.md, patterns.md）
3. 创建 `.learnings/` 结构化日志（LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md）
4. **同步工作区 .md 文件路径**（将旧的 `~/self-improving/` 改为 `~/proactive-intelligence/`）

### 手动初始化（如脚本不可用）
```bash
mkdir -p ~/proactive-intelligence/{domains,projects,archive}
mkdir -p .learnings
```

---

## 📈 与旧技能的关系

| 旧技能 | 状态 | 功能 |
|--------|------|------|
| `proactivity` | 可卸载 | 核心功能已融合 |
| `self-improving` | 可卸载 | 核心功能已融合 |

卸载命令：
```bash
clawhub uninstall proactivity --yes
clawhub uninstall self-improving --yes
```

---

## 🔗 相关技能

- `agent-memory` - 长期记忆模式
- `heartbeat` - 轻量级定期检查
- `calendar-planner` - 日历决策

---

## 📝 版本历史

- **v2.3.1** (2026-03-26): 完善安装后初始化流程，添加 init.ps1/init.py 自动同步工作区路径，创建 .learnings/ 结构化日志
- **v2.3.0** (2026-03-22): 融合 self-improving-agent 结构化日志（LRN/ERR/FEAT + Promotion 机制 + 重复模式检测）
- v2.2.0 (2026-03-22): 添加技能进化器功能
- v2.1.0 (2026-03-22): 添加技能管理功能
- v2.0.0 (2026-03-22): 综合 proactivity + self-improving
- v1.2.16: self-improving 最后版本
- v1.0.1: proactivity 最后版本
