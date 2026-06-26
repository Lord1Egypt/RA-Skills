#!/usr/bin/env node

/**
 * Maccabi Pharmacy Stock Check
 *
 * Search medications and check real-time stock availability at Maccabi Pharm.
 * NO AUTHENTICATION REQUIRED!
 *
 * Usage:
 *   node pharmacy-search.js search acamol       # Search for medications
 *   node pharmacy-search.js stock 32833         # Check stock for Vyvanse 30mg
 *   node pharmacy-search.js stock 113 5000      # Check stock for Acamol in Tel Aviv
 *   node pharmacy-search.js branches maccabi    # List Maccabi branches
 */

import https from 'https';
import { URL } from 'url';

// Helper function for HTTPS requests
async function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const requestOptions = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://serguide.maccabi4u.co.il/heb/pharmacy/',
        ...options.headers
      }
    };

    const req = https.request(requestOptions, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (data.startsWith('<!DOCTYPE') || data.startsWith('<html')) {
          resolve({ error: 'HTML_RESPONSE', message: 'Received HTML instead of JSON.' });
          return;
        }

        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ error: 'INVALID_JSON', message: 'Invalid JSON response', raw: data.substring(0, 200) });
        }
      });
    });

    req.on('error', (err) => reject({ error: 'NETWORK_ERROR', message: err.message }));

    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    req.end();
  });
}

// Maccabi API adapter
class MaccabiAdapter {
  constructor() {
    this.baseUrl = 'https://serguide.maccabi4u.co.il';
  }

  async searchDrug(query) {
    try {
      const catalogUrl = `${this.baseUrl}/Api/api/mac_pharmacy/v1/medications/catalog?largo=&name=${encodeURIComponent(query)}&category=&item_state=`;
      const response = await makeRequest(catalogUrl);

      if (response.error) {
        console.error('Search error:', response.message);
        return [];
      }

      if (!response.results || !Array.isArray(response.results)) return [];

      return response.results.map(m => ({
        id: m.largo_code.toString(),
        name: m.name,
        nameWithCode: m.medicine_name,
        category: m.category,
        prescriptionRequired: m.prescription_drug === 1,
        largoCode: m.largo_code
      }));
    } catch (error) {
      console.error('Search error:', error.message);
      return [];
    }
  }

  async getBranches(cityCode = '5000') {
    try {
      const response = await makeRequest(`${this.baseUrl}/webapi/api/SearchPage/GetSearchPageSearch/`, {
        method: 'POST',
        body: {
          City: cityCode,
          ChapterId: '006',
          InitiatorCode: '001',
          isKosher: 0,
          IsMobileApplication: 0,
          PageNumber: 1
        }
      });

      if (response.error) return [];
      if (!response.Items || !Array.isArray(response.Items)) return [];

      return response.Items.map(item => ({
        id: item.CITY_CODE || '',
        name: item.SERVICE_NAME || item.CITY_NAME || '',
        city: item.CITY_NAME || '',
        address: `${item.STREET_NAME || ''} ${item.HOUSE_NUMBER || ''}`.trim(),
        coordinates: {
          lat: parseFloat(item.COORDINATEY),
          lng: parseFloat(item.COORDINATEX)
        },
        distance: item.DIST_FROM_XY,
        phone: item.MOBPHONENUMBER || '',
        positionId: item.PositionId
      }));
    } catch (error) {
      console.error('Branches error:', error.message);
      return [];
    }
  }

