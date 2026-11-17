// golden.js — 黄金主回归测试 harness
// 三层等价判定(重构期间"功能不变"的客观标准):
//   L1 提取层: 每页 extractPrimitives 产出的 {prims, notes, canvasBg, canvasBgImage},
//              规范化(键排序+浮点4位截断)后深比较
//   L2 输出层: 用真实 convert.js CLI 转 playlist,解包 pptx 比对 slide XML;
//              notesSlide 合并为单项比对(2026-08-05 瘦身:notes 管线是单一特性,
//              逐文件锚定 N 次是冗余;失败时明细列出具体文件)
//   L3 渲染层: 仅对**含 capture 基元的页**(渐变/图片/SVG/canvas/特效/图标)做
//              1920x1080 截图比对(2026-08-05 瘦身:纯原生页的渲染完全由 L1 基元
//              决定——颜色/字体/几何都在 prims 里,截图与之冗余;判定与 L1 同源,
//              extract 退化会先触发 L1 失败,故不会漏护)
//
// 用法:
//   node golden.js update [--l1] [--l2] [--l3] [--only <子串>]   # 落盘基线
//   node golden.js verify [--l1] [--l2] [--l3] [--only <子串>]   # 比对(默认三层全跑)
// 退出码: verify 有 FAIL → 1;全绿 → 0
//
// L1 与 convert.js 共用同一注入通道(core/inject.js)+ 同一配置,保证"黄金所见 = 转换所得"。
const fs = require("fs");
const os = require("os");
const path = require("path");
const zlib = require("zlib");
const { execFileSync } = require("child_process");
const { chromium } = require("playwright");
const JSZip = require("jszip");

// ---- P2 2.9:感知 diff(L3 像素级容忍)----
// webfont 时序抖动会导致同一页面截图有亚像素级差异(如 slide-template-layout 0.65%)。
// 精确比较(Buffer.equals)失败时,降级到像素差异比例:低于阈值视为等价。
// 纯 Node.js 实现(zlib 解压 IDAT + 手写 unfilter),不引入新依赖。
function decodePngRaw(buf) {
  // 解析 PNG:提取 width/height/bitDepth/colorType + 解压 IDAT
  if (buf[0] !== 0x89 || buf[1] !== 0x50) return null; // 非 PNG
  let off = 8, w = 0, h = 0, bd = 8, ct = 6, idat = [];
  while (off < buf.length) {
    const len = buf.readUInt32BE(off); off += 4;
    const type = buf.toString("ascii", off, off + 4); off += 4;
    const data = buf.slice(off, off + len); off += len + 4; // +4 CRC
    if (type === "IHDR") { w = data.readUInt32BE(0); h = data.readUInt32BE(4); bd = data[8]; ct = data[9]; }
    else if (type === "IDAT") idat.push(data);
    else if (type === "IEND") break;
  }
  if (bd !== 8) return null; // 仅支持 8-bit
  const bpp = ct === 6 ? 4 : ct === 2 ? 3 : ct === 0 ? 1 : null; // RGBA/RGB/Gray
  if (!bpp) return null;
  const raw = zlib.inflateSync(Buffer.concat(idat));
  // Unfilter(5 种 filter type)
  const stride = w * bpp + 1; // 每行 = 1 filter byte + w*bpp 像素
  const pixels = Buffer.alloc(h * w * bpp);
  const prev = Buffer.alloc(w * bpp);
  for (let y = 0; y < h; y++) {
    const rowStart = y * stride;
    const filter = raw[rowStart];
    const src = raw.slice(rowStart + 1, rowStart + 1 + w * bpp);
    const dst = Buffer.alloc(w * bpp);
    for (let x = 0; x < w * bpp; x++) {
      const a = x >= bpp ? dst[x - bpp] : 0;       // left
      const b = prev[x];                              // up
      const c = x >= bpp ? prev[x - bpp] : 0;        // upper-left
      let v = src[x];
      if (filter === 1) v = (v + a) & 0xff;           // Sub
      else if (filter === 2) v = (v + b) & 0xff;      // Up
      else if (filter === 3) v = (v + ((a + b) >> 1)) & 0xff; // Average
      else if (filter === 4) {                        // Paeth
        const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
        v = (v + (pa <= pb && pa <= pc ? a : pb <= pc ? b : c)) & 0xff;
      }
      dst[x] = v;
    }
    dst.copy(pixels, y * w * bpp);
    dst.copy(prev);
  }
  return { w, h, bpp, pixels };
}

