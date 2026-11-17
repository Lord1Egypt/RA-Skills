// capture-text-test.js — 截图隐藏文字回归测试(2026-07-23 重影 bug)
// 场景:方式 B/C 下,文字作为渐变 shape 对象的子元素存在;
// 修复前 capture-pass 只隐藏 [data-object-type="textbox"] 内的文字 → 子级文字烙进 PNG → 重影。
// 断言:转换产物的截图 PNG 中,不含任何"只属于文字"的颜色(浅蓝 #D9E2F0 / 黄色 #FFD966),
//       且白圆(合法形状)仍在(存在纯白像素)。
// 用法: node test/capture-text-test.js   (通过 exit 0,否则 exit 1)
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { chromium } = require("playwright");
const JSZip = require("jszip");

const SCRIPTS_DIR = path.resolve(__dirname, "..");
const FIX = path.join(__dirname, "fixtures-layout", "gradient-text.html");

// 像素断言:在给定容差内,目标颜色出现次数
function countColor(pixels, [tr, tg, tb], tol) {
  let n = 0;
  for (let i = 0; i < pixels.length; i += 4) {
    if (Math.abs(pixels[i] - tr) <= tol && Math.abs(pixels[i + 1] - tg) <= tol && Math.abs(pixels[i + 2] - tb) <= tol) n++;
  }
  return n;
}

(async () => {
  let failures = 0;
  const check = (name, ok, detail = "") => {
    console.log(`${ok ? "✅" : "❌"} ${name}${detail ? " — " + detail : ""}`);
    if (!ok) failures++;
  };

  // 1) 用真实 CLI 转换单页
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "cap-text-"));
  const slidesDir = path.join(tmpDir, "slides");
  fs.mkdirSync(slidesDir, { recursive: true });
  fs.copyFileSync(FIX, path.join(slidesDir, "01.html"));
  fs.writeFileSync(path.join(slidesDir, "playlist.json"), JSON.stringify({ playlist: ["01.html"] }));
  const pptx = path.join(tmpDir, "out.pptx");
  execFileSync(process.execPath, [path.join(SCRIPTS_DIR, "convert.js"), slidesDir, path.join(slidesDir, "playlist.json"), pptx], { stdio: "pipe" });

  // 2) 解出截图 PNG
  const zip = await JSZip.loadAsync(fs.readFileSync(pptx));
  const mediaName = Object.keys(zip.files).find((n) => /^ppt\/media\/.*\.png$/.test(n));
  check("产物含截图 PNG", !!mediaName, mediaName || "未找到");
  const pngBuf = await zip.files[mediaName].async("nodebuffer");

  // 3) 用浏览器 canvas 解码像素
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const pixels = await page.evaluate(async (b64) => {
    const img = new Image();
    await new Promise((res, rej) => {
      img.onload = res;
      img.onerror = rej;
      img.src = "data:image/png;base64," + b64;
    });
    const c = document.createElement("canvas");
    c.width = img.naturalWidth;
    c.height = img.naturalHeight;
    const ctx = c.getContext("2d");
    ctx.drawImage(img, 0, 0);
    return Array.from(ctx.getImageData(0, 0, c.width, c.height).data);
  }, pngBuf.toString("base64"));
  await browser.close();

  // 4) 颜色断言(文字色特意选与白→深蓝抗锯齿混合永不碰撞的橙/黄)
  const orange = countColor(pixels, [0xf3, 0x98, 0x00], 6);    // 标题文字色
  const yellow = countColor(pixels, [0xff, 0xd9, 0x66], 6);    // 副题文字色
  const white = countColor(pixels, [0xff, 0xff, 0xff], 2);     // 白圆(合法形状,76px 直径 ≈ 4500px)
  check("截图不含标题文字色 #F39800", orange === 0, `命中 ${orange} px`);
  check("截图不含副题文字色 #FFD966", yellow === 0, `命中 ${yellow} px`);
  check("截图保留白圆(形状不被误伤)", white > 4000, `白色 ${white} px`);

  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log(failures ? `\n❌ ${failures} 项失败` : "\n✅ 截图隐藏文字回归测试通过");
  process.exit(failures ? 1 : 0);
})();
