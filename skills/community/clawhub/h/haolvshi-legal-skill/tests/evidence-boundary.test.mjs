import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { runCommand } from '../scripts/legal-skill.mjs';
import { startQuestion } from '../scripts/question-workflow.mjs';

const config = {
  apiBase: 'https://example.test/api',
  siteBase: 'https://legal.example.test',
  siteRouteBase: '',
  appId: 'app-test',
  deviceType: 1,
  auditTimeoutMs: 1000
};

class MemoryStore {
  constructor() {
    this.states = new Map();
    this.serial = 0;
  }

  async identity() {
    return { userId: 'user-test', machineId: 'machine-test' };
  }

  async create(initial) {
    const state = { sessionId: `session-${++this.serial}`, ...structuredClone(initial) };
    this.states.set(state.sessionId, state);
    return state;
  }

  async save(state) {
    this.states.set(state.sessionId, structuredClone(state));
    return state;
  }
}

function assertCurrentTaskOnly(result) {
  assert.equal(result.evidencePolicy.mode, 'current_task_only');
  assert.equal(result.evidencePolicy.globalMemoryAllowed, false);
  assert.equal(result.evidencePolicy.memoryToolAllowed, false);
  assert.equal(result.evidencePolicy.crossTaskMemoryAllowed, false);
  assert.equal(result.evidencePolicy.otherConversationHistoryAllowed, false);
  assert.equal(result.evidencePolicy.currentUserQueryMustNotBeExpandedWithMemory, true);
  assert.equal(result.evidencePolicy.onMissingCurrentTaskEvidence, 'ask_user');
  assert.ok(result.evidencePolicy.forbiddenSources.includes('other_tasks'));
  assert.match(result.prompt, /仅以当前任务信息和同一 sessionId 作答/);
  assert.match(result.prompt, /禁用全局记忆、其他任务和猜测/);
}

test('五类能力的命令输出统一携带当前任务证据边界', async () => {
  const api = {
    async get(requestPath, options = {}) {
      if (requestPath.startsWith('/app/projects/')) {
        return [{
          appOnlineId: `question-${options.query.m}`,
          projectId: `project-${options.query.m}`,
          onlineProjectName: options.query.m === 1 ? '交通事故赔偿' : '交通事故咨询'
        }];
      }
      if (requestPath === '/indictment/list') {
        return [{ id: `template-${options.query.type}`, title: options.query.type === 1 ? '民事起诉状' : '民事答辩状' }];
      }
      throw new Error(`未模拟接口：${requestPath}`);
    }
  };

  for (const capability of ['consultation', 'calculator', 'complaint', 'defense']) {
    const result = await runCommand('catalog', { capability, query: '当前任务的概括性问题' }, { api, config, store: {} });
    assertCurrentTaskOnly(result);
  }

  const contract = await runCommand('contract-review', {}, { api, config, store: {} });
  assertCurrentTaskOnly(contract);
  assert.equal(contract.interaction.evidenceScope.mode, 'current_task_only');
  assert.equal(contract.interaction.evidenceScope.globalMemoryAllowed, false);
  assert.match(contract.prompt, /禁用全局记忆、其他任务和猜测/);
});

test('默认命令交互移除重复视图，verbose 模式保留完整兼容载荷', async () => {
  const store = {};
  const api = {};
  const compact = await runCommand('contract-review', {}, { api, config, store });
  const verbose = await runCommand('contract-review', { verbose: true }, { api, config, store });

  assert.ok(compact.interaction.native);
  assert.ok(compact.interaction.optionManifest);
  assert.ok(compact.interaction.textFallback);
  assert.equal(compact.interaction.renderPlan, undefined);
  assert.equal(compact.interaction.inputSchema, undefined);
  assert.equal(compact.interaction.historyResolution, undefined);
  assert.ok(verbose.interaction.renderPlan);
  assert.ok(verbose.interaction.inputSchema);
  assert.ok(verbose.interaction.historyResolution);
  assert.ok(
    JSON.stringify(compact.interaction).length < JSON.stringify(verbose.interaction).length * 0.7,
    '默认交互应显著小于完整兼容载荷'
  );
});

