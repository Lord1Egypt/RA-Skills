/**
 * 国央企Word文档创建脚本
 * 创建符合中国政府公文规范的.docx文件
 *
 * 使用方法:
 *   node scripts/create_gov_doc.js <output_filename.docx> [content_json]
 *
 * 示例:
 *   node scripts/create_gov_doc.js report.docx '{"title": "报告标题", "sections": [...]}'
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, ImageRun, UnderlineType
} = require('docx');
const fs = require('fs');

// ========== 格式常量定义 ==========
// 中文字体名称
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
 * 将文本中的 ASCII 双引号 " 替换为配对的中文双引号 ""（\u201c / \u201d）
 * 规则：
 *   1. 已有的正确中文引号对保持不变
 *   2. 孤立的中文左/右引号尝试与相邻的 ASCII 引号配对
 *   3. 剩余的 ASCII 引号按奇偶交替配对（奇数位→左引号，偶数位→右引号）
 *   4. 中文全角引号 " " 也统一为 \u201c \u201d
 */
function normalizeQuotes(text) {
  const LEFT = '\u201c';   // "
  const RIGHT = '\u201d';  // "

  let result = '';
  let quoteCount = 0; // 用于 ASCII 引号的奇偶配对

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];

    if (ch === '"' || ch === '\u201d' || ch === '\u201c') {
      // ASCII 双引号或中文双引号统一处理
      if (quoteCount % 2 === 0) {
        result += LEFT;
      } else {
        result += RIGHT;
      }
      quoteCount++;
    } else {
      result += ch;
    }
  }

  // 如果最终引号数量为奇数，说明有一个未配对的引号，强制闭合为右引号
  // 这种情况属于输入错误，做容错处理
  return result;
}

/**
 * 判断字符是否为西文字符（字母、数字、常见西文标点）
 */
function isLatinChar(char) {
  // ASCII码范围: 32-126, 以及扩展西文字符
  const code = char.charCodeAt(0);
  // 字母、数字、西文标点、空格等
  if ((code >= 32 && code <= 126) ||
      (code >= 160 && code <= 255) ||
      // 常见西文标点符号（不在ASCII但属于拉丁字母）
      'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏàáâãäåæçèéêëìíîïòóôõöøùúûüÿ'.indexOf(char) !== -1) {
    // 排除一些可能是中文标点的情况
    const latinPunct = '(),.;:!?\"\'-()[]{}';
    // 如果是基本ASCII或已知拉丁字符，且不是中文标点，则认为是西文
    return true;
  }
  return false;
}

/**
 * 将混合文本分割成中西文片段
 * 返回数组，每个元素: { text: string, isLatin: boolean }
 */
function splitByScript(text) {
  const segments = [];
  let currentText = '';
  let currentIsLatin = null;

  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    const isLatin = isLatinChar(char);

    // 换行符单独处理
    if (char === '\n') {
      if (currentText) {
        segments.push({ text: currentText, isLatin: currentIsLatin });
        currentText = '';
        currentIsLatin = null;
      }
      segments.push({ text: '\n', isLatin: false });
      continue;
    }

    if (currentIsLatin === null) {
      currentIsLatin = isLatin;
      currentText = char;
    } else if (currentIsLatin === isLatin) {
      currentText += char;
    } else {
      segments.push({ text: currentText, isLatin: currentIsLatin });
      currentText = char;
      currentIsLatin = isLatin;
    }
  }

  if (currentText) {
    segments.push({ text: currentText, isLatin: currentIsLatin });
  }

  return segments;
}

/**
 * 根据文本片段创建TextRun数组
 * 中文用 chineseFont, 西文用 latinFont
 * 
 * 每个 TextRun 均明确写入对应的中西文字体，确保 Word 在混合文本中
 * 正确渲染字体，不依赖样式继承的不确定性。
 * 行距、缩进等段落属性仍由段落样式控制，不在 TextRun 中重复设置。
 * 
 * @param {string} text - 文本内容
 * @param {string} chineseFont - 中文字体（eastAsia）
 * @param {string} latinFont - 西文字体（ascii / hAnsi）
 * @param {number} fontSize - 字体大小（半磅）
 * @param {object} options - 选项
 * @param {boolean} options.bold - 是否加粗
 * @param {boolean} options.italic - 是否斜体
 * @param {boolean} options.useDirectFormatting - 保留参数，已弃用（始终写入字体）
 */
