---
title: OrgTree 组织树
description: 基于 react-org-tree 的组织架构树组件
keywords: ['组织树', '树形展示', '组织架构图']
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 数据展示
  order: 2
---

# OrgTree 组织架构树

OrgTree 是基于 react-org-tree 的组织架构树组件，用于展示组织层级关系，支持垂直和水平两种布局方式，并提供丰富的自定义选项。

## 组件特性

- 🌳 支持垂直和水平两种布局方式
- 🎨 支持自定义节点的内容, 样式和标签宽度
- 📦 支持节点折叠/展开控制
- 🎯 提供丰富的 API 和事件回调
  点击回调

## 基本使用

<code src="./demos/basic.tsx" description="最简单的用法，展示基本组织架构树。"></code>

## 水平布局

<code src="./demos/horizontal.tsx" description="水平方向展示组织架构树。"></code>

## 折叠控制

<code src="./demos/collapse.tsx" description="collapse树形可以控制节点的折叠/展开状态。"></code>

## 标签样式

<code src="./demos/label-styles.tsx" description="自定义节点标签的宽度和样式"></code>

## 自定义渲染节点

<code src="./demos/custom-node.tsx" description="自定义渲染节点"></code>

## API

### OrgTreeProps

| 参数           | 说明                                                    | 类型                                                   | 默认值 |
| -------------- | ------------------------------------------------------- | ------------------------------------------------------ | ------ |
| data           | 组织树数据                                              | [OrgTreeNode](#orgtreenode)                            | -      |
| horizontal     | 是否水平布局                                            | boolean                                                | false  |
| collapsable    | 是否允许节点折叠，默认为 true，可在单个节点上覆盖此设置 | boolean                                                | true   |
| expandAll      | 是否默认展开所有节点                                    | boolean                                                | false  |
| labelWidth     | 标签宽度，可以是数字(像素)或字符串                      | string \| number                                       | auto   |
| labelClassName | 标签自定义类名，用于自定义标签样式                      | string                                                 | -      |
| className      | 自定义类名                                              | string                                                 | -      |
| style          | 自定义样式                                              | React.CSSProperties                                    | -      |
| renderContent  | 自定义渲染节点内容                                      | (node: [OrgTreeNode](#orgtreenode)) => React.ReactNode | -      |

### OrgTreeNode

| 参数        | 说明           | 类型                          | 默认值 |
| ----------- | -------------- | ----------------------------- | ------ |
| id          | 节点唯一标识   | string \| number              | -      |
| label       | 节点显示文本   | string                        | -      |
| title       | 节点标题       | string                        | -      |
| children    | 子节点         | [OrgTreeNode](#orgtreenode)[] | -      |
| expand      | 节点是否展开   | boolean                       | -      |
| collapsable | 节点是否可折叠 | boolean                       | -      |
| className   | 自定义节点类名 | string                        | -      |

### 事件回调

| 事件名  | 说明           | 参数                                                     |
| ------- | -------------- | -------------------------------------------------------- |
| onClick | 节点点击时触发 | (e: React.MouseEvent, node: [OrgTreeNode](#orgtreenode)) |

## 注意事项

1. 组件依赖于 `react-org-tree`，使用前请确保已安装该依赖。
2. 数据结构必须包含 `id` 和 `label` 字段，`children` 字段用于表示子节点。
3. 在大数据量情况下，建议使用虚拟滚动或分页加载，以避免性能问题。
