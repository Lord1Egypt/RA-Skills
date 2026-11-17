import assert from 'node:assert/strict';
import { test } from 'node:test';
import http from 'node:http';
import { verifyCode, uploadPayload, KLIK_BASE_URL } from '../src/uploader.ts';

test('default KLIK_BASE_URL points to hiklik.ai, not api.klik.app', () => {
  // Regression guard: api.klik.app has no DNS records and will never resolve.
  // The production backend lives at hiklik.ai.
  assert.equal(KLIK_BASE_URL, 'https://hiklik.ai');
  assert.ok(!KLIK_BASE_URL.includes('api.klik.app'), 'must not reference dead hostname');
});

async function withMockServer(
  handler: (req: http.IncomingMessage, res: http.ServerResponse) => void,
  fn: (baseUrl: string) => Promise<void>
): Promise<void> {
  const server = http.createServer(handler);
  await new Promise<void>(r => server.listen(0, '127.0.0.1', r));
  const addr = server.address() as { port: number };
  const base = `http://127.0.0.1:${addr.port}`;
  try {
    await fn(base);
  } finally {
    await new Promise<void>(r => server.close(() => r()));
  }
}

test('verifyCode returns token on 200', async () => {
  await withMockServer((req, res) => {
    let body = '';
    req.on('data', d => (body += d));
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        user_id: 'user_abc',
        import_token: 'klik_imp_test',
        ttl_seconds: 900,
      }));
    });
  }, async (base) => {
    const result = await verifyCode('123456', { baseUrl: base });
    assert.equal(result.import_token, 'klik_imp_test');
    assert.equal(result.user_id, 'user_abc');
  });
});

test('verifyCode throws on 400', async () => {
  await withMockServer((_req, res) => {
    res.writeHead(400, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'invalid_or_expired' }));
  }, async (base) => {
    await assert.rejects(
      () => verifyCode('000000', { baseUrl: base }),
      /invalid_or_expired/
    );
  });
});

test('uploadPayload returns import_id on 200', async () => {
  await withMockServer((_req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ import_id: 'uuid-123', accepted: [], server_timestamp: 'now' }));
  }, async (base) => {
    const result = await uploadPayload(
      { schema_version: '1.0', client: {} as any, redaction: {} as any, collectors: [] },
      'klik_imp_token',
      { baseUrl: base }
    );
    assert.equal(result.import_id, 'uuid-123');
  });
});
