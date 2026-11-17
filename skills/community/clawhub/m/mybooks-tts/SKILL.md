---
name: mybooks_tts
homepage: https://www.mybooks.top
allowed-tools: Bash(python3:*)
metadata: {"clawdbot":{},"openclaw":{"requires":{"bins":["python3"],"env":["MYBOOKS_HOST","MYBOOKS_USER","MYBOOKS_PASSWORD"]}}}
description: "MyBooks(PoxenStudio/Talebook)的MiMo TTS有声书工具，支持将EPUB电子书转换为有声书。你可以帮助用户：配置TTS API（MiMo或OpenAI兼容）、测试API连接、开始EPUB转有声书、查询转换进度、管理克隆音色库（上传/列表/删除/试听）、管理自定义语音提示词库（保存/列表/删除）等。所有操作需要管理员权限。"
---

# MyBooks TTS (MiMo TTS 有声书工具)

## Requirements
```bash
# 需要配置以下环境变量后方可使用
export MYBOOKS_HOST="http://127.0.0.1:8082"
export MYBOOKS_USER="admin"
export MYBOOKS_PASSWORD="your_password"
export MYBOOKS_SSL_VERIFY="false"   # 如服务器使用自签名证书，设为 false

然后按如下方式执行：
<skill-installation-path>/scripts/mybooks_tts_api.py <tool-name> '<json-args>'
```

> **安全提示**：请勿将凭据写入共享或全局配置文件（如 `~/.openclaw/.env`），以避免凭据被其他 agent 或进程意外读取。建议通过会话级环境变量或专用密钥管理工具传入凭据。

## 通用响应格式与认证方式

### 通用 JSON 响应结构
所有 API 均返回如下格式：
```json
{
  "err": "ok",       // "ok" 表示成功，其他字符串表示错误码
  "msg": "...",      // 可选，人类可读的成功/错误说明
  "data": { }        // 可选，具体响应数据（因接口而异）
}
```

常见错误码：
| `err` 值 | 含义 |
|----------|------|
| `"ok"` | 操作成功 |
| `"user.need_login"` | 未登录或登录态已过期 |
| `"permission"` | 无权限（需管理员） |
| `"params.invalid"` | 请求参数错误 |
| `"params.book.invalid"` | 书籍不存在或 ID 错误 |
| `"task.running"` | 后台任务正在进行中，稍后重试 |
| `"tts.converting"` | TTS 转换任务正在运行 |
| `"tts.no_config"` | 未配置 API |
| `"clone.exists"` | 克隆音色名称已存在 |
| `"clone.not_found"` | 克隆音色不存在 |
| `"clone.too_large"` | 文件超过 7MB 限制 |
| `"clone.invalid_format"` | 仅支持 MP3/WAV 格式 |
| `"prompt.exists"` | 提示词名称已存在 |
| `"prompt.not_found"` | 提示词不存在 |

### 认证方式
- 脚本通过 `MYBOOKS_USER` / `MYBOOKS_PASSWORD` 环境变量自动调用 `/api/user/sign_in` 完成登录
- 服务端通过 **Secure Cookie**（`user_id` + `lt`）维持会话
- 若响应中出现 `err=user.need_login`，脚本会自动重新登录后重试一次；仍失败则报错退出
- **必须**在调用前配置 `MYBOOKS_HOST`、`MYBOOKS_USER`、`MYBOOKS_PASSWORD` 三个环境变量，否则脚本直接报错退出
- 所有 TTS 接口均需要**管理员权限**

---

## 工具列表

### `tts_save_config` — 保存 TTS API 配置

**使用场景**：配置 TTS API 的连接参数（API URL、模型、密钥、类型等），保存后服务端加密存储

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `api_url` | string | ✅ | API 地址，如 `https://api.xiaomimimo.com/v1/chat/completions` |
| `model_name` | string | ✅ | 模型 ID，MiMo TTS 类型固定为 `mimo-v2.5-tts` |
| `api_type` | string | ✅ | API 类型：`chat_completions`（MiMo TTS）/ `audio_speech`（OpenAI 兼容）/ `custom` |
| `api_key` | string | ✅ | API 密钥 |
| `auth_type` | string | ❌ | 认证类型：`bearer`（默认）/ `basic` / `custom` |
| `voice_name` | string | ❌ | 预置音色 ID（`api_type=chat_completions` 且 `voiceType=preset` 时）或 `audio_speech` 的音色名 |
| `voice_desc` | string | ❌ | 自定义音色描述（`voiceType=custom` 时） |
| `clone_voice` | string | ❌ | 克隆音色名称（`voiceType=clone` 时） |

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_save_config '{"api_url":"https://api.xiaomimimo.com/v1/chat/completions","model_name":"mimo-v2.5-tts","api_type":"chat_completions","api_key":"sk-xxx","voice_name":"mimo_default"}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "配置已保存"
}
```

---

### `tts_test_connection` — 测试 API 连接

**使用场景**：使用当前保存的配置发送一次测试请求，验证 API Key 和端点是否可用

**权限**：管理员

**参数**：无（使用已保存的配置）

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_test_connection '{}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "连接成功"
}
```