// 感知比较:返回 { equivalent, diffPct }
const PERCEPTUAL_THRESHOLD = 1.0; // 差异像素 <1.0% 视为等价(webfont 时序抖动通常 <1%)
function perceptualCompare(bufA, bufB) {
  const a = decodePngRaw(bufA), b = decodePngRaw(bufB);
  if (!a || !b || a.w !== b.w || a.h !== b.h || a.bpp !== b.bpp) return { equivalent: false, diffPct: 100 };
  let diff = 0;
  const total = a.w * a.h;
  const threshold = 15; // 每通道差异 >15 视为不同
  for (let i = 0; i < a.pixels.length; i += a.bpp) {
    // 比较像素(任一通道差异 >threshold 视为不同像素)
    let pixelDiff = false;
    for (let c = 0; c < a.bpp; c++) {
      if (Math.abs(a.pixels[i + c] - b.pixels[i + c]) > threshold) { pixelDiff = true; break; }
    }
    if (pixelDiff) diff++;
  }
  const diffPct = (diff / total) * 100;
  return { equivalent: diffPct < PERCEPTUAL_THRESHOLD, diffPct };
}

const TEST_DIR = __dirname;
const SCRIPTS_DIR = path.resolve(TEST_DIR, "..");
const GOLDEN_DIR = path.join(TEST_DIR, "golden");
const FIXTURES = JSON.parse(fs.readFileSync(path.join(TEST_DIR, "fixtures.json"), "utf-8"));
// 夹具路径统一相对 TEST_DIR 解析(fixtures.json 内存相对路径,技能目录自包含可迁移)
FIXTURES.slidesDir = path.resolve(TEST_DIR, FIXTURES.slidesDir);
FIXTURES.playlistFile = path.resolve(TEST_DIR, FIXTURES.playlistFile);
FIXTURES.extraPages = (FIXTURES.extraPages || []).map((p) => path.resolve(TEST_DIR, p));
const { prepareExtraction } = require(path.join(SCRIPTS_DIR, "core", "inject.js"));
const { gotoSettled } = require(path.join(SCRIPTS_DIR, "core", "browser.js"));
const DEFAULT_CONFIG = require(path.join(SCRIPTS_DIR, "config", "default.config.js"));
const SETTLE_MS = DEFAULT_CONFIG.settleMs; // 与 convert.js 同一来源,防门禁与产品漂移

// ---------- 规范化:递归排序键 + 浮点截断 4 位 ----------
const { stable } = require("./lib/normalize.js");

// ---------- L1:提取层 ----------
async function collectL1(page, file) {
  await gotoSettled(page, "file://" + file);
  // 等 webfont 就绪(封顶 2s 防挂起)再 settle —— 消除字体加载时序导致的 L1/L3 抖动(与 pipeline 一致)
  await Promise.race([
    page.evaluate(() => (document.fonts && document.fonts.ready ? document.fonts.ready.then(() => true) : true)),
    page.waitForTimeout(2000),
  ]);
  await page.waitForTimeout(SETTLE_MS);
  await prepareExtraction(page);
  return await page.evaluate((cfg) => window.__htmlSlides.extract(cfg), DEFAULT_CONFIG.extract);
}

// ---------- L2:输出层(真实 CLI 转换 + 解包 XML) ----------
// --no-cache(2026-08-05):回归必须测真实管线。缓存键不含浏览器端脚本,
// 改 extract/render 后吃缓存会产出"假基线"(H12 教训:106 页底纹修复被缓存藏掉)。
function collectL2(tmpPptx) {
  execFileSync(
    process.execPath,
    [path.join(SCRIPTS_DIR, "convert.js"), FIXTURES.slidesDir, FIXTURES.playlistFile, tmpPptx, "--no-cache"],
    { stdio: ["ignore", "pipe", "inherit"] }
  );
}

const XML_PREFIXES = ["ppt/slides/slide", "ppt/notesSlides/notesSlide"];
// 2026-08-05 瘦身:notesSlide 不再逐文件锚定,合并为一个合成键比对
const NOTES_MERGED_KEY = "__notesSlides__(合并锚定)";
async function extractXmlMap(pptxPath) {
  const zip = await JSZip.loadAsync(fs.readFileSync(pptxPath));
  const names = Object.keys(zip.files)
    .filter((n) => XML_PREFIXES.some((p) => n.startsWith(p)) && n.endsWith(".xml"))
    .sort();
  const map = {};
  const noteParts = [];
  for (const n of names) {
    const content = await zip.files[n].async("string");
    if (n.startsWith("ppt/notesSlides/")) noteParts.push(n + "\n" + content);
    else map[n] = content;
  }
  if (noteParts.length) map[NOTES_MERGED_KEY] = noteParts.join("\n");
  return map;
}

