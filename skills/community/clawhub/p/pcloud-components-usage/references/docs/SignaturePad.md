---
title: SignaturePad 电子签名
description: 用于在线手写签名的组件
keywords: ['签名', 'signature', '手写']
demo:
  cols: 2
tocDepth: 3
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# SignaturePad 电子签名

在线手写签名组件，支持触屏和鼠标书写，可用于电子合同、文档签署等场景。

## 组件特性

- 📝 支持手写和鼠标书写
- 📱 适配移动端触摸屏
- 🎨 可自定义笔画颜色和粗细
- 🖼️ 可导出签名图片
- 🔄 支持清除重写
- ⚙️ 丰富的自定义配置

## 代码演示

### 基础用法

最简单的签名板用法。

<code src="./demos/demo1.tsx"></code>

### 自定义样式

可以自定义笔画颜色、粗细和背景色等。

<code src="./demos/demo2.tsx"></code>

### 回显和编辑签名

支持加载已有签名并在其基础上继续编辑。

<code src="./demos/demo3.tsx"></code>

## API

| 参数            | 说明                                   | 类型                        | 默认值      |
| --------------- | -------------------------------------- | --------------------------- | ----------- |
| width           | 画布宽度                               | `number`                    | `600`       |
| height          | 画布高度                               | `number`                    | `200`       |
| penColor        | 线条颜色                               | `string`                    | `'#000000'` |
| penWidth        | 线条粗细                               | `number`                    | `2`         |
| backgroundColor | 背景颜色                               | `string`                    | `'#ffffff'` |
| clearText       | 清除按钮文字                           | `string`                    | `'清除'`    |
| doneText        | 完成按钮文字                           | `string`                    | `'完成'`    |
| showToolbar     | 是否显示工具栏                         | `boolean`                   | `true`      |
| onDone          | 签名完成回调                           | `(dataUrl: string) => void` | -           |
| defaultValue    | 默认签名图片（支持 base64 或图片 URL） | `string`                    | -           |
| className       | 自定义类名                             | `string`                    | -           |
| style           | 自定义样式                             | `CSSProperties`             | -           |
| prefixCls       | 自定义前缀，一般不需要设置             | `string`                    | -           |

### Ref 实例方法

| 名称       | 说明                                                       | 类型                        |
| ---------- | ---------------------------------------------------------- | --------------------------- |
| clear      | 清除画布内容                                               | `() => void`                |
| getDataURL | 获取签名图片的 base64 数据，如果画布不存在则返回 undefined | `() => string \| undefined` |

注意：getDataURL 方法返回的是 PNG 格式的 base64 图片数据。

## FAQ

### 1. 如何获取签名图片？

使用 `onDone` 回调或者 `Ref`实例中的`getDataURL`方法可以获取签名的 base64 图片数据：

```tsx | pure
<SignaturePad
  onDone={(dataUrl) => {
    // 可以直接用于显示
    const img = new Image();
    img.src = dataUrl;
    // 或者下载为文件
    const link = document.createElement('a');
    link.download = 'signature.png';
    link.href = dataUrl;
    link.click();
  }}
/>
```

```tsx | pure
const getUrl = () => {
  signaturePadRef.current?.getDataURL();
};
<SignaturePad ref={signaturePadRef} />;
```

### 2. 如何清除签名？

有两种方式：

1. 使用内置的清除按钮（默认显示）
2. 使用 ref 获取组件实例，调用清除方法

```tsx | pure
import { useRef } from 'react';
import type { SignaturePadHandle } from '@pointcloud/pcloud-components';

const Demo = () => {
  const signaturePadRef = useRef<SignaturePadHandle>(null);

  const handleClear = () => {
    signaturePadRef.current?.clear();
  };

  return <SignaturePad ref={signaturePadRef} />;
};
```

加载的图片会自动按比例缩放并居中显示。你可以在已有签名的基础上继续签名或修改。

### 3. 如何调整画布大小以适应容器？

可以结合 ResizeObserver 来实现自适应大小：

```tsx | pure
const Demo = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 600, height: 200 });

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const observer = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setSize({ width, height });
    });

    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={containerRef} style={{ width: '100%', height: '300px' }}>
      <SignaturePad width={size.width} height={size.height} />
    </div>
  );
};
```
