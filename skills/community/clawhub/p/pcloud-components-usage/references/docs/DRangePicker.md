---
title: DRangePicker 日期范围组件
description: 基于 antd 4.24.16 RangePicker 的二次封装组件，支持快捷选项位置自定义
keywords: ['日期范围', 'range picker', '快捷选择日期']
demo:
  cols: 2
tocDepth: 3
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DRangePicker 日期范围组件

DRangePicker 是一个基于 Ant Design RangePicker 的增强组件，允许用户选择一个日期范围。该组件在原有基础上增加了快捷选项位置自定义功能，可以将快捷选项显示在面板的左侧、底部或右侧。

## 组件特性

- 🎯 支持自定义快捷选项位置（左侧、底部、右侧）
- 📦 继承 Ant Design RangePicker 的所有功能
- 🎨 支持通过 popupClassName 自定义弹出层样式
- ⚙️ 与 Ant Design 表单组件无缝集成

## 基础用法

<code src="./demos/basic.tsx" title="默认位置" description="默认和`antd`保持一致,`ranges`均在弹出面板的下方"></code>

## 不同位置

<code src="./demos/basic2.tsx" title="位于左侧" description="指定rangePosition为left"></code>
<code src="./demos/basic3.tsx" title="位于右侧" description="指定rangePosition为right"></code>

## API

### DRangePickerProps

DRangePicker 继承了 Ant Design [DatePicker.RangePicker](https://4x-ant.design/components/date-picker/#RangePicker) 的所有属性，除此之外还支持以下属性：

| 参数           | 说明                 | 类型                          | 默认值   |
| -------------- | -------------------- | ----------------------------- | -------- |
| rangesPosition | 快捷选项位置         | `left` \| `bottom` \| `right` | `bottom` |
| popupClassName | 弹出日历的自定义类名 | `string`                      | -        |
