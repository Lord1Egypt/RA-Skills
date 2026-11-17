---
name: hr-recruitment-jd-generator
description: Use when users ask to create a recruitment JD, initialize recruiting files, or configure the HR JD generator or its optional model.
---

# OPIE Engine 职位 JD 生成 Skill

## 核心工作流程

将用户的自然语言招聘需求整理为一次经过校验的 CLI 调用，生成职位 JD 和岗位工作区文件。模型配置为可选项：未配置模型时，必须继续使用内置本地规则生成，不得阻塞用户。

1. 收集以下六个字段；仅追问缺失项：

   | 字段 | 说明 |
   |---|---|
   | `mode` | 固定为 `generate_jd` |
   | `job_id` | 唯一职位编号，格式为 `JOB-YYYY-NNN` |
   | `job_title` | 职位名称 |
   | `department` | 招聘部门 |
   | `location` | 工作地点 |
   | `description` | 岗位职责、经验、技能、学历及其他与岗位直接相关的要求 |

2. 模型增强为可选项。用户要求配置模型或需要更精细的 JD 时，指导其在 OPIE Engine 的安全环境变量中配置：`LLM_BASE_URL`、`LLM_MODEL` 和 `LLM_API_KEY`。未配置模型时，直接使用本地规则生成基础 JD。

3. 不得在普通聊天中索取、接收或复述 API Key；不得将 API Key 持久化到请求 JSON、日志、`.env` 或其他文件。密钥只能保存在 OPIE Engine 的安全设置中。

4. 在 Skill 根目录调用现有 CLI：

   ```text
   python main.py --request <request.json>
   ```

   请求必须只包含上述六个业务字段。不得直接修改应用代码或 workspace 中既有职位文件。

5. 读取 CLI 返回的单个 JSON 对象。成功时，向用户说明 `message`、每个 `generated_files` 工作区相对路径和全部 `warnings`。若 `generation_source` 为 `rules_fallback`，明确说明已使用本地规则并展示回退提示。失败时，说明 `error_code` 和 `message`，再请求用户修正输入。

6. 生成结果必须由 HR 人工复核后再使用。确认岗位职责和任职条件均与岗位直接相关（岗位相关）、必要、合法且无歧视；不得虚构或加入性别、年龄、婚育、民族、籍贯、宗教、健康、外貌等受保护或无关特征要求。

## 常见错误

- 未配置模型不是停止生成 JD 的理由；本地规则回退仍可用。
- 不得隐藏回退警告，也不得把工作区相对路径改成机器绝对路径。
- 职位编号重复时，不得覆盖原有职位；请用户提供新的 `job_id`。
