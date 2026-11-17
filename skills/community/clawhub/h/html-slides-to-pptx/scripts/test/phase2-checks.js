// phase2-checks.js — Phase 2 验收测试(布局放开)
// 1) violations.html → validate 报出预期 3 个 ERROR(嵌套/布局子级未标记/流式未标记),退出码 1
// 2) ab-flex.html + ab-absolute.html → validate 0 ERROR
// 3) A/B 提取等价:同一视觉的绝对定位版与 flex 版,提取的 prims 规范化后逐字节相等
// 用法: node test/phase2-checks.js   (全过 exit 0,否则 exit 1)
const path = require("path");
const { spawnSync } = require("child_process");
const { chromium } = require("playwright");
const { stable } = require("./lib/normalize.js");
const { injectExtractors } = require("../core/inject.js");
const { gotoSettled } = require("../core/browser.js");
const DEFAULT_CONFIG = require("../config/default.config.js");

const FIX_DIR = path.join(__dirname, "fixtures-layout");
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
  // ---- 1) 违规页:预期 3 个具体 ERROR,exit 1 ----
  const v = runValidate([path.join(FIX_DIR, "violations.html")]);
  check("违规页退出码为 1", v.status === 1, `实际 ${v.status}`);
  check("报 data-object 嵌套", v.out.includes("data-object 嵌套"));
  check("报布局容器子级未标记", v.out.includes("布局容器(flex)的可见子级未标记"));
  check("报流式未标记元素", v.out.includes('元素未标记 data-object="true"'));
  const errCount = (v.out.match(/❌ ERROR/g) || []).length;
  check("恰好 3 个 ERROR(规则互不重复)", errCount === 3, `实际 ${errCount}`);

  // ---- 2) A/B 两页:validate 0 ERROR ----
  const ab = runValidate([path.join(FIX_DIR, "ab-absolute.html"), path.join(FIX_DIR, "ab-flex.html")]);
  check("A/B 页 validate 0 ERROR(退出码 0)", ab.status === 0, ab.out.trim().split("\n").pop());

  // ---- 3) A/B 提取等价 ----
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const extractOf = async (file) => {
    await gotoSettled(page, "file://" + file);
    await page.waitForTimeout(DEFAULT_CONFIG.settleMs);
    await injectExtractors(page);
    return page.evaluate((cfg) => window.__htmlSlides.extract(cfg), DEFAULT_CONFIG.extract);
  };
  const a = stable(await extractOf(path.join(FIX_DIR, "ab-absolute.html")));
  const b = stable(await extractOf(path.join(FIX_DIR, "ab-flex.html")));
  await browser.close();
  if (a === b) {
    check("A/B 提取等价(绝对定位版 == flex 版,逐 prim 相等)", true);
  } else {
    check("A/B 提取等价", false, "prims 不一致");
    const al = a.split("\n"), bl = b.split("\n");
    for (let i = 0; i < Math.max(al.length, bl.length); i++)
      if (al[i] !== bl[i]) {
        console.log(`  首个差异 @行${i + 1}:\n    绝对版: ${al[i]}\n    flex版: ${bl[i]}`);
        break;
      }
  }

  console.log(failures ? `\n❌ ${failures} 项失败` : "\n✅ Phase 2 验收全过");
  process.exit(failures ? 1 : 0);
})();
