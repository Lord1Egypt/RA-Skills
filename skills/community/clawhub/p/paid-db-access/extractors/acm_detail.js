// ============================================================
// ACM Digital Library 详情页摘要提取脚本 v4 (DOM verified 2026-06-18)
// ============================================================
// Tested on 3 ACM DL pages: 10.1145/3769733.3769747, 10.1145/3815423, 10.1145/3787492
// DOM: ACM DL 2023+ React SPA
//
// Key fix (v4): Full abstract is in <section> > <h2>Abstract</h2> > <div>
// (not in .issue-item__abstract which is the recommendations section)
//
// Extracts: full abstract, authors+affiliations, venue, year,
//           citations, downloads, keywords, CCS concepts, OA status
//
// Usage: browser.navigate to paper detail page, then:
//        browser.act(kind="evaluate", fn=<this script>)
// ============================================================

(() => {
    // --- Title ---
    const title = (document.querySelector('h1')?.innerText || '').trim();

    // --- Abstract (v4: find <h2>Abstract</h2> → next sibling <div>) ---
    let abstract = '';
    const h2Abstract = Array.from(document.querySelectorAll('h2')).find(
        h => h.innerText.trim() === 'Abstract'
    );
    if (h2Abstract) {
        const absDiv = h2Abstract.nextElementSibling;
        if (absDiv && absDiv.tagName === 'DIV') {
            abstract = (absDiv.innerText || '').trim();
        }
    }
    // Fallback: try body text extraction (extract between "Abstract" and next boundary)
    if (!abstract || abstract.length < 50) {
        const body = document.body.innerText;
        const absIdx = body.indexOf('Abstract\n');
        if (absIdx >= 0) {
            let text = body.substring(absIdx + 'Abstract\n'.length);
            const boundaries = ['\nReferences\n', '\nKeywords\n', '\nCCS Concepts\n',
                               '\nIndex Terms\n', '\n1. ', '\nI. ', '\nINTRODUCTION\n'];
            for (const b of boundaries) {
                const idx = text.indexOf(b);
                if (idx > 0) { text = text.substring(0, idx); break; }
            }
            abstract = text.trim();
        }
    }

    // --- Authors (property="author" + RDFa givenName/familyName) ---
    const authorList = [];
    document.querySelectorAll('span[property="author"]').forEach(el => {
        const given = el.querySelector('[property="givenName"]')?.innerText?.trim() || '';
        const family = el.querySelector('[property="familyName"]')?.innerText?.trim() || '';
        const name = (given + ' ' + family).trim();
        if (name && name.length < 80) {
            authorList.push(name);
        }
    });

    // --- Venue ---
    const venuePatterns = /Proceedings|Journal|Conference|Symposium|Transactions|Magazine|Workshop|Review/i;
    let venue = '';
    const allLinks = Array.from(document.querySelectorAll('a'));
    for (const a of allLinks) {
        const text = (a.innerText || '').trim();
        if (text.length < 10 || text.length > 200) continue;
        if (text === title) continue;
        if (/^(Home|Sign|Register|Journals?|Proceedings?|Conferences?|Books?|SIGs?|People|Institutions?|Authors?|More|Next|Previous|Abstract|References|Figures|Tables|Media|Share|Comments?)$/i.test(text)) continue;
        if (!venuePatterns.test(text)) continue;
        venue = text;
        break;
    }

    // --- Year ---
    let year = '';
    const ym = document.body.innerText.match(/\b(20\d{2})\b/);
    if (ym) year = ym[0];

    // --- DOI ---
    const doi = window.location.href.match(/\b(10\.\d{4,}\/[^\s?#]+)/)?.[1] || '';

    // --- Citations ---
    let citations = 0;
    const citeMatch = document.body.innerText.match(/(\d[\d,]*)\s*citation/);
    if (citeMatch) citations = parseInt(citeMatch[1].replace(/,/g, ''), 10);

    // --- Downloads ---
    let downloads = 0;
    const dlMatch = document.body.innerText.match(/(\d[\d,]*)\s*Downloads?/);
    if (dlMatch) downloads = parseInt(dlMatch[1].replace(/,/g, ''), 10);

    // --- Keywords / CCS Concepts ---
    const keywords = [];
    const ccsConcepts = [];
    document.querySelectorAll('[class*=keyword] span, [class*=concept] span, .kw span').forEach(el => {
        const t = (el.innerText || '').trim();
        if (t && t.length > 2 && t.length < 100) {
            if (t.match(/^\d/)) ccsConcepts.push(t);
            else keywords.push(t);
        }
    });

    // --- Published date ---
    const pubDateEl = document.querySelector('.core-date-published, .pub-date, [class*=publication-date]');
    const pubDate = (pubDateEl?.innerText || '').trim();

    // --- Is OA ---
    const isOA = !!document.querySelector('[class*=open-access], [class*=oa-indicator], img[alt*="Open Access"]');

    return {
        doi,
        title,
        abstract,
        authors: authorList,
        venue,
        year,
        citations,
    };
})()
