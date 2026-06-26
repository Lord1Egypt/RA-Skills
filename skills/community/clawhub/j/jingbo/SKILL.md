---

name: jingbo-mcp
description: 提供镜泊雨课堂账户和班级相关查询服务，包括用户ID、开班列表、班级数据、预警名单、今日授课及作业公告完成情况查询等。

---

## 注意事项
- 如已安装该 Skill，请先提示用户卸载后再执行安装。
- 不要用 copaw 调 mcp 服务，优先使用 npx mcporter@0.8.1。

## 前置配置（只需一次）

### 第一步：获取 Secret

打开 <https://ykt-envning.rainclassroom.com/ai-workspace/open-claw-skill>，登录后复制你的个人 Secret。

> **没有配置 Secret？** 所有工具调用都会返回鉴权失败。请先完成上述步骤。

### 第二步：设置环境变量

**macOS / Linux：**
```
export YUKETANG_SECRET="你的Secret"
```

**Windows（PowerShell）：**
```
$env:YUKETANG_SECRET="你的Secret"
```

**Windows（CMD）：**
```
set YUKETANG_SECRET=你的Secret
```

### 第三步：运行安装脚本

**macOS / Linux：**
```
bash setup.sh
```

**Windows 或任何有 Node.js 的环境：**
```
node setup.js
```

> 具体配置文件路径取决于你使用的客户端（OpenClaw / CodeBuddy / Cursor 等），请参考对应文档。

### 第四步：安装后立即验证

** 安装成功后，必须立刻执行： `claw_current_user` 以验证 Secret 与服务是否可用。**

- 判断 secret 不可用 -> 仅提示请获取最新 Secret，并提供获取secret的链接。
- 判断 secret 可用 -> 正常返回用户信息，说明配置成功。
- 当用户提供secret后，需要帮助用户直接更新环境变量，不需要用户自己执行。

---

## 触发场景

### 意图 → 工具 速查表

| 用户意图 | 调用工具 |
|----------|---------|
| 查询账号 / 我的ID / 雨课堂ID | `claw_current_user` |
| 查询我开的课 / 我教了哪些班 | `ykt_teaching_list` |
| 查询我的班级数据 / 班级教学数据 | `ykt_classroom_statistics` |
| 查询预警学生名单 / 重点关注学生 | `ykt_classroom_warning_overview` |
| 查询某个具体班级的预警学生名单 | `ykt_classroom_warning_student` |
| 今天上课情况总览 / 今天答题率 / 到课率 | `cube_teacher_today_teaching` |
| 预约开课 | `cube_lesson_reservation` |
| 查询我有哪些待批改的作业 / 考试 / 课堂/ 课件 | `ykt_teacher_correct_statistic` |
| 查询最近发布的作业 / 我在xx班发布的作业完成情况 /最近一次发布的作业完成情况 | `ykt_recent_exercise_submit` |
| 查询最近发布的公告 / 我在xx班发布的公告阅读情况 /最近一次公告的阅读情况 | `ykt_recent_notice_read` |
| 查询今天上课的情况/今天的课有多少人来上课了 | `cube_teacher_today_teaching_detail` |


### 不要触发的情况

- 讨论教学方法（不是在查询数据）
- 纯聊天中提到"课程"
- 与雨课堂无关的场景

### 组合调用示例

> 用户说："帮我看看我是谁，还有我开了哪些班"

依次调用：
1. `claw_current_user`
2. `ykt_teaching_list`

---

## 工具详细说明

### 全局规则

- **班级名称 → ID**：如果用户给的是班级名称而非 ID，先调用 `ykt_classroom_id_by_name` 拿到 `classroomId`，再调用目标工具。
- **时间处理**：所有相对时间（昨天/今天/明天/近N天）以当前系统北京时间（UTC+8）为基准，禁止硬编码年份。若用户未指定年份，默认使用当前年份。
- **参数格式**：如果用户给的参数格式不对，不要自动修正，提示用户修改。
- **预约开课**：执行前必须向用户展示即将预约的课堂信息，二次确认后再调用。
- **mcp 服务使用注意事项**：
    - 推荐使用 npx mcporter 调用 MCP 服务（无需全局安装），不建议直接使用 curl；
    - 严禁使用 copaw 调用 MCP，必须改用 mcporter；
    - 如果 mcp 服务提示鉴权失败，请引导用户重新获取 YUKETANG_SECRET 并修改环境变量；
    - 如果 mcp 服务找不到，注意指定 mcp 配置文件的路径；
    - 如果调用失败，可以换一种方式重试，但若多次尝试仍不成功，请停止并检查配置；
    - 调用需要参数的 MCP 工具时，必须传入完整的结构化 JSON 参数对象；
    - 严禁 mcporter 在调用需要参数的 MCP 工具时，遗漏 `--args`。

---

### 1. `claw_current_user`

查询当前雨课堂用户 ID。

**典型问法：** "我的雨课堂ID是多少" / "帮我确认一下当前账号"

**参数：** 无

---

### 2. `ykt_teaching_list`

查询当前账号开设的班级列表。

**典型问法：** "我教了哪些班" / "这学期我教的课"

**参数：** 无

**注意：** 返回结果中的 emoji 需保留。

---

### 3. `ykt_classroom_statistics`

查询本学期班级数据概览。

