---
title: ConfigProvider
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 其他
---

# ConfigProvider 全局化配置

为组件提供统一的全局化配置。

## 使用

GlobalConfig 使用 React 的 context 特性，只需在应用外围包裹一次即可全局生效。

```jsx | pure
import { ConfigProvider } from '@pointcloud/pcloud-components';
import zhCN from 'antd/locale/zh_CN';

export default () => (
  <ConfigProvider prefixCls="myClassName" locale={zhCN}>
    <App />
  </ConfigProvider>
);
```

## 其他

该组件的 `prefixCls` 属性，只适用于本组件库,不会对 `antd` 组件生效, 且不会覆盖默认值`pui`,而是取并集; 假如设置 `prefixCls='test'`，则生效类名为`"text-search pui-search"`,原 `antd` 组件类名不会变化。开发者可自行覆盖样式。

## API

| 参数名称  | 说明             | 类型              | 默认值 |
| --------- | ---------------- | ----------------- | ------ |
| prefixCls | 全局样式类名前缀 | `string`          | `pui`  |
| children  | children 节点    | `React.ReactNode` |        |

其他参数完全继承 [Ant Design ConfigProvider](https://4x-ant-design.antgroup.com/components/config-provider-cn/#API)
