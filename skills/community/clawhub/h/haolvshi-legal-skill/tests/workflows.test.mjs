import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { reviewContract, resumeContract } from '../scripts/contract-workflow.mjs';
import { extractPleading, generatePleading, pleadingResume, updatePleading } from '../scripts/pleading-workflow.mjs';
import { extractPleadingFormSchema } from '../scripts/interaction-normalizer.mjs';
import {
  generateQuestionReport,
  questionCatalog,
  questionResume,
  replyQuestion,
  startQuestion
} from '../scripts/question-workflow.mjs';

const config = {
  apiBase: 'https://example.test/api',
  siteBase: 'https://legal.example.test',
  siteRouteBase: '',
  appId: 'app-test',
  deviceType: 1,
  auditTimeoutMs: 1000
};

class MemoryStore {
  constructor(initial = []) {
    this.states = new Map(initial.map(state => [state.sessionId, structuredClone(state)]));
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

  async load(sessionId) {
    return structuredClone(this.states.get(sessionId));
  }

  async writeArtifact(sessionId, filename) {
    return `/tmp/${sessionId}/${filename}`;
  }
}

// 地区题的取值是地区表 id，工作流测试需要一份最小地区表。
const AREA_FIXTURE = [
  { id: 'area-yn', name: '云南省', parentId: null },
  { id: 'area-km', name: '昆明市', parentId: 'area-yn' },
  { id: 'area-wh', name: '五华区', parentId: 'area-km' },
  { id: 'area-zj', name: '浙江省', parentId: null },
  { id: 'area-hz', name: '杭州市', parentId: 'area-zj' }
];

test('项目目录分别携带 m=2 和 m=1，并完整保留可启动项目供大模型语义选择', async () => {
  const queries = [];
  const api = {
    async get(path, options) {
      queries.push({ path, query: options.query });
      return [
        { id: 'root-traffic', appOnlineId: 'app-root-traffic', onlineProjectName: '交通事故', module: options.query.m },
        { id: 'leaf-traffic', parentId: 'root-traffic', appOnlineId: 'app-leaf-traffic', projectId: 'project-traffic', onlineProjectName: '损害赔偿', module: options.query.m },
        { id: 'root-labor', appOnlineId: 'app-root-labor', onlineProjectName: '劳动争议', module: options.query.m },
        { id: 'leaf-labor', parentId: 'root-labor', appOnlineId: 'app-leaf-labor', projectId: 'project-labor', onlineProjectName: '损害赔偿', module: options.query.m }
      ];
    }
  };

  const consultations = await questionCatalog(api, config, 'consultation', '劳动争议损害赔偿', 10);
  const calculators = await questionCatalog(api, config, 'calculator', '劳动争议损害赔偿', 10);

  assert.equal(queries[0].query.m, 2);
  assert.equal(queries[1].query.m, 1);
  assert.equal(consultations[0].id, 'app-leaf-traffic');
  assert.equal(consultations[0].parentName, '交通事故');
  assert.equal(consultations[0].displayName, '交通事故 > 损害赔偿');
  assert.equal(calculators[0].id, 'app-leaf-traffic');
  assert.equal(consultations[1].parentName, '劳动争议');
  assert.ok(consultations.every(item => item.projectId));
});

test('多个咨询项目时不再按用户原话分词自动选择，而是交给大模型语义评分', async () => {
  const store = new MemoryStore();
  const api = {
    async get(requestPath) {
      if (requestPath.startsWith('/app/projects/')) {
        return [
          { appOnlineId: 'service-contract', projectId: 'service-project', onlineProjectName: '服务合同纠纷' },
          { appOnlineId: 'rental-deposit', projectId: 'rental-project', onlineProjectName: '租金与押金纠纷' }
        ];
      }
      throw new Error(`不应在未完成项目语义选择前访问：${requestPath}`);
    },
    async post() {
      throw new Error('不应在未完成项目语义选择前提交问答');
    }
  };

  const result = await startQuestion({
    api,
    config,
    store,
    input: {
      capability: 'consultation',
      query: '租约到期后中介迟迟不退押金，且没有拿到合同，我该怎么办'
    }
  });

  assert.equal(result.stage, 'needs_model_selection');
  assert.equal(result.interaction, null);
  assert.equal(result.data.candidates.length, 2);
  assert.equal(result.data.selection.mode, 'host_model_semantic_scoring');
  assert.equal(result.data.selection.autoSelect.minimumConfidence, 0.85);
  assert.match(result.prompt, /不得按关键词命中数量、分词结果或目录原始顺序选择/);
});

test('启动时自动跳过非必填敏感字段并继续请求下一题', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'sensitive-online', projectId: 'sensitive-project', onlineProjectName: '交通事故咨询' }];
      if (path === '/question/project/sensitive-online') return { pvId: 'pv-sensitive' };
      if (path === '/question/getRecordId/sensitive-online') return 'record-sensitive';
      if (path === '/area/getQuestionAllArea') return AREA_FIXTURE;
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [
            { id: 'phone', title: '联系电话', component: '3', config: { required: false } },
            { id: 'identity', title: '身份证号码', component: '3', config: { required: false } }
          ]
        };
      }
      if (answerCalls.length === 2) {
        return { status: 1, node: [{ id: 'liveAt', title: '实际居住地', component: '17', config: { required: true } }] };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({
    api,
    config,
    store,
    input: { capability: 'consultation', query: '交通事故咨询' }
  });

  assert.equal(answerCalls.length, 2, '空的非必填敏感字段应直接提交并继续后端流程');
  assert.deepEqual(started.interaction.fields.map(field => field.key), ['liveAt']);
  assert.equal(started.interaction.fields[0].skipIfOptionalSensitive, false);
  assert.equal(answerCalls[1].answer[0].value ?? '', '');
  assert.equal(answerCalls[1].answer[1].value ?? '', '');

  const completed = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { liveAt: '杭州' } }
  });
  assert.equal(completed.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 3);
});

