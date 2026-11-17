## tmeet CLI 完整参考

> 本文档为 `tmeet`（腾讯会议命令行工具）的**最小必要但完整的**CLI参考。
> 当 `meeting-deep-process` 技能未加载任何会议数据源技能时，可直接使用本文档中的命令获取原始会议数据。

---

### 安装

```bash
npm install -g @tencentcloud/tmeet@latest
```

---

### 认证

```bash
# 登录（必须后台运行以捕获授权URL）
tmeet auth login 2>&1 &

# 禁用自动打开浏览器
tmeet auth login --no-browser 2>&1 &

# 登出
tmeet auth logout

# 查看登录状态（无需登录即可执行）
tmeet auth status
```

> 除 `auth login`, `auth status` 外所有命令需先登录。

---

### 全局约定

**时间格式**：ISO 8601，含时区。例：`2026-03-12T14:00:00+08:00`。

**输出格式**：
| 参数 | 效果 |
|------|------|
| `--format json`（默认） | 紧凑JSON，模型解析用 |
| `--format json-pretty` | 美化缩进，展示用户阅读用 |
| `--compact` | 裁剪`data`字段，只保留必要字段（推荐查询类命令使用） |

**分页**：所有列表类命令统一用 `--page-token <token>` + `--page-size <n>`。
- 首页不传 `--page-token`
- 翻页取上次响应的 `data.next_page_token`
- 弃用参数：`--page` / `--pos` / `--pid` / `--size` / `--limit`

---

### 命令参考

#### meeting — 会议管理

##### create — 创建会议

```bash
tmeet meeting create --subject "主题" --start "2026-04-10T14:00:00+08:00" --end "2026-04-10T15:00:00+08:00"
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--subject <text>` | ✅ | — | 会议主题 |
| `--start <time>` | ✅ | — | 开始时间 |
| `--end <time>` | ✅ | — | 结束时间 |
| `--password <pwd>` | | — | 密码（4-6位数字） |
| `--timezone <tz>` | | — | 时区 |
| `--meeting-type <n>` | | `0` | `0`普通 `1`周期性 |
| `--join-type <n>` | | `0` | `1`所有 `2`仅受邀 `3`仅企业内部 |
| `--waiting-room` | | `false` | 开启等候室 |
| `--recurring-type <n>` | | `0` | `0`每天 `1`工作日 `2`每周 `3`每两周 `4`每月 |
| `--until-type <n>` | | `0` | `0`按日期 `1`按次数 |
| `--until-count <n>` | | `7` | 重复次数（天/周≤500，双周/月≤50） |
| `--until-date <date>` | | — | 结束日期 |
| `--invitees <ids>` | | — | openid列表，逗号分隔，≤100人 |
| `--water-mark-type <n>` | | `2` | `0`单排 `1`双排 `2`关闭 |
| `--audio-watermark` | | `false` | 音频水印，关闭用`=false` |
| `--auto-record-type` | | `none` | `none`/`local`/`cloud` |
| `--auto-asr` | | `false` | 自动转写，关闭用`=false` |

##### update — 更新会议

```bash
tmeet meeting update --meeting-id "100000000" [参数]
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-id <id>` | ✅ | 会议ID |
| `--subject <text>` | | 新主题 |
| `--start <time>` | | 新开始时间 |
| `--end <time>` | | 新结束时间 |
| `--meeting-type <n>` | 周期必填 | `0`普通 `1`周期性（修改周期性会议必须传`1`） |
| `--invitees <ids>` | | 与`--invitees-type`同时使用 |
| `--invitees-type <add\|remove\|replace>` | | 邀请变更策略 |
| 其余参数同create | | |

##### cancel — 取消会议

```bash
tmeet meeting cancel --meeting-id "100000000"
tmeet meeting cancel --meeting-id "100000000" --sub-meeting-id "200000001"  # 取消子会议
tmeet meeting cancel --meeting-id "100000000" --meeting-type 1               # 取消整场周期性
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-id <id>` | ✅ | 会议ID |
| `--sub-meeting-id <id>` | | 子会议ID |
| `--meeting-type <n>` | | `0`普通 `1`周期性 |

##### get — 获取会议详情

```bash
tmeet meeting get --meeting-id "100000000"
tmeet meeting get --meeting-code "123456789"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-id <id>` | 二选一 | 会议ID（优先级高） |
| `--meeting-code <code>` | 二选一 | 会议码 |

##### list — 待开始/进行中的会议列表

