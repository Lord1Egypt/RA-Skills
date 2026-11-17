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
  await p.addInitScript(() => { try { localStorage.removeItem('kw_best'); localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });
  await p.goto(FILE); await sleep(400);
  await p.click('#startBtn'); await sleep(500);
  // force a win
  await p.evaluate(() => { const ey = G.enemy.buildings.find(x => x.type === 'yard'); if (ey) damage(ey, 99999, 'player'); });
  await sleep(700);
  const r = await p.evaluate(() => ({
    goBest: document.getElementById('goBest').textContent,
    kwBest: localStorage.getItem('kw_best'),
    shareBtn: !!document.querySelector('#gameOverScreen button[onclick="screenshot()"]')
  }));
  // click share button, ensure no error
  let clickErr = null;
  try { await p.click('#gameOverScreen button[onclick="screenshot()"]'); await sleep(400); } catch (e) { clickErr = e.message; }
  console.log('BEST:', JSON.stringify(r));
  console.log('SHARE CLICK ERR:', clickErr);
  const okBest = r.goBest && /个人最佳/.test(r.goBest) && r.kwBest && /bestTime/.test(r.kwBest) && r.shareBtn && !clickErr && errors.length === 0;
  console.log(okBest ? 'PASS: 最佳战绩显示+持久化+分享按钮可用' : 'FAIL');
  await b.close();
  process.exit(okBest ? 0 : 1);
})();
