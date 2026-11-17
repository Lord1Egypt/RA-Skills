/**
 * IT 集成公司企业解决方案文档创建脚本
 * 创建符合企业级专业规范的 .docx 文件
 *
 * 基于国央企Word文档规范，适配企业级 IT 集成方案的专业排版需求
 *
 * 使用方法:
 *   node scripts/create_it_solution.js <output_filename.docx> [content_json]
 *
 * 示例:
 *   node scripts/create_it_solution.js solution.docx '{"cover": {...}, "chapters": [...]}'
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, ImageRun, UnderlineType,
  TableOfContents, SectionType, Bookmark, PageReference, TabStopType, SimpleField,
} = require('docx');
const fs = require('fs');

// ========== 格式常量定义 ==========
const CHINESE_FONTS = {
  FZXiaoBiaoSong: 'FZXiaoBiaoSong-B05S',  // 方正小标宋简体
  FZFangSong: 'FZFangSong-Z02S',          // 方正仿宋简体
  HeiTi: '黑体',
  KaiTi: '楷体',
  SongTi: '宋体',
  TimesNewRoman: 'Times New Roman'
};

// ========== 辅助函数 ==========

/**
 * 从 Paragraph 内部属性树中提取样式名称
 * docx 库的 Paragraph 没有 .style 属性，样式存储在 properties.root 内部
 */
function getParagraphStyle(para) {
  try {
    if (para && para.properties && Array.isArray(para.properties.root)) {
      const pStyle = para.properties.root.find(node => node.rootKey === 'w:pStyle');
      if (pStyle && Array.isArray(pStyle.root) && pStyle.root[0] && pStyle.root[0].root && pStyle.root[0].root.val) {
        return pStyle.root[0].root.val.value || '';
      }
    }
  } catch (e) {
    // ignore
  }
  return '';
}

/**
 * 将文本中的 ASCII 双引号 " 替换为配对的中文双引号
 */
function normalizeQuotes(text) {
  const LEFT = '\u201c';
  const RIGHT = '\u201d';
  let result = '';
  let quoteCount = 0;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '"' || ch === '\u201d' || ch === '\u201c') {
      result += (quoteCount % 2 === 0) ? LEFT : RIGHT;
      quoteCount++;
    } else {
      result += ch;
    }
  }
  return result;
}

function isLatinChar(char) {
  const code = char.charCodeAt(0);
  if ((code >= 32 && code <= 126) || (code >= 160 && code <= 255)) return true;
  if ('ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏàáâãäåæçèéêëìíîïòóôõöøùúûüÿ'.indexOf(char) !== -1) return true;
  return false;
}

function splitByScript(text) {
  const segments = [];
  let currentText = '';
  let currentIsLatin = null;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    const isLatin = isLatinChar(char);
    if (char === '\n') {
      if (currentText) { segments.push({ text: currentText, isLatin: currentIsLatin }); currentText = ''; currentIsLatin = null; }
      segments.push({ text: '\n', isLatin: false });
      continue;
    }
    if (currentIsLatin === null) { currentIsLatin = isLatin; currentText = char; }
    else if (currentIsLatin === isLatin) { currentText += char; }
    else { segments.push({ text: currentText, isLatin: currentIsLatin }); currentText = char; currentIsLatin = isLatin; }
  }
  if (currentText) segments.push({ text: currentText, isLatin: currentIsLatin });
  return segments;
}

function createTextRunsFromSegments(text, chineseFont, latinFont, fontSize, options = {}) {
  const { bold = false, italic = false } = options;
  const normalizedText = normalizeQuotes(text);
  const segments = splitByScript(normalizedText);
  const runs = [];
  for (const seg of segments) {
    if (seg.text === '\n') continue;
    if (seg.isLatin) {
      runs.push(new TextRun({
        text: seg.text,
        font: { ascii: latinFont, hAnsi: latinFont, cs: latinFont },
        bold, italic,
      }));
    } else {
      runs.push(new TextRun({
        text: seg.text,
        font: { eastAsia: chineseFont, ascii: latinFont, hAnsi: latinFont, cs: latinFont },
        bold, italic,
      }));
    }
  }
  return runs;
}

