/**
 * gongwen_template.js - 公文模板 for docx-js
 *
 * 基于 GB/T 9704-2012 和企业内部公文格式要求
 *
 * 使用方法:
 *   1. npm install docx
 *   2. node gongwen_template.js
 */

const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, LineRuleType, HeadingLevel
} = require('docx');
const fs = require('fs');

// ============================================
// 公文字体定义 (Font Definitions)
// ============================================
const FONTS = {
  // 标题字体
  xiaobiaosong: '方正小标宋简体',

  // 正文字体
  fangsong: '方正仿宋',

  // 标题层级字体
  heiti: '方正黑体',     // 一级标题
  kaiti: '方正楷体',     // 二级标题

  // 备用字体 (系统未安装方正字体时使用)
  fangsong_alt: 'FangSong',
  heiti_alt: 'SimHei',
  kaiti_alt: 'KaiTi',
};

// ============================================
// 公文字号定义 (Size Definitions in half-points)
// ============================================
const SIZES = {
  erhao: 44,   // 二号 = 22pt = 44 half-points (标题)
  sanhao: 32,  // 三号 = 16pt = 32 half-points (正文)
  sihao: 36,   // 四号 = 18pt (副标题等)
};

// ============================================
// 页面设置 (Page Settings - A4)
// ============================================
// A4: 210mm × 297mm
// 页边距: 上37mm, 下35mm, 左28mm, 右26mm
// 换算为 DXA: 1mm = 56.69 DXA
const PAGE = {
  width: 11906,    // A4 width in DXA
  height: 16838,   // A4 height in DXA
  margin: {
    top: 2097,     // 37mm
    bottom: 1984,  // 35mm
    left: 1587,    // 28mm
    right: 1474,   // 26mm
  }
};

// ============================================
// 公文样式创建函数 (Style Helper Functions)
// ============================================

/**
 * 创建标题段落 (二级/三号方正小标宋简体)
 */
function createTitle(text, options = {}) {
  const isMultiLine = options.multiLine || false;
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: text,
        font: FONTS.xiaobiaosong,
        size: SIZES.erhao,
        bold: false,  // 标题不加粗
      })
    ],
    spacing: {
      line: isMultiLine ? 760 : 600,  // 多行38磅，单行30磅
      lineRule: LineRuleType.AUTO,
    },
  });
}

/**
 * 创建正文段落 (三号方正仿宋，行距28磅)
 */
function createBody(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    children: [
      new TextRun({
        text: text,
        font: FONTS.fangsong,
        size: SIZES.sanhao,
        bold: false,
      })
    ],
    spacing: {
      line: 560,  // 28磅 = 560 DXA (28 * 20)
      lineRule: LineRuleType.AUTO,
      before: 0,
      after: 0,
    },
    indent: {
      firstLine: 684,  // 首行缩进2字符 (约34pt)
    },
  });
}

/**
 * 创建一级标题 (一、/ 二、/ ...)
 */
function createHeading1(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        font: FONTS.heiti,
        size: SIZES.sanhao,
        bold: false,
      })
    ],
    spacing: {
      line: 560,  // 28磅
      lineRule: LineRuleType.AUTO,
      before: 240,  // 段前12磅
      after: 0,
    },
  });
}

/**
 * 创建二级标题 (（一）/（二）/ ...)
 */
function createHeading2(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        font: FONTS.kaiti,
        size: SIZES.sanhao,
        bold: false,
      })
    ],
    spacing: {
      line: 560,
      lineRule: LineRuleType.AUTO,
      before: 120,  // 段前6磅
      after: 0,
    },
  });
}

/**
 * 创建三级标题 (1. / 2. / ...)
 */
function createHeading3(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        font: FONTS.fangsong,
        size: SIZES.sanhao,
        bold: false,
      })
    ],
    spacing: {
      line: 560,
      lineRule: LineRuleType.AUTO,
      before: 60,
      after: 0,
    },
    indent: {
      left: 342,  // 左缩进约1字符
    },
  });
}

