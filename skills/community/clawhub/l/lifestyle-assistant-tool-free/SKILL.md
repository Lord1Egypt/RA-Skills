---

name: "lifestyle-assistant-tool-free"
description: "个人任务、沟通与日程管理助手,主动跟进待办、邮件摘要与会议安排。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "生活助手免费版"
  version: "1.0.0"
  summary: "个人任务、沟通与日程管理助手,主动跟进待办、邮件摘要与会议安排"
  tags:
    - "个人助手"
    - "任务管理"
    - "日程管理"
    - "效率工具"
    - "沟通优化"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 生活助手 (免费版)

## 概述

本工具是面向个人用户的生活与工作助理,帮助用户高效管理任务、优化沟通、安排日程。助手会主动捕获待办事项,在恰当时间提醒跟进,把长邮件提炼成关键要点,把零散信息整理为可检索的知识库。

免费版聚焦个人用户的日常管理需求,适合自由职业者、独立开发者以及需要一位靠谱数字助手的人士。

## 核心能力

| 能力模块 | 描述 | 免费版支持 |
|:--------|:-----|:-----------|
| 任务捕获与分解 | 即时记录、拆解大任务为可执行步骤 | 支持 |
| 截止日期追踪 | 自动提醒即将到期事项 | 支持 |
| 邮件摘要 | 长邮件提炼要点与行动项 | 每日 10 封 |
| 日程冲突检测 | 安排会议前检查时间冲突 | 支持 |
| 跨时区协调 | 处理远程协作时区问题 | 支持 |
| 信息归档 | 笔记、偏好、历史记录管理 | 本地存储 |
| 主动支持 | 预判需求并提前准备材料 | 基础能力 |
| 团队协作 | 多人任务分配与进度跟踪 | 不支持 (升级 PRO) |
| 自动化工作流 | 触发器联动外部服务 | 不支持 (升级 PRO) |
| 知识库共享 | 团队共享信息库 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：个人任务、沟通与日程管理助、主动跟进待办、邮件摘要与会议安、面向个人用户的生、活与工作助理、聚焦任务捕获、沟通优化与日程管、核心能力、任务分解与跟进、邮件长文摘要、日程冲突检测、提醒推送、信息归档、适用场景、自由职业者日程管、个人事务跟进、邮件处理、会议准备、差异化、免费版专注单用户、日常任务管理、配置简单、适合个人使用、适用关键词、任务管理、日程安排、邮件摘要、待办清单等。

## 使用场景

### 场景一: 任务管理

将模糊想法转化为可执行任务,自动跟踪截止日期。

```text
用户: "下周三要交一份产品方案,帮我拆解一下"

助手:
1. 已捕获任务: 产品方案 (截止 2026-07-23)
2. 拆解为 5 个子任务:
   - [ ] 调研竞品方案 (建议 2 天)
   - [ ] 整理用户反馈 (建议 1 天)
   - [ ] 撰写产品需求文档 (建议 2 天)
   - [ ] 内部评审 (建议 0.5 天)
   - [ ] 修改定稿 (建议 0.5 天)
3. 设置提醒:
   - 2026-07-19: 启动调研
   - 2026-07-22: 完成评审
   - 2026-07-23: 提交定稿
```

### 场景二: 邮件摘要

把冗长邮件提炼为关键要点与行动项。

```python
import json
from pathlib import Path

def summarize_email(subject, body, sender):
    """生成本地邮件摘要 (示例)"""
    summary = {
        "subject": subject,
        "sender": sender,
        "key_points": [
            "项目 A 需在 7 月 25 日前完成验收",
            "预算上限调整为 50 万",
            "需要补充技术方案章节"
        ],
        "action_items": [
            {"task": "回复确认验收日期", "due": "2026-07-19"},
            {"task": "更新技术方案文档", "due": "2026-07-22"}
        ],
        "priority": "high"
    }
    return summary

# 存储到本地
archive = Path.home() / ".assistant" / "email_summaries.json"
archive.parent.mkdir(parents=True, exist_ok=True)
```

### 场景三: 日程协调

在安排会议前自动检查冲突并建议优选时间。

```text
用户: "明天下午帮我安排一个 1 小时的产品评审"

助手:
1. 检查日程: 明天 14:00-15:00 已有客户会议
2. 建议时间:
   - 15:30-16:30 (推荐,会后可直接整理客户反馈)
   - 16:30-17:30 (备选)
3. 已生成会议邀请草稿,确认后发送
```

## 快速开始

### Step 1: 初始化助手工作区

```bash
mkdir -p $HOME/.assistant/{tasks,emails,notes,reminders}
echo '{"version":"1.0","edition":"free"}' > $HOME/.assistant/config.json
```

### Step 2: 配置个人偏好

```yaml
# $HOME/.assistant/preferences.yaml
profile:
  name: 你的名字
  timezone: Asia/Shanghai
  work_hours: "09:00-18:00"
  focus_blocks: ["10:00-12:00", "14:00-16:00"]

notifications:
  daily_summary: "08:30"
  end_of_day: "18:00"
  task_reminders: true
  buffer_minutes: 15

email:
  batch_times: ["09:00", "13:00", "17:00"]
  summarize_threshold_words: 200
```