// notesSlide 合并项比对失败时,逐文件定位差异(供人工复核明细)
async function diffNotesDetail(pptxPath, goldenJoined) {
  const zip = await JSZip.loadAsync(fs.readFileSync(pptxPath));
  const names = Object.keys(zip.files)
    .filter((n) => n.startsWith("ppt/notesSlides/") && n.endsWith(".xml"))
    .sort();
  const diffs = [];
  for (const n of names) {
    const content = await zip.files[n].async("string");
    if (!goldenJoined.includes(n + "\n" + content)) diffs.push(n);
  }
  return diffs;
}

// ---------- 主流程 ----------
function parseArgs(argv) {
  const mode = argv[2];
  if (!["update", "verify"].includes(mode)) {
    console.error("用法: node golden.js update|verify [--l1] [--l2] [--l3] [--only <子串>]");
    process.exit(2);
  }
  const flags = new Set(argv.slice(3).filter((a) => a.startsWith("--l")));
  const onlyIdx = argv.indexOf("--only");
  const only = onlyIdx > -1 ? argv[onlyIdx + 1] : null;
  return {
    mode,
    l1: flags.size === 0 || flags.has("--l1"),
    l2: flags.size === 0 || flags.has("--l2"),
    l3: flags.size === 0 || flags.has("--l3"),
    only,
  };
}

function ensureDirs() {
  fs.mkdirSync(path.join(GOLDEN_DIR, "shots"), { recursive: true });
}

// ---- 基线读写:合并 JSON 格式(1 个文件替代 N 个散文件)----
const PRIMS_BASELINE = path.join(GOLDEN_DIR, "prims-baseline.json");
const XML_BASELINE = path.join(GOLDEN_DIR, "xml-baseline.json");

function loadPrimsBaseline() {
  if (!fs.existsSync(PRIMS_BASELINE)) return {};
  try { return JSON.parse(fs.readFileSync(PRIMS_BASELINE, "utf-8")); } catch (e) { return {}; }
}
function savePrimsBaseline(map) {
  fs.writeFileSync(PRIMS_BASELINE, JSON.stringify(map, null, 2));
}
function loadXmlBaseline() {
  if (!fs.existsSync(XML_BASELINE)) return {};
  try { return JSON.parse(fs.readFileSync(XML_BASELINE, "utf-8")); } catch (e) { return {}; }
}
function saveXmlBaseline(map) {
  fs.writeFileSync(XML_BASELINE, JSON.stringify(map, null, 2));
}

