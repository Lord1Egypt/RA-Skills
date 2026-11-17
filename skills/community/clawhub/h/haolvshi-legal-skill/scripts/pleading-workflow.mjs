import crypto from 'node:crypto';
import { SkillError } from './errors.mjs';
import {
  capabilityResultLink,
  pleadingDownloadUrl,
  resultDelivery,
  resultGroundingPolicy
} from './report-links.mjs';
import {
  extractPleadingFormSchema,
  parseMaybeJson,
  plainText,
  withInteractionRendering
} from './interaction-normalizer.mjs';
import {
  applyPartyAction,
  applyPatches,
  getAtPath,
  summarizePleadingParams
} from './party-manager.mjs';
import {
  createFileFormData,
  validatePleadingImage
} from './multipart.mjs';
import {
  attachCaseContext,
  materialExtractionRequired,
  prepareCaseMaterials,
  publicCaseContext
} from './case-materials.mjs';

const TYPE_BY_CAPABILITY = { complaint: 1, defense: 2 };
const STEP_NAMES = [
  '案件材料',
  '当事人信息',
  '诉讼请求或答辩意见',
  '事实与理由',
  '证据材料',
  '法院、管辖与送达',
  '其他信息',
  '确认生成'
];
const FIELD_PAGE_SIZE = 8;
const PARTY_SUMMARY_LIMIT = 20;

function normalizedTemplate(item) {
  return { id: item.id, name: item.title || item.name || '', title: item.title || item.name || '' };
}

export async function pleadingCatalog(api, config, capability, query, limit) {
  const type = TYPE_BY_CAPABILITY[capability];
  if (!type) throw new SkillError('CAPABILITY_INVALID', '文书能力应为 complaint 或 defense');
  const items = await api.get('/indictment/list', { query: { appId: config.appId, type } });
  const templates = (items || []).map(normalizedTemplate);
  // 和咨询、计算器同样的道理：模板名是“民事起诉状（劳动争议）”这类法律术语，
  // 用户说的是“追讨拖欠工资”，分词打分一个都命中不了，会把目录整个过滤成空，
  // 用户直接用不了文书功能。这里返回完整模板，由宿主大模型做语义选型。
  return Number.isInteger(limit) && limit >= 0 ? templates.slice(0, limit) : templates;
}

function withClientIds(value) {
  if (Array.isArray(value)) {
    return value.map(item => {
      const next = withClientIds(item);
      return next && typeof next === 'object' && !Array.isArray(next)
        ? { _clientId: next._clientId || crypto.randomUUID(), ...next }
        : next;
    });
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, child]) => [key, withClientIds(child)]));
  }
  return value;
}

function stripInternal(value) {
  if (Array.isArray(value)) return value.map(stripInternal);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value)
        .filter(([key]) => !key.startsWith('_'))
        .map(([key, child]) => [key, stripInternal(child)])
    );
  }
  return value;
}

function parseExtracted(value) {
  let parsed = parseMaybeJson(value);
  if (typeof parsed === 'string') {
    const cleaned = parsed.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '').trim();
    parsed = parseMaybeJson(cleaned);
    if (typeof parsed === 'string') {
      const objectMatch = cleaned.match(/\{[\s\S]*\}/);
      if (objectMatch) parsed = parseMaybeJson(objectMatch[0]);
    }
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new SkillError('PLEADING_EXTRACTION_INVALID', 'AI 提取结果不是有效的文书字段对象', {
      details: { preview: plainText(String(value)).slice(0, 500) }
    });
  }
  return withClientIds(parsed);
}

function sectionFields(schema, sectionName) {
  return (schema?.fields || []).filter(field => field.section === sectionName);
}

function collectionLabel(collection, fields = []) {
  const source = `${collection} ${fields.map(field => field.key).join(' ')}`;
  if (/orgPlaintiff/i.test(source)) return '法人或组织原告';
  if (/plaintiff/i.test(source)) return '自然人原告';
  if (/orgDefendant|defendantOrg/i.test(source)) return '法人或组织被告';
  if (/defendant/i.test(source)) return '自然人被告';
  if (/orgThird/i.test(source)) return '法人或组织第三人';
  if (/third/i.test(source)) return '第三人';
  if (/respondent/i.test(source)) return '答辩人';
  if (/defender/i.test(source)) return '辩护人';
  if (/agent/i.test(source)) return '委托诉讼代理人';
  if (/applicant/i.test(source)) return '申请人';
  return collection;
}

