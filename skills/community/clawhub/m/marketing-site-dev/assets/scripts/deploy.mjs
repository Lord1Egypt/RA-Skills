#!/usr/bin/env node
/**
 * Volcengine TOS deployment script.
 *
 * Run via `pnpm deploy` — that wraps `node --env-file=.env` so .env is auto-loaded.
 *
 * Credentials (any of these names works):
 *   VOLC_ACCESS_KEY / VOLC_ACCESSKEY / VOLCENGINE_ACCESSKEY / TOS_ACCESS_KEY
 *   VOLC_SECRET_KEY / VOLC_SECRETKEY / VOLCENGINE_SECRETKEY / TOS_SECRET_KEY
 *
 * Optional:
 *   VOLC_SESSION_TOKEN — when using STS temporary credentials
 *   TOS_BUCKET / TOS_REGION / TOS_ENDPOINT — override deploy.config.mjs
 *
 * Behavior:
 *   1. Walks dist/ recursively
 *   2. Uploads every file with the right Content-Type and Cache-Control
 *   3. Deletes objects in the bucket that no longer exist locally (sync semantics)
 */

import { readdir, stat, readFile } from 'node:fs/promises';
import { join, relative, posix, sep } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import process from 'node:process';
import mime from 'mime';
import { TosClient, TosServerError } from '@volcengine/tos-sdk';

import config from '../deploy.config.mjs';

// TOS lives inside China and shouldn't go through a foreign HTTP proxy.
// axios picks up these env vars globally, so scrub them for this process.
for (const key of [
  'HTTP_PROXY',
  'HTTPS_PROXY',
  'http_proxy',
  'https_proxy',
  'ALL_PROXY',
  'all_proxy',
]) {
  delete process.env[key];
}

const accessKey =
  process.env.VOLC_ACCESS_KEY ||
  process.env.VOLC_ACCESSKEY ||
  process.env.VOLCENGINE_ACCESSKEY ||
  process.env.TOS_ACCESS_KEY;
const secretKey =
  process.env.VOLC_SECRET_KEY ||
  process.env.VOLC_SECRETKEY ||
  process.env.VOLCENGINE_SECRETKEY ||
  process.env.TOS_SECRET_KEY;
const sessionToken =
  process.env.VOLC_SESSION_TOKEN || process.env.TOS_SESSION_TOKEN;

if (!accessKey || !secretKey) {
  console.error(
    '\n[deploy] 缺少凭证。请在 .env 中设置：\n' +
      '  VOLC_ACCESS_KEY=AKLT...\n' +
      '  VOLC_SECRET_KEY=...\n' +
      '（或在 shell 中 export 同名变量）\n' +
      '可在 https://console.volcengine.com/iam/keymanage/ 创建。\n',
  );
  process.exit(1);
}

const bucket = process.env.TOS_BUCKET || config.bucket;
const region = process.env.TOS_REGION || config.region;
const endpoint = process.env.TOS_ENDPOINT || config.endpoint;
const distDir = config.distDir;

const client = new TosClient({
  accessKeyId: accessKey,
  accessKeySecret: secretKey,
  stsToken: sessionToken,
  region,
  endpoint,
});

function pickCacheControl(key) {
  for (const rule of config.cacheRules || []) {
    if (key === rule.prefix || key.startsWith(rule.prefix)) {
      return rule.cacheControl;
    }
  }
  return config.defaultCacheControl;
}

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(full);
    } else if (entry.isFile()) {
      yield full;
    }
  }
}

function toKey(absPath, rootAbs) {
  return relative(rootAbs, absPath).split(sep).join(posix.sep);
}

function md5Base64(buf) {
  return createHash('md5').update(buf).digest('base64');
}

