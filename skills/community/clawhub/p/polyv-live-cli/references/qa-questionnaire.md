# 问答问卷管理

本文档详细介绍保利威直播 CLI 的问答卡和问卷管理命令。

## 命令概览

```bash
# 问答卡命令
<CLI> qa <子命令> [选项]

# 问卷命令
<CLI> questionnaire <子命令> [选项]
```

---

## 问答卡命令 (QA)

问答卡用于在直播过程中发起答题互动。

### qa add-edit - 新建或编辑问答卡

新建或编辑频道答题卡。后端接口语义是：省略 `--question-id` 新建答题卡；传入 `--question-id` 编辑已有答题卡。

```bash
<CLI> qa add-edit -c <频道ID> --name <标题> --type R --item-type 0 \
  --option <选项A> --option <选项B> --answer A [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |
| `--type <type>` | 题型：R（单选）、C（多选）、S（评分）、V（投票） |
| `--answer <answer>` | 正确答案 |
| `--name <name>` | 问答卡标题 |
| `--item-type <number>` | 类型：0 答题卡，1 问答 |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `--question-id <id>` | 问答卡 ID；省略表示新建，传入表示编辑 |
| `--option <value...>` | 选项值，可重复提供 |
| `--tip <value...>` | 答案说明，可重复提供 |
| `-f, --force` | 跳过写入确认 |
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 示例

```bash
# 新建单选答题卡
<CLI> qa add-edit -c <频道ID> \
  --name "新品首发到手价是多少？" --type R --item-type 0 \
  --option "299元" --option "399元" --answer A \
  --tip "正确答案是299元" -f -o json

# 编辑已有答题卡
<CLI> qa add-edit -c <频道ID> --question-id gv0uf9s5v7 \
  --name "新品首发到手价是多少？" --type R --item-type 0 \
  --option "299元" --option "399元" --answer A -f -o json
