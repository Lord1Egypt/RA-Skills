# Memo — 能跟 AI 协作的备忘录技能

> 一个能跟AI协作的备忘录技能，是你工作、生活和学习的私人助理。

[![Version](https://img.shields.io/badge/version-v2.0.1-blue)](https://github.com/QU8/Memo)
[![Platform](https://img.shields.io/badge/platform-WorkBuddy-green)](https://www.codebuddy.cn/docs/workbuddy/Overview)
[![Python](https://img.shields.io/badge/python-3.8+-yellow)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 📥 **口语化记录** | 直接说"帮我记一下…"，自动解析时间、类型、涉及人员等字段；**口语日期**（今天/明天/下周/X月X日等）自动写入工作日期，无需手动指定 `--date` |
| 📊 **统计报告** | 按本周/上周/本月等时间段汇总工作内容，生成结构化报告 |
| ✅ **待办管理** | 添加含"明天/下周"等时间意图的记录自动标记为待办 |
| 🔔 **自定义时间提醒** | 添加待办时可指定任意提醒时间（如"下午4点"），未指定默认 08:00；标记完成后自动删除提醒 |
| 🔄 **智能同步** | 修改待办的日期/提醒时间/内容时，自动同步对应自动化提醒，无需重复操作 |
| 🔍 **智能搜索** | 按关键词检索历史记录，支持分词匹配和多关键词组合（如"华夏卡"可匹配"华夏银行信用卡"） |
| ✏️ **修改/删除** | 支持按关键词定位并修改或删除已有记录，含歧义保护和删除前确认 |
| 📄 **导出文件** | 将统计报告导出为本地 Markdown 文件 |
| 🆔 **确认回执** | 每次添加记录回复中展示具体内容+事件ID，确保用户可核实记录入库 |
| 🔒 **写入安全** | 并发写入自动重试（3次/0.3s间隔），解决多进程同时写入的文件锁冲突 |
| 🆔 **ID唯一性保障** | 毫秒级时间戳+序号生成唯一ID，杜绝快速连续添加时ID重复 |

---

## 兼容性说明

| 功能 | WorkBuddy | OpenClaw | 其他框架 |
|------|-----------|----------|----------|
| 基础记录功能 | ✅ 已测试 | ✅ 已测试 | 未测试 |
| 自动化提醒 | ✅ 已测试 | ⚠️ 未测试 | ⚠️ 未测试 |
| 修改/删除记录 | ✅ 已测试 | ⚠️ 未测试 | 未测试 |

> **提醒功能说明**：自动化提醒（添加待办时自动创建提醒、标记完成时自动删除提醒）是基于 WorkBuddy 的自动化系统实现的。如果你在 OpenClaw 或其他框架中安装使用，这部分功能可能需要自行适配。

---

## 快速开始

### 1. 安装技能

将本仓库克隆或下载到 WorkBuddy 用户级技能目录：

```bash
# Windows
git clone https://github.com/QU8/Memo.git "%USERPROFILE%\.workbuddy\skills\Memo"

# macOS / Linux
git clone https://github.com/QU8/Memo.git ~/.workbuddy/skills/Memo
```

### 2. 初始化数据文件

数据文件会在首次写入记录时自动创建，无需手动操作。

默认路径：`~/.workbuddy/skills/Memo/records.json`

### 3. 在 WorkBuddy 中加载技能

在对话框输入：

```
加载记事本技能
```

---

## 使用示例

### 添加记录

```
帮我记一下今天和贾辉沟通了ERP权限的问题
```

```
✅ 记录已保存
📝 内容：和贾辉沟通了ERP权限的问题
🆔 事件ID：20260322090000_00
📅 工作日期：2026-03-22
🏷️ 类型：沟通 | 临时
👤 涉及人员：贾辉
```

---

### 添加待办（自动创建提醒）

```
记一下明天上午要去财务对账
```

```
✅ 记录已保存
📝 内容：明天上午要去财务对账
🆔 事件ID：20260323080000_00
📅 工作日期：2026-03-23
🏷️ 类型：其他 | 临时
🔔 已自动创建提醒：2026-03-23 工作提醒（周一 08:00 触发）
```

---

### 统计报告

```
帮我统计本周工作
```

```markdown
# 工作记录导出

**导出时间**：2026年03月22日 09:00
**记录期间**：2026-03-16 - 2026-03-22
**记录总数**：12条

## 统计汇总
| 统计维度 | 数量/占比 |
|----------|-----------|
| 总记录数 | 12条 |
| 计划内事务 | 4条 (33%) |
| 临时事务 | 8条 (66%) |
...
```

---

### 标记完成（自动删除提醒）

```
财务对账的事搞定了
```

```
✅ 记录已更新（待办已完成）
🆔 事件ID：20260323080000_00
🗑️ 已删除自动化提醒：2026-03-23 工作提醒
```

---

### 修改记录

```
把ERP权限那条改成：贾辉确认ERP权限已开通
```

```
✅ 记录已更新
📝 修改内容：content 已更新
🆔 事件ID：20260322090000_00
📅 工作日期：2026-03-22
```

---

## 命令行（CLI）

`main.py` 内置完整 CLI 入口，无需 AI 即可直接操作：

```bash
python main.py <command> [options]
```

**常用命令：**

```bash
# 添加记录
python main.py add "今天和财务对账" --date 2026-04-01
python main.py add "明天上午开会" --date 2026-04-02 --todo --reminder 09:00

# 标记完成
python main.py done 20260401100000_00
python main.py done --keyword 财务对账   # 按关键词

# 关键词搜索
python main.py search 财务

# 列出所有未完成待办
python main.py todos

# 统计
python main.py stat --start 2026-03-01 --end 2026-03-31

# 导出报告
python main.py export 2026-03-01 2026-03-31 --out 3月报告.md
```

**add 命令选项：**
| 选项 | 说明 |
|------|------|
| `--date / -d` | 工作日期，默认今天 |
| `--type / -t` | 工作类型（沟通/会议/文档/其他…） |
| `--todo` | 标记为待办 |
| `--done` | 标记已完成 |
| `--reminder` | 提醒时间，格式 HH:MM |

---

## 文件结构

```
Memo/
├── SKILL.md              # 技能行为定义（AI 读取）
├── main.py               # 数据操作工具层
├── skill.yaml            # 技能元数据配置
├── README.md             # 项目说明文档
└── references/
    ├── field-rules.md    # 字段自动识别规则
    └── report-format.md  # 统计报告输出格式
```

> ⚠️ `records.json`（个人数据文件）不会上传到仓库。

---

## 数据格式

每条记录的 JSON 结构如下：

```json
{
  "id": "20260322090000_00",
  "content": "和贾辉沟通了ERP权限的问题",
  "timestamp": "2026-03-22T09:00:00",
  "work_date": "2026-03-22",
  "work_type": "沟通",
  "planning": "临时",
  "importance": "未标注",
  "urgency": "未标注",
  "quality": "未标注",
  "contacts": ["贾辉"],
  "contact_count": 1,
  "time_info": "未标注",
  "is_todo": false,
  "todo_done": false,
  "reminder_time": null
}
```

---

## Python API

`main.py` 提供完整的数据操作接口，可在脚本中直接调用：

```python
from main import MemoSkill

s = MemoSkill()

# 添加记录（含自定义提醒时间）
s.add_record("明天下午4点要去财务对账", work_date="2026-03-27",
             extra_fields={"is_todo": True, "reminder_time": "16:00"})

# 按日期筛选（推荐，查询首选）
records = s.filter_by_date("2026-03-16", "2026-03-22")

# 获取待办
todos = s.get_todos()

# 关键词搜索
results = s.search("ERP")

# 修改记录
s.update_record(keyword="ERP", updates={"content": "ERP权限已开通"})

# 删除记录
s.delete_record(keyword="周报")

# 导出报告
path = s.export_report("2026-03-16", "2026-03-22")
print(f"报告已导出：{path}")

# 智能同步辅助
name = s.get_automation_name("2026-03-27")          # "2026-03-27 工作提醒"
rrule = s.build_reminder_rrule("2026-03-27", "16:00") # "FREQ=WEEKLY;BYDAY=SA;BYHOUR=16;BYMINUTE=0"
todos = s.get_pending_todos_for_date("2026-03-27")   # 该日期所有未完成待办
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v2.0.1** | 2026-05-27 | **Bug修复**：ID生成增加毫秒精度，修复同秒内多次添加导致记录ID重复的问题；timestamp字段统一 |
| **v2.0.0** | 2026-05-10 | **体验优化**：1) 回复必须展示📝具体内容+🆔事件ID；2) save_records() 并发写入重试机制（3次/0.3s）；3) 查询优先 filter_by_date()；4) 扩展人名识别规则 |
| **v1.13.0** | 2026-04-24 | **数据安全防护**：save_records() 三层防护（备份+对比警告+自动合并） |
| **v1.12.0** | 2026-04-10 | **智能搜索**：search() 支持分词匹配和多关键词OR匹配 |
| **v1.11.0** | 2026-04-03 | **安全修复**：统一走 MemoSkill 实例方法 |
| **v1.10.0** | 2026-04-02 | 口语日期智能解析 |
| **v1.9.0** | 2026-04-01 | 内置 CLI 入口 |
| **v1.8.1** | 2026-03-30 | 修复单次提醒参数 |
| **v1.8.0** | 2026-03-30 | validFrom/validUntil 单次提醒 |
| **v1.7.0** | 2026-03-30 | SQLite 数据库方案 |
| **v1.6.0** | 2026-03-28 | 本地单文件存储 |
| **v1.5.0** | 2026-03-26 | 智能同步 |
| **v1.4.0** | 2026-03-26 | 任意时间提醒 |
| **v1.3.0** | 2026-03-16 | 修改/删除记录 |
| **v1.2.0** | 2026-03-15 | 多设备支持 |
| **v1.1.0** | 2026-03-01 | 自动化提醒管理 |
| **v1.0.0** | 2026-02-28 | 初始版本 |

---

## License

MIT License — 自由使用、修改和分发。
