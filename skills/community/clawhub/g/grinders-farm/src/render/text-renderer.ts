import { FarmState, GrowthStage, PlantedCrop } from "../game/types.js";
import { getCropDef, getStage } from "../game/crops.js";

const STAGE_EMOJI: Record<string, string> = {
  [GrowthStage.Seed]: "🟤",
  [GrowthStage.Sprout]: "🌱",
  [GrowthStage.Growing1]: "🌿",
  [GrowthStage.Growing2]: "🌳",
  [GrowthStage.Ready]: "✅",
};

function plotEmoji(crop: PlantedCrop | null): string {
  if (!crop) return "⬜";
  const stage = getStage(crop);
  if (stage === GrowthStage.Ready) {
    const def = getCropDef(crop.cropId);
    return def?.emoji ?? "✅";
  }
  return STAGE_EMOJI[stage] ?? "❓";
}

export function renderFarmText(state: FarmState): string {
  const lines: string[] = [];

  lines.push(`🌿 Grinder's Farm — 第 ${state.day} 天 | 💰 ${state.gold}G`);
  if (state.activeOrder) {
    const def = getCropDef(state.activeOrder.cropId);
    const dueIn = Math.max(0, state.activeOrder.dueDay - state.day);
    lines.push(
      `📦 订单: ${def?.emoji ?? "📦"} ${def?.name ?? state.activeOrder.cropId} ×${state.activeOrder.quantity} | 奖励 ${state.activeOrder.rewardGold}G | 截止第 ${state.activeOrder.dueDay} 天（剩 ${dueIn} 天）`,
    );
  }
  lines.push("");

  const colNums = Array.from({ length: state.gridCols }, (_, i) => String(i + 1));
  lines.push(`| | ${colNums.join(" | ")} |`);
  lines.push(`|---|${colNums.map(() => "---").join("|")}|`);

  for (let r = 0; r < state.gridRows; r++) {
    const rowLabel = String.fromCharCode(65 + r);
    const cells = state.grid[r].map((p) => plotEmoji(p.crop));
    lines.push(`| ${rowLabel} | ${cells.join(" | ")} |`);
  }

  lines.push("");

  const planted = new Map<string, { count: number; stages: Map<string, number> }>();
  for (const row of state.grid) {
    for (const plot of row) {
      if (!plot.crop) continue;
      const key = plot.crop.cropId;
      const stage = getStage(plot.crop);
      if (!planted.has(key)) planted.set(key, { count: 0, stages: new Map() });
      const entry = planted.get(key)!;
      entry.count++;
      entry.stages.set(stage, (entry.stages.get(stage) ?? 0) + 1);
    }
  }

  if (planted.size > 0) {
    lines.push("作物状态:");
    for (const [cropId, info] of planted) {
      const def = getCropDef(cropId);
      if (!def) continue;
      const stageStr = Array.from(info.stages.entries())
        .map(([s, n]) => `${s}×${n}`)
        .join(" ");
      lines.push(`  ${def.emoji} ${def.name}: ${info.count}块 (${stageStr})`);
    }
  }

  if (state.inventory.length > 0) {
    lines.push("");
    lines.push("📦 仓库: " + state.inventory.map((i) => {
      const def = getCropDef(i.itemId);
      return `${def?.emoji ?? ""} ${i.name}×${i.quantity}`;
    }).join("  "));
  }

  return lines.join("\n");
}
