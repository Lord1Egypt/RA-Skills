import { createCanvas, loadImage } from "@napi-rs/canvas";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";
import { fileURLToPath } from "node:url";
import { FarmState, GrowthStage, PlantedCrop } from "../game/types.js";
import { getStage } from "../game/crops.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
function resolveTilesDir(): string | null {
  const fromEnv = process.env.GRINDERS_FARM_TILES_DIR?.trim();
  const candidates = [
    fromEnv || "",
    // source layout: src/render -> ../../assets/tiles
    path.join(__dirname, "..", "..", "assets", "tiles"),
    // packaged layout: dist/src/render -> ../../../assets/tiles
    path.join(__dirname, "..", "..", "..", "assets", "tiles"),
    path.join(process.cwd(), "assets", "tiles"),
  ]
    .map((p) => p.trim())
    .filter(Boolean);
  for (const dir of candidates) {
    if (fs.existsSync(path.join(dir, "terrain", "empty.png"))) return dir;
  }
  return null;
}
const TILES_DIR = resolveTilesDir();
const TILE = 16;
const SCALE = 4;
const SCALED_TILE = TILE * SCALE;
const CELL_GAP = 18;
const PADDING = 12;
const HEADER_HEIGHT = 40;
const HEADER_TO_GRID_GAP = 10;
const ROW_LABEL_WIDTH = 18;
const COL_LABEL_HEIGHT = 18;
const LABEL_TO_GRID_GAP = 10;
const STAGE_Y_OFFSET_PX: Record<GrowthStage, number> = {
  [GrowthStage.Empty]: 0,
  [GrowthStage.Seed]: -14,
  [GrowthStage.Sprout]: -11,
  [GrowthStage.Growing1]: -8,
  [GrowthStage.Growing2]: -6,
  [GrowthStage.Ready]: -4,
};

const imageCache = new Map<string, Awaited<ReturnType<typeof loadImage>>>();
const cropAnchorCache = new Map<string, { x: number; y: number }>();

async function getTile(subdir: string, name: string) {
  if (!TILES_DIR) return null;
  const key = `${subdir}/${name}`;
  if (imageCache.has(key)) return imageCache.get(key)!;
  const filePath = path.join(TILES_DIR, subdir, `${name}.png`);
  if (!fs.existsSync(filePath)) return null;
  const img = await loadImage(filePath);
  imageCache.set(key, img);
  return img;
}

function cropTileName(crop: PlantedCrop): string {
  const stage = getStage(crop);
  const stageMap: Record<string, string> = {
    [GrowthStage.Seed]: "seed",
    [GrowthStage.Sprout]: "sprout",
    [GrowthStage.Growing1]: "growing_1",
    [GrowthStage.Growing2]: "growing_2",
    [GrowthStage.Ready]: "ready",
  };
  return `${crop.cropId}_${stageMap[stage] ?? "seed"}`;
}

function drawTileKeepAspect(
  ctx: ReturnType<ReturnType<typeof createCanvas>["getContext"]>,
  image: Awaited<ReturnType<typeof loadImage>>,
  x: number,
  y: number,
  anchor?: { x: number; y: number },
  yOffsetPx = 0
) {
  // Small source sprites (<16px wide) keep their native width (scaled by global SCALE), no forced stretch.
  const pixelScale = SCALED_TILE / TILE;
  const srcWidth = image.width || TILE;
  const srcHeight = image.height || TILE;
  const targetWidth = srcWidth < TILE ? Math.max(1, Math.round(srcWidth * pixelScale)) : SCALED_TILE;
  const targetHeight = Math.max(1, Math.round((srcHeight / srcWidth) * targetWidth));
  const targetX = anchor
    ? x + Math.round(SCALED_TILE / 2 - ((anchor.x + 0.5) / srcWidth) * targetWidth)
    : x + Math.max(0, Math.floor((SCALED_TILE - targetWidth) / 2));
  const targetY = anchor
    ? y + Math.round(SCALED_TILE - ((anchor.y + 1) / srcHeight) * targetHeight) + yOffsetPx
    : y + (SCALED_TILE - targetHeight);

  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(image, targetX, targetY, targetWidth, targetHeight);
}

