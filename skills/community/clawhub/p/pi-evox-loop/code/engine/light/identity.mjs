/**
 * engine/light/identity.mjs — 基因 provenance 签名链（0.21，1.0 判据之一）
 *
 * 设计：每台机器一个 Ed25519 身份（keypair 存 ~/.evomap/identity/，零依赖，Node 内置 crypto）。
 *   - 沉淀（distill/draft）时用私钥对基因内容签名 → 基因带 {sig, keyid, pubkey} 字段；
 *   - 入池（gene submit）时签名随基因一起导出（submit 不过滤这些字段）；
 *   - 导入（gene import）时用随附 pubkey 验签：内容被篡改 → 拒绝；keyid 不认识 → 接受但警告
 *     （无法验证 ≠ 有问题；老基因无签名字段 → 原样接受，legacy）。
 *   - 验签用公钥、不暴露私钥；私钥文件权限 0600，绝不出本机（脱敏闸门另有一道）。
 *
 * 签名域：asset_id + 规范化基因内容（去掉签名字段后的稳定 JSON）。
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';

const IDENTITY_DIR = process.env.EVO_IDENTITY_DIR || path.join(os.homedir(), '.evomap', 'identity');
const PRIV_PATH = path.join(IDENTITY_DIR, 'identity.pem');
const PUB_PATH = path.join(IDENTITY_DIR, 'identity.pub.pem');

function ensureDir() { try { fs.mkdirSync(IDENTITY_DIR, { recursive: true }); } catch { /* 已存在 */ } }

/** 生成或加载本机身份；返回 {keyId, privateKey, publicKey}（PEM 字符串） */
export function loadIdentity() {
  if (fs.existsSync(PRIV_PATH) && fs.existsSync(PUB_PATH)) {
    const privateKey = fs.readFileSync(PRIV_PATH, 'utf8');
    const publicKey = fs.readFileSync(PUB_PATH, 'utf8');
    return { keyId: keyIdOf(publicKey), privateKey, publicKey };
  }
  ensureDir();
  const { privateKey, publicKey } = crypto.generateKeyPairSync('ed25519');
  const privPem = privateKey.export({ type: 'pkcs8', format: 'pem' });
  const pubPem = publicKey.export({ type: 'spki', format: 'pem' });
  fs.writeFileSync(PRIV_PATH, privPem, { mode: 0o600 });
  fs.writeFileSync(PUB_PATH, pubPem);
  return { keyId: keyIdOf(pubPem), privateKey: privPem, publicKey: pubPem };
}

/** 身份目录与私钥路径（展示/诊断用） */
export function identityDir() { return IDENTITY_DIR; }
export function privateKeyPath() { return PRIV_PATH; }

/** keyid = pubkey 的 sha256 前 16 hex（稳定短标识） */
export function keyIdOf(publicKeyPem) {
  return crypto.createHash('sha256').update(publicKeyPem).digest('hex').slice(0, 16);
}

/**
 * 规范化签名域。
 *
 * ⚠️ 有两个版本，且**必须并存**：
 *  - v1（历史）：`JSON.stringify(rest, Object.keys(rest).sort())`。replacer 数组会被应用到
 *    **每一层嵌套对象** ⇒ 嵌套里不在顶层键名列表中的属性被**静默丢弃**，不在签名域内。
 *    实测后果：改嵌套内容后验签仍是 `verified`（ClawHub clawscan 于 0.30.0 点名）。
 *  - v2（0.31 起）：递归规范化，所有嵌套内容都进签名域。
 * 若直接把 v1 换成 v2，存量已签名基因会**集体验签失败**并被判 `tampered`
 * （`gene import` 会直接 BLOCK 导入）⇒ 因此按 `sig_v` 分派，存量基因继续用 v1 验，
 * 新签名一律 v2。用户可跑 `light-cli resign --yes` 把存量升级到 v2。
 */
const SIG_META = ['sig', 'keyid', 'pubkey', 'signed_at', 'sig_v'];
export const SIG_V2 = 2;

function stripMeta(gene) {
  const rest = { ...(gene || {}) };
  for (const k of SIG_META) delete rest[k];
  return rest;
}

/** v1：与历史行为逐字节一致（仅用于验签存量基因，不再用于签名） */
function canonicalV1(gene) {
  const rest = stripMeta(gene);
  return String(rest.asset_id || '') + '\n' + JSON.stringify(rest, Object.keys(rest).sort());
}

