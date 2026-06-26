import lark from '@larksuiteoapi/node-sdk';
import { baseError } from './errors.js';

function normalizeDomain(domain) {
  if (!domain || domain === 'feishu') return lark.Domain.Feishu;
  if (domain === 'lark') return lark.Domain.Lark;
  return domain;
}

export function createFeishuClient(accountConfig) {
  if (!accountConfig?.appId || !accountConfig?.appSecret) {
    throw baseError(
      'FEISHU_NOT_CONFIGURED',
      'Missing Feishu appId/appSecret. Runtime config did not provide channels.feishu and persisted config fallback did not resolve usable credentials.',
      {
        accountId: accountConfig?.accountId,
        hasAppId: Boolean(accountConfig?.appId),
        hasAppSecret: Boolean(accountConfig?.appSecret),
      },
    );
  }

  return new lark.Client({
    appId: accountConfig.appId,
    appSecret: accountConfig.appSecret,
    domain: normalizeDomain(accountConfig.domain),
  });
}