function detectCropAnchor(
  image: Awaited<ReturnType<typeof loadImage>>
): { x: number; y: number } {
  const srcWidth = image.width || TILE;
  const srcHeight = image.height || TILE;
  const probe = createCanvas(srcWidth, srcHeight);
  const probeCtx = probe.getContext("2d");
  probeCtx.clearRect(0, 0, srcWidth, srcHeight);
  probeCtx.drawImage(image, 0, 0);
  const pixels = probeCtx.getImageData(0, 0, srcWidth, srcHeight).data;

  let maxY = -1;
  for (let py = srcHeight - 1; py >= 0; py--) {
    for (let px = 0; px < srcWidth; px++) {
      const alpha = pixels[(py * srcWidth + px) * 4 + 3];
      if (alpha > 0) {
        maxY = py;
        break;
      }
    }
    if (maxY >= 0) break;
  }

  if (maxY < 0) return { x: Math.floor(srcWidth / 2), y: srcHeight - 1 };

  const sampleFromY = Math.max(0, maxY - 1);
  let sumX = 0;
  let count = 0;
  for (let py = sampleFromY; py <= maxY; py++) {
    for (let px = 0; px < srcWidth; px++) {
      const alpha = pixels[(py * srcWidth + px) * 4 + 3];
      if (alpha > 0) {
        sumX += px;
        count++;
      }
    }
  }

  const anchorX = count > 0 ? sumX / count : Math.floor(srcWidth / 2);
  return { x: anchorX, y: maxY };
}

function getCropAnchor(
  cropName: string,
  image: Awaited<ReturnType<typeof loadImage>>
): { x: number; y: number } {
  const cached = cropAnchorCache.get(cropName);
  if (cached) return cached;
  const anchor = detectCropAnchor(image);
  cropAnchorCache.set(cropName, anchor);
  return anchor;
}

export async function renderFarmImage(state: FarmState): Promise<string> {
  const gridW = state.gridCols * SCALED_TILE + Math.max(0, state.gridCols - 1) * CELL_GAP;
  const gridH = state.gridRows * SCALED_TILE + Math.max(0, state.gridRows - 1) * CELL_GAP;
  const canvasW = PADDING + ROW_LABEL_WIDTH + LABEL_TO_GRID_GAP + gridW + PADDING;
  const canvasH =
    HEADER_HEIGHT + HEADER_TO_GRID_GAP + COL_LABEL_HEIGHT + LABEL_TO_GRID_GAP + gridH + PADDING;

  const canvas = createCanvas(canvasW, canvasH);
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#1a1a2e";
  ctx.fillRect(0, 0, canvasW, canvasH);

  ctx.fillStyle = "#e0e0e0";
  ctx.font = "bold 18px sans-serif";
  ctx.fillText(`Day ${state.day}`, PADDING, 26);

  ctx.font = "14px sans-serif";
  ctx.fillStyle = "#FFD700";
  ctx.fillText(`${state.gold}G`, canvasW - 80, 26);

  const gridStartX = PADDING + ROW_LABEL_WIDTH + LABEL_TO_GRID_GAP;
  const gridStartY = HEADER_HEIGHT + HEADER_TO_GRID_GAP + COL_LABEL_HEIGHT + LABEL_TO_GRID_GAP;

  ctx.fillStyle = "#aaaaaa";
  ctx.font = "12px sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "bottom";
  for (let c = 0; c < state.gridCols; c++) {
    const x = gridStartX + c * (SCALED_TILE + CELL_GAP) + SCALED_TILE / 2;
    ctx.fillText(`${c + 1}`, x, gridStartY - LABEL_TO_GRID_GAP);
  }
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";
  for (let r = 0; r < state.gridRows; r++) {
    const y = gridStartY + r * (SCALED_TILE + CELL_GAP) + SCALED_TILE / 2;
    ctx.fillText(String.fromCharCode(65 + r), gridStartX - LABEL_TO_GRID_GAP, y);
  }
  ctx.textAlign = "start";
  ctx.textBaseline = "alphabetic";

  for (let r = 0; r < state.gridRows; r++) {
    for (let c = 0; c < state.gridCols; c++) {
      const plot = state.grid[r][c];
      const x = gridStartX + c * (SCALED_TILE + CELL_GAP);
      const y = gridStartY + r * (SCALED_TILE + CELL_GAP);

      const terrainName = plot.crop?.watered ? "watered" : "empty";
      const terrainTile = await getTile("terrain", terrainName);
      if (terrainTile) {
        drawTileKeepAspect(ctx, terrainTile, x, y);
      }

      if (plot.crop) {
        const stage = getStage(plot.crop);
        const name = cropTileName(plot.crop);
        const cropTile = await getTile("crops", name);
        if (cropTile) {
          drawTileKeepAspect(
            ctx,
            cropTile,
            x,
            y,
            getCropAnchor(name, cropTile),
            STAGE_Y_OFFSET_PX[stage] ?? 0
          );
        }
      }

    }
  }

  const outDir = path.join(os.homedir(), ".grinders-farm");
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, "farm.png");

  const buf = canvas.toBuffer("image/png");
  fs.writeFileSync(outPath, buf);

  return outPath;
}
