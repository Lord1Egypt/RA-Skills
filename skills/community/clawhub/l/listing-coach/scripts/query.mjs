#!/usr/bin/env node
import { createHash, createHmac, randomUUID } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const COLLECTION_NAME = process.env.VOLCENGINE_KB_COLLECTION ?? 'app';
const PROJECT_NAME = process.env.VOLCENGINE_KB_PROJECT ?? 'default';
const BASE_HOST = normalizeHost(
  process.env.VOLCENGINE_KB_HOST ?? 'api-knowledxxxxxe.mlp.cn-beijing.volces.com',
);
const BASE_URL = `http://${BASE_HOST}`;
const ACCESS_KEY_ID =
  process.env.VOLCENGINE_ACCESS_KEY_ID ??
  'AKLTZTQ4MmExxxxxyMzgWJlYzQ';
const SECRET_ACCESS_KEY =
  process.env.VOLCENGINE_SECRET_ACCESS_KEY ??
  'TWpCa01qRTNNR1xxxxxlUTmlOalJrTURNd01';
const SERVICE = process.env.VOLCENGINE_SERVICE ?? 'air';
const REGION = process.env.VOLCENGINE_REGION ?? 'cn-north-1';
const SEARCH_PATH = '/api/knowledge/collection/search_knowledge';

const question = process.argv.slice(2).join(' ').trim();
if (!question) {
  process.stderr.write('Usage: node query.mjs "<question>"\n');
  process.exit(1);
}

const startedAt = Date.now();
const body = JSON.stringify(buildSearchBody(question));
const headers = signRequest({
  method: 'POST',
  path: SEARCH_PATH,
  query: {},
  body,
  host: BASE_HOST,
  accessKeyId: ACCESS_KEY_ID,
  secretAccessKey: SECRET_ACCESS_KEY,
  service: SERVICE,
  region: REGION,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json; charset=utf-8',
    Host: BASE_HOST,
  },
});

