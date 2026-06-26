---
title: IconFont
nav:
  title: 字体图标组件
  path: /components
group:
  title: 业务组件
---

# IconFont 字体图标组件

IconFont 是一个基于 @ant-design/icons 封装的字体图标组件，摒弃了内置图标集合，支持从 iconfont.cn 平台加载自定义图标，提供全局和局部两种注册方式，适用于需要使用个性化图标集合的项目。

## 组件特性

- 🎨 自定义图标支持，基于 @ant-design/icons 封装
- 🌐 灵活加载方式，支持离线图标和在线 CDN 加载
- 🔧 双模式注册，支持全局注册和局部注册
- 🎯 样式可定制，支持全局设置和自定义图标样式
- 🧹 无内置图标，避免无用图标增加包体积
- 🔗 平台集成，无缝对接 iconfont.cn 图标平台

## 基础使用

<code title="全局注册" src="./demos/demo1.tsx" description="需要在项目入口处注册iconfont的脚本地址,其他组件即可引用使用; iconfont脚本地址需要在[iconfont.cn](https://www.iconfont.cn/)上生成"></code>

## 局部使用

<code title="局部使用" src="./demos/demo2.tsx" description="在组件内部通过scriptUrl属性指定图标脚本地址"></code>

## 自定义样式

<code title="自定义样式" src="./demos/demo3.tsx" description="通过className和style属性自定义图标样式"></code>

## API

### IconFontProps

| 参数      | 说明         | 类型                             | 默认值 |
| --------- | ------------ | -------------------------------- | ------ |
| type      | 图标类型     | `string`                         | -      |
| scriptUrl | 图标脚本地址 | `string` \| `string[]`           | -      |
| className | 图标类名     | `string`                         | -      |
| style     | 图标样式     | `CSSProperties`                  | -      |
| onClick   | 点击事件     | `MouseEventHandler<HTMLElement>` | -      |

### Methods

| 方法名               | 说明                 | 参数类型                             |
| -------------------- | -------------------- | ------------------------------------ |
| setIconfontScriptUrl | 设置全局图标脚本地址 | `(urls: string \| string[]) => void` |
| getTwoToneColor      | 获取双色图标颜色     | `() => string`                       |
| setTwoToneColor      | 设置双色图标颜色     | `(color: string) => void`            |