(async () => {
  const { mode, l1, l2, l3, only } = parseArgs(process.argv);
  ensureDirs();
  const results = [];
  const record = (layer, name, ok, detail = "") => {
    results.push({ layer, name, ok });
    if (!ok || process.env.GOLDEN_VERBOSE)
      console.log(`  ${ok ? "✅" : "❌"} [${layer}] ${name}${detail ? " — " + detail : ""}`);
  };

  // 夹具 = 项目页(相对 slidesDir) + 技能模板页(extraPages,绝对路径)
  const allPages = [
    ...FIXTURES.pages.map((f) => ({ abs: path.join(FIXTURES.slidesDir, f), name: f })),
    ...(FIXTURES.extraPages || []).map((p) => ({ abs: p, name: path.basename(p) })),
  ];
  const pages = allPages.filter((p) => !only || p.name.includes(only));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  // ---- L1 + L3(逐页) ----
  // L1 基线:合并 JSON(键=stem,值=规范化 JSON 字符串)
  const primsBaseline = (l1 && mode === "verify") ? loadPrimsBaseline() : {};
  // update --only 时先载入既有基线再合并,避免只更新子集却把整份基线覆盖成子集
  // (全量 update 仍整体重写,顺带 prunes 已删除页面的陈旧条目)
  const primsUpdated = (l1 && mode === "update" && only) ? loadPrimsBaseline() : {};
  const SHOTS_DIR = path.join(GOLDEN_DIR, "shots");
  let l3Captured = 0, l3Skipped = 0;
  const shotStems = new Set(); // update 时记录实际落盘的 shot,用于 prune 陈旧/原生页 PNG

  for (const { abs: fp, name: f } of pages) {
    const stem = f.replace(/\.html$/, "");
    // L3 门控需要 extract 结果(判定含 capture 基元与否);与 L1 共用同一次页面加载
    let ext = null;
    if (l1 || l3) ext = await collectL1(page, fp);
    if (l1) {
      const got = stable(ext);
      if (mode === "update") {
        primsUpdated[stem] = got;
      } else {
        const golden = primsBaseline[stem];
        record("L1", f, golden !== undefined && golden === got);
      }
    }
    if (l3) {
      const hasCapture = (ext.prims || []).some((p) => p.kind === "capture");
      const gp = path.join(SHOTS_DIR, stem + ".png");
      if (!hasCapture) {
        l3Skipped++;
        if (mode === "update" && fs.existsSync(gp)) fs.rmSync(gp); // 页面变成纯原生 → 移除陈旧 shot
      } else {
        shotStems.add(stem);
        const buf = await page.screenshot();
        if (mode === "update") fs.writeFileSync(gp, buf);
        else {
          // P2 2.9:精确比较优先;失败时降级到感知 diff(像素差异 <0.5% 视为等价)
          const goldenBuf = fs.existsSync(gp) ? fs.readFileSync(gp) : null;
          let ok = goldenBuf && goldenBuf.equals(buf);
          let note = "";
          if (!ok && goldenBuf) {
            const pc = perceptualCompare(goldenBuf, buf);
            ok = pc.equivalent;
            note = pc.equivalent ? ` (感知 diff 通过,差异 ${pc.diffPct.toFixed(2)}%)` : ` (感知 diff 失败,差异 ${pc.diffPct.toFixed(2)}%)`;
            if (!ok) fs.writeFileSync(gp + ".actual.png", buf); // 供人工复核
          }
          record("L3", f, !!ok, goldenBuf ? note : " (golden 中缺失,先跑 update)");
        }
        l3Captured++;
      }
    }
  }

  // 全量 update:prune 不在本次落盘集合的 PNG(退役页孤儿/已转纯原生页/复核残留 .actual)
  if (l3 && mode === "update" && !only) {
    for (const f of fs.readdirSync(SHOTS_DIR)) {
      const stem = f.replace(/\.actual\.png$/, "").replace(/\.png$/, "");
      if (!shotStems.has(stem)) fs.rmSync(path.join(SHOTS_DIR, f));
    }
  }

  // L1 update:一次性写入合并 JSON
  if (l1 && mode === "update") savePrimsBaseline(primsUpdated);

  // ---- L2(playlist 整体转换) ----
  if (l2) {
    const tmp = path.join(os.tmpdir(), `golden-${process.pid}.pptx`);
    try {
      collectL2(tmp);
      const got = await extractXmlMap(tmp);
      const gotKeys = Object.keys(got);
      if (mode === "update") {
        saveXmlBaseline(got);
        console.log(`  (L2 解包 ${gotKeys.length} 个 XML → 合并 JSON)`);
      } else {
        const xmlBaseline = loadXmlBaseline();
        const goldenKeys = Object.keys(xmlBaseline).sort();
        const want = new Set(gotKeys);
        for (const gk of goldenKeys) {
          const ok = got[gk] !== undefined && xmlBaseline[gk] === got[gk];
          let detail = "";
          if (!ok && gk === NOTES_MERGED_KEY && got[gk] !== undefined) {
            const diffs = await diffNotesDetail(tmp, xmlBaseline[gk]);
            detail = diffs.length ? `差异文件: ${diffs.join(", ")}` : "notesSlide 文件集合不一致";
          }
          record("L2", gk, ok, detail);
          want.delete(gk);
        }
        for (const missing of want) record("L2", missing, false, "golden 中缺失");
      }
    } finally {
      if (fs.existsSync(tmp)) { try { fs.rmSync(tmp, { force: true }); } catch (e) {} }
    }
  }

  await browser.close();

  if (mode === "update") {
    console.log(`✅ 基线已落盘: ${GOLDEN_DIR} (L1=${l1 ? pages.length : 0} 页, L2=${l2 ? "是" : "否"}, L3=${l3 ? `${l3Captured} 页截图,${l3Skipped} 页纯原生免截图` : "否"})`);
    return;
  }
  const fails = results.filter((r) => !r.ok);
  const byLayer = (l) => results.filter((r) => r.layer === l);
  console.log(`\n──────────────────────────────`);
  for (const l of ["L1", "L2", "L3"]) {
    const rs = byLayer(l);
    if (rs.length) console.log(`${l}: ${rs.filter((r) => r.ok).length}/${rs.length} 通过`);
  }
  if (l3 && l3Skipped) console.log(`   (L3 免截图: ${l3Skipped} 页纯原生,渲染完全由 L1 基元锚定)`);
  if (fails.length) {
    console.log(`❌ ${fails.length} 项不等价:`);
    for (const f of fails) console.log(`   [${f.layer}] ${f.name}`);
    process.exit(1);
  }
  console.log(`✅ 全部等价 (${results.length} 项)`);
})();
