'use strict';

// Local reported answer keys and relevant explanations. No browser or model call.
const path = require('node:path');
const crypto = require('node:crypto');
const { FileAssetCache } = require('./asset-cache.cjs');
const ROOT = path.resolve(__dirname, '..');
const stores = new Map();
const digest = value => crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
const TYPES = new Set(['single', 'multiple', 'judge']);
// `trusted` marks a bank whose owner confirmed every entry: a hit is answered directly, with
// no policy tiering or re-verification. The legacy values stay accepted so older banks and
// any user-supplied bank continue to load.
const POLICIES = new Set(['trusted', 'stable', 'fixed_record', 'dynamic', 'product', 'calculation']);
const SOURCES = new Set(['user_supplied_official_sample', 'user_supplied_platform_report']);
// Only this source can carry judge records whose answer fields contradict each other. A
// `trusted` bank resolves judgment answers when it is built, so it never needs this guard.
const JUDGE_REVIEW_SOURCE = '题库总表.md';

// Retain numbers, negation, operators, formula punctuation and literal whitespace.
function normalize(value) {
  const text = String(value).normalize('NFKC').replace(/[“”]/g, '"').replace(/[‘’]/g, "'").trim();
  return text.split(/("[^"\n]*"|'[^'\n]*')/g).map((part, index) => index % 2 ? part : part.replace(/\s+/g, ' ')).join('');
}
const stemKey = value => normalize(value).replace(/(?:[。.?？])$/, '').trim();
const optionKey = value => normalize(value);
function booleanOption(value) {
  const key = optionKey(value).toLowerCase();
  if (['正确', '对', '是', 'true', '√', '✔'].includes(key)) return true;
  if (['错误', '错', '否', 'false', '×', '✘'].includes(key)) return false;
  return null;
}

function input(question) {
  if (!question || typeof question.question !== 'string' || !question.question.trim()) throw new Error('Supply the complete question stem.');
  if (question.type !== undefined && !TYPES.has(question.type) && question.type !== 'unknown') throw new Error('Use single, multiple, judge or unknown question type.');
  const options = question.options ?? {};
  if (!options || typeof options !== 'object' || Array.isArray(options) || Object.entries(options).some(([label, text]) => !label || typeof text !== 'string' || !text.trim())) throw new Error('Options must map current labels to complete text.');
  return { ...question, options, type: question.type ?? 'unknown' };
}

function optionMapping(entry, question) {
  const current = Object.entries(question.options), old = Object.entries(entry.options);
  if (entry.type === 'judge') {
    if (typeof entry.judge_answer !== 'boolean') return null;
    if (!current.length) return { answer_labels: [], answer_texts: [entry.judge_answer ? '正确' : '错误'], judge_answer: entry.judge_answer };
    if (current.length !== 2 || new Set(current.map(([, text]) => booleanOption(text))).size !== 2 || current.some(([, text]) => booleanOption(text) === null)) return null;
    const [label, text] = current.find(([, text]) => booleanOption(text) === entry.judge_answer);
    return { answer_labels: [label], answer_texts: [text], judge_answer: entry.judge_answer };
  }
  if (current.length !== old.length || !current.length) return null;
  const currentKeys = current.map(([, text]) => optionKey(text)), oldKeys = old.map(([, text]) => optionKey(text));
  if (new Set(currentKeys).size !== current.length || new Set(oldKeys).size !== old.length || oldKeys.some(key => !currentKeys.includes(key))) return null;
  const chosen = new Set(entry.answer_texts.map(optionKey));
  const selections = current.filter(([, text]) => chosen.has(optionKey(text)));
  return { answer_labels: selections.map(([label]) => label), answer_texts: selections.map(([, text]) => text) };
}

function completeMatch(entry, question) {
  if (entry.type !== question.type || stemKey(entry.stem) !== stemKey(question.question)) return false;
  if (entry.type !== 'judge') return Boolean(optionMapping(entry, question));
  const values = Object.values(question.options);
  return !values.length || values.length === 2 && values.every(value => booleanOption(value) !== null) && new Set(values.map(booleanOption)).size === 2;
}

function exactKey(entry) {
  return JSON.stringify([entry.type, stemKey(entry.stem), entry.type === 'judge' ? 'judge' : Object.values(entry.options).map(optionKey).sort()]);
}
function verdictKey(entry) { return entry.type === 'judge' ? String(entry.judge_answer) : JSON.stringify(entry.answer_texts.map(optionKey).sort()); }
function tokens(value) {
  const text = normalize(value).toLowerCase(), result = new Set(text.match(/[a-z0-9]+(?:[-_.][a-z0-9]+)*/g) || []);
  for (const segment of text.match(/[\p{Script=Han}]+/gu) || []) {
    if (segment.length === 1) result.add(segment);
    else for (let i = 0; i < segment.length - 1; i++) result.add(segment.slice(i, i + 2));
  }
  return result;
}

class QuestionBank {
  constructor(root = ROOT) {
    this.root = path.resolve(root);
    this.file = path.join(this.root, 'references', 'question-bank.json');
    this.files = new FileAssetCache();
    this.signature = null;
  }

  refresh() {
    const asset = this.files.load(this.file, { allowedRoot: path.join(this.root, 'references'), json: true });
    if (asset.signature === this.signature) return;
    const bank = asset.value;
    if (bank?.version !== 1 || !Array.isArray(bank.entries) || typeof bank.provenance?.file !== 'string' || !bank.provenance.file ||
      !/^[a-f0-9]{64}$/i.test(bank.provenance.sha256 || '') || bank.entries_sha256 !== digest(bank.entries)) throw new Error('Question bank provenance or content digest is invalid.');
    const ids = new Set(), exact = new Map(), counts = new Map();
    const indexed = bank.entries.map(entry => {
      if (!entry || typeof entry.id !== 'string' || !entry.id || ids.has(entry.id) || typeof entry.base_id !== 'string' || !entry.base_id ||
        typeof entry.stem !== 'string' || !entry.stem.trim() || !TYPES.has(entry.type) || !POLICIES.has(entry.reuse_policy) || !SOURCES.has(entry.source_kind) ||
        !Array.isArray(entry.issues) || entry.issues.some(issue => typeof issue !== 'string') || !Number.isInteger(entry.line_start) || entry.line_start < 1 ||
        !entry.options || typeof entry.options !== 'object' || Array.isArray(entry.options) || Object.values(entry.options).some(text => typeof text !== 'string' || !text.trim()) ||
        !Array.isArray(entry.answer_labels) || !Array.isArray(entry.answer_texts) || typeof entry.explanation !== 'string' || !Array.isArray(entry.urls) || entry.urls.some(url => typeof url !== 'string')) throw new Error('Question bank entry is malformed: ' + (entry?.id || 'unknown'));
      ids.add(entry.id);
      if (new Set(entry.answer_labels).size !== entry.answer_labels.length || entry.answer_labels.some(label => typeof label !== 'string' || !Object.hasOwn(entry.options, label))) throw new Error('Question bank answer refers to absent or repeated options: ' + entry.id);
      const expected = entry.answer_labels.map(label => entry.options[label]);
      if (entry.type !== 'judge' && (!expected.length || expected.length !== entry.answer_texts.length || expected.some((text, i) => text !== entry.answer_texts[i]) || entry.type === 'single' && expected.length !== 1)) throw new Error('Question bank label/text answer mismatch: ' + entry.id);
      if (entry.type === 'judge' && (entry.judge_answer !== null && typeof entry.judge_answer !== 'boolean' ||
        typeof entry.judge_answer === 'boolean' && (entry.answer_texts.length !== 1 || booleanOption(entry.answer_texts[0]) !== entry.judge_answer || expected.some(text => booleanOption(text) !== entry.judge_answer)))) throw new Error('Question bank judgment answer is inconsistent: ' + entry.id);
      const key = exactKey(entry), words = tokens(entry.stem + ' ' + entry.title);
      for (const word of words) counts.set(word, (counts.get(word) || 0) + 1);
      if (!exact.has(key)) exact.set(key, []);
      exact.get(key).push(entry);
      return { entry, key, words };
    });
    const conflicts = new Set();
    for (const entries of exact.values()) if (new Set(entries.map(verdictKey)).size > 1) entries.forEach(entry => conflicts.add(entry.id));
    this.bank = structuredClone(bank); this.indexed = indexed; this.exact = exact; this.conflicts = conflicts;
    this.idf = new Map([...counts].map(([word, count]) => [word, Math.log(1 + indexed.length / count)]));
    this.signature = asset.signature;
  }

  reasons(entry) {
    const reasons = [...entry.issues];
    if (this.conflicts.has(entry.id)) reasons.push('conflicting_answer_keys');
    // A trusted bank resolves judgment answers when it is built, so the missing-boolean guard
    // applies only to the legacy source that is known to carry contradictory judge records.
    const judgeReviewNeeded = entry.source_file === JUDGE_REVIEW_SOURCE;
    if (judgeReviewNeeded && entry.type === 'judge' && typeof entry.judge_answer !== 'boolean') reasons.push('ambiguous_judge_answer');
    if (entry.type !== 'judge' && new Set(Object.values(entry.options).map(optionKey)).size !== Object.keys(entry.options).length) reasons.push('duplicate_option_text');
    // Policy tiers no longer gate a trusted bank; they only stay meaningful for legacy banks.
    if (entry.reuse_policy !== 'trusted') {
      if (entry.reuse_policy === 'dynamic') reasons.push('dynamic_lookup_requires_current_evidence');
      if (entry.reuse_policy === 'product') reasons.push('product_feature_requires_applicable_version_evidence');
    }
    return [...new Set(reasons)];
  }

  source(entry) {
    return { name: '题库总表（用户提供的答案记录）', path: this.bank.provenance.file,
      line: entry.line_start, entry_id: entry.id, kind: entry.source_kind,
      verification: 'user_supplied_reported', original_sha256: this.bank.provenance.sha256,
      bank_path: this.file, referenced_urls: [...entry.urls] };
  }

  preload() {
    try {
      this.refresh();
      const eligible = this.indexed.filter(({ entry }) => !this.reasons(entry).length).length;
      return { total: this.indexed.length, base_questions: new Set(this.bank.entries.map(entry => entry.base_id)).size,
        eligible, review_required: this.indexed.length - eligible, failures: [] };
    } catch (error) { return { total: 0, base_questions: 0, eligible: 0, review_required: 0, failures: [error.message] }; }
  }

  lookup(question, { limit = 3 } = {}) {
    const q = input(question);
    if (!Number.isInteger(limit) || limit < 1 || limit > 5) throw new Error('Use a candidate limit from 1 to 5.');
    try { this.refresh(); }
    catch (error) { return { status: 'needs_verification', reason: '题库不可用：' + error.message, candidates: [] }; }
    const queryWords = tokens(q.question), score = words => {
      let overlap = 0, union = 0;
      for (const word of new Set([...queryWords, ...words])) {
        const weight = this.idf.get(word) || Math.log(1 + this.indexed.length);
        union += weight;
        if (queryWords.has(word) && words.has(word)) overlap += weight;
      }
      return union ? overlap / union : 0;
    };
    const sameStem = this.indexed.filter(({ entry }) => stemKey(entry.stem) === stemKey(q.question));
    const exactMatches = sameStem.filter(({ entry }) => completeMatch(entry, q));
    // Candidate floor. At 0.12 nearly every off-bank question returned a candidate (measured
    // median similarity 0.147), which surfaced unrelated stems as if they were related. 0.3
    // keeps the genuinely overlapping ones and drops that noise. Questions that share a stem
    // take the `sameStem` branch above and never reach this floor, so raising it does not lose
    // them.
    const choices = (exactMatches.length ? exactMatches : sameStem.length ? sameStem : this.indexed.map(item => ({ ...item, similarity: score(item.words) }))
      .filter(item => item.similarity >= 0.3).sort((a, b) => b.similarity - a.similarity || a.entry.id.localeCompare(b.entry.id))).slice(0, limit);
    const candidates = choices.map(({ entry, similarity }) => {
      const isExact = completeMatch(entry, q);
      const details = Object.fromEntries(['id', 'base_id', 'stem', 'type', 'options', 'answer_texts', 'judge_answer',
        'explanation', 'urls', 'source_kind', 'reuse_policy', 'reuse_note', 'issues'].filter(key => key in entry).map(key => [key, entry[key]]));
      return { entry: structuredClone(details), match_kind: isExact ? 'exact' : 'similar',
        similarity: isExact ? 1 : Math.round((similarity ?? score(tokens(entry.stem))) * 1000) / 1000,
        reason: isExact ? '题干、题型及当前全部选项一致；按内容重新映射。' : '仅供借鉴解析；需核对本题对象、条件、否定词和所有选项。',
        needs_review: this.reasons(entry), source: this.source(entry) };
    });
    if (exactMatches.length) {
      const outcomes = new Set(exactMatches.map(({ entry }) => verdictKey(entry)));
      const problems = [...new Set(exactMatches.flatMap(({ entry }) => this.reasons(entry)))];
      if (outcomes.size > 1) problems.push('conflicting_answer_keys');
      if (!problems.length) {
        const entry = exactMatches[0].entry;
        return { status: 'matched', ...optionMapping(entry, q), explanation: entry.explanation,
          basis: 'user_supplied_reported_answer', sources: exactMatches.map(({ entry }) => this.source(entry)), candidates };
      }
      return { status: 'needs_verification', reason: problems.join('; '), candidates };
    }
    return { status: candidates.length ? 'candidates' : 'miss', candidates };
  }
}

function store(root) {
  const key = path.resolve(root);
  if (!stores.has(key)) stores.set(key, new QuestionBank(key));
  return stores.get(key);
}
function lookupQuestionBank(question, { root = ROOT, ...options } = {}) { return store(root).lookup(question, options); }
function preloadQuestionBank({ root = ROOT } = {}) { return store(root).preload(); }
function installQuestionBank(Session, { root = ROOT } = {}) {
  Session.prototype.lookupQuestionBank = function (question, options) { return lookupQuestionBank(question, { ...options, root }); };
  Session.prototype.preloadQuestionBank = function () { return preloadQuestionBank({ root }); };
}

module.exports = { QuestionBank, lookupQuestionBank, preloadQuestionBank, installQuestionBank };
