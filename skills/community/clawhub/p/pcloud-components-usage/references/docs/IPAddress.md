---
title: IPAddress
nav:
  title: IP地址输入框
  path: /components
group:
  title: 业务组件
---

# IPAddress IP 地址输入框组件

IPAddress 是一个专门用于输入和展示 IP 地址的组件，支持 IPv4 和 IPv6 两种格式，提供自动聚焦、格式校验和标准化输出等功能，适用于网络配置、设备管理等需要输入 IP 地址的场景。

## 组件特性

- 🌐 双版本支持，同时支持 IPv4 和 IPv6 格式输入
- ⌨️ 智能输入体验，支持输入过程自动聚焦到下一节
- ✅ 格式校验机制，自动校验和修正输入内容
- 🎨 样式兼容设计，完美匹配 antd input 框样式
- 🔧 表单友好集成，无缝支持表单嵌入和校验
- 🔄 IPv6 标准化输出，自动简化标准格式的 IPv6 地址

## 基础用法

<code src="./demos/demo1.tsx" title="基础用法" description="通过`value`设置绑定值, type可选值为`IPv4`和`IPv6`"></code>

## 基础样式

<code src="./demos/demo2.tsx" title="三种大小" description="定义了三种尺寸（大、默认、小），完全对照antd的input输入框"></code>

## 分隔符

<code src="./demos/demo3.tsx" title="分隔符" description="通过`delimiter`设置分隔符,支持自定义react元素或者字符串"></code>

## 只读和禁用

<code src="./demos/demo4.tsx" title="只读和禁用" description="`readOnly`设置只读, `disabled`设置禁用,样式完全对标antd"></code>

## 标准化输出

<code src="./demos/demo5.tsx" title="IPv6标准化处理" description="`normalize`可以控制输出的IPv6地址是否进行简化;首选格式是RFC文档定义的规范全写形式,简化形式是采用了`最长零段压缩`和`前导零省略‌`的标准进行输出."></code>

## 自动聚焦

<code src="./demos/demo6.tsx" title="自动聚焦" description="开始自动聚焦时,在输入过程中,如果字符长度达到单个输入框上限,则会自动跳转到下一个输入框进行聚焦"></code>

## API

| 参数名称     | 说明                                                  | 类型                                                  | 默认值                      |
| ------------ | ----------------------------------------------------- | ----------------------------------------------------- | --------------------------- |
| className    | 自定义类名                                            | `string`                                              | -                           |
| style        | 自定义样式                                            | `React.CSSProperties`                                 | -                           |
| value        | 当前 IP 地址值                                        | `string`                                              | -                           |
| type         | IP 地址类型，可选 IPv4 或 IPv6                        | `'IPv4' \| 'IPv6'`                                    | 'IPv4'                      |
| delimiter    | 自定义分隔符元素                                      | `React.ReactNode`                                     | 自动根据类型显示 ':' 或 '·' |
| readOnly     | 是否只读模式                                          | `boolean`                                             | false                       |
| disabled     | 是否禁用状态                                          | `boolean`                                             | false                       |
| size         | 输入框尺寸大小                                        | `'small'` \| `'middle'` \| `'large'`                  | middle                      |
| autoComplete | 自动聚焦到下一个输入框                                | `boolean`                                             | true                        |
| normalize    | 是否对 IPv6 地址进行标准化输出（前导零省略/零段压缩） | `boolean`                                             | true                        |
| inputProps   | 内部 input 元素的额外属性                             | `{ style?: React.CSSProperties; [key: string]: any }` | -                           |
| onChange     | 值变化时的回调函数                                    | `(value: string) => void`                             | -                           |
| onFocus      | 获得焦点时的回调                                      | `(value: string, index: number) => void`              | -                           |
| onBlur       | 失去焦点时的回调                                      | `(value: string, index: number) => void`              | -                           |
