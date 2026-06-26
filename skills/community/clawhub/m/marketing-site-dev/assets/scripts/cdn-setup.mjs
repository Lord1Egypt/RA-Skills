#!/usr/bin/env node
/**
 * End-to-end CDN setup via `ve` CLI:
 *   1. Find ZID of the domain in ve dns
 *   2. Ensure _dnsauth TXT has the current verification token
 *   3. Submit ve dcdn VerifyDomainOwnership, poll until success
 *   4. ve cdn AddCdnDomain × 2 (apex + www)
 *   5. ve cdn StartCdnDomain × 2
 *   6. Read CNAME targets, upsert CNAME records in ve dns
 *
 * Idempotent — re-running picks up wherever it left off.
 */
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import config from '../deploy.config.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const payloadDir = join(here, 'cdn-payloads');

const apex = config.cdnDomains[0];
const www = config.cdnDomains[1];
const apexParts = apex.split('.');
const zoneName = apexParts.slice(-2).join('.');

function ve(...args) {
  const r = spawnSync('ve', args, { encoding: 'utf8' });
  if (r.status !== 0 && !r.stdout.startsWith('{')) {
    throw new Error(`ve ${args.join(' ')}\n${r.stderr || r.stdout}`);
  }
  try {
    return JSON.parse(r.stdout);
  } catch {
    throw new Error(`ve ${args[0]} ${args[1]} returned non-JSON:\n${r.stdout}`);
  }
}

function step(msg) {
  console.log(`\n▶ ${msg}`);
}

// ---------- 1. find zone ----------
step(`1/6  查找 zone: ${zoneName}`);
const zones = ve('dns', 'ListZones', '--SearchKeyWord', zoneName);
const zone = (zones.Result?.Zones || []).find((z) => z.ZoneName === zoneName);
if (!zone) {
  console.error(`  ✗ 在 ve dns 找不到 zone ${zoneName}. 先在控制台添加。`);
  process.exit(1);
}
const ZID = zone.ZID;
console.log(`  ✓ ZID=${ZID}`);

// ---------- 2. ensure _dnsauth TXT ----------
step(`2/6  写入 _dnsauth TXT`);
const verify = ve('dcdn', 'DescribeVerifyContent', '--DomainName', apex);
const token = verify.Result?.Content;
if (verify.Result?.Verified) {
  console.log(`  ✓ 已验证过，跳过`);
} else {
  console.log(`  当前 token: ${token}`);
  const list = ve('dns', 'ListRecords', '--body', JSON.stringify({ ZID, Host: '_dnsauth', PageSize: 50 }));
  const records = list.Result?.Records || [];
  const matching = records.filter((r) => r.Value === token);
  const stale = records.filter((r) => r.Value !== token);
  for (const r of stale) {
    console.log(`  - 删除过期记录 ${r.RecordID} (${r.Value.slice(0, 40)}…)`);
    ve('dns', 'DeleteRecord', '--body', JSON.stringify({ RecordID: r.RecordID }));
  }
  if (matching.length === 0) {
    const created = ve('dns', 'CreateRecord', '--body', JSON.stringify({
      ZID,
      Host: '_dnsauth',
      Type: 'TXT',
      Value: token,
      TTL: 600,
      Line: 'default',
      Remark: 'Volcengine CDN domain ownership verification',
    }));
    console.log(`  ✓ 创建 TXT RecordID=${created.Result?.RecordID}`);
  } else {
    console.log(`  ✓ TXT 已存在 (RecordID=${matching[0].RecordID})`);
  }
}

