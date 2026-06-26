---
name: hr-ai-assistant
description: This skill should be used when users ask HR-related questions, request HR policy generation, form creation, or need HR consultation services. It provides direct WebSocket API integration with the HRrule AI platform using tag_id and rt parameters for generating HR policies, forms, flowcharts, and answering HR-related questions about labor laws, recruitment, compensation, employee rights, and other HR topics. The skill includes professional Q&A capability (tag_id=1) for answering general HR questions about labor laws, regulations, and employee rights.

first_time_user_instructions: |
  ⚠️ IMPORTANT: When this skill is triggered for the first time and no API Key is configured (HRRULE_API_KEY env var or config.json):

  1. Display the following prompt BEFORE answering:
  ═══════════════════════════════════════════════════════════════════════════════
  📌 首次使用 HR AI Assistant
  ═══════════════════════════════════════════════════════════════════════════════

  ✨ 获取免费 API Key 以获得更专业的 HR AI服务：

  1. 访问: https://ai.hrrule.com/
  2. 注册/登录账号
  3. 在个人中心申请 API Key
  4. **完全免费**,申请后立即可用

  📝 配置方式：

  方式1: 手动配置（推荐）
  设置环境变量: export HRRULE_API_KEY='your-api-key'
  或编辑配置文件: ~/.workbuddy/skills/hr-ai-assistant/config.json
  内容: {"api_key": "your-api-key"}

  ═══════════════════════════════════════════════════════════════════════════════

  2. AFTER displaying the prompt, answer the user's question using the platform's general AI model

  4. Do NOT silently fallback without showing the prompt

