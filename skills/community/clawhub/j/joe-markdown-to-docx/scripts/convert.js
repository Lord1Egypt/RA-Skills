#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { 
  Document, 
  Packer, 
  Paragraph, 
  TextRun, 
  HeadingLevel, 
  AlignmentType,
  ImageRun,
  Table,
  TableRow,
  TableCell,
  WidthType,
  BorderStyle,
  VerticalAlign
} from 'docx';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import fetch from 'node-fetch';

/**
 * 将 Markdown 转换为 DOCX
 */
async function convertMarkdownToDocx(markdownText, outputPath, baseDir) {
  const processor = unified()
    .use(remarkParse)
    .use(remarkGfm);

  const ast = processor.parse(markdownText);
  const transformed = processor.runSync(ast);

  const docChildren = [];

  for (const node of transformed.children || []) {
    const converted = await convertNode(node, baseDir);
    if (converted) {
      if (Array.isArray(converted)) {
        docChildren.push(...converted);
      } else {
        docChildren.push(converted);
      }
    }
  }

  const doc = new Document({
    creator: 'Markdown to DOCX Skill',
    sections: [{
      properties: {
        page: {
          margin: {
            top: 1440,
            right: 1440,
            bottom: 1440,
            left: 1440
          }
        }
      },
      children: docChildren
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  
  console.log(`✅ DOCX 文件已生成: ${outputPath}`);
}

/**
 * 转换单个节点
 */
async function convertNode(node, baseDir) {
  switch (node.type) {
    case 'heading':
      return convertHeading(node);
    case 'paragraph':
      return await convertParagraph(node, baseDir);
    case 'code':
      return convertCodeBlock(node);
    case 'list':
      return convertList(node);
    case 'table':
      return await convertTable(node);
    case 'image':
      return await convertImage(node, baseDir);
    default:
      return null;
  }
}

/**
 * 转换标题
 */
function convertHeading(node) {
  const levels = {
    1: HeadingLevel.HEADING_1,
    2: HeadingLevel.HEADING_2,
    3: HeadingLevel.HEADING_3,
    4: HeadingLevel.HEADING_4,
    5: HeadingLevel.HEADING_5,
    6: HeadingLevel.HEADING_6,
  };

  const text = extractText(node);
  
  return new Paragraph({
    text,
    heading: levels[node.depth] || HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 120 }
  });
}

/**
 * 转换段落
 */
async function convertParagraph(node, baseDir) {
  const children = await convertInlineNodes(node.children || [], baseDir);
  
  return new Paragraph({
    children: children.length > 0 ? children : [new TextRun('')],
    spacing: { before: 0, after: 200 }
  });
}

/**
 * 转换代码块
 */
function convertCodeBlock(node) {
  const lines = (node.value || '').split('\n');
  const runs = [];
  
  lines.forEach((line, index) => {
    if (index > 0) {
      runs.push(new TextRun({ break: 1 }));
    }
    runs.push(new TextRun({
      text: line || ' ',
      font: 'Consolas',
      size: 20
    }));
  });

  return new Paragraph({
    children: runs,
    shading: { fill: 'F6F8FA' },
    spacing: { before: 200, after: 200 },
    border: {
      top: { color: 'E1E4E8', space: 1, style: BorderStyle.SINGLE, size: 6 },
      bottom: { color: 'E1E4E8', space: 1, style: BorderStyle.SINGLE, size: 6 },
      left: { color: 'E1E4E8', space: 1, style: BorderStyle.SINGLE, size: 6 },
      right: { color: 'E1E4E8', space: 1, style: BorderStyle.SINGLE, size: 6 }
    }
  });
}

/**
 * 转换列表
 */
function convertList(node) {
  const items = [];
  
  for (const item of node.children || []) {
    if (item.type === 'listItem') {
      const text = extractText(item);
      items.push(new Paragraph({
        text,
        bullet: { level: 0 },
        spacing: { before: 100, after: 100 }
      }));
    }
  }
  
  return items;
}

/**
 * 转换表格
 */
async function convertTable(node) {
  const rows = [];
  const tableRows = node.children || [];
  const alignments = node.align || [];

  for (let rowIndex = 0; rowIndex < tableRows.length; rowIndex++) {
    const row = tableRows[rowIndex];
    const isHeader = rowIndex === 0;
    const cells = [];

    for (let colIndex = 0; colIndex < (row.children || []).length; colIndex++) {
      const cell = row.children[colIndex];
      const text = extractText(cell);
      
      // 确定对齐方式
      let alignment = AlignmentType.LEFT;
      if (isHeader) {
        alignment = AlignmentType.CENTER;
      } else if (alignments[colIndex] === 'center') {
        alignment = AlignmentType.CENTER;
      } else if (alignments[colIndex] === 'right') {
        alignment = AlignmentType.RIGHT;
      }

      const cellParagraph = new Paragraph({
        children: [new TextRun({
          text,
          bold: isHeader,
          size: 20
        })],
        alignment,
        spacing: { before: 100, after: 100 }
      });

      cells.push(new TableCell({
        children: [cellParagraph],
        shading: isHeader ? { fill: 'E8E8E8' } : undefined,
        verticalAlign: VerticalAlign.CENTER,
        margins: {
          top: 100,
          bottom: 100,
          left: 100,
          right: 100
        }
      }));
    }

    rows.push(new TableRow({ children: cells }));
  }

  return new Table({
    rows,
    width: {
      size: 100,
      type: WidthType.PERCENTAGE
    },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      left: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      right: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' }
    }
  });
}

/**
 * 转换图片
 */
async function convertImage(node, baseDir) {
  try {
    const imageUrl = node.url;
    const altText = node.alt || 'Image';
    
    let imageBuffer;
    
    // 判断是本地文件还是网络 URL
    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
      // 网络图片
      const response = await fetch(imageUrl);
      const arrayBuffer = await response.arrayBuffer();
      imageBuffer = Buffer.from(arrayBuffer);
    } else if (imageUrl.startsWith('data:')) {
      // Data URL
      const base64Data = imageUrl.split(',')[1];
      imageBuffer = Buffer.from(base64Data, 'base64');
    } else {
      // 本地文件
      const imagePath = path.resolve(baseDir, imageUrl);
      if (!fs.existsSync(imagePath)) {
        console.warn(`⚠️  图片不存在: ${imagePath}`);
        return new Paragraph({
          children: [new TextRun({
            text: `[图片: ${altText}]`,
            italics: true,
            color: '999999'
          })],
          spacing: { before: 200, after: 200 }
        });
      }
      imageBuffer = fs.readFileSync(imagePath);
    }

    // 获取图片尺寸（简化版，固定宽度）
    const maxWidth = 600; // 最大宽度（像素）
    
    const imageRun = new ImageRun({
      data: imageBuffer,
      transformation: {
        width: maxWidth,
        height: maxWidth * 0.75 // 假设 4:3 比例
      }
    });

    return new Paragraph({
      children: [imageRun],
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 200 }
    });
  } catch (error) {
    console.error(`❌ 图片处理失败: ${node.url}`, error.message);
    return new Paragraph({
      children: [new TextRun({
        text: `[图片加载失败: ${node.alt || node.url}]`,
        italics: true,
        color: 'FF0000'
      })],
      spacing: { before: 200, after: 200 }
    });
  }
}

