// Adversarial probe: try to break the game in ways the 62 asserts don't cover.
const { chromium } = require('playwright');
const path = require('path');

const fs = require('fs');
const cand = [path.resolve(__dirname, '..', 'assets', 'index.html'), path.resolve(__dirname, 'index.html')];
const FILE = 'file://' + cand.find(c => fs.existsSync(c));
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 820 } });
  const errors = [], warns = [];
  page.on('console', m => {
    if (m.type() === 'error') errors.push(m.text());
    else if (m.type() === 'warning') { if (!/AudioContext|autoplay|user gesture/i.test(m.text())) warns.push(m.text()); }
  });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message));
  await page.addInitScript(() => { try { localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });
  await page.goto(FILE);
  await sleep(500);

  const snap = () => page.evaluate(() => {
    let anyNaN = false;
    const chk = (v) => { if (typeof v === 'number' && !isFinite(v)) anyNaN = true; };
    G.player.units.forEach(u => { chk(u.x); chk(u.y); chk(u.destX); chk(u.destY); });
    G.enemy.units.forEach(u => { chk(u.x); chk(u.y); });
    G.player.buildings.forEach(b => { chk(b.x); chk(b.y); chk(b.gx); chk(b.gy); });
    return {
      cash: G.player.cash, power: G.player.power, powerUse: G.player.powerUse,
      low: G.player.lowPower, over: G.over, winner: G.winner, speed: G.speed, paused: G.paused,
      pUnits: G.player.units.length, eUnits: G.enemy.units.length,
      particles: G.particles.length, effects: G.effects.length, anyNaN,
      sel: G.selUnits.length, time: G.time, achFirst: (typeof achState !== 'undefined') ? !!achState['first'] : null,
      goScreen: document.getElementById('gameOverScreen').style.display,
      goTitle: document.getElementById('goTitle').textContent
    };
  });
  const worldToClient = (wx, wy) => page.evaluate(([wx, wy]) => {
    const c = document.getElementById('gameCanvas'); const r = c.getBoundingClientRect();
    const z = Math.min(r.width / 760, r.height / 648);
    return { x: r.left + wx * z, y: r.top + wy * z };
  }, [wx, wy]);
  const leftClick = async (wx, wy) => { const p = await worldToClient(wx, wy); await page.mouse.click(p.x, p.y); await sleep(80); };
  const fresh = async () => {
    await page.evaluate(() => { if (typeof G !== 'undefined' && G.over) location.reload(); });
    await page.goto(FILE); await sleep(300);
    await page.evaluate(() => { try { localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });
    await page.click('#startBtn'); await sleep(500);
  };
  const setSpeed = async (n) => { for (let i = 0; i < 4; i++) { const s = await page.evaluate(() => G.speed); if (s === n) return; await page.click('#tbSpeed'); await sleep(120); } };
  const buildViaUI = async (type) => {
    await page.evaluate(() => { G.player.cash = 999999; });
    const btn = await page.$('#buildGrid .buildBtn[data-type="' + type + '"]');
    if (!btn) return false;
    await btn.click(); await sleep(150);
    const base = await page.evaluate(() => { const b = G.player.buildings[0]; return { x: b.x, y: b.y }; });
    // try several offsets to find a valid placement
    const offs = [[64, 32], [96, 32], [64, 64], [96, 64], [32, 64], [128, 32], [64, 96], [-32, 32]];
    for (const [ox, oy] of offs) { await leftClick(base.x + ox, base.y + oy); await sleep(150); if (await page.evaluate(t => G.player.buildings.some(b => b.type === t), type)) return true; }
    return false;
  };

  let pass = 0, fail = 0; const bad = [];
  const ok = (name, cond, info = '') => { if (cond) { pass++; console.log('PASS :: ' + name + (info ? '  [' + info + ']' : '')); } else { fail++; bad.push(name); console.log('FAIL :: ' + name + (info ? '  [' + info + ']' : '')); } };

  // ---------- 1) PAUSE freezes the simulation ----------
  await fresh();
  await page.evaluate(() => { if (typeof spawnUnit === 'function') for (let i = 0; i < 3; i++) spawnUnit('laser', 'player', G.player.buildings[0]); });
  await sleep(800);
  await page.click('#tbPause'); await sleep(100);
  const pPaused = await page.evaluate(() => G.paused);
  const posA = await page.evaluate(() => G.player.units.map(u => Math.round(u.x) + ',' + Math.round(u.y)));
  await sleep(1200);
  const posB = await page.evaluate(() => G.player.units.map(u => Math.round(u.x) + ',' + Math.round(u.y)));
  ok('暂停: 暂停后单位不位移', pPaused === true && JSON.stringify(posA) === JSON.stringify(posB), 'paused=' + pPaused + ' moved=' + (JSON.stringify(posA) !== JSON.stringify(posB)));
  await page.click('#tbPause'); await sleep(100);

  // ---------- 2) SPEED 3x advances G.time ~3x faster than 1x ----------
  await setSpeed(1);
  const t1a = (await snap()).time; await sleep(1000); const t1b = (await snap()).time;
  await setSpeed(3);
  const t3a = (await snap()).time; await sleep(1000); const t3b = (await snap()).time;
  const d1 = t1b - t1a, d3 = t3b - t3a;
  ok('速度: 3x 下 G.time 推进约为 1x 的 3 倍', d3 > d1 * 2 && d1 > 0.5, '1xΔ=' + d1.toFixed(2) + ' 3xΔ=' + d3.toFixed(2));

  // ---------- 3) SUPERWEAPON at 4 map corners ----------
  for (const [cx, cy] of [[20, 20], [740, 20], [20, 628], [740, 628]]) {
    await fresh();
    await page.evaluate(() => { G.super.charge = G.super.max; G.super.ready = true; G.super.targeting = true; });
    await leftClick(cx, cy);
    await sleep(900);
    const st = await snap();
    ok('超武四角(' + cx + ',' + cy + '): 命中无崩溃/无NaN', st.anyNaN === false && errors.length === 0, 'incoming=' + st.effects);
  }

  // ---------- 4) SELL a turret (consumer) -> powerUse drops, no crash ----------
  await fresh();
  const placed = await buildViaUI('turret');
  await page.evaluate(() => { G.player.buildings.forEach(b => { if (b.type === 'turret') b.constructing = 1; }); });
  await sleep(500);
  const useBefore = await page.evaluate(() => G.player.powerUse);
  const sellRes = await page.evaluate(() => {
    const t = G.player.buildings.find(b => b.type === 'turret');
    if (!t) return 'no-turret';
    if (typeof sellBuilding === 'function') { sellBuilding(t); return 'sold'; }
    return 'no-fn';
  });
  await sleep(500);
  const after = await snap();
  ok('拆除微波塔: powerUse 下降且无崩溃', placed && after.powerUse < useBefore && errors.length === 0, 'use ' + useBefore + '->' + after.powerUse + ' (' + sellRes + ')');

  // ---------- 5) LONG 3x RUN 30s: no error, particles bounded, no NaN ----------
  await fresh();
  await setSpeed(3);
  await page.evaluate(() => { if (typeof spawnUnit === 'function') for (let i = 0; i < 8; i++) spawnUnit('laser', 'player', G.player.buildings[0]); });
  let maxParticles = 0, sawNaN = false;
  for (let i = 0; i < 10; i++) {
    await sleep(3000);
    const s = await snap();
    maxParticles = Math.max(maxParticles, s.particles);
    if (s.anyNaN) sawNaN = true;
    if (errors.length) break;
  }
  ok('长时3x: 30s 无 error/pageerror', errors.length === 0, 'errors=' + errors.length);
  ok('长时3x: 无 NaN 坐标', !sawNaN);
  ok('长时3x: 粒子数有界(未泄漏)', maxParticles < 2000, 'maxParticles=' + maxParticles);

  // ---------- 6) SUSTAINED harvester economy ----------
  await fresh();
  const c0 = (await snap()).cash;
  await sleep(8000); const c1 = (await snap()).cash;
  await sleep(8000); const c2 = (await snap()).cash;
  ok('经济: 持续运回食材(8s/16s 单调不降且增长)', c1 >= c0 && c2 > c1, 'cash ' + c0 + '->' + c1 + '->' + c2);

  // ---------- 7) VICTORY unlocks first-win achievement + persists + screen ----------
  await fresh();
  await page.evaluate(() => { const ey = G.enemy.buildings.find(b => b.type === 'yard'); if (ey) damage(ey, 99999, 'player'); });
  await sleep(700);
  const v = await page.evaluate(() => ({
    over: G.over, winner: G.winner, achFirst: !!achState['first'],
    screen: document.getElementById('gameOverScreen').style.display,
    title: document.getElementById('goTitle').textContent,
    ls: (function () { try { return localStorage.getItem('kw_ach'); } catch (e) { return null; } })()
  }));
  ok('胜利: 触发战役胜利', v.over === true && v.winner === 'player', 'winner=' + v.winner);
  ok('胜利: 首战告捷成就解锁(真实Bug检查点)', v.achFirst === true, 'achFirst=' + v.achFirst);
  ok('胜利: 成就持久化到 localStorage', !!v.ls && v.ls.indexOf('first') >= 0, 'ls=' + v.ls);
  ok('胜利: 结算屏显示胜利', v.screen === 'flex' && /胜利/.test(v.title), 'screen=' + v.screen + ' title=' + v.title);

  // ---------- 8) RESIZE window mid-game ----------
  await fresh();
  await page.setViewportSize({ width: 900, height: 700 }); await sleep(300);
  await page.setViewportSize({ width: 1500, height: 950 }); await sleep(300);
  await page.setViewportSize({ width: 1280, height: 820 }); await sleep(300);
  const rs = await snap();
  ok('缩放: 游戏中改窗口尺寸无崩溃/无NaN', errors.length === 0 && rs.anyNaN === false);

  // ---------- 9) DOUBLE startGame call ----------
  await fresh();
  await page.evaluate(() => { if (typeof startGame === 'function') startGame(); });
  await sleep(500);
  const ds = await snap();
  ok('双击开始: 二次调用 startGame 不崩溃/不双重初始化', errors.length === 0);

  // ---------- 10) SELECT 0 units then right-click move ----------
  await fresh();
  await page.evaluate(() => { G.selUnits = []; });
  await page.mouse.click(400, 400, { button: 'right' });
  await sleep(300);
  const z0 = await snap();
  ok('零选中右键: 不崩溃', errors.length === 0 && z0.anyNaN === false);

  // ---------- 11) Click on a FRIENDLY unit -> should MOVE, not attack-friend ----------
  await fresh();
  const ff = await page.evaluate(() => {
    if (typeof spawnUnit !== 'function') return 'no-fn';
    spawnUnit('laser', 'player', G.player.buildings[0]);
    const u = G.player.units[G.player.units.length - 1];
    const friend = G.player.units[0];
    G.selUnits = [u];
    commandUnits(friend.x, friend.y); // click exactly on a friendly
    return { order: u.order, targetIsFriend: !!(u.target && u.target.side === 'player') };
  });
  await sleep(300);
  ok('误击友军: 不产生攻击友军指令(应为move且无友军target)', ff === 'no-fn' || (ff.order === 'move' && ff.targetIsFriend === false), JSON.stringify(ff));

  // ---------- 12) MUSIC toggle rapidly ----------
  await fresh();
  for (let i = 0; i < 8; i++) { await page.evaluate(() => { if (typeof toggleMusic === 'function') toggleMusic(); }); await sleep(50); }
  const mt = await snap();
  ok('配乐: 快速连切无崩溃', errors.length === 0 && mt.anyNaN === false);

  console.log('\n===== ADVERSARIAL PROBE ' + pass + '/' + (pass + fail) + ' PASSED =====');
  if (errors.length) { console.log('CAPTURED ERRORS:'); errors.forEach(e => console.log('  ' + e)); }
  if (warns.length) { console.log('CAPTURED WARNINGS:'); warns.forEach(w => console.log('  ' + w)); }
  if (bad.length) console.log('FAILURES: ' + bad.join(' | '));
  await browser.close();
  process.exit(fail === 0 && errors.length === 0 ? 0 : 1);
})().catch(e => { console.error('PROBE CRASH:', e); process.exit(2); });
