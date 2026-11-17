/* eslint-disable */
/**
 * docx-template.js — paper-report skill 的 Word (.docx) 构建器
 *
 * 双重身份：
 *   1. 库     —— 导出 buildDocx + 一组声明式原语（h2/h3/p/b/i/code/bullet/numbered/highlight/figure/table）。
 *   2. 自检例 —— 文件底部 if (require.main === module) 块直接运行一段通用占位论文示例，
 *                可作为 API 演示与回归测试：`node docx-template.js`。
 *
 * agent 写真实报告时：复制本文件为 `gen_<简短标题>.js`，删掉底部示例块，
 *                    保留 require + 顶层 buildDocx({...}) 调用，填充真实 meta + sections。
 *
 * 详细约定参见同目录 docx.md。
 */

const fs = require('fs');
const path = require('path');

// docx-js 解析顺序：本地 node_modules → 全局 `npm root -g` 目录 → 抛错。
// 保持机器无关：不写死具体全局路径（Homebrew / 系统 npm / nvm 各不相同）。
const DOCX_PATH = (() => {
  // 1) 本地或 NODE_PATH 里能直接解析到 'docx'
  try { require.resolve('docx'); return 'docx'; } catch (_) {}
  // 2) 从 npm 询问全局安装根目录，再拼 'docx'
  try {
    const { execSync } = require('child_process');
    const globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    if (globalRoot) {
      const candidate = path.join(globalRoot, 'docx');
      require.resolve(candidate);
      return candidate;
    }
  } catch (_) {}
  throw new Error('docx-js 未安装。请先运行：npm install -g docx');
})();

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
  WidthType, ShadingType,
} = require(DOCX_PATH);

// ============================================================
// 视觉常量（修改此处即可统一调整所有论文报告的外观）
// ============================================================
// OOXML 的字体属性有四槽：ascii / hAnsi / cs / eastAsia。
// 只写 `font: 'Arial'` 会把四槽全填成 Arial，中文字符是否显示完全依赖
// 渲染器"字体缺失自动回退"这个隐式行为，跨 Word 版本 / 字体包 / 企业
// 字体策略 / Word Online 表现不稳，属于结果不确定的写法。
// 因此每个 TextRun 必须传对象形式，把 eastAsia 单独指向 CJK 字体，
// 并加 `hint: 'eastAsia'` 让渲染器优先按东亚字体渲染混排文本。
const FONT = {
  ascii:    'Arial',
  hAnsi:    'Arial',
  cs:       'Arial',
  eastAsia: 'PingFang SC',   // macOS 默认；缺失时 Word/WPS 会回退 Microsoft YaHei / SimSun
  hint:     'eastAsia',
};
const COLOR_H1     = '1A365D';
const COLOR_H2     = '1A365D';
const COLOR_H3     = '2B6CB0';
const COLOR_MUTED  = '718096';
const COLOR_CAPTION= '718096';
const COLOR_HIGHLIGHT_BG     = 'F7FAFC';
const COLOR_HIGHLIGHT_BAR    = '2B6CB0';
const COLOR_TABLE_BORDER     = 'BFC9D1';
const COLOR_TABLE_HEADER_BG  = 'EDF2F7';

// US Letter, 1 英寸边距 → 正文可用宽 = 12240 - 2*1440 = 9360 DXA
const PAGE_W       = 12240;
const PAGE_H       = 15840;
const MARGIN       = 1440;
const CONTENT_W    = PAGE_W - 2 * MARGIN; // 9360

const SIZE_BODY    = 22; // 半磅 → 11pt
const SIZE_H1      = 36; // 18pt
const SIZE_H2      = 28; // 14pt
const SIZE_H3      = 24; // 12pt
const SIZE_CAPTION = 18; // 9pt
const SIZE_META    = 20; // 10pt
const SIZE_TABLE   = 18; // 9pt

