import {
  FarmState,
  Plot,
  GrowthStage,
  CommandResult,
  coordToLabel,
  labelToCoord,
  FarmMarketState,
  FarmOrder,
} from "./types.js";
import { CROP_DEFS, getCropDef, createPlantedCrop, advanceCropGrowth, getStage } from "./crops.js";

const DEFAULT_ROWS = 4;
const DEFAULT_COLS = 5;
const STARTING_GOLD = 50;
const MIN_MARKET_MULTIPLIER = 0.65;
const MAX_MARKET_MULTIPLIER = 1.35;
const MAX_SUPPLY_PENALTY = 0.35;

function clamp(n: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, n));
}

function createEmptyMarketState(): FarmMarketState {
  const sellMultipliers: Record<string, number> = {};
  const recentSales: Record<string, number> = {};
  for (const cropId of Object.keys(CROP_DEFS)) {
    sellMultipliers[cropId] = 1;
    recentSales[cropId] = 0;
  }
  return { sellMultipliers, recentSales };
}

function isValidOrder(order: FarmOrder): boolean {
  return Boolean(order?.cropId && Number.isFinite(order.quantity) && Number.isFinite(order.rewardGold) && Number.isFinite(order.dueDay));
}

export function ensureFarmState(state: FarmState): FarmState {
  state.gridRows = state.gridRows || state.grid.length || DEFAULT_ROWS;
  state.gridCols = state.gridCols || state.grid[0]?.length || DEFAULT_COLS;
  state.market = state.market ?? createEmptyMarketState();
  state.market.sellMultipliers = state.market.sellMultipliers ?? {};
  state.market.recentSales = state.market.recentSales ?? {};
  for (const cropId of Object.keys(CROP_DEFS)) {
    if (!Number.isFinite(state.market.sellMultipliers[cropId])) state.market.sellMultipliers[cropId] = 1;
    if (!Number.isFinite(state.market.recentSales[cropId])) state.market.recentSales[cropId] = 0;
  }
  if (state.activeOrder != null && !isValidOrder(state.activeOrder)) {
    state.activeOrder = null;
  }
  for (let r = 0; r < state.grid.length; r++) {
    for (let c = 0; c < state.grid[r].length; c++) {
      const plot = state.grid[r][c];
      plot.row = r;
      plot.col = c;
      plot.consecutiveSameCrop = plot.consecutiveSameCrop ?? 0;
      if (plot.crop) {
        const def = getCropDef(plot.crop.cropId);
        if (!Number.isFinite(plot.crop.requiredWaterDays)) {
          plot.crop.requiredWaterDays = def?.growthDays ?? 4;
        }
      }
    }
  }
  return state;
}

function getMarketMultiplier(state: FarmState, cropId: string): number {
  const market = state.market ?? createEmptyMarketState();
  const m = market.sellMultipliers[cropId];
  if (!Number.isFinite(m)) return 1;
  return clamp(m, MIN_MARKET_MULTIPLIER, MAX_MARKET_MULTIPLIER);
}

export function getCurrentSellPrice(state: FarmState, cropId: string): number {
  const def = getCropDef(cropId);
  if (!def) return 0;
  return Math.max(1, Math.round(def.sellPrice * getMarketMultiplier(state, cropId)));
}

function rollDailyMarket(state: FarmState): void {
  const market = state.market ?? (state.market = createEmptyMarketState());
  for (const cropId of Object.keys(CROP_DEFS)) {
    const demandNoise = (Math.random() - 0.5) * 0.5; // ±25%
    const supplyPenalty = Math.min(MAX_SUPPLY_PENALTY, (market.recentSales[cropId] ?? 0) * 0.04);
    market.sellMultipliers[cropId] = clamp(1 + demandNoise - supplyPenalty, MIN_MARKET_MULTIPLIER, MAX_MARKET_MULTIPLIER);
    market.recentSales[cropId] = Math.max(0, (market.recentSales[cropId] ?? 0) - 1);
  }
}