function createTextRunsFromSegments(text, chineseFont, latinFont, fontSize, options = {}) {
  const { bold = false, italic = false } = options;
  // 先规范化双引号为中文配对引号
  const normalizedText = normalizeQuotes(text);
  const segments = splitByScript(normalizedText);
  const runs = [];

  for (const seg of segments) {
    if (seg.text === '\n') {
      // 换行符不创建空run
      continue;
    }

    // 始终明确写入字体：西文用 latinFont，中文用 chineseFont
    // 这样可以确保 Word 混合文本的字体不依赖样式继承，结果稳定可靠
    if (seg.isLatin) {
      runs.push(new TextRun({
        text: seg.text,
        font: {
          ascii: latinFont,
          hAnsi: latinFont,
          cs: latinFont,
        },
        bold: bold,
        italic: italic,
      }));
    } else {
      runs.push(new TextRun({
        text: seg.text,
        font: {
          eastAsia: chineseFont,
          ascii: latinFont,
          hAnsi: latinFont,
          cs: latinFont,
        },
        bold: bold,
        italic: italic,
      }));
    }
  }

  return runs;
}

// 字号转换 (Word中的"号"转换为半磅值)
const FONT_SIZES = {
  '小二号': 36,    // 18pt = 36 half-points
  '小三号': 30,    // 15pt = 30 half-points
  '四号': 28,       // 14pt = 28 half-points
  '小五号': 18     // 9pt = 18 half-points
};

// 行间距常数 (固定值28磅 = 28 * 20 = 560 twips)
const LINE_SPACING_EXACT_28 = { line: 560, lineRule: "exact" };
const LINE_SPACING_SINGLE = { line: 276, lineRule: "auto" };

// 页边距 (单位: DXA, 1440 DXA = 1英寸 = 2.54厘米)
// A4: 宽度 11906 DXA, 高度 16838 DXA
const PAGE_MARGINS = {
  top: Math.round(3.7 / 2.54 * 1440),    // 上 3.7cm
  bottom: Math.round(3.5 / 2.54 * 1440), // 下 3.5cm
  left: Math.round(2.8 / 2.54 * 1440),   // 左 2.8cm
  right: Math.round(2.6 / 2.54 * 1440)   // 右 2.6cm
};

// 内容宽度 = A4宽度 - 左右边距
const CONTENT_WIDTH = 11906 - PAGE_MARGINS.left - PAGE_MARGINS.right;

// ========== 样式定义 ==========

/**
 * 创建页码样式 (用于页脚)
 */
function createPageNumberStyle() {
  return {
    id: "页码样式",
    name: "页码样式",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: CHINESE_FONTS.SongTi,
      size: FONT_SIZES['四号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0 }
    }
  };
}

/**
 * 创建首页大标题样式
 */
function createTitleStyle() {
  return {
    id: "首页大标题",
    name: "首页大标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: {
        eastAsia: CHINESE_FONTS.FZXiaoBiaoSong,
        ascii: CHINESE_FONTS.TimesNewRoman,
        hAnsi: CHINESE_FONTS.TimesNewRoman,
        cs: CHINESE_FONTS.TimesNewRoman,
      },
      size: FONT_SIZES['小二号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
    }
  };
}

/**
 * 创建正文样式 (有首行缩进)
 */
function createBodyStyle() {
  return {
    id: "正文有缩进",
    name: "正文有缩进",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
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
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * FONT_SIZES['小三号'] * 10 }, // 首行缩进2字符: 2 * 15pt * 20twips/pt = 600twips
    }
  };
}

/**
 * 创建一级标题样式
 */
function createLevel1HeadingStyle() {
  return {
    id: "一级的标题",
    name: "一级的标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: {
        eastAsia: CHINESE_FONTS.HeiTi,
        ascii: CHINESE_FONTS.TimesNewRoman,
        hAnsi: CHINESE_FONTS.TimesNewRoman,
        cs: CHINESE_FONTS.TimesNewRoman,
      },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * FONT_SIZES['小三号'] * 10 }, // 首行缩进2字符: 600twips
      outlineLevel: 0,
    }
  };
}

