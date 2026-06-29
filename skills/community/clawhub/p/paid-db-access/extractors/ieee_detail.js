// ============================================================
// IEEE Xplore 详情页摘要提取脚本
// 用于 enrich_abstracts.py CDPDetailEnricher 自动注入
// 在论文详情页 (https://ieeexplore.ieee.org/document/<id>/) 执行
// ============================================================

(() => {
    // --- 标题 ---
    const titleEl = document.querySelector('h1.document-title, h1');
    const title = titleEl?.innerText?.trim() || '';

    // --- 摘要 —— 按优先级尝试选择器 ---
    const abstractSelectors = [
        'div.abstract-text-content',           // 摘要纯文本（通常在 div.abstract-desktop-div 内）
        'div.abstract-desktop-div div.abstract-text',  // 桌面版摘要区域
        'section.document-abstract',           // 移动版（包含 "Abstract:" 前面的标题）
        'div.abstract-text',                   // 回退
        'div.abstract-mobile-div',            // 纯移动版
        '[class*=abstract-text]',             // 最终回退
    ];

    let abstract = '';
    for (const sel of abstractSelectors) {
        const el = document.querySelector(sel);
        if (el) {
            const text = el.innerText.trim();
            if (text.length > 50) {
                abstract = text;
                break;
            }
        }
    }

    // 清理：去掉 "Abstract:" 前缀（如有）
    abstract = abstract.replace(/^Abstract:?\s*/i, '').trim();

    // --- 会议/期刊信息 ---
    const venueEl = document.querySelector('.stats-document-abstract-publishedIn, .u-pb-1.stats-document-abstract-publishedIn, [class*=publishedIn]');
    let venue = venueEl?.innerText?.trim() || '';
    venue = venue.replace(/^Published in:\s*/i, '').trim();

    // --- 日期 ---
    const dateEl = document.querySelector('.doc-abstract-confdate, [class*=confdate], [class*=dateadded]');
    let dateText = dateEl?.innerText?.trim() || '';
    const yearMatch = dateText.match(/\b(19|20)\d{2}\b/);
    const year = yearMatch ? yearMatch[0] : '';

    // --- DOI ---
    const doiEl = document.querySelector('.stats-document-abstract-doi, [class*=abstract-doi], a[href*=doi]');
    const doi = doiEl?.innerText?.trim()?.replace(/^DOI:\s*/i, '') ||
                doiEl?.href?.match(/(10\.\S+)/)?.[1] || '';

    // --- docId — 从当前页面 URL 提取，用于 Tier 2 匹配 ---
    const docIdMatch = window.location.href.match(/\/document\/(\d+)/);
    const docId = docIdMatch ? docIdMatch[1] : '';

    // --- 作者 ---
    const authorEls = document.querySelectorAll('.authors-accordion-container a[href*="author"], .authors-container a, [class*=authors] a');
    const authors = Array.from(authorEls)
        .map(a => a.innerText.trim())
        .filter(n => n && n.length < 60)
        .join('; ') || '';

    // --- 会议地点 ---
    const locationEl = document.querySelector('.doc-abstract-location, [class*=location]');
    const location = locationEl?.innerText?.trim()?.replace(/^Conference Location:\s*/i, '') || '';

    return {
        title,
        abstract,
        authors: authors || undefined,
        venue: venue || undefined,
        year: year || undefined,
        doi: doi || undefined,
        docId: docId || undefined,
        location: location || undefined,
    };
})()
