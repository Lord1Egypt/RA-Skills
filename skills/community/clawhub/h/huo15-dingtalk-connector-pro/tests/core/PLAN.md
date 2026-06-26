# core（核心能力聚合）测试方案

## 1. 目的与覆盖范围

`tests/core` 更像一个 **“核心能力冒烟/回归集合”**：把插件中最关键、最常被上层调用的函数挑出来做快速验证，确保跨模块基础能力没有被破坏。

主要覆盖（以测试文件实际引用为准）：

- 会话指令归一：**normalizeSlashCommand**
- 消息去重：**isMessageProcessed / markMessageProcessed / cleanupProcessedMessages**
- 配置读取与校验：**getConfig / isConfigured**
- 鉴权：**getAccessToken / getOapiAccessToken**
- 媒体：**toLocalPath / buildMediaSystemPrompt / isAudioFile / getFfprobePath**

## 2. 用例表（覆盖现有测试）

### 2.1 normalizeSlashCommand

| 序号 | 输入 | 期望 |
|------|------|------|
| 1 | `/new`/`/reset`/`/clear`/`新会话`/`重新开始` | 统一为 `/new` |
| 2 | `/help`/`hello`/`some text` | 原样返回 |

### 2.2 消息去重

| 序号 | 场景 | 期望 |
|------|------|------|
| 3 | cleanup 后首次 isMessageProcessed('msg1') | false |
| 4 | markMessageProcessed('msg1') 后再查 | true |
| 5 | 空 messageId | 不写入且始终 false |

### 2.3 getConfig / isConfigured

| 序号 | 场景 | 期望 |
|------|------|------|
| 6 | cfg.channels['dingtalk-connector'] 存在 | 正确提取 clientId/clientSecret |
| 7 | 缺配置 | getConfig 返回 `{}` |
| 8 | 有 clientId+clientSecret | isConfigured=true |
| 9 | 缺任一字段 | isConfigured=false |

### 2.4 getAccessToken / getOapiAccessToken

| 序号 | 场景 | 期望 |
|------|------|------|
| 10 | getAccessToken 成功 | 返回 token |
| 11 | getAccessToken API 报错 | promise reject |
| 12 | getOapiAccessToken errcode=0 | 返回 access_token |
| 13 | getOapiAccessToken errcode!=0 | 返回 null |
| 14 | getOapiAccessToken 网络异常 | 返回 null |

### 2.5 toLocalPath / buildMediaSystemPrompt / isAudioFile / getFfprobePath

| 序号 | 场景 | 期望 |
|------|------|------|
| 15 | toLocalPath URL | 结果包含原文件名 |
| 16 | toLocalPath 本地路径 | 原样返回 |
| 17 | buildMediaSystemPrompt | 包含“图片/视频/音频”等关键词 |
| 18 | isAudioFile('mp3','wav','ogg','m4a') | true；非音频 false |
| 19 | getFfprobePath | 返回字符串且可用（不为 undefined） |

## 3. 预期正确输出与潜在错误

- **正确**：核心函数在最常见输入下行为稳定；异常路径返回 null 或抛出（按契约）一致；不会因为外部依赖（如 ffprobe）缺失导致整个测试崩溃。
- **潜在错误原因**：把回归集合误当成“全覆盖”，导致边界用例缺失；不同模块对错误处理约定不一致（有的 throw，有的 return null）；mock 依赖不完整导致测试脆弱。

