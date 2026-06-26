// 快速 HTML 转 PDF 脚本
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function convert() {
  const inputHtml = process.argv[2];
  const outputPdf = inputHtml.replace('.html', '.pdf');
  
  if (!fs.existsSync(inputHtml)) {
    console.error(`❌ 文件不存在：${inputHtml}`);
    process.exit(1);
  }

  console.log(`📄 HTML → PDF`);
  console.log(`   输入：${path.basename(inputHtml)}`);
  console.log(`   输出：${path.basename(outputPdf)}`);

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    const absolutePath = path.resolve(inputHtml);
    await page.goto(`file://${absolutePath}`, { waitUntil: 'networkidle', timeout: 60000 });
    
    await page.pdf({
      path: outputPdf,
      format: 'A4',
      printBackground: true,
      margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
    });

    console.log(`✅ PDF 已生成：${path.basename(outputPdf)}`);
    console.log(`MEDIA: ${path.resolve(outputPdf)}`);
    
  } catch (error) {
    console.error(`❌ 错误：${error.message}`);
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

convert();
