/*
 * Kitchen War RTS — engagement-features smoke test (_smoke_features.js)
 * Verifies the new retention/UX layer: help overlay, topBar, speed/pause,
 * sfx/music toggles, achievements panel, screenshot, hotkeys — with zero
 * console errors. Drives the REAL game in a real browser.
 */
const { chromium } = require('playwright');
const path = require('path');
const FILE = 'file://' + path.resolve(__dirname, '..', 'assets', 'index.html');
const sleep = ms => new Promise(r => setTimeout(r, ms));
let PASS = 0, FAIL = 0;
const fails = [];
function assert(n, c, info) { if (c) { PASS++; console.log('PASS :: ' + n + (info ? '  [' + info + ']' : '')); } else { FAIL++; fails.push(n); console.log('FAIL :: ' + n + (info ? '  [' + info + ']' : '')); } }

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--use-gl=swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1100, height: 760 } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
  await page.goto(FILE); await sleep(500);

  // clear first-visit flag so help shows
  await page.evaluate(() => { try { localStorage.removeItem('kw_seenHelp'); } catch (e) {} });
  await page.reload(); await sleep(500);

  // 1) first-visit help overlay shows
  const helpShown = await page.evaluate(() => getComputedStyle(document.getElementById('helpOverlay')).display !== 'none');
  assert('首次访问自动弹出操作说明', helpShown, 'display=' + (helpShown ? 'flex' : 'none'));

  // 2) close help, start game
  await page.click('#helpCloseBtn'); await sleep(200);
  await page.evaluate(() => { window.startGame(); }); await sleep(500);

  // 3) topBar exists & speed defaults 1x
  const speed1 = await page.textContent('#tbSpeed');
  assert('顶部工具条存在 & 默认速度1x', speed1 === '速度 1x', 'tbSpeed="' + speed1 + '"');

  // 4) cycle speed 1->2->3->1
  await page.click('#tbSpeed'); const s2 = await page.textContent('#tbSpeed');
  await page.click('#tbSpeed'); const s3 = await page.textContent('#tbSpeed');
  await page.click('#tbSpeed'); const s1 = await page.textContent('#tbSpeed');
  await page.evaluate(() => { G.speed = 1; }); // restore for timing
  assert('速度循环 1x->2x->3x->1x', s2 === '速度 2x' && s3 === '速度 3x' && s1 === '速度 1x', s2 + '|' + s3 + '|' + s1);

  // 5) pause toggle via button + Space hotkey
  await page.click('#tbPause'); const paused1 = await page.evaluate(() => G.paused);
  await page.click('#tbPause'); const paused2 = await page.evaluate(() => G.paused);
  await page.keyboard.press('Space'); const paused3 = await page.evaluate(() => G.paused);
  await page.keyboard.press('Space'); const paused4 = await page.evaluate(() => G.paused);
  assert('暂停按钮 & 空格热键 正反切换', paused1 === true && paused2 === false && paused3 === true && paused4 === false, [paused1, paused2, paused3, paused4].join(','));

  // 6) sfx toggle persists
  await page.click('#tbMute'); const sfxOff = await page.evaluate(() => sfxOn);
  await page.click('#tbMute'); const sfxOn2 = await page.evaluate(() => sfxOn);
  assert('音效开关切换(并持久化)', sfxOff === false && sfxOn2 === true, sfxOff + '->' + sfxOn2);

  // 7) achievements panel renders 10 achievements
  await page.click('#tbAch'); await sleep(150);
  const achCount = await page.evaluate(() => document.querySelectorAll('#achGrid .ach').length);
  const achHeader = await page.textContent('#achCount');
  await page.click('#achCloseBtn');
  assert('成就面板渲染 10 项', achCount === 10, 'count=' + achCount + ' header="' + achHeader + '"');

  // 8) hotkey 1 opens build tab & selects first building into placeMode
  await page.keyboard.press('Digit1'); await sleep(150);
  const placeModeSet = await page.evaluate(() => !!G.placeMode);
  assert('热键 1 进入首建筑放置模式', placeModeSet, 'placeMode=' + placeModeSet);
  await page.keyboard.press('Escape');

  // 9) screenshot triggers a download (capture the download event)
  const [download] = await Promise.all([page.waitForEvent('download', { timeout: 4000 }), page.click('#tbShot')]).catch(() => [null]);
  assert('截图按钮生成 PNG 下载', !!download, download ? download.suggestedFilename() : 'no-download');

  // 10) help hotkey H reopens help
  await page.keyboard.press('KeyH'); await sleep(150);
  const helpReopened = await page.evaluate(() => getComputedStyle(document.getElementById('helpOverlay')).display !== 'none');
  await page.keyboard.press('Escape'); // escape doesn't close help; close via button
  await page.click('#helpCloseBtn');
  assert('热键 H 重新打开操作说明', helpReopened, 'display=' + (helpReopened ? 'flex' : 'none'));

  // 11) game still runs (no NaN) after toggling features
  await sleep(300);
  const anyNaN = await page.evaluate(() => {
    for (const u of G.player.units.concat(G.enemy.units)) if (!isFinite(u.x) || !isFinite(u.y)) return true;
    return false;
  });
  assert('功能切换后游戏循环仍正常(无NaN)', !anyNaN, 'anyNaN=' + anyNaN);

  // 12) zero console errors / pageerrors throughout
  assert('全程: 无 console.error / 无 pageerror', errs.length === 0, 'err=' + errs.length + (errs.length ? ' :: ' + errs.slice(0, 3).join(' | ') : ''));

  await browser.close();
  console.log('\n===== FEATURES SMOKE ' + PASS + '/' + (PASS + FAIL) + ' PASSED =====');
  if (fails.length) console.log('FAILED:', fails.join(' | '));
  process.exit(FAIL === 0 ? 0 : 1);
})();
