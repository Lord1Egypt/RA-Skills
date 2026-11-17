import assert from 'node:assert/strict';
import test from 'node:test';
import { runCommand } from '../scripts/legal-skill.mjs';

const config = {
  apiBase: 'https://example.test/api',
  siteBase: 'https://legal.example.test',
  siteRouteBase: '',
  appId: 'app-test',
  deviceType: 1,
  requestTimeoutMs: 1000,
  auditTimeoutMs: 1000,
  stateTtlMs: 60_000,
  stateDir: '/tmp/lvpin-health-test'
};

function healthApi(siteConfig) {
  return {
    async get(path) {
      if (path === '/app/detailByAppId/app-test') {
        return { appId: 'app-test', config: JSON.stringify(siteConfig) };
      }
      if (path.startsWith('/app/projects/')) {
        return [{ appOnlineId: 'online-1', onlineProjectName: '测试项目' }];
      }
      if (path === '/indictment/list') {
        return [{ id: 'template-1', name: '测试模板', type: 1 }];
      }
      throw new Error(`未模拟接口：${path}`);
    }
  };
}

test('健康检查真实识别 llm.contract 且不泄露密钥', async () => {
  const secret = '仅用于测试的敏感值';
  const result = await runCommand('health', {}, {
    config,
    api: healthApi({ llm: { contract: { apiKey: secret } } })
  });

  assert.equal(result.data.contract, true);
  assert.match(result.prompt, /合同审核配置已就绪/);
  assert.doesNotMatch(JSON.stringify(result), new RegExp(secret));
});

test('健康检查在合同配置缺失时返回 false', async () => {
  const result = await runCommand('health', {}, {
    config,
    api: healthApi({ llm: {} })
  });

  assert.equal(result.data.contract, false);
  assert.match(result.data.contractCheck, /未检测到/);
});
