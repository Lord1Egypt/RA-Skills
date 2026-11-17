// render/media-renderer.js — media 基元 → 原生 addMedia(2026-07-27 P2 2.6)
// video/audio → slide.addMedia({type, path/data, x, y, w, h, cover})
// 本地文件路径由 pipeline 预解析为绝对路径(渲染端同步读文件为 base64 data)
const fs = require("fs");
const path = require("path");

const MIME_BY_EXT = {
  mp4: "video/mp4", webm: "video/webm", ogv: "video/ogg", mov: "video/quicktime",
  mp3: "audio/mpeg", wav: "audio/wav", ogg: "audio/ogg", m4a: "audio/mp4",
};

function renderMedia(slide, p, units, config) {
  if (!p.hasMedia && !p.poster) return; // 无 src 且无 poster → 跳过

  const opts = {
    x: units.px(p.rect.x),
    y: units.px(p.rect.y),
    w: units.px(p.rect.w),
    h: units.px(p.rect.h),
    type: p.mediaType, // 'video' | 'audio'
  };

  // 解析 src 为 data URI(渲染端同步,需读文件)
  if (p.src && p.__resolvedData) {
    opts.data = p.__resolvedData; // pipeline 预解析的 data URI
  } else if (p.src && p.__resolvedPath) {
    opts.path = p.__resolvedPath; // 绝对路径
  }

  // 封面:poster 已被 capturePass 截图为 data URI
  if (p.__posterData) {
    opts.cover = p.__posterData;
  }

  try {
    slide.addMedia(opts);
  } catch (e) {
    // addMedia 失败(文件不存在/格式不支持)→ 静默跳过,不阻断转换
    console.warn(`⚠️  媒体嵌入失败: ${p.src || "(无src)"} - ${e.message}`);
  }
}

module.exports = { renderMedia };
