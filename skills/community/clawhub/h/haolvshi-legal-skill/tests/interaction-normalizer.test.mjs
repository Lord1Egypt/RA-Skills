import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import test from 'node:test';
import {
  applyAnswersToNodes,
  extractPleadingFormSchema,
  materializeInteractionChoices,
  missingRequiredFields,
  nextUnresolvedInteraction,
  normalizeQuestionNodes,
  onlyAutoSkippableFieldsRemain,
  unansweredFields
} from '../scripts/interaction-normalizer.mjs';
import { applyPartyAction } from '../scripts/party-manager.mjs';

test('咨询单选题被转换为可显示的题目卡片并接受中文选项', () => {
  const nodes = [{
    id: 'married',
    title: '是否已经登记结婚？',
    component: '1',
    config: { required: true },
    children: [{ id: 'yes', title: '是' }, { id: 'no', title: '否' }]
  }];
  const interaction = normalizeQuestionNodes(nodes);
  assert.equal(interaction.type, 'question');
  assert.equal(interaction.fields[0].type, 'single_select');
  assert.deepEqual(interaction.fields[0].options.map(item => item.label), ['是', '否']);
  assert.equal(interaction.protocol, 'lvpin.interaction/v1');
  assert.equal(interaction.renderHints.preferNativeControls, true);
  assert.equal(interaction.renderHints.nativeControlsRequired, true);
  assert.equal(interaction.renderHints.mustInvokeNativeTool, true);
  assert.equal(interaction.renderHints.capabilityDetection, true);
  assert.equal(interaction.renderHints.requireCompleteRepresentation, true);
  assert.equal(interaction.renderHints.requireAllOptionsRendered, true);
  assert.equal(interaction.renderHints.requireRenderedOptionCountMatch, true);
  assert.equal(interaction.renderHints.forbidOptionTruncation, true);
  assert.equal(interaction.renderHints.forbidOptionOmission, true);
  assert.equal(interaction.renderHints.incompleteRenderingAction, 'reject_and_rerender');
  assert.equal(interaction.renderHints.tryAlternativeNativeToolsBeforeFallback, true);
  assert.equal(interaction.renderHints.forbidPlainTextWhenNativeAvailable, true);
  assert.equal(interaction.renderHints.fallbackRequiresCapabilityCheck, true);
  assert.equal(interaction.renderHints.fallbackAllowedOnlyWhen, 'no_compatible_native_tool');
  assert.equal(interaction.presentation.mode, 'native_control_required');
  assert.equal(interaction.presentation.mustUseNativeComponent, true);
  assert.equal(interaction.presentation.allOptionsMustBeVisible, true);
  assert.equal(interaction.presentation.optionCountVerificationRequired, true);
  assert.equal(interaction.presentation.incompleteOptionSetIsInvalid, true);
  assert.equal(interaction.presentation.acceptAnswerOnlyAfterCompleteRendering, true);
  assert.equal(interaction.presentation.doNotRenderTextFallbackWhenNativeAvailable, true);
  assert.equal(interaction.evidenceScope.mode, 'current_task_only');
  assert.equal(interaction.evidenceScope.globalMemoryAllowed, false);
  assert.equal(interaction.evidenceScope.memoryToolAllowed, false);
  assert.equal(interaction.evidenceScope.crossTaskMemoryAllowed, false);
  assert.equal(interaction.evidenceScope.otherConversationHistoryAllowed, false);
  assert.equal(interaction.evidenceScope.currentUserQueryMustNotBeExpandedWithMemory, true);
  assert.equal(interaction.historyResolution.mode, 'current_task_evidence_first');
  assert.equal(interaction.historyResolution.scope, 'current_task_only');
  assert.equal(interaction.historyResolution.globalMemoryAllowed, false);
  assert.equal(interaction.historyResolution.memoryToolAllowed, false);
  assert.equal(interaction.historyResolution.crossTaskMemoryAllowed, false);
  assert.ok(interaction.historyResolution.forbiddenSources.includes('other_tasks'));
  assert.equal(interaction.historyResolution.resolveBeforePresenting, true);
  assert.equal(interaction.historyResolution.submitResolvedValues, true);
  assert.equal(interaction.historyResolution.presentUnresolvedOnly, true);
  assert.equal(interaction.historyResolution.requireExplicitUnambiguousSupport, true);
  assert.equal(interaction.historyResolution.latestExplicitCorrectionWins, true);
  assert.equal(interaction.historyResolution.silenceDoesNotMeanNegative, true);
  assert.equal(interaction.historyResolution.noMatchAction, 'present_question_to_user');
  assert.equal(interaction.historyResolution.forbidGuessing, true);
  assert.equal(interaction.historyResolution.forbidDefaultSelection, true);
  assert.equal(interaction.historyResolution.forbidFallbackOptionSelection, true);
  assert.equal(interaction.historyResolution.backendPreselectionIsNotEvidence, true);
  assert.equal(interaction.historyResolution.uncertaintyOptionRequiresExplicitUserChoice, true);
  assert.equal(interaction.historyResolution.autoSubmitOnlyWhen, 'explicit_direct_unambiguous_case_evidence');
  assert.equal(interaction.answerPolicy.onNoCurrentTaskEvidenceMatch, 'render_complete_question_and_wait_for_user');
  assert.equal(interaction.answerPolicy.globalMemoryMustNeverBecomeAnswer, true);
  assert.equal(interaction.answerPolicy.crossTaskFactsMustNeverBecomeAnswer, true);
  assert.equal(interaction.answerPolicy.neverChooseUnknownAsDefault, true);
  assert.equal(interaction.answerPolicy.neverChooseAnyOptionToAdvanceWorkflow, true);
  assert.equal(interaction.answerPolicy.userMustChooseWhenEvidenceMissing, true);
  assert.deepEqual(interaction.choices.map(item => item.label), ['是', '否']);
  assert.deepEqual(interaction.choices.map(item => item.number), [1, 2]);
  assert.deepEqual(interaction.choices.map(item => item.answer), ['是', '否']);
  assert.deepEqual(interaction.choices.map(item => item.hasFollowUp), [false, false]);
  assert.equal(interaction.optionCount, 2);
  assert.equal(interaction.choicesComplete, true);
  assert.equal(interaction.optionManifest[0].expectedOptionCount, 2);
  assert.deepEqual(interaction.optionManifest[0].options.map(item => item.label), ['是', '否']);
  assert.equal(interaction.native.preferredTool, 'AskUserQuestion');
  assert.equal(interaction.native.complete, true);
  assert.deepEqual(interaction.native.coveredFieldKeys, ['married']);
  assert.deepEqual(interaction.native.batches[0].input, {
    questions: [{
      question: '是否已经登记结婚？',
      header: '是否已经登记结婚',
      options: [
        { label: '是', description: '' },
        { label: '否', description: '' }
      ],
      multiSelect: false
    }]
  });
  assert.deepEqual(interaction.inputSchema.properties.married.enum, ['yes', 'no']);
  assert.deepEqual(interaction.inputSchema.properties.married.oneOf, [
    { const: 'yes', title: '是' },
    { const: 'no', title: '否' }
  ]);
  assert.match(interaction.textFallback, /1\. 是\n2\. 否/);

  const answered = applyAnswersToNodes(nodes, { married: '是' });
  assert.equal(answered[0].value, 'yes');
  assert.equal(answered[0].children[0].value, true);
  assert.deepEqual(missingRequiredFields(normalizeQuestionNodes(answered)), []);
});

