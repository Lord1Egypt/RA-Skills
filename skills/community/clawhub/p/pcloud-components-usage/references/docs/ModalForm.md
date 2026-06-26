---
title: ModalForm
nav:
  title: 组件
  path: /components
group:
  title: 组合组件
---

# ModalForm 弹窗表单组件

ModalForm 是一个融合了弹窗和表单功能的组合组件，基于 DModal 和 DForm 封装，提供了一站式的弹窗表单解决方案，简化了弹窗表单的开发流程，适用于各种需要弹窗填写表单的业务场景。

## 组件特性

- 🔄 一体化解决方案，融合弹窗和表单功能
- ✅ 自动表单校验，提交时自动验证表单数据
- 🎯 智能状态管理，禁用表单时自动隐藏底部操作按钮
- 📐 灵活布局支持，支持表单的多种布局方式
- 🧩 内容扩展性强，支持弹窗内嵌其他子级元素
- ⚙️ 集成表单状态管理，支持动态管理表单值
- 🔒 内部 loading 状态锁定, 防止多次点击及误操作

## 基本使用

<code src="./demos/demo1.tsx" ></code>

## 回填数据、禁用表单

<code src="./demos/demo2.tsx" title="回填数据" description="通过`values`属性进行`Form`的内部状态管理, 不同于`initialValues`, `values`更贴合使用场景,可以使用`useState`进行动态更新"></code>

## 布局方式

<code src="./demos/demo3.tsx" ></code>

## API

### ModalFormProps

| 参数       | 说明                             | 类型                                                | 默认值 |
| ---------- | -------------------------------- | --------------------------------------------------- | ------ |
| modalProps | 弹窗属性，支持 DModal 的所有属性 | `DModalProps & { onError?: (_error: any) => void }` | -      |
| formProps  | 表单属性，支持 DForm 的所有属性  | `DFormProps & { values?: any }`                     | -      |
| children   | 子元素                           | `ReactNode`                                         | -      |