// ========== 字号转换 ==========
const FONT_SIZES = {
  '小初号': 72,   // 36pt
  '小一号': 48,   // 24pt
  '小二号': 36,   // 18pt
  '小三号': 30,   // 15pt
  '四号': 28,     // 14pt
  '五号': 21,     // 10.5pt
  '小五号': 18,   // 9pt
};

// 行间距
const LINE_SPACING_EXACT_28 = { line: 560, lineRule: "exact" };
const LINE_SPACING_EXACT_36 = { line: 720, lineRule: "exact" };
const LINE_SPACING_SINGLE = { line: 276, lineRule: "auto" };

// 字符宽度 (小三号字体, 1字符 = 15pt = 300 twips)
const CHAR_WIDTH = FONT_SIZES['小三号'] * 10;

// 页边距
const COVER_MARGINS = {
  top: Math.round(3.7 / 2.54 * 1440),
  bottom: Math.round(3.5 / 2.54 * 1440),
  left: Math.round(2.8 / 2.54 * 1440),
  right: Math.round(2.6 / 2.54 * 1440)
};

const BODY_MARGINS = {
  top: Math.round(2.54 / 2.54 * 1440),
  bottom: Math.round(2.54 / 2.54 * 1440),
  left: Math.round(3.17 / 2.54 * 1440),
  right: Math.round(3.17 / 2.54 * 1440)
};

const A4_WIDTH = 11906;
const A4_HEIGHT = 16838;
const CONTENT_WIDTH = A4_WIDTH - BODY_MARGINS.left - BODY_MARGINS.right;

// ========== 样式定义 ==========

function createCoverCompanyStyle() {
  return {
    id: "封面公司名称",
    name: "封面公司名称",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZXiaoBiaoSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小一号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 720, lineRule: "exact" },
    }
  };
}

function createCoverProjectStyle() {
  return {
    id: "封面项目名称",
    name: "封面项目名称",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZXiaoBiaoSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小一号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 720, lineRule: "exact" },
    }
  };
}

function createCoverDocTypeStyle() {
  return {
    id: "封面文档类型",
    name: "封面文档类型",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.HeiTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小二号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 720, lineRule: "exact" },
    }
  };
}

function createCoverInfoStyle() {
  return {
    id: "封面信息",
    name: "封面信息",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 720, lineRule: "exact" },
    }
  };
}

function createBodyStyle() {
  return {
    id: "正文",
    name: "正文",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * CHAR_WIDTH },
    }
  };
}

function createLevel1HeadingStyle() {
  return {
    id: "一级标题",
    name: "一级标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.HeiTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 120, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * CHAR_WIDTH },
      outlineLevel: 0,
    }
  };
}

function createLevel2HeadingStyle() {
  return {
    id: "二级标题",
    name: "二级标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.KaiTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 80, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * CHAR_WIDTH },
      outlineLevel: 1,
    }
  };
}

function createLevel3HeadingStyle() {
  return {
    id: "三级标题",
    name: "三级标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
      bold: true,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 40, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * CHAR_WIDTH },
      outlineLevel: 2,
    }
  };
}

function createLevel4HeadingStyle() {
  return {
    id: "四级标题",
    name: "四级标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 40, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * CHAR_WIDTH },
      outlineLevel: 3,
    }
  };
}

function createImageStyle() {
  return {
    id: "图片",
    name: "图片",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    }
  };
}

function createTableBodyStyle() {
  return {
    id: "表格正文",
    name: "表格正文",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小五号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    }
  };
}

function createTableHeaderStyle() {
  return {
    id: "表格表头",
    name: "表格表头",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.HeiTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小五号'],
      bold: true,
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    }
  };
}

function createSignatureStyle() {
  return {
    id: "落款",
    name: "落款",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.RIGHT,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 0 },
    }
  };
}

