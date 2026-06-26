---
title: WordCloud 词云
description: 一个高性能的词云可视化组件
keywords: ['词云', 'WordCloud', '可视化']
demo:
  cols: 2
tocDepth: 3
nav:
  title: 组件
  path: /components
group:
  title: 数据展示
---

# WordCloud 词云

词云组件用于可视化文本数据，根据词语的权重以不同大小显示在画布上。支持多种自定义配置，如形状、颜色、旋转等。

## 组件特性

- 📊 基于 Canvas 的高性能渲染
- 🎨 丰富的自定义样式选项
- 🖱️ 完整的交互事件支持
- 📱 自适应容器大小
- 🔍 支持缩放和高分屏适配
- 💫 平滑的动画过渡效果

## 代码演示

### 基础用法

最简单的词云展示，展示一组词语及其权重。

<code src="./demos/demo1.tsx"></code>

### 交互事件

支持鼠标悬浮提示和点击回调。

<code src="./demos/demo2.tsx"></code>

### 自定义样式

通过 options 属性自定义词云的外观，包括形状、颜色、字体等。

<code src="./demos/demo3.tsx"></code>

## API

### WordCloud

| 参数      | 说明                                       | 类型                                                                        | 默认值       |
| --------- | ------------------------------------------ | --------------------------------------------------------------------------- | ------------ |
| list      | 词云数据列表，每项为 `[word, weight]` 格式 | `[string, number][]`                                                        | `[]`         |
| className | 自定义类名                                 | `string`                                                                    | -            |
| tooltip   | 是否显示悬浮提示                           | `boolean`                                                                   | `true`       |
| onClick   | 点击词语时的回调函数                       | `(item: [string, number], dimension: Dimension, event: MouseEvent) => void` | -            |
| options   | 词云配置项，见下方 Options                 | `Partial<WordCloud2.Options>`                                               | 见下方默认值 |

### Options

以下是常用的配置项，完整配置项请参考 [wordcloud2.js](https://github.com/timdream/wordcloud2.js) 文档。

| 参数            | 说明                   | 类型                                                                                                      | 默认值                |
| --------------- | ---------------------- | --------------------------------------------------------------------------------------------------------- | --------------------- |
| shape           | 词云形状               | `'circle' \| 'cardioid' \| 'diamond' \| 'triangle-forward' \| 'triangle' \| 'pentagon' \| 'star'`         | `'circle'`            |
| backgroundColor | 背景颜色               | `string`                                                                                                  | `'#ffffff'`           |
| fontFamily      | 字体                   | `string`                                                                                                  | `'Arial, sans-serif'` |
| fontWeight      | 字体粗细               | `string \| number`                                                                                        | `'bold'`              |
| color           | 文字颜色               | `string \| ((word: string, weight: number, fontSize: number, distance: number, theta: number) => string)` | `'random-dark'`       |
| gridSize        | 网格大小，影响词语间距 | `number`                                                                                                  | `4`                   |
| weightFactor    | 字体大小权重因子       | `number \| ((weight: number) => number)`                                                                  | `1`                   |
| rotateRatio     | 旋转概率               | `number`                                                                                                  | `0.5`                 |
| rotationSteps   | 旋转步数               | `number`                                                                                                  | `10`                  |
| minSize         | 最小字体大小           | `number`                                                                                                  | `12`                  |
| drawMask        | 是否绘制掩码           | `boolean`                                                                                                 | `false`               |
| drawOutOfBound  | 是否允许绘制超出边界   | `boolean`                                                                                                 | `false`               |
| shrinkToFit     | 是否缩小以适应画布     | `boolean`                                                                                                 | `true`                |
| minRotation     | 最小旋转角度           | `number`                                                                                                  | `-Math.PI/4`          |
| maxRotation     | 最大旋转角度           | `number`                                                                                                  | `Math.PI/4`           |
| shuffle         | 是否打乱词语顺序       | `boolean`                                                                                                 | `true`                |

### Dimension 类型

点击回调函数中的 dimension 参数包含以下属性：

| 属性 | 说明          | 类型     |
| ---- | ------------- | -------- |
| x    | 词语的 x 坐标 | `number` |
| y    | 词语的 y 坐标 | `number` |
| w    | 词语的宽度    | `number` |
| h    | 词语的高度    | `number` |

## 注意事项

1. 组件会自动适应容器大小，请确保父容器有明确的宽高
2. 高分辨率屏幕上会自动适配设备像素比，保证清晰度
3. 为了获得更好的性能，建议控制数据量在合理范围内
4. 如果使用自定义颜色函数，请确保返回合法的颜色值

## FAQ

### 1. 词云显示模糊怎么办？

组件已经内置了高分辨率屏幕适配，如果仍然模糊，可以：

- 检查容器大小是否合适
- 调整 `gridSize` 参数
- 适当增加 `weightFactor` 值

### 2. 如何控制词语的大小范围？

可以通过以下参数调整：

- `weightFactor`: 控制整体字体大小
- `minSize`: 设置最小字体大小
- 调整输入数据中的权重值范围

### 3. 如何实现渐变色文字？

可以通过 `color` 参数传入自定义函数：

```ts
options={{
  color: (word, weight, fontSize) => {
    return weight > 20 ? '#f52443' : weight > 10 ? '#0088ff' : '#00aa00';
  }
}}
```
