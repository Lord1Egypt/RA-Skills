// ============================================================
// arabic_docx_template.js — قالب توليد مستند Word عربي
// ============================================================
// هذا القالب يحتوي على جميع الدوال المساعدة المُختبَرة لتوليد
// مستندات Word عربية بشكل صحيح: خطوط منفصلة (عربي/إنجليزي)،
// تخطيط RTL، أرقام عربية، جداول، فهرس، ترويسة/تذييل.
//
// الاستخدام: انسخ هذا الملف، عدّل المحتوى في قسم "المحتوى"،
// ثم شغّله: node arabic_docx_template.js
// ============================================================

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  PageBreak, Header, Footer, PageNumber, NumberFormat,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
  PageOrientation, SectionType, TableOfContents, LevelFormat,
  TableLayoutType, VerticalAlign, Bookmark, InternalHyperlink,
} = require("docx");
const fs = require("fs");

// ===== الخطوط والألوان =====
// الخط الإنجليزي (ASCII/hAnsi): للنص اللاتيني والمصطلحات الإنجليزية
// الخط العربي (cs / Complex Script): للنص العربي والأرقام العربية
const FONT_EN = "Times New Roman";
const FONT_AR = "Simplified Arabic";

// بدائل مقترحة:
//   عربي: "Traditional Arabic" (للعناوين)، "Arial"، "Sakkal Majalla"
//   إنجليزي: "Arial"، "Calibri"

// أحجام الخطوط (بنصف النقطة): 11pt=22, 12pt=24, 14pt=28, 15pt=30, 18pt=36
const SIZE_BODY = 28;   // 14pt — حجم النص الأساسي
const SIZE_H1 = 36;     // 18pt
const SIZE_H2 = 30;     // 15pt
const SIZE_H3 = 28;     // 14pt
const SIZE_CAPTION = 22; // 11pt — عناوين الجداول والأشكال
const SIZE_HEADER = 20;  // 10pt — الترويسة
const SIZE_FOOTER = 22;  // 11pt — التذييل
const SIZE_TABLE = 22;   // 11pt — خلايا الجدول
const SIZE_TABLE_HEAD = 24; // 12pt — رؤوس الجدول

// الألوان
const COLOR_BLACK = "000000";
const COLOR_DARK = "1A1A1A";
const COLOR_GREY = "606060";
const COLOR_ACCENT = "1A5276";     // أزرق داكن أكاديمي
const COLOR_TABLE_HEAD = "1A5276"; // خلفية رأس الجدول
const COLOR_TABLE_ALT = "EDF3F8";  // خلفية الصفوف البديلة
const COLOR_BORDER = "9AA6B2";

// اختصار للخط المنقسم (يستخدم في كل TextRun)
const FONT_BODY = { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR };
const FONT_HEAD = { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR };

// ===== ثوابت الحدود =====
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };

// ===== مساعدات النص =====

// قيمة آمنة (تستبدل undefined/NaN بعنصر نائب)
function safeText(v, placeholder) {
  if (v === undefined || v === null || v === "" || String(v) === "NaN" || String(v) === "undefined") {
    return placeholder || "【يُملأ لاحقًا】";
  }
  return String(v);
}

// فقرة عربية أساسية (RTL، مضبوطة، بمسافة بادئة)
function p(text, opts) {
  opts = opts || {};
  return new Paragraph({
    bidirectional: true,
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: opts.before || 0, after: opts.after != null ? opts.after : 120 },
    indent: opts.noIndent ? undefined : { firstLine: 480 },
    children: [new TextRun({
      text: text,
      rightToLeft: true,
      size: opts.size || SIZE_BODY,
      bold: opts.bold || false,
      italics: opts.italics || false,
      color: opts.color || COLOR_BLACK,
      font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
    })],
  });
}

// فقرة فارغة بمسافة كبيرة (للفصل بين الأقسام)
function pGap(twips) {
  return new Paragraph({ spacing: { before: twips || 240 }, children: [] });
}

