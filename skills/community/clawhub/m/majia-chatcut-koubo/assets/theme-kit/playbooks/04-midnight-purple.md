---
id: midnight-purple
name: 午夜紫
mode: dark
layout: orbit-focus
tokensSource: ../tokens/themes.json
playbookVersion: 1.1.0
palette: { canvas: "#1A1026", surface: "#241536", surfaceMuted: "rgba(36,21,54,0.76)", textPrimary: "#FFFFFF", textSecondary: "#DDD1F3", emphasis: "#A78BFA", accent: "#A78BFA", accentStrong: "#6D28D9", border: "rgba(167,139,250,0.72)", ctaBackground: "#6D28D9", ctaText: "#FFFFFF" }
---

# 午夜紫 · 主题 playbook

神秘高端、差异化强。适合趋势洞察、创新话题、产品发布——制造「接下来有东西」的期待感。

## Token 语义与档位(实测)

- `textPrimary #FFFFFF` 对 canvas 18.3:1,正文/字幕直接可用
- `accent #A78BFA` 浅紫为大标题级(6.7:1),大号强调可用,不进小字
- `accentStrong #6D28D9` 只做填充底配白字(7.1:1)
- `border` 浅紫半透明达图形级(深色主题)

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `orbit-focus`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

标题卡、关键词强调条、问答卡、数字变化——悬念与揭示类块最合拍。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕纯白字,底板 surfaceMuted 深紫半透明。

## 动效档

准许:淡入/上移入;揭示类块允许一次由暗到亮的显影;禁:弹入/闪烁/漂浮。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 午夜紫洞察风:canvas #1A1026 深紫底,面板 surface #241536 圆角;正文纯白;浅紫 #A78BFA 只做大号强调,深紫 #6D28D9 只做填充底配白字;可用 glow 紫辉做焦点晕染但不支撑可读性;动效入场淡入+轻上移,揭示类块允许一次由暗到亮的显影,不闪烁。