function partySummary(row, index) {
  const entries = Object.entries(row || {}).filter(([key, value]) => !key.startsWith('_') && value !== '' && value !== null && value !== undefined);
  const named = entries.find(([key]) => /name|姓名|名称/i.test(key));
  const identified = entries.find(([key]) => /idnumber|证件|身份证/i.test(key));
  return {
    index,
    label: String(named?.[1] || `第${index + 1}位`),
    secondary: identified ? String(identified[1]).replace(/(.{4}).+(.{4})/, '$1****$2') : '',
    filledFieldCount: entries.length
  };
}

function pleadingSummary(params = {}) {
  const summary = summarizePleadingParams(params);
  return {
    parties: summary.parties.map(party => ({
      collection: party.collection,
      label: collectionLabel(party.collection),
      count: party.count,
      items: party.items.slice(0, PARTY_SUMMARY_LIMIT).map(partySummary),
      omittedItemCount: Math.max(0, party.count - PARTY_SUMMARY_LIMIT)
    })),
    filledFieldCount: summary.filledFieldCount,
    fields: summary.fields.slice(0, 50).map(field => ({
      key: field.key,
      value: typeof field.value === 'string' && field.value.length > 500
        ? `${field.value.slice(0, 500)}…`
        : field.value
    })),
    omittedFieldCount: Math.max(0, summary.fields.length - 50)
  };
}

function buildStepFields(state, sectionName) {
  const schemaFields = sectionFields(state.schema, sectionName);
  const params = state.params || {};
  const scalarFields = [];
  const repeatable = new Map();

  for (const field of schemaFields) {
    const match = field.key.match(/^(.+)\[\]\.([^.]+(?:\..+)?)$/);
    if (match) {
      const [, collection, childKey] = match;
      if (!repeatable.has(collection)) repeatable.set(collection, []);
      repeatable.get(collection).push({ ...field, key: childKey });
    } else {
      scalarFields.push({ ...field, value: getAtPath(params, field.key) ?? '' });
    }
  }

  if (sectionName === '当事人信息') {
    const represented = new Set(repeatable.keys());
    for (const party of summarizePleadingParams(params).parties) {
      if (!represented.has(party.collection)) {
        repeatable.set(party.collection, []);
      }
    }

    const collections = [...repeatable.keys()];
    const requestedCollection = state.partyFocus?.collection;
    const activeCollection = collections.includes(requestedCollection)
      ? requestedCollection
      : collections.find(collection => (getAtPath(params, collection) || []).length > 0) || collections[0] || null;
    const fields = collections.map(collection => {
      const childFields = repeatable.get(collection) || [];
      const allRows = Array.isArray(getAtPath(params, collection)) ? getAtPath(params, collection) : [];
      const requestedIndex = activeCollection === collection ? Number(state.partyFocus?.index || 0) : 0;
      const activeIndex = allRows.length ? Math.max(0, Math.min(allRows.length - 1, requestedIndex)) : 0;
      const active = collection === activeCollection;
      return {
        key: collection,
        label: collectionLabel(collection, childFields),
        type: 'repeatable_group',
        required: childFields.some(field => field.required),
        fields: active ? childFields : [],
        rows: active && allRows.length ? [{ ...allRows[activeIndex], _rowIndex: activeIndex }] : [],
        itemCount: allRows.length,
        active,
        activeIndex,
        itemSummaries: allRows.slice(0, PARTY_SUMMARY_LIMIT).map(partySummary),
        omittedItemCount: Math.max(0, allRows.length - PARTY_SUMMARY_LIMIT),
        minItems: 0,
        maxItems: 50,
        actions: ['focus', 'add', 'update', 'remove']
      };
    });
    return {
      fields,
      view: {
        mode: 'party_cards',
        activeCollection,
        collectionCount: collections.length,
        instruction: '同一时间只展开一类当事人的一张卡片；使用 focus 切换当事人类型或序号。'
      }
    };
  }

  const repeatableCollections = [...repeatable.keys()];
  const requestedCollection = state.partyFocus?.collection;
  const activeCollection = repeatableCollections.includes(requestedCollection)
    ? requestedCollection
    : repeatableCollections[0] || null;
  const repeatableFields = repeatableCollections.map(collection => {
    const childFields = repeatable.get(collection) || [];
    const allRows = Array.isArray(getAtPath(params, collection)) ? getAtPath(params, collection) : [];
    const requestedIndex = activeCollection === collection ? Number(state.partyFocus?.index || 0) : 0;
    const activeIndex = allRows.length ? Math.max(0, Math.min(allRows.length - 1, requestedIndex)) : 0;
    const active = collection === activeCollection;
    return {
      key: collection,
      label: collectionLabel(collection, childFields),
      type: 'repeatable_group',
      required: childFields.some(field => field.required),
      fields: active ? childFields : [],
      rows: active && allRows.length ? [{ ...allRows[activeIndex], _rowIndex: activeIndex }] : [],
      itemCount: allRows.length,
      active,
      activeIndex,
      itemSummaries: allRows.slice(0, PARTY_SUMMARY_LIMIT).map(partySummary),
      omittedItemCount: Math.max(0, allRows.length - PARTY_SUMMARY_LIMIT),
      minItems: 0,
      maxItems: 50,
      actions: ['focus', 'add', 'update', 'remove']
    };
  });
  const pageCount = Math.max(1, Math.ceil(scalarFields.length / FIELD_PAGE_SIZE));
  const requestedPage = Number(state.fieldPages?.[sectionName] || 0);
  const page = Math.max(0, Math.min(pageCount - 1, requestedPage));
  return {
    fields: [
      ...repeatableFields,
      ...scalarFields.slice(page * FIELD_PAGE_SIZE, (page + 1) * FIELD_PAGE_SIZE)
    ],
    view: {
      mode: 'field_pages',
      page,
      pageCount,
      pageSize: FIELD_PAGE_SIZE,
      totalFields: scalarFields.length,
      repeatableCollectionCount: repeatableCollections.length,
      activeCollection
    }
  };
}