function createCaptionStyle() {
  return {
    id: "题注",
    name: "题注",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['五号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 40, after: 120, line: 276, lineRule: "auto" },
    }
  };
}

function createPageNumberStyle() {
  return {
    id: "页码",
    name: "页码",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: CHINESE_FONTS.SongTi,
      size: FONT_SIZES['五号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0 }
    }
  };
}

function createTOCTitleStyle() {
  return {
    id: "目录标题",
    name: "目录标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.HeiTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 200, line: 560, lineRule: "exact" },
    }
  };
}

function createTOCEntryStyle() {
  return {
    id: "目录条目",
    name: "目录条目",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 0 },
    }
  };
}

// TOC 自动生成条目样式（行距固定28磅，首行不缩进）
function createTOC1Style() {
  return {
    id: "TOC1",
    name: "TOC 1",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: { font: { eastAsia: CHINESE_FONTS.HeiTi, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman }, size: FONT_SIZES['小三号'] },
    paragraph: { spacing: { before: 60, after: 0, line: 560, lineRule: "exact" }, indent: { firstLine: 0 },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH, leader: 'dot' }] },
  };
}

function createTOC2Style() {
  return {
    id: "TOC2",
    name: "TOC 2",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: { font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman }, size: FONT_SIZES['小三号'] },
    paragraph: { spacing: { before: 0, after: 0, line: 560, lineRule: "exact" }, indent: { firstLine: 2 * CHAR_WIDTH },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH, leader: 'dot' }] },
  };
}

function createTOC3Style() {
  return {
    id: "TOC3",
    name: "TOC 3",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: { font: { eastAsia: CHINESE_FONTS.FZFangSong, ascii: CHINESE_FONTS.TimesNewRoman, hAnsi: CHINESE_FONTS.TimesNewRoman, cs: CHINESE_FONTS.TimesNewRoman }, size: FONT_SIZES['小三号'] },
    paragraph: { spacing: { before: 0, after: 0, line: 560, lineRule: "exact" }, indent: { firstLine: 2 * CHAR_WIDTH },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH, leader: 'dot' }] },
  };
}

// ========== 文档创建函数 ==========

/**
 * 创建解决方案文档实例
 */
