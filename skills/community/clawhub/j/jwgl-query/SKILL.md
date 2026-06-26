---
name: jwgl-query
description: Query a university jwgl/教务系统 for teacher-facing data such as 课程表 and 考试相关信息（监考/考务安排、课程考试安排、考试信息）. Also manage saved school URLs and teacher credentials through natural language. Use when the user asks to 查课程表、查考试安排、查监考/考务安排、添加学校 URL，或要求从教务系统按教师/学期提取表格结果。适合 legacy iframe-heavy jwgl sites with stored local credentials.
---

# JWGL Query

执行教务系统查询并直接返回结果。优先按用户原话理解需求，不要把老师、学期、输出样式写死。

## Interaction model

这个 skill 的正确分工是：

- **自然语言交互由 agent 负责**
- **脚本负责底层执行**

也就是说，用户应该直接说：

- 查某老师这周课表
- 查考试安排
- 添加学校，学校叫某学校，地址是 https://jwgl.example.edu.cn
- 添加某老师账号
- 删除某老师信息
- 删除某学校 URL
- 把某老师设为当前老师

然后由 agent：

1. 理解意图
2. 缺信息时继续追问
3. 必要时做删除确认 / 录入确认
4. 再调用脚本执行
5. 把结果整理成中文返回

不要把 CLI 命令当作对用户的主入口。CLI 只是底层执行接口。

对 agent 而言，脚本应该被当作“执行接口”而不是“交互界面”：

- 缺参数 → agent 追问用户
- 删除/覆盖 → agent 做确认
- 脚本返回结构化结果或结构化错误
- agent 再把结果翻译成自然语言

## Use

优先用这个 skill 处理以下需求：

- 查课程表
- 查考试相关信息（监考安排、考务安排、课程考试安排、考试信息）
- 查考试安排（默认走 `exam_all` 聚合查询）
- 管理学校 URL（新增、更新、删除、设置当前学校）
- 按教师 + 学期查询教务系统表格

如果用户只说“查考试安排”，优先用 `exam_all`。

## Query types

- `course_schedule`：课程表
- `invigilation`：考务安排 / 监考安排
- `exam_course_arrangement`：课程考试安排查询
- `exam_info`：考试信息查询
- `exam_all`：考试相关总查询（聚合考试类入口）

查询类型细节见 `references/query-types.md`。

## Natural-language usage

优先按下面这种方式理解并处理用户请求：

- “查某老师这周课表”
- “查某老师 2025-2026-2 的监考安排”
- “查考试安排”
- “添加学校，学校叫某学校，地址是 https://jwgl.example.edu.cn”
- “把某学校设为当前学校”
- “添加某老师账号，账号是 xxx，密码是 xxx”
- “删除某老师信息”
- “删除某学校这个学校 URL”
- “把某老师设为当前老师”

处理原则：

- 缺老师名就问老师名
- 缺学校 URL 时先问学校 URL
- 缺学期时按用户原话推断；不确定再追问
- 删除/覆盖账号前要确认
- 查询结果优先直接整理成中文摘要返回
- 只有在调试、回归测试或底层执行时才直接使用 CLI

## Agent behavior / language flow

### 添加老师账号

当用户说“添加老师”“录入老师账号”“记住某老师账号密码”时：

1. **若本地还没有学校 URL** → 先追问：
   - “先把学校教务系统 URL 发我一下，比如 `https://jwgl.example.edu.cn`。”
2. **若有多所学校且老师未明确属于哪所学校** → 追问：
   - “这位老师属于哪所学校？我这边要绑定到对应的学校 URL。”
1. **缺老师名** → 追问：
   - “要添加哪位老师？老师姓名是？”
2. **缺账号** → 追问：
   - “这位老师的登录账号是什么？”
3. **缺密码** → 追问：
   - “密码也发我一下，我录进去后后续就能直接查。”
4. **邮箱/手机号** → 明确视为可选项，默认不追问；只有用户主动提到时才保存
5. **老师已存在** → 不直接覆盖，先确认：
   - “已经有这位老师的记录了。要覆盖更新吗？”
6. **保存完成后** → 可补一句：
   - “要不要顺手把这位老师设为当前老师？”

### 管理学校 URL

当用户说“添加学校”“保存学校 URL”“修改学校地址”“删除学校 URL”“设为当前学校”时：

1. **新增学校时缺学校名** → 追问：
   - “这所学校叫什么名字？我本地会按学校名保存。”
2. **新增学校时缺 URL** → 追问：
   - “把这所学校的教务系统 URL 发我一下，比如 `https://jwgl.example.edu.cn`。”
3. **只给学校 URL，没给登录页 URL** → 默认拼成 `{base_url}/jsxsd/framework/jsMain.jsp`，一般不额外追问
4. **学校已存在** → 不直接覆盖，先确认：
   - “已经有这所学校的 URL 记录了。要覆盖更新吗？”
