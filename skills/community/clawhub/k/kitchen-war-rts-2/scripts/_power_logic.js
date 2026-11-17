const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const cand = [path.resolve(__dirname, '..', 'assets', 'index.html'), path.resolve(__dirname, 'index.html')];
const FILE = 'file://' + cand.find(c => fs.existsSync(c));
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 820 } });
  const errors = [];
  p.on('pageerror', e => errors.push('PAGEERR: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await p.addInitScript(() => { try { localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });
  await p.goto(FILE); await sleep(400);
  await p.click('#startBtn'); await sleep(500);
  const res = await p.evaluate(() => {
    const sd = G.player;
    const use0 = sd.powerUse;
    const base = sd.buildings[0];
    // find a valid turret tile via the game's own snapBuild
    const spot = snapBuild('turret', base.gx + 3, base.gy, sd);
    if (!spot) return { err: 'no-spot' };
    const t = placeBuildingInstant('turret', spot.gx, spot.gy, sd);
    const use1 = sd.powerUse;
    if (typeof sellBuilding === 'function') sellBuilding(t); else return { err: 'no-sell' };
    recalcPower(sd);
    const use2 = sd.powerUse;
    return { use0, use1, use2 };
  });
  console.log('POWER LOGIC:', JSON.stringify(res));
  console.log(res.use1 > res.use0 && res.use2 < res.use1 && errors.length === 0 ? 'PASS: 放塔升耗电, 拆塔降耗电, 无崩溃' : 'FAIL');
  await b.close();
})();
