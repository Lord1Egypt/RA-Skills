// core/post-process.js — PPTX 写入后处理:将占位色 solidFill 替换为 a:gradFill
// 2026-07-27 P2 1.6:pptxgenjs 4.0.1 不支持渐变填充,渲染端用占位色画形状,
// 此模块在 pptxgenjs.writeFile 后读取 PPTX(JSZip),替换占位色为原生渐变 XML。
const fs = require("fs");
const JSZip = require("jszip");

// 构建 a:gradFill XML
// angle: PPTX 角度(60000ths of degree);stops: [{pos(0-100000), color(HEX)}]
function buildGradFillXml(g) {
  const stops = g.stops
    .map((s) => `<a:gs pos="${Math.round(s.pos)}"><a:srgbClr val="${s.color}"/></a:gs>`)
    .join("");
  return `<a:gradFill><a:gsLst>${stops}</a:gsLst><a:lin ang="${Math.round(g.angle)}" scaled="1"/></a:gradFill>`;
}

// 替换 slide XML 中的占位色 solidFill 为 gradFill
function replaceInXml(xml, gradMap) {
  for (const g of gradMap) {
    const gradFill = buildGradFillXml(g);
    // 匹配 <a:solidFill><a:srgbClr val="FEXXXX"/>...</a:solidFill>
    // 支持自闭合(无 alpha)和含 alpha 两种写法;占位色唯一,不会误伤
    const re = new RegExp(
      `<a:solidFill><a:srgbClr val="${g.placeholder}".*?</a:solidFill>`,
      "g"
    );
    xml = xml.replace(re, gradFill);
  }
  return xml;
}

async function postProcessGradient(outFile, gradMap) {
  if (!gradMap || gradMap.length === 0) return; // 无渐变 → 跳过
  const buf = fs.readFileSync(outFile);
  const zip = await JSZip.loadAsync(buf);
  let modified = 0;
  for (const [path, file] of Object.entries(zip.files)) {
    if (file.dir) continue;
    if (!/^ppt\/slides\/slide\d+\.xml$/.test(path)) continue;
    let xml = await file.async("string");
    const before = xml;
    xml = replaceInXml(xml, gradMap);
    if (xml !== before) {
      zip.file(path, xml);
      modified++;
    }
  }
  if (modified > 0) {
    const out = await zip.generateAsync({ type: "nodebuffer" });
    fs.writeFileSync(outFile, out);
  }
}

// P2 2.2:转场动画后处理 —— 注入 p:transition 到每页 slide XML
// transitions: 数组,索引对齐 slide 序号(从 1 开始);每项为 fade/push/wipe/cover/split 或 null
// 注意:<p:transition> 不带 xmlns:p —— 根元素 <p:sld> 已声明该命名空间,
// 子元素重复声明会导致 PowerPoint 校验失败("需要修复")
const TRANSITION_XML = {
  fade: '<p:transition spd="med"><p:fade/></p:transition>',
  push: '<p:transition spd="med"><p:push dir="l"/></p:transition>',
  wipe: '<p:transition spd="med"><p:wipe dir="l"/></p:transition>',
  cover: '<p:transition spd="med"><p:cover dir="l"/></p:transition>',
  split: '<p:transition spd="med"><p:split orient="horz" dir="out"/></p:transition>',
};

async function postProcessTransitions(outFile, transitions) {
  const buf = fs.readFileSync(outFile);
  const zip = await JSZip.loadAsync(buf);
  let modified = 0;
  for (let i = 0; i < transitions.length; i++) {
    const t = transitions[i];
    if (!t) continue;
    const tLower = String(t).toLowerCase();
    const xml = TRANSITION_XML[tLower];
    if (!xml) continue; // 未知类型跳过
    const slidePath = `ppt/slides/slide${i + 1}.xml`;
    const file = zip.file(slidePath);
    if (!file) continue;
    let slideXml = await file.async("string");
    // 已有 transition → 跳过(不重复注入)
    if (/<p:transition[\s>]/.test(slideXml)) continue;
    // 注入到 </p:cSld> 之后、<p:clrMapOvr> 之前(或 </p:sld> 之前)
    // PowerPoint schema:transition 在 cSld 之后、timing 之前
    if (/<\/p:cSld>/.test(slideXml)) {
      slideXml = slideXml.replace(/<\/p:cSld>/, "</p:cSld>" + xml);
    } else if (/<\/p:sld>/.test(slideXml)) {
      slideXml = slideXml.replace(/<\/p:sld>/, xml + "</p:sld>");
    } else continue;
    zip.file(slidePath, slideXml);
    modified++;
  }
  if (modified > 0) {
    const out = await zip.generateAsync({ type: "nodebuffer" });
    fs.writeFileSync(outFile, out);
  }
}

module.exports = { postProcessGradient, postProcessTransitions, postProcessChartPaths, buildGradFillXml };

// P2 修复:pptxgenjs 4.0.1 的 chart 引用 Target 使用了绝对路径 "/ppt/charts/chart1.xml"
// PowerPoint 不接受这种格式(必须相对路径),导致打开时报"需要修复"。
// 在 rels 文件中将 Target="/ppt/..." 替换为相对路径。
// 计算路径深度:从 rels 文件所在目录到包根目录的 "../" 数
function fixAbsolutePathsInRels(relsPath, xml) {
  // rels 文件位于: ppt/slides/_rels/slideN.xml.rels (深度 2,从包根)
  // 或: ppt/charts/_rels/chart1.xml.rels (深度 2)
  // 计算"从 rels 所在目录到包根"的相对路径:每层 1 个 "../"
  const dirParts = relsPath.split("/");
  const relsIdx = dirParts.indexOf("_rels");
  const depth = relsIdx; // _rels 之前的目录层数
  const upPath = depth > 0 ? "../".repeat(depth) : "";
  // 替换 Target="/ppt/..." 为 Target="<upPath>ppt/..."
  return xml.replace(/Target="\/ppt\//g, `Target="${upPath}ppt/`);
}

async function postProcessChartPaths(outFile) {
  const buf = fs.readFileSync(outFile);
  const zip = await JSZip.loadAsync(buf);
  let modified = 0;
  for (const [path, file] of Object.entries(zip.files)) {
    if (file.dir) continue;
    if (!path.endsWith(".rels")) continue;
    let xml = await file.async("string");
    if (!/Target="\/ppt\//.test(xml)) continue;
    const before = xml;
    xml = fixAbsolutePathsInRels(path, xml);
    if (xml !== before) {
      zip.file(path, xml);
      modified++;
    }
  }
  if (modified > 0) {
    const out = await zip.generateAsync({ type: "nodebuffer" });
    fs.writeFileSync(outFile, out);
  }
  return modified;
}
