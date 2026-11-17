// extract/primitives/media.js — 音视频基元(2026-07-27 P2 2.6)
// <video> → media 基元(type:video,src/poster);<audio> → media 基元(type:audio,src)
// poster 优先用 video.poster 属性;无 poster 时用 data-poster 或留空(渲染端用默认封面)
// 媒体文件路径保留原样(相对 HTML 解析),渲染端解析为绝对路径读文件
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  ns.primitives.media = {
    name: "media",
    emit(el, cs, rect, collector, cfg) {
      const tag = el.tagName.toLowerCase();
      const isVideo = tag === "video";
      const isAudio = tag === "audio";
      if (!isVideo && !isAudio) return;

      // video:poster 属性优先;data-poster 次之;无则留空(渲染端用默认封面)
      let poster = null;
      if (isVideo) {
        poster = el.getAttribute("poster") || el.getAttribute("data-poster") || null;
      }

      // src:video/audio 的 src 属性,或 <source> 子元素的 src
      let src = el.getAttribute("src");
      if (!src) {
        const source = el.querySelector("source");
        if (source) src = source.getAttribute("src");
      }

      collector.push({
        kind: "media",
        mediaType: isVideo ? "video" : "audio",
        rect,
        src: src || null,
        poster: poster,
        // video 无 src 时仍可仅用 poster 做封面(纯展示)
        hasMedia: !!src,
      });
    },
  };
})();
