---
title: CRUD
description: 基于DForm和DTable的快速增删改查组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 组合组件
---

# CRUD 组件

CRUD 是基于 DForm 和 DTable 的高阶组件，用于快速实现数据的增删改查功能，整合了表单搜索、数据展示、新增编辑和删除操作，极大简化了业务开发流程。

## 组件特性

- 📝 整合 DForm 表单，支持灵活的搜索配置
- 📊 基于 DTable 组件，提供高效的数据展示和分页
- ➕ 内置新增功能，支持模态框表单配置
- ✏️ 内置编辑功能，自动回显数据到表单
- 🗑️ 内置删除功能，支持单条删除和批量删除
- 👁️ 内置详情查看功能，支持模态框展示
- 🎨 支持自定义操作栏和操作列
- 🔄 智能化刷新策略,支持自主配置
- 📋 支持表格行选择和批量操作
- ⚙️ 支持手动刷新,全屏及列设置（显示/隐藏和拖拽排序）
- 📞 提供丰富的 ref 方法，方便外部调用组件内部功能

## 基础用法

<!-- <code src="./demos/test.tsx" title="自定义操作列" description="通过自定义 actionColumn 配置，实现自定义操作列"></code> -->

<code src="./demos/basicDemo.tsx" title="基础用法" description="整合DForm和DTable组件，实现数据的增删改查功能"></code>

## 自定义操作列

<code src="./demos/customActions.tsx" title="自定义操作列" description="通过自定义 `actionColumn` 配置，实现自定义操作列; 同时也可以通过`ref`调用组件内部的新增,编辑及删除按钮的操作逻辑"></code>

## 立即检索

<code src="./demos/immediateDemo.tsx" title="立即检索" description="`immediate`开启时,会自动隐藏内置的搜索表单按钮,当表单值变化时会自动触发列表请求;建议配合`dInput`的防抖机制,提升用户体验"></code>

## 异步加载表单项

<code src="./demos/asyncDemo.tsx" title="异步加载" description="搜索表单项及弹窗表单项均支持数据的异步加载, 尤其适合于`Select`,`TreeSelect`,`Radio`, `CheckBox`等表单组件中`options`的异步加载"></code>

## 请求参数初始值设置

<code src="./demos/initialParams.tsx" title="请求参数的初始值" description="搜索表单的`initialValues`可以指定列表请求的初始参数. 如果是异步的,建议在请求列表前进行判断,避免不必要的接口请求; 如果是同步的,直接指定值即可."></code>

## 额外请求参数

<code src="./demos/extraParams.tsx" title="额外请求参数" description="`extraParams`接收除内置的检索条件表单外的其他参数,`extraParams`变化时会自动触发条件检索; 尝试更改左侧树的筛选条件,看看控制台的打印参数"></code>

## 全量数据

<code src="./demos/fullDataDemo.tsx" title="全量数据" description="加载全量数据时,设置隐藏分页`hideOnSinglePage`为`true`, 会自动计算列表滚动高度"></code>

## 高级用法

<code src="./demos/advancedDemo.tsx" title="高级用法" description="开启立即检索会自动隐藏`搜索和重置`按钮; 行选择在组件内内置, 默认多选, 可通过`type:'radio'`设置单选, 若要隐藏直接传`undefiend`, 否则不要传, 如果传`{}`, 会覆盖组件内的rowSelection属性,需要在外部组件自定实现相关逻辑;`showEdit`和`showDelete`控制操作列编辑和删除的显示隐藏, 适合需要控制按钮权限的场景"></code>

## API

### CRUDProps