// ============================================================
// 内部辅助：把字符串或 run 对象规范化为 TextRun 数组
// ============================================================
function toRuns(input, baseProps = {}) {
  if (input == null) return [];
  if (Array.isArray(input)) {
    const out = [];
    for (const item of input) out.push(...toRuns(item, baseProps));
    return out;
  }
  if (typeof input === 'string') {
    return [new TextRun({ text: input, font: FONT, size: SIZE_BODY, ...baseProps })];
  }
  // 已是 TextRun 或 { __run: true, props }
  if (input && input.__run) {
    return [new TextRun({ font: FONT, size: SIZE_BODY, ...baseProps, ...input.props })];
  }
  // 已是 TextRun 实例
  return [input];
}

function mkRun(text, props) {
  return { __run: true, props: { text, ...props } };
}

// ============================================================
// 内联标记原语
// ============================================================
function b(text)    { return mkRun(text, { bold: true }); }
function i(text)    { return mkRun(text, { italics: true }); }
function code(text) {
  return mkRun(text, {
    font: 'Menlo',
    size: SIZE_BODY - 2,
    shading: { fill: 'F2F2F2', type: ShadingType.CLEAR, color: 'auto' },
  });
}

// ============================================================
// 段落级原语
// ============================================================
function p(content, opts = {}) {
  return new Paragraph({
    children: toRuns(content),
    spacing: { after: 120, line: 360 },
    alignment: opts.align || AlignmentType.JUSTIFIED,
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 320, after: 160 },
    children: [new TextRun({ text, font: FONT, size: SIZE_H2, bold: true, color: COLOR_H2 })],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, font: FONT, size: SIZE_H3, bold: true, color: COLOR_H3 })],
  });
}

function bullet(content) {
  return new Paragraph({
    numbering: { reference: 'bullets', level: 0 },
    spacing: { after: 80, line: 340 },
    alignment: AlignmentType.JUSTIFIED,
    children: toRuns(content),
  });
}

function numbered(content) {
  return new Paragraph({
    numbering: { reference: 'numbers', level: 0 },
    spacing: { after: 80, line: 340 },
    alignment: AlignmentType.JUSTIFIED,
    children: toRuns(content),
  });
}

// ============================================================
// 高亮卡片：单格表格 + 左侧蓝边 + 浅灰底
// ============================================================
function highlight(children) {
  const cellChildren = (Array.isArray(children) ? children : [children]).map(node =>
    node instanceof Paragraph ? node : p(node)
  );
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CONTENT_W, type: WidthType.DXA },
        shading: { fill: COLOR_HIGHLIGHT_BG, type: ShadingType.CLEAR, color: 'auto' },
        borders: {
          top:    { style: BorderStyle.NONE,   size: 0,  color: 'FFFFFF' },
          bottom: { style: BorderStyle.NONE,   size: 0,  color: 'FFFFFF' },
          right:  { style: BorderStyle.NONE,   size: 0,  color: 'FFFFFF' },
          left:   { style: BorderStyle.SINGLE, size: 24, color: COLOR_HIGHLIGHT_BAR },
        },
        margins: { top: 160, bottom: 160, left: 220, right: 220 },
        children: cellChildren,
      })],
    })],
  });
}

