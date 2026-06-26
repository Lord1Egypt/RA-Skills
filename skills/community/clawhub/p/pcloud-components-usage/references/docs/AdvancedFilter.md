---
title: AdvancedFilter
description: 高级搜索组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# AdvancedFilter 高级搜索组件

AdvancedFilter 是一个功能丰富的搜索筛选组件，集成了关键字搜索和高级筛选面板，支持多种表单控件类型，可帮助用户快速构建复杂的业务筛选功能。

## 组件特性

- 🔍 集成关键字搜索与高级筛选面板，提供一体化搜索体验
- 🧩 支持多种表单控件类型（输入框、选择器、日期选择器、开关等）
- 🎨 灵活布局，支持自定义左右两侧内容区域
- ⚡ 响应式设计，适配不同屏幕尺寸
- 🔄 完整的表单方法支持，可轻松集成到现有业务流程中

## 基础使用

<code src="./demos/demo1.tsx" ></code>

## 自定义两侧渲染区

<code src="./demos/demo2.tsx" ></code>

## 自定义筛选项

<code src="./demos/demo3.tsx" ></code>

## API

|    参数名称    | 说明               |           类型            |   默认值   |
| :------------: | :----------------- | :-----------------------: | :--------: |
| formItemConfig | 筛选项配置         |  [FormItem[]](#formitem)  | (required) |
| onValuesChange | 筛选项值变更时触发 |       `(v) => void`       |            |
|    onSearch    | 点击查询按钮时触发 |       `(v) => void`       |            |
|    onReset     | 点击重置按钮时触发 |       `() => void`        |            |
|      left      | 左侧内容区         |     `React.ReactNode`     |            |
|     right      | 右侧内容区         |     `React.ReactNode`     |            |
|   inputProps   | input 框的 props   | [InputProps](#inputprops) |            |
|    children    | children 节点      |     `React.ReactNode`     |            |
|      fRef      | 表单引用 ref 值    |           `any`           |            |
|      icon      | 筛选文字按钮图标   |     `React.ReactNode`     |            |

### FormItem

|  参数名称   | 说明                                                 |                                                    类型                                                    |       默认值        |
| :---------: | :--------------------------------------------------- | :--------------------------------------------------------------------------------------------------------: | :-----------------: |
|    label    | 筛选项 label 文字                                    |                                                  `string`                                                  |                     |
|    name     | 筛选项字段名                                         |                                                  `string`                                                  |                     |
|    type     | 筛选项类型                                           | `input \| inputNumber \| radio \| select \| checkbox \| datePicker \| rangePicker \| switch \| treeSelect` |                     |
| placeholder | 筛选项 placeholder                                   |                                                  `string`                                                  |                     |
|   options   | 筛选项的配置项(select \| treeSelect 时可用)          |                                               `同 antd 组件`                                               |                     |
|   format    | 筛选项的格式化配置(rangePicker \| datePicker 时可用) |                                                  `string`                                                  | YYYY-MM-DD HH:mm:ss |

### InputProps

|  参数名称   | 说明                                   |        类型        |   默认值   |
| :---------: | :------------------------------------- | :----------------: | :--------: |
| placeholder | input 检索框 placeholder               |      `string`      |            |
|    name     | input 检索框字段名                     |      `string`      | (required) |
| inputSearch | input 检索框回车时或点击检索图标时触发 | `(v: any) => void` |            |

方法同 antd Form 组件，详见：https://4x-ant-design.antgroup.com/components/form-cn/#FormInstance
