/**
 * v5.8.4 模型路由配置 — 持久化到 ~/.openclaw/enhance/model-route.json
 *
 * 取代 v5.8.3 的 hardcode PROVIDER_REGISTRY，让用户能：
 *   - 对话式调整每个 task tier 下各 provider 的 priority / weight / enabled
 *   - 在 priority / weighted / speed / auto-task 四种路由模式间切换
 *
 * 红线一致：
 *   - 文件归 enhance 自己控制（~/.openclaw/enhance/），不动 openclaw 核心配置
 *   - atomic write（tmp + renameSync）
 *   - 损坏时不抛——回退到 default + 自动重建
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync, renameSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";

export type RouteMode = "priority" | "weighted" | "speed" | "auto-task" | "cost-budget";

export interface ProviderBinding {
  /** "<provider>/<model-id>"，与 openclaw.json#models.providers.* 对齐 */
  id: string;
  /** 数值越小越优先；priority 模式下选最小，auto-task 模式下 tier 内 tiebreaker */
  priority: number;
  /** 0-100 权重，weighted 模式下抽样用；speed 模式下被 latency 自动调整 */
  weight: number;
  enabled: boolean;
}

export interface ModelTierConfig {
  providers: ProviderBinding[];
}

/**
 * v5.8.5 speed mode 用：每个 provider 的最近运行时统计（auto 维护，用户只读）
 */
export interface SpeedSample {
  p50Ms: number;
  p95Ms: number;
  errRate: number;
  samples: number;
  /** ISO 时间戳；超过 1h 视为陈旧需要重置 */
  windowStartedAt: string;
}

export interface ModelRouteConfig {
  mode: RouteMode;
  /** task tier 名（flash / pro / reasoner / fast / vl / hailuo）→ provider 列表 */
  models: Record<string, ModelTierConfig>;
  /** v5.8.5 占位：providerId → 最近延迟 + 错误率 */
  speedTracking?: Record<string, SpeedSample>;
  /** schema 版本，方便未来 migration */
  schemaVersion?: number;
}

const CURRENT_SCHEMA_VERSION = 1;

export function getModelRouteConfigPath(): string {
  return join(homedir(), ".openclaw", "enhance", "model-route.json");
}

/**
 * v6.1.2 默认值——和 PROVIDER_REGISTRY 保持一致。
 *
 * 之前的默认（deepseek/* + google-ai-studio/* + custom-sidus-ai/*）三个 provider
 * 都不存在于通用 OpenClaw 配置里，导致 selectProvider 选了它们后 runtime 找不到
 * provider，把 model id 整串塞给 fallback provider，被远端拒 400。
 *
 * 新默认只用通用名 sidus（DeepSeek/GLM 全家）+ minimax（M2.7）；vl/hailuo 留空，
 * 让上层走 OpenClaw 原生 fallback，避免发不存在的 model id。
 */
export function getDefaultModelRouteConfig(): ModelRouteConfig {
  return {
    mode: "auto-task",
    schemaVersion: CURRENT_SCHEMA_VERSION,
    models: {
      // v6.5.6: 默认从 sidus 改 deepseek + minimax —— 跟 OpenClaw 核心 cfg 默认对齐。
      // sidus provider 已下线，改成 deepseek 官方避免 "Model not allowed" 误调。
      flash: {
        providers: [
          { id: "deepseek/deepseek-v4-flash", priority: 1, weight: 70, enabled: true },
          { id: "minimax/MiniMax-M2.7", priority: 2, weight: 30, enabled: true },
        ],
      },
      pro: {
        providers: [
          { id: "deepseek/deepseek-v4-pro", priority: 1, weight: 70, enabled: true },
          { id: "minimax/MiniMax-M2.7", priority: 2, weight: 30, enabled: true },
        ],
      },
      reasoner: {
        providers: [
          { id: "deepseek/deepseek-v4-pro", priority: 1, weight: 100, enabled: true },
        ],
      },
      fast: {
        providers: [
          { id: "deepseek/deepseek-v4-flash", priority: 1, weight: 70, enabled: true },
          { id: "minimax/MiniMax-M2.7", priority: 2, weight: 30, enabled: true },
        ],
      },
      vl: {
        providers: [],
      },
      hailuo: {
        providers: [],
      },
    },
  };
}

export function loadModelRouteConfig(): ModelRouteConfig {
  const p = getModelRouteConfigPath();
  if (!existsSync(p)) {
    const def = getDefaultModelRouteConfig();
    try {
      saveModelRouteConfig(def);
    } catch {
      // 写默认失败也无所谓，下一轮启动会再试
    }
    return def;
  }
  try {
    const raw = readFileSync(p, "utf-8");
    const parsed = JSON.parse(raw) as ModelRouteConfig;
    if (!parsed.mode || !parsed.models) {
      // schema 不对，落回默认
      return getDefaultModelRouteConfig();
    }
    return parsed;
  } catch {
    // 损坏——回退到默认（不覆写损坏文件，让用户能看到原始内容）
    return getDefaultModelRouteConfig();
  }
}

