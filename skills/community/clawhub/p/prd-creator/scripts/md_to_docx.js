#!/usr/bin/env node
/**
 * PRD Markdown to Word Converter
 * 将 Markdown 格式的 PRD 转换为专业排版的 .docx 文档
 *
 * 用法:
 *   node md_to_docx.js input.md [output.docx]
 *
 * 依赖: npm install docx
 */

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageBreak, LevelFormat,
  TabStopType, TabStopPosition, UnderlineType, PageNumber
} = require('docx');

// ═══════════════════════════════════════════════════════════════════════════════
//  1. 配色系统（与 docx-builder 保持一致）
// ═══════════════════════════════════════════════════════════════════════════════
const C = {
  brand:      '1E40AF',
  brandLight: 'DBEAFE',
  accent:     '0F766E',
  warn:       'B45309',
  danger:     'B91C1C',
  ok:         '15803D',
  gray1:      'F8FAFC',
  gray2:      'E2E8F0',
  gray3:      '94A3B8',
  border:     'CBD5E1',
  text:       '1E293B',
};

// ═══════════════════════════════════════════════════════════════════════════════
//  2. 基础样式
// ═══════════════════════════════════════════════════════════════════════════════
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: C.border };
const allBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const cellPad = { top: 90, bottom: 90, left: 140, right: 140 };

// ═══════════════════════════════════════════════════════════════════════════════
//  3. 辅助函数
// ═══════════════════════════════════════════════════════════════════════════════
const T  = (text, opts = {}) => new TextRun({ text, font: 'Arial', color: C.text, size: 22, ...opts });
const TB = (text, opts = {}) => T(text, { bold: true, ...opts });
const TG = (text, opts = {}) => T(text, { color: C.gray3, size: 18, ...opts });
const TC = (text, color, opts = {}) => T(text, { color, ...opts });

const P = (children, opts = {}) => new Paragraph({
  children: Array.isArray(children) ? children : [children],
  spacing: { after: 100, line: 276 },
  ...opts,
});

const PH1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 400, after: 200 },
  children: [T(text, { bold: true, size: 36 })],
});

const PH2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 300, after: 160 },
  children: [T(text, { bold: true, size: 28, color: C.accent })],
});

const PH3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 200, after: 120 },
  children: [T(text, { bold: true, size: 24 })],
});

const PH4 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_4,
  spacing: { before: 160, after: 100 },
  children: [T(text, { bold: true, size: 22 })],
});

const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const hdrCell = (text, width, span = 1) => new TableCell({
  borders: allBorders,
  width: { size: width, type: WidthType.DXA },
  columnSpan: span,
  shading: { fill: C.gray2, type: ShadingType.CLEAR },
  margins: cellPad,
  verticalAlign: VerticalAlign.CENTER,
  children: [new Paragraph({ children: [TB(text, { size: 18 })], spacing: { after: 0 } })],
});

const dataCell = (content, width, fill = null, opts = {}) => {
  let children;
  if (typeof content === 'string') {
    children = [new Paragraph({ children: inlineToRuns(content, { size: 18 }), spacing: { after: 0 } })];
  } else if (Array.isArray(content)) {
    children = content;
  } else {
    children = [content];
  }
  return new TableCell({
    borders: allBorders,
    width: { size: width, type: WidthType.DXA },
    shading: fill ? { fill, type: ShadingType.CLEAR } : undefined,
    margins: cellPad,
    verticalAlign: VerticalAlign.CENTER,
    children,
    ...opts,
  });
};

const altFill = (i) => (i % 2 === 0 ? C.gray1 : null);

