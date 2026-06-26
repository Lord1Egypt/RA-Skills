// Test Westmetall for all metals LME inventory
// Confirmed: LME_Cu_cash gives copper stock data

const metals = [
  { field: 'LME_Cu_cash', name: 'copper' },
  { field: 'LME_Al_cash', name: 'aluminum' },
  { field: 'LME_Ni_cash', name: 'nickel' },
  { field: 'LME_Zn_cash', name: 'zinc' },
  { field: 'LME_Pb_cash', name: 'lead' },
  { field: 'LME_Sn_cash', name: 'tin' },
  { field: 'LME_Co_cash', name: 'cobalt' },
];

async function fetchWestmetall(field, name) {
  const url = `https://www.westmetall.com/en/markdaten.php?action=table&field=${field}`;
  try {
    const r = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.westmetall.com/en/markdaten.php',
      },
      signal: AbortSignal.timeout(10000)
    });
    
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const html = await r.text();
    
    // Check if page has stock column
    if (!html.includes('stock') && !html.includes('Stock')) {
      console.log(`${name}: no stock column`);
      return null;
    }
    
    // Parse first data row: looking for pattern
    // <td >16. March 2026</td><td >xxx</td><td >xxx</td><td class="last">311,600</td>
    const firstRowMatch = html.match(/<tbody>\s*<tr>\s*<td[^>]*>([^<]+)<\/td>((?:<td[^>]*>[^<]*<\/td>)*)<td[^>]*class="[^"]*last[^"]*"[^>]*>([^<]+)<\/td>/);
    if (firstRowMatch) {
      const date = firstRowMatch[1].trim();
      const stock = parseInt(firstRowMatch[3].replace(/[,\s]/g, ''), 10);
      console.log(`${name} (${field}): date=${date}, stock=${isNaN(stock) ? 'N/A' : stock + ' tonnes'}`);
      
      // Show the header to understand columns
      const headerMatch = html.match(/<thead>([\s\S]*?)<\/thead>/);
      if (headerMatch) {
        const headers = headerMatch[1].match(/<th[^>]*>([^<]+)<\/th>/g)?.map(h => h.replace(/<[^>]+>/g, '').trim());
        console.log(`  Headers:`, headers);
      }
      return { date, stock: isNaN(stock) ? null : stock };
    } else {
      // Try simpler pattern
      const lastTdMatch = html.match(/<td class="last">([^<]+)<\/td>/);
      if (lastTdMatch) {
        const stock = parseInt(lastTdMatch[1].replace(/[,\s]/g, ''), 10);
        console.log(`${name}: stock (simple)=${isNaN(stock) ? 'N/A' : stock}`);
      } else {
        console.log(`${name}: could not parse`, html.slice(html.indexOf('<tbody>'), html.indexOf('<tbody>') + 300));
      }
    }
    return null;
  } catch(e) {
    console.log(`${name} error:`, e.message);
    return null;
  }
}

for (const { field, name } of metals) {
  await fetchWestmetall(field, name);
}
console.log('Done');
