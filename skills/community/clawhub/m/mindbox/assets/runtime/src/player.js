(function(){
 'use strict';
 const K=window.MindmapKit,L=K.library,R=window.MindmapRenderer,M=window.MindmapMedia,boot=window.ATLAS_BOOT,$=id=>document.getElementById(id),esc=K.escapeXML;
 const model=window.MindmapEdit.create(boot);let root=model.root();
 const initial=L.resolveRecipe(boot.recipeCode||boot.preset||'P61'),selected=initial,options=M.choices(selected);
 const state={recipe:initial,mode:'map',markdownBase:'',composing:false,collapsed:new Set(),scene:null,zoom:1,x:0,y:0,drag:null,moved:false,scale:null,restoreScale:null,tour:null,index:0,timer:null,paused:false,busy:false,selected:null,hoverBranch:null,editor:null};
 const view=boot.view||{};state.restoreScale=Number.isFinite(view.scale)&&view.scale>0?view.scale:null;state.collapsed=new Set((Array.isArray(view.collapsed)?view.collapsed:[]).filter(id=>model.find(id)));state.zoom=Number.isFinite(view.zoom)?Math.max(.2,view.zoom):1;state.x=Number.isFinite(view.x)?Math.max(-1e6,Math.min(1e6,view.x)):0;state.y=Number.isFinite(view.y)?Math.max(-1e6,Math.min(1e6,view.y)):0;
 let savedSignature;const signature=()=>JSON.stringify([model.document(),model.markdown(),state.recipe.code,state.mode==='markdown'&&$('markdown-editor').value!==state.markdownBase?$('markdown-editor').value:null]);
 function updateTitle(){$('document-title').textContent=root.text;document.title=root.text+' · mindbox';}
 updateTitle();
 $('style-choices').innerHTML=options.map(p=>`<button id="map-view" data-style="${p.code}" aria-pressed="true" aria-controls="stage" title="查看导图"><i style="--swatch:${L.themeFor(L.resolveRecipe(p.code)).palette[0]}" aria-hidden="true"></i>${esc(p.name)}</button>`).join('')+'<button id="markdown-view" aria-pressed="false" aria-controls="markdown-panel" title="用 Markdown 快速编辑整张导图"><span class="markdown-symbol" aria-hidden="true">M↓</span>Markdown</button>';
 function message(text,error=false,persistent=false){clearTimeout(message.timer);$('export-status').textContent=text;$('export-status').dataset.error=String(error);$('export-status').hidden=false;if(!persistent)message.timer=setTimeout(()=>$('export-status').hidden=true,error?7000:3200);}
 function transform(bounds,reading=false){
  const rect=$('stage').getBoundingClientRect(),s=Math.min(rect.width/bounds.w,rect.height/bounds.h)*(reading?.83:state.zoom);
  $('map-world').setAttribute('transform',`translate(${rect.width/2-(bounds.x+bounds.w/2)*s+(reading?0:state.x)} ${rect.height/2-(bounds.y+bounds.h/2)*s+(reading?-18:state.y)}) scale(${s})`);
  $('zoom-level').textContent=M.zoomPercent(s)+'%';$('zoom-level').setAttribute('aria-label',`当前比例 ${M.zoomPercent(s)}%，点击恢复原始大小`);$('zoom-level').title='100% 为样式原始字号；点击恢复原始大小';if(!reading)state.scale=s;if(state.editor)positionEditor();paintSelection();
 }
 function updateView(){if(state.mode==='markdown')return;if(state.tour){const rect=$('stage').getBoundingClientRect();transform(M.cameraBounds(state.scene.geo,state.tour[state.index],rect.width/rect.height),true);}else{const rect=$('stage').getBoundingClientRect(),p=M.zoomPolicy(state.scene.geo.bounds,rect,state.scene.fullGeo.nodes,state.scene.fullGeo.bounds);if(state.restoreScale){state.zoom=state.restoreScale/p.fit;state.restoreScale=null;}state.zoom=M.clampZoom(state.zoom,state.scene.geo.bounds,rect,state.scene.fullGeo.nodes,state.scene.fullGeo.bounds);$('zoom-in').disabled=state.zoom*p.fit>=p.maxScale-1e-8;$('zoom-out').disabled=state.zoom*p.fit<=p.minScale+1e-8;$('zoom-in').title=$('zoom-in').disabled?'已达到适合当前字号与窗口的细节比例':'放大';transform(state.scene.geo.bounds);}}
 function render(){
  const t=L.themeFor(state.recipe),geo=K.layoutTree(root,state.recipe.tokens.L.id,state.collapsed,Infinity,t.density);state.scene={root,recipe:state.recipe,theme:t,geo,fullGeo:state.collapsed.size?K.layoutTree(root,state.recipe.tokens.L.id,new Set(),Infinity,t.density):geo};
  for(const [key,value] of Object.entries({bg:t.bg,ink:t.ink,line:L.mix(t.bg,t.ink,.16),accent:L.contrast(t.accent,t.bg)>=3?t.accent:t.palette.find(c=>L.contrast(c,t.bg)>=3)||t.ink}))document.documentElement.style.setProperty('--'+key,value);
  const pattern=R.canvasPattern(t);$('stage').style.backgroundImage=pattern.image;$('stage').style.backgroundSize=pattern.size;
  $('stage').innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" ${Object.entries(R.svgAttributes(state.recipe)).map(([k,v])=>`${k}="${v}"`).join(' ')} aria-label="${esc(root.text)}"><g id="map-world">${R.svgContent(geo,t,state.recipe.tokens.L.id,state.collapsed,true)}<g id="guide-focus" aria-hidden="true"></g><g id="edit-selection" aria-hidden="true"></g></g></svg>`;
  $('map-info').textContent=`${geo.nodes.length} / ${K.descendants(root)+1} 个节点 · ${state.recipe.tokens.L.name}`;
  document.querySelectorAll('[data-style]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.style===state.recipe.code)));
  document.querySelectorAll('#stage .map-node').forEach(n=>{
   const item=model.find(n.dataset.nodeId),action=state.collapsed.has(item.id)?'展开':'收起';
   n.setAttribute('role','button');n.setAttribute('tabindex','0');n.setAttribute('aria-label',item.text+'，双击修改，Tab 增加子节点'+(item.children.length?'，空格'+action+'子节点':''));n.setAttribute('aria-keyshortcuts','F2 Tab Enter Delete'+(item.children.length?' Space ArrowLeft ArrowRight':''));n.setAttribute('aria-describedby','edit-hint');
   n.addEventListener('click',e=>{if(state.moved||state.busy)return;endTour(false);if(!finishEditing())return;selectNode(n.dataset.nodeId);if(e.target.closest('.fold-badge'))toggleNode(n.dataset.nodeId);});
   n.addEventListener('dblclick',e=>{if(e.target.closest('.fold-badge')||state.busy)return;e.preventDefault();startEditing(n.dataset.nodeId);});
   n.addEventListener('pointerenter',()=>{state.hoverBranch=n.dataset.nodeId;positionBranch();});
   n.addEventListener('pointerleave',e=>{if(e.relatedTarget?.closest?.('#branch-toggle'))return;state.hoverBranch=null;positionBranch();});
   n.addEventListener('focus',()=>{if(state.busy||state.editor||state.tour)return;state.selected=n.dataset.nodeId;state.hoverBranch=null;paintSelection();updateEditHint();});
  });updateView();paintSelection();updateEditHint();

 }
 function schedule(){clearTimeout(state.timer);if(!state.paused)state.timer=setTimeout(()=>{if(state.index<state.tour.length-1){state.index++;showStep();}else endTour();},1400);}
 function showStep(){
  const step=state.tour[state.index];document.querySelectorAll('#stage .map-node').forEach(n=>n.style.opacity=step.active.includes(n.dataset.nodeId)?'1':'.2');
  $('guide-focus').innerHTML=state.scene.geo.nodes.filter(n=>step.targets.includes(n.id)).map(n=>`<rect class="reading-focus" x="${n.x-n.w/2-9}" y="${n.y-n.h/2-9}" width="${n.w+18}" height="${n.h+18}" rx="16"/><circle class="reading-dot" cx="${n.x+n.w/2+5}" cy="${n.y-n.h/2-6}" r="4"/>`).join('');
  $('reading-count').textContent=`${state.index+1} / ${state.tour.length}`;$('reading-label').textContent=step.label;$('reading-path').textContent=step.path.join(' → ');$('reading-progress').style.width=`${(state.index+1)/state.tour.length*100}%`;
  $('previous-step').disabled=state.index===0;$('next-step').disabled=state.index===state.tour.length-1;updateView();schedule();
 }
 function endTour(restore=true){clearTimeout(state.timer);state.timer=null;state.tour=null;state.paused=false;document.body.classList.remove('tour-running');$('reading-bar').hidden=true;$('play').textContent='▶ 阅读演示';document.querySelectorAll('#stage .map-node').forEach(n=>n.style.opacity='1');if($('guide-focus'))$('guide-focus').innerHTML='';if(restore&&state.scene)updateView();}
 $('play').addEventListener('click',()=>{if(!finishEditing())return;state.selected=null;paintSelection();if(state.tour){endTour();return;}state.collapsed.clear();render();state.tour=M.readingSteps(state.scene.geo);state.index=0;state.paused=false;$('pause').textContent='暂停';$('reading-bar').hidden=false;document.body.classList.add('tour-running');$('play').textContent='■ 结束演示';showStep();});
 $('pause').addEventListener('click',()=>{state.paused=!state.paused;$('pause').textContent=state.paused?'继续':'暂停';schedule();});
 for(const [id,offset] of [['previous-step',-1],['next-step',1]])$(id).addEventListener('click',()=>{state.index=Math.max(0,Math.min(state.tour.length-1,state.index+offset));showStep();});
 $('stop').addEventListener('click',()=>endTour());
 $('map-view').addEventListener('click',showMap);
 $('markdown-view').addEventListener('click',()=>showMarkdown());
 function updateMode(){
  const editing=state.mode==='markdown';document.body.classList.toggle('markdown-mode',editing);$('stage').hidden=editing;$('markdown-panel').hidden=!editing;
  $('map-view').setAttribute('aria-pressed',String(!editing));$('markdown-view').setAttribute('aria-pressed',String(editing));
  for(const id of ['play','export-menu-toggle','expand','zoom-out','zoom-level','zoom-in','fit'])$(id).disabled=editing;
  if(editing){$('branch-toggle').hidden=true;$('export-menu').hidden=true;$('export-menu-toggle').setAttribute('aria-expanded','false');}
  updateEditHint();
 }
 function showMarkdown(draft){
  if(state.busy||state.mode==='markdown'||!finishEditing())return;endTour(false);state.hoverBranch=null;
  state.markdownBase=editableMarkdown();$('markdown-editor').value=typeof draft==='string'?draft:state.markdownBase;state.mode='markdown';
  $('markdown-error').textContent='';updateMode();$('markdown-editor').focus();$('markdown-editor').setSelectionRange(0,0);$('markdown-editor').scrollTop=0;
 }
 function applyMarkdown(){
  if(state.composing)return false;if($('markdown-editor').value===state.markdownBase)return true;
  try{const changed=model.revise($('markdown-editor').value);state.markdownBase=$('markdown-editor').value;state.collapsed=new Set([...state.collapsed].filter(id=>model.find(id)));if(changed){state.zoom=1;state.x=state.y=0;state.restoreScale=null;}syncDocument();$('markdown-error').textContent='';return true;}
  catch(error){$('markdown-error').textContent=error.message.replace(/[。；]$/,'')+'；文字已保留，修正后再切换。';$('markdown-editor').setAttribute('aria-invalid','true');return false;}
 }
 function showMap(){
  if(state.busy||state.mode!=='markdown'||!applyMarkdown())return;
  state.mode='map';$('markdown-editor').removeAttribute('aria-invalid');updateMode();render();$('stage').focus();
 }
 $('markdown-editor').addEventListener('input',()=>{$('markdown-error').textContent='';$('markdown-editor').removeAttribute('aria-invalid');updateEditHint();});
 $('markdown-editor').addEventListener('compositionstart',()=>state.composing=true);
 $('markdown-editor').addEventListener('compositionend',()=>state.composing=false);
 $('markdown-editor').addEventListener('keydown',e=>{
  if(e.isComposing||state.composing||e.keyCode===229)return;
  if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();showMap();}
  if(e.key==='Escape'){e.preventDefault();$('map-view').focus();}
  if(e.key==='Tab'){
   e.preventDefault();const f=e.target,start=f.selectionStart,end=f.selectionEnd,from=f.value.lastIndexOf('\n',start-1)+1;
   if(start===end&&!e.shiftKey)f.setRangeText('  ',start,end,'end');
   else{const text=f.value.slice(from,end),lines=text.split('\n'),out=lines.map(line=>e.shiftKey?line.replace(/^ {1,2}/,''):'  '+line).join('\n'),delta=out.split('\n')[0].length-lines[0].length;f.setRangeText(out,from,end,'preserve');f.setSelectionRange(Math.max(from,start+delta),end+out.length-text.length);}
   updateEditHint();
  }
 });
 $('expand').addEventListener('click',()=>{endTour(false);state.collapsed.clear();render();});
 function zoom(f,point){endTour(false);const rect=$('stage').getBoundingClientRect(),old=state.zoom;state.zoom=M.clampZoom(old*f,state.scene.geo.bounds,rect,state.scene.fullGeo.nodes,state.scene.fullGeo.bounds);const ratio=state.zoom/old,px=point?point.x-rect.left-rect.width/2:0,py=point?point.y-rect.top-rect.height/2:0;state.x=px-(px-state.x)*ratio;state.y=py-(py-state.y)*ratio;updateView();}
 $('zoom-in').addEventListener('click',()=>zoom(1.2));$('zoom-out').addEventListener('click',()=>zoom(1/1.2));$('fit').addEventListener('click',()=>{endTour(false);state.zoom=1;state.x=state.y=0;updateView();});
 $('zoom-level').addEventListener('click',()=>{const rect=$('stage').getBoundingClientRect(),fit=M.zoomPolicy(state.scene.geo.bounds,rect,state.scene.fullGeo.nodes,state.scene.fullGeo.bounds).fit;zoom(1/(fit*state.zoom));});
 $('stage').addEventListener('wheel',e=>{if(state.editor)return;e.preventDefault();zoom(e.deltaY<0?1.08:1/1.08,{x:e.clientX,y:e.clientY});},{passive:false});
 $('stage').addEventListener('pointerdown',e=>{state.moved=false;if(e.target.closest('.map-node')||state.busy)return;if(!finishEditing())return;state.selected=null;paintSelection();updateEditHint();endTour(false);state.drag={x:e.clientX,y:e.clientY,px:state.x,py:state.y};$('stage').setPointerCapture(e.pointerId);});
 $('stage').addEventListener('pointermove',e=>{if(!state.drag)return;const p=state.drag;state.x=p.px+e.clientX-p.x;state.y=p.py+e.clientY-p.y;state.moved=Math.abs(e.clientX-p.x)+Math.abs(e.clientY-p.y)>4;updateView();});
 for(const event of ['pointerup','pointercancel'])$('stage').addEventListener(event,()=>state.drag=null);
 $('stage').addEventListener('keydown',e=>{if(e.target!==$('stage'))return;const delta={ArrowLeft:[40,0],ArrowRight:[-40,0],ArrowUp:[0,40],ArrowDown:[0,-40]}[e.key];if(delta){e.preventDefault();endTour(false);state.x+=delta[0];state.y+=delta[1];updateView();}});
 new ResizeObserver(()=>{if(state.scale&&state.zoom!==1&&!state.tour)state.restoreScale=state.scale;updateView();}).observe($('stage'));
 function save(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);}
 const filename=()=>root.text.replace(/[\\/:*?"<>|\x00-\x1f]/g,'_').slice(0,60)||'mindmap';
 function selectedMarkdown(){return model.markdown(state.recipe.code);}
 function editableMarkdown(){return selectedMarkdown().replace(/^---\r?\n([\s\S]*?)\r?\n---\s*/,(_,body)=>{const fields=body.split(/\r?\n/).filter(line=>!/^\s*(?:style|preset|layout|theme):/.test(line)).join('\n').trim();return fields?'---\n'+fields+'\n---\n\n':'';});}
 function syncDocument(){
  root=model.root();boot.document=model.document();boot.source=selectedMarkdown();boot.recipeCode=state.recipe.code;
  $('atlas-boot').textContent='window.ATLAS_BOOT='+JSON.stringify(boot).replace(/</g,'\\u003c')+';';updateTitle();updateEditHint();
 }
 function updateEditHint(){
  const dirty=savedSignature!==undefined&&signature()!==savedSignature;
  $('save-html').textContent=dirty?'保存 HTML ·':'保存 HTML';
  const n=model.find(state.selected),fold=n?.children.length?`空格${state.collapsed.has(n.id)?'展开':'收起'} · `:'';
  if(state.mode==='markdown')$('map-info').textContent='Markdown · '+$('markdown-editor').value.length+' 字符';
  $('markdown-help').textContent=$('markdown-editor').value!==state.markdownBase?'尚未应用 · 点击上方样式查看修改；保存 HTML 也会保留草稿。':'与导图共用文字和层级 · 修改后点击上方样式查看。';
  $('edit-hint').textContent=state.mode==='markdown'?'Tab 缩进 · Ctrl/⌘ Enter 查看导图 · Ctrl/⌘ S 保存':state.editor?'Enter 完成改字 · Esc 取消':state.selected?fold+'双击 / F2 改字 · Tab 子节点 · Ctrl/⌘ S 保存':'单击选中 · 双击改字 · 节点旁 − / 数字折叠展开';
 }
 function parentOf(id,n=root){for(const child of n.children){if(child.id===id)return n;const found=parentOf(id,child);if(found)return found;}return null;}
 function paintSelection(){
  const layer=$('edit-selection');if(!layer)return;const n=state.scene.geo.nodes.find(n=>n.id===state.selected);
  const scale=$('map-world').getScreenCTM()?.a||1,pad=4/scale;
  layer.innerHTML=n?`<rect class="selection-ring" vector-effect="non-scaling-stroke" x="${n.x-n.w/2-pad}" y="${n.y-n.h/2-pad}" width="${n.w+pad*2}" height="${n.h+pad*2}" rx="${6/scale}"/>`:'';
  positionBranch();
 }
 function positionBranch(){
  const button=$('branch-toggle'),id=state.hoverBranch||state.selected,n=state.scene?.geo.nodes.find(n=>n.id===id);
  document.querySelectorAll('.has-fold-control').forEach(el=>el.classList.remove('has-fold-control'));
  if(state.mode==='markdown'||!n?.children.length||state.editor||state.tour||state.busy||state.drag){button.hidden=true;return;}
  const element=document.querySelector(`#stage [data-node-id="${id}"]`),box=element?.querySelector('.node-hit')?.getBoundingClientRect(),stage=$('stage').getBoundingClientRect();
  if(!box||box.right<stage.left||box.left>stage.right||box.bottom<stage.top||box.top>stage.bottom){button.hidden=true;return;}
  const layout=state.recipe.tokens.L.id,left=layout==='outline'||(n.direction||1)<0,down=layout==='down';
  const hidden=state.collapsed.has(id),count=K.descendants(model.find(id)),offset=hidden?24:18;
  let x=down?box.x+box.width/2:left?box.left-offset:box.right+offset,y=down?box.bottom+offset:box.y+box.height/2;
  button.style.left=Math.max(stage.left+22,Math.min(stage.right-22,x))+'px';button.style.top=Math.max(stage.top+22,Math.min(stage.bottom-22,y))+'px';
  const label=`${hidden?'展开':'收起'}“${model.find(id).text}”的 ${count} 个子节点`;
  button.dataset.nodeId=id;button.dataset.collapsed=String(hidden);button.querySelector('.branch-mark').textContent=hidden?'+'+count:'−';button.setAttribute('aria-label',label);button.setAttribute('aria-expanded',String(!hidden));button.title=label+' · 空格';button.hidden=false;element.classList.add('has-fold-control');
 }
 $('branch-toggle').addEventListener('pointerenter',()=>state.hoverBranch=$('branch-toggle').dataset.nodeId);
 $('branch-toggle').addEventListener('pointerleave',()=>{state.hoverBranch=null;positionBranch();});
 $('branch-toggle').addEventListener('click',()=>{if(state.busy||!finishEditing())return;endTour(false);toggleNode($('branch-toggle').dataset.nodeId);});
 function selectNode(id,focus=true){state.selected=id;if(focus)state.hoverBranch=null;paintSelection();updateEditHint();if(focus)document.querySelector(`#stage [data-node-id="${id}"]`)?.focus({preventScroll:true});}
 function toggleNode(id){
  if(!model.find(id)?.children.length)return;
  const old=state.scene.geo.nodes.find(n=>n.id===id),matrix=$('map-world').getScreenCTM(),rect=$('stage').getBoundingClientRect(),point=old&&matrix?{x:old.x*matrix.a+matrix.e-rect.left,y:old.y*matrix.d+matrix.f-rect.top}:null;
  state.collapsed.has(id)?state.collapsed.delete(id):state.collapsed.add(id);state.selected=id;state.hoverBranch=null;render();
  const next=state.scene.geo.nodes.find(n=>n.id===id);if(point&&next){Object.assign(state,M.anchoredView(state.scene.geo.bounds,rect,point,next,matrix.a,state.scene.fullGeo.nodes,state.scene.fullGeo.bounds));updateView();}selectNode(id);
 }
 function changed(id){
  endTour(false);syncDocument();state.collapsed=new Set([...state.collapsed].filter(id=>model.find(id)));state.selected=model.find(id)?id:root.id;render();selectNode(state.selected);
 }
 function positionEditor(){
  if(!state.editor)return;const hit=document.querySelector(`#stage [data-node-id="${state.editor.id}"] .node-hit`);if(!hit)return;
  const box=hit.getBoundingClientRect(),field=$('node-editor'),width=Math.min(window.innerWidth-32,Math.max(200,Math.min(440,box.width)));
  field.style.width=width+'px';field.style.left=Math.max(16,Math.min(window.innerWidth-width-16,box.x+box.width/2-width/2))+'px';
  field.style.height='auto';field.style.height=Math.min(180,Math.max(46,field.scrollHeight+2))+'px';
  const height=parseFloat(field.style.height);field.style.top=Math.max(90,Math.min(window.innerHeight-height-65,box.y+box.height/2-height/2))+'px';
 }
 function startEditing(id){
  if(state.busy||!finishEditing())return;endTour(false);selectNode(id,false);const n=model.find(id);if(!n)return;
  state.editor={id};positionBranch();const field=$('node-editor');field.hidden=false;field.value=n.text;field.style.fontFamily=L.themeFor(state.recipe).font;positionEditor();field.focus();field.select();updateEditHint();
 }
 function finishEditing(accept=true){
  if(!state.editor)return true;if(state.editor.composing)return false;
  const id=state.editor.id,field=$('node-editor');
  if(accept){try{model.rename(id,field.value.replace(/[\r\n\t]+/g,' ').trim());}catch(error){message(error.message,true);queueMicrotask(()=>field.focus());return false;}}
  state.editor=null;field.hidden=true;field.value='';if(accept)changed(id);else{selectNode(id);updateEditHint();}return true;
 }
 $('node-editor').addEventListener('input',positionEditor);
 $('node-editor').addEventListener('compositionstart',()=>{if(state.editor)state.editor.composing=true;});
 $('node-editor').addEventListener('compositionend',()=>{if(state.editor)state.editor.composing=false;});
 $('node-editor').addEventListener('blur',()=>finishEditing());
 $('node-editor').addEventListener('keydown',e=>{if(e.isComposing||e.keyCode===229)return;if(e.key==='Enter'){e.preventDefault();finishEditing();}else if(e.key==='Escape'){e.preventDefault();e.stopPropagation();finishEditing(false);}});
 $('document-title').addEventListener('dblclick',()=>{if(state.mode==='map')startEditing(root.id);});
 document.addEventListener('keydown',e=>{
  const typing=e.target.closest('textarea,input,[contenteditable=true]');if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();if(!state.busy)saveHTML();return;}
  if(typing||state.busy||e.isComposing)return;
  if((e.ctrlKey||e.metaKey)&&['z','y'].includes(e.key.toLowerCase())){e.preventDefault();const redo=e.key.toLowerCase()==='y'||e.shiftKey;if(redo?model.redo():model.undo()){changed(state.selected);message(redo?'已重做':'已撤销');}return;}
  const item=e.target.closest('#stage .map-node');if(!item)return;const id=item.dataset.nodeId;selectNode(id,false);
  if(e.key==='F2'){e.preventDefault();startEditing(id);return;}
  if(e.key==='Escape'){e.preventDefault();state.selected=null;state.hoverBranch=null;paintSelection();updateEditHint();$('stage').focus();return;}
  if(e.key===' '){e.preventDefault();toggleNode(id);return;}
  if(e.key==='Tab'&&!e.shiftKey||e.key==='Enter'){
   e.preventDefault();try{const kind=e.key==='Tab'||id===root.id?'child':'sibling',next=model.add(id,kind);state.collapsed.delete(kind==='child'?id:parentOf(id)?.id);changed(next);startEditing(next);}catch(error){message(error.message,true);}return;
  }
  if(['Delete','Backspace'].includes(e.key)){e.preventDefault();try{const count=K.descendants(model.find(id))+1,parent=model.remove(id);changed(parent);message(`已删除 ${count} 个节点 · Ctrl/⌘ Z 撤销`);}catch(error){message(error.message,true);}return;}
  if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){
   e.preventDefault();let next;
   if(e.key==='ArrowLeft'){if(model.find(id).children.length&&!state.collapsed.has(id)){toggleNode(id);return;}next=parentOf(id)?.id;}
   else if(e.key==='ArrowRight'){if(state.collapsed.has(id)){toggleNode(id);return;}next=model.find(id).children[0]?.id;}
   else{const ids=state.scene.geo.nodes.map(n=>n.id),at=ids.indexOf(id);next=ids[at+(e.key==='ArrowDown'?1:-1)];}
   if(next)selectNode(next);
  }
 });
 function saveHTML(){
  if(!finishEditing()||state.composing)return;if(state.mode==='markdown')applyMarkdown();syncDocument();const doc=document.documentElement.cloneNode(true);
  doc.querySelector('#stage').innerHTML='';doc.querySelector('#style-choices').innerHTML='';doc.querySelector('#reading-bar').hidden=true;doc.querySelector('#play').textContent='▶ 阅读演示';doc.querySelectorAll('button').forEach(b=>b.disabled=false);doc.querySelector('#branch-toggle').hidden=true;doc.querySelector('#export-menu-toggle').setAttribute('aria-expanded','false');doc.querySelector('#export-status').hidden=true;doc.querySelector('#export-menu').hidden=true;doc.querySelector('#node-editor').hidden=true;doc.querySelector('#node-editor').textContent='';doc.querySelector('body').classList.remove('tour-running');
  const data={...boot,source:selectedMarkdown(),document:model.document(),recipeCode:state.recipe.code,selectedRecipeCode:state.recipe.code,editorView:state.mode,...(state.mode==='markdown'&&$('markdown-editor').value!==state.markdownBase?{markdownDraft:$('markdown-editor').value}:{}),view:{collapsed:[...state.collapsed],zoom:state.zoom,scale:state.scale,x:state.x,y:state.y}};
  if(state.mode!=='markdown'||$('markdown-editor').value===state.markdownBase)delete data.markdownDraft;doc.querySelector('body').classList.remove('markdown-mode');doc.querySelector('#markdown-editor').textContent='';doc.querySelector('#markdown-error').textContent='';doc.querySelector('#stage').hidden=false;doc.querySelector('#markdown-panel').hidden=true;
  doc.querySelector('#atlas-boot').textContent='window.ATLAS_BOOT='+JSON.stringify(data).replace(/</g,'\\u003c')+';';
  save(new Blob(['<!doctype html>\n'+doc.outerHTML],{type:'text/html;charset=utf-8'}),filename()+'.html');savedSignature=signature();updateEditHint();message(state.mode==='markdown'&&$('markdown-editor').value!==state.markdownBase?'已生成 HTML 下载，含尚未应用的 Markdown 草稿':'已生成最新 HTML 下载，请保留这份文件继续编辑');
 }
 $('save-html').addEventListener('click',()=>{if(!state.busy)saveHTML();});
 window.addEventListener('beforeunload',e=>{if(window.top!==window)return;if(signature()!==savedSignature||state.editor&&$('node-editor').value!==model.find(state.editor.id).text){e.preventDefault();e.returnValue='';}});
 function fonts(){/* Keep each embedded font's license with its face definition. */const css=document.querySelector('head style').textContent,t=L.themeFor(state.recipe);return [...css.matchAll(/\/\*[\s\S]*?\*\/\s*@font-face\{[^}]+\}/g)].map(m=>m[0]).filter(rule=>t.font.includes(rule.match(/font-family:'([^']+)'/)[1])||rule.includes("'Atlas Business'")).join('\n');}
 async function imageFor(text){const url=URL.createObjectURL(new Blob([text],{type:'image/svg+xml'}));try{const image=new Image();image.src=url;await image.decode();return image;}catch{throw new Error('导图图像暂时无法生成，请重新打开 HTML 后重试。');}finally{URL.revokeObjectURL(url);}}
 function encode(canvas,type){return new Promise((resolve,reject)=>{canvas.toBlob(blob=>blob&&blob.type===type?resolve(blob):reject(new Error(type==='image/webp'?'当前浏览器不支持 WebP 动图编码，请使用较新的 Chrome 或 Edge。':'图像编码失败，请重新打开 HTML 后重试。')),type,1);});}
 function rounded(ctx,x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);}
 async function exportFile(format){
  if(state.busy||!finishEditing())return;if(!['png','animated-webp'].includes(format))return;state.busy=true;positionBranch();clearTimeout(state.timer);const buttons=[...document.querySelectorAll('.reader-actions button,.style-choices button,[data-export],#save-html')];buttons.forEach(b=>b.disabled=true);$('export-menu').hidden=true;$('export-menu-toggle').setAttribute('aria-expanded','false');message('正在准备完整导图…',false,true);
  try{
   const snapshot=M.scene(root,state.recipe),fontCSS=fonts(),animated=format==='animated-webp';
   const plan=animated?M.animationPlan(snapshot.geo):M.imagePlan(snapshot.geo.bounds,snapshot.geo.nodes);
   await document.fonts.ready;
   {
    const size={width:plan.width,height:plan.height},canvas=document.createElement('canvas');canvas.width=size.width;canvas.height=size.height;const ctx=canvas.getContext('2d');if(!ctx)throw new Error('浏览器无法创建图像画布，请重试或使用较新的浏览器。');
    const clear=()=>{ctx.globalAlpha=1;ctx.fillStyle=snapshot.theme.bg;ctx.fillRect(0,0,canvas.width,canvas.height);};
    if(!animated){const image=await imageFor(M.svg(snapshot,fontCSS,false,size));clear();ctx.drawImage(image,0,0);save(await encode(canvas,'image/png'),filename()+'.png');image.src='';}
    else{
     const frames=[],steps=plan.steps,accent=L.contrast(snapshot.theme.accent,snapshot.theme.bg)>=3?snapshot.theme.accent:snapshot.theme.ink,header=64,pixels={width:size.width,height:size.height-header};
     const record=async duration=>frames.push({bytes:new Uint8Array(await(await encode(canvas,'image/webp')).arrayBuffer()),duration});
     function caption(text,count){ctx.save();ctx.fillStyle=snapshot.theme.bg;ctx.fillRect(0,0,size.width,header);ctx.fillStyle=snapshot.theme.ink;ctx.font=`20px ${snapshot.theme.font}`;ctx.textBaseline='middle';let label=text;while(label.length&&ctx.measureText(label).width>size.width-170)label=label.slice(0,-1);ctx.fillText(label===text?label:label+'…',24,header/2);ctx.textAlign='right';ctx.fillText(count,size.width-24,header/2);ctx.restore();}
     async function overview(duration){const image=await imageFor(M.svg(snapshot,fontCSS,false,pixels));clear();ctx.drawImage(image,0,header);caption(root.text,'全图');await record(duration);image.src='';}
     await overview(900);
     for(let i=0;i<steps.length;i++){
      const step=steps[i],b=plan.cameras[i],sx=pixels.width/b.w,sy=pixels.height/b.h;
      message(`正在导出阅读动图 ${i+1} / ${steps.length}…`,false,true);
      // Re-render this vector viewport at final resolution; never enlarge a thumbnail.
      const image=await imageFor(M.svg(snapshot,fontCSS,false,pixels,b));
      for(let phase=0;phase<2;phase++){
       const base=()=>{clear();ctx.drawImage(image,0,header);};base();
       ctx.fillStyle=snapshot.theme.bg;ctx.globalAlpha=.5;ctx.fillRect(0,header,canvas.width,pixels.height);ctx.globalAlpha=1;
       for(const n of snapshot.geo.nodes.filter(n=>step.active.includes(n.id))){ctx.save();rounded(ctx,(n.x-n.w/2-b.x-16)*sx,header+(n.y-n.h/2-b.y-32)*sy,(n.w+32)*sx,(n.h+48)*sy,10);ctx.clip();ctx.drawImage(image,0,header);ctx.restore();}
       ctx.strokeStyle=accent;ctx.fillStyle=accent;ctx.lineWidth=2;ctx.setLineDash([6,6]);ctx.lineDashOffset=-phase*5;
       for(const n of snapshot.geo.nodes.filter(n=>step.targets.includes(n.id))){rounded(ctx,(n.x-n.w/2-b.x-9)*sx,header+(n.y-n.h/2-b.y-9)*sy,(n.w+18)*sx,(n.h+18)*sy,12);ctx.stroke();ctx.beginPath();ctx.arc((n.x+n.w/2-b.x+5)*sx,header+(n.y-n.h/2-b.y-6)*sy,phase?5:3,0,Math.PI*2);ctx.fill();}
       ctx.setLineDash([]);caption(step.path.join(' → '),`${i+1} / ${steps.length}`);await record(phase?950:250);
      }
      image.src='';await new Promise(resolve=>setTimeout(resolve,0));
     }
     await overview(1800);save(new Blob([M.animatedWebP(frames,size.width,size.height)],{type:'image/webp'}),filename()+'-阅读演示.webp');
    }
   }
   message(`${format==='animated-webp'?'阅读动图':'完整导图'}已导出 · ${plan.width} × ${plan.height}${plan.limited?' · 已达像素上限，细节请用 HTML 放大阅读':''}`);
  }catch(error){message(error.message,true);}finally{state.busy=false;buttons.forEach(b=>b.disabled=false);positionBranch();if(state.tour)schedule();}
 }
 $('export-menu-toggle').addEventListener('click',()=>{const open=$('export-menu').hidden;$('export-menu').hidden=!open;$('export-menu-toggle').setAttribute('aria-expanded',String(open));if(open)$('export-menu').style.top=($('export-menu-toggle').getBoundingClientRect().bottom+8)+'px';});
 document.querySelectorAll('[data-export]').forEach(b=>b.addEventListener('click',()=>exportFile(b.dataset.export)));
 document.addEventListener('pointerdown',e=>{if(!e.target.closest('#export-menu,.export-group')){$('export-menu').hidden=true;$('export-menu-toggle').setAttribute('aria-expanded','false');}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){$('export-menu').hidden=true;$('export-menu-toggle').setAttribute('aria-expanded','false');endTour();}});
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.tour){state.paused=true;$('pause').textContent='继续';clearTimeout(state.timer);}});
 render();if(boot.editorView==='markdown'||typeof boot.markdownDraft==='string')showMarkdown(boot.markdownDraft);savedSignature=signature();updateEditHint();
})();