test('用户已明确选择财产类别后，后续不适用的车辆数量题自动保留空值并继续', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'cohabitation-online', projectId: 'cohabitation-project', onlineProjectName: '同居财产咨询' }];
      if (path === '/question/project/cohabitation-online') return { pvId: 'pv-cohabitation' };
      if (path === '/question/getRecordId/cohabitation-online') return 'record-cohabitation';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [{
            id: 'assetType',
            title: '争议财产类型',
            component: '2',
            config: { required: true },
            children: [
              { id: 'deposit', title: '存款' },
              { id: 'vehicle', title: '车辆' },
              { id: 'realEstate', title: '房产' }
            ]
          }]
        };
      }
      if (answerCalls.length === 2) {
        return {
          status: 1,
          node: [{
            id: 'vehicleCount',
            title: '有几辆车存在争议',
            component: '12',
            config: { required: true }
          }]
        };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({
    api,
    config,
    store,
    input: { capability: 'consultation', query: '同居期间财产分割' }
  });
  assert.deepEqual(started.interaction.fields.map(field => field.key), ['assetType']);

  const completed = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { assetType: '存款' } }
  });

  assert.equal(completed.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 3, '不适用车辆题应由脚本提交空值推进，而不是交给用户填写');
  assert.equal(answerCalls[2].answer[0].value ?? '', '');
  assert.equal(completed.interaction, null);
});

test('法律咨询和计算器把上传材料持续附加到每一道题的内部案情上下文', async t => {
  const materialDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-question-materials-'));
  t.after(() => fs.rm(materialDir, { recursive: true, force: true }));
  const materialPath = `${materialDir}/事故经过.txt`;
  await fs.writeFile(materialPath, '事故发生在杭州，对方全责，伤者十级伤残，医疗费12000元。', 'utf8');

  for (const capability of ['consultation', 'calculator']) {
    const store = new MemoryStore();
    let answerCount = 0;
    const api = {
      async get(requestPath) {
        if (requestPath.startsWith('/app/projects/')) return [{ appOnlineId: `${capability}-online`, projectId: `${capability}-project`, onlineProjectName: '交通事故赔偿' }];
        if (requestPath === `/question/project/${capability}-online`) return { pvId: `${capability}-pv` };
        if (requestPath === `/question/getRecordId/${capability}-online`) return `${capability}-record`;
        throw new Error(`未模拟接口：${requestPath}`);
      },
      async post(requestPath, body) {
        assert.equal(requestPath, '/question/answer');
        answerCount += 1;
        if (body.action === 1) {
          return { status: 1, node: [{ id: 'liability', title: '对方是否承担全部责任？', component: '1', config: { required: true }, children: [{ id: 'yes', title: '是' }, { id: 'no', title: '否' }] }] };
        }
        return { status: 1, node: [{ id: 'medicalFee', title: '医疗费是多少元？', component: '9', config: { required: true } }] };
      }
    };

    const started = await startQuestion({
      api,
      config,
      store,
      input: { capability, query: '交通事故赔偿', filePaths: [materialPath] }
    });
    assert.match(started.interaction.caseContext.text, /对方全责/);
    assert.match(started.data.caseContext.text, /医疗费12000元/);

    const next = await replyQuestion({
      api,
      config,
      store,
      input: { sessionId: started.sessionId, answers: { liability: '是' } }
    });
    assert.equal(answerCount, 2);
    assert.match(next.interaction.caseContext.text, /伤者十级伤残/);

    const resumed = questionResume(await store.load(started.sessionId), config);
    assert.match(resumed.interaction.caseContext.text, /事故发生在杭州/);
  }
});

test('咨询或计算器遇到尚未提取的PDF时先返回材料提取阶段且不创建后端任务', async t => {
  const materialDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-pending-materials-'));
  t.after(() => fs.rm(materialDir, { recursive: true, force: true }));
  const materialPath = `${materialDir}/判决书.pdf`;
  await fs.writeFile(materialPath, 'PDF测试占位');
  const store = new MemoryStore();
  let apiCalls = 0;
  const api = new Proxy({}, {
    get() {
      return async () => { apiCalls += 1; throw new Error('材料未提取前不应调用后端'); };
    }
  });

  const result = await startQuestion({
    api,
    config,
    store,
    input: { capability: 'consultation', query: '请分析案件', filePaths: [materialPath] }
  });

  assert.equal(result.stage, 'needs_material_extraction');
  assert.equal(result.data.unresolvedFiles[0].extension, '.pdf');
  assert.equal(apiCalls, 0);
  assert.equal(store.states.size, 0);
});

