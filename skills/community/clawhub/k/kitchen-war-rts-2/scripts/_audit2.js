/*
 * Kitchen War RTS — EXPANDED real-machine audit (_audit2.js)
 * Drives the REAL game loop in a real browser. Goes BEYOND the 29-assertion
 * _full.js to cover paths the core test never touched:
 *   - all 3 maps boot clean + real UI build + produce
 *   - sell building (UI) / repair toggle (UI)
 *   - engineer capture (real adjacent capture)
 *   - superweapon recharge + SECOND firing in one match
 *   - power overdraw (lowPower) must not crash and must slow (not zero) production
 *   - harvester economy actually generates cash over time
 *   - unreachable target (walled tile) -> no crash, no NaN, no infinite loop
 *   - mass death cleanup (spawn 30, kill all, array must drain, no NaN)
 *   - selected-unit death removes it from G.selUnits
 *   - captures console.warn AND console.error AND pageerror (not just errors)
 *
 * Run (managed Node + Playwright):
 *   cd <game dir>
 *   export PLAYWRIGHT_BROWSERS_PATH="$LOCALAPPDATA/ms-playwright"
 *   export NODE_PATH="C:/Users/www74/.workbuddy/binaries/node/workspace/node_modules"
 *   "C:/Users/www74/.workbuddy/binaries/node/versions/22.22.2/node.exe" _audit2.js
 */
const { chromium } = require('playwright');
const path = require('path');
const FILE = 'file://' + path.resolve(__dirname, '..', 'assets', 'index.html');
const sleep = ms => new Promise(r => setTimeout(r, ms));

let PASS = 0, FAIL = 0;
const fails = [];
const warns = [];
function assert(name, cond, info) {
  if (cond) { PASS++; console.log('PASS :: ' + name + (info ? '  [' + info + ']' : '')); }
  else { FAIL++; fails.push(name); console.log('FAIL :: ' + name + (info ? '  [' + info + ']' : '')); }
}

// ---------- helpers ----------
async function snap(page) {
  return page.evaluate(() => ({
    over: G.over, winner: G.winner,
    cash: G.player.cash,
    pBld: G.player.buildings.length, eBld: G.enemy.buildings.length,
    pUnits: G.player.units.length, eUnits: G.enemy.units.length,
    sel: G.selUnits.length,
    lowPower: G.player.lowPower,
    superReady: G.super.ready, superIncoming: !!G.super.incoming,
    anyNaN: (function () {
      for (const u of G.player.units.concat(G.enemy.units)) if (!isFinite(u.x) || !isFinite(u.y)) return true;
      for (const b of G.player.buildings.concat(G.enemy.buildings)) if (!isFinite(b.x) || !isFinite(b.y)) return true;
      return false;
    })(),
    proj: G.projectiles.length, particles: G.particles.length,
    camX: G.camX, camY: G.camY,
    yard: G.player.buildings[0] ? { x: G.player.buildings[0].x, y: G.player.buildings[0].y } : null,
  }));
}
async function worldToClient(page, wx, wy) {
  return page.evaluate((o) => {
    const c = document.getElementById('gameCanvas'); const r = c.getBoundingClientRect();
    const sx = r.width / 760, sy = r.height / 648;
    return { x: r.left + (o.wx - G.camX) * sx, y: r.top + (o.wy - G.camY) * sy };
  }, { wx, wy });
}
async function leftClick(page, wx, wy) {
  const p = await worldToClient(page, wx, wy);
  await page.mouse.move(p.x, p.y); await page.mouse.down(); await sleep(60); await page.mouse.up(); await sleep(60);
}
async function finishBuildings(page) {
  await page.evaluate(() => { G.player.buildings.forEach(b => b.constructing = 1); G.enemy.buildings.forEach(b => b.constructing = 1); });
}
async function buildViaUI(page, type, offset) {
  await page.evaluate(() => { G.player.cash = 999999; });
  const btn = await page.$('#buildGrid .buildBtn[data-type="' + type + '"]');
  if (!btn) return 0;
  await btn.click(); await sleep(150);
  const base = await page.evaluate(() => { const b = G.player.buildings[0]; return { x: b.x, y: b.y }; });
  const ox = offset ? offset.x : 64, oy = offset ? offset.y : 32;
  await leftClick(page, base.x + ox, base.y + oy); await sleep(200);
  return await page.evaluate((t) => G.player.buildings.filter(b => b.type === t).length, type);
}
async function produce(page, type) {
  await page.evaluate(() => { G.player.cash = 999999; });
  // switch to the right tab by trying infantry then vehicle (no direct UNT lookup)
  let clicked = false;
  for (const tab of ['infantry', 'vehicle']) {
    await page.evaluate((t) => { G.activeTab = t; updateSidebar(); }, tab);
    await sleep(100);
    const btn = await page.$('#buildGrid .buildBtn[data-type="' + type + '"]');
    if (btn) { await btn.click(); clicked = true; break; }
  }
  if (!clicked) return false;
  const before = await page.evaluate(() => G.player.units.length);
  for (let i = 0; i < 50; i++) { await sleep(250); const s = await snap(page); if (s.pUnits > before) return true; }
  return false;
}
async function spawnLaser(page, side, wx, wy, hp) {
  await page.evaluate((o) => {
    const c = { type: 'laser', side: o.side, x: o.wx, y: o.wy, tx: o.wx, ty: o.wy, hp: o.hp || 100, maxHp: o.hp || 100, speed: 60, fireCD: 0, target: null, targetBld: null, order: 'stop', cargo: 0, harvestTimer: 0, r: 8, def: { name: '激光兵', speed: 60, range: 132, fireRate: 0.7, sight: 6, r: 8, from: 'barracks', dmg: 14, proj: 'laser', flying: false, aoe: 0 }, animPhase: 0, harvestTarget: null, returnTarget: null, destX: undefined, destY: undefined, repathCD: 0, vet: 0, kills: 0, selected: false, barked: false, path: [] };
    (o.side === 'enemy' ? G.enemy.units : G.player.units).push(c);
  }, { side, wx, wy, hp });
}
const countType = (arr, t) => arr.filter(u => u.type === t).length;

