---
title: LabelValue
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# LabelValue 标签值组件

LabelValue 是一个用于展示标签和对应值的组件，常用于详情页的信息展示，提供统一的展示格式和灵活的自定义选项，适用于用户信息展示、配置信息展示等场景。

## 组件特性

- 🏷️ 标签值配对展示，结构清晰统一
- 🎨 空值处理机制，自动处理空值显示默认内容
- 🔄 内容格式化支持，可自定义值的展示格式
- 📏 文本省略处理，支持文本过长时的省略显示
- 🎯 灵活布局控制，可控制冒号显示和换行行为

## 基础使用

<code src="./demos/demo1.tsx" ></code>

## 省略冒号

配置 noColon 为 true,省略了中间的冒号

<code src="./demos/demo2.tsx" ></code>

## 空值

值为空时,则默认展示 emptyValue 的属性值
<code src="./demos/demo3.tsx" ></code>

## 自定义显示 value 值

通过传入 React 节点或者配置格式化函数 formatter 可以自定义显示内容

<code src="./demos/demo4.tsx" ></code>

## API

### LabelValueProps

| 参数       | 说明                 | 类型                    | 默认值                             |
| ---------- | -------------------- | ----------------------- | ---------------------------------- |
| label      | 文字标签             | `string` \| `ReactNode` | -                                  |
| value      | 文字标签值           | `string` \| `ReactNode` | -                                  |
| formatter  | 格式化 value 值      | `(\_v?: string          | ReactNode) => string \| ReactNode` |
| emptyValue | 文字标签值为空时的值 | `string` \| `ReactNode` | `'-'`                              |
| className  | 类名                 | `string`                | `''`                               |
| style      | 样式                 | `CSSProperties`         | -                                  |
| noWrap     | 是否不换行           | `boolean`               | `false`                            |
| noColon    | 是否隐藏冒号         | `boolean`               | `false`                            |
