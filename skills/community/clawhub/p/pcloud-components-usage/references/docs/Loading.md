---
title: Loading
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# Loading 加载组件

Loading 是一个用于展示加载状态的组件，采用单例模式设计，提供函数式调用方式，支持全局和局部加载状态展示，帮助用户了解当前正在进行的操作，提升用户体验。

## 组件特性

- 🔄 单例模式设计，确保全局唯一实例
- ⚡ 函数式调用，使用简便快捷
- 🎯 灵活挂载方式，支持指定容器或全局显示
- ⏱️ 延迟显示支持，避免短暂加载的闪烁问题
- 🎨 样式可定制，支持自定义加载提示文字

## 使用

<code src="./demos/demo1.tsx" ></code>

## 自定义内容

<code src="./demos/demo2.tsx" ></code>

## 指定挂载位置

<code src="./demos/demo3.tsx" ></code>

## hooks 用法

<code src="./demos/demo4.tsx" ></code>

## API

### LoadingInstanceProps

| 参数      | 说明                 | 类型                            | 默认值    |
| --------- | -------------------- | ------------------------------- | --------- |
| container | 加载框容器           | `ReactInstance`                 | `body`    |
| delay     | 延迟显示加载框毫秒数 | `number`                        | `0`       |
| tip       | 加载提示文字         | `string`                        | -         |
| size      | 加载图标大小         | `small` \| `default` \| `large` | `default` |
| spinning  | 是否为加载中状态     | `boolean`                       | `true`    |
| indicator | 自定义加载指示符     | `ReactNode`                     | -         |

### Methods

| 方法名      | 说明                                     | 参数类型                                                               |
| ----------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| open        | 打开加载框                               | `(params?: LoadingInstanceProps) => ILoadingInstance`                  |
| close       | 关闭加载框                               | `() => void`                                                           |
| getInstance | 获取加载框实例                           | `() => ILoadingInstance \| null`                                       |
| useLoading  | React Hook，用于在函数组件中使用加载状态 | `(initialState?: boolean) => { isLoading, openLoading, closeLoading }` |
