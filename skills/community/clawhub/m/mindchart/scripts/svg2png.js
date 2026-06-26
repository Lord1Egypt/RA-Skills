import sharp from 'sharp';
import opentype from 'opentype.js';
import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const svgPath = args[0] ? path.resolve(args[0]) : path.join(process.cwd(), 'input.svg');
const outputPath = args[1] ? path.resolve(args[1]) : path.join(process.cwd(), 'output.png');
const fontPath = path.join(process.cwd(), 'skills', 'mindchart', 'fonts', 'wqy-microhei.otf.txt');
const fontName = 'WenQuanYi Micro Hei';

const DPI = 300;

sharp.cache({ fonts: [fontPath] });

const font = opentype.loadSync(fontPath);

function measureTextWidth(text, fontSize) {
  const p = font.getPath(text, 0, 0, fontSize);
  const box = p.getBoundingBox();
  return box.x2 - box.x1;
}

let svgContent = fs.readFileSync(svgPath, 'utf8');
svgContent = svgContent.replace(/font-family="[^"]*PuHuiTi[^"]*"/g, `font-family="${fontName}"`);
svgContent = svgContent.replace(/#PuHuiTi/g, `#${fontName}`);

svgContent = svgContent.replace(/font-family="[^"]*SourceHanSansSC[^"]*"/g, `font-family="${fontName}"`);
svgContent = svgContent.replace(/#SourceHanSansSC/g, `#${fontName}`);

svgContent = svgContent.replace(/<\?xml-stylesheet[^?]*\?>/g, '');
svgContent = svgContent.replace(/url\(##/g, 'url(#');
svgContent = svgContent.replace(/id="#([^"]+)"/g, 'id="$1"');

function wrapText(text, maxWidth, fontSize, measureFn) {
  const lines = [];
  const paragraphs = text.split('\n');
  
  for (const paragraph of paragraphs) {
    if (paragraph.trim() === '') {
      lines.push('');
      continue;
    }
    
    let currentLine = '';
    const chars = paragraph.split('');
    
    for (const char of chars) {
      if (char === ' ') {
        if (currentLine.trim()) {
          currentLine += char;
        }
        continue;
      }
      
      const testLine = currentLine + char;
      const width = measureFn(testLine, fontSize);
      
      if (width > maxWidth && currentLine !== '') {
        lines.push(currentLine.trim());
        currentLine = char;
      } else {
        currentLine = testLine;
      }
    }
    
    if (currentLine.trim()) {
      lines.push(currentLine.trim());
    }
  }
  
  return lines;
}

// 先收集所有匹配，避免边匹配边替换导致位置偏移
const foreignObjectRegex = /<foreignObject([^>]*)>([\s\S]*?)<\/foreignObject>/g;
const matches = [];
let match;

while ((match = foreignObjectRegex.exec(svgContent)) !== null) {
  matches.push({
    fullMatch: match[0],
    attrs: match[1],
    foreignObjectContent: match[2],
    index: match.index
  });
}

// 从后往前替换，避免位置偏移
for (let i = matches.length - 1; i >= 0; i--) {
  const { fullMatch, attrs, foreignObjectContent } = matches[i];

  const xMatch = attrs.match(/x="([^"]*)"/);
  const yMatch = attrs.match(/y="([^"]*)"/);
  const widthMatch = attrs.match(/width="([^"]*)"/);

  const x = xMatch ? parseFloat(xMatch[1]) : 0;
  const y = yMatch ? parseFloat(yMatch[1]) : 0;
  const containerWidth = widthMatch ? parseFloat(widthMatch[1]) : 200;

  const spanStyleRegex = /<span[^>]*style="([^"]*)"[^>]*>([\s\S]*?)<\/span>/;
  const spanStyleMatch = foreignObjectContent.match(spanStyleRegex);
  let fontSize = 16;
  let fill = '#000000';
  let lineHeight = 1.4;
  let textAlign = 'center';
  let textContent = '';

  if (spanStyleMatch) {
    const style = spanStyleMatch[1];
    textContent = spanStyleMatch[2].replace(/<[^>]+>/g, '').trim();
    const fsMatch = style.match(/font-size:(\d+(?:\.\d+)?)px/);
    const colorMatch = style.match(/color:\s*([^;]+)/);
    const lhMatch = style.match(/line-height:\s*([^;]+)/);
    const alignMatch = style.match(/text-align:\s*([^;]+)/);
    if (fsMatch) fontSize = parseFloat(fsMatch[1]);
    if (colorMatch) fill = colorMatch[1].trim();
    if (lhMatch) lineHeight = parseFloat(lhMatch[1]);
    if (alignMatch) textAlign = alignMatch[1].trim();
  }

  const noWrap = attrs.match(/data-no-wrap="true"/);
  if (textContent) {
    const lines = noWrap ? [textContent] : wrapText(textContent, containerWidth, fontSize, measureTextWidth);
    const lineHeightPx = fontSize * lineHeight;
    const totalHeight = lines.length * lineHeightPx;
    let startY = y + (totalHeight > fontSize * lineHeight ? fontSize * 0.85 : fontSize * 0.85 + (fontSize * lineHeight - totalHeight) / 2);

    const pathElements = [];

    for (let j = 0; j < lines.length; j++) {
      const line = lines[j];
      let lineX = x;

      if (textAlign === 'center') {
        const lineWidth = measureTextWidth(line, fontSize);
        lineX = x + (containerWidth - lineWidth) / 2;
      } else if (textAlign === 'right') {
        const lineWidth = measureTextWidth(line, fontSize);
        lineX = x + containerWidth - lineWidth;
      }

      const lineY = startY + j * lineHeightPx;
      const path = font.getPath(line, lineX, lineY, fontSize, {
        align: 'left',
        features: {}
      });
      const pathData = path.toPathData(2);
      pathElements.push(`<path d="${pathData}" fill="${fill}" />`);
    }

    svgContent = svgContent.replace(fullMatch, pathElements.join(''));
  }
}

sharp(Buffer.from(svgContent), { limit: 0, density: DPI })
  .flatten({ background: { r: 255, g: 255, b: 255, alpha: 1 } })
  .png()
  .toFile(outputPath)
  .then(() => {
    console.log(`Converted to PNG at ${DPI} DPI: ${outputPath}`);
  })
  .catch(err => {
    console.error('Error:', err);
  });