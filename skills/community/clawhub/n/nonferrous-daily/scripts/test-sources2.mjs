// Test Chinese financial data aggregators for LME inventory

// 1. 金十数据 (jin10.com) - often has LME inventory
async function testJin10() {
  const urls = [
    'https://rong360.jin10.com/api/flash_newest?category=0&channel=-1&vip=0',
    'https://flash-api.jin10.com/get_flash_by_category?category=15&count=20&vip=0',
    'https://datacenter.jin10.com/reportType/dc_lme_inventory',
    'https://datacenter.jin10.com/reportType/dc_copper_inventory',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': 'application/json', 'Referer': 'https://www.jin10.com/' },
        signal: AbortSignal.timeout(6000)
      });
      const ct = r.headers.get('content-type') || '';
      const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 400) : (await r.text()).slice(0, 200);
      console.log('Jin10', url.split('/').pop(), ':', r.status, '|', body.slice(0, 200));
    } catch(e) { console.log('Jin10 err', url.split('/').pop(), ':', e.message); }
  }
}

// 2. 东方财富 (eastmoney.com) - comprehensive financial data
async function testEastmoney() {
  const urls = [
    'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_FUTU_LME_INVENTORY&columns=ALL&pageSize=10&sortColumns=UPDATE_DATE&sortTypes=-1',
    'https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_FUTU_METAL_INVENTORY&columns=ALL&pageSize=10',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com/', 'Accept': 'application/json' },
        signal: AbortSignal.timeout(8000)
      });
      const ct = r.headers.get('content-type') || '';
      const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 500) : (await r.text()).slice(0, 200);
      console.log('Eastmoney', url.split('reportName=')[1]?.split('&')[0] || url.split('/').pop(), ':', r.status, '|', body.slice(0, 300));
    } catch(e) { console.log('Eastmoney err:', e.message); }
  }
}

// 3. 同花顺 iFinD
async function testThs() {
  const urls = [
    'https://d.10jqka.com.cn/v2/future/hs_lme_inventory/block/json',
    'https://data.10jqka.com.cn/futures/lme_inventory/',
    'https://d.10jqka.com.cn/v2/report/hs_lme_copper/json',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.10jqka.com.cn/' },
        signal: AbortSignal.timeout(6000)
      });
      const ct = r.headers.get('content-type') || '';
      const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 300) : (await r.text()).slice(0, 200);
      console.log('THS', url.split('/').pop(), ':', r.status, '|', body.slice(0, 200));
    } catch(e) { console.log('THS err', url.split('/').pop(), ':', e.message); }
  }
}

// 4. CME Group COMEX copper inventory
async function testCme() {
  const urls = [
    'https://www.cmegroup.com/CmeWS/mvc/Settlements/futures/options/tradeDate/20260314/productCode/HG/type/ALL/code/ALL',
    'https://www.cmegroup.com/CmeWS/mvc/Volume/getCombinedVolumeDownloadDetails/tradeDate/20260314/asset/copper.csv',
    'https://www.cmegroup.com/CmeWS/mvc/Warehouse/getCopperWarehouseStocks.json',
    'https://www.cmegroup.com/market-data/reports/warehouse-stock-reports.html',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': '*/*' },
        signal: AbortSignal.timeout(6000)
      });
      const ct = r.headers.get('content-type') || '';
      const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 300) : (await r.text()).slice(0, 200);
      console.log('CME', url.split('/').pop(), ':', r.status, '|', body.slice(0, 150));
    } catch(e) { console.log('CME err', url.split('/').pop(), ':', e.message); }
  }
}

// 5. Try westmetall.com (German metals data site)
async function testWestmetall() {
  try {
    const r = await fetch('https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash', {
      headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html' },
      signal: AbortSignal.timeout(8000)
    });
    const html = await r.text();
    // Look for inventory/stock keywords
    const hasStock = html.toLowerCase().includes('stock') || html.toLowerCase().includes('inventory') || html.toLowerCase().includes('tonne');
    console.log('Westmetall:', r.status, 'hasStock:', hasStock, html.slice(0, 200));
  } catch(e) { console.log('Westmetall err:', e.message); }
}

await Promise.all([testJin10(), testEastmoney(), testThs(), testCme(), testWestmetall()]);
console.log('Done');