function createSolutionDocument(options = {}) {
  const { title = '', sections = [], hasCover = false, hasTOC = false, signature = null } = options;

  // 组织 sections：封面 section + 目录 section + 正文 sections
  const docSections = [];

  if (hasCover || hasTOC) {
    // 找出封面相关的 sections
    const coverSections = [];
    const tocSections = [];
    const bodySections = [];
    let afterCover = false;
    let afterTOC = false;

    for (const s of sections) {
      const style = getParagraphStyle(s);
      if (style.includes('封面') && !afterCover && !afterTOC) {
        coverSections.push(s);
      } else if ((style.includes('目录') || s._isTOC || s._isTOCSection) && !afterTOC) {
        tocSections.push(s);
        afterCover = true;
      } else {
        afterCover = true;
        afterTOC = true;
        bodySections.push(s);
      }
    }

    // 落款（如有）：自动追加到正文末尾，避免漏调用导致丢失
    if (signature && signature.company) {
      bodySections.push(...createSignatureBlock(signature.company, signature.date || ''));
    }

    // 封面 section
    if (hasCover && coverSections.length > 0) {
      docSections.push({
        properties: {
          page: { size: { width: A4_WIDTH, height: A4_HEIGHT }, margin: COVER_MARGINS },
          titlePage: true,
        },
        children: coverSections,
      });
    }

    // 目录 section — 独立分页
    if (hasTOC && tocSections.length > 0) {
      docSections.push({
        properties: {
          page: { size: { width: A4_WIDTH, height: A4_HEIGHT }, margin: BODY_MARGINS },
          type: SectionType.NEXT_PAGE,
        },
        children: tocSections,
      });
    } else if (hasTOC && !hasCover && tocSections.length > 0) {
      docSections.push({
        properties: {
          page: { size: { width: A4_WIDTH, height: A4_HEIGHT }, margin: BODY_MARGINS },
          type: SectionType.NEXT_PAGE,
        },
        children: tocSections,
      });
    }

    // 正文 sections — 独立分页
    docSections.push({
      properties: {
        page: {
          size: { width: A4_WIDTH, height: A4_HEIGHT },
          margin: BODY_MARGINS,
          pageNumbers: { start: 1 },
        },
        type: SectionType.NEXT_PAGE,
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              style: "页码",
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "第 ", font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ children: [PageNumber.CURRENT], font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ text: " 页 / 共 ", font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES_IN_SECTION], font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ text: " 页", font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
              ]
            })
          ]
        })
      },
      children: bodySections,
    });
  } else {
    // 无封面无目录，单 section
    docSections.push({
      properties: {
        page: { size: { width: A4_WIDTH, height: A4_HEIGHT }, margin: BODY_MARGINS },
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              style: "页码",
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "第 ", font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ children: [PageNumber.CURRENT], font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ text: " 页 / 共 ", font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES_IN_SECTION], font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
                new TextRun({ text: " 页", font: { eastAsia: CHINESE_FONTS.SongTi, ascii: CHINESE_FONTS.SongTi, hAnsi: CHINESE_FONTS.SongTi, cs: CHINESE_FONTS.SongTi }, size: FONT_SIZES['五号'] }),
              ]
            })
          ]
        })
      },
      children: sections,
    });
  }

  const doc = new Document({
    title: title,
    description: '',
    styles: {
      default: {
        document: {
          run: {
            font: {
              eastAsia: CHINESE_FONTS.FZFangSong,
              ascii: CHINESE_FONTS.TimesNewRoman,
              hAnsi: CHINESE_FONTS.TimesNewRoman,
              cs: CHINESE_FONTS.TimesNewRoman,
            },
            size: FONT_SIZES['小三号'],
          },
          paragraph: {
            spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
          }
        }
      },
      paragraphStyles: [
        createCoverCompanyStyle(),
        createCoverProjectStyle(),
        createCoverDocTypeStyle(),
        createCoverInfoStyle(),
        createTOCTitleStyle(),
        createTOCEntryStyle(),
        createTOC1Style(),
        createTOC2Style(),
        createTOC3Style(),
        createBodyStyle(),
        createLevel1HeadingStyle(),
        createLevel2HeadingStyle(),
        createLevel3HeadingStyle(),
        createLevel4HeadingStyle(),
        createImageStyle(),
        createTableBodyStyle(),
        createTableHeaderStyle(),
        createSignatureStyle(),
        createCaptionStyle(),
        createPageNumberStyle(),
      ]
    },
    sections: docSections,
  });

  return doc;
}

// ========== 封面创建函数 ==========

/**
 * 创建封面页
 * @param {Object} options
 * @param {string} options.companyName - 公司名称
 * @param {string} options.projectName - 项目名称
 * @param {string} options.docType - 文档类型（如"技术解决方案"）
 * @param {string} options.date - 日期
 * @param {string} options.version - 版本号
 * @param {string} options.confidentiality - 保密等级
 * @param {string} options.compilationUnit - 编制单位（默认同 companyName）
 */
