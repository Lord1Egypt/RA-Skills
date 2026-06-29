// ============================================================
// Web of Science 搜索结果提取脚本
// ============================================================
(() => {
    const seen = new Set();
    const results = [];

    const countEl = document.querySelector('.results-count, [class*=brand]');
    const totalMatch = countEl?.innerText?.match(/([\d,]+)/);
    const totalResults = totalMatch ? totalMatch[1].replace(',', '') : '?';

    const selectorGroups = [
        '.search-results-item',
        '[class*=record]',
        '.app-records-list > *'
    ];
    let bestItems = [];
    for (const sel of selectorGroups) {
        const nodes = document.querySelectorAll(sel);
        if (nodes.length > bestItems.length) bestItems = Array.from(nodes);
    }

    bestItems.forEach(item => {
        const titleEl = item.querySelector('.title, [class*=title] a, h3 a');
        const title = titleEl?.innerText?.trim() || '';
        if (!title || title.length < 10) return;

        const link = titleEl?.href || '';
        const dedupKey = link || title.toLowerCase();
        if (seen.has(dedupKey)) return;
        seen.add(dedupKey);

        const authorsEl = item.querySelector('.author, [class*=author]');
        const authors = authorsEl?.innerText?.trim()?.replace(/\n/g, '; ') || '';

        const sourceEl = item.querySelector('.source, [class*=source], .journal');
        const source = sourceEl?.innerText?.trim() || '';

        const yearMatch = source.match(/(\d{4})/);
        const year = yearMatch ? yearMatch[1] : '';

        const doiEl = item.querySelector('a[href*=doi]');
        const doi = doiEl?.href?.match(/(10\.\S+)/)?.[1] || '';

        const citeEl = item.querySelector('.times-cited, [class*=citation]');
        const citations = citeEl?.innerText?.match(/(\d+)/)?.[1] || '';

        results.push({
            title, authors, year,
            venue: source,
            type: source.includes('Conference') ? 'Conference Paper' : 'Journal Article',
            citations, doi, link
        });
    });

    return { totalResults, count: results.length, database: 'wos', papers: results };
})()
