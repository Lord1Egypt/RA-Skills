// ============================================================
// Scopus 详情页摘要提取脚本
// ============================================================
// 用于: https://www.scopus.com/pages/publications/{scopus_id}
//       或 https://www.scopus.com/record/display.uri?eid={eid}
//
// 前提: 用户已通过机构 SSO 登录 Scopus（浏览器中可见）
// 提取: 完整摘要、作者+机构、期刊/会议、年份、DOI、引用数、关键词、OA 状态
//
// Usage: browser.navigate 到论文详情页，然后:
//        browser.act(kind="evaluate", fn=<this script>)
// ============================================================

(() => {
    const body = document.body.innerText;

    // --- Title ---
    const title = (document.querySelector('h2')?.innerText || '').trim();

    // --- Abstract (stable ID: #document-details-abstract) ---
    let abstract = '';
    const absDiv = document.querySelector('#document-details-abstract');
    if (absDiv) {
        abstract = absDiv.innerText.replace(/^Abstract\s*\n*/i, '').trim();
        // Remove "Author keywords" section if it bleeds in
        const kwIdx = abstract.indexOf('\nAuthor keywords');
        if (kwIdx > -1) abstract = abstract.substring(0, kwIdx).trim();
    }
    // Fallback: find h3 "Abstract" in tabpanel → next paragraph
    if (!abstract) {
        const tp = document.querySelector('[role="tabpanel"]');
        if (tp) {
            const h3s = tp.querySelectorAll('h3');
            for (const h3 of h3s) {
                if (h3.innerText.trim() === 'Abstract') {
                    const p = h3.closest('section, div')?.querySelector('p');
                    if (p && p.innerText.length > 50) {
                        abstract = p.innerText.trim();
                    }
                    break;
                }
            }
        }
    }

    // --- Authors (from body text, between DOI line and "Show all") ---
    let authors = '';
    const lines = body.split('\n').map(l => l.trim()).filter(Boolean);
    const doiLineIdx = lines.findIndex(l => l.startsWith('DOI:'));
    if (doiLineIdx > -1) {
        // Authors are after DOI, before affiliations start
        const afterDoi = lines.slice(doiLineIdx + 1);
        // Skip "Copy to clipboard" button text
        const startIdx = afterDoi.findIndex(l => l !== 'Copy to clipboard');
        if (startIdx > -1) {
            const showAllIdx = afterDoi.findIndex((l, i) => i > startIdx &&
                (l.startsWith('Show all') || l.match(/^\d[\d,]*\s/)));
            const endIdx = showAllIdx > -1 ? showAllIdx : afterDoi.length;
            const authorBlock = afterDoi.slice(startIdx, endIdx);
            // Filter out superscript letters, email links, affiliation lines (long text)
            authors = authorBlock
                .filter(l => l.length > 2 && l.length < 80 &&
                    !l.startsWith('Send mail') && !l.startsWith('View') &&
                    !l.match(/^[a-z],?\s*$/) && // superscript letters
                    !l.match(/^Department|^School|^College|^Institute|^Faculty|^Center|^Centre|^University|^Laboratory|^Division/))
                .join('; ');
        }
    }

    // --- Venue, Type, Year, OA (from meta line after title) ---
    let venue = '';
    let doctype = '';
    let year = '';
    let isOA = false;
    const titleIdx = lines.findIndex(l => l === title);
    if (titleIdx > -1 && titleIdx + 1 < lines.length) {
        const metaLine = lines[titleIdx + 1];
        // Pattern: "{Venue}{Type}Open Access{Year}" (concatenated without spaces!)
        // e.g. "Healthcare (Switzerland)ReviewOpen Access2023"
        // e.g. "Journal of Medical SystemsArticle2023"

        // Extract year (4 digits, last number in line)
        const yrMatch = metaLine.match(/(\d{4})(?!.*\d{4})/);
        if (yrMatch) year = yrMatch[1];

        // Extract Open Access
        if (metaLine.includes('Open Access')) {
            isOA = true;
        }

        // Extract type — try concatenated pattern first
        const typePatterns = [
            'Conference Paper', 'Conference Review', 'Book Chapter', 'Short Survey',
            'Article', 'Review', 'Note', 'Editorial', 'Letter', 'Erratum', 'Book', 'Retracted'
        ];
        for (const tp of typePatterns) {
            const idx = metaLine.indexOf(tp);
            if (idx > 0) {  // > 0 ensures it's not at position 0 (venue shouldn't be empty)
                doctype = tp;
                // Venue = everything before the type
                venue = metaLine.substring(0, idx).trim();
                break;
            }
        }
        // If no type found embedded in line, try regex
        if (!doctype) {
            const typeMatch = metaLine.match(/(Article|Review|Conference Paper|Book Chapter|Note|Editorial|Letter|Erratum|Short Survey|Conference Review|Book|Retracted)/i);
            if (typeMatch) doctype = typeMatch[1];
        }
        if (!venue) {
            venue = metaLine
                .replace(/Open Access/gi, '')
                .replace(/\d{4}/, '')
                .replace(/•/g, '')
                .trim();
        }
    }

    // --- DOI ---
    const doiMatch = body.match(/DOI:\s*(10\.[^\s\n]+)/);
    const doi = doiMatch ? doiMatch[1].trim() : '';

    // --- Citations ---
    let citations = 0;
    const citeMatch = body.match(/(\d[\d,]*)\s*(?:99th percentile\s*)?Citations?/);
    if (citeMatch) citations = parseInt(citeMatch[1].replace(/,/g, ''), 10);

    // --- Author keywords ---
    let keywords = '';
    const kwHeadingIdx = lines.findIndex(l => l === 'Author keywords');
    if (kwHeadingIdx > -1 && kwHeadingIdx + 1 < lines.length) {
        keywords = lines[kwHeadingIdx + 1];
    }

    // --- Scopus ID (from URL) ---
    const scopusIdMatch = window.location.href.match(/\/publications\/(\d+)/);
    const scopusId = scopusIdMatch ? scopusIdMatch[1] : '';

    // --- EID (from URL if available) ---
    const eidMatch = window.location.href.match(/eid=([^&]+)/);
    const eid = eidMatch ? decodeURIComponent(eidMatch[1]) : '';

    return {
        // 核心字段（enrich 匹配 + 评分需要）
        doi,
        title,
        abstract,
        authors,
        venue,
        year,
        citations,
        type: doctype,
    };
})()
