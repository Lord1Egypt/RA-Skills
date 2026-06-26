/**
 * Renders a showcase farm PNG: all four crops × main growth stages on the 4×5 grid.
 * Output: docs/images/demo-farm.png (for README / SKILL screenshots).
 */
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { createNewFarm, ensureFarmState } from "../src/game/farm.js";
import type { PlantedCrop } from "../src/game/types.js";
import { getCropDef } from "../src/game/crops.js";
import { renderFarmImage } from "../src/render/image-renderer.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");

function makeCrop(cropId: string, wateredDays: number, watered: boolean): PlantedCrop {
  const def = getCropDef(cropId)!;
  return {
    cropId,
    wateredDays,
    watered,
    requiredWaterDays: def.growthDays,
  };
}

async function main(): Promise<void> {
  const state = ensureFarmState(createNewFarm());
  state.day = 7;
  state.gold = 128;

  const crops = ["carrot", "potato", "tomato", "pumpkin"] as const;

  // Row A–D: one crop type per row; columns 1–5: seed → sprout → growing1 → growing2 → ready
  for (let row = 0; row < 4; row++) {
    const id = crops[row];
    const req = getCropDef(id)!.growthDays;
    const stages: Array<{ wd: number; w: boolean }> = [
      { wd: 0, w: row % 2 === 0 },
      { wd: Math.max(1, Math.floor(req / 6)), w: true },
      { wd: Math.floor(req / 3), w: true },
      { wd: Math.floor((2 * req) / 3), w: true },
      { wd: req, w: true },
    ];
    for (let col = 0; col < 5; col++) {
      const s = stages[col];
      state.grid[row][col].crop = makeCrop(id, s.wd, s.w);
    }
  }

  const out = await renderFarmImage(state);
  const dir = path.join(repoRoot, "docs", "images");
  fs.mkdirSync(dir, { recursive: true });
  const dest = path.join(dir, "demo-farm.png");
  fs.copyFileSync(out, dest);
  console.log(`Wrote ${dest}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
