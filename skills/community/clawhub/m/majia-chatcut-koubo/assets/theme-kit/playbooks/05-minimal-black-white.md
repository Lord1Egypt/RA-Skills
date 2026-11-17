---
id: minimal-black-white
name: 极简黑白
mode: light
layout: minimal-column
tokensSource: ../tokens/themes.json
playbookVersion: 1.2.0
palette: { canvas: "#F5F5F5", surface: "#FFFFFF", surfaceMuted: "rgba(255,255,255,0.82)", textPrimary: "#111111", textSecondary: "#4A4A4A", emphasis: "#111111", accent: "#111111", accentStrong: "#333333", border: "rgba(17,17,17,0.76)", ctaBackground: "#111111", ctaText: "#FFFFFF" }
---

# 极简黑白 · 主题 playbook

极致简洁、信息聚焦。适合知识卡片、观点输出、问答栏目——把全部注意力留给内容本身。

## Token 语义与档位(实测)

- `textPrimary #111111` 对 canvas 17.3:1;黑白互为填充/反色(18.9:1),全部正文级
- 本主题 accent=ink,**没有彩色强调**:强调只靠字重、字号、黑白反转
- `border` 黑色半透明达信息级,可承担真实分隔

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `minimal-column`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

标题卡、引用卡、关键词强调条、章节导航——文字本位的块;图表用黑白灰阶+直接标注。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕深黑字配纯白底板,或黑底白字反转;二选一后全片一致。

## 动效档

仅准许:淡入/上移入——本主题动效收到最窄;禁:其余全部(含缩放/滑入/一切循环强调)。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 极简黑白风:canvas #F5F5F5 浅灰底,卡片纯白;全部文字 #111111;没有彩色——强调只用黑底白字反转、加大字号、加重字重三种手段;栏式排版、大留白、细黑分隔线;动效只有淡入与轻上移,无任何弹跳与发光。
