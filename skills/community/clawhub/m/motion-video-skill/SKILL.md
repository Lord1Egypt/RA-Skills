---
name: motion-video-maker
description: 根据文本、脚本或 Markdown 生成结构化讲解动画视频，使用 Web 页面制作和预览 AE / PR 风格的动效。必须严格根据解说文本规划合理的动画播放与切换时间，先生成预览，只有在用户明确确认后才导出 mp4。适用于知识讲解、产品介绍、口播配套动画、字幕强化、步骤演示和数据解说视频。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["node"] },
        "platforms": ["macos", "linux", "windows"],
        "install":
          [
            {
              "id": "node-brew",
              "kind": "brew",
              "formula": "node",
              "bins": ["node"],
              "label": "Install Node.js (brew)",
            },
            {
              "id": "ffmpeg-brew",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (brew)",
            },
          ],
      },
  }
---

# Motion Video Maker

本技能用于构建结构化讲解动画视频，而不是让 AI 直接输出一份不可维护的随意 HTML。

核心工作流是：

`用户输入 -> 拆分分镜与讲述节奏 -> 按解说文本同步 timing -> 生成 movie.json -> Web 预览 -> 自然语言编辑 -> 用户确认 -> 导出 mp4`

## ClawHub 版本说明

- 发布包默认不包含 `node_modules`、Chromium 浏览器二进制和历史导出产物。
- 首次使用先进入 `{baseDir}` 安装依赖；只有在需要导出 mp4 时才安装 Playwright 浏览器。
- 导出 mp4 还需要系统里有 `ffmpeg`；仅做预览和结构编辑时不依赖它。

```bash
cd {baseDir}
npm install
npx playwright install chromium
```

- 云端 TTS 需要用户自行配置 API key；未配置时可只做 preview，或使用 `system` fallback。

## 何时使用

- 用户要把一段文字、脚本或 Markdown 做成讲解型动画视频
- 用户要做类似 AE / PR 风格的口播辅助动效、字幕强化或知识讲解卡片
- 用户想先在 Web 页面里预览动效，再导出成视频
- 用户希望后续能继续改文案、调整节奏、换模板，而不是每次重做页面

## 核心原则

- `movie.json` 是唯一事实来源，不能只改最终 HTML
- 一段视频先拆成多个 `scene`，每个 scene 只负责一个讲述重点
- 动效优先服务“讲解清晰度”，不是无目的堆特效
- 文本语义要先映射成合适的版式与动画模板，再生成具体元素
- `scene.durationMs`、元素入场时间和分步出现节奏必须优先根据 `scene.narration` 推导，不能凭感觉平均分配
- 配置引导要先收窄再确认：先帮助用户选内容结构和视觉方向，再进入 TTS 与导出
- 在用户没有明确说“确认导出”“可以导出视频”之前，只允许生成和修改预览，不允许自动导出视频
- 如果用户要接入语音，必须先确认 TTS provider、voice、language、speed 和 fallback，不能默认假设
- 音色必须由用户明确点名确认；如果用户还没选定 voice，只能停留在 `pending`，不能直接开始合成
- 如果用户没有明确说“你来定”，不要擅自替用户选模板、主题或音色
- 本技能的本机 TTS 兜底必须同时兼容 macOS 和 Windows
- 优先产出稳定可编辑的讲解视频，再逐步扩展更复杂的 AE 风格动效

## 目录导航

- `references/movie-schema.md`
  定义 `movie.json` 的结构、scene 与 element 字段。
- `references/animation-rules.md`
  定义“文本内容 -> 讲解动画”的映射规则。
- `scripts/sync_timings.js`
  按 `scene.narration` 自动同步场景时长和动画开始时间。
- `references/template-catalog.md`
  定义当前可选模板、主题配色、适用场景与 UI 风格。
- `references/tts-catalog.md`
  定义当前支持的 TTS provider、确认要求和兜底规则。
- `references/prompt-patterns.md`
  定义从原始文本生成分镜、scene 和节奏的提示模式。
- `scripts/init_project.js`
  创建新的独立项目目录与 starter `movie.json`。
- `scripts/validate_movie.js`
  校验 `movie.json` 是否满足最小结构要求。
- `scripts/render_preview.js`
  根据 `movie.json` 生成可播放的 `preview.html`。
