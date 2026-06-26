#!/usr/bin/env node

/**
 * mofang-records CLI entry point
 * OpenClaw agents call this via exec:
 *   node cli.mjs <command> '<json-params>'
 *
 * Config is read from env vars:
 *   MOFANG_BASE_URL / BASE_URL
 *   MOFANG_USERNAME / USERNAME
 *   MOFANG_PASSWORD / PASSWORD
 *
 * Or from a .env file in the same directory as this script.
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ── .env loader (no dependencies) ──────────────────────────────

function loadDotEnv() {
  try {
    const envPath = join(__dirname, '.env');
    const content = readFileSync(envPath, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIdx = trimmed.indexOf('=');
      if (eqIdx < 1) continue;
      const key = trimmed.slice(0, eqIdx).trim();
      let val = trimmed.slice(eqIdx + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      if (!(key in process.env)) {
        process.env[key] = val;
      }
    }
  } catch {
    // .env not found — that's fine
  }
}

loadDotEnv();

// ── Config from env ────────────────────────────────────────────

function getConfig() {
  return {
    BASE_URL: process.env.MOFANG_BASE_URL || process.env.BASE_URL || '',
    USERNAME: process.env.MOFANG_USERNAME || process.env.USERNAME || '',
    PASSWORD: process.env.MOFANG_PASSWORD || process.env.PASSWORD || '',
  };
}

// ── Command routing table ──────────────────────────────────────

const COMMANDS = {
  mofang_test_connection: {
    load: () => import('./dist/health.js'),
    exportName: 'handler',
    desc: '测试连接和配置',
    skipConfigCheck: true,
  },
  mofang_list_spaces: {
    load: () => import('./dist/spaces.js'),
    exportName: 'handler',
    desc: '列出/搜索空间 (q?, spaceHint?, page?, pageSize?, all?)',
  },
  mofang_list_forms: {
    load: () => import('./dist/forms.js'),
    exportName: 'handler',
    desc: '列出空间下表单 (spaceHint?)',
  },
  mofang_get_field_definitions: {
    load: () => import('./dist/fields.js'),
    exportName: 'handler',
    desc: '获取表单字段定义 (formHint, spaceHint?)',
  },
  mofang_query_records: {
    load: () => import('./dist/records.js'),
    exportName: 'queryRecordsHandler',
    desc: '查询记录 (formHint, filters?, page?, pageSize?)',
  },
  mofang_create_record: {
    load: () => import('./dist/records.js'),
    exportName: 'createRecordHandler',
    desc: '创建记录 (formHint, data)',
  },
  mofang_update_record: {
    load: () => import('./dist/records.js'),
    exportName: 'updateRecordHandler',
    desc: '修改记录 (formHint, recordId, data)',
  },
  mofang_delete_record: {
    load: () => import('./dist/records.js'),
    exportName: 'deleteRecordHandler',
    desc: '删除记录 (formHint, recordId)',
  },
  mofang_bpm_list_tasks: {
    load: () => import('./dist/bpm.js'),
    exportName: 'listBpmTasksHandler',
    desc: 'BPM 待办列表 (mode?, page?, pageSize?, processDefinitionKey?, descriptionLike?)',
  },
  mofang_bpm_query_tasks: {
    load: () => import('./dist/bpm.js'),
    exportName: 'queryBpmTasksHandler',
    desc: 'BPM 条件查询任务 (formHint?, recordId?, processDefinitionName?, taskName?, page?, pageSize?)',
  },
  mofang_bpm_get_task: {
    load: () => import('./dist/bpm.js'),
    exportName: 'getBpmTaskHandler',
    desc: 'BPM 任务详情与变量 (taskId)',
  },
  mofang_bpm_complete_task: {
    load: () => import('./dist/bpm.js'),
    exportName: 'completeBpmTaskHandler',
    desc: 'BPM 提交/完成任务 (taskId, simple?, variables?)',
  },
  mofang_bpm_delegate_task: {
    load: () => import('./dist/bpm.js'),
    exportName: 'delegateBpmTaskHandler',
    desc: 'BPM 转办 (taskId, assignee)',
  },
  mofang_bpm_claim_task: {
    load: () => import('./dist/bpm.js'),
    exportName: 'claimBpmTaskHandler',
    desc: 'BPM 认领组任务 (taskId, assignee?)',
  },
  mofang_bpm_resolve_task: {
    load: () => import('./dist/bpm.js'),
    exportName: 'resolveBpmTaskHandler',
    desc: 'BPM 归还委托 (resolve) (taskId)',
  },
  mofang_bpm_jump_task: {
    load: () => import('./dist/bpm.js'),
    exportName: 'jumpBpmTaskHandler',
    desc: 'BPM 跳转: 终止/驳回/取回 (taskId, kind, jumpTargetId?, targetTaskName?)',
  },
  mofang_bpm_open_transaction: {
    load: () => import('./dist/bpm.js'),
    exportName: 'openBpmTransactionHandler',
    desc: 'BPM 开启事务如加签 (taskAction, processName?, taskName?, processKey?, taskId?, processInstId?)',
  },
  mofang_bpm_close_transaction: {
    load: () => import('./dist/bpm.js'),
    exportName: 'closeBpmTransactionHandler',
    desc: 'BPM 关闭事务 (transactionId)',
  },
};

// ── Help ───────────────────────────────────────────────────────

function printHelp() {
  const lines = [
    'mofang-records CLI',
    '',
    'Usage: node cli.mjs <command> \'<json-params>\'',
    '',
    'Commands:',
  ];
  for (const [name, info] of Object.entries(COMMANDS)) {
    lines.push(`  ${name.padEnd(34)} ${info.desc}`);
  }
  lines.push('');
  lines.push('Environment variables:');
  lines.push('  MOFANG_BASE_URL   魔方网表服务器地址（优先于 BASE_URL）');
  lines.push('  MOFANG_USERNAME   登录用户名（优先于 USERNAME；.env 里若已设 MOFANG_USERNAME，仅设 USERNAME 不会覆盖）');
  lines.push('  MOFANG_PASSWORD   登录密码（优先于 PASSWORD）');
  console.log(lines.join('\n'));
}

// ── Main ───────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    process.exit(0);
  }

  const command = args[0];
  const route = COMMANDS[command];

  if (!route) {
    const out = { success: false, message: `Unknown command: ${command}. Run with --help to see available commands.` };
    console.log(JSON.stringify(out));
    process.exit(1);
  }

  let params = {};
  if (args[1]) {
    try {
      params = JSON.parse(args[1]);
    } catch (e) {
      const out = { success: false, message: `Invalid JSON params: ${e.message}` };
      console.log(JSON.stringify(out));
      process.exit(1);
    }
  }

  const config = getConfig();
  if (!route.skipConfigCheck && !config.BASE_URL) {
    const out = { success: false, message: 'MOFANG_BASE_URL (or BASE_URL) environment variable is not set.' };
    console.log(JSON.stringify(out));
    process.exit(1);
  }

  const context = { config };

  const mod = await route.load();
  const handler = mod[route.exportName];

  if (typeof handler !== 'function') {
    const out = { success: false, message: `Handler "${route.exportName}" not found in module for command "${command}".` };
    console.log(JSON.stringify(out));
    process.exit(1);
  }

  const result = await handler(params, context);
  console.log(JSON.stringify(result));
}

main().catch((err) => {
  const out = { success: false, message: `CLI error: ${err.message || String(err)}` };
  console.log(JSON.stringify(out));
  process.exit(1);
});
