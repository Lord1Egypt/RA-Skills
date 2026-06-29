// Engineering Village (Compendex) Detail Page Extractor
// Use after navigating to a paper detail page (browser.act navigate to paper.link).
// Extracts full abstract, controlled terms, classification codes, and Scopus metrics.
//
// Usage: browser.act(kind="evaluate", fn=<this script>)

(() => {
    const text = document.body.innerText;

    // --- Title ---
    const titleMatch = text.match(/^([^\n]+)\n/);
    const title = titleMatch ? titleMatch[1].trim() : '';

    // --- Abstract (between "Abstract\nBack to ToC" markers) ---
    let abstract = '';
    const absStart = text.indexOf('\nAbstract\nBack to ToC\n');
    if (absStart > -1) {
        const afterLabel = text.substring(absStart + '\nAbstract\nBack to ToC\n'.length);
        // Abstract ends at the copyright line or next "Back to ToC"
        const absEnd = afterLabel.search(/\n(?:©|Indexing\n|Back to ToC\n)/);
        abstract = absEnd > -1 ? afterLabel.substring(0, absEnd).trim() : afterLabel.substring(0, 3000).trim();
    }

    // --- Authors ---
    const authSection = text.match(/Author affiliations:[\s\S]*?(?=Accession number)/);
    let authors = '';
    if (authSection) {
        const authText = text.substring(0, text.indexOf('Author affiliations:'));
        const lines = authText.split('\n');
        // Authors are lines between title/source and "Corresponding author" / "Author affiliations"
        const titleIdx = lines.findIndex(l => l.includes(title?.substring(0, 20) || 'NOMATCH'));
        let authorStart = titleIdx > -1 ? titleIdx + 3 : -1;
        const corrIdx = lines.findIndex(l => l.startsWith('Corresponding author'));
        const affIdx = lines.findIndex(l => l.startsWith('Author affiliations:'));
        const authorEnd = corrIdx > -1 ? corrIdx : affIdx > -1 ? affIdx : lines.length;
        if (authorStart > -1 && authorStart < authorEnd) {
            authors = lines.slice(authorStart, authorEnd)
                .filter(l => l.trim())
                .map(l => l.replace(/\[\d+\]/g, '').trim())
                .join('; ');
        }
    }

    // --- Source / Venue ---
    const sourceMatch = text.match(/^([^\n]+,\s*(?:Volume|v)\s*[^\n]+)$/m);
    const venue = sourceMatch ? sourceMatch[1].trim() : '';

    // --- Year ---
    const yearMatch = venue?.match(/(\d{4})/);
    const year = yearMatch ? yearMatch[1] : '';

    // --- DOI ---
    const doiMatch = text.match(/DOI\n(10\.[^\n]+)/);
    const doi = doiMatch ? doiMatch[1].trim() : '';

    // --- Document type ---
    const typeMatch = text.match(/Compendex(Conference article|Journal article|Preprint|Book chapter|Conference proceeding)[^\n]*/);
    const type = typeMatch ? typeMatch[1].trim() : '';

    // --- Scopus citations ---
    const scopusMatch = text.match(/Scopus\s*\n(\d+)/);
    const citations = scopusMatch ? parseInt(scopusMatch[1], 10) : 0;

    // --- Controlled terms ---
    let controlledTerms = [];
    const ctSection = text.match(/Controlled terms:[\s\S]*?(?=Uncontrolled terms:|Classification codes:|$)/);
    if (ctSection) {
        controlledTerms = ctSection[0]
            .replace('Controlled terms:', '')
            .split('\n')
            .map(l => l.trim())
            .filter(l => l && !l.startsWith('Back to ToC'));
    }

    // --- Uncontrolled terms ---
    let uncontrolledTerms = [];
    const utSection = text.match(/Uncontrolled terms:[\s\S]*?(?=Classification codes:|$)/);
    if (utSection) {
        uncontrolledTerms = utSection[0]
            .replace('Uncontrolled terms:', '')
            .split('\n')
            .map(l => l.trim())
            .filter(l => l && !l.startsWith('Back to ToC'));
    }

    // --- Classification codes ---
    let classCodes = [];
    const ccSection = text.match(/Classification codes:[\s\S]*?(?=Metrics|Conference Information|Funding|$)/);
    if (ccSection) {
        classCodes = ccSection[0]
            .replace('Classification codes:', '')
            .split('\n')
            .map(l => l.trim())
            .filter(l => l && !l.startsWith('Back to ToC'));
    }

    // --- Conference info (if applicable) ---
    let conference = '';
    const confMatch = text.match(/Conference name\n([^\n]+)[\s\S]*?Conference date\n([^\n]+)/);
    if (confMatch) {
        conference = `${confMatch[1].trim()} (${confMatch[2].trim()})`;
    }

    // --- ISSN / ISBN ---
    const issnMatch = text.match(/ISSN\n([^\n]+)/);
    const isbnMatch = text.match(/ISBN-13\n([^\n]+)/);
    const issn = issnMatch ? issnMatch[1].trim() : '';
    const isbn = isbnMatch ? isbnMatch[1].trim() : '';

    // --- Publisher ---
    const pubMatch = text.match(/Publisher\n([^\n]+)/);
    const publisher = pubMatch ? pubMatch[1].trim() : '';

    // --- docId (for matching back to search results) ---
    const docIdMatch = window.location.href.match(/docid=([^&]+)/);
    const docId = docIdMatch ? decodeURIComponent(docIdMatch[1]) : '';

    return {
        // 核心字段
        docId,
        doi,
        title,
        abstract,
        authors,
        venue,
        year,
        citations,
        type,
    };
})()