test('混合字段页按字段拆分原生选择和文本输入，不把五字段表单交给选择器', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'injuredPerson',
    title: '受伤人员信息',
    component: '4',
    children: [
      { id: 'name', title: '姓名', component: '3' },
      { id: 'gender', title: '性别', component: '1', children: [{ id: 'male', title: '男' }, { id: 'female', title: '女' }] },
      { id: 'age', title: '年龄', component: '12' },
      { id: 'liveAt', title: '实际居住地', component: '17', tips: '离开户籍地连续居住满一年的地方' },
      { id: 'registeredAt', title: '户籍地', component: '17', tips: '户口簿、身份证上的登记地址' }
    ]
  }]);

  assert.equal(interaction.fields.length, 5);
  assert.equal(interaction.fields[0].displayOnly, true);
  assert.equal(interaction.renderPlan.mode, 'sequential_units');
  assert.equal(interaction.renderPlan.nativeChoiceCoverageComplete, false, '被跳过的姓名不需要进入原生组件');
  // 地区题按输入呈现并由 area-resolver 解析成地区 id，不再进入原生选择。
  assert.deepEqual(interaction.renderPlan.nativeChoiceFieldKeys, [
    'injuredPerson.gender',
    'injuredPerson.age'
  ]);
  assert.equal(interaction.renderPlan.nativeQuestionBatches.length, 1);
  assert.deepEqual(interaction.renderPlan.nativeQuestionBatches[0].input.questions.map(item => item.question), [
    '性别？', '年龄？'
  ]);
  assert.deepEqual(interaction.renderPlan.units.map(item => item.mode), [
    'skip', 'native_choice', 'native_choice', 'input', 'input'
  ]);
  assert.equal(interaction.native.complete, false);
  assert.deepEqual(interaction.native.coveredFieldKeys, [
    'injuredPerson.gender',
    'injuredPerson.age'
  ]);
  assert.equal(interaction.suggestedChoices.materializedBySkill, true);
  assert.equal(interaction.suggestedChoices.hostGenerationRequired, false);
  assert.deepEqual(interaction.suggestedChoices.fieldKeys, [
    'injuredPerson.age'
  ]);
  assert.equal(interaction.fields[2].type, 'single_select');
  assert.equal(interaction.fields[2].originalType, 'number');
  assert.deepEqual(interaction.fields[2].options.map(item => item.label), ['18岁', '30岁', '45岁', '60岁']);
  assert.equal(interaction.renderPlan.nativeToolConstraints.maxQuestions, 4);
  assert.equal(interaction.renderPlan.nativeToolConstraints.maxOptions, 4);
  assert.equal(interaction.renderPlan.nativeToolConstraints.textInputsSupported, false);
});

