---
name: management-dashboard
description: >-
  管理驾驶舱技能：基于录音 AI 总结内容，生成管理者日报 HTML 报表。
  通过分页接口获取录音的 ai_summary_content，使用 LLM 分析生成包含团队资产、外勤效能、
  合规监控、RM 排行、线索转化、管理建议六大板块的可视化报表。
  MUST resolve agentId via session_status (sessionKey=current) before APIs.
  MUST run main.py as the only entry point; empty contents still generates HTML report.
  Use for 系统驾驶舱、管理驾驶舱、日报生成、管理者报表、团队分析。
disable-model-invocation: false
---

# 管理驾驶舱 · 管理者日报生成

## 硬性约束（必守）

本技能**只做「录音 AI 总结内容」的管理分析与报表生成**，数据源**唯一**为录音服务返回的 `ai_summary_content` 字段，**不是**当前对话里的文字、也不是 Agent 臆测。

| 禁止 | 必须 |
|------|------|
| 未执行分页接口拉取数据就向用户输出「分析/报表」 | **先** `session_status` → **再** 调用 **`main.py`** 完整流程 → 返回文件路径 |
| 数据为空时编造指标或调用 LLM 臆测 | `contents` 为空时**仍生成 HTML**，使用空结果（指标为 0），**不调用 LLM** |
| 仅凭用户当轮聊天内容编造分析 | 报表内容须由 LLM 基于 **AI 总结内容** 生成（有数据时） |
| 一次性加载所有数据到内存 | 使用分页接口（每页 20 条），循环获取直到 `completed=true` |
| **向用户返回包含 `agentId` 的信息** | `agentId` 仅用于接口调用，**禁止**出现在任何用户可见的回复中 |
| **使用历史数据或自行编造数据进行分析** | 分析必须严格基于**本次分页调用返回的 `contents` 数据**，禁止引用历史数据或编造数据 |

**完成前不得结束任务**：完成 **步骤 1（session_status）→ 2（main.py）→ 3（返回文件路径）**。`contents` 为空时 `main.py` 仍须生成 HTML，**禁止**提前结束。

## 目标

1. **直接调用宿主「当前会话」查询**（OpenClaw：`session_status`，`sessionKey="current"`），从返回的 `agentId` 获取 **agentId**。
2. 调用录音服务 **`POST /api/recordings/asr-completed/page`**，以 **`agentId`** 分页拉取 AI 总结内容。
3. **使用 LLM 分析所有 AI 总结**：生成包含六大板块的管理驾驶舱数据。
4. 生成适配手机/PC 的 **HTML 报表**，保存到 skill 目录下的 `reports/` 子目录。
5. 向用户返回 **生成的文件路径**。

**常见触发说法**：`系统驾驶舱`、`system dashboard`（中英文均可触发）。

## LegionClaw 运行约定

- **会话形态**：`agent:<agentid>:<渠道>:<用户 id>`；渠道为空时为三段 `agent:<agentid>:<用户 id>`（无 `::`）。
- **执行位置**：`curl` 与 Python 脚本须在 **LegionClaw 任务运行环境**执行；环境需能访问录音服务（见下文接口）。
- **成功判定**：HTTP 2xx 且响应 JSON **`code === 0`**（数值零）。
- **零条数据**：`contents` 为空数组时，**仍生成 HTML 空报表**（各指标为 0），并返回文件路径。

### 请求体参数

| 字段 | 必填 | 格式 | 说明 |
|------|------|------|------|
| `agentId` | **是** | 字符串 | 取会话标识解析出的 **agentId** |
| `uuid` | **是** | 字符串 | 分页标识，首次请求生成，后续请求复用 |
| `startTime` | 条件必填 | **`YYYY-MM-DD HH:mm:ss`** | 统计窗口起始时间，由用户话术换算 |
| `endTime` | 条件必填 | **`YYYY-MM-DD HH:mm:ss`** | 统计窗口结束时间 |

- 用户**未明确**查询时间范围：**固定按「近一周」** 换算并传入 `startTime` / `endTime`（`endTime` = 当前时间，`startTime` = 当前时间 − 7 天）。
- 用户**明确说了**范围（如「近三天」「上周」「6 月 1 日到 6 月 4 日」）：按话术换算为 **`YYYY-MM-DD HH:mm:ss`** 后传入。
- 每次请求应同时包含 **`agentId`、`uuid`、`startTime`、`endTime`** 四个字段。

```json
{
  "agentId": "<agentid>",
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "startTime": "2026-06-07 00:00:00",
  "endTime": "2026-06-08 23:59:59"
}
```

### 从用户话术换算时间（Agent 必做）

