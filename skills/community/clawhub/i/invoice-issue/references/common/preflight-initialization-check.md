# 场景：preflight-initialization-check（任务执行前初始化检测）

## 模板用途

用于在正式执行业务场景前，统一执行预检脚本，检查当前工作区配置、工作区目录、企业绑定、登录状态和账密状态是否可继续执行。


## 场景说明

- 业务目标：在任务开始前先跑一遍统一预检，尽量把会阻断执行的问题提前暴露出来。
- 当前入口：统一执行预检脚本。
- 失败处理：若预检失败，必须直接读取命令生成的 Markdown 报告正文，并原样渲染回对话中；不得因脱敏需求，对md内容进行二次修改、总结；不得根据接口响应、或其他中间结果自行补充解释或猜测处理办法。如果问题涉及工作区目录不可用或需要重新指定目录，应通过 `workspace-config-writer` 更新配置后再次执行预检。
- API Key 权限处理：若预检报告、接口响应或命令输出中出现“无权调用该能力”，必须视为当前 API Key 未绑定本 skill 所需能力权限或企业，不得引导用户登录或重新登录。Agent 必须在原样渲染预检 Markdown 报告后，按同级 `README.md` 中的 API Key 获取方式告知用户为当前 API Key 绑定对应能力权限及企业后再重新预检。
- 扩展性：后续公共检测逻辑继续追加到这个预检脚本里，不再分散到多个独立校验入口。

## 执行步骤

1. 根据用户输入判断是否已提供企业名称或税号，如果有执行：
   
```powershell
.\bin\windows-amd64\invoice-assistant_windows_amd64.exe task-preflight-check --enterprise-name "企业名称或税号"
```
否则执行

```powershell
.\bin\windows-amd64\invoice-assistant_windows_amd64.exe task-preflight-check
```

1. 命令执行结束后，按照以下规则，处理预检结果：

- `preflight_passed=true`：预检通过，可以继续后续业务步骤。
- `preflight_passed=false`：预检未通过，立即中止后续流程，不输入与后续流程相关的内容；必须直接读取并原样渲染 Markdown 报告正文给用户，**禁止因任何原因进行二次改动或补充描述**。
- 若 Markdown 报告正文出现“无权调用该能力”，原样渲染报告后还必须按同级 `README.md` 中的 API Key 获取方式告知用户配置对应能力权限；不得改为提示用户去税局登录、重新登录或继续快速登录。
- 只有重新执行预检并确认通过后，才能继续后续业务场景。

## 配置更新方式

- 预检脚本读取的配置文件是 `.invoice-config/workspace-config.json`；若文件不存在，会在首次读取时自动创建默认配置。
- 如果 Agent 需要补写或更新配置，必须调用工作区配置写入脚本，不能直接手改 `workspace-config.json`。
- 配置更新命令入口：`.\bin\windows-amd64\invoice-assistant_windows_amd64.exe workspace-config-writer`
- 该脚本负责统一读取配置；当配置文件不存在时，会先写入默认配置，再按传入字段合并更新并重新写回配置文件。

### 常用写法

1. 更新工作区目录：

```powershell
.\bin\windows-amd64\invoice-assistant_windows_amd64.exe workspace-config-writer --workspace-dir "D:\\your-workspace"
```

2. 更新 apikey：

```powershell
.\bin\windows-amd64\invoice-assistant_windows_amd64.exe workspace-config-writer --apikey "your_apikey"
```
