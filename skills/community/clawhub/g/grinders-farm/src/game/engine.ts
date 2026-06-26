import { FarmState, CommandResult } from "./types.js";
import {
  createNewFarm,
  plant,
  water,
  harvest,
  sellAll,
  nextDay,
  getShopText,
  getInventoryText,
  ensureFarmState,
} from "./farm.js";
import { renderFarmText } from "../render/text-renderer.js";
import { renderFarmImage } from "../render/image-renderer.js";
import { LocalStorage } from "../storage/local-storage.js";
import { startLocalAuto, stopLocalAuto } from "../local-auto.js";

const DEFAULT_START_INTERVAL_SEC = 20 * 60;

const KNOWN_COMMANDS = new Set([
  "farm",
  "status",
  "plant",
  "water",
  "harvest",
  "shop",
  "sell",
  "inventory",
  "inv",
  "start",
  "stop",
  "help",
  "reset",
]);

export class GameEngine {
  private state: FarmState;
  private storage: LocalStorage;

  constructor(storage: LocalStorage) {
    this.storage = storage;
    this.state = ensureFarmState(storage.load() ?? createNewFarm());
  }

  getState(): FarmState {
    return this.state;
  }

  private save(): void {
    this.storage.save(this.state);
  }

  private reload(): void {
    this.state = ensureFarmState(this.storage.load() ?? createNewFarm());
  }

  private isMutatingCommand(cmd: string): boolean {
    return cmd === "plant" || cmd === "water" || cmd === "harvest" || cmd === "sell" || cmd === "reset";
  }

  async advanceDay(): Promise<CommandResult> {
    return this.storage.withStateLock(async () => {
      this.reload();
      const result = nextDay(this.state);
      this.save();

      if (result.success) {
        const farmView = renderFarmText(this.state);
        result.message += "\n\n" + farmView;
        try {
          result.imagePath = await renderFarmImage(this.state);
        } catch {
          // image rendering unavailable, text-only fallback
        }
      }

      return result;
    });
  }

  async executeCommand(input: string): Promise<CommandResult> {
    const normalizedInput = normalizeFarmInput(input);
    const parts = normalizedInput.trim().toLowerCase().split(/\s+/);
    const cmd = parts[0];

    if (!cmd) {
      return { success: false, message: '输入 "help" 查看帮助' };
    }

    if (this.isMutatingCommand(cmd)) {
      return this.storage.withStateLock(async () => {
        this.reload();
        return this.executeWithCurrentState(cmd, parts);
      });
    }

    this.reload();
    return this.executeWithCurrentState(cmd, parts);
  }

  private async executeWithCurrentState(cmd: string, parts: string[]): Promise<CommandResult> {
    let result: CommandResult;

    switch (cmd) {
      case "farm":
      case "status": {
        const text = renderFarmText(this.state);
        let imagePath: string | undefined;
        try {
          imagePath = await renderFarmImage(this.state);
        } catch {
          // image rendering unavailable, text-only fallback
        }
        return { success: true, message: text, imagePath };
      }

      case "plant": {
        const cropId = parts[1];
        const label = parts[2];
        if (!cropId || !label) {
          return { success: false, message: '用法: plant <作物> <位置>\n例如: plant carrot A1' };
        }
        result = plant(this.state, cropId, label.toUpperCase());
        break;
      }

      case "water": {
        const label = parts[1]?.toUpperCase();
        result = water(this.state, label);
        break;
      }

      case "harvest": {
        const label = parts[1]?.toUpperCase();
        result = harvest(this.state, label);
        break;
      }

      case "shop":
        return { success: true, message: getShopText(this.state) };

      case "sell":
        result = sellAll(this.state);
        break;

      case "inventory":
      case "inv":
        return { success: true, message: getInventoryText(this.state) };

      case "start":
        if (parts.length > 1) {
          return { success: false, message: '用法: start（固定每 20 分钟推进一天）' };
        }
        return startLocalAuto(DEFAULT_START_INTERVAL_SEC);

      case "stop":
        if (parts.length > 1) {
          return { success: false, message: '用法: stop' };
        }
        return stopLocalAuto();

      case "help":
        return { success: true, message: getHelpText() };

      case "reset": {
        this.state = createNewFarm();
        this.save();
        const resetView = renderFarmText(this.state);
        let resetImagePath: string | undefined;
        try {
          resetImagePath = await renderFarmImage(this.state);
        } catch {
          // image rendering unavailable
        }
        return { success: true, message: "农场已重置！全新开始 🌱\n\n" + resetView, imagePath: resetImagePath };
      }

      default:
        return { success: false, message: `未知命令 "${cmd}"。输入 "help" 查看帮助` };
    }

    this.save();

    if (result.success) {
      const farmView = renderFarmText(this.state);
      result.message += "\n\n" + farmView;
      try {
        result.imagePath = await renderFarmImage(this.state);
      } catch {
        // image rendering unavailable, text-only fallback
      }
    }

    return result;
  }
}

