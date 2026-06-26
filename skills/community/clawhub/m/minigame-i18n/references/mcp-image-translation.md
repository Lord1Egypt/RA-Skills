# MCP 图片翻译接口说明

## 概述

MCP 图片翻译服务（`minigame-l10n`）用于处理小游戏项目中包含文字的图片资源。通过微信出海工具提供的 OCR 和图片翻译重绘能力，实现图片中文字的自动识别与翻译。

所有工具按功能分为 **5 个组合**，围绕 `file_id`（integer）串联：

| 组合 | 工具 | 功能 |
|------|------|------|
| 语言查询 | `GetLanguageInfoMcp` | 获取目标语言列表 |
| 图片上传 | `scripts/upload-images.js`（⛔ 禁止 AI 调用上传 MCP 接口） | 脚本自动完成 zip 打包 + 分片上传 |
| OCR 识别 | `StartImageOcrMcp` → `GetImageOcrProgressMcp` → `GetImageOcrResultMcp` | 图片文字识别 |
| 术语表 | `UploadTermDataMcp` | 上传术语对照表 |
| 图片翻译 | `StartImageTranslateMcp` → `GetImageTranslateProgressMcp` → `GetImageTranslateResultMcp` | 图片翻译重绘 |

## MCP 服务配置

### 认证参数

| 参数 | Header / 字段名 | 说明 |
|------|-----------------|------|
| AppID | `APPID` | 小游戏的 AppID，如 `wxa94ef53986427800` |
| Token | `TOKEN` | 访问令牌，由出海工具平台分配 |

### 各 IDE 配置方式

不同 IDE 的 MCP 配置文件路径和格式不同。安装时需要**识别当前运行环境**，将配置写入对应文件。

#### WorkBuddy

**配置文件**：`~/.workbuddy/mcp.json`

```json
{
  "mcpServers": {
    "minigame-l10n": {
      "url": "http://gamemp.weixin.qq.com/cgi-bin/gamewxagl10nwap/mcptransfer",
      "headers": {
        "APPID": "<小游戏AppID>",
        "TOKEN": "<访问令牌>"
      },
      "disabled": false
    }
  }
}
```

#### CodeBuddy

**配置文件**：`~/.codebuddy/mcp.json`

```json
{
  "mcpServers": {
    "minigame-l10n": {
      "url": "http://gamemp.weixin.qq.com/cgi-bin/gamewxagl10nwap/mcptransfer",
      "headers": {
        "APPID": "<小游戏AppID>",
        "TOKEN": "<访问令牌>"
      },
      "disabled": false
    }
  }
}
```

#### Cursor

**配置文件**：`~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "minigame-l10n": {
      "url": "http://gamemp.weixin.qq.com/cgi-bin/gamewxagl10nwap/mcptransfer",
      "headers": {
        "APPID": "<小游戏AppID>",
        "TOKEN": "<访问令牌>"
      },
      "disabled": false
    }
  }
}
```

#### Claude Code

**配置文件**：`~/.claude/mcp.json`

```json
{
  "mcpServers": {
    "minigame-l10n": {
      "url": "http://gamemp.weixin.qq.com/cgi-bin/gamewxagl10nwap/mcptransfer",
      "headers": {
        "APPID": "<小游戏AppID>",
        "TOKEN": "<访问令牌>"
      },
      "disabled": false
    }
  }
}
```

#### Codex (OpenAI)

**配置文件**：`~/.codex/mcp.json`

```json
{
  "mcpServers": {
    "minigame-l10n": {
      "url": "http://gamemp.weixin.qq.com/cgi-bin/gamewxagl10nwap/mcptransfer",
      "headers": {
        "APPID": "<小游戏AppID>",
        "TOKEN": "<访问令牌>"
      },
      "disabled": false
    }
  }
}
```

#### 环境识别策略

安装时按以下优先级自动识别当前 IDE 环境：

| 优先级 | 判断方式 | IDE |
|--------|----------|-----|
| 1 | 存在 `~/.workbuddy/` 目录 | WorkBuddy |
| 2 | 存在 `~/.codebuddy/` 目录 | CodeBuddy |
| 3 | 存在 `~/.cursor/` 目录 | Cursor |
| 4 | 存在 `~/.claude/` 目录 | Claude Code |
| 5 | 存在 `~/.codex/` 目录 | Codex |

如果无法自动识别，询问用户正在使用哪个 IDE。

