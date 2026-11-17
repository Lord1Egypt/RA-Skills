---
id: earth-brown
name: 大地棕
mode: light
layout: earth-bands
tokensSource: ../tokens/themes.json
playbookVersion: 1.2.0
palette: { canvas: "#F6F1E9", surface: "#EFE2D2", surfaceMuted: "rgba(246,241,233,0.78)", textPrimary: "#3E2C23", textSecondary: "#594234", emphasis: "#8B5E34", accent: "#8B5E34", accentStrong: "#3E2C23", border: "rgba(139,94,52,0.66)", ctaBackground: "#6B3F1F", ctaText: "#FFFFFF" }
---

# 大地棕 · 主题 playbook

沉稳可靠、质感高级。适合商业思考、案例复盘、品牌故事——时间感和手工感。

## Token 语义与档位(实测)

- `textPrimary #3E2C23` 对 canvas 11.8:1,正文/字幕直接可用
- `accent #8B5E34` 棕为大标题级(5.0:1);填充底(ctaBackground)已加深为 `#6B3F1F`,配白字约 8.0:1 可进正文级
- `border` 棕色半透明为纯装饰线,不承担信息分隔
- 深棕 `accentStrong #3E2C23` 与正文同色,做填充底时配白字

半透明角色(`surfaceMuted`/`speakerSurface`/`glow`)一律按五类背景(亮/暗/肤色/彩色 UI/高细节)的最终合成像素验收。色值以 `tokens/themes.json` 为唯一真相源,本文不一致时以 JSON 为准。

## 版式搭配

绑定布局 `earth-bands`(坐标见 `tokens/layouts.json`);双画面版式从 `assets/compositions.json` 按语义选,主讲人窗描边、观点条、字幕底板一律从本主题语义 token 取色,不逐元素挑色。

## 信息块偏好

引用卡、标题卡、章节导航、趋势与对比图——叙事与复盘类块;色带分区是本主题的版式母题。(块的进入信号与禁忌见 `02-剪辑方法手册/04-信息块与画面任务.md`。)

## 字幕底板

字幕深棕字配米白底板;棕色系不进字幕正文。

## 动效档

准许:淡入/上移入/纸片式轻位移;禁:旋转/弹入/闪烁/漂浮。(词汇定义、时长基线与块×动效推荐见 `02-剪辑方法手册/04-信息块与画面任务.md`「块级动效词汇表」。)

## 调用 crib(生成 MG/图形时直接嵌入指令)

> 大地棕质感风:canvas #F6F1E9 米色底,面板 surface #EFE2D2 暖棕纸感;正文深棕 #3E2C23;棕 #8B5E34 只做大号强调与填充底;横向色带分区构图,层与层用色差不用线;动效入场淡入+轻上移,允许纸片式轻位移,不旋转不弹跳。
