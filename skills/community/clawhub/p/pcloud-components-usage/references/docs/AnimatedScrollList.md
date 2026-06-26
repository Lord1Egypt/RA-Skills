---
title: AnimatedScrollList
nav:
  title: 组件
  path: /components
group:
  title: 数据展示
---

# AnimatedScrollList 自动滚动列表组件

AnimatedScrollList 是一个支持自动无缝循环滚动的列表组件，通过 `requestAnimationFrame` 和 `transform` 实现平滑动画效果，支持四个方向的滚动，适用于公告、通知、跑马灯等需要自动滚动的场景。

> 列表项之间的间距由自定义渲染内容自身的 `margin` 控制，无需额外配置。

## 组件特性

- 🎯 四向滚动支持，支持 `up`、`down`、`left`、`right` 四个方向
- 🔄 无缝循环滚动，自动复制列表项实现无缝循环效果
- ⚡ 高性能动画，使用 `requestAnimationFrame` 和 `transform` 实现平滑动画，避免闪烁
- 🖱️ 悬停暂停，支持鼠标悬停时自动暂停滚动，离开时恢复
- 🔋 资源优化，页面不可见或暂停状态下自动停止帧循环，释放资源
- 📏 灵活尺寸，支持固定高度和不固定高度的列表项都能无缝循环滚动

## 基础用法

<code src="./demos/demo1.tsx" title="向上滚动" description="最基本的用法，向上自动滚动"></code>

## 不同方向

<code src="./demos/demo2.tsx" title="四个方向" description="展示四个方向的滚动效果"></code>

## 固定高度列表项

<code src="./demos/demo3.tsx" title="固定高度" description="列表项具有固定高度时的滚动效果"></code>

## 不固定高度列表项

<code src="./demos/demo4.tsx" title="不固定高度" description="列表项高度不固定时的滚动效果。如果列表项中有图片,要给图片设置高度"></code>

## 固定表头

<code src="./demos/demo9.tsx" title="表头固定" description="通过 `header` 属性传入表头结构，表头固定展示，内容区域自动滚动"></code>

## 自定义速度

<code src="./demos/demo5.tsx" title="自定义速度" description="通过 speed 属性自定义滚动速度, `speed` 表示每秒移动的像素值"></code>

## 悬停暂停

<code src="./demos/demo6.tsx" title="悬停暂停" description="鼠标悬停时暂停滚动，离开时恢复"></code>

## 水平滚动

<code src="./demos/demo7.tsx" title="水平滚动" description="水平方向的滚动效果"></code>

## 数据不够一屏

<code src="./demos/demo8.tsx" title="数据不够一屏" description="5条数据总高度为`150px`, 父容器高度为`200px`, 数据不够一屏时，默认不会自动启动动画, 鼠标悬停时开启动画,或者设置`scrollWhenInsufficient`为`true`"></code>

## 动态更新数据

<code src="./demos/demo10.tsx" title="动态更新数据" description="动态更新数据，列表项数量变化时，滚动效果会自动更新"></code>

## API

### AnimatedScrollListProps

| 参数                   | 说明                                       | 类型                                                         | 默认值  |
| ---------------------- | ------------------------------------------ | ------------------------------------------------------------ | ------- |
| direction              | 滚动方向                                   | `'up' \| 'down' \| 'left' \| 'right'`                        | `'up'`  |
| speed                  | 滚动速度，单位 px/s                        | `number`                                                     | `50`    |
| hoverStop              | 是否在鼠标悬停时暂停滚动                   | `boolean`                                                    | `true`  |
| autoStart              | 是否自动开始滚动                           | `boolean`                                                    | `true`  |
| containerHeight        | 容器高度（垂直滚动时）或宽度（水平滚动时） | `number \| string`                                           | -       |
| containerWidth         | 容器宽度（水平滚动时）或高度（垂直滚动时） | `number \| string`                                           | -       |
| data                   | 列表数据                                   | `any[]`                                                      | -       |
| renderItem             | 渲染列表项的方法                           | `(item: any, index: number) => ReactNode`                    | -       |
| itemKey                | 列表项的唯一标识字段，用于 key             | `string \| ((item: any, index: number) => string \| number)` | `'id'`  |
| className              | 自定义类名                                 | `string`                                                     | `''`    |
| style                  | 自定义样式                                 | `CSSProperties`                                              | -       |
| showScrollbar          | 是否显示滚动条                             | `boolean`                                                    | `false` |
| scrollWhenInsufficient | 当列表项数量不足一屏时是否仍然滚动         | `boolean`                                                    | `false` |
| header                 | 表头内容，传入后表头固定展示               | `ReactNode`                                                  | -       |
