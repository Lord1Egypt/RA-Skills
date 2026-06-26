---
title: DTable
description: 基于 antd 4.24.10 Table 的二次封装组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DTable 表格组件

DTable 是基于 Ant Design Table 组件的增强封装，专注于简化数据加载、分页处理和样式定制，提供自动分页加载、异步数据处理等功能，适用于需要展示大量结构化数据的业务场景。

## 组件特性

- 📊 数据加载优化，支持表格数据异步加载和自动分页处理
- ⚡ 智能分页管理，分页变化时自动调用加载函数
- 🎨 样式优化增强，默认提供更好的滚动体验和加载效果
- 🧩 灵活列配置，支持统一设置列属性和独立操作列
- 🎯 表单集成友好，轻松集成到各类表单场景中

## 基础用法

<code src="./demos/basicDemo.tsx" title="基础用法" description="设置loadMore属性即可自动加载表格数据，分页变化时会自动调用该函数，如果在外部监听了分页的onChange事件，则不会触发loadMore，但如果外部onChange返回值为undefined则正常触loadMore"></code>

## 统一设置列配置

<code src="./demos/columnsPropDemo.tsx" title="统一设置列配置" description="columnsProp可以用来统一设置列的基本属性,其设置会被columns中同名属性覆盖"></code>

## 添加操作列

<code src="./demos/actionColumnDemo.tsx" title="添加操作列" description="actionColumn可以在列的最后添加一列操作列，可以是一个column对象，也可以是一个column render函数,该列默认拥有{ width:140, title:'操作', dataIndex:'action' }属性" ></code>

## 指定额外的请求参数

<code src="./demos/extraParamsDemo.tsx" title="指定额外的请求参数" description="extraParams可以指定current和size以外的其他参数,当extraParams发生变化时，自动使用默认分页参数调用loadMore方法" ></code>

## 显示错误信息

<code src="./demos/errorMsgDemo.tsx" title="显示错误信息" description="showErrorMsg可以在loadMore发生错误显示相应的提示信息,可以是布尔值（true按默认规则显示错误信息，false不显示），也可以是一个返回字符串的函数" ></code>

## API

### DTableProps

| 参数               | 说明                                                                                                | 类型                                                        | 默认值                            |
| ------------------ | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | --------------------------------- |
| loadMore           | 表格数据的加载函数,在表格创建、分页变化、额外参数变化时自动运行，如果设置该属性，则 dataSource 失效 | `(params?: TableParamsProps) => Promise<DTableSourceProps>` | -                                 |
| defaultColumnProps | 表格列的基础默认配置,默认所有列居中，表头文字超出显示省略号，详见 antd columns                      | `ColumnsType[]`                                             | { align: 'center',ellipsis: true} |
| actionColumn       | 操作列配置,可以是一个普通列配置对象，也可以是一个 columns 的 render 函数                            | `ColumnType<any> \| ColumnType<any>['render']`              | -                                 |
| showErrorMsg       | 加载数据失败时是否显示错误信息（仅 loadMore 可用时生效）                                            | `boolean \| (err:any) => string`                            | true                              |
| extraParams        | 额外的请求参数,（仅 loadMore 可用时生效）                                                           | `TableParamsProps`                                          | -                                 |
| autoSerialNumber   | 首列自动展示序号                                                                                    | `boolean`                                                   | false                             |

### DTableSourceProps

| 参数    | 说明                                               | 类型       | 默认值 |
| ------- | -------------------------------------------------- | ---------- | ------ |
| records | 表格数据列表，等同于 antd table 的 datasource 属性 | `object[]` | -      |
| total   | 当前请求参数下的列表总数（用于分页）               | `number`   | -      |

### TableParamsProps

| 参数    | 说明     | 类型     | 默认值 |
| ------- | -------- | -------- | ------ |
| current | 当前页码 | `number` | 1      |
| size    | 分页大小 | `number` | 10     |

### Methods

| 方法名             | 说明             | 类型                                                     |
| ------------------ | ---------------- | -------------------------------------------------------- |
| refresh            | 手动刷新表格数据 | ([TableParamsProps](#tableparamsprops)) => void          |
| refreshToPage      | 刷新到指定页码   | `(page: number) => void`                                 |
| getPaginationState | 获取分页状态     | `() => ({current: number, size: number, total: number})` |

其他属性同 antd Table 组件，详见：https://4x-ant-design.antgroup.com/components/table-cn/#API
