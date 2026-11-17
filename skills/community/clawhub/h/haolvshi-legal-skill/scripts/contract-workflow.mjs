import { ApiError, SkillError } from './errors.mjs';
import {
  createFileFormData,
  fileDescriptor,
  validateContractFiles
} from './multipart.mjs';
import { buildContractReportHtml } from './report-builder.mjs';
import {
  capabilityResultLink,
  contractReportUrl,
  resultDelivery,
  resultGroundingPolicy
} from './report-links.mjs';
import { withInteractionRendering } from './interaction-normalizer.mjs';

function riskSummary(riskPoints = []) {
  const levels = {};
  for (const risk of riskPoints) {
    const level = risk.riskPointLevel || '未分级';
    levels[level] = (levels[level] || 0) + 1;
  }
  return { total: riskPoints.length, levels };
}

async function finalizeContract({ api, config, store, state, result, saveHtml = true }) {
  const riskPoints = Array.isArray(result?.riskPoints) ? result.riskPoints : [];
  const recordId = result?.recordId;
  if (!recordId) throw new SkillError('CONTRACT_RESULT_INVALID', '合同审核结果缺少记录编号');

  const html = result.reportHtml || buildContractReportHtml({
    riskPoints,
    standing: state.contractualStanding
  });
  const warnings = [];
  if (saveHtml && !result.reportHtml) {
    try {
      await api.post('/contract/saveAuditHtml', {
        recordId,
        appId: config.appId,
        html: Buffer.from(html, 'utf8').toString('base64'),
        cover: null
      });
    } catch (error) {
      warnings.push(`审核结果已取得，但服务端报告保存失败：${error.message}`);
    }
  }

  state.stage = 'completed';
  state.recordId = recordId;
  state.auditResult = { ...result, riskPoints };
  state.reportUrl = contractReportUrl(config, state.pvId);
  state.links = [capabilityResultLink('contract', state.reportUrl)];
  await store.save(state);
  const resultPolicy = resultGroundingPolicy('contract');

  return {
    ok: true,
    capability: 'contract',
    stage: 'completed',
    sessionId: state.sessionId,
    prompt: `合同审核已经完成。最终总结、风险结论、修改建议和法律依据只能忠实使用 data.riskPoints 及生成报告中已有内容；不得调用网页搜索、法律数据库检索、联网查询或其他外部查询工具，不得补充报告中没有的法规、案例或观点。按风险等级展示重点风险和修改建议后，当前用户可见回复必须原样包含 data.delivery.markdown（${state.links[0].markdown}），并立即用宿主内置浏览器打开 data.delivery.url（不得调起外部浏览器）；禁止自行生成 HTML、Markdown、PDF 等任何报告文件；若宿主没有内置浏览器，仍须在同一轮回复中发送该链接，不得等待用户再次索取。`,
    data: {
      pvId: state.pvId,
      recordId,
      contractualStanding: state.contractualStanding,
      summary: riskSummary(riskPoints),
      riskPoints,
      reportUrl: state.reportUrl,
      reportLinkMarkdown: state.links[0].markdown,
      delivery: resultDelivery(state.links[0])
    },
    resultPolicy,
    links: state.links,
    warnings
  };
}

export async function reviewContract({ api, config, store, input }) {
  const standing = Number(input.contractualStanding);
  if (![1, 2].includes(standing)) {
    return {
      ok: true,
      capability: 'contract',
      stage: 'needs_input',
      prompt: '开始审核前，只检查当前任务/当前线程内用户是否已经明确本次合同的审核立场；禁止从全局记忆、长期记忆、用户画像、其他任务、其他线程、旧合同、旧报告或示例推断甲乙方。当前任务未说明时，请确认“您是甲方还是乙方？”。必须调用当前会话兼容的原生单选或表单组件，并核对原生界面实际显示的选项数量与 interaction.optionManifest[].expectedOptionCount 完全一致；少一个选项也不得接受答案。选择器容量不足时改用能完整展示编号选项的原生表单或输入组件；只有确认没有任何兼容原生组件后，才允许完整展示 interaction.textFallback 并接受 1 或 2。合同文件也只能使用当前任务中用户提供的文件。',
      interaction: withInteractionRendering({
        type: 'question',
        title: '请选择合同审核立场',
        fields: [{
          key: 'contractualStanding',
          label: '我方合同立场',
          type: 'single_select',
          required: true,
          value: '',
          options: [{ value: '1', label: '甲方' }, { value: '2', label: '乙方' }]
        }],
        submitLabel: '开始审核'
      })
    };
  }

  const paths = input.filePaths || (input.filePath ? [input.filePath] : []);
  const descriptors = await Promise.all(paths.map(fileDescriptor));
  const { doc } = validateContractFiles(descriptors);

  const identity = await store.identity();
  const state = await store.create({
    capability: 'contract',
    stage: 'uploading',
    contractualStanding: standing,
    thinking: Boolean(input.thinking),
    doc,
    files: descriptors.map(({ path, name, extension, size }) => ({ path, name, extension, size }))
  });

  try {
    const fileIds = [];
    for (const descriptor of descriptors) {
      const form = await createFileFormData('file', descriptor);
      fileIds.push(await api.upload('/file/upload', form));
    }
    state.fileIds = fileIds;
    state.stage = 'creating';
    await store.save(state);

    state.pvId = await api.post('/contract/create', {
      appId: config.appId,
      deviceType: config.deviceType,
      userId: identity.userId
    });
    state.stage = 'audit_started';
    await store.save(state);

    const result = await api.post('/contract/audit', {
      pvId: state.pvId,
      fileIds,
      contractualStanding: standing,
      thinking: Boolean(input.thinking),
      doc
    }, { timeoutMs: config.auditTimeoutMs });
    return finalizeContract({ api, config, store, state, result });
  } catch (error) {
    const uncertain = state.stage === 'audit_started'
      && error instanceof ApiError
      && ['REQUEST_TIMEOUT', 'NETWORK_ERROR', 'HTTP_ERROR'].includes(error.code);
    state.stage = uncertain ? 'audit_unknown' : 'failed';
    state.lastError = { code: error.code || 'UNEXPECTED_ERROR', message: error.message };
    await store.save(state);
    throw new SkillError(error.code || 'CONTRACT_REVIEW_FAILED', error.message, {
      retryable: uncertain || Boolean(error.retryable),
      cause: error,
      details: { sessionId: state.sessionId, pvId: state.pvId || null, canResume: uncertain }
    });
  }
}

export async function resumeContract({ api, config, store, state }) {
  if (state.stage === 'completed' && state.auditResult) {
    return finalizeContract({ api, config, store, state, result: state.auditResult, saveHtml: false });
  }
  if (!state.pvId) {
    return {
      ok: true,
      capability: 'contract',
      stage: state.stage,
      sessionId: state.sessionId,
      prompt: '任务尚未进入审核阶段，请重新提交合同审核。',
      data: { lastError: state.lastError || null }
    };
  }

  const result = await api.get(`/contract/getAuditDetail/${encodeURIComponent(state.pvId)}`);
  if (!result?.recordId) {
    return {
      ok: true,
      capability: 'contract',
      stage: 'audit_unknown',
      sessionId: state.sessionId,
      prompt: '本次恢复查询尚未取得审核结果。请让用户确认后重新发起审核；技能不会自动轮询。',
      data: { pvId: state.pvId, checkedOnce: true }
    };
  }
  return finalizeContract({ api, config, store, state, result });
}