在运行环境用**当前时间**作 `endTime`（除非用户明确指定结束时间）。`startTime` = 结束时间往前推对应天数。

| 用户说法（示例） | startTime | endTime |
|------------------|-----------|---------|
| **未说明时间（默认）** | 当前时间 − 7 天 | 当前时间 |
| 近1小时 / 最近1小时 | 当前时间 − 1 小时 | 当前时间 |
| 近N小时 / 最近 N 小时 | 当前时间 − N 小时 | 当前时间 |
| 近三天 / 最近 3 天 | 当前时间 − 3 天 | 当前时间 |
| 近一周 / 最近 7 天 | 当前时间 − 7 天 | 当前时间 |
| 今天 | 今天 00:00:00 | 今天 23:59:59 |
| 昨天 | 昨天 00:00:00 | 昨天 23:59:59 |
| 指定区间「6 月 1 日到 6 月 4 日」 | `2026-06-01 00:00:00` | `2026-06-04 23:59:59` |

### 成功响应（示例结构）

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "userId": "<userid>",
    "orgId": "<orgid>",
    "startTime": "2026-05-07T00:00:00",
    "endTime": "2026-06-08T23:59:59",
    "isAdmin": true,
    "contents": [
      {
        "aiSummaryContent": "# **会议纪要**\n\n## 会议总结\n\n本次会议...",
        "email": null,
        "memberName": null,
        "mobile": null,
        "orgId": null,
        "orgName": null,
        "userId": "e7a9123e12c54f06bf75a1e931beef87",
        "userName": "17639418027"
      },
      {
        "aiSummaryContent": "# **会议纪要**\n\n## 会议总结\n\n本次会议...",
        "userId": "d8db9fe5eb1a4880bc57dd7852edeb08",
        "userName": "18762097213"
      }
    ],
    "currentPage": 1,
    "pageSize": 20,
    "total": 45,
    "totalPages": 3,
    "completed": false
  }
}
```

**关键字段**：

| 字段 | 说明 |
|------|------|
| `data.contents` | 当前页的 AI 总结内容数组，每项为对象，包含 `aiSummaryContent`（AI 总结文本）和 `userName`（成员姓名） |
| `data.contents[].aiSummaryContent` | 单条记录的 AI 总结内容文本，用于分析 |
| `data.contents[].userName` | 成员姓名，用于第三模块 RM 评分统计 |
| `data.completed` | **是否查询完成**：`false` 表示还有数据，需继续请求下一页；`true` 表示所有数据已获取 |
| `data.currentPage` | 当前页码 |
| `data.totalPages` | 总页数 |

**分页逻辑**：
1. 首次请求：生成新的 `uuid`，发送请求
2. 检查 `data.completed`：
   - 若为 `false`：**使用相同的 `uuid`** 再次请求，获取下一页
   - 若为 `true`：所有数据已获取完毕，停止分页
3. 累积所有页的 `contents` 到同一个数组

### 用户回复规范

**接口失败**（`code` 非 0、网络错误）：正文一行 + 可选收尾提问。禁止过程描述。

- `code` 为 **4001 / 5001**：正文取接口 **`msg`**
- 其他失败：取 `msg`，无则用「暂未获取到数据」

**接口成功但 `contents` 为空**（`code=0`）：**禁止**回复「暂无可统计数据」「未查到录音数据」等而不生成报表。**必须**执行 `main.py` 生成空报表，按下方「零条数据」示例返回文件路径。

## agentId 自动获取（必做 · 直接查当前会话）

**必须先调用宿主「当前会话」查询 agentId，再拉数。** 不得在未调用**步骤 1** 前回复「无法获取语音数据」。

### 禁止行为

| 禁止 | 正确做法 |
|------|----------|
| 首句就向用户索要 agentId | **先**调 `session_status`（`sessionKey="current"`） |
| 未调会话工具就声称「当前对话没有 agentId」 | 用 **当前会话查询** 获取 agentId |
| 向用户展示完整会话串 | 只说明「已根据当前 LegionClaw 会话解析 agentId」 |

### 获取步骤（按序执行）

**步骤 0 — 用户消息已带 agentId**

- 用户明确给出 agentId → 直接采用，可跳过步骤 1。

**步骤 1 — 当前会话查询（主路径，必须执行）**

在 **LegionClaw / OpenClaw 宿主**上调用内置会话工具：

| 项 | 值 |
|----|-----|
| 工具 | `session_status` |
| 参数 | `sessionKey`: **`"current"`** |

**Agent 操作说明：**

1. 调用 **`session_status`**，传入 **`sessionKey="current"`**。
2. 从返回 JSON 中读取 **`agentId`** 字段。
3. 校验 `agentId` 非空后，再执行分页请求。

**步骤 2 — 仍为空（仅此情况可索要）**

```markdown
已调用当前会话查询（session_status current），仍无法获取 agentId。
请确认本任务是否绑定当前 LegionClaw 会话，或直接提供 **agentId**。
```

### 执行前自检

- [ ] 已调用 **`session_status` + `sessionKey="current"`**
- [ ] 已从返回的 **`agentId`** 字段得到非空值
- [ ] 已生成分页用的 `uuid`
- [ ] 已执行**分页 curl** 获取所有 `contents`，未仅凭对话生成分析
- [ ] 无论 `contents` 是否为空，均完成 HTML 生成并返回文件路径

## 分析方式（核心）

**只分析接口返回的 AI 总结内容**，生成管理驾驶舱报表。

| 场景 | Agent 怎么做 |
|------|--------------|
| **数据为空** | 跳过 LLM，用空结果（指标为 0）生成 HTML，返回文件路径 |
| **数据非空** | 调用 LLM 分析所有 AI 总结，生成六大板块数据，再生成 HTML |

### LLM 分析（步骤 6 · 必做）

1. 将所有 `contents` 中的 `aiSummaryContent` 按发言人 `userName` 合并为一个大文本。
2. 调用 LLM，使用步骤 6 中的 prompt 模板。
3. 解析 LLM 返回的 JSON，验证所有必需字段存在。

## 执行步骤

1. **【必做】** 调用 **`session_status`（`sessionKey="current"`）** 获取 **agentId**；不得跳过。

2. **【必做 · 唯一入口】** 调用 **`main.py`** 完成拉数、分析、生成 HTML（空数据也会生成空报表）：

```bash
python3 skills/management-dashboard/main.py "${USER_INPUT}" "${AGENTID}"
```

工作目录为技能目录时：

```bash
python3 main.py "${USER_INPUT}" "${AGENTID}"
```

3. **解析 `main.py` 输出**（取最后一行 JSON）：
   - **`success: true`**：向用户返回 `message` 与 **`file_path`**（无论 `data_count` 是否为 0）
   - **`success: false`**：仅返回 `message`（接口错误，不生成 HTML）

4. **按 [用户回复规范](#用户回复规范) 返回结果**。

> **禁止**跳过 `main.py` 自行 curl 后在空数据时文字回复；

---

<details>
<summary>附录：手动 curl 分页（仅供调试，Agent 勿用此路径替代 main.py）</summary>

1. 根据用户对话换算时间（见上表）。
2. 分页拉取录音数据：

```bash
# 生成 UUID
UUID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

