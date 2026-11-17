/*
 * Kitchen War RTS — mandatory quality gate.
 * Drives the REAL game (real browser, real game loop) — not a one-frame stub —
 * because multi-frame interaction bugs are invisible to instant tests.
 *
 * Covers:
 *   A) Real UI: build a barracks via side-panel button + ghost placement,
 *      select a unit, command a move (across two viewports 800x560 & 1280x800).
 *   B) Real loop: enemy AI launches an attack wave; player destroys the enemy
 *      central kitchen -> victory; superweapon detonates and damages the enemy.
 *   C) Zero pageerror / console.error throughout.
 *
 * Run (managed Node + Playwright):
 *   cd <skill>/scripts
 *   export PLAYWRIGHT_BROWSERS_PATH="$LOCALAPPDATA/ms-playwright"
 *   export NODE_PATH="C:/Users/www74/.workbuddy/binaries/node/workspace/node_modules"
 *   "C:/Users/www74/.workbuddy/binaries/node/versions/22.22.2/node.exe" verify_game.js
 */
const { chromium } = require('playwright');
const path = require('path');
const FILE = 'file://' + path.resolve(__dirname, '../assets/index.html');
const sleep = ms => new Promise(r => setTimeout(r, ms));

// faithful unit factory (mirrors spawnUnit's top-level fields) — page-injected.
const MK = function (side, x, y, type) {
  var def = { name: type, hp: 100, speed: 60, r: 9, range: 300, fireRate: 0.5, dmg: 30, indirect: false, flying: false };
  return {
    type, side, x, y, tx: x, ty: y, hp: 100, maxHp: 100,
    speed: def.speed, slowTimer: 0, fireCD: 0, target: null, targetBld: null,
    order: 'stop', cargo: 0, harvestTimer: 0, r: def.r, def: def, animPhase: 0,
    harvestTarget: null, returnTarget: null, destX: undefined, destY: undefined, repathCD: 0,
    vet: 0, kills: 0, selected: false, barked: false, path: []
  };
};

async function humanClick(page, x, y) {
  await page.mouse.move(x, y);
  await page.mouse.down();
  await sleep(90);            // straddle multiple frames like a real human
  await page.mouse.up();
  await sleep(60);
}

// ---- Part A: real UI build / select / move ----
async function runUI(vw, vh) {
  const TILE = 32;
  const errors = [];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: vw, height: vh } });
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message));
  // suppress the first-visit help overlay so it doesn't block automated UI clicks
  await page.addInitScript(() => { try { localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });
  await page.goto(FILE);
  await sleep(300);
  await page.click('#startBtn');
  await sleep(400);
  const map = await page.evaluate(() => {
    const c = document.getElementById('gameCanvas'); const r = c.getBoundingClientRect();
    const sx = r.width / 760, sy = r.height / 648;
    const sd = G.player; let spot = null; const M = 2;
    for (let bi = 0; bi < sd.buildings.length && !spot; bi++) {
      const b = sd.buildings[bi];
      for (let dy = -M; dy <= b.h + M && !spot; dy++) for (let dx = -M; dx <= b.w + M && !spot; dx++) {
        const gx = b.gx + dx, gy = b.gy + dy;
        if (gx < 1 || gy < 1 || gx + 2 >= MAP_W - 1 || gy + 1 >= MAP_H - 1) continue;
        if (canPlace('barracks', gx, gy, sd)) {
          const cx = (gx + 1) * TILE, cy = (gy + 1) * TILE;
          if (cx - G.camX > 30 && cx - G.camX < 730 && cy - G.camY > 30 && cy - G.camY < 618) spot = { gx, gy };
        }
      }
    }
    const base = sd.buildings[0];
    return { nBuild: sd.buildings.length, nUnits: sd.units.length, base: { x: base.x, y: base.y }, spot };
  });
  const btnBox = await page.evaluate(() => {
    const grid = document.getElementById('buildGrid');
    const btns = grid.querySelectorAll('.buildBtn');
    for (const b of btns) { if (b.dataset.type === 'barracks') { const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; } }
    return null;
  });
  let buildBtnWorked = false, ghostValid = false, placed = false;
  if (btnBox) {
    await humanClick(page, btnBox.x, btnBox.y);
    buildBtnWorked = await page.evaluate(() => G.placeMode === 'barracks');
    ghostValid = await page.evaluate(() => {
      if (!G.placeMode) return false;
      const d = BLD[G.placeMode];
      const gx = Math.floor((G.mouseX + G.camX) / TILE) - Math.floor(d.w / 2);
      const gy = Math.floor((G.mouseY + G.camY) / TILE) - Math.floor(d.h / 2);
      return !!snapBuild(G.placeMode, gx, gy, G.player);
    });
    if (map.spot) {
      const cx = (map.spot.gx + 1) * TILE, cy = (map.spot.gy + 1) * TILE;
      const s = await page.evaluate((o) => { const c = document.getElementById('gameCanvas'); const r = c.getBoundingClientRect(); const sx = r.width / 760, sy = r.height / 648; return { x: r.left + (o.wx - G.camX) * sx, y: r.top + (o.wy - G.camY) * sy }; }, { wx: cx, wy: cy });
      await humanClick(page, s.x, s.y);
      placed = await page.evaluate(() => G.player.buildings.length) > map.nBuild;
    }
  }
  const laser = await page.evaluate(() => {
    const u = G.player.units.find(u => u.type === 'laser' && u.hp > 0);
    if (!u) return null;
    const c = document.getElementById('gameCanvas'); const r = c.getBoundingClientRect(); const sx = r.width / 760, sy = r.height / 648;
    return { x: r.left + (u.x - G.camX) * sx, y: r.top + (u.y - G.camY) * sy, wx: u.x, wy: u.y };
  });
  let selOk = false, moved = false, order = null;
  if (laser) {
    await humanClick(page, laser.x, laser.y);
    selOk = await page.evaluate(() => G.selUnits.length) > 0;
    if (selOk) {
      const before = await page.evaluate(() => { const u = G.selUnits[0]; return { x: u.x, y: u.y }; });
      const tx = laser.wx + 70, ty = laser.wy;
      const s = await page.evaluate((o) => { const c = document.getElementById('gameCanvas'); const r = c.getBoundingClientRect(); const sx = r.width / 760, sy = r.height / 648; return { x: r.left + (o.wx - G.camX) * sx, y: r.top + (o.wy - G.camY) * sy }; }, { wx: tx, wy: ty });
      await humanClick(page, s.x, s.y);
      order = await page.evaluate(() => G.selUnits[0] ? G.selUnits[0].order : null);
      await sleep(700);
      const after = await page.evaluate(() => { const u = G.selUnits[0]; return u ? { x: u.x, y: u.y } : null; });
      if (after) moved = Math.hypot(after.x - before.x, after.y - before.y) > 5;
    }
  }
  await browser.close();
  return { vw, vh, buildBtnWorked, ghostValid, placed, selOk, order, moved, errors };
}