function createCoverPage(options = {}) {
  const {
    companyName = '',
    projectName = '',
    docType = '技术解决方案',
    date = '',
    version = 'V1.0',
    confidentiality = '内部资料',
    compilationUnit = '',
  } = options;

  const unit = compilationUnit || companyName;
  const paragraphs = [];

  // 顶部留白
  for (let i = 0; i < 3; i++) {
    paragraphs.push(new Paragraph({ style: "封面信息", children: [new TextRun({ text: "" })] }));
  }

  // 公司名称
  if (companyName) {
    paragraphs.push(new Paragraph({
      style: "封面公司名称",
      children: [new TextRun({ text: normalizeQuotes(companyName) })]
    }));
  }

  // 项目名称（与公司名称之间不空行）
  if (projectName) {
    paragraphs.push(new Paragraph({
      style: "封面项目名称",
      children: [new TextRun({ text: normalizeQuotes(projectName) })]
    }));
  }

  // 中间留白：用空行填充，把底部信息推到接近页面底部（数量已收紧，避免溢出第二页）
  for (let i = 0; i < 6; i++) {
    paragraphs.push(new Paragraph({ style: "封面信息", children: [new TextRun({ text: "" })] }));
  }

  // 底部信息（编制单位、日期、版本，置于页面底部；不含保密等级与文档类型）
  const infoLines = [];
  if (unit) infoLines.push(`编制单位：${unit}`);
  if (date) infoLines.push(`编制日期：${date}`);
  if (version) infoLines.push(`文档版本：${version}`);

  for (const line of infoLines) {
    paragraphs.push(new Paragraph({
      style: "封面信息",
      children: [new TextRun({ text: normalizeQuotes(line) })]
    }));
  }

  return paragraphs;
}

// ========== 目录创建函数 ==========

/**
 * 创建目录页（预置 TOC 复杂域）
 * TOC1/TOC2/TOC3 样式已定义在文档中，TOC 域更新后自动使用这些样式
 */
function createTableOfContents() {
  const paragraphs = [];

  const tocTitle = new Paragraph({
    style: "目录标题",
    children: [new TextRun({ text: "目  录" })]
  });
  tocTitle._isTOC = true;
  paragraphs.push(tocTitle);

  // 预置 TOC 域（复杂域，Word 右键更新域即可生成目录）
  const tocField = new TableOfContents("目录", {
    hyperlink: false,
    headingStyleRange: "1-3",
  });
  tocField._isTOC = true;
  paragraphs.push(tocField);

  return paragraphs;
}

// ========== Docx 后处理 ==========

/**
 * 后处理：移除 TOC 的 w:sdt 包装和 w:dirty，使 Word 能正常打开无警告
 */
function removeTOCSDT(docxBuffer) {
  const JSZip = require('jszip');
  return JSZip.loadAsync(docxBuffer).then(async (zip) => {
    const file = zip.file('word/document.xml');
    let xml = await file.async('text');

    // 1. 移除所有 w:dirty="true"
    xml = xml.replace(/ w:dirty="true"/g, '');

    // 2. 移除 TOC 的 <w:sdt> 包装，保留内部 <w:sdtContent> 的内容
    xml = xml.replace(
      /<w:sdt>\s*<w:sdtPr>[\s\S]*?<\/w:sdtPr>\s*<w:sdtContent>/g,
      ''
    );
    xml = xml.replace(/<\/w:sdtContent>\s*<\/w:sdt>/g, '');

    zip.file('word/document.xml', xml);

    return zip.generateAsync({
      type: 'nodebuffer',
      compression: 'DEFLATE',
      compressionOptions: { level: 9 },
    });
  });
}

// ========== 标题创建函数 ==========

const CHAPTER_NUMBERS = [
  '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
  '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十'
];

/**
 * 创建一级标题（章标题），可选添加书签
 * 格式：第一章 项目概述
 * @param {string} text - 标题文字（不含"第X章"前缀）
 * @param {number} number - 章节序号 (0-based)
 * @param {string} bookmarkId - 可选，书签 ID（用于目录页码引用）
 */
function createChapterHeading(text, number, bookmarkId) {
  const chapterNum = (number !== undefined) ? CHAPTER_NUMBERS[number] || String(number + 1) : '';
  const prefix = chapterNum ? `第${chapterNum}章 ` : '';
  const fullText = prefix + text;

  const textRuns = createTextRunsFromSegments(
    fullText, CHINESE_FONTS.HeiTi, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
  );

  return new Paragraph({
    style: "一级标题",
    children: bookmarkId
      ? [new Bookmark({ id: bookmarkId, children: textRuns })]
      : textRuns
  });
}

/**
 * 创建二级标题（节标题），可选添加书签
 * 格式：1.1 项目背景
 * @param {string} text - 标题文字（不含"X.X"前缀）
 * @param {number} chapterNumber - 所属章序号 (0-based)
 * @param {number} sectionNumber - 节序号 (0-based)
 * @param {string} bookmarkId - 可选，书签 ID
 */
