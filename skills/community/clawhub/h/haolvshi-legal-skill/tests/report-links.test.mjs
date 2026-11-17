import assert from 'node:assert/strict';
import test from 'node:test';
import { DEFAULT_CONFIG } from '../scripts/config.mjs';
import {
  capabilityResultLink,
  contractReportUrl,
  pleadingDownloadUrl,
  questionReportUrl,
  RESULT_GROUNDING_POLICY,
  RESULT_LINK_LABELS,
  resultDelivery,
  resultGroundingPolicy
} from '../scripts/report-links.mjs';

const config = {
  apiBase: 'https://front.example.test/api/speed-front/',
  siteBase: 'https://legal.example.test/',
  siteRouteBase: '',
  appId: '应用 编号',
  deviceType: 1
};

test('咨询、合同在线地址和法律文书下载地址与实际路由一致', () => {
  assert.equal(
    questionReportUrl(config, '问答/记录'),
    'https://legal.example.test/g/r/%E9%97%AE%E7%AD%94%2F%E8%AE%B0%E5%BD%95?appId=%E5%BA%94%E7%94%A8+%E7%BC%96%E5%8F%B7&device_type=1'
  );
  assert.equal(
    contractReportUrl(config, '合同 访问'),
    'https://legal.example.test/contract_review/detail?id=%E5%90%88%E5%90%8C+%E8%AE%BF%E9%97%AE&appId=%E5%BA%94%E7%94%A8+%E7%BC%96%E5%8F%B7&device_type=1'
  );
  assert.equal(
    pleadingDownloadUrl(config, '文书/记录'),
    'https://front.example.test/api/speed-front/indictment/download/%E6%96%87%E4%B9%A6%2F%E8%AE%B0%E5%BD%95.docx?appId=%E5%BA%94%E7%94%A8+%E7%BC%96%E5%8F%B7&deviceType=1'
  );
});

test('最终总结只允许依据生成结果及其中已有法规且禁止外部检索', () => {
  assert.equal(RESULT_GROUNDING_POLICY.sourceOfTruth, 'generated_result_only');
  assert.equal(RESULT_GROUNDING_POLICY.reportContentControls, true);
  assert.equal(RESULT_GROUNDING_POLICY.externalSearchAllowed, false);
  assert.equal(RESULT_GROUNDING_POLICY.externalLookupAllowed, false);
  assert.equal(RESULT_GROUNDING_POLICY.supplementalLegalResearchAllowed, false);
  assert.equal(RESULT_GROUNDING_POLICY.addAuthoritiesNotInResultAllowed, false);

  const policy = resultGroundingPolicy('consultation');
  assert.equal(policy.capability, 'consultation');
  assert.deepEqual(policy.allowedSources, [
    'generated_report_or_document_content',
    'laws_cases_and_authorities_embedded_in_that_result'
  ]);
  assert.match(policy.instruction, /不得再搜索、查询或补充外部内容/);
});

test('空前端路由不会额外拼接目录', () => {
  assert.match(questionReportUrl(config, '1'), /^https:\/\/legal\.example\.test\/g\/r\/1/);
});

test('默认在线报告站点使用新的技能域名', () => {
  assert.equal(DEFAULT_CONFIG.siteBase, 'https://skill.ai.lvpin100.com');
  assert.match(
    questionReportUrl(DEFAULT_CONFIG, 'record-1'),
    /^https:\/\/skill\.ai\.lvpin100\.com\/g\/r\/record-1/
  );
});

test('五类结果链接稳定交付，在线报告自动打开而文书保持下载链接', () => {
  const expected = {
    consultation: '法律咨询报告',
    calculator: '法律计算报告',
    contract: '合同审核报告',
    complaint: '起诉状（Word）',
    defense: '答辩状（Word）'
  };

  assert.deepEqual(RESULT_LINK_LABELS, expected);
  for (const [capability, label] of Object.entries(expected)) {
    const link = capabilityResultLink(capability, `https://example.test/${capability}`);
    assert.equal(link.label, label);
    assert.equal(link.markdown, `[${label}](https://example.test/${capability})`);
    assert.equal(link.autoOpen, !['complaint', 'defense'].includes(capability));
    assert.equal(link.openBehavior, ['complaint', 'defense'].includes(capability) ? 'user_click_only' : 'open_immediately');
    assert.equal(link.type, ['complaint', 'defense'].includes(capability) ? 'download' : 'online_report');
    const delivery = resultDelivery(link);
    assert.equal(delivery.markdown, link.markdown);
    assert.equal(delivery.url, link.url);
    assert.equal(delivery.mustDisplayInFinalResponse, true);
    assert.equal(delivery.autoOpen, link.autoOpen);
  }
});