- `scripts/export_video.js`
  用浏览器逐帧截图并调用 `ffmpeg` 导出 `.mp4`，必须显式确认。
- `scripts/build_project.js`
  一键完成 timing 同步、校验、预览生成；只有显式确认后才导出视频。
- `scripts/list_catalog.js`
  列出可用模板、主题与 TTS provider。
- `scripts/configure_tts.js`
  先把 TTS provider、language、speed 和 fallback 写入 `movie.json`，并保持 `pending`。
- `scripts/confirm_tts.js`
  在用户明确选定 voice 后，把 voice 写入 `movie.json`，并把状态切到 `confirmed`。
- `scripts/synthesize_voice.js`
  生成逐 scene 音频。当前支持 MiniMax 和本机朗读兜底；本机兜底兼容 macOS 与 Windows。
- `assets/themes/*.json`
  定义主题颜色、字体、背景与高亮色。
- `assets/templates/*.json`
  定义预设模板的 UI 风格、舞台样式和推荐主题。
- `samples/example-movie.json`
  示例动画工程。

## 推荐工作流

1. 先读 `references/animation-rules.md`，把用户原文拆成 4 到 8 个讲述节拍。
2. 再读 `references/movie-schema.md`，把每个节拍映射成 `scene`，同时补齐 `scene.narration`。
3. 在 `{baseDir}/projects/<slug>/movie.json` 中写入结构化分镜，并选择合适的 `template`。
4. 运行 `node {baseDir}/scripts/build_project.js {baseDir}/projects/<slug>`。该命令会先同步 narration timing，再生成 `preview.html`。
5. 通过自然语言继续修改某个 scene、元素、文案、时长和动效。
6. 如果用户没指定视觉风格，先按 `references/template-catalog.md` 给出 2 到 4 个模板选项，并明确推荐 1 个；theme 默认跟模板走。
7. 只有当用户明确说想换配色、品牌色或 UI 质感时，才单独展开 theme 选项。
8. 如果用户要接入语音，先按 `references/tts-catalog.md` 确认 provider、language、speed、fallback，先写入 `pending` 的 `audio` 配置。
9. 然后必须把可用 voice 列给用户，等用户明确点名其中一个 voice。
10. 只有在用户明确选定 voice 后，才运行 `node {baseDir}/scripts/confirm_tts.js {baseDir}/projects/<slug> --voice <voice-id> ...`，再运行 `node {baseDir}/scripts/synthesize_voice.js {baseDir}/projects/<slug>`。
11. 只有用户明确确认导出后，才运行 `node {baseDir}/scripts/build_project.js {baseDir}/projects/<slug> --export --confirm-export`。

## 命令示例

在本技能目录下运行：

```bash
cd {baseDir}
npm install
npx playwright install chromium
node scripts/list_catalog.js
node scripts/init_project.js demo-video "AI 剪辑讲解" --template creator-pop
node scripts/sync_timings.js samples/example-movie.json
node scripts/configure_tts.js projects/demo-video --provider minimax --language zh-CN --speed 1.0 --fallback system
node scripts/list_tts_voices.js minimax
node scripts/confirm_tts.js projects/demo-video --voice "Chinese (Mandarin)_Reliable_Executive" --provider minimax --language zh-CN --speed 1.0 --fallback system
node scripts/synthesize_voice.js projects/demo-video
node scripts/validate_movie.js samples/example-movie.json
node scripts/render_preview.js samples/example-movie.json outputs/example-preview.html
node scripts/export_video.js samples/example-movie.json outputs/example.mp4 --confirm
node scripts/build_project.js projects/demo-video
node scripts/build_project.js projects/demo-video --export --confirm-export
```

## 结构化生成要求

- 每个 `scene` 必须有稳定的 `id`
- 每个 `element` 必须有稳定的 `id`
- `scene.narration` 不能为空或应能从当前元素文本推导
- `scene.durationMs` 要真实反映讲解节奏，并且优先根据解说文本自动同步
- 所有元素必须显式给出 `x`, `y`, `w`, `h`
- 预览画布固定为 `1280 x 720`
- 动效统一写在元素的 `animation` 字段里
- 同一 scene 内不宜同时出现过多入场动画，优先控制信息密度
- 如需完全手动控制 timing，必须把 `scene.timingMode` 设为 `manual`
- 如需接入语音，`audio.confirmationStatus` 在用户确认前必须保持 `pending`

