import os from "node:os";
import path from "node:path";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import { resolvePreferredOpenClawTmpDir } from "openclaw/plugin-sdk/infra-runtime";
import { resolveChannelMediaMaxBytes } from "openclaw/plugin-sdk/media-runtime";

// 默认给一个相对“够用”的上限（80MB），避免视频/较大文件频繁触发失败。
// 仍保留上限以防止恶意大文件把进程内存打爆（下载实现会读入内存再保存）。
export const DEFAULT_WECOM_MEDIA_MAX_BYTES = 80 * 1024 * 1024;

function parsePositiveNumber(value: unknown): number | undefined {
  const parsed = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return undefined;
  }
  return parsed;
}

function resolveStateDirForWecomMedia(): string {
  const stateOverride =
    process.env.OPENCLAW_STATE_DIR?.trim() || process.env.CLAWDBOT_STATE_DIR?.trim();
  if (stateOverride) {
    return stateOverride;
  }
  return path.join(os.homedir(), ".openclaw");
}

function normalizeWecomLocalRoot(root: string): string | undefined {
  const trimmed = root.trim();
  if (!trimmed) {
    return undefined;
  }
  return path.resolve(trimmed.replace(/^~(?=\/|$)/, os.homedir()));
}

function getWecomCommonUserMediaLocalRoots(): readonly string[] {
  const home = os.homedir();
  return [
    path.join(home, "Desktop"),
    path.join(home, "Documents"),
    path.join(home, "Downloads"),
    path.join(home, "Movies"),
    path.join(home, "Pictures"),
  ];
}

export function getWecomDefaultMediaLocalRoots(): readonly string[] {
  const stateDir = path.resolve(resolveStateDirForWecomMedia());
  return [
    path.resolve(resolvePreferredOpenClawTmpDir()),
    stateDir,
    path.join(stateDir, "media"),
    path.join(stateDir, "agents"),
    path.join(stateDir, "workspace"),
    path.join(stateDir, "sandboxes"),
    ...getWecomCommonUserMediaLocalRoots(),
  ];
}

export function resolveWecomConfiguredMediaLocalRoots(cfg: OpenClawConfig): readonly string[] {
  const rawWecom = cfg.channels?.wecom as
    | {
        media?: { localRoots?: unknown };
        mediaLocalRoots?: unknown;
      }
    | undefined;
  const configured = Array.isArray(rawWecom?.media?.localRoots)
    ? rawWecom.media.localRoots
    : Array.isArray(rawWecom?.mediaLocalRoots)
      ? rawWecom.mediaLocalRoots
      : [];
  return configured
    .filter((root): root is string => typeof root === "string")
    .map(normalizeWecomLocalRoot)
    .filter((root): root is string => Boolean(root));
}

export function resolveWecomMergedMediaLocalRoots(params: {
  cfg: OpenClawConfig;
  baseRoots?: readonly string[];
}): readonly string[] {
  const merged: string[] = [];
  const seen = new Set<string>();
  const pushRoot = (root: string) => {
    const normalized = normalizeWecomLocalRoot(root);
    if (!normalized || seen.has(normalized)) {
      return;
    }
    seen.add(normalized);
    merged.push(normalized);
  };

  for (const root of getWecomDefaultMediaLocalRoots()) {
    pushRoot(root);
  }
  for (const root of params.baseRoots ?? []) {
    pushRoot(root);
  }
  for (const root of resolveWecomConfiguredMediaLocalRoots(params.cfg)) {
    pushRoot(root);
  }
  return merged;
}

function resolveLegacyWecomMediaMaxBytes(cfg: OpenClawConfig): number | undefined {
  const raw = (cfg.channels?.wecom as any)?.media?.maxBytes;
  const bytes = parsePositiveNumber(raw);
  if (bytes) {
    return Math.floor(bytes);
  }
  return undefined;
}

export function resolveWecomMediaMaxBytes(
  cfg: OpenClawConfig,
  accountId?: string | null,
): number {
  const mediaMaxBytes = resolveChannelMediaMaxBytes({
    cfg,
    accountId,
    resolveChannelLimitMb: ({ cfg, accountId }) => {
      const wecom = cfg.channels?.wecom as
        | {
            mediaMaxMb?: unknown;
            accounts?: Record<string, { mediaMaxMb?: unknown }>;
          }
        | undefined;
      const accountLimitMb = parsePositiveNumber(wecom?.accounts?.[accountId]?.mediaMaxMb);
      if (accountLimitMb) {
        return accountLimitMb;
      }
      return parsePositiveNumber(wecom?.mediaMaxMb);
    },
  });
  if (mediaMaxBytes) {
    return mediaMaxBytes;
  }
  return resolveLegacyWecomMediaMaxBytes(cfg) ?? DEFAULT_WECOM_MEDIA_MAX_BYTES;
}
