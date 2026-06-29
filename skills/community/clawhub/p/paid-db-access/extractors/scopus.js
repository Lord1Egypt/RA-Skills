// ============================================================
// Scopus 搜索结果提取脚本
// ============================================================
(() => {
    const seen = new Set();
    const results = [];

    const countEl = document.querySelector('[data-testid="results-count"], .results-count');
    const totalMatch = countEl?.innerText?.match(/([\d,]+)/);
    const totalResults = totalMatch ? totalMatch[1].replace(',', '') : '?';

    const selectorGroups = [
        '.search-result',
        '.document-item',
        '[class*=DocHorizon]',
        '[class*=result-item]'
    ];
    let bestItems = [];
    for (const sel of selectorGroups) {
        const nodes = document.querySelectorAll(sel);
        if (nodes.length > bestItems.length) bestItems = Array.from(nodes);
    }

    bestItems.forEach(item => {
        const titleEl = item.querySelector('.ddmDocTitle a, [class*=title] a, h3 a');
        const title = titleEl?.innerText?.trim() || '';
        if (!title || title.length < 10) return;

        const link = titleEl?.href || '';
        const dedupKey = link || title.toLowerCase();
        if (seen.has(dedupKey)) return;
        seen.add(dedupKey);

        const doi = link.match(/(10\.\S+)/)?.[1] || item.querySelector('[class*=doi]')?.innerText?.trim() || '';

        const authorsEl = item.querySelector('[class*=author], .ddmAuthorList');
        let authors = authorsEl?.innerText?.trim() || '';
        authors = authors.replace(/;;+/g, ';').replace(/\s*\n\s*/g, '; ').replace(/;+/g, ';');

        const sourceEl = item.querySelector('[class*=source], .ddmJournalTitle');
        const source = sourceEl?.innerText?.trim() || '';

        const yearEl = item.querySelector('[class*=year], .ddmPubYr');
        const year = yearEl?.innerText?.trim() || '';

        const typeEl = item.querySelector('[class*=doctype], .ddmDocType');
        const type = typeEl?.innerText?.trim() || 'Unknown';

        const citeEl = item.querySelector('[class*=citedby], .ddmCitationCount');
        const citations = citeEl?.innerText?.match(/(\d+)/)?.[1] || '';

        results.push({ title, authors, year, venue: source, type, citations, doi, link });
    });

    return { totalResults, count: results.length, database: 'scopus', papers: results };
})()