/**
 * 创建四级标题 ((1) / (2) / ...)
 */
function createHeading4(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        font: FONTS.fangsong,
        size: SIZES.sanhao,
        bold: false,
      })
    ],
    spacing: {
      line: 560,
      lineRule: LineRuleType.AUTO,
    },
    indent: {
      left: 684,  // 左缩进约2字符
    },
  });
}

/**
 * 创建附件列表项
 */
function createAttachment(text, number) {
  return new Paragraph({
    children: [
      new TextRun({
        text: `${number}. `,
        font: FONTS.fangsong,
        size: SIZES.sanhao,
        bold: false,
      }),
      new TextRun({
        text: text,
        font: FONTS.fangsong,
        size: SIZES.sanhao,
        bold: false,
      }),
    ],
    spacing: {
      line: 560,
      lineRule: LineRuleType.AUTO,
    },
    indent: {
      left: 1026,  // 左缩进约3字符
    },
  });
}

// ============================================
// 公文文档创建示例 (Example Document)
// ============================================

function createGongwen() {
  const doc = new Document({
    sections: [{
      properties: {
        page: {
          size: {
            width: PAGE.width,
            height: PAGE.height,
          },
          margin: PAGE.margin,
        },
      },
      children: [
        // 标题
        createTitle('关于XXXX的工作通知'),

        // 空行
        new Paragraph({ children: [] }),

        // 正文
        createBody('根据公司战略部署和年度工作安排，现就XXXX工作通知如下：'),

        // 一级标题
        createHeading1('一、总体要求'),

        // 二级标题
        createHeading2('（一）基本原则'),
        createBody('坚持统筹推进、分步实施，确保各项工作有序开展。'),

        createHeading2('（二）工作目标'),
        createBody('通过本次工作，进一步提升公司管理水平，增强核心竞争力。'),

        // 一级标题
        createHeading1('二、重点任务'),
        createBody('具体任务安排如下：'),

        // 三级标题
        createHeading3('1. 任务一'),
        createBody('全面梳理现有流程，优化资源配置，提高工作效率。'),

        createHeading3('2. 任务二'),
        createBody('建立健全规章制度，完善考核机制，强化执行力度。'),

        // 四级标题示例
        createHeading4('（1）第一阶段'),
        createBody('完成基础调研和方案制定工作。'),

        createHeading4('（2）第二阶段'),
        createBody('组织实施并进行跟踪评估。'),

        // 一级标题
        createHeading1('三、保障措施'),

        createHeading2('（一）加强组织领导'),
        createBody('成立专项工作组，明确责任分工，确保工作落实到位。'),

        createHeading2('（二）强化监督检查'),
        createBody('定期开展工作检查，及时发现问题并督促整改。'),

        // 附件
        new Paragraph({ children: [] }),
        new Paragraph({
          children: [
            new TextRun({
              text: '附件：',
              font: FONTS.fangsong,
              size: SIZES.sanhao,
              bold: false,
            })
          ],
        }),
        createAttachment('《XXXX任务清单》', 1),
        createAttachment('《XXXX进度安排表》', 2),

        // 落款
        new Paragraph({ children: [] }),
        new Paragraph({ children: [] }),
        new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({
              text: 'XXXX公司',
              font: FONTS.fangsong,
              size: SIZES.sanhao,
              bold: false,
            })
          ],
          spacing: { line: 560, lineRule: LineRuleType.AUTO },
        }),
        new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({
              text: '2026年4月5日',
              font: FONTS.fangsong,
              size: SIZES.sanhao,
              bold: false,
            })
          ],
          spacing: { line: 560, lineRule: LineRuleType.AUTO },
        }),
      ],
    }],
  });

  return doc;
}

// ============================================
// 生成公文
// ============================================

const doc = createGongwen();

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('gongwen_output.docx', buffer);
  console.log('公文已生成: gongwen_output.docx');
}).catch(err => {
  console.error('生成失败:', err);
});
