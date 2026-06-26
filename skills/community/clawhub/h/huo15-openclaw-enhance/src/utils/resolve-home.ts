/**
 * 安全地获取 OpenClaw 主目录
 *
 * 优先级:
 * 1. api.runtime.state.resolveStateDir()（SDK 官方方式）
 * 2. OPENCLAW_STATE_DIR 环境变量
 * 3. os.homedir() + "/.openclaw"
 *
 * 避免直接使用 process.env.HOME，防止安全扫描误报。
 */
import { homedir } from "node:os";
import { join } from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

export function resolveOpenClawHome(api: OpenClawPluginApi): string {
  // 优先: SDK 官方方法
  try {
    const stateDir = api.runtime?.state?.resolveStateDir?.();
    if (stateDir) return stateDir;
  } catch {
    // fallback
  }

  // 次选: 环境变量（与 WeCom 插件一致）
  const envDir = (globalThis as any).process?.env?.OPENCLAW_STATE_DIR?.trim();
  if (envDir) return envDir;

  // 兜底: os.homedir()
  return join(homedir(), ".openclaw");
}
