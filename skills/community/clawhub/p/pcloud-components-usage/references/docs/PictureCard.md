---
title: PictureCard
description: 图文卡片组件
keywords: ['卡片', '文字卡片', '图片']
tocDepth: 2
demo:
  cols: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# PictureCard 图文卡片组件

PictureCard 是一个用于展示图片和相关信息的卡片组件，支持单张或多张图片展示，提供灵活的布局选项和丰富的交互功能，适用于图片展示、产品展示、内容预览等场景。

## 组件特性

- 🖼️ 多图片支持，可展示单张或多张图片
- 🔍 图片预览功能，支持放大、缩小、旋转等操作
- 🎨 灵活布局方式，支持垂直和水平图文排列
- 🎯 交互增强，支持悬停效果和边框自定义
- 🧩 内容自定义，可自由添加文字和其他内容

## 基础用法

<code src="./demos/demo1.tsx" title="一般效果"></code>
<code src="./demos/demo2.tsx" title="无边框,无hover效果"></code>

## 布局方式

<code src="./demos/demo3.tsx"></code>

## 图片预览

<code src="./demos/demo4.tsx" title="单张图片" description="支持预览时旋转、放大、缩小等"></code>
<code src="./demos/demo5.tsx" title="多张图片" description="多张图片时,默认显示第一张图片;预览时支持切换"></code>

## API

### 通用属性

| 参数名称   | 说明       | 类型                                      | 默认值     |
| ---------- | ---------- | ----------------------------------------- | ---------- |
| className  | 类名       | string                                    |            |
| layout     | 布局方式   | `'vertical' \| 'horizontal'`              | 'vertical' |
| src        | 图片地址   | `ImageProps['src'] \|ImageProps['src'][]` |            |
| imageWidth | 图片宽度   | `ImageProps['width']`                     |            |
| content    | 内容区     | `React.ReactNode`                         |            |
| style      | 自定义样式 | `React.CSSProperties`                     |            |
| hoverable  | 开启 hover | boolean                                   | true       |
| bordered   | 显示边框   | boolean                                   | true       |

ImageProps 见[Antd4.x Image API](https://4x-ant-design.antgroup.com/components/image-cn/#API)
