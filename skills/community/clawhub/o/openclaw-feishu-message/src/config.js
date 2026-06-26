import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

export function resolvePluginConfig(pluginConfig = {}) {
  return {
    enabled: pluginConfig.enabled !== false,
    defaultAccountId: typeof pluginConfig.defaultAccountId === 'string' && pluginConfig.defaultAccountId ? pluginConfig.defaultAccountId : undefined,
    allowSend: pluginConfig.allowSend !== false,
    defaultReceiveIdType: typeof pluginConfig.defaultReceiveIdType === 'string' && pluginConfig.defaultReceiveIdType ? pluginConfig.defaultReceiveIdType : 'open_id',
    debug: pluginConfig.debug === true,
  };
}

function readPersistedOpenClawConfig() {
  const candidates = [
    process.env.OPENCLAW_CONFIG_PATH,
    path.join(os.homedir(), '.openclaw', 'openclaw.json'),
  ].filter(Boolean);

  for (const file of candidates) {
    try {
      if (!fs.existsSync(file)) continue;
      const raw = fs.readFileSync(file, 'utf8');
      return JSON.parse(raw);
    } catch {
      // ignore and continue fallback search
    }
  }

  return {};
}

function pickFeishuConfig(runtimeLike = {}) {
  const runtimeChannels =
    runtimeLike?.config?.channels ||
    runtimeLike?.cfg?.channels ||
    runtimeLike?.channels;

  if (runtimeChannels?.feishu?.appId || runtimeChannels?.feishu?.app_id || runtimeChannels?.feishu?.accounts) {
    return runtimeChannels.feishu;
  }

  const persisted = readPersistedOpenClawConfig();
  return persisted?.channels?.feishu || {};
}

function pickImplicitRuntimeAccountId(runtimeLike = {}) {
  return (
    runtimeLike?.accountId ||
    runtimeLike?.account_id ||
    runtimeLike?.session?.accountId ||
    runtimeLike?.session?.account_id ||
    runtimeLike?.context?.accountId ||
    runtimeLike?.context?.account_id ||
    runtimeLike?.meta?.accountId ||
    runtimeLike?.meta?.account_id ||
    runtimeLike?.channelContext?.accountId ||
    runtimeLike?.channelContext?.account_id ||
    runtimeLike?.config?.accountId ||
    runtimeLike?.cfg?.accountId ||
    undefined
  );
}

export function resolveFeishuAccountConfig(runtimeLike = {}, pluginCfg = {}, requestedAccountId = undefined) {
  const feishu = pickFeishuConfig(runtimeLike);
  const accounts = feishu.accounts || {};
  const implicitRuntimeAccountId = pickImplicitRuntimeAccountId(runtimeLike);
  const accountId = requestedAccountId || implicitRuntimeAccountId || pluginCfg.defaultAccountId || feishu.defaultAccountId || feishu.defaultAccount || Object.keys(accounts)[0] || 'default';
  const account = accounts[accountId] || feishu;

  return {
    accountId,
    appId: account?.appId || account?.app_id,
    appSecret: account?.appSecret || account?.app_secret,
    domain: account?.domain || feishu?.domain || 'feishu',
    raw: account,
    _debug: {
      requestedAccountId,
      implicitRuntimeAccountId,
      pluginDefaultAccountId: pluginCfg.defaultAccountId,
      feishuDefaultAccountId: feishu.defaultAccountId,
      feishuDefaultAccount: feishu.defaultAccount,
      knownAccounts: Object.keys(accounts),
    },
  };
}
