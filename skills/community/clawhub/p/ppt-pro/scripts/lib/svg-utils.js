/**
 * SVG computed-style inlining utilities for browser-injected DOM analysis.
 * PowerPoint / OOXML ignores CSS class-based styling on embedded SVGs,
 * so all computed styles must be inlined as presentation attributes.
 *
 * Exposed on window.__pptLib.svg — consumed by dom-analyzer.js.
 *
 * Ref: SVG 1.1 §6.4 Presentation Attributes
 * Ref: https://stackoverflow.com/questions/6042550 (rgba in SVG)
 */
(function () {
  "use strict";

  const ns = (window.__pptLib = window.__pptLib || {});
  const { toSvgHexAlpha } = ns.color;

  // SVG CSS properties that need inlining for PowerPoint compatibility
  const STYLE_PROPS = [
    "fill", "stroke", "stroke-width", "stroke-dasharray", "stroke-linecap",
    "stroke-linejoin", "stroke-opacity", "fill-opacity", "opacity",
    "color", "font-size", "font-family", "font-weight", "text-anchor",
    "dominant-baseline", "letter-spacing", "visibility", "display",
    "stop-color", "stop-opacity", "fill-rule", "clip-rule",
  ];

  // Default browser values — skip inlining when equal (avoids bloat)
  const DEFAULTS = {
    "fill": "rgb(0, 0, 0)", "stroke": "none", "stroke-width": "1px",
    "stroke-dasharray": "none", "stroke-linecap": "butt",
    "stroke-linejoin": "miter", "stroke-opacity": "1",
    "fill-opacity": "1", "opacity": "1", "visibility": "visible",
    "display": "inline", "stop-color": "rgb(0, 0, 0)", "stop-opacity": "1",
    "fill-rule": "nonzero", "clip-rule": "nonzero",
    "font-weight": "400", "text-anchor": "start",
    "dominant-baseline": "auto", "letter-spacing": "normal",
  };

  // Properties that must also be set as DOM attributes (not just style)
  const PRES_ATTRS = new Set([
    "fill", "stroke", "stroke-width", "stroke-dasharray", "stroke-linecap",
    "stroke-linejoin", "stroke-opacity", "fill-opacity", "opacity",
    "font-size", "font-family", "font-weight", "text-anchor",
    "dominant-baseline", "letter-spacing", "visibility",
    "stop-color", "stop-opacity", "fill-rule", "clip-rule",
  ]);

  // Color properties that need their alpha split into a separate opacity attr
  const COLOR_TO_OPACITY = {
    "fill":       "fill-opacity",
    "stroke":     "stroke-opacity",
    "stop-color": "stop-opacity",
  };
  const COLOR_PROPS = new Set(["fill", "stroke", "stop-color", "color"]);

  function inlineOnElement(el) {
    const cs = window.getComputedStyle(el);
    for (const prop of STYLE_PROPS) {
      let val = cs.getPropertyValue(prop);
      if (!val || val === "" || val === "initial" || val === "inherit") continue;
      const defaultVal = DEFAULTS[prop];
      const attrVal = el.getAttribute(prop);
      if (defaultVal && val === defaultVal && !attrVal) continue;
      if (COLOR_PROPS.has(prop)) {
        const parsed = toSvgHexAlpha(val);
        val = parsed.hex;
        const opacityProp = COLOR_TO_OPACITY[prop];
        if (opacityProp && parsed.alpha < 1) {
          const alphaStr = String(Math.round(parsed.alpha * 1000) / 1000);
          el.style.setProperty(opacityProp, alphaStr);
          if (PRES_ATTRS.has(opacityProp)) {
            el.setAttribute(opacityProp, alphaStr);
          }
        }
      }
      el.style.setProperty(prop, val);
      if (PRES_ATTRS.has(prop)) {
        el.setAttribute(prop, val);
      }
    }
  }

  /**
   * Inline all computed SVG styles as presentation attributes on svgEl
   * and all its descendants. Required because OOXML strips CSS classes.
   */
  function inlineSvgStyles(svgEl) {
    for (const child of svgEl.querySelectorAll("*")) {
      if (child.nodeType === 1) inlineOnElement(child);
    }
    inlineOnElement(svgEl);
  }

  ns.svg = { inlineSvgStyles };
})();