function createRandomOrder(state: FarmState): FarmOrder {
  const cropIds = Object.keys(CROP_DEFS);
  const cropId = cropIds[Math.floor(Math.random() * cropIds.length)];
  const def = getCropDef(cropId)!;
  const quantity = 2 + Math.floor(Math.random() * 3); // 2-4
  const dueDay = state.day + 2 + Math.floor(Math.random() * 3); // +2~4 days
  const rewardGold = Math.max(8, Math.round(quantity * def.sellPrice * 0.75));
  return {
    id: `D${state.day}-${Math.floor(Math.random() * 10000)}`,
    cropId,
    quantity,
    rewardGold,
    dueDay,
  };
}

function applyRotationGrowthDays(plot: Plot, cropId: string, baseGrowthDays: number): { requiredWaterDays: number; note: string } {
  const streak = plot.consecutiveSameCrop ?? 0;
  if (plot.lastCropId === cropId && streak >= 1) {
    return {
      requiredWaterDays: baseGrowthDays + 1,
      note: "（连作惩罚：生长 +1 天）",
    };
  }
  if (plot.lastCropId && plot.lastCropId !== cropId) {
    return {
      requiredWaterDays: Math.max(2, baseGrowthDays - 1),
      note: "（轮作加成：生长 -1 天）",
    };
  }
  return { requiredWaterDays: baseGrowthDays, note: "" };
}

export function createNewFarm(rows = DEFAULT_ROWS, cols = DEFAULT_COLS): FarmState {
  const grid: Plot[][] = [];
  for (let r = 0; r < rows; r++) {
    const row: Plot[] = [];
    for (let c = 0; c < cols; c++) {
      row.push({ row: r, col: c, crop: null });
    }
    grid.push(row);
  }
  const state = ensureFarmState({
    day: 1,
    gold: STARTING_GOLD,
    grid,
    inventory: [],
    gridRows: rows,
    gridCols: cols,
    market: createEmptyMarketState(),
    activeOrder: null,
  });
  state.activeOrder = createRandomOrder(state);
  return state;
}

function getPlot(state: FarmState, row: number, col: number): Plot | null {
  if (row < 0 || row >= state.gridRows || col < 0 || col >= state.gridCols) return null;
  return state.grid[row][col];
}

function addToInventory(state: FarmState, itemId: string, name: string, qty: number): void {
  const existing = state.inventory.find((i) => i.itemId === itemId);
  if (existing) {
    existing.quantity += qty;
  } else {
    state.inventory.push({ itemId, name, quantity: qty });
  }
}

export function plant(state: FarmState, cropId: string, label: string): CommandResult {
  ensureFarmState(state);
  const def = getCropDef(cropId);
  if (!def) {
    const validIds = Object.keys(CROP_DEFS).join(", ");
    return { success: false, message: `未知作物 "${cropId}"。可选: ${validIds}` };
  }

  const coord = labelToCoord(label);
  if (!coord) {
    return { success: false, message: `无效坐标 "${label}"。格式如 A1, B3` };
  }

  const plot = getPlot(state, coord.row, coord.col);
  if (!plot) {
    return {
      success: false,
      message: `坐标 ${label} 超出农场范围 (${state.gridRows}×${state.gridCols})`,
    };
  }

  if (plot.crop) {
    return { success: false, message: `${coordToLabel(plot.row, plot.col)} 已有作物，请先收获或清除` };
  }

  if (state.gold < def.seedPrice) {
    return { success: false, message: `金币不足！需要 ${def.seedPrice}G，当前 ${state.gold}G` };
  }

  state.gold -= def.seedPrice;
  const planted = createPlantedCrop(cropId);
  const rotation = applyRotationGrowthDays(plot, cropId, def.growthDays);
  planted.requiredWaterDays = rotation.requiredWaterDays;
  plot.crop = planted;

  return {
    success: true,
    message: `在 ${coordToLabel(plot.row, plot.col)} 种下了${def.name} ${def.emoji}（-${def.seedPrice}G，余 ${state.gold}G）${rotation.note}`,
  };
}

