const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const SKILL_DIR = path.resolve(__dirname, '..', '..');

function readSkillFile(relativePath) {
  return fs.readFileSync(path.join(SKILL_DIR, relativePath), 'utf8');
}

test('hot path relies on output-contracts for script-owned field handling', () => {
  const skill = readSkillFile('SKILL.md');

  assert.match(skill, /Use compact wrappers for normal work/);
  assert.match(skill, /selection_handle/);
  assert.match(skill, /prepare paid unlock plans/);
  assert.doesNotMatch(skill, /Do not print raw API JSON, full profiles, full local state, full email bodies, internal IDs, unlock keys, domains, websites, homepages, URLs, or link fields/);
  assert.doesNotMatch(skill, /Do not show wrapper metadata such as `batch_id`, `raw_path`, `private_mapping_saved`, or verbose `output_budget`/);
});

test('non-owner references avoid duplicating script-owned privacy field lists', () => {
  const fastPath = readSkillFile('references/search-fast-path.md');
  const paidActions = readSkillFile('references/paid-actions.md');
  const outputContracts = readSkillFile('references/output-contracts.md');

  assert.match(outputContracts, /Field Ownership/);
  assert.match(outputContracts, /Do not replace deterministic script ownership/);

  assert.doesNotMatch(fastPath, /Do not display domains, URLs, internal IDs, raw paths, batch IDs, raw API JSON, or private mapping status/);
  assert.doesNotMatch(paidActions, /Do not print domains, company hash IDs, raw paths, batch IDs, or raw payloads/);
  assert.doesNotMatch(paidActions, /Do not print internal contact IDs/);
});

test('structured output ownership covers presentation shape and cardinality', () => {
  const skill = readSkillFile('SKILL.md');
  const fastPath = readSkillFile('references/search-fast-path.md');
  const searchStrategy = readSkillFile('references/search-strategy.md');
  const expansion = readSkillFile('references/expansion-playbook.md');
  const outputContracts = readSkillFile('references/output-contracts.md');

  assert.match(outputContracts, /structured presentation/);
  assert.match(outputContracts, /fields, order, row set, cardinality, and counts/);
  assert.match(outputContracts, /this display rule applies to every mode that runs a new free company search/);
  assert.match(skill, /preserving script-owned output structure/);
  assert.match(skill, /Do not rebuild, filter, reorder, rename, truncate, or summarize script-owned tables or details into a new structured format/);
  assert.match(fastPath, /Use `output-contracts\.md` as the single owner/);
  assert.match(searchStrategy, /using `output-contracts\.md`/);
  assert.match(expansion, /using `output-contracts\.md`/);
  assert.doesNotMatch(fastPath, /Do not filter `display_table_markdown` rows by model judgment/);
});

test('analysis modes separate recommendations from script-owned result display', () => {
  const resultReview = readSkillFile('references/result-review.md');
  const searchStrategy = readSkillFile('references/search-strategy.md');
  const expansion = readSkillFile('references/expansion-playbook.md');

  assert.match(resultReview, /Analysis groups are recommendations over the displayed batch/);
  assert.match(resultReview, /must not replace, filter, renumber, or restate the script-owned result table/);
  assert.match(searchStrategy, /Local priority rules guide analysis after the company discovery output contract/);
  assert.match(expansion, /show the company discovery result using `output-contracts\.md`/);
});

test('L0 presentation preserves lightweight recommendation guidance after the full table', () => {
  const skill = readSkillFile('SKILL.md');
  const fastPath = readSkillFile('references/search-fast-path.md');
  const resultReview = readSkillFile('references/result-review.md');

  assert.match(skill, /After each free-search table, add brief priority guidance/);
  assert.match(fastPath, /After the table and any lightweight recommendation overlay/);
  assert.match(outputContractsText(), /recommendation groups and coaching are analysis overlays after the table/);
  assert.match(resultReview, /Use this same overlay wording when L0 already showed the full table/);
});

test('paid action references use script-provided structured outputs', () => {
  const paidActions = readSkillFile('references/paid-actions.md');
  const outputContracts = readSkillFile('references/output-contracts.md');

  assert.match(paidActions, /script-rendered `unlock_details_markdown` exactly as the chat display/);
  assert.match(paidActions, /script-provided contact rows/);
  assert.match(paidActions, /script-provided task IDs, counts, status, and next status-check command/);
  assert.match(outputContracts, /script-rendered `unlock_details_markdown` for chat display/);
  assert.match(outputContracts, /`company_details` compatibility data/);
  assert.match(outputContracts, /details_markdown_artifact/);
  assert.match(outputContracts, /DETAILS_MARKDOWN_PRECHECK_FAILED/);
  assert.match(outputContracts, /authorize_artifact_dir/);
  assert.match(outputContracts, /the model does not rebuild it from `company_details`/);
  assert.match(outputContracts, /model for prose around them/);
});

test('paid unlock path uses prepared plans instead of latest row execution', () => {
  const skill = readSkillFile('SKILL.md');
  const paidActions = readSkillFile('references/paid-actions.md');
  const outputContracts = readSkillFile('references/output-contracts.md');

  assert.match(skill, /prepare-unlock-plan\.js --selection-handle/);
  assert.match(skill, /unlock-companies\.js --plan/);
  assert.match(skill, /--artifact-dir '<agent-visible-output-dir>'/);
  assert.match(paidActions, /Preparing an unlock plan is not confirmation/);
  assert.match(paidActions, /no credit was charged because no details-document path was writable/);
  assert.match(outputContracts, /`unlock_plan_id` \| Scripts\. \| Under `debug_metadata` only/);
  assert.doesNotMatch(skill, /unlock-companies\.js --batch latest/);
  assert.doesNotMatch(paidActions, /unlock-companies\.js --batch latest/);
});

test('processed unlock target sets and post-unlock outreach guidance are script-owned', () => {
  const skill = readSkillFile('SKILL.md');
  const paidActions = readSkillFile('references/paid-actions.md');
  const outputContracts = readSkillFile('references/output-contracts.md');
  const scriptsReadme = readSkillFile('scripts/README.md');

  assert.match(skill, /selection-set-file/);
  assert.match(paidActions, /final unlock target set/);
  assert.match(paidActions, /If the user changes the final target set before confirmation/);
  assert.match(outputContracts, /`next_action`: `draft_outreach`/);
  assert.match(outputContracts, /Agent-provided writable artifact directories/);
  assert.match(outputContracts, /Do not present paid `contacts\/search` as the normal next step after selected-company unlock/);
  assert.match(scriptsReadme, /processed target set/);
  assert.match(scriptsReadme, /OKKIGO_ARTIFACT_DIR/);
  assert.doesNotMatch(outputContracts, /attempted_count/);
  assert.doesNotMatch(outputContracts, /not_attempted_count/);
});

function outputContractsText() {
  return readSkillFile('references/output-contracts.md');
}
