#!/usr/bin/env node
import path from 'node:path';
import fs from 'node:fs/promises';
import {randomUUID,createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {workspaceFolder,readLocal,writeNew,options,md,language,noLinks} from './local-files.mjs';

const normalized=value=>value.normalize('NFC').replace(/\s+/g,' ').trim();
export function paragraphs(source){const chunks=[];for(const p of source.replace(/\r\n?/g,'\n').split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean)){const chars=Array.from(p);for(let i=0;i<chars.length;i+=2000)chunks.push(chars.slice(i,i+2000).join(''));}if(!chunks.length||chunks.length>80)throw Error('Use 1–80 bounded paragraphs; shorten the source');return chunks.map((text,i)=>({id:'P'+(i+1),text}));}
export async function prepare({workspace,sourceFile,lang='en',maxCards=8}){
 language(lang);if(!Number.isInteger(maxCards)||maxCards<1||maxCards>20)throw Error('max-cards must be 1–20');
 const source=await readLocal(workspace,sourceFile,65536),runId=randomUUID();const evidence={schema:'mochi-learning-cards.v1',runId,language:lang,maxCards,sourceName:path.basename(sourceFile),preparedAt:new Date().toISOString(),sourceText:source,sourceSha256:createHash('sha256').update(source,'utf8').digest('hex'),paragraphs:paragraphs(source)};
 const folder=await workspaceFolder(workspace,'.mochi-learning-cards'),evidenceFile=path.join(folder,'evidence-'+runId+'.json'),cardsFile=path.join(folder,'cards-'+runId+'.json');await writeNew(evidenceFile,JSON.stringify(evidence,null,2)+'\n');return {evidenceFile,cardsFile,...evidence};
}
export function validateCards(e,cards){
 if(e.schema!=='mochi-learning-cards.v1'||!Number.isInteger(e.maxCards)||e.maxCards<1||e.maxCards>20||!Array.isArray(e.paragraphs)||!e.paragraphs.length||e.paragraphs.length>80)throw Error('Invalid prepared evidence');
 if(typeof e.sourceText!=='string'||createHash('sha256').update(e.sourceText,'utf8').digest('hex')!==e.sourceSha256||JSON.stringify(paragraphs(e.sourceText))!==JSON.stringify(e.paragraphs))throw Error('Source snapshot/paragraph mismatch; prepare again');
 const byId=new Map(e.paragraphs.map((p,i)=>{if(p.id!=='P'+(i+1)||typeof p.text!=='string'||p.text.length>4000)throw Error('Invalid source paragraph');return[p.id,p.text];}));
 if(!Array.isArray(cards)||!cards.length||cards.length>e.maxCards)throw Error('Card count must be 1..the requested maximum');
 const seen=new Set();return cards.map((card,i)=>{
  if(!card||typeof card!=='object'||Object.keys(card).some(k=>!['question','answer','sourceId','quote'].includes(k)))throw Error('Card fields: question, answer, sourceId, quote only');
  for(const key of ['question','answer','sourceId','quote'])if(typeof card[key]!=='string'||!card[key].trim())throw Error('Card fields must be nonempty text');
  if(card.question.length>500||card.answer.length>2000||card.quote.length>2000||/<[^>]*>|\[sound:|\{\{/i.test(card.question+card.answer+card.quote))throw Error('Use bounded plain-text cards without HTML/media/template syntax');
  const original=byId.get(card.sourceId),quote=normalized(card.quote);if(!original||quote.length<Math.min(8,normalized(original).length)||!normalized(original).includes(quote))throw Error('Card evidence quote is not present in its source paragraph');
  const key=normalized(card.question).toLowerCase();if(seen.has(key))throw Error('Duplicate card question');seen.add(key);
  return {id:i+1,question:card.question.trim(),answer:card.answer.trim(),sourceId:card.sourceId,quote:card.quote.trim()};
 });
}
export function tsv(value){let clean=String(value).replace(/[\t\r\n]+/g,' ').replace(/[\p{Cc}\p{Cf}]/gu,'');if(/^\s*[=+\-@]/u.test(clean))clean="'"+clean;return '"'+clean.replace(/"/g,'""')+'"';}
export async function exportCards({workspace,evidenceFile}){
 const folder=await workspaceFolder(workspace,'.mochi-learning-cards'),file=path.resolve(evidenceFile);if(path.dirname(file)!==folder||!/^evidence-[a-f0-9-]{36}\.json$/.test(path.basename(file)))throw Error('Use evidence prepared in this workspace');
 const e=JSON.parse(await readLocal(workspace,file,262144));if(path.basename(file)!=='evidence-'+e.runId+'.json')throw Error('Evidence/run ID mismatch');language(e.language);
 const draft=path.join(folder,'cards-'+e.runId+'.json'),cards=validateCards(e,JSON.parse(await readLocal(workspace,draft,131072))),en=e.language==='en';
 const output=await workspaceFolder(workspace,'learning-cards'),markdownFile=path.join(output,'cards-'+e.runId+'.md'),tsvFile=path.join(output,'cards-'+e.runId+'.tsv'),reviewFile=path.join(output,'review-'+e.runId+'.md');
 for(const target of [markdownFile,tsvFile,reviewFile]){await noLinks(target);try{await fs.lstat(target);throw Error('Output already exists; prepare a new run');}catch(error){if(error.code!=='ENOENT')throw error;}}
 const lines=['# '+(en?'Learning cards':'学习卡片'),'',(en?'Source':'原文')+': '+md(e.sourceName),''];
 const review=['# '+(en?'Local review checklist':'本地复习清单'),'',en?'Try each answer before revealing it. Tick the box yourself after review; this list does not schedule reminders or synchronize progress.':'先尝试回忆再看答案。复习后自行勾选；本清单不创建提醒，也不自动同步学习进度。',''];
 const rows=['#separator:Tab','#html:false','#columns:Front\tBack'];
 for(const c of cards){lines.push('## '+c.id+'. '+md(c.question),'',md(c.answer),'',`> ${c.sourceId}: ${md(c.quote)}`,'');rows.push(tsv(c.question)+'\t'+tsv(c.answer+' — '+c.sourceId+': '+c.quote));review.push('- [ ] '+c.id+'. '+md(c.question));}
 lines.push(en?'Quotes were checked against the supplied text. This does not prove the source or the answer is true; review meaning and ambiguity before studying.':'已检查引用是否存在于给定原文，不等于证明原文或答案正确；学习前请核对含义与歧义。','');
 await writeNew(markdownFile,lines.join('\n'));await writeNew(tsvFile,rows.join('\n')+'\n');await writeNew(reviewFile,review.join('\n')+'\n');return {markdownFile,tsvFile,reviewFile,cards:cards.length,source:e.sourceName};
}
export async function main(argv){const [command,...args]=argv;if(!command||command==='help'){console.log('prepare --workspace PATH --source FILE [--language en|zh-CN] [--max-cards 1..20]\nexport --workspace PATH --evidence FILE\nUses supplied local text, no model API, network, schedule or external learning platform.');return;}const a=options(args,command==='prepare'?['--workspace','--source','--language','--max-cards']:['--workspace','--evidence']);if(!a['--workspace'])throw Error('--workspace is required');if(command==='prepare'){if(!a['--source'])throw Error('--source is required');const n=a['--max-cards']||'8';if(!/^\d+$/.test(n))throw Error('Invalid max-cards');console.log(JSON.stringify(await prepare({workspace:a['--workspace'],sourceFile:a['--source'],lang:a['--language']||'en',maxCards:Number(n)}),null,2));}else if(command==='export'){if(!a['--evidence'])throw Error('--evidence is required');console.log(JSON.stringify(await exportCards({workspace:a['--workspace'],evidenceFile:a['--evidence']}),null,2));}else throw Error('Use prepare or export');}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(e=>{console.error('Learning cards stopped: '+e.message);process.exitCode=1;});
