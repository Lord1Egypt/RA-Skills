// evidence.mjs — 证据文件归档（户型图/政府公示/政策 PDF/截图），纯函数 + 落盘助手
// 存储约定（SoT：modes/scan.md「证据归档」节）：
//   房源级  data/evidence/{platform}-{listing_id}/{YYYYMMDD}-{type}[-{note}].{ext}
//   共享级  data/policy/{YYYYMMDD}-{type}[-{note}].{ext}   （政策 PDF/规划公示等非单房源文件）
// 每条归档必须登记进扫描记录的 evidence 数组（type/path/source_url/captured_at/note）。

import { copyFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

export const EVIDENCE_TYPES = ['huxing', 'photo', 'gov_notice', 'policy_pdf', 'screenshot', 'other'];

export function evidenceTypeValid(type) {
  return EVIDENCE_TYPES.includes(type);
}

export function isHttpUrl(src) {
  return /^https?:\/\//i.test(src ?? '');
}

// 归档文件名：{YYYYMMDD}-{type}[-{note-slug}].{ext}
export function buildEvidenceName({ captured_at, type, note = '', src = '', customName = '' }) {
  if (customName) return customName;
  const ext = customName.includes('.') ? '' : (path.extname(src ?? '') || '.bin').toLowerCase();
  const date = String(captured_at ?? '').replaceAll('-', '') || 'nodate';
  const slug = String(note ?? '').replace(/[^\w\u4e00-\u9fa5]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 24);
  return `${date}-${type}${slug ? '-' + slug : ''}${ext || '.bin'}`;
}

// 归档目录：policy_pdf/gov_notice 等非单房源文件进 data/policy/，其余进房源文件夹
export function evidenceDirFor({ type, platform, listing_id }, dirs) {
  if (type === 'policy_pdf' || type === 'gov_notice') return dirs.policyDir;
  if (platform && listing_id) return path.join(dirs.evidenceDir, `${platform}-${listing_id}`);
  return dirs.evidenceDir;
}

// 单条证据登记项
export function evidenceEntry({ type, relPath, src, captured_at, note = '' }) {
  return {
    type,
    path: relPath,
    source_url: isHttpUrl(src) ? src : '',
    captured_at: captured_at || new Date().toISOString().slice(0, 10),
    note: note || '',
  };
}

/**
 * 归档一个证据文件：复制（本地）或下载（http）到规范路径。
 * 纯 I/O 编排——命名/目录/登记项构造逻辑见上方纯函数（可测）。
 */
export async function evidenceSave({ recordPath, type, src, note = '', name = '', referer = '', captured_at = '', scansDir, evidenceDir, policyDir }) {
  if (!evidenceTypeValid(type)) {
    throw new Error(`未知证据类型 "${type}"——可选：${EVIDENCE_TYPES.join(' | ')}`);
  }
  const { readFile } = await import('node:fs/promises');
  const record = JSON.parse(await readFile(recordPath, 'utf8'));
  const capturedAt = captured_at || new Date().toISOString().slice(0, 10);
  const dirs = { evidenceDir, policyDir };

  const dir = evidenceDirFor({ type, platform: record.platform, listing_id: record.listing_id }, { evidenceDir, policyDir });
  await mkdir(dir, { recursive: true });

  const fileName = buildEvidenceName({ captured_at: capturedAt, type, note, src, customName: name });
  const absPath = path.join(dir, fileName);

  if (isHttpUrl(src)) {
    const res = await fetch(src, { headers: referer ? { Referer: referer } : {} });
    if (!res.ok) throw new Error(`下载失败 HTTP ${res.status}（防盗链时可先从浏览器另存为本地文件再归档）`);
    const buf = Buffer.from(await res.arrayBuffer());
    if (buf.length < 1024) throw new Error(`下载内容仅 ${buf.length} 字节——疑似占位/防盗链响应，已放弃（可从浏览器另存后按本地路径归档）`);
    await writeFile(absPath, buf);
  } else {
    await copyFile(src, absPath);
  }

  const relPath = path.relative(path.dirname(recordPath), absPath);
  record.evidence ??= [];
  const entry = evidenceEntry({ type, relPath, src, captured_at: capturedAt, note });
  record.evidence.push(entry);

  await writeFile(recordPath, JSON.stringify(record, null, 2) + '\n', 'utf8');
  return { savedPath: absPath, relPath, entry, index: record.evidence.length - 1 };
}

// 列出扫描记录已归档证据（list 子命令展示用）
export async function evidenceListOf(record) {
  return record.evidence ?? [];
}