test('法律咨询逐题收集并生成报告', async () => {
  const store = new MemoryStore();
  const calls = [];
  const api = {
    async get(path) {
      calls.push(['get', path]);
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'online-1', projectId: 'project-1', onlineProjectName: '离婚财产分割' }];
      if (path === '/question/project/online-1') return { pvId: 'pv-question' };
      if (path === '/question/getRecordId/online-1') return 'record-question';
      if (path.startsWith('/question/getCasesAndLawArticles/')) return { laws: [{ title: '民法典' }], caseList: [] };
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      calls.push(['post', path, body]);
      if (path === '/question/answer' && body.action === 1) {
        return { status: 1, node: [{ id: 'married', title: '是否登记结婚？', component: '1', config: { required: true }, children: [{ id: 'yes', title: '是' }, { id: 'no', title: '否' }] }] };
      }
      if (path === '/question/answer' && body.action === 2) return { status: 0 };
      if (path === '/question/report') return '<p>财产分割结论</p>';
      if (path === '/question/saveReport') return true;
      throw new Error(`未模拟接口：${path}`);
    },
  };

  const started = await startQuestion({ api, config, store, input: { capability: 'consultation', query: '离婚财产分割' } });
  assert.equal(started.interaction.type, 'question');
  assert.equal(started.interaction.historyResolution.mode, 'current_task_evidence_first');
  assert.equal(started.interaction.evidenceScope.globalMemoryAllowed, false);
  assert.equal(started.interaction.evidenceScope.crossTaskMemoryAllowed, false);
  assert.equal(started.interaction.historyResolution.noMatchAction, 'present_question_to_user');
  assert.equal(started.interaction.answerPolicy.neverChooseUnknownAsDefault, true);
  assert.match(started.prompt, /呈现选项时直接用 native\.batches\[0\]/);
  assert.match(started.prompt, /按含义比对，不要求字面相同|含义一致即可，不要求字面相同/);
  assert.deepEqual(started.interaction.choices.map(choice => choice.label), ['是', '否']);
  assert.match(started.interaction.textFallback, /1\. 是/);
  const replied = await replyQuestion({ api, config, store, input: { sessionId: started.sessionId, answers: { married: '是' } } });
  assert.equal(replied.stage, 'ready_for_report');
  const report = await generateQuestionReport({ api, config, store, input: { sessionId: started.sessionId } });
  assert.equal(report.stage, 'completed');
  assert.deepEqual(report.warnings, []);
  assert.deepEqual(
    calls.filter(([method]) => method === 'post').map(([, path]) => path),
    ['/question/answer', '/question/answer', '/question/report', '/question/saveReport']
  );
  assert.match(report.data.summary, /财产分割结论/);
  assert.equal(report.data.reportUrl, 'https://legal.example.test/g/r/record-question?appId=app-test&device_type=1');
  assert.equal(report.data.reportLinkMarkdown, '[法律咨询报告](https://legal.example.test/g/r/record-question?appId=app-test&device_type=1)');
  assert.equal(report.links[0].type, 'online_report');
  assert.equal(report.links[0].label, '法律咨询报告');
  assert.equal(report.links[0].autoOpen, true);
  assert.equal(report.data.delivery.markdown, report.links[0].markdown);
  assert.equal(report.data.delivery.autoOpen, true);
  assert.equal(report.resultPolicy.sourceOfTruth, 'generated_result_only');
  assert.equal(report.resultPolicy.externalSearchAllowed, false);
  assert.equal(report.resultPolicy.addAuthoritiesNotInResultAllowed, false);
  assert.match(report.prompt, /不得调用网页搜索、法律数据库检索、联网查询/);
  assert.match(report.prompt, /立即用宿主内置浏览器打开/);
  assert.match(report.prompt, /不得调起外部浏览器/);
  assert.match(report.prompt, /禁止自行生成 HTML、Markdown、PDF 等任何报告文件/);
  assert.equal(report.downloads, undefined);
});

test('当前任务证据只覆盖部分字段时先保存已知答案并标记所有剩余未答项', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'partial-online', projectId: 'partial-project', onlineProjectName: '交通事故咨询' }];
      if (path === '/question/project/partial-online') return { pvId: 'pv-partial' };
      if (path === '/question/getRecordId/partial-online') return 'record-partial';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [
            {
              id: 'insured',
              title: '是否投保交强险？',
              component: '1',
              config: { required: true },
              children: [{ id: 'yes', title: '是' }, { id: 'no', title: '否' }]
            },
            {
              id: 'accidentDate',
              title: '事故发生日期',
              component: '10',
              config: { required: true }
            }
          ]
        };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({ api, config, store, input: { capability: 'consultation', query: '交通事故咨询' } });
  const partial = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { insured: '是' } }
  });

  assert.equal(partial.stage, 'needs_input');
  assert.deepEqual(partial.data.missing, ['事故发生日期']);
  assert.deepEqual(partial.interaction.fields.map(field => field.key), ['accidentDate']);
  assert.equal(partial.interaction.renderPlan.units.length, 1);
  assert.equal(answerCalls.length, 1, '仅自动填写部分字段时不应提前提交后端');

  const completed = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { accidentDate: '2026-08-01' } }
  });

  assert.equal(completed.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 2);
  assert.equal(answerCalls[1].answer[0].value, 'yes');
  // 日期题提交给后端的是 unix 秒，不是日期字符串（前端 QDate 的取值契约）。
  assert.equal(answerCalls[1].answer[1].value, String(Math.floor(new Date(2026, 7, 1).getTime() / 1000)));
});