5. **脚本参数兼容**
   - 学校名允许 `--school` 或旧写法 `--name`
   - 老师名允许 `--teacher` 或旧写法 `--name`
6. **删除学校 URL**
   - 缺学校名就追问
   - 若有老师绑定该学校，先明确提示影响，再确认删除
6. **设置当前学校**
   - 学校名明确就直接设置
   - 学校名不明确就追问：
     - “你要把哪所学校设为当前学校？”

### 删除老师账号信息

当用户说“删除老师”“删掉某老师信息”时：

1. **缺老师名** → 追问：
   - “你要删哪位老师？我这边删的是本地保存的账号信息。”
2. **老师名明确** → 必须二次确认：
   - “确认删除‘某老师’的本地账号信息吗？删掉后后续查询需要重新录入。”
3. 只有得到明确确认（如“是”“确认”“删除”）后才执行
4. 删除后明确告知结果；若影响 `current_teacher`，也要说明

### 设置当前老师

当用户说“设为当前老师”“默认用某老师”时：

1. **老师名明确** → 直接设置
2. **老师名不明确** → 追问：
   - “你要把哪位老师设为当前老师？”
3. 若该老师尚未保存账号信息，先提示录入，不要假设存在

### 查询课表 / 监考 / 考试安排

当用户发起查询时：

1. **先确定学校**
   - 如果老师已绑定学校，优先使用老师绑定的学校 URL
   - 否则如果已有 `current_school`，优先使用当前学校
   - 如果本地还没有学校 URL，先追问：
     - “先把学校教务系统 URL 发我一下，我保存后就能继续查。”
   - 如果本地保存了多所学校但当前请求无法确定是哪所，追问：
     - “你这次要查哪所学校的教务系统？”
2. **缺老师名**
   - 如果已有 `current_teacher`，优先默认使用当前老师，并可简短说明
   - 如果没有 `current_teacher`，追问：
     - “你要查哪位老师？”
3. **缺学期**
   - 如果用户说“这周课表”“这学期安排”，优先按当前学期理解
   - 如果用户明确指定学期，直接按指定学期查
   - 如果需求涉及历史数据且不明确，再追问：
     - “你要查哪个学期？比如 `2025-2026-2`。”
4. **老师账号不存在**
   - 不直接甩 CLI 命令给用户，先用自然语言追问：
     - “还没有保存这位老师的账号信息。把登录账号和密码发我，我先录入，再帮你查。”
5. **查到数据**
   - 优先返回中文摘要
   - 只有在调试或用户明确要求时再贴 JSON

### 查不到数据时的回复

区分三种情况：

1. **确实无数据**
   - “没查到数据。”
   - 或更具体：
     - “没查到这位老师这周的课表。”
     - “没查到这个学期的监考安排。”
2. **条件可能不对**
   - “没查到数据。可能是老师名称或学期不对，要不要我换个学期再查一次？”
3. **查询过程报错 / 页面异常**
   - 不要伪装成“无数据”
   - 应明确说：
     - “这次不是没数据，是查询过程出错了。我可以继续帮你排查。”

### 总体风格

- 让用户通过自然语言完成操作，不要求用户直接使用 CLI
- 追问只补必要信息，避免一次性盘问过多字段
- 删除、覆盖、替换当前老师等动作都要确认
- 返回结果时优先用简洁中文总结，必要时再附结构化数据

## Response templates

### 列出老师怎么回

当用户问“现在有哪些老师”“列出老师账号”时：

- 优先返回简洁列表，不直接贴底层 JSON
- 标出当前老师

推荐格式：

- 已保存老师：
  - 叶志鹏（当前）
  - 默认

如果为空：

- 现在还没有保存任何老师账号信息。

### 查课表怎么回

当查到课表时：

- 先给一句结论：
  - “查到了，某老师这周课表如下：”
- 再按星期顺序列出
- 每条尽量包含：星期、节次、时间、课程名、教室；班级/人数视情况附上

推荐格式：

- 星期一 1,2节 `08:00-09:40`
  - 某课程
  - 教室：某教学楼A101[01-02]节
  - 班级：某班级
  - 人数：40

如果用户问“今天还有什么课”或“明天课表”，优先只返回对应日期的子集，不把整周都贴出来。

### 查考试安排 / 监考安排怎么回

当查到考试相关数据时：

- 先一句总结：
  - “查到了，这学期共有 N 条考试安排。”
- 再按条目列出关键字段，例如：课程名称、考试时间、考场、类别、考生数
- 若 `exam_all` 返回多类结果，可按 `query_type` 分组摘要：
  - 考务安排：0 条
  - 课程考试安排：2 条
  - 考试信息：1 条

### 没数据怎么回

当底层成功返回 `count=0` 时，不要说“报错”，应明确说：

- “没查到数据。”
- 或更具体：
  - “没查到某老师这周的课表。”
  - “没查到这个学期的监考安排。”

