#!/usr/bin/env node
/**
 * Offline parameter-validation smoke test.
 *
 * This intentionally avoids child_process spawning so it remains stable in
 * Windows/sandboxed agents where spawning node.exe can return EPERM.
 */

import {
  getBpmTaskHandler,
  jumpBpmTaskHandler,
  delegateBpmTaskHandler,
  openBpmTransactionHandler,
  closeBpmTransactionHandler,
  queryBpmTasksHandler,
  listBpmTasksHandler,
  completeBpmTaskHandler,
} from '../dist/bpm.js';

const context = {
  config: {
    BASE_URL: 'http://127.0.0.1:9',
    USERNAME: 'smoke',
    PASSWORD: 'smoke',
  },
};

const cases = [
  ['mofang_bpm_get_task', getBpmTaskHandler, {}, '需要 taskId'],
  ['mofang_bpm_jump_task', jumpBpmTaskHandler, { taskId: '1' }, 'kind'],
  ['mofang_bpm_delegate_task', delegateBpmTaskHandler, { taskId: '1' }, 'assignee'],
  ['mofang_bpm_open_transaction', openBpmTransactionHandler, {}, 'taskAction'],
  ['mofang_bpm_close_transaction', closeBpmTransactionHandler, {}, 'transactionId'],
  ['mofang_bpm_query_tasks', queryBpmTasksHandler, { recordId: '1' }, 'formHint'],
  ['mofang_bpm_list_tasks', listBpmTasksHandler, { mode: 'nope' }, 'mode'],
  ['mofang_bpm_complete_task', completeBpmTaskHandler, { taskId: '1', simple: true }, 'variables'],
];

console.log('smoke-cli-validation: param checks');
for (const [name, handler, params, needle] of cases) {
  const result = await handler(params, context);
  if (result?.success) {
    console.error('FAIL expected failure:', name, result);
    process.exit(1);
  }
  if (!result?.message || !String(result.message).includes(needle)) {
    console.error('FAIL message mismatch', name, result?.message, 'expected contains:', needle);
    process.exit(1);
  }
  console.log('  ok', name);
}

try {
  JSON.parse('{x}');
  console.error('FAIL invalid JSON handling');
  process.exit(1);
} catch (err) {
  if (!String(err.message || err).includes('JSON')) {
    console.error('FAIL invalid JSON error shape', err);
    process.exit(1);
  }
  console.log('  ok invalid JSON');
}

console.log('all param-validation checks passed.');
