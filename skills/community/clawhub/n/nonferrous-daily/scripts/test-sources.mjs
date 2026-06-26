// Test alternative LME inventory data sources

async function testShfe() {
  const urls = [
    'https://www.shfe.com.cn/data/dailydata/WarehouseReceipt20260317.dat',
    'https://www.shfe.com.cn/data/dailydata/wr/wr20260317.dat',
    'https://datacenter.shfe.com.cn/statement/datatype/WareHouseReceipt//otc',
  ];
  for (const url of urls) {
    try {
      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.shfe.com.cn/' },
        signal: AbortSignal.timeout(6000)
      });
      const body = (await r.text()).slice(0, 300);
      console.log('SHFE', url.split('/').pop().slice(0,40), ':', r.status, '|', body.slice(0,200));
    } catch(e) { console.log('SHFE err:', e.message); }
  }
}

async function testMacrotrends() {
  const r = await fetch('https://www.macrotrends.net/assets/php/fund_and_commodity_chart_data_download.php?t=HG00&type=price', {
    headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.macrotrends.net/' },
    signal: AbortSignal.timeout(8000)
  });
  console.log('macrotrends:', r.status, (await r.text()).slice(0, 300));
}

async function testSmmInv() {
  const slugs = ['copper-stocks', 'lme-stocks', 'warehouse', 'cu-stocks', 'shfe-warehouse'];
  for (const slug of slugs) {
    try {
      const r = await fetch('https://hq.smm.cn/h5/' + slug, {
        headers: { 'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'zh-CN,zh;q=0.9' },
        signal: AbortSignal.timeout(4000)
      });
      console.log('SMM slug', slug, ':', r.status);
    } catch(e) { console.log('SMM slug err', slug, ':', e.message); }
  }
}

// Try LME with more browser-like headers
async function testLmeDirect() {
  try {
    const r = await fetch('https://www.lme.com/api/Reports/WarehouseStockByMetalReportDownload?fileName=&isInternal=false', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.lme.com/Market-Data/Reports-and-data/Warehouse-Stock-Statistics',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
      },
      signal: AbortSignal.timeout(8000)
    });
    const ct = r.headers.get('content-type') || '';
    console.log('LME direct:', r.status, ct, r.headers.get('cf-ray') ? '(Cloudflare)' : '');
    if (r.status === 200) {
      const body = await r.text();
      console.log('LME body:', body.slice(0, 400));
    }
  } catch(e) { console.log('LME err:', e.message); }
}

// Test worldbank commodities
async function testWorldBank() {
  const r = await fetch('https://api.worldbank.org/v2/en/indicator/PCOPP.USD?downloadformat=json&mrv=5', {
    headers: { 'User-Agent': 'Mozilla/5.0' },
    signal: AbortSignal.timeout(8000)
  });
  const ct = r.headers.get('content-type') || '';
  const body = ct.includes('json') ? JSON.stringify(await r.json()).slice(0, 400) : (await r.text()).slice(0, 200);
  console.log('WorldBank copper:', r.status, body.slice(0, 300));
}

await Promise.all([testShfe(), testMacrotrends(), testSmmInv(), testLmeDirect(), testWorldBank()]);
console.log('Done');
