// ============================================================
// ACM Digital Library 下载链接提取器 v2 (REAL DOM verified)
// ============================================================
// Tested on: https://dl.acm.org/doi/10.1145/3779295
//
// 不自动下载——提取 PDF/eReader/XML/HTML 链接，返回 URL 让用户手动操作。
//
// ACM 下载链接格式：
//   PDF:      https://dl.acm.org/doi/pdf/10.1145/{doi}
//   eReader:  https://dl.acm.org/doi/epdf/10.1145/{doi}
//   HTML:     https://dl.acm.org/doi/fullHtml/10.1145/{doi}
//   XML:      https://dl.acm.org/doi/full-xml/10.1145/{doi}
//
// Usage:
//   1. browser.navigate to paper detail page
//   2. browser.act(kind="evaluate", fn=<this script>)
//   3. 脚本返回下载链接，AI 用 browser.navigate 打开让用户手动保存
// ============================================================

(() => {
    const links = [];

    // 在详情页搜索所有下载链接
    document.querySelectorAll('a[href*="/doi/"]').forEach(a => {
        const text = (a.innerText || '').trim();
        const href = a.href || '';

        // 只收集明确的下载/阅读链接
        if (text === 'PDF' || text === 'eReader' || text === 'View online with eReader') {
            links.push({ type: text.includes('eReader') ? 'eReader' : 'PDF', url: href });
        }
        if (text.includes('HTML') || text === 'View this article in HTML format') {
            links.push({ type: 'HTML', url: href });
        }
        if (text === 'XML') {
            links.push({ type: 'XML', url: href });
        }
    });

    // 去重
    const seen = new Set();
    const unique = links.filter(l => {
        const key = l.type + '|' + l.url;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    });

    // 如果没有找到任何链接，尝试构造
    const doi = window.location.href.match(/\b(10\.\d{4,}\/[^\s?#]+)/)?.[1];
    if (unique.length === 0 && doi) {
        unique.push({ type: 'PDF (constructed)', url: 'https://dl.acm.org/doi/pdf/' + doi });
    }

    // 标题
    const title = (document.querySelector('h1')?.innerText || document.title || '').trim();

    return {
        title: title.substring(0, 120),
        doi: doi || '',
        pageUrl: window.location.href,
        downloadLinks: unique,
        instruction: unique.length > 0
            ? `推荐: ${unique[0].url}`
            : '无下载链接。可能需要机构登录或订阅。',
    };
})()