**常见错误**：
| `err` 值 | 含义 |
|----------|------|
| `"tts.no_config"` | 未保存配置，请先调用 `tts_save_config` |
| `"tts.connection_failed"` | 无法连接到 API 服务器 |
| `"tts.invalid_key"` | API Key 无效 |

---

### `tts_convert` — 开始 EPUB 转有声书

**使用场景**：将指定 EPUB 电子书转换为有声书，后台逐章合成 WAV 音频

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `book_id` | int | ✅ | 书籍 ID |
| `api_url` | string | ✅ | API 地址 |
| `model_name` | string | ✅ | 模型 ID |
| `api_type` | string | ✅ | API 类型：`chat_completions` / `audio_speech` / `custom` |
| `api_key` | string | ✅ | API 密钥 |
| `auth_type` | string | ❌ | 认证类型（默认 `bearer`） |
| `voice_name` | string | ❌ | 预置音色 ID 或 `audio_speech` 音色名 |
| `voice_desc` | string | ❌ | 自定义音色描述 |
| `clone_voice` | string | ❌ | 克隆音色名称 |

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_convert '{"book_id":42,"api_url":"https://api.xiaomimimo.com/v1/chat/completions","model_name":"mimo-v2.5-tts","api_type":"chat_completions","api_key":"sk-xxx","voice_name":"mimo_default"}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "转换任务已启动"
}
```

**常见错误**：
| `err` 值 | 含义 |
|----------|------|
| `"params.book.invalid"` | 书籍不存在 |
| `"tts.converting"` | 已有转换任务在运行 |
| `"book.no_epub"` | 书籍没有 EPUB 格式 |

---

### `tts_progress` — 查询转换进度

**使用场景**：查询当前 TTS 转换任务的进度、阶段和章节信息

**权限**：管理员

**参数**：无

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_progress '{}'
```

**响应示例**：
```json
{
  "err": "ok",
  "status": "running",
  "progress": 35,
  "stage": "converting",
  "current_chapter": 7,
  "total_chapters": 20,
  "current_title": "第七章 归途",
  "book_id": 42
}
```

**status 值**：
| 值 | 含义 |
|----|------|
| `"idle"` | 无任务运行 |
| `"running"` | 转换进行中 |
| `"completed"` | 转换已完成 |
| `"failed"` | 转换失败 |

---

### `tts_clone_upload` — 上传克隆音色

**使用场景**：上传 MP3/WAV 音频样本作为克隆音色，上传后自动切换到 `mimo-v2.5-tts-voiceclone` 模型

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `voice_name` | string | ✅ | 克隆音色名称（如"旁白"、"男主"） |
| `file_path` | string | ✅ | 本地音频文件的绝对路径（MP3/WAV，≤7MB） |

**限制**：
- 格式：仅支持 `.mp3` 和 `.wav`
- 大小：原始文件 ≤ 7MB（Base64 编码后约 9.3MB，MiMo 官方限制 Base64 ≤ 10MB）

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_clone_upload '{"voice_name":"旁白","file_path":"/path/to/sample.mp3"}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "克隆音色上传成功",
  "data": { "name": "旁白", "ext": "mp3", "size": 1048576 }
}
```

**常见错误**：
| `err` 值 | 含义 |
|----------|------|
| `"clone.exists"` | 音色名称已存在 |
| `"clone.too_large"` | 文件超过 7MB |
| `"clone.invalid_format"` | 格式不支持 |

---

### `tts_clone_list` — 克隆音色列表

**使用场景**：获取所有已上传的克隆音色列表

**权限**：管理员

**参数**：无

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_clone_list '{}'
```

**响应示例**：
```json
{
  "err": "ok",
  "clones": [
    { "name": "旁白", "ext": "mp3", "size": 1048576 },
    { "name": "男主", "ext": "wav", "size": 2097152 }
  ]
}
```

---

### `tts_clone_delete` — 删除克隆音色

**使用场景**：删除指定的克隆音色

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `voice_name` | string | ✅ | 要删除的克隆音色名称 |

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_clone_delete '{"voice_name":"旁白"}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "克隆音色已删除"
}
```

---

### `tts_clone_audio` — 下载克隆音频

**使用场景**：下载/试听指定的克隆音色原始音频文件（返回二进制 WAV 数据）

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `voice_name` | string | ✅ | 克隆音色名称 |
| `save_to` | string | ❌ | 保存到本地路径（不传则返回 base64） |

**执行脚本**：
```bash
# 保存到文件
<skill-installation-path>/scripts/mybooks_tts_api.py tts_clone_audio '{"voice_name":"旁白","save_to":"/tmp/clone_preview.wav"}'

# 返回 base64（小文件）
<skill-installation-path>/scripts/mybooks_tts_api.py tts_clone_audio '{"voice_name":"旁白"}'
```

**响应示例**（保存到文件）：
```json
{
  "err": "ok",
  "msg": "音频已保存",
  "path": "/tmp/clone_preview.wav",
  "size": 1048576
}
```

---

### `tts_prompt_list` — 提示词列表

**使用场景**：获取所有已保存的自定义语音提示词

**权限**：管理员

**参数**：无

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_prompt_list '{}'
```