/**
 * 创建二级标题样式
 */
function createLevel2HeadingStyle() {
  return {
    id: "二级的标题",
    name: "二级的标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: {
        eastAsia: CHINESE_FONTS.KaiTi,
        ascii: CHINESE_FONTS.TimesNewRoman,
        hAnsi: CHINESE_FONTS.TimesNewRoman,
        cs: CHINESE_FONTS.TimesNewRoman,
      },
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * FONT_SIZES['小三号'] * 10 }, // 首行缩进2字符: 600twips
      outlineLevel: 1,
    }
  };
}

/**
 * 创建三级标题样式
 */
function createLevel3HeadingStyle() {
  return {
    id: "三级的标题",
    name: "三级的标题",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: {
        eastAsia: CHINESE_FONTS.FZFangSong,
        ascii: CHINESE_FONTS.TimesNewRoman,
        hAnsi: CHINESE_FONTS.TimesNewRoman,
        cs: CHINESE_FONTS.TimesNewRoman,
      },
      size: FONT_SIZES['小三号'],
      bold: true,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 2 * FONT_SIZES['小三号'] * 10 }, // 首行缩进2字符: 600twips
      outlineLevel: 2,
    }
  };
}

/**
 * 创建图片样式
 */
function createImageStyle() {
  return {
    id: "图片样式",
    name: "图片样式",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: CHINESE_FONTS.FZFangSong,
      size: FONT_SIZES['小三号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    }
  };
}

/**
 * 创建表格样式
 */
function createTableStyle() {
  return {
    id: "表格样式",
    name: "表格样式",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
    run: {
      font: {
        eastAsia: CHINESE_FONTS.FZFangSong,
        ascii: CHINESE_FONTS.TimesNewRoman,
        hAnsi: CHINESE_FONTS.TimesNewRoman,
        cs: CHINESE_FONTS.TimesNewRoman,
      },
      size: FONT_SIZES['小五号'],
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    }
  };
}

/**
 * 创建落款-部门样式（右下对齐，无缩进）
 */
function createSignatureDeptStyle() {
  return {
    id: "落款-部门",
    name: "落款-部门",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
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
      alignment: AlignmentType.RIGHT,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 0 },
    }
  };
}

/**
 * 创建落款-日期样式（右下对齐，与部门名称左对齐）
 */
function createSignatureDateStyle() {
  return {
    id: "落款-日期",
    name: "落款-日期",
    basedOn: "Normal",
    next: "Normal",
    quickFormat: true,
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
      alignment: AlignmentType.RIGHT,
      spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
      indent: { firstLine: 0 },
    }
  };
}

// ========== 文档创建函数 ==========

/**
 * 创建文档实例
 */