const res = await fetch(`${BASE_URL}${SEARCH_PATH}`, {
  method: 'POST',
  headers,
  body,
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

if (!res.ok || (typeof data?.code === 'number' && data.code !== 0)) {
  process.stderr.write(
    `API error ${res.status}: ${data?.message ?? data?.msg ?? res.statusText}\n`,
  );
  process.stderr.write(raw + '\n');
  process.exit(1);
}

const output = formatSearchResult(data, elapsedSec);
const outFile = join(
  tmpdir(),
  `listing-coach-result-${Date.now()}-${process.pid}-${randomUUID()}.md`,
);
writeFileSync(outFile, output, { encoding: 'utf8', flag: 'wx' });
process.stdout.write(outFile + '\n');

function buildSearchBody(query) {
  return {
    project: PROJECT_NAME,
    name: COLLECTION_NAME,
    query,
    limit: Number(process.env.VOLCENGINE_KB_LIMIT ?? 10),
    pre_processing: {
      need_instruction: true,
      return_token_usage: true,
      messages: [
        {
          role: 'system',
          content: '',
        },
        {
          role: 'user',
        },
      ],
    },
    dense_weight: Number(process.env.VOLCENGINE_KB_DENSE_WEIGHT ?? 0.5),
    post_processing: {
      get_attachment_link: true,
      rerank_only_chunk: false,
      rerank_switch: false,
    },
    image_query: process.env.VOLCENGINE_KB_IMAGE_QUERY ?? '',
  };
}

function signRequest({
  method,
  path,
  query,
  body,
  host,
  accessKeyId,
  secretAccessKey,
  service,
  region,
  headers,
}) {
  const xDate = getDateTimeNow();
  const bodyHash = sha256(body);
  const signedSourceHeaders = {
    ...headers,
    Host: host,
    'X-Date': xDate,
    'X-Content-Sha256': bodyHash,
  };
  const signedHeaders = {};

  for (const [key, value] of Object.entries(signedSourceHeaders)) {
    if (key === 'Content-Type' || key === 'Content-Md5' || key === 'Host' || key.startsWith('X-')) {
      signedHeaders[key.toLowerCase()] = normalizeHeaderValue(value);
    }
  }

  if (signedHeaders.host?.includes(':')) {
    const [hostName, port] = signedHeaders.host.split(':');
    if (port === '80' || port === '443') {
      signedHeaders.host = hostName;
    }
  }

  const signedHeaderNames = Object.keys(signedHeaders).sort();
  const signedHeaderText = signedHeaderNames
    .map((key) => `${key}:${signedHeaders[key]}`)
    .join('\n');
  const signedHeaderNamesText = signedHeaderNames.join(';');
  const canonicalRequest = [
    method.toUpperCase(),
    normUri(path),
    normQuery(query),
    `${signedHeaderText}\n`,
    signedHeaderNamesText,
    bodyHash,
  ].join('\n');

  const credentialDate = xDate.slice(0, 8);
  const credentialScope = [credentialDate, region, service, 'request'].join('/');
  const stringToSign = [
    'HMAC-SHA256',
    xDate,
    credentialScope,
    sha256(canonicalRequest),
  ].join('\n');
  const signingKey = getSigningKey(secretAccessKey, credentialDate, region, service);
  const signature = hmacHex(signingKey, stringToSign);

  return {
    ...signedSourceHeaders,
    Authorization:
      `HMAC-SHA256 Credential=${accessKeyId}/${credentialScope}, ` +
      `SignedHeaders=${signedHeaderNamesText}, Signature=${signature}`,
  };
}

function formatSearchResult(data, elapsedSec) {
  const resultList = data?.data?.result_list ?? data?.result_list ?? [];
  const tokenUsage = data?.data?.token_usage ?? data?.token_usage ?? {};
  const totalTokens = sumTokenUsage(tokenUsage);
  const lines = [];

  lines.push('Search results');
  lines.push(
    `Elapsed ${elapsedSec} s | Total tokens ${totalTokens} | Request ID: ${data?.request_id ?? '-'}`,
  );
  lines.push('');

  if (!Array.isArray(resultList) || resultList.length === 0) {
    lines.push('(No results found.)');
    return `${lines.join('\n')}\n`;
  }

  for (let i = 0; i < resultList.length; i++) {
    const item = resultList[i];
    const docName = item?.doc_info?.doc_name ?? item?.doc_info?.title ?? item?.doc_name ?? 'Unknown';
    const chunkTitle = (item?.chunk_title ?? item?.title ?? '').trim();
    const score = typeof item?.score === 'number' ? item.score.toFixed(4) : '-';
    const content = (item?.content ?? item?.text ?? '').trim();

    lines.push('---');
    lines.push(`NO.${i + 1} | Recall score ${score}`);
    if (chunkTitle) {
      lines.push(`**${chunkTitle}**`);
    }
    lines.push('');
    if (content) {
      lines.push(content);
    }
    lines.push('');
    lines.push(`Source: ${docName}`);
    lines.push('');
  }

  return `${lines.join('\n')}\n`;
}

function sumTokenUsage(value) {
  if (!value || typeof value !== 'object') {
    return 0;
  }

  let total = 0;
  for (const [key, nested] of Object.entries(value)) {
    if (key === 'total_tokens' && typeof nested === 'number') {
      total += nested;
    } else if (typeof nested === 'number' && key.endsWith('_tokens')) {
      total += nested;
    } else if (nested && typeof nested === 'object') {
      total += sumTokenUsage(nested);
    }
  }
  return total;
}

function getSigningKey(secretAccessKey, date, region, service) {
  const kDate = hmac(secretAccessKey, date);
  const kRegion = hmac(kDate, region);
  const kService = hmac(kRegion, service);
  return hmac(kService, 'request');
}

function hmac(key, content) {
  return createHmac('sha256', key).update(content, 'utf8').digest();
}

function hmacHex(key, content) {
  return createHmac('sha256', key).update(content, 'utf8').digest('hex');
}

function sha256(content) {
  return createHash('sha256').update(content ?? '', 'utf8').digest('hex');
}

function normUri(path) {
  return percentEncode(path || '/').replace(/%2F/g, '/');
}

function normQuery(params) {
  return Object.keys(params ?? {})
    .sort()
    .flatMap((key) => {
      const value = params[key];
      if (Array.isArray(value)) {
        return value.map((item) => `${percentEncode(key)}=${percentEncode(item)}`);
      }
      return `${percentEncode(key)}=${percentEncode(value)}`;
    })
    .join('&')
    .replace(/\+/g, '%20');
}

function percentEncode(value) {
  return encodeURIComponent(String(value ?? '')).replace(/[!'()*]/g, (char) =>
    `%${char.charCodeAt(0).toString(16).toUpperCase()}`,
  );
}

function normalizeHeaderValue(value) {
  return String(value ?? '').trim().replace(/\s+/g, ' ');
}

function normalizeHost(value) {
  let host = String(value ?? '').trim();
  const markdownLink = host.match(/^\[[^\]]+\]\(([^)]+)\)$/);
  if (markdownLink) {
    host = markdownLink[1];
  }
  if (/^https?:\/\//i.test(host)) {
    return new URL(host).host;
  }
  return host.replace(/^\/+/, '').replace(/\/.*$/, '');
}

function getDateTimeNow() {
  return new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
}