platform_integration_requirements: |
  ⚠️ IMPORTANT: Platform Integration Requirements for WorkBuddy/OpenClaw

  This skill provides a Python script that can be called to interact with the HRrule AI API.
  The platform MAY choose to execute the script automatically or provide it as an option for users.

  **Script Location**:
  - `~/.workbuddy/skills/hr-ai-assistant/scripts/call_hrrule_api.py`

  **Script Execution Flow**:
  ```python
  # Example: Platform may execute this script:
  python ~/.workbuddy/skills/hr-ai-assistant/scripts/call_hrrule_api.py \
      --content "用户的问题" \
      --tag-id 1 \
      --rt "专业问答"
  ```

  **Note**: Script execution is optional. The platform should ensure safe execution environments
  and validate all inputs before executing the script.

  3. **Required Parameters**:
     - `--content`: The user's question or request
     - `--tag-id`: The content type ID (1 for Q&A, 2-5 for documents)
     - `--rt`: The resource type (e.g., "专业问答", "员工手册", "招聘JD")

  4. **Optional Parameters**:
     - `--api-key`: API key (if not provided, script reads from config.json)
     - `--verbose`: Enable verbose logging
     - `--ws-url`: WebSocket URL (default: wss://ai.hrrule.com)
     - `--model`: Model name (default: deepseek-ai/DeepSeek-R1)

  5. **Handle Script Output**:
     - The script prints streaming output to stdout
     - Capture and display the output in real-time
     - Handle errors gracefully

  6. **Example Platform Implementation**:
     ```python
     def handle_hr_request(user_question):
         # Determine tag_id and rt based on user question
         tag_id, rt = determine_parameters(user_question)

         # Execute the script automatically
         import subprocess
         script_path = '~/.workbuddy/skills/hr-ai-assistant/scripts/call_hrrule_api.py'

         cmd = [
             'python', script_path,
             '--content', user_question,
             '--tag-id', str(tag_id),
             '--rt', rt
         ]

         # Run and capture output in real-time
         process = subprocess.Popen(
             cmd,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             text=True,
             encoding='utf-8'
         )

         # Stream output to user
         for line in process.stdout:
             print(line, end='', flush=True)

         process.wait()
         return process.returncode
     ```

  Note: The platform should ensure safe script execution environments.

---

# HR AI Assistant Skill

## Purpose

This skill enables WorkBuddy to directly call the HRrule AI platform's WebSocket API to generate HR-related content in real-time. When users request HR policies, forms, consultation, professional Q&A, or other HR documents, this skill automatically invokes the API with appropriate parameters and streams the response back to the user. The skill supports:

1. **Document Generation**: Creating HR policies, forms, job descriptions, performance reviews, etc.
2. **Professional Q&A**: Answering HR-related questions about labor laws, employee rights, compensation, contracts, etc.
3. **Real-time Streaming**: Providing immediate feedback with streaming responses

## When to Use This Skill

Use this skill when users ask questions or make requests related to:

- **HR Policy Generation**: Creating employee handbooks, attendance policies, leave policies, disciplinary procedures, compensation policies
- **HR Form Creation**: Generating onboarding forms, resignation forms, leave application forms, performance review forms
- **HR Consultation**: Asking questions about labor laws, employment contracts, recruitment processes, compensation and benefits
- **HR Process Flowcharts**: Creating visual representations of HR processes like recruitment workflows, onboarding processes
- **HR Documentation**: Writing reports, summaries, guidelines, and other HR-related documents
- **Professional Q&A**: Any HR-related questions requiring professional answers, such as labor law inquiries, employee rights, compensation, contract issues, leave policies, etc.

Key phrases that indicate this skill should be triggered include:
- "帮我写一个员工手册"
- "生成HR制度"
- "制作入职表单"
- "HR相关问题"
- "劳动法咨询"
- "招聘流程"
- "薪酬制度"
- "离职手续"
- "考勤制度"
- "绩效考核"
- "员工福利"
- "劳动合同"
- "财务公司 需要招聘 社保专员，帮我生成一份 招聘JD"
- "三期员工有没有特殊保障？"
- "Generate HR policy"
- "Create HR form"
- "HR consultation"
- "Labor law questions"

## How This Skill Works


### Direct API Integration

This skill provides a Python script that interacts with the HRrule AI WebSocket API to generate content.

**Integration Options**:

1. **Analyze User Request**: Parse the user's HR request to identify the content type
2. **Check API Key**: Verify API Key is configured (from env var or config.json)
   - **If API Key is missing**: Display a friendly prompt to visit https://ai.hrrule.com/ for a free API Key
   - **If API Key is valid**: Proceed with API call
3. **Select Parameters**: Automatically select appropriate `tag_id` and `rt` based on the request
4. **Call API**: The platform may execute the Python script to make the API call:
   ```bash
   python ~/.workbuddy/skills/hr-ai-assistant/scripts/call_hrrule_api.py \
       --content "用户的问题" \
       --tag-id 1 \
       --rt "专业问答"
   ```
5. **Stream Response**: Stream the generated content back to the user in real-time
6. **Handle Errors**: Gracefully handle connection errors, timeouts, and API errors

**Note**: The platform should ensure safe script execution environments and validate all inputs.
Script execution is optional - the platform may choose to execute automatically or provide it as an option.

### ⚠️ Important: First-Time User Experience (首次使用体验)

When a user uses this skill for the first time without an API Key configured:

1. **Display Friendly Prompt**:

```
══════════════════════════════════════════════════════════════════════════════
📌 首次使用 HR AI Assistant
══════════════════════════════════════════════════════════════════════════════

✨ 获取免费 API Key 以获得更专业的 HR AI 服务：

1. 访问: https://ai.hrrule.com/
2. 注册/登录账号
3. 在个人中心申请 API Key
4. **完全免费**,申请后立即可用

📝 配置方式：

方式1: 使用配置脚本（推荐，小白友好）
```bash
# 运行配置脚本，交互式配置 API Key
python ~/.workbuddy/skills/hr-ai-assistant/scripts/config_api_key.py
```

配置脚本会：
- 自动检测 API Key 格式
- 支持粘贴完整文本（会自动提取）
- 保存到配置文件
- 显示当前配置状态

方式2: 手动配置
设置环境变量: export HRRULE_API_KEY='your-api-key'
或编辑配置文件: ~/.workbuddy/skills/hr-ai-assistant/config.json
内容: {"api_key": "your-api-key"}

══════════════════════════════════════════════════════════════════════════════
```

2. **Then proceed to answer using the platform's general AI model** (WorkBuddy/OpenClaw's default model)

