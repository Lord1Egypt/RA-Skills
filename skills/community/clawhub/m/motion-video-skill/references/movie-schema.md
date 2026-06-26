# Movie Schema

`movie.json` 是整个动画项目的唯一事实来源。

## 顶层结构

```json
{
  "meta": {
    "title": "AI 剪辑讲解",
    "theme": "signal-ink",
    "template": "signal-stage",
    "ratio": "16:9",
    "fps": 30,
    "width": 1280,
    "height": 720
  },
  "audio": {
    "enabled": false,
    "mode": "tts",
    "confirmationRequired": true,
    "confirmationStatus": "pending",
    "provider": null,
    "voice": null,
    "language": "zh-CN",
    "speed": 1,
    "fallbackProvider": "system",
    "outputDir": "audio",
    "tracks": []
  },
  "subtitles": {
    "enabled": true,
    "source": "scene-cues",
    "stylePreset": "bottom-band",
    "maxLines": 2,
    "tracks": []
  },
  "scenes": []
}
```

## meta 字段

- `title`: 视频标题
- `theme`: 主题名称，对应 `assets/themes/*.json`
- `template`: 模板名称，对应 `assets/templates/*.json`
- `ratio`: 当前固定为 `16:9`
- `fps`: 默认 `30`
- `width`: 当前固定 `1280`
- `height`: 当前固定 `720`

## audio 字段

- `enabled`: 是否启用 TTS
- `mode`: 当前固定为 `tts`
- `confirmationRequired`: 是否必须先确认
- `confirmationStatus`: `pending`、`confirmed` 或 `synthesized`
- `provider`: `microsoft-azure`、`openai`、`minimax`、`doubao`、`system`
- `voice`: 具体 voice 名称
- `language`: 例如 `zh-CN`
- `speed`: 朗读语速，默认 `1`
- `fallbackProvider`: 推荐默认 `system`
- `outputDir`: 音频输出目录
- `tracks`: 每个 scene 对应一条音频任务
- `providerConfig`: provider 的补充参数，例如 `model`、`format`

在用户确认 provider 和 voice 之前，`confirmationStatus` 必须保持 `pending`。

## subtitles 字段

- `enabled`: 是否显示字幕层
- `source`: 当前固定推荐 `scene-cues`
- `stylePreset`: `bottom-band`、`short-video-pop`、`minimal-center`
- `maxLines`: 单次最多显示几行
- `tracks`: 由 scene cue 自动生成的字幕轨

## scene 结构

```json
{
  "id": "scene-01",
  "label": "开场定义",
  "type": "hero",
  "timingMode": "auto",
  "transition": {
    "enterEffect": "zoom-out",
    "exitEffect": "fade",
    "enterDurationMs": 360,
    "exitDurationMs": 220
  },
  "durationMs": 3200,
  "narration": "一句话说清问题和价值。",
  "cues": [],
  "elements": []
}
```

## 当前支持的 scene type

- `hero`
- `problem`
- `steps`
- `comparison`
- `stat`
- `quote`
- `closing`

## scene 字段说明

- `id`: 稳定标识
- `label`: 人类可读名称
- `type`: 版式类型
- `durationMs`: 当前 scene 总时长
- `timingMode`: `auto` 或 `manual`，默认推荐 `auto`
- `narration`: 记录口播或讲解意图，是 timing 的主要依据
- `cues`: 逐句级时间锚点，字幕和更细粒度动画都应优先基于它
- `transition`: 当前 scene 的入场和出场方式
- `background.gradient`: 可选，覆盖主题默认背景
- `elements`: 页面元素数组

## cue 结构

```json
{
  "id": "scene-01-cue-01",
  "text": "OpenClaw 是一个跑在你自己设备上的个人 AI 助手。",
  "startMs": 180,
  "endMs": 1840
}
```

