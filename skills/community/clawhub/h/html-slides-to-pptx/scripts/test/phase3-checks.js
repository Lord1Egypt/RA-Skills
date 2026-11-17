// phase3-checks.js — Phase 3 验收测试(data-layout 声明式自动布局)
// 1) slide-template-layout.html → validate 0 ERROR
// 2) 方式 C 等价对照:layout 模板与 flex 模板提取的 prims 逐 prim 相等(忽略备注文案)
// 3) bad-layout.html → validate 报出预期 3 类 ERROR(未知策略/混写几何/嵌套)
// 4) resolver 对无 data-layout 页面恒等 no-op(resolveAll 返回 0/0,DOM 不变)
// 用法: node test/phase3-checks.js   (全过 exit 0,否则 exit 1)
const path = require("path");
const { spawnSync } = require("child_process");
const { chromium } = require("playwright");
const { stable } = require("./lib/normalize.js");
const { prepareExtraction } = require("../core/inject.js");
const { gotoSettled } = require("../core/browser.js");
const DEFAULT_CONFIG = require("../config/default.config.js");

const FIX_DIR = path.join(__dirname, "fixtures-layout");
const ASSETS_DIR = path.join(__dirname, "..", "..", "assets");
const VALIDATE = path.join(__dirname, "..", "validate.js");
let failures = 0;
const check = (name, ok, detail = "") => {
  console.log(`${ok ? "✅" : "❌"} ${name}${detail ? " — " + detail : ""}`);
  if (!ok) failures++;
};

function runValidate(files) {
  const r = spawnSync(process.execPath, [VALIDATE, ...files], { encoding: "utf-8" });
  return { status: r.status, out: (r.stdout || "") + (r.stderr || "") };
}

(async () => {
  // ---- 1) 模板页 validate 0 ERROR ----
  const v1 = runValidate([path.join(ASSETS_DIR, "slide-template-layout.html")]);
  check("layout 模板 validate 0 ERROR", v1.status === 0, v1.out.trim().split("\n").pop());

  // ---- 2) 方式 C ≡ 方式 B:prims 逐 prim 相等 ----
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const extractOf = async (file) => {
    await gotoSettled(page, "file://" + file);
    await page.waitForTimeout(DEFAULT_CONFIG.settleMs);
    await prepareExtraction(page);
    return page.evaluate((cfg) => window.__htmlSlides.extract(cfg), DEFAULT_CONFIG.extract);
  };
  const strip = (e) => ({ prims: e.prims, canvasBg: e.canvasBg, canvasBgImage: e.canvasBgImage });
  const flex = stable(strip(await extractOf(path.join(ASSETS_DIR, "slide-template-flex.html"))));
  const layout = stable(strip(await extractOf(path.join(ASSETS_DIR, "slide-template-layout.html"))));
  if (flex === layout) {
    check("方式 C ≡ 方式 B(layout 模板 == flex 模板,逐 prim 相等)", true);
  } else {
    check("方式 C ≡ 方式 B", false, "prims 不一致");
    const al = flex.split("\n"), bl = layout.split("\n");
    for (let i = 0; i < Math.max(al.length, bl.length); i++)
      if (al[i] !== bl[i]) {
        console.log(`  首个差异 @行${i + 1}:\n    flex:   ${al[i]}\n    layout: ${bl[i]}`);
        break;
      }
  }

  // ---- 3) 违规页:预期 3 类 ERROR ----
  const v3 = runValidate([path.join(FIX_DIR, "bad-layout.html")]);
  check("bad-layout 退出码为 1", v3.status === 1, `实际 ${v3.status}`);
  check("报未知策略", v3.out.includes('未知 data-layout 策略: "masonry"'));
  check("报子级混写几何", v3.out.includes("混写了几何属性"));
  check("报嵌套 data-layout", v3.out.includes("不允许嵌套"));

  // ---- 4) resolver 对无 data-layout 页面 no-op ----
  await gotoSettled(page, "file://" + path.join(FIX_DIR, "ab-absolute.html"));
  await prepareExtraction(page);
  const stats = await page.evaluate(() => window.__htmlSlidesLastStats || null);
  // prepareExtraction 不回传统计,这里直接再调一次 resolveAll 验证恒等:
  const r = await page.evaluate(() => window.__htmlSlides.layout.resolveAll(document));
  await browser.close();
  check("无 data-layout 页面 resolveAll 恒等 no-op", r.containers === 0 && r.children === 0, JSON.stringify(r));

  console.log(failures ? `\n❌ ${failures} 项失败` : "\n✅ Phase 3 验收全过");
  process.exit(failures ? 1 : 0);
})();
