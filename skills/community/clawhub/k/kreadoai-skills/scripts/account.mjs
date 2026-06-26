#!/usr/bin/env node
/**
 * KreadoAI — 账号：查询余额/会员到期时间、配置凭证
 */
import { kreadoGet } from './shared/client.mjs';
import {
  getApiToken,
  writeToken,
  maskToken,
  promptInteractiveToken,
  getCredentialsFilePath,
} from './shared/auth.mjs';
import { parseArgs, getTokenOrExit } from './shared/args.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const API_GET_INFO = '/apis/open/user/v3/getInfo';

function printHelp() {
  console.log(`KreadoAI account — 余额、会员信息、凭证配置

用法：
  node kreado.mjs account [选项]
  node kreado.mjs account --info     （默认：查询余额和 VIP 到期时间）
  node kreado.mjs account --configure
  node kreado.mjs account --import-token <token>

--info（默认）
  GET ${API_GET_INFO}
  返回 K-Coin 余额和会员到期时间。

--configure
  交互式输入并保存 API Token。

--import-token <token>
  直接保存 API Token（无需交互）。

环境变量：
  KREADO_API_TOKEN          API Token（在 KreadoAI 账号 -> API 设置中获取）
  KREADO_STORAGE_ROOT       可选，凭证存储根目录`);
}

export async function main() {
  const args = parseArgs(process.argv, ['info', 'configure']);

  if (args.help) {
    printHelp();
    return;
  }

  if (args.configure) {
    try {
      await promptInteractiveToken();
    } catch (e) {
      console.error(`错误：${e?.message || e}`);
      process.exit(1);
    }
    return;
  }

  if (args['import-token']) {
    const token = typeof args['import-token'] === 'string' ? args['import-token'] : '';
    if (!token) {
      console.error('错误：--import-token 需要提供 Token 值');
      process.exit(1);
    }
    const savePath = writeToken(token);
    console.error(`✓ Token 已保存：${savePath}`);
    console.error(`  Token（脱敏）：${maskToken(token)}`);
    return;
  }

  const token = getTokenOrExit();
  try {
    const data = await kreadoGet(API_GET_INFO, token);
    console.error('账号状态：OK');
    console.log(JSON.stringify(data, null, 2));
  } catch (e) {
    console.error(`错误：${e?.message || e}`);
    process.exit(1);
  }
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(__filename) === resolve(process.argv[1])) {
  main().catch((e) => {
    console.error(`错误：${e?.message || e}`);
    process.exit(1);
  });
}
