const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

/**
 * 通用网页解析器 - 得到笔记/分享链接
 */
async function parsePage(url, options = {}) {
  const {
    saveImages = true,
    minImageSize = 50 * 1024,  // 最小50KB才保存
    contentSelectors = [
      '.article-content',
      '.content',
      '.packet-content',
      '.detail-body',
      '.rich-text',
      'article',
      '.article'
    ]
  } = options;

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
  });

  const result = {
    success: false,
    title: '',
    content: '',      // A: 原文
    summary: '',      // B: 摘要
    images: [],      // C: 图片路径列表
    error: null
  };

  try {
    await page.goto(url, { timeout: 60000, waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);

    // 1. 提取标题
    const titleSelectors = ['h1', '.title', '.article-title', '[class*="title"]', 'title'];
    for (const sel of titleSelectors) {
      try {
        const t = await page.locator(sel).first().textContent({ timeout: 2000 });
        if (t && t.trim().length > 0 && t.trim().length < 200) {
          result.title = t.trim();
          break;
        }
      } catch (e) {}
    }

    // 2. 提取正文内容 (A)
    let content = '';
    for (const sel of contentSelectors) {
      try {
        const text = await page.locator(sel).first().textContent({ timeout: 3000 });
        if (text && text.trim().length > 50) {
          content = text;
          break;
        }
      } catch (e) {}
    }

    if (!content) {
      content = await page.locator('body').textContent();
    }

    result.content = content
      .replace(/\n\s*\n/g, '\n')
      .replace(/\s+/g, ' ')
      .trim();

    // 3. 下载图片 (C)
    if (saveImages) {
      const imgUrls = await page.evaluate(() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs.map(img => img.dataset.src || img.dataset.lazySrc || img.src || '')
          .filter(src => src && src.startsWith('http') && !src.includes('track') && !src.includes('pixel'));
      });

      for (const imgUrl of imgUrls) {
        try {
          const imgResponse = await page.goto(imgUrl, { timeout: 30000, waitUntil: 'domcontentloaded' });
          
          if (imgResponse && imgResponse.ok()) {
            const buffer = await imgResponse.body();
            
            // 跳过太小的图片
            if (buffer.length < minImageSize) continue;
            
            let ext = '.jpg';
            if (imgUrl.includes('.png')) ext = '.png';
            else if (imgUrl.includes('.gif')) ext = '.gif';
            else if (imgUrl.includes('.webp')) ext = '.webp';
            
            result.images.push({ url: imgUrl, buffer, ext });
          }
        } catch (imgErr) {
          // 单张失败不影响
        }
      }
    }

    result.success = true;

  } catch (err) {
    result.error = err.message;
  } finally {
    await browser.close();
  }

  return result;
}

module.exports = { parsePage };