function pleadingInteraction(state, requestedStep) {
  const step = Math.max(0, Math.min(
    STEP_NAMES.length - 1,
    Number.isInteger(requestedStep) ? requestedStep : Number(state.step || 0)
  ));
  const title = STEP_NAMES[step];
  const summary = pleadingSummary(state.params || {});
  if (step === 0) {
    return attachCaseContext(withInteractionRendering({
      type: 'form',
      title: '请提供案件材料',
      step,
      steps: STEP_NAMES,
      fields: [
        { key: 'content', label: '案情描述', type: 'textarea', required: false, responseRequired: false, value: state.inputContent || '' },
        { key: 'filePaths', label: '案件材料文件', type: 'file', required: false, responseRequired: false, value: [] }
      ],
      submitLabel: 'AI 提取文书要素'
    }), state.caseContext);
  }
  if (step === STEP_NAMES.length - 1) {
    return attachCaseContext(withInteractionRendering({
      type: 'confirmation',
      title: '确认生成文书',
      step,
      steps: STEP_NAMES,
      fields: [],
      summary,
      submitLabel: '确认并生成'
    }), state.caseContext);
  }
  const stepContent = buildStepFields(state, title);
  return attachCaseContext(withInteractionRendering({
    type: 'step_form',
    title,
    step,
    steps: STEP_NAMES,
    presentation: {
      mode: 'wizard',
      collapseInactiveCards: true,
      plainChatFallback: '每次只询问当前页或当前当事人卡片中的字段，不在一条消息中展开整份文书。'
    },
    fields: stepContent.fields,
    view: stepContent.view,
    submitLabel: step === STEP_NAMES.length - 2 ? '查看生成确认' : '保存并继续'
  }), state.caseContext);
}

async function chooseTemplate(api, config, input) {
  const candidates = await pleadingCatalog(api, config, input.capability, input.query, 12);
  if (input.templateId) {
    const exact = candidates.find(item => item.id === input.templateId)
      || (await pleadingCatalog(api, config, input.capability, '', 500)).find(item => item.id === input.templateId);
    if (!exact) throw new SkillError('TEMPLATE_NOT_FOUND', '没有找到指定文书模板');
    return { template: exact, candidates };
  }
  return { template: candidates.length === 1 ? candidates[0] : null, candidates };
}

