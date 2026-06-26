---
name: pretext-reporter-bao
description: 文本测量和Canvas布局报告工具 - 基于Pretext库，支持多语言文本测量、行布局计算、可视化报告生成
compatibility: opencode
---

# Pretext Reporter

基于 Pretext 库的文本测量和布局报告工具，支持多语言（包括表情符号、BIDI、CJK）、Canvas 可视化输出。

## 主要功能

### 文本测量
- 快速测量文本高度和宽度
- 支持所有语言（中文、日文、韩文、阿拉伯语、希伯来语等）
- 表情符号和混合文本支持
- 避免DOM布局回流，纯算术计算

### 行布局计算
- 自动换行计算
- 支持固定宽度和行高
- 流式布局支持（可变宽度）
- Shrink Wrap - 找到最窄的适配容器

### 报告生成
- 文本统计（字符数、行数）
- 布局信息（高度、宽度）
- 多种输出格式（Markdown、JSON）
- Canvas 可视化（PNG 导出）

## 使用场景

1. **虚拟列表高度计算** - 精确计算项目容器高度
2. **动态UI布局** - 预先测量文本防止布局偏移
3. **Canvas/SVG渲染** - 文本渲染到Canvas或SVG
4. **开发时验证** - 测试按钮标签是否溢出
5. **文本编辑器** - 实现自定义文本编辑和测量

## 核心优势

- **性能优异** - prepare 约19ms，layout 约0.09ms（500个文本批次）
- **无DOM依赖** - 纯算术计算，不触发浏览器回流
- **精确测量** - 使用浏览器字体引擎作为基准
- **全面支持** - 所有语言、表情符号、混合BIDI

## API 对接

使用 Pretext 的核心 API：

```typescript
// 用例1：简单测量
import { prepare, layout } from '@chenglou/pretext'

const prepared = prepare('你好世界 🚀', '16px Inter')
const { height, lineCount } = layout(prepared, 320, 24)

// 用例2：行级控制
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

const prepared = prepareWithSegments('你好世界 🚀', '16px Inter')
const { lines } = layoutWithLines(prepared, 320, 24)

// 用例3：流式布局
import { layoutNextLine } from '@chenglou/pretext'

let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let y = 0

while (true) {
  const width = y < image.bottom ? 300 : 320
  const line = layoutNextLine(prepared, cursor, width)
  if (line === null) break
  
  ctx.fillText(line.text, 0, y)
  cursor = line.end
  y += 24
}
```

## 使用方法

### 基础用法

```typescript
// 测量文本
import { measureText } from '@claw/skills/pretext-reporter-bao'

const result = await measureText('你好世界 🚀', {
  font: '16px Inter',
  maxWidth: 320,
  lineHeight: 24
})

console.log(result)
// {
//   text: '你好世界 🚀',
//   characterCount: 5,
//   lineCount: 1,
//   height: 24,
//   lines: [{ text: '你好世界 🚀', width: 87.5 }]
// }
```

### 生成Canvas报告

```typescript
// 生成Canvas可视化
import { generateCanvasReport } from '@claw/skills/pretext-reporter-bao'

const canvas = await generateCanvasReport('你好世界 🚀', {
  font: '16px Inter',
  maxWidth: 320,
  lineHeight: 24,
  backgroundColor: '#ffffff',
  textColor: '#000000'
})

// 保存或使用Canvas
const png = canvas.toDataURL('image/png')
```

### 流式布局

```typescript
// 流式布局（支持图片环绕等）
import { createFlowLayout } from '@claw/skills/pretext-reporter-bao'

const layout = createFlowLayout('你好世界 🚀', {
  font: '16px Inter',
  lineHeight: 24
})

// 逐行布局
let line
while ((line = layout.nextLine(320)) !== null) {
  console.log(line.text, line.width)
}
```

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|---------|------|
| `font` | string | `'16px Inter'` | 字体（与CSS font属性格式一致） |
| `maxWidth` | number | `320` | 最大宽度（像素） |
| `lineHeight` | number | `24` | 行高（像素） |
| `whiteSpace` | `'normal' \| 'pre-wrap'` | `'normal'` | 空白处理方式 |
| `backgroundColor` | string | `'#ffffff'` | Canvas背景色 |
| `textColor` | string | `'#000000'` | Canvas文字颜色 |

## 输出格式

### Markdown报告

```markdown
# 文本测量报告

## 基本信息
- 文本：你好世界 🚀
- 字符数：5
- 行数：1
- 字体：16px Inter

## 布局信息
- 最大宽度：320px
- 计算高度：24px
- 行高：24px

## 行详情
| 行号 | 文本 | 宽度 |
|------|------|------|
| 1 | 你好世界 🚀 | 87.5px |
```

### JSON报告

```json
{
  "text": "你好世界 🚀",
  "font": "16px Inter",
  "config": {
    "maxWidth": 320,
    "lineHeight": 24,
    "whiteSpace": "normal"
  },
  "stats": {
    "characterCount": 5,
    "lineCount": 1,
    "height": 24
  },
  "lines": [
    {
      "index": 0,
      "text": "你好世界 🚀",
      "width": 87.5,
      "start": { "segmentIndex": 0, "graphemeIndex": 0 },
      "end": { "segmentIndex": 0, "graphemeIndex": 5 }
    }
  ]
}
```

## 性能基准

| 操作 | 时间 | 说明 |
|------|------|------|
| `prepare()` | ~19ms | 500个文本批次（一次性分析） |
| `layout()` | ~0.09ms | 热路径（纯算术计算） |
| `layoutWithLines()` | ~0.12ms | 包含行信息返回 |

## 依赖

- `@chenglou/pretext` - 核心文本测量库（需手动安装）

## 安装说明

**前置步骤：Pretext 还未发布到 npm，需要手动安装：**

```bash
# 方式1：从 GitHub 克隆
git clone https://github.com/chenglou/pretext.git
cd pretext
npm install
npm link  # 全局链接

# 方式2：在项目中本地引用
# 将 pretext 目录复制到 node_modules/@chenglou/pretext
```

**然后安装本 Skill：**
```bash
cd skills/pretext-reporter-bao
npm install
```

## 参考资料

- Pretext GitHub: https://github.com/chenglou/pretext
- Pretext Demo: https://chenglou.me/pretext
- Pretext Docs: https://github.com/chenglou/pretext#readme
