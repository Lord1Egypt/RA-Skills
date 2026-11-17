function trimTrailingSlash(value) {
  return String(value || '').replace(/\/+$/, '');
}

function normalizeRouteBase(value) {
  const route = String(value || '').trim();
  if (!route || route === '/') return '';
  return `/${route.replace(/^\/+|\/+$/g, '')}`;
}

function frontendBase(config) {
  const siteBase = trimTrailingSlash(config.siteBase);
  const routeBase = normalizeRouteBase(config.siteRouteBase);
  return routeBase && !siteBase.endsWith(routeBase)
    ? `${siteBase}${routeBase}`
    : siteBase;
}

function queryString(values) {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) {
    if (value !== undefined && value !== null && value !== '') query.set(key, String(value));
  }
  return query.toString();
}

export function questionReportUrl(config, recordId) {
  const query = queryString({ appId: config.appId, device_type: config.deviceType });
  return `${frontendBase(config)}/g/r/${encodeURIComponent(recordId)}?${query}`;
}

export function contractReportUrl(config, pvId) {
  const query = queryString({ id: pvId, appId: config.appId, device_type: config.deviceType });
  return `${frontendBase(config)}/contract_review/detail?${query}`;
}

export function pleadingDownloadUrl(config, recordId, extension = 'docx') {
  const query = queryString({ appId: config.appId, deviceType: config.deviceType });
  const safeExtension = String(extension || 'docx').replace(/^\.+/, '').toLowerCase();
  return `${trimTrailingSlash(config.apiBase)}/indictment/download/${encodeURIComponent(recordId)}.${encodeURIComponent(safeExtension)}?${query}`;
}

export const RESULT_LINK_LABELS = Object.freeze({
  consultation: '法律咨询报告',
  calculator: '法律计算报告',
  contract: '合同审核报告',
  complaint: '起诉状（Word）',
  defense: '答辩状（Word）'
});

export const RESULT_GROUNDING_POLICY = Object.freeze({
  sourceOfTruth: 'generated_result_only',
  allowedSources: Object.freeze([
    'generated_report_or_document_content',
    'laws_cases_and_authorities_embedded_in_that_result'
  ]),
  reportContentControls: true,
  externalSearchAllowed: false,
  externalLookupAllowed: false,
  supplementalLegalResearchAllowed: false,
  addAuthoritiesNotInResultAllowed: false
});

export function resultGroundingPolicy(capability) {
  if (!RESULT_LINK_LABELS[capability]) throw new TypeError(`未知结果能力：${capability}`);
  return {
    ...RESULT_GROUNDING_POLICY,
    allowedSources: [...RESULT_GROUNDING_POLICY.allowedSources],
    capability,
    instruction: '最终总结、结论和法律依据只能来自已生成的报告或文书，以及其中已经列明的法规、案例和其他依据；不得再搜索、查询或补充外部内容。'
  };
}

function markdownLink(label, url) {
  const safeLabel = String(label || '').replace(/([\[\]])/g, '\\$1');
  return `[${safeLabel}](${String(url || '')})`;
}

function passiveLink(type, url, label, extra = {}) {
  return {
    type,
    label,
    url,
    markdown: markdownLink(label, url),
    autoOpen: false,
    openBehavior: 'user_click_only',
    ...extra
  };
}

export function onlineReportLink(url, label = '在线报告') {
  return passiveLink('online_report', url, label, {
    autoOpen: true,
    openBehavior: 'open_immediately'
  });
}

export function downloadFileLink(url, label = '下载文件', format = 'docx') {
  return passiveLink('download', url, label, { format });
}

export function resultDelivery(link) {
  return {
    markdown: link.markdown,
    url: link.url,
    mustDisplayInFinalResponse: true,
    autoOpen: Boolean(link.autoOpen),
    openBehavior: link.openBehavior,
    // 报告正文由服务端渲染在 url 上。宿主自己再写一份 HTML/Markdown/PDF
    // 既慢又会和线上报告不一致，必须明确禁止。
    forbidGeneratingReportFile: true,
    openWith: link.autoOpen ? 'host_internal_browser_only' : 'user_click_only',
    instruction: link.autoOpen
      ? '报告已生成：当前用户可见回复必须原样包含 markdown；随后立即用宿主内置的浏览器或页面预览能力打开 url，不得调起系统默认浏览器或任何外部应用。禁止自行生成 HTML、Markdown、PDF 或任何报告文件，报告正文只在该链接上。若宿主没有内置浏览器，仍须在同一轮回复中发送 markdown，不得等待用户再次索取链接。'
      : '文书已生成：当前用户可见回复必须原样包含 markdown，不得等待用户再次索取链接。禁止自行生成任何文书文件，用户点击链接下载即可。'
  };
}

export function capabilityResultLink(capability, url) {
  const label = RESULT_LINK_LABELS[capability];
  if (!label) throw new TypeError(`未知结果链接能力：${capability}`);
  return ['complaint', 'defense'].includes(capability)
    ? downloadFileLink(url, label)
    : onlineReportLink(url, label);
}