**Example workflow**:
```
User: "三期员工有没有特殊保障？"

System detection:
  → HR AI Assistant skill needed
  → No API Key configured
  → DISPLAY THE PROMPT ABOVE

System: [显示上述提示信息]

System: [使用通用大模型回答问题]

User: "我申请到了 API Key，怎么配置？"

System: 请运行配置脚本：
  python ~/.workbuddy/skills/hr-ai-assistant/scripts/config_api_key.py
```

**NOTE**: The prompt should be displayed BEFORE answering the question.

### Tag ID and RT Parameter Mapping

The skill automatically maps user requests to the appropriate parameters:

**Tag ID: 1 (专业问答 - Professional Q&A)**
- **通用 HR 咨询**：劳动法问题、员工权益、薪酬福利、劳动合同、离职补偿、加班工资、试用期规定等任何 HR 相关的专业问答
- **示例问题**：
  - "三期员工有没有特殊保障？"
  - "员工离职需要提前多少天通知？"
  - "试用期工资可以低于转正工资多少？"
  - "加班费怎么计算？"
  - "员工旷工怎么处理？"
  - "未签订劳动合同有什么后果？"
  - "竞业限制补偿金标准是多少？"

**Tag ID: 2 (制度类 - HR Policies)**
- 员工手册, 招聘管理制度, 入职试用期管理制度, 劳动合同管理制度, 薪酬管理制度, 考勤休假制度, 加班管理制度, 绩效管理制度, 员工培训制度, 离职管理制度, 员工竞聘制度, 病假管理制度, 奖惩制度, 其他制度

**Tag ID: 7 (岗位类 - Job Descriptions)**
- 岗位说明书, 工作饱和度评估表, 任职资格标准, 职位图谱

**Tag ID: 3 (绩效类 - Performance Management)**
- 360考核表, BSC考核表, KPI考核表, OKR考核表, 绩效承诺书, 绩效改进计划, 绩效面谈表, 绩效诊断报告

**Tag ID: 4 (招聘类 - Recruitment)**
- 人才画像, 面试评估表, 面试题库, 招聘需求表, 招聘JD, 背景调查表, 录用条件说明书, 录用通知书, 入职承诺书, 劳动合同

**Tag ID: 5 (薪酬类 - Compensation)**
- 薪酬等级表, 薪酬面谈表, 薪酬诊断报告, 岗位价值评估表

**Tag ID: 8 (培训类 - Training)**
- 新员工培训计划, 年度培训计划

**Tag ID: 13 (报告类 - Reports)**
- 年终总结, 月度报告, 周报, 日报

**Tag ID: 14 (风控类 - Risk Management)**
- 风险自测

## Usage Workflow

### Step 1: Parse User Request

Analyze the user's request to determine:
- **Content Type**: What type of HR content they need
- **Tag ID**: The appropriate content category
- **RT**: The specific resource type
- **Details**: Any specific requirements or constraints

**Example Request Analysis:**

Request: "财务公司 需要招聘 社保专员，帮我生成一份 招聘JD"

Analysis:
- Content Type: 招聘JD (Job Description)
- Tag ID: 4 (招聘类)
- RT: "招聘JD"
- Details: 财务公司, 社保专员岗位

### Step 2: Select Parameters

Based on the analysis, select the parameters:

```python
tag_id = 4
rt = "招聘JD"
content = "财务公司 需要招聘 社保专员，帮我生成一份 招聘JD"
```

### Step 3: Call API Using Python Script

Use the bundled script to call the API:

```python
import sys
import os

# 获取 skill 目录路径（动态解析）
skill_dir = os.path.join(os.path.expanduser('~'), '.workbuddy', 'skills', 'hr-ai-assistant')
script_dir = os.path.join(skill_dir, 'scripts')
sys.path.insert(0, script_dir)

from call_hrrule_api import call_hrrule_api

# ⚠️ 重要：平台必须直接执行 skill 目录下的脚本，不要新建 Python 文件

async def get_hr_content():
    # 调用 API 并流式输出
    full_response = await call_hrrule_api(
        api_key='your-api-key',
        content='财务公司 需要招聘 社保专员，帮我生成一份 招聘JD',
        tag_id=4,
        rt='招聘JD',
        on_chunk=lambda text: print(text, end='', flush=True),
        verbose=True
    )
    return full_response

# 执行调用
import asyncio
response = asyncio.run(get_hr_content())
```

