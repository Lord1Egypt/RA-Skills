import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
let data;
try {
  data = JSON.parse(
    fs.readFileSync(path.join(here, "../tokens/themes.json"), "utf8"),
  );
} catch (error) {
  const code = error instanceof SyntaxError
    ? "INVALID_JSON"
    : error?.code ?? "READ_FAILED";
  console.error(`theme contrast input is unavailable: ${code}`);
  process.exit(2);
}

function rgb(hex) {
  const value = hex.replace("#", "");
  return [0, 2, 4].map((i) => parseInt(value.slice(i, i + 2), 16) / 255);
}
function luminance(hex) {
  return rgb(hex).map((c) => c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)
    .reduce((sum, c, i) => sum + c * [0.2126, 0.7152, 0.0722][i], 0);
}
function contrast(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

// Keep these thresholds aligned with 02-剪辑方法手册/03-主题配色.md.
// Body/secondary/CTA copy may render at phone-scale, so they use the
// repository's stricter 7:1 internal target. Emphasis is headline-only.
const INTERNAL_THRESHOLDS = Object.freeze({
  bodyText: 7,
  secondaryText: 7,
  headline: 4.5,
  ctaText: 7,
});

let failed = false;
for (const theme of data.themes) {
  const s = theme.semantic;
  const checks = [
    ["正文", s.textPrimary, s.canvas, INTERNAL_THRESHOLDS.bodyText],
    ["次级文字", s.textSecondary, s.canvas, INTERNAL_THRESHOLDS.secondaryText],
    ["大字号强调", s.emphasis, s.canvas, INTERNAL_THRESHOLDS.headline],
    ["CTA", s.ctaText, s.ctaBackground, INTERNAL_THRESHOLDS.ctaText],
  ];
  console.log(`\n${theme.index} ${theme.name}`);
  for (const [label, fg, bg, min] of checks) {
    const ratio = contrast(fg, bg);
    const ok = ratio >= min;
    console.log(`${ok ? "PASS" : "FAIL"}  ${label.padEnd(8)} ${ratio.toFixed(2)}:1  ${fg} / ${bg}`);
    if (!ok) failed = true;
  }
}
if (failed) process.exitCode = 1;