### Step 3: 验证助手响应

```bash
# 添加一个测试任务
cat > $HOME/.assistant/tasks/test.json << 'EOF'
{
  "id": "t001",
  "title": "测试任务",
  "due": "2026-07-20",
  "priority": "medium",
  "status": "pending"
}
EOF

# 查看今日待办
ls -la $HOME/.assistant/tasks/
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

### 任务管理模板

```python
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json

@dataclass
class Task:
    id: str
    title: str
    due: str
    priority: str  # high, medium, low
    status: str    # pending, in_progress, done
    subtasks: list
    created_at: str

class TaskManager:
    def __init__(self, base_dir="$HOME/.assistant/tasks"):
        self.base_dir = Path(base_dir).expanduser()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def add(self, title, due, priority="medium"):
        task = Task(
            id=f"t{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            due=due,
            priority=priority,
            status="pending",
            subtasks=[],
            created_at=datetime.now().isoformat(),
        )
        path = self.base_dir / f"{task.id}.json"
        path.write_text(json.dumps(asdict(task), ensure_ascii=False, indent=2))
        return task

    def due_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        tasks = []
        for f in self.base_dir.glob("*.json"):
            t = json.loads(f.read_text())
            if t["due"] == today and t["status"] != "done":
                tasks.append(t)
        return sorted(tasks, key=lambda x: {"high":0,"medium":1,"low":2}[x["priority"]])
```

### 日程协调示例

```python
def find_slot(existing_events, duration_min, work_hours=("09:00","18:00")):
    """在空闲时段寻找合适时间槽"""
    from datetime import datetime, timedelta
    work_start = datetime.strptime(f"{today} {work_hours[0]}", "%Y-%m-%d %H:%M")
    work_end = datetime.strptime(f"{today} {work_hours[1]}", "%Y-%m-%d %H:%M")
    duration = timedelta(minutes=duration_min)

    slots = []
    cursor = work_start
    for event in sorted(existing_events, key=lambda e: e["start"]):
        if datetime.fromisoformat(event["start"]) - cursor >= duration:
            slots.append({
                "start": cursor.isoformat(),
                "end": (cursor + duration).isoformat(),
            })
        cursor = max(cursor, datetime.fromisoformat(event["end"]))
    if work_end - cursor >= duration:
        slots.append({
        })
    return slots
```

## 优选实践

### 1. 任务捕获原则

- 模糊需求先澄清再执行,避免返工
- 大任务拆解为可执行的小步骤,每步不超过 2 小时
- 标注优先级时使用"紧急且重要"矩阵,而非全部标记为高

### 2. 沟通优化

- 对外正式场合用书面语气,内部沟通可适当轻松
- 起草回复时预判可能的问题并主动回答
- 长邮件先输出摘要,再附详细内容

### 3. 日程管理

- 安排会议前检查冲突,预留 15 分钟缓冲
- 保护深度工作时段,避免会议占据全部空档
- 重要事件提前 1 天与 1 小时双重提醒

### 4. 信息归档

```bash
# 推荐目录结构
$HOME/.assistant/
├── tasks/         # 任务记录
├── emails/        # 邮件摘要
├── notes/         # 笔记
├── reminders/     # 提醒
├── preferences/   # 个人偏好
└── history/       # 历史记录
```

## 常见问题

### Q1: 免费版能管理多少任务?

无硬性上限,但建议单日活跃任务不超过 50 项,以保证执行效率。超出可考虑升级 PRO 版本获得自动化分派能力。

### Q2: 数据存储在哪里?

所有数据存储在本地 `$HOME/.assistant/` 目录,JSON 格式,易于备份与迁移。不上传任何数据到云端。

### Q3: 支持哪些提醒渠道?

免费版支持控制台输出与本地文件提醒。如需邮件、Webhook、即时消息推送,请升级 PRO 版本。

### Q4: 能否对接日历应用?

支持导入 ICS 格式日历文件。实时双向同步需要 PRO 版本的日历集成能力。

### Q5: 如何备份数据?

```bash
# 备份整个助手工作区
tar -czf assistant-backup-$(date +%Y%m%d).tar.gz $HOME/.assistant/
```

## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **存储**: 本地文件系统,建议预留 50MB 空间

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 可选 | python.org 下载,用于脚本化任务 |
| PyYAML | Python 库 | 可选 | `pip install pyyaml` (解析配置文件) |

### API Key 配置

```bash
# 免费版无需外部 API Key
# 所有数据本地存储,无需认证

# 可选: 配置个人偏好
export ASSISTANT_TIMEZONE="Asia/Shanghai"
export ASSISTANT_WORK_HOURS="09:00-18:00"
```

### 可用性分类

- **分类**: MD+execute(Markdown 指令 + 命令行执行)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 管理本地任务、邮件摘要与日程,所有数据保存在本地
- **免费版限制**: 单用户、本地存储、无自动化工作流、每日邮件摘要 10 封

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。