test('只有 value 的后端选项也能按显示文字稳定回传', () => {
  const nodes = [{
    id: 'gender',
    title: '性别',
    component: '1',
    children: [{ value: 'male', title: '男' }, { value: 'female', title: '女' }]
  }];
  const answered = applyAnswersToNodes(nodes, { gender: '女' });

  assert.equal(answered[0].value, 'female');
  assert.deepEqual(answered[0].children.map(option => option.value), [false, true]);
  assert.equal(normalizeQuestionNodes(answered).fields[0].value, 'female');
});

test('下一轮交互只暴露一个未回答字段，并保留多填空候选选择能力', () => {
  const interaction = normalizeQuestionNodes([
    { id: 'name', title: '姓名', component: '3' },
    { id: 'age', title: '年龄', component: '12' },
    { id: 'liveAt', title: '实际居住地', component: '17' }
  ]);
  const next = nextUnresolvedInteraction(interaction);

  assert.deepEqual(next.fields.map(field => field.key), ['age']);
  assert.deepEqual(next.renderPlan.units.map(unit => unit.fieldKey), ['age']);
  assert.equal(next.fields[0].type, 'single_select');
  assert.equal(next.fields[0].originalType, 'number');
  assert.equal(next.renderPlan.units[0].mode, 'native_choice');
  assert.equal(next.suggestedChoices.hostGenerationRequired, false);
  assert.equal(next.native.batches.length, 1);
  assert.equal(next.sequence.mode, 'one_field_per_turn');
  assert.equal(next.sequence.totalRemaining, 2);
});

