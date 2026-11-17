import assert from 'node:assert/strict';
import test from 'node:test';

import { runCommand } from '../scripts/legal-skill.mjs';
import { normalizeQuestionNodes, withInteractionRendering } from '../scripts/interaction-normalizer.mjs';

// 这些用例锁住"喂给宿主模型的载荷"这一层。选型和逐题作答的耗时主要花在
// 模型阅读与推理上，一旦这里重新塞回重复内容，宿主的决策速度会直接变慢。

const PROJECTS = Array.from({ length: 40 }, (_, index) => ({
  id: `project-${index}`,
  projectId: `pid-${index}`,
  appOnlineId: `online-${index}`,
  sourceProjectId: `source-${index}`,
  parentId: 'parent-1',
  name: `具体项目${index}`,
  onlineProjectName: `具体项目${index}`,
  onlineProjectParentName: '父级领域',
  module: 2,
  price: 990
}));

function createApi() {
  return {
    async get(path) {
      if (path.startsWith('/app/projects/')) return PROJECTS;
      throw new Error(`未模拟接口：${path}`);
    },
    async post() {
      throw new Error('未模拟 post');
    }
  };
}

const config = {
  appId: 'app-test',
  apiBase: 'https://example.test/api/speed-front',
  deviceType: 1,
  userAgent: 'test',
  requestTimeoutMs: 1000
};

async function catalogResult(extra = {}) {
  return runCommand(
    'catalog',
    { capability: 'consultation', query: '当前任务的问题', ...extra },
    { api: createApi(), config, store: {} }
  );
}

test('目录候选只下发 id 和 displayName，不带内部编号和价格', async () => {
  const result = await catalogResult();

  assert.equal(result.data.candidates.length, 40);
  for (const candidate of result.data.candidates) {
    assert.deepEqual(Object.keys(candidate), ['id', 'displayName']);
  }
  assert.equal(result.data.candidates[0].displayName, '父级领域 > 具体项目0');
});

test('verbose 仍然返回完整候选记录', async () => {
  const compact = await catalogResult();
  const verbose = await catalogResult({ verbose: true });

  assert.ok(Object.keys(verbose.data.candidates[0]).includes('appOnlineId'));
  assert.ok(Object.keys(verbose.data.candidates[0]).includes('price'));
  const compactSize = Buffer.byteLength(JSON.stringify(compact));
  const verboseSize = Buffer.byteLength(JSON.stringify(verbose));
  assert.ok(
    compactSize * 2 < verboseSize,
    `精简载荷应显著小于完整载荷，实际 ${compactSize} vs ${verboseSize}`
  );
});

test('候选瘦身后仍能用返回的 id 定位到完整项目', async () => {
  const result = await catalogResult();
  const picked = result.data.candidates[7];

  // 对外暴露的 id 就是 appOnlineId，脚本内部据此定位完整记录。
  const source = PROJECTS.find(item => item.appOnlineId === picked.id);
  assert.ok(source, '返回的 id 必须能对应到目录中的真实项目');
  assert.equal(source.projectId, 'pid-7');
  assert.equal(picked.id, 'online-7');
});

test('证据边界声明的长数组在一个响应里只出现一次', async () => {
  const result = await catalogResult();

  // 顶层保留完整声明，供宿主机读。
  assert.ok(result.evidencePolicy.forbiddenSources.includes('other_tasks'));
  assert.ok(result.evidencePolicy.allowedSources.length > 0);

  const serialized = JSON.stringify(result);
  const occurrences = serialized.split('"other_tasks"').length - 1;
  assert.equal(occurrences, 1, '禁止来源列表不应在同一响应里重复出现');
});

test('caseContext 里的嵌套边界声明不再重复长数组', async () => {
  const result = await runCommand(
    'catalog',
    {
      capability: 'consultation',
      query: '当前任务的问题',
      extractedTexts: [{ filePath: '/tmp/note.txt', text: '当前任务的案情材料文字' }]
    },
    { api: createApi(), config, store: {} }
  );

  const caseContext = result.data?.caseContext || result.interaction?.caseContext;
  if (!caseContext?.evidencePolicy) return;
  assert.equal(caseContext.evidencePolicy.forbiddenSources, undefined);
  assert.equal(caseContext.evidencePolicy.sameAs, 'evidencePolicy');
  // 机读的标志位必须保留。
  assert.equal(caseContext.evidencePolicy.mode, 'current_task_only');
  assert.equal(caseContext.evidencePolicy.globalMemoryAllowed, false);
});

test('文书模板目录不会被关键词过滤成空', async () => {
  // 模板名是“民事起诉状（劳动争议纠纷）”这类法律术语，用户说的是
  // “追讨拖欠工资”，按分词打分一个都命中不了。以前会把目录整个过滤成空，
  // 用户直接用不了文书功能。
  const templates = [
    { id: 't1', title: '民事起诉状（劳动争议纠纷）' },
    { id: 't2', title: '民事起诉状（民间借贷纠纷）' },
    { id: 't3', title: '民事起诉状（机动车交通事故责任纠纷）' }
  ];
  const api = {
    async get(path) {
      if (path === '/indictment/list') return templates;
      throw new Error(`未模拟接口：${path}`);
    },
    async post() { throw new Error('未模拟 post'); }
  };

  const result = await runCommand(
    'catalog',
    { capability: 'complaint', query: '追讨拖欠工资' },
    { api, config, store: {} }
  );

  assert.equal(result.data.candidates.length, 3, '完整模板都要交给宿主做语义选型');
  assert.ok(result.data.candidates.some(item => /劳动争议/.test(item.displayName)));
});

test('逐题作答走语义契约，不由脚本用规则代答', async () => {
  // 选项内容开放、案情表达千变万化，脚本用关键词或正则去匹配只能覆盖
  // 少数固定形态：覆盖不到的静默漏掉，覆盖错的静默填错。这里锁住
  // "脚本只声明门槛、语义判断交给模型"这一分工。
  const nodes = [{
    id: 'duration',
    title: '你的工钱被拖欠多久了？',
    component: '1',
    config: { required: true },
    children: [
      { id: 'a', title: '未超过一年' },
      { id: 'b', title: '超过一年不满三年' },
      { id: 'c', title: '超过三年' }
    ]
  }];
  const interaction = withInteractionRendering(
    normalizeQuestionNodes(nodes),
    { suggestionContext: '包工头拖欠工资5年了' }
  );

  assert.equal(interaction.answerPolicy.matchingMode, 'host_model_semantic_answering');
  assert.equal(interaction.answerPolicy.mode, 'evidence_or_user_input_only');
  assert.equal(interaction.answerPolicy.matching, 'meaning_not_literal');
  assert.equal(interaction.answerPolicy.autoAnswer.minimumConfidence, 0.85);
  assert.equal(interaction.answerPolicy.uncertain.neverGuess, true);
  assert.equal(interaction.answerPolicy.uncertain.neverDefaultToCatchAllOption, true);

  // 脚本不得自行替模型选定答案。
  assert.equal(interaction.fields[0].value, '');
  assert.equal(interaction.fields[0].evidenceMatch, undefined);
});