function createSectionHeading(text, chapterNumber, sectionNumber, bookmarkId) {
  const prefix = (chapterNumber !== undefined && sectionNumber !== undefined)
    ? `${chapterNumber + 1}.${sectionNumber + 1} `
    : '';
  const fullText = prefix + text;

  const textRuns = createTextRunsFromSegments(
    fullText, CHINESE_FONTS.KaiTi, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
  );

  return new Paragraph({
    style: "二级标题",
    children: bookmarkId
      ? [new Bookmark({ id: bookmarkId, children: textRuns })]
      : textRuns
  });
}

/**
 * 创建三级标题（条标题），可选添加书签
 * 格式：1.1.1 建设背景
 * @param {string} text - 标题文字
 * @param {number} chapterNumber - 所属章序号 (0-based)
 * @param {number} sectionNumber - 所属节序号 (0-based)
 * @param {number} subNumber - 条序号 (0-based)
 * @param {string} bookmarkId - 可选，书签 ID
 */
function createSubsectionHeading(text, chapterNumber, sectionNumber, subNumber, bookmarkId) {
  const prefix = (chapterNumber !== undefined && sectionNumber !== undefined && subNumber !== undefined)
    ? `${chapterNumber + 1}.${sectionNumber + 1}.${subNumber + 1} `
    : '';
  const fullText = prefix + text;

  const textRuns = createTextRunsFromSegments(
    fullText, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号'], { bold: true }
  );

  return new Paragraph({
    style: "三级标题",
    children: bookmarkId
      ? [new Bookmark({ id: bookmarkId, children: textRuns })]
      : textRuns
  });
}

/**
 * 创建四级标题（款标题）
 * 格式：（1）网络现状
 * @param {string} text - 标题文字
 * @param {number} number - 序号 (0-based)
 */
function createLevel4Heading(text, number) {
  const prefix = (number !== undefined) ? `（${number + 1}）` : '';
  const fullText = prefix + text;

  return new Paragraph({
    style: "四级标题",
    children: createTextRunsFromSegments(
      fullText, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
    )
  });
}

// ========== 正文创建函数 ==========

/**
 * 创建正文段落
 */
function createBodyParagraph(text, options = {}) {
  const { bold = false, italic = false } = options;
  if (!text) {
    return new Paragraph({
      style: "正文",
      children: [new TextRun({ text: "" })]
    });
  }
  return new Paragraph({
    style: "正文",
    children: createTextRunsFromSegments(
      text, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号'], { bold, italic }
    )
  });
}

/**
 * 创建项目符号列表
 * @param {string[]} items - 列表项
 */
function createBulletList(items) {
  return items.map(item => new Paragraph({
    style: "正文",
    children: createTextRunsFromSegments(
      `● ${item}`, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
    )
  }));
}

/**
 * 创建编号列表
 * @param {string[]} items - 列表项
 */
function createNumberedList(items) {
  return items.map((item, idx) => new Paragraph({
    style: "正文",
    children: createTextRunsFromSegments(
      `${idx + 1}. ${item}`, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
    )
  }));
}

// ========== 表格创建函数 ==========

/**
 * 创建解决方案表格
 * rows: [{ children: ['cell1', 'cell2', ...] }]
 * 第一行自动作为表头（灰色底、黑体加粗）
 */