function createDocument(options = {}) {
  const {
    title = '',
    author = '',
    sections = [],
    footnotes = {}
  } = options;

  // 计算首行缩进字符宽度 (小三号字体，1字符 = 15pt = 300twips)
  const firstLineChars = 2;
  const charWidth = FONT_SIZES['小三号'] * 10; // 30 半磅 * 10 = 300 twips = 1字符宽度

  const doc = new Document({
    creator: author,
    title: title,
    description: '',
    styles: {
      default: {
        document: {
          run: {
            // 分中西文设置字体，避免 docDefaults 中 ascii/hAnsi 被设置为中文字体
            font: {
              eastAsia: CHINESE_FONTS.FZFangSong,
              ascii: CHINESE_FONTS.TimesNewRoman,
              hAnsi: CHINESE_FONTS.TimesNewRoman,
              cs: CHINESE_FONTS.TimesNewRoman,
            },
            size: FONT_SIZES['小三号'],
          },
          // 设置文档默认段落属性（pPrDefault），确保 Normal（正文）样式有固定28磅行距
          paragraph: {
            spacing: { before: 0, after: 0, line: 560, lineRule: "exact" },
          }
        }
      },
      paragraphStyles: [
        createPageNumberStyle(),
        createTitleStyle(),
        createBodyStyle(),
        createLevel1HeadingStyle(),
        createLevel2HeadingStyle(),
        createLevel3HeadingStyle(),
        createImageStyle(),
        createTableStyle(),
        createSignatureDeptStyle(),
        createSignatureDateStyle(),
      ]
    },
    numbering: {
      config: [
        // 一级标题编号: 一、二、三、
        {
          reference: "level1-numbers",
          levels: [{
            level: 0,
            format: LevelFormat.UPPER_ROMAN,
            text: "",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: charWidth * (firstLineChars + 1), hanging: charWidth }
              }
            }
          }]
        },
        // 二级标题编号: （一）、（二）、（三）
        {
          reference: "level2-numbers",
          levels: [{
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: charWidth * (firstLineChars + 1), hanging: charWidth }
              }
            }
          }]
        },
        // 三级标题编号: 1.、2.、3.
        {
          reference: "level3-numbers",
          levels: [{
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: charWidth * (firstLineChars + 1), hanging: charWidth }
              }
            }
          }]
        },
      ]
    },
    sections: [{
      properties: {
        page: {
          size: {
            width: 11906,  // A4宽度
            height: 16838, // A4高度
          },
          margin: PAGE_MARGINS
        }
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              style: "页码样式",
              children: [
                new TextRun({
                  children: [PageNumber.CURRENT]
                })
              ]
            })
          ]
        })
      },
      children: sections
    }],
    footnotes: footnotes
  });

  return doc;
}

/**
 * 创建首页大标题段落
 */
function createTitleParagraph(text) {
  return new Paragraph({
    style: "首页大标题",
    children: [new TextRun({ text: normalizeQuotes(text) })]
  });
}

/**
 * 创建正文段落 (有首行缩进)
 * 中文字符使用方正仿宋，西文字符使用Times New Roman
 */
function createBodyParagraph(text, options = {}) {
  const { bold = false, italic = false } = options;
  return new Paragraph({
    style: "正文有缩进",
    children: createTextRunsFromSegments(
      text,
      CHINESE_FONTS.FZFangSong,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { bold, italic, useDirectFormatting: false }
    )
  });
}

/**
 * 创建一级标题
 * 序号格式: 一、二、三、
 * 中文字符使用黑体，西文字符使用Times New Roman
 */
function createLevel1Heading(text, number) {
  const chineseNumbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                          '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十'];

  let prefix = '';
  let expectedNumeral = '';
  if (number !== undefined) {
    // 生成中文序号
    const num = number + 1;
    if (num <= 20) {
      expectedNumeral = chineseNumbers[num - 1];
      prefix = expectedNumeral + '、';
    } else {
      expectedNumeral = String(num);
      prefix = expectedNumeral + '、';
    }
  }

  // 检测text是否已包含序号前缀，避免重复
  let finalText = text;
  if (text && number !== undefined && expectedNumeral) {
    // 匹配 "一、" 或 "一" 开头的模式
    const existingMatch = text.match(/^([一二三四五六七八九十]+)、?/);
    if (existingMatch && existingMatch[1] === expectedNumeral) {
      // 已有对应序号的前缀，不再添加
      finalText = text;
    } else if (existingMatch) {
      // 有其他序号前缀，替换为正确的
      finalText = prefix + text.replace(/^[一二三四五六七八九十]+、?/, '');
    } else {
      // 没有序号前缀，添加
      finalText = prefix + text;
    }
  } else if (prefix) {
    finalText = prefix + text;
  }

  return new Paragraph({
    style: "一级的标题",
    children: createTextRunsFromSegments(
      finalText,
      CHINESE_FONTS.HeiTi,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { useDirectFormatting: false }
    )
  });
}

/**
 * 创建二级标题
 * 序号格式: （一）、（二）、（三）
 * 中文字符使用楷体，西文字符使用Times New Roman
 */
