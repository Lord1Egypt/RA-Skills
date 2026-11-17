---
name: international_draft_ocr
description: 国际汇票 OCR 技能：仅在用户明确同意后，读取本地票据图像/PDF，上传至 Scnet OCR 服务并提取收付方信息、币种金额、到期日、付款银行及票据号码。
version: 1.0.2
author: SCNet
license: MIT
tags:
  - OCR
  - 证件识别
  - 国际汇票识别
required_env_vars:
  - SCNET_API_KEY
optional_env_vars:
  - SCNET_API_BASE
primary_credential: SCNET_API_KEY
dependencies:
  - python3
  - requests
input:
  - ocrType : 识别类型，仅允许 INTERNATIONAL_BILL
  - filePath : 待识别图片/文档的本地路径
output: 结构化的 JSON 数据，包含识别结果
---

# Sugon-Scnet 国际汇票识别 OCR 技能

> **安全与隐私提示**
> 本技能会将您提供的本地票据图像、PDF 或压缩包上传至第三方 Scnet OCR 服务（`https://api.scnet.cn`）进行识别。上传内容可能包含收款人、付款行、信用证号码、金额等敏感金融信息。请在确认了解数据将离开本地环境、可能被第三方处理或跨境传输后，再开启使用。

本技能封装了国际汇票识别的 OCR 服务，通过单一接口即可调用 1 种识别能力，高效提取票据内容。

---

## 功能特性

- **国际汇票识别**：支持识别提取收付方信息、币种金额、到期日、付款银行及票据号码内容。

## MCP 权限与数据外传声明

本技能需要以下权限，并已在 `skill.yaml` 中声明：

| 权限 | 范围 | 用途 |
|------|------|------|
| files | read | 读取用户提供的本地图片、PDF 或压缩包文件 |
| network | upload | 将文件上传至 Scnet OCR API（`https://api.scnet.cn/api/llm/v1/ocr/recognize`） |
| shell | execute (python3/python) | 执行 Python 脚本以调用 OCR 服务 |

