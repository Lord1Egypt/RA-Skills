---
title: DynamicFormItem
description: 基于 DForm 的动态表单项组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DynamicFormItem 动态表单项组件

DynamicFormItem 是基于`Antd Form List` 组件的动态表单项管理组件，支持动态添加和删除表单项，提供了丰富的配置选项和灵活的自定义能力。使用时必须被 antd 的`Form` 或者`DForm` 包裹。

## 组件特性

- 🔄 动态增删：支持运行时动态添加和删除表单项
- 🧩 多种控件：支持 input、select、treeSelect、inputNumber 等多种表单控件
- 🎨 自定义渲染：支持自定义组件渲染
- ⚙️ 灵活配置：支持最小/最大项数限制、按钮自定义等
- 📦 嵌套字段：支持 Form 嵌套字段展示

## 基础用法

<code src="./demos/basicDemo.tsx" title="基础用法" description="基本的动态表单项使用"></code>

## 表单控件类型

<code src="./demos/controlTypesDemo.tsx" title="表单控件类型" description="支持的各种表单控件类型"></code>

## 嵌套字段

<code src="./demos/nestDemo.tsx" title="嵌套字段" description="支持嵌套字段"></code>

## 配置选项

<code src="./demos/configDemo.tsx" title="配置选项" description="按钮位置、最小最大项数等配置"></code>

## 图标自定义

<code src="./demos/iconDemo.tsx" title="图标自定义" description="自定义添加和删除按钮图标"></code>

## 自定义组件

<code src="./demos/customComponentDemo.tsx" title="自定义组件" description="使用自定义渲染组件, `custom`方式的自定义渲染不会被`Form.Item`包裹,因此不会注入表单,需要自行实现数据回显等逻辑;而`other`方式则被`Form.Item`包裹, 会自动注入`value`和`onChange`"></code>

## API

### DynamicFormItemProps

扩展自 `FormListProps`，额外属性如下：

| 参数              | 说明                                 | 类型                                  | 默认值        | 版本 |
| :---------------- | :----------------------------------- | :------------------------------------ | :------------ | :--- |
| itemConfig        | 表单项配置，基于 DForm 的 DItemProps | `DItemProps \| DItemProps[]`          | -             |      |
| initialValue      | 初始值                               | `any[]`                               | `[undefined]` |      |
| addButtonText     | 新增按钮文本                         | `string`                              | `'添加'`      |      |
| addButtonProps    | 新增按钮属性                         | `React.ComponentProps<typeof Button>` | `{}`          |      |
| addAtHead         | 是否添加到头部                       | `boolean`                             | `false`       |      |
| removeButtonText  | 删除按钮文本                         | `string`                              | `'移除'`      |      |
| removeButtonProps | 删除按钮属性                         | `React.ComponentProps<typeof Button>` | `{}`          |      |
| minItems          | 最小项数                             | `number`                              | `0`           |      |
| maxItems          | 最大项数                             | `number`                              | -             |      |
| showAdd           | 是否显示添加按钮                     | `boolean`                             | `true`        |      |
| showRemove        | 是否显示删除按钮                     | `boolean`                             | `true`        |      |
| addPosition       | 添加按钮位置                         | `'top' \| 'bottom'`                   | `'bottom'`    |      |

## 注意事项

- 组件必须被 antd 的`Form` 或者`DForm` 包裹
- 组件内部使用 `Form.List` 管理动态字段，确保与 antd Form 的兼容性
- `value` 和 `onChange` 必须配套使用以实现完全受控
- 自定义组件时，需要确保渲染的内容符合表单验证要求
- 父容器 Form 组件 laypout 为垂直布局时, 删除按钮会错位,需要外部覆盖样式`align-items: flex-end;`
