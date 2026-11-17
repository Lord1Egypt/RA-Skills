"use strict";
/**
 * 简单表格格式化器（备用）
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TableFormatter = void 0;
class TableFormatter {
    /**
     * 生成 Markdown 表格
     */
    static create(headers, rows) {
        const lines = [];
        // 表头
        lines.push(`| ${headers.join(' | ')} |`);
        lines.push(`|${headers.map(() => '---').join('|')}|`);
        // 行
        for (const row of rows) {
            lines.push(`| ${row.join(' | ')} |`);
        }
        return lines.join('\n');
    }
    /**
     * 对齐文本
     */
    static pad(str, width, align = 'left') {
        const len = this.displayWidth(str);
        if (len >= width)
            return str;
        const padSize = width - len;
        switch (align) {
            case 'left':
                return str + ' '.repeat(padSize);
            case 'right':
                return ' '.repeat(padSize) + str;
            case 'center':
                const left = Math.floor(padSize / 2);
                const right = padSize - left;
                return ' '.repeat(left) + str + ' '.repeat(right);
            default:
                return str;
        }
    }
    /**
     * 计算显示宽度（简化版）
     */
    static displayWidth(str) {
        return str.length;
    }
}
exports.TableFormatter = TableFormatter;
//# sourceMappingURL=TableFormatter.js.map