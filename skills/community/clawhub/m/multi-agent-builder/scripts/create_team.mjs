#!/usr/bin/env node
import { spawnSync } from 'child_process';

const args = process.argv.slice(2);
const get = (k, d='') => {
  const i = args.indexOf(`--${k}`);
  return i>=0 ? (args[i+1] ?? d) : d;
};
const team = get('team');
const roles = get('roles');
const accountId = get('account-id','');
const locale = get('locale','zh-CN');
const channel = get('channel','telegram');
const model = get('model','openai-codex/gpt-5.3-codex');
if (!team || !roles) {
  console.error('missing --team and/or --roles');
  process.exit(2);
}

const run = (file, extra=[]) => {
  const r = spawnSync('node', [new URL(file, import.meta.url).pathname, ...extra], { stdio: 'pipe', encoding: 'utf8' });
  if (r.status !== 0) {
    console.error(r.stdout || '');
    console.error(r.stderr || '');
    process.exit(r.status || 1);
  }
  return r.stdout.trim();
};

const common = ['--team', team, '--roles', roles, '--channel', channel, '--locale', locale, '--model', model, ...(accountId?['--account-id',accountId]:[])];
const m = run('./materialize_team.mjs', common);
const v = run('./validate_team.mjs', common);
const vr = JSON.parse(v);
if (vr.status !== 'ready') {
  console.log(JSON.stringify({ ok:false, stage:'validate', result: vr }, null, 2));
  process.exit(3);
}
const rep = run('./emit_report.mjs', common);
console.log(JSON.stringify({ ok:true, materialize: JSON.parse(m), validate: vr, report: JSON.parse(rep) }, null, 2));
