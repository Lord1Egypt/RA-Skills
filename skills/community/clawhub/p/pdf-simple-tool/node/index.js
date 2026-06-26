import fs from "fs/promises";
import { PDFDocument } from "pdf-lib";
import pdfParse from "pdf-parse";
import {
  Document,
  Packer,
  Paragraph,
  TextRun
} from "docx";

/**
 * 拆分 PDF 指定页码范围
 * @param {string} inputPath
 * @param {string} outputPath
 * @param {number} fromPage 1-based
 * @param {number} toPage 1-based, inclusive
 */
export async function splitPdf(inputPath, outputPath, fromPage, toPage) {
  if (fromPage <= 0 || toPage <= 0) {
    throw new Error("from_page 和 to_page 必须 >= 1");
  }
  if (fromPage > toPage) {
    throw new Error("from_page 不能大于 to_page");
  }

  const inputExists = await fileExists(inputPath);
  if (!inputExists) {
    throw new Error(`输入文件不存在: ${inputPath}`);
  }

  const pdfBytes = await fs.readFile(inputPath);
  const srcDoc = await PDFDocument.load(pdfBytes);

  const totalPages = srcDoc.getPageCount();
  if (fromPage > totalPages) {
    throw new Error(
      `from_page 超过总页数: from_page=${fromPage}, total=${totalPages}`
    );
  }
  const clampedTo = Math.min(toPage, totalPages);

  const newDoc = await PDFDocument.create();
  const pagesToCopy = [];
  for (let i = fromPage - 1; i < clampedTo; i++) {
    pagesToCopy.push(i);
  }

  const copiedPages = await newDoc.copyPages(srcDoc, pagesToCopy);
  copiedPages.forEach((p) => newDoc.addPage(p));

  const newPdfBytes = await newDoc.save();
  await fs.writeFile(outputPath, newPdfBytes);
  return {
    ok: true,
    message: `Created ${outputPath} with pages ${fromPage}-${clampedTo}`
  };
}

/**
 * 简单版 PDF -> Word：把整本 PDF 的文本导出到一个 .docx
 * - 不保留复杂排版，只按行粗略分段
 */
export async function pdfToWord(inputPath, outputPath) {
  const inputExists = await fileExists(inputPath);
  if (!inputExists) {
    throw new Error(`输入文件不存在: ${inputPath}`);
  }

  const pdfBuffer = await fs.readFile(inputPath);
  const data = await pdfParse(pdfBuffer);
  const text = data.text || "";

  // 按行拆分，生成 docx 段落
  const lines = text.split(/\r?\n/);

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: lines.map((line) =>
          new Paragraph({
            children: [new TextRun(line)]
          })
        )
      }
    ]
  });

  const buffer = await Packer.toBuffer(doc);
  await fs.writeFile(outputPath, buffer);

  return {
    ok: true,
    message: `Created Word file: ${outputPath}`
  };
}

async function fileExists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

// 可选：命令行测试入口
if (process.argv[1] === new URL(import.meta.url).pathname) {
  // 用法示例：
  // node index.js split input.pdf output_3_5.pdf 3 5
  // node index.js docx input.pdf output.docx
  const [,, cmd, input, output, from, to] = process.argv;
  (async () => {
    try {
      if (cmd === "split") {
        const res = await splitPdf(input, output, Number(from), Number(to));
        console.log(res.message);
      } else if (cmd === "docx") {
        const res = await pdfToWord(input, output);
        console.log(res.message);
      } else {
        console.error("Usage:");
        console.error("  node index.js split <input.pdf> <output.pdf> <from> <to>");
        console.error("  node index.js docx <input.pdf> <output.docx>");
        process.exit(1);
      }
    } catch (e) {
      console.error("Error:", e.message);
      process.exit(1);
    }
  })();
}