// ═══════════════════════════════════════════════════════════════════════════════
//  4. 行内 Markdown 解析（bold, italic, code, strikethrough）
// ═══════════════════════════════════════════════════════════════════════════════
function inlineToRuns(text, baseOpts = {}) {
  const runs = [];
  let remaining = text;
  const patterns = [
    { regex: /\*\*\*(.+?)\*\*\*/g,          opts: { bold: true, italics: true } },
    { regex: /\*\*(.+?)\*\*/g,              opts: { bold: true } },
    { regex: /\*(.+?)\*/g,                  opts: { italics: true } },
    { regex: /`(.+?)`/g,                    opts: { font: 'Courier New', color: C.danger } },
    { regex: /~~(.+?)~~/g,                  opts: { strike: true } },
    { regex: /\[(.+?)\]\((.+?)\)/g,         opts: { underline: { type: UnderlineType.SINGLE }, color: C.brand }, transform: (m) => m[1] },
  ];

  while (remaining.length > 0) {
    let earliest = null;
    let earliestIdx = Infinity;

    for (const pat of patterns) {
      pat.regex.lastIndex = 0;
      const m = pat.regex.exec(remaining);
      if (m && m.index < earliestIdx) {
        earliest = { match: m, opts: pat.opts, transform: pat.transform || ((m) => m[1]) };
        earliestIdx = m.index;
      }
    }

    if (earliest && earliestIdx < Infinity) {
      if (earliestIdx > 0) {
        runs.push(T(remaining.slice(0, earliestIdx), baseOpts));
      }
      const content = earliest.transform(earliest.match);
      runs.push(T(content, { ...baseOpts, ...earliest.opts }));
      remaining = remaining.slice(earliestIdx + earliest.match[0].length);
    } else {
      runs.push(T(remaining, baseOpts));
      break;
    }
  }

  return runs.length > 0 ? runs : [T(text, baseOpts)];
}

// ═══════════════════════════════════════════════════════════════════════════════
//  5. Markdown 解析器
// ═══════════════════════════════════════════════════════════════════════════════
class MarkdownParser {
  constructor(text) {
    this.lines = text.split('\n');
    this.pos = 0;
    this.children = [];
  }

  peek() {
    return this.pos < this.lines.length ? this.lines[this.pos] : null;
  }

  advance() {
    return this.lines[this.pos++];
  }

  parse() {
    while (this.pos < this.lines.length) {
      const line = this.peek();
      if (line === null) break;

      const trimmed = line.trim();
      if (trimmed === '') {
        this.advance();
        continue;
      }

      if (this.parseYamlBlock()) continue;
      if (this.parseTable()) continue;
      if (this.parseHeading()) continue;
      if (this.parseCodeBlock()) continue;
      if (this.parseBlockquote()) continue;
      if (this.parseHorizontalRule()) continue;
      if (this.parseBulletList()) continue;
      if (this.parseNumberedList()) continue;
      if (this.parseParagraph()) continue;

      this.advance();
    }
    return this.children;
  }

  // YAML frontmatter ```yaml ... ```
  parseYamlBlock() {
    const line = this.peek();
    if (line.trim().startsWith('```yaml') || line.trim() === '---') {
      this.advance();
      while (this.peek() !== null) {
        const l = this.peek();
        if (l.trim() === '```' || l.trim() === '---') {
          this.advance();
          break;
        }
        this.advance();
      }
      return true;
    }
    return false;
  }

