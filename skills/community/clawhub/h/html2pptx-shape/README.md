# html2pptx-shape

HTML 转 PPTX 形状转换器 — 将 HTML 幻灯片转换为完全可编辑的 PPTX，自动内嵌外部 CSS，保留 CSS 样式、布局，映射为 PPTX 原生形状。

## 快速开始

### 安装依赖

```bash
pip3 install -r requirements.txt
playwright install chromium
```

### 使用示例

```bash
# 基本用法（自动内嵌外部 CSS）
python3 index.py examples/demo.html

# 指定输出文件
python3 index.py input.html output.pptx
```

输出：`<input>_converted.pptx`

---

## 功能特性

✅ **自动 CSS 内嵌** — 将 `<link>` 引用的 CSS 嵌入到 `<style>` 标签  
✅ **CSS 样式保留** — 颜色、字体、边框、背景、阴影  
✅ **布局精确还原** — 绝对定位、尺寸计算  
✅ **PPTX 原生形状** — div→矩形，p/h→文本框，img→图片  
✅ **16:9 标准比例** — 宽屏演示文稿  
✅ **完全可编辑** — 所有文字和形状可在 PowerPoint 中编辑  

---

## 元素映射

| HTML | PPTX |
|------|------|
| `<div>` | 矩形 |
| `<h1>`-`<h6>`, `<p>` | 文本框 |
| `<img>` | 图片 |
| `<svg>` | 占位符 |

---

## CSS 支持

| 属性 | 支持度 |
|------|--------|
| 颜色/字体/字号 | ✅ |
| 边框/圆角/阴影 | ✅ |
| 背景渐变 | ⚠️ 转纯色 |
| CSS 变量 | ✅ |
| Grid/Flex 布局 | ⚠️ 转绝对定位 |
| CSS 动画 | ❌ |

---

## 示例

查看 `examples/demo.html` 和生成的 `demo_converted.pptx` 了解效果。

---

## 完整文档

详见 `SKILL.md`

---

## License

MIT
