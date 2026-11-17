// core/pipeline.js — 转换主编排:逐页 加载→稳定→注入→提取→截图→渲染→备注
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const PptxGenJS = require("pptxgenjs");
const { resolveConfig } = require("../config/merge.js");
const { launchPage, gotoSettled } = require("./browser.js");
const { prepareExtraction } = require("./inject.js");
const { capturePass } = require("./capture-pass.js");
const { renderAll } = require("../render/index.js");
const { postProcessGradient, postProcessTransitions, postProcessChartPaths } = require("./post-process.js");

// P2 2.8:增量缓存 —— 基于 HTML 内容 hash + config hash 缓存提取+截图结果。
// 未变化的页面跳过浏览器交互(加载/提取/截图),直接用缓存数据渲染。
// 缓存目录:slides/.cache/(与 playlist 同级);手动删除即清空。
// 缓存键 = sha256(htmlContent + configJson);缓存值 = { withCaptures, notes, canvasBg }
function computeCacheKey(htmlContent, config) {
  const configRelevant = JSON.stringify({
    nativeGradient: config.nativeGradient,
    extract: config.extract,
    canvas: config.canvas,
    iconFonts: config.iconFonts,
    capture: { imageType: config.capture.imageType, quality: config.capture.quality },
  });
  return crypto.createHash("sha256").update(htmlContent + configRelevant).digest("hex").slice(0, 16);
}

function loadCache(cacheDir, key) {
  const cacheFile = path.join(cacheDir, key + ".json");
  if (!fs.existsSync(cacheFile)) return null;
  try {
    return JSON.parse(fs.readFileSync(cacheFile, "utf-8"));
  } catch (e) {
    return null; // 缓存损坏 → 视为 miss
  }
}

function saveCache(cacheDir, key, data) {
  try {
    if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });
    fs.writeFileSync(path.join(cacheDir, key + ".json"), JSON.stringify(data));
  } catch (e) {
    // 缓存写入失败 → 静默跳过(不影响转换)
  }
}

