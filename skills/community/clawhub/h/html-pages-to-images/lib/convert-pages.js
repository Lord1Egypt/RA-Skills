/**
 * 核心转换逻辑
 * 将 HTML 中的页面元素转换为图片
 */

import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { join, resolve } from 'path';
import { existsSync, mkdirSync } from 'fs';

/**
 * 转换页面为图片
 * @param {Object} options - 配置选项
 * @param {string} options.htmlFile - HTML 文件路径
 * @param {string} options.outputDir - 输出目录
 * @param {number} options.pageWidth - 页面宽度
 * @param {number} options.pageHeight - 页面高度
 * @param {string} options.selector - 页面元素选择器
 * @returns {Promise<Object>} 转换结果
 */
export async function convertPagesToImages(options = {}) {
  const {
    htmlFile,
    outputDir,
    pageWidth = 375,
    pageHeight = 667,
    selector = '.page'
  } = options;

  // 确保输出目录存在
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  let browser;
  const images = [];

  try {
    // 读取 HTML 文件
    if (!existsSync(htmlFile)) {
      throw new Error(`HTML 文件不存在: ${htmlFile}`);
    }

    const htmlContent = readFileSync(htmlFile, 'utf-8');
    
    // 启动浏览器
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 设置视口大小
    await page.setViewport({
      width: pageWidth,
      height: pageHeight,
      deviceScaleFactor: 2 // 2x 分辨率，获得更清晰的图片
    });
    
    // 加载 HTML 内容
    await page.setContent(htmlContent, {
      waitUntil: 'networkidle0'
    });
    
    // 等待字体和样式加载
    await page.evaluateHandle(() => document.fonts.ready);
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 获取所有页面元素
    const pageElements = await page.$$(selector);
    
    if (pageElements.length === 0) {
      throw new Error(`未找到匹配选择器 "${selector}" 的元素`);
    }

    console.log(`📄 找到 ${pageElements.length} 个页面元素\n`);
    
    // 为每个页面截图
    for (let i = 0; i < pageElements.length; i++) {
      const element = pageElements[i];
      
      // 获取页面标题或编号
      const pageInfo = await page.evaluate((el) => {
        const pageNumber = el.querySelector('.page-number')?.textContent?.trim() || '';
        const sectionTitle = el.querySelector('.section-title')?.textContent?.trim() || 
                           el.querySelector('.cover-title')?.textContent?.trim() ||
                           el.querySelector('.interaction-title')?.textContent?.trim() ||
                           '';
        return { pageNumber, sectionTitle };
      }, element);
      
      // 生成文件名 - 统一使用两位数格式
      let pageNum = pageInfo.pageNumber || String(i + 1);
      // 如果是纯数字，格式化为两位数
      if (/^\d+$/.test(pageNum)) {
        pageNum = String(parseInt(pageNum)).padStart(2, '0');
      }
      const fileName = `page-${pageNum}.png`;
      const filePath = join(outputDir, fileName);
      
      // 截图
      await element.screenshot({
        path: filePath,
        type: 'png',
        omitBackground: false
      });
      
      images.push(filePath);
      console.log(`✅ 已保存: ${fileName}${pageInfo.sectionTitle ? ` (${pageInfo.sectionTitle})` : ''}`);
    }
    
    return {
      images,
      count: images.length
    };
    
  } catch (error) {
    throw error;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}
