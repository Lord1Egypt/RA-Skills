---
id: vitality-lime
name: 活力青柠
mode: light
layout: playful-corner
tokensSource: ../tokens/themes.json
playbookVersion: 1.1.0
palette: { canvas: "#ECFDF5", surface: "#F7FFE9", surfaceMuted: "rgba(247,255,233,0.78)", textPrimary: "#163300", textSecondary: "#3F5B31", emphasis: "#387A05", accent: "#84CC16", accentStrong: "#16A34A", border: "rgba(132,204,22,0.72)", ctaBackground: "#84CC16", ctaText: "#163300" }
---

# 活力青柠 · 主题 playbook

年轻活力、轻快明亮。适合活动宣导、会员日、上新传播——短平快的传播型内容。

## Token 语义与档位(实测)

- `textPrimary #163300` 对 canvas 13.2:1,正文/字幕直接可用
- `accent #84CC16` 青柠做填充底配深字 #163300(7.1:1)是本主题主打组合
- `emphasis #387A05` 深绿 5.0:1 大标题级,可做标题文字色
- `border` 青柠半透明为纯装饰线

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `playful-corner`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

大数字、关键词强调条、标题卡、行动引导(仅当平台路由保留 CTA 时)——传播型块;节奏可以比其他主题快半档。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕墨绿字配浅色底板;青柠不做字幕文字色。

## 动效档

准许:淡入/上移入(可稍快至 8–12 帧)/缩放到位(强调条一次);**弹入唯一豁免主题**——仍需用户点头才用,默认不用;禁:闪烁/漂浮。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 活力青柠传播风:canvas #ECFDF5 浅青柠底,卡片 surface #F7FFE9;正文墨绿 #163300;青柠 #84CC16 只做填充底配深字,深绿 #387A05 做标题;角标式活泼构图但保护区纪律不变;动效入场可稍快(8–12 帧)仍不弹跳,强调条允许一次缩放到位。
