// render/image-renderer.js — image 基元 → 原生可编辑图片(2026-07-27 P1)
// src 解析:file:// → 读文件;http(s):// → fetch;data: → 直传。
// object-fit:contain/cover → pptxgenjs sizing;fill/none/scale-down → 直接 w/h(拉伸/原位)。
const fs = require("fs");
const path = require("path");

const MIME_BY_EXT = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp" };

function resolveImageData(src) {
  if (!src) return null;
  if (src.startsWith("data:")) return src; // 已是 data URI
  if (src.startsWith("file://")) {
    const fp = decodeURIComponent(src.replace("file://", ""));
    const ext = path.extname(fp).toLowerCase();
    const mime = MIME_BY_EXT[ext] || "image/png";
    if (!fs.existsSync(fp)) return null;
    const b64 = fs.readFileSync(fp).toString("base64");
    return mime + ";base64," + b64;
  }
  if (/^https?:\/\//.test(src)) {
    // 同步取不到——渲染端是同步调用;fetch 异步。改在 pipeline 预解析(见 convert 流程)。
    // 此处兜底:返回 null,图片不输出(validate 可提示改用本地 file://)。
    return null;
  }
  return null;
}

function renderImage(slide, p, units, config) {
  const data = resolveImageData(p.src);
  if (!data) return;
  const opts = {
    data,
    x: units.px(p.rect.x),
    y: units.px(p.rect.y),
    w: units.px(p.rect.w),
    h: units.px(p.rect.h),
  };
  const fit = p.fit || "fill";
  if (fit === "cover" || fit === "contain") {
    opts.sizing = { type: fit, w: opts.w, h: opts.h };
  }
  // fill / none / scale-down → 直接按 w/h(拉伸);scale-down 的"小于原尺寸才缩"语义无原生对应,近似 fill
  slide.addImage(opts);
}

module.exports = { renderImage, resolveImageData };