test('单个填空字段直接组装为与普通选择题一致的标准原生单选题', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'injuryGrade',
    title: '伤残等级',
    component: '12',
    config: { required: true }
  }]);

  assert.equal(interaction.fields[0].type, 'single_select');
  assert.equal(interaction.fields[0].originalType, 'number');
  assert.deepEqual(interaction.fields[0].options.map(item => item.label), [
    '无伤残等级', '十级伤残', '九级伤残', '八级伤残'
  ]);
  assert.equal(interaction.renderPlan.mode, 'native_choice');
  assert.equal(interaction.renderPlan.units[0].mode, 'native_choice');
  assert.equal(interaction.suggestedChoices.hostGenerationRequired, false);
  assert.equal(interaction.native.complete, true);
  assert.deepEqual(interaction.native.batches[0].input.questions[0], {
    question: '伤残等级？',
    header: '伤残等级',
    options: [
      { label: '无伤残等级', description: '' },
      { label: '十级伤残', description: '' },
      { label: '九级伤残', description: '' },
      { label: '八级伤残', description: '' }
    ],
    multiSelect: false
  });
  assert.equal(Object.hasOwn(interaction, 'aiChoice'), false);
});

test('鉴定费填空生成二至四个常识金额选项并把显示值转换为后端数值', () => {
  const nodes = [{
    id: 'appraisalFee',
    title: '三期鉴定费金额',
    component: '9',
    config: { required: true }
  }];
  const interaction = normalizeQuestionNodes(nodes);

  assert.equal(interaction.fields[0].type, 'single_select');
  assert.equal(interaction.fields[0].originalType, 'money');
  assert.deepEqual(interaction.fields[0].options.map(item => item.label), [
    '500元', '1,000元', '2,000元', '3,000元'
  ]);
  assert.equal(interaction.optionCount, 4);
  assert.equal(interaction.choicesComplete, true);
  assert.deepEqual(interaction.inputSchema.properties.appraisalFee.enum, ['500', '1000', '2000', '3000']);

  const answered = applyAnswersToNodes(nodes, { appraisalFee: '1,000元' });
  assert.equal(answered[0].value, 1000);
});

test('非必填敏感字段直接跳过，但居住地和户籍地仍保留', () => {
  const interaction = normalizeQuestionNodes([
    { id: 'name', title: '姓名', component: '3', config: { required: false } },
    { id: 'phone', title: '联系电话', component: '3', config: { required: false } },
    { id: 'identity', title: '身份证号码', component: '3', config: { required: false } },
    { id: 'liveAt', title: '实际居住地', component: '17', config: { required: false } },
    { id: 'registeredAt', title: '户籍地', component: '17', config: { required: false } }
  ]);

  assert.deepEqual(interaction.fields.map(field => field.skipIfOptionalSensitive), [true, true, true, false, false]);
  assert.deepEqual(interaction.fields.map(field => field.responseRequired), [false, false, false, true, true]);
  // 地区题的取值是地区表 id，凭空造出的“经常居住地”之类不是地区，不能当选项，
  // 因此没有案情地名时按输入题呈现，由 area-resolver 校验并回真实候选。
  assert.deepEqual(interaction.renderPlan.units.map(unit => unit.mode), ['skip', 'skip', 'skip', 'input', 'input']);
  assert.equal(interaction.fields[3].valueContract.submit, 'area_id');
  assert.equal(interaction.fields[3].valueContract.areaLevel, 2);
  assert.equal(interaction.sensitiveFieldPolicy.repeatedGroupFieldsAreNeverAutoSkipped, true);
  assert.deepEqual(unansweredFields(interaction).map(field => field.key), ['liveAt', 'registeredAt']);
  assert.deepEqual(nextUnresolvedInteraction(interaction).fields.map(field => field.key), ['liveAt']);
  assert.equal(onlyAutoSkippableFieldsRemain(normalizeQuestionNodes([
    { id: 'phone', title: '联系电话', component: '3', config: { required: false } }
  ])), true);
  assert.equal(onlyAutoSkippableFieldsRemain(normalizeQuestionNodes([
    { id: 'liveAt', title: '居住地', component: '17', config: { required: false } }
  ])), false);
  const requiredSensitive = normalizeQuestionNodes([
    { id: 'phone', title: '联系电话', component: '3', config: { required: true } }
  ]);
  assert.equal(requiredSensitive.fields[0].skipIfOptionalSensitive, false);
  assert.equal(requiredSensitive.fields[0].type, 'text');
  assert.equal(requiredSensitive.renderPlan.units[0].mode, 'input');
  assert.deepEqual(requiredSensitive.fields[0].options, []);
  assert.deepEqual(unansweredFields(requiredSensitive).map(field => field.key), ['phone']);
});