```

> 注意：从 `polyv-live-cli@latest` 1.2.33 起，省略 `--question-id` 可新建答题卡；传入 `--question-id` 表示编辑已有答题卡。

### qa send - 发送问答卡

向指定频道发送一个问答卡（答题卡）。

```bash
<CLI> qa send -c <频道ID> --question-id <问题ID> [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |
| `--question-id <id>` | 问答卡 ID |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `--duration <秒数>` | 答题限时（1-99秒） |
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 示例

```bash
# 发送问答卡
<CLI> qa send -c <频道ID> --question-id gv0uf9s5v7

# 发送带30秒限时
<CLI> qa send -c <频道ID> --question-id gv0uf9s5v7 --duration 30

# JSON 格式输出
<CLI> qa send -c <频道ID> --question-id gv0uf9s5v7 -o json
```

---

### qa list - 查询问答卡列表

获取频道的所有问答卡列表。

```bash
<CLI> qa list -c <频道ID> [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 示例

```bash
# 查询问答卡列表
<CLI> qa list -c <频道ID>

# JSON 格式输出
<CLI> qa list -c <频道ID> -o json
```

#### 表格输出字段

| 字段 | 说明 |
|------|------|
| Question ID | 问答卡 ID |
| Name | 问题名称 |
| Type | 类型：R（单选）、C（多选）、S（评分）、V（投票） |
| Status | 状态：draft（草稿）、send（已发送）、delete（已删除） |
| Times | 发送次数 |

---

### qa stop - 停止问答卡

停止正在进行的问答卡，并获取答题统计结果。

```bash
<CLI> qa stop -c <频道ID> --question-id <问题ID> [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |
| `--question-id <id>` | 问答卡 ID |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 示例

```bash
# 停止问答卡
<CLI> qa stop -c <频道ID> --question-id gv0uf9s5v7

# JSON 格式输出
<CLI> qa stop -c <频道ID> --question-id gv0uf9s5v7 -o json
```

#### 输出信息

停止后会显示答题统计：
- **Correct Answer**: 正确答案
- **Total Respondents**: 答题总人数
- **Correct**: 答对人数
- **Incorrect**: 答错人数
- **Option Distribution**: 各选项选择人数

---

## 问卷命令 (Questionnaire)

问卷用于在直播过程中收集观众反馈。

### questionnaire create - 创建问卷

为指定频道创建一个新问卷。

```bash
<CLI> questionnaire create -c <频道ID> --title <标题> --questions '<JSON数组>' [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |
| `--title <标题>` | 问卷标题 |
| `--questions <json>` | 题目数组（JSON 字符串） |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `--custom-questionnaire-id <id>` | 自定义问卷 ID |
| `--auto-publish-time <时间戳>` | 自动发布时间（时间戳） |
| `--auto-end-time <时间戳>` | 自动结束时间（时间戳） |
| `--privacy-enabled` | 启用隐私模式 |
| `--privacy-content <文本>` | 隐私协议内容 |
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 题目 JSON 格式

```json
[
  {
    "name": "问题内容",
    "type": "R",
    "options": ["选项1", "选项2"],
    "required": "Y",
    "scoreEnabled": "Y",
    "score": 10,
    "answer": "A"
  }
]
```

#### 题目类型

| 类型 | 说明 | 必需字段 |
|------|------|---------|
| `R` | 单选题 | `options` |
| `C` | 多选题 | `options` |
| `Q` | 填空题 | - |
| `J` | 判断题 | - |
| `X` | 评分题 | - |

#### 示例

```bash
# 创建简单问卷（单选题）
<CLI> questionnaire create -c <频道ID> --title "满意度调查" \
  --questions '[{"name":"您的性别?","type":"R","options":["男","女"],"required":"Y"}]'

# 创建带评分题的问卷
<CLI> questionnaire create -c <频道ID> --title "服务评价" \
  --questions '[{"name":"您对我们的服务满意吗?","type":"X","required":"Y"}]'

# 创建带自定义 ID 的问卷
<CLI> questionnaire create -c <频道ID> --title "调查问卷" \
  --questions '[...]' --custom-questionnaire-id "survey-001"

# JSON 格式输出
<CLI> questionnaire create -c <频道ID> --title "调查" \
  --questions '[...]' -o json
```

---

### questionnaire list - 查询问卷列表

查询频道的问卷列表。

```bash
<CLI> questionnaire list -c <频道ID> [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `--page <数字>` | 页码（默认 1） |
| `--size <数字>` | 每页数量（默认 20） |
| `--start-time <时间戳>` | 开始时间戳 |
| `--end-time <时间戳>` | 结束时间戳 |
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 示例

```bash
# 查询问卷列表
<CLI> questionnaire list -c <频道ID>

# 分页查询
<CLI> questionnaire list -c <频道ID> --page 1 --size 20

# 按时间戳范围筛选
<CLI> questionnaire list -c <频道ID> --start-time 1704067200000 --end-time 1706745599000

# JSON 格式输出
<CLI> questionnaire list -c <频道ID> -o json
```

#### 表格输出字段

| 字段 | 说明 |
|------|------|
| Questionnaire ID | 问卷 ID |
| Title | 问卷标题 |
| Last Modified | 最后修改时间 |
| Users | 答题人数 |

---

### questionnaire result-list - 分页查询问卷结果

分页查询频道的问卷答题结果。

```bash
<CLI> questionnaire result-list -c <频道ID> [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `--page <数字>` | 页码（默认 1） |
| `--size <数字>` | 每页数量（默认 20） |
| `--session-id <id>` | 按场次 ID 筛选 |
| `--start-date <日期>` | 开始日期（格式：yyyy-MM-dd） |
| `--end-date <日期>` | 结束日期（格式：yyyy-MM-dd） |
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

> 注意：日期范围默认为最近 7 天。

#### 示例

```bash
# 查询问卷结果
<CLI> questionnaire result-list -c <频道ID>

# 分页查询
<CLI> questionnaire result-list -c <频道ID> --page 1 --size 20

# 按场次筛选
<CLI> questionnaire result-list -c <频道ID> --session-id fwly13xczv

# 按日期范围筛选
<CLI> questionnaire result-list -c <频道ID> --start-date 2024-01-01 --end-date 2024-01-31

# JSON 格式输出
<CLI> questionnaire result-list -c <频道ID> -o json
```

---

### questionnaire detail - 查询问卷详情

获取指定问卷的详细信息，包括题目列表。

```bash
<CLI> questionnaire detail -c <频道ID> --questionnaire-id <问卷ID> [选项]
```

#### 必需选项

| 选项 | 说明 |
|------|------|
| `-c, --channel-id <id>` | 频道 ID |
| `--questionnaire-id <id>` | 问卷 ID |

#### 可选选项

| 选项 | 说明 |
|------|------|
| `-o, --output <格式>` | 输出格式：table（默认）或 json |

#### 示例

```bash
# 查询问卷详情
<CLI> questionnaire detail -c <频道ID> --questionnaire-id fs9v59nq4u

# JSON 格式输出
<CLI> questionnaire detail -c <频道ID> --questionnaire-id fs9v59nq4u -o json
```

#### 输出信息

- **Channel ID**: 频道 ID
- **Questionnaire ID**: 问卷 ID
- **Name**: 问卷名称
- **Status**: 问卷状态
- **Questions**: 题目列表
  - Question ID: 题目 ID
  - Name: 题目内容
  - Type: 题目类型
  - Required: 是否必答
  - Score Enabled: 是否计分

---

## 常见工作流程

### 1. 发起快速答题

```bash
# 1. 查看可用的问答卡
<CLI> qa list -c <频道ID>

# 2. 发送问答卡
<CLI> qa send -c <频道ID> --question-id gv0uf9s5v7 --duration 30

# 3. 停止答题并查看结果
<CLI> qa stop -c <频道ID> --question-id gv0uf9s5v7
```

### 2. 创建并发布问卷

```bash
# 1. 创建问卷
<CLI> questionnaire create -c <频道ID> --title "课后反馈" \
  --questions '[{"name":"课程难度如何?","type":"R","options":["简单","适中","困难"],"required":"Y"}]'

# 2. 查询问卷列表确认创建成功
<CLI> questionnaire list -c <频道ID>

# 3. 查看问卷详情
<CLI> questionnaire detail -c <频道ID> --questionnaire-id <问卷ID>
```

### 3. 查看直播场次问卷统计

```bash
# 按场次查询问卷结果
<CLI> questionnaire result-list -c <频道ID> --session-id <场次ID>

# 导出为 JSON 便于分析
<CLI> questionnaire result-list -c <频道ID> --session-id <场次ID> -o json > survey_results.json
```

---

## 错误处理

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `channelId is required` | 未指定频道 ID | 使用 `-c` 参数指定频道 |
| `questionId is required` | 发送、停止、删除、发布结果或编辑已有问答卡时未指定问答卡 ID；新建问答卡应省略该参数 | 对已有问答卡操作时使用 `--question-id` 参数 |
| `questionnaireId is required` | 未指定问卷 ID | 使用 `--questionnaire-id` 参数 |
| `title is required` | 未指定问卷标题 | 使用 `--title` 参数 |
| `questions is required` | 未提供题目数组 | 使用 `--questions` 参数 |
| `Invalid JSON format for questions` | 题目 JSON 格式错误 | 检查 JSON 格式是否正确 |
| `duration must be between 1 and 99` | 答题时长超出范围 | 设置 1-99 之间的值 |
| `Invalid startDate format` | 日期格式错误 | 使用 yyyy-MM-dd 格式 |

---

## API 参考

相关 API 文档：
- [发送答题卡](https://help.polyv.net/#/live/v4/api/interact/question/send)
- [查询答题卡列表](https://help.polyv.net/#/live/v3/api/interact/question/list)
- [停止答题卡](https://help.polyv.net/#/live/v4/api/interact/question/stop)
- [创建问卷](https://help.polyv.net/#/live/v4/api/interact/questionnaire/save)
- [查询问卷列表](https://help.polyv.net/#/live/v3/api/interact/questionnaire/list)
- [查询问卷详情](https://help.polyv.net/#/live/v3/api/interact/questionnaire/detail)