test('多个填空字段在自动填写部分选择后按一题一题的候选选择计划返回', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'injured-online', projectId: 'injured-project', onlineProjectName: '交通事故咨询' }];
      if (path === '/question/project/injured-online') return { pvId: 'pv-injured' };
      if (path === '/question/getRecordId/injured-online') return 'record-injured';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [{
            id: 'injuredPerson',
            title: '受伤人员信息',
            component: '4',
            children: [
              { id: 'name', title: '姓名', component: '3' },
              { id: 'gender', title: '性别', component: '1', children: [{ id: 'male', title: '男' }, { id: 'female', title: '女' }] },
              { id: 'age', title: '年龄', component: '12' },
              { id: 'liveAt', title: '实际居住地', component: '17' },
              { id: 'registeredAt', title: '户籍地', component: '17' }
            ]
          }]
        };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({
    api,
    config,
    store,
    input: { capability: 'consultation', query: '交通事故咨询' }
  });
  assert.deepEqual(started.interaction.fields.map(field => field.key), ['injuredPerson.gender']);
  assert.equal(started.interaction.sequence.mode, 'one_field_per_turn');
  assert.equal(started.interaction.sequence.totalRemaining, 4);
  assert.equal(started.interaction.renderPlan.units.length, 1);
  assert.equal(started.interaction.renderPlan.units[0].mode, 'native_choice');

  const partial = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { 'injuredPerson.gender': '女' } }
  });

  assert.equal(partial.stage, 'needs_input');
  assert.deepEqual(partial.interaction.fields.map(field => field.key), ['injuredPerson.age']);
  assert.equal(partial.interaction.sequence.mode, 'one_field_per_turn');
  assert.equal(partial.interaction.sequence.totalRemaining, 3);
  assert.equal(partial.interaction.fields[0].type, 'single_select');
  assert.equal(partial.interaction.fields[0].originalType, 'number');
  assert.equal(partial.interaction.suggestedChoices.hostGenerationRequired, false);
  assert.deepEqual(partial.interaction.renderPlan.units.map(unit => unit.mode), ['native_choice']);
  assert.deepEqual(partial.interaction.native.batches[0].input.questions[0].options.map(option => option.label), [
    '18岁', '30岁', '45岁', '60岁'
  ]);
  assert.match(partial.prompt, /呈现选项时直接用 native\.batches\[0\]/);
  assert.match(partial.prompt, /按含义比对，不要求字面相同|含义一致即可，不要求字面相同/);
  assert.equal(answerCalls.length, 1, '部分自动填写时不应提前提交后端');
});

test('法律咨询选择带追加题的选项后先本地收集追加答案再合并提交', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'consult-online', projectId: 'consult-project', onlineProjectName: '离婚咨询' }];
      if (path === '/question/project/consult-online') return { pvId: 'pv-consult' };
      if (path === '/question/getRecordId/consult-online') return 'record-consult';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [{
            id: 'gender',
            title: '您是男方还是女方？',
            component: '1',
            config: { required: true },
            children: [
              {
                id: 'male',
                title: '男方',
                add: [{
                  id: 'age',
                  title: '您的年龄是多少？',
                  component: '12',
                  config: { required: true, addType: 'dialog' }
                }]
              },
              { id: 'female', title: '女方' }
            ]
          }]
        };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({ api, config, store, input: { capability: 'consultation', query: '离婚' } });
  assert.equal(started.interaction.choices[0].hasFollowUp, true);

  const followUp = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { gender: '男方' } }
  });
  assert.equal(followUp.stage, 'needs_follow_up');
  assert.equal(followUp.data.backendRequestPending, true);
  assert.equal(followUp.interaction.kind, 'follow_up');
  assert.equal(followUp.interaction.fields[0].key, 'age');
  assert.match(followUp.interaction.textFallback, /您的年龄是多少/);
  assert.equal(answerCalls.length, 1, '主选项触发追加题时不得调用后端下一题');

  const resumed = questionResume(await store.load(started.sessionId), config);
  assert.equal(resumed.stage, 'needs_follow_up');
  assert.equal(resumed.interaction.fields[0].key, 'age');

  const completed = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { age: 36 } }
  });
  assert.equal(completed.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 2);
  const submitted = answerCalls[1].answer[0];
  assert.equal(submitted.value, 'male');
  assert.equal(submitted.children[0].value, true);
  assert.equal(submitted.children[0].add[0].value, 36);
});