// عنوان رئيسي H1
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    bidirectional: true,
    alignment: AlignmentType.CENTER,
    spacing: { before: 480, after: 280, line: 360 },
    children: [new TextRun({
      text: text,
      rightToLeft: true,
      size: SIZE_H1,
      bold: true,
      color: COLOR_BLACK,
      font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
    })],
  });
}

// عنوان فرعي H2
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 320, after: 180, line: 360 },
    children: [new TextRun({
      text: text,
      rightToLeft: true,
      size: SIZE_H2,
      bold: true,
      color: COLOR_BLACK,
      font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
    })],
  });
}

// عنوان فرعي H3
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 240, after: 120, line: 360 },
    children: [new TextRun({
      text: text,
      rightToLeft: true,
      size: SIZE_H3,
      bold: true,
      color: COLOR_DARK,
      font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
    })],
  });
}

// نقطة في قائمة نقطية
function bullet(text, level) {
  level = level || 0;
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, after: 100 },
    bullet: { level: level },
    children: [new TextRun({
      text: text,
      rightToLeft: true,
      size: SIZE_BODY,
      color: COLOR_BLACK,
      font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
    })],
  });
}

// نقطة مرقمة يدوياً (الترقيم اليدوي أفضل من قوائم Word للأرقام العربية)
function numItem(text, num) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, after: 100 },
    indent: { left: 720, hanging: 360 },
    children: [
      new TextRun({ text: num + ". ", rightToLeft: true, size: SIZE_BODY, bold: true, color: COLOR_BLACK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } }),
      new TextRun({ text: text, rightToLeft: true, size: SIZE_BODY, color: COLOR_BLACK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } }),
    ],
  });
}

// عنوان جدول/شكل (يُحفظ مع الجدول التالي عبر keepNext)
function tableCaption(text) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 100, line: 320 },
    keepNext: true,
    children: [new TextRun({
      text: text,
      rightToLeft: true,
      size: SIZE_CAPTION,
      bold: true,
      color: COLOR_DARK,
      font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
    })],
  });
}

// خلية جدول عربية (تدعم أسطرًا متعددة عبر \n)
function tCell(text, opts) {
  opts = opts || {};
  const isHeader = opts.header || false;
  const bgFill = opts.fill || (isHeader ? COLOR_TABLE_HEAD : (opts.alt ? COLOR_TABLE_ALT : "FFFFFF"));
  const textStr = String(text == null ? "" : text);
  const lines = textStr.split("\n");
  const paras = lines.map(function(line) {
    return new Paragraph({
      bidirectional: true,
      alignment: opts.align || (isHeader ? AlignmentType.CENTER : AlignmentType.RIGHT),
      spacing: { line: 300, after: 0 },
      children: [new TextRun({
        text: line,
        rightToLeft: true,
        size: opts.size || (isHeader ? SIZE_TABLE_HEAD : SIZE_TABLE),
        bold: isHeader || opts.bold || false,
        color: isHeader ? "FFFFFF" : COLOR_BLACK,
        font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
      })],
    });
  });
  return new TableCell({
    width: opts.width ? { size: opts.width, type: WidthType.PERCENTAGE } : undefined,
    shading: { type: ShadingType.CLEAR, fill: bgFill },
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    verticalAlign: VerticalAlign.CENTER,
    children: paras,
  });
}

// جدول بسيط: رؤوس + صفوف (RTL عبر visuallyRightToLeft)
function buildTable(headers, rows, colWidths) {
  const headerRow = new TableRow({
    tableHeader: true,
    cantSplit: true,
    children: headers.map((h, i) => tCell(h, { header: true, width: colWidths ? colWidths[i] : undefined })),
  });
  const dataRows = rows.map((row, idx) => new TableRow({
    cantSplit: true,
    children: row.map((c, i) => tCell(c, { alt: idx % 2 === 0, width: colWidths ? colWidths[i] : undefined })),
  }));
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    visuallyRightToLeft: true,  // ← يجعل الأعمدة تُقرأ من اليمين لليسار
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: COLOR_ACCENT },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR_ACCENT },
      left: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: "D0DDE8" },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: "D0DDE8" },
    },
    rows: [headerRow, ...dataRows],
  });
}