test('日期填空优先把案情中的明确日期放入标准单选选项', () => {
  const interaction = materializeInteractionChoices(normalizeQuestionNodes([{
    id: 'accidentDate',
    title: '事故发生日期',
    component: '10',
    config: { required: true }
  }]), '2024年11月20号在云南省大理州下关市发生交通事故');

  assert.equal(interaction.fields[0].type, 'single_select');
  assert.equal(interaction.fields[0].originalType, 'date');
  assert.equal(interaction.fields[0].options[0].value, '2024-11-20');
  assert.equal(interaction.fields[0].options[0].description, '来自当前案情中的日期');
});

test('可选且仅用于报告展示的空姓名不会成为待渲染题目', () => {
  const interaction = normalizeQuestionNodes([
    { id: 'name', title: '姓名', component: '3' },
    { id: 'age', title: '年龄', component: '12' }
  ]);

  assert.deepEqual(unansweredFields(interaction), [{
    key: 'age',
    label: '年龄',
    backendRequired: false,
    responseRequired: true
  }]);
  assert.deepEqual(nextUnresolvedInteraction(interaction).fields.map(field => field.key), ['age']);
});

test('没有匹配案情时不把不清楚或后端值误当成默认选择', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'insurance',
    title: '车辆是否购买商业险？',
    component: '1',
    config: { required: true },
    children: [
      { value: 'yes', title: '是' },
      { value: 'no', title: '否' },
      { value: 'unknown', title: '不清楚' }
    ]
  }]);

  assert.deepEqual(interaction.fields[0].options.map(option => option.selected), [false, false, false]);
  assert.deepEqual(interaction.choices.map(option => option.selected), [false, false, false]);
  assert.deepEqual(interaction.optionManifest[0].options.map(option => option.selected), [false, false, false]);
  assert.deepEqual(interaction.choices.map(option => option.value), ['yes', 'no', 'unknown']);
  assert.match(interaction.textFallback, /3\. 不清楚/);
  assert.ok(interaction.historyResolution.uncertaintyLabels.includes('不清楚'));
});

test('非必填题没有答案时仍要求用户回答且不能留空提交', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'futureTreatmentFee',
    title: '后续治疗费用金额',
    component: '9',
    config: { required: false },
    value: ''
  }]);

  assert.equal(interaction.fields[0].required, false);
  assert.equal(interaction.fields[0].backendRequired, false);
  assert.equal(interaction.fields[0].responseRequired, true);
  assert.deepEqual(interaction.inputSchema.required, ['futureTreatmentFee']);
  assert.equal(interaction.presentation.optionalFieldsMustAlsoBePresented, true);
  assert.equal(interaction.presentation.requireResponseForEveryUnresolvedField, true);
  assert.equal(interaction.historyResolution.presentOptionalWhenUnresolved, true);
  assert.equal(interaction.historyResolution.autoSkipOptionalFields, false);
  assert.equal(interaction.answerPolicy.allowBlankOptionalAnswer, false);
  assert.equal(interaction.answerPolicy.allowAutomaticOptionalSkip, false);
  assert.deepEqual(unansweredFields(interaction), [{
    key: 'futureTreatmentFee',
    label: '后续治疗费用金额',
    backendRequired: false,
    responseRequired: true
  }]);
  assert.match(interaction.textFallback, /后续治疗费用金额（请回答）/);
});

