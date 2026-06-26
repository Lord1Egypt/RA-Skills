---
title: DModal
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DModal 模态框组件

DModal 是基于 Ant Design Modal 组件的增强封装，提供了更灵活的定位模式和更便捷的使用方式，支持绝对定位和相对定位两种模式，适用于各种场景的弹窗需求。

## 组件特性

- 🎯 多模式定位支持，可选择绝对定位,相对定位,浏览器窗口定位
- 🎨 统一的样式规范，与项目整体设计风格保持一致
- ⚙️ 保留 Ant Design Modal 的所有功能和属性
- 🧩 提供便捷的删除确认框方法，快速实现删除操作确认

## 全局弹框

<code src="./demos/demo1.tsx" title="默认模式" description="默认为绝对定位模式,基于内置的父容器进行定位"></code>

## 浏览器窗口定位

<code src="./demos/demo5.tsx" title="fixed模式" description="即便存在默认的定位父容器,`mode=fixed`时依然优先基于浏览器窗口进行定位"></code>

## 相对弹框

<code src="./demos/demo2.tsx" title="relative模式" description="如果指定mode为relative模式,则会基于自身定位"></code>

## 弹框大小

<code src="./demos/demo3.tsx"></code>

## 弹框自定义显示内容

<code src="./demos/demo4.tsx"></code>

## API

### DModalProps

DModal 继承了 Ant Design Modal 的所有属性。

| 参数                   | 说明                                                             | 类型                                                    | 默认值              |
| ---------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- | ------------------- |
| children               | 自定义弹框内容                                                   | `React.ReactDOM`                                        | -                   |
| mode                   | 定位模式，absolute 为绝对定位，relative 为相对定位               | `absolute` \| `relative` \| `panel` \| `fixed`          | `absolute`          |
| afterClose             | Modal 完全关闭后的回调                                           | `Function`                                              | -                   |
| cancelButtonProps      | cancel 按钮 props                                                | `ButtonProps`                                           | -                   |
| cancelText             | 取消按钮文字                                                     | `ReactNode`                                             | 取消                |
| centered               | 垂直居中展示 Modal                                               | `boolean`                                               | `false`             |
| closable               | 是否显示右上角的关闭按钮                                         | `boolean`                                               | `true`              |
| closeIcon              | 自定义关闭图标                                                   | `ReactNode`                                             | `<CloseOutlined />` |
| confirmLoading         | 确定按钮 loading                                                 | `boolean`                                               | `false`             |
| destroyOnClose         | 关闭时销毁 Modal 里的子元素                                      | `boolean`                                               | `false`             |
| focusTriggerAfterClose | 对话框关闭后是否需要聚焦触发元素                                 | `boolean`                                               | `true`              |
| footer                 | 底部内容，当不需要默认底部按钮时，可以设为  footer={null}        | `ReactNode`                                             | (确定取消按钮)      |
| forceRender            | 强制渲染 Modal                                                   | `boolean`                                               | `false`             |
| getContainer           | 指定 Modal 挂载的节点，但依旧为全局展示，false  为挂载在当前位置 | `HTMLElement\| () => HTMLElement \| Selectors \| false` | `document.body`     |
| keyboard               | 是否支持键盘 esc 关闭                                            | `boolean`                                               | `true`              |
| mask                   | 是否展示遮罩                                                     | `boolean`                                               | `true`              |
| maskClosable           | 点击蒙层是否允许关闭                                             | `boolean`                                               | `true`              |
| maskStyle              | 遮罩样式                                                         | `CSSProperties`                                         | -                   |
| modalRender            | 自定义渲染对话框                                                 | `(node: ReactNode) => ReactNode`                        | -                   |
| okButtonProps          | ok 按钮 props                                                    | `ButtonProps`                                           | -                   |
| okText                 | 确认按钮文字                                                     | `ReactNode`                                             | 确定                |
| okType                 | 确认按钮类型                                                     | `string`                                                | `primary`           |
| style                  | 可用于设置浮层的样式，调整浮层位置等                             | `CSSProperties`                                         | -                   |
| title                  | 标题                                                             | `ReactNode`                                             | -                   |
| wrapClassName          | 对话框外层容器的类名                                             | `string`                                                | -                   |
| onCancel               | 点击遮罩层或右上角叉或取消按钮的回调                             | `Function(e)`                                           | -                   |
| onOk                   | 点击确定回调                                                     | `Function(e)`                                           | -                   |

### DModal.delete

快速创建删除确认框的静态方法。

| 参数     | 说明                    | 类型        | 默认值 |
| -------- | ----------------------- | ----------- | ------ |
| content  | 确认框内容              | `ReactNode` | -      |
| onOk     | 点击确定回调            | `function`  | -      |
| onCancel | 点击取消回调            | `function`  | -      |
| zIndex   | 设置 Modal 的 `z-index` | `number`    | -      |
