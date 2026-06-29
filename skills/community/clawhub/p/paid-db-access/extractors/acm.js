// ============================================================
// ACM Digital Library 搜索结果提取脚本 v3 (REAL DOM verified)
// ============================================================
// Tested on: https://dl.acm.org/action/doSearch?AllField=AI&pageSize=5
// DOM: ACM DL 2023+ React SPA
//
// Extracts: title, authors, year, venue, type, citations, doi, link,
//           abstract snippet, isOA, PDF link
//
// Usage: browser.act(kind="evaluate", fn=<this script>)
// ============================================================

(() => {
    const seen = new Set();
    const results = [];

    // --- 结果总数 ---
    const bodyText = document.body.innerText;
    const totalMatch = bodyText.match(/of\s*([\d,]+)\s*Results?/i);
    const totalResults = totalMatch ? totalMatch[1].replace(/,/g, '') : '?';

    // --- 分页 ---
    const showingMatch = bodyText.match(/Showing\s+(\d+)\s*-\s*(\d+)/);
    const pageSize = showingMatch
        ? parseInt(showingMatch[2]) - parseInt(showingMatch[1]) + 1
        : 0;
    const currentStart = showingMatch ? parseInt(showingMatch[1]) : 0;

    // --- URL 参数检测翻页 ---
    const urlParams = new URLSearchParams(window.location.search);
    const startPage = parseInt(urlParams.get('startPage') || '0');
    const perPage = parseInt(urlParams.get('pageSize') || pageSize.toString());

    // --- 提取论文 ---
    const items = document.querySelectorAll('li.search__item');

    items.forEach(item => {
        // 标题 & 链接
        const titleEl = item.querySelector('.issue-item__title a');
        const title = (titleEl?.innerText || '').trim();
        if (!title || title.length < 10) return;

        const link = titleEl?.href || '';
        if (!link) return;

        const dedupKey = link;
        if (seen.has(dedupKey)) return;
        seen.add(dedupKey);

        // DOI
        const doiMatch = link.match(/\b(10\.\d{4,}\/[^\s?#]+)/);
        const doi = doiMatch ? doiMatch[1] : '';

        // 作者 (ul.rlist--inline.loa > li > a)
        const authorEls = item.querySelectorAll('ul[class*="loa"] a');
        let authors = '';
        if (authorEls.length > 0) {
            authors = Array.from(authorEls)
                .map(a => (a.innerText || '').trim())
                .filter(n => n && n.length < 50)
                .join('; ');
        }

        // 日期 (直接提取)
        const dateEl = item.querySelector('.bookPubDate');
        const dateText = (dateEl?.innerText || '').trim();
        // 从日期中提取年份
        let year = '';
        const yearMatch = dateText.match(/\b(19|20)\d{2}\b/);
        if (yearMatch) year = yearMatch[0];

        // Venue
        const venueEl = item.querySelector('.issue-item__detail');
        let venue = (venueEl?.innerText || '').trim();

        // 清理 venue：去掉 Article No., Pages, DOI URL 等后缀
        venue = venue
            .replace(/Article\s*No\.?:.*$/, '')
            .replace(/Pages\s*[\d–-]+.*$/, '')
            .replace(/https?:\/\/doi\.org\/\S+.*$/, '')
            .replace(/\s+$/, '')
            .trim();

        // 如果 venue 里没有年份，从 date 取
        if (!year) {
            const vy = venue.match(/\b(19|20)\d{2}\b/);
            if (vy) year = vy[0];
        }

        // 类型（标题+内容双重检测）
        let type = 'Unknown';
        const text = item.innerText || '';
        if (/research-?article/i.test(text)) type = 'Journal Article';
        else if (/conference-?paper|proceeding/i.test(text)) type = 'Conference Paper';
        else if (/review-?article/i.test(text)) type = 'Review';
        else if (/short-?paper/i.test(text)) type = 'Short Paper';
        else if (/book-?chapter/i.test(text)) type = 'Book Chapter';
        // 从 venue 推断
        else if (/proceed|conf|sympos/i.test(venue)) type = 'Conference Paper';
        else if (/journal|trans|magaz/i.test(venue)) type = 'Journal Article';
        // 🔧 修复：从标题关键词推断 survey/review
        const titleLower = title.toLowerCase();
        if (type === 'Unknown' || type === 'Journal Article') {
            if (/\bsurvey\b|\breview\b/i.test(titleLower) && title.length > 40) type = 'Review';
        }

        // 引用数 & 下载数 (footer: "N M" where N=citations, M=downloads)
        let citations = '';
        const metricsEl = item.querySelector('.metric-holder, .issue-item__footer-info');
        if (metricsEl) {
            const mText = (metricsEl.innerText || '').trim();
            // 格式："9 1,917" → citations=9, downloads=1917
            const parts = mText.split(/\s+/);
            if (parts.length >= 2 && /^\d[\d,]*$/.test(parts[0])) {
                citations = parts[0].replace(/,/g, '');
            } else {
                const numMatch = mText.match(/^(\d[\d,]*)/);
                if (numMatch) citations = numMatch[1].replace(/,/g, '');
            }
        }

        // 备选：从整个 item 文本找
        if (!citations) {
            const cm = text.match(/Cited\s+by\s+(\d[\d,]*)/i);
            if (cm) citations = cm[1].replace(/,/g, '');
        }

        // ⛔ 摘要不入上下文 — 列表页不抓取 abstract。
        // 摘要由 enrich_abstracts.py 统一在文件侧补全。
        // 仅记录是否有摘要 snippet 可用。
        const absEl = item.querySelector('.issue-item__abstract');
        const hasAbstract = !!absEl;

        // Open Access
        const isOA = !!item.querySelector('[class*=open-access], [class*=oa]');

        // PDF 链接
        const pdfEl = item.querySelector('a[href*="/doi/pdf/"]');
        const pdfUrl = pdfEl?.href || '';

        results.push({
            title,
            authors,
            year,
            venue,
            type,
            citations,
            doi,
            link,
            hasAbstract,
            isOA,
            pdfUrl,
        });
    });

    return {
        totalResults,
        count: results.length,
        totalPages: totalResults !== '?' && perPage > 0
            ? Math.ceil(parseInt(totalResults) / perPage)
            : '?',
        currentPage: startPage + 1,
        perPage: perPage || results.length,
        paginationParam: 'startPage',  // ACM uses startPage (0-indexed)
        database: 'acm',
        papers: results,
    };
})()