export function water(state: FarmState, label?: string): CommandResult {
  ensureFarmState(state);
  if (label) {
    const coord = labelToCoord(label);
    if (!coord) return { success: false, message: `无效坐标 "${label}"` };
    const plot = getPlot(state, coord.row, coord.col);
    if (!plot) return { success: false, message: `坐标 ${label} 超出范围` };
    if (!plot.crop) return { success: false, message: `${label} 是空地，无需浇水` };
    if (getStage(plot.crop) === GrowthStage.Ready)
      return { success: false, message: `${label} 的作物已成熟，请收获` };
    plot.crop.watered = true;
    const def = getCropDef(plot.crop.cropId);
    return {
      success: true,
      message: `给 ${label} 的${def?.name ?? "作物"}浇了水 💧`,
    };
  }

  let count = 0;
  for (const row of state.grid) {
    for (const plot of row) {
      if (plot.crop && getStage(plot.crop) !== GrowthStage.Ready && !plot.crop.watered) {
        plot.crop.watered = true;
        count++;
      }
    }
  }

  if (count === 0) return { success: false, message: "没有需要浇水的作物" };
  return { success: true, message: `给 ${count} 块地浇了水 💧` };
}

export function harvest(state: FarmState, label?: string): CommandResult {
  ensureFarmState(state);
  if (label) {
    const coord = labelToCoord(label);
    if (!coord) return { success: false, message: `无效坐标 "${label}"` };
    const plot = getPlot(state, coord.row, coord.col);
    if (!plot) return { success: false, message: `坐标 ${label} 超出范围` };
    if (!plot.crop) return { success: false, message: `${label} 是空地` };
    if (getStage(plot.crop) !== GrowthStage.Ready)
      return { success: false, message: `${label} 的作物还未成熟` };

    const def = getCropDef(plot.crop.cropId)!;
    addToInventory(state, def.id, def.name, 1);
    if (plot.lastCropId === def.id) {
      plot.consecutiveSameCrop = (plot.consecutiveSameCrop ?? 0) + 1;
    } else {
      plot.consecutiveSameCrop = 1;
    }
    plot.lastCropId = def.id;
    plot.crop = null;
    return {
      success: true,
      message: `收获了 ${def.name} ${def.emoji}！已放入仓库`,
    };
  }

  const harvested: string[] = [];
  for (const row of state.grid) {
    for (const plot of row) {
      if (plot.crop && getStage(plot.crop) === GrowthStage.Ready) {
        const def = getCropDef(plot.crop.cropId)!;
        addToInventory(state, def.id, def.name, 1);
        harvested.push(`${coordToLabel(plot.row, plot.col)}:${def.name}`);
        if (plot.lastCropId === def.id) {
          plot.consecutiveSameCrop = (plot.consecutiveSameCrop ?? 0) + 1;
        } else {
          plot.consecutiveSameCrop = 1;
        }
        plot.lastCropId = def.id;
        plot.crop = null;
      }
    }
  }

  if (harvested.length === 0) return { success: false, message: "没有可收获的作物" };
  return {
    success: true,
    message: `收获了 ${harvested.length} 个作物: ${harvested.join(", ")}`,
  };
}

export function sellAll(state: FarmState): CommandResult {
  ensureFarmState(state);
  if (state.inventory.length === 0) {
    return { success: false, message: "仓库是空的，没什么可卖的" };
  }

  let orderMsg = "";
  if (state.activeOrder) {
    const order = state.activeOrder;
    const inventoryItem = state.inventory.find((i) => i.itemId === order.cropId);
    if (inventoryItem && inventoryItem.quantity >= order.quantity) {
      inventoryItem.quantity -= order.quantity;
      state.gold += order.rewardGold;
      const def = getCropDef(order.cropId);
      orderMsg = `\n✅ 完成订单：交付 ${def?.name ?? order.cropId}×${order.quantity}，额外奖励 ${order.rewardGold}G！`;
      if (inventoryItem.quantity <= 0) {
        state.inventory = state.inventory.filter((i) => i.quantity > 0);
      }
      state.activeOrder = createRandomOrder(state);
    }
  }

  let totalGold = 0;
  const sold: string[] = [];
  const marketFeedback: string[] = [];
  const market = state.market ?? (state.market = createEmptyMarketState());

  for (const item of state.inventory) {
    if (item.quantity <= 0) continue;
    const def = getCropDef(item.itemId);
    if (def) {
      const unitPrice = getCurrentSellPrice(state, def.id);
      const earn = unitPrice * item.quantity;
      totalGold += earn;
      sold.push(`${def.name}×${item.quantity} = ${earn}G（${unitPrice}G/个）`);
      market.recentSales[def.id] = (market.recentSales[def.id] ?? 0) + item.quantity;
      const pressure = item.quantity >= 6 ? "高" : item.quantity >= 3 ? "中" : "低";
      const dropLikelihood = pressure === "高" ? "大概率降价" : pressure === "中" ? "中概率降价" : "小概率降价";
      marketFeedback.push(`${def.name}+${item.quantity}（压力${pressure}，${dropLikelihood}）`);
    }
  }

  state.gold += totalGold;
  state.inventory = [];

  const feedbackMsg =
    marketFeedback.length > 0
      ? `\n📉 市场反馈（仅以下作物更可能降价）：${marketFeedback.join("；")}。`
      : "";

  return {
    success: true,
    message: `出售: ${sold.join(", ")}。共获得 ${totalGold}G（余 ${state.gold}G）${orderMsg}${feedbackMsg}`,
  };
}

