const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const SKILL_DIR = path.resolve(__dirname, '..', '..');

function readSkillFile(relativePath) {
  return fs.readFileSync(path.join(SKILL_DIR, relativePath), 'utf8');
}

test('ordinary OKKI prospecting cannot fall back to public web search', () => {
  const skill = readSkillFile('SKILL.md');
  const fastPath = readSkillFile('references/search-fast-path.md');
  const strategy = readSkillFile('references/search-strategy.md');

  assert.match(skill, /OKKI Data Source Boundary/);
  assert.match(skill, /do not use public web search/i);
  assert.match(skill, /API is busy/i);
  assert.match(skill, /not a fallback/i);

  assert.match(fastPath, /No Web Fallback/i);
  assert.match(fastPath, /system busy/i);
  assert.match(fastPath, /do not switch to public web search/i);

  assert.match(strategy, /External research is not a recovery path/i);
  assert.match(strategy, /explicitly asks for independent external research/i);
});

test('web research add-on is explicit and lower priority than OKKI discovery', () => {
  const skill = readSkillFile('SKILL.md');

  assert.match(
    skill,
    /WEB_RESEARCH_ADDON`\s*\|\s*User explicitly asks for independent external\/latest\/source-backed research/
  );
  assert.match(skill, /not for ordinary find companies, buyers, importers, distributors, customers, target accounts, or prospects/i);
  assert.match(skill, /Web Research Add-on is never an OKKI failure fallback/i);
});

test('company search guidance separates product terms from buyer roles to avoid ES rewrite overload', () => {
  const skill = readSkillFile('SKILL.md');
  const fastPath = readSkillFile('references/search-fast-path.md');
  const scriptsReadme = readSkillFile('scripts/README.md');

  assert.match(skill, /Put product or offer terms in `productKeywords`/);
  assert.match(skill, /put buyer roles in `companyTypeKeywords`/);
  assert.match(skill, /Do not combine product and buyer-role terms inside `companyTypeKeywords`/);
  assert.match(skill, /工业自动化系统集成商/);
  assert.match(skill, /"industryKeywords": \["工业自动化系统"\]/);
  assert.match(skill, /"companyTypeKeywords": \["集成商"\]/);
  assert.match(skill, /Target-side first still applies/);

  assert.match(fastPath, /Do not pack product \+ role phrases into `companyTypeKeywords`/);
  assert.match(fastPath, /"companyTypeKeywords": \["控制系统工程商"\]/);
  assert.match(fastPath, /"productKeywords": \["控制系统"\]/);
  assert.match(fastPath, /"companyTypeKeywords": \["工程商"\]/);
  assert.match(fastPath, /target-buyer profile keywords/i);
  assert.match(fastPath, /"productKeywords": \["汽车玻璃", "挡风玻璃"\]/);
  assert.match(fastPath, /"companyTypeKeywords": \["进口商"\]/);
  assert.match(fastPath, /`size` and `from` do not reduce ES query rewrite clauses/);

  assert.match(scriptsReadme, /companyTypeKeywords` to one value per API request/);
  assert.match(scriptsReadme, /reject compound phrases such as `汽车玻璃供应商` before API calls/);
  assert.match(scriptsReadme, /target-buyer `productKeywords` or `industryKeywords` plus pure role `companyTypeKeywords`/);
});

test('companyHashId guidance forbids using free-search IDs for profile lookups', () => {
  const skill = readSkillFile('SKILL.md');
  const paidActions = readSkillFile('references/paid-actions.md');
  const outputContracts = readSkillFile('references/output-contracts.md');
  const apiReference = readSkillFile('references/api-reference.md');
  const scriptsReadme = readSkillFile('scripts/README.md');

  for (const content of [skill, paidActions, outputContracts, apiReference, scriptsReadme]) {
    assert.match(content, /companyHashId/);
    assert.match(content, /\/companies\/unlock/);
    assert.match(content, /free[- ]search ID/i);
  }

  assert.match(apiReference, /Do not use free[- ]search `id`/i);
  assert.match(apiReference, /The only valid source for `companyHashId` is the `\/companies\/unlock` response/i);
  assert.doesNotMatch(apiReference, /companyHashId[^.\n]*来自搜索结果/i);
});
