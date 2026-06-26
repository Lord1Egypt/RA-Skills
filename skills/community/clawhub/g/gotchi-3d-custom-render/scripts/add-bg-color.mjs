#!/usr/bin/env node

import fs from "node:fs";
import { PNG } from "pngjs";

function parseHexColor(raw) {
  const value = String(raw || "").trim().replace(/^#/, "");
  const normalized = value.length === 3
    ? value.split("").map((char) => `${char}${char}`).join("")
    : value;

  if (!/^[0-9a-fA-F]{6}$/.test(normalized)) {
    throw new Error(`Unsupported hex color: ${raw}`);
  }

  return {
    r: Number.parseInt(normalized.slice(0, 2), 16),
    g: Number.parseInt(normalized.slice(2, 4), 16),
    b: Number.parseInt(normalized.slice(4, 6), 16)
  };
}

function blendPixel(fg, bg) {
  const alpha = fg.a / 255;
  const invAlpha = 1 - alpha;
  return {
    r: Math.round((fg.r * alpha) + (bg.r * invAlpha)),
    g: Math.round((fg.g * alpha) + (bg.g * invAlpha)),
    b: Math.round((fg.b * alpha) + (bg.b * invAlpha)),
    a: 255
  };
}

export function applySolidBackground(inputPath, outputPath, hexColor) {
  const input = PNG.sync.read(fs.readFileSync(inputPath));
  const background = parseHexColor(hexColor);
  const output = new PNG({ width: input.width, height: input.height });

  for (let offset = 0; offset < input.data.length; offset += 4) {
    const blended = blendPixel({
      r: input.data[offset],
      g: input.data[offset + 1],
      b: input.data[offset + 2],
      a: input.data[offset + 3]
    }, background);

    output.data[offset] = blended.r;
    output.data[offset + 1] = blended.g;
    output.data[offset + 2] = blended.b;
    output.data[offset + 3] = blended.a;
  }

  fs.writeFileSync(outputPath, PNG.sync.write(output));
}