**建议同时写入所有已安装的 IDE**，确保用户在任何环境下都能使用。

## 如何检测 MCP 是否可用

1. 调用 `mcp_get_tool_description` 查看 `minigame-l10n` 服务下是否有可用工具
2. 如果返回了工具列表 → MCP 可用
3. 如果服务不存在或工具列表为空 → MCP 不可用，走降级方案

---

## 组合 1：语言查询

### GetLanguageInfoMcp

获取当前项目的语言配置信息，返回原始语言和目标翻译语言列表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _(无参数)_ | — | — | 无需传入参数 |

**用途**：在流程开始前调用，确认用户想要翻译的目标语言列表。

---

## 组合 2：图片上传

将项目中需要处理的图片打包为 zip 文件，通过三步分片上传到服务端。上传完成后获得的 `file_id` 是后续所有操作（OCR、术语表、翻译）的核心标识。

### ⛔ 上传方式：必须使用 `upload-images.js` 脚本，严禁 AI 自行上传

> **🚫🚫🚫 绝对红线：AI 不得以任何方式自行处理图片上传，包括 zip 压缩、base64 编码、分片上传。违反此规则将导致流程失败。**

**严禁 AI 自行执行图片上传的任何步骤，包括但不限于：**
- ❌ 自行创建 zip 压缩包（不要用 `zip` 命令、不要用 Node.js 的 archiver/yazl 等库）
- ❌ 自行读取图片文件的二进制内容并做 base64 编码
- ❌ 自行调用 `UploadScanFilesInitMcp` / `UploadScanFilesPartMcp` / `UploadScanFilesCompleteMcp` 等 MCP 分片上传接口
- ❌ 自行编写或执行任何分片上传逻辑
- ❌ 通过 `mcp_call_tool` 直接调用上传相关的 MCP 工具
- ❌ 自行编写任何 Node.js/Python/Shell 脚本来处理 zip 打包或分片上传
- ❌ 尝试用 `Buffer`、`fs.readFileSync`、`base64` 等方式读取图片二进制数据
- ❌ 在任何情况下尝试"优化"或"替代"上传脚本的功能

**为什么 AI 绝对不能自行处理上传：**
1. 图片是二进制文件，AI 无法正确处理二进制数据的 base64 编码（token 限制、编码错误）
2. 分片逻辑涉及精确的字节切分和 etag 追踪，AI 执行这些操作必然出错
3. zip 打包需要精确的二进制操作，AI 生成的 zip 包格式不正确
4. **已有现成的 `upload-images.js` 脚本完美处理了所有这些工作**，AI 只需执行一行命令

**唯一正确做法**：使用 `scripts/upload-images.js` 辅助脚本在本地直接通过 HTTP 调用 MCP 接口完成上传。该脚本封装了完整的 zip 打包、MCP 配置读取、分片上传、结果输出全流程。

**调用方式**：
```bash
# 指定图片列表
node scripts/upload-images.js --project <projectRoot> --images "assets/img/btn.png,assets/img/title.png"

# 使用图片列表文件（每行一个相对路径）
node scripts/upload-images.js --project <projectRoot> --images-file i18n/image_list.txt

# 输出 file_id 到指定文件
node scripts/upload-images.js --project <projectRoot> --images-file i18n/image_list.txt --output i18n/upload_result.json
```

**脚本功能**：
1. 自动从多个 IDE 配置路径读取 MCP 配置（APPID、TOKEN、URL），按优先级依次尝试 `~/.workbuddy/mcp.json`、`~/.codebuddy/mcp.json`、`~/.cursor/mcp.json`、`~/.claude/mcp.json`、`~/.codex/mcp.json`
2. 按 MCP 要求的 zip 目录结构打包图片（`data.json` + `files/`）
3. 自动完成 Init → Part × N → Complete 三步分片上传
4. 输出 `file_id` 到 `i18n/upload_result.json`，供后续 OCR/翻译步骤使用
5. stdout 最后一行输出 `__FILE_ID__=<id>` 供 AI 直接捕获

**`upload_result.json` 输出格式**：
```json
{
  "fileId": 18,
  "timestamp": "2026-04-08T12:46:03.290Z",
  "imageCount": 1,
  "images": [
    "assets/Images/btn_start.png"
  ]
}
```

