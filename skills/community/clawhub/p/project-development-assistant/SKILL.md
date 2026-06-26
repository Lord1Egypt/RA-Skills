---
name: project-development-assistant
description: "Project Development Assistant — structured logging + issue tracking with anti-spam design. Trigger ONLY when user explicitly says new project, continue project, or log progress. NOT for casual chat. Developer: 杨荣才 (yangrongcai141@gmail.com)"
---

# 工程开发助理 (Project Development Assistant)

**设计原则：随时可中断，随时可继续。日志静默写入，聊天只回一行摘要。**

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 📁 项目初始化 | 创建标准项目结构 + 状态文件 |
| 📝 日志管理 | 静默写入文件，聊天只回一行确认 |
| 📊 状态追踪 | 结构化状态文件（.project_state.json） |
| 🔍 进度简报 | 生成项目快照（JSON），聊天只回关键信息 |
| ⚠️ 问题记录 | 自动提取 open_issues，标注阻塞点 |

**防刷屏核心规则：**
- `log` / `progress` / `generate` 默认静默，只写文件不输出
- 加 `--show` 才在聊天显示摘要
- 所有脚本输出控制在 **3行以内**

---

## 触发条件（精确激活）

**仅在以下明确指令时激活：**

| 用户说 | 激活动作 |
|--------|----------|
| 「新建项目」「创建项目」 | 项目初始化 |
| 「继续项目」「接着上次」 | 读取状态 + 最新日志摘要 |
| 「项目进度」「状态如何」 | 显示简报摘要 |
| 「记录」「日志」「标记」+ 某事 | 写入日志（静默） |
| 「项目结构」「看下结构」 | 显示结构（限深2层） |

**不激活：** 闲聊、问候、模糊请求与项目无关的内容

---

## 一、新建项目

```
用户：「新建项目」「创建项目」
```

```bash
python <skill>/scripts/log_project.py -a new -p <项目路径> -n <项目名称>
```

**创建内容：**
```
项目/
├── logs/                     # 每日开发日志
├── sessions/                 # 会话归档目录
│   └── session_latest.md     # 始终指向最新归档
├── configs/
├── firmware/
├── docs/
├── hardware/
├── references/
├── tools/
└── PROJECT_INFO.md
```

**状态文件：** `.project_state.json`（结构化状态，替代散乱日志读取）

---

## 二、继续项目

```
用户：「继续项目」「接着上次」
```

**执行顺序（不可跳过）：**

```bash
# 1. 项目结构
python <skill>/scripts/log_project.py -a structure -p <项目路径>

# 2. 状态文件（结构化，一行摘要）
python <skill>/scripts/log_project.py -a state -p <项目路径>

# 3. 最新日志（只显示最后8条）
python <skill>/scripts/log_project.py -a read -p <项目路径>
```

**回复模板（限3句）：**
```
📊 项目名 | 🔄 进行中
   当前：xxx
   问题：xxx（若有）
```

---

## 三、记录进度

```
用户：「记录 xxx」
```

```bash
# 默认静默写入，不打扰聊天
python <skill>/scripts/log_project.py -a log -p <项目路径> -m "<消息>" -c <类别>

# 需要显示确认时加 --show
python <skill>/scripts/log_project.py -a log -p <项目路径> -m "<消息>" -c INFO --show
```

**日志类别：**

| 类别 | 触发时机 | 示例 |
|------|----------|------|
| INFO | 任务开始/完成、状态更新 | 「开始开发驱动」「编译成功」 |
| ERROR | 任何错误 | 「编译失败」「连接超时」 |
| FIXED | 解决方案 | 「已解决引脚冲突」 |
| PROGRESS | 进行中里程碑 | 「完成了屏幕驱动」 |
| WARNING | 潜在风险 | 「闪存空间不足」 |
| SUCCESS | 重要里程碑达成 | 「固件烧录成功」 |

---

## 四、更新状态

```
用户：「项目状态改为进行中」「当前任务是xxx」
```

```bash
# 更新状态（静默）
python <skill>/scripts/log_project.py -a state -p <项目路径> -s 进行中 -t "开发LCD驱动"

# 添加问题（可多次 -i）
python <skill>/scripts/log_project.py -a state -p <项目路径> -i "SPI引脚冲突"

# 添加下一步（可多次 --step）
python <skill>/scripts/log_project.py -a state -p <项目路径> --step "修复SPI" --step "测试显示"
```

---

## 五、项目简报

```bash
# 生成所有项目简报（静默）
python <skill>/scripts/task_briefing.py -a generate

# 显示摘要（--show 才输出）
python <skill>/scripts/task_briefing.py -a generate --show

# 查看单个项目状态
python <skill>/scripts/task_briefing.py -a status -p <项目名>

# 检查需要恢复的任务
python <skill>/scripts/task_briefing.py -a check-resume

# 列出所有项目
python <skill>/scripts/task_briefing.py -a list
```

**简报存储：** `briefings/*.json`（结构化，不在聊天刷屏）

---

## 六、快速命令参考

