# 巨构提示词生成器 for Krea 2 · 安装说明

为 Krea 2 图像模型生成**巨构 / 超尺度结构**类生图提示词的 skill。覆盖建筑巨构、生物巨兽、自然与地质巨构、机械载具巨构、超现实混合巨构五大场景。

## 安装

### 方式一：用户级安装（推荐，所有项目可用）

把整个 `krea2-megastructure-prompts` 文件夹复制到：

- **Windows**：`C:\Users\<你的用户名>\.workbuddy\skills\`
- **macOS / Linux**：`~/.workbuddy/skills/`

最终路径形如：

```
~/.workbuddy/skills/krea2-megastructure-prompts/SKILL.md
```

复制完成后重启一次会话（或新开一个对话），即可通过描述需求触发。

### 方式二：项目级安装（仅当前项目可用，可随仓库共享）

把文件夹复制到项目根目录下：

```
<项目根目录>/.workbuddy/skills/krea2-megastructure-prompts/
```

### 方式三：从 zip 安装

解压 `krea2-megastructure-prompts.zip`，得到 `krea2-megastructure-prompts` 文件夹，再按方式一或方式二放置。

## 目录结构

```
krea2-megastructure-prompts/
├── SKILL.md                        # 主入口：工作流、七层公式、Krea 2 硬规则、参数速查、翻车修法
├── README.md                       # 本文件
├── references/
│   ├── scene-playbooks.md          # 五类场景剧本（A建筑/B生物/C自然/D机械/E超现实）+ 跨类配方
│   ├── layer-vocabulary.md         # 七层词库、尺度锚定技法、组装模板、反模式清单
│   └── style-presets.md            # 12 组风格预设 + 调色速查
└── assets/
    └── prompt-library.md           # 30 条可直接复制的完整提示词
```

## 怎么触发

直接描述需求即可，例如：

- "帮我写一个 Krea 2 提示词，沙漠里一座巨大的水坝"
- "生成一条巨鲸飘在城市上空的 krea2 提示词，竖构图"
- "这条提示词帮我按巨构思路润色一下：a huge tree in the cloud"
- "给我 3 个不同方向的超现实巨构探索种子"

## 输出包含什么

- 1 条英文主提示词（Krea 2 是英文模型，长句自然语言效果最好）
- 2 条同主体的风格/视角变体
- 中文要点说明
- 参数建议：`aspect_ratio`、`creativity`（raw / low / medium / high）、模型变体（Medium / Large）

## 关于 Krea 2 的关键事实（写提示词时据此判断）

- **自然语言长句**优于逗号标签堆砌；长而具体的描写效果最好。
- **不要元语言**（"the image shows…"），直接从主体开始。
- **画面里要出字就把文字放进引号**。
- **creativity 参数**：提示词写得越详细，越应该用 `raw`；只有一句话的种子才用 `high` 做探索。
- **摄影参数它真的懂**：焦距、光圈、ISO、布光方式都会被真实反映。
- **风格参考图 > 形容词堆砌**：想锁定某个画风，上传 1–10 张参考图比堆风格词可靠得多。

## 版本

v1.0.0 — 依据 Krea 2 官方 prompting 指南与 prompt expander 规范编写。
