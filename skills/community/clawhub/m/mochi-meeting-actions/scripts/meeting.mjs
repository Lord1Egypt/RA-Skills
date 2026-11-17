import path from 'node:path';
import { createHash } from 'node:crypto';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';
import { readText, newOutput, writeNew, md, csvCell } from './io.mjs';

const digest = text => createHash('sha256').update(text,'utf8').digest('hex');
function keys(value, allowed) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(key => !allowed.includes(key))) throw new Error('Unexpected JSON object/field.');
}
function text(value, name, max = 800) { if (typeof value !== 'string' || !value.trim() || value.length > max || /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value)) throw new Error('Invalid '+name+'.'); return value; }
export function evidence(source) {
  source = source.replace(/\r\n?/g,'\n');
  if (!source.trim() || Buffer.byteLength(source,'utf8') > 1048576) throw new Error('Provide nonempty UTF-8 text up to1 MiB.');
  const lines = source.split('\n').map((value,index) => ({ id:'L'+String(index+1).padStart(4,'0'), text:value }));
  if (lines.length > 5000 || lines.some(line => line.text.length > 4000)) throw new Error('Limit is5000 lines and4000 characters per line.');
  return { schemaVersion:1, sourceSha256:digest(source), sourceText:source, lines };
}
function isoDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(value+'T00:00:00Z'); return Number.isFinite(date.valueOf()) && date.toISOString().slice(0,10) === value;
}
export function validate(rawEvidence, draft) {
  keys(rawEvidence,['schemaVersion','sourceSha256','sourceText','lines']);
  const rebuilt = evidence(text(rawEvidence.sourceText,'sourceText',1048576));
  if (rawEvidence.schemaVersion !== 1 || rawEvidence.sourceSha256 !== rebuilt.sourceSha256 || JSON.stringify(rawEvidence.lines) !== JSON.stringify(rebuilt.lines)) throw new Error('Evidence was changed or has an invalid hash/index.');
  keys(draft,['schemaVersion','sourceSha256','language','title','summary','decisions','actions','openQuestions']);
  if (draft.schemaVersion !== 1 || draft.sourceSha256 !== rebuilt.sourceSha256 || !['zh-CN','en'].includes(draft.language)) throw new Error('Draft source hash/schema/language mismatch.');
  text(draft.title,'title',160);
  const index = new Map(rebuilt.lines.map((line,n) => [line.id,{...line,index:n}]));
  function cited(item, action) {
    keys(item,action ? ['task','owner','due','quote','evidence'] : ['text','quote','evidence']);
    text(item[action ? 'task':'text'],action?'task':'text'); text(item.quote,'quote',2000);
    if (!Array.isArray(item.evidence) || item.evidence.length < 1 || item.evidence.length > 12 || new Set(item.evidence).size !== item.evidence.length || item.evidence.some(id => !index.has(id))) throw new Error('Each item needs existing, unique evidence line IDs.');
    const selected = item.evidence.map(id => index.get(id));
    if (selected.some((line,n) => n && line.index !== selected[n-1].index+1)) throw new Error('Quoted evidence must use consecutive lines in source order.');
    if (!selected.map(line => line.text).join('\n').includes(item.quote)) throw new Error('Quote is not an exact excerpt of the cited lines.');
    if (action) {
      if (item.owner !== null && (typeof item.owner !== 'string' || !item.owner.trim() || item.owner.length > 120 || !item.quote.includes(item.owner))) throw new Error('Owner must be null or explicitly present in the quoted evidence.');
      if (item.due !== null && (!isoDate(item.due) || !item.quote.includes(item.due))) throw new Error('Due date must be null or a valid explicit YYYY-MM-DD date present in the quote.');
    }
    return item;
  }
  for (const key of ['summary','decisions','actions','openQuestions']) {
    if (!Array.isArray(draft[key]) || draft[key].length > (key === 'actions'?50:30)) throw new Error('Missing/oversized '+key+' array.');
    draft[key].forEach(item => cited(item,key === 'actions'));
  }
  return draft;
}
export function markdown(draft) {
  const en = draft.language === 'en', unknown = en?'Unknown':'未知';
  const lines = ['# '+md(draft.title),'',en?'Evidence-checked local draft. Review whether the quotations actually support each interpretation.':'本地证据校验后的草稿。请复核原文是否真正支持每项解释。',''];
  const quote = item => '> '+md(item.quote).replace(/\n/g,'\n> ')+' ['+item.evidence.join(', ')+']';
  for (const [key,label] of [['summary',en?'Summary':'摘要'],['decisions',en?'Decisions':'决定'],['actions',en?'Action items':'行动清单'],['openQuestions',en?'Open questions':'待确认问题']]) {
    lines.push('## '+label,'');
    if (!draft[key].length) lines.push(en?'None evidenced.':'没有足够证据的项目。','');
    draft[key].forEach(item => { lines.push('- '+md(item.task ?? item.text)); if (key === 'actions') lines.push('  '+(en?'Owner':'负责人')+': '+md(item.owner ?? unknown)+'; '+(en?'Due':'日期')+': '+md(item.due ?? unknown)); lines.push('',quote(item),''); });
  }
  return lines.join('\n')+'\n';
}
export async function main(argv = process.argv.slice(2)) {
  const command = argv[0];
  const { values } = parseArgs({ args:argv.slice(1), options: { input:{type:'string'}, evidence:{type:'string'}, draft:{type:'string'}, out:{type:'string'}, help:{type:'boolean'} } });
  if (values.help || !command) { console.log('prepare --input TEXT_OR_- --out NEW_DIRECTORY | render --evidence evidence.json --draft EXTRACTION_JSON_OR_- --out NEW_DIRECTORY'); return; }
  if (!values.out) throw new Error('--out is required.');
  if (command === 'prepare') {
    if (!values.input || values.evidence || values.draft) throw new Error('prepare requires only --input and --out.');
    const result = evidence(await readText(values.input,1048576)), directory = newOutput(values.out);
    writeNew(directory,'evidence.json',JSON.stringify(result,null,2)+'\n');
    writeNew(directory,'source-numbered.txt',result.lines.map(line=>line.id+' | '+line.text).join('\n')+'\n');
    writeNew(directory,'extraction-template.json',JSON.stringify({schemaVersion:1,sourceSha256:result.sourceSha256,language:'en',title:'Meeting notes',summary:[],decisions:[],actions:[],openQuestions:[]},null,2)+'\n');
    console.log(JSON.stringify({ evidenceFile:path.join(directory,'evidence.json'), numberedText:path.join(directory,'source-numbered.txt'), templateFile:path.join(directory,'extraction-template.json'), draftFile:path.join(directory,'extraction.json'), sourceSha256:result.sourceSha256 }));
  } else if (command === 'render') {
    if (!values.evidence || !values.draft || values.input || values.evidence === '-') throw new Error('render requires --evidence FILE and --draft FILE_OR_-.');
    const original = JSON.parse(await readText(values.evidence,8*1048576)), draft = validate(original,JSON.parse(await readText(values.draft,1048576))), directory = newOutput(values.out);
    writeNew(directory,'meeting.json',JSON.stringify(draft,null,2)+'\n'); writeNew(directory,'meeting.md',markdown(draft));
    const rows = [['task','owner','due','owner_status','due_status','evidence','quote'],...draft.actions.map(item=>[item.task,item.owner ?? '',item.due ?? '',item.owner===null?'unknown':'explicit',item.due===null?'unknown':'explicit',item.evidence.join(';'),item.quote])];
    writeNew(directory,'tasks.csv',rows.map(row=>row.map(csvCell).join(',')).join('\r\n')+'\r\n');
    console.log(JSON.stringify({ output:directory, actions:draft.actions.length, unknownOwners:draft.actions.filter(item=>item.owner===null).length, unknownDates:draft.actions.filter(item=>item.due===null).length, externalActions:0 }));
  } else throw new Error('Use prepare or render.');
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main().catch(error => { console.error('ERROR: '+error.message); process.exitCode=1; });