```bash
tmeet meeting list
tmeet meeting list --start "..." --end "..."
tmeet meeting list --show-all-sub 1
tmeet meeting list --page-token "<token>" --page-size 20
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--start <time>` | — | 起始时间 |
| `--end <time>` | — | 结束时间 |
| `--show-all-sub <n>` | `0` | `0`不展示 `1`展示所有子会议 |
| `--page-token <token>` | — | 分页游标 |
| `--page-size <n>` | `20` | ≤20 |

##### list-ended — 已结束会议列表

```bash
tmeet meeting list-ended
tmeet meeting list-ended --start "..." --end "..."
tmeet meeting list-ended --page-token "<token>" --page-size 30
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--start <time>` | — | 起始时间 |
| `--end <time>` | — | 结束时间 |
| `--page-token <token>` | — | 分页游标 |
| `--page-size <n>` | `30` | ≤30 |

##### invitees-list — 获取受邀者列表

```bash
tmeet meeting invitees-list --meeting-id "100000000"
tmeet meeting invitees-list --meeting-id "100000000" --page-token "<token>" --page-size 30
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--meeting-id <id>` | ✅ | — | 会议ID |
| `--page-token <token>` | | — | 分页游标 |
| `--page-size <n>` | | `30` | ≤30 |

##### invitees-add / invitees-remove / invitees-replace

```bash
tmeet meeting invitees-add    --meeting-id "100000000" --invitees "id1,id2"
tmeet meeting invitees-remove --meeting-id "100000000" --invitees "id1,id2"
tmeet meeting invitees-replace --meeting-id "100000000" --invitees "id1,id2,id3"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-id <id>` | ✅ | 会议ID |
| `--invitees <list>` | ✅ | openid列表，逗号分隔或重复传参，≤100人 |

---

#### contact — 通讯录

##### search — 搜索成员

```bash
tmeet contact search --username "张三"
tmeet contact search --username "张三" --job-title "工程师" --department-name "研发部"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--username <name>` | ✅ | 用户名 |
| `--job-title <title>` | | 职位过滤 |
| `--department-name <dept>` | | 部门过滤 |

##### lookup-by-phone / lookup-by-email

```bash
tmeet contact lookup-by-phone --phones "13800138000,13900139000"
tmeet contact lookup-by-email --emails "a@x.com,b@x.com"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--phones <list>` / `--emails <list>` | ✅ | 逗号分隔，≤50个 |

> `contact` 仅用于会议邀请和呼叫入会场景，严禁用于 `control kick`。

---

#### record — 录制管理

##### list — 查询录制列表

```bash
tmeet record list --meeting-id "100000000"
tmeet record list --meeting-code "123456789"
tmeet record list --start "2026-04-01T00:00:00+08:00" --end "2026-04-30T23:59:59+08:00"
tmeet record list --meeting-id "100000000" --start "..." --end "..."  # 组合
tmeet record list --page-token "<token>" --page-size 30
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--meeting-id <id>` | 至少一组 | — | 会议ID |
| `--meeting-code <code>` | 至少一组 | — | 会议码 |
| `--start <time>` + `--end <time>` | 至少一组 | — | 时间范围 |
| `--page-token <token>` | | — | 分页游标 |
| `--page-size <n>` | | `30` | ≤30 |

##### address — 获取录制文件下载地址

```bash
tmeet record address --meeting-record-id "record_abc123"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-record-id <id>` | ✅ | 录制ID（来自record list） |
| `--page-token <token>` | | 分页游标 |
| `--page-size <n>` | | ≤30 |

##### smart-minutes — 获取智能纪要

```bash
tmeet record smart-minutes --record-file-id "file_abc123"
tmeet record smart-minutes --record-file-id "file_abc123" --lang zh
tmeet record smart-minutes --record-file-id "file_abc123" --pwd "123456"
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--record-file-id <id>` | ✅ | — | 录制文件ID（来自record address） |
| `--lang <lang>` | | `default` | `default`原文 `zh`简中 `en`英文 `ja`日语 |
| `--pwd <pwd>` | | — | 录制文件访问密码 |

##### transcript-get — 获取转写详情

```bash
tmeet record transcript-get --record-file-id "file_abc123"
tmeet record transcript-get --record-file-id "file_abc123" --meeting-id "100000000" --pid "<id>" --limit "30"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--record-file-id <id>` | ✅ | 录制文件ID |
| `--meeting-id <id>` | | 会议ID |
| `--pid <id>` | | 起始段落ID |
| `--limit <n>` | | 查询段落数 |

##### transcript-paragraphs — 获取转写段落列表

```bash
tmeet record transcript-paragraphs --record-file-id "file_abc123"
tmeet record transcript-paragraphs --record-file-id "file_abc123" --meeting-id "100000000"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--record-file-id <id>` | ✅ | 录制文件ID |
| `--meeting-id <id>` | | 会议ID |

