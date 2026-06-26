---
name: interview-scheduler-claw
description: "面试邀约自动化协调。核心职责：自动联系候选人并协调面试官时间。业务价值：日程同步——自动查询全员日历空档，实现精准邀约。激活场景：用户提供面试安排表格（Excel/CSV），包含候选人邮箱、面试官信息，要求安排面试、约面试、发面试邀请、协调面试时间、查面试官空闲等。也适用于自然语言如帮我安排这几场面试、把这批候选人约起来、查一下面试官下周有没有空等请求。触发关键词：安排面试、约面试、面试邀约、协调面试、面试安排、面试邀请、候选人面试、发面试邮件、约面、安排面试时间、面试官空闲、查面试官日程、批量约面、面试协调。依赖飞书日历 API（含视频会议创建）和邮件发送能力。"
---

# 约面招聘协调虾 — 面试邀约自动化

## 执行策略（按优先级）

### 🥇 优先级 1：飞书插件工具（openclaw-lark）

检查环境是否安装了 `openclaw-lark` 插件。涉及飞书日历和通讯录的操作优先使用插件原生工具：

| 工具名 | 用途 |
|--------|------|
| `feishu_search_user` | 按姓名搜索员工 open_id |
| `feishu_calendar_event` | 创建/查询/修改/删除面试日程 |
| `feishu_calendar_freebusy` | 批量查询面试官空闲忙状态（1-10 人） |
| `feishu_calendar_event_attendee` | 添加面试官为参会人 |
| `feishu_calendar_calendar` | 获取/管理日历 |

**判断条件**：当前环境中可用 `feishu_calendar_event` 工具时，直接使用插件工具完成所有飞书操作，跳过优先级 2。

> ⚠️ 插件工具使用**用户身份**（user_access_token），需用户完成 OAuth 授权。如授权未完成，工具会自动引导用户授权。

**插件工具要点**：
- 时间格式：ISO 8601（带时区），如 `2026-03-28T10:00:00+08:00`
- `user_open_id` 必填：值取 SenderId（`ou_xxx`）
- 参会人 ID 统一用 `open_id`
- 创建日程时可直接传 `attendees` + `vchat`（视频会议），无需分步
- `list` 自动展开重复日程，时间区间不超过 40 天

### 🥈 优先级 2：API 脚本方式

当飞书插件未安装或不可用时，退化为使用 API 脚本。

**前置要求**：
- 环境变量 `FEISHU_APP_ID`、`FEISHU_APP_SECRET`
- 应用后台已开启 `calendar:calendar`、`contact:user.id:readonly` 权限
- 详见 [references/feishu-calendar-api.md](references/feishu-calendar-api.md)
- 脚本：[scripts/feishu-calendar.sh](scripts/feishu-calendar.sh)

> ⚠️ 脚本方式使用 `tenant_access_token`（应用身份），只能操作应用日历，**无法查询用户 freebusy**。查空闲功能将不可用。

### 📧 邮件发送（独立于飞书）

- **有 SMTP 配置**：`SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASS` → Python `smtplib` 直接发送
- **无 SMTP 配置**：生成邮件草稿文本，用户手动发送

---

## 表格格式约定

输入表格（Excel/CSV）应包含以下字段：

**必填：**

| 字段 | 说明 |
|------|------|
| 候选人姓名 | 候选人全名 |
| 候选人邮箱 | 用于发送面试邀请 |
| 面试官 | 面试官姓名（多人用中文逗号或顿号分隔） |

**可选：**

| 字段 | 说明 | 默认值 |
|------|------|-------|
| 应聘岗位 | 岗位名称 | "技术面试" |
| 面试时长 | 分钟数 | 60 |
| 期望日期范围 | 如"下周"、"3/28-3/30" | 最近 5 个工作日 |
| 备注 | 补充信息 | — |

表头名称可灵活变体（如"邮箱"≈"电子邮件"≈"Email"），智能识别。

---

## 工作流

### 步骤 1：解析表格

读取 Excel/CSV（`openpyxl` 或 `pandas`），逐行提取候选人信息。校验必填字段，缺失则标记并通知用户补充，不中断其他记录。

### 步骤 2：查询面试官 open_id

将面试官姓名转为飞书 `open_id`：

- **插件方式**：调用 `feishu_search_user` 按姓名搜索
- **脚本方式**：调用飞书通讯录搜索 API（见 [references/feishu-calendar-api.md](references/feishu-calendar-api.md)）

找不到时向用户确认正确姓名或要求提供 open_id。缓存已查到的映射，同批次不重复查询。

### 步骤 3：查询空闲时间

对该候选人的所有面试官批量查询空闲时段：

- **插件方式**：调用 `feishu_calendar_freebusy`，传 `user_ids`（数组）+ `time_min` + `time_max`
- **脚本方式**：告知用户 freebusy 需要用户身份，引导安装飞书插件

查询范围按"期望日期范围"确定：
- "下周" → 下周一至周五
- "3/28-3/30" → 指定日期范围
- 未指定 → 最近 5 个工作日（跳过周末）

### 步骤 4：计算并推荐时段