  /**
   * Check stock at Maccabi pharmacies - NO AUTHENTICATION REQUIRED!
   *
   * @param {string|number} largoCode - The drug's largo code (e.g., 32833 for Vyvanse 30mg)
   * @param {string} cityCode - City code (default: 5000 for Tel Aviv)
   * @returns {object} Stock results with pharmacies that have the drug
   */
  async checkStock(largoCode, cityCode = '5000') {
    try {
      // First get drug info
      const catalogUrl = `${this.baseUrl}/Api/api/mac_pharmacy/v1/medications/catalog?largo=${largoCode}&name=&category=&item_state=`;
      const drugInfo = await makeRequest(catalogUrl);

      let drugName = 'Unknown';
      let prescriptionRequired = false;
      if (drugInfo.results && drugInfo.results[0]) {
        drugName = drugInfo.results[0].name;
        prescriptionRequired = drugInfo.results[0].prescription_drug === 1;
      }

      // Make the stock check request with 'largo' parameter
      const response = await makeRequest(`${this.baseUrl}/webapi/api/SearchPage/GetSearchPageSearch/`, {
        method: 'POST',
        body: {
          City: cityCode,
          ChapterId: '006',
          InitiatorCode: '001',
          isKosher: 0,
          IsMobileApplication: 0,
          PageNumber: 1,
          largo: String(largoCode)
        }
      });

      if (response.error) {
        return { error: response.error, message: response.message, results: [] };
      }

      if (!response.Items || !Array.isArray(response.Items)) {
        return { error: 'NO_RESULTS', message: 'No pharmacies found', results: [] };
      }

      // Process results
      const allPharmacies = response.Items.map(item => ({
        name: item.SERVICE_NAME || item.CITY_NAME,
        address: `${item.STREET_NAME || ''} ${item.HOUSE_NUMBER || ''}`.trim(),
        city: item.CITY_NAME,
        distance: item.DIST_FROM_XY,
        phone: item.MOBPHONENUMBER || '',
        coordinates: {
          lat: parseFloat(item.COORDINATEY),
          lng: parseFloat(item.COORDINATEX)
        },
        drugsInStock: item.DRUGS_IN_STOCK || [],
        drugsFewInStock: item.DRUGS_FEW_IN_STOCK || [],
        drugsNotInStock: item.DRUGS_NOT_IN_STOCK || [],
        drugsTotalCount: item.DRUGS_TOTAL_COUNT || 0,
        inStock: (item.DRUGS_IN_STOCK && item.DRUGS_IN_STOCK.length > 0),
        lowStock: (item.DRUGS_FEW_IN_STOCK && item.DRUGS_FEW_IN_STOCK.length > 0),
        outOfStock: (item.DRUGS_NOT_IN_STOCK && item.DRUGS_NOT_IN_STOCK.length > 0)
      }));

      // Separate by stock status
      const inStock = allPharmacies.filter(p => p.inStock);
      const lowStock = allPharmacies.filter(p => p.lowStock && !p.inStock);
      const outOfStock = allPharmacies.filter(p => p.outOfStock && !p.inStock && !p.lowStock);
      const unknown = allPharmacies.filter(p => !p.inStock && !p.lowStock && !p.outOfStock);

      return {
        success: true,
        drugId: largoCode,
        drugName,
        prescriptionRequired,
        cityCode,
        summary: {
          totalPharmacies: allPharmacies.length,
          inStock: inStock.length,
          lowStock: lowStock.length,
          outOfStock: outOfStock.length,
          unknown: unknown.length
        },
        pharmaciesInStock: inStock,
        pharmaciesLowStock: lowStock,
        pharmaciesOutOfStock: outOfStock,
        pharmaciesUnknown: unknown,
        allPharmacies
      };
    } catch (error) {
      console.error('Stock check error:', error.message);
      return { error: 'FAILED', message: error.message, results: [] };
    }
  }
}