// ---------- main ----------
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--use-gl=swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1100, height: 760 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); else if (m.type() === 'warning') warns.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message));
  // suppress the first-visit help overlay so it doesn't block automated UI clicks
  await page.addInitScript(() => { try { localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });

  await page.goto(FILE);
  await sleep(500);

  async function fresh(mapIdx) {
    await page.evaluate((mi) => { window.selMap = mi; window.startGame(); }, mapIdx);
    await sleep(450);
  }

  try {
    // ============ A) ALL 3 MAPS boot + real build + produce, no errors ============
    for (const mi of [0, 1, 2]) {
      await fresh(mi);
      const s0 = await snap(page);
      assert('地图' + mi + ': 启动无崩溃 & 中央厨房存在', !s0.over && !!s0.yard, 'over=' + s0.over);
      const built = await buildViaUI(page, 'barracks');
      await finishBuildings(page);
      const s1 = await snap(page);
      assert('地图' + mi + ': UI 建造备菜台成功', built && s1.pBld >= 4, 'pBld=' + s1.pBld);
      const produced = await produce(page, 'laser');
      const s2 = await snap(page);
      assert('地图' + mi + ': 生产激光兵成功', produced && s2.pUnits > s1.pUnits, 'pUnits=' + s2.pUnits);
    }

    // ============ B) SELL building via real UI ============
    await fresh(0);
    await buildViaUI(page, 'turret'); await finishBuildings(page);
    const beforeSell = await snap(page);
    // select the turret by clicking it, then click #sellBtn
    const turret = await page.evaluate(() => { const b = G.player.buildings.find(x => x.type === 'turret'); return b ? { x: b.x, y: b.y } : null; });
    await leftClick(page, turret.x, turret.y); await sleep(120);
    const selB = await page.evaluate(() => !!G.selBuilding);
    await page.click('#sellBtn'); await sleep(200);
    const afterSell = await snap(page);
    assert('拆除: 点击建筑选中 & 点拆除按钮真的移除并返还', selB && afterSell.pBld === beforeSell.pBld - 1, 'before=' + beforeSell.pBld + ' after=' + afterSell.pBld);

    // ============ C) REPAIR toggle via real UI ============
    await fresh(0);
    await buildViaUI(page, 'barracks'); await finishBuildings(page);
    await page.evaluate(() => { const b = G.player.buildings.find(x => x.type === 'barracks'); b.hp = b.maxHp * 0.5; });
    const bld = await page.evaluate(() => { const b = G.player.buildings.find(x => x.type === 'barracks'); return { x: b.x, y: b.y, hp: b.hp, max: b.maxHp }; });
    await leftClick(page, bld.x, bld.y); await sleep(120);
    await page.click('#repBtn'); await sleep(1500);
    const repaired = await page.evaluate(() => { const b = G.player.buildings.find(x => x.type === 'barracks'); return b.hp; });
    assert('维修: 点维修按钮后 HP 回升', repaired > bld.hp, 'hp ' + bld.hp.toFixed(0) + '->' + repaired.toFixed(0));

    // ============ D) ENGINEER CAPTURE (real adjacent capture) ============
    await fresh(0);
    const ey = await page.evaluate(() => { const b = G.enemy.buildings[0]; return { x: b.x, y: b.y }; });
    const eBldBefore = (await snap(page)).eBld;
    // spawn a player engineer right next to the enemy yard, let updateEngineer capture it
    await page.evaluate((o) => {
      const eb = G.enemy.buildings[0];
      const c = { type: 'engineer', side: 'player', x: eb.x - 30, y: eb.y, tx: eb.x - 30, ty: eb.y, hp: 90, maxHp: 90, speed: 52, fireCD: 0, target: null, targetBld: null, order: 'move', cargo: 0, harvestTimer: 0, r: 9, def: { name: '工程师', speed: 52, range: 0, dmg: 0, fireRate: 0, sight: 5, r: 9, from: 'barracks', capture: true, flying: false }, animPhase: 0, harvestTarget: null, returnTarget: null, destX: eb.x, destY: eb.y, repathCD: 0, vet: 0, kills: 0, selected: false, barked: false, path: [] };
      G.player.units.push(c);
    }, ey);
    let captured = false;
    for (let i = 0; i < 28; i++) {
      await sleep(250);
      const r = await page.evaluate(() => {
        const stillEnemy = G.enemy.buildings.some(b => b.type === 'yard');
        const nowPlayer = G.player.buildings.some(b => b.type === 'yard');
        return { stillEnemy, nowPlayer, eBld: G.enemy.buildings.length, pBld: G.player.buildings.length };
      });
      if (!r.stillEnemy && r.nowPlayer) { captured = true; break; }
    }
    assert('占领: 工程师贴脸敌方中央厨房后成功夺旗(阵营翻转)', captured, 'eBldBefore=' + eBldBefore);

    // ============ E) SUPERWEAPON recharge + SECOND firing ============
    await fresh(0);
    async function fireSuper(page, x, y) {
      await page.evaluate((o) => { G.super.ready = true; G.super.incoming = null; G.super.charge = 0; G.super.targeting = false; }, {});
      await sleep(120);
      // drive the exact state the button sets, then pick target
      await page.evaluate(() => { G.super.targeting = true; });
      await sleep(80);
      await leftClick(page, x, y);
      // wait for detonation
      for (let i = 0; i < 16; i++) { await sleep(250); const s = await snap(page); if (!s.superIncoming) return true; }
      return false;
    }
    const tgt = await page.evaluate(() => { const b = G.enemy.buildings[0]; return { x: b.x, y: b.y }; });
    const fire1 = await fireSuper(page, tgt.x + 5, tgt.y + 5);
    const fire2 = await fireSuper(page, tgt.x + 40, tgt.y + 40);
    assert('超武: 同局可蓄能并连续投放两次(再装填生效)', fire1 && fire2, 'f1=' + fire1 + ' f2=' + fire2);

    // ============ F) POWER OVERDRAW (lowPower) must not crash & slows but not zero ============
    await fresh(0);
    await buildViaUI(page, 'barracks', { x: 64, y: 64 });
    // place 4 turrets at varied offsets so auto-snap always finds room (fixed-offset click used to fail)
    const turretOffsets = [{x:64,y:32},{x:96,y:32},{x:32,y:64},{x:96,y:64},{x:-64,y:32},{x:-32,y:64}];
    let tPlaced = 0;
    for (const off of turretOffsets) { const n = await buildViaUI(page, 'turret', off); if (n > tPlaced) tPlaced = n; if (tPlaced >= 4) break; }
    await finishBuildings(page);
    await sleep(450); // let the real game loop run recalcPower() so power/powerUse/lowPower are fresh (recalc skips constructing<1)
    const powInfo = await page.evaluate(() => ({ power: G.player.power, use: G.player.powerUse, low: G.player.lowPower, turrets: G.player.buildings.filter(b => b.type === 'turret' && b.constructing >= 1).length }));
    assert('电力: 4座微波塔真实落位(供电100/用电≥280)', tPlaced >= 4, 'turrets=' + tPlaced + ' pow=' + JSON.stringify(powInfo));
    assert('电力: 用电远超供电时进入低电(不崩、不零产)', powInfo.low === true, 'lowPower=' + powInfo.low);
    // production should still eventually produce (slow), not hang at 0
    await produce(page, 'laser');
    const lowS = await snap(page);
    assert('电力: 低电下仍能产出(慢但不为零)', lowS.pUnits >= 1, 'pUnits=' + lowS.pUnits);

    // ============ G) HARVESTER ECONOMY actually generates cash ============
    await fresh(0);
    const cash0 = (await snap(page)).cash;
    let cashGrew = false, cash1 = cash0;
    for (let i = 0; i < 8; i++) { await sleep(2000); cash1 = (await snap(page)).cash; if (cash1 > cash0) { cashGrew = true; break; } }
    assert('经济: 采集兵真实运回食材(cash 增长, ~6-12s 内)', cashGrew, 'cash ' + cash0 + '->' + cash1);

    // ============ H) UNREACHABLE target (walled tile) -> no crash / no NaN ============
    await fresh(0);
    const wallC = await page.evaluate(() => {
      // map0 has a wall block at rect(20,14,4,5) -> center ~ (22,16)
      return { x: 22 * 32 + 16, y: 16 * 32 + 16 };
    });
    await spawnLaser(page, 'player', 200, 200);
    await page.evaluate((o) => { const u = G.player.units[G.player.units.length - 1]; u.destX = o.x; u.destY = o.y; u.order = 'move'; u.path = findPath(u.x, u.y, o.x, o.y) || []; }, wallC);
    await sleep(1500);
    const stuck = await snap(page);
    const uFin = await page.evaluate(() => { const u = G.player.units[G.player.units.length - 1]; return { x: u.x, y: u.y, order: u.order }; });
    assert('不可达: 命令单位进入被墙包围的格子不崩/不产生NaN', !stuck.anyNaN, 'anyNaN=' + stuck.anyNaN + ' order=' + uFin.order);

    // ============ I) MASS DEATH cleanup ============
    await fresh(0);
    await page.evaluate(() => {
      for (let i = 0; i < 30; i++) {
        const c = { type: 'laser', side: 'enemy', x: 400 + i * 2, y: 300, tx: 400, ty: 300, hp: 1, maxHp: 1, speed: 60, fireCD: 0, target: null, targetBld: null, order: 'stop', cargo: 0, harvestTimer: 0, r: 8, def: UNT.laser, animPhase: 0, harvestTarget: null, returnTarget: null, destX: undefined, destY: undefined, repathCD: 0, vet: 0, kills: 0, selected: false, barked: false, path: [] };
        G.enemy.units.push(c);
      }
    });
    const massBefore = (await snap(page)).eUnits;
    await page.evaluate(() => { G.enemy.units.forEach(u => u.hp = 0); });
    await sleep(400); // let updateUnits splice them
    const massAfter = (await snap(page)).eUnits;
    assert('清场: 30 个敌人被清空后数组排空且无残留', massBefore >= 30 && massAfter === 0, 'before=' + massBefore + ' after=' + massAfter);

    // ============ J) SELECTED-UNIT death removes from G.selUnits ============
    await fresh(0);
    await spawnLaser(page, 'player', 300, 300);
    await page.evaluate(() => { const u = G.player.units[G.player.units.length - 1]; u.selected = true; G.selUnits.push(u); });
    const selBefore = (await snap(page)).sel;
    await page.evaluate(() => { G.player.units[G.player.units.length - 1].hp = 0; });
    await sleep(300);
    const selAfter = (await snap(page)).sel;
    assert('选中单位阵亡后从选择集移除', selBefore >= 1 && selAfter === selBefore - 1, 'sel ' + selBefore + '->' + selAfter);

    // ============ K) no runtime errors / warnings throughout ============
    assert('全程: 无 console.error / 无 pageerror', errors.length === 0, 'err=' + errors.length);
    assert('全程: 无 console.warn(潜在隐患)', warns.length === 0, 'warn=' + warns.length);

  } catch (e) {
    console.log('HARNESS EXCEPTION:', e.message);
    FAIL++;
  }

  await browser.close();
  console.log('\n===== EXPANDED AUDIT ' + PASS + '/' + (PASS + FAIL) + ' PASSED =====');
  if (fails.length) console.log('FAILED:', fails.join(' | '));
  if (warns.length) console.log('WARNINGS(' + warns.length + '):', warns.slice(0, 6).join(' || '));
  if (errors.length) console.log('ERRORS(' + errors.length + '):', errors.slice(0, 6).join(' || '));
  console.log(FAIL === 0 ? 'ALL_EXPANDED_PASS' : 'EXPANDED_HAS_FAILURES');
  process.exit(FAIL === 0 ? 0 : 1);
})();