function createLevel2Heading(text, number) {
  const chineseNumbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                          '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十'];
  let prefix = '';
  let expectedNumeral = '';

  if (number !== undefined) {
    const num = number + 1;
    if (num <= 20) {
      expectedNumeral = chineseNumbers[num - 1];
      prefix = '（' + expectedNumeral + '）';
    } else {
      expectedNumeral = String(num);
      prefix = '（' + expectedNumeral + '）';
    }
  }

  // 检测text是否已包含序号前缀，避免重复
  let finalText = text;
  if (text && number !== undefined && expectedNumeral) {
    // 匹配 "（一）" 开头的模式（不再带顿号）
    const existingMatch = text.match(/^（([一二三四五六七八九十]+)）、?/);
    if (existingMatch && existingMatch[1] === expectedNumeral) {
      // 已有对应序号的前缀（可能带或不带顿号），统一去掉顿号
      finalText = prefix + text.replace(/^（[一二三四五六七八九十]+）、?/, '');
    } else if (existingMatch) {
      // 有其他序号前缀，替换为正确的
      finalText = prefix + text.replace(/^（[一二三四五六七八九十]+）、?/, '');
    } else {
      // 没有序号前缀，添加
      finalText = prefix + text;
    }
  } else if (prefix) {
    finalText = prefix + text;
  }

  return new Paragraph({
    style: "二级的标题",
    children: createTextRunsFromSegments(
      finalText,
      CHINESE_FONTS.KaiTi,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { useDirectFormatting: false }
    )
  });
}

/**
 * 创建三级标题
 * 序号格式: 1.、2.、3.（序号后跟点号，不跟顿号）
 * 中文字符使用方正仿宋（加粗），西文字符使用Times New Roman
 */
function createLevel3Heading(text, number) {
  let prefix = '';
  let expectedNumeral = '';

  if (number !== undefined) {
    expectedNumeral = String(number + 1);
    prefix = expectedNumeral + '.';
  }

  // 检测text是否已包含序号前缀，避免重复
  // 匹配 "1." 或 "1、" 或 "1 " 等模式（数字开头）
  let finalText = text;
  if (text && number !== undefined && expectedNumeral) {
    const existingMatch = text.match(/^(\d+)[、.\s]/);
    if (existingMatch && existingMatch[1] === expectedNumeral) {
      // 已有对应序号前缀，统一替换为标准格式（点号）
      finalText = prefix + text.replace(/^\d+[、.\s]/, '');
    } else if (existingMatch) {
      // 有其他数字序号前缀，替换为正确的
      finalText = prefix + text.replace(/^\d+[、.\s]/, '');
    } else {
      // 没有数字序号前缀，添加
      finalText = prefix + text;
    }
  } else if (prefix) {
    finalText = prefix + text;
  }

  return new Paragraph({
    style: "三级的标题",
    children: createTextRunsFromSegments(
      finalText,
      CHINESE_FONTS.FZFangSong,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { bold: true, useDirectFormatting: false }
    )
  });
}

/**
 * 安全创建一级标题（自动处理重复前缀）
 * 如果传入的text已以中文序号开头，则不再添加前缀
 * 中文字符使用黑体，西文字符使用Times New Roman
 */
function createLevel1HeadingSafe(text, number) {
  const chineseNumbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                          '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十'];

  let prefix = '';
  if (number !== undefined) {
    const num = number + 1;
    if (num <= 20) {
      prefix = chineseNumbers[num - 1] + '、';
    } else {
      prefix = num + '、';
    }
  }

  // 检查text是否已经以prefix开头（处理重复）
  let finalText = text;
  if (text && prefix && text.startsWith(prefix)) {
    finalText = text; // 已有前缀，不再添加
  } else if (prefix) {
    finalText = prefix + text;
  }

  return new Paragraph({
    style: "一级的标题",
    children: createTextRunsFromSegments(
      finalText,
      CHINESE_FONTS.HeiTi,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { useDirectFormatting: false }
    )
  });
}

/**
 * 安全创建二级标题（自动处理重复前缀）
 * 如果传入的text已以中文序号开头，则不再添加前缀
 * 序号格式: （一）、（二）、（三）
 */