export function nextDay(state: FarmState): CommandResult {
  ensureFarmState(state);
  const events: string[] = [];

  for (const row of state.grid) {
    for (const plot of row) {
      if (plot.crop) {
        const before = getStage(plot.crop);
        plot.crop = advanceCropGrowth(plot.crop);
        const after = getStage(plot.crop);
        if (after !== before) {
          const def = getCropDef(plot.crop.cropId);
          const label = coordToLabel(plot.row, plot.col);
          if (after === GrowthStage.Ready) {
            events.push(`${label} ${def?.name} 成熟了！🎉`);
          } else {
            events.push(`${label} ${def?.name} → ${after}`);
          }
        }
      }
    }
  }

  state.day++;
  rollDailyMarket(state);
  if (!state.activeOrder) {
    state.activeOrder = createRandomOrder(state);
    const def = getCropDef(state.activeOrder.cropId);
    events.push(`📦 新订单：${def?.name ?? state.activeOrder.cropId} ×${state.activeOrder.quantity}，截止第 ${state.activeOrder.dueDay} 天，奖励 ${state.activeOrder.rewardGold}G`);
  } else if (state.day > state.activeOrder.dueDay) {
    const old = state.activeOrder;
    const oldDef = getCropDef(old.cropId);
    state.activeOrder = createRandomOrder(state);
    const nextDef = getCropDef(state.activeOrder.cropId);
    events.push(`⌛ 订单过期：${oldDef?.name ?? old.cropId} ×${old.quantity}`);
    events.push(`📦 新订单：${nextDef?.name ?? state.activeOrder.cropId} ×${state.activeOrder.quantity}，截止第 ${state.activeOrder.dueDay} 天，奖励 ${state.activeOrder.rewardGold}G`);
  }

  let msg = `☀️ 第 ${state.day} 天到了！`;
  if (events.length > 0) {
    msg += "\n" + events.join("\n");
  } else {
    msg += "\n今天农场一片宁静。";
  }
  return { success: true, message: msg };
}

export function getShopText(state?: FarmState): string {
  const lines = ["🏪 种子商店：", ""];
  for (const def of Object.values(CROP_DEFS)) {
    const unitSell = state ? getCurrentSellPrice(state, def.id) : def.sellPrice;
    const todayRoi = `${unitSell - def.seedPrice}G`;
    const marketTag = state
      ? unitSell > def.sellPrice
        ? "📈"
        : unitSell < def.sellPrice
          ? "📉"
          : "➖"
      : "➖";
    lines.push(
      `  ${def.emoji} ${def.name} (${def.id}) — 种子 ${def.seedPrice}G | 今日售价 ${unitSell}G ${marketTag}（原价 ${def.sellPrice}G） | 生长 ${def.growthDays} 天 | 今日单个利润 ${todayRoi}`
    );
  }
  return lines.join("\n");
}

export function getInventoryText(state: FarmState): string {
  ensureFarmState(state);
  if (state.inventory.length === 0) {
    return "📦 仓库: 空";
  }
  const lines = ["📦 仓库:"];
  for (const item of state.inventory) {
    const def = getCropDef(item.itemId);
    lines.push(`  ${def?.emoji ?? "?"} ${item.name} × ${item.quantity}`);
  }
  return lines.join("\n");
}