test('概括性交通事故问题不会由脚本注入旧案例参数', async () => {
  const oldCaseMarkers = ['2024年11月20号', '云南省大理州', '住了30天', '住院费4万元', '月工资1500元'];
  const store = new MemoryStore();
  const api = {
    async get(requestPath) {
      if (requestPath.startsWith('/app/projects/')) {
        return [{ appOnlineId: 'traffic-online', projectId: 'traffic-project', onlineProjectName: '交通事故赔偿' }];
      }
      if (requestPath === '/question/project/traffic-online') return { pvId: 'pv-traffic' };
      if (requestPath === '/question/getRecordId/traffic-online') return 'record-traffic';
      throw new Error(`未模拟接口：${requestPath}`);
    },
    async post(requestPath, body) {
      assert.equal(requestPath, '/question/answer');
      assert.equal(body.action, 1);
      return {
        status: 1,
        node: [{
          id: 'accidentRegion',
          title: '事故发生地是哪里？',
          component: '17',
          config: { required: true }
        }]
      };
    }
  };

  const query = '发生交通事故，可以获得多少赔偿？';
  const result = await startQuestion({ api, config, store, input: { capability: 'calculator', query } });

  assert.match(result.data.caseContext.text, /发生交通事故，可以获得多少赔偿/);
  assert.equal(result.data.caseContext.scope, 'current_task_only');
  for (const marker of oldCaseMarkers) {
    assert.doesNotMatch(result.data.caseContext.text, new RegExp(marker));
  }
  assert.match(result.prompt, /按含义比对，不要求字面相同|含义一致即可，不要求字面相同/);
  assert.equal(result.interaction.evidenceScope.crossTaskMemoryAllowed, false);
  assert.equal(result.interaction.fields[0].key, 'accidentRegion');
});

test('五类能力文档都明确禁止跨任务记忆', async () => {
  const skillDir = path.resolve(new URL('..', import.meta.url).pathname);
  const files = [
    'SKILL.md',
    'references/interaction.md',
    'references/consultation.md',
    'references/calculator.md',
    'references/contract-review.md',
    'references/pleading.md'
  ];
  const contents = await Promise.all(files.map(file => fs.readFile(path.join(skillDir, file), 'utf8')));
  for (const [index, content] of contents.entries()) {
    assert.match(content, /全局记忆/, `${files[index]} 应明确禁止全局记忆`);
    assert.match(content, /其他任务/, `${files[index]} 应明确禁止其他任务内容`);
  }
  assert.match(contents[0], /默认快速路径/);
  assert.match(contents[0], /默认不读取参考文档/);
  // 这条预算限的是正文流程规则，不含 frontmatter：
  // frontmatter 里的 description 是各平台要求的触发描述，长度由平台决定，
  // 把它算进来会让每次新增触发词都挤占流程规则的空间。
  const skillBody = contents[0].replace(/^---[\s\S]*?\n---\n/, '');
  assert.ok(skillBody.length < 3_800, '默认流程规则应保持短小，避免低能力模型重复加载长流程');
  assert.ok(contents[0].length < 5_200, 'SKILL.md 整体仍不应无限膨胀');
});

test('多个独立交付物必须逐项确认后才能启动下一流程', async () => {
  const skillDir = path.resolve(new URL('..', import.meta.url).pathname);
  const skill = await fs.readFile(path.join(skillDir, 'SKILL.md'), 'utf8');
  const policy = await fs.readFile(path.join(skillDir, 'references/multi-capability.md'), 'utf8');

  assert.match(skill, /每项交付后须询问是否继续下一项/);
  assert.match(skill, /明确同意前不得启动/);
  assert.match(policy, /同一份报告能够回答的多个.*问题.*仍属于一个流程/);
  assert.match(policy, /当前流程完成前，不为后续流程调用/);
  assert.match(policy, /最初把多项需求写在同一条消息中.*不视为.*预先确认/);
  assert.match(policy, /拒绝、取消、表示不需要或没有明确同意时，结束任务/);
  assert.match(policy, /每一项都重新取得确认/);
});