**AI 执行流程**：
1. 将需要上传的图片相对路径写入列表文件 `i18n/image_list.txt`
2. 执行 `node scripts/upload-images.js --project <root> --images-file i18n/image_list.txt`
3. 从命令输出中捕获 `__FILE_ID__=<id>` 获取 file_id
4. 后续使用 `mcp_call_tool` 调用 OCR/术语表/翻译接口时传入该 file_id

---

## 组合 3：OCR 识别

对已上传的图片执行文字识别。需传入上传时获得的 `file_id`。

### OCR 流程

```
StartImageOcrMcp        →  启动 OCR 任务
        ↓
GetImageOcrProgressMcp  →  轮询进度（status: 1=运行中, 2=成功, 3=失败）
        ↓
GetImageOcrResultMcp    →  获取识别结果（文本内容 + 位置信息）
```

### StartImageOcrMcp — 启动 OCR

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 分片上传完成后的文件 ID |

### GetImageOcrProgressMcp — 查询 OCR 进度

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 文件 ID |

**返回值**：

| 字段 | 说明 |
|------|------|
| `status` | `1` = 运行中，`2` = 成功，`3` = 失败 |
| `progress` | 进度详情对象 |

`progress` 对象：

| 字段 | 类型 | 说明 |
|------|------|------|
| `count` | integer | 已完成数量 |
| `total` | integer | 总数量 |
| `progress` | integer | 进度百分比（0-100） |
| `predict_time` | integer | 预计剩余秒数，完成时为 0 |

**实际返回示例**：
```json
{"progress":{"count":2,"total":2,"progress":100,"predict_time":0},"status":2}
```

**轮询策略**：间隔 5 秒，最多 60 次（5 分钟超时）。

### GetImageOcrResultMcp — 获取 OCR 结果

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 文件 ID |

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `ocr_items` | array | OCR 识别结果列表 |

`ocr_items` 每个元素：

| 字段 | 类型 | 说明 |
|------|------|------|
| `text` | string | 识别出的文本内容（多行文本用 `\n` 分隔） |
| `locations` | string[] | 该文本所在的图片路径列表（相对于上传 zip 中 `files/` 目录的路径） |

**实际返回示例**：
```json
{
  "ocr_items": [
    {
      "text": "如约出行\n广州交通贴身向导\n点击使用实时公交小程序",
      "locations": [
        "upload_image_example/files/assets/Images/99FBB9A2...80B0.png"
      ]
    }
  ]
}
```

仅在 OCR 任务成功（status=2）后调用。

---

## 组合 4：术语表上传

在图片翻译前上传专业术语对照表，约束翻译用词，提升翻译准确性。需传入上传时获得的 `file_id`。

### UploadTermDataMcp

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 关联的图片文件 ID |
| `target_lang` | string[] | ✅ | 目标翻译语言列表，如 `["en", "ja", "ko"]` |
| `text_items` | array | ✅ | 术语文本列表 |

`text_items` 每个元素：

| 字段 | 类型 | 说明 |
|------|------|------|
| `text` | string | 原始文本（源语言） |
| `translate_text` | string[] | 各目标语言的翻译，顺序与 `target_lang` 一一对应 |

**示例**：
```json
{
  "file_id": 12345,
  "target_lang": ["en", "ko"],
  "text_items": [
    {
      "text": "金币",
      "translate_text": ["Gold", "골드"]
    },
    {
      "text": "开始游戏",
      "translate_text": ["Start Game", "게임 시작"]
    }
  ]
}
```

---

## 组合 5：图片翻译

对已上传的图片执行翻译重绘。需传入上传时获得的 `file_id`。

### 翻译流程

```
StartImageTranslateMcp        →  启动翻译任务
        ↓
GetImageTranslateProgressMcp  →  轮询进度（status: 1=运行中, 2=成功, 3=失败）
        ↓
GetImageTranslateResultMcp    →  获取翻译后图片的下载链接
```

### StartImageTranslateMcp — 启动翻译

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 分片上传完成后的文件 ID |

### GetImageTranslateProgressMcp — 查询翻译进度

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 文件 ID |

**返回值**：

| 字段 | 说明 |
|------|------|
| `status` | `1` = 运行中，`2` = 成功，`3` = 失败 |
| `progress` | 进度详情对象 |

`progress` 对象（与 OCR 进度结构相同）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `count` | integer | 已完成数量 |
| `total` | integer | 总数量（= 目标语言数 × 图片数 + 其他处理步骤） |
| `progress` | integer | 进度百分比（0-100） |
| `predict_time` | integer | 预计剩余秒数，完成时为 0 |