## 文本到动画的默认映射

- 金句 / 定义句：大标题 + 强调副标题 + `fade-up`
- 步骤说明：标题 + 列表分步出现 + `itemStaggerMs`
- 对比内容：左右分栏 + `slide-left` / `slide-right`
- 数据结论：大数字或结论卡片 + `pop`
- 总结 / 行动号召：收束标题 + 标语 + `fade` / `pop`

## Timing 规则

- 默认以 `scene.narration` 作为 timing 真相来源
- 单个 scene 的总时长必须覆盖该段解说的朗读时长，并留出开场和收尾缓冲
- 标题通常先于正文出现，正文和 bullet 要跟着语义停顿逐步展开
- 列表项的 `itemStaggerMs` 要根据解说内容长度自动调整，不能固定套用同一个值
- 如果某段 narration 太长，优先拆分 scene，而不是强行压缩动画

## 编辑要求

当用户说“第二段太长”“第三个要点出现快一点”“把结论页更像 AE 的 kinetic typography”时：

- 先定位 `scene`
- 再定位对应 `element`
- 修改 `movie.json`
- 重新生成预览
- 不要直接只改 `preview.html`

## 配置引导顺序

当用户还没把配置说全时，优先按这个顺序引导，不要一次把所有问题都堆给用户：

1. 先确认内容目标：这条视频是在讲产品、教程、步骤、案例，还是观点总结。
2. 再确认视觉方向：优先给 2 到 4 个模板选项，并说明推荐理由。
3. theme 默认跟模板走；只有用户明确说“换配色”“更亮一点”“更像品牌视觉”时，才展开 theme。
4. narration 与 timing 优先根据文本自动生成，不把它当成需要用户手调的首轮配置。
5. 如果用户要配音，先确认 provider、language、speed、fallback。
6. 然后列出当前 provider 的可用 voice，让用户点名选择。
7. 最后再问是否导出视频；未确认导出前只给 preview。

建议用“推荐项 + 2 到 3 个备选”的方式提问，而不是开放式追问。只有当用户明确说“你来定”时，才可以直接使用推荐模板和其默认 theme。

## 视觉配置引导

- 模板是主风格选择，theme 是细化配色和气质的次级选择
- 用户没提视觉风格时，必须至少给出一个推荐模板，并说明为什么适合当前内容
- 如果用户只是说“做一个介绍视频”，优先推荐 `signal-stage`
- 如果用户强调教程拆解、案例复盘，优先推荐 `editorial-board`
- 如果用户强调短视频感、字幕冲击力、社媒节奏，优先推荐 `creator-pop`
- 如果用户强调极简、理性、访谈摘要，优先推荐 `mono-frame`
- 如果用户说“你定”，可以直接采用推荐模板和默认 theme，但要在回复里说清楚你替他采用了什么

## TTS 确认要求

- 当用户说“接语音”“配音”“上 TTS”时，必须先停下来确认
- 必须确认：`provider`、`voice`、`language`、`speed`、`fallbackProvider`
- 可选 provider：`microsoft-azure`、`openai`、`minimax`、`doubao`、`system`
- 如果用户没有指定，必须先问，不能擅自选定
- 如果用户还没选中 voice，必须先展示可选音色，再等用户点名确认
- 如果用户选择的是当前还未接好适配器的 provider，必须明确告知“现在只能做配置或回退到 `system`，不能假装已经原生接通”
- 默认推荐保留 `system` 作为 fallback
- `system` fallback 在 macOS 使用 `say`，在 Windows 使用 PowerShell + `System.Speech`

## 导出确认要求

- 默认只构建预览，不自动导出视频
- 只有用户明确表达“确认导出”“可以导出视频”“开始导出”这类意思后，才允许使用导出命令
- 如果用户还在看预览、改文案或调 timing，严禁提前导出

## 导出说明

- 预览层由 Web 页面实时渲染
- 导出层通过浏览器逐帧截图 + `ffmpeg` 合成 `.mp4`
- 当前 MVP 重点支持无音轨讲解动画；后续可扩展旁白、BGM 和字幕烧录
