# Personal Assistant CLI 命令参考

所有命令通过 `scripts/personal_assistant.py` 执行，运行目录为 skill 根目录。

## 全局选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--db-path PATH` | SQLite 数据库路径 | `~/.hermes/data/personal_assistant/tasks.db` |
| `--json` | JSON 格式输出 | - |
| `--help` | 查看帮助 | - |

---

## 任务管理 (`task`)

### 添加任务

```bash
python3 scripts/personal_assistant.py task add \
  --title "完成 Q2 述职 PPT" \
  --deadline "2026-06-01T18:00" \
  --priority 2 \
  --category "文档" \
  --estimated-hours 8 \
  --description "包含 Q2 关键成果汇总"
```

| 选项 | 说明 |
|------|------|
| `--title` | 任务标题（必填） |
| `--deadline` | 截止时间，ISO 8601 格式 |
| `--priority` | 优先级：1=最高, 5=最低（默认 3） |
| `--category` | 分类标签（如 "开发"、"会议"、"文档"） |
| `--estimated-hours` | 预估耗时（小时） |
| `--description` | 详细描述（支持 Markdown） |
| `--okr-id` | 关联的 OKR ID |
| `--parent-id` | 父任务 ID（创建子任务） |

### 查询任务

```bash
# 列表查询
python3 scripts/personal_assistant.py task list \
  --status "todo,in_progress" \
  --category "开发" \
  --sort "deadline" \
  --order "asc" \
  --limit 20

# 今日待办
python3 scripts/personal_assistant.py task today

# 查看详情
python3 scripts/personal_assistant.py task show 42

# 搜索
python3 scripts/personal_assistant.py task search "述职 PPT"
```

| 选项 | 说明 |
|------|------|
| `--status` | 逗号分隔的状态过滤 |
| `--category` | 分类过滤 |
| `--priority` | 优先级过滤 |
| `--sort` | 排序字段：`deadline`, `priority`, `created_at`, `updated_at` |
| `--order` | `asc` 或 `desc` |
| `--limit` | 返回条数上限（默认 50） |

### 更新任务

```bash
# 更新字段
python3 scripts/personal_assistant.py task update 42 \
  --status "in_progress" \
  --priority 1

# 完成任务
python3 scripts/personal_assistant.py task done 42 \
  --note "已完成并发送给主管审核"

# 添加子任务（通过 task add --parent-id）
python3 scripts/personal_assistant.py task add \
  --title "收集 Q2 数据" \
  --parent-id 42
```

### 删除任务

```bash
# 软删除（status → cancelled）
python3 scripts/personal_assistant.py task delete 42

# 物理删除
python3 scripts/personal_assistant.py task delete 42 --hard
```

---

## 进展管理 (`progress`)

### 记录进展

```bash
python3 scripts/personal_assistant.py progress log 42 \
  --content "已完成数据收集部分，正在整理 PPT 大纲" \
  --progress 60 \
  --hours 3
```

| 选项 | 说明 |
|------|------|
| `--content` | 进展内容（必填，Markdown） |
| `--progress` | 更新后的进度百分比 (0-100) |
| `--hours` | 本次投入小时数 |

### 查看进展

```bash
# 查看进展历史
python3 scripts/personal_assistant.py progress history 42

# 列出里程碑
python3 scripts/personal_assistant.py progress milestone-list 42
```

### 里程碑管理

```bash
# 添加里程碑
python3 scripts/personal_assistant.py progress milestone-add 42 \
  --title "完成数据收集" \
  --due "2026-05-28"

# 完成里程碑
python3 scripts/personal_assistant.py progress milestone-done 7
```

---

## 周期任务管理 (`recurring`)

### 添加周期任务

```bash
# 双周例会
python3 scripts/personal_assistant.py recurring add \
  --title "公司双周例会" \
  --type "biweekly" \
  --next-run "2026-05-28" \
  --advance-days 3 \
  --category "会议" \
  --priority 2 \
  --estimated-hours 1.5

# 自定义规则（每周五）
python3 scripts/personal_assistant.py recurring add \
  --title "每周五代码评审" \
  --type "custom" \
  --rule "FREQ=WEEKLY;BYDAY=FR" \
  --next-run "2026-05-29"
```

