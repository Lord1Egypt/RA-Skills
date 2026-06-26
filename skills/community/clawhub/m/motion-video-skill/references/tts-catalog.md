# TTS Catalog

当用户要接入语音时，默认使用可配置 TTS。

## 必须先确认

在真正生成语音前，必须先向用户确认这些字段：

- `provider`
  可选：`microsoft-azure`、`openai`、`minimax`、`doubao`、`system`
- `voice`
  具体音色名；若用户没给，必须追问或保留为待确认
- `language`
  例如 `zh-CN`
- `speed`
  默认 `1.0`
- `fallbackProvider`
  默认推荐 `system`

如果用户只说“加语音”或“接 TTS”，不能直接假设 provider，必须先停下来确认。
如果用户只确定了 provider，但没点名具体 voice，也不能进入 confirmed 或开始合成。

## 必须走两步

1. 先配置 provider、language、speed、fallback，状态保持 `pending`
2. 列出可选 voice，等用户明确点名后，再切到 `confirmed`

不允许把“我替用户选一个看起来合适的音色”当成确认。

## 推荐确认问法

```text
要接 TTS 的话，我先确认 5 项：provider（微软 / OpenAI / MiniMax / 豆包 / 本机朗读）、voice、语言、语速，以及是否保留本机朗读兜底。
```

如果用户还没给 voice，需要先补一句：

```text
我先不替你选音色。我把当前 provider 的可选 voice 列给你，你点一个之后我再开始合成。
```

## 当前 provider 定位与支持状态

- 已实现并可直接合成：`minimax`
- 已实现并可本机兜底：`system`
- 仅支持配置占位，暂未实现原生适配：`openai`、`microsoft-azure`、`doubao`

如果用户选择了尚未原生适配的 provider，必须明确说明当前结果会是：

- 先写入配置
- 如果继续执行合成，会回退到 `system`
- 或者暂停，等后续补该 provider 的适配器

不能把“可配置”描述成“已经能按该 provider 真实合成”。

### `openai`

- 适合：通用 API 接入、快速接入
- 特点：配置简单，适合先跑通
- 当前状态：仅支持配置占位，暂未实现原生合成适配

### `microsoft-azure`

- 适合：企业环境、多语种、已有 Azure 体系
- 特点：稳定，适合公司内长期使用
- 当前状态：仅支持配置占位，暂未实现原生合成适配

### `minimax`

- 适合：中文内容生产、短视频语音
- 特点：更偏中文内容场景
- 当前技能内已实现同步 TTS 适配，可按 scene 逐段生成音频

### `doubao`

- 适合：中文内容流、字节生态相关流程
- 特点：同样适合中文内容生产
- 当前状态：仅支持配置占位，暂未实现原生合成适配

### `system`

- 适合：试听、调 timing、离线兜底
- 特点：无需云端密钥，但音色质感通常弱于云端 TTS
- macOS：使用系统 `say`
- Windows：使用 PowerShell + `System.Speech`

## 兜底规则

- 如果用户选择云端 provider，默认仍建议保留 `system` 作为 fallback
- 如果云端 provider 未配置密钥或适配器暂未接好，可回退到 `system`

## 引导顺序

推荐 AI 按下面的顺序带用户确认：

1. 先确认 provider
2. 再确认 language、speed、fallbackProvider
3. 如果 provider 已实现，立刻列出可选 voice
4. 如果 provider 暂未实现，先明确告知当前只能配置占位或回退到 `system`
5. 只有在用户点名 voice 后，才能切到 `confirmed`

## 推荐问法

先问 provider：

```text
这版要不要接语音？如果要，我先给你 3 个更实际的选择：MiniMax（中文表现更好，当前已接好）、System（本机朗读，适合试听）、或者先记下 OpenAI / Azure / 豆包配置但暂时不直接合成。你想用哪个？
```

然后问 voice：

```text
我先不替你选音色。下面是当前 provider 下更适合这条视频的几个 voice，你点一个，我再开始合成。
```

## key 存储建议

- provider key 不应写进 `movie.json`
- 当前技能默认把 key 存到本机的私有配置文件中，再由脚本读取
- 如果 key 曾经被直接粘贴到聊天或代码里，建议后续自行轮换

## 平台说明

- 当前本机兜底 TTS 目标平台是 macOS 和 Windows
- macOS 无需额外安装系统 TTS
- Windows 依赖系统自带的 PowerShell 与语音引擎
