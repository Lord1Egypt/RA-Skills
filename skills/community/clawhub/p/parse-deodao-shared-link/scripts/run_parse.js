const { parsePage } = require('./parse.js');
const path = require('path');
const fs = require('fs');

/**
 * 完整处理流程：
 * 1. 解析得到链接，提取内容(A)
 * 2. 总结关键信息(B)
 * 3. 下载图片(C)
 * 4. 保存到 biji\0000\<title>.md
 */

const url = process.argv[2];
if (!url) {
  console.error('[ERROR] Please provide URL');
  process.exit(1);
}

const OUTPUT_BASE = 'D:/notes/biji/0000';

console.log('[INFO] Processing URL:', url);

parsePage(url, { saveImages: true }).then(async result => {
  if (!result.success) {
    console.error('[ERROR]', result.error);
    process.exit(1);
  }

  console.log('[OK] Content extracted, length:', result.content.length);
  console.log('[OK] Images found:', result.images.length);

  // 生成标题：YYYYMMDD+关键主题
  const today = new Date().toISOString().split('T')[0].replace(/-/g, '');
  
  // 提取标题中的关键主题（去掉书名号等）
  let keyTopic = result.title
    .replace(/《》/g, '')
    .replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '')
    .substring(0, 20);
  
  const mdFileName = `${today}_${keyTopic}.md`;
  const mdFilePath = path.join(OUTPUT_BASE, mdFileName);
  
  // 图片保存到 md 同一目录（不建子目录）
  const imgDir = path.dirname(mdFilePath);
  const baseName = path.basename(mdFilePath, '.md');
  
  // 保存图片（直接在该目录下，不建子目录）
  for (let i = 0; i < result.images.length; i++) {
    const img = result.images[i];
    // 图片文件名加序号
    const imgFileName = `${baseName}_image_${i + 1}${img.ext}`;
    const imgPath = path.join(imgDir, imgFileName);
    fs.writeFileSync(imgPath, img.buffer);
    // 替换 buffer 为相对路径
    result.images[i] = {
      url: img.url,
      localPath: imgPath.replace(OUTPUT_BASE, '.').replace(/\\/g, '/')
    };
    console.log('[OK] Saved image:', imgFileName);
  }

  // 生成 B（摘要）- 这里先用标题代替，实际由 AI 补充
  const summary = `## 中心思想\n\n**待补充...**`;

  // 组装完整内容
  const imagesList = result.images.length > 0
    ? '\n\n## C) 图片\n\n' + result.images.map((img, i) => `![image_${i + 1}](${path.basename(img.localPath)})`).join('\n')
    : '';

  const fullContent = `# ${result.title}

> 链接：${url}
> 处理时间：${new Date().toLocaleString('zh-CN')}

---

## 中心思想

（待AI总结补充...）

---

## 原文内容

${result.content}

${imagesList}

---

*由小虾自动解析整理*
`;

  fs.writeFileSync(mdFilePath, fullContent, 'utf8');
  console.log('[OK] Saved to:', mdFilePath);

  console.log('\n=== DONE ===');
  console.log('MD file:', mdFilePath);
  console.log('Images dir:', imgDir);

}).catch(err => {
  console.error('[ERROR]', err.message);
  process.exit(1);
});