| 选项 | 说明 |
|------|------|
| `--title` | 任务标题模板（必填） |
| `--type` | 周期类型：`daily`, `weekly`, `biweekly`, `monthly`, `custom` |
| `--rule` | 自定义规则（type=custom 时使用，类 iCal RRULE） |
| `--next-run` | 下次生成实例的日期 |
| `--advance-days` | 提前生成天数（如提前 3 天生成例会任务） |
| `--category` | 分类标签 |
| `--priority` | 优先级 |
| `--estimated-hours` | 预估工时 |
| `--description` | 任务描述模板 |

### 管理周期任务

```bash
# 列出
python3 scripts/personal_assistant.py recurring list

# 暂停/恢复
python3 scripts/personal_assistant.py recurring toggle 3

# 删除
python3 scripts/personal_assistant.py recurring delete 3
```

---

## OKR 管理 (`okr`)

### 同步 OKR

```bash
# 从飞书文档同步
python3 scripts/personal_assistant.py okr sync \
  --doc-token "YOUR_DOC_TOKEN_HERE" \
  --period "2026Q2"
```

### 手动管理 OKR

```bash
# 添加 Objective
python3 scripts/personal_assistant.py okr add-objective \
  --title "提升系统稳定性" \
  --desc "确保核心服务可用性达到 99.9%" \
  --start "2026-04-01" \
  --end "2026-06-30"

# 添加 Key Result（关联到 Objective）
python3 scripts/personal_assistant.py okr add-kr \
  --parent 1 \
  --title "P99 延迟降至 200ms" \
  --desc "优化数据库查询和缓存策略"

# 查看列表
python3 scripts/personal_assistant.py okr list

# 查看全景树
python3 scripts/personal_assistant.py okr tree

# 查看详情（含关联任务）
python3 scripts/personal_assistant.py okr show 1

# 关联任务到 OKR
python3 scripts/personal_assistant.py okr link --okr 1 --task 42
```

---

## 提醒管理 (`remind`)

```bash
# 手动触发提醒（用于调试）
python3 scripts/personal_assistant.py remind trigger --type morning

# 预览待提醒任务（dry-run，不实际发送）
python3 scripts/personal_assistant.py remind preview --type afternoon

# 查看最近提醒记录
python3 scripts/personal_assistant.py remind history --limit 10
```

| 选项 | 说明 |
|------|------|
| `--type` | 提醒类型：`morning`, `afternoon`, `evening`, `deadline_alert`, `manual` |
| `--limit` | 返回条数（history 命令） |

---

## 报告生成 (`report`)

```bash
# 生成月度报告
python3 scripts/personal_assistant.py report monthly \
  --month 2026-05 \
  --output ~/.hermes/reports/2026-05-report.md

# 生成半年度报告
python3 scripts/personal_assistant.py report semiannual \
  --half 2026H1 \
  --output ~/.hermes/reports/2026H1-report.md

# 预览报告（不生成文件）
python3 scripts/personal_assistant.py report monthly --month 2026-05 --preview
```

| 选项 | 说明 |
|------|------|
| `--month` | 月份，格式 `YYYY-MM` |
| `--half` | 半年度，格式 `YYYYH1` 或 `YYYYH2` |
| `--output` | 输出文件路径 |
| `--preview` | 仅预览，不写入文件 |

---

## 数据库维护 (`db`)

```bash
# 查看统计
python3 scripts/personal_assistant.py db stats

# 导出数据
python3 scripts/personal_assistant.py db export --output backup.json

# 导入数据
python3 scripts/personal_assistant.py db import backup.json

# 清理历史数据（删除已完成超过 90 天且无 OKR 关联的任务）
python3 scripts/personal_assistant.py db cleanup --older-than 90
```

| 选项 | 说明 |
|------|------|
| `--output` | 导出文件路径 |
| `--older-than` | 清理天数阈值 |
