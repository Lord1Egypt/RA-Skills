/**
 * HTML <table> → structured region extractor for PPTX native table conversion.
 * Runs in Puppeteer page context; reads computed styles before text is hidden.
 *
 * Exposed on window.__pptLib.table — consumed by dom-analyzer.js.
 */
(function () {
  "use strict";

  const ns = (window.__pptLib = window.__pptLib || {});
  const { toHexAlpha } = ns.color;
  const { pxToPt } = ns.K;

  function parseColor(str) {
    const r = toHexAlpha(str);
    if (!r.hex && r.alpha === 1) return { hex: "000000", alpha: 0 };
    return r;
  }

  /**
   * Scan all <table> elements wrapped in [data-pptx-role] containers.
   * Returns array of tableRegion objects with rows/cells/styling data.
   */
  function extractTables() {
    const tableRegions = [];

    document.querySelectorAll("table").forEach(function (tableEl) {
      const wrap = tableEl.closest("[data-pptx-role]");
      if (!wrap) return;
      const wrapRect = wrap.getBoundingClientRect();
      if (wrapRect.width < 50 || wrapRect.height < 50) return;

      const rows = [];
      for (const tr of tableEl.querySelectorAll("tr")) {
        const cells = [];
        for (const cell of tr.querySelectorAll("th, td")) {
          const cs = window.getComputedStyle(cell);
          const cellRect = cell.getBoundingClientRect();
          const textContent = cell.innerText.trim();
          const parsed = parseColor(cs.color || "");
          const bgParsed = parseColor(cs.backgroundColor || "rgba(0,0,0,0)");
          const cellFsPx = parseFloat(cs.fontSize) || 12;
          cells.push({
            text: textContent,
            isHeader: cell.tagName === "TH",
            fontSizePx: cellFsPx,
            fontSizePt: pxToPt(cellFsPx),
            fontWeight: parseInt(cs.fontWeight) || 400,
            color: parsed.hex,
            colorAlpha: Math.round(parsed.alpha * 100000),
            bgColor: bgParsed.hex,
            bgAlpha: Math.round(bgParsed.alpha * 100000),
            widthPx: cellRect.width,
          });
        }
        rows.push(cells);
      }

      if (rows.length >= 2 && rows[0].length >= 2) {
        tableRegions.push({
          x: wrapRect.left, y: wrapRect.top,
          w: wrapRect.width, h: wrapRect.height,
          rows: rows,
          cols: rows[0].length,
          rowCount: rows.length,
        });
      }
    });

    return tableRegions;
  }

  ns.table = { extractTables };
})();