// Main CLI
async function main() {
  const [,, command, ...args] = process.argv;

  if (!command) {
    console.log(`
Maccabi Pharmacy Stock Check
============================

Search medications and check real-time stock at Maccabi Pharm.
NO AUTHENTICATION REQUIRED!

Commands:
  search <query>           Search for medications by name
  stock <largoCode> [city] Check stock at pharmacies (use largo code from search)
  branches maccabi [city]  List Maccabi Pharm branches
  cities                   List available city codes
  test                     Run test searches

Examples:
  node pharmacy-search.js search nurofen
  node pharmacy-search.js stock 58299           # Nurofen in Tel Aviv
  node pharmacy-search.js stock 58299 3000      # Nurofen in Jerusalem
  node pharmacy-search.js cities                # List all city codes
`);
    return;
  }

  const maccabi = new MaccabiAdapter();

  try {
    switch (command) {
      case 'search': {
        const query = args[0];
        if (!query) {
          console.error('Please provide a search query');
          return;
        }

        console.log(`Searching for: ${query}\n`);

        const results = await maccabi.searchDrug(query);

        console.log('=== Maccabi Results ===');
        if (results.length > 0) {
          results.forEach(drug => {
            console.log(`  ${drug.name}`);
            console.log(`    Largo Code: ${drug.largoCode} (use this for stock check)`);
            console.log(`    Prescription: ${drug.prescriptionRequired ? 'Yes' : 'No'}`);
            console.log('');
          });
        } else {
          console.log('  No results found');
        }
        break;
      }

      case 'stock': {
        const largoCode = args[0];
        if (!largoCode) {
          console.error('Usage: stock <largoCode> [cityCode]');
          console.error('Example: stock 32833 5000');
          console.error('\nFirst use "search" command to find the largo code for your medication.');
          return;
        }

        const cityCode = args[1] || '5000';
        console.log(`Checking stock for drug ${largoCode} in city ${cityCode}...\n`);

        const result = await maccabi.checkStock(largoCode, cityCode);

        if (result.error) {
          console.error('Error:', result.message);
          return;
        }

        console.log(`Drug: ${result.drugName}`);
        console.log(`Prescription Required: ${result.prescriptionRequired ? 'Yes' : 'No'}`);
        console.log('');
        console.log('=== Stock Summary ===');
        console.log(`  In Stock: ${result.summary.inStock} pharmacies`);
        console.log(`  Low Stock: ${result.summary.lowStock} pharmacies`);
        console.log(`  Out of Stock: ${result.summary.outOfStock} pharmacies`);
        console.log('');

        if (result.pharmaciesInStock.length > 0) {
          console.log('=== Pharmacies with Stock ===');
          result.pharmaciesInStock.forEach(p => {
            console.log(`  📍 ${p.name}`);
            console.log(`     ${p.address}, ${p.city}`);
            console.log(`     📞 ${p.phone}`);
            console.log(`     Distance: ${p.distance} km`);
            console.log('');
          });
        }

        if (result.pharmaciesLowStock.length > 0) {
          console.log('=== Pharmacies with Low Stock ===');
          result.pharmaciesLowStock.forEach(p => {
            console.log(`  ⚠️ ${p.name} - ${p.address} - ${p.phone}`);
          });
          console.log('');
        }
        break;
      }

      case 'branches': {
        const provider = args[0];

        if (provider !== 'maccabi') {
          console.error('Usage: branches maccabi [cityCode]');
          return;
        }

        const cityCode = args[1] || '5000';
        const branches = await maccabi.getBranches(cityCode);
        console.log(`Found ${branches.length} Maccabi pharmacies in city ${cityCode}\n`);
        branches.forEach(b => {
          console.log(`  ${b.name}`);
          console.log(`    ${b.address}, ${b.city}`);
          console.log(`    📞 ${b.phone}`);
          console.log('');
        });
        break;
      }

      case 'cities': {
        console.log('=== Available City Codes ===\n');
        const cities = [
          ['1200', 'מודיעין-מכבים-רעות', 'Modiin'],
          ['2100', 'טירת כרמל', 'Tirat Carmel'],
          ['2200', 'דימונה', 'Dimona'],
          ['2300', 'קריית טבעון', 'Kiryat Tivon'],
          ['2400', 'אור יהודה', 'Or Yehuda'],
          ['2500', 'נשר', 'Nesher'],
          ['2600', 'אילת', 'Eilat'],
          ['2800', 'קריית שמונה', 'Kiryat Shmona'],
          ['3000', 'ירושלים', 'Jerusalem'],
          ['3400', 'כפר עציון', 'Gush Etzion'],
          ['4000', 'חיפה', 'Haifa'],
          ['4100', 'קצרין', 'Katzrin'],
          ['5000', 'תל אביב', 'Tel Aviv'],
          ['6000', 'באקה אל-גרביה', 'Baqa al-Gharbiyye'],
          ['6100', 'בני ברק', 'Bnei Brak'],
          ['6200', 'בת ים', 'Bat Yam'],
          ['6300', 'גבעתיים', 'Givatayim'],
          ['6400', 'הרצליה', 'Herzliya'],
          ['6500', 'חדרה', 'Hadera'],
          ['6600', 'חולון', 'Holon'],
          ['6700', 'טבריה', 'Tiberias'],
          ['6800', 'קריית אתא', 'Kiryat Ata'],
          ['6900', 'כפר סבא', 'Kfar Saba'],
          ['7000', 'לוד', 'Lod'],
          ['7100', 'אשקלון', 'Ashkelon'],
          ['7200', 'נס ציונה', 'Ness Ziona'],
          ['7300', 'נצרת', 'Nazareth'],
          ['7400', 'נתניה', 'Netanya'],
          ['7500', 'סח\'נין', 'Sakhnin'],
          ['7600', 'עכו', 'Acre'],
          ['7700', 'עפולה', 'Afula'],
          ['7800', 'פרדס חנה-כרכור', 'Pardes Hanna'],
          ['7900', 'פתח תקווה', 'Petah Tikva'],
          ['8000', 'צפת', 'Tzfat'],
          ['8200', 'קריית מוצקין', 'Kiryat Motzkin'],
          ['8300', 'ראשון לציון', 'Rishon LeZion'],
          ['8400', 'רחובות', 'Rehovot'],
          ['8500', 'רמלה', 'Ramla'],
          ['8600', 'רמת גן', 'Ramat Gan'],
          ['8700', 'רעננה', 'Raanana'],
          ['8800', 'שפרעם', 'Shfaram'],
          ['8900', 'טמרה', 'Tamra'],
          ['9000', 'באר שבע', 'Beer Sheva'],
          ['9100', 'נהרייה', 'Nahariya'],
          ['9200', 'בית שאן', 'Beit Shean'],
          ['9300', 'זכרון יעקב', 'Zichron Yaakov'],
          ['9400', 'יהוד-מונוסון', 'Yehud'],
          ['9500', 'קריית ביאליק', 'Kiryat Bialik'],
          ['9600', 'קריית ים', 'Kiryat Yam'],
          ['9700', 'הוד השרון', 'Hod HaSharon'],
          ['9800', 'בנימינה', 'Binyamina'],
        ];
        cities.forEach(([code, hebrew, english]) => {
          console.log(`  ${code}  ${english} (${hebrew})`);
        });
        console.log('\nDefault is 5000 (Tel Aviv). Use: stock <largo_code> <city_code>');
        break;
      }

      case 'test': {
        console.log('=== Running Maccabi Pharmacy Tests ===\n');

        // Test 1: Drug search
        console.log('[TEST 1] Drug Search');
        const searchResults = await maccabi.searchDrug('nurofen');
        console.log(`  Found: ${searchResults.length} results`);
        if (searchResults[0]) {
          console.log(`  Sample: ${searchResults[0].name} (code: ${searchResults[0].largoCode})`);
        }
        console.log(`  Status: ${searchResults.length > 0 ? '✅ PASS' : '❌ FAIL'}\n`);

        // Test 2: Stock check
        console.log('[TEST 2] Stock Check');
        const stockResult = await maccabi.checkStock('58299', '5000'); // Nurofen
        console.log(`  Drug: ${stockResult.drugName}`);
        console.log(`  Total pharmacies: ${stockResult.summary?.totalPharmacies || 0}`);
        console.log(`  In stock: ${stockResult.summary?.inStock || 0}`);
        console.log(`  Status: ${stockResult.success ? '✅ PASS' : '❌ FAIL'}\n`);

        // Test 3: Branches
        console.log('[TEST 3] Branch Listing');
        const branches = await maccabi.getBranches('5000');
        console.log(`  Found: ${branches.length} branches in Tel Aviv`);
        console.log(`  Status: ${branches.length > 0 ? '✅ PASS' : '❌ FAIL'}\n`);

        console.log('=== Summary ===');
        const allPassed = searchResults.length > 0 && stockResult.success && branches.length > 0;
        console.log(allPassed ? '✅ All tests passed!' : '⚠️ Some tests failed');
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        console.error('Use: search, stock, branches, cities, or test');
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { MaccabiAdapter };
