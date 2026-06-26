---
title: ErrorBoundary
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

## 基础使用

```jsx
import * as React from 'react';
import { ErrorBoundary } from '@pointcloud/pcloud-components';

const Test = () => {
  const err = '网络开小差了...';
  return <ErrorBoundary err={err} />;
};
export default Test;
```

## API

| 参数名称  | 说明         | 类型     | 默认值               |
| --------- | ------------ | -------- | -------------------- |
| className | 容器样式类名 | `string` | `pui-error-boundary` |
| err       | 错误信息     | `any`    | ——                   |