function createLevel2HeadingSafe(text, number) {
  const chineseNumbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                          '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十'];
  let prefix = '';
  let expectedNumeral = '';

  if (number !== undefined) {
    const num = number + 1;
    if (num <= 20) {
      expectedNumeral = chineseNumbers[num - 1];
      prefix = '（' + expectedNumeral + '）';
    } else {
      expectedNumeral = String(num);
      prefix = '（' + expectedNumeral + '）';
    }
  }

  // 提取text中已有的中文数字序号（用于检测是否重复）
  // 匹配 "（一）" 或 "（一）、" 等模式
  let finalText = text;
  if (text && number !== undefined && expectedNumeral) {
    const existingMatch = text.match(/^（([一二三四五六七八九十]+)）、?/);
    if (existingMatch && existingMatch[1] === expectedNumeral) {
      // 已有对应序号（可能带顿号），统一去掉顿号
      finalText = prefix + text.replace(/^（[一二三四五六七八九十]+）、?/g, '');
    } else if (existingMatch) {
      // 有其他序号前缀，替换为正确的
      finalText = prefix + text.replace(/^（[一二三四五六七八九十]+）、?/g, '');
    } else {
      // 没有序号前缀，添加
      finalText = prefix + text;
    }
  } else if (prefix) {
    finalText = prefix + text;
  }

  return new Paragraph({
    style: "二级的标题",
    children: createTextRunsFromSegments(
      finalText,
      CHINESE_FONTS.KaiTi,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { useDirectFormatting: false }
    )
  });
}

/**
 * 创建图片段落
 */
function createImageParagraph(imageData, width, height, options = {}) {
  const { transformation = {} } = options;
  const actualWidth = transformation.width || width;
  const actualHeight = transformation.height || height;

  return new Paragraph({
    style: "图片样式",
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
    children: [
      new ImageRun({
        type: 'png',
        data: imageData,
        transformation: {
          width: actualWidth,
          height: actualHeight,
        },
        altText: {
          title: options.altText || '',
          description: options.description || '',
          name: options.name || ''
        }
      })
    ]
  });
}

/**
 * 计算字符串显示宽度（中文字符按1个宽度，ASCII按0.5个宽度）
 * @param {string} str
 * @returns {number}
 */
function calcDisplayWidth(str) {
  let width = 0;
  for (const ch of str) {
    const code = ch.charCodeAt(0);
    if (code >= 0x4e00 && code <= 0x9fff || code >= 0x3000 && code <= 0x303f || code >= 0xff00 && code <= 0xffef) {
      // 中日韩统一表意文字、标点
      width += 1;
    } else if (code <= 127) {
      // ASCII（字母/数字/西文标点）
      width += 0.5;
    } else {
      // 其他全角字符
      width += 1;
    }
  }
  return width;
}

/**
 * 创建落款段落（右下对齐，无首行缩进）
 * @param {string} text - 落款文本
 * @param {object} options - 选项 { bold, indentRight, styleName }
 */
function createSignatureParagraph(text, options = {}) {
  const { bold = false, indentRight = 0, styleName = "落款-部门" } = options;
  const paraOptions = {
    style: styleName,
    children: createTextRunsFromSegments(
      text,
      CHINESE_FONTS.FZFangSong,
      CHINESE_FONTS.TimesNewRoman,
      FONT_SIZES['小三号'],
      { bold }
    )
  };
  // 右缩进（将段落整体向左推移）
  if (indentRight > 0) {
    paraOptions.indent = { right: indentRight * FONT_SIZES['小三号'] * 10 };
  }
  return new Paragraph(paraOptions);
}

/**
 * 创建落款块（部门名称 + 日期，与正文间隔一行）
 * 两行均右顶格对齐，不加任何缩进，日期自然向左延伸
 * @param {string} department - 部门名称
 * @param {string} date - 日期
 * @param {object} options - 选项 { boldDepartment }
 */
function createSignatureBlock(department, date, options = {}) {
  const { boldDepartment = false } = options;
  const paragraphs = [];

  // 与正文间隔一行（空行）
  paragraphs.push(new Paragraph({
    style: "落款-部门",
    children: [new TextRun({ text: "" })]
  }));

  // 部门名称（右顶格）
  paragraphs.push(createSignatureParagraph(department, {
    bold: boldDepartment,
    styleName: "落款-部门"
  }));

  // 日期（右顶格，自然比部门名称向左延伸）
  paragraphs.push(createSignatureParagraph(date, {
    styleName: "落款-日期"
  }));

  return paragraphs;
}