async function listAllRemote() {
  const seen = new Map();
  let continuationToken;
  while (true) {
    // SDK signs every key in the params object, but axios drops undefined values
    // from the URL — only include continuationToken when actually paging.
    const input = { bucket, maxKeys: 1000, listOnlyOnce: true };
    if (continuationToken) input.continuationToken = continuationToken;
    const res = await client.listObjectsType2(input);
    for (const obj of res.data?.Contents ?? []) {
      seen.set(obj.Key, obj.ETag?.replace(/"/g, '') ?? '');
    }
    if (!res.data?.IsTruncated) break;
    continuationToken = res.data?.NextContinuationToken;
    if (!continuationToken) break;
  }
  return seen;
}

async function ensureBucketExists() {
  try {
    await client.headBucket(bucket);
  } catch (err) {
    if (err instanceof TosServerError && err.statusCode === 404) {
      console.error(
        `\n[deploy] Bucket "${bucket}" 不存在。请先用 ve CLI 创建（见 DEPLOY.md §2）。\n`,
      );
    } else {
      console.error('[deploy] 访问 bucket 失败：', err.message || err);
    }
    process.exit(1);
  }
}

async function uploadFile(absPath, key) {
  const body = await readFile(absPath);
  const contentType =
    mime.getType(key) || 'application/octet-stream';
  const cacheControl = pickCacheControl(key);

  await client.putObject({
    bucket,
    key,
    body,
    contentType,
    cacheControl,
    contentMD5: md5Base64(body),
    acl: 'public-read',
  });

  return body.length;
}

async function main() {
  console.log(
    `[deploy] bucket=${bucket} region=${region} endpoint=${endpoint}`,
  );
  await ensureBucketExists();

  const distAbs = fileURLToPath(new URL(`../${distDir}/`, import.meta.url));
  let local;
  try {
    local = (await stat(distAbs)).isDirectory() ? distAbs : null;
  } catch {
    local = null;
  }
  if (!local) {
    console.error(
      `\n[deploy] ${distDir}/ 不存在。请先运行 \`pnpm build\`。\n`,
    );
    process.exit(1);
  }

  console.log('[deploy] 收集本地文件…');
  const localKeys = new Set();
  const files = [];
  for await (const abs of walk(distAbs)) {
    const key = toKey(abs, distAbs);
    files.push({ abs, key });
    localKeys.add(key);
  }
  console.log(`[deploy] 本地共 ${files.length} 个文件`);

  console.log('[deploy] 拉取桶内对象清单…');
  const remote = await listAllRemote();
  console.log(`[deploy] 桶内现有 ${remote.size} 个对象`);

  let uploaded = 0;
  let bytes = 0;
  for (const { abs, key } of files) {
    const size = await uploadFile(abs, key);
    uploaded += 1;
    bytes += size;
    process.stdout.write(
      `\r[deploy] 上传 ${uploaded}/${files.length}  (${(bytes / 1024).toFixed(1)} KB)   `,
    );
  }
  process.stdout.write('\n');

  // delete remote objects no longer in local
  const toDelete = [...remote.keys()].filter((k) => !localKeys.has(k));
  if (toDelete.length > 0) {
    console.log(`[deploy] 删除桶内过期对象 ${toDelete.length} 个…`);
    // batch delete in chunks of 1000
    for (let i = 0; i < toDelete.length; i += 1000) {
      const chunk = toDelete.slice(i, i + 1000);
      await client.deleteMultiObjects({
        bucket,
        objects: chunk.map((Key) => ({ key: Key })),
        quiet: true,
      });
    }
  }

  console.log(`\n[deploy] ✓ 完成。已上传 ${uploaded} 个文件 / 删除 ${toDelete.length} 个旧对象`);
  console.log(
    `[deploy] → https://${bucket}.${endpoint}/index.html  (TOS 原始域)`,
  );
  console.log(
    `[deploy] → 通过 CDN 访问：${config.cdnDomains
      ?.map((d) => `https://${d}/`)
      .join('  ')}`,
  );
  console.log(
    `[deploy] 提示：发布后可执行 \`pnpm cdn:refresh\` 刷新 CDN 缓存`,
  );
}

main().catch((err) => {
  console.error('\n[deploy] 失败：', err?.message || err);
  if (err?.requestId) console.error('  requestId =', err.requestId);
  process.exit(1);
});