// ===== الرأس والتذييل =====

// ترويسة الصفحة (عنوان القسم + حد سفلي)
function buildHeader(title) {
  return new Header({
    children: [new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR_ACCENT } },
      children: [new TextRun({
        text: title,
        rightToLeft: true,
        size: SIZE_HEADER,
        color: COLOR_GREY,
        font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR },
      })],
    })],
  });
}

// تذييل الصفحة (رقم صفحة عربي RTL)
// ملاحظة: حقل PAGE ديناميكي؛ مع bidirectional+rightToLeft يعرض Word
// الرقم بالصيغة العربية تلقائياً عند ضبط الأرقام على "سياق" (الافتراضي)
function buildPageFooter() {
  return new Footer({
    children: [new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: "- ", rightToLeft: true, size: SIZE_FOOTER, color: COLOR_GREY, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } }),
        new TextRun({ children: [PageNumber.CURRENT], rightToLeft: true, size: SIZE_FOOTER, color: COLOR_GREY, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } }),
        new TextRun({ text: " -", rightToLeft: true, size: SIZE_FOOTER, color: COLOR_GREY, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } }),
      ],
    })],
  });
}

// ===== صفحة الغلاف =====
// عدّل هذه الدالة لتناسب مستندك
function buildCover() {
  const TITLE = "عنوان المستند الرئيسي";
  const SUBTITLE = "العنوان الفرعي";
  const DOC_LABEL = "نوع المستند";

  const infoRows = [
    ["الجهة", "【اسم الجهة】"],
    ["القسم", "【اسم القسم】"],
    ["الاسم", "【الاسم】"],
    ["التاريخ", "1447هـ - 2026م"],
  ];

  const infoTable = new Table({
    width: { size: 75, type: WidthType.PERCENTAGE },
    alignment: AlignmentType.CENTER,
    visuallyRightToLeft: true,
    borders: allNoBorders,
    rows: infoRows.map(([label, value]) => new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          width: { size: 35, type: WidthType.PERCENTAGE },
          borders: { top: NB, left: NB, right: NB, bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000" } },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { line: 320, after: 0 },
            children: [new TextRun({ text: label + " :", rightToLeft: true, size: SIZE_BODY, bold: true, color: COLOR_BLACK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } })],
          })],
        }),
        new TableCell({
          width: { size: 65, type: WidthType.PERCENTAGE },
          borders: { top: NB, left: NB, right: NB, bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000" } },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { line: 320, after: 0 },
            children: [new TextRun({ text: value, rightToLeft: true, size: SIZE_BODY, color: COLOR_BLACK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } })],
          })],
        }),
      ],
    })),
  });

  return [
    pGap(2000),
    new Paragraph({
      bidirectional: true, alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({ text: DOC_LABEL, rightToLeft: true, size: 32, bold: true, color: COLOR_ACCENT, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } })],
    }),
    pGap(600),
    new Paragraph({
      bidirectional: true, alignment: AlignmentType.CENTER, spacing: { line: 480, after: 200 },
      children: [new TextRun({ text: TITLE, rightToLeft: true, size: 44, bold: true, color: COLOR_BLACK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } })],
    }),
    new Paragraph({
      bidirectional: true, alignment: AlignmentType.CENTER, spacing: { after: 800 },
      children: [new TextRun({ text: SUBTITLE, rightToLeft: true, size: 30, color: COLOR_DARK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } })],
    }),
    pGap(600),
    infoTable,
  ];
}

// ===== الفهرس =====
function buildTOC() {
  return [
    new Paragraph({
      bidirectional: true, alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 360, line: 360 },
      children: [new TextRun({ text: "فهرس المحتويات", rightToLeft: true, size: SIZE_H1, bold: true, color: COLOR_BLACK, font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR } })],
    }),
    new TableOfContents("Table of Contents", {
      hyperlink: true,
      headingStyleRange: "1-3",
    }),
  ];
}