| 参数                   | 说明                                              | 类型                                                                                               | 默认值                                        |
| ---------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| className              | 自定义类名                                        | `string`                                                                                           |                                               |
| style                  | 自定义样式                                        | `React.CSSProperties`                                                                              | `{}`                                          |
| searchFormProps        | 查询表单配置，支持`immediate`属性控制是否立即检索 | [DFormProps](../DForm/index.zh-CN.md/#dformprops) `& { immediate?: boolean }`                      | -                                             |
| tableProps             | 表格配置                                          | [DTableProps](../DTable/index.zh-CN.md#DTableProps)                                                | -                                             |
| modalFormProps         | 新增\编辑\详情表单配置                            | `{ formProps?: DFormProps; modalProps?: DModalProps }`                                             | -                                             |
| deleteModalProps       | 删除确认弹窗配置                                  | 同 Antd [ModalFuncProps](<https://4x-ant-design.antgroup.com/components/modal-cn/#Modal.method()>) | -                                             |
| addButtonProps         | 新增按钮配置                                      | 同 Antd [ButtonProps](https://4x-ant-design.antgroup.com/components/button-cn/#API)                | -                                             |
| addButtonText          | 新增按钮文本                                      | `string`                                                                                           | `'新增'`                                      |
| showAddButton          | 是否显示新增按钮                                  | `boolean`                                                                                          | `true`                                        |
| showBatchDelete        | 是否显示批量删除按钮                              | `boolean`                                                                                          | `true`                                        |
| batchDeleteButtonText  | 批量删除按钮文本                                  | `string`                                                                                           | `'批量删除'`                                  |
| batchDeleteButtonProps | 批量删除按钮配置                                  | 同 Antd [ButtonProps](https://4x-ant-design.antgroup.com/components/button-cn/#API)                | -                                             |
| showEdit               | 是否显示操作列编辑                                | `boolean`                                                                                          | `true`                                        |
| editButtonText         | 行编辑按钮文本                                    | `string`                                                                                           | `'编辑'`                                      |
| editButtonProps        | 编辑按钮配置                                      | 同 Antd [ButtonProps](https://4x-ant-design.antgroup.com/components/button-cn/#API)                | -                                             |
| showDelete             | 是否显示操作列删除                                | `boolean`                                                                                          | `true`                                        |
| deleteButtonText       | 删除按钮文本                                      | `string`                                                                                           | `'删除'`                                      |
| deleteButtonProps      | 删除按钮配置                                      | 同 Antd [ButtonProps](https://4x-ant-design.antgroup.com/components/button-cn/#API)                | -                                             |
| showView               | 是否显示操作列详情                                | `boolean`                                                                                          | `true`                                        |
| viewButtonText         | 行查看按钮文本                                    | `string`                                                                                           | `'查看'`                                      |
| viewButtonProps        | 行查看按钮配置                                    | 同 Antd [ButtonProps](https://4x-ant-design.antgroup.com/components/button-cn/#API)                | -                                             |
| actionBar              | 自定义操作栏                                      | `ReactNode`                                                                                        | -                                             |
| onRefresh              | 数据刷新回调                                      | `() => void`                                                                                       | -                                             |
| crudApi                | CRUD 操作 API 配置                                | [CRUD API](#crud-api)                                                                              | -                                             |
| refreshStrategy        | 全局刷新策略                                      | [RefreshStrategy](#refreshstrategy)                                                                | `{ keepSearchValues: true, keepPage: false }` |
| addRefreshStrategy     | 新增场景刷新策略，优先级高于全局配置              | [RefreshStrategy](#refreshstrategy)                                                                | `{ keepSearchValues: true, keepPage: false }` |
| editRefreshStrategy    | 编辑场景刷新策略，优先级高于全局配置              | [RefreshStrategy](#refreshstrategy)                                                                | `{ keepSearchValues: true, keepPage: true }`  |
| deleteRefreshStrategy  | 删除场景刷新策略，优先级高于全局配置              | [RefreshStrategy](#refreshstrategy)                                                                | `{ keepSearchValues: true, keepPage: true }`  |

### CRUD API

| 参数   | 说明         | 类型                                          | 是否必须 |
| ------ | ------------ | --------------------------------------------- | -------- |
| list   | 列表请求 api | `(params: any) => Promise<DTableSourceProps>` | 是       |
| add    | 新增数据 api | `(params: any) => Promise<any>`               | 是       |
| edit   | 编辑数据 api | `(params: any) => Promise<any>`               | 是       |
| delete | 删除数据 api | `(params: any) => Promise<any>`               | 是       |
| detail | 获取详情 api | `(params: any) => Promise<any>`               | 否       |

### RefreshStrategy

| 参数             | 说明                                 | 类型      |
| ---------------- | ------------------------------------ | --------- |
| keepSearchValues | 是否保留检索条件                     | `boolean` |
| keepPage         | 是否保持当前页码，false 则回到第一页 | `boolean` |

`keepSearchValues`在所有场景下默认为 `true`，表示保留当前的检索条件，其优先级高于 `keepPage`;若 `keepSearchValues` 为 `false`，则 `keepPage` 无效, 因为当检索条件改变时，用户自然期望自动回到第一页, 是否保留`keepPage`将无任何意义。

### CRUDRefProps

| 方法名          | 说明                     | 参数                                             | 返回值                                            |
| --------------- | ------------------------ | ------------------------------------------------ | ------------------------------------------------- |
| refresh         | 刷新表格数据             | \_strategy?: [RefreshStrategy](#refreshstrategy) | -                                                 |
| getSelectedRows | 获取选中的数据           | -                                                | `{ selectedRowKeys: any[]; selectedRows: any[] }` |
| getSearchValues | 获取搜索表单值           | -                                                | `Record<string, any>`                             |
| openAddModal    | 打开内置的新增模态框     | `_record?: any`                                  | -                                                 |
| openEditModal   | 打开内置的编辑模态框     | `_record?: any`                                  | -                                                 |
| openDeleteModal | 打开内置的删除确认模态框 | `_record?: any`                                  | -                                                 |
| openDetailModal | 打开内置的详情模态框     | `_record?: any`                                  | -                                                 |

## 组件依赖

- `DForm` - 表单组件，用于搜索和新增编辑表单
- `DTable` - 表格组件，用于数据展示
- `DModal` - 模态框组件，用于删除的提示弹窗
- `ModalForm` - 模态框表单组件，整合了 DModal 和 DForm

## 使用场景

1. **数据管理页面** - 快速实现数据的增删改查功能
2. **后台管理系统** - 简化各种资源的管理操作
3. **表单搜索 + 表格展示** - 整合搜索和展示功能
4. **标准化业务流程** - 统一数据操作的交互体验
5. **批量操作场景** - 支持表格行选择和批量删除
6. **详情查看场景** - 快速实现数据详情的模态框展示
7. **个性化表格展示** - 通过列设置功能让用户自定义表格列的显示和排序

## 注意事项

1. 如果自定义操作栏, 可以使用`ref`调用内部的方法, 否则需要自行实现相关逻辑;如果有其他逻辑或 UI 需求, 建议使用`DTable`组件自行实现
2. 搜索表单的`initialValues`是用于设置表单项的初始值, 而`extraParams`是用于除搜索表单之外的其他请求参数,比如那些不能通过表单渲染的组件参数, 虽然二者都会在请求参数中, 但在设计上存在区别;
3. `搜索表单`和新增编辑中用到的`弹窗表单`都基于`DForm`,可以使用`initialValues`设置初始值,不同于 Antd 的 Form 组件, `CRUD`在内部进行了优化,因此此处的`initialValues`可以通过`setState`设置.
4. 数据加载依赖 `crudApi` 配置, 建议将 `crudApi` 抽离或使用`useMemo` 缓存, 避免组件刷新时产生额外副作用.
5. 编辑场景回显数据时, 组件内部会默认调用`crudApi.detail`详情接口, 如果没有配置则使用当前数据; 如果表单回显值的层级太深, 则需要在外部进行扁平化处理;
6. 组件已经内置了刷新策略, 在新增,编辑,删除请求完成时会自动刷新数据, 如需阻断刷新, 直接在接口逻辑中抛出异常`throw new Error()`或者`return Promise.reject()`.
7. 搜索表单中的`immediate`属性控制是否为立即检索, 当`immediate`为`true`或者在搜索表单中已经配置了`htmlType`为`submit`和`reset`类型的按钮时, 搜索表单值变化时会自动提交表单数据, 触发搜索请求;
