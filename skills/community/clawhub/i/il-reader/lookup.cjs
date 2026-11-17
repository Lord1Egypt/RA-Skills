'use strict';

/*
 * il-reader bank lookup for WorkBuddy.
 *
 *   node lookup.cjs <question.json>        # answer one question from the bank
 *   node lookup.cjs --status               # bank counts
 *
 * Only the local question bank is involved: no browser, no network. Paths are resolved from
 * this file's own location, so the caller's working directory never matters.
 *
 * Question JSON: { "id": "...", "type": "single|multiple|judge",
 *                  "question": "题干", "options": { "A": "...", "B": "..." } }
 *
 * Prints one JSON object. Exit code 0 on success, 2 when the bank itself is unusable, 1 for
 * usage or input errors.
 */

const fs = require('node:fs');
const path = require('node:path');
const { lookupQuestionBank, preloadQuestionBank } = require('./lib/question-bank.cjs');

const SKILL_DIR = __dirname;

function emit(value, code = 0) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\n');
  process.exitCode = code;
}

function readQuestion(file) {
  const text = fs.readFileSync(path.resolve(file), 'utf8').replace(/^\uFEFF/, '');
  const question = JSON.parse(text);
  if (!question || typeof question !== 'object' || Array.isArray(question)) throw new Error('Question JSON must be an object.');
  if (typeof question.id !== 'string' || !question.id.trim()) throw new Error('Question needs a nonempty string id.');
  if (typeof question.question !== 'string' || !question.question.trim()) throw new Error('Question needs a nonempty string question.');
  if (!['single', 'multiple', 'judge'].includes(question.type)) throw new Error('Question type must be single, multiple or judge.');
  const options = question.options || {};
  if (typeof options !== 'object' || Array.isArray(options) || !Object.keys(options).length) throw new Error('Question needs at least one option.');
  return question;
}

function main() {
  const arg = process.argv[2];
  if (!arg || arg === '--help' || arg === '-h') {
    process.stdout.write([
      'usage: node lookup.cjs <question.json>',
      '       node lookup.cjs --status',
      '',
      'question JSON: {"id":"q1","type":"single","question":"题干","options":{"A":"…","B":"…"}}',
      '',
    ].join('\n'));
    process.exitCode = arg ? 0 : 1;
    return;
  }

  if (arg === '--status') {
    const status = preloadQuestionBank({ root: SKILL_DIR });
    emit({ ok: !status.failures.length, result: status }, status.failures.length ? 2 : 0);
    return;
  }

  let question;
  try {
    question = readQuestion(arg);
  } catch (error) {
    emit({ ok: false, error: 'Invalid question file: ' + error.message });
    process.exitCode = 1;
    return;
  }

  const result = lookupQuestionBank(question, { root: SKILL_DIR, limit: 3 });
  if (result.status === 'needs_verification' && result.reason && /题库不可用/.test(result.reason)) {
    emit({ ok: false, error: result.reason }, 2);
    return;
  }
  emit({ ok: true, result });
}

main();
