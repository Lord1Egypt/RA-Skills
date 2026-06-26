#!/usr/bin/env node
/**
 * 验证 fetch-form-spec --import-json 离线输出结构，以及按空间/表单名称解析真实接口的路径。
 * 不连接真实魔方环境。
 */

import { mkdtempSync, readFileSync, rmSync, existsSync } from 'fs';
import { tmpdir } from 'os';
import { dirname, join, resolve } from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const script = resolve(__dirname, 'fetch-form-spec.mjs');
const mockScript = resolve(__dirname, 'mock-jsonv2.mjs');
const mockDir = resolve(root, 'assets/mock-data');
const spaceId = '00000000-0000-0000-0000-000000000001';
const formId = '00000000-0000-0000-0000-000000000002';
const fielddef = resolve(root, 'assets/mock-data', formId, 'fielddef.json');

function runNode(args, cwd) {
  return new Promise((resolveRun, rejectRun) => {
    const child = spawn(process.execPath, args, { cwd, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (b) => {
      stdout += b.toString('utf8');
    });
    child.stderr.on('data', (b) => {
      stderr += b.toString('utf8');
    });
    child.on('exit', (code) => {
      if (code === 0) resolveRun({ stdout, stderr });
      else rejectRun(new Error(`命令失败 ${code}\n${stdout}\n${stderr}`));
    });
  });
}

async function waitForReady(baseUrl) {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`${baseUrl}/magicflu/service/json/spaces/feed?start=0&limit=1`);
      if (res.ok) return;
    } catch {
      /* retry */
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  throw new Error('mock-jsonv2 未在 10s 内就绪');
}

async function main() {
  const work = mkdtempSync(join(tmpdir(), 'mofang-fetch-import-smoke-'));
  const labelWork = mkdtempSync(join(tmpdir(), 'mofang-fetch-label-smoke-'));
  const port = 3861;
  const baseUrl = `http://127.0.0.1:${port}`;
  const child = spawn(process.execPath, [mockScript, '--port', String(port), '--dir', mockDir], {
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let mockStderr = '';
  child.stderr.on('data', (buf) => {
    mockStderr += buf.toString('utf8');
  });

  try {
    await runNode(
      [
        script,
        '--spaceId',
        spaceId,
        '--formId',
        formId,
        '--out',
        './mock-data',
        '--import-json',
        fielddef,
      ],
      work
    );

    const out = join(work, 'mock-data');
    const expected = [
      'manifest.json',
      'typesnippets.md',
      'api-outline.md',
      join(formId, 'fielddef.json'),
      join(formId, 'records.seed.json'),
    ];
    for (const rel of expected) {
      if (!existsSync(join(out, rel))) throw new Error(`缺少输出文件: ${rel}`);
    }

    const manifest = JSON.parse(readFileSync(join(out, 'manifest.json'), 'utf8'));
    if (manifest.spaceId !== spaceId || manifest.forms?.[0]?.formId !== formId) {
      throw new Error(`manifest 内容异常: ${JSON.stringify(manifest)}`);
    }

    const records = JSON.parse(readFileSync(join(out, formId, 'records.seed.json'), 'utf8'));
    if (!Array.isArray(records)) throw new Error('records.seed.json 不是数组');

    await waitForReady(baseUrl);
    await runNode(
      [
        script,
        '--baseUrl',
        baseUrl,
        '--spaceLabel',
        '示例空间',
        '--formLabel',
        '示例表',
        '--out',
        './mock-data',
        '--cookie',
        'mock=1',
      ],
      labelWork
    );

    const labelOut = join(labelWork, 'mock-data');
    const labelManifest = JSON.parse(readFileSync(join(labelOut, 'manifest.json'), 'utf8'));
    if (
      labelManifest.spaceId !== spaceId ||
      labelManifest.spaceLabel !== '示例空间' ||
      labelManifest.forms?.[0]?.formId !== formId
    ) {
      throw new Error(`名称解析 manifest 异常: ${JSON.stringify(labelManifest)}`);
    }

    console.log('fetch-form-spec import smoke passed');
  } finally {
    child.kill('SIGTERM');
    rmSync(work, { recursive: true, force: true });
    rmSync(labelWork, { recursive: true, force: true });
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