// ---------- 3. verify ownership (poll) ----------
step(`3/6  验证归属权（火山引擎修改 TXT 后约需 10 分钟生效）`);
let verified = verify.Result?.Verified;
const maxAttempts = 30;
let attempt = 0;
while (!verified && attempt < maxAttempts) {
  attempt += 1;
  const v = ve('dcdn', 'VerifyDomainOwnership', '--body', JSON.stringify({
    DomainName: apex,
    VerifyType: 'dns',
  }));
  verified = v.Result?.Result === true;
  if (verified) {
    console.log(`  ✓ 验证通过 (attempt ${attempt})`);
    break;
  }
  process.stdout.write(`  [attempt ${attempt}/${maxAttempts}] ${v.Result?.Message || '失败'}\n`);
  if (attempt < maxAttempts) await new Promise((r) => setTimeout(r, 30000));
}
if (!verified) {
  console.error(`\n  ✗ 验证仍未通过。请再等 10 分钟后重跑本脚本。`);
  console.error(`    或在控制台手工点 "重新验证":`);
  console.error(`    https://console.volcengine.com/cdn/domain/owndomain`);
  process.exit(2);
}

// ---------- 4-5. AddCdnDomain + StartCdnDomain ----------
step(`4/6  注册并启用 CDN 域名`);
const existingCdn = ve('cdn', 'ListCdnDomains');
const existingDomains = (existingCdn.Result?.Data || []).map((d) => d.Domain);
for (const [name, file] of [[apex, 'apex.json'], [www, 'www.json']]) {
  if (existingDomains.includes(name)) {
    console.log(`  - ${name} 已注册，跳过`);
    continue;
  }
  const body = readFileSync(join(payloadDir, file), 'utf8');
  const add = ve('cdn', 'AddCdnDomain', '--body', body);
  if (add.ResponseMetadata?.Error) {
    console.error(`  ✗ AddCdnDomain ${name} 失败:`, add.ResponseMetadata.Error.Message);
    process.exit(3);
  }
  console.log(`  ✓ ${name} 已注册`);
  const start = ve('cdn', 'StartCdnDomain', '--Domain', name);
  if (!start.ResponseMetadata?.Error) console.log(`  ✓ ${name} 已启用`);
}

// ---------- 6. read CNAME targets, upsert CNAME records ----------
step(`5/6  拉取 CNAME 目标`);
const finalList = ve('cdn', 'ListCdnDomains');
const targets = (finalList.Result?.Data || []).filter((d) => [apex, www].includes(d.Domain));
const cnameMap = new Map();
for (const t of targets) {
  console.log(`  ${t.Domain.padEnd(35)} → ${t.Cname}`);
  cnameMap.set(t.Domain, t.Cname);
}

step(`6/6  在 ve dns 写入 CNAME 解析`);
const allRecords = ve('dns', 'ListRecords', '--body', JSON.stringify({ ZID, PageSize: 100 }));
const allRecs = allRecords.Result?.Records || [];

for (const [name, cname] of cnameMap) {
  const host = name === zoneName ? '@' : name.slice(0, -(zoneName.length + 1));
  const existing = allRecs.find((r) => r.Host === host && r.Type === 'CNAME');
  if (existing && existing.Value.replace(/\.$/, '') === cname.replace(/\.$/, '')) {
    console.log(`  - ${host}.${zoneName} CNAME 已指向 ${cname}`);
    continue;
  }
  if (existing) {
    ve('dns', 'UpdateRecord', '--body', JSON.stringify({
      RecordID: existing.RecordID,
      Host: host,
      Type: 'CNAME',
      Value: cname,
      TTL: 600,
      Line: 'default',
    }));
    console.log(`  ✓ ${host}.${zoneName} CNAME 已更新 → ${cname}`);
  } else {
    ve('dns', 'CreateRecord', '--body', JSON.stringify({
      ZID,
      Host: host,
      Type: 'CNAME',
      Value: cname,
      TTL: 600,
      Line: 'default',
      Remark: 'Volcengine CDN',
    }));
    console.log(`  ✓ ${host}.${zoneName} CNAME 已创建 → ${cname}`);
  }
}

console.log(`\n✓ 完成。等 1-3 分钟 DNS 生效后访问：`);
console.log(`  http://${apex}/`);
console.log(`  http://${www}/`);
console.log(`\n下一步：申请 / 上传 SSL 证书并通过 \`ve cdn BatchDeployCert\` 绑定，启用 HTTPS。`);