/**
 * 转换内联节点
 */
async function convertInlineNodes(nodes, baseDir) {
  const runs = [];
  
  for (const node of nodes) {
    if (node.type === 'text') {
      runs.push(new TextRun(node.value || ''));
    } else if (node.type === 'strong') {
      const text = extractText(node);
      runs.push(new TextRun({ text, bold: true }));
    } else if (node.type === 'emphasis') {
      const text = extractText(node);
      runs.push(new TextRun({ text, italics: true }));
    } else if (node.type === 'inlineCode') {
      runs.push(new TextRun({
        text: node.value || '',
        font: 'Consolas',
        size: 20,
        shading: { fill: 'F6F8FA' }
      }));
    } else if (node.type === 'link') {
      const text = extractText(node);
      runs.push(new TextRun({ 
        text, 
        color: '0563C1',
        underline: {}
      }));
    } else if (node.type === 'image') {
      // 内联图片（较少见，但支持）
      try {
        const imageElement = await convertImage(node, baseDir);
        if (imageElement && imageElement.root && imageElement.root[0]) {
          runs.push(imageElement.root[0]);
        }
      } catch (error) {
        runs.push(new TextRun({
          text: `[图片: ${node.alt || ''}]`,
          italics: true
        }));
      }
    }
  }
  
  return runs;
}

/**
 * 提取节点的纯文本
 */
function extractText(node) {
  if (node.type === 'text') {
    return node.value || '';
  }
  
  if (node.children) {
    return node.children.map(extractText).join('');
  }
  
  return '';
}

// 主程序
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('用法: node main.js <input.md> [output.docx]');
  console.log('');
  console.log('功能:');
  console.log('  ✅ 标题 (H1-H6)');
  console.log('  ✅ 段落、粗体、斜体、行内代码');
  console.log('  ✅ 代码块');
  console.log('  ✅ 列表');
  console.log('  ✅ 表格（支持对齐）');
  console.log('  ✅ 图片（本地/网络/Data URL）');
  process.exit(1);
}

const inputPath = args[0];
const outputPath = args[1] || inputPath.replace(/\.md$/i, '.docx');

if (!fs.existsSync(inputPath)) {
  console.error(`❌ 文件不存在: ${inputPath}`);
  process.exit(1);
}

const markdown = fs.readFileSync(inputPath, 'utf-8');
const baseDir = path.dirname(path.resolve(inputPath));

await convertMarkdownToDocx(markdown, outputPath, baseDir);