##### transcript-search — 搜索转写内容

```bash
tmeet record transcript-search --record-file-id "file_abc123" --text "关键词"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--record-file-id <id>` | ✅ | 录制文件ID |
| `--text <keyword>` | ✅ | 搜索关键词 |
| `--meeting-id <id>` | | 会议ID |

##### permission-apply-prepare / permission-apply-commit

```bash
tmeet record permission-apply-prepare --meeting-record-id "record_abc123"
tmeet record permission-apply-commit  --meeting-record-id "record_abc123"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-record-id <id>` | ✅ | 会议录制ID |
| `--meeting-id <id>` | | 会议ID |

> 无权限时先`prepare`预览→用户确认→再`commit`提交。

---

#### report — 会议报告

##### participants — 参会人列表

```bash
tmeet report participants --meeting-id "100000000"
tmeet report participants --meeting-id "100000000" --sub-meeting-id "200000001"
tmeet report participants --meeting-id "100000000" --start "..." --end "..."
tmeet report participants --meeting-id "100000000" --page-token "<token>" --page-size 50
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--meeting-id <id>` | ✅ | — | 会议ID |
| `--sub-meeting-id <id>` | | — | 子会议ID |
| `--start <time>` | | — | 起始时间 |
| `--end <time>` | | — | 结束时间 |
| `--page-token <token>` | | — | 分页游标 |
| `--page-size <n>` | | `100` | ≤100 |

##### waiting-room-log — 等候室成员

```bash
tmeet report waiting-room-log --meeting-id "100000000"
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--meeting-id <id>` | ✅ | — | 会议ID |
| `--page-token <token>` | | — | 分页游标 |
| `--page-size <n>` | | `100` | ≤100 |

---

#### control — 会中控制

##### call — 呼叫成员入会

```bash
tmeet control call --meeting-id "100000000" --users "id1,id2"
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--meeting-id <id>` | ✅ | 会议ID |
| `--users <list>` | ✅ | openid列表，≤20人 |

##### kick — 踢出成员

```bash
tmeet control kick --meeting-id "100000000" --users "id1,id2"
tmeet control kick --meeting-id "100000000" --users "id1" --sip-users "ms1" --pstn-users "mp1"
tmeet control kick --meeting-id "100000000" --allow-rejoin --users "id1"
```

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `--meeting-id <id>` | ✅ | — | 会议ID |
| `--users <list>` | 三选一 | — | 普通成员open_id |
| `--sip-users <list>` | 三选一 | — | Sip设备ms_open_id |
| `--pstn-users <list>` | 三选一 | — | Pstn设备ms_open_id |
| `--allow-rejoin` | | `false` | 是否允许重新入会 |

> `kick`的成员open_id必须来自`report participants`，严禁使用`contact search`结果。

---

#### tshoot — 问题排查

##### log — 导出日志

```bash
tmeet tshoot log
tmeet tshoot log --start "..." --end "..."
tmeet tshoot log --upload
```

| 参数 | 说明 |
|------|------|
| `--start <time>` | 日志起始时间（与`--end`同时使用） |
| `--end <time>` | 日志结束时间 |
| `--upload` | 上传至服务器（需登录） |

##### feedback — 反馈问题

```bash
tmeet tshoot feedback --category "tool_error" --intent "用户意图" --tool-name "子命令名" --error-code "错误码" --actions-tried "已尝试操作" --result "结果"
```

| 参数 | 必填 | 最大长度 | 说明 |
|------|:--:|:--:|------|
| `--category` | ✅ | — | `tool_not_found` / `tool_error` / `tool_inadequate` / `unexpected_result` / `suggestion` |
| `--intent` | ✅ | 200 | 用户原始意图 |
| `--actions-tried` | | 500 | 已尝试的操作 |
| `--result` | | 500 | 结果或阻塞点 |
| `--tool-name` | | — | 涉及子命令名 |
| `--error-code` | | — | 业务错误码 |

---

### 典型数据获取工作流

```
1. 获取会议列表
   tmeet meeting list --start "..." --end "..."
   tmeet meeting list-ended --start "..." --end "..."

2. 获取会议详情
   tmeet meeting get --meeting-id "..."

3. 获取录制列表
   tmeet record list --meeting-id "..."

4. 获取录制文件地址
   tmeet record address --meeting-record-id "..."

5. 获取智能纪要 / 转写
   tmeet record smart-minutes --record-file-id "..."
   tmeet record transcript-get --record-file-id "..."
   tmeet record transcript-paragraphs --record-file-id "..."
   tmeet record transcript-search --record-file-id "..." --text "关键词"

6. 获取参会人数据
   tmeet report participants --meeting-id "..."
```
