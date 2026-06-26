# Pretext Reporter Bao

基于 Pretext 库的文本测量和布局报告工具，支持多语言、表情符号、混合 BIDI 文本。

## 特性

- ⚡ **超快性能** - prepare 约 19ms，layout 约 0.09ms
- 🌍 **全语言支持** - 中文、日文、韩文、阿拉伯语、希伯来语、表情符号
- 🎨 **Canvas 可视化** - 生成 PNG 报告
- 📊 **多格式报告** - Markdown、JSON
- 🔀 **流式布局** - 支持动态宽度、图片环绕
- 📐 **Shrink Wrap** - 找到最窄的适配容器

## 安装

### 步骤 1: 安装 Pretext

**Pretext 已包含在 Skill 目录中！** 无需额外下载。

```bash
cd skills/pretext-reporter-bao

# Pretext 已在 ./pretext 目录中
# 如果需要重新构建 Pretext:
cd pretext
npm install -g typescript
tsc -p tsconfig.build.json
cd ..
```

### 步骤 2: 安装本 Skill 依赖

```bash
cd skills/pretext-reporter-bao
npm install
```

### 步骤 3: 测试安装

```bash
# 运行基础导入测试
node test.mjs
```

**预期输出：**
```
🧪 Pretext 基础导入测试

📦 测试 1: 导入 Pretext 模块
   ✅ 成功导入 Pretext

📦 测试 2: 导入 Inline Flow 模块
   ✅ 成功导入 Inline Flow
```

### 步骤 4: 构建 TypeScript

```bash
npm run build
```

## 使用方法

### 1. 文本测量

```typescript
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
//   maxWidth: 320,
//   lineHeight: 24,
//   lines: [{ text: '你好世界 🚀', width: 87.5 }]
// }
```

### 2. 生成Canvas报告

```typescript
import { generateCanvasReport } from '@claw/skills/pretext-reporter-bao'

const canvas = await generateCanvasReport('你好世界 🚀', {
  font: '16px Inter',
  maxWidth: 320,
  lineHeight: 24,
  backgroundColor: '#ffffff',
  textColor: '#000000'
})

// 保存为PNG
const png = canvas.toDataURL('image/png')
```

### 3. 流式布局

```typescript
import { createFlowLayout } from '@claw/skills/pretext-reporter-bao'

const layout = createFlowLayout('你好世界 🚀', {
  font: '16px Inter',
  lineHeight: 24
})

// 逐行布局（可变宽度）
let line
while ((line = layout.nextLine(320)) !== null) {
  console.log(`宽度: ${line.width.toFixed(2)}px, 文本: ${line.text}`)
}
```

### 4. Shrink Wrap

```typescript
import { findTightestWidth } from '@claw/skills/pretext-reporter-bao'

const tightestWidth = findTightestWidth('你好世界 🚀', {
  font: '16px Inter',
  lineHeight: 24,
  maxWidth: 500,
  step: 10
})

console.log(`最窄适配宽度: ${tightestWidth}px`)
```

## API 参考

### measureText(text, options?)

测量文本并返回布局信息。

**参数：**
- `text: string` - 要测量的文本
- `options?: MeasureOptions` - 配置选项
  - `font?: string` - 字体（默认：`'16px Inter'`）
  - `maxWidth?: number` - 最大宽度（默认：`320`）
  - `lineHeight?: number` - 行高（默认：`24`）
  - `whiteSpace?: 'normal' | 'pre-wrap'` - 空白处理（默认：`'normal'`）

**返回：** `Promise<MeasureResult>`

```typescript
interface MeasureResult {
  text: string
  font: string
  characterCount: number
  lineCount: number
  height: number
  maxWidth: number
  lineHeight: number
  lines: LayoutLine[]
}
```

### generateCanvasReport(text, options?)

生成 Canvas 可视化报告。

**参数：**
- `text: string` - 要渲染的文本
- `options?: CanvasOptions` - 配置选项
  - 继承 `MeasureOptions` 的所有选项
  - `backgroundColor?: string` - 背景色（默认：`'#ffffff'`）
  - `textColor?: string` - 文字颜色（默认：`'#000000'`）

**返回：** `Promise<HTMLCanvasElement>`

### generateMarkdownReport(result)

生成 Markdown 格式的报告。

**参数：**
- `result: MeasureResult` - 测量结果

**返回：** `string`

### generateJSONReport(result)

生成 JSON 格式的报告。

**参数：**
- `result: MeasureResult` - 测量结果

**返回：** `object`

### createFlowLayout(text, options?)

创建流式布局器。

**参数：**
- `text: string` - 要布局的文本
- `options?: FlowLayoutOptions` - 配置选项

**返回：** `FlowLayout`

**FlowLayout 方法：**
- `nextLine(maxWidth: number): LayoutLine | null` - 布局下一行
- `reset(): void` - 重置游标

### findTightestWidth(text, options?)

找到最窄的适配宽度（Shrink Wrap）。

**参数：**
- `text: string` - 要测量的文本
- `options?: ShrinkWrapOptions` - 配置选项
  - 继承 `MeasureOptions` 的所有选项
  - `maxWidth?: number` - 搜索上限（默认：`1000`）
  - `step?: number` - 搜索步长（默认：`10`）

**返回：** `number` - 最窄宽度

## 使用场景

### 虚拟列表高度计算

```typescript
import { measureText } from '@claw/skills/pretext-reporter-bao'

// 精确计算每项高度
const items = ['项目1', '项目2', '项目3']

for (const item of items) {
  const { height } = await measureText(item, {
    font: '16px Inter',
    maxWidth: 300,
    lineHeight: 24
  })
  console.log(`${item} 高度: ${height}px`)
}

// 总高度 = sum(heights)
```

### 防止布局偏移

```typescript
// 新文本加载时，预先测量高度
const { height: newTextHeight } = await measureText(newText)

// 更新滚动位置，保持相对位置
scrollPosition = currentScroll + newTextHeight - oldTextHeight
```

### Canvas 文本渲染

```typescript
import { generateCanvasReport } from '@claw/skills/pretext-reporter-bao'

// 渲染到Canvas并导出
const canvas = await generateCanvasReport('你好世界 🚀', {
  font: '24px Inter',
  maxWidth: 640,
  lineHeight: 36
})

// 下载PNG
const link = document.createElement('a')
link.download = 'text-report.png'
link.href = canvas.toDataURL('image/png')
link.click()
```

## 性能基准

基于 500 个文本批次：

| 操作 | 时间 | 说明 |
|------|------|------|
| `prepare()` | ~19ms | 一次性分析 + 测量 |
| `layout()` | ~0.09ms | 热路径，纯算术 |
| `layoutWithLines()` | ~0.12ms | 包含行信息 |

## 依赖

- `@chenglou/pretext@^1.0.0`

## 相关资源

- Pretext GitHub: https://github.com/chenglou/pretext
- Pretext Demo: https://chenglou.me/pretext
- SKILL.md: ./SKILL.md

## 开发

```bash
# 安装依赖
npm install

# 构建TypeScript
npm run build

# 监听模式
npm run dev
```

## 许可证

MIT
