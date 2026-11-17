# OPIE Engine 职位 JD 生成 Skill

该 Skill 让 OPIE Engine 智能体根据自然语言招聘需求生成结构化职位 JD，并在 workspace 中创建对应岗位文件。即使未配置模型，也能通过确定性的本地规则完成基础 JD 生成；OpenAI 兼容模型仅用于增强生成质量。

## 安装与运行环境

- Python 3.11 或更高版本
- 一个具有写入权限的 OPIE Engine workspace

```powershell
cd hr_recruitment_onboarding_skill
python -m pip install -r requirements.txt
```

## 可选模型配置

如需获得模型增强的职位要求提取能力，请在 OPIE Engine 的安全环境变量中配置：

- `LLM_BASE_URL`：OpenAI 兼容 API 基础地址
- `LLM_MODEL`：模型标识
- `LLM_API_KEY`：模型服务密钥

不得在普通聊天中粘贴 API Key，也不得将其写入 `.env`、请求 JSON、源代码、日志或 workspace 文件。密钥只能保存在 OPIE Engine 的安全设置中。

任一模型配置缺失，或模型调用失败时，程序仍会使用本地规则完成生成，并在返回结果中给出供 HR 复核的警告。

`OPIE_WORKSPACE` 为可选环境变量，用于指定输出工作空间根目录；未设置时，数据会保存到 Skill 目录下的 `workspace/`。

## 调用方式

请在本目录执行。请求必须包含 `mode`、`job_id`、`job_title`、`department`、`location` 和 `description`。

从 JSON 文件调用：

```powershell
python main.py --request samples/create_position_request.json
```

从标准输入（stdin）调用：

```powershell
Get-Content -Raw samples/create_position_request.json | python main.py
```

程序标准输出只会返回一个 JSON 对象。成功时，`generated_files` 中的文件路径相对于 `OPIE_WORKSPACE`；请始终向 HR 展示 `warnings`，尤其是 `generation_source` 为 `rules_fallback` 时的本地规则回退提示。

## 验收示例：无模型生成

以下命令应从仓库根目录运行。它会清除当前进程中的模型变量，并创建一个唯一的临时 workspace：

```powershell
[Environment]::SetEnvironmentVariable('LLM_BASE_URL', $null, 'Process')
[Environment]::SetEnvironmentVariable('LLM_MODEL', $null, 'Process')
[Environment]::SetEnvironmentVariable('LLM_API_KEY', $null, 'Process')
$acceptanceWorkspaceName = 'hr-jd-acceptance-{0:yyyyMMddHHmmssfff}-{1}' -f (Get-Date), (Get-Random)
$env:OPIE_WORKSPACE = Join-Path ([System.IO.Path]::GetTempPath()) $acceptanceWorkspaceName
New-Item -ItemType Directory -Path $env:OPIE_WORKSPACE | Out-Null
python .\hr_recruitment_onboarding_skill\main.py --request .\hr_recruitment_onboarding_skill\samples\create_position_request.json
Get-ChildItem -Recurse "$env:OPIE_WORKSPACE\hr_recruitment_data\positions\JOB-2026-001"
```

第一次调用必须返回一个 `success: true` 的 JSON 对象，且 `generation_source` 为 `rules_fallback`；同时创建 `position.json`、`jd.md` 和 `talent_pool.json`。在同一个 workspace 中再次运行 Python 命令，应返回一次 `DUPLICATE_JOB_ID` 错误，且原始文件保持不变。

## 上传到 ClawHub

ClawHub 接受文件夹上传时，请直接选择本 Skill 的根目录：

```text
E:\HR-skill\hr_recruitment_onboarding_skill
```

请勿选择上层的 `E:\HR-skill`，也无需生成 ZIP 压缩包。上传前请确认该文件夹包含 `SKILL.md`、`LICENSE`、`main.py`、`app/`、`services/`、`prompts/` 和 `samples/`。

文件夹中的 `.git`、`.env*`、`workspace`、`__pycache__`、`.pytest_cache` 和 `dist` 均不应上传。如 ClawHub 支持排除规则，请将这些名称加入排除列表。
