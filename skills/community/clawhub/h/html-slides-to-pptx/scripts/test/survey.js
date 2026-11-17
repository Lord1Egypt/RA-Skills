// survey.js — 现状测绘扫描(Phase 0 一次性决策依据,后续可复用)
// 对 fixtures.json 全部页面扫描四项事实:
//   a. 嵌套 data-object(H2):内层标记对象会被 walk 两遍 → 双重提取。预期 0
//   b. DOM 序 vs z-index 序(H3):实现按 DOM 遍历序叠放,规范声称 z-index。
//      若两序逐页一致 → 保持 DOM 序语义安全。预期一致
//   c. grid 容器+纯内联子级(H4):hasBlockChild 只认 flex,grid 容器会被错误拍平。预期 0
//   d. validate.js 现状输出基线(后续阶段不得新增告警)
// 用法: node survey.js            # 扫描 a/b/c 并刷新 validate 基线文件
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { chromium } = require("playwright");
const { gotoSettled } = require("../core/browser.js");

const TEST_DIR = __dirname;
const SCRIPTS_DIR = path.resolve(TEST_DIR, "..");
const FIXTURES = JSON.parse(fs.readFileSync(path.join(TEST_DIR, "fixtures.json"), "utf-8"));
FIXTURES.slidesDir = path.resolve(TEST_DIR, FIXTURES.slidesDir); // 相对 TEST_DIR 解析(与 golden.js 一致)
const BASELINE_TXT = path.join(TEST_DIR, "golden", "validate-baseline.txt");

