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

  assert.match(fastPath, /Do not pack product \+ role phrases into `companyTypeKeywords`/);
  assert.match(fastPath, /"productKeywords": \["汽车玻璃", "挡风玻璃"\]/);
  assert.match(fastPath, /"companyTypeKeywords": \["进口商"\]/);
  assert.match(fastPath, /`size` and `from` do not reduce ES query rewrite clauses/);

  assert.match(scriptsReadme, /companyTypeKeywords` to one value per API request/);
  assert.match(scriptsReadme, /does not semantically split compound phrases/);
});
