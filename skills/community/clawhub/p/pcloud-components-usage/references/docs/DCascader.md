---
title: DCascader
description: 基于 antd 4.24.10 Cascader 的二次封装组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DCascader 级联选择器

DCascader 是基于 Ant Design Cascader 组件的增强封装，专门优化了异步数据加载体验，提供更便捷的级联选择功能，适用于需要动态加载选项的复杂业务场景。

## 组件特性

- ⚡ 异步数据加载优化，options 和 loadData 均支持传入异步函数
- 🔄 智能加载状态管理，自动显示加载中效果提升用户体验
- 🔍 本地搜索增强，默认匹配 label 字段，搜索更便捷
- 📐 自适应宽度设计，下拉框与下拉面板保持同宽
- 🎯 表单友好，在 From 表单组件中使用更方便

## 基础用法

<code src="./demos/basicDemo.tsx"  title="基础用法" description="默认开启异步加载,自动加载子级列表,加载时会显示加载中效果"></code>

## 动态加载子级列表

<code src="./demos/loadChildrenDemo.tsx" title="动态加载子级列表" description="loadData属性用于开启动态加载，默认使用options提供的方法,传入null表示不开启态加载"></code>

## 显示加载中

<code src="./demos/loadingDemo.tsx" title="显示加载中" description="设置loading属性即可在远程搜索时显示加载中，支持延迟显示，默认600毫秒，传入false或0表示不显示（loading效果目前对下拉列表无效）"></code>

## API

| 参数       | 说明                                                                                                                                                                | 类型                                            | 默认值 | 版本 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------ | ---- |
| options    | antd 的 options 属性，可以是一个 options 数组，或一个返回等价 options 数组的 promise                                                                                | `(value?,option?,options) => Promise<option[]>` | -      |      |
| loadData   | antd 的 loadData 属性，动态加载子级列表数据，默认使用 options 所提供的方法，如果传入 null，则表示不进行动态加载,该方法要求返回一个 options 数组或与其等价的 Promise | `(value?,option?,options) => Promise<option[]>` | -      |      |
| onLoadData | 等同 antd 的 loadData 属性,用于监听 antd loadData 事件                                                                                                              | `(value?,option?,options) => void`              | -      |      |
| loading    | 是否显示加载中（传入数字表示延迟加载,单位毫秒，0 等同于 false）                                                                                                     | `boolean \| number`                             | 600    |      |

其他属性同 antd Cascader 组件，详见：https://4x-ant-design.antgroup.com/components/cascader-cn/#API
