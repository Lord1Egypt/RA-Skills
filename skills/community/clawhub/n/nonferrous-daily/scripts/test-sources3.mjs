// Deep investigation of promising sources

// 1. Westmetall - returns 200 with stock keywords
async function testWestmetallDeep() {
  try {
    const r = await fetch('https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash', {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': 'text/html,*/*', 'Accept-Language': 'en-US,en;q=0.9' },
      signal: AbortSignal.timeout(10000)
    });
    const html = await r.text();
    console.log('=== WESTMETALL full HTML length:', html.length);
    // Find all "stock" occurrences
    const lower = html.toLowerCase();
    let pos = 0;
    while ((pos = lower.indexOf('stock', pos)) !== -1) {
      console.log('  "stock" at', pos, ':', html.slice(Math.max(0, pos-50), pos+100));
      pos += 5;
    }
    // Find tonnage patterns
    const tonneMatches = html.match(/[\d,]+\s*(tonne|ton|mt)/gi);
    if (tonneMatches) console.log('  Tonne patterns:', tonneMatches.slice(0, 5));
    // Show first table or data block
    const tableIdx = html.indexOf('<table');
    if (tableIdx > -1) console.log('  First table:', html.slice(tableIdx, tableIdx + 500));
  } catch(e) { console.log('Westmetall deep err:', e.message); }
}

// 2. Jin10 datacenter LME inventory
async function testJin10Deep() {
  const urls = [
    'https://datacenter.jin10.com/reportType/dc_lme_inventory',
    'https://datacenter.jin10.com/reportType/dc_copper_inventory',
    'https://datacenter.jin10.com/v2/lme/inventory/latest',
    'https://datacenter.jin10.com/v3/lme/inventory',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Referer': 'https://datacenter.jin10.com/',
          'Accept': 'application/json, text/plain, */*',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'x-app-id': 'rU6QIu7JHe2gOUeR',
          'x-version': '1.0.0',
        },
        signal: AbortSignal.timeout(8000)
      });
      const ct = r.headers.get('content-type') || '';
      const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 500) : (await r.text()).slice(0, 500);
      console.log('Jin10 deep', url.split('/').pop(), ':', r.status, ct.slice(0,30), '|', body.slice(0, 300));
    } catch(e) { console.log('Jin10 deep err:', url.split('/').pop(), e.message); }
  }
}

// 3. 东方财富 - try correct report name for LME inventory
async function testEastmoneyInv() {
  // Try to discover actual report names by browsing the futures data center
  const urls = [
    'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_LME_INVENTORY&columns=ALL&pageSize=5',
    'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_FUTURES_LME_INVENTORY&columns=ALL&pageSize=5',
    'https://futurold.eastmoney.com/web/api/lme/inventory?page=1&pagesize=5',
    // Try futures page
    'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_FUTU_POSITIONS&columns=ALL&pageSize=5&sortColumns=DATE&sortTypes=-1',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/futures/', 'Accept': 'application/json' },
        signal: AbortSignal.timeout(8000)
      });
      const ct = r.headers.get('content-type') || '';
      const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 400) : (await r.text()).slice(0, 200);
      console.log('EM', url.split('reportName=')[1]?.split('&')[0] || url.split('/').pop(), ':', r.status, '|', body.slice(0, 250));
    } catch(e) { console.log('EM err:', e.message); }
  }
}

// 4. Try the actual LME warehouse stats page HTML for warehouse data scraping
async function testLmeHtml() {
  // The LME publishes CSV files too - maybe those aren't CF-protected
  const urls = [
    'https://www.lme.com/api/Graphs/LMEStockData',
    'https://api.lme.com/warehouse/stock',
    'https://www.lme.com/en-GB/Trading/Physical-market/Warehousing/LME-stocks',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Accept': '*/*',
          'Referer': 'https://www.lme.com/',
        },
        signal: AbortSignal.timeout(6000)
      });
      const ct = r.headers.get('content-type') || '';
      const cfRay = r.headers.get('cf-ray');
      console.log('LME', url.split('/').pop(), ':', r.status, ct.slice(0,30), cfRay ? '(CF)' : '');
      if (r.status === 200) {
        console.log('  Body:', (await r.text()).slice(0, 400));
      }
    } catch(e) { console.log('LME err:', url.split('/').pop(), e.message); }
  }
}

await Promise.all([testWestmetallDeep(), testJin10Deep(), testEastmoneyInv(), testLmeHtml()]);
console.log('Done');
