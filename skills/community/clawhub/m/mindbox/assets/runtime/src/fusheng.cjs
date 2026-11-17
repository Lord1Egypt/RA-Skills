/* 浮生小趣: sixteen original vectors shared by the website, reader and exports. */
(function(scope){
 'use strict';
 const K=typeof module!=='undefined'?require('./engine.cjs'):scope.MindmapKit,L=K.library,esc=K.escapeXML;
 const tag=(name,attrs,body='')=>`<${name} ${Object.entries(attrs).map(([k,v])=>`${k}="${esc(v)}"`).join(' ')}>${body}</${name}>`;
 const actors=Object.freeze(['borrow-wind','more-tasks','steady-face','next-hurdle','little-garden','waiting-tea','paper-pie','no-blame']);
 const notes=Object.freeze(['tab-note','thought-bubble','fold-page','progress-ticket']);
 const parts=[
  ['borrow-wind','借风不丢线','actor','借一点助力，方向还在自己手里'],
  ['more-tasks','能干就多干','actor','笑着接住，耳朵却悄悄垂下来'],
  ['steady-face','我稳得很','actor','上面比赞，下面腿抖'],
  ['next-hurdle','还有下一关','actor','刚刚跨过，又看见前面的一关'],
  ['little-garden','留一小园','actor','工作之外，也有值得照料的生活'],
  ['waiting-tea','等个懂的人','actor','留一杯茶，给懂自己的人'],
  ['paper-pie','纸上大饼','actor','还愿意相信，也开始留个心眼'],
  ['no-blame','帮忙不背锅','actor','愿意伸手，也守住自己的边界'],
  ['tab-note','起念方笺','note','给完整主题留一个位置'],
  ['thought-bubble','转念气泡','note','放进一个追问或新的角度'],
  ['fold-page','折页备忘','note','留一角，之后接着想'],
  ['progress-ticket','进度票签','note','收好阶段、候选与小行动'],
  ['soft-highlight','轻划重点','mark','轻轻划过，留住关键词'],
  ['focus-loop','绕圈想想','mark','圈起一个值得琢磨的地方'],
  ['turn-arrow','转个方向','mark','换个角度，再往前一步'],
  ['open-question','暂存问号','mark','还没想清楚的，留着慢慢琢磨']
 ].map(([id,name,kind,hint])=>({id,name,kind,hint}));
 const families=[
  {id:'paper',name:'给想法一个位置',hint:'4种纸笺 · 装下主题、追问和零散线索',parts:[...notes]},
  {id:'mark',name:'给思路一点提示',hint:'4种记号 · 重点、圈注、转折与疑问',parts:['soft-highlight','focus-loop','turn-arrow','open-question']},
  {id:'actor',name:'在小事里看见自己',hint:'8个小毛驴 · 有点无奈，也留一点盼头',parts:[...actors]}
 ];
 function colors(t){return{ink:t.ink,body:'#b8b1a6',muzzle:'#e8e2d7',accent:t.recipe.tokens.C.mark||'#d99670',paper:t.surface,bg:t.bg};}
 function actor(kind,c){
  const {ink,body,muzzle,accent,paper,bg}=c;
  const line=(d,width=2.5,color=ink)=>tag('path',{d,fill:'none',stroke:color,'stroke-width':width,'stroke-linecap':'round','stroke-linejoin':'round'});
  const shape=(d,fill=body,width=2.5)=>tag('path',{d,fill,stroke:ink,'stroke-width':width,'stroke-linejoin':'round','stroke-linecap':'round'});
  const dot=(x,y,r=1.7,fill=ink)=>tag('circle',{cx:x,cy:y,r,fill});
  const rect=(x,y,w,h,fill=paper,r=2)=>tag('rect',{x,y,width:w,height:h,rx:r,fill,stroke:ink,'stroke-width':2,'stroke-linejoin':'round'});
  const cup=(x,y)=>shape(`M${x},${y}h13v8q-6,6 -13,0Z`,accent,1.8)+line(`M${x+13},${y+1}q8,-2 3,6h-3`,1.5);
  const stool=(x,y)=>rect(x,y,23,5,accent)+line(`M${x+4},${y+5}l-2,14M${x+19},${y+5}l2,14`,3);
  const thumbs=(x,y)=>shape(`M${x},${y}q-2,-4 0,-7q3,-1 3,5q10,-1 9,5q-2,5 -12,1Z`,ink,1.2);
  let rear='',arms='',props='',front='',legs='M81,121L76,142M99,121L107,141',headTransform='',eyes='open',brow='';
  let torso='M78,94Q89,89 100,94L109,120Q90,125 73,120Z';
  let ears='M73,49Q59,26 62,10Q65,5 71,12L83,44M94,45L105,23Q108,18 113,23L132,37Q136,44 129,45L114,37L105,55';
  rear+=line('M76,112Q63,117 57,111',2.2)+shape('M59,110q-9,-5 -10,2q2,7 11,1Z',ink,1);
  if(kind==='borrow-wind'){
   headTransform='rotate(-9 87 75)';brow='M74,58l5,-2';
   legs='M80,121L72,141M100,121L111,141';
   arms=line('M78,102Q91,112 108,92M101,101L112,94',3);
   props=line('M108,94L132,40',1.5)+shape('M131,9L151,23L138,44L119,28Z',accent,2)+line('M131,10L138,43M120,28L150,23',1.3);
   props+=tag('g',{transform:'translate(14 106)'},rect(0,0,23,20,paper,3)+line('M12,0v-6M4,20l-2,6M19,20l3,6M0,8l-4,2M23,8l4,-2',1.8)+dot(12,-7,2,accent)+dot(7,8,1.5)+dot(16,8,1.5)+line('M9,14q3,2 6,0',1));
   props+=line('M39,112q9,-2 15,-10M43,120q14,-1 21,-11',1.5,accent);
  }else if(kind==='more-tasks'){
   headTransform='rotate(7 87 75)';brow='M91,54q4,-3 7,1';
   legs='M80,122L83,133L76,141M100,122L96,133L108,141';
   arms=line('M77,102L56,96M102,102L126,117',3);
   props=tag('ellipse',{cx:49,cy:87,rx:13,ry:22,transform:'rotate(20 49 87)',fill:accent,stroke:ink,'stroke-width':2})+line('M45,72l7,28M40,83l17,3',1.4);
   for(let i=0;i<4;i++)props+=shape(`M114,${113-i*5}l14,-4 17,6 -14,4Z`,paper,1.5);
   props+=shape('M18,62l20,4 -5,15 -20,-3Z',paper,1.6)+line('M13,83l9,2M10,77l8,1',1.2);
  }else if(kind==='steady-face'){
   eyes='closed';legs='M80,120L89,132L87,142M101,120L111,128L112,139';
   rear+=stool(76,123);arms=line('M79,102L83,118M101,103L115,98',3)+thumbs(116,97);
   props=shape('M66,48Q87,43 105,47L105,51Q86,48 66,53Z',muzzle,1.5);
   props+=line('M120,129q4,4 0,8M124,127q5,6 1,12M91,146l4,1',1.4);
  }else if(kind==='next-hurdle'){
   brow='M92,55q3,-4 6,0';headTransform='rotate(5 87 75)';
   legs='M80,122L65,131L58,126M101,122L118,117L124,124';
   arms=line('M78,101L61,87L58,77M101,102L116,107L122,103',3);
   rear+=line('M13,147Q34,126 55,147M112,147Q133,105 155,144',3,accent)+line('M64,139l-3,6M70,140l-3,6',1.2);
  }else if(kind==='little-garden'){
   eyes='closed';headTransform='rotate(15 87 75)';
   ears='M72,49Q48,46 43,76Q43,88 49,81L66,56M94,45L105,23Q109,19 115,25L130,40Q132,46 125,44L113,37L104,55';
   torso='M78,95Q91,92 100,97L108,120Q93,134 76,124Z';legs='M79,125L70,139L85,140M102,124L121,139L132,135';
   arms=line('M78,104Q80,118 99,115M102,103L110,114',3);
   props=shape('M93,111h20l-3,19H96Z',accent,1.8)+line('M103,111V99M102,103q-12,-1 -12,-9q9,-1 12,9M104,105q1,-11 11,-11q2,8 -11,11',1.7);
   rear+=shape('M14,118l24,2 5,20 -25,-1Z',body,1.6)+line('M18,141h34',1.8)+dot(28,130,1.7,ink);
  }else if(kind==='waiting-tea'){
   legs='M80,121L88,129L87,143M100,121L109,128L108,142';headTransform='rotate(5 87 75)';
   rear+=stool(75,123)+stool(125,132);
   arms=line('M78,102Q82,112 107,108M101,102L109,108',3);
   front+=cup(108,105)+cup(130,123)+line('M112,100q-3,-3 0,-6M136,118q-3,-3 0,-6',1.2);
  }else if(kind==='paper-pie'){
   headTransform='rotate(-8 87 75)';brow='M91,55q4,-3 7,1';
   arms=line('M78,102L56,115M101,102L84,115',3);
   front+=shape('M35,82L75,78q0,6 6,5q-1,6 5,3l8,-3 8,51 -60,6Z',paper,1.8);
   front+=tag('ellipse',{cx:66,cy:115,rx:18,ry:7,fill:'none',stroke:accent,'stroke-width':2})+tag('path',{d:'M48,115Q64,94 84,113M59,108l2,-4M66,107l2,-5M73,109l2,-4',fill:'none',stroke:accent,'stroke-width':2,'stroke-linecap':'round'});
   front+=dot(40,111,3.2)+dot(92,108,3.2)+line('M88,86q5,5 10,1',1.8)+shape('M64,148l3,-5 3,5Z',accent,1);
  }else if(kind==='no-blame'){
   brow='M92,54q4,-3 7,0';arms=line('M78,102L62,112M101,102L127,100',3)+thumbs(127,99);
   legs='M80,121L73,143M100,121L117,133L125,125';
   props=shape('M132,129h19v13q-9,6 -19,0Z',accent,1.8)+line('M132,132q-8,-3 -6,3h6M151,132q8,-3 6,3h-6M124,135l4,2M124,140l4,1',1.5);
  }
  const feet=line(legs,3.4)+line(kind==='next-hurdle'?'M54,127l6,2M120,125l6,-1':kind==='little-garden'?'M80,140h6M130,135l4,-2':'M72,143h7M105,142h7',3.8);
  let face=shape(ears,body,2.5)+line('M86,45q-2,-7 2,-10M91,45q0,-6 4,-8',2);
  face+=shape('M64,68C61,45 83,39 99,47C112,53 114,78 103,88C90,99 67,91 64,68Z',body);
  face+=eyes==='closed'?line('M76,63q3,4 5,0M91,61q3,4 5,0',1.8):tag('ellipse',{cx:78,cy:63,rx:1.8,ry:2.7,fill:ink})+tag('ellipse',{cx:94,cy:61,rx:1.8,ry:2.7,fill:ink});
  if(brow)face+=line(brow,1.6);
  face+=tag('ellipse',{cx:99,cy:81,rx:18,ry:12,transform:'rotate(-12 99 81)',fill:muzzle,stroke:ink,'stroke-width':2.3});
  face+=dot(108,77,1.6)+line(kind==='next-hurdle'?'M96,85q2,-3 4,0q2,-3 4,0':kind==='paper-pie'?'M97,85q4,4 7,0':'M97,85q4,4 7,-1',1.5);
  return rear+feet+shape(torso)+arms+tag('g',{transform:headTransform||'translate(0 0)'},face)+props+front;
 }
 function renderPart(id,o={}){
  const part=parts.find(p=>p.id===id);if(!part)throw new Error('未知浮生小趣组件：'+id);
  const c=o.theme?colors(o.theme):{ink:'#292d32',body:'#b8b1a6',muzzle:'#e8e2d7',accent:'#d99670',paper:'#e8edec',bg:'#ccd9de'};
  Object.assign(c,o.colors||{});
  const {x=0,y=0,w=160,h=150}=o;let art='';
  if(part.kind==='actor'){
   const scale=Math.min(w/160,h/160),dx=x+(w-160*scale)/2,dy=y+(h-160*scale)/2;
   return tag('g',{'data-fusheng-part':id,class:'fusheng-actor','aria-hidden':'true','pointer-events':'none',transform:`translate(${dx} ${dy}) scale(${scale})`},actor(id,c));
  }
  const line=(d,width=1.6,color=c.ink,extra={})=>tag('path',{d,fill:'none',stroke:color,'stroke-width':width,'stroke-linecap':'round','stroke-linejoin':'round',...extra});
  const shape=(d,fill=c.paper)=>tag('path',{d,fill,stroke:c.ink,'stroke-width':o.root?1.8:1.35,'stroke-linecap':'round','stroke-linejoin':'round',class:'node-shape fusheng-note'});
  const r=Math.min(7,h/4),fold=Math.min(11,h/4);
  if(id==='tab-note'){
   art+=shape(`M${x+r},${y}H${x+w-r}Q${x+w},${y} ${x+w},${y+r}V${y+h-r}L${x+w-r},${y+h}H${x+r}Q${x},${y+h} ${x},${y+h-r}V${y+r}Q${x},${y} ${x+r},${y}Z`);
   art+=tag('rect',{x:x+12,y:y-3,width:20,height:7,rx:1.5,fill:c.accent,stroke:c.ink,'stroke-width':1});
  }else if(id==='thought-bubble'){
   // Both horizontal ports and the bottom midpoint remain on the layout bounds.
   art+=shape(`M${x},${y+h/2}C${x},${y+3} ${x+w*.25},${y} ${x+w/2},${y}S${x+w},${y+3} ${x+w},${y+h/2}Q${x+w},${y+h*.78} ${x+w-9},${y+h*.81}L${x+w-3},${y+h-2}L${x+w-20},${y+h-6}Q${x+w*.65},${y+h} ${x+w/2},${y+h}Q${x},${y+h} ${x},${y+h/2}Z`);
   art+=line(`M${x+12},${y+5}l7,-3`,2,c.accent);
  }else if(id==='fold-page'){
   art+=shape(`M${x+2},${y}H${x+w-fold}L${x+w},${y+fold}V${y+h}H${x}Z`);
   art+=shape(`M${x+w-fold},${y}V${y+fold}H${x+w}Z`,c.accent);
  }else if(id==='progress-ticket'){
   art+=shape(`M${x+r},${y}H${x+w-r}Q${x+w},${y} ${x+w},${y+r}V${y+h/2-4}q-5,4 0,8V${y+h-r}Q${x+w},${y+h} ${x+w-r},${y+h}H${x+r}Q${x},${y+h} ${x},${y+h-r}V${y+h/2+4}q5,-4 0,-8V${y+r}Q${x},${y} ${x+r},${y}Z`);
   art+=line(`M${x+10},${y+7}V${y+h-7}`,1.4,c.accent,{'stroke-dasharray':'2 4'});
  }else if(id==='soft-highlight'){
   art+=tag('rect',{x,y,width:w,height:Math.max(3,h*.5),rx:Math.min(4,h/3),fill:c.accent,opacity:o.opacity??.48});
   art+=line(`M${x+w*.12},${y+h*.9}Q${x+w*.5},${y+h*.8} ${x+w*.89},${y+h*.86}`,Math.min(1.2,h*.16));
  }else if(id==='focus-loop'){
   art+=line(`M${x+w*.73},${y+h*.1}C${x-w*.05},${y-h*.12} ${x-w*.03},${y+h*1.04} ${x+w*.51},${y+h*.94}S${x+w*1.06},${y+h*.17} ${x+w*.81},${y+h*.12}`,1.4);
   art+=line(`M${x+w*.03},${y+h*.7}Q${x+w*.1},${y+h*.96} ${x+w*.3},${y+h*1.02}`,2,c.accent);
  }else if(id==='turn-arrow'){
   art+=line(`M${x+w*.1},${y+h*.86}H${x+w*.61}Q${x+w*.85},${y+h*.86} ${x+w*.85},${y+h*.23}`,1.8);
   art+=shape(`M${x+w*.85},${y+h*.04}L${x+w*.76},${y+h*.28}H${x+w*.94}Z`,c.accent);
   art+=tag('circle',{cx:x+w*.03,cy:y+h*.86,r:1.8,fill:c.ink});
  }else if(id==='open-question'){
   art+=line(`M${x+w*.37},${y+h*.29}C${x+w*.35},${y+h*.02} ${x+w*.68},${y+h*.02} ${x+w*.67},${y+h*.29}C${x+w*.66},${y+h*.47} ${x+w*.5},${y+h*.48} ${x+w*.5},${y+h*.68}`,1.8);
   art+=tag('circle',{cx:x+w*.5,cy:y+h*.88,r:Math.max(.7,Math.min(3,h*.04)),fill:c.accent});
  }
  return tag('g',{'data-fusheng-part':id,'aria-hidden':'true','pointer-events':'none'},art);
 }
 function renderNode(n,t){
  const x=n.x-n.w/2,y=n.y-n.h/2,c=colors(t);let seed=0;for(const ch of n.id)seed=(Math.imul(seed,31)+ch.charCodeAt(0))>>>0;
  const part=(id,extra={})=>renderPart(id,{x,y,w:n.w,h:n.h,theme:t,...extra});
  let art='';
  if(n.depth<2){
   art+=part(n.depth?notes[n.branch%notes.length]:'tab-note',{root:!n.depth});
   const size=!n.depth?(t.density.rowGap>=44?54:36):38;
   if(!n.depth||t.density.rowGap>=44)art+=part(actors[n.depth?n.branch%actors.length:0],{x:x+n.w-size-8,y:y-size+3,w:size,h:size});
  }else{
   const baseline=n.y+((n.lines?.length||1)-1)*(n.lineHeight||21)/2;
   if(n.depth===2&&n.children.length&&seed%4===0)art+=part('fold-page');
   else if(n.depth===2&&t.density.rowGap>=30&&seed%4===1)art+=part('focus-loop',{x:x+3,y:y+2,w:n.w-6,h:n.h-4});
   else art+=part('soft-highlight',{x:x+14,y:baseline+(n.fontSize||14)*.55,w:n.w-28,h:4,opacity:n.depth>2?.2:.32});
   if(n.depth===2&&t.density.rowGap>=30&&seed%4===2)art+=part('turn-arrow',{x:x+n.w-12,y:y+3,w:10,h:8});
   // Echo an authored question; stable decorative seeds must never invent uncertainty.
   if(/[?？]\s*$/.test(n.text))art+=part('open-question',{x:x+n.w-22,y:y+2,w:26,h:18});
  }
  return tag('g',{class:'fusheng-art','aria-hidden':'true','pointer-events':'none'},art);
 }
 const api={parts,families,colors,renderPart,renderNode};
 if(typeof module!=='undefined')module.exports=api;else scope.FushengKit=api;
})(typeof globalThis!=='undefined'?globalThis:this);