```bash
# === 新建 ===
python log_project.py -a new -p <路径> -n <名称>

# === 记录（静默）===
python log_project.py -a log -p <路径> -m <消息> -c INFO

# === 记录（显示）===
python log_project.py -a log -p <路径> -m <消息> -c INFO --show

# === 状态 ===
python log_project.py -a state -p <路径>          # 读取
python log_project.py -a state -p <路径> -s 进行中 -t "任务名"  # 更新

# === 读取 ===
python log_project.py -a read -p <路径>            # 日志（最后20条）
python log_project.py -a progress -p <路径>       # 状态+日志摘要
python log_project.py -a structure -p <路径>      # 结构（限深2层）
python log_project.py -a list -p <路径>            # 日志列表

# === 简报 ===
python task_briefing.py -a generate --show        # 生成+显示
python task_briefing.py -a status -p <项目名>     # 单项目状态
python task_briefing.py -a check-resume           # 检查需恢复任务
```

---

## 七、防刷屏规则

| 操作 | 默认行为 | 聊天输出 |
|------|----------|----------|
| 新建项目 | 静默创建 | ✅ 1行确认 |
| 记录日志 | 静默写入 | ❌ 无输出 |
| 记录日志+--show | 写入+显示 | ✅ 1行摘要 |
| 读取日志 | 显示摘要 | ≤3行 |
| 进度摘要 | 显示状态 | ≤5行 |
| 生成简报 | 静默写文件 | ✅ 1行统计 |
| 生成简报+--show | 写+显示 | ≤N项目行 |

**原则：一个开发动作 → 最多一行聊天回复**

---

## 八、状态文件格式

`.project_state.json` 结构：

```json
{
  "project": "项目名",
  "status": "进行中",
  "current_task": "当前任务描述",
  "last_updated": "2026-03-22 22:00:00",
  "summary": "一句话状态",
  "open_issues": ["问题1", "问题2"],
  "next_steps": ["下一步1", "下一步2"],
  "milestones": []
}
```

---

## 九、会话精简与上下文管理

### 问题分析

单次会话对话过长会导致：
- 上下文窗口逐渐填满，AI 响应变慢变贵
- 早期上下文被"挤出"，丢失项目背景
- 新会话无法感知上一个会话的结论

### 解决方案：会话归档协议（Session Archival Protocol）

核心思路：**用结构化文件代替对话记录来传递上下文**。

#### 归档触发时机

满足以下任一条件时，主动触发归档：

| 触发条件 | 说明 |
|----------|------|
| 会话消息数 > 50 条 | 对话密度已高，需要整理 |
| AI 主动提示上下文接近上限 | 模型响应开始变慢或重复 |
| 项目进入新阶段 | 完成一个里程碑，准备下一阶段 |
| 重要结论已形成 | 决定/方案已确认，需要存档 |

#### 归档操作步骤

当检测到需要归档时，执行以下步骤：

**Step 1：生成归档摘要**

```
用户：「归档当前会话」
```

主动用日志记录归档内容，不依赖 AI 总结：

```bash
# 用时间戳+类别记录归档点
python log_project.py -a log -p <项目路径> -m "【会话归档】<项目名> - 第N次会话" -c PROGRESS --show
```

**Step 2：写入会话归档文件**

在 `sessions/` 目录下创建归档文件：

```
项目/sessions/session_<日期>.md
```

文件格式：
```markdown
# 会话归档 - <项目名>
日期：<YYYY-MM-DD>
会话数：<N条消息>

## 背景
<项目的技术栈、目标、当前阶段>

## 达成的结论
1. <结论1>
2. <结论2>

## 未解决的问题
- <问题1>
- <问题2>

## 当前任务
- 当前：<正在做的事>
- 下一步：<准备做的事>

## 关键文件/代码位置
- <文件路径>：<说明>
```

**Step 3：更新项目状态**

```bash
# 读取当前状态
python log_project.py -a state -p <项目路径>

# 更新当前任务
python log_project.py -a state -p <项目路径> -s 进行中 -t "<当前任务>"
```

**Step 4：开启新会话**

在 AI 端发起 `/new` 或 `/reset`，清除上下文。

**Step 5：新会话恢复**

继续项目时，读取最近的归档文件恢复上下文：

```bash
# 读取最新归档
Get-Content "项目/sessions/session_*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

**新会话开场白模板：**
```
请读取 D:\项目路径\sessions\ 目录下最新的归档文件，了解项目当前状态和历史结论。
```

#### 上下文管理原则

| 做法 | 原因 |
|------|------|
| 细节操作写日志，不在聊天反复确认 | 日志是文件不占上下文 |
| 结论性对话主动归档 | 防止结论被后续对话挤出 |
| 按功能阶段开新会话 | 每个阶段独立，减少上下文纠缠 |
| 归档文件命名含日期 | 便于快速找到最新归档 |

#### 会话目录结构

```
项目/
├── sessions/              # 会话归档目录
│   ├── session_2026-03-20.md
│   ├── session_2026-03-22.md
│   └── session_latest.md  # 始终指向最新归档
```

#### 与其他工具的关系

```
会话对话
    ↓（归档时写入）
sessions/session_YYYY-MM-DD.md
    ↓（新会话时读取）
.project_state.json ← 由 log_project.py 管理
    ↓（cron 监控读取）
briefings/*.json
```

---

## 相关参考

- 工作流详细说明：[references/workflow.md](references/workflow.md)
- 简报存储：`briefings/*.json`
- 会话归档存储：`sessions/session_*.md`
