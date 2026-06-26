#!/usr/bin/env node
/* Start a Google Voice outbound call from an already-authenticated browser session via CDP.
 * This avoids storing cookies. It drives the Google Voice web UI for /u/N/calls.
 */
const CDP_HTTP = process.env.GV_CDP_URL || 'http://127.0.0.1:19222';
let AUTHUSER = process.env.GV_AUTHUSER || '0';

function usage(code=0) {
  const text = `Usage:
  node skills/google-voice/scripts/google-voice-start-call.js --number '+1234567890' --authuser 0

Options:
  --number E164      Recipient number, preferably E.164. Required.
  --authuser N       Google account index, e.g. 0, 1, 2. Default GV_AUTHUSER or 0.
  --dry-run          Open/focus Google Voice calls page but do not click final call button.
  --timeout-ms N     UI automation timeout, default 30000.

Safety:
  Outbound calls are external actions. Confirm exact recipient before running without --dry-run.
`;
  (code ? console.error : console.log)(text.trim()); process.exit(code);
}
function parseArgs(argv){const args={timeoutMs:30000,dryRun:false}; for(let i=0;i<argv.length;i++){const a=argv[i]; if(a==='--help'||a==='-h') usage(0); if(a==='--dry-run'){args.dryRun=true;continue;} if(a.startsWith('--')){const k=a.slice(2),v=argv[++i]; if(v==null) usage(2); if(k==='number') args.number=v; else if(k==='authuser') {AUTHUSER=String(v); args.authuser=String(v);} else if(k==='timeout-ms') args.timeoutMs=Number(v); else usage(2); continue;} if(!args.number) args.number=a; else usage(2);} if(!args.number) usage(2); return args;}
function cdpWsUrl(tabId){const cdp=new URL(CDP_HTTP); const wsProto=cdp.protocol==='https:'?'wss':'ws'; return `${wsProto}://${cdp.host}/devtools/page/${tabId}`;}
async function cdpEval(tabId, expression, timeout=30000){const ws=new WebSocket(cdpWsUrl(tabId)); await new Promise((res,rej)=>{ws.onopen=res;ws.onerror=rej;}); const p=new Promise((res,rej)=>{ws.onmessage=e=>res(JSON.parse(e.data));ws.onerror=rej;}); ws.send(JSON.stringify({id:1,method:'Runtime.evaluate',params:{expression,awaitPromise:true,returnByValue:true,timeout}})); const msg=await p; ws.close(); if(msg.result?.exceptionDetails) throw new Error(msg.result.exceptionDetails.exception?.description||msg.result.exceptionDetails.text); if(msg.error) throw new Error(msg.error.message); return msg.result.result.value;}
async function getCallsTab(){const tabs=await (await fetch(`${CDP_HTTP}/json/list`)).json(); const userRe=new RegExp(`voice\\.google\\.com/u/${AUTHUSER}/calls(?:[/?#]|$)`); const exact=tabs.find(t=>userRe.test(t.url||'')); if(exact) return exact.id; const j=await (await fetch(`${CDP_HTTP}/json/new?`+encodeURIComponent(`https://voice.google.com/u/${AUTHUSER}/calls`),{method:'PUT'})).json(); await new Promise(r=>setTimeout(r,3500)); return j.id;}
function automationExpression(number,dryRun){return `
(async()=>{
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 const norm=s=>(s||'').toLowerCase();
 const visible=el=>!!(el&&el.getClientRects&&el.getClientRects().length);
 const click=el=>{el.scrollIntoView({block:'center',inline:'center'}); el.click();};
 const findButton=patterns=>Array.from(document.querySelectorAll('button,[role="button"]')).find(b=>visible(b)&&patterns.some(p=>norm(b.getAttribute('aria-label')||b.innerText||b.textContent).includes(p)));
 const findInput=()=>Array.from(document.querySelectorAll('input,textarea,[contenteditable="true"]')).find(el=>visible(el)&&/(number|name|phone|search|号码|电话|名称)/i.test([el.placeholder,el.getAttribute('aria-label'),el.getAttribute('data-placeholder')].filter(Boolean).join(' '))) || Array.from(document.querySelectorAll('input,textarea,[contenteditable="true"]')).find(visible);
 for(let i=0;i<30;i++){ if(document.readyState==='complete') break; await sleep(500); }
 let dial=findButton(['make a call','place a call','new call','call','拨打','呼叫']);
 if(dial) { click(dial); await sleep(1200); }
 let input=null;
 for(let i=0;i<20;i++){ input=findInput(); if(input) break; await sleep(500); }
 if(!input) return {ok:false,step:'find-input',url:location.href,title:document.title};
 input.focus();
 if(input.isContentEditable){ input.textContent=${JSON.stringify(number)}; input.dispatchEvent(new InputEvent('input',{bubbles:true,inputType:'insertText',data:${JSON.stringify(number)}})); }
 else { input.value=''; input.dispatchEvent(new Event('input',{bubbles:true})); input.value=${JSON.stringify(number)}; input.dispatchEvent(new Event('input',{bubbles:true})); }
 await sleep(800);
 input.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}));
 await sleep(1500);
 if(${dryRun?'true':'false'}) return {ok:true,dryRun:true,step:'filled-number',url:location.href,title:document.title};
 let callBtn=null;
 for(let i=0;i<16;i++){ callBtn=findButton(['call','拨打','呼叫']); if(callBtn && !callBtn.disabled) break; await sleep(500); }
 if(!callBtn || callBtn.disabled) return {ok:false,step:'find-call-button',url:location.href,title:document.title};
 click(callBtn);
 await sleep(1000);
 return {ok:true,dryRun:false,step:'clicked-call',url:location.href,title:document.title};
})()`;}
async function main(){const args=parseArgs(process.argv.slice(2)); const tab=await getCallsTab(); const result=await cdpEval(tab, automationExpression(args.number,args.dryRun), args.timeoutMs); console.log(JSON.stringify({authuser:AUTHUSER,number:args.number,result},null,2)); if(!result?.ok) process.exit(1);}
main().catch(e=>{console.error('google-voice-start-call:',e.message||e); process.exit(1);});
