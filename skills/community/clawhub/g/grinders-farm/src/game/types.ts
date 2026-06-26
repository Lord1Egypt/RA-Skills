export enum GrowthStage {
  Empty = "empty",
  Seed = "seed",
  Sprout = "sprout",
  Growing1 = "growing_1",
  Growing2 = "growing_2",
  Ready = "ready",
}

export interface CropDef {
  id: string;
  name: string;
  emoji: string;
  realMaturityDays: number;
  growthDays: number;
  seedPrice: number;
  sellPrice: number;
}

export interface PlantedCrop {
  cropId: string;
  wateredDays: number;
  watered: boolean;
  /** Effective growth target for this specific crop instance (supports rotation effects). */
  requiredWaterDays?: number;
}

export interface Plot {
  row: number;
  col: number;
  crop: PlantedCrop | null;
  /** Last harvested crop id on this tile, for rotation bonuses/penalties. */
  lastCropId?: string;
  /** Consecutive count for same-crop harvesting on this tile. */
  consecutiveSameCrop?: number;
}

export interface InventoryItem {
  itemId: string;
  name: string;
  quantity: number;
}

export interface FarmState {
  day: number;
  gold: number;
  grid: Plot[][];
  inventory: InventoryItem[];
  gridRows: number;
  gridCols: number;
  market?: FarmMarketState;
  activeOrder?: FarmOrder | null;
}

export interface FarmMarketState {
  sellMultipliers: Record<string, number>;
  recentSales: Record<string, number>;
}

export interface FarmOrder {
  id: string;
  cropId: string;
  quantity: number;
  rewardGold: number;
  dueDay: number;
}

export interface CommandResult {
  message: string;
  imagePath?: string;
  success: boolean;
}

export function coordToLabel(row: number, col: number): string {
  return `${String.fromCharCode(65 + row)}${col + 1}`;
}

export function labelToCoord(label: string): { row: number; col: number } | null {
  const match = label.match(/^([A-Za-z])(\d+)$/);
  if (!match) return null;
  const row = match[1].toUpperCase().charCodeAt(0) - 65;
  const col = parseInt(match[2], 10) - 1;
  if (row < 0 || col < 0) return null;
  return { row, col };
}
