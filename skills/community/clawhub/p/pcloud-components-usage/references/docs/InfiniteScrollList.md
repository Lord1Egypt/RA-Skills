---
title: InfiniteScrollList
nav:
  title: 无限滚动列表组件
  path: /components
group:
  title: 组合组件
---

# InfiniteScrollList 无限滚动列表组件

InfiniteScrollList 是一个支持无限滚动加载的列表组件，自动处理分页加载逻辑，提供加载状态提示和回到顶部功能，适用于大量数据展示的场景，能够有效提升页面性能和用户体验。

## 组件特性

- 📜 无限滚动加载，自动处理分页和数据请求
- ⚡ 高性能渲染，支持大数据量流畅展示
- 🔄 智能加载状态，内置加载中和加载完成提示
- 🎯 快速回顶功能，内置回到顶部按钮
- 🎨 灵活内容渲染，支持自定义列表项渲染方式
- 📐 栅格布局支持，可配置网格化列表展示
- 🎯 智能事件处理，内置事件委托提升性能，小数据量支持自定义事件绑定

## 基础用法

<code src="./demos/demo1.tsx" title="基础用法" description="最基本的用法,没有额外参数"></code>

## 携带参数

<code src="./demos/demo2.tsx" title="携带参数" description="携带参数时,组件会对内置的分页参数 `{ current:1, size: 10 }` 和传递进来的参数进行浅合并,并会在loadMore函数中将最终请求的参数抛出;支持将内置分页参数覆盖"></code>

## 栅格列表

<code src="./demos/demo3.tsx" title="栅格列表" description="通过grid属性配置栅格列表"></code>

## API

### InfiniteScrollListProps

| 参数             | 说明                               | 类型                                                                   | 默认值            |
| ---------------- | ---------------------------------- | ---------------------------------------------------------------------- | ----------------- |
| containerId      | 容器 id                            | `string`                                                               | `'scrollableDiv'` |
| itemKey          | 列表项的唯一标识字段               | `string`                                                               | `'id'`            |
| containerHeight  | 容器高度(超过此高度将滚动)         | `number` \| `string`                                                   | -                 |
| initialParams    | 列表请求的初始参数                 | `any`                                                                  | `{}`              |
| loadMore         | 列表请求方法                       | `(params?: T) => Promise<{ data: { total: number; records: any[] } }>` | -                 |
| renderItem       | 列表项的渲染方法                   | `(item: P, index: number) => ReactNode`                                | -                 |
| grid             | 栅格配置                           | `object`                                                               | -                 |
| className        | 类名                               | `string`                                                               | `''`              |
| scrollThreshold  | 滚动阈值                           | `string` \| `number`                                                   | `'100px'`         |
| visibilityHeight | 滚动高度达到此参数值才出现 BackTop | `number`                                                               | `200`             |
| showBackTop      | 是否显示 BackTop                   | `boolean`                                                              | `true`            |
| endMessage       | 列表底部提示                       | `ReactNode`                                                            | -                 |
| onItemClick      | 列表项点击事件                     | `(item: P, index: number) => void`                                     | -                 |
