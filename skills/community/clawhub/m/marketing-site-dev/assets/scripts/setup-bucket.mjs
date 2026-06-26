#!/usr/bin/env node
/**
 * One-time TOS bucket setup:
 *   1. Create the bucket (public-read, Standard storage)
 *   2. Enable static website hosting (index.html / 404.html)
 *
 * Idempotent — re-running on an existing bucket reapplies the website config.
 */
import process from 'node:process';
import { TosClient, TosServerError } from '@volcengine/tos-sdk';
import config from '../deploy.config.mjs';

for (const k of ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']) {
  delete process.env[k];
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

if (!accessKey || !secretKey) {
  console.error('[setup] 缺少 VOLC_ACCESS_KEY / VOLC_SECRET_KEY，请检查 .env');
  process.exit(1);
}

const bucket = process.env.TOS_BUCKET || config.bucket;
const region = process.env.TOS_REGION || config.region;
const endpoint = process.env.TOS_ENDPOINT || config.endpoint;

const client = new TosClient({
  accessKeyId: accessKey,
  accessKeySecret: secretKey,
  region,
  endpoint,
});

console.log(`[setup] bucket=${bucket} region=${region}`);

try {
  await client.headBucket(bucket);
  console.log('[setup] bucket 已存在，跳过创建');
} catch (err) {
  if (err instanceof TosServerError && err.statusCode === 404) {
    console.log('[setup] bucket 不存在，正在创建…');
    await client.createBucket({
      bucket,
      acl: 'public-read',
      storageClass: 'STANDARD',
    });
    console.log('[setup] ✓ bucket 创建成功');
  } else {
    console.error('[setup] headBucket 失败：', err.message || err);
    process.exit(1);
  }
}

console.log('[setup] 配置静态网站托管 (index.html / 404.html)…');
await client.putBucketWebsite({
  bucket,
  indexDocument: {
    suffix: 'index.html',
  },
  errorDocument: {
    key: '404.html',
  },
});
console.log('[setup] ✓ 静态网站托管已启用');

console.log(
  `\n[setup] 完成。TOS 原始访问域：\n  https://${bucket}.${endpoint}/index.html\n` +
    `\n  下一步：pnpm deploy\n`,
);
