/**
 * generate_report.js
 * 学术论文精读报告 Word 文档生成器
 *
 * 用法：
 *   node generate_report.js --data <json_file_path>
 *
 * JSON 格式（推荐）：
 * {
 *   "title": "论文主标题",
 *   "subtitle": "副标题",
 *   "author": "作者",
 *   "school": "学校/机构",
 *   "date": "日期",
 *   "quickOverview": "5分钟导读内容（可用 \\n 分隔多段）",
 *   "moments": [
 *     { "icon": "💡", "title": "灵感时刻标题", "content": "具体内容（可用 \\n 分隔多段）" },
 *     ...
 *   ],
 *   "dimensions": [
 *     { "heading": "维度一：xxx", "content": "内容（可用 \\n 分隔多段）" },
 *     ...
 *   ],
 *   "summary": "总结内容",
 *   "filename": "输出文件名（不含扩展名）"
 * }
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, LevelFormat
} = require('docx');
const fs = require('fs');
const path = require('path');

// ==================== 常量 ====================
const BRAND_BLUE  = '2E75B6';
const DARK_BLUE   = '1F4E79';
const GRAY        = '555555';
const LIGHT_GRAY  = '888888';
const BORDER_CLR  = 'CCCCCC';
const ACCENT_BG   = 'E8F4FD';  // 灵感时刻背景色
const MOMENT_ICON_BG = 'FFF3CD'; // 灵感图标背景

// ==================== 工具函数 ====================

const borders = (color = BORDER_CLR) => ({
  top:    { style: BorderStyle.SINGLE, size: 1, color },
  bottom: { style: BorderStyle.SINGLE, size: 1, color },
  left:   { style: BorderStyle.SINGLE, size: 1, color },
  right:  { style: BorderStyle.SINGLE, size: 1, color },
});

function blank(before = 0, after = 0) {
  return new Paragraph({ spacing: { before, after }, children: [new TextRun({ text: '' })] });
}

function sectionTitle(text) {
  return new Paragraph({
    spacing: { before: 400, after: 160 },
    children: [new TextRun({ text, font: 'Arial', size: 36, bold: true, color: DARK_BLUE })]
  });
}

function sectionDivider() {
  return new Paragraph({
    spacing: { before: 0, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BRAND_BLUE, space: 4 } },
    children: [new TextRun({ text: '' })]
  });
}

function h3(text) {
  return new Paragraph({
    spacing: { before: 320, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BRAND_BLUE, space: 4 } },
    children: [new TextRun({ text, font: 'Arial', size: 26, bold: true, color: DARK_BLUE })]
  });
}

function h4(text) {
  return new Paragraph({
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, font: 'Arial', size: 24, bold: true, color: BRAND_BLUE })]
  });
}

// 通用文本块渲染（支持加粗、引用、编号）
function splitLines(text) {
  if (!text) return [new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun({ text: '' })] })];
  return text.split('\n').filter(l => l.trim()).map(line => {
    const trimmed = line.trim();
    const m = trimmed.match(/^\*\*(.+?)\*\*(.*)$/);
    if (m) {
      return new Paragraph({
        spacing: { before: 100, after: 60 },
        children: [
          new TextRun({ text: m[1], font: 'Arial', size: 22, bold: true }),
          ...(m[2] ? [new TextRun({ text: m[2], font: 'Arial', size: 22 })] : [])
        ]
      });
    }
    if (trimmed.startsWith('>')) {
      return new Paragraph({
        spacing: { before: 60, after: 60 },
        indent: { left: 360 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: BRAND_BLUE, space: 8 } },
        children: [new TextRun({ text: trimmed.slice(1).trim(), font: 'Arial', size: 21, color: GRAY, italics: true })]
      });
    }
    if (/^\d+\./.test(trimmed)) {
      return new Paragraph({
        numbering: { reference: 'numbers', level: 0 },
        spacing: { before: 60, after: 60 },
        children: [new TextRun({ text: trimmed, font: 'Arial', size: 22 })]
      });
    }
    return new Paragraph({
      spacing: { before: 60, after: 60 },
      children: [new TextRun({ text: trimmed, font: 'Arial', size: 22 })]
    });
  });
}

// 两列信息表
function infoTable(rows, colWidths = [2600, 6800]) {
  const total = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: rows.map(([k, v], i) =>
      new TableRow({
        children: [
          new TableCell({
            borders: borders(),
            width: { size: colWidths[0], type: WidthType.DXA },
            shading: { fill: i % 2 === 0 ? 'EBF3FB' : 'FFFFFF', type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({ children: [new TextRun({ text: k, font: 'Arial', size: 20, bold: true, color: DARK_BLUE })] })]
          }),
          new TableCell({
            borders: borders(),
            width: { size: colWidths[1], type: WidthType.DXA },
            shading: { fill: i % 2 === 0 ? 'F5F9FD' : 'FFFFFF', type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({ children: [new TextRun({ text: v || '-', font: 'Arial', size: 20 })] })]
          })
        ]
      })
    )
  });
}

// 构建灵感时刻单块
function buildMomentBlock(moment, index) {
  const blocks = [];
  const num = String(index + 1).padStart(2, '0');

  // 时刻编号 + 标题行（带背景色）
  blocks.push(
    new Paragraph({
      spacing: { before: 240, after: 80 },
      shading: { fill: MOMENT_ICON_BG, type: ShadingType.CLEAR },
      children: [
        new TextRun({ text: `${moment.icon || '💡'} 灵感时刻 ${num}`, font: 'Arial', size: 24, bold: true, color: 'B45309' }),
        ...(moment.title ? [new TextRun({ text: `  ${moment.title}`, font: 'Arial', size: 24, bold: true, color: DARK_BLUE })] : [])
      ]
    })
  );

  // 内容（带浅色左边框背景）
  const contentLines = (moment.content || '').split('\n').filter(l => l.trim());
  contentLines.forEach(line => {
    const trimmed = line.trim();
    if (trimmed.startsWith('>')) {
      blocks.push(new Paragraph({
        spacing: { before: 60, after: 60 },
        indent: { left: 360 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: 'F59E0B', space: 8 } },
        children: [new TextRun({ text: trimmed.slice(1).trim(), font: 'Arial', size: 21, color: GRAY, italics: true })]
      }));
    } else {
      blocks.push(new Paragraph({
        spacing: { before: 60, after: 60 },
        indent: { left: 240 },
        children: [new TextRun({ text: trimmed, font: 'Arial', size: 22 })]
      }));
    }
  });

  blocks.push(blank(0, 80));
  return blocks;
}

// 构建维度内容块
function buildDimContent(dim) {
  const blocks = [];
  const lines = (dim.content || '').split('\n').filter(l => l.trim());

  for (const line of lines) {
    const t = line.trim();
    if (/^\d+\.\d+\s/.test(t)) { blocks.push(h4(t)); continue; }
    if (t.startsWith('>')) {
      blocks.push(new Paragraph({
        spacing: { before: 60, after: 60 },
        indent: { left: 360 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: BRAND_BLUE, space: 8 } },
        children: [new TextRun({ text: t.slice(1).trim(), font: 'Arial', size: 21, color: GRAY, italics: true })]
      }));
      continue;
    }
    const m = t.match(/^\*\*(.+?)\*\*(.*)$/);
    if (m) {
      blocks.push(new Paragraph({
        spacing: { before: 100, after: 60 },
        children: [
          new TextRun({ text: m[1], font: 'Arial', size: 22, bold: true }),
          ...(m[2] ? [new TextRun({ text: m[2], font: 'Arial', size: 22 })] : [])
        ]
      }));
      continue;
    }
    if (/^\d+\./.test(t)) {
      blocks.push(new Paragraph({
        numbering: { reference: 'numbers', level: 0 },
        spacing: { before: 60, after: 60 },
        children: [new TextRun({ text: t, font: 'Arial', size: 22 })]
      }));
      continue;
    }
    blocks.push(new Paragraph({
      spacing: { before: 60, after: 60 },
      children: [new TextRun({ text: t, font: 'Arial', size: 22 })]
    }));
  }
  return blocks;
}

// 维度编号映射
const DIM_LABELS = ['一', '二', '三', '四', '五', '六'];

// ==================== 核心函数 ====================

function generateDocument(data) {
  const {
    title       = '未知论文',
    subtitle    = '精读报告',
    author      = '',
    school      = '',
    date        = '',
    quickOverview = '',
    moments     = [],
    dimensions  = [],
    summary     = ''
  } = data;

  const children = [

    // ===== 封面 =====
    blank(600, 0),

    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 200 },
      children: [new TextRun({ text: title, font: 'Arial', size: 52, bold: true, color: DARK_BLUE })]
    }),

    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 400 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BRAND_BLUE, space: 6 } },
      children: [new TextRun({ text: subtitle, font: 'Arial', size: 36, color: BRAND_BLUE })]
    }),

    blank(0, 300),
    infoTable([
      ['论文标题', title],
      ['作者', author],
      ['学校/机构', school],
      ['日期', date]
    ]),
    blank(0, 400),

    // ===== 一、研究灵感时刻（前置·核心）=====
    sectionTitle('一、研究灵感时刻'),
    sectionDivider(),
    blank(0, 60),

    ...(moments.length > 0
      ? moments.flatMap((m, i) => buildMomentBlock(m, i))
      : [
          new Paragraph({
            spacing: { before: 120, after: 120 },
            children: [new TextRun({ text: '（精读分析完成后，这里将展示从论文中提炼的研究灵感时刻）', font: 'Arial', size: 22, color: LIGHT_GRAY, italics: true })]
          }),
          blank(0, 100)
        ]
    ),

    // ===== 二、快速一览 =====
    sectionTitle('二、快速一览（5分钟导读）'),
    sectionDivider(),
    blank(0, 100),
    ...splitLines(quickOverview),
    blank(0, 100),

    // ===== 三、六大维度深度解读 =====
    sectionTitle('三、六大维度深度解读'),
    sectionDivider(),
    blank(0, 100),

    ...dimensions.flatMap((dim, i) => {
      if (!dim || !dim.content) return [];
      const label = DIM_LABELS[i] || DIM_LABELS[DIM_LABELS.length - 1];
      const heading = dim.heading.replace(new RegExp(`^维度\\d：`), '');
      return [h3(`维度${label}：${heading}`), ...buildDimContent(dim), blank(0, 100)];
    }),

    // ===== 四、总结 =====
    sectionTitle('四、总结'),
    sectionDivider(),
    blank(0, 100),
    ...splitLines(summary),
    blank(0, 200),

    // 脚注
    new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: `报告生成时间：${date}`, font: 'Arial', size: 20, color: LIGHT_GRAY })]
    }),
    new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: '由 paper-reader Skill 自动生成', font: 'Arial', size: 20, color: LIGHT_GRAY })]
    }),
  ];

  return new Document({
    numbering: {
      config: [
        { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] },
        { reference: 'numbers', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] }
      ]
    },
    styles: { default: { document: { run: { font: 'Arial', size: 22 } } } },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, right: 1134, bottom: 1440, left: 1134 }
        }
      },
      children
    }]
  });
}

// 获取桌面路径
function getDesktopPath() {
  const home = process.env.HOME || process.env.USERPROFILE || '';
  return path.join(home, 'Desktop');
}

// ==================== 主入口 ====================

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || !args.includes('--data')) {
    console.error('用法: node generate_report.js --data <json_file>');
    process.exit(1);
  }

  const idx = args.indexOf('--data');
  const jsonPath = args[idx + 1];
  if (!jsonPath) { console.error('Error: --data requires a file path'); process.exit(1); }

  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  const outputPath = data.filename
    ? path.join(getDesktopPath(), `${data.filename}.docx`)
    : path.join(getDesktopPath(), '精读报告.docx');

  const doc = generateDocument(data);
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log('Word document created: ' + outputPath);
}

main().catch(err => { console.error(err); process.exit(1); });
