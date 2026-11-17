// core/capture-pass.js — 渐变/图片/SVG 区域截图(红线③:截图前先隐藏文字)
// 不可变:返回新的 prims 数组,不改传入数组;capture 基元补上 __img/__clip。
async function capturePass(page, prims, config) {
  // 截图前把页面里所有文字临时变透明(保留渐变/图片/底色),
  // 否则叠在渐变上的文字会被烙进 PNG,再叠加可编辑文本框时就会重复。
  await page.evaluate((css) => {
    const st = document.createElement("style");
    st.id = "__capHideText";
    st.textContent = css;
    document.head.appendChild(st);
  }, config.capture.hideTextCss + " [data-keep-text]{color:unset !important;}");

  // 无 data-keep-text 的 bgclip:text 元素:移除渐变背景(否则 color:transparent
  // 的文字仍通过 bgclip 可见,且 background-clip:border-box 会产生渐变矩形)。
  // 直接设为 background:none,文字和矩形都不会出现。
  await page.evaluate(() => {
    document.querySelectorAll("*").forEach((el) => {
      if (el.hasAttribute("data-keep-text")) return;
      const clip = (el.style.getPropertyValue("-webkit-background-clip")
        || el.style.getPropertyValue("background-clip") || "").toLowerCase();
      if (clip !== "text") return;
      el.setAttribute("data-cap-bg", el.style.background || "");
      el.style.setProperty("background", "none", "important");
    });
  });

  const W = config.canvas.width, H = config.canvas.height;
  const out = [];
  for (const p of prims) {
    if (p.kind !== "capture") {
      out.push(p);
      continue;
    }
    // 截图区域与画布求交集:Playwright 会把 clip 钳制到视口内,若元素超出画布,
    // 直接截原始 rect 会得到被裁小的图,再按原尺寸贴回就会拉伸错位 —— 只截/只贴可见部分
    const ix = Math.max(0, p.rect.x), iy = Math.max(0, p.rect.y);
    const iw = Math.min(W, p.rect.x + p.rect.w) - ix;
    const ih = Math.min(H, p.rect.y + p.rect.h) - iy;
    if (iw < 1 || ih < 1) {
      out.push({ ...p, __img: null }); // 完全在画布外,不可见
      continue;
    }
    const buf = await page.screenshot({
      clip: { x: ix, y: iy, width: iw, height: ih },
      type: config.capture.imageType === "jpeg" ? "jpeg" : "png",
      ...(config.capture.imageType === "jpeg" ? { quality: config.capture.quality } : {}),
    });
    out.push({
      ...p,
      __img: "image/" + (config.capture.imageType === "jpeg" ? "jpeg" : "png") + ";base64," + buf.toString("base64"),
      __clip: { x: ix, y: iy, w: iw, h: ih },
    });
  }

  // P2 2.6:video poster 截图作为 addMedia 的 cover
  // video 元素本身在浏览器中渲染 poster 帧 → 截取该区域作为封面
  for (const p of prims) {
    if (p.kind !== "media" || p.mediaType !== "video") continue;
    const ix = Math.max(0, p.rect.x), iy = Math.max(0, p.rect.y);
    const iw = Math.min(W, p.rect.x + p.rect.w) - ix;
    const ih = Math.min(H, p.rect.y + p.rect.h) - iy;
    if (iw < 1 || ih < 1) continue;
    try {
      const buf = await page.screenshot({
        clip: { x: ix, y: iy, width: iw, height: ih },
        type: "png",
      });
      p.__posterData = "image/png;base64," + buf.toString("base64");
    } catch (e) { /* 截图失败:用默认封面 */ }
  }

  // 恢复:移除隐藏文字的 style + 恢复渐变背景
  await page.evaluate(() => {
    const st = document.getElementById("__capHideText");
    if (st) st.remove();
    document.querySelectorAll("[data-cap-bg]").forEach((el) => {
      el.style.background = el.getAttribute("data-cap-bg");
      el.removeAttribute("data-cap-bg");
    });
  });
  return out;
}

module.exports = { capturePass };