test('追加题包含多个填空字段时逐题返回标准单选，全部答完后才提交后端', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'calc-online', projectId: 'calc-project', onlineProjectName: '交通事故赔偿计算' }];
      if (path === '/question/project/calc-online') return { pvId: 'pv-calc' };
      if (path === '/question/getRecordId/calc-online') return 'record-calc';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [{
            id: 'hasAppraisal',
            title: '是否做过三期鉴定？',
            component: '1',
            config: { required: true },
            children: [{
              id: 'yes',
              title: '是',
              add: [{
                id: 'appraisalDetail',
                title: '三期鉴定信息',
                component: '4',
                config: { addType: 'dialog' },
                children: [
                  { id: 'appraisalFee', title: '三期鉴定费金额', component: '9', config: { required: true } },
                  { id: 'nursingDays', title: '护理期天数', component: '12', config: { required: true } }
                ]
              }]
            }, { id: 'no', title: '否' }]
          }]
        };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({
    api,
    config,
    store,
    input: { capability: 'calculator', query: '交通事故赔偿，已经做过三期鉴定但费用忘记了' }
  });
  const firstFill = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { hasAppraisal: '是' } }
  });

  assert.equal(firstFill.stage, 'needs_follow_up');
  assert.deepEqual(firstFill.interaction.fields.map(field => field.key), ['appraisalDetail.appraisalFee']);
  assert.equal(firstFill.interaction.sequence.mode, 'one_field_per_turn');
  assert.equal(firstFill.interaction.sequence.totalRemaining, 2);
  assert.equal(firstFill.interaction.fields[0].type, 'single_select');
  assert.equal(firstFill.interaction.fields[0].originalType, 'money');
  assert.deepEqual(firstFill.interaction.native.batches[0].input.questions[0].options.map(option => option.label), [
    '500元', '1,000元', '2,000元', '3,000元'
  ]);
  assert.equal(answerCalls.length, 1, '多填追加题开始时不得提交后端');

  const secondFill = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { 'appraisalDetail.appraisalFee': '1,000元' } }
  });

  assert.equal(secondFill.stage, 'needs_follow_up');
  assert.deepEqual(secondFill.interaction.fields.map(field => field.key), ['appraisalDetail.nursingDays']);
  assert.equal(secondFill.interaction.fields[0].type, 'single_select');
  assert.equal(secondFill.interaction.fields[0].originalType, 'number');
  assert.equal(answerCalls.length, 1, '多填追加题未全部回答时不得提交后端');

  const completed = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { 'appraisalDetail.nursingDays': '60天' } }
  });

  assert.equal(completed.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 2, '全部子字段回答后只提交一次完整答案');
  const detail = answerCalls[1].answer[0].children[0].add[0];
  assert.equal(detail.children[0].value, 1000);
  assert.equal(detail.children[1].value, 60);
});

test('非必填追加题没有案情答案时必须询问且空值不会提交后端', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'consult-online', projectId: 'consult-project', onlineProjectName: '交通事故咨询' }];
      if (path === '/question/project/consult-online') return { pvId: 'pv-consult' };
      if (path === '/question/getRecordId/consult-online') return 'record-consult';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(structuredClone(body));
      if (body.action === 1) {
        return {
          status: 1,
          node: [{
            id: 'futureTreatment',
            title: '是否存在后续治疗费？',
            component: '1',
            config: { required: true },
            children: [{
              id: 'exists',
              title: '存在',
              add: [{
                id: 'futureTreatmentFee',
                title: '后续治疗费用金额',
                component: '9',
                config: { required: false, addType: 'dialog' }
              }]
            }, { id: 'none', title: '不存在' }]
          }]
        };
      }
      return { status: 0, node: [] };
    }
  };

  const started = await startQuestion({ api, config, store, input: { capability: 'consultation', query: '交通事故' } });
  const followUp = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { futureTreatment: '存在' } }
  });
  assert.equal(followUp.stage, 'needs_follow_up');
  assert.equal(followUp.interaction.fields[0].required, false);
  assert.equal(followUp.interaction.fields[0].responseRequired, true);
  assert.deepEqual(followUp.interaction.inputSchema.required, ['futureTreatmentFee']);
  assert.equal(answerCalls.length, 1);

  const blankAttempt = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { futureTreatmentFee: '' }, allowIncomplete: true }
  });
  assert.equal(blankAttempt.stage, 'needs_follow_up');
  assert.match(blankAttempt.prompt, /无论后端是否标记必填/);
  assert.match(blankAttempt.prompt, /不得留空、自动跳过或直接提交/);
  assert.equal(answerCalls.length, 1, '非必填追加题留空时也不能提交后端');

  const completed = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { futureTreatmentFee: 5000 } }
  });
  assert.equal(completed.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 2);
  assert.equal(answerCalls[1].answer[0].children[0].add[0].value, 5000);
});

