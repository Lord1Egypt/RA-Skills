#!/usr/bin/env node
// scrape_baomoi_v2.js — lấy title + URL từ Báo Mới, trả về JSON
const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
        ],
        timeout: 20000,
    });

    const page = await browser.newPage();
    await page.goto('https://baomoi.com', { timeout: 25000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(4000);

    const items = await page.evaluate(() => {
        let results = [];
        const seen = new Set();

        // Strategy 1: Standard headline selectors (no /c/ filter — these are already news links)
        let els = document.querySelectorAll('h3 a, h4 a, .story__title a, .item__title a, a.story__title');
        if (els.length === 0) {
            // Strategy 2: fallback to /c/ links
            els = document.querySelectorAll('a[href*="/c/"]');
        }

        for (const a of els) {
            const href = a.getAttribute('href') || '';
            const text = a.textContent.trim();

            // Resolve full URL
            let url = href;
            if (href.startsWith('/')) url = 'https://baomoi.com' + href;

            // Skip external links
            if (href.startsWith('http') && !href.includes('baomoi.com')) continue;
            // Skip ads/social links
            if (href.includes('google.com') || href.includes('facebook.com') || href.includes('twitter.com')) continue;

            if (text.length > 15 && text.length < 200 && !seen.has(text)) {
                seen.add(text);
                results.push({ text, url });
            }

            if (results.length >= 5) break;
        }

        // Strategy 3: if still nothing, get any links with /c/ from all links
        if (results.length === 0) {
            const allLinks = document.querySelectorAll('a[href]');
            for (const a of allLinks) {
                const href = a.getAttribute('href') || '';
                const text = a.textContent.trim();
                if (href.includes('/c/') && text.length > 20 && !seen.has(text)) {
                    let url = href.startsWith('/') ? 'https://baomoi.com' + href : href;
                    seen.add(text);
                    results.push({ text, url });
                }
                if (results.length >= 5) break;
            }
        }

        return results;
    });

    await browser.close();

    for (const item of items) {
        console.log(JSON.stringify(item));
    }

    if (items.length === 0) {
        process.exit(1);
    }
})().catch(e => {
    console.error('ERROR: ' + e.message);
    process.exit(1);
});