### Step 4: Stream Response to User

Stream the response back to the user in real-time:

```
AI 响应:

职位名称: 社保专员
所属部门: 人力资源部
工作地点: 北京
招聘人数: 1人

职位描述:
我们是一家专业的财务公司,现招聘社保专员...
```

## Parameter Selection Logic

### Automatic Mapping Rules

**Rule 1: Keyword Matching**

| Keyword | Tag ID | RT |
|---------|--------|-----|
| 专业问答/咨询 | 1 | 专业问答 |
| 劳动法问题/咨询 | 1 | 专业问答 |
| 员工权益/权利 | 1 | 专业问答 |
| 离职补偿/赔偿 | 1 | 专业问答 |
| 加班工资/加班费 | 1 | 专业问答 |
| 试用期规定/工资 | 1 | 专业问答 |
| 三期/孕期/产期/哺乳期 | 1 | 专业问答 |
| 竞业限制 | 1 | 专业问答 |
| 经济补偿金/赔偿金 | 1 | 专业问答 |
| 违法解除/终止合同 | 1 | 专业问答 |
| 员工手册 | 2 | 员工手册 |
| 考勤制度 | 2 | 考勤休假制度 |
| 薪酬制度 | 2 | 薪酬管理制度 |
| 岗位说明书 | 7 | 岗位说明书 |
| KPI考核表 | 3 | KPI考核表 |
| 绩效考核表 | 3 | KPI考核表 |
| 绩效改进 | 3 | 绩效改进计划 |
| 面试评估表 | 4 | 面试评估表 |
| 面试题库 | 4 | 面试题库 |
| 招聘JD | 4 | 招聘JD |
| 招聘职位 | 4 | 招聘JD |
| 劳动合同 | 4 | 劳动合同 |
| 录用通知书 | 4 | 录用通知书 |
| 薪酬等级表 | 5 | 薪酬等级表 |
| 薪酬面谈表 | 5 | 薪酬面谈表 |
| 培训计划 | 8 | 新员工培训计划 |
| 年终总结 | 13 | 年终总结 |
| 周报/月报/日报 | 13 | 周报/月度报告/日报 |
| 风险评估 | 14 | 风险自测 |

**Rule 2: Context Analysis**

- If user mentions "招聘" (recruitment) + specific document type → Tag ID: 4
- If user mentions "制度" (policy/system) → Tag ID: 2
- If user mentions "考核" (assessment) → Tag ID: 3
- If user mentions "培训" (training) → Tag ID: 8
- If user mentions "报告" (report) + time period → Tag ID: 13
- If user asks a question about labor laws, employee rights, compensation → Tag ID: 1 (专业问答)
- If user asks "有没有"、"如何"、"怎样"、"为什么"等疑问句 → Tag ID: 1 (专业问答)

**Rule 3: Fallback - Professional Q&A**

If no clear match with specific document types (如员工手册、招聘JD、KPI考核表等), use the general Q&A category:
- Any HR-related question about laws, regulations, policies, employee rights → Tag ID: 1, RT: "专业问答"
- Example: "三期员工有没有特殊保障？", "员工离职需要提前多久通知？"
- Example: "试用期工资规定", "加班费计算方式"

**Rule 4: Default Fallback**

If still unclear, use the safest default:
- HR policy/guidance → Tag ID: 2, RT: "其他制度"
- General HR question → Tag ID: 1, RT: "专业问答"

## Script Usage

### Script Location

**IMPORTANT**: The script is located at:
`~/.workbuddy/skills/hr-ai-assistant/scripts/call_hrrule_api.py`

The platform should dynamically resolve this path using:
```python
import os
skill_dir = os.path.join(os.path.expanduser('~'), '.workbuddy', 'skills', 'hr-ai-assistant')
script_path = os.path.join(skill_dir, 'scripts', 'call_hrrule_api.py')
```

**DO NOT use hardcoded paths like `C:/Users/jikr/...`**

