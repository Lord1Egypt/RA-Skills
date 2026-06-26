import { createCanvas } from "@napi-rs/canvas";
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TILE = 16;
const ASSETS = path.join(__dirname, "..", "assets", "tiles");

interface TileSpec {
  dir: string;
  name: string;
  pixels: [number, number, string][]; // [x, y, hex color]
}

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function drawTile(spec: TileSpec) {
  const canvas = createCanvas(TILE, TILE);
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, TILE, TILE);
  for (const [x, y, color] of spec.pixels) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, 1, 1);
  }

  const dir = path.join(ASSETS, spec.dir);
  ensureDir(dir);
  const buf = canvas.toBuffer("image/png");
  fs.writeFileSync(path.join(dir, `${spec.name}.png`), buf);
}

function rect(x: number, y: number, w: number, h: number, color: string): [number, number, string][] {
  const pixels: [number, number, string][] = [];
  for (let dx = 0; dx < w; dx++) {
    for (let dy = 0; dy < h; dy++) {
      pixels.push([x + dx, y + dy, color]);
    }
  }
  return pixels;
}

function terrainTiles() {
  // empty plot - brown soil
  drawTile({
    dir: "terrain",
    name: "empty",
    pixels: [
      ...rect(0, 0, 16, 16, "#8B6914"),
      ...rect(1, 1, 14, 14, "#A0782C"),
      ...rect(3, 7, 2, 1, "#8B6914"),
      ...rect(8, 4, 2, 1, "#8B6914"),
      ...rect(12, 10, 2, 1, "#8B6914"),
      ...rect(5, 12, 2, 1, "#8B6914"),
    ],
  });

  // watered plot - darker soil
  drawTile({
    dir: "terrain",
    name: "watered",
    pixels: [
      ...rect(0, 0, 16, 16, "#5C4410"),
      ...rect(1, 1, 14, 14, "#6B5220"),
      ...rect(3, 7, 2, 1, "#4A3A10"),
      ...rect(8, 4, 2, 1, "#4A3A10"),
      ...rect(12, 10, 2, 1, "#4A3A10"),
      ...rect(5, 12, 2, 1, "#4A3A10"),
    ],
  });
}

interface CropColor {
  stem: string;
  body: string;
  accent: string;
}

const CROP_COLORS: Record<string, CropColor> = {
  carrot: { stem: "#2D8B2D", body: "#FF8C00", accent: "#FFA500" },
  potato: { stem: "#2D6B2D", body: "#B58A5A", accent: "#D2A679" },
  tomato: { stem: "#2D8B2D", body: "#E53935", accent: "#FF6F61" },
  pumpkin: { stem: "#2D6B2D", body: "#FF6600", accent: "#FF8C00" },
};

function cropTiles() {
  for (const [cropId, colors] of Object.entries(CROP_COLORS)) {
    // seed stage - small dot in soil
    drawTile({
      dir: "crops",
      name: `${cropId}_seed`,
      pixels: [
        ...rect(0, 0, 16, 16, "#A0782C"),
        ...rect(7, 10, 2, 2, "#5C3A10"),
        ...rect(7, 9, 2, 1, colors.body),
      ],
    });

    // sprout - small green shoot
    drawTile({
      dir: "crops",
      name: `${cropId}_sprout`,
      pixels: [
        ...rect(0, 0, 16, 16, "#A0782C"),
        ...rect(7, 12, 2, 2, "#5C3A10"),
        ...rect(7, 8, 2, 4, colors.stem),
        ...rect(6, 7, 1, 2, colors.stem),
        ...rect(9, 8, 1, 1, colors.stem),
      ],
    });

    // growing stage 1 - medium plant
    drawTile({
      dir: "crops",
      name: `${cropId}_growing_1`,
      pixels: [
        ...rect(0, 0, 16, 16, "#A0782C"),
        ...rect(7, 13, 2, 2, "#5C3A10"),
        ...rect(7, 6, 2, 7, colors.stem),
        ...rect(5, 5, 6, 3, colors.stem),
        ...rect(6, 4, 4, 2, colors.body),
        ...rect(7, 3, 2, 1, colors.accent),
      ],
    });

    // growing stage 2 - almost mature
    drawTile({
      dir: "crops",
      name: `${cropId}_growing_2`,
      pixels: [
        ...rect(0, 0, 16, 16, "#A0782C"),
        ...rect(7, 14, 2, 2, "#5C3A10"),
        ...rect(7, 6, 2, 8, colors.stem),
        ...rect(5, 4, 6, 3, colors.stem),
        ...rect(5, 2, 6, 3, colors.body),
        ...rect(6, 1, 4, 1, colors.accent),
      ],
    });

    // ready - full plant with vibrant crop color
    drawTile({
      dir: "crops",
      name: `${cropId}_ready`,
      pixels: [
        ...rect(0, 0, 16, 16, "#A0782C"),
        ...rect(7, 14, 2, 2, "#5C3A10"),
        ...rect(7, 6, 2, 8, colors.stem),
        ...rect(5, 5, 6, 2, colors.stem),
        ...rect(4, 2, 8, 4, colors.body),
        ...rect(5, 1, 6, 2, colors.accent),
        ...rect(6, 0, 4, 1, colors.accent),
      ],
    });
  }
}

console.log("Generating tiles...");
terrainTiles();
cropTiles();
console.log("Done! Tiles written to assets/tiles/");
