/**
 * Minimal Volcengine OpenAPI client — SigV4 signing, zero deps.
 * Use for actions not exposed by the `ve` CLI binary (e.g. CDN DescribeRetrieveInfo,
 * CheckCdnDomain — these exist in the API but the CLI we have is stale).
 *
 * Reads credentials from env: VOLC_ACCESS_KEY / VOLC_SECRET_KEY
 */
import { createHash, createHmac } from 'node:crypto';

const HOST = 'open.volcengineapi.com';
const ALGO = 'HMAC-SHA256';

function sha256Hex(s) {
  return createHash('sha256').update(s).digest('hex');
}
function hmac(key, s) {
  return createHmac('sha256', key).update(s).digest();
}

function getCreds() {
  const ak = process.env.VOLC_ACCESS_KEY || process.env.VOLC_ACCESSKEY;
  const sk = process.env.VOLC_SECRET_KEY || process.env.VOLC_SECRETKEY;
  if (!ak || !sk) {
    throw new Error('VOLC_ACCESS_KEY / VOLC_SECRET_KEY missing');
  }
  return { ak, sk };
}

/**
 * Call a Volcengine OpenAPI action.
 * @param {object} opts
 * @param {string} opts.service        e.g. "cdn"
 * @param {string} opts.region         e.g. "cn-beijing"
 * @param {string} opts.action         e.g. "DescribeRetrieveInfo"
 * @param {string} opts.version        e.g. "2021-03-01"
 * @param {object} [opts.body]         request body (JSON-serializable)
 * @param {object} [opts.query]        extra query params (Action + Version are added automatically)
 * @param {string} [opts.method]       "POST" (default) or "GET"
 * @returns {Promise<object>}
 */
export async function callVolc({
  service,
  region,
  action,
  version,
  body,
  query = {},
  method = 'POST',
}) {
  const { ak, sk } = getCreds();

  const bodyStr = body == null ? '' : JSON.stringify(body);
  const bodyHash = sha256Hex(bodyStr);

  const now = new Date();
  const xDate = now.toISOString().replace(/[-:]|\.\d{3}/g, '');
  const shortDate = xDate.slice(0, 8);

  const allQuery = { Action: action, Version: version, ...query };
  const sortedQs = Object.keys(allQuery)
    .sort()
    .map((k) => `${encodeURIComponent(k)}=${encodeURIComponent(allQuery[k])}`)
    .join('&');

  const headers = {
    'content-type': 'application/json',
    host: HOST,
    'x-content-sha256': bodyHash,
    'x-date': xDate,
  };

  const signedHeaders = Object.keys(headers).sort().join(';');
  const canonicalHeaders = Object.keys(headers)
    .sort()
    .map((k) => `${k}:${headers[k]}`)
    .join('\n') + '\n';

  const canonicalRequest = [
    method,
    '/',
    sortedQs,
    canonicalHeaders,
    signedHeaders,
    bodyHash,
  ].join('\n');

  const credentialScope = `${shortDate}/${region}/${service}/request`;
  const stringToSign = [
    ALGO,
    xDate,
    credentialScope,
    sha256Hex(canonicalRequest),
  ].join('\n');

  const kDate = hmac(sk, shortDate);
  const kRegion = hmac(kDate, region);
  const kService = hmac(kRegion, service);
  const kSigning = hmac(kService, 'request');
  const signature = hmac(kSigning, stringToSign).toString('hex');

  const authorization =
    `${ALGO} Credential=${ak}/${credentialScope}, ` +
    `SignedHeaders=${signedHeaders}, Signature=${signature}`;

  const url = `https://${HOST}/?${sortedQs}`;

  // honor user's local proxy preferences (TOS endpoint avoided proxy because it's CN-internal;
  // open.volcengineapi.com is also CN-internal so skip proxy here too)
  for (const k of ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']) {
    delete process.env[k];
  }

  const res = await fetch(url, {
    method,
    headers: { ...headers, Authorization: authorization },
    body: bodyStr || undefined,
  });

  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(
      `${service}:${action} → non-JSON response (${res.status}):\n${text.slice(0, 500)}`,
    );
  }
  return json;
}