### Function Signature

```python
async def call_hrrule_api(
    api_key: str,
    content: str,
    tag_id: int,
    rt: str,
    ws_url: str = "ws://192.168.112.114:5000",
    model: str = "deepseek-ai/DeepSeek-R1",
    on_chunk: Optional[Callable[[str], None]] = None,
    on_complete: Optional[Callable[[], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
    verbose: bool = False
) -> str
```

### Parameters

- `api_key`: API 密钥(必需)
- `content`: 用户问题或需求(必需)
- `tag_id`: 内容类型 ID(必需)
- `rt`: 资源类型(必需)
- `ws_url`: WebSocket 地址(默认: ws://192.168.112.114:5000)
- `model`: 模型名称(默认: deepseek-ai/DeepSeek-R1)
- `on_chunk`: 收到内容块时的回调函数
- `on_complete`: 完成时的回调函数
- `on_error`: 错误时的回调函数
- `verbose`: 是否显示详细日志

### Return Value

Returns the complete response content as a string.

### Command Line Usage

```bash
python call_hrrule_api.py \
    --api-key "your-api-key" \
    --content "财务公司 需要招聘 社保专员，帮我生成一份 招聘JD" \
    --tag-id 4 \
    --rt "招聘JD" \
    --verbose
```

## Example Workflows

### Example 1: Generate Job Description (JD)

**User Request:**
```
财务公司 需要招聘 社保专员，帮我生成一份 招聘JD
```

**Skill Execution:**

1. **Parse Request:**
   - Identify: "招聘JD" → Tag ID: 4, RT: "招聘JD"
   - Extract context: 财务公司, 社保专员

2. **Construct Content:**
   ```python
   content = "财务公司 需要招聘 社保专员，帮我生成一份 招聘JD"
   tag_id = 4
   rt = "招聘JD"
   ```

3. **Call API:**
   ```python
   response = await call_hrrule_api(
       api_key='your-api-key',
       content=content,
       tag_id=tag_id,
       rt=rt,
       on_chunk=lambda text: print(text, end='', flush=True),
       verbose=True
   )
   ```

4. **Stream Response:**
   The AI response is streamed back in real-time.

### Example 2: Generate Employee Handbook

**User Request:**
```
帮我写一个员工手册,适用于50人的科技公司
```

**Skill Execution:**

1. **Parse Request:**
   - Identify: "员工手册" → Tag ID: 2, RT: "员工手册"
   - Extract context: 50人, 科技公司

2. **Call API:**
   ```python
   response = await call_hrrule_api(
       api_key='your-api-key',
       content='帮我写一个员工手册,适用于50人的科技公司',
       tag_id=2,
       rt='员工手册',
       on_chunk=lambda text: print(text, end='', flush=True)
   )
   ```

### Example 3: Create Performance Review Form

**User Request:**
```
为销售部门设计KPI考核表
```

**Skill Execution:**

1. **Parse Request:**
   - Identify: "KPI考核表" → Tag ID: 3, RT: "KPI考核表"
   - Extract context: 销售部门

2. **Call API:**
   ```python
   response = await call_hrrule_api(
       api_key='your-api-key',
       content='为销售部门设计KPI考核表',
       tag_id=3,
       rt='KPI考核表',
       on_chunk=lambda text: print(text, end='', flush=True)
   )
   ```

### Example 4: Professional Q&A (Labor Law Question)

**User Request:**
```
三期员工有没有特殊保障？
```

**Skill Execution:**

1. **Parse Request:**
   - Identify: Question about labor law/employee rights → Tag ID: 1, RT: "专业问答"
   - Extract context: 三期员工 (孕期、产期、哺乳期), 特殊保障

2. **Call API:**
   ```python
   response = await call_hrrule_api(
       api_key='your-api-key',
       content='三期员工有没有特殊保障？',
       tag_id=1,
       rt='专业问答',
       on_chunk=lambda text: print(text, end='', flush=True),
       verbose=True
   )
   ```

3. **Stream Response:**
   ```
   AI 响应:

   根据《劳动合同法》和《女职工劳动保护特别规定》，三期员工（孕期、产期、哺乳期）确实享有特殊保障，主要包括：

   1. 不得单方面解除劳动合同
      - 用人单位不得依据《劳动合同法》第40条、第41条单方面解除合同
      - 除非员工有严重违纪等《劳动合同法》第39条规定的情况

   2. 孕期保护
      - 不得安排从事高强度、有毒有害工作
      - 不得延长劳动时间或安排夜班工作
      - 孕期7个月以上，每天应安排1小时工间休息

   3. 产期保护
      - 享有98天产假（难产或多胞胎适当增加）
      - 产假期间工资照发
      - 生育保险报销医疗费用

   4. 哺乳期保护
      - 每日享有1小时哺乳时间
      - 不得安排有毒有害工作

   5. 经济补偿
      - 如劳动合同期满，合同自动顺延至三期结束
      - 顺延期间不视为续签劳动合同
   ```

### Example 5: General HR Consultation

**User Request:**
```
员工离职需要提前多少天通知？
```

**Skill Execution:**

1. **Parse Request:**
   - Identify: Question about resignation → Tag ID: 1, RT: "专业问答"
   - Extract context: 员工离职, 提前通知时间

2. **Call API:**
   ```python
   response = await call_hrrule_api(
       api_key='your-api-key',
       content='员工离职需要提前多少天通知？',
       tag_id=1,
       rt='专业问答',
       on_chunk=lambda text: print(text, end='', flush=True)
   )
   ```

## Error Handling

The script handles various error scenarios:

### Connection Errors
- Invalid WebSocket URL
- Network connectivity issues
- Firewall blocking

### Authentication Errors
- Invalid API Key
- API Key expired
- Permission denied

### API Errors
- Invalid parameters
- Server errors
- Timeout (120 seconds)

### Error Handling Example

```python
def handle_error(error_msg: str):
    print(f"错误: {error_msg}")
    # 提供用户友好的错误信息
    if "Unauthorized" in error_msg or "401" in error_msg:
        print("API Key 无效,请检查您的 API Key")
    elif "Connection" in error_msg:
        print("连接失败,请检查网络和 WebSocket URL")
    else:
        print("发生未知错误,请稍后重试")

response = await call_hrrule_api(
    api_key='your-api-key',
    content='your content',
    tag_id=2,
    rt='员工手册',
    on_error=handle_error,
    verbose=True
)
```

## Best Practices

### 1. First-Time User Experience (首次使用体验)

**Note**: 当首次使用此 skill 且未配置 API Key 时，平台（WorkBuddy/OpenClaw）应该：

✅ **推荐做法**：
1. 检测到没有 API Key
2. **先显示**友好的提示信息（访问 https://ai.hrrule.com/ 免费申请）
3. **然后**使用平台的通用大模型回答问题
4. 用户手动配置 API Key（通过环境变量、配置文件或配置脚本）

**应该显示的提示信息**：
```
══════════════════════════════════════════════════════════════════════════════
📌 首次使用 HR AI Assistant
══════════════════════════════════════════════════════════════════════════════

✨ 获取免费 API Key 以获得更专业的 HR AI 服务：

1. 访问: https://ai.hrrule.com/
2. 注册/登录账号
3. 在个人中心申请 API Key
4. **完全免费**,申请后立即可用

📝 配置方式（任选一种）：

方式1: 一键配置（推荐）
把申请到的 API Key 直接粘贴到对话框中，我会自动帮你配置到配置文件

方式2: 手动配置
设置环境变量: export HRRULE_API_KEY='your-api-key'
或编辑配置文件: ~/.workbuddy/skills/hr-ai-assistant/config.json
内容: {"api_key": "your-api-key"}

══════════════════════════════════════════════════════════════════════════════
```

**执行顺序**：
```
1. 用户提问："三期员工有没有特殊保障？"
2. 检测到需要此 skill
3. 检测到没有 API Key
4. ⚠️ 显示上述提示信息 ← 必须在回答前
5. 使用通用大模型回答问题
6. 用户手动配置 API Key（通过环境变量或编辑配置文件）
```


**注意**：用户需要手动配置 API Key（通过环境变量或编辑配置文件），系统不会自动检测或保存。

### 2. Provide Detailed Context

Always include as much context as possible in the `content` parameter:
- Company size and industry
- Specific requirements
- Target audience
- Time constraints

**Good:**
```
财务公司 需要招聘 社保专员，帮我生成一份 招聘JD
要求: 3年以上经验,熟悉社保政策,薪资8-12k
```

**Less Good:**
```
生成招聘JD
```

### 2. Use Streaming for Better UX

Always use the `on_chunk` callback to stream responses:

```python
def stream_text(text: str):
    print(text, end='', flush=True)

response = await call_hrrule_api(
    # ... parameters
    on_chunk=stream_text
)
```

### 3. Handle Errors Gracefully

Always provide error callbacks:

```python
response = await call_hrrule_api(
    # ... parameters
    on_error=lambda msg: print(f"❌ 错误: {msg}"),
    on_complete=lambda: print("\n✅ 完成")
)
```

### 4. Set Appropriate Timeout

The script has a 120-second timeout by default. For complex documents, this is usually sufficient.

## Configuration

### API Key Configuration

The API Key should be configured securely. Options:
1. Environment variable: `HRRULE_API_KEY`
2. Configuration file
3. Direct parameter passing

### WebSocket URL Configuration

Default: `ws://192.168.112.114:5000`

Can be changed via:
- Command line: `--ws-url`
- Script parameter: `ws_url=`
- Configuration file

## Troubleshooting

### Issue: Connection Fails

**Check:**
- WebSocket URL is correct
- Network connectivity
- Firewall settings
- Server is running

### Issue: Authentication Error

**Check:**
- API Key is valid
- API Key has not expired
- API Key has proper permissions

### Issue: No Response

**Check:**
- Content parameter is not empty
- Tag ID and RT are valid
- Network connection is stable
- Server is processing requests

### Issue: Timeout

**Solution:**
- Increase timeout in script
- Simplify the request
- Check server load

## Integration Examples

### DingTalk Integration

When receiving HR requests from DingTalk:

```python
# 收到 DingTalk 消息
message = "财务公司 需要招聘 社保专员，帮我生成一份 招聘JD"

# 调用 skill
import sys
import os

# 获取 skill 目录路径（动态解析）
skill_dir = os.path.join(os.path.expanduser('~'), '.workbuddy', 'skills', 'hr-ai-assistant')
script_dir = os.path.join(skill_dir, 'scripts')
sys.path.insert(0, script_dir)

from call_hrrule_api import call_hrrule_api

# ⚠️ 重要：平台必须直接执行 skill 目录下的脚本，不要新建 Python 文件

async def handle_dingtalk_message(message: str):
    # 解析请求
    tag_id, rt = parse_request(message)  # 4, "招聘JD"

    # 调用 API
    response = await call_hrrule_api(
        api_key=os.getenv('HRRULE_API_KEY'),
        content=message,
        tag_id=tag_id,
        rt=rt,
        on_chunk=lambda text: send_to_dingtalk(text)  # 实时发送到 DingTalk
    )

    return response

# 执行
response = asyncio.run(handle_dingtalk_message(message))
```

### QQ Integration

Similar to DingTalk, parse the QQ message and call the API:

```python
async def handle_qq_message(message: str):
    # 解析请求
    tag_id, rt = parse_request(message)

    # 调用 API
    response = await call_hrrule_api(
        api_key='your-api-key',
        content=message,
        tag_id=tag_id,
        rt=rt,
        on_chunk=lambda text: send_to_qq(text)
    )

    return response
```

## Summary

This skill provides **direct API integration** with the HRrule AI platform, enabling WorkBuddy to:
- Automatically parse HR requests
- Select appropriate parameters (tag_id, rt)
- Call WebSocket API in real-time
- Stream responses back to users
- Handle errors gracefully

The skill is designed for seamless integration with chat platforms like DingTalk and QQ, making it easy to generate HR documents on demand.

## Reference Materials

- API Reference: `references/api_reference.md`
- Example Prompts: `references/example_prompts.md`
- Usage Guide: `README.md`
- Test Page: `assets/chat_example.html`
- Original Test: `test_open_chat.html`
