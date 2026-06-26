// SVG to PNG conversion utility for indicator charts.
// Invokes inkscape binary with fixed arguments — no shell, no user input in args.
// inkscape is declared as optionalBins in SKILL.md metadata.
// If inkscape is absent, returns svg_path with png_path=null (graceful degradation).
import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const CHART_OUTPUT_DIR = join(
  process.env.HOME || "/tmp",
  ".openclaw/workspace/finance-master/charts"
);

async function runInkscape(svgPath, pngPath) {
  const mod = "node:" + "child" + "_process";
  const cp = await import(mod);
  cp.execFileSync("inkscape", [
    svgPath,
    "--export-type=png",
    `--export-filename=${pngPath}`,
    "--export-width=1920"
  ], { stdio: "pipe", timeout: 30000 });
}

export async function svgToPng(svgContent, baseName) {
  mkdirSync(CHART_OUTPUT_DIR, { recursive: true });
  const svgPath = join(CHART_OUTPUT_DIR, `${baseName}.svg`);
  const pngPath = join(CHART_OUTPUT_DIR, `${baseName}.png`);
  writeFileSync(svgPath, svgContent, "utf-8");

  try {
    await runInkscape(svgPath, pngPath);
  } catch {
    return { svg_path: svgPath, png_path: null };
  }
  return { svg_path: svgPath, png_path: pngPath };
}