# 从 config.py 读取 API 地址
API_BASE_URL=$(python3 -c "import sys; sys.path.insert(0, 'skills/management-dashboard'); from config import API_BASE_URL; print(API_BASE_URL)")

# 首次请求
END_TIME=$(date "+%Y-%m-%d %H:%M:%S")
START_TIME=$(date -v-1d "+%Y-%m-%d %H:%M:%S")  # macOS; Linux: date -d '1 day ago'

curl -sS -X POST "${API_BASE_URL}/api/recordings/asr-completed/page" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"agentId\":\"${AGENTID}\",\"uuid\":\"${UUID}\",\"startTime\":\"${START_TIME}\",\"endTime\":\"${END_TIME}\"}" \
  -o /tmp/dashboard_page_1.json

# 检查 completed 字段
COMPLETED=$(python3 -c "import json; d=json.load(open('/tmp/dashboard_page_1.json')); print(d['data']['completed'])")

# 若 completed=false，继续请求下一页（使用相同的 UUID）
PAGE=2
while [ "$COMPLETED" = "False" ] || [ "$COMPLETED" = "false" ]; do
  curl -sS -X POST "${API_BASE_URL}/api/recordings/asr-completed/page" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"agentId\":\"${AGENTID}\",\"uuid\":\"${UUID}\",\"startTime\":\"${START_TIME}\",\"endTime\":\"${END_TIME}\"}" \
    -o "/tmp/dashboard_page_${PAGE}.json"
  
  COMPLETED=$(python3 -c "import json; d=json.load(open('/tmp/dashboard_page_${PAGE}.json')); print(d['data']['completed'])")
  PAGE=$((PAGE + 1))
done
```

4. **合并所有页的 contents** 并检查是否为空：

```bash
python3 -c "
import json, glob