test('计算器通过 answer 接口逐题作答并在追加题完成前不请求下一题', async () => {
  const store = new MemoryStore();
  const answerCalls = [];
  const api = {
    async get(path) {
      if (path.startsWith('/app/projects/')) return [{ appOnlineId: 'calc-online', projectId: 'calc-project', onlineProjectParentName: '计算器', onlineProjectName: '交通事故赔偿计算' }];
      if (path === '/question/project/calc-online') return { pvId: 'pv-calc' };
      if (path === '/question/getRecordId/calc-online') return 'record-calc';
      throw new Error(`未模拟接口：${path}`);
    },
    async post(path, body) {
      assert.equal(path, '/question/answer');
      answerCalls.push(body);
      if (body.action === 1) {
        return {
          status: 1,
          node: [{
            id: 'disabled',
            title: '本次事故是否造成伤残？',
            component: '1',
            config: { required: true },
            children: [{
              id: 'yes',
              title: '是',
              add: [{ id: 'grade', title: '伤残等级是多少级？', component: '12', config: { required: true, addType: 'follow' } }]
            }, { id: 'no', title: '否' }]
          }]
        };
      }
      if (answerCalls.length === 2) {
        return {
          status: 1,
          node: [{ id: 'medicalFee', title: '医疗费是多少元？', component: '9', config: { required: true }, value: '' }]
        };
      }
      return { status: 0, node: [] };
    }
  };
  const started = await startQuestion({ api, config, store, input: { capability: 'calculator', query: '交通事故赔偿' } });
  assert.equal(started.interaction.type, 'question');
  assert.equal(started.interaction.fields.length, 1);
  assert.deepEqual(started.interaction.choices.map(choice => choice.label), ['是', '否']);
  assert.match(started.interaction.textFallback, /本次事故是否造成伤残/);

  const gradeQuestion = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { disabled: '是' } }
  });
  assert.equal(gradeQuestion.stage, 'needs_follow_up');
  assert.equal(gradeQuestion.interaction.fields[0].key, 'grade');
  assert.equal(answerCalls.length, 1);

  const secondQuestion = await replyQuestion({
    api,
    config,
    store,
    input: { sessionId: started.sessionId, answers: { grade: 10 } }
  });
  assert.equal(secondQuestion.stage, 'collecting');
  assert.equal(secondQuestion.interaction.fields[0].key, 'medicalFee');
  assert.match(secondQuestion.interaction.textFallback, /医疗费是多少元/);
  assert.equal(answerCalls[1].answer[0].children[0].add[0].value, 10);

  const final = await replyQuestion({ api, config, store, input: { sessionId: started.sessionId, answers: { medicalFee: 12000 } } });
  assert.equal(final.stage, 'ready_for_report');
  assert.equal(answerCalls.length, 3);
  assert.ok(answerCalls.every(call => [1, 2].includes(call.action)));
});

test('合同审核缺少立场时先询问甲方或乙方且不读取文件、不调用接口', async () => {
  const store = new MemoryStore();
  let apiCalls = 0;
  const api = new Proxy({}, {
    get() {
      return async () => {
        apiCalls += 1;
        throw new Error('缺少审核立场时不应调用接口');
      };
    }
  });

  const result = await reviewContract({ api, config, store, input: {} });

  assert.equal(result.stage, 'needs_input');
  assert.match(result.prompt, /甲方还是乙方/);
  assert.deepEqual(result.interaction.fields[0].options.map(option => option.label), ['甲方', '乙方']);
  assert.equal(apiCalls, 0);
  assert.equal(store.states.size, 0);
});

test('合同审核以 audit 返回值为最终结果，正常流程不查询详情', async () => {
  const store = new MemoryStore();
  const calls = [];
  const api = {
    async upload(path) {
      calls.push(['upload', path]);
      return 'file-1';
    },
    async post(path) {
      calls.push(['post', path]);
      if (path === '/contract/create') return 'pv-contract';
      if (path === '/contract/audit') return {
        recordId: 'record-contract',
        riskPoints: [{ riskPointLevel: 'High', riskPoint: '违约责任过重', riskPointSolution: '调整违约金' }]
      };
      if (path === '/contract/saveAuditHtml') return true;
      throw new Error(`未模拟接口：${path}`);
    },
    async get(path) {
      calls.push(['get', path]);
      throw new Error('正常流程不应查询详情');
    }
  };
  const filePath = new URL('./fixtures/contract.docx', import.meta.url).pathname;
  const result = await reviewContract({ api, config, store, input: { filePath, contractualStanding: 1 } });
  assert.equal(result.stage, 'completed');
  assert.equal(result.data.recordId, 'record-contract');
  assert.equal(result.data.reportUrl, 'https://legal.example.test/contract_review/detail?id=pv-contract&appId=app-test&device_type=1');
  assert.equal(result.data.reportLinkMarkdown, '[合同审核报告](https://legal.example.test/contract_review/detail?id=pv-contract&appId=app-test&device_type=1)');
  assert.equal(result.links[0].type, 'online_report');
  assert.equal(result.links[0].label, '合同审核报告');
  assert.equal(result.links[0].autoOpen, true);
  assert.equal(result.data.delivery.markdown, result.links[0].markdown);
  assert.equal(result.data.delivery.autoOpen, true);
  assert.equal(result.resultPolicy.sourceOfTruth, 'generated_result_only');
  assert.equal(result.resultPolicy.externalLookupAllowed, false);
  assert.match(result.prompt, /不得调用网页搜索、法律数据库检索、联网查询/);
  assert.match(result.prompt, /立即用宿主内置浏览器打开/);
  assert.match(result.prompt, /不得调起外部浏览器/);
  assert.match(result.prompt, /禁止自行生成 HTML、Markdown、PDF 等任何报告文件/);
  assert.equal(result.downloads, undefined);
  assert.equal(calls.filter(([method]) => method === 'get').length, 0);
  assert.equal(calls.filter(([, path]) => path === '/contract/audit').length, 1);
});

