/* Bind data into the canonical reader. No alternative layout, UI or runtime. */
(function(scope){
 'use strict';
 const K=typeof module!=='undefined'?require('./engine.cjs'):scope.MindmapKit,L=K.library;
 function fonts(css,boot){
  const selected=L.resolveRecipe(boot.recipeCode||boot.preset||'P61'),families=L.themeFor(selected).font+",'Atlas Business'";
  return css.replace(/\/\*[\s\S]*?\*\/\s*@font-face\{[^}]+\}/g,rule=>families.includes(rule.match(/font-family:'([^']+)'/)[1])?rule:'');
 }
 const encode=data=>JSON.stringify(data).replace(/</g,'\\u003c');
 function prepare(template,boot){
  if(!template.includes('id="stage"')||!template.includes('id="branch-toggle"')||!template.includes('data:font/woff2;base64,')||!/<script id="atlas-boot">window\.ATLAS_BOOT=/.test(template))throw new Error('完整脑图模板暂不可用，请稍后重试');
  boot={...boot,standalone:true,player:true};
  if(boot.document){const E=typeof module!=='undefined'?require('./edit.cjs'):scope.MindmapEdit,model=E.create(boot);boot={...boot,document:model.document(),source:model.markdown(boot.recipeCode)};}
  L.resolveRecipe(boot.recipeCode||boot.preset||'P61');const root=K.parseMindmap(boot.source);
  return template.replace(/<style>([\s\S]*?)<\/style>/,(_,css)=>'<style>'+fonts(css,boot)+'</style>').replace(/<title>[\s\S]*?<\/title>/,()=>'<title>'+K.escapeXML(root.text)+' · mindbox</title>').replace(/<script id="atlas-boot">[\s\S]*?<\/script>/,()=>'<script id="atlas-boot">window.ATLAS_BOOT='+encode(boot)+';</'+'script>');
 }
 function createLoader({baseURL,fetch:fetchResource=scope.fetch,timeoutMs=15000,assets={shell:'downloads/reader-shell.html',fonts:'downloads/reader-fonts.json'}}){
  const base=new URL(baseURL),cache=new Map(),faces=new Map();
  function resource(file,type){
   const url=new URL(file,base);
   if(url.origin!==base.origin)throw new Error('脑图资源地址不正确，请刷新页面重试');
   if(!cache.has(url.href)){
    const controller=new AbortController();let expired=false;
    const timer=setTimeout(()=>{expired=true;controller.abort();},timeoutMs);
    const pending=(async()=>{
     try{const response=await fetchResource(url.href,{signal:controller.signal});if(!response.ok)throw new Error('脑图资源暂时无法加载，请重试');return await response[type]();}
     catch(error){throw new Error(expired?'连接超时，请重试打开脑图':error.message);}
     finally{clearTimeout(timer);}
    })();
    cache.set(url.href,pending);pending.catch(()=>{if(cache.get(url.href)===pending)cache.delete(url.href);});
   }
   return cache.get(url.href);
  }
  function face(entry){
   if(!faces.has(entry.url)){
    const pending=resource(entry.url,'arrayBuffer').then(buffer=>{
     const bytes=new Uint8Array(buffer);let binary='';
     for(let i=0;i<bytes.length;i+=32768)binary+=String.fromCharCode(...bytes.subarray(i,i+32768));
     return entry.css.replace('__MINDBOX_FONT_DATA__',()=>scope.btoa(binary));
    });
    faces.set(entry.url,pending);pending.catch(()=>{if(faces.get(entry.url)===pending)faces.delete(entry.url);});
   }
   return faces.get(entry.url);
  }
  return async boot=>{
   const [shell,manifest]=await Promise.all([resource(assets.shell,'text'),resource(assets.fonts,'json')]);
   const selected=L.themeFor(L.resolveRecipe(boot.recipeCode||boot.preset||'P61')).font+",'Atlas Business'";
   if(manifest.format!==1||!Array.isArray(manifest.fonts)||!shell.includes('/*__MINDBOX_READER_FONTS__*/'))throw new Error('脑图资源已更新，请刷新页面重试');
   const entries=manifest.fonts.filter(entry=>selected.includes("'"+entry.family+"'"));
   if(!entries.some(entry=>entry.family==='Atlas Business'))throw new Error('脑图字体暂时无法加载，请重试');
   const css=(await Promise.all(entries.map(face))).join('');
   return prepare(shell.replace('/*__MINDBOX_READER_FONTS__*/',()=>css),boot);
  };
 }
 function preview({dialog,frame,status,message,retry,load}){
  let sequence=0,last,active;
  function release(button){if(button){button.disabled=false;button.setAttribute('aria-busy','false');}}
  async function open(boot,button){
   release(active);active=button;last={boot,button};const request=++sequence;
   if(button){button.disabled=true;button.setAttribute('aria-busy','true');}
   frame.hidden=true;status.hidden=false;retry.hidden=true;message.textContent='正在准备这张脑图…';
   if(!dialog.open)dialog.showModal();
   try{
    const html=await load(boot);
    if(request!==sequence||!dialog.open)return false;
    frame.onload=()=>{if(request===sequence&&dialog.open)status.hidden=true;};
    frame.srcdoc=html;frame.hidden=false;return true;
   }catch(error){
    if(request===sequence&&dialog.open){message.textContent=error.message;retry.hidden=false;}
    return false;
   }finally{if(request===sequence||button!==active)release(button);}
  }
  retry.addEventListener('click',()=>{if(last)open(last.boot,last.button);});
  dialog.addEventListener('close',()=>{sequence++;release(active);active=null;last=null;frame.onload=null;frame.removeAttribute('srcdoc');frame.hidden=true;status.hidden=true;});
  return {open};
 }
 const api={fonts,encode,prepare,createLoader,preview};if(typeof module!=='undefined')module.exports=api;else scope.MindboxReaderExport=api;
})(typeof globalThis!=='undefined'?globalThis:this);
