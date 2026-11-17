#!/usr/bin/env node
import path from 'node:path';
import {randomUUID} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {fetchPublic,publicUrl,utf8} from './public-net.mjs';
import {pageMetadata} from './html-text.mjs';
import {workspaceFolder,readLocal,writeNew,options,md,language} from './local-files.mjs';

function findingText(value,en){if(en)return value;const known={'HTTP status is outside 2xx':'HTTP 状态不在 2xx 成功范围','Not an HTML response; page metadata was not inspected':'响应不是 HTML，未检查页面元信息','Canonical is not an accepted public URL; value omitted':'canonical 不是允许的公开网址，已省略该值','No HTML title found':'未找到 HTML title','No meta description found':'未找到 description 元信息','No usable canonical found':'未找到可用的 canonical','Only UTF-8 pages are supported':'只支持 UTF-8 页面'};return known[value]||('观察信息：'+value);}
function errorText(value,en){if(en)return value;const known=[[/CERT_HAS_EXPIRED/i,'证书已过期'],[/SELF_SIGNED|UNABLE_TO_VERIFY|CERT_UNTRUSTED/i,'证书信任校验失败'],[/ERR_TLS_CERT_ALTNAME_INVALID/i,'证书域名不匹配'],[/ENOTFOUND|EAI_AGAIN/i,'域名解析失败'],[/deadline|ETIMEDOUT/i,'请求超时'],[/ECONNREFUSED/i,'连接被拒绝'],[/ECONNRESET/i,'连接被重置'],[/DNS includes a private or reserved address/i,'域名解析包含内网或保留地址，已拒绝访问'],[/Redirect limit/i,'跳转次数超过上限'],[/exceeds download limit/i,'下载数据超过上限'],[/expanded body limit/i,'解压后正文超过上限']];return (known.find(([pattern])=>pattern.test(value))?.[1]||'网络请求失败')+'（'+value+'）';}
export function inspect(response){
 const html=/^(?:text\/html|application\/xhtml\+xml)(?:;|$)/i.test(response.contentType);let meta={title:'',description:'',robots:'',canonical:''},decodeError=null;
 if(html){try{meta=pageMetadata(utf8(response.body));}catch(e){decodeError=e.message;}}
 const findings=[];if(response.status<200||response.status>=300)findings.push('HTTP status is outside 2xx');if(!html)findings.push('Not an HTML response; page metadata was not inspected');if(decodeError)findings.push(decodeError);
 let canonical=null;if(meta.canonical){try{canonical=publicUrl(new URL(meta.canonical,response.finalUrl).href).href;}catch{findings.push('Canonical is not an accepted public URL; value omitted');}}
 if(html&&!decodeError){if(!meta.title)findings.push('No HTML title found');if(!meta.description)findings.push('No meta description found');if(!canonical)findings.push('No usable canonical found');}
 return {url:response.requestedUrl,finalUrl:response.finalUrl,status:response.status,elapsedMs:response.elapsedMs,tlsValidated:true,redirects:response.redirects,contentType:response.contentType,title:meta.title,description:meta.description,robots:meta.robots||null,canonical,findings};
}
export async function check({workspace,urlsFile,lang='en'},fetcher=fetchPublic){
 language(lang);const input=JSON.parse(await readLocal(workspace,urlsFile,16384));if(!Array.isArray(input)||!input.length||input.length>5||input.some(x=>typeof x!=='string'))throw Error('Provide one to five explicit public HTTPS URLs in a JSON array');
 const urls=[...new Set(input.map(x=>publicUrl(x).href))],results=[];
 for(let i=0;i<urls.length;i+=2){const batch=await Promise.all(urls.slice(i,i+2).map(async url=>{try{return inspect(await fetcher(url));}catch(e){return {url,status:null,tlsValidated:null,error:String(e.message).replace(/[\r\n]/g,' ').slice(0,180)};}}));results.push(...batch);}
 const runId=randomUUID(),checkedAt=new Date().toISOString(),en=lang==='en';
 const report={schema:'mochi-site-check.v1',runId,checkedAt,language:lang,results,scope:'One-off bounded GET from this host. No robots.txt, browser JavaScript, links, ports, forms or vulnerabilities scanned.'};
 const lines=['# '+(en?'Website availability and basic SEO check':'网站可用性与基础 SEO 巡检'),'',(en?'Checked':'检查时间')+': '+checkedAt,''];
 for(const [i,r] of results.entries()){
  lines.push('## '+(i+1)+'. '+md(r.url),'');
  if(r.error){lines.push((en?'Request incomplete':'请求未完成')+': '+md(errorText(r.error,en)),'');continue;}
  const missing=en?'(not found)':'（未找到）';
  lines.push('- HTTP: '+r.status,'- '+(en?'Final URL':'最终网址')+': '+md(r.finalUrl),'- '+(en?'Elapsed from this host (DNS/redirects/body included)':'本机耗时（含DNS、跳转与正文）')+': '+r.elapsedMs+' ms','- TLS: '+(en?'Certificate validation succeeded':'证书正常校验通过'),'- '+(en?'Redirect count':'跳转次数')+': '+r.redirects.length,'- title: '+md(r.title||missing),'- description: '+md(r.description||missing),'- robots meta: '+md(r.robots||(en?'(not declared in HTML)':'（HTML 未声明）')),'- canonical: '+md(r.canonical||missing),'');
  if(r.findings.length)lines.push((en?'Observations':'观察项')+': '+r.findings.map(value=>md(findingText(value,en))).join(en?'; ':'；'),'');
 }
 lines.push(en?'A missing robots meta tag does not establish crawl permission: robots.txt and other signals were not checked. These observations do not guarantee indexing, rankings, continuous uptime or security.':'没有 robots meta 不代表已经允许抓取：本次不检查 robots.txt 等其他信号。结果不保证收录、排名、持续在线或系统安全。','');
 const output=await workspaceFolder(workspace,'site-checks'),jsonFile=path.join(output,'site-check-'+runId+'.json'),markdownFile=path.join(output,'site-check-'+runId+'.md');
 await writeNew(jsonFile,JSON.stringify(report,null,2)+'\n');await writeNew(markdownFile,lines.join('\n'));return {jsonFile,markdownFile,...report};
}
export async function main(argv){const [command,...args]=argv;if(!command||command==='help'){console.log('check --workspace PATH --urls FILE [--language en|zh-CN]\nOne-off GET of 1–5 explicit public HTTPS URLs; no schedule or external delivery.');return;}if(command!=='check')throw Error('Use check');const a=options(args,['--workspace','--urls','--language']);if(!a['--workspace']||!a['--urls'])throw Error('--workspace and --urls are required');console.log(JSON.stringify(await check({workspace:a['--workspace'],urlsFile:a['--urls'],lang:a['--language']||'en'}),null,2));}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv.slice(2)).catch(e=>{console.error('Site check stopped: '+e.message);process.exitCode=1;});