const scanInPage = () => {
  const OBJ = '[data-object="true"]';
  const INLINE = new Set(["SPAN", "BR", "B", "I", "STRONG", "EM", "A", "SUP", "SUB", "FONT"]);
  const out = { nested: [], zMismatched: false, gridFlatten: [], transforms: [] };

  // a. 嵌套 data-object
  document.querySelectorAll(OBJ).forEach((el) => {
    const parent = el.parentElement && el.parentElement.closest(OBJ);
    if (parent)
      out.nested.push({
        inner: el.tagName.toLowerCase() + "." + (el.className || ""),
        innerText: (el.textContent || "").trim().slice(0, 24),
      });
  });

  // b. DOM 序 vs z-index 序(稳定排序后应完全一致)
  const objs = Array.from(document.querySelectorAll(OBJ)).map((el, i) => {
    const z = getComputedStyle(el).zIndex;
    return { dom: i, z: z === "auto" ? 0 : parseInt(z, 10) || 0 };
  });
  const sorted = objs.slice().sort((a, b) => a.z - b.z || a.dom - b.dom);
  out.zMismatched = !objs.every((o, i) => o.dom === sorted[i].dom);

  // c. grid 容器 + 纯内联元素子级 + 有文字(hasBlockChild 对 grid 误判为 false 的形态)
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const cs = getComputedStyle(el);
    if (!cs.display.includes("grid")) return;
    const kids = Array.from(el.children);
    if (!kids.length) return;
    if (kids.every((c) => INLINE.has(c.tagName)) && (el.textContent || "").trim() !== "")
      out.gridFlatten.push(el.tagName.toLowerCase() + ' "' + el.textContent.trim().slice(0, 24) + '"');
  });

  // d2. transform 使用(规范禁止,顺带确认)
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const t = getComputedStyle(el).transform;
    if (t && t !== "none") out.transforms.push(el.tagName.toLowerCase());
  });

  // e. 未标记且不在 data-object 内的"非绝对定位"可见元素(Phase 2 流式检查的安全性预扫描)
  out.unmarkedFlow = [];
  document.querySelectorAll(".slide-container *").forEach((el) => {
    if (el.closest('[data-object="true"]')) return;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    if (cs.position === "absolute" || cs.position === "fixed") return; // 旧规则已覆盖
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const hasVisual =
      cs.backgroundColor !== "rgba(0, 0, 0, 0)" ||
      (cs.backgroundImage && cs.backgroundImage !== "none") ||
      (el.textContent || "").trim() !== "";
    if (hasVisual)
      out.unmarkedFlow.push(el.tagName.toLowerCase() + ' "' + (el.textContent || "").trim().slice(0, 20) + '"');
  });

  // f. 重叠 data-object 对的 z-index/DOM 序倒挂(Phase 2 重叠预警的安全性预扫描)
  out.overlapInverted = 0;
  const boxes = Array.from(document.querySelectorAll('[data-object="true"]')).map((el, i) => {
    const cs = getComputedStyle(el);
    const z = cs.zIndex;
    return { dom: i, z: z === "auto" ? 0 : parseInt(z, 10) || 0, r: el.getBoundingClientRect() };
  });
  const overlap = (a, b) =>
    a.r.left < b.r.right && b.r.left < a.r.right && a.r.top < b.r.bottom && b.r.top < a.r.bottom;
  for (let i = 0; i < boxes.length; i++)
    for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j]; // a 先 DOM
      if (a.z > b.z && overlap(a, b)) out.overlapInverted++; // DOM 在前却 z 更高 → 两序倒挂
    }

  return out;
};

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const totals = { nested: 0, zMismatchPages: [], gridFlatten: 0, transformPages: [], unmarkedFlow: 0, overlapInverted: 0 };

  for (const f of FIXTURES.pages) {
    await gotoSettled(page, "file://" + path.join(FIXTURES.slidesDir, f));
    await page.waitForTimeout(200);
    const r = await page.evaluate(scanInPage);
    totals.nested += r.nested.length;
    totals.gridFlatten += r.gridFlatten.length;
    if (r.nested.length) console.log(`⚠️  [a] ${f}: ${r.nested.length} 处嵌套`, r.nested.slice(0, 3));
    if (r.zMismatched) { totals.zMismatchPages.push(f); console.log(`⚠️  [b] ${f}: DOM 序 ≠ z-index 序`); }
    if (r.gridFlatten.length) console.log(`⚠️  [c] ${f}: ${r.gridFlatten.length} 处 grid 拍平风险`, r.gridFlatten.slice(0, 3));
    if (r.transforms.length) totals.transformPages.push(`${f}(${r.transforms.length})`);
    if (r.unmarkedFlow.length) { totals.unmarkedFlow += r.unmarkedFlow.length; console.log(`⚠️  [e] ${f}: ${r.unmarkedFlow.length} 处未标记流式可见元素`, r.unmarkedFlow.slice(0, 3)); }
    if (r.overlapInverted) { totals.overlapInverted += r.overlapInverted; console.log(`⚠️  [f] ${f}: ${r.overlapInverted} 对重叠倒挂`); }
  }
  await browser.close();

  // d. validate 输出基线(对 slidesDir 全量跑一遍,原样落盘)
  let vout;
  try {
    vout = execFileSync(process.execPath, [path.join(SCRIPTS_DIR, "validate.js"), FIXTURES.slidesDir], { encoding: "utf-8" });
  } catch (e) {
    vout = (e.stdout || "") + (e.stderr || ""); // ERROR 时退出码 1,输出照常保存
  }
  fs.writeFileSync(BASELINE_TXT, vout);
  const vSummary = vout.trim().split("\n").pop();

  console.log(`\n──────── 测绘结论 ────────`);
  console.log(`a. 嵌套 data-object 总数: ${totals.nested} ${totals.nested === 0 ? "→ H2 可定为非法" : "→ H2 需兼容开关!"}`);
  console.log(`b. DOM 序≠z-index 序的页面: ${totals.zMismatchPages.length} ${totals.zMismatchPages.length === 0 ? "→ H3 保持 DOM 序安全" : totals.zMismatchPages.join(",")}`);
  console.log(`c. grid 拍平风险形态: ${totals.gridFlatten} ${totals.gridFlatten === 0 ? "→ H4 修复安全" : "→ H4 需兼容开关!"}`);
  console.log(`d. transform 页面: ${totals.transformPages.length ? totals.transformPages.join(",") : "无"}`);
  console.log(`e. 未标记流式可见元素: ${totals.unmarkedFlow} ${totals.unmarkedFlow === 0 ? "→ 流式检查安全" : "→ 流式检查会误报旧页!"}`);
  console.log(`f. 重叠 z/DOM 倒挂对: ${totals.overlapInverted} ${totals.overlapInverted === 0 ? "→ 重叠预警安全" : "→ 重叠预警会误报旧页!"}`);
  console.log(`g. validate 基线: ${vSummary}(已存 golden/validate-baseline.txt)`);
})();
