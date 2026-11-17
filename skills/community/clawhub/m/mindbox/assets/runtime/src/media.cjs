/* Pure reading sequence, vector scenes and animated WebP container. */
(function(scope){
 'use strict';
 const K=typeof module!=='undefined'?require('./engine.cjs'):scope.MindmapKit;
 const R=typeof module!=='undefined'?require('./render.cjs'):scope.MindmapRenderer,L=K.library,esc=K.escapeXML;
 function choices(recipe){
  const codes=[recipe.code];
  return [...new Set(codes)].map(code=>{const r=L.resolveRecipe(code);return {code,name:r.preset?.name.split(' · ')[0]||'所选搭配',preset:r.preset?.id||null};});
 }
 function scene(root,recipe){
  const theme=L.themeFor(recipe),geo=K.layoutTree(root,recipe.tokens.L.id,new Set(),Infinity,theme.density);
  return {root,recipe,theme,geo};
 }
 function readingSteps(geo,limit=24){
  const aspect=animationAspect(geo),capacity=frameCapacity(aspect);
  if(!Number.isInteger(limit)||limit<2)throw new Error('阅读分组数量须至少为2');
  const children=new Map(),parents=new Map(),nodes=new Map(geo.nodes.map(n=>[n.id,n]));
  geo.edges.forEach(e=>{if(!children.has(e.from))children.set(e.from,[]);children.get(e.from).push(e.to);parents.set(e.to,e.from);});
  // Balanced geometry groups right/left branches for placement; reading keeps authored order.
  children.forEach((kids,id)=>{const authored=nodes.get(id).children?.map(n=>n.id)||kids;children.set(id,[...authored.filter(child=>kids.includes(child)),...kids.filter(child=>!authored.includes(child))]);});
  const root=geo.nodes.find(n=>!n.depth),ordered=[];
  function visit(id){ordered.push(nodes.get(id));(children.get(id)||[]).forEach(visit);}visit(root.id);
  // The old 24-step cap combined distant branches into unreadable overviews.
  // Keep DFS order but split a group whenever its camera would shrink the text.
  const batch=Math.min(6,Math.max(1,Math.ceil((ordered.length-1)/(limit-1)))),groups=[[root]];
  let group=[];
  for(const n of ordered.slice(1)){
   const candidate=[...group,n],camera=cameraBounds(geo,{targets:candidate.map(n=>n.id)},aspect);
   if(group.length&&(candidate.length>batch||minFont(candidate)*capacity.width/camera.w<24.5)){groups.push(group);group=[];}
   group.push(n);
  }
  if(group.length)groups.push(group);
  return groups.map(group=>{
   const active=new Set();for(const n of group){let id=n.id;while(id){active.add(id);id=parents.get(id);}}
   const n=group[0],path=[];let id=n.id;while(id){path.unshift(nodes.get(id).text);id=parents.get(id);}
   return {targets:group.map(n=>n.id),active:[...active],label:group.length===1?n.text:`${n.text} 等 ${group.length} 项`,path};
  });
 }
 function nodeBounds(nodes,pad=36){
  const x=Math.min(...nodes.map(n=>n.x-n.w/2))-pad,y=Math.min(...nodes.map(n=>n.y-n.h/2))-pad;
  return {x,y,w:Math.max(...nodes.map(n=>n.x+n.w/2))+pad-x,h:Math.max(...nodes.map(n=>n.y+n.h/2))+pad-y};
 }
 function focusBounds(geo,step){return nodeBounds(geo.nodes.filter(n=>step.targets.includes(n.id)));}
 function minFont(nodes=[]){const sizes=nodes.map(n=>n.fontSize).filter(n=>Number.isFinite(n)&&n>0);return sizes.length?Math.min(...sizes):14;}
 function animationAspect(geo){
  const tall=geo.nodes.filter(n=>n.h>n.w).map(n=>(n.w+72)/(n.h+72));
  return tall.length?Math.max(.6,Math.min(16/9,...tall)):16/9;
 }
 function frameCapacity(aspect){return dimensions({w:1920,h:1920/aspect+64},1,2560,4000000);}
 function cameraBounds(geo,step,aspect=16/9){
  const targets=geo.nodes.filter(n=>step.targets.includes(n.id)),parentIds=new Set(geo.edges.filter(e=>step.targets.includes(e.to)).map(e=>e.from));
  const frame=b=>{const w=Math.max(b.w,360,b.h*aspect,200*aspect);return{x:b.x+b.w/2-w/2,y:b.y+b.h/2-w/aspect/2,w,h:w/aspect};};
  const context=frame(nodeBounds(geo.nodes.filter(n=>step.targets.includes(n.id)||parentIds.has(n.id))));
  // Keep parent context only while the target text still meets the reading budget.
  return minFont(targets)*frameCapacity(aspect).width/context.w>=24.5?context:frame(nodeBounds(targets));
 }
 function zoomPolicy(bounds,viewport,nodes=[],contentBounds=bounds){
  const fit=Math.min(viewport.width/bounds.w,viewport.height/bounds.h),referenceFit=Math.min(viewport.width/contentBounds.w,viewport.height/contentBounds.h),font=minFont(nodes),detailTextPx=Math.max(32,Math.min(64,Math.min(viewport.width,viewport.height)/10));
  return {fit,minScale:Math.min(referenceFit*.2,1),maxScale:Math.max(referenceFit,detailTextPx/font),detailTextPx,minFont:font};
 }
 function zoomPercent(scale){return Math.round(scale*1000)/10;}
 // Ratios remain relative to fit internally so old saved views remain compatible.
 function maxZoom(bounds,viewport,nodes=[],contentBounds=bounds){const p=zoomPolicy(bounds,viewport,nodes,contentBounds);return p.maxScale/p.fit;}
 function clampZoom(value,bounds,viewport,nodes=[],contentBounds=bounds){const p=zoomPolicy(bounds,viewport,nodes,contentBounds);return Number.isFinite(value)?Math.max(p.minScale/p.fit,Math.min(p.maxScale/p.fit,value)):1;}
 function anchoredView(bounds,viewport,point,node,scale,nodes=[],contentBounds=bounds){
  const fit=Math.min(viewport.width/bounds.w,viewport.height/bounds.h),zoom=clampZoom(scale/fit,bounds,viewport,nodes,contentBounds),actual=fit*zoom;
  return {zoom,x:point.x-viewport.width/2+(bounds.x+bounds.w/2-node.x)*actual,y:point.y-viewport.height/2+(bounds.y+bounds.h/2-node.y)*actual};
 }
 function dimensions(bounds,scale=2,maxSide=8192,maxPixels=16000000){
  const factor=Math.min(scale,maxSide/bounds.w,maxSide/bounds.h,Math.sqrt(maxPixels/(bounds.w*bounds.h)));
  return {width:Math.max(1,Math.floor(bounds.w*factor)),height:Math.max(1,Math.floor(bounds.h*factor))};
 }
 function imagePlan(bounds,nodes=[]){
  const font=minFont(nodes),targetTextPx=28,desiredScale=Math.max(2,targetTextPx/font),size=dimensions(bounds,desiredScale,32760,64000000),scale=Math.min(size.width/bounds.w,size.height/bounds.h);
  return {...size,scale,minTextPx:font*scale,targetTextPx,limited:scale<desiredScale-.002};
 }
 function animationPlan(geo){
  const aspect=animationAspect(geo),steps=readingSteps(geo),cameras=steps.map(step=>cameraBounds(geo,step,aspect)),fontFor=step=>minFont(geo.nodes.filter(n=>step.targets.includes(n.id)));
  const targetTextPx=24,width=Math.ceil(Math.max(Math.min(960,720*aspect),...cameras.map((b,i)=>b.w*targetTextPx/fontFor(steps[i])*1.02)));
  const size=dimensions({w:width,h:width/aspect+64},1,2560,4000000),actualAspect=size.width/(size.height-64),finalCameras=steps.map(step=>cameraBounds(geo,step,actualAspect));
  const minTextPx=Math.min(...finalCameras.map((b,i)=>fontFor(steps[i])*size.width/b.w));
  return {...size,steps,cameras:finalCameras,minTextPx,targetTextPx,limited:minTextPx<targetTextPx-.02};
 }
 function exportDimensions(bounds,animated=false,nodes=[]){
  if(!animated){const {width,height}=imagePlan(bounds,nodes);return{width,height};}
  if(!nodes.length)return dimensions(bounds,2,1920,2000000);
  const ids=new Set(nodes.map(n=>n.id)),geo={bounds,nodes,edges:nodes.flatMap(n=>(n.children||[]).filter(c=>ids.has(c.id)).map(c=>({from:n.id,to:c.id})))};
  const {width,height}=animationPlan(geo);return{width,height};
 }
 function background(s){
  const b=s.geo.bounds,t=s.theme;
  let marks='';
  if(['grid','ruled','dots'].includes(t.canvas.pattern)){
   const kind=t.canvas.pattern,color=L.mix(t.bg,L.readableText(t.bg),.12);
   marks=`<defs><pattern id="paper" width="${kind==='ruled'?28:22}" height="${kind==='ruled'?28:22}" patternUnits="userSpaceOnUse">${kind==='dots'?`<circle cx="2" cy="2" r=".8" fill="${color}"/>`:`<path d="M0 0H28${kind==='grid'?'M0 0V28':''}" stroke="${color}" stroke-width=".6"/>`}</pattern></defs><rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" fill="url(#paper)"/>`;
  }
  return `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" fill="${t.bg}"/>${marks}`;
 }
 function svg(s,fonts='',animated=false,pixels=null,camera=null){
  const b=camera||s.geo.bounds,steps=animated?readingSteps(s.geo):[],stepMs=900,total=(steps.length+2)*stepMs;
  const art=R.svgContent(s.geo,s.theme,s.recipe.tokens.L.id,new Set(),false);
  let content=art;
  if(animated){
   const rectangles=step=>s.geo.nodes.filter(n=>step.active.includes(n.id)).map(n=>`<rect x="${n.x-n.w/2-16}" y="${n.y-n.h/2-32}" width="${n.w+32}" height="${n.h+48}" rx="10"/>`).join('');
   const times=Array.from({length:steps.length+3},(_,i)=>i/(steps.length+2));
   const overlays=steps.map((step,i)=>{
    const values=times.map((_,j)=>j===i?'1':'0');
    const focus=s.geo.nodes.filter(n=>step.targets.includes(n.id)).map(n=>`<rect x="${n.x-n.w/2-8}" y="${n.y-n.h/2-8}" width="${n.w+16}" height="${n.h+16}" rx="15" fill="none" stroke="${L.contrast(s.theme.accent,s.theme.bg)>=3?s.theme.accent:s.theme.ink}" stroke-width="2" stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" from="0" to="-20" dur="900ms" repeatCount="indefinite"/></rect>`).join('');
    return `<clipPath id="focus-${i}">${rectangles(step)}</clipPath><g opacity="0"><animate attributeName="opacity" values="${values.join(';')}" keyTimes="${times.join(';')}" dur="${total}ms" calcMode="discrete" repeatCount="indefinite"/><g clip-path="url(#focus-${i})"><use href="#art"/></g>${focus}</g>`;
   }).join('');
   const visibility=times.map((_,j)=>j>=steps.length?'1':'.22').join(';');
   // Viewers without SMIL still display the complete, readable vector map.
   content=`<defs><g id="art">${art}</g></defs><use href="#art" opacity="1"><animate attributeName="opacity" values="${visibility}" keyTimes="${times.join(';')}" dur="${total}ms" calcMode="discrete" repeatCount="indefinite"/></use>${overlays}`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="${b.x} ${b.y} ${b.w} ${b.h}" width="${pixels?.width||Math.ceil(b.w)}" height="${pixels?.height||Math.ceil(b.h)}" role="img" aria-label="${esc(s.root.text)}" data-recipe="${s.recipe.code}"><title>${esc(s.root.text)}</title><style><![CDATA[${fonts.replace(/\]\]>/g,']]]]><![CDATA[>')}]]></style>${background(s)}${content}</svg>`;
 }
 const ascii=s=>Uint8Array.from(s,c=>c.charCodeAt(0));
 const le=(n,bytes)=>Uint8Array.from({length:bytes},(_,i)=>Math.floor(n/2**(8*i))&255);
 function join(parts){const out=new Uint8Array(parts.reduce((n,p)=>n+p.length,0));let at=0;parts.forEach(p=>{out.set(p,at);at+=p.length;});return out;}
 const chunk=(name,data)=>join([ascii(name),le(data.length,4),data,...(data.length%2?[new Uint8Array(1)]:[])]);
 function frameData(bytes){
  if(!(bytes instanceof Uint8Array)||bytes.length<20||String.fromCharCode(...bytes.slice(0,4))!=='RIFF'||String.fromCharCode(...bytes.slice(8,12))!=='WEBP')throw new Error('浏览器未提供WebP图像，不能生成WebP动图');
  const size=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength).getUint32(4,true)+8;
  if(size!==bytes.length)throw new Error('WebP帧长度无效');
  const parts=[];let image=false,alpha=false;
  for(let at=12;at+8<=size;){const tag=String.fromCharCode(...bytes.slice(at,at+4)),length=new DataView(bytes.buffer,bytes.byteOffset+at+4,4).getUint32(0,true),end=at+8+length+(length%2);if(end>size)throw new Error('WebP帧数据不完整');
   if(['ALPH','VP8 ','VP8L'].includes(tag)){parts.push(bytes.slice(at,end));image ||= tag!=='ALPH';alpha ||=tag==='ALPH'||tag==='VP8L'&&Boolean(bytes[at+12]&16);}
   at=end;
  }
  if(!image)throw new Error('WebP帧缺少图像数据');return {bytes:join(parts),alpha};
 }
 function animatedWebP(frames,width,height){
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1||width>16383||height>16383||!frames.length)throw new Error('WebP动画尺寸或帧数无效');
  const decoded=frames.map(f=>({...frameData(f.bytes),duration:f.duration}));
  if(decoded.some(f=>!Number.isInteger(f.duration)||f.duration<1||f.duration>0xffffff))throw new Error('WebP帧时长无效');
  const extended=chunk('VP8X',join([Uint8Array.of(2|(decoded.some(f=>f.alpha)?16:0),0,0,0),le(width-1,3),le(height-1,3)]));
  const animation=chunk('ANIM',Uint8Array.of(255,255,255,255,0,0));
  const data=join([ascii('WEBP'),extended,animation,...decoded.map(f=>chunk('ANMF',join([new Uint8Array(6),le(width-1,3),le(height-1,3),le(f.duration,3),Uint8Array.of(2),f.bytes])))]);
  return join([ascii('RIFF'),le(data.length,4),data]);
 }
 const api={choices,scene,readingSteps,focusBounds,cameraBounds,zoomPolicy,zoomPercent,imagePlan,animationPlan,maxZoom,clampZoom,anchoredView,dimensions,exportDimensions,svg,animatedWebP,frameData};
 if(typeof module!=='undefined')module.exports=api;else scope.MindmapMedia=api;
})(typeof globalThis!=='undefined'?globalThis:this);