test('合同请求结果不确定时，恢复流程只查询一次详情', async () => {
  const state = { sessionId: 'session-contract', capability: 'contract', stage: 'audit_unknown', pvId: 'pv-contract', contractualStanding: 2 };
  const store = new MemoryStore([state]);
  let details = 0;
  const api = {
    async get(path) {
      assert.equal(path, '/contract/getAuditDetail/pv-contract');
      details += 1;
      return { recordId: 'record-contract', riskPoints: [] };
    },
    async post() {
      return true;
    }
  };
  const result = await resumeContract({ api, config, store, state: await store.load(state.sessionId) });
  assert.equal(result.stage, 'completed');
  assert.equal(details, 1);
});

test('多当事人界面一次只展开一张卡片并限制摘要数量', async () => {
  const html = await fs.readFile(new URL('./fixtures/pleading-form.html', import.meta.url), 'utf8');
  const plaintiffs = Array.from({ length: 25 }, (_, index) => ({ plaintiffName: `原告${index + 1}`, plaintiffGender: index % 2 ? '女' : '男' }));
  const state = {
    sessionId: 'session-pleading',
    capability: 'complaint',
    stage: 'collecting',
    step: 1,
    schema: extractPleadingFormSchema(html),
    params: { plaintiffs, defendants: [{ defendantName: '被告一' }] }
  };
  const store = new MemoryStore([state]);
  const result = await updatePleading({ store, input: { sessionId: state.sessionId, focus: { collection: 'plaintiffs', index: 12 } } });
  const active = result.interaction.fields.find(field => field.active);
  const collapsed = result.interaction.fields.find(field => !field.active);
  assert.equal(result.interaction.view.mode, 'party_cards');
  assert.equal(result.interaction.historyResolution.mode, 'current_task_evidence_first');
  assert.equal(result.interaction.evidenceScope.globalMemoryAllowed, false);
  assert.equal(active.rows.length, 1);
  assert.equal(active.rows[0]._rowIndex, 12);
  assert.equal(active.itemSummaries.length, 20);
  assert.equal(active.omittedItemCount, 5);
  assert.equal(collapsed.rows.length, 0);
});

test('起诉状和答辩状会把上传案件文件内容送入文书要素提取', async t => {
  const materialDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-pleading-materials-'));
  t.after(() => fs.rm(materialDir, { recursive: true, force: true }));
  const materialPath = `${materialDir}/借款事实.txt`;
  await fs.writeFile(materialPath, '原告张三向被告李四出借10万元，借款到期后被告至今未还。', 'utf8');
  const html = await fs.readFile(new URL('./fixtures/pleading-form.html', import.meta.url), 'utf8');

  for (const capability of ['complaint', 'defense']) {
    const state = {
      sessionId: `session-${capability}-materials`,
      capability,
      stage: 'collecting_materials',
      step: 0,
      pvId: `pv-${capability}`,
      schema: extractPleadingFormSchema(html),
      params: {}
    };
    const store = new MemoryStore([state]);
    const api = {
      async post(requestPath, body) {
        assert.equal(requestPath, '/indictment/aiExtractsInfo');
        assert.match(body.inputContent, /出借10万元/);
        assert.match(body.inputContent, /借款到期后被告至今未还/);
        return {
          plaintiffs: [{ plaintiffName: '张三' }],
          defendants: [{ defendantName: '李四' }],
          litigationRequest: '请求返还借款10万元'
        };
      }
    };

    const result = await extractPleading({
      api,
      store,
      input: { sessionId: state.sessionId, filePaths: [materialPath] }
    });

    assert.equal(result.stage, 'collecting');
    assert.match(result.data.caseContext.text, /原告张三/);
    assert.match(result.interaction.caseContext.text, /被告李四/);
    assert.equal(result.data.summary.parties[0].items[0].label, '张三');
  }
});

