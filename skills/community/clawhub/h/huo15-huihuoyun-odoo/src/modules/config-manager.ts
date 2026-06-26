/**
 * 辉火云企业套件插件配置管理器 — v4（per-agent 默认 + shared override）
 *
 * **v1.23.0 默认权限模型反转**：
 *   v1.10–v1.22 默认 shared（全员共用一个 Odoo 账号），导致 Odoo 内部 RBAC
 *   失效（销售/管理员看到的数据完全一样）。v1.23 起反转默认：
 *   - 默认 scope='agent' —— 每个渠道（企微/钉钉/飞书）的每个 sender_id 配自己
 *     的辉火云账号，写入 `{agentId}.json`，与 Odoo 内部权限对齐。
 *   - 仅当用户明确说"组织共用"/"配一次大家都用"时才传 shared=true 写入
 *     `default.json`，作为兜底 fallback。
 *
 * **Fallback 链**（load 时自动走一遍）：
 *   1) `{agentId}.json`     — 该 agent 自己的独立凭据（默认写这里）
 *   2) `default.json`       — 组织共享凭据（fallback，仅当显式 shared=true 时写）
 *   3) `pluginConfig.odoo`  — 由 openclaw.plugin.json 注入的静态配置（manifest 预填）
 *   4) legacy `odoo-config.json` — 旧版单文件，向下兼容
 *
 *  第 3 层（pluginConfig）不在本模块处理，由调用方传入。load() 只走 1/2/4。
 *
 * 存储路径: ~/.openclaw/plugin-configs/odoo/{agentId}.json
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, unlinkSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import type { OdooPluginConfig, OdooConfig } from '../types/index.js';

const CONFIG_BASE = '.openclaw/plugin-configs/odoo';
const LEGACY_FILE = '.openclaw/plugin-configs/odoo-config.json';
const SHARED_AGENT_ID = 'default';

export type ConfigSource = 'agent' | 'shared' | 'legacy' | 'none';

function sanitizeAgentId(agentId: string): string {
  return agentId.replace(/[^a-zA-Z0-9_\-]/g, '_').substring(0, 128) || SHARED_AGENT_ID;
}

export class ConfigManager {
  private baseDir: string;
  private legacyPath: string;

  constructor(homeDir: string = process.env['HOME'] ?? '/root') {
    this.baseDir = join(homeDir, CONFIG_BASE);
    this.legacyPath = join(homeDir, LEGACY_FILE);
  }

  /** 获取 agent 配置文件路径 */
  private agentPath(agentId: string): string {
    return join(this.baseDir, `${sanitizeAgentId(agentId)}.json`);
  }

  private sharedPath(): string {
    return join(this.baseDir, `${SHARED_AGENT_ID}.json`);
  }

  private readJson(path: string): OdooPluginConfig | null {
    try {
      if (!existsSync(path)) return null;
      return JSON.parse(readFileSync(path, 'utf-8')) as OdooPluginConfig;
    } catch {
      return null;
    }
  }

  /**
   * 加载配置（带 fallback chain）
   *
   * 优先级：agent 独立 → 共享（default）→ legacy 单文件
   */
  load(agentId: string = SHARED_AGENT_ID): OdooPluginConfig | null {
    const aid = sanitizeAgentId(agentId);

    // 1) 该 agent 自己的独立配置
    if (aid !== SHARED_AGENT_ID) {
      const own = this.readJson(this.agentPath(aid));
      if (own?.odoo) return own;
    }

    // 2) 共享（default）配置 —— 即使 aid === default 也走这里
    const shared = this.readJson(this.sharedPath());
    if (shared?.odoo) return shared;

    // 3) legacy 兼容
    const legacy = this.readJson(this.legacyPath);
    if (legacy?.odoo) return legacy;

    return null;
  }

  /**
   * 判断 agent 是否有自己独立的配置文件（不走 fallback）
   * 用于 odoo_disconnect 判断"断开的是独立还是共享"
   */
  hasOwnConfig(agentId: string): boolean {
    const aid = sanitizeAgentId(agentId);
    if (aid === SHARED_AGENT_ID) return false;
    return existsSync(this.agentPath(aid));
  }

  /**
   * 判断共享配置是否存在
   */
  hasSharedConfig(): boolean {
    return existsSync(this.sharedPath()) || existsSync(this.legacyPath);
  }

  /**
   * 返回当前 agent 实际命中的配置来源
   *   agent  — 命中 {agentId}.json
   *   shared — 命中 default.json
   *   legacy — 命中 odoo-config.json
   *   none   — 都没有（可能需要 pluginConfig 兜底，由调用方处理）
   */
  getActiveSource(agentId: string = SHARED_AGENT_ID): ConfigSource {
    const aid = sanitizeAgentId(agentId);
    if (aid !== SHARED_AGENT_ID && existsSync(this.agentPath(aid))) return 'agent';
    if (existsSync(this.sharedPath())) return 'shared';
    if (existsSync(this.legacyPath)) return 'legacy';
    return 'none';
  }

  /**
   * 保存完整配置到指定文件
   */
  private save(config: OdooPluginConfig, targetPath: string): boolean {
    try {
      if (!existsSync(this.baseDir)) {
        mkdirSync(this.baseDir, { recursive: true });
      }
      writeFileSync(targetPath, JSON.stringify(config, null, 2), 'utf-8');
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 保存 Odoo 连接凭据
   *
   * @param odooConfig 要保存的凭据
   * @param agentId    当前 agent（决定 scope=agent 时写哪个文件）
   * @param scope      'agent'（v1.23 起默认）写到 {agentId}.json，仅当前 sender_id
   *                   生效，配合 Odoo 内部 RBAC 区分权限；
   *                   'shared' 写到 default.json，全员共用同一 Odoo 账号（Odoo
   *                   RBAC 失效，仅适合"组织内只有一个 Odoo 公共只读账号"场景）。
   */
  saveOdooConfig(
    odooConfig: OdooConfig,
    agentId: string = SHARED_AGENT_ID,
    scope: 'shared' | 'agent' = 'agent',
  ): boolean {
    const targetPath = scope === 'agent'
      ? this.agentPath(agentId)
      : this.sharedPath();

    // 合并现有配置（保留 sync 等其他字段）
    const existing = this.readJson(targetPath) ?? {};
    existing.odoo = odooConfig;
    return this.save(existing, targetPath);
  }

  /**
   * 清除当前 agent 的独立配置文件（如果存在）
   * 返回是否真删了东西
   */
  clearOwnConfig(agentId: string): boolean {
    try {
      const path = this.agentPath(agentId);
      if (existsSync(path)) {
        unlinkSync(path);
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  /**
   * 清除共享凭据 —— 危险操作，会让所有无独立配置的 agent 断开
   */
  clearSharedConfig(): boolean {
    let cleared = false;
    try {
      if (existsSync(this.sharedPath())) { unlinkSync(this.sharedPath()); cleared = true; }
    } catch { /* noop */ }
    try {
      if (existsSync(this.legacyPath)) { unlinkSync(this.legacyPath); cleared = true; }
    } catch { /* noop */ }
    return cleared;
  }

  /**
   * 旧接口保留兼容 —— 默认行为是清除当前 agent 自己的配置（不碰共享）
   */
  clear(agentId: string = SHARED_AGENT_ID): boolean {
    if (sanitizeAgentId(agentId) === SHARED_AGENT_ID) return this.clearSharedConfig();
    return this.clearOwnConfig(agentId);
  }

  /** 列出所有已保存配置的 agentId（包括共享 default） */
  listAgents(): string[] {
    try {
      if (!existsSync(this.baseDir)) return [];
      return readdirSync(this.baseDir)
        .filter(f => f.endsWith('.json'))
        .map(f => f.replace(/\.json$/, ''));
    } catch {
      return [];
    }
  }
}