// ============================================================
// 图片：读 PNG IHDR 自动按比例缩放 + 居中 caption
// ============================================================
function readPngSize(buf) {
  // PNG 头：[8B 签名][4B 长度][4B "IHDR"][4B width][4B height]...
  // 即 width 偏移 16，height 偏移 20，big-endian uint32。
  if (buf.length < 24) throw new Error('PNG 文件过短，无法读取 IHDR。');
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

const EXT_TO_TYPE = { png: 'png', jpg: 'jpeg', jpeg: 'jpeg', gif: 'gif', bmp: 'bmp', svg: 'svg' };

function figure(filename, caption, opts = {}) {
  // 惰性标记：实际读盘 + 构造 Paragraph 延迟到 buildDocx 内部，
  // 以避免 sections 数组构造时 figDir 尚未注入。
  return { __figure: true, filename, caption, opts };
}

function _materializeFigure({ filename, caption, opts }, figDir) {
  const widthPx = opts.widthPx || 560;
  const dir = opts.figDir || figDir;
  if (!dir) throw new Error('figure(): 未指定 figDir。请通过 buildDocx({figDir}) 或 figure(_, _, {figDir}) 提供。');
  const fullPath = path.isAbsolute(filename) ? filename : path.join(dir, filename);
  const data = fs.readFileSync(fullPath);
  const ext = filename.split('.').pop().toLowerCase();
  const type = EXT_TO_TYPE[ext];
  if (!type) throw new Error(`figure(): 不支持的扩展名 .${ext}，仅支持 ${Object.keys(EXT_TO_TYPE).join('/')}`);

  let height;
  if (type === 'png') {
    const { width: pw, height: ph } = readPngSize(data);
    height = Math.round(widthPx * (ph / pw));
  } else {
    height = opts.heightPx || Math.round(widthPx * 0.75);
  }

  const imgPara = new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 160, after: 80 },
    children: [new ImageRun({
      type,
      data,
      transformation: { width: widthPx, height },
      altText: { title: filename, description: caption || filename, name: filename },
    })],
  });
  const capPara = new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 240 },
    children: [new TextRun({
      text: caption || '', font: FONT, size: SIZE_CAPTION,
      italics: true, color: COLOR_CAPTION,
    })],
  });
  return [imgPara, capPara];
}

// ============================================================
// 表格
// ============================================================
const TABLE_BORDER = { style: BorderStyle.SINGLE, size: 4, color: COLOR_TABLE_BORDER };
const ALL_BORDERS  = { top: TABLE_BORDER, bottom: TABLE_BORDER, left: TABLE_BORDER, right: TABLE_BORDER };

function tcell(content, { width, isHeader, headerFill, align }) {
  // content 可以是字符串、run、run 数组、或 paragraphs 数组
  let paragraphChildren;
  if (Array.isArray(content) && content[0] instanceof Paragraph) {
    paragraphChildren = content;
  } else {
    const runs = toRuns(content, { size: SIZE_TABLE, bold: !!isHeader });
    paragraphChildren = [new Paragraph({
      alignment: align,
      children: runs,
    })];
  }
  return new TableCell({
    borders: ALL_BORDERS,
    width: { size: width, type: WidthType.DXA },
    shading: isHeader
      ? { fill: headerFill, type: ShadingType.CLEAR, color: 'auto' }
      : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: paragraphChildren,
  });
}

function table({ caption, cols, rows, headerFill = COLOR_TABLE_HEADER_BG }) {
  if (!Array.isArray(cols) || cols.length === 0) {
    throw new Error('table(): cols 必须是非空数组。');
  }
  const sum = cols.reduce((a, b) => a + b, 0);
  if (sum !== CONTENT_W) {
    throw new Error(`table(): cols 之和 ${sum} ≠ ${CONTENT_W}（US Letter 1in 边距下的内容宽度）。`);
  }
  if (!Array.isArray(rows) || rows.length === 0) {
    throw new Error('table(): rows 必须是非空数组。');
  }
  for (const r of rows) {
    if (!Array.isArray(r) || r.length !== cols.length) {
      throw new Error(`table(): 每行长度必须等于 cols.length=${cols.length}，发现 ${r && r.length}。`);
    }
  }

  const result = [];
  if (caption) {
    result.push(new Paragraph({
      spacing: { before: 80, after: 80 },
      children: [new TextRun({
        text: caption, font: FONT, size: SIZE_CAPTION,
        italics: true, color: COLOR_CAPTION,
      })],
    }));
  }
  result.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: cols,
    rows: rows.map((row, ri) => new TableRow({
      tableHeader: ri === 0,
      children: row.map((cellContent, ci) => tcell(cellContent, {
        width: cols[ci],
        isHeader: ri === 0,
        headerFill,
        align: ci === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
      })),
    })),
  }));
  // 表后留一个空段避免下一段贴住表格
  result.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: '', font: FONT, size: SIZE_BODY })] }));
  return result;
}