export async function startPleading({ api, config, store, input }) {
  const { template, candidates } = await chooseTemplate(api, config, input);
  if (!template) {
    return {
      ok: true,
      capability: input.capability,
      stage: 'needs_selection',
      prompt: '找到多个文书模板。只能依据当前任务内用户消息和当前任务材料选择模板；禁止使用全局记忆、其他任务、其他线程、旧案例、旧文书或示例补充 query 或选择模板。只有当前任务证据能够直接、明确、唯一匹配时才自动选择；没有匹配或仍有实质歧义时必须向用户展示完整候选项，不得自动选择“不清楚”“其他”或任意默认模板。',
      data: { candidates }
    };
  }
  const identity = await store.identity();
  const pvId = await api.post('/indictment/generatePvId', {
    id: template.id,
    appId: config.appId,
    deviceType: config.deviceType,
    machineId: identity.machineId,
    code: input.code || null
  });
  const html = await api.get(`/indictment/view/${encodeURIComponent(template.id)}`, {
    query: {
      appId: config.appId,
      deviceType: config.deviceType,
      machineId: identity.machineId,
      code: input.code || null,
      pvId
    },
    unwrap: false,
    accept: 'text/html'
  });
  const schema = extractPleadingFormSchema(String(html || ''));
  const state = await store.create({
    capability: input.capability,
    stage: 'collecting_materials',
    step: 0,
    template,
    templateId: template.id,
    pvId,
    code: input.code || null,
    schema,
    params: {}
  });
  state.formHtmlPath = await store.writeArtifact(state.sessionId, 'template.html', String(html || ''));
  await store.save(state);

  return {
    ok: true,
    capability: state.capability,
    stage: state.stage,
    sessionId: state.sessionId,
    prompt: '模板已准备好。只忠实汇总当前任务/当前线程内用户已经提供的案情并连同当前任务材料调用 pleading-extract；content 必须来自当前任务，禁止读取或混入全局记忆、其他任务、其他线程、旧案例、旧文书、示例、评测、交接文档、测试记录或日志。只有当前任务消息和材料均没有案件事实时才请用户补充。',
    interaction: pleadingInteraction(state, 0),
    data: {
      template,
      pvId,
      schema: {
        templateName: schema.templateName,
        fieldCount: schema.fieldCount,
        sections: schema.sections.map(section => ({ title: section.title, fieldCount: section.fields.length }))
      }
    }
  };
}

export async function extractPleading({ api, store, input }) {
  const state = await store.load(input.sessionId);
  if (!['complaint', 'defense'].includes(state.capability)) {
    throw new SkillError('SESSION_CAPABILITY_MISMATCH', '该任务不是起诉状或答辩状任务');
  }
  const materials = await prepareCaseMaterials(input, {
    deferredExtensions: ['.jpg', '.jpeg', '.png']
  });
  if (materials.unresolvedFiles.length) {
    return materialExtractionRequired({
      capability: state.capability,
      sessionId: state.sessionId,
      unresolvedFiles: materials.unresolvedFiles
    });
  }
  const combinedContent = [String(input.content || '').trim(), materials.text]
    .filter(Boolean)
    .join('\n\n');
  if (!combinedContent && materials.deferredFiles.length === 0) {
    throw new SkillError('PLEADING_MATERIAL_REQUIRED', '请提供案情描述或案件材料文件');
  }
  for (const descriptor of materials.deferredFiles) {
    validatePleadingImage(descriptor);
    const form = await createFileFormData('image', descriptor, { pvId: state.pvId });
    await api.upload('/indictment/uploadImage', form);
  }
  const extracted = await api.post('/indictment/aiExtractsInfo', {
    pvId: state.pvId,
    inputContent: combinedContent
  });
  state.inputContent = combinedContent;
  state.caseContext = publicCaseContext(materials);
  state.params = parseExtracted(extracted);
  state.step = 1;
  state.stage = 'collecting';
  await store.save(state);
  return {
    ok: true,
    capability: state.capability,
    stage: state.stage,
    sessionId: state.sessionId,
    prompt: '文书要素已经提取。每个步骤在展示前只依据当前任务内用户消息、当前任务材料、当前 sessionId 已有提取值和当前任务更正匹配；禁止使用全局记忆、其他任务、其他线程、旧案例、旧文书、示例、评测、交接文档、测试记录或日志填写 patches、当事人、请求、事实理由等字段。只有存在直接、明确、唯一的当前任务依据时才能自动填写。没有匹配、证据不足、冲突或无法唯一判断的信息必须返回给用户本人填写或选择，不得用“不清楚”、其他兜底值或任意默认值代填；生成前再让用户确认一次完整摘要。',
    interaction: pleadingInteraction(state, 1),
    data: {
      summary: pleadingSummary(state.params),
      caseContext: state.caseContext
    }
  };
}

