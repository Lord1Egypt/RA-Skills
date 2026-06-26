import { createCanvas, loadImage } from "@napi-rs/canvas";

/**
 * Render a PNG image as ANSI true-color art using half-block characters (▀).
 * Each character cell represents 2 vertical pixels: foreground = top, background = bottom.
 */
export async function renderAnsiFromImage(
  imagePath: string,
  targetWidth?: number,
): Promise<string> {
  const img = await loadImage(imagePath);
  const { width, height } = img;

  const w = targetWidth ?? Math.min(process.stdout.columns || 80, 72);
  const scale = w / width;
  const h = Math.round(height * scale);
  const evenH = h % 2 === 0 ? h : h + 1;

  const canvas = createCanvas(w, evenH);
  const ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0, w, evenH);

  const { data } = ctx.getImageData(0, 0, w, evenH);
  const lines: string[] = [];

  for (let y = 0; y < evenH; y += 2) {
    let line = "";
    let prevFg = "";
    let prevBg = "";

    for (let x = 0; x < w; x++) {
      const ti = (y * w + x) * 4;
      const bi = ((y + 1) * w + x) * 4;

      const fg = `${data[ti]};${data[ti + 1]};${data[ti + 2]}`;
      const bg = `${data[bi]};${data[bi + 1]};${data[bi + 2]}`;

      let esc = "";
      if (fg !== prevFg) esc += `\x1b[38;2;${fg}m`;
      if (bg !== prevBg) esc += `\x1b[48;2;${bg}m`;
      line += esc + "▀";

      prevFg = fg;
      prevBg = bg;
    }

    line += "\x1b[0m";
    lines.push(line);
  }

  return lines.join("\n");
}
