/**
 * Shared constants for browser-injected DOM analysis modules.
 * Exposed on window.__pptLib.K — consumed by dom-analyzer.js.
 */
(function () {
  "use strict";

  const ns = (window.__pptLib = window.__pptLib || {});

  // 1 CSS px = 0.75 PowerPoint pt (96 dpi vs 72 dpi)
  const CSS_PX_TO_PT = 0.75;

  function pxToPt(px) {
    return Math.round(px * CSS_PX_TO_PT * 100) / 100;
  }

  const SKIP_TAGS = new Set([
    "SVG", "CANVAS", "IMG", "VIDEO", "IFRAME",
    "SCRIPT", "STYLE", "BR", "HR", "NOSCRIPT",
  ]);

  // flow-root is a block formatting context — treated as block
  const BLOCK_DISPLAYS = new Set([
    "block", "flex", "grid", "list-item", "table", "table-cell",
    "table-row", "table-header-group", "table-row-group",
    "table-footer-group", "flow-root", "table-caption",
  ]);

  // HTML tags that are semantically inline — flex/grid "blockifies" their
  // display, but they should still be treated as inline for text extraction
  // (CSS Display L3 §2.5 blockification).
  const INLINE_TAGS = new Set([
    "SPAN", "A", "EM", "STRONG", "B", "I", "U", "S", "MARK", "SMALL",
    "SUB", "SUP", "ABBR", "CITE", "CODE", "KBD", "SAMP", "VAR", "TIME",
    "LABEL", "Q", "DFN", "BDO", "BDI", "RUBY", "DATA", "WBR",
  ]);

  function isArrowChar(ch) {
    const c = ch.codePointAt(0);
    if (c >= 0x2190 && c <= 0x21FF) return true;  // Arrows block
    if (c >= 0x27F0 && c <= 0x27FF) return true;  // Supplemental Arrows-A
    if (c >= 0x2900 && c <= 0x297F) return true;  // Supplemental Arrows-B
    if (c >= 0x2B00 && c <= 0x2B11) return true;  // Misc Symbols arrows
    if (c === 0x27A1) return true;                 // ➡ BLACK RIGHTWARDS ARROW
    // Geometric triangles used as directional indicators
    if ("\u25B2\u25BC\u25C0\u25B6\u25B3\u25BD\u25C1\u25B7".includes(ch)) return true;
    return false;
  }

  const ARROW_CHARS = { has(ch) { return isArrowChar(ch); } };

  ns.K = {
    CSS_PX_TO_PT,
    pxToPt,
    SKIP_TAGS,
    BLOCK_DISPLAYS,
    INLINE_TAGS,
    ARROW_CHARS,
  };
})();