**数据外传说明**：
- 文件会离开本地环境，上传至 Scnet 云服务器处理
- 可能涉及跨境数据传输
- 数据保留与处理策略受 [Scnet 服务条款](https://www.scnet.cn) 约束
- 仅当用户通过以下任一方式明确同意后，脚本才会执行上传：
  - 环境变量 `SCNET_OCR_UPLOAD_CONFIRMED=1`
  - 命令行参数 `--confirm-upload`
  - 配置文件 `config/.env` 中设置 `SCNET_OCR_UPLOAD_CONFIRMED=1`

## 前置配置

> **重要**：使用前需要申请 Scnet API Token，并明确同意将识别文件上传至第三方服务。

### 申请 API Token

1. 访问 [Scnet 官网](https://www.scnet.cn) 注册/登录
2. 在控制台申请 API 密钥（格式：`sc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
3. 复制密钥备用

### 配置 Token

**手动配置（推荐）**
1. 在技能目录下创建 `config/.env` 文件，内容如下：

```ini
# =====  Sugon-Scnet OCR API 配置 =====
# 申请地址：https://www.scnet.cn
SCNET_API_KEY=your_scnet_api_key_here

# API 基础地址（一般无需修改）
SCNET_API_BASE=https://api.scnet.cn/api/llm/v1

# 确认已了解隐私风险并同意上传文件（设为 1 表示同意）
SCNET_OCR_UPLOAD_CONFIRMED=1
```

2. 将 `SCNET_API_KEY` 替换为您的真实密钥
3. 将 `SCNET_OCR_UPLOAD_CONFIRMED` 设置为 `1`，表示您已阅读并同意本技能的数据上传说明
4. 设置文件权限为 600（仅所有者可读写）

**安全警告**：
- 切勿将 API Key 直接粘贴到聊天对话中，否则可能被记录或泄露。
- 本技能上传的文件内容会离开本地环境并由 Scnet 服务处理，请勿上传包含国家秘密、个人隐私或您无权披露的敏感信息的文件。

### Token 更新

Token 过期后调用会返回 401 或 403 错误。更新方法：重新申请 Token 并替换 `config/.env` 中的 `SCNET_API_KEY`。

### 依赖安装

本技能需要 Python 3.6+ 和 requests 库。请运行以下命令：

```bash
pip install requests
```

---

## 使用方法

### 参数说明

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| ocrType | string | 是 | 识别类型枚举。必须为以下之一：<br>• INTERNATIONAL_BILL（国际汇票） |
| filePath | string | 是 | 待识别图片的本地绝对路径。支持 jpg、png、pdf 等常见格式。 |

### 命令行调用示例

在确认同意上传后执行：

```bash
# 方式一：通过环境变量声明同意
export SCNET_OCR_UPLOAD_CONFIRMED=1
python .claude/skills/international_draft_ocr/scripts/main.py INTERNATIONAL_BILL /path/to/test.jpg

# 方式二：通过 --confirm-upload 参数声明同意
python .claude/skills/international_draft_ocr/scripts/main.py --confirm-upload INTERNATIONAL_BILL /path/to/test.jpg
```

### 在 AI 对话中使用

用户可以说：

- "帮我识别这张图像中的国际汇票信息，图片在 /Users/name/Downloads/test.jpg"

AI 会根据 description 中的关键词自动触发本技能。触发前会告知您文件将被上传至 Scnet OCR 服务，并在获得同意后继续。

### AI 调用建议

为避免触发 API 速率限制（10 QPS），请串行调用本技能，即等待前一个识别完成后再发起下一个请求。
如果使用 OpenClaw 的 exec 工具，建议设置 timeout 或 yieldMs 参数，让命令同步执行，避免多个命令同时运行导致并发。

### 配置选项

编辑 `config/.env` 文件：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| SCNET_API_KEY | 必需 | Scnet API 密钥 |
| SCNET_API_BASE | https://api.scnet.cn/api/llm/v1 | API 基础地址（一般无需修改） |
| SCNET_OCR_UPLOAD_CONFIRMED | 未设置 | 设置为 `1` 表示您已了解并同意文件将被上传至第三方 Scnet 服务 |

### 输出

- 标准输出：识别结果的 JSON 数据，结构与 API 文档一致，位于 `data` 字段内。
- 识别结果位于 `data[0].result[0].elements` 中，具体字段取决于 `ocrType`。
- 错误信息：如果发生错误，会输出以 `错误:` 开头的友好提示。

### 注意事项

- 本技能调用的 OCR API 有 10 QPS 的速率限制。
- 如果遇到 429 错误，请等待 2-3 秒后重试，不要连续发起请求。
- 建议在调用前确保图片已准备就绪，避免因网络问题导致重复调用。
- 上传文件前，脚本会检查 `SCNET_OCR_UPLOAD_CONFIRMED` 环境变量或 `--confirm-upload` 参数，确保您已被告知数据将离开本地环境。
- 脚本会对 `ocrType` 进行白名单校验，仅允许 `INTERNATIONAL_BILL`。

### 数据隐私与合规

- **数据出境**：识别文件会上传至 Scnet 云服务器，可能涉及跨境数据传输，请确保符合您所在地区的数据合规要求。
- **数据保留**：请查阅 [Scnet 服务条款](https://www.scnet.cn) 了解文件上传后的保留、删除及处理策略。
- **最小化原则**：仅上传当前识别任务所需的文件，避免上传无关或包含过度敏感信息的文档。
- **访问控制**：`config/.env` 文件包含 API 密钥，请确保仅所有者可读写（建议权限 600）。

### 故障排除

| 问题 | 解决方案 |
|------|----------|
| 配置文件不存在 | 创建 config/.env 并填入 Token（参考前置配置） |
| API Key 无效/过期 | 重新申请 Token 并更新 `.env` 文件 |
| 文件不存在 | 检查提供的文件路径是否正确 |
| 网络连接失败 | 检查网络连接或防火墙设置 |
| 不支持的文件类型 | 确保文件扩展名为允许的类型（参考 API 文档） |
| 不支持的 ocrType | 仅支持 `INTERNATIONAL_BILL` |
| 401/403/Unauthorized | Token 无效或过期，重新申请并配置 |
| 429 Too Many Requests | 请求过于频繁，技能会自动等待并重试（最多 3 次）。若持续失败，请降低调用频率或联系服务方提高限额。 |
| 未确认上传同意 | 设置 `SCNET_OCR_UPLOAD_CONFIRMED=1` 或使用 `--confirm-upload` 参数（参考使用方法） |
