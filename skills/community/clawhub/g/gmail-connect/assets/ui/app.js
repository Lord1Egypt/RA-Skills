'use strict';
const $=id=>document.getElementById(id);
const fragment=location.hash.slice(1);
if(fragment && !['setup','connect','verify','mail'].includes(fragment)){
 sessionStorage.setItem('gmail-connect-key',fragment);history.replaceState(null,'','/');
}
const key=sessionStorage.getItem('gmail-connect-key')||'';
let nextPage=null;
const notice=(text,error=false)=>{$('notice').textContent=text;$('notice').className=error?'error':'';};
async function api(path,data){
 const response=await fetch('/api/'+path,{method:data===undefined?'GET':'POST',headers:{'Authorization':'Bearer '+key,...(data===undefined?{}:{'Content-Type':'application/json'})},...(data===undefined?{}:{body:JSON.stringify(data)})});
 const result=await response.json();if(!response.ok)throw Error(result.error||'Request failed.');return result;
}
function bind(id,fn){$(id).addEventListener('click',async()=>{const b=$(id);b.disabled=true;try{await fn();}catch(e){notice(e.message,true);}finally{b.disabled=false;}});}
function links(){const p=$('project').value.trim();const suffix=p?'?project='+encodeURIComponent(p):'';
 $('project-console-link').href=p?'https://console.cloud.google.com/home/dashboard?project='+encodeURIComponent(p):'https://console.cloud.google.com/projectselector2/home/dashboard';
 $('api-link').href='https://console.cloud.google.com/apis/library/gmail.googleapis.com'+suffix;
 $('branding-link').href='https://console.cloud.google.com/auth/overview'+suffix;
 $('audience-link').href='https://console.cloud.google.com/auth/audience'+suffix;
 $('data-link').href='https://console.cloud.google.com/auth/scopes'+suffix;
 $('client-link').href='https://console.cloud.google.com/auth/clients'+suffix;
}
$('project').addEventListener('input',links);links();
async function status(){const s=await api('status');$('badge').textContent=s.connected?'Connected':'Not connected';$('account').textContent=s.email||'Not connected';$('monitor').textContent=s.service.active?'Running · about every minute':'Off';$('last-sync').textContent=s.sync?.at?new Date(s.sync.at*1000).toLocaleString():'Not yet checked';$('sending').checked=s.sending;
 if(s.project&&$('project').value!==s.project){$('project').value=s.project;links();}
 notice(s.connected?'Connected to '+s.email+'. Verify Gmail to check live access.':s.clientImported?'Credentials imported. Connect with Google to continue.':'Start with your Google project, then upload its Desktop client JSON.');}
$('client').addEventListener('change',async()=>{try{const f=$('client').files[0];if(!f)return;if(f.size>20000)throw Error('Choose the small OAuth client JSON file (under 20 KB).');await api('client',JSON.parse(await f.text()));await status();}catch(e){notice(e.message,true);}finally{$('client').value='';}});
bind('authorize',async()=>{const tab=window.open('about:blank','_blank');try{const r=await api('connect',{sending:$('sending').checked});if(tab){tab.opener=null;tab.location=r.url;}else{const a=document.createElement('a');a.href=r.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent='Continue to Google authorization ↗';$('notice').replaceChildren(a);return;}notice('Complete authorization in the Google tab, then return here and click Refresh status.');}catch(e){tab?.close();throw e;}});
bind('refresh',status);
bind('verify-button',async()=>{await api('check',{});await status();notice('Verified: Google authorization, Gmail profile access, and mailbox synchronization succeeded. Ask OpenClaw to use Gmail Connect to read your inbox.');});
bind('start-monitor',async()=>{const r=await api('monitor/start',{});await status();notice(r.note);});
bind('stop-monitor',async()=>{await api('monitor/stop',{});await status();notice('Background checks stopped.');});
async function search(page){const result=await api('search',{query:$('query').value,page});$('messages').replaceChildren();for(const m of result.messages){const row=document.createElement('div');row.className='mail-row';const b=document.createElement('button');b.textContent=m.subject||'(No subject)';b.onclick=async()=>{try{const full=await api('read',{id:m.id});$('message-body').hidden=false;$('message-body').textContent=full.text||full.snippet||'No plain text body available.';}catch(e){notice(e.message,true);}};const p=document.createElement('p');p.textContent=m.from+' · '+m.date;row.append(b,p);$('messages').append(row);}if(!result.messages.length)$('messages').textContent='No matching messages.';nextPage=result.nextPageToken;$('next').hidden=!nextPage;}
bind('search',()=>search(null));bind('next',()=>search(nextPage));
async function drafts(){const result=await api('drafts',{});$('drafts').replaceChildren();if(!result.length)$('drafts').textContent='No prepared messages yet.';for(const d of result){const box=document.createElement('div');box.className='draft';const h=document.createElement('h4');h.textContent=d.subject;const p=document.createElement('p');p.textContent='From: '+d.account+' → To: '+d.to+' · '+d.status;const body=document.createElement('pre');body.textContent=d.body;box.append(h,p,body);if(d.status==='pending'){const send=document.createElement('button');send.textContent='Send this exact message';send.onclick=async()=>{if(!window.confirm('Send this displayed message to '+d.to+'?'))return;send.disabled=true;try{await api('send',{id:d.id});notice('Message sent.');await drafts();}catch(e){notice(e.message,true);await drafts();}};box.append(send);}$('drafts').append(box);}}
bind('drafts-button',drafts);
bind('disconnect',async()=>{if(!window.confirm('Stop background checks and delete local Gmail tokens, cached events, and prepared messages?'))return;const r=await api('disconnect',{});$('messages').replaceChildren();$('drafts').replaceChildren();$('message-body').hidden=true;await status();notice(r.note);});
status().catch(e=>notice(e.message,true));
