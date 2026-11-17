import assert from 'node:assert/strict';
import test from 'node:test';
import { ApiClient, unwrapServiceResult } from '../scripts/api-client.mjs';

const config = {
  apiBase: 'https://example.test/api',
  requestTimeoutMs: 1000,
  userAgent: 'test'
};

test('服务结果成功时只返回 data', () => {
  assert.deepEqual(unwrapServiceResult({
    response: { success: true, code: 200 },
    data: { id: '1' }
  }), { id: '1' });
});

test('服务结果失败时抛出结构化错误', () => {
  assert.throws(
    () => unwrapServiceResult({ response: { success: false, code: 500, msg: '失败原因' } }),
    error => error.code === 'SERVICE_500' && error.message === '失败原因'
  );
});

test('原始字符串接口支持双层 JSON 解码', async () => {
  let method;
  const client = new ApiClient(config, {
    fetchImpl: async (_url, options) => {
      method = options.method;
      return new Response(JSON.stringify(JSON.stringify({ status: 1, node: [] })));
    }
  });
  const result = await client.post('/question/answer', {}, { unwrap: false });
  assert.deepEqual(result, { status: 1, node: [] });
  assert.equal(method, 'POST');
});

test('有副作用的请求遇到网络错误不会自动重试', async () => {
  let calls = 0;
  const client = new ApiClient(config, {
    fetchImpl: async () => {
      calls += 1;
      throw new Error('连接中断');
    }
  });
  await assert.rejects(() => client.post('/contract/audit', {}), error => error.code === 'NETWORK_ERROR');
  assert.equal(calls, 1);
});