**实际返回示例**：
```json
{"progress":{"count":3,"total":3,"progress":100,"predict_time":0},"status":2}
```

**轮询策略**：间隔 10 秒，最多 60 次（10 分钟超时）。

### GetImageTranslateResultMcp — 获取翻译结果

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | integer | ✅ | 文件 ID |

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `url` | string | 翻译后 zip 文件的下载 URL（带签名，有效期约 72 小时） |

**实际返回示例**：
```json
{
  "url": "https://wxagl10n-40068.sh.gfp.tencent-cloud.com/translate/data_translate_74/v0?sign=..."
}
```

仅在翻译任务成功（status=2）后调用。

### 翻译结果 zip 目录结构

下载的 zip 解压后，目录结构如下：

```
<解压根目录>/
├── translate_text_map.csv        # 文本翻译映射表（CSV，含表头 key,zh_CN,ko,en 等）
├── translate_image_map.csv       # 图片翻译映射表（CSV，含表头 key,zh_CN,ko,en 等）
├── en/                           # 英文翻译图片目录
│   └── <上传时的相对路径>/
│       └── <原始图片文件名>.png   # 英文版翻译重绘图片
├── ko/                           # 韩文翻译图片目录（如有）
│   └── <上传时的相对路径>/
│       └── <原始图片文件名>.png
└── zh_CN/                        # 中文原图目录
    └── <上传时的相对路径>/
        └── <原始图片文件名>.png   # 中文原图副本
```

**实际示例**（file_id=18 测试结果）：

```
test_translated_output/
├── translate_text_map.csv                    # 表头: key,zh_CN,ko,en
├── translate_image_map.csv                   # 表头: key,zh_CN,ko,en
├── en/
│   └── upload_image_example/files/assets/Images/
│       └── 99FBB9A2...80B0.png              # 43.2 KB（英文翻译重绘）
└── zh_CN/
    └── upload_image_example/files/assets/Images/
        └── 99FBB9A2...80B0.png              # 22.1 KB（中文原图）
```

**关键说明**：
- 翻译图片按 `{语言代码}/{上传时图片的完整相对路径}` 组织
- `zh_CN/` 目录包含原图副本，可用于对比验证
- CSV 映射表包含表头行（`key,zh_CN,ko,en,...`），数据行为翻译对照（可能为空）
- 并非所有目标语言都一定会产出翻译图片，取决于服务端对图片内容的分析结果
- 翻译后图片通常比原图大（因为重绘后包含新的文字渲染）

### AI 处理翻译结果的流程

1. **下载 zip**：使用 `GetImageTranslateResultMcp` 返回的 URL 下载
2. **解压**：解压到 `{projectRoot}/i18n/translated_output/` 或 `i18n/assets/` 目录
3. **遍历语言目录**：对每个 `{lang}/` 子目录，提取翻译后的图片
4. **映射回项目路径**：翻译图片路径中包含了上传时的相对路径，需要去掉上传脚本添加的路径前缀，还原为项目中的实际资源路径
5. **更新 image_translations.json**：将下载到的图片路径填入 `targetFile` 字段，`status` 设为 `completed`

**路径还原示例**：
```
翻译结果路径:  en/upload_image_example/files/assets/Images/btn.png
上传时路径:    upload_image_example/files/assets/Images/btn.png
项目实际路径:  assets/Images/btn.png  (去掉 upload-images.js 添加的前缀)
目标存放路径:  i18n/assets/en/assets/Images/btn.png
```

---

## 完整调用流程

### 标准流程（OCR + 翻译）

```
1. GetLanguageInfoMcp                    → 获取目标语言列表
2. node scripts/upload-images.js         → ⛔ 必须且只能使用脚本上传图片，获得 file_id
   （脚本自动完成 zip 打包 + 分片上传全流程，AI 不要自行处理 zip/base64/分片）
3. UploadTermDataMcp                     → 上传术语表（可选，使用 mcp_call_tool 调用）
4. StartImageOcrMcp                      → 启动 OCR（使用 mcp_call_tool 调用）
5. GetImageOcrProgressMcp × N            → 轮询 OCR 进度（使用 mcp_call_tool 调用）
6. GetImageOcrResultMcp                  → 获取 OCR 结果（使用 mcp_call_tool 调用）
7. StartImageTranslateMcp                → 启动图片翻译（使用 mcp_call_tool 调用）
8. GetImageTranslateProgressMcp × N      → 轮询翻译进度（使用 mcp_call_tool 调用）
9. GetImageTranslateResultMcp            → 获取翻译结果下载链接（使用 mcp_call_tool 调用）
```

