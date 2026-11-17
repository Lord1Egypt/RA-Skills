(function(){
  'use strict';
  const K=window.MindmapKit,Lib=K.library,boot=window.ATLAS_BOOT,$=id=>document.getElementById(id),esc=K.escapeXML;
  let initial=Lib.resolveRecipe(boot.recipeCode||boot.preset||(boot.theme?Lib.legacy[boot.theme]:'P07'));
  if(boot.layout)initial=Lib.replaceToken(initial,'L',Lib.axes.L.items.find(l=>l.id===boot.layout)?.code||'L01');
  const state={recipe:initial,source:boot.source,root:K.parseMindmap(boot.source),collapsed:new Set(),zoom:1,panX:0,panY:0,overview:false,geometry:null,pointer:null,dragged:false,task:'all',search:'',catalogueView:'compare'};
  (function fold(n){if(n.depth===2&&n.children.length)state.collapsed.add(n.id);n.children.forEach(fold);})(state.root);
  if(boot.standalone)document.body.classList.add('standalone');
  const featured=Lib.selectedPresets(),samples=boot.showcase||[],sampleFor=id=>samples.find(s=>s.preset===id);
  const displayName=p=>p.name.split(' · ')[0];
  const ordinal=index=>String(index+1).padStart(2,'0');
  const presetLabel=p=>Picker.presetLabel(p);
  const Picker=window.StylePicker;
  const byTheme=()=>Lib.themeFor(state.recipe),byLayout=()=>K.layouts.find(l=>l.id===state.recipe.tokens.L.id);
  const tag=(name,attrs,body='')=>`<${name} ${Object.entries(attrs).map(([k,v])=>`${k}="${esc(v)}"`).join(' ')}>${body}</${name}>`;
  const {svgContent,staticSVG,canvasPattern,svgAttributes}=window.MindmapRenderer;
  const specimenFor=recipe=>{const sample=sampleFor(recipe.preset?.id);if(sample)return K.parseMindmap(sample.previewSource);const p=recipe.preset?.positioning;return p?K.parseMindmap(p.specimens[recipe.tokens.T.language==='en'?'en':'zh']):littleTree;};
  const recommended=Lib.recommendations.items;
  const quickPresets=recommended.map(item=>featured.find(p=>p.id===item.preset));
  const startLabel=p=>{const rec=recommended.find(item=>item.preset===p.id);return `${presetLabel(p)} · ${rec?.scenario||p.positioning.useCase}${rec?.preset==='P61'?'（上手首选）':''}`;};
  const fontCaption=recipe=>`${recipe.tokens.T.language==='en'?'English':'中文'} · ${recipe.tokens.T.family||recipe.tokens.T.name}`;
  const littleTree=K.parseMindmap('```mermaid\nmindmap\n  root((知识主题))\n    核心观点\n      支撑依据\n    应用方法\n      实践反馈\n```');
  function setupSelectors(){
    $('layout-tabs').innerHTML=Lib.axes.L.items.map((l,index)=>{const r=Lib.replaceToken(Lib.resolveRecipe('P07'),'L',l.code);return `<button class="layout-option" data-layout="${l.code}" aria-pressed="false">${staticSVG(littleTree,r,1)}<span><strong>${l.name}</strong><small>${l.code}</small></span></button>`;}).join('');
    $('theme-grid').innerHTML=quickPresets.map((p,index)=>`<button class="theme-option" data-preset="${p.id}" aria-pressed="false" title="${esc(p.description)}"><span class="theme-sample">${staticSVG(specimenFor(Lib.resolveRecipe(p.id)),Lib.resolveRecipe(p.id),1)}</span><span class="theme-meta"><strong>${esc(displayName(p))}</strong><small>${p.uid} · ${esc(recommended[index].scenario)}</small></span></button>`).join('');
    $('design-studies').innerHTML=featured.slice(0,8).map(p=>{const id=p.id;return `<article class="design-study"><button data-study="${id}" aria-label="应用精修 ${esc(p.name)}">${staticSVG(specimenFor(Lib.resolveRecipe(id)),Lib.resolveRecipe(id),1)}</button><div><span>${p.uid} / ${esc(fontCaption(Lib.resolveRecipe(id)))}</span><h3>${esc(p.name.split(' · ')[0])}</h3><p>${id==='P61'?'饱满圆角，留白与清晰轮廓':id==='P48'?'奶油色中心，自然舒展的彩枝':id==='P40'?'石板底色，明亮而圆润的枝条':id==='P53'?'深黑留白，轻快字体与彩色弧线':id==='P39'?'鲜明实色卡片，轻松的视觉节奏':id==='P60'?'柔和粉彩，带一点手作的缝边':id==='P65'?'黑墨轮廓、亮色点睛，像随手画在纸上':id==='P67'?'豆芽小搭子与纸片圈注，把脑洞轻轻画出来':'蓝灰纸面、暖灰小毛驴，留一点生活的小趣味'}</p></div></article>`}).join('');
    document.querySelectorAll('[data-study]').forEach(b=>b.addEventListener('click',()=>{usePreset(b.dataset.study);$('playground').scrollIntoView({behavior:'smooth'});}));
    $('preset-total').textContent=featured.length;$('all-presets-link').textContent=`查看 ${featured.length} 个精选预设 ↗`;
    $('preset-options').innerHTML=Lib.tasks.map(task=>`<div role="group" aria-labelledby="preset-group-${task.id}"><h4 id="preset-group-${task.id}">${esc(task.name)}<span>4 套</span></h4>${featured.filter(p=>p.positioning.task===task.id).map(p=>`<button type="button" role="option" data-preset-choice="${p.id}" aria-label="${esc(startLabel(p))}" aria-selected="false" tabindex="-1"><i class="preset-swatch" style="--swatch:${Lib.themeFor(Lib.resolveRecipe(p.id)).palette[0]}" aria-hidden="true"></i><span class="preset-option-copy"><strong>${esc(displayName(p))}</strong><small>${esc(recommended.find(r=>r.preset===p.id)?.scenario||p.positioning.useCase)}${p.id==='P61'?' · 上手首选':''}</small></span><span class="preset-option-uid">${p.uid}</span><span class="preset-option-check" aria-hidden="true">✓</span></button>`).join('')}</div>`).join('');
    $('preset-options').querySelectorAll('[data-preset-choice]').forEach(b=>b.addEventListener('click',()=>{closePresetPicker(true);usePreset(b.dataset.presetChoice);}));
    $('preset-scenarios').innerHTML=Lib.tasks.map(task=>`<button type="button" data-pick-task="${task.id}" aria-pressed="false">${esc(task.name)}</button>`).join('');
    document.querySelectorAll('[data-pick-task]').forEach(b=>b.addEventListener('click',()=>usePreset(Lib.tasks.find(t=>t.id===b.dataset.pickTask).start)));
    $('component-controls').innerHTML=Lib.order.map(axis=>`<div class="component-field"><span class="component-heading"><small aria-hidden="true">${axis}</small>${Lib.axes[axis].name}</span><button type="button" class="component-picker" data-axis="${axis}" role="combobox" aria-label="${Lib.axes[axis].name}" aria-haspopup="listbox" aria-expanded="false" aria-controls="component-menu"></button></div>`).join('');
    document.querySelectorAll('[data-gallery-view]').forEach(b=>b.addEventListener('click',()=>{state.catalogueView=b.dataset.galleryView;updateGalleryView();}));
    $('family-filters').innerHTML=[{id:'all',name:'全部样式'},...Lib.tasks].map(t=>`<button data-task="${t.id}" aria-pressed="${t.id===state.task}">${t.name}</button>`).join('');
    $('task-guide').innerHTML=Lib.tasks.map((t,i)=>`<button class="task-guide-item" data-task="${t.id}" aria-pressed="false"><span class="task-number">${ordinal(i)}</span><strong>${esc(t.prompt)}</strong><span>${esc(t.hint)}</span><small>查看 4 套样式 <span aria-hidden="true">↗</span></small></button>`).join('');
    document.querySelectorAll('[data-layout]').forEach(b=>b.addEventListener('click',()=>{const old=state.recipe.tokens.E.code;state.recipe=Lib.replaceToken(state.recipe,'L',b.dataset.layout);render();if(old!==state.recipe.tokens.E.code)notify('已切换为该结构适用的连线');}));
    document.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>usePreset(b.dataset.preset)));
    document.querySelectorAll('[data-axis]').forEach(button=>{button.addEventListener('click',()=>openPicker(button.dataset.axis));button.addEventListener('keydown',e=>{if(['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();openPicker(button.dataset.axis,false);}});});
    document.querySelectorAll('[data-task]').forEach(b=>b.addEventListener('click',()=>{state.task=b.dataset.task;state.search='';$('catalogue-search').value='';buildCatalogue();if(state.task!=='all')usePreset(Lib.tasks.find(t=>t.id===state.task).start);}));
    $('preset-select').addEventListener('click',()=>presetOpen?closePresetPicker(true):openPresetPicker());
    $('preset-select').addEventListener('keydown',e=>{if(['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();openPresetPicker();}});
  }
  let presetOpen=false;
  function closePresetPicker(returnFocus=false){
    presetOpen=false;$('preset-menu').hidden=true;$('preset-select').setAttribute('aria-expanded','false');
    if(returnFocus)$('preset-select').focus({preventScroll:true});
  }
  function syncPresetPicker(){
    const p=featured.find(p=>p.id===state.recipe.preset?.id),button=$('preset-select');button.value=p?.id||'custom';
    button.innerHTML=`<i class="preset-swatch" style="--swatch:${byTheme().palette[0]}" aria-hidden="true"></i><span class="preset-trigger-copy"><strong id="preset-selected-name">${esc(p?displayName(p):'已导入样式')}</strong><small>${esc(p?p.uid+' · '+p.positioning.useCase:'保留当前外观')}</small></span><span class="preset-chevron" aria-hidden="true">⌄</span>`;
    $('preset-options').querySelectorAll('[data-preset-choice]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.presetChoice===p?.id)));
  }
  function positionPresetPicker(){
    if(!presetOpen)return;
    const r=$('preset-select').getBoundingClientRect(),menu=$('preset-menu'),vh=window.innerHeight,vw=document.documentElement.clientWidth;
    if(r.bottom<0||r.top>vh){closePresetPicker();return;}
    const width=menu.getBoundingClientRect().width,below=Math.max(0,vh-r.bottom-18),above=Math.max(0,r.top-18),up=below<400&&above>below;
    let height=Math.min(540,up?above:below),top=up?r.top-height-6:r.bottom+6;
    if(height<150){height=vh-24;top=12;}
    Object.assign(menu.style,{maxHeight:height+'px',left:Math.max(12,Math.min(r.right-width,vw-width-12))+'px',top:Math.max(12,top)+'px'});
  }
  function openPresetPicker(){
    closePicker();presetOpen=true;$('preset-menu').hidden=false;$('preset-select').setAttribute('aria-expanded','true');positionPresetPicker();
    const selected=$('preset-options').querySelector('[aria-selected="true"]')||$('preset-options').querySelector('[role="option"]');
    selected.focus({preventScroll:true});$('preset-options').scrollTop=Math.max(0,selected.offsetTop-$('preset-options').clientHeight/2+selected.offsetHeight/2);
  }
  $('preset-options').addEventListener('keydown',e=>{
    if(e.key==='Escape'){e.preventDefault();closePresetPicker(true);return;}
    if(e.key==='Tab'){closePresetPicker(true);return;}
    const options=[...$('preset-options').querySelectorAll('[role="option"]')],at=options.indexOf(document.activeElement);let next;
    if(e.key==='ArrowDown')next=(at+1)%options.length;if(e.key==='ArrowUp')next=(at-1+options.length)%options.length;
    if(e.key==='Home')next=0;if(e.key==='End')next=options.length-1;
    if(next!==undefined){e.preventDefault();options[next].focus({preventScroll:true});options[next].scrollIntoView({block:'nearest'});}
  });
  document.addEventListener('pointerdown',e=>{if(presetOpen&&!$('preset-menu').contains(e.target)&&!$('preset-select').contains(e.target))closePresetPicker();});
  window.addEventListener('resize',positionPresetPicker);
  window.addEventListener('scroll',e=>{if(!$('preset-menu').contains(e.target))positionPresetPicker();},true);
  let openAxis=null;
  function updatePickerTriggers(){
    document.querySelectorAll('[data-axis]').forEach(button=>{
      const axis=button.dataset.axis,item=state.recipe.tokens[axis],view=Picker.describe(axis,item,state.recipe.tokens.L.id);
      button.value=item.code;button.title=`${view.label} · ${view.hint}`;
      button.innerHTML=`<span class="picker-mini">${Picker.preview(axis,item,state.recipe.tokens.L.id)}</span><span class="picker-current"><small class="picker-code">${esc(view.code)}</small><span>${esc(view.name)}</span></span><svg class="picker-chevron" viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4 3 3 3-3"/></svg>`;
    });
  }
  function updateRecipeMatch(){
    const pending=$('recipe-code').value.trim()!==state.recipe.code,matched=featured.find(p=>p.code===state.recipe.code);
    $('copy-recipe').disabled=pending;
    $('recipe-match').textContent=pending?'代号待应用 · 点击“应用代号”后更新模板与预览':matched?`已匹配模板：${presetLabel(matched)}`:state.recipe.preset?`兼容模板：${presetLabel(state.recipe.preset)}（非当前 16 套）`:'自定义组合 · 未匹配默认模板';
    $('recipe-match').dataset.state=pending?'pending':matched?'matched':'custom';
  }
  function closePicker(returnFocus=false){
    const button=openAxis?document.querySelector(`[data-axis="${openAxis}"]`):null,menu=$('component-menu');
    if(button)button.setAttribute('aria-expanded','false');
    menu.hidden=true;openAxis=null;if(returnFocus&&button)button.focus({preventScroll:true});
  }
  function openPicker(axis,toggle=true){
    closePresetPicker();
    if(openAxis===axis&&toggle){closePicker(true);return;}
    closePicker();openAxis=axis;
    const button=document.querySelector(`[data-axis="${axis}"]`),menu=$('component-menu'),layout=state.recipe.tokens.L.id,items=Picker.itemsFor(axis,state.recipe);
    button.setAttribute('aria-expanded','true');menu.setAttribute('aria-label',Lib.axes[axis].name+'选项');menu.dataset.axisMenu=axis;
    const fontColumns=axis==='T'&&items.every(item=>Lib.selection.axes.T.includes(item.code));menu.classList.toggle('font-columns',fontColumns);
    menu.innerHTML=`<div class="picker-menu-head" aria-hidden="true"><strong>${axis}${Lib.axes[axis].name}</strong><span>${items.length} 种可选</span></div><div class="picker-menu-list">${items.map((item,index)=>{
      const view=Picker.describe(axis,item,layout),selected=item.code===state.recipe.tokens[axis].code,imported=!Lib.selection.axes[axis].includes(item.code);
      const languageTitle=fontColumns&&(index===0||index===4)?`<div class="picker-language" aria-hidden="true">${index===0?'中文 · 四种字形':'English · Four typefaces'}</div>`:'';
      return `${languageTitle}<button type="button" role="option" aria-label="${esc(view.label)}" aria-describedby="hint-${item.code}" aria-selected="${selected}" tabindex="-1" data-choice="${item.code}"><span class="picker-example">${Picker.preview(axis,item,layout)}</span><span class="picker-option-text"><strong><span class="picker-code">${esc(view.code)}</span>${esc(view.name)}${imported?'<em>已导入</em>':''}</strong><small id="hint-${item.code}">${esc(view.hint)}</small></span><span class="picker-check" aria-hidden="true">${selected?'✓':''}</span></button>`;
    }).join('')}</div><div class="picker-menu-foot" aria-hidden="true">${axis==='E'&&['brace','outline'].includes(layout)?'当前结构已匹配可用连线':'点击即应用 · 随时可以换'}</div>`;
    button.parentElement.append(menu);menu.hidden=false;
    positionPicker();
    menu.querySelectorAll('[data-choice]').forEach(option=>option.addEventListener('click',()=>{
      const old=state.recipe.tokens.E.code;state.recipe=Lib.replaceToken(state.recipe,axis,option.dataset.choice);closePicker(true);render();
      if(axis==='L'&&old!==state.recipe.tokens.E.code)notify('已切换为该结构适用的连线');
    }));
    const selected=menu.querySelector('[aria-selected="true"]'),list=menu.querySelector('.picker-menu-list');if(selected){selected.focus({preventScroll:true});list.scrollTop=Math.max(0,selected.offsetTop-list.clientHeight/2+selected.offsetHeight/2);}
  }
  $('component-menu').addEventListener('keydown',e=>{
    if(!openAxis)return;
    if(e.key==='Escape'){e.preventDefault();e.stopPropagation();closePicker(true);return;}
    if(e.key==='Tab'){closePicker(true);return;}
    const options=[...$('component-menu').querySelectorAll('[role="option"]')],index=options.indexOf(document.activeElement);let next;
    if(e.key==='ArrowDown')next=(index+1)%options.length;
    if(e.key==='ArrowUp')next=(index-1+options.length)%options.length;
    if($('component-menu').classList.contains('font-columns')&&['ArrowLeft','ArrowRight'].includes(e.key))next=(index+4)%options.length;
    if(e.key==='Home')next=0;if(e.key==='End')next=options.length-1;
    if(next!==undefined){e.preventDefault();options[next].focus();}
  });
  function positionPicker(){
    if(!openAxis)return;
    const button=document.querySelector(`[data-axis="${openAxis}"]`),menu=$('component-menu'),r=button.getBoundingClientRect(),below=window.innerHeight-r.bottom-14,above=r.top-14,desired=menu.querySelector('.picker-menu-head').offsetHeight+menu.querySelector('.picker-menu-list').scrollHeight+menu.querySelector('.picker-menu-foot').offsetHeight+4,up=below<Math.min(desired,600)&&above>below;
    menu.classList.toggle('opens-up',up);menu.style.setProperty('--picker-height',`${Math.max(160,Math.min(600,up?above:below))}px`);
  }
  document.addEventListener('pointerdown',e=>{if(openAxis&&!$('component-menu').contains(e.target)&&!e.target.closest('[data-axis]'))closePicker();});
  window.addEventListener('resize',positionPicker);
  function usePreset(id){state.recipe=Lib.resolveRecipe(id);$('code-error').textContent='';render();}
  function updateGalleryView(){
    $('catalogue-grid').dataset.view=state.catalogueView;
    document.querySelectorAll('[data-gallery-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.galleryView===state.catalogueView)));
  }
  function buildCatalogue(){
    const found=featured.filter(p=>{const r=Lib.resolveRecipe(p.id),v=p.positioning,sample=sampleFor(p.id),text=[sample?.title||'',sample?.audience||'',p.uid,p.id,p.name,p.family,p.description,p.code,v.useCase,v.outcome,v.audience,Lib.tasks.find(t=>t.id===v.task).name,...Lib.order.map(k=>r.tokens[k].name)].join(' ').toLowerCase();return (state.task==='all'||v.task===state.task)&&text.includes(state.search.toLowerCase());});
    $('catalogue-grid').innerHTML=found.map(p=>{const sample=sampleFor(p.id);return `<article class="preset-card" data-card="${p.id}"><button class="preset-preview" data-use="${p.id}" aria-label="使用样式 ${esc(presetLabel(p))}">${staticSVG(specimenFor(Lib.resolveRecipe(p.id)),Lib.resolveRecipe(p.id),2)}</button><div class="preset-card-body"><div class="preset-title"><span title="样式 UID">${p.uid}</span><h3>${esc(displayName(p))}</h3><small>${esc(p.positioning.useCase)}</small></div><p class="style-outcome">${esc(sample?.title||p.positioning.outcome)}</p><p class="style-intent">${esc(sample?.summary||p.description)}</p><div class="style-fit"><span>${esc(sample?.audience||p.positioning.audience)}</span><span>${esc(Lib.resolveRecipe(p.id).tokens.L.name)} · ${esc(Lib.resolveRecipe(p.id).tokens.D.name)}</span></div><p class="specimen-font">${sample?esc(sample.audience):esc(fontCaption(Lib.resolveRecipe(p.id)))}</p>${sample?`<a class="content-example" href="showcase/${sample.id}.html" target="_blank" rel="noopener">完整范例 · ${sample.nodes}节点 ↗</a>`:''}<a class="depth-example" href="depth-examples/${p.id}.html" target="_blank" rel="noopener">多层范例 ↗</a><code aria-label="${p.uid} 完整组合代号">${p.code}</code><div class="preset-bottom"><button class="copy-style" data-prompt="${p.id}" aria-label="复制 ${esc(displayName(p))} 生成指令">给 Agent 用</button><button class="apply-style" data-use="${p.id}" aria-label="应用样式 ${esc(presetLabel(p))}">${sample?'试着改这张图':'看这个效果'} <span aria-hidden="true">↗</span></button></div></div></article>`;}).join('')||'<p class="empty-state">没有找到匹配的配方，换个关键词试试。</p>';
    updateGalleryView();
    $('catalogue-count').textContent=`${state.task==='all'?'全部样式':Lib.tasks.find(t=>t.id===state.task).name} · ${found.length} / ${featured.length} 套`;
    $('task-suggestion').textContent=state.task==='all'?'先选你要完成的任务，再选喜欢的表达。每套都是搭配好的完整方案。':Lib.tasks.find(t=>t.id===state.task).pick;
    document.querySelectorAll('[data-task]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.task===state.task)));
    document.querySelectorAll('[data-use]').forEach(b=>b.addEventListener('click',()=>{const sample=sampleFor(b.dataset.use);if(sample){state.source=sample.source;state.root=K.parseMindmap(sample.source);state.collapsed.clear();$('source-editor').value=sample.source;usePreset(b.dataset.use);tryReader(sample.source,Lib.resolveRecipe(b.dataset.use),b);}else{usePreset(b.dataset.use);$('playground').scrollIntoView({behavior:'smooth'});}}));
    document.querySelectorAll('[data-prompt]').forEach(b=>b.addEventListener('click',()=>copyUsage(b.dataset.prompt)));markSelection();
  }
  function markSelection(){document.querySelectorAll('[data-card]').forEach(c=>c.classList.toggle('selected',Lib.presets.find(p=>p.id===c.dataset.card).code===state.recipe.code));}
  function updateView(){
    if(!state.geometry)return;const rect=$('canvas').getBoundingClientRect(),b=state.geometry.bounds,reading=byLayout().id==='outline'&&!state.overview,scale=(reading?Math.min(1,rect.width/b.w):Math.min(rect.width/b.w,rect.height/b.h))*state.zoom;
    if(reading)state.panY=Math.max(Math.min(0,rect.height-56-b.h*scale),Math.min(0,state.panY));
    $('map-world').setAttribute('transform',`translate(${rect.width/2-(b.x+b.w/2)*scale+state.panX} ${reading?28-b.y*scale+state.panY:rect.height/2-(b.y+b.h/2)*scale+state.panY}) scale(${scale})`);$('zoom-label').textContent=`${Math.round(state.zoom*100)}%`;
    $('fit').textContent=byLayout().id==='outline'?(state.overview?'恢复阅读':'纵览全图'):'适应画布';
  }
  function render(fit=true){
    $('download-file').hidden=true;
    closePicker();closePresetPicker();
    if(boot.standalone){document.title=state.root.text+' · Mindbox导图';document.querySelector('#playground .section-head h2').textContent=state.root.text;}
    $('code-error').textContent='';
    const t=byTheme(),l=byLayout();if(fit){state.zoom=1;state.panX=0;state.panY=0;state.overview=false;}
    state.geometry=K.layoutTree(state.root,l.id,state.collapsed,Infinity,t.density);
    $('preview-shell').style.setProperty('--canvas-bg',t.bg);$('preview-shell').style.setProperty('--canvas-ink',t.ink);
    const pattern=canvasPattern(t);$('canvas').style.backgroundImage=pattern.image;$('canvas').style.backgroundSize=pattern.size;
    $('canvas').innerHTML=tag('svg',{xmlns:'http://www.w3.org/2000/svg',...svgAttributes(state.recipe),'aria-label':`${state.root.text}，${l.name}，${t.name}`},tag('g',{id:'map-world'},svgContent(state.geometry,t,l.id,state.collapsed,true)));
    $('doodle-kit').hidden=t.node!=='marker';
    $('fusheng-kit').hidden=t.family!=='fusheng';
    if(t.family==='fusheng'){
      const kit=window.FushengKit;
      $('fusheng-parts').innerHTML=kit.families.map((family,index)=>`<section class="doodle-group" data-fusheng-family="${family.id}" aria-label="${esc(family.name)}"><div class="doodle-group-heading"><span>0${index+1}</span><h4>${esc(family.name)}</h4><p>${esc(family.hint)}</p></div><div class="doodle-group-grid">${family.parts.map(id=>{
        const p=kit.parts.find(p=>p.id===id),actor=p.kind==='actor';
        return `<figure class="doodle-part" data-fusheng-card="${p.id}">${tag('svg',{viewBox:actor?'0 0 160 160':'-10 -10 180 100','aria-hidden':'true',style:`background:${t.bg}`},kit.renderPart(p.id,{x:0,y:0,w:160,h:actor?160:p.kind==='mark'?55:75,theme:t}))}<figcaption><strong>${esc(p.name)}</strong><span>${esc(p.hint)}</span></figcaption></figure>`;
      }).join('')}</div></section>`).join('');
    }
    if(t.node==='marker'){
      const c=window.DoodleKit.colors(t);
      const parts=window.DoodleKit.parts;
      $('doodle-parts').innerHTML=window.DoodleKit.families.map((family,index)=>`<section class="doodle-group" data-doodle-family="${family.id}" aria-label="${esc(family.name)}"><div class="doodle-group-heading"><span>0${index+1}</span><h4>${esc(family.name)}</h4><p>${esc(family.hint)}</p></div><div class="doodle-group-grid">${family.parts.map(id=>parts.find(p=>p.id===id)).map(p=>{
        const actor=p.id.startsWith('mascot-'),view=actor?'-38 -59 76 70':p.id==='spark'?'30 6 40 38':'-12 -14 128 82';
        const opts={...c,x:0,y:0,w:100,h:p.id==='tape'?9:['marker','double-line'].includes(p.id)?8:54,seed:3};
        if(actor)Object.assign(opts,{ink:c.looseInk,paper:t.bg});
        if(p.id==='spark')Object.assign(opts,{x:50,y:25});
        if(['tape','marker','double-line'].includes(p.id))Object.assign(opts,{y:25});
        if(p.id==='tape')opts.paper=c.tape;
        return `<figure class="doodle-part" data-part-card="${p.id}">${tag('svg',{viewBox:view,'aria-hidden':'true',style:`background:${t.bg}`},window.DoodleKit.renderPart(p.id,opts))}<figcaption><strong>${esc(p.name)}</strong><span>${esc(p.hint)}</span></figcaption></figure>`;
      }).join('')}</div></section>`).join('');
    }
    $('map-title').textContent=state.root.text;$('selection-label').textContent=`${l.name} / ${state.recipe.tokens.T.family||state.recipe.tokens.T.name}`;$('layout-purpose').textContent=`${l.purpose} · ${l.relation}`;
    $('node-status').textContent=`${state.geometry.nodes.length} / ${K.descendants(state.root)+1} 个节点已展开 · ${state.collapsed.size} 处分支已收起`;
    $('navigation-hint').textContent=l.id==='outline'?'滚轮纵向阅读 · 纵览全图查看结构 · Ctrl / ⌘ + 滚轮缩放':'节点可折叠 · 空白可拖动 · Ctrl / ⌘ + 滚轮缩放';
    $('recipe-code').value=state.recipe.code;syncPresetPicker();$('preset-current').textContent=state.recipe.preset?presetLabel(state.recipe.preset):'已导入样式';
    document.querySelectorAll('[data-pick-task]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.pickTask===state.recipe.preset?.positioning?.task)));
    updateRecipeMatch();
    const rec=recommended.find(item=>item.preset===state.recipe.preset?.id);
    $('preset-recommendation').textContent=rec?`${rec.reason}`:state.recipe.preset?.positioning?`${state.recipe.preset.description}`:'已保留导入样式，可从16套完整样式中选择更适合的表达。';
    $('recommendation-date').textContent=state.recipe.preset?.positioning?`适合${state.recipe.preset.positioning.useCase}`:'已导入样式';
    $('recipe-description').textContent=state.recipe.preset?.positioning?`${state.recipe.preset.positioning.useCase} · ${state.recipe.preset.positioning.outcome}。`:state.recipe.preset?.description||'已保留导入的内容与外观，也可以选择上方16套完整样式。';
    $('compatibility-note').textContent=l.id==='brace'?'当前为括号分解，使用结构括号连接；节点造型不另加分组线。':l.id==='outline'?'当前为缩进大纲，使用提纲导线连接；可纵向阅读或切换全图。':'七个维度可以独立修改；所选配色会沿主分支向子节点继承。';
    document.querySelectorAll('[data-layout]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.layout===state.recipe.tokens.L.code)));
    document.querySelectorAll('[data-preset]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.preset===state.recipe.preset?.id)));
    updatePickerTriggers();
    document.querySelectorAll('#canvas .map-node[role="button"]').forEach(n=>{
      const toggle=()=>{const id=n.dataset.nodeId;state.collapsed.has(id)?state.collapsed.delete(id):state.collapsed.add(id);render(l.id!=='outline');document.querySelector(`#canvas .map-node[data-node-id="${id}"]`)?.focus({preventScroll:true});};
      n.addEventListener('click',()=>{if(!state.dragged)toggle();});n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});
    });markSelection();updateView();
  }
  function fitPrompt(){const field=$('skill-prompt');field.style.height='auto';field.style.height=Math.max(140,field.scrollHeight)+'px';}
  $('skill-prompt').addEventListener('input',fitPrompt);window.addEventListener('resize',fitPrompt);fitPrompt();
  async function copyUsage(id,phrase){
    const text=phrase||(id?`用 $mindbox 使用“${displayName(Lib.presets.find(p=>p.id===id))}”风格，将【我的主题或资料】整理成一份可编辑的思维导图。\n例如：上传的文档、正在阅读的网站、代码项目，或我感兴趣的话题。`:$('skill-prompt').value);
    $('skill-prompt').value=text;fitPrompt();
    try{await navigator.clipboard.writeText(text);notify('使用指令已复制，粘贴给你的 Agent 即可');}catch{$('skill-prompt').value=text;$('use-skill').scrollIntoView({behavior:'smooth'});$('skill-prompt').focus();$('skill-prompt').select();notify('指令已选中，可手动复制');}
  }
  for(const [action,label] of [['install','安装'],['update','更新'],['list','查看'],['remove','卸载'],['hero-install','安装']])$('copy-'+action+'-command').addEventListener('click',async()=>{const code=$(action+'-command');try{await navigator.clipboard.writeText(code.textContent);notify(label+'命令已复制');}catch{const selection=window.getSelection(),range=document.createRange();range.selectNodeContents(code);selection.removeAllRanges();selection.addRange(range);notify(label+'命令已选中，可手动复制');}});
  $('copy-skill-prompt').addEventListener('click',()=>copyUsage());
  document.querySelectorAll('[data-skill-phrase]').forEach(b=>b.addEventListener('click',()=>copyUsage(null,b.dataset.skillPhrase)));
  $('copy-manual').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('manual-example').textContent);notify('使用范例已复制');}catch{notify('可直接选中范例文字复制');}});
  function notify(text){$('toast').textContent=text;$('toast').classList.add('visible');clearTimeout(notify.timer);notify.timer=setTimeout(()=>$('toast').classList.remove('visible'),2300);}
  async function copyCode(code){try{await navigator.clipboard.writeText(code);notify('配方代号已复制');}catch{$('recipe-code').value=code;$('recipe-code').select();notify('代号已选中，可按 Ctrl / ⌘ + C 复制');}}
  function download(text,type,name){if(download.url)URL.revokeObjectURL(download.url);const a=$('download-file');download.url=URL.createObjectURL(new Blob([text],{type}));a.href=download.url;a.download=name;a.textContent='文件已就绪，再次下载';a.hidden=false;a.click();}
  function markdownWithSelection(){const field=`style: ${state.recipe.code}`,re=/^---\r?\n([\s\S]*?)\r?\n---/;return re.test(state.source)?state.source.replace(re,(_,body)=>`---\n${body.split(/\r?\n/).filter(l=>!/^\s*(?:layout|theme|style|preset):/.test(l)).join('\n')}\n${field}\n---`):`---\n${field}\n---\n\n${state.source}`;}
  $('recipe-form').addEventListener('submit',e=>{e.preventDefault();try{state.recipe=Lib.resolveRecipe($('recipe-code').value);$('code-error').textContent='';render();}catch(error){$('code-error').textContent=error.message;}});
  $('recipe-code').addEventListener('input',updateRecipeMatch);
  $('copy-recipe').addEventListener('click',()=>copyCode(state.recipe.code));$('catalogue-search').addEventListener('input',e=>{state.search=e.target.value;buildCatalogue();});
  $('apply-source').addEventListener('click',()=>{
    try{const next=$('source-editor').value,root=K.parseMindmap(next),options=K.parseOptions(next);let recipe=state.recipe;
      if(options.recipeCode)recipe=Lib.resolveRecipe(options.recipeCode);else{if(options.theme)recipe=Lib.resolveRecipe(Lib.legacy[options.theme]);if(options.layout)recipe=Lib.replaceToken(recipe,'L',Lib.axes.L.items.find(l=>l.id===options.layout).code);}
      Object.assign(state,{root,source:next,recipe});state.collapsed.clear();$('source-error').textContent='';if(!boot.standalone)buildCatalogue();render();notify('地图与配方已按文字更新');
    }catch(error){$('source-error').textContent=error.message;}
  });
  $('collapse-all').addEventListener('click',()=>{state.collapsed.clear();state.root.children.filter(n=>n.children.length).forEach(n=>state.collapsed.add(n.id));render();});$('expand-all').addEventListener('click',()=>{state.collapsed.clear();render();});
  function zoom(f){const rect=$('canvas').getBoundingClientRect(),b=state.geometry.bounds,fit=Math.min(rect.width/b.w,rect.height/b.h),old=state.zoom;state.zoom=Math.max(.2,Math.min(Math.max(20,2/fit),old*f));state.panX*=state.zoom/old;state.panY*=state.zoom/old;updateView();}
  $('zoom-in').addEventListener('click',()=>zoom(1.2));$('zoom-out').addEventListener('click',()=>zoom(1/1.2));$('fit').addEventListener('click',()=>{if(byLayout().id==='outline')state.overview=!state.overview;state.zoom=1;state.panX=0;state.panY=0;updateView();});
  $('canvas').addEventListener('wheel',e=>{
    if(e.ctrlKey||e.metaKey){e.preventDefault();zoom(e.deltaY<0?1.08:1/1.08);}
    else if(byLayout().id==='outline'&&!state.overview){const previous=state.panY;state.panY-=e.deltaY;updateView();if(previous!==state.panY)e.preventDefault();}
  },{passive:false});
  $('canvas').addEventListener('keydown',e=>{if(e.target!==$('canvas')||byLayout().id!=='outline'||state.overview)return;const steps={ArrowDown:48,ArrowUp:-48,PageDown:$('canvas').clientHeight*.75,PageUp:-$('canvas').clientHeight*.75};if(steps[e.key]){e.preventDefault();state.panY-=steps[e.key];updateView();}});
  $('canvas').addEventListener('pointerdown',e=>{state.dragged=false;if(e.target.closest('.map-node'))return;state.pointer={x:e.clientX,y:e.clientY,px:state.panX,py:state.panY};$('canvas').setPointerCapture(e.pointerId);});
  $('canvas').addEventListener('pointermove',e=>{if(!state.pointer)return;const p=state.pointer;state.panX=p.px+e.clientX-p.x;state.panY=p.py+e.clientY-p.y;if(Math.abs(e.clientX-p.x)+Math.abs(e.clientY-p.y)>4)state.dragged=true;updateView();});
  $('canvas').addEventListener('pointerup',()=>{state.pointer=null;});$('canvas').addEventListener('pointercancel',()=>{state.pointer=null;});new ResizeObserver(updateView).observe($('canvas'));
  const loadReader=window.MindboxReaderExport.createLoader({baseURL:document.baseURI,assets:boot.readerAssets});
  function readerHTML(source,recipe,collapsed=[]){
    return loadReader({source,recipeCode:recipe.code,standalone:true,player:true,...(collapsed.length?{view:{collapsed,zoom:1,x:0,y:0}}:{})});
  }
  const readerPreview=window.MindboxReaderExport.preview({dialog:$('reader-demo'),frame:$('reader-demo-frame'),status:$('reader-load-status'),message:$('reader-load-message'),retry:$('retry-reader-demo'),load:loadReader});
  function tryReader(source,recipe,button){
    if(button.disabled)return;
    return readerPreview.open({source,recipeCode:recipe.code,standalone:true,player:true},button);
  }
  $('source-toggle').addEventListener('click',e=>tryReader(markdownWithSelection(),state.recipe,e.currentTarget));
  $('try-current-reader').addEventListener('click',e=>tryReader(markdownWithSelection(),state.recipe,e.currentTarget));
  document.addEventListener('mindbox-demo',e=>tryReader(e.detail.source,Lib.resolveRecipe(e.detail.recipeCode),$('hero-open-reader')));
  function readerHasChanges(){const doc=$('reader-demo-frame').contentDocument,editor=doc?.querySelector('#node-editor');return !!(doc?.querySelector('#save-html')?.textContent.includes('·')||editor&&!editor.hidden);}
  function closeReaderDemo(){
    if(readerHasChanges()){$('reader-close-warning').hidden=false;$('continue-reader-demo').focus();return;}
    $('reader-demo').close();
  }
  $('close-reader-demo').addEventListener('click',closeReaderDemo);
  $('reader-demo').addEventListener('cancel',e=>{e.preventDefault();closeReaderDemo();});
  $('continue-reader-demo').addEventListener('click',()=>{$('reader-close-warning').hidden=true;$('reader-demo-frame').focus();});
  $('discard-reader-demo').addEventListener('click',()=>$('reader-demo').close());
  window.addEventListener('beforeunload',e=>{if($('reader-demo').open&&readerHasChanges()){e.preventDefault();e.returnValue='';}});
  $('reader-demo').addEventListener('close',()=>{$('reader-close-warning').hidden=true;});
  $('download-html').addEventListener('click',async()=>{
    const button=$('download-html');button.disabled=true;button.textContent='正在打包…';
    try{const html=await readerHTML(markdownWithSelection(),state.recipe,[...state.collapsed]);download(html,'text/html;charset=utf-8',`mindmap-${state.recipe.preset?.uid||'custom'}.html`);notify('已保存与 Skill 相同的可编辑脑图');}
    catch(error){notify(error.message);}finally{button.disabled=false;button.textContent='下载当前 HTML';}
  });
  setupSelectors();if(!boot.standalone)buildCatalogue();render();
})();