/**
 * 创建表格
 * rows: 数组，可以是:
 *   - { children: ['cell1', 'cell2', ...] } 格式的普通对象
 *   - 已经创建好的 TableRow 对象（如从 createTableHeaderRow 返回的）
 * 表格宽度自动适应窗口和内容（WidthType.AUTO）
 */
function createTable(rows, options = {}) {
  const { columnWidths = [] } = options;

  // 计算总宽度（仅用于均分列宽的参考，实际表格宽度由 AUTO 决定）
  const totalWidth = columnWidths.reduce((sum, w) => sum + w, 0) || CONTENT_WIDTH;

  // 确保列宽数组有值（用于单元格相对比例，实际由 AUTO 自动调整）
  const widths = columnWidths.length > 0
    ? columnWidths
    : Array(rows[0]?.children?.length || 0).fill(Math.floor(totalWidth / (rows[0]?.children?.length || 1)));

  const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
  const borders = { top: border, bottom: border, left: border, right: border };

  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },  // 自动适应窗口宽度（百分比100%）
    columnWidths: widths,
    rows: rows.map(row => {
      // 如果已经是 TableRow 实例，直接返回
      if (row instanceof TableRow) {
        return row;
      }

      // 否则按普通对象处理
      const cells = row.children || row;
      return new TableRow({
        children: cells.map((cell, idx) => {
          // 如果已经是 TableCell 实例，直接返回
          if (cell instanceof TableCell) {
            return cell;
          }

          // 普通对象或字符串，转为字符串处理
          const cellText = typeof cell === 'string' ? cell : (cell.text || String(cell));
          const normalizedCellText = normalizeQuotes(cellText);
          return new TableCell({
            borders: borders,
            width: { size: widths[idx] || Math.floor(totalWidth / cells.length), type: WidthType.DXA },
            shading: { fill: "FFFFFF", type: ShadingType.CLEAR },
            margins: { top: 50, bottom: 50, left: 100, right: 100 },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              style: "表格样式",
              alignment: AlignmentType.CENTER,
              spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
              children: [new TextRun({ text: normalizedCellText })]
            })]
          });
        })
      });
    })
  });
}

/**
 * 创建表头行 (灰色底)
 * 与 createTable 配合使用时，表格整体宽度由 createTable 的 PERCENTAGE 控制
 */
function createTableHeaderRow(cells, columnWidths) {
  const totalWidth = columnWidths.reduce((sum, w) => sum + w, 0) || CONTENT_WIDTH;
  const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
  const borders = { top: border, bottom: border, left: border, right: border };

  return new TableRow({
    tableHeader: true,
    children: cells.map((cell, idx) => {
      const cellText = String(cell);
      // 表头文本使用直接格式化加粗
      const textRuns = [new TextRun({ text: normalizeQuotes(cellText), bold: true })];
      return new TableCell({
        borders: borders,
        width: { size: columnWidths[idx] || Math.floor(totalWidth / cells.length), type: WidthType.DXA },
        shading: { fill: "D9D9D9", type: ShadingType.CLEAR }, // 灰色底
        margins: { top: 50, bottom: 50, left: 100, right: 100 },
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
          style: "表格样式",
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 0, line: 276, lineRule: "auto" },
          children: textRuns
        })]
      });
    })
  });
}

/**
 * 添加页码
 */
function addPageNumber(paragraph) {
  paragraph.addRun(new TextRun({
    children: [PageNumber.CURRENT],
    font: CHINESE_FONTS.SongTi,
    size: FONT_SIZES['四号']
  }));
  return paragraph;
}

// ========== 便捷函数 ==========
/**
 * 创建国央企标准文档（便捷函数）
 * @param {Object} content - 文档内容
 * @param {string} content.title - 文档标题
 * @param {Array} content.sections - 文档段落数组，每个元素可以是：
 *   - { type: 'title', text: '标题文字' }
 *   - { type: 'body', text: '正文文字' }
 *   - { type: 'heading1', text: '一级标题' }
 *   - { type: 'heading2', text: '二级标题' }
 *   - { type: 'heading3', text: '三级标题' }
 *   - { type: 'table', headers: [...], rows: [...] }
 * @param {string} outputPath - 输出文件路径
 */