**关键区分**：
- **步骤 2（图片上传）**：必须且只能通过 `scripts/upload-images.js` 脚本在终端执行。**绝对不能**通过 `mcp_call_tool` 调用上传接口，也不能自行编写 zip 打包或 base64 分片逻辑
- **步骤 3-9（术语表/OCR/翻译）**：通过 `mcp_call_tool` 正常调用 MCP 接口即可，传入脚本返回的 `file_id`

### 仅 OCR 流程

执行步骤 1-6 即可。

### 仅翻译流程（已有 OCR 结果）

执行步骤 1-3，然后跳到步骤 7-9。

---

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| MCP 服务无响应 | 降级到手动模式，标记 `pending_manual` |
| 上传脚本执行失败 | 检查 MCP 配置是否正确（APPID/TOKEN/URL），重试 1 次 |
| OCR 超时（> 5 分钟） | 记录超时图片，标记 `ocr_timeout`，继续文本翻译 |
| OCR 失败（status=3） | 标记 `ocr_failed`，继续文本翻译 |
| 翻译失败（status=3） | 标记 `translate_failed`，继续文本翻译 |
| 下载失败 | 重试 3 次，仍失败标记 `download_failed` |

## AI 执行调用流程

### 标准流程

```
1. mcp_get_tool_description           → 获取实际工具列表和参数
2. node scripts/upload-images.js      → ⛔ 必须且只能使用脚本上传图片，获得 file_id
   （绝对禁止自行创建 zip、读取图片二进制、base64 编码、调用分片上传 MCP 接口）
3. mcp_call_tool: UploadTermDataMcp   → 上传术语表（可选）
4. mcp_call_tool: StartImageOcrMcp    → 触发 OCR
5. mcp_call_tool: GetImageOcrProgressMcp → 轮询 OCR 结果（每 5 秒一次，最多 60 次）
6. mcp_call_tool: GetImageOcrResultMcp   → 获取 OCR 结果
7. mcp_call_tool: StartImageTranslateMcp → 触发图片翻译
8. mcp_call_tool: GetImageTranslateProgressMcp → 轮询翻译进度（每 10 秒一次，最多 60 次）
9. mcp_call_tool: GetImageTranslateResultMcp   → 获取翻译结果下载链接
10. 下载翻译后的图片 zip
```

> ⛔ **再次强调**：步骤 2 只允许执行 `node scripts/upload-images.js` 命令。如果脚本执行失败，应检查脚本报错信息并修复问题后重试，**绝对不能**尝试自行实现上传逻辑作为"替代方案"。

### 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| MCP 服务无响应 | 降级到手动模式，标记 `pending_manual` |
| 上传脚本执行失败 | 检查 MCP 配置是否正确（APPID/TOKEN/URL），重试 1 次 |
| OCR 超时（> 5 分钟） | 记录已超时的图片，标记 `ocr_timeout`，继续文本翻译 |
| 翻译失败（部分图片） | 已完成的标记 `completed`，失败的标记 `failed`，继续流程 |
| 下载失败 | 重试 3 次，仍失败标记 `download_failed` |

### 轮询策略

```
OCR 轮询: 间隔 5 秒，最大 60 次（5 分钟超时）
翻译轮询: 间隔 10 秒，最大 60 次（10 分钟超时）
```

## 无 MCP 时的降级方案

如果 MCP 图片翻译服务不可用（服务未配置、网络不通、工具列表为空），采用以下降级策略：

1. **跳过图片翻译**：不阻塞文本翻译流程
2. **手动标记**：在 `image_translations.json` 中标记所有需要翻译的图片，`status` 设为 `pending_manual`
3. **提示用户**：在最终摘要中告知用户哪些图片包含文字需要手动处理
4. **生成替换清单**：用户可以使用其他工具翻译后手动放入对应目录

```json
{
  "key": "img_abc123",
  "sourceFile": "assets/images/start_btn.png",
  "expectedTargetFile": "i18n/assets/en/start_btn.png",
  "ocrText": null,
  "status": "pending_manual",
  "method": "manual",
  "note": "MCP 图片翻译服务不可用，需手动处理"
}
```
