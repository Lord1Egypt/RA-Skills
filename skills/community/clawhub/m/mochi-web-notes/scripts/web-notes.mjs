#!/usr/bin/env node
import path from 'node:path';
import {randomUUID} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {fetchPublic,publicUrl,utf8} from './public-net.mjs';
import {articleText,pageMetadata} from './html-text.mjs';
import {workspaceFolder,readLocal,writeNew,options,md,language} from './local-files.mjs';

export function sourceDate(raw){if(!/^\d{4}-\d\d-\d\d(?:T[^\s]+)?$/.test(raw))return null;const calendar=new Date(raw.slice(0,10)+'T00:00:00Z'),d=new Date(raw);return Number.isFinite(calendar.getTime())&&calendar.toISOString().slice(0,10)===raw.slice(0,10)&&Number.isFinite(d.getTime())?d.toISOString():null;}
export async function collect({workspace,urlsFile,lang='en'},fetcher=fetchPublic){
 language(lang);const urls=JSON.parse(await readLocal(workspace,urlsFile,16384));
 if(!Array.isArray(urls)||!urls.length||urls.length>3||urls.some(x=>typeof x!=='string'))throw Error('Provide one to three explicit public HTTPS URLs in a JSON array');
 const normalized=[...new Set(urls.map(x=>publicUrl(x).href))],sources=[],coverage=[];
 for(const url of normalized){
  try{
   const response=await fetcher(url);if(response.status!==200)throw Error('HTTP '+response.status);
   if(!/^(?:text\/html|application\/xhtml\+xml|text\/plain)(?:;|$)/i.test(response.contentType))throw Error('Only HTML and plain-text pages are supported');
   const html=utf8(response.body),meta=/^text\/plain/i.test(response.contentType)?{title:'',publishedRaw:''}:pageMetadata(html),text=/^text\/plain/i.test(response.contentType)?articleText(html.replace(/</g,'&lt;')):articleText(html);
   if(text.length<20)throw Error('No useful static page text; JavaScript/login/paywall pages are not bypassed');
   const source={id:sources.length+1,url:publicUrl(response.finalUrl).href,title:meta.title||new URL(response.finalUrl).hostname,publishedAt:sourceDate(meta.publishedRaw||''),collectedAt:new Date().toISOString(),excerpt:text.slice(0,1200),text,truncated:text.length>=24000};sources.push(source);coverage.push({url,status:'ok'});
  }catch(error){coverage.push({url,status:'failed',error:String(error.message).replace(/[\r\n]/g,' ').slice(0,180)});}
 }
 const runId=randomUUID(),folder=await workspaceFolder(workspace,'.mochi-web-notes');
 const evidence={schema:'mochi-web-notes.v1',runId,language:lang,createdAt:new Date().toISOString(),sources,coverage};
 const evidenceFile=path.join(folder,'evidence-'+runId+'.json'),draftFile=path.join(folder,'draft-'+runId+'.md');
 await writeNew(evidenceFile,JSON.stringify(evidence,null,2)+'\n');return {evidenceFile,draftFile,...evidence};
}
export async function save({workspace,evidenceFile}){
 const folder=await workspaceFolder(workspace,'.mochi-web-notes'),file=path.resolve(evidenceFile);
 if(path.dirname(file)!==folder||!/^evidence-[a-f0-9-]{36}\.json$/.test(path.basename(file)))throw Error('Use this workspace collector evidence file');
 const e=JSON.parse(await readLocal(workspace,file,512000));
 if(e.schema!=='mochi-web-notes.v1'||path.basename(file)!=='evidence-'+e.runId+'.json'||!Array.isArray(e.sources)||e.sources.length>3||!Array.isArray(e.coverage)||e.coverage.length>3)throw Error('Invalid evidence');
 const en=language(e.language)==='en';
 for(let i=0;i<e.sources.length;i++){const s=e.sources[i];if(s.id!==i+1||typeof s.title!=='string'||typeof s.text!=='string'||typeof s.collectedAt!=='string')throw Error('Invalid source record');publicUrl(s.url);}
 let draft=en?'No usable source text was collected; no summary was invented.':'未取得可用正文，没有编造摘要。';
 if(e.sources.length){
  draft=(await readLocal(workspace,path.join(folder,'draft-'+e.runId+'.md'),50000)).trim();const refs=[...draft.matchAll(/\[(\d+)\]/g)].map(x=>+x[1]);
  if(!draft||!refs.length||refs.some(x=>x<1||x>e.sources.length)||/https?:\/\/|<[^>]*>/i.test(draft))throw Error('Draft needs valid [number] citations and no raw URLs/HTML');
 }
 const renderedDraft=draft.split(/\r?\n/).map(line=>md(line)).join('\n');
 const lines=['# '+(en?'Web research notes':'网页资料笔记'),'',renderedDraft,'','## '+(en?'Sources, dates and excerpts':'来源、日期与摘录'),''];
 for(const s of e.sources){lines.push(`${s.id}. [${md(s.title)}](${s.url.replace(/\(/g,'%28').replace(/\)/g,'%29')})`,`   - ${en?'Publisher date':'页面发布日期'}: ${md(s.publishedAt|| (en?'Not supplied':'页面未提供'))}`,`   - ${en?'Collected':'采集时间'}: ${md(s.collectedAt)}`,`   - ${en?'Excerpt':'摘录'}: ${md(s.excerpt)}`,'');}
 const failed=e.coverage.filter(x=>x.status!=='ok');if(failed.length){lines.push('## '+(en?'Unavailable sources':'未取得的来源'),'');for(const x of failed)lines.push('- '+md(x.url)+': '+md(x.error));}
 lines.push('',en?'Based on bounded static page text. Publisher dates are reported metadata; collection time is not a publication date. No login, JavaScript or paywall was bypassed.':'依据有限的静态网页正文整理。页面日期来自其元数据，采集时间不等于发布日期；未绕过登录、脚本页面或付费墙。','');
 const output=await workspaceFolder(workspace,'web-notes'),report=path.join(output,'web-notes-'+e.runId+'.md');await writeNew(report,lines.join('\n'));return {file:report,sources:e.sources.length,failed:failed.length};
}
export async function main(argv){
 const [command,...args]=argv;if(!command||command==='help'){console.log('collect --workspace PATH --urls FILE [--language en|zh-CN]\nsave --workspace PATH --evidence FILE\nOne-off public-page notes; no schedule, model API or message delivery.');return;}
 const a=options(args,command==='collect'?['--workspace','--urls','--language']:['--workspace','--evidence']);if(!a['--workspace'])throw Error('--workspace is required');
 if(command==='collect'){if(!a['--urls'])throw Error('--urls is required');console.log(JSON.stringify(await collect({workspace:a['--workspace'],urlsFile:a['--urls'],lang:a['--language']||'en'}),null,2));}
 else if(command==='save'){if(!a['--evidence'])throw Error('--evidence is required');console.log(JSON.stringify(await save({workspace:a['--workspace'],evidenceFile:a['--evidence']}),null,2));}else throw Error('Use collect or save');
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(e=>{console.error('Web notes stopped: '+e.message);process.exitCode=1;});