- `id`: cue 唯一标识
- `text`: 对应这一句 narration
- `startMs`: 相对当前 scene 的开始时间
- `endMs`: 相对当前 scene 的结束时间

## transition 字段

```json
{
  "transition": {
    "enterEffect": "wipe-left",
    "exitEffect": "slide-right",
    "enterDurationMs": 320,
    "exitDurationMs": 240
  }
}
```

- `enterEffect` / `exitEffect`: scene 级转场
- 当前支持：`fade`、`slide-left`、`slide-right`、`lift-up`、`zoom-in`、`zoom-out`、`blur-in`、`wipe-left`、`wipe-up`、`iris-in`
- `enterDurationMs` / `exitDurationMs`: 入场和出场持续时间

## element 通用字段

每个元素都必须包含：

- `id`
- `type`
- `x`
- `y`
- `w`
- `h`

建议额外包含：

- `label`
- `text`
- `style`
- `animation`

坐标单位统一为像素，对齐 `1280 x 720` 画布。

## 当前支持的 element type

### `title`

```json
{
  "id": "hero-title",
  "type": "title",
  "text": "让字幕也承担讲解任务",
  "x": 96,
  "y": 116,
  "w": 720,
  "h": 180
}
```

### `subtitle`

用于补充定义、结论或副标题。

### `text`

普通说明文本，适合 1 到 3 句短段落。

### `bullet-list`

```json
{
  "id": "steps-list",
  "type": "bullet-list",
  "items": [
    "先把口播拆成节拍",
    "再匹配镜头和动效",
    "最后导出为视频"
  ],
  "x": 100,
  "y": 188,
  "w": 520,
  "h": 300,
  "animation": {
    "effect": "fade-up",
    "startMs": 380,
    "durationMs": 500,
    "itemStaggerMs": 180
  }
}
```

### `chip`

小型标签，适合场景类型、关键词、章节名。

### `stat`

```json
{
  "id": "stat-main",
  "type": "stat",
  "value": "3x",
  "text": "讲解信息密度提升",
  "x": 90,
  "y": 146,
  "w": 380,
  "h": 220
}
```

### `quote`

强调某句话、金句或结尾总结。

### `shape`

纯装饰形状，可用于色块、背景发光、分栏卡片。

## animation 字段

```json
{
  "animation": {
    "effect": "slide-left",
    "startMs": 420,
    "durationMs": 640,
    "itemStaggerMs": 0
  }
}
```

- `effect`: 当前支持 `fade`、`fade-up`、`slide-left`、`slide-right`、`pop`、`clip-up`
- 另外支持：`zoom-in`、`blur-in`、`glow-pop`、`swing-up`、`reveal-right`、`reveal-down`
- `startMs`: 相对当前 scene 的开始时间，默认应由 narration 自动同步
- `durationMs`: 动画时长，默认应由 narration 自动同步
- `itemStaggerMs`: 仅对 `bullet-list` 生效，用于逐条出现

## narration timing 约定

- 当 `scene.timingMode` 为 `auto` 时，`durationMs` 和元素动画时间应由 narration 自动推导
- 当 `scene.timingMode` 为 `auto` 时，系统应同时生成逐句级 `cues`
- 如果已经有真实音频时长，`cues` 应尽量跟真实语音长度对齐，而不是只用文本估算
- narration 太长时，应拆分成多个 scene
- 只有用户明确要求精细手调时，才切到 `manual`

## style 常用字段

- `fontSize`
- `fontWeight`
- `textAlign`
- `lineHeight`
- `letterSpacing`
- `color`
- `background`
- `borderRadius`
- `padding`
- `borderColor`
- `opacity`

## 结构建议

- 每个 scene 最好只保留一个中心观点
- 单个 scene 内正文不宜超过 40 个汉字或 3 条 bullet
- 金句和结论页优先用 `title` + `quote` + `chip`
- 复杂逻辑优先拆多个 scene，而不是塞满一个 scene
