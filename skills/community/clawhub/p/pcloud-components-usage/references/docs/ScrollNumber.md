---
title: ScrollNumber
description: 数字滚动组件
keywords: ['数字', '滚动', 'number', 'scroll']
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

# ScrollNumber 数字滚动组件

ScrollNumber 是一个用于展示数字动画效果的组件，通过滚动数字的方式吸引用户注意力，提供多种自定义配置选项，适用于数据展示、统计信息、计数器等需要数字动画效果的场景。

## 组件特性

- 🎯 数字滚动动画，吸引用户注意力提升数据展示效果
- ⚙️ 灵活起始数值，支持自定义起始数值而非固定从 0 开始
- 📏 千分位分隔符，支持自定义千分位分隔符格式
- 🎨 精度控制，支持自定义小数位数保留
- ⏱️ 智能动画时长，根据数值大小自动调整动画时间
- 🧩 完全可配置，支持所有 react-countup 组件属性

## 基础使用

<code src="./demos/basicDemo.tsx" ></code>

## 千分位分隔符

<code src="./demos/separatorDemo.tsx" title="千分位分隔符"></code>

## 自定义过渡动画时间

<code src="./demos/durationDemo.tsx" title="自定义过渡动画时间"></code>

## 保留小数

<code src="./demos/noDecimalsDemo.tsx" title="不保留小数"></code>
<code src="./demos/decimalDemo.tsx" title="小数分隔符"></code>

## 自定义控制开始时间

<code src="./demos/delayStartDemo.tsx" title="延迟开始"></code>
<code src="./demos/manuallyStartDemo.tsx" title="手动开始"></code>

## 自定义前后缀

<code src="./demos/prefixDemo.tsx" title="自定义前缀"></code>
<code src="./demos/suffixDemo.tsx" title="自定义后缀"></code>

## Hooks 使用

<code src="./demos/hooksSimpleDemo.tsx" title="Hooks简单示例"></code>
<code src="./demos/hooksDemo.tsx" title="Hooks完整示例"></code>

## API

| 参数名称      | 说明              | 类型                                         | 默认值                   |
| ------------- | ----------------- | -------------------------------------------- | ------------------------ |
| className     | 样式类名          | `string`                                     | ——                       |
| start         | 开始数值          | `number`                                     | 0                        |
| end           | 结束数值          | `number`                                     | ——                       |
| duration      | 动画过渡时间(s)   | `number`                                     | 1 位数 0.8s；3 位数 1.5s |
| delay         | 延迟开始时间(s)   | `number`                                     | 0                        |
| decimals      | 保留小数位数      | `number`                                     | 2                        |
| decimal       | 小数位分隔符      | `string`                                     | `.`                      |
| separator     | 千分位分隔符      | `string`                                     | `,`                      |
| suffix        | 数值后缀字符      | `string`                                     | ——                       |
| prefix        | 数值前缀字符      | `string`                                     | ——                       |
| onReset       | 重置函数回调      | `({pauseResume,start,update}) => void`       | ——                       |
| onUpdate      | 更新函数回调      | `({pauseResume,start,reset}) => void`        | ——                       |
| onPauseResume | 暂停/恢复函数回调 | `({update,start,reset}) => void`             | ——                       |
| onStart       | 开始函数回调      | `({pauseResume,reset,update}) => void`       | ——                       |
| onEnd         | 结束函数回调      | `({pauseResume,reset,start,update}) => void` | ——                       |
