---
title: TypewriterText
description: 打字机风格文本展示组件
keywords: ['typewriter', 'text', 'animation', '打字', '文本展示']
demo:
  cols: 2
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 数据展示
  order: 4
---

# TypewriterText 打字文本组件

TypewriterText 提供轻量的打字机文本动画，支持多段文案、随机速度、循环播放等能力，配合命令式控制方法可在引导页、版本更新提示、活动营销等场景中快速输出吸睛的动效文案。

## 组件特性

- 📜 支持字符串与字符串数组输入，可按顺序循环展示多段文案
- ↩️ 识别 `\n` / `\r\n` 换行符，自动插入换行并让光标随之到新行
- ⚡️ 自定义输入/删除速度，支持随机区间，真实还原打字机体验
- ⏳ 精细化节奏控制，包含首段延时、删除前停顿、循环次数等配置
- ✋ 暴露 pause/resume/reset/skip 方法，方便外部交互组件联动
- ♿️ 支持配置 `aria-live`，兼顾屏幕阅读器播报体验
- 🎯 光标样式、闪烁节奏与样式完全可定制

## 基础使用

<code src="./demos/basicDemo.tsx" title="基础演示"></code>

## 自定义鼠标样式

<code src="./demos/cursorDemo.tsx" title="特殊鼠标样式"></code>

## 多段文本与循环

<code src="./demos/multiTextDemo.tsx" title="多段循环/多行文本"></code>

## 回删与随机速度

<code src="./demos/backspaceDemo.tsx" title="回删动画"></code>

## 命令式控制

<code src="./demos/controlDemo.tsx" title="命令式控制 (暂停/继续/重置)"></code>

## API

### TypewriterText

| 参数              | 说明                             | 类型                                      | 默认值  |
| ----------------- | -------------------------------- | ----------------------------------------- | ------- |
| text              | 展示文案；支持字符串或字符串数组 | `string \| string[]`                      | ——      |
| speed             | 打字速度 (ms) 或随机区间         | `number \| { min: number; max: number }`  | `50`    |
| deleteSpeed       | 删除速度 (ms)                    | `number`                                  | `30`    |
| backspace         | 是否启用回删效果                 | `boolean`                                 | `false` |
| pauseBeforeDelete | 回删前的停顿时间 (ms)            | `number`                                  | `600`   |
| startDelay        | 每段文本开头的延时 (ms)          | `number`                                  | `0`     |
| loop              | 是否循环；数字表示循环次数       | `boolean \| number`                       | `false` |
| cursor            | 是否展示光标                     | `boolean`                                 | `true`  |
| cursorChar        | 光标字符                         | `string` \| `ReactNode`                   | \|      |
| cursorBlinkSpeed  | 光标闪烁节奏 (ms)                | `number`                                  | `600`   |
| onStep            | 每次新增字符时触发               | `(index: number, output: string) => void` |         |
| onComplete        | 单段文本输入结束时触发           | `() => void`                              |         |
| ...rest           | 透传 `HTMLSpanElement` 属性      | ——                                        |         |

### TypewriterTextHandle

| 方法   | 说明                       | 类型         |
| ------ | -------------------------- | ------------ |
| pause  | 暂停动画                   | `() => void` |
| resume | 继续动画                   | `() => void` |
| reset  | 重置到第一段重新播放       | `() => void` |
| skip   | 跳过当前段落直接进入下一段 | `() => void` |
