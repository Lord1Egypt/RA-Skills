---
name: pcloud-components-usage
description: Use when developer needs to install, use, or look up components from @pointcloud/pcloud-components npm package
---

# pcloud-components Usage Guide

## Overview

`@pointcloud/pcloud-components` is a React component library based on Ant Design v4.24.16 and React v18. Contains 30+ business components for enterprise mid-backend products.

## Quick Start

### Installation

```bash
# npm
npm install @pointcloud/pcloud-components

# yarn
yarn add @pointcloud/pcloud-components

# pnpm
pnpm add @pointcloud/pcloud-components
```

### Peer Dependencies (Required)

```bash
npm install @ant-design/icons@^4.8.3 antd@^4.24.16 react@18 react-dom@18
```

### Basic Usage

```jsx
import React from 'react';
import { DCascader } from '@pointcloud/pcloud-components';

const App = () => {
  const handleChange = (value, selectedOptions) => {
    console.log(value, selectedOptions);
  };

  return <DCascader showSearch placeholder="请选择" onChange={handleChange} />;
};

export default App;
```

### Using Form Components (DForm)

```jsx
import { DForm } from '@pointcloud/pcloud-components';

const App = () => {
  const onFinish = (values) => {
    console.log('表单值:', values);
  };
  const items = [
    {
      label: '用户名',
      name: 'username',
      rules: [{ required: true, message: '请输入用户名' }],
      renderType: 'input',
    },
    {
      label: '状态',
      name: 'status',
      rules: [{ required: true, message: '请选择状态' }],
      renderType: 'select',
      options: [
        { label: '启用', value: 1 },
        { label: '禁用', value: 0 },
      ],
    },
    {
      label: '提交',
      renderType: 'button',
      type: 'primary',
      htmlType: 'submit',
    },
  ];

  return <DForm onFinish={onFinish} items={items}></DForm>;
};
```

### UMD/CDN Usage

```html
<link rel="stylesheet" href="https://unpkg.com/@pointcloud/pcloud-components@1.0.0/dist/umd/pcloud-components.min.css" />
<script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@pointcloud/pcloud-components@1.0.0/dist/umd/pcloud-components.min.js"></script>
```

## Component List

### Form Components

| Component | Description |
| --------- |-------------|
| DForm | Enhanced form based on Ant Design Form |
| DInput | Enhanced input component |
| DSelect | Select with async loading support |
| DCascader | Cascader with async loading support |
| DTreeSelect | TreeSelect with async loading support |
| DUpload | File upload component |
| DRangePicker | Date range picker |
| DynamicFormItem | Dynamic form component |

### Data Display

| Component | Description |
| --------- |-------------|
| DTable | Enhanced table component |
| LabelValue | Label-value display component |
| WordCloud | Word cloud visualization |
| ScrollNumber | Number animation component |
| AspectRatio | Aspect ratio container |
| NoData | No data display component |
| IPAddress | IP address input component |
| AnimatedScrollList | Animated scroll list |
| OrgTree | Organization tree component |
| TypewriterText | Typewriter effect component |
| ErrorBoundary | Error boundary component |
| IconFont | Custom icon component |

### Modal

| Component | Description |
| --------- |-------------|
| DModal | Enhanced modal component |
| ModalForm | Modal form component |
| LoginForm | Login form component |

### Other Components

| Component | Description |
| --------- |-------------|
| Loading | Global loading component |
| ContextMenu | Right-click menu component |
| AdvancedFilter | Advanced filter component |
| InfiniteScrollList | Infinite scroll list |
| PictureCard | Picture card component |
| SignaturePad | Signature pad component |
| RndDrag | Draggable resizable component |
| RCropper | Image cropper component |
| CRUD | CRUD operation component |
| AuthComponent | Permission component |
| ColorPicker | Color picker component |

## Import All Components

```jsx
import * as PCloud from '@pointcloud/pcloud-components';
// PCloud.DForm, PCloud.DTable, etc.
```

## Documentation

Online docs: https://frank17008.github.io/pcloud-components

## Detailed Component Reference

所有组件的详细文档已内置在 skill 中，位置: `references/docs/组件名.md`

### 表单组件

| 组件 | 文档 |
|------|------|
| DForm | `references/docs/DForm.md` |
| DInput | `references/docs/DInput.md` |
| DSelect | `references/docs/DSelect.md` |
| DCascader | `references/docs/DCascader.md` |
| DTreeSelect | `references/docs/DTreeSelect.md` |
| DUpload | `references/docs/DUpload.md` |
| DRangePicker | `references/docs/DRangePicker.md` |
| DynamicFormItem | `references/docs/DynamicFormItem.md` |

### 数据展示组件

| 组件 | 文档 |
|------|------|
| DTable | `references/docs/DTable.md` |
| NoData | `references/docs/NoData.md` |
| Loading | `references/docs/Loading.md` |
| LabelValue | `references/docs/LabelValue.md` |
| ScrollNumber | `references/docs/ScrollNumber.md` |
| TypewriterText | `references/docs/TypewriterText.md` |
| WordCloud | `references/docs/WordCloud.md` |
| AspectRatio | `references/docs/AspectRatio.md` |
| AnimatedScrollList | `references/docs/AnimatedScrollList.md` |
| ErrorBoundary | `references/docs/ErrorBoundary.md` |
| IconFont | `references/docs/IconFont.md` |
| IPAddress | `references/docs/IPAddress.md` |
| OrgTree | `references/docs/OrgTree.md` |

### 模态框组件

| 组件 | 文档 |
|------|------|
| DModal | `references/docs/DModal.md` |
| ModalForm | `references/docs/ModalForm.md` |
| LoginForm | `references/docs/LoginForm.md` |

### 其他组件

| 组件 | 文档 |
|------|------|
| CRUD | `references/docs/CRUD.md` |
| AdvancedFilter | `references/docs/AdvancedFilter.md` |
| ContextMenu | `references/docs/ContextMenu.md` |
| InfiniteScrollList | `references/docs/InfiniteScrollList.md` |
| PictureCard | `references/docs/PictureCard.md` |
| SignaturePad | `references/docs/SignaturePad.md` |
| RndDrag | `references/docs/RndDrag.md` |
| RCropper | `references/docs/RCropper.md` |
| AuthComponent | `references/docs/AuthComponent.md` |
| ColorPicker | `references/docs/ColorPicker.md` |
| ConfigProvider | `references/docs/ConfigProvider.md` |

### 在线文档

如需最新在线版本: https://frank17008.github.io/pcloud-components

## Environment Requirements

- React >= 18
- Ant Design <= 6.x
- Node >= 16.20.0
- Modern browsers

## Common Issues

1. **Missing peer dependencies**: Ensure `@ant-design/icons`, `antd`, `react`, `react-dom` are installed
2. **Version mismatch**: This library requires React 18 and Ant Design 4.x
3. **Style not loading**: Import component CSS or use ConfigProvider for global styles