// ============================================================
// 顶层封装：buildDocx({ meta, figDir, sections, out })
// ============================================================
function buildCoverParagraphs(meta) {
  const out = [];
  out.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    alignment: AlignmentType.CENTER,
    spacing: { before: 240, after: 240 },
    children: [new TextRun({ text: meta.titleCn || '', font: FONT, size: SIZE_H1, bold: true, color: COLOR_H1 })],
  }));
  if (meta.titleEn) {
    out.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 80 },
      children: [new TextRun({ text: meta.titleEn, font: FONT, size: SIZE_BODY, italics: true, color: '4A5568' })],
    }));
  }
  for (const line of [meta.authors, meta.org, meta.source].filter(Boolean)) {
    out.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: line, font: FONT, size: SIZE_META, color: COLOR_MUTED })],
    }));
  }
  // 封面与正文之间的空隙
  out.push(new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: '', font: FONT, size: SIZE_BODY })] }));
  return out;
}

function flat(arr, figDir) {
  // 浅展开一层数组；同时把 figure 惰性标记实化为真正的 [Paragraph, Paragraph]
  const out = [];
  for (const x of arr) {
    if (x && typeof x === 'object' && x.__figure) {
      for (const y of _materializeFigure(x, figDir)) out.push(y);
    } else if (Array.isArray(x)) {
      for (const y of flat(x, figDir)) out.push(y);
    } else {
      out.push(x);
    }
  }
  return out;
}

async function buildDocx({ meta, figDir, sections, out }) {
  const body = [];
  body.push(...buildCoverParagraphs(meta || {}));

  for (const sec of sections || []) {
    if (sec.h2)   body.push(h2(sec.h2));
    if (sec.body) body.push(...flat(sec.body, figDir));
  }

  const doc = new Document({
    creator: 'paper-report skill',
    title: (meta && meta.titleCn) || 'Paper Report',
    styles: {
      default: { document: { run: { font: FONT, size: SIZE_BODY } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: SIZE_H1, bold: true, font: FONT, color: COLOR_H1 },
          paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: SIZE_H2, bold: true, font: FONT, color: COLOR_H2 },
          paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 1 } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: SIZE_H3, bold: true, font: FONT, color: COLOR_H3 },
          paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 } },
      ],
    },
    numbering: {
      config: [
        { reference: 'bullets',
          levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
        { reference: 'numbers',
          levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      children: body,
    }],
  });

  const buf = await Packer.toBuffer(doc);
  if (out) {
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, buf);
  }
  return { buffer: buf, bytes: buf.length, out };
}

// ============================================================
// 公共导出
// ============================================================
module.exports = {
  buildDocx,
  h2, h3, p, b, i, code,
  bullet, numbered,
  highlight, figure, table,
  // 常量也导出，便于自定义扩展
  CONTENT_W, PAGE_W, PAGE_H, MARGIN,
};

