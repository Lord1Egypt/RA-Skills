// ============================================================
// 中国知网 (CNKI) 搜索结果提取脚本
// 已验证选择器: table.result-table-list (2026-06)
// ============================================================
(() => {
    const results = [];

    // 总结果数
    const countEl = document.querySelector('.pagerTitleCell, [class*=count]');
    const totalMatch = document.body?.innerText?.match(/共找到\s*([\d,]+)\s*条结果/);
    const totalResults = totalMatch ? totalMatch[1].replace(',', '') : '?';

    // 知网搜索结果表
    const table = document.querySelector('table.result-table-list');
    if (!table) {
        return { error: 'table.result-table-list not found', totalResults, count: 0, database: 'cnki', papers: [] };
    }

    const rows = table.querySelectorAll('tr');
    rows.forEach((row, idx) => {
        if (idx === 0) return; // 跳过表头
        const cells = row.querySelectorAll('td');
        if (cells.length < 6) return;

        const title = cells[1]?.innerText?.trim();
        if (!title || title === '题名' || title.length < 3) return;

        const authors = cells[2]?.innerText?.trim() || '';
        const source = cells[3]?.innerText?.trim() || '';
        const date = cells[4]?.innerText?.trim() || '';
        const database = cells[5]?.innerText?.trim() || '';
        const citations = cells[6]?.innerText?.trim() || '';
        const downloads = cells[7]?.innerText?.trim() || '';

        // 判断类型
        let type = 'Journal Article';
        if (database.includes('硕士') || database.includes('博士')) type = 'Dissertation';
        else if (database.includes('会议')) type = 'Conference Paper';
        else if (database.includes('报纸')) type = 'News';
        else if (database.includes('图书')) type = 'Book';
        else if (database.includes('专利')) type = 'Patent';
        else if (database.includes('期刊')) type = 'Journal Article';

        // 提取年份
        const yearMatch = date.match(/(\d{4})/);
        const year = yearMatch ? yearMatch[1] : '';

        results.push({
            title: title.substring(0, 200),
            authors,
            year,
            venue: source,
            date,
            type,
            database,
            citations,
            downloads
        });
    });

    return { totalResults, count: results.length, database: 'cnki', papers: results };
})()
