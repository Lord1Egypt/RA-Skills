#!/usr/bin/env node
/**
 * 验证 mock-jsonv2 mock 模式的基础路由：spaces/feed、forms/feed、fielddef、list、create、update、delete。
 * 不连接真实魔方环境。
 */

import { spawn } from 'child_process';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const script = resolve(__dirname, 'mock-jsonv2.mjs');
const mockDir = resolve(root, 'assets/mock-data');
const spaceId = '00000000-0000-0000-0000-000000000001';
const formId = '00000000-0000-0000-0000-000000000002';

function once(emitter, event) {
  return new Promise((resolveOnce) => emitter.once(event, resolveOnce));
}

async function waitForReady(baseUrl) {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}?selector=fielddef&lng=en`);
      if (res.ok) return;
    } catch {
      /* retry */
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  throw new Error('mock-jsonv2 未在 10s 内就绪');
}

async function expectJson(res, label) {
  const text = await res.text();
  if (!res.ok) throw new Error(`${label} HTTP ${res.status}: ${text.slice(0, 300)}`);
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${label} 响应非 JSON: ${text.slice(0, 300)}`);
  }
}

async function main() {
  const port = 3857;
  const baseUrl = `http://127.0.0.1:${port}`;
  const child = spawn(process.execPath, [script, '--port', String(port), '--dir', mockDir], {
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  let stderr = '';
  child.stderr.on('data', (buf) => {
    stderr += buf.toString('utf8');
  });

  try {
    const earlyExit = Promise.race([
      waitForReady(baseUrl).then(() => null),
      once(child, 'exit').then((code) => ({ code })),
    ]);
    const exited = await earlyExit;
    if (exited) throw new Error(`mock-jsonv2 提前退出: ${exited.code}\n${stderr}`);

    const spaces = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/json/spaces/feed?start=0&limit=10&bq=(label,eq,示例空间)`),
      'spaces/feed'
    );
    if (spaces.items?.[0]?.id !== spaceId || spaces.items[0].label !== '示例空间') {
      throw new Error(`spaces/feed 返回异常: ${JSON.stringify(spaces)}`);
    }

    const forms = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/json/${spaceId}/forms/feed?start=0&limit=-1`),
      'forms/feed'
    );
    if (forms.feed?.entry?.[0]?.id !== formId || forms.feed.entry[0].content?.form?.label !== '示例表') {
      throw new Error(`forms/feed 返回异常: ${JSON.stringify(forms)}`);
    }

    const fielddef = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}?selector=fielddef&lng=en`),
      'fielddef'
    );
    if (!Array.isArray(fielddef.fields) || !fielddef.fields.some((f) => f.name === 'jine')) {
      throw new Error('fielddef 未包含模板字段 jine');
    }

    const list1 = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry?start=0&limit=10`),
      'list'
    );
    if (!Array.isArray(list1.entry) || list1.totalCount !== 2) {
      throw new Error(`list 返回异常: ${JSON.stringify(list1)}`);
    }

    const listAll = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry?start=0&limit=-1`),
      'list all'
    );
    if (!Array.isArray(listAll.entry) || listAll.entry.length !== 2) {
      throw new Error(`list all 返回异常: ${JSON.stringify(listAll)}`);
    }

    const created = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mingcheng: 'Smoke', jine: 300 }),
      }),
      'create'
    );
    if (!created.id || created.mingcheng !== 'Smoke') {
      throw new Error(`create 返回异常: ${JSON.stringify(created)}`);
    }

    const updated = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry/${created.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jine: 301 }),
      }),
      'update'
    );
    if (updated.jine !== 301) throw new Error(`update 返回异常: ${JSON.stringify(updated)}`);

    const deleted = await expectJson(
      await fetch(`${baseUrl}/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry/${created.id}`, {
        method: 'DELETE',
      }),
      'delete'
    );
    if (deleted.ok !== true) throw new Error(`delete 返回异常: ${JSON.stringify(deleted)}`);

    console.log('mock-jsonv2 smoke passed');
  } finally {
    child.kill('SIGTERM');
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