1. 提取每位面试官的 busy 时段，合并取**并集**
2. 在查询范围内找出 busy 之间的空闲间隔
3. 按面试时长过滤（默认 60 分钟），保留足够长的空闲段
4. 排序：工作日 > 周末，上午(9:00-12:00) > 下午(14:00-18:00)

**向用户展示 2-3 个推荐时段，等待确认后再创建日程。不自动创建。**

输出示例：
```
🎯 张三（前端工程师）面试官空闲时段推荐：

1. 3/28 周五 10:00-11:00  ✅ 首选
2. 3/31 周一 14:00-15:00
3. 4/1 周二 09:00-10:00

请确认时段（回复序号或指定时间）。
```

### 步骤 5：创建飞书会议日程

用户确认时段后创建带视频会议的面试日程：

**插件方式：**
```json
{
  "action": "create",
  "summary": "面试 — 前端工程师 — 张三",
  "start_time": "2026-03-28T10:00:00+08:00",
  "end_time": "2026-03-28T11:00:00+08:00",
  "description": "岗位：前端工程师\n候选人：张三\n面试官：李四、王五",
  "user_open_id": "ou_xxx",
  "attendees": [
    {"type": "user", "id": "ou_aaa"},
    {"type": "user", "id": "ou_bbb"}
  ],
  "vchat": {"vc_type": "vc"}
}
```

**脚本方式：**
```bash
# 获取主日历
cal_id=$(./scripts/feishu-calendar.sh primary-calendar)

# 创建日程（--meeting 自动生成飞书视频会议链接）
resp=$(./scripts/feishu-calendar.sh create-event \
  "$cal_id" \
  "面试 — 前端工程师 — 张三" \
  "1711497600" "1711501200" \
  "岗位：前端工程师\n候选人：张三\n面试官：李四、王五" \
  --meeting)

event_id=$(echo "$resp" | jq -r '.data.event.event_id')

# 添加面试官为参会者（脚本方式必须分两步）
./scripts/feishu-calendar.sh add-attendees "$cal_id" "$event_id" /tmp/attendees.json
```

> ⚠️ 脚本方式关键注意：
> - `timestamp` 必须是秒级字符串（如 `"1711497600"`）
> - 创建 event 不接受 `attendees`，必须先创建再单独添加
> - 插件方式无此限制

### 步骤 6：发送面试邀请邮件

邮件模板见 [references/email-templates.md](references/email-templates.md)。

根据候选人姓名自动选择尊称（"先生"/"女士"），模板占位符全部替换为实际值。

- **有 SMTP 配置**：`smtplib` 直接发送
- **无 SMTP 配置**：生成完整邮件文本，附在汇总中提示用户手动发送

### 步骤 7：输出汇总

每处理完一个候选人后输出结构化汇总：

```
✅ 面试安排完成

📋 已安排：
1. 张三（前端工程师）— 3/28 周五 10:00-11:00
   面试官：李四 · 邮件已发送 ✓ · 飞书会议已创建 ✓
   🔗 会议链接：https://vc.feishu.cn/j/xxx

⚠️ 待处理：
2. 王五（后端工程师）— 未找到面试官"赵六"的 ID，请确认姓名

📝 待发送邮件（未配置 SMTP）：
收件人：wangwu@email.com
Subject: 【面试邀请】XX公司 — 后端工程师 — 王五
Body: （邮件正文）
```

批量处理时逐个展示，全部完成后给出总数统计。

---

## 关键规则

- **插件优先**：有飞书插件时必须优先使用，退化为脚本时明确告知用户限制
- **先查空闲再创建**：创建面试日程前必须确认面试官空闲
- **逐条确认**：推荐时段后等待用户确认，不自动创建日程
- **去重保护**：同一候选人 24 小时内不重复发送邀请
- **错误隔离**：单个候选人失败不影响其他候选人处理
- **时区统一**：所有时间处理用 `Asia/Shanghai` (UTC+8)，展示用北京时间
- **对外操作先确认**：创建日程、发送邮件等操作需先与用户确认细节

## 插件工具速查

| 用户意图 | 工具 | action | 必填参数 |
|---------|------|--------|---------|
| 搜索员工 | feishu_search_user | - | query |
| 查空闲 | feishu_calendar_freebusy | list | time_min, time_max, user_ids[] |
| 创建面试日程 | feishu_calendar_event | create | summary, start_time, end_time, user_open_id |
| 查日程 | feishu_calendar_event | list | start_time, end_time |
| 邀请参会人 | feishu_calendar_event_attendee | create | calendar_id, event_id, attendees[] |

## 脚本命令速查（备选方案）

| 操作 | 脚本命令 |
|------|---------|
| 获取 token | `feishu-calendar.sh token` |
| 获取主日历 | `feishu-calendar.sh primary-calendar` |
| 创建日程(含会议) | `feishu-calendar.sh create-event <cal> <title> <start> <end> [desc] --meeting` |
| 添加参会者 | `feishu-calendar.sh add-attendees <cal> <evt> <json>` |

> ⚠️ 脚本方式**不支持** `freebusy-batch`（查询空闲），需引导安装飞书插件。

> 详细 API 参考见 [references/feishu-calendar-api.md](references/feishu-calendar-api.md)
