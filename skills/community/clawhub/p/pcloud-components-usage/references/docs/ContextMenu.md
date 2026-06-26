---
title: ContextMenu 右键菜单
description: 自定义右键菜单组件
keywords: ['右键菜单', 'context menu', '自定义菜单']
demo:
  cols: 2
tocDepth: 3
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# ContextMenu 右键菜单

用于展示自定义的右键菜单内容，可以与 Antd Menu 组件结合使用。

## 组件特性

- 🎯 支持自定义触发区域
- 📦 灵活的菜单内容
- 🔄 智能边界处理
- ⌨️ 支持键盘操作（ESC 关闭）
- 🎨 可自定义样式

## 代码演示

### 基础用法

最简单的右键菜单使用。

<code src="./demos/demo1.tsx"></code>

### 配合 Antd Menu

使用 Antd Menu 组件来构建菜单内容。

<code src="./demos/demo2.tsx"></code>

### 自定义挂载容器

通过 getPopupContainer 指定菜单挂载的父节点，实现滚动区域内的菜单定位。

<code src="./demos/demo3.tsx"></code>

## API

| 参数              | 说明                 | 类型                                        | 默认值                |
| ----------------- | -------------------- | ------------------------------------------- | --------------------- |
| className         | 自定义类名           | `string`                                    | -                     |
| style             | 自定义样式           | `CSSProperties`                             | -                     |
| children          | 菜单内容             | `ReactNode`                                 | -                     |
| trigger           | 触发区域内容         | `ReactNode`                                 | -                     |
| closeOnOutside    | 点击外部是否关闭     | `boolean`                                   | `true`                |
| offset            | 展示位置偏移量       | `{ x?: number; y?: number }`                | `{ x: 0, y: 0 }`      |
| onShow            | 菜单显示时的回调     | `() => void`                                | -                     |
| onHide            | 菜单隐藏时的回调     | `() => void`                                | -                     |
| getPopupContainer | 指定菜单挂载的父节点 | `(triggerNode: HTMLElement) => HTMLElement` | `() => document.body` |

## FAQ

### 1. 如何处理菜单项点击事件？

你可以在菜单内容中直接添加点击事件处理器：

```tsx | pure
<ContextMenu trigger={<div>触发区域</div>}>
  <div className="ant-context-menu-item" onClick={() => console.log('点击了编辑')}>
    编辑
  </div>
</ContextMenu>
```

### 2. 如何控制菜单的显示位置？

使用 `offset` 属性可以调整菜单的显示位置：

```tsx | pure
<ContextMenu offset={{ x: 10, y: 10 }} trigger={<div>触发区域</div>}>
  菜单内容
</ContextMenu>
```

### 3. 如何阻止特定区域的默认右键菜单？

在触发区域上添加 `onContextMenu` 事件处理：

```tsx | pure
<div onContextMenu={(e) => e.preventDefault()}>
  <ContextMenu trigger={<div>触发区域</div>}>菜单内容</ContextMenu>
</div>
```

### 4. 如何在菜单中使用图标？

可以直接使用 Antd 的图标组件：

```tsx | pure
import { EditOutlined } from '@ant-design/icons';

<ContextMenu trigger={<div>触发区域</div>}>
  <div className="ant-context-menu-item">
    <EditOutlined /> 编辑
  </div>
</ContextMenu>;
```

### 5. 如何创建多级菜单？

推荐使用 Antd 的 Menu 组件来创建多级菜单：

```tsx | pure
import { Menu } from 'antd';

const items = [
  {
    key: '1',
    label: '选项1',
    children: [
      {
        key: '1-1',
        label: '子选项1',
      },
    ],
  },
];

<ContextMenu trigger={<div>触发区域</div>}>
  <Menu items={items} mode="vertical" />
</ContextMenu>;
```
