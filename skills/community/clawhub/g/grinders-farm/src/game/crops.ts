import { CropDef, GrowthStage, PlantedCrop } from "./types.js";

const MIN_GAME_GROWTH_DAYS = 5;
const REAL_MATURITY_BASELINE_DAYS = 70;

function scaleGrowthDays(realMaturityDays: number): number {
  return Math.max(2, Math.round((realMaturityDays / REAL_MATURITY_BASELINE_DAYS) * MIN_GAME_GROWTH_DAYS));
}

function makeCropDef(
  id: string,
  name: string,
  emoji: string,
  realMaturityDays: number,
  seedPrice: number,
  sellPrice: number
): CropDef {
  return {
    id,
    name,
    emoji,
    realMaturityDays,
    growthDays: scaleGrowthDays(realMaturityDays),
    seedPrice,
    sellPrice,
  };
}

export const CROP_DEFS: Record<string, CropDef> = {
  carrot: {
    ...makeCropDef("carrot", "胡萝卜", "🥕", 70, 5, 11),
  },
  potato: {
    ...makeCropDef("potato", "土豆", "🥔", 95, 8, 22),
  },
  tomato: {
    ...makeCropDef("tomato", "番茄", "🍅", 80, 9, 24),
  },
  pumpkin: {
    ...makeCropDef("pumpkin", "南瓜", "🎃", 110, 12, 34),
  },
};

export function getAllCropIds(): string[] {
  return Object.keys(CROP_DEFS);
}

export function getCropDef(cropId: string): CropDef | undefined {
  return CROP_DEFS[cropId];
}

export function getStage(crop: PlantedCrop): GrowthStage {
  const def = getCropDef(crop.cropId);
  if (!def) return GrowthStage.Seed;
  const requiredWaterDays = Math.max(1, crop.requiredWaterDays ?? def.growthDays);

  if (crop.wateredDays >= requiredWaterDays) return GrowthStage.Ready;
  if (crop.wateredDays <= 0) return GrowthStage.Seed;

  const progress = crop.wateredDays / requiredWaterDays;
  if (progress < 1 / 3) return GrowthStage.Sprout;
  if (progress < 2 / 3) return GrowthStage.Growing1;
  return GrowthStage.Growing2;
}

export function advanceCropGrowth(crop: PlantedCrop): PlantedCrop {
  const before = getStage(crop);
  if (before === GrowthStage.Ready) {
    return { ...crop, watered: false };
  }

  const newWatered = crop.watered ? crop.wateredDays + 1 : crop.wateredDays;
  return { ...crop, wateredDays: newWatered, watered: false };
}

export function createPlantedCrop(cropId: string): PlantedCrop {
  const def = getCropDef(cropId);
  return {
    cropId,
    wateredDays: 0,
    watered: false,
    requiredWaterDays: def?.growthDays ?? 4,
  };
}
