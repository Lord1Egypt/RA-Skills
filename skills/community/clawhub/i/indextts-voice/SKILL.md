---
name: indextts-voice
description: IndexTTS 语音克隆和合成技能 - 创建声音模型、文本转语音、参考音频管理（需要企业会员）
triggers:
  - 语音合成
  - 声音克隆
  - TTS
  - indextts
  - 文本转语音
  - 声音模型
  - 参考音频
---

# IndexTTS 语音克隆与合成技能

> [!IMPORTANT]
> ## ⚠️ 企业会员专属技能
> 
> **本技能需要 IndexTTS 企业会员才能使用**
> 
> | 项目 | 说明 |
> |------|------|
> | **API 签名** | 仅企业会员可获得 |
> | **官方网站** | [https://indextts.cn](https://indextts.cn) |
> | **购买方式** | 访问官网 → 会员中心 → 购买企业会员 |
> | **免费替代** | 使用 [网页版](https://indextts.cn) 进行声音克隆和语音合成（无需 API） |
> | **价格咨询** | 请访问官网或联系客服 |
> 
> **未购买企业会员请勿安装此技能！**

## 技能描述
IndexTTS 是一个专业的语音克隆和语音合成 API 服务。本技能提供完整的命令行接口，支持声音模型管理、异步语音合成、参考音频管理、配额查询等核心功能。

## 适用场景
- 创建声音克隆模型（基于 2-60 秒的音频样本）
- 管理已创建的语音模型（列表查询、详情、删除）
- 使用克隆的声音进行文本转语音（TTS）
- 上传/管理语调参考音频（用于情感合成，24 小时有效）
- 查询合成任务状态和下载音频
- 查询用户剩余配额/额度

## 环境要求
- Python 3.6+
- requests 库
- **需要设置环境变量 `INDEX_API_SIGN`（API 签名，需企业会员）**

## 安装依赖
```bash
pip install requests
```

## 配置环境变量

### Windows PowerShell
```powershell
$env:INDEX_API_SIGN='你的 API 签名'
$env:INDEX_BASE_URL='https://openapi.lipvoice.cn'
```

### Windows CMD
```cmd
set INDEX_API_SIGN=你的 API 签名
set INDEX_BASE_URL=https://openapi.lipvoice.cn
```

### 永久设置（推荐）
将环境变量添加到系统环境变量中，或写入脚本自动加载。

## API 签名获取

> 📌 **企业会员专属**
> 
> API 签名是 IndexTTS 企业会员的专属功能，用于通过 API 调用语音合成服务。
> 
> **获取步骤：**
> 1. 访问 [https://indextts.cn](https://indextts.cn)
> 2. 注册/登录账户
> 3. **购买企业会员服务**（在会员中心）
> 4. 进入「开发者中心」或「API 管理」
> 5. 复制 API 签名/密钥
> 
> **价格咨询：** 请访问 IndexTTS 官网查看企业会员价格
> 
> **免费替代方案：** 如不需要 API 调用，可直接使用网页版进行声音克隆和语音合成。

---

## 命令参考

### 一、声音模型管理

#### 1. 创建声音模型
```bash
python scripts/indextts_api.py create-model "模型名称" "音频文件路径" [--describe "描述"]
```

**参数说明：**
- `模型名称` - 自定义模型名称（必需）
- `音频文件路径` - MP3/WAV/M4A 格式，<50MB，时长 2-60 秒（必需）
- `--describe` - 模型描述（可选）

**示例：**
```powershell
python scripts/indextts_api.py create-model "我的旁白声" "C:/Users/yanyu/Desktop/voice.wav" --describe "温暖男声"
```

**返回：**
```json
{
  "code": 0,
  "data": {
    "audioId": "ABuVg22s3ydwS7RtkVyVN86Egq",
    "name": "我的旁白声",
    "describe": "温暖男声"
  },
  "msg": "成功"
}
```

---

#### 2. 查询模型列表
```bash
python scripts/indextts_api.py list-models [--page 1] [--page-size 10]
```

**参数说明：**
- `--page` - 页码，默认 1
- `--page-size` - 每页条数，默认 10，最大 20

**示例：**
```powershell
python scripts/indextts_api.py list-models --page 1 --page-size 20
```

---

#### 3. 查询模型详情
```bash
python scripts/indextts_api.py get-model <audioId>
```

**参数说明：**
- `audioId` - 模型 ID（从 list-models 获取）

**示例：**
```powershell
python scripts/indextts_api.py get-model ABuVg22s3ydwS7RtkVyVN86Egq
```

**注意：** 此接口可能未在所有账户中开放，如返回 404 请使用网页版查看模型详情。

---

#### 4. 删除模型
```bash
python scripts/indextts_api.py delete-model <audioId>
```

**参数说明：**
- `audioId` - 模型 ID（必需）
- **注意：** 删除后数据不可恢复

**示例：**
```powershell
python scripts/indextts_api.py delete-model ABuVg22s3ydwS7RtkVyVN86Egq
```

---

### 二、语调参考音频管理（用于情感合成）

**重要说明：**
- 参考音频用于 `genre=1`（语气参考）模式下的情感语音合成
- 上传的参考音频仅保存 **24 小时**，过期自动清理
- 最多上传 **30 个** 参考音频，每个 < 50MB

#### 5. 上传参考音频
```bash
python scripts/indextts_api.py upload-tts-reference "音频文件路径"
```

**参数说明：**
- `音频文件路径` - MP3/WAV/M4A 格式，<50MB（必需）

**示例：**
```powershell
python scripts/indextts_api.py upload-tts-reference "C:/Users/yanyu/Desktop/emotion_sample.wav"
```

**返回：**
```json
{
  "code": 0,
  "data": {
    "file": {
      "emotionPath": "1cb251ec0d568de6a929b520c4aed8d1_20260401104924.wav"
    }
  },
  "msg": "上传成功"
}
```

---

#### 6. 查询参考音频列表
```bash
python scripts/indextts_api.py list-tts-references [--page 1] [--page-size 10]
```

**参数说明：**
- `--page` - 页码，默认 1
- `--page-size` - 每页条数，默认 10，最大 30

**示例：**
```powershell
python scripts/indextts_api.py list-tts-references
```

**返回：**
```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "emotionPath": "1cb251ec0d568de6a929b520c4aed8d1_20260401104924.wav",
        "name": "text.mp3",
        "createdAt": "2026-04-01T10:49:24.147+08:00"
      }
    ],
    "total": 1,
    "page": 1,
    "pageSize": 10
  },
  "msg": "获取成功"
}
```

---

#### 7. 删除参考音频
```bash
python scripts/indextts_api.py delete-tts-reference <emotionPath>
```

**参数说明：**
- `emotionPath` - 参考音频名称（从 list-tts-references 获取，必需）

**示例：**
```powershell
python scripts/indextts_api.py delete-tts-reference "1cb251ec0d568de6a929b520c4aed8d1_20260401104924.wav"
```

---

### 三、语音合成（TTS）

#### 8. 语音合成
```bash
python scripts/indextts_api.py tts-create "文本内容" <audioId> [选项]
```

**参数说明：**
- `文本内容` - 要合成的文字，最大 5000 字符（必需）
- `audioId` - 模型 ID（必需）
- `--style` - 模型版本：1=基础 (默认) 2=专业 3=多语言
- `--speed` - 语速：0.5-1.5，默认 1.0
- `--genre` - 模型类别（必需）
  - `0` = 参考原音频（默认，支持所有模型）
  - `1` = 语气参考模式（仅专业模型，使用情感参数）
  - `2` = 使用参考音频（仅专业模型，需要 emotionPath）
- `--emotion-path` - 参考音频路径（genre=2 时必需，从 list-tts-references 获取）
- `--happy` - 开心程度 (0-1，genre=1 时使用)
- `--angry` - 愤怒程度 (0-1，genre=1 时使用)
- `--sad` - 悲伤程度 (0-1，genre=1 时使用)
- `--afraid` - 恐惧程度 (0-1，genre=1 时使用)
- `--disgusted` - 厌恶程度 (0-1，genre=1 时使用)
- `--melancholic` - 忧郁程度 (0-1，genre=1 时使用)
- `--surprised` - 惊讶程度 (0-1，genre=1 时使用)
- `--calm` - 平静程度 (0-1，genre=1 时使用)

**示例：**
```powershell
# 基础合成（genre=0）
python scripts/indextts_api.py tts-create "你好，这是测试文本" ABuVg22s3ydwS7RtkVyVN86Egq

# 使用情感参数合成（genre=1，需要专业模型 style=2）
python scripts/indextts_api.py tts-create "太棒了！" ABuVg22s3ydwS7RtkVyVN86Egq `
  --style 2 --genre 1 --happy 0.8 --speed 1.1

# 使用参考音频合成（genre=2，需要先上传参考音频）
# 1. 先上传参考音频
python scripts/indextts_api.py upload-tts-reference "C:/Users/yanyu/Desktop/emotion.wav"

# 2. 查看参考音频列表，获取 emotionPath
python scripts/indextts_api.py list-tts-references

# 3. 使用参考音频进行合成（genre=2，自动使用 style=2）
python scripts/indextts_api.py tts-create "今天天气真好" ABuVg22s3ydwS7RtkVyVN86Egq `
  --genre 2 --emotion-path "1cb251ec0d568de6a929b520c4aed8d1_20260401104924.wav"
```

**返回：**
```json
{
  "code": 0,
  "data": {
    "taskId": "ABuVg22sQoSxZ7DFDTXqFP7dA9",
    "status": 1,
    "voiceUrl": ""
  },
  "msg": "成功"
}
```

---

#### 9. 查询合成任务列表
```bash
python scripts/indextts_api.py tts-list [--page 1] [--page-size 10]
```

**参数说明：**
- `--page` - 页码，默认 1
- `--page-size` - 每页条数，默认 10，最大 20

**示例：**
```powershell
python scripts/indextts_api.py tts-list --page 1 --page-size 20
```

---

#### 10. 查询合成任务结果
```bash
python scripts/indextts_api.py tts-result <taskId>
```

**参数说明：**
- `taskId` - 任务 ID（从 tts-create 获取）

**状态说明：**
- `1` - 处理中
- `2` - 已完成
- `3` - 失败

**示例：**
```powershell
python scripts/indextts_api.py tts-result ABuVg22sQoSxZ7DFDTXqFP7dA9
```

**返回（已完成）：**
```json
{
  "code": 0,
  "data": {
    "taskId": "ABuVg22sQoSxZ7DFDTXqFP7dA9",
    "status": 2,
    "voiceUrl": "https://openapi.lipvoice.cn/file/download/xxx.wav"
  },
  "msg": "成功"
}
```

---

#### 11. 下载合成音频
```bash
python scripts/indextts_api.py tts-download <taskId> <输出文件路径>
```

**参数说明：**
- `taskId` - 任务 ID（必需）
- `输出文件路径` - 保存的 WAV 文件路径（必需）

**示例：**
```powershell
python scripts/indextts_api.py tts-download ABuVg22sQoSxZ7DFDTXqFP7dA9 "C:/Users/yanyu/Desktop/output.wav"
```

**注意：** 此命令会自动查询任务状态并下载音频，如任务未完成会提示错误。

---

### 四、其他功能

#### 12. 查询用户配额
```bash
python scripts/indextts_api.py quota
```

**说明：** 查询剩余字符额度、已用额度等信息

**示例：**
```powershell
python scripts/indextts_api.py quota
```

**注意：** 此接口可能未在所有账户中开放，如返回 404 请登录网页版查看配额。

---

## API 接口文档

**官方文档**: https://indextts.cn/main/developer

**API 基础 URL**: `https://openapi.lipvoice.cn/api/third/`

**鉴权方式**: 所有接口需要在 Header 中传递 `sign` 参数，或在 URL params 中拼接 `sign`

### 声音模型接口

| 功能 | 方法 | 端点 | 命令 | 状态 |
|------|------|------|------|------|
| 创建模型 | POST | `/reference/upload` | `create-model` | ✅ 已验证 |
| 模型列表 | GET | `/reference/list` | `list-models` | ✅ 已验证 |
| 模型详情 | GET | `/reference/detail` | `get-model` | ⚠️ 部分账户可用 |
| 删除模型 | DELETE | `/reference/delete` | `delete-model` | ✅ 已验证 |

### 参考音频接口（24 小时有效）

| 功能 | 方法 | 端点 | 命令 | 状态 |
|------|------|------|------|------|
| 上传参考音频 | POST | `/tts/uploadCustom` | `upload-tts-reference` | ✅ 已验证 |
| 参考音频列表 | GET | `/tts/listCustom` | `list-tts-references` | ✅ 已验证 |
| 删除参考音频 | POST | `/tts/deleteCustom` | `delete-tts-reference` | ✅ 已验证 |

### 语音合成接口

| 功能 | 方法 | 端点 | 命令 | 状态 |
|------|------|------|------|------|
| 异步语音合成 | POST | `/tts/create` | `tts-create` | ✅ 已验证 |
| 任务列表 | GET | `/tts/list` | `tts-list` | ✅ 已验证 |
| 任务结果 | GET | `/tts/result` | `tts-result` | ✅ 已验证 |
| 下载音频 | GET | (voiceUrl) | `tts-download` | ✅ 已验证 |

### 用户接口

| 功能 | 方法 | 端点 | 命令 | 状态 |
|------|------|------|------|------|
| 用户配额 | GET | `/user/quota` | `quota` | ⚠️ 部分账户可用 |

---

### API 响应格式

所有接口返回统一的 JSON 格式：

```json
{
  "code": 0,          // 0=成功，7=异常
  "data": { ... },    // 返回数据
  "msg": "成功"       // 描述信息
}
```

### 错误码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 7 | 异常/错误（如 sign 无效、参数错误、资源不存在等） |

---

## 使用流程示例

### 完整 TTS 工作流

```powershell
# 1. 设置环境变量
$env:INDEX_API_SIGN = '你的 API 签名'
$env:INDEX_BASE_URL = 'https://openapi.lipvoice.cn'

# 2. 查看已有声音模型
python scripts/indextts_api.py list-models

# 3. 上传参考音频（用于情感合成）
python scripts/indextts_api.py upload-tts-reference "C:/Users/yanyu/Desktop/emotion.wav"

# 4. 查看参考音频列表，获取 emotionPath
python scripts/indextts_api.py list-tts-references

# 5. 使用参考音频进行情感合成
python scripts/indextts_api.py tts-create "今天天气真好！" ABuVg22s3ydwS7RtkVyVN86Egq --genre 1

# 6. 等待几秒后查询结果
Start-Sleep -Seconds 5
python scripts/indextts_api.py tts-result <taskId>

# 7. 下载合成音频
python scripts/indextts_api.py tts-download <taskId> "C:/Users/yanyu/Desktop/output.wav"
```

---

## 常见问题

### Q: 如何获取 API 签名？
A: 登录 IndexTTS 官网，进入开发者中心或个人中心复制 API 签名。

### Q: 音频文件有什么要求？
A: 
- **声音模型**: MP3/WAV/M4A，<50MB，时长 2-60 秒，清晰无噪音
- **参考音频**: MP3/WAV/M4A，<50MB，时长不限，用于情感参考

### Q: 合成的音频有效期多久？
A: 生成的音频文件有效期为 24 小时，请尽快下载保存。

### Q: 参考音频有效期多久？
A: 参考音频上传后保存 24 小时，过期自动清理，需要重新上传。

### Q: 最多可以上传多少个参考音频？
A: 最多 30 个。如超过限制，请先使用 `delete-tts-reference` 删除不需要的参考音频。

### Q: 情感参数怎么用？
A: 设置 `--genre 1` 启用语气参考模式，然后通过 `--happy`、`--angry` 等参数调整情感强度（0-1）。也可以先上传参考音频，系统会自动参考其情感。

### Q: 遇到 401 错误怎么办？
A: 检查 `INDEX_API_SIGN` 环境变量是否正确设置。

### Q: 遇到 404 错误怎么办？
A: 
- 确认 API 端点是否正确
- 部分接口（如模型详情、配额查询）可能未在所有账户中开放

---

## 更新日志

### v1.3.0 - 2026-04-20
- 🔧 修复元数据不一致问题：明确标注 INDEX_API_SIGN 为必需环境变量
- 🗑️ 移除飞书集成相关内容
- 📝 简化文档，专注于核心 IndexTTS API 功能

### v1.2.1 - 2026-04-02
- 🎯 品牌调整为 IndexTTS（indextts.cn）
- ✅ 更新所有文档和配置

### v1.2.0 - 2026-04-01
- ✅ 新增参考音频管理功能（上传/列表/删除）
- ✅ 修复所有 API 端点为正确路径
- ✅ 修复 `voiceUrl` 字段名问题
- ✅ 优化日志输出（Windows 控制台兼容）

### v1.1.0
- 新增 `get-model` 命令查询模型详情
- 新增 `tts-download` 命令直接下载合成音频
- 新增 `quota` 命令查询用户配额

### v1.0.0
- 初始版本，支持基础模型管理和 TTS 功能