export async function updatePleading({ store, input }) {
  const state = await store.load(input.sessionId);
  if (!['complaint', 'defense'].includes(state.capability)) {
    throw new SkillError('SESSION_CAPABILITY_MISMATCH', '该任务不是起诉状或答辩状任务');
  }
  if (input.patches) state.params = applyPatches(state.params, input.patches);
  state.partyFocus ||= {};
  state.fieldPages ||= {};
  const actions = input.partyActions || (input.partyAction ? [input.partyAction] : []);
  for (const action of actions) {
    state.params = applyPartyAction(state.params, action);
    const parties = getAtPath(state.params, action.collection) || [];
    if (action.type === 'add') {
      state.partyFocus = { collection: action.collection, index: Math.max(0, parties.length - 1) };
    } else if (action.type === 'remove' && state.partyFocus.collection === action.collection) {
      state.partyFocus.index = Math.max(0, Math.min(Number(state.partyFocus.index || 0), parties.length - 1));
    }
  }
  if (input.focus?.collection) {
    const collection = input.focus.collection;
    const parties = getAtPath(state.params, collection);
    if (parties !== undefined && !Array.isArray(parties)) {
      throw new SkillError('PARTY_COLLECTION_INVALID', `字段 ${collection} 不是可重复列表`);
    }
    const index = Number(input.focus.index || 0);
    if (Array.isArray(parties) && parties.length && (!Number.isInteger(index) || index < 0 || index >= parties.length)) {
      throw new SkillError('PARTY_INDEX_INVALID', '需要查看的当事人序号不存在');
    }
    state.partyFocus = { collection, index: Number.isInteger(index) ? index : 0 };
  }
  if (input.step !== undefined) {
    state.step = typeof input.step === 'string' ? STEP_NAMES.indexOf(input.step) : Number(input.step);
    if (state.step < 0) throw new SkillError('PLEADING_STEP_INVALID', '没有找到指定文书步骤');
  } else if (input.direction === 'next') {
    state.step = Math.min(STEP_NAMES.length - 1, Number(state.step || 0) + 1);
  } else if (input.direction === 'previous') {
    state.step = Math.max(1, Number(state.step || 1) - 1);
  }
  if (input.fieldPage !== undefined) {
    const page = Number(input.fieldPage);
    if (!Number.isInteger(page) || page < 0) throw new SkillError('PLEADING_PAGE_INVALID', '字段页码应为从 0 开始的整数');
    state.fieldPages[STEP_NAMES[state.step]] = page;
  }
  state.stage = state.step === STEP_NAMES.length - 1 ? 'ready_to_generate' : 'collecting';
  await store.save(state);
  return {
    ok: true,
    capability: state.capability,
    stage: state.stage,
    sessionId: state.sessionId,
    prompt: state.stage === 'ready_to_generate'
      ? '请向用户展示完整摘要，确认后再生成文书。'
      : `继续处理“${STEP_NAMES[state.step]}”前，只依据当前任务内用户消息、当前任务材料、当前 sessionId 已有值和当前任务更正逐字段匹配；禁止使用全局记忆、其他任务、其他线程、旧案例、旧文书或示例填写字段。只有存在直接、明确、唯一的当前任务依据时才能自动填写。没有匹配的字段必须返回给用户，不得选择“不清楚”、其他兜底值或默认值代填；已可靠完成才直接切换下一页或步骤。`,
    interaction: pleadingInteraction(state),
    data: { summary: pleadingSummary(state.params) }
  };
}

