---
title: RCropper
description: 图片裁剪组件
keywords: ['图片', '裁剪', 'Cropperjs']
tocDepth: 2
demo:
  cols: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# RCropper 图片裁剪组件

RCropper 是一个基于 Cropper.js 封装的现代化图片裁剪组件，提供丰富的图片处理功能和灵活的配置选项，支持矩形选区、固定比例裁剪、图片变换等操作，适用于头像上传、图片编辑、内容裁剪等场景。

## 组件特性

- 🖼️ 高性能裁剪引擎，基于 Cropper.js 最新版本封装
- 📐 灵活选区控制，支持矩形选区和固定/自定义宽高比裁剪
- 🔧 图片变换功能，支持缩放、旋转、翻转等基础操作
- 🎨 网格线与画布配置，支持自定义网格线与画布样式
- 🎯 实例对象访问，通过 ref 获取实例对象调用底层方法
- 📱 响应式设计，适配不同屏幕和容器尺寸
- 🔄 裁剪结果导出，支持 base64 或 File 对象格式输出
- 🖱️ 交互体验优化，选区可拖拽、缩放、重置
- ⚙️ 高级配置支持，支持禁用缩放、调整选区等高级配置

## 基础使用

<code src="./demos/demo1.tsx" title="基础用法" description="最基本的图片裁剪用法"></code>

## 自定义选区

<code src="./demos/demo2.tsx" title="自定义选区" description="通过selection属性自定义选区配置"></code>

## 自定义网格线

<code src="./demos/demo3.tsx" title="自定义网格线" description="通过grid属性自定义网格线配置"></code>

## API

### RCropperProps

| 参数         | 说明           | 类型                                                                               | 默认值    |
| ------------ | -------------- | ---------------------------------------------------------------------------------- | --------- |
| src          | 图片的源地址   | `string`                                                                           | -         |
| alt          | 图片的替代文本 | `string`                                                                           | `'image'` |
| className    | 容器类名       | `string`                                                                           | -         |
| style        | 容器样式       | `CSSProperties`                                                                    | -         |
| dragMode     | 拖拽模式       | `crop` \| `move` \| `none`                                                         | `'crop'`  |
| grid         | 网格线配置     | `RCropperGrid`                                                                     | -         |
| selection    | 裁剪区域配置   | `RCropperSelection`                                                                | -         |
| image        | 图片配置       | `RCropperImage`                                                                    | -         |
| canvas       | 画布配置       | `RCropperCanvas`                                                                   | -         |
| onCrop       | 裁剪完成回调   | `(\_src: string \| undefined, \_file?: File) => void`                              |
| onZoom       | 缩放回调       | `(imgData: number[] \| undefined) => void`                                         | -         |
| onRotate     | 旋转回调       | `(imgData: number[] \| undefined) => void`                                         | -         |
| onFlip       | 翻转回调       | `(imgData: number[] \| undefined) => void`                                         | -         |
| onReset      | 重置回调       | `(imgData: number[] \| undefined) => void`                                         | -         |
| onCancelCrop | 取消裁剪回调   | `(selectionData: { x: number; y: number; width: number; height: number }) => void` | -         |

### RCropperGrid

| 参数    | 说明     | 类型     |
| ------- | -------- | -------- |
| rows    | 网格行数 | `number` |
| columns | 网格列数 | `number` |

### RCropperSelection

| 参数               | 说明           | 类型      |
| ------------------ | -------------- | --------- |
| x                  | 选区 x 坐标    | `number`  |
| y                  | 选区 y 坐标    | `number`  |
| width              | 选区宽度       | `number`  |
| height             | 选区高度       | `number`  |
| aspectRatio        | 选区宽高比     | `number`  |
| initialAspectRatio | 初始宽高比     | `number`  |
| zoomable           | 是否可缩放     | `boolean` |
| resizable          | 是否可调整大小 | `boolean` |

### RCropperImage

| 参数         | 说明       | 类型      |
| ------------ | ---------- | --------- |
| rotatable    | 是否可旋转 | `boolean` |
| scalable     | 是否可缩放 | `boolean` |
| skewable     | 是否可倾斜 | `boolean` |
| translatable | 是否可平移 | `boolean` |

### RCropperCanvas

| 参数      | 说明     | 类型      |
| --------- | -------- | --------- |
| scaleStep | 缩放步长 | `number`  |
| disabled  | 是否禁用 | `boolean` |

### RCropperRef

通过 ref 可以获取到 RCropper 的实例对象，实例对象包含以下属性：

| 参数      | 说明         | 类型               |
| --------- | ------------ | ------------------ |
| cropper   | Cropper 实例 | `Cropper`          |
| image     | 图片对象     | `CropperImage`     |
| canvas    | 画布对象     | `CropperCanvas`    |
| selection | 选区对象     | `CropperSelection` |