// ============================================================
// 自检示例：node docx-template.js
// 生成一份通用占位论文报告，演示全部原语用法。
// agent 写真实报告时复制本文件，删除以下整块。
// ============================================================
if (require.main === module) {
  (async () => {
    const OUT_DIR = path.join(__dirname, '_example_out');
    fs.mkdirSync(OUT_DIR, { recursive: true });

    // 生成一张 1×1 的占位 PNG，证明 figure() 的链路能跑通
    // 真实使用时 figDir 指向 {workspace}/figures。
    const PLACEHOLDER_PNG = Buffer.from(
      '89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4' +
      '890000000A49444154789C636000000000050001A5F645400000000049454E44' +
      'AE426082', 'hex');
    fs.writeFileSync(path.join(OUT_DIR, 'placeholder.png'), PLACEHOLDER_PNG);

    await buildDocx({
      meta: {
        titleCn: '示例论文标题：方法 X 在任务 Y 上的研究',
        titleEn: 'Example Paper: Method X for Task Y',
        authors: '作者甲 · 作者乙 · 作者丙',
        org:     '示例研究机构',
        source:  'arXiv:0000.00000 · 示例年份',
      },
      figDir: OUT_DIR,
      sections: [
        { h2: '一、研究背景与动机', body: [
            p(['任务 Y 在领域内长期面临 ', b('两类核心挑战'), '：(i) 表征瓶颈；(ii) 评测脱节。']),
            p([
              '先前工作多采用方案 ', code('A'), ' 与 ', code('B'),
              '，但二者均依赖额外标注。本文提出方法 ', b('X'), '，',
              i('无需额外标注'), ' 即可同时缓解上述两点。',
            ]),
            highlight([
              p([b('核心结论：'), '方法 X 在通用基准上相对最强基线提升 N%，且推理成本不增加。']),
            ]),
        ]},

        { h2: '二、方法概览', body: [
            figure('placeholder.png', '图 1：方法 X 总体架构示意（原文 Figure 1）。'),
            h3('2.1 模块 A'),
            p('模块 A 的设计目标是 …（此处填写原文相关描述）。'),
            h3('2.2 模块 B'),
            p('模块 B 在模块 A 输出之上施加 …（此处填写原文相关描述）。'),
        ]},

        { h2: '三、实验设计', body: [
            p('实验在三个公开基准上展开，并对照若干代表性基线。主要超参数见表 1。'),
            table({
              caption: '表 1：主要超参数对照（示例占位数据）。',
              cols: [3120, 3120, 3120],
              rows: [
                ['超参',     '取值',        '说明'],
                ['学习率',   '5e-4',        '余弦退火，warmup 1k 步'],
                ['批大小',   b('1024'),     '梯度累积 4 步'],
                ['训练轮数', '50',          '早停于验证集 loss 不下降 3 epoch'],
              ],
            }),
        ]},

        { h2: '四、主要结果', body: [
            p('在三个基准上的主结果如表 2。最佳值已加粗。'),
            table({
              caption: '表 2：主基准结果（示例占位数据）。',
              cols: [2520, 2280, 2280, 2280],
              rows: [
                ['方法',     'Bench-A', 'Bench-B', 'Bench-C'],
                ['基线 P',   '30.1',    '52.4',    '41.7'],
                ['基线 Q',   '32.6',    '54.8',    '44.0'],
                [b('方法 X'), b('35.2'), b('57.1'), b('46.9')],
              ],
            }),
            p('结果显示方法 X 在全部三个基准上均显著优于基线。'),
        ]},

        { h2: '五、主要贡献与创新点', body: [
            bullet([b('1. 表征层面：'), '提出模块 A，缓解了任务 Y 中长期存在的表征瓶颈。']),
            bullet([b('2. 训练层面：'), '通过模块 B 的辅助目标，整体训练成本与基线持平。']),
            bullet([b('3. 评测层面：'), '在三个通用基准上验证有效性，且无需额外标注。']),
        ]},

        { h2: '六、局限性与未来方向', body: [
            numbered('仅在英文场景验证，跨语言泛化尚待评估。'),
            numbered('未对极小模型规模进行系统性消融。'),
            numbered('实际部署延迟、显存等工程指标未在原文报告。'),
        ]},

        { h2: '七、个人点评与总结', body: [
            p('（此处填写读者的批判性思考，注意保持基于原文事实，不臆造数据。）'),
        ]},
      ],
      out: path.join(OUT_DIR, 'report_Example.docx'),
    });

    console.log('Example written:', path.join(OUT_DIR, 'report_Example.docx'));
  })().catch(err => {
    console.error(err);
    process.exit(1);
  });
}