function createSolutionTable(rows, options = {}) {
  const { columnWidths = [], hasHeader = true } = options;

  if (!rows || rows.length === 0) {
    return new Paragraph({ children: [] });
  }

  const widths = columnWidths.length > 0
    ? columnWidths
    : Array(rows[0]?.children?.length || 0).fill(Math.floor(CONTENT_WIDTH / (rows[0]?.children?.length || 1)));

  const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
  const borders = { top: border, bottom: border, left: border, right: border };

  const tableRows = rows.map((row, rowIdx) => {
    const isHeader = hasHeader && rowIdx === 0;
    const cells = row.children || row;

    return new TableRow({
      tableHeader: isHeader,
      children: cells.map((cell, colIdx) => {
        const cellText = typeof cell === 'string' ? cell : (cell.text || String(cell));
        const normalizedText = normalizeQuotes(cellText);

        if (isHeader) {
          return new TableCell({
            borders,
            width: { size: widths[colIdx] || Math.floor(CONTENT_WIDTH / cells.length), type: WidthType.DXA },
            shading: { fill: "D9D9D9", type: ShadingType.CLEAR },
            margins: { top: 50, bottom: 50, left: 100, right: 100 },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              style: "表格表头",
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: normalizedText, bold: true })]
            })]
          });
        }

        return new TableCell({
          borders,
          width: { size: widths[colIdx] || Math.floor(CONTENT_WIDTH / cells.length), type: WidthType.DXA },
          shading: { fill: "FFFFFF", type: ShadingType.CLEAR },
          margins: { top: 50, bottom: 50, left: 100, right: 100 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            style: "表格正文",
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: normalizedText })]
          })]
        });
      })
    });
  });

  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: widths,
    rows: tableRows,
  });
}

// ========== 图片创建函数 ==========

/**
 * 创建图片段落（可带图注）
 * @param {Buffer} imageData - 图片数据
 * @param {number} width - 图片宽度
 * @param {number} height - 图片高度
 * @param {Object} options
 * @param {string} options.caption - 图注文字
 * @param {number} options.figureIndex - 独立图片序号（如 1, 2, 3...）
 */
function createImageWithCaption(imageData, width, height, options = {}) {
  const { caption, figureIndex, transformation = {} } = options;
  const actualWidth = transformation.width || width;
  const actualHeight = transformation.height || height;

  const paragraphs = [];

  // 图片
  paragraphs.push(new Paragraph({
    style: "图片",
    spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    children: [
      new ImageRun({
        type: 'png',
        data: imageData,
        transformation: { width: actualWidth, height: actualHeight },
        altText: { title: options.altText || '', description: options.description || '', name: options.name || '' }
      })
    ]
  }));

  // 图注
  if (caption) {
    const figLabel = (figureIndex !== undefined)
      ? `图${figureIndex} `
      : '';
    paragraphs.push(new Paragraph({
      style: "题注",
      children: createTextRunsFromSegments(
        `${figLabel}${caption}`,
        CHINESE_FONTS.SongTi, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['五号']
      )
    }));
  }

  return paragraphs;
}

// ========== 落款创建函数 ==========

/**
 * 创建落款块
 * @param {string} company - 公司名称
 * @param {string} date - 日期
 */
function createSignatureBlock(company, date) {
  const paragraphs = [];

  // 与正文间隔两行
  paragraphs.push(new Paragraph({ style: "落款", children: [new TextRun({ text: "" })] }));
  paragraphs.push(new Paragraph({ style: "落款", children: [new TextRun({ text: "" })] }));

  // 公司名称
  paragraphs.push(new Paragraph({
    style: "落款",
    children: createTextRunsFromSegments(
      company, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
    )
  }));

  // 日期
  paragraphs.push(new Paragraph({
    style: "落款",
    children: createTextRunsFromSegments(
      date, CHINESE_FONTS.FZFangSong, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['小三号']
    )
  }));

  return paragraphs;
}

// ========== 便捷函数：一键创建完整解决方案 ==========

/**
 * 创建完整 IT 解决方案文档（便捷函数）
 * @param {Object} content - 文档内容
 * @param {Object} content.cover - 封面信息
 * @param {Array} content.chapters - 章节数组
 * @param {Object} content.signature - 落款信息
 * @param {string} outputPath - 输出文件路径
 */