test('当前任务明确只有存款时，车辆数量等条件字段标记为不适用并保留空值', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'vehicleCount',
    title: '有几辆车存在争议',
    component: '12',
    config: { required: true }
  }], {
    suggestionContext: '争议财产类型=存款；用户选择的只有存款，其他财产都没有'
  });

  const field = interaction.fields[0];
  assert.equal(field.notApplicable, true);
  assert.equal(field.applicability.status, 'not_applicable');
  assert.equal(field.applicability.category, 'vehicle');
  assert.equal(field.responseRequired, false);
  assert.deepEqual(unansweredFields(interaction), []);
  assert.deepEqual(interaction.inputSchema.required, []);
  assert.equal(interaction.renderPlan.units[0].reason, 'explicit_non_applicable');
  assert.equal(onlyAutoSkippableFieldsRemain(interaction), true);
  assert.deepEqual(field.value, '');
  assert.deepEqual(field.options.map(option => option.label), ['1', '2', '3', '5']);
  assert.equal(interaction.presentation.nonApplicableEvidenceMustBeExplicit, true);
  assert.equal(interaction.answerPolicy.explicitNonApplicableAction, 'preserve_blank_and_advance');
});

test('仅因案情没有提到车辆不能把车辆字段误判为不适用', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'vehicleCount',
    title: '有几辆车存在争议',
    component: '12',
    config: { required: true }
  }], { suggestionContext: '当前任务未提到车辆情况' });

  assert.equal(interaction.fields[0].notApplicable, false);
  assert.equal(interaction.fields[0].responseRequired, true);
  assert.deepEqual(unansweredFields(interaction).map(field => field.key), ['vehicleCount']);
  assert.equal(onlyAutoSkippableFieldsRemain(interaction), false);
});

test('超过常见组件容量的选项仍完整保留并要求逐项核对渲染数量', () => {
  const labels = ['无责任', '次要责任', '同等责任', '主要责任', '全部责任', '责任未认定', '其他责任'];
  const interaction = normalizeQuestionNodes([{
    id: 'liability',
    title: '请选择事故责任',
    component: '1',
    config: { required: true },
    children: labels.map((title, index) => ({ id: `value-${index + 1}`, title }))
  }]);

  assert.equal(interaction.optionCount, labels.length);
  assert.equal(interaction.choices.length, labels.length);
  assert.deepEqual(interaction.choices.map(item => item.label), labels);
  assert.deepEqual(interaction.choices.map(item => item.total), Array(labels.length).fill(labels.length));
  assert.equal(interaction.optionManifest[0].expectedOptionCount, labels.length);
  assert.equal(interaction.optionManifest[0].requireExactRenderedCount, true);
  assert.deepEqual(interaction.inputSchema.properties.liability['x-enumNames'], labels);
  labels.forEach((label, index) => assert.match(interaction.textFallback, new RegExp(`${index + 1}\\. ${label}`)));
  assert.deepEqual(interaction.renderHints.capacityFallbackOrder, [
    'native_selector_with_all_options',
    'native_form_or_input_with_complete_numbered_option_list',
    'complete_text_fallback_only_without_compatible_native_tool'
  ]);
});

test('选项下存在追加题时交互结构会标记但不提前展开追加题', () => {
  const nodes = [{
    id: 'gender',
    title: '您是男方还是女方？',
    component: '1',
    children: [
      {
        id: 'male',
        title: '男方',
        add: [{ id: 'age', title: '您的年龄是多少？', component: '12', config: { required: true } }]
      },
      { id: 'female', title: '女方' }
    ]
  }];

  const interaction = normalizeQuestionNodes(nodes);
  assert.equal(interaction.fields.length, 1);
  assert.equal(interaction.fields[0].options[0].hasFollowUp, true);
  assert.equal(interaction.fields[0].options[0].followUpCount, 1);
  assert.equal(interaction.choices[0].hasFollowUp, true);
  assert.doesNotMatch(interaction.textFallback, /您的年龄是多少/);
});