export function saveModelRouteConfig(config: ModelRouteConfig): void {
  const p = getModelRouteConfigPath();
  const dir = dirname(p);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const tmp = `${p}.tmp`;
  const next = { ...config, schemaVersion: CURRENT_SCHEMA_VERSION };
  writeFileSync(tmp, JSON.stringify(next, null, 2) + "\n", "utf-8");
  renameSync(tmp, p);
}

/**
 * 按当前 mode 从给定 tier 选一个 provider。
 * 返回 null 表示该 tier 无可用 provider（让调用方走 openclaw fallback）。
 */
export function selectProvider(
  config: ModelRouteConfig,
  taskTier: string,
): { id: string; reason: string } | null {
  const tier = config.models[taskTier];
  if (!tier || tier.providers.length === 0) return null;
  const enabled = tier.providers.filter((p) => p.enabled);
  if (enabled.length === 0) return null;

  const mode = config.mode;

  // priority / auto-task：选 priority 最小的
  if (mode === "priority" || mode === "auto-task") {
    const sorted = [...enabled].sort((a, b) => a.priority - b.priority);
    return { id: sorted[0].id, reason: `${mode} → ${taskTier} priority=${sorted[0].priority}` };
  }

  // weighted：按 weight 加权随机
  if (mode === "weighted") {
    const totalW = enabled.reduce((s, p) => s + Math.max(0, p.weight), 0);
    if (totalW <= 0) {
      const sorted = [...enabled].sort((a, b) => a.priority - b.priority);
      return { id: sorted[0].id, reason: `weighted-fallback (all weights 0) → ${taskTier}` };
    }
    let roll = Math.random() * totalW;
    for (const p of enabled) {
      roll -= Math.max(0, p.weight);
      if (roll <= 0) {
        return { id: p.id, reason: `weighted (w=${p.weight}/${totalW}) → ${taskTier}` };
      }
    }
    const last = enabled[enabled.length - 1];
    return { id: last.id, reason: `weighted-tail → ${taskTier}` };
  }

  // speed：v5.8.5 按 speedTracking p50+errRate 调权；v5.8.4 占位回退到 priority
  if (mode === "speed") {
    const tracking = config.speedTracking ?? {};
    const scored = enabled
      .map((p) => {
        const s = tracking[p.id];
        if (!s || s.samples < 5) {
          return { p, score: 100000 + p.priority };
        }
        return { p, score: s.p50Ms * (1 + s.errRate * 5) };
      })
      .sort((a, b) => a.score - b.score);
    const winner = scored[0];
    return { id: winner.p.id, reason: `speed (score=${Math.round(winner.score)}) → ${taskTier}` };
  }

  // v6.1.4 ⭐ cost-budget：按 priority 升序选第一个（用户在 model-route.json 里
  // 把"便宜的"放高 priority 即生效）。这其实跟 priority mode 等效，但语义上明示
  // "我在意成本而非延迟"——为以后加"硬性 monthly budget cap"留扩展点。
  // 当前实现：priority 升序 → 取第一个。
  if (mode === "cost-budget") {
    const sorted = [...enabled].sort((a, b) => a.priority - b.priority);
    return { id: sorted[0].id, reason: `cost-budget (priority=${sorted[0].priority}) → ${taskTier}` };
  }

  return null;
}

/**
 * 修改单个 provider 字段（tier + providerId 定位）。返回是否找到。
 */
export function patchProvider(
  config: ModelRouteConfig,
  tier: string,
  providerId: string,
  patch: Partial<Pick<ProviderBinding, "priority" | "weight" | "enabled">>,
): boolean {
  const t = config.models[tier];
  if (!t) return false;
  const idx = t.providers.findIndex((p) => p.id === providerId);
  if (idx < 0) return false;
  t.providers[idx] = { ...t.providers[idx], ...patch };
  return true;
}

/**
 * 列所有 tier × provider 的当前状态。
 */
export function listAllProviders(
  config: ModelRouteConfig,
): Array<{ tier: string; provider: ProviderBinding; speed?: SpeedSample }> {
  const out: Array<{ tier: string; provider: ProviderBinding; speed?: SpeedSample }> = [];
  for (const [tier, t] of Object.entries(config.models)) {
    for (const p of t.providers) {
      out.push({
        tier,
        provider: p,
        speed: config.speedTracking?.[p.id],
      });
    }
  }
  return out;
}