function normalizeFarmInput(input: string): string {
  const raw = input.trim();
  if (!raw) return raw;

  const parts = raw.toLowerCase().split(/\s+/);
  if (KNOWN_COMMANDS.has(parts[0])) return raw;

  const cropMap: Array<{ id: string; aliases: string[] }> = [
    { id: "carrot", aliases: ["carrot", "胡萝卜"] },
    { id: "potato", aliases: ["potato", "土豆", "马铃薯"] },
    { id: "tomato", aliases: ["tomato", "番茄", "西红柿"] },
    { id: "pumpkin", aliases: ["pumpkin", "南瓜"] },
  ];

  const posMatch = raw.match(/([A-Da-d])\s*([1-5])/);
  const pos = posMatch ? `${posMatch[1].toUpperCase()}${posMatch[2]}` : "";
  const text = raw.toLowerCase();
  const has = (...tokens: string[]): boolean => tokens.some((t) => text.includes(t));
  const findCropId = (): string | null => {
    for (const c of cropMap) {
      if (c.aliases.some((a) => text.includes(a.toLowerCase()))) return c.id;
    }
    return null;
  };

  if (has("自动", "auto")) {
    if (has("停", "关闭", "关掉", "stop")) return "stop";
    if (has("开", "启动", "start")) return "start";
  }

  if (has("种", "种植", "播种", "plant")) {
    const cropId = findCropId();
    if (cropId && pos) return `plant ${cropId} ${pos}`;
    if (cropId) return "farm";
  }

  if (has("浇水", "water")) return pos ? `water ${pos}` : "water";
  if (has("收获", "harvest")) return pos ? `harvest ${pos}` : "harvest";
  if (has("商店", "shop", "买种子", "买什么")) return "shop";
  if (has("出售", "卖掉", "卖出", "sell")) return "sell";
  if (has("仓库", "背包", "库存", "inventory", "inv")) return "inventory";
  if (has("重置", "reset", "重新开始")) return "reset";
  if (has("开始", "启动", "start")) return "start";
  if (has("停止", "关闭", "关掉", "stop")) return "stop";
  if (has("帮助", "help")) return "help";
  if (has("农场", "farm", "地块", "作物", "庄稼")) return "farm";

  return raw;
}

function getHelpText(): string {
  return [
    "🌿 Grinder's Farm — 命令帮助",
    "",
    "  farm / status     查看农场全景",
    "  plant <作物> <位置>  种植作物 (如: plant carrot A1)",
    "  water [位置]       浇水（不指定则浇全部）",
    "  harvest [位置]     收获（不指定则收全部成熟作物）",
    "  shop              查看种子商店",
    "  sell              出售仓库中所有农产品",
    "  inventory / inv   查看仓库",
    "  start             启动自动推进（固定20分钟/天，自动推送到已绑定频道）",
    "  stop              停止自动推进",
    "  reset             重新开始",
    "  help              显示此帮助",
    "",
    "位置格式: 行字母 + 列数字，如 A1, B3, D5",
  ].join("\n");
}