/** v2：递归规范化——对象按键排序、数组保序，嵌套内容全部纳入签名域 */
function canonicalValue(v) {
  if (Array.isArray(v)) return '[' + v.map(canonicalValue).join(',') + ']';
  if (v && typeof v === 'object') {
    return '{' + Object.keys(v).sort()
      .map((k) => JSON.stringify(k) + ':' + canonicalValue(v[k])).join(',') + '}';
  }
  return JSON.stringify(v === undefined ? null : v);
}

function canonicalV2(gene) {
  const rest = stripMeta(gene);
  return String(rest.asset_id || '') + '\n' + canonicalValue(rest);
}

/** 按基因自带的 sig_v 分派；缺省视为 v1（legacy） */
function canonical(gene) {
  return Number(gene && gene.sig_v) === SIG_V2 ? canonicalV2(gene) : canonicalV1(gene);
}

/** 给基因签名（原地补 {sig, keyid, pubkey, signed_at} 并返回同一对象） */
export function signGene(gene) {
  if (!gene || !gene.asset_id) return gene;
  const { privateKey, publicKey, keyId } = loadIdentity();
  gene.sig_v = SIG_V2; // 先打版本，再用 v2 规范化（canonicalV2 会剔除 sig_v 自身）
  const data = Buffer.from(canonicalV2(gene), 'utf8');
  const sig = crypto.sign(null, data, privateKey).toString('base64');
  gene.sig = sig; gene.keyid = keyId; gene.pubkey = publicKey; gene.signed_at = new Date().toISOString();
  return gene;
}

/**
 * 验签。pubkeyPem 省略时用基因自带 pubkey。
 * 返回 {ok, status, why}：status = 'verified' | 'tampered' | 'unsigned' | 'bad-format' | 'unverifiable'
 */
export function verifyGene(gene, pubkeyPem) {
  if (!gene || !gene.asset_id) return { ok: false, status: 'bad-format', why: '基因缺少 asset_id' };
  if (!gene.sig) return { ok: true, status: 'unsigned', why: '无签名字段（legacy 基因，原样接受）' };
  const pem = pubkeyPem || gene.pubkey;
  if (!pem) return { ok: true, status: 'unverifiable', why: '有 sig 但无 pubkey，无法验证' };
  try {
    const v2 = Number(gene.sig_v) === SIG_V2;
    const data = Buffer.from(v2 ? canonicalV2(gene) : canonicalV1(gene), 'utf8');
    const ok = crypto.verify(null, data, pem, Buffer.from(String(gene.sig), 'base64'));
    if (ok) {
      // v1（legacy）虽然验签通过，但其签名域不含嵌套内容 —— 明确告知，不静默当作同等强度。
      const note = v2 ? '签名有效' : '签名有效（v1 规范化：嵌套字段不在签名域，建议 light-cli resign 升级）';
      return { ok: true, status: 'verified', why: `${note}（keyid=${gene.keyid || '?'}）` };
    }
    return { ok: false, status: 'tampered', why: '签名与内容不匹配——基因可能被篡改' };
  } catch (e) {
    return { ok: true, status: 'unverifiable', why: `验签异常（${e.message}）——按无法验证处理` };
  }
}

/** 0.25 维1：license token（JWT-lite：base64url(payload).base64url(sig)） */
const b64u = (buf) => Buffer.from(buf).toString('base64url');
const unb64u = (s) => Buffer.from(String(s), 'base64url').toString('utf8');

export function signLicense(payload, privateKeyPem) {
  const body = b64u(JSON.stringify(payload));
  const sig = crypto.sign(null, Buffer.from(body), privateKeyPem).toString('base64url');
  return body + '.' + sig;
}

export function verifyLicense(token, publicKeyPem) {
  const parts = String(token || '').split('.');
  if (parts.length !== 2) return { ok: false, reason: 'token 格式错误（应为 payload.signature）' };
  try {
    const ok = crypto.verify(null, Buffer.from(parts[0]), publicKeyPem, Buffer.from(parts[1], 'base64url'));
    if (!ok) return { ok: false, reason: '签名无效' };
    return { ok: true, payload: JSON.parse(unb64u(parts[0])) };
  } catch (e) { return { ok: false, reason: '解析失败: ' + String(e.message || e) }; }
}