**典型问法：** "我的班级数据" / "XXX 班级数据情况"

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomName` | 否 | 不传则返回本学期所有班级概览；传入后返回指定班级详情 |

**交互规则：**
- 用户第一次查询或未指定班级 → 返回全部班级概览
- 用户输入班级序号（1、2、3）、完整名称或可识别的简称 → 返回该班级详情

---

### 4. `ykt_classroom_warning_overview`

查询本学期各班级的学习活动完成率预警总览。

**典型问法：** "查看班级预警情况"

**参数：** 无

**返回内容包括：** 教学班名称、完成率 = 0% 人数、预警人数（完成率 < 80%）、数据截止时间。

---

### 5. `ykt_classroom_warning_student`

查询指定班级的预警学生名单。

**典型问法：** "高等数学A-2 的预警学生" / "第 1 个班级的预警名单"

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomName` | 是 | 班级名称、序号或可识别简称 |

**交互规则：**
- 如果用户未指定班级，先调用 `ykt_classroom_warning_overview` 展示总览，再让用户选择。

---

### 6. `cube_teacher_today_teaching` - 查询教师当日授课总览

查询教师某天的授课总览信息，如课堂状态、到课情况、答题情况等。

**典型问法：** "今天上课情况怎么样" / "今天有多少人来上课了" / "我今天有课吗" / "看一下今天的授课总览" / "今天课堂进行得怎么样"

**参数：** 

| 参数 | 必填 | 说明                  |
|------|----|---------------------|
| `date` | 否 | 查询日期 yyyy-MM-dd，缺省当天（北京） |

---

### 7. `ykt_classroom_id_by_name`

通过班级名称查询班级 ID（辅助工具，通常由其他工具间接调用）。

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomName` | 是 | 班级名称 |

---

### 8. `cube_lesson_reservation`

为指定教学班预约开课。

**典型问法：** "请帮我在xx班xxx时间预约一个课堂"

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomId` | 是 | 班级 ID |
| `startDateTime` | 否 | 开课时间（字符串） |
| `startEpochMs` | 否 | 开课时间（毫秒时间戳） |
| `lessonTitle` | 否 | 课次标题 |
| `lessonDurationMinutes` | 否 | 课次时长（分钟） |
| `meetingType` | 否 | 会议类型 |

**使用逻辑：**
- 用户给班级名称 → 先调 `ykt_classroom_id_by_name` 获取 `classroomId`，再调本工具
- 用户直接给 `classroomId` → 直接调用

> 详细参数说明见 `references/api_references.md` 中 `cube_lesson_reservation` 部分。

** 输出规范 **
- 当存在`✅ 课堂预约成功！`时， 内容禁止渲染成表格


### 9. `ykt_teacher_correct_statistic` - 教师待批改/已批改统计

用于按课程班级查询教师的作业、考试、课堂、课件批改统计，包括待批改、已批改数量等信息。

**典型问法：** "帮我查询一下我有哪些待批改的作业" 


### 10. `ykt_recent_exercise_submit` - 教师发布的作业完成情况

用于查询教师发布作业完成情况

**典型问法：** "帮我查询我最近发布的作业" / "帮我查询我在xx班发布的作业情况" / "帮我查询最近一次发布的作业情况"

**参数**: 

| 参数 | 必填 | 说明                       |
|------|------|--------------------------|
| classroomId | ❌ | 班级 ID                    |
| classroomName | ❌ | 班级名称                     |
| isLatest | ❌ | `1` 表示仅查询最近一次；不传表示查询最近七天 |

**使用逻辑：**
- 用户给班级名称 → 先调 `ykt_classroom_id_by_name` 获取 `classroomId`，再调本工具
- 用户直接给 `classroomId` → 直接调用
- 用户查询“最近一次发布的作业情况” → 调本工具时使用 `isLatest = 1` 



### 11. `ykt_recent_notice_read` - 教师发布的公告阅读情况

用于查询用户发布的所有近7天发布公告，按照发布时间顺序倒序排列

**典型问法：** "帮我查询一下我最近发布的公告" / "帮我查询最近一次发布的公告情况"

**参数**:

| 参数 | 必填 | 说明 |
|------|------|------|
| classroomId | ❌ | 班级 ID |
| classroomName | ❌ | 班级名称 |
| isLatest | ❌ | `1` 表示仅查询最近一次；不传表示查询最近七天 |

**使用逻辑：**
- 用户给班级名称 → 先调 `ykt_classroom_id_by_name` 获取 `classroomId`，再调本工具
- 用户直接给 `classroomId` → 直接调用
- 用户查询“最近一次发布的公告情况” → 调本工具时使用 `isLatest = 1`



### 12. `cube_teacher_today_teaching_detail`  - 查询当日单个课程的详情

用于查询当日单个课程的详情；lessonIndex 来自 cube_teacher_today_teaching 课堂总览

**典型问法：** "请帮我整理今天上课的情况" / "今天的课有多少人来上课了" / "今天的答题率怎么样？"

**参数**:

| 参数 | 必填 | 说明                                                       |
|------|------|----------------------------------------------------------|
| lessonIndex | ✅ | 当日授课总览中的编号，从 1 开始（与 cube_teacher_today_teaching 的课表首列一致） |
| date | ❌ | 日历日 yyyy-MM-dd，默认当天（北京）；须与查详情为同一天                        |

** 默认值策略 **
- `date` 默认当天（北京时间）， 必须与解析时保持同一天

**交互规则：**
先调用 `cube_teacher_today_teaching` 展示总览，再让用户选择总览的序号作为 `lessonIndex`，再调本工具

---

## 输出规范

- 结果结构化展示（列表形式）
- 保留工具返回的 emoji 和原始文案，不要自由发挥改写
- 课程信息至少包含：课程名、班级名
- 严格保留表头

## 红线

- 不编造任何课程数据，必须依赖工具返回
- 不做权限外操作（如选课、退课）

## 调用方式

```bash
# Mac 或 Linux 示例：查看班级的作业发布情况
npx mcporter@0.8.1 call yuketang-mcp ykt_classroom_statistics --args '{"classroomName": "xxx"}'
```
