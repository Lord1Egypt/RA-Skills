---
id: sea-salt-cyan
name: 海盐青
mode: light
layout: fresh-frame
tokensSource: ../tokens/themes.json
playbookVersion: 1.2.0
palette: { canvas: "#E6F4F1", surface: "#F7FFFD", surfaceMuted: "rgba(247,255,253,0.74)", textPrimary: "#07554F", textSecondary: "#24504C", emphasis: "#0F766E", accent: "#14B8A6", accentStrong: "#0F766E", border: "rgba(20,184,166,0.66)", ctaBackground: "#14B8A6", ctaText: "#000000" }
---

# 海盐青 · 主题 playbook

清新干净、减压舒适。适合用户运营、会员增长、轻量科普——专业但不压人。

## Token 语义与档位(实测)

- v1.3 token 已把正文色加深:`textPrimary #07554F` 对 canvas 约 7.67:1,达到字幕/正文 7:1 内部目标(旧 `#0B5F58` 仅 6.65:1,已废止);字幕仍推荐配 `surface #F7FFFD` 底板,复杂录屏背景上底板是保底
- `accent #14B8A6` 青绿为大标题级(4.8:1 档),大号强调可用,不进正文小字
- 青绿做填充底配 `ctaText #000000` 纯黑字(约 8.4:1),不配白字
- `border` 青绿半透明为纯装饰线

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `fresh-frame`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

步骤清单、趋势与对比图、关键词强调条、标题卡——运营讲解类块;强调条用青绿描边框+surface 底。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕深青字 `#07554F` 配 surface 白青底板;录屏等复杂背景上必须保留底板,这是本主题的硬规则。

## 动效档

准许:淡入/上移入;缩放入仅限关键词强调条一次;禁:弹入/闪烁/漂浮。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 海盐青清新风:canvas #E6F4F1 海盐底,一切文字落在 surface #F7FFFD 卡片上(本主题正文禁止裸压底色);深青 #07554F 做正文,青绿 #14B8A6 只做大号强调与描边框,青绿底配深字;圆角框式构图、边界清晰;动效入场淡入+轻上移 10–16 帧,克制不闹。
