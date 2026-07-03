#!/usr/bin/env node
import { randomUUID } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const API_KEY = 'AXT0Z4NERS4SJR11MDEG0C1HJYZXKNZ60GXDM80VERE6PWG6V1SG60R30D1Q70T3C';
const SERVICE_RESOURCE_ID = 'kb-service-4f2ab940e1b403e';
const BASE_URL = 'http://api-knowledgebase.mlp.cn-beijing.volces.com';

const question = process.argv[2];
if (!question?.trim()) {
  process.stderr.write('Usage: node query.mjs "<question>"\n');
  process.exit(1);
}

const startedAt = Date.now();
const res = await fetch(`${BASE_URL}/api/knowledge/service/chat`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    service_resource_id: SERVICE_RESOURCE_ID,
    stream: false,
    messages: [{ role: 'user', content: question.trim() }],
  }),
  signal: AbortSignal.timeout(30000),
});

const raw = await res.text();
const elapsedSec = ((Date.now() - startedAt) / 1000).toFixed(2);
let data;
try {
  data = JSON.parse(raw);
} catch {
  data = null;
}

if (!res.ok) {
  process.stderr.write(`API error ${res.status}: ${data?.message ?? res.statusText}\n`);
  process.stderr.write(raw + '\n');
  process.exit(1);
}

const resultList = data?.data?.result_list ?? [];

// Token usage, mirroring the official console's "共使用 N tokens".
const tu = data?.data?.token_usage ?? {};
const totalTokens =
  (tu?.embedding_token_usage?.total_tokens ?? 0) + (tu?.rerank_token_usage ?? 0);

// Header + ranked result cards, matching the official console's layout.
const lines = [];
lines.push('检索结果');
lines.push(`总耗时 ${elapsedSec} s | 共使用 ${totalTokens} tokens | Request ID: ${data?.request_id ?? '-'}`);
lines.push('');

if (!resultList.length) {
  lines.push('（无检索结果 / No results found.）');
} else {
  for (let i = 0; i < resultList.length; i++) {
    const item = resultList[i];
    const docName = item?.doc_info?.doc_name ?? 'Unknown';
    const chunkTitle = (item?.chunk_title ?? '').trim();
    const score = typeof item?.score === 'number' ? item.score.toFixed(4) : '-';
    const content = (item?.content ?? '').trim();

    lines.push('---');
    lines.push(`NO.${i + 1} | 召回分数 ${score}`);
    if (chunkTitle) lines.push(`**${chunkTitle}**`);
    lines.push('');
    if (content) lines.push(content);
    lines.push('');
    lines.push(`📄 来源: ${docName}`);
    lines.push('');
  }
}

const outFile = join(
  tmpdir(),
  `listing-coach-result-${Date.now()}-${process.pid}-${randomUUID()}.md`,
);
writeFileSync(outFile, lines.join('\n') + '\n', { encoding: 'utf8', flag: 'wx' });
process.stdout.write(outFile + '\n');
