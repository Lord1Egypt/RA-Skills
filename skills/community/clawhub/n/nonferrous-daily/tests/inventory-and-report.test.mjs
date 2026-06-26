import test from 'node:test';
import assert from 'node:assert/strict';

import {
  buildInventorySnapshot,
  buildMagnesiumPrice,
  parseShfeInventoryHtml,
} from '../scripts/lib/market-data-utils.mjs';
import { buildReport } from '../scripts/lib/report-builder.mjs';

test('parseShfeInventoryHtml extracts latest weekly copper inventory from MacroMicro HTML', () => {
  const html = `
    <html><body>
      <h1>SHFE-铜库存量</h1>
      <div>#### 最新数据</div>
      <div>SHFE-铜库存量</div>
      <div>2026 W06</div>
      <div>248,911.00</div>
      <div>233,004.00</div>
      <div>资料来源</div>
    </body></html>
  `;

  assert.deepEqual(parseShfeInventoryHtml(html, 'copper'), {
    tonnes: 248911,
    change: 15907,
    unit: 'tonnes',
    dataDate: '2026 W06',
    weekLabel: '2026 W06',
    source: 'SHFE/MacroMicro',
  });
});

test('buildInventorySnapshot preserves legacy LME fields and adds SHFE branch', () => {
  const lme = {
    copper: { tonnes: 123000, change: -1200, unit: 'tonnes', dataDate: '2026-04-03', source: 'Westmetall/LME_Cu_stock' },
    zinc: null,
    nickel: { tonnes: 45600, change: 100, unit: 'tonnes', dataDate: '2026-04-03', source: 'Westmetall/LME_Ni_stock' },
    cobalt: null,
    note: null,
  };
  const shfe = {
    copper: { tonnes: 248911, change: 15907, unit: 'tonnes', dataDate: '2026 W06', weekLabel: '2026 W06', source: 'SHFE/MacroMicro' },
    zinc: null,
    nickel: { tonnes: 57457, change: 2061, unit: 'tonnes', dataDate: '2026 W06', weekLabel: '2026 W06', source: 'SHFE/MacroMicro' },
  };

  const snapshot = buildInventorySnapshot(lme, shfe);

  assert.equal(snapshot.copper.tonnes, 123000);
  assert.equal(snapshot.nickel.tonnes, 45600);
  assert.deepEqual(snapshot.lme.copper, lme.copper);
  assert.deepEqual(snapshot.shfe.copper, shfe.copper);
  assert.equal(snapshot.shfe.zinc, null);
});

test('buildMagnesiumPrice adds USD estimate only when CCMN and FX data exist', () => {
  assert.deepEqual(
    buildMagnesiumPrice(
      { magnesium: { price: 15400, updown: 150 }, dataDate: '2026-04-07' },
      { price: 7.2, source: 'Yahoo Finance', symbol: 'USDCNY=X' },
    ),
    {
      cny: 15400,
      cnyChange: 150,
      cnyUnit: '元/吨',
      usdEstimate: 2139,
      usdUnit: 'USD/t',
      usdSource: 'CCMN/FX-estimate',
      dataDate: '2026-04-07',
      source: 'CCMN',
    },
  );

  assert.deepEqual(
    buildMagnesiumPrice(
      { magnesium: { price: 15400, updown: 150 }, dataDate: '2026-04-07' },
      null,
    ),
    {
      cny: 15400,
      cnyChange: 150,
      cnyUnit: '元/吨',
      usdEstimate: null,
      usdUnit: 'USD/t',
      usdSource: null,
      dataDate: '2026-04-07',
      source: 'CCMN',
    },
  );
});

test('buildReport labels LME and SHFE inventory separately and shows magnesium USD estimate', () => {
  const report = buildReport({
    date: '2026-04-07',
    prices: {
      copper: { usd: 4.2, usdChangePct: 0.5, cny: 76000, cnyChange: 100 },
      zinc: { usd: 2500, usdChangePct: null, cny: 22000, cnyChange: -50 },
      nickel: { usd: 16000, usdChangePct: null, cny: 126000, cnyChange: 200 },
      cobalt: { usd: null, cny: 220000, cnyChange: 0 },
      bismuth: { usd: 15600, cny: 163000, cnyChange: 0, cnyChangePct: 0 },
      magnesium: {
        cny: 15400,
        cnyChange: 150,
        cnyUnit: '元/吨',
        usdEstimate: 2139,
        usdUnit: 'USD/t',
        usdSource: 'CCMN/FX-estimate',
        dataDate: '2026-04-07',
        source: 'CCMN',
      },
    },
    forwards: { copper: null },
    indices: [],
    inventory: {
      copper: { tonnes: 123000, change: -1200, unit: 'tonnes', dataDate: '2026-04-03', source: 'Westmetall/LME_Cu_stock' },
      zinc: null,
      nickel: null,
      cobalt: null,
      note: null,
      lme: {
        copper: { tonnes: 123000, change: -1200, unit: 'tonnes', dataDate: '2026-04-03', source: 'Westmetall/LME_Cu_stock' },
        zinc: null,
        nickel: null,
      },
      shfe: {
        copper: { tonnes: 248911, change: 15907, unit: 'tonnes', dataDate: '2026 W06', weekLabel: '2026 W06', source: 'SHFE/MacroMicro' },
        zinc: null,
        nickel: null,
      },
    },
    news: [],
    ibNews: [],
    forumSentiment: {},
  });

  assert.match(report, /SHFE 周庫存/);
  assert.match(report, /LME：123,000 t/);
  assert.match(report, /SHFE：248,911 t/);
  assert.match(report, /USD est\. 2,139\/t \[CCMN\/FX-estimate\]/);
});