// ===== المحتوى =====
// استبدل هذا بالمحتوى الفعلي لمستندك
const bodyContent = [
  h1("المبحث الأول: المقدمة"),
  p("هذا نص تجريبي للمقدمة. استبدله بمحتوى مستندك الفعلي. يمكن استخدام الأرقام مثل 2026 و1432هـ وستُحوّل تلقائياً إلى ٢٠٢٦ و١٤٣٢هـ عبر سكريبت تحويل الأرقام."),
  h2("المطلب الأول: تمهيد"),
  p("نص المطلب الأول."),
  bullet("نقطة أولى في القائمة"),
  bullet("نقطة ثانية في القائمة"),
  numItem("عنصر مرقم أول", 1),
  numItem("عنصر مرقم ثانٍ", 2),
  h2("المطلب الثاني: جدول تجريبي"),
  tableCaption("الجدول 1: جدول تجريبي"),
  buildTable(
    ["العمود الأول", "العمود الثاني", "العمود الثالث"],
    [
      ["صف 1", "قيمة", "100"],
      ["صف 2", "قيمة", "200"],
      ["صف 3", "قيمة", "300"],
    ],
    [40, 30, 30]
  ),
];

// ===== بناء المستند =====
function buildDocument() {
  return new Document({
    styles: {
      default: {
        document: {
          run: { font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }, size: SIZE_BODY, color: COLOR_BLACK },
          paragraph: { spacing: { line: 360 } },
        },
        heading1: {
          run: { font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }, size: SIZE_H1, bold: true, color: COLOR_BLACK },
          paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 480, after: 280, line: 360 } },
        },
        heading2: {
          run: { font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }, size: SIZE_H2, bold: true, color: COLOR_BLACK },
          paragraph: { spacing: { before: 320, after: 180, line: 360 } },
        },
        heading3: {
          run: { font: { ascii: FONT_EN, hAnsi: FONT_EN, cs: FONT_AR }, size: SIZE_H3, bold: true, color: COLOR_DARK },
          paragraph: { spacing: { before: 240, after: 120, line: 360 } },
        },
      },
    },
    sections: [
      // القسم 1: الغلاف (بدون رأس/تذييل، بدون رقم صفحة)
      {
        properties: {
          page: {
            size: { width: 11906, height: 16838 }, // A4
            margin: { top: 0, bottom: 0, left: 0, right: 0 },
          },
        },
        children: buildCover(),
      },
      // القسم 2: فهرس المحتويات
      {
        properties: {
          type: SectionType.NEXT_PAGE,
          page: {
            size: { width: 11906, height: 16838 },
            margin: { top: 1440, bottom: 1440, left: 1701, right: 1417, header: 850, footer: 992 },
          },
        },
        headers: { default: buildHeader("فهرس المحتويات") },
        footers: { default: buildPageFooter() },
        children: buildTOC(),
      },
      // القسم 3: المتن
      {
        properties: {
          type: SectionType.NEXT_PAGE,
          page: {
            size: { width: 11906, height: 16838 },
            margin: { top: 1440, bottom: 1440, left: 1701, right: 1417, header: 850, footer: 992 },
          },
        },
        headers: { default: buildHeader("عنوان المستند") },
        footers: { default: buildPageFooter() },
        children: bodyContent,
      },
    ],
  });
}

// ===== التوليد =====
const OUTPUT_PATH = process.argv[2] || "./output.docx";

Packer.toBuffer(buildDocument()).then((buffer) => {
  fs.writeFileSync(OUTPUT_PATH, buffer);
  const stats = fs.statSync(OUTPUT_PATH);
  console.log("✓ تم إنشاء الملف: " + OUTPUT_PATH);
  console.log("✓ حجم الملف: " + (stats.size / 1024).toFixed(1) + " كيلوبايت");
}).catch((err) => {
  console.error("✗ خطأ:", err);
  process.exit(1);
});