test('文书图片会上传并参与后端视觉要素提取', async t => {
  const materialDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-pleading-images-'));
  t.after(() => fs.rm(materialDir, { recursive: true, force: true }));
  const imagePath = path.join(materialDir, '借条.jpg');
  await fs.writeFile(imagePath, 'JPG测试占位');
  const html = await fs.readFile(new URL('./fixtures/pleading-form.html', import.meta.url), 'utf8');
  const state = {
    sessionId: 'session-complaint-image',
    capability: 'complaint',
    stage: 'collecting_materials',
    step: 0,
    pvId: 'pv-complaint-image',
    schema: extractPleadingFormSchema(html),
    params: {}
  };
  const store = new MemoryStore([state]);
  let uploadCount = 0;
  const api = {
    async upload(requestPath, form) {
      uploadCount += 1;
      assert.equal(requestPath, '/indictment/uploadImage');
      assert.equal(form.get('pvId'), state.pvId);
      assert.equal(form.get('image').name, '借条.jpg');
    },
    async post(requestPath, body) {
      assert.equal(requestPath, '/indictment/aiExtractsInfo');
      assert.equal(body.pvId, state.pvId);
      assert.equal(body.inputContent, '');
      return {
        plaintiffs: [{ plaintiffName: '张三' }],
        defendants: [{ defendantName: '李四' }],
        litigationRequest: '请求返还借款10万元'
      };
    }
  };

  const result = await extractPleading({
    api,
    store,
    input: { sessionId: state.sessionId, imagePaths: [imagePath] }
  });

  assert.equal(uploadCount, 1);
  assert.equal(result.stage, 'collecting');
  assert.equal(result.data.caseContext, null);
  assert.equal(result.data.summary.parties[0].items[0].label, '张三');
});

test('文书流程遇到未提取的Word材料时保留原任务并等待宿主读取', async t => {
  const materialDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-pending-pleading-'));
  t.after(() => fs.rm(materialDir, { recursive: true, force: true }));
  const materialPath = `${materialDir}/借款合同.docx`;
  await fs.writeFile(materialPath, 'DOCX测试占位');
  const state = {
    sessionId: 'session-pending-pleading',
    capability: 'complaint',
    stage: 'collecting_materials',
    step: 0,
    pvId: 'pv-pending',
    schema: { fields: [], sections: [] },
    params: {}
  };
  const store = new MemoryStore([state]);
  let apiCalls = 0;
  const api = new Proxy({}, {
    get() {
      return async () => { apiCalls += 1; throw new Error('材料未提取前不应调用后端'); };
    }
  });

  const result = await extractPleading({
    api,
    store,
    input: { sessionId: state.sessionId, filePaths: [materialPath] }
  });

  assert.equal(result.stage, 'needs_material_extraction');
  assert.equal(result.sessionId, state.sessionId);
  assert.equal(apiCalls, 0);
  const saved = await store.load(state.sessionId);
  assert.equal(saved.stage, 'collecting_materials');
  assert.equal(saved.step, 0);
});

test('起诉状和答辩状返回点击即下载的 Word 文件链接', async () => {
  const state = {
    sessionId: 'session-pleading-report',
    capability: 'complaint',
    stage: 'ready_to_generate',
    templateId: 'template-1',
    template: { id: 'template-1', title: '民事起诉状' },
    pvId: 'pv-pleading',
    params: {
      plaintiffs: [{ plaintiffName: '张某' }],
      defendants: [{ defendantName: '李某' }],
      litigationRequest: '请求判令返还借款'
    }
  };
  const store = new MemoryStore([state]);
  const api = {
    async post(path) {
      assert.equal(path, '/indictment/generateReport');
      return 'record-pleading';
    }
  };
  const result = await generatePleading({
    api,
    config,
    store,
    input: { sessionId: state.sessionId, confirmed: true }
  });

  assert.equal(result.data.downloadUrl, 'https://example.test/api/indictment/download/record-pleading.docx?appId=app-test&deviceType=1');
  assert.equal(result.data.reportUrl, undefined);
  assert.equal(result.links[0].type, 'download');
  assert.equal(result.links[0].format, 'docx');
  assert.equal(result.links[0].label, '起诉状（Word）');
  assert.equal(result.links[0].markdown, '[起诉状（Word）](https://example.test/api/indictment/download/record-pleading.docx?appId=app-test&deviceType=1)');
  assert.equal(result.links[0].autoOpen, false);
  assert.equal(result.data.downloadLinkMarkdown, result.links[0].markdown);
  assert.equal(result.data.delivery.markdown, result.links[0].markdown);
  assert.equal(result.data.delivery.autoOpen, false);
  assert.equal(result.resultPolicy.sourceOfTruth, 'generated_result_only');
  assert.equal(result.resultPolicy.supplementalLegalResearchAllowed, false);
  assert.match(result.prompt, /不得调用网页搜索、法律数据库检索、联网查询/);
});

test('恢复已完成的答辩状任务时将旧在线地址替换为直接下载链接', () => {
  const result = pleadingResume({
    sessionId: 'session-defense-report',
    capability: 'defense',
    stage: 'completed',
    recordId: 'record-defense',
    reportUrl: 'https://old.example.test/indictment/report/record-defense',
    params: {}
  }, config);

  assert.equal(result.data.reportUrl, undefined);
  assert.equal(result.data.downloadUrl, 'https://example.test/api/indictment/download/record-defense.docx?appId=app-test&deviceType=1');
  assert.equal(result.links[0].type, 'download');
  assert.equal(result.links[0].label, '答辩状（Word）');
  assert.equal(result.links[0].markdown, '[答辩状（Word）](https://example.test/api/indictment/download/record-defense.docx?appId=app-test&deviceType=1)');
  assert.equal(result.links[0].autoOpen, false);
  assert.equal(result.data.downloadLinkMarkdown, result.links[0].markdown);
  assert.equal(result.data.delivery.markdown, result.links[0].markdown);
});