// 把 http(s) 图片预取为 data URI,塞回 prim.src(渲染端同步,无法 fetch)
async function resolveHttpImages(prims) {
  for (const p of prims) {
    if (p.kind !== "image" || !p.src || p.src.startsWith("data:") || p.src.startsWith("file://")) continue;
    if (!/^https?:\/\//.test(p.src)) continue;
    try {
      const res = await fetch(p.src);
      if (!res.ok) { p.src = null; continue; }
      const buf = Buffer.from(await res.arrayBuffer());
      const mime = res.headers.get("content-type") || "image/png";
      p.src = (mime.split(";")[0] || "image/png") + ";base64," + buf.toString("base64");
    } catch (e) {
      p.src = null; // 取失败:渲染端跳过
    }
  }
}

// P2 2.6:解析媒体文件路径(相对 HTML 页面 → 绝对路径)并读取为 data URI
// poster(如有)已在 capturePass 截图为 __posterData;此处仅解析媒体文件本身
async function resolveMediaFiles(prims, pageUrl) {
  const fs = require("fs");
  const path = require("path");
  const pageDir = path.dirname(pageUrl.replace("file://", ""));
  const MIME_BY_EXT = {
    mp4: "video/mp4", webm: "video/webm", ogv: "video/ogg", mov: "video/quicktime",
    mp3: "audio/mpeg", wav: "audio/wav", ogg: "audio/ogg", m4a: "audio/mp4",
  };
  for (const p of prims) {
    if (p.kind !== "media" || !p.hasMedia || !p.src) continue;
    if (p.src.startsWith("data:")) { p.__resolvedData = p.src; continue; }
    // 解析相对路径 → 绝对路径
    let absPath;
    if (p.src.startsWith("file://")) {
      absPath = p.src.replace("file://", "");
    } else if (path.isAbsolute(p.src)) {
      absPath = p.src;
    } else {
      absPath = path.resolve(pageDir, p.src);
    }
    if (!fs.existsSync(absPath)) {
      console.warn(`⚠️  媒体文件不存在: ${p.src}`);
      p.hasMedia = false;
      continue;
    }
    const ext = path.extname(absPath).slice(1).toLowerCase();
    const mime = MIME_BY_EXT[ext] || "application/octet-stream";
    const buf = fs.readFileSync(absPath);
    p.__resolvedData = `data:${mime};base64,${buf.toString("base64")}`;
    p.__resolvedPath = absPath;
  }
}

async function convert(baseDir, playlistFile, outFile, overrides) {
  const config = resolveConfig(overrides);
  const rawPlaylist = JSON.parse(fs.readFileSync(playlistFile, "utf-8")).playlist;
  if (!Array.isArray(rawPlaylist))
    throw new Error(`${playlistFile} 格式错误: playlist 必须是数组`);
  // 2.2 转场:playlist 项支持字符串("01.html")或对象({file, transition})
  // transition: fade/push/wipe/cover/split(不区分大小写);缺省 = 无转场
  const playlist = rawPlaylist.map((item) =>
    typeof item === "string" ? { file: item, transition: null } : { file: item.file, transition: item.transition || null }
  );
  if (playlist.some((it) => !it.file || typeof it.file !== "string"))
    throw new Error(`${playlistFile} 格式错误: playlist 项必须是字符串或 {file, transition} 对象`);
  const { browser, page } = await launchPage(config);

  const pptx = new PptxGenJS();
  pptx.defineLayout({
    name: config.layout.name,
    width: config.slide.widthIn,
    height: config.slide.heightIn,
  });
  pptx.layout = config.layout.name;

  const allGradMaps = []; // P2 1.6:收集所有页的渐变映射,writeFile 后做 XML 后处理
  const slideTransitions = []; // P2 2.2:每页转场类型(索引对齐 slide 序号)

  // P2 2.8:增量缓存目录(与 playlist 同级的 .cache/)
  const cacheDir = path.join(path.dirname(path.resolve(playlistFile)), ".cache");
  const useCache = config.incrementalCache !== false; // 默认开;config.incrementalCache:false 可关闭

  // P2 2.1:母版(defineSlideMaster 承接页码;页脚逐页 addText)
  // pptxgenjs 4.0.1 的 defineSlideMaster.objects 不写入 XML(bug),故页脚用逐页 addText 兜底
  let masterName = null;
  if (config.master && (config.master.pageNumbers || config.master.footer)) {
    masterName = "htmlSlidesMaster";
    const masterOpts = { title: masterName, background: { color: "FFFFFF" } };
    // 页码:用 slideNumber 属性创建 sldNum 占位符(实测有效)
    if (config.master.pageNumbers) {
      masterOpts.slideNumber = {
        x: config.slide.widthIn - 1.2,
        y: config.slide.heightIn - 0.5,
        w: 1.0,
        h: 0.3,
        fontSize: 10,
        color: config.master.footerColor || "999999",
        align: "right",
      };
    }
    pptx.defineSlideMaster(masterOpts);
  }

  for (const item of playlist) {
    const file = item.file;
    const fp = path.resolve(baseDir, file);
    if (!fs.existsSync(fp)) {
      console.warn(`⚠️  playlist 中的文件不存在,已跳过: ${file}`);
      continue;
    }

    // P2 2.8:增量缓存 —— 命中则跳过浏览器交互,直接用缓存数据渲染
    const htmlContent = fs.readFileSync(fp, "utf-8");
    const cacheKey = useCache ? computeCacheKey(htmlContent, config) : null;
    let cached = useCache ? loadCache(cacheDir, cacheKey) : null;

    let withCaptures, notes, canvasBg;
    if (cached) {
      // 缓存命中:跳过加载/提取/截图,直接用缓存数据
      withCaptures = cached.withCaptures;
      notes = cached.notes;
      canvasBg = cached.canvasBg;
      console.log(`✓ ${file} (${withCaptures.length} objects) [cached]${item.transition ? ` [${item.transition}]` : ""}`);
    } else {
      // 缓存未命中:完整提取流程
      await gotoSettled(page, "file://" + fp);
      // 先等 webfont 就绪(封顶 2s 防挂起),再等 settleMs 让 CSS 稳定
      await Promise.race([
        page.evaluate(() => (document.fonts && document.fonts.ready ? document.fonts.ready.then(() => true) : true)),
        page.waitForTimeout(2000),
      ]);
      await page.waitForTimeout(config.settleMs);

      await prepareExtraction(page); // 注入 + data-layout 解析(无则 no-op)
      // nativeGradient 是顶层 config 键,但 extract 端需要读取 → 合并进 extract cfg
      const extractCfg = { ...config.extract, nativeGradient: config.nativeGradient };
      const extractResult = await page.evaluate(
        (cfg) => window.__htmlSlides.extract(cfg),
        extractCfg
      );
      const prims = extractResult.prims;
      notes = extractResult.notes;
      canvasBg = extractResult.canvasBg;

      // 渐变/图片背景:全画布截图还原。检测 .slide-container 是否有 background-image
      const hasComplexBg = await page.evaluate(() => {
        const el = document.querySelector(".slide-container") || document.body;
        const bg = getComputedStyle(el).backgroundImage;
        return bg && bg !== "none";
      });
      if (hasComplexBg) {
        prims.unshift({ kind: "capture", rect: { x: 0, y: 0, w: config.canvas.width, h: config.canvas.height }, reason: "slide-bg" });
      }

      withCaptures = await capturePass(page, prims, config);

      // 预解析 http(s) 图片为 data URI(渲染端同步调用,无法 fetch;file:///data: 由渲染端处理)
      await resolveHttpImages(withCaptures);
      // P2 2.6:解析媒体文件(相对 HTML → 绝对路径 → data URI)
      await resolveMediaFiles(withCaptures, "file://" + fp);

      // 缓存写入
      if (useCache) saveCache(cacheDir, cacheKey, { withCaptures, notes, canvasBg });
      console.log(`✓ ${file} (${withCaptures.length} objects)${item.transition ? ` [${item.transition}]` : ""}`);
    }

    // 分离全画布背景 capture 与内容 prims
    let contentPrims = withCaptures;
    const slide = pptx.addSlide({ masterName: masterName || undefined });
    // 纯色底色
    slide.background = { color: canvasBg || "FFFFFF" };
    // 渐变/图片背景:截图为图片作为幻灯片背景(powerpoint 原生支持)
    if (withCaptures.length > 0 && withCaptures[0].reason === "slide-bg" && withCaptures[0].__img) {
      slide.background = { data: withCaptures[0].__img };
      contentPrims = withCaptures.slice(1); // 移除背景 capture,其余正常渲染
    }
    renderAll(slide, contentPrims, config, allGradMaps);

    // P2 2.1:页脚逐页 addText(defineSlideMaster.objects 在 pptxgenjs 4.0.1 不写入 XML,故兜底)
    if (config.master && config.master.footer) {
      slide.addText(config.master.footer, {
        x: 0,
        y: config.slide.heightIn - 0.4,
        w: config.slide.widthIn,
        h: 0.3,
        fontSize: 9,
        color: config.master.footerColor || "999999",
        align: "center",
        valign: "middle",
        margin: 0,
      });
    }

    if (notes) slide.addNotes(notes);
    slideTransitions.push(item.transition);
  }

  await browser.close();
  await pptx.writeFile({ fileName: outFile });
  // P2 修复:pptxgenjs 4.0.1 chart 引用用了绝对路径 Target="/ppt/..."(PowerPoint 报"需要修复"),
  // 必须先于其他后处理(或其他后处理可能干扰 rels),统一修正为相对路径
  await postProcessChartPaths(outFile);
  // P2 1.6:原生线性渐变后处理 —— 替换占位色 solidFill 为 a:gradFill
  if (config.nativeGradient) {
    await postProcessGradient(outFile, allGradMaps);
  }
  // P2 2.2:转场动画后处理 —— 注入 p:transition 到每页 slide XML
  if (slideTransitions.some((t) => t)) {
    await postProcessTransitions(outFile, slideTransitions);
  }
  console.log(`✅ 导出完成: ${outFile}`);
}

module.exports = { convert };