all_contents = []
for f in sorted(glob.glob('/tmp/dashboard_page_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    contents = (d.get('data') or {}).get('contents') or []
    
    # 新格式：contents 为对象数组，提取 aiSummaryContent 和 userName
    for item in contents:
        if isinstance(item, dict):
            all_contents.append({
                'aiSummaryContent': item.get('aiSummaryContent', ''),
                'userName': item.get('userName') or item.get('memberName') or '',
                'userId': item.get('userId', ''),
            })
        else:
            # 兼容旧格式：纯字符串
            all_contents.append({
                'aiSummaryContent': str(item),
                'userName': '',
                'userId': '',
            })

print(f'total_contents={len(all_contents)}')

# 保存到文件供后续使用（空数组也保存）
json.dump(all_contents, open('/tmp/dashboard_all_contents.json', 'w', encoding='utf-8'), ensure_ascii=False)
"
```

5. **若 `contents` 条数为 0**：跳过 LLM，使用空分析结果，**继续生成 HTML**（见步骤 6～7）。

6. **调用 LLM 分析**（`contents` 非空时必做；为空时跳过）→ 保存分析结果为 `/tmp/dashboard_analysis.json`。

使用以下 prompt 模板（注意：使用 `aiSummaryContent` 字段进行分析，使用 `userName` 字段进行成员评分）：

```
你是一个专业的销售团队管理分析师。请分析以下录音 AI 总结内容，生成管理驾驶舱报表数据。

团队：{team_name}
日期：{date_str}
成员分组统计：{user_groups_str}

【重要规则】
- **数据来源唯一性**：所有分析必须严格基于下方「录音内容」中的 AI 总结文本，禁止使用历史数据、外部数据或自行编造数据。
- **成员姓名**：必须严格使用上方「成员分组统计」中列出的姓名，禁止虚构、编造或使用 userId/数字ID 作为姓名。
- **无法识别时跳过**：如果录音内容中无法识别到具体成员姓名或关键信息，不要猜测，直接跳过该条记录的分析。
- **top_performers 和 needs_improvement**：其中的 name 字段必须是成员分组统计中存在的姓名。
- **数值必须来自原文**：所有统计数据（客户数、录音时长、拜访次数等）必须从录音 AI 总结内容中提取，禁止凭空编造。如果原文中未提及某项数据，返回 0 或空值。

录音内容（每条记录包含发言人信息）：
{combined_contents}

请从以下维度进行分析，并以 JSON 格式返回：

1. **团队资产沉淀大盘**（长期累积维度）
   - total_customers: 历史累积拜访客户总量（整数）
   - month_customers: 本月至今累积拜访（整数）
   - today_customers: 今日新增实地拜访（整数）
   - avg_per_person: 人均长期维护客群深度（整数）

2. **每日外勤实地效能监测**
   - total_recording_minutes: 今日双向有效录音总时长（分钟，整数）
   - avg_minutes_per_person: 人均日面谈时长（分钟，浮点数）
   - total_visits: 今日实地有效面谈总数（整数）
   - avg_visits_per_person: 人均日均实地探店次数（浮点数）
   - customer_distribution: 客群结构分布
     * old_customer_maintenance: 老客维护与转介绍（整数）
     * new_customer_prospecting: 陌生新商圈扫街（整数）
   - regional_distribution: 产业带轨迹分布（数组，每项包含 region 和 visit_count）

3. **当日合规与红线监控**
   - compliance_metrics: 合规指标数组，每项包含：
     * metric_name: 监控指标名称
     * achievement_rate: 达成率（百分比字符串，如 "100%"）
     * status: 状态（"正常" / "警告" / "危险"）
     * ai_audit_opinion: AI 每日穿透审计意见

4. **当日 RM 业务水平排行**
   - top_performers: 优秀 RM 数组（最多3名），每项包含：
     * rank: 排名（1, 2, 3）
     * region: 片区
     * name: 姓名
     * score: 得分（百分制）
     * behavior_description: 销冠/高水平行为描述
   - needs_improvement: 待提升 RM 数组，每项包含：
     * region: 片区
     * name: 姓名
     * score: 得分
     * problem_diagnosis: 问题诊断
   - user_scores: 按成员分组统计得分（数组），每项包含：
     * user_name: 成员姓名（必须与上方成员分组统计中的姓名一致）
     * total_score: 总分
     * avg_score: 平均分
     * recording_count: 录音条数（必须与上方成员分组统计中的条数一致）
     * top_score: 最高分
     * min_score: 最低分

5. **当日线索转化效率**
   - lead_conversion:
     * a_level_count: A 级商机数量
     * a_level_details: A 级详情描述
     * b_level_count: B 级商机数量
     * b_level_followup: B 级跟进建议
     * c_level_count: C 级商机数量
     * c_level_interception: C 级 AI 拦截核查

6. **管理者跟进与靶向督导建议**
   - management_suggestions: 建议数组，每项包含：
     * title: 建议标题
     * content: 建议内容

请确保返回的是合法的 JSON 格式，不要包含其他文字说明。
```

</details>

### 回复示例

**接口错误（4001 / 5001）**

```markdown
当前用户非管理员，拒绝执行

请问您是否需要我们协助联系管理员开通权限？
```

**零条数据（仍生成报表）**

```markdown
已根据 2026-06-23 13:16:00 至 2026-06-23 14:16:00 生成管理驾驶舱报告（当前查询周期暂无录音数据）。

报表已保存至：`skills/management-dashboard/reports/系统驾驶舱报告_2026-06-23.html`

<!-- 请问您是否希望扩大时间范围后重新查询？ -->
```

**成功生成报表**

```markdown
已根据 2026-06-07 00:00:00 至 2026-06-14 23:59:59（近一周）的 45 条录音 AI 总结，生成管理驾驶舱报告。

报表已保存至：`skills/management-dashboard/reports/系统驾驶舱报告_2026-06-07_06-14.html`
```

## 文件结构

```
management-dashboard-skill/
├── SKILL.md                    # 本文件
├── main.py                     # 主逻辑入口
├── analyzer.py                 # LLM 分析模块
├── html_generator.py           # HTML 生成器
├── utils.py                    # 工具函数
├── config.py                   # 配置文件
├── requirements.txt            # Python 依赖
├── reports/                    # 报表输出目录（自动创建）
└── README.md                   # 说明文档
```

## 配置说明

所有配置集中在 `config.py` 文件中，修改该文件即可：

```python
# API 配置（唯一配置位置，其他文档引用此文件）
API_BASE_URL = os.getenv('API_BASE_URL', 'http://your-api-server:port')
API_ENDPOINT = '/api/recordings/asr-completed/page'

# 分页配置
DEFAULT_PAGE_SIZE = 20
DEFAULT_DAYS = 7  # 默认查询最近 7 天（一周）
```

如需修改 API 地址，请直接编辑 `config.py` 文件中的 `API_BASE_URL`。

## 文件编码规范（必守 · 全平台展示）

生成的报表须在 **iOS / Android / iPad / PC / 微信小程序 WebView** 上正确显示中文，**统一使用 UTF-8**：

| 文件类型 | 编码 | 说明 |
|----------|------|------|
| **HTML 报表** | **UTF-8 with BOM**（`utf-8-sig`） | 写入时带 BOM，避免 Android/小程序按 GBK 误解析导致乱码 |
| **JSON 中间文件** | **UTF-8**（无 BOM） | `json.dump(..., ensure_ascii=False)` 保留中文 |
| **接口响应** | **UTF-8** | `curl` 保存 JSON 时用 `encoding='utf-8'` 读取 |

**HTML 头部必须包含**（`html_generator.py` 已内置，禁止删除）：

```html
<meta charset="UTF-8">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
```

**写入 HTML 时必须**调用 `utils.write_html_file()` 或等价地使用：

```python
with open(path, 'w', encoding='utf-8-sig', newline='\n') as f:
    f.write(html)
```

**禁止**：使用系统默认编码、`gbk`/`gb2312`、或不指定 `encoding` 参数写文件。

若报表通过 HTTP 服务访问，服务端响应头须包含：`Content-Type: text/html; charset=utf-8`。

## 注意事项

1. **LLM 调用**：需要在 `main.py` 的 `_get_llm_client()` 方法中实现实际的 OpenClaw LLM 调用逻辑。
2. **API 地址**：确保 `config.py` 中的 `API_BASE_URL` 配置正确。
3. **输出目录**：`reports/` 目录会自动创建，无需手动配置。
4. **网络访问**：Skill 需要访问录音查询 API，确保网络连通。
5. **分页逻辑**：必须使用相同的 `uuid` 进行分页请求，直到 `completed=true`。
6. **文件编码**：严格遵守上文「文件编码规范」，HTML 必须用 `utf-8-sig` 写入。

## 故障排查

### 问题：接口调用失败

**解决**：检查 `config.py` 中的 `API_BASE_URL` 是否正确，确保 API 服务正常运行。

### 问题：LLM 返回空结果

**解决**：检查 `main.py` 中的 `_get_llm_client()` 实现，确保 OpenClaw LLM 调用正常。

### 问题：数据为空但未生成报表

**解决**：检查 `main.py` 是否在 `contents` 为空时提前 `return`；空数据应继续走 `analyzer._empty_result()` 和 HTML 生成。
