---
title: RndDrag
description: 基于react-rnd的拖拽组件
keywords: ['拖拽']
tocDepth: 2
demo:
  cols: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# RndDrag 拖拽组件

RndDrag 是一个基于 react-rnd 封装的拖拽组件，支持元素的拖拽移动和尺寸调整功能，提供了灵活的边界控制和多种自定义选项，适用于需要实现可拖拽、可调整大小界面元素的场景。

## 组件特性

- 🎯 拖拽移动支持，可限制移动边界防止元素移出容器
- 📏 八个方向尺寸调整，支持精确控制元素大小
- 🔒 比例锁定功能，保持元素宽高比不变形
- 🎨 样式完全可定制，支持 CSS 样式覆盖
- 🖱️ 自定义拖动句柄，灵活控制拖拽触发区域

## 基础用法

<code src="./demos/demo1.tsx" title="基础用法" description="指定默认属性值,相对于父容器的`x,y`的位置以及容器`width, height`宽高"></code>

## 受控的 Position 和 Size

<code src="./demos/demo3.tsx" title="基础用法" description="动态更改`position`和`size`属性, 控制容器的位置及宽高"></code>

## 移动范围限制

<code src="./demos/demo2.tsx" title="范围限制" description="通过设置`bounds`属性来指定拖动的范围限制"></code>

## 启用/禁用拖动

<code src="./demos/demo4.tsx" title="启用/禁用" description="通过设置`disableDragging`属性来启用或禁用容器是否能拖动"></code>

## 允许容器的移动方向

<code src="./demos/demo5.tsx" title="移动方向" description="通过设置`dragAxis`属性来控制容器可移动的方向, 可选值:`x`,`y`,`both`,`none`, 设置为`none`时等同于disableDragging为true"></code>

## 自定义拖动句柄

<code src="./demos/demo6.tsx" title="自定义拖动句柄" description="自定义`resizeHandleComponent`属性,任意设置容器八个方向上的拖动句柄"></code>

## API

| 参数名称                   | 说明                                                               | 类型                                                                          | 默认值     |
| -------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ---------- |
| className                  | 容器根元素类名                                                     | `string`                                                                      | -          |
| style                      | 容器根元素内联样式                                                 | `React.CSSProperties`                                                         | -          |
| bounds                     | 拖动边界限制，支持：CSS 选择器、DOM 元素、'window'/'body'/'parent' | `string \| Element`                                                           | -          |
| disableDragging            | 完全禁用拖动                                                       | `boolean`                                                                     | `false`    |
| dragAxis                   | 拖动方向限制                                                       | `'x' \| 'y' \| 'both' \| 'none'`                                              | `'both'`   |
| dragHandleClassName        | 指定可拖动区域的类名（仅限类名选择器）                             | `string`                                                                      | -          |
| position                   | 受控模式下的位置坐标                                               | `{ x: number, y: number }`                                                    | -          |
| size                       | 受控模式下的尺寸                                                   | `{ width: number \| string, height: number \| string }`                       | -          |
| default                    | 非受控模式的初始位置和尺寸                                         | `{ x: number, y: number, width: number \| string, height: number \| string }` | -          |
| resizeHandleComponent      | 自定义句柄组件                                                     | `{ top?: React.ReactNode, right?: React.ReactNode, ... }`                     | -          |
| resizeHandleStyles         | 句柄样式配置                                                       | `{ top?: React.CSSProperties, right?: React.CSSProperties, ... }`             | -          |
| resizeHandleClasses        | 句柄类名配置                                                       | `{ top?: string, right?: string, ... }`                                       | -          |
| resizeHandleWrapperClass   | 设置调整大小手柄包装元素`span`的类名                               | `string`                                                                      | -          |
| resizeHandleWrapperStyle   | 设置调整大小手柄包装元素`span`的样式                               | `React.CSSProperties`                                                         | -          |
| minWidth                   | 最小宽度                                                           | `number \| string`                                                            | `10`       |
| minHeight                  | 最小高度                                                           | `number \| string`                                                            | `10`       |
| maxWidth                   | 最大宽度                                                           | `number \| string`                                                            | `Infinity` |
| maxHeight                  | 最大高度                                                           | `number \| string`                                                            | `Infinity` |
| lockAspectRatio            | 锁定宽高比例（true=当前比例，number=指定比例）                     | `boolean \| number`                                                           | `false`    |
| lockAspectRatioExtraHeight | 可调整大小的组件能够保持宽高比并额外增加高度                       | `[number, number]`                                                            | -          |
| enableResizing             | 启用调整方向配置                                                   | `{ top?: boolean, right?: boolean, ... } \| boolean`                          | `true`     |
| dragGrid                   | 拖动对齐网格 [x,y]                                                 | `[number, number]`                                                            | -          |
| resizeGrid                 | 调整大小对齐网格 [x,y]                                             | `[number, number]`                                                            | -          |
| cancel                     | 指定一个选择器，以防止拖动初始化（例如 `.body`）                   | `string`                                                                      | -          |
| scale                      | 缩放比例（用于适配缩放容器）                                       | `number`                                                                      | `1`        |
| enableUserSelectHack       | 是否启用防止文本选择的样式修复                                     | `boolean`                                                                     | `true`     |
| children                   | 子元素内容                                                         | `React.ReactNode`                                                             | -          |

### 事件回调

| 参数名称      | 说明         | 回调参数                                                                                                                                                                           |
| ------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| onDragStart   | 拖动开始事件 | `(e: SyntheticMouseEvent \| SyntheticTouchEvent, data: { node: HTMLElement, x: number, y: number, deltaX: number, deltaY: number, lastX: number, lastY:number }) => void \| false` |
| onDrag        | 拖动过程事件 | `(e: SyntheticMouseEvent \| SyntheticTouchEvent, data: { node: HTMLElement, x: number, y: number, deltaX: number, deltaY: number, lastX: number, lastY:number }) => void \| false` |
| onDragStop    | 拖动结束事件 | `(e: SyntheticMouseEvent \| SyntheticTouchEvent, data: { node: HTMLElement, x: number, y: number, deltaX: number, deltaY: number, lastX: number, lastY:number }) => void \| false` |
| onResizeStart | 调整开始事件 | `(e: MouseEvent\|TouchEvent, dir: ResizeDirection, ref: React.ElementRef<'div'>) => void`                                                                                          |
| onResize      | 调整过程事件 | `(e: MouseEvent\|TouchEvent, dir: ResizeDirection, ref: React.ElementRef<'div'>, delta: Size, position: Position) => void`                                                         |
| onResizeStop  | 调整结束事件 | `(e: MouseEvent\|TouchEvent, dir: ResizeDirection, ref: React.ElementRef<'div'>, delta: Size, position: Position) => void`                                                         |

### 类型定义

```typescript
type Position = { x: number; y: number };
type Size = { width: number; height: number };
type ResizeDirection = 'top' | 'right' | 'bottom' | 'left' | 'topRight' | 'bottomRight' | 'bottomLeft' | 'topLeft';
type ResizeEnable = {
  top?: boolean;
  right?: boolean;
  bottom?: boolean;
  left?: boolean;
  topRight?: boolean;
  bottomRight?: boolean;
  bottomLeft?: boolean;
  topLeft?: boolean;
};
```
