#!/usr/bin/env node
// tests/mock-knowledge-server.js · v3.3.0 测试用
//
// 模拟 server /api/knowledge/ingest v2 的 4 种响应:
//   1. created
//   2. no_change
//   3. soft_chain_override
//   4. conflict
//
// 用法:
//   node tests/mock-knowledge-server.js
//   OPPHUB_API_BASE=http://localhost:4001 opphub knowledge-submit --cards cards.json
//
// 内部状态: in-memory Map, key = SHA256(userId|type|dimension), value = {rawText, contentHash}

import { createServer } from "node:http";
import { createHash } from "node:crypto";

const PORT = parseInt(process.env.MOCK_PORT || "4001", 10);
const store = new Map(); // idempotencyKey -> { rawText, contentHash, entryId }

function sha256(s) { return createHash("sha256").update(s, "utf8").digest("hex"); }
function cuid() { return "cm_" + Math.random().toString(36).slice(2, 14); }

function diffRawText(oldText, newText) {
  // 简化的关键字段冲突检测
  const oldFields = extractKeyFields(oldText);
  const newFields = extractKeyFields(newText);
  const conflictFields = [];
  for (const key of ["legal_person", "business_direction"]) {
    if (oldFields[key] && newFields[key] && oldFields[key] !== newFields[key]) {
      conflictFields.push(`${key}: ${oldFields[key]} → ${newFields[key]}`);
    }
  }
  return { hasConflict: conflictFields.length > 0, conflictFields };
}

function extractKeyFields(text) {
  const fields = {};
  const lp = text.match(/法[定]?人[::]?\s*([^\n]+)/);
  if (lp) {
    // 只取法人名, 不包括后续内容
    const m = lp[1].match(/^([^\s,，;；]+)/);
    if (m) fields.legal_person = m[1];
  }
  if (boss) {
    const m = boss[1].match(/^([^\s,，;；]+)/);
    if (m) fields.legal_person = m[1];
  }
  const bd = text.match(/业务方向[::]?\s*([^\n]+)/);
  if (bd) fields.business_direction = bd[1].trim();
  return fields;
}

const server = createServer(async (req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (req.url !== "/api/knowledge/ingest" || req.method !== "POST") {
    res.statusCode = 404;
    res.end(JSON.stringify({ ok: false, error: "not_found" }));
    return;
  }
  const body = await new Promise(r => {
    let chunks = [];
    req.on("data", c => chunks.push(c));
    req.on("end", () => r(Buffer.concat(chunks).toString("utf8")));
  });
  const data = JSON.parse(body || "{}");
  const { userId, rawText, entryType, entryDimension, idempotencyKey, contentHash, forceOverride } = data;
  
  const existing = store.get(idempotencyKey);
  
  if (!existing) {
    // 1. created
    const entryId = cuid();
    store.set(idempotencyKey, { rawText, contentHash, entryId });
    res.end(JSON.stringify({ ok: true, action: "created", entryId, status: "pending" }));
    return;
  }
  
  if (existing.contentHash === contentHash) {
    // 2. no_change
    res.end(JSON.stringify({ ok: true, action: "no_change", entryId: existing.entryId }));
    return;
  }
  
  const diff = diffRawText(existing.rawText, rawText);
  if (diff.hasConflict && !forceOverride) {
    // 4. conflict
    res.end(JSON.stringify({
      ok: false,
      conflict: true,
      conflictReport: {
        entryId: existing.entryId,
        oldRawText: existing.rawText,
        newRawText: rawText,
        conflictFields: diff.conflictFields,
        diffType: "key_field_conflict",
      },
    }));
    return;
  }
  
  // 3. soft_chain_override
  const oldEntryId = existing.entryId;
  const newEntryId = cuid();
  store.set(idempotencyKey, { rawText, contentHash, entryId: newEntryId, previousEntryId: oldEntryId });
  res.end(JSON.stringify({
    ok: true,
    action: "soft_chain_override",
    entryId: newEntryId,
    previousEntryId: oldEntryId,
    supersededEntry: { id: oldEntryId, supersededAt: new Date().toISOString() },
  }));
});

server.listen(PORT, () => {
  console.log(`🧪 Mock knowledge server on http://localhost:${PORT}`);
  console.log(`   POST /api/knowledge/ingest`);
  console.log(`   4 种响应: created / no_change / soft_chain_override / conflict`);
});
