/**
 * Pretext Reporter Bao
 * 基于 Pretext 库的文本测量和布局工具
 */

// 使用本地 Pretext
import {
  prepare,
  layout,
  prepareWithSegments,
  layoutWithLines,
  layoutNextLine,
  measureNaturalWidth,
  type LayoutLine,
  type LayoutCursor,
  type LayoutResult,
  type LayoutLinesResult
} from '../pretext/dist/layout.js'

/**
 * 文本测量结果
 */
export interface MeasureResult {
  text: string
  font: string
  characterCount: number
  lineCount: number
  height: number
  maxWidth: number
  lineHeight: number
  width: number
  lines: LayoutLine[]
}

/**
 * 流式布局器
 */
export class FlowLayout {
  private prepared: any
  private cursor: LayoutCursor
  private font: string
  private lineHeight: number

  constructor(text: string, font: string, lineHeight: number) {
    this.prepared = prepareWithSegments(text, font)
    this.cursor = { segmentIndex: 0, graphemeIndex: 0 }
    this.font = font
    this.lineHeight = lineHeight
  }

  /**
   * 布局下一行
   */
  nextLine(maxWidth: number): LayoutLine | null {
    const line = layoutNextLine(this.prepared, this.cursor, maxWidth)
    if (line === null) {
      return null
    }
    this.cursor = line.end
    return line
  }

  /**
   * 重置游标
   */
  reset(): void {
    this.cursor = { segmentIndex: 0, graphemeIndex: 0 }
  }
}

/**
 * 文本测量选项
 */
export interface MeasureOptions {
  font?: string
  maxWidth?: number
  lineHeight?: number
  whiteSpace?: 'normal' | 'pre-wrap'
}

/**
 * Canvas 选项
 */
export interface CanvasOptions extends MeasureOptions {
  backgroundColor?: string
  textColor?: string
  padding?: number
}

/**
 * Shrink Wrap 选项
 */
export interface ShrinkWrapOptions extends MeasureOptions {
  maxWidth?: number
  step?: number
}

/**
 * 测量文本并返回布局信息
 */
export async function measureText(text: string, options: MeasureOptions = {}): Promise<MeasureResult> {
  const {
    font = '16px Inter',
    maxWidth = 320,
    lineHeight = 24
  } = options

  const prepared = prepareWithSegments(text, font)
  const result: LayoutLinesResult = layoutWithLines(prepared, maxWidth, lineHeight)
  const naturalWidth = measureNaturalWidth(prepared)

  return {
    text,
    font,
    characterCount: text.length,
    lineCount: result.lineCount,
    height: result.height,
    maxWidth,
    lineHeight,
    width: Math.min(naturalWidth, maxWidth),
    lines: result.lines
  }
}

/**
 * 生成 Canvas 可视化报告
 */
export async function generateCanvasReport(text: string, options: CanvasOptions = {}): Promise<any> {
  const {
    font = '16px Inter',
    maxWidth = 320,
    lineHeight = 24,
    backgroundColor = '#ffffff',
    textColor = '#000000',
    padding = 20
  } = options

  const prepared = prepareWithSegments(text, font)
  const layoutResult = layoutWithLines(prepared, maxWidth, lineHeight)
  const naturalWidth = measureNaturalWidth(prepared)

  // 创建 Canvas（需要在浏览器环境中）
  // 这里返回配置对象，实际使用时需要传入 Canvas
  return {
    config: {
      text,
      font,
      maxWidth,
      lineHeight,
      backgroundColor,
      textColor,
      padding
    },
    layout: layoutResult,
    width: Math.max(maxWidth + padding * 2, Math.min(naturalWidth, maxWidth) + padding * 2),
    height: layoutResult.height + padding * 2
  }
}

/**
 * 生成 Markdown 格式的报告
 */
export function generateMarkdownReport(result: MeasureResult): string {
  const linesInfo = result.lines.map((line, i) =>
    `行 ${i + 1}: "${line.text}" (宽度: ${line.width.toFixed(2)}px)`
  ).join('\n')

  return `
# 文本测量报告

## 基本信息
- **文本**: \`${result.text}\`
- **字体**: ${result.font}
- **字符数**: ${result.characterCount}
- **行数**: ${result.lineCount}
- **实际宽度**: ${result.width.toFixed(2)}px
- **高度**: ${result.height}px
- **行高**: ${result.lineHeight}px
- **最大宽度**: ${result.maxWidth}px

## 布局信息
${linesInfo}
`
}

/**
 * 生成 JSON 格式的报告
 */
export function generateJSONReport(result: MeasureResult): object {
  return {
    metadata: {
      timestamp: new Date().toISOString(),
      version: '1.0.0'
    },
    measurement: result
  }
}

/**
 * 创建流式布局器
 */
export function createFlowLayout(text: string, options: MeasureOptions = {}): FlowLayout {
  const { font = '16px Inter', lineHeight = 24 } = options
  return new FlowLayout(text, font, lineHeight)
}

/**
 * 找到最窄的适配宽度（Shrink Wrap）
 */
export function findTightestWidth(text: string, options: ShrinkWrapOptions = {}): number {
  const {
    font = '16px Inter',
    lineHeight = 24,
    maxWidth = 1000,
    step = 10
  } = options

  const prepared = prepare(text, font)

  // 二分查找最窄宽度
  let low = 0
  let high = maxWidth

  while (high - low > step) {
    const mid = Math.floor((low + high) / 2)
    const result = layout(prepared, mid, lineHeight)

    // 如果行数增加，说明宽度不够
    if (result.lineCount > 1) {
      low = mid
    } else {
      high = mid
    }
  }

  return high
}