  // 标题 # ## ### #### #####
  parseHeading() {
    const line = this.peek();
    const m = line.match(/^(#{1,6})\s+(.+)$/);
    if (!m) return false;

    const level = m[1].length;
    const text = m[2].trim();
    this.advance();

    if (level === 1) this.children.push(PH1(text));
    else if (level === 2) this.children.push(PH2(text));
    else if (level === 3) this.children.push(PH3(text));
    else this.children.push(PH4(text));

    return true;
  }

  // 表格
  parseTable() {
    const line = this.peek();
    if (!line.trim().startsWith('|')) return false;

    const rows = [];
    while (this.peek() !== null && this.peek().trim().startsWith('|')) {
      rows.push(this.advance());
    }

    if (rows.length < 2) {
      // 不是表格，回退并当作段落处理
      for (const r of rows) this.children.push(P(inlineToRuns(r)));
      return true;
    }

    // 跳过第二行的分隔符
    const headerRow = rows[0];
    const dataRows = rows.slice(2);

    const headers = this.splitCells(headerRow);
    const numCols = headers.length;
    if (numCols === 0) return true;

    const colWidth = Math.floor(9360 / numCols);

    const tableRows = [
      new TableRow({
        children: headers.map(h => hdrCell(h.trim(), colWidth)),
      }),
    ];

    dataRows.forEach((row, i) => {
      const cells = this.splitCells(row);
      // 补齐或截断单元格
      while (cells.length < numCols) cells.push('');
      const trimmed = cells.slice(0, numCols);
      tableRows.push(new TableRow({
        children: trimmed.map(c => dataCell(c.trim(), colWidth, altFill(i))),
      }));
    });

    this.children.push(new Table({
      width: { size: 9360, type: WidthType.DXA },
      columnWidths: Array(numCols).fill(colWidth),
      rows: tableRows,
    }));

    // 表格后空一行
    this.children.push(new Paragraph({ spacing: { after: 100 }, children: [] }));

    return true;
  }

  splitCells(row) {
    // 处理 | a | b | c | 格式
    const trimmed = row.trim();
    if (!trimmed.startsWith('|')) return [];
    let content = trimmed;
    if (content.endsWith('|')) content = content.slice(0, -1);
    if (content.startsWith('|')) content = content.slice(1);
    return content.split('|').map(c => c.trim());
  }

  // 代码块 ```...```
  parseCodeBlock() {
    const line = this.peek();
    if (!line.trim().startsWith('```')) return false;

    const lang = line.trim().slice(3).trim();
    this.advance();
    const lines = [];
    while (this.peek() !== null) {
      const l = this.peek();
      if (l.trim() === '```') {
        this.advance();
        break;
      }
      lines.push(this.advance());
    }

    const code = lines.join('\n');
    this.children.push(new Paragraph({
      shading: { fill: C.gray1, type: ShadingType.CLEAR },
      spacing: { before: 100, after: 100 },
      indent: { left: 200 },
      children: [T(code, { font: 'Courier New', size: 18, color: C.text })],
    }));

    return true;
  }

  // 引用块 > ...
  parseBlockquote() {
    const line = this.peek();
    if (!line.trim().startsWith('>')) return false;

    const lines = [];
    while (this.peek() !== null && this.peek().trim().startsWith('>')) {
      const l = this.advance();
      lines.push(l.replace(/^>\s?/, ''));
    }

    const text = lines.join(' ').trim();
    this.children.push(new Paragraph({
      spacing: { before: 100, after: 100 },
      indent: { left: 400 },
      border: {
        left: { style: BorderStyle.SINGLE, size: 12, color: C.brand, space: 8 },
      },
      children: inlineToRuns(text),
    }));

    return true;
  }

  // 水平分隔线 --- / *** / ___
  parseHorizontalRule() {
    const line = this.peek();
    if (/^(---+|\*\*\*+|___+)\s*$/.test(line.trim())) {
      this.advance();
      this.children.push(new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C.border, space: 4 } },
        spacing: { before: 200, after: 200 },
        children: [],
      }));
      return true;
    }
    return false;
  }

  // 无序列表 - / * / +
  parseBulletList() {
    const line = this.peek();
    const m = line.match(/^(\s*)[-*+]\s+(.+)$/);
    if (!m) return false;

    const items = [];
    while (this.peek() !== null) {
      const l = this.peek();
      const bm = l.match(/^(\s*)[-*+]\s+(.+)$/);
      if (!bm) break;
      const indent = bm[1].length;
      const text = bm[2];
      this.advance();

      // 收集多行内容（缩进的下一行）
      const contentLines = [text];
      while (this.peek() !== null) {
        const next = this.peek();
        if (next.trim() === '') { contentLines.push(''); this.advance(); continue; }
        if (next.match(/^(\s*)[-*+]\s+/)) break;
        if (next.match(/^(\s*)\d+\.\s+/)) break;
        const leading = next.match(/^(\s*)/)[1].length;
        if (leading > indent) {
          contentLines.push(next.trim());
          this.advance();
        } else {
          break;
        }
      }

      items.push({ level: Math.floor(indent / 2), text: contentLines.join(' ') });
    }

    items.forEach(item => {
      this.children.push(new Paragraph({
        numbering: { reference: 'bullets', level: Math.min(item.level, 1) },
        spacing: { after: 60 },
        children: inlineToRuns(item.text),
      }));
    });

    return true;
  }

  // 有序列表 1. / 2. / ...
  parseNumberedList() {
    const line = this.peek();
    const m = line.match(/^(\s*)\d+\.\s+(.+)$/);
    if (!m) return false;

    const items = [];
    while (this.peek() !== null) {
      const l = this.peek();
      const nm = l.match(/^(\s*)\d+\.\s+(.+)$/);
      if (!nm) break;
      const indent = nm[1].length;
      const text = nm[2];
      this.advance();

      const contentLines = [text];
      while (this.peek() !== null) {
        const next = this.peek();
        if (next.trim() === '') { contentLines.push(''); this.advance(); continue; }
        if (next.match(/^(\s*)(?:\d+\.\s+|[-*+]\s+)/)) break;
        const leading = next.match(/^(\s*)/)[1].length;
        if (leading > indent) {
          contentLines.push(next.trim());
          this.advance();
        } else {
          break;
        }
      }

      items.push({ text: contentLines.join(' ') });
    }

    items.forEach(item => {
      this.children.push(new Paragraph({
        numbering: { reference: 'numbers', level: 0 },
        spacing: { after: 60 },
        children: inlineToRuns(item.text),
      }));
    });

    return true;
  }

  // 普通段落
  parseParagraph() {
    const lines = [];
    while (this.peek() !== null) {
      const l = this.peek();
      if (l.trim() === '') break;
      // 如果下一行是某种块级元素，停止
      if (l.match(/^(#{1,6}\s|\s*[-*+]\s+|\s*\d+\.\s+|\s*\||\s*>\s*|\s*```|(\s*)[-*]{3,}\s*$)/)) break;
      lines.push(this.advance());
    }

    if (lines.length === 0) {
      this.advance(); // skip empty
      return true;
    }

    const text = lines.join(' ').trim();
    this.children.push(P(inlineToRuns(text)));
    return true;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
//  6. 文档构建
// ═══════════════════════════════════════════════════════════════════════════════
async function convertMarkdownToDocx(inputPath, outputPath) {
  if (!fs.existsSync(inputPath)) {
    console.error(`❌ 文件不存在: ${inputPath}`);
    process.exit(1);
  }

  const text = fs.readFileSync(inputPath, 'utf-8');
  const parser = new MarkdownParser(text);
  const children = parser.parse();

  // 提取标题用于页眉
  let title = '产品需求文档';
  const titleMatch = text.match(/^#\s+(.+)$/m);
  if (titleMatch) title = titleMatch[1].trim();

  const doc = new Document({
    numbering: {
      config: [
        {
          reference: 'bullets',
          levels: [
            { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } },
            { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1120, hanging: 280 } } } },
          ],
        },
        {
          reference: 'numbers',
          levels: [
            { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } },
          ],
        },
      ],
    },
    styles: {
      default: {
        document: {
          run: { font: 'Arial', size: 22, color: C.text },
        },
      },
      paragraphStyles: [
        {
          id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 36, bold: true, font: 'Arial', color: C.brand },
          paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0,
            border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: C.brand, space: 1 } } },
        },
        {
          id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 28, bold: true, font: 'Arial', color: C.accent },
          paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 1 },
        },
        {
          id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 24, bold: true, font: 'Arial', color: C.text },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
        },
        {
          id: 'Heading4', name: 'Heading 4', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 22, bold: true, font: 'Arial', color: C.text },
          paragraph: { spacing: { before: 160, after: 100 }, outlineLevel: 3 },
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C.brand, space: 4 } },
            children: [TB(title.slice(0, 40), { size: 18, color: C.brand })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { top: { style: BorderStyle.SINGLE, size: 2, color: C.brand, space: 4 } },
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            children: [
              T('PRD Document', { size: 18, color: C.gray3 }),
              new TextRun({ text: '\t', size: 18 }),
              new TextRun({ children: [PageNumber.CURRENT], size: 18, color: C.gray3 }),
              T(' / ', { size: 18, color: C.gray3 }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: C.gray3 }),
            ],
          })],
        }),
      },
      children,
    }],
  });

  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buf);
  console.log(`✅ Word 文档已生成: ${outputPath}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
//  7. 主函数
// ═══════════════════════════════════════════════════════════════════════════════
async function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log('用法: node md_to_docx.js <输入.md> [输出.docx]');
    console.log('示例: node md_to_docx.js PRD-01_用户管理_v1.0.md PRD-01_用户管理_v1.0.docx');
    process.exit(0);
  }

  const inputPath = path.resolve(args[0]);
  const outputPath = args[1]
    ? path.resolve(args[1])
    : inputPath.replace(/\.md$/i, '.docx');

  await convertMarkdownToDocx(inputPath, outputPath);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