async function createGovDocument(content, outputPath) {
  const { title = '', sections = [] } = content;
  
  // 转换sections为段落对象
  const paragraphs = [];
  let heading1Count = 0;
  let heading2Count = 0;
  let heading3Count = 0;
  
  for (const section of sections) {
    switch (section.type) {
      case 'title':
        paragraphs.push(createTitleParagraph(section.text));
        break;
      case 'body':
        if (section.text) {
          paragraphs.push(createBodyParagraph(section.text));
        } else {
          // 空行
          paragraphs.push(createBodyParagraph(''));
        }
        break;
      case 'heading1':
        paragraphs.push(createLevel1HeadingSafe(section.text, heading1Count));
        heading1Count++;
        heading2Count = 0;
        heading3Count = 0;
        break;
      case 'heading2':
        paragraphs.push(createLevel2HeadingSafe(section.text, heading2Count));
        heading2Count++;
        heading3Count = 0;
        break;
      case 'heading3':
        paragraphs.push(createLevel3Heading(section.text, heading3Count));
        heading3Count++;
        break;
      case 'table':
        if (section.headers && section.rows) {
          paragraphs.push(createTable(section.rows, { headers: section.headers }));
        }
        break;
      case 'signature':
        // 落款块：department + date
        if (section.department && section.date) {
          paragraphs.push(...createSignatureBlock(section.department, section.date, section.options || {}));
        } else if (section.text) {
          // 单个落款行
          paragraphs.push(createSignatureParagraph(section.text, section.options || {}));
        }
        break;
    }
  }
  
  const doc = createDocument({
    title,
    sections: paragraphs
  });
  
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`文档已保存: ${outputPath}`);
}

// ========== 导出函数 ==========
module.exports = {
  // 字体常量
  CHINESE_FONTS,
  FONT_SIZES,
  LINE_SPACING_EXACT_28,
  LINE_SPACING_SINGLE,
  PAGE_MARGINS,
  CONTENT_WIDTH,

  // 文档创建
  createDocument,
  createGovDocument,
  createTitleParagraph,
  createBodyParagraph,
  createLevel1Heading,
  createLevel2Heading,
  createLevel3Heading,
  createLevel1HeadingSafe,
  createLevel2HeadingSafe,
  createImageParagraph,
  createSignatureParagraph,
  createSignatureBlock,
  calcDisplayWidth,
  createTable,
  createTableHeaderRow,

  // 常量
  AlignmentType,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  PageNumber,
  PageBreak,
  ImageRun,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  Footer,
  Document,
  Packer,
};

// ========== CLI 入口 ==========
if (require.main === module) {
  const args = process.argv.slice(2);
  const outputFile = args[0] || 'output.docx';
  let content = {};

  if (args[1]) {
    try {
      content = JSON.parse(args[1]);
    } catch (e) {
      console.error('Invalid JSON content:', e.message);
      process.exit(1);
    }
  }

  const {
    title = '',
    body = [],
  } = content;

  // 构建文档内容
  const sections = [];

  // 添加标题
  if (title) {
    sections.push(createTitleParagraph(title));
  }

  // 添加正文
  body.forEach(item => {
    if (item.type === 'heading1') {
      sections.push(createLevel1Heading(item.text, item.number));
    } else if (item.type === 'heading2') {
      sections.push(createLevel2Heading(item.text, item.number));
    } else if (item.type === 'heading3') {
      sections.push(createLevel3Heading(item.text, item.number));
    } else if (item.type === 'paragraph') {
      sections.push(createBodyParagraph(item.text, item.options || {}));
    } else if (item.type === 'table') {
      sections.push(createTable(item.rows, { columnWidths: item.columnWidths }));
    } else if (item.type === 'image') {
      sections.push(createImageParagraph(item.data, item.width, item.height, item.options || {}));
    }
  });

  const doc = createDocument({ title, sections });

  Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputFile, buffer);
    console.log(`Document created: ${outputFile}`);
  }).catch(err => {
    console.error('Error creating document:', err);
    process.exit(1);
  });
}
