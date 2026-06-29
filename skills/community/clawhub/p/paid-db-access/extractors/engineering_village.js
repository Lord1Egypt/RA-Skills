// Engineering Village (Compendex) Extractor v2
// Browser Relay evaluate script — extracts paper metadata from search results page.
// Built-in dedup (by docId) + pagination info. 
//
// ** Abstract extraction: use detail page in a separate tab. **
// On detail page: document.querySelector('#abstractText').innerText
// Search result page abstracts are not visible without AJAX expansion.
//
// DOM: React/MUI SPA. Results in div.row.result-row, COinS metadata in span.Z3988[title].
// Pagination: JS-based (#next-page-top click). Auto-attach delay: 1-3s after navigation.

(() => {
    const seen = new Set();
    const results = [];

    const rows = document.querySelectorAll('.row.result-row');

    rows.forEach(row => {
        // Dedup by document ID (unique per record in Compendex)
        const docId = row.getAttribute('data-docid');
        if (!docId || seen.has(docId)) return;
        seen.add(docId);

        // --- Parse COinS metadata (span.Z3988[title]) ---
        const coins = row.querySelector('.Z3988');
        const coinsData = {};
        if (coins) {
            const titleAttr = coins.getAttribute('title') || '';
            titleAttr.split('&').forEach(pair => {
                const eq = pair.indexOf('=');
                if (eq > 0) {
                    const key = pair.substring(0, eq);
                    const val = pair.substring(eq + 1);
                    try {
                        coinsData[key] = decodeURIComponent(val.replace(/\+/g, ' '));
                    } catch (e) {
                        coinsData[key] = val;
                    }
                }
            });
        }

        // --- Title ---
        const titleEl = row.querySelector('.result-title a, .result-title');
        const title = (titleEl?.innerText || '').trim() || (coinsData['rft.atitle'] || '');

        // --- Detail page link ---
        const detailA = row.querySelector('.result-title a.combinedlink');
        const relLink = detailA?.getAttribute('href') || '';
        const fullLink = relLink ? 'https://www.engineeringvillage.com' + relLink : '';

        // --- Authors ---
        const authorEls = row.querySelectorAll('.authors a.authorSearchLink');
        const authors = Array.from(authorEls).map(a => a.innerText.trim()).join('; ');

        // --- Source / Venue ---
        const sourceEl = row.querySelector('.source-info');
        const venue = (sourceEl?.innerText || '').trim() || (coinsData['rft.jtitle'] || '');

        // --- Year ---
        const year = coinsData['rft.date'] || '';

        // --- DOI ---
        let doi = coinsData['rft_id'] || '';
        if (doi.startsWith('info:doi/')) doi = doi.replace('info:doi/', '');

        // --- Document type (from data-doctype attribute) ---
        const docTypeAttr = row.getAttribute('data-doctype') || '';
        let type = '';
        if (docTypeAttr.includes('Journal article')) type = 'Journal Article';
        else if (docTypeAttr.includes('Conference article')) type = 'Conference Paper';
        else if (docTypeAttr.includes('Preprint')) type = 'Preprint';
        else if (docTypeAttr.includes('Book chapter')) type = 'Book Chapter';
        else if (docTypeAttr.includes('Conference proceeding')) type = 'Conference Proceeding';
        else type = docTypeAttr.replace('ev:', '').replace(':cpx', '');

        // --- Citation count (from Scopus) ---
        const citationMatch = row.innerText.match(/Cited by in Scopus\s*\((\d+)\)/);
        const citations = citationMatch ? parseInt(citationMatch[1], 10) : 0;

        // --- Open Access ---
        const isOA = !!row.querySelector('.ev-open-acess-indicator');

        // ⛔ 摘要不入上下文 — 列表页不抓取 abstract。
        // EV 搜索列表页摘要不可见（需 AJAX 展开），
        // 摘要由 enrich_abstracts.py 统一在文件侧补全。
        const abstractEl = row.querySelector('.show-preview-content.in .abstract_content, .collapse.in .abstract_content');
        const hasAbstract = !!abstractEl;

        results.push({
            title,
            authors,
            year,
            venue,
            type,
            link: fullLink,
            doi,
            hasAbstract,
            citations,
            isOA,
            docId,
        });
    });

    // --- Pagination info ---
    const pageCountEl = document.querySelector('.page-count');
    const pageMatch = pageCountEl?.innerText?.match(/(\d+)\s*of\s*(\d+)/);
    const totalMatch = document.body.innerText.match(/(\d+)\s*records?\s*found/i);

    return {
        totalResults: totalMatch ? totalMatch[1] : '?',
        count: results.length,
        totalPages: pageMatch ? pageMatch[2] : '?',
        currentPage: pageMatch ? pageMatch[1] : '1',
        perPage: results.length,
        database: 'engineering_village',
        papers: results,
    };
})()