// ---- Part B: real-loop AI / victory / superweapon ----
async function runLoopChecks() {
  const errors = [];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message));
  await page.addInitScript(() => { try { localStorage.setItem('kw_seenHelp', '1'); } catch (e) {} });
  await page.goto(FILE);
  await sleep(300);
  await page.evaluate(() => window.startGame && window.startGame());
  await sleep(400);

  // AI attacks
  await page.evaluate((mkSrc) => {
    const mk = eval('(' + mkSrc + ')');
    const b = G.enemy.buildings[0];
    for (let i = 0; i < 4; i++) G.enemy.units.push(mk('enemy', b.x + 40 + i * 18, b.y + 40, 'laser'));
    G.attackTimer = 0; G.aiTimer = 0; G.diff.reqArmy = 1;
  }, MK.toString());
  await sleep(4200);
  const ai = await page.evaluate(() => G.enemy.units.filter(u => u.order === 'attackMove' && u.target && u.target.side === 'player').length);
  const aiOk = ai >= 1;

  // Victory via real combat on the enemy yard
  await page.evaluate((mkSrc) => {
    const mk = eval('(' + mkSrc + ')');
    const yard = G.enemy.buildings.find(b => b.type === 'yard');
    yard.hp = 1;
    const u = mk('player', yard.x + 12, yard.y + 12, 'laser');
    u.def.range = 400; u.target = yard; u.order = 'attackMove'; u.destX = yard.x; u.destY = yard.y; u.path = [];
    G.player.units.push(u);
  }, MK.toString());
  await sleep(1800);
  const vic = await page.evaluate(() => ({ over: G.over, winner: G.winner }));
  const vicOk = vic.over === true && vic.winner === 'player';

  // fresh match for superweapon
  await page.evaluate(() => window.startGame());
  await sleep(300);
  const sw = await page.evaluate((mkSrc) => {
    const mk = eval('(' + mkSrc + ')');
    const ex = G.enemy.buildings[0].x, ey = G.enemy.buildings[0].y;
    const u = mk('enemy', ex, ey, 'laser');
    G.enemy.units.push(u);
    const idx = G.enemy.units.length - 1;
    G.super.ready = true;
    G.super.incoming = { x: ex, y: ey, t: 0, delay: 0.05 };
    return idx;
  }, MK.toString());
  await sleep(600);
  const swAfter = await page.evaluate((idx) => { const u = G.enemy.units[idx]; return u ? u.hp : 0; }, sw);
  const swOk = swAfter <= 0;

  await browser.close();
  return { aiOk, vicOk, swOk, errors };
}

(async () => {
  const ui1 = await runUI(800, 560);
  const ui2 = await runUI(1280, 800);
  const loop = await runLoopChecks();
  const allErrors = [...ui1.errors, ...ui2.errors, ...loop.errors];

  const uiOk = [ui1, ui2].every(o => o.buildBtnWorked && o.ghostValid && o.placed && o.selOk && o.moved && o.errors.length === 0);
  const ok = uiOk && loop.aiOk && loop.vicOk && loop.swOk && allErrors.length === 0;

  console.log(`[UI 800x560] build=${ui1.buildBtnWorked} ghost=${ui1.ghostValid} placed=${ui1.placed} sel=${ui1.selOk} order=${ui1.order} moved=${ui1.moved} err=${ui1.errors.length}`);
  console.log(`[UI 1280x800] build=${ui2.buildBtnWorked} ghost=${ui2.ghostValid} placed=${ui2.placed} sel=${ui2.selOk} order=${ui2.order} moved=${ui2.moved} err=${ui2.errors.length}`);
  console.log(`[LOOP] aiAttack=${loop.aiOk} victory=${loop.vicOk} superweapon=${loop.swOk} err=${loop.errors.length}`);
  if (allErrors.length) console.log('ERRORS:', allErrors.slice(0, 5));
  console.log(ok ? 'VERIFY_GAME_PASS' : 'VERIFY_GAME_FAIL');
  process.exit(ok ? 0 : 1);
})();
