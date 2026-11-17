/* The homepage demo uses the production layout and renderer, not a simulated generation. */
(function(){
  'use strict';
  const K=window.MindmapKit,L=K.library,R=window.MindmapRenderer,$=id=>document.getElementById(id);
  const scenes={
    read:{preset:'P61',type:'文章与笔记',source:'读完一篇文章，不只是记住几句话。找到主张、核对依据、连接已有经验，再决定自己要做什么。',root:'读懂一篇文章',branches:[['核心观点','作者主张','适用条件'],['论证依据','关键事实','证据边界'],['已有知识','相同之处','不同角度'],['我的行动','先试一步','留下问题']]},
    code:{preset:'P40',type:'代码与文档',source:'src/entry → services → data。理解一个项目，先找入口，再看规则、数据和测试边界。',root:'Code map',branches:[['Entry','Routes','Validation'],['Logic','Services','Rules'],['Data','Models','Storage'],['Tests','Unit tests','Edge cases']]},
    idea:{preset:'P67',type:'零散的想法',source:'如果把常规做法反过来？想做一个让知识整理更轻松的小工具，也想给它一点好玩的性格。',root:'做个有趣的产品',branches:[['反过来想','试个反例','找个例外'],['随手联想','画条联系','混合点子'],['小小实验','先做一版','看看反馈'],['留下问题','还有什么','下一次试']]}
  };
  let key='read',tree,collapsed,style='MMP0A7';
  function reset(next,preferredStyle){key=next;style=preferredStyle||scenes[key].preset;const s=scenes[key],sample=(window.ATLAS_BOOT.showcase||[]).find(x=>x.preset===s.preset);tree=sample?K.parseMindmap(sample.previewSource):K.parseMindmap('```mermaid\nmindmap\n  root(('+s.root+'))\n'+s.branches.map(b=>'    '+b[0]+'\n      '+b[1]+'\n      '+b[2]+'\n').join('')+'```');collapsed=new Set();render();}
  function render(){
    const s=scenes[key],recipe=L.resolveRecipe(style),theme=L.themeFor(recipe),geo=K.layoutTree(tree,recipe.tokens.L.id,collapsed,Infinity,theme.density),b=geo.bounds;
    $('hero-source-type').textContent=s.type;$('hero-source-text').textContent=s.source;$('hero-map').style.backgroundColor=theme.bg;
    $('hero-map').innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${b.x} ${b.y} ${b.w} ${b.h}" aria-label="${tree.text}，可点击分支展开" data-hero-preset="${recipe.preset.uid}">${R.svgContent(geo,theme,recipe.tokens.L.id,collapsed,true)}</svg>`;
    $('hero-map-hint').textContent=`${recipe.preset.uid} · ${recipe.preset.name.split(' · ')[0]} · 点分支展开`;$('hero-expand').textContent=collapsed.size?'全部展开':'收起细节';
    document.querySelectorAll('[data-hero-style]').forEach(btn=>btn.setAttribute('aria-pressed',String(L.resolveRecipe(btn.dataset.heroStyle).code===recipe.code)));
    document.querySelectorAll('[data-scene]').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.scene===key)));
    $('hero-map').querySelectorAll('.map-node[role="button"]').forEach(node=>{const toggle=()=>{collapsed.has(node.dataset.nodeId)?collapsed.delete(node.dataset.nodeId):collapsed.add(node.dataset.nodeId);render();$('hero-map').querySelector(`[data-node-id="${node.dataset.nodeId}"]`)?.focus({preventScroll:true});};node.addEventListener('click',toggle);node.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});});
  }
  document.querySelectorAll('[data-scene]').forEach(btn=>btn.addEventListener('click',()=>reset(btn.dataset.scene)));
  $('hero-open-reader').addEventListener('click',()=>{const sample=(window.ATLAS_BOOT.showcase||[]).find(x=>x.preset===scenes[key].preset),source=sample?.source||'```mermaid\nmindmap\n  root(('+tree.text+'))\n'+scenes[key].branches.map(b=>'    '+b[0]+'\n      '+b[1]+'\n      '+b[2]+'\n').join('')+'```';document.dispatchEvent(new CustomEvent('mindbox-demo',{detail:{source,recipeCode:L.resolveRecipe(style).code}}));});
  $('hero-expand').addEventListener('click',()=>{collapsed=collapsed.size?new Set():new Set(tree.children.map(n=>n.id));render();});
  document.querySelectorAll('[data-hero-style]').forEach(btn=>btn.addEventListener('click',()=>{style=btn.dataset.heroStyle;render();}));
  reset('read','MMP0A7');
  const image=$('doodle-story-image'),toggle=$('doodle-story-toggle'),status=$('doodle-story-state'),reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  let visible=false,manual=null,playing=false;
  function showMotion(next){
    next=!!next;if(playing===next)return;playing=next;image.src=next?image.dataset.motion:'showcase/doodle-story-poster.png';
    toggle.setAttribute('aria-pressed',String(next));toggle.textContent=next?'静止看全图':'播放脑洞小剧场';status.textContent=next?'跟着分支，一点点展开':'静态全图';
  }
  function syncMotion(){showMotion(visible&&!document.hidden&&(manual===null?!reduced.matches:manual));}
  toggle.addEventListener('click',()=>{manual=!playing;syncMotion();});
  const observer=new IntersectionObserver(entries=>{visible=entries[0].intersectionRatio>=.25;syncMotion();},{threshold:.25});observer.observe(image);
  document.addEventListener('visibilitychange',syncMotion);reduced.addEventListener('change',()=>{manual=null;syncMotion();});
  image.addEventListener('error',()=>{if(playing){manual=false;showMotion(false);status.textContent='当前显示静态全图';}});
})();
