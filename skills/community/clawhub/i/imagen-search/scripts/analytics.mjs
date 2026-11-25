import { readFile, mkdir, writeFile, rename } from 'node:fs/promises';
import { homedir } from 'node:os';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
export const ANALYTICS_CONFIG = path.join(homedir(), '.config', 'imagen-chat', 'search-privacy.json');
export async function readAnalytics(file = ANALYTICS_CONFIG) {
  try { const value=JSON.parse(await readFile(file,'utf8')); return value.record_keywords === true; }
  catch(e) { if(e.code==='ENOENT')return false; throw new Error('Cannot read search privacy settings. Fix or remove search-privacy.json before searching.'); }
}
export async function setAnalytics(enabled, file = ANALYTICS_CONFIG) {
  await mkdir(path.dirname(file),{recursive:true,mode:0o700});
  const temporary=`${file}.${randomUUID()}.tmp`;
  await writeFile(temporary,JSON.stringify({record_keywords:enabled}),{mode:0o600,flag:'wx'});
  await rename(temporary,file);
  return {record_keywords:enabled,notice:enabled?'Future search terms may be retained for 30 days. Turn off with analytics --keywords off.':'Future search terms are not retained in Skill analytics. Previously consented aggregates expire after 30 days.'};
}
