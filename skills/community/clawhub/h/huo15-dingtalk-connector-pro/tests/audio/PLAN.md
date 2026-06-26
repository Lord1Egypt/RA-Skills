# Audio 模块测试方案

## 1. 模块划分与职责

本套件覆盖音频相关的工具函数与发送逻辑：

- **isAudioFile(ext: string): boolean**：判断扩展名是否属于音频类型（大小写不敏感）。
- **getFfprobePath(): string**：优先使用 `@ffprobe-installer/ffprobe` 提供的路径；若不可用则读取 `FFPROBE_PATH`；再否则回退到 `'ffprobe'`。
- **extractAudioDuration(filePath: string, log): Promise<number \| null>**：通过 ffprobe 解析音频时长（秒）并转换为毫秒；异常/解析失败返回 null。
- **processAudioMarkers(content, accessToken, config, oapiToken, log)**：处理内容中的音频标记；缺 `oapiToken` 时原样返回并告警；标记 JSON 非法则移除并告警；文件不存在时给出提示并清理标记。
- **sendAudioMessage(...) / sendAudioProactive(...)**：发送音频消息（普通 webhook / 主动消息 API），支持 duration 传入与默认值。

## 2. 用例表（覆盖现有测试）

### 2.1 isAudioFile

| 序号 | 输入 | 期望 | 说明 |
|------|------|------|------|
| 1 | `mp3/wav/amr/ogg/aac/flac/m4a` | true | 音频扩展名 |
| 2 | 大写扩展名（如 `MP3`） | true | 大小写不敏感 |
| 3 | `mp4/txt/pdf/png/jpg/''` | false | 非音频 |

### 2.2 getFfprobePath

| 序号 | 场景 | 输入/环境 | 期望 | 说明 |
|------|------|-----------|------|------|
| 4 | env 有值 | `FFPROBE_PATH=/custom/ffprobe` | 返回 env | 兼容 CI/本地自定义 |
| 5 | env 无值且包不可用 | 无 env | 返回 `'ffprobe'` | 最终回退（走系统 PATH） |

### 2.3 extractAudioDuration

| 序号 | 场景 | execFile 输出 | 期望 | 说明 |
|------|------|---------------|------|------|
| 7 | 成功 | JSON `{ format: { duration: '123.45' } }` | `123450` | 秒→毫秒 |
| 8 | execFile 失败 | callback(err) | null | 记录 error |
| 9 | JSON 解析失败 | 输出非 JSON | null | 记录 error |
| 10 | duration 非数字 | `'not-a-number'` | null | 记录 warn |
| 11 | format 缺失 | `{}` | null | 记录 warn |

### 2.4 processAudioMarkers

| 序号 | 场景 | 输入 | 期望 | 说明 |
|------|------|------|------|------|
| 12 | oapiToken 缺失 | `oapiToken=null` + 含标记文本 | 原样返回 | 并 warn |
| 13 | 无标记 | 普通文本 | 原样返回 |  |
| 14 | 标记 JSON 非法 | `...{invalid-json}...` | 清理标记、保留其余文本 | warn |
| 15 | 文件不存在 | marker path 不存在 | 结果包含提示符号（如 `⚠️`） | 并清理标记 |

### 2.5 sendAudioMessage / sendAudioProactive

| 序号 | 场景 | 输入 | 期望 | 说明 |
|------|------|------|------|------|
| 16 | sendAudioMessage 默认 duration | 不传 duration | 不抛错并 info | 默认时长 |
| 17 | sendAudioMessage 指定 duration | duration=30000 | 不抛错并 info | 透传 |
| 18 | sendAudioMessage 失败 | axios.post 抛错 | 不抛错并 error | 错误收敛 |
| 19 | proactive user | target=user | 不抛错并 info | 主动消息 |
| 20 | proactive group | target=group | 不抛错并 info |  |
| 21 | proactive duration 透传 | duration=45000 | msgParam.duration === '45000' | 字符串化 |

## 3. 预期正确输出与潜在错误

- **正确**：音频类型识别覆盖常见扩展名；ffprobe 路径优先级明确且可在 CI 环境运行；时长解析异常均返回 null 且有日志；标记处理不会把原文其它部分误删。
- **潜在错误原因**：大小写处理遗漏；duration 单位错用（秒/毫秒）；ffprobe 路径优先级颠倒；JSON 标记解析失败未清理导致下游发送异常；文件不存在未提示。