**响应示例**：
```json
{
  "err": "ok",
  "prompts": [
    { "name": "温柔女声", "desc": "温柔细腻的语调，语速偏慢，咬字清晰" },
    { "name": "沉稳男声", "desc": "沉稳厚重的语调，语速适中偏低" }
  ]
}
```

---

### `tts_prompt_save` — 保存提示词

**使用场景**：将自定义音色描述保存为提示词（同名覆盖），存储于服务端 `voice_prompts.json`

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 提示词名称 |
| `desc` | string | ✅ | 音色描述（自然语言描述语音特征） |

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_prompt_save '{"name":"温柔女声","desc":"温柔细腻的语调，语速偏慢，咬字清晰，富有亲和力"}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "提示词已保存"
}
```

---

### `tts_prompt_delete` — 删除提示词

**使用场景**：删除指定的语音提示词

**权限**：管理员

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 要删除的提示词名称 |

**执行脚本**：
```bash
<skill-installation-path>/scripts/mybooks_tts_api.py tts_prompt_delete '{"name":"温柔女声"}'
```

**响应示例**：
```json
{
  "err": "ok",
  "msg": "提示词已删除"
}
```

---

## 使用场景决策指南

```
用户请求
│
├─ "配置 TTS API" / "设置 MiMo API Key"
│   → tts_save_config
│
├─ "测试 API 能不能用" / "连接正常吗"
│   → tts_test_connection
│
├─ "把这本书转成有声书" / "开始转换"
│   → tts_convert（需先有配置或直接传参）
│
├─ "转换到哪了" / "进度怎么样"
│   → tts_progress
│
├─ "上传克隆音色" / "我想用自己的声音"
│   → tts_clone_upload
│
├─ "有哪些克隆音色" / "看看上传的音色"
│   → tts_clone_list
│
├─ "删除克隆音色" / "不要这个音色了"
│   → tts_clone_delete
│
├─ "试听克隆音色" / "下载克隆音频"
│   → tts_clone_audio
│
├─ "有哪些提示词" / "保存的音色描述"
│   → tts_prompt_list
│
├─ "保存这个音色描述" / "存一个提示词"
│   → tts_prompt_save
│
└─ "删除提示词" / "不要这个描述了"
    → tts_prompt_delete
```

---

## 预置音色参考

MiMo TTS 类型（`api_type=chat_completions`）内置 9 个预置音色：

| ID | 名称 | 语言 | 性别 |
|----|------|------|------|
| `mimo_default` | MiMo-默认 | 中文 | 女 |
| `冰糖` | 冰糖 | 中文 | 女 |
| `茉莉` | 茉莉 | 中文 | 女 |
| `苏打` | 苏打 | 中文 | 男 |
| `白桦` | 白桦 | 中文 | 男 |
| `Mia` | Mia | 英文 | 女 |
| `Chloe` | Chloe | 英文 | 女 |
| `Milo` | Milo | 英文 | 男 |
| `Dean` | Dean | 英文 | 男 |

---

## 错误处理规范

| `err` 值 | 含义 | 建议处理 |
|----------|------|----------|
| `"ok"` | 操作成功 | 展示结果 |
| `"user.need_login"` | 未登录 | 脚本自动重登录，仍失败则检查环境变量 |
| `"permission"` | 非管理员 | 说明当前账号权限不足 |
| `"params.book.invalid"` | 书籍不存在 | 建议用搜索确认 book_id |
| `"task.running"` / `"tts.converting"` | 任务进行中 | 等待完成后重试 |
| `"tts.no_config"` | 未配置 | 先调用 `tts_save_config` |
| `"clone.too_large"` | 文件超限 | 提示用户裁剪音频至 7MB 内 |
| `"clone.invalid_format"` | 格式不支持 | 仅支持 MP3/WAV |
| `"clone.exists"` | 名称重复 | 换名或先删除旧的 |

---

## 注意事项

1. **管理员权限**：所有 TTS 接口均需要管理员权限，普通用户无法使用。
2. **异步转换**：`tts_convert` 启动后台任务后立即返回，需用 `tts_progress` 轮询进度。
3. **断点续传**：重复转换同一本书时，自动跳过已存在的 WAV 文件（≥44 字节），中断后可继续。
4. **音频输出**：转换完成后，音频输出到 `/audio/{book_id}` 页面播放，也可通过 Web 界面访问。
5. **克隆音色限制**：MP3/WAV ≤ 7MB；上传后自动切换 `mimo-v2.5-tts-voiceclone` 模型。
6. **提示词存储**：提示词保存在服务端 `voice_prompts.json`，跨浏览器共享，不依赖本地存储。
7. **API Key 加密**：API Key 经 PBKDF2-SHA256 + 流加密保存，密钥文件权限 0o600。
8. **模型锁定**：MiMo TTS 类型下模型 ID 固定为 `mimo-v2.5-tts`，不可修改；`audio_speech` 和 `custom` 类型可自由修改。
