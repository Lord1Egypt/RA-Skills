/* Visual vocabulary for the same seven recipe axes; no second rendering model. */
(function(scope){
  'use strict';
  const Lib=typeof module!=='undefined'?require('./library.cjs'):scope.StyleLibrary;
  const xml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
  const vocabulary={
    L01:['左右展开','主题放中间，适合发散想法'],L02:['向右展开','从左往右读，适合说明和汇报'],L03:['向下分层','从上往下看，适合职责与项目'],L04:['括号分组','用大括号归类，适合知识拆解'],L05:['大纲列表','像文档目录，适合长内容'],
    N06:['只留文字','没有边框，轻巧易读'],N13:['线上的文字','不加外框，文字沿分支排布'],N19:['圆角边框','像整齐的卡片，清楚稳重'],N20:['彩色卡片','大块颜色，分组更醒目'],N21:['手作贴纸','粉彩填色与缝边，更活泼'],N16:['手绘方框','像 Excalidraw 白板，随手画'],N18:['趣味涂鸦','纸片、圈注和小人，边画边想'],N17:['手绘圆圈','用不规则圆圈圈住想法'],
    E01:['弯曲线','圆滑转弯，适合发散'],E02:['直角线','横平竖直，层次清楚'],E04:['直线','两点相连，简单直接'],E07:['圆角折线','转弯带圆角，柔和整齐'],E09:['手绘线','轻轻描两笔，像手画'],E10:['粗细彩枝','主干粗、分支细，重点清楚'],E03:['渐细曲枝','从粗到细，像树枝生长'],E05:['虚线','断续的短线'],E06:['点线','连续的小圆点'],
    C03:['商务蓝','深蓝、灰蓝，稳重清楚'],C17:['明亮多彩','鲜明彩虹，轻快醒目'],C18:['夜间亮彩','黄、珊瑚、青，适合深色底'],C26:['自然暖彩','红、橙、黄绿，温暖自然'],C38:['复古粉彩','莓紫、蓝灰、墨绿，低调有趣'],C39:['蓝绿配珊瑚','蓝绿分支，珊瑚色主题'],C43:['手绘柔彩','绿、棕、蓝、粉，像彩铅'],C45:['暖灰杏彩','蓝灰、暖灰与杏色，含蓄又轻快'],
    B36:['纯白','干净清楚，适合展示'],B23:['浅灰暖纸','浅灰背景，奶油色主题'],B15:['石板蓝灰','深色底，专注阅读'],B14:['柔和浅灰','浅灰背景，白色主题'],B35:['深灰','暗色背景，突出彩色节点'],B40:['速写本','无横线的米白纸，适合随手画'],B41:['横线纸','像笔记本，有淡淡横线'],B42:['浮生蓝灰','清爽的蓝灰底，衬托暖灰与杏色'],
    T06:['清晰黑体','中文 · Noto Sans SC，像文档正文'],T05:['阅读宋体','中文 · Noto Serif SC，像书籍内文'],T09:['手写文楷','中文 · 霞鹜文楷，像日常笔记'],T08:['趣味圆体','中文 · 站酷快乐体，轻松活泼'],T10:['清晰英文','Inter · 像界面正文，清楚利落'],T11:['书卷英文','Lora · 像杂志正文，适合阅读'],T12:['代码英文','JetBrains Mono · 像代码编辑器'],T13:['手写英文','Excalifont · 像白板涂鸦'],
    D01:['紧凑','间距小，一屏装下更多内容'],D02:['标准','间距适中，日常最省心'],D03:['舒展','留白多，适合展示和构思']
  };
  function describe(axis,item,layout){
    let [name,hint]=vocabulary[item.code]||[item.name,item.description||'已导入的历史样式'];
    if(axis==='E'&&layout==='brace'){name=Lib.edgeLabel(layout,item.code);hint='结构括号连接，同组内容放在一起';}
    if(axis==='E'&&layout==='outline'){name=item.code==='E02'?'大纲导线':Lib.edgeLabel(layout,item.code);hint='沿缩进连接上下层，像文档目录';}
    return{code:item.code,label:`${item.code} · ${name}`,name,hint};
  }
  function presetLabel(preset){return `${preset.uid||preset.id} · ${preset.name.split(' · ')[0]}`;}
  function itemsFor(axis,recipe){const items=Lib.selectedItems(axis,recipe.tokens[axis].code);return axis==='E'?items.filter(item=>Lib.allowedEdges(recipe.tokens.L.id).includes(item.code)):items;}
  const svg=body=>`<svg viewBox="0 0 88 48" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
  const path=(d,attrs='')=>`<path d="${d}" fill="none" ${/\bstroke=/.test(attrs)?'':'stroke="currentColor"'} ${/\bstroke-width=/.test(attrs)?'':'stroke-width="1.8"'} stroke-linecap="round" stroke-linejoin="round" ${attrs}/>`;
  const rect=(x,y,w,h,fill='none',rx=4,attrs='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" ${attrs}/>`;
  function preview(axis,item,layout){
    if(axis==='C')return `<span class="picker-palette" aria-hidden="true"><em style="background:${xml(item.accent)}"></em>${item.colors.map(color=>`<i style="background:${xml(color)}"></i>`).join('')}</span>`;
    if(axis==='T')return `<span class="picker-font" style="font-family:${xml(item.font)}" aria-hidden="true">${item.language==='en'?'Bright ideas':'把想法画出来'}</span>`;
    if(axis==='B'){
      let marks='';if(item.pattern==='ruled')for(const y of [13,23,33])marks+=path(`M7 ${y}H81`,'opacity=".15"');
      if(item.pattern==='grid')for(const x of [16,32,48,64])marks+=path(`M${x} 4V44`,'opacity=".1"');
      return svg(`<g style="color:${Lib.readableText(item.bg)}">${rect(2,3,84,42,item.bg,6,'stroke="#93a08d" stroke-opacity=".35"')}${marks}<circle cx="17" cy="24" r="3" fill="currentColor" opacity=".45"/>${path('M27 24H67','opacity=".4"')}</g>`);
    }
    if(axis==='D'){
      const gap=item.code==='D01'?7:item.code==='D02'?11:16,start=24-gap;
      return svg([0,1,2].map((n)=>`${rect(10,start+gap*n,7,4,'#8ba180',1)}${rect(24,start+gap*n,50-(n%2)*12,4,'#b5c3ac',2)}`).join(''));
    }
    if(axis==='L'){
      const box=(x,y,w=18,h=9)=>rect(x,y,w,h,'#e7eee1',2,'stroke="currentColor" stroke-width="1.3"');
      if(item.id==='balanced')return svg(path('M33 24H25Q21 24 21 10H16M21 24V38H16M55 24H63Q67 24 67 10H72M67 24V38H72')+box(33,17,22,14)+box(2,6,14)+box(2,34,14)+box(72,6,14)+box(72,34,14));
      if(item.id==='down')return svg(path('M44 17V25M15 32V25H73V32M44 25V32')+box(33,4,22,13)+box(6,33)+box(35,33)+box(64,33));
      if(item.id==='brace')return svg(box(4,17,24,14)+path('M28 24H38M49 5Q42 5 42 12V18Q42 24 37 24Q42 24 42 30V36Q42 43 49 43')+box(58,3,24)+box(58,19,24)+box(58,35,24));
      if(item.id==='outline')return svg(path('M13 10V36M13 22H27M13 36H27')+rect(7,5,48,5,'#78916d',2)+rect(27,19,48,5,'#b4c4a9',2)+rect(27,33,37,5,'#b4c4a9',2));
      return svg(box(4,18,24,14)+path('M28 25H42Q47 25 47 10H60M47 25V39H60')+box(60,6,24)+box(60,35,24));
    }
    if(axis==='E'){
      if(layout==='brace')return svg(path('M8 24H30M43 5Q34 5 34 14V17Q34 24 28 24Q34 24 34 31V34Q34 43 43 43M44 6H79M44 42H79',item.id==='dash'?'stroke-dasharray="4 4"':item.id==='dotted'?'stroke-dasharray="1 4"':''));
      if(layout==='outline')return svg(path('M18 5V36H77M18 20H77',item.id==='dash'?'stroke-dasharray="4 4"':item.id==='dotted'?'stroke-dasharray="1 4"':''));
      const d=item.id==='elbow'?'M5 38H43V10H83':item.id==='rounded'?'M5 38H33Q43 38 43 28V20Q43 10 53 10H83':item.id==='straight'?'M5 38L83 10':'M5 38C48 38 39 10 83 10';
      if(['roundbranch','organic'].includes(item.id))return svg(`<path d="M5 35C48 35 39 9 83 9L83 11C39 11 48 41 5 41Z" fill="currentColor"/>`);
      if(item.id==='pencil')return svg(path(d)+path('M5 39C46 36 40 13 83 11','opacity=".35" stroke-width="1"'));
      if(item.id==='double')return svg(path(d,'transform="translate(0 -2)"')+path(d,'transform="translate(0 2)"'));
      return svg(path(d,item.id==='dash'?'stroke-dasharray="5 4"':item.id==='dotted'?'stroke-dasharray="1 4"':''));
    }
    if(axis==='N'){
      const text=`<text x="44" y="26" text-anchor="middle" dominant-baseline="middle" fill="currentColor" font-size="14">想法</text>`;
      if(item.id==='text')return svg(text);
      if(item.id==='hierarchy')return svg(text+path('M9 38H79','stroke="#80a98b" stroke-width="3"'));
      if(item.id==='capsule-outline')return svg(rect(7,7,74,34,'#fafcf8',13,'stroke="currentColor" stroke-width="1.6"')+text);
      if(item.id==='colorblock')return svg(rect(7,7,74,34,'#526d87',8)+text.replace('fill="currentColor"','fill="#fff"'));
      if(item.id==='pastel-patch')return svg(rect(7,7,74,34,'#c6d7bb',4,'stroke="#6e8d62" stroke-width="1.6" stroke-dasharray="5 3"')+text);
      if(item.id==='marker')return svg(rect(6,10,68,31,'#dce0d7',2)+path('M5 9Q40 6 73 9L74 39Q40 41 5 39Z')+path('M15 31Q29 33 49 31','stroke="#e27a50" stroke-width="4"')+`<circle cx="70" cy="6" r="4" fill="#fff" stroke="currentColor" stroke-width="1.3"/>`+text);
      if(item.id==='bubble')return svg(`<ellipse cx="44" cy="25" rx="37" ry="18" fill="none" stroke="currentColor" stroke-width="1.6"/>`+text);
      return svg(path('M7 9Q40 6 80 9L79 39Q41 42 7 39Z')+path('M6 11Q39 8 81 10L80 40Q41 43 6 40Z','opacity=".3"')+text);
    }
    return svg(path('M10 24H78'));
  }
  const api={describe,presetLabel,itemsFor,preview};if(typeof module!=='undefined')module.exports=api;else scope.StylePicker=api;
})(typeof globalThis!=='undefined'?globalThis:this);
