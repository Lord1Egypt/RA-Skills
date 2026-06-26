---
title: DSelect
description: 基于 antd 4.24.10 Select 的二次封装组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DSelect 选择器组件

DSelect 是基于 Ant Design Select 组件的增强封装，专门优化了异步数据加载和搜索体验，提供防抖搜索、加载状态管理等功能，适用于需要远程数据加载和复杂搜索场景的选择器。

## 组件特性

- ⚡ 异步数据优化，options 和 onSearch 均支持传入异步函数
- 🔄 智能加载状态，加载选项列表或搜索时自动显示加载中效果
- 🎯 防抖搜索功能，避免频繁请求提升性能
- 🔍 本地搜索增强，默认匹配 label 字段，搜索更便捷
- 🎯 表单友好，在 From 表单组件中使用更方便

## 基础用法

<code src="./demos/basicDemo.tsx" title="基础用法"  description="默认开启输入防抖和异步加载,异步加载时会显示加载中效果"></code>

## 远程搜索

<code src="./demos/searchDemo.tsx" title="远程搜索"  description="设置onSearch属性即可开启远程搜索功能而不用设置showSearch，若仅设置showSearch为true，则使用默认本地搜索方法，与and默认使用value搜索不同，DSelect默认使用label进行搜索"></code>

## 搜索时防抖

<code src="./demos/debounceDemo.tsx" title="搜索时防抖"  description="使用远程搜索时启用输入防抖功能，可避免频繁调用远程接口导致服务器压力过大的问题"></code>

## 显示加载中

<code src="./demos/loadingDemo.tsx" title="显示加载中"  description="设置loading属性即可在远程搜索时显示加载中，支持延迟显示，默认600毫秒，传入0等同于false"></code>

## API

### DSelectProps

DSelect 继承了 Ant Design Select 的所有属性。

| 参数     | 说明                                                                      | 类型                                                                                 | 默认值 |
| -------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------ |
| options  | 选项数据，可以是一个 options 数组，或一个返回等价 options 数组的 promise  | `DefaultOptionType[]` \| `((params?: any) => Promise<DefaultOptionType[] \| any[]>)` | -      |
| onSearch | 搜索回调函数，返回 Promise 格式的选项数据                                 | `(params?: any) => Promise<DefaultOptionType[] \| any[]>`                            | -      |
| loading  | 是否显示加载中：传入数字表示延迟加载,单位毫秒，0 等同于 false             | `boolean` \| `number`                                                                | -      |
| debounce | 是否开启防抖： true 表示 800 毫秒，true 表示默认值，false 或 0 表示不开启 | `boolean` \| `number`                                                                | false  |
