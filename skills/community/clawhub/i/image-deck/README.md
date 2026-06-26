# image-deck

## English

`image-deck` is used to create PPT, PowerPoint-style presentations, slide decks, and carousel decks where every page is a complete generated image. It uses Codex built-in `image_gen` (GPT Image 2) to generate slides one by one, with each slide's title, labels, and short copy generated inside the same image.

This skill requires Codex built-in `image_gen` (GPT Image 2).

Search keywords: `slide`, `slides`, `slide deck`, `presentation`, `PowerPoint`, `PPT`, `PPTX`, `deck`, `carousel`, `GPT Image 2`, `image generation`, `OpenClaw`, `Codex`.

## Trigger

Use this skill when asking for: `make a PPT`, `create a PowerPoint`, `build a presentation`, `make slides`, `create slides`, `generate slides`, `make a slide`, `create a slide deck`, `make a deck`, or `make a carousel`.

## Best For

- Every PPT page should be one complete generated image
- Images and text should be generated together in the same image
- Page count, language, style, and text richness/content density should be confirmed before planning; page count and style should include recommendations, and text richness should default to information-rich
- A slide-by-slide design document should be shown before prompt generation
- Prompts should be shown before generation so the user can review or edit them
- Normal content slides default to information-rich, while balanced and concise modes remain available
- After the deck is created, the user can revise one slide or several slides
- After the deck is created, the user can add new generated image slides

## Preview

![image-deck preview](https://raw.githubusercontent.com/tseng71/skills/main/skills/image-deck/assets/preview.jpg)

## Install

ClawHub page:

```text
https://clawhub.ai/tseng71/image-deck
```

GitHub repository / Codex install URL:

```text
https://github.com/tseng71/skills
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/image-deck ~/.codex/skills/image-deck
```

Restart Codex after installing.

## 中文说明

这是 `tseng71` 的个人 AI Agent Skills 仓库中的一个 skill。

`image-deck` 用于制作“每一页都是完整生成图片”的 PPT、PowerPoint 风格演示、slide deck 和 carousel deck。它会通过 Codex 内置的 `image_gen`（GPT Image 2）逐页生成，每页的标题、标签和短文案都在同一张生成图里完成。

使用这个 skill 需要可用的 Codex 内置 `image_gen`（GPT Image 2）。

搜索关键词：`slide`、`slides`、`slide deck`、`presentation`、`PowerPoint`、`PPT`、`PPTX`、`deck`、`carousel`、`GPT Image 2`、`image generation`、`OpenClaw`、`Codex`。

## 触发方式

可以这样说：`做PPT`、`制作PPT`、`帮我做PPT`、`生成PPT`、`做slides`、`做deck`、`做演示文稿`。

## 适合使用

- 每一页 PPT 都要是一张完整生成图
- 图片和文字要一起生成在同一张图里
- 制作前先确认页数、语言、风格和内容密度；页数和风格给出推荐，内容密度默认推荐文字丰富，语言由用户自己选择
- 生成提示词前先展示 PPT 逐页设计文档
- 生成前先输出提示词，让用户确认或修改
- 普通内容页默认推荐文字丰富，也可以按用户选择改成平衡或文字简洁
- 制作完成后，用户可以指定修改某一页或几页
- 制作完成后，用户可以继续追加新的图片页

## 安装

ClawHub 页面：

```text
https://clawhub.ai/tseng71/image-deck
```

GitHub 仓库 / Codex 安装地址：

```text
https://github.com/tseng71/skills
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/image-deck ~/.codex/skills/image-deck
```

安装后重启 Codex。