test('用户输入编号时始终按当前显示顺序选择而不是按后端数字编号选择', () => {
  const nodes = [{
    id: 'standing',
    title: '请选择审核立场',
    component: '1',
    children: [{ id: '2', title: '甲方' }, { id: '1', title: '乙方' }]
  }];

  const interaction = normalizeQuestionNodes(nodes);
  assert.match(interaction.textFallback, /1\. 甲方\n2\. 乙方/);

  const first = applyAnswersToNodes(nodes, { standing: '1' });
  assert.equal(first[0].value, '2');
  assert.equal(first[0].children[0].value, true);

  const second = applyAnswersToNodes(nodes, { standing: '乙方' });
  assert.equal(second[0].value, '1');
  assert.equal(second[0].children[1].value, true);
});

test('计算器动态矩阵被转换为可重复记录卡片', () => {
  const nodes = [{
    id: 'income',
    title: '收入记录',
    component: '6',
    config: { matrixDynamicTitle: '月收入', nameUnit: '笔' },
    children: [
      { id: 'amount', title: '金额', component: '9', config: { required: true }, value: [1000, 2000] },
      { id: 'month', title: '月份', component: '10', value: ['2026-01', '2026-02'] }
    ]
  }];
  const interaction = normalizeQuestionNodes(nodes, { form: true });
  assert.equal(interaction.fields[0].type, 'repeatable_group');
  assert.equal(interaction.fields[0].rows.length, 2);

  const answered = applyAnswersToNodes(nodes, {
    income: [{ amount: 3000, month: '2026-03' }]
  });
  assert.deepEqual(answered[0].children[0].value, [3000]);
});

test('重复记录中的姓名不因敏感字段规则被自动跳过', () => {
  const interaction = normalizeQuestionNodes([{
    id: 'parties',
    title: '当事人',
    component: '6',
    children: [{ id: 'name', title: '姓名', component: '3', config: { required: false } }]
  }], { form: true });

  assert.equal(interaction.fields[0].fields[0].sensitive, true);
  assert.equal(interaction.fields[0].fields[0].skipIfOptionalSensitive, false);
  assert.equal(unansweredFields(interaction)[0].label, '当事人1：姓名');
});

test('模板表单能识别多原告、多被告及主要步骤', async () => {
  const html = await fs.readFile(new URL('./fixtures/pleading-form.html', import.meta.url), 'utf8');
  const schema = extractPleadingFormSchema(html);
  assert.ok(schema.fields.some(field => field.key === 'plaintiffs[].plaintiffName' && field.section === '当事人信息'));
  assert.ok(schema.fields.some(field => field.key === 'defendants[].defendantName' && field.section === '当事人信息'));
  assert.ok(schema.fields.some(field => field.key === 'litigationRequest' && field.section === '诉讼请求或答辩意见'));
  assert.ok(schema.fields.some(field => field.key === 'evidenceList' && field.section === '证据材料'));
  assert.ok(schema.fields.some(field => field.key === 'courtName' && field.section === '法院、管辖与送达'));
});

test('可重复当事人支持新增、修改和删除', () => {
  let params = { plaintiffs: [{ plaintiffName: '张一' }] };
  params = applyPartyAction(params, { type: 'add', collection: 'plaintiffs', value: { plaintiffName: '张二' } });
  assert.equal(params.plaintiffs.length, 2);
  params = applyPartyAction(params, { type: 'update', collection: 'plaintiffs', index: 1, value: { plaintiffName: '张三' } });
  assert.equal(params.plaintiffs[1].plaintiffName, '张三');
  params = applyPartyAction(params, { type: 'remove', collection: 'plaintiffs', index: 0 });
  assert.equal(params.plaintiffs[0].plaintiffName, '张三');
});