async function createItSolution(content, outputPath) {
  const { cover, chapters = [], signature } = content;

  // 独立序号计数器（图片和表格各自独立编号）
  let figureCounter = 0;
  let tableCounter = 0;

  const allSections = [];

  // 封面
  if (cover) {
    const coverSections = createCoverPage(cover);
    allSections.push(...coverSections);
  }

  // 目录（占位页，用户在 Word 中手动插入目录）
  if (cover) {
    const tocSections = createTableOfContents();
    allSections.push(...tocSections);
  }

  // 正文章节
  for (let chIdx = 0; chIdx < chapters.length; chIdx++) {
    const chapter = chapters[chIdx];

    // 章标题（带书签用于目录页码）
    allSections.push(createChapterHeading(chapter.heading, chIdx));

    // 节内容
    if (chapter.sections) {
      for (let secIdx = 0; secIdx < chapter.sections.length; secIdx++) {
        const section = chapter.sections[secIdx];

        // 节标题（带书签）
        if (section.heading) {
          allSections.push(createSectionHeading(section.heading, chIdx, secIdx));
        }

        // 正文段落
        if (section.body) {
          for (const para of section.body) {
            allSections.push(createBodyParagraph(para));
          }
        }

        // 项目符号列表
        if (section.bulletList) {
          allSections.push(...createBulletList(section.bulletList));
        }

        // 编号列表
        if (section.numberedList) {
          allSections.push(...createNumberedList(section.numberedList));
        }

        // 表格
        if (section.tables) {
          for (const tableData of section.tables) {
            allSections.push(createSolutionTable(tableData.rows, tableData.options || {}));
            if (tableData.caption) {
              tableCounter++;
              const capPara = new Paragraph({
                style: "题注",
                children: createTextRunsFromSegments(
                  `表${tableCounter} ${tableData.caption}`,
                  CHINESE_FONTS.SongTi, CHINESE_FONTS.TimesNewRoman, FONT_SIZES['五号']
                )
              });
              allSections.push(capPara);
            }
          }
        }

        // 子节（三级标题）
        if (section.subsections) {
          for (let subIdx = 0; subIdx < section.subsections.length; subIdx++) {
            const sub = section.subsections[subIdx];
            if (sub.heading) {
              allSections.push(createSubsectionHeading(sub.heading, chIdx, secIdx, subIdx));
            }
            if (sub.body) {
              for (const para of sub.body) {
                allSections.push(createBodyParagraph(para));
              }
            }
            if (sub.bulletList) {
              allSections.push(...createBulletList(sub.bulletList));
            }
          }
        }
      }
    }
  }

  // 落款（如有）：自动追加到文档末尾
  if (signature && signature.company) {
    allSections.push(...createSignatureBlock(signature.company, signature.date || ''));
  }

  // 创建文档
  const doc = createSolutionDocument({
    title: cover?.projectName || '',
    sections: allSections,
    hasCover: !!cover,
    hasTOC: !!cover,
  });

  const buffer = await Packer.toBuffer(doc);

  // 后处理：移除 TOC 的 SDT 包装（保留 dirty 使 Word 可更新域）
  const cleaned = await removeTOCSDT(buffer);

  fs.writeFileSync(outputPath, cleaned);
  console.log(`文档已保存: ${outputPath}`);
  return outputPath;
}

// ========== 导出 ==========
module.exports = {
  // 字体常量
  CHINESE_FONTS,
  FONT_SIZES,
  LINE_SPACING_EXACT_28,
  LINE_SPACING_EXACT_36,
  LINE_SPACING_SINGLE,
  COVER_MARGINS,
  BODY_MARGINS,
  CONTENT_WIDTH,

  // 文档创建
  createSolutionDocument,
  createItSolution,
  createCoverPage,
  createTableOfContents,
  createChapterHeading,
  createSectionHeading,
  createSubsectionHeading,
  createLevel4Heading,
  createBodyParagraph,
  createBulletList,
  createNumberedList,
  createSolutionTable,
  createImageWithCaption,
  createSignatureBlock,

  // 工具函数
  normalizeQuotes,
  createTextRunsFromSegments,

  // docx 对象
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, ImageRun, TableOfContents,
  SectionType, Bookmark, PageReference, TabStopType,
};
