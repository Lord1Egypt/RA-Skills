---
title: AspectRatio
description: 宽高比组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# AspectRatio 宽高比组件

AspectRatio 是一个用于保持元素宽高比的容器组件，可以确保内容（如图片、视频等）在不同屏幕尺寸下保持固定的宽高比例，避免变形。

## 组件特性

- 📐 智能宽高比控制，保持内容不变形
- 🔧 渐进式增强，现代浏览器使用 CSS aspect-ratio，老旧浏览器自动降级处理
- 📱 响应式布局友好，自适应不同屏幕尺寸
- 🎯 支持任意类型的子元素，如图片、视频、div、canvas 等

## 基础使用

<code src="./demos/demo1.tsx" title="基础用法" description="只设置父容器宽度,子元素一般要设置宽高100%,才能最大限度的保持固定的ratio;如果父容器设置了固定宽高,则ratio就失效了.">基础使用</code>

<code src="./demos/demo2.tsx" title="自适应" description="不设置宽高时,会自适应;改变浏览器窗口大小试试...">自适应</code>

<code src="./demos/demo3.tsx" title="Video 标签" description="子元素是Video, 设置宽高充满父容器则会最大限度的保持ratio, video有默认宽高320*176;">Video 标签</code>

<code src="./demos/demo4.tsx" title="Canvas" description="子元素是canvas,父容器的盒子一直保持固定的ratio">Canvas</code>

## Tips

`AspectRatio`组件只是创建一个具有固定宽高比的`容器盒子`,并不能完全约束子元素的宽高, 一般情况下设置子元素的宽高为 100%,则会让子元素充满父容器,从而最大程度的保持 ratio;一般常用于`img`和`video`, `objectFit: 'contain'`会让子元素在内容区完整显示,不会被裁剪;

### API

| 参数名称  | 说明                 | 类型                  | 默认值 |
| :-------: | :------------------- | :-------------------- | :----: |
|   ratio   | 宽高比，宽/高        | `number`              |  16/9  |
| className | 自定义外层容器 class | `string`              |   -    |
| children  | 需要保持比例的子元素 | `React.ReactNode`     |   -    |
|   style   | 自定义外层容器样式   | `React.CSSProperties` |   -    |