export async function generatePleading({ api, config, store, input }) {
  const state = await store.load(input.sessionId);
  if (!['complaint', 'defense'].includes(state.capability)) {
    throw new SkillError('SESSION_CAPABILITY_MISMATCH', '该任务不是起诉状或答辩状任务');
  }
  if (input.confirmed !== true) {
    return {
      ok: true,
      capability: state.capability,
      stage: 'needs_confirmation',
      sessionId: state.sessionId,
      prompt: '生成前请让用户确认当事人、诉讼请求或答辩意见、事实理由等信息。',
      interaction: pleadingInteraction({ ...state, step: STEP_NAMES.length - 1 }),
      data: { summary: pleadingSummary(state.params) }
    };
  }
  const identity = await store.identity();
  const params = stripInternal(input.params || state.params);
  if (!params || Object.keys(params).length === 0) {
    throw new SkillError('PLEADING_PARAMS_EMPTY', '文书字段为空，请先提取或填写案件信息');
  }
  const recordId = await api.post('/indictment/generateReport', {
    id: input.recordId || null,
    pvId: state.pvId,
    templateId: state.templateId,
    params,
    deviceType: config.deviceType,
    appId: config.appId,
    machineId: identity.machineId,
    code: state.code || null
  }, { timeoutMs: 180_000 });
  state.stage = 'completed';
  state.recordId = recordId;
  state.params = withClientIds(params);
  state.downloadUrl = pleadingDownloadUrl(config, recordId);
  delete state.reportUrl;
  state.links = [capabilityResultLink(state.capability, state.downloadUrl)];
  await store.save(state);
  const resultPolicy = resultGroundingPolicy(state.capability);
  return {
    ok: true,
    capability: state.capability,
    stage: 'completed',
    sessionId: state.sessionId,
    prompt: `文书已经生成。最终摘要和法律依据只能忠实使用已生成文书及文书中已经列明的法规、案例和其他依据；不得调用网页搜索、法律数据库检索、联网查询或其他外部查询工具，不得补充文书中没有的内容。展示摘要后，当前用户可见回复必须原样包含 data.delivery.markdown（${state.links[0].markdown}），不得等待用户再次索取，也不得自行生成任何文书文件。`,
    data: {
      recordId,
      template: state.template,
      summary: pleadingSummary(state.params),
      downloadUrl: state.downloadUrl,
      downloadLinkMarkdown: state.links[0].markdown,
      delivery: resultDelivery(state.links[0])
    },
    resultPolicy,
    links: state.links
  };
}

export function pleadingResume(state, config) {
  const downloadUrl = state.stage === 'completed' && state.recordId
    ? pleadingDownloadUrl(config, state.recordId)
    : null;
  const downloadLink = downloadUrl ? capabilityResultLink(state.capability, downloadUrl) : null;
  const resultPolicy = downloadLink ? resultGroundingPolicy(state.capability) : null;
  return {
    ok: true,
    capability: state.capability,
    stage: state.stage,
    sessionId: state.sessionId,
    prompt: state.stage === 'completed'
      ? `文书已经生成。最终摘要和法律依据只能依据已生成文书及其中已有法规、案例和其他依据，不得搜索、查询或补充外部内容；当前用户可见回复必须原样包含 data.delivery.markdown（${downloadLink.markdown}），不得等待用户再次索取。`
      : `任务已经恢复到“${STEP_NAMES[state.step || 0]}”。只可复用这个 sessionId 中的状态，并只依据当前任务内用户消息、当前任务材料、当前 sessionId 已有值和当前任务更正逐字段匹配；禁止使用全局记忆、其他任务、其他线程、旧案例、旧文书或示例。只有存在直接、明确、唯一的当前任务依据时才能自动填写；没有匹配的字段必须返回给用户，不得选择“不清楚”、其他兜底值或默认值代填。`,
    interaction: state.stage === 'completed' ? null : pleadingInteraction(state),
    data: {
      template: state.template,
      recordId: state.recordId || null,
      summary: pleadingSummary(state.params || {}),
      downloadUrl,
      downloadLinkMarkdown: downloadLink?.markdown || null,
      delivery: downloadLink ? resultDelivery(downloadLink) : null
    },
    resultPolicy,
    links: downloadLink ? [downloadLink] : []
  };
}
