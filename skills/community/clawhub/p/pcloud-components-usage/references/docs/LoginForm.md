---
title: LoginForm
description: 基于 DForm 组件封装的登录表单，内置用户名、密码表单项及校验规则
keywords: ['登录表单', 'LoginForm', '表单', '认证']
nav:
  title: 组件
  path: /components
group:
  title: 组合组件
  order: 2
---

# LoginForm 登录表单

基于 DForm 组件封装的登录表单，内置用户名、密码表单项及校验规则，支持添加额外表单项和登录按钮。

## 组件特性

- ✅ 内置用户名和密码字段及校验规则
- 🎨 支持自定义表单项配置
- ➕ 支持添加额外表单项（如验证码）
- ⚙️ 继承 DForm 和 Ant Design Form 的所有属性
- 🔄 支持异步登录处理和加载状态

## 代码演示

### 基础用法

<code src="./demos/demo1.tsx"></code>

### 带验证码的登录表单

<code src="./demos/demo2.tsx" title="额外配置表单" description="`extraItems`支持用户配置额外的表单项,比如验证码;额外的表单项会被插入在登录按钮之前"></code>

### 自定义表单项配置及样式

<code src="./demos/demo3.tsx" title="自定义配置及样式" description="通过`usernameItem`, `passwordItem`, `loginButtonItem`来自定义输入框或者登录按钮的配置和样式"></code>

## API

### LoginForm

LoginForm 继承了 [DForm](/components/d-form) 的所有属性.

| 参数                | 说明                 | 类型                                     | 默认值       |
| ------------------- | -------------------- | ---------------------------------------- | ------------ |
| extraItems          | 登录表单额外的表单项 | [DItemProps](/components/d-form#ditem)[] | `[]`         |
| onFinish            | 点击登录按钮的回调   | `(values: any) => void \| Promise<any>`  | -            |
| loginText           | 登录按钮文本         | `string`                                 | `登录`       |
| loginButtonDisabled | 是否禁用登录按钮     | `boolean`                                | `false`      |
| usernameItem        | 用户名表单项配置     | `Partial<DItemProps>`                    | 见下方默认值 |
| passwordItem        | 密码表单项配置       | `Partial<DItemProps>`                    | 见下方默认值 |
| loginButtonItem     | 登录按钮表单项配置   | `Partial<DItemProps>`                    | 见下方默认值 |

### 默认值

#### usernameItem 默认值

```tsx | pure
{
  name: 'username',
  label: '用户名',
  renderType: 'input',
  formItemProps: {
    rules: [
      {
        required: true,
        message: '请输入用户名',
      },
    ],
  },
  placeholder: '请输入用户名',
  prefix: <UserOutlined />,
}
```

#### passwordItem 默认值

```tsx | pure
{
  name: 'password',
  label: '密码',
  renderType: 'password',
  formItemProps: {
    rules: [
      {
        required: true,
        message: '请输入密码',
      },
    ],
  },
  placeholder: '请输入密码',
  prefix: <LockOutlined />,
}
```

#### loginButtonItem 默认值

```tsx | pure
{
  renderType: 'button',
  type: 'primary',
  htmlType: 'submit',
  label: '登录',
  block: true,
}
```

## 注意事项

1. `extraItems` 中的表单项会插入在默认的用户名、密码字段之后，登录按钮之前
2. `onFinish` 回调支持返回 Promise，用于处理异步登录逻辑
3. 登录按钮会自动在处理过程中显示加载状态
4. 可通过 `usernameItem`、`passwordItem` 和 `loginButtonItem` 分别自定义对应表单项的属性
5. 组件内部使用了 `DForm.useForm()` 创建表单实例，如需外部控制表单，可通过 `form` 属性传入自定义表单实例
