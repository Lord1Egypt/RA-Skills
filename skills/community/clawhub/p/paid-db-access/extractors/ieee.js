// ============================================================
// IEEE Xplore 搜索结果提取脚本 v2
// 改进：去重 (by link)、翻页信息、摘要提取、作者清理
// 用法：browser.act(profile="chrome", kind="evaluate", fn=<本文件内容>)
// ============================================================

(() => {
    const seen = new Set();
    const results = [];

    // --- 结果总数 & 分页信息 ---
    const headingEl = document.querySelector('h1, [class*=results-header]');
    const headingText = headingEl?.innerText || '';
    const totalMatch = headingText.match(/Showing\s+\d+-\d+\s+of\s+([\d,]+)/);
    const pageMatch = headingText.match(/Showing\s+(\d+)-(\d+)\s+of/);
    const totalResults = totalMatch ? totalMatch[1].replace(',', '') : '?';
    const pageSize = pageMatch ? parseInt(pageMatch[2]) - parseInt(pageMatch[1]) + 1 : 0;
    const currentStart = pageMatch ? parseInt(pageMatch[1]) : 0;

    // 检测每页条数选择器
    const perPageEl = document.querySelector('[class*=items-per-page] select, select[class*=page]');
    const perPage = perPageEl?.value ? parseInt(perPageEl.value) : pageSize || 25;

    // --- 提取论文 —— 按优先级尝试选择器，取匹配最多的那个 ---
    const selectorGroups = [
        'xpl-result-item',                                    // IEEE 新版 (2025+)
        '.List-results-items > div[class*="result"]',          // 标准列表 item
        '.List-results-items > *',                             // 全列表回退
    ];

    let bestItems = [];
    for (const sel of selectorGroups) {
        const nodes = document.querySelectorAll(sel);
        // 选产生最多有效标题的那个选择器
        if (nodes.length > bestItems.length) bestItems = Array.from(nodes);
    }

    bestItems.forEach(item => {
        // 跳过非论文元素
        if (item.querySelector('[class*=ad], [class*=banner]')) return;

        // 标题 + 链接（主要去重 key）
        const titleEl = item.querySelector('h3 a, h2 a, [class*=title] a, a[class*=title]');
        const title = titleEl?.innerText?.trim() || '';
        if (!title || title.length < 5) return;

        const link = titleEl?.href || '';
        // 用 link 去重（同一论文可能出现在多个嵌套 wrapper 中）
        const dedupKey = link || title.toLowerCase();
        if (seen.has(dedupKey)) return;
        seen.add(dedupKey);

        // --- 作者 ---
        const authorsEl = item.querySelector('[class*=author], .authors, [class*=contributor]');
        let authors = authorsEl?.innerText?.trim() || '';
        // 清理分隔符：多个分号 → 单个，换行 → ;
        authors = authors.replace(/;;+/g, ';').replace(/;\s*;/g, ';').replace(/\s*\n\s*/g, '; ').replace(/;+/g, ';');

        // --- 描述/元数据区域 ---
        const descEl = item.querySelector('[class*=description], .description, [class*=meta]');
        const desc = descEl?.innerText?.trim() || '';

        // 年份
        const yearMatch = desc.match(/Year:\s*(\d{4})/);
        const year = yearMatch ? yearMatch[1] : '';

        // 类型
        let type = 'Unknown';
        if (desc.includes('Journal Article')) type = 'Journal Article';
        else if (desc.includes('Conference Paper')) type = 'Conference Paper';
        else if (desc.includes('Conference')) type = 'Conference Paper';
        else if (desc.includes('Magazine')) type = 'Magazine Article';
        else if (desc.includes('Early Access')) type = 'Early Access';
        else if (desc.includes('Book')) type = 'Book';
        else if (desc.includes('Standard')) type = 'Standard';

        // 期刊/会议名 —— 取描述的前几行中不含 Year/Cited 的最长行
        const descLines = desc.split('\n').filter(l => l.trim());
        const venueLine = descLines.find(l =>
            !l.startsWith('Year:') && !l.startsWith('Cited by:') &&
            !l.includes('Journal Article') && !l.includes('Conference Paper') &&
            l.trim().length > 3
        );
        const venue = venueLine?.trim() || '';

        // 引用数 — 主选择器 + 3 级回退
        let citations = '';
        // 主选择器
        const citeMatch = desc.match(/Cited by:\s*Papers\s*\((\d+)\)/);
        if (citeMatch) citations = citeMatch[1];
        // 回退 1: "Citations: N"
        if (!citations) {
            const cm2 = desc.match(/Citations?:\s*(\d+)/i);
            if (cm2) citations = cm2[1];
        }
        // 回退 2: 页面其他位置的引用计数
        if (!citations) {
            const bodyText = document.body.innerText;
            const cm3 = bodyText.match(/Cited by:\s*(\d+)/i);
            if (cm3) citations = cm3[1];
        }
        // 回退 3: 从结果项内的数字模式中提取
        if (!citations) {
            const allNums = item.innerText.match(/(?:cited|citations?|references?)\s*[:\s]*(\d+)/gi);
            if (allNums && allNums.length > 0) {
                const lastMatch = allNums[allNums.length - 1].match(/(\d+)/);
                if (lastMatch) citations = lastMatch[1];
            }
        }

        // ⛔ 摘要不入上下文 — 列表页不抓取 abstract。
        // 摘要由 enrich_abstracts.py 统一在文件侧补全。
        const abstractEl = item.querySelector('[class*=abstract], .abstract, [class*=snippet]');
        const hasAbstract = !!abstractEl;

        // docId — 从 /document/XXXXX/ 链接提取，IEEE DOI 末尾 = docId
        const docIdMatch = link.match(/\/document\/(\d+)\//);
        const docId = docIdMatch ? docIdMatch[1] : '';

        // DOI — 搜索列表页不可用（IEEE 不展示），由 enrich 详情页步骤补全
        const doi = '';

        // 开放获取
        const isOA = !!item.querySelector('[class*=open-access], [class*=oa], img[alt*=Open]');

        results.push({
            title,
            authors,
            year,
            venue,
            type,
            citations,
            doi,
            docId,
            link,
            isOA,
            hasAbstract
        });
    });

    return {
        totalResults,
        count: results.length,
        totalPages: totalResults !== '?' ? Math.ceil(parseInt(totalResults) / perPage) : '?',
        currentPage: currentStart > 0 ? Math.ceil(currentStart / perPage) : 1,
        perPage,
        database: 'ieee',
        papers: results
    };
})()