如果条件可能有问题，可追加：

- “可能是老师名称或学期不对，要不要我换个学期再查一次？”

### 报错怎么回

当底层返回结构化错误或执行失败时：

1. **缺老师账号**（例如 `MISSING_TEACHER_CREDENTIALS`）
   - “还没有保存这位老师的账号信息。把登录账号和密码发我，我先录入，再帮你查。”
2. **老师不存在**（例如 `TEACHER_NOT_FOUND`）
   - “本地还没有这位老师的信息。要不要我先帮你添加？”
3. **老师已存在**（例如 `TEACHER_ALREADY_EXISTS`）
   - “已经有这位老师的记录了。要覆盖更新吗？”
4. **缺少必要字段**（例如 `MISSING_REQUIRED_FIELDS` / `MISSING_TEACHER_NAME`）
   - 不向用户展示错误码，直接补问缺的字段
5. **页面结构 / 系统异常**
   - “这次不是没数据，是查询过程出错了。我可以继续帮你排查。”

除非用户明确要求调试细节，否则不要直接把 traceback 或 CLI 原文贴给用户。

## Script execution

在 skill 根目录执行底层脚本时，可使用：

```bash
# 可手动初始化环境（首次拉取后）
bash scripts/setup.sh

# 查询执行（首次运行会自动补环境）
bash scripts/run.sh --config config.json --teacher "某老师" --term "2025-2026-2" --query-type exam_all --headless
bash scripts/run.sh --config config.json --teacher "某老师" --term "2025-2026-2" --query-type invigilation --headless
bash scripts/run.sh --config config.json --teacher "某老师" --term "2025-2026-2" --query-type exam_course_arrangement --headless
bash scripts/run.sh --config config.json --teacher "某老师" --term "2025-2026-2" --query-type exam_info --headless
bash scripts/run.sh --config config.json --teacher "某老师" --query-type course_schedule --headless

# 账号管理执行接口
python3 scripts/manage_accounts.py --config config.json list
python3 scripts/manage_accounts.py --config config.json add --teacher "某老师" --username "账号" --password "密码" --set-current
python3 scripts/manage_accounts.py --config config.json update --teacher "某老师" --password "新密码"
python3 scripts/manage_accounts.py --config config.json remove --teacher "某老师"
python3 scripts/manage_accounts.py --config config.json set-current --teacher "某老师"
python3 scripts/manage_accounts.py --config config.json school-list
python3 scripts/manage_accounts.py --config config.json school-add --school "某学校" --base-url "https://jwgl.example.edu.cn" --set-current
python3 scripts/manage_accounts.py --config config.json school-update --school "某学校" --base-url "https://jwgl.example.edu.cn"
python3 scripts/manage_accounts.py --config config.json school-remove --school "某学校"
python3 scripts/manage_accounts.py --config config.json school-set-current --school "某学校"
```

兼容旧写法（为了减少踩坑）：

- 学校名：`--school` / `--name`
- 老师名：`--teacher` / `--name`
- 登录账号：`--username` / `--user` / `--account`
- 登录密码：`--password` / `--pass`

不要假设 `scripts/*.sh` 在安装后的 skill 目录里保留了可执行位。执行底层 shell 脚本时，优先使用 `bash scripts/...`。

调试探测脚本已放到 `tools/`，仅在诊断页面结构时使用，不作为主流程入口。

## Output

默认输出 JSON。

返回时：

- 直接给用户结论
- 有数据时，提炼为中文摘要
- 无数据时，明确说“未查询到数据”
- 需要调试时再使用 `--debug-dir`

## Account management

账号管理的对外入口应是自然语言，例如：

- “添加某老师，账号是 xxx，密码是 xxx”
- “删除某老师信息”
- “把某老师设为当前老师”
- “更新某老师账号密码”

agent 负责：

- 问缺失字段
- 做删除/覆盖确认
- 再调用底层脚本

底层脚本仍保留，便于调试或手动执行：

```bash
python3 scripts/manage_accounts.py --config config.json list
python3 scripts/manage_accounts.py --config config.json add
python3 scripts/manage_accounts.py --config config.json update
python3 scripts/manage_accounts.py --config config.json remove
python3 scripts/manage_accounts.py --config config.json set-current
```

若查询时未找到该老师账号：

- 在终端交互环境中，脚本会自动进入交互式录入
- 在非交互环境中，脚本会提示先补录账号密码，再重新查询

## Rules

- 只在本地 `config.json` 中保存凭据，不要外发
- 用户提供新的教师账号/密码时，应更新到本地配置中保存，便于后续直接查询
- Chrome / ChromeDriver 版本不一致时，优先自动探测并使用与当前 Chrome 匹配的驱动，不依赖写死的本地驱动包
- 优先返回对话结果，不依赖通知/邮件
- 遇到页面结构差异时，先看 `references/query-types.md` 再调整对应 query config
