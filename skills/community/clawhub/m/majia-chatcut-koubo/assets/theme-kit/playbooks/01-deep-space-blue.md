---
id: deep-space-blue
name: 深空蓝
mode: dark
layout: diagonal-tech
tokensSource: ../tokens/themes.json
playbookVersion: 1.1.0
palette: { canvas: "#0B132B", surface: "#111D36", surfaceMuted: "rgba(17,29,54,0.72)", textPrimary: "#FFFFFF", textSecondary: "#CBD5E1", emphasis: "#60A5FA", accent: "#60A5FA", accentStrong: "#1E3A8A", border: "rgba(96,165,250,0.80)", ctaBackground: "#1E3A8A", ctaText: "#FFFFFF" }
---

# 深空蓝 · 主题 playbook

专业稳重、科技感强。适合数据分析、技术解释、AI 实战类口播——观点靠证据压场,不靠情绪。

## Token 语义与档位(实测)

- `textPrimary #FFFFFF` 对 canvas 18.4:1,正文/字幕直接可用
- `accent #60A5FA` 达正文级(7.2:1),本主题少数可放宽到正文强调的 accent
- `accentStrong #1E3A8A` 对 canvas 仅 2.x:1——**只做填充底**配 `ctaText #FFFFFF`(10.4:1),禁止当文字色
- `border` 为高透明度电蓝,可承担图形级分隔(深色主题 border 达标)

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `diagonal-tech`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

大数字、趋势与对比图、代码/命令卡、章节导航——数据与工程类块最合拍;关键词强调条用 accent 描边而非填充。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕直接用白字,底板可用 surfaceMuted 半透明面板;发光 glow 只做点缀不做可读性支撑。

## 动效档

准许:淡入/上移入/缩放入(数字块一次性);循环:pulse ≤1 次;禁:弹入/闪烁/漂浮。数字类块可用滚动到位。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 深空蓝科技风:canvas #0B132B 深空底,卡片落 surface #111D36 圆角面板;正文与字幕纯白,电蓝 #60A5FA 只标记「被测量的那个东西」,一块一个;深蓝 #1E3A8A 只做按钮/标签填充底配白字;线条与分隔用半透明电蓝细线;动效入场淡入+轻上移 10–16 帧,不弹跳,数字类块可用滚动到位。
