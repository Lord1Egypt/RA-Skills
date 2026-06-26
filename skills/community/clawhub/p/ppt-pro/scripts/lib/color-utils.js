/**
 * Unified color parsing utilities for browser-injected DOM analysis.
 * Consolidates rgba/srgb parsing that was duplicated across dom-analyzer.js.
 *
 * Exposed on window.__pptLib.color — consumed by dom-analyzer.js and svg-utils.js.
 *
 * Ref: CSS Color Level 4 — w3.org/TR/css-color-4/#color-function
 * Ref: CSS Color Level 4 Serialization — w3.org/TR/css-color-4/#serializing-color-values
 */
(function () {
  "use strict";

  const ns = (window.__pptLib = window.__pptLib || {});

  // ── Regex ────────────────────────────────────────────────────────
  // Legacy rgb()/rgba(): rgb(R, G, B) or rgba(R, G, B, A)
  const RGBA_RE = /^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)$/;
  // CSS Color Level 4: color(srgb r g b) or color(srgb r g b / a)
  const SRGB_RE = /^color\(\s*srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\s*\)$/;

  // ── Helpers ──────────────────────────────────────────────────────

  function channelsToHex(r, g, b) {
    return ((1 << 24) | (r << 16) | (g << 8) | b)
      .toString(16).slice(1).toUpperCase();
  }

  function isTransparent(color) {
    return !color || color === "transparent" ||
      color === "rgba(0, 0, 0, 0)" || color === "inherit";
  }

  /**
   * Parse any CSS color string into {r, g, b, a}.
   * Returns null for transparent / unparseable.
   */
  function parseRGBA(color) {
    if (isTransparent(color)) return null;

    if (color.startsWith("#")) {
      let h = color.slice(1).toUpperCase();
      if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
      return {
        r: parseInt(h.slice(0, 2), 16),
        g: parseInt(h.slice(2, 4), 16),
        b: parseInt(h.slice(4, 6), 16),
        a: 1,
      };
    }

    const srgb = color.match(SRGB_RE);
    if (srgb) {
      const a = srgb[4] !== undefined ? parseFloat(srgb[4]) : 1;
      return {
        r: Math.round(parseFloat(srgb[1]) * 255),
        g: Math.round(parseFloat(srgb[2]) * 255),
        b: Math.round(parseFloat(srgb[3]) * 255),
        a,
      };
    }

    const m = color.match(RGBA_RE);
    if (m) {
      return {
        r: parseInt(m[1]),
        g: parseInt(m[2]),
        b: parseInt(m[3]),
        a: m[4] !== undefined ? parseFloat(m[4]) : 1,
      };
    }

    const nums = color.match(/[\d.]+/g);
    if (nums && nums.length >= 3) {
      return {
        r: parseInt(nums[0]),
        g: parseInt(nums[1]),
        b: parseInt(nums[2]),
        a: nums.length > 3 ? parseFloat(nums[3]) : 1,
      };
    }

    return null;
  }

  // ── Public API (replaces rgbToHex, parseColorWithAlpha, parseCssColor, svgColorToHexAlpha) ──

  /**
   * Convert CSS color string → 6-char uppercase hex (no #). Empty string if transparent.
   * Replaces: rgbToHex
   */
  function toHex(color) {
    const c = parseRGBA(color);
    if (!c || c.a === 0) return "";
    return channelsToHex(c.r, c.g, c.b);
  }

  /**
   * Convert CSS color string → { hex: "RRGGBB", alpha: 0-1 }.
   * Replaces: parseColorWithAlpha, parseCssColor
   */
  function toHexAlpha(color) {
    const c = parseRGBA(color);
    if (!c || c.a === 0) return { hex: "", alpha: c ? 0 : 1 };
    return { hex: channelsToHex(c.r, c.g, c.b), alpha: c.a };
  }

  /**
   * Convert CSS color string → { hex: "#RRGGBB", alpha: 0-1 }.
   * Returns raw string as hex when unparseable (SVG named colors etc.).
   * Replaces: svgColorToHexAlpha
   */
  function toSvgHexAlpha(color) {
    const c = parseRGBA(color);
    if (!c) return { hex: color, alpha: 1 };
    return { hex: "#" + channelsToHex(c.r, c.g, c.b), alpha: c.a };
  }

  // ── Export ────────────────────────────────────────────────────────
  ns.color = {
    RGBA_RE,
    SRGB_RE,
    parseRGBA,
    toHex,
    toHexAlpha,
    toSvgHexAlpha,
  };
})();
