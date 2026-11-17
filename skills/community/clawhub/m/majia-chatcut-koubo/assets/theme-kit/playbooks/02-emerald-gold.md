---
id: emerald-gold
name: 墨绿金
mode: dark
layout: executive-split
tokensSource: ../tokens/themes.json
playbookVersion: 1.1.0
palette: { canvas: "#0F2E2E", surface: "#173A33", surfaceMuted: "rgba(23,58,51,0.76)", textPrimary: "#F8F4E8", textSecondary: "#D6E2DB", emphasis: "#D4AF37", accent: "#D4AF37", accentStrong: "#1E584E", border: "rgba(212,175,55,0.72)", ctaBackground: "#D4AF37", ctaText: "#14241F" }
---

# 墨绿金 · 主题 playbook

商务高级、信任感强。适合业务复盘、策略拆解、经营分析——把「稳」写在画面里。

## Token 语义与档位(实测)

- `textPrimary #F8F4E8` 对 canvas 13.2:1,正文/字幕直接可用
- `accent #D4AF37` 金色为大标题级(6.9:1):大号强调词、数字高亮可用,不进正文与小字
- 金色做填充底时配 `ctaText #14241F` 深字(7.7:1),不配白字
- `accentStrong #1E584E` 只做填充底;`border` 金色半透明达图形级

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `executive-split`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

标题卡、大数字、趋势与对比图、引用卡——复盘叙事的骨架块;金色只给结论级信息。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕米白字,底板 surfaceMuted;金色不进字幕。

## 动效档

准许:淡入/上移入;金色扫过为一次性强调、全片 ≤2 次;缩放入慎用(商务克制);禁:弹入/闪烁/漂浮。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 墨绿金商务风:canvas #0F2E2E 墨绿底,面板 surface #173A33 圆角;正文米白 #F8F4E8;金 #D4AF37 只给结论级强调(大标题/关键数字),金底必配深字 #14241F;分隔线用金色半透明细线;整体克制少动,入场淡入+轻上移,数据块可加一次金色扫过强调,全片不超过两次。
