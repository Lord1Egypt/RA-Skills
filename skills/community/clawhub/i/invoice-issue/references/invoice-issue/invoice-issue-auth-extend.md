# 场景：invoice-issue-auth-extend（开票权限延长）

## 触发时机

本场景可由两类请求触发：

1. 开票场景返回“请先扫码验证获取开票权限”或等价语义时，转入本场景完成认证后，再返回开票流程继续提交。
2. 用户主动提出“开票权限延长”“重新获取开票权限二维码”“开票权限认证”等需求时，直接进入本场景执行认证。

## 触发关键词

开票权限延长,开票权限续期,延长开票权限,开票权限人脸认证,开票权限认证

## 场景说明

本场景用于完成开票权限延长认证，可由开票流程衔接触发，也可由用户单独主动触发。执行顺序固定如下：

1. 优先复用当前开票任务中已识别的 `uscc`、`areaCode`、`personalAccount`；若当前不是从开票流程衔接进入，则直接使用本次用户提供并经编码转换后的参数。
2. 调用二进制命令 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-auth-workflow --action start --pretty` 获取二维码。
3. 二进制命令将二维码阶段结果写回当前开票任务 JSON 的 `issue_auth_result`，并落地二维码 Markdown 文件。
4. Agent 读取二维码 Markdown，原样展示给用户，提示其完成扫码。
5. 用户明确表示“我已完成扫码”后，调用二进制命令 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-auth-workflow --action verify --pretty` 校验扫码状态。
6. 若任一二维码扫码成功，二进制命令继续查询人脸认证状态，并将校验结果写回当前开票任务 JSON 的 `issue_auth_result`，同时落地认证结果 Markdown 文件。
7. Agent 读取认证结果 Markdown，原样展示给用户；若认证通过，再返回开票主流程继续正式开票。

## 参数规格

| 参数名            | 类型    | 必填 | 说明                               |
| ----------------- | ------- | ---- | ---------------------------------- |
| `uscc`            | string  | Y    | 纳税人识别号                       |
| `areaCode`        | integer | Y    | 地区编码                           |
| `personalAccount` | string  | Y    | 个人账号（身份证号/手机号/用户名） |

## 参数来源约束

1. 若存在当前开票任务，优先复用当前开票任务 JSON 中 `raw_input_json` 里的 `uscc`、`areaCode`、`personalAccount`。
2. 若用户主动触发本场景且当前不存在可复用任务，则使用用户本轮输入提供的 `uscc`、`areaCode`、`personalAccount`。
3. 若三项参数任一缺失，必须一次性向用户追问；不得自行生成、猜测或替换。
4. `areaCode` 的自然语言转换规则沿用 [SKILL.md](../../SKILL.md) 中的编码映射规则。

## 二进制 CLI 与产物约定

### 获取二维码

- 命令：`.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-auth-workflow --action start --pretty`
- 输入来源：优先使用当前开票任务状态 JSON；若为用户主动触发，也可使用本次输入整理出的参数
- 若未传 `--task-file`，二进制会优先读取当前任务；因此当本场景是“用户单独触发”，而不是从开票流程检测到“无开票权限”后衔接进入时，若当前不存在可复用的任务 JSON，则不能直接执行 `--action start`
- 此时应先准备最小输入 JSON，例如：

```json
{
  "uscc": "91440300MAD66AAP45"
}
```

- 再调用 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-auth-workflow --action start --input <临时输入文件>.json --pretty`，由二进制基于该输入构建或复用标准任务状态 JSON
- 二进制在构建 task JSON 时，会按 `uscc` 自动从 `workspace-config.json` 的企业配置中补齐 `areaCode`、`personalAccount`；若配置文件不存在，会先自动创建默认配置；若配置中缺少这两项中的任一项，任务初始化会直接失败，需先补齐企业配置
- 上述初始化步骤的目的，是补齐 `raw_input_json`、`workspace_dir`、`task_file_path`、`storage` 等任务上下文字段，避免因缺少当前任务而报错
- 任务状态回写位置：`issue_auth_result.qrcode_response`、`issue_auth_result.qrcode_list`、`issue_auth_result.qrcode_markdown`、`issue_auth_result.qrcode_markdown_path`
- Markdown 产物要求：
  - 必须包含二维码认证 ID、二维码类型、扫码链接、当前状态、下一步说明
  - Agent 必须读取 `issue_auth_result.qrcode_markdown_path` 指向的本地 Markdown 文件并原样展示

### 校验扫码与认证状态

- 命令：`.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-auth-workflow --action verify --pretty`
- 前置条件：当前任务 JSON 中已存在 `issue_auth_result.qrcode_list`
- 任务状态回写位置：`issue_auth_result.scan_status_response`、`issue_auth_result.scan_status_list`、`issue_auth_result.auth_status_response`、`issue_auth_result.verify_markdown`、`issue_auth_result.verify_markdown_path`
- Markdown 产物要求：
  - 必须包含每个二维码的扫码状态
  - 若已触发认证状态查询，必须包含人脸认证状态
  - Agent 必须读取 `issue_auth_result.verify_markdown_path` 指向的本地 Markdown 文件并原样展示

## 状态判定规则

1. 任一二维码状态为 `1`：视为待扫码，提示用户继续扫码，不自动轮询。
2. 任一二维码状态为 `3`：视为二维码已失效，提示用户重新获取二维码。
3. 任一二维码状态为 `2`：继续查询认证状态。
4. 认证状态 `status=1` 且 `isAuth=true`：视为开票权限延长成功，可返回开票流程。
5. 认证状态 `status=0/2`：视为认证处理中，提示用户稍后再次校验。
6. 认证状态 `status=-1`：视为认证失败，提示用户重新发起认证。

## 输出模板

### 成功

```
✅ 开票权限延长成功

二维码认证ID：{rzid}
扫码状态：已完成
人脸认证：已通过

我将返回开票流程继续处理。
```

### 待用户扫码

```
⏱ 开票权限延长任务待确认扫码

二维码认证ID：{rzid_list}
当前扫码状态：{scan_status_text}
请完成扫码后回复“我已完成扫码”。
```

### 失败

```
❌ 开票权限延长失败：{error_message}
```
