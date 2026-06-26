import { LoroDoc } from 'loro-crdt';
import * as fs from 'fs';
import * as path from 'path';
// @ts-ignore
import { run as agentComm } from '../agent-comm-skill/index.ts';

const SESSIONS_PATH = path.join(process.cwd(), 'data/sessions');

function ensureDir() {
  if (!fs.existsSync(SESSIONS_PATH)) fs.mkdirSync(SESSIONS_PATH, { recursive: true });
}

export async function run(action: string, params: any) {
  ensureDir();
  try {
    switch (action) {
      case 'team.create': return await createTeam(params);
      case 'team.sync': return await syncTeam(params);
      case 'team.load': return await loadTeam(params);
      default: return { success: false, error: `Action ${action} unsupported` };
    }
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

/**
 * 创建会话：仅写入初始 Snapshot
 */
async function createTeam(params: any) {
  const { taskName } = params;
  if (!taskName) return { success: false, error: "Missing taskName" };
  
  const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;
  const doc = new LoroDoc();
  doc.getMap('metadata').set('taskName', taskName);
  
  // 基础快照文件
  const snapshotPath = path.join(SESSIONS_PATH, `${sessionId}.snapshot`);
  fs.writeFileSync(snapshotPath, doc.export({ mode: 'snapshot' }));
  
  // 初始化空的增量日志文件
  const updatesPath = path.join(SESSIONS_PATH, `${sessionId}.updates`);
  fs.writeFileSync(updatesPath, Buffer.alloc(0));

  return { success: true, data: { sessionId } };
}

/**
 * 增量同步：性能 O(1)
 * 仅验证签名并追加写入二进制日志，不再读取/重写全量快照
 */
async function syncTeam(params: any) {
  const { sessionId, updatePayload, publicKeyHex, signatureHex } = params;
  
  if (!sessionId || !updatePayload || !publicKeyHex || !signatureHex) {
    return { success: false, error: "Zero-Trust Violation" };
  }

  // 🛡️ 1. 签名验证 (不耗费磁盘 IO)
  const verifyRes = await agentComm('message.verify', {
    publicKeyHex,
    payload: updatePayload,
    signatureHex
  }) as any;

  if (!verifyRes.success || !verifyRes.data!.verified) {
    return { success: false, error: "Signature Verification Failed" };
  }

  // 🛡️ 2. 极致性能 IO：追加写入 (Append-only)
  const updatesPath = path.join(SESSIONS_PATH, `${sessionId}.updates`);
  if (!fs.existsSync(updatesPath)) return { success: false, error: "Session updates log not found" };

  const binaryUpdate = Buffer.from(updatePayload, 'base64');
  
  // 使用 appendFileSync 确保原子化追加，性能极高
  fs.appendFileSync(updatesPath, binaryUpdate);
  
  console.log(`⚡ [Operator] 性能优化：增量片段已追加至日志 (Size: ${binaryUpdate.length} bytes)`);

  return { success: true, data: { status: "Deltas Appended" } };
}

/**
 * 按需加载：读取快照 + 顺序回放日志
 */
async function loadTeam(params: any) {
  const { sessionId } = params;
  const snapshotPath = path.join(SESSIONS_PATH, `${sessionId}.snapshot`);
  const updatesPath = path.join(SESSIONS_PATH, `${sessionId}.updates`);
  
  if (!fs.existsSync(snapshotPath)) return { success: false, error: "Session not found" };

  // 1. 加载基础快照
  const doc = new LoroDoc();
  doc.import(fs.readFileSync(snapshotPath));

  // 2. 如果存在增量日志，顺序合入
  if (fs.existsSync(updatesPath)) {
    const allUpdates = fs.readFileSync(updatesPath);
    if (allUpdates.length > 0) {
      doc.import(allUpdates);
    }
  }

  return { 
    success: true, 
    data: { 
      payload: Buffer.from(doc.export({ mode: 'snapshot' })).toString('base64'),
      format: 'full-merged-snapshot'
    } 
  };
}
