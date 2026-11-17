/**
 * 简单表格格式化器（备用）
 */

export class TableFormatter {
  /**
   * 生成 Markdown 表格
   */
  static create(headers: string[], rows: string[][]): string {
    const lines: string[] = []

    // 表头
    lines.push(`| ${headers.join(' | ')} |`)
    lines.push(`|${headers.map(() => '---').join('|')}|`)

    // 行
    for (const row of rows) {
      lines.push(`| ${row.join(' | ')} |`)
    }

    return lines.join('\n')
  }

  /**
   * 对齐文本
   */
  static pad(str: string, width: number, align: 'left' | 'center' | 'right' = 'left'): string {
    const len = this.displayWidth(str)
    if (len >= width) return str

    const padSize = width - len
    switch (align) {
      case 'left':
        return str + ' '.repeat(padSize)
      case 'right':
        return ' '.repeat(padSize) + str
      case 'center':
        const left = Math.floor(padSize / 2)
        const right = padSize - left
        return ' '.repeat(left) + str + ' '.repeat(right)
      default:
        return str
    }
  }

  /**
   * 计算显示宽度（简化版）
   */
  private static displayWidth(str: string): number {
    return str.length
  }
}