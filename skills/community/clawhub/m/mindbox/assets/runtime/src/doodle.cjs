/* Original, reusable SVG parts. Decoration never creates a relationship or changes a font. */
(function(scope){
  'use strict';
  const K=typeof module!=='undefined'?require('./engine.cjs'):scope.MindmapKit,L=K.library,esc=K.escapeXML;
  const tag=(name,attrs,body='')=>`<${name} ${Object.entries(attrs).map(([k,v])=>`${k}="${esc(v)}"`).join(' ')}>${body}</${name}>`;
  const parts=[
    ['paper','涂鸦纸片','装进想法','收好一个完整主题'],['capsule','豆形圈注','装进想法','圈住值得记下的关键词'],
    ['speech','灵感气泡','装进想法','给新冒出的点子留位置'],['fold-note','折角便笺','装进想法','留一页，之后接着想'],
    ['marker','轻笔色标','随手强调','在关键词下轻轻画一笔'],['tape','纸胶带','随手强调','把纸片贴在思考现场'],
    ['spark','星星点点','随手强调','让一个小发现亮起来'],['emphasis','三笔强调','随手强调','这里值得多看一眼'],
    ['mascot-peek','探头搭子','一起想想','从主题上探头打个招呼'],['mascot-think','思考搭子','一起想想','陪一个还没想明白的问题'],
    ['mascot-pencil','举笔搭子','一起想想','边想边画，不急着定稿'],['mascot-aha','灵光搭子','一起想想','接住突然冒出的灵感'],
    ['ticket','灵感票签','慢慢展开','给一个分支留张入场券'],['orbit','灵感光圈','慢慢展开','用不规整的圈留住注意力'],
    ['mascot-read','翻书搭子','慢慢展开','翻一页，发现新的线索'],['mascot-go','出发搭子','慢慢展开','带着一个小想法开始行动'],
    ['torn-note','撕边纸笺','收好片段','零散的念头，也有一角安放'],['stitched-note','线装小页','收好片段','把几条线索慢慢缝在一起'],
    ['label-note','耳朵纸签','收好片段','给这个想法留一点俏皮'],['stacked-note','叠叠纸片','收好片段','想法不止一页，慢慢往下翻'],
    ['double-line','双笔下划','留点笔迹','一笔轻轻带过，再补一笔'],['corner-glint','角落微光','留点笔迹','一点点光，不抢走正文'],
    ['petal','四瓣小花','留点笔迹','让留白里长出一点好心情'],['confetti','纸屑小雨','留点笔迹','散落几笔，给思考松松绑'],
    ['mascot-listen','侧耳搭子','陪你琢磨','先听听，另一个角度怎么说'],['mascot-look','找找搭子','陪你琢磨','凑近一点，看看藏着的线索'],
    ['mascot-link','牵线搭子','陪你琢磨','两头都拿着，慢慢找关联'],['mascot-water','浇水搭子','陪你琢磨','小小的念头，也值得照料'],
    ['mascot-rest','歇歇搭子','走走停停','喝口热的，给脑袋一点空白'],['mascot-stretch','伸腰搭子','走走停停','换个姿势，想法也舒展开'],
    ['mascot-cheer','撒花搭子','走走停停','为一个小发现开心一下'],['mascot-build','搭搭搭子','走走停停','一块一块，把想法搭起来']
  ].map(([id,name,group,hint])=>({id,name,group,hint}));
  // Display order is editorial. It must never become the renderer's identity table.
  const families=[
    {id:'paper',name:'给想法一个形状',hint:'9种纸片 · 从完整主题到零散片段',parts:['paper','capsule','speech','fold-note','ticket','label-note','torn-note','stitched-note','stacked-note']},
    {id:'mark',name:'留一点轻轻的笔迹',hint:'9种记号 · 色标与胶带在前，小小点缀在后',parts:['marker','double-line','tape','orbit','emphasis','corner-glint','spark','petal','confetti']},
    {id:'actor',name:'让小搭子陪着想',hint:'14种姿态 · 好奇、琢磨、动手，也记得歇一歇',parts:['mascot-peek','mascot-listen','mascot-read','mascot-look','mascot-think','mascot-link','mascot-aha','mascot-pencil','mascot-build','mascot-water','mascot-go','mascot-stretch','mascot-rest','mascot-cheer']}
  ];
  const poses=Object.freeze(['mascot-peek','mascot-think','mascot-pencil','mascot-aha','mascot-read','mascot-go','mascot-listen','mascot-look','mascot-link','mascot-water','mascot-rest','mascot-stretch','mascot-cheer','mascot-build']);
  for(const family of families)for(const id of family.parts)parts.find(p=>p.id===id).group=family.name;
  function colors(t){
    const ink=L.readableText(t.surface),looseInk=L.readableText(t.bg);
    let accent=t.recipe.tokens.C.mark||(L.contrast(t.accent,t.surface)>=2?t.accent:t.palette[0]);
    if(L.contrast(accent,t.surface)<2)accent=L.mix(accent,ink,.35);
    return{ink,looseInk,accent,paper:t.surface,tape:L.mix(t.surface,accent,.17),shadow:L.mix(t.bg,looseInk,.12)};
  }
  function renderPart(kind,o){
    if(!parts.some(p=>p.id===kind))throw new Error('未知涂鸦组件：'+kind);
    const {x=0,y=0,w=100,h=54,seed=0,ink='#26332c',accent='#e57446',paper='#fffdf7',shadow='#e4e4dc'}=o;
    const line=(d,width=1.5,opacity=1,color=ink)=>tag('path',{d,fill:'none',stroke:color,'stroke-width':width,'stroke-linecap':'round','stroke-linejoin':'round',opacity});
    let art='';
    if(kind==='paper'){
      art+=tag('path',{d:L.pencilBox(x+4,y+4,w,h,seed),fill:shadow,stroke:'none',class:'journal-paper-shadow'});
      art+=tag('path',{d:L.pencilBox(x,y,w,h,seed),fill:paper,stroke:ink,'stroke-width':o.root?1.9:1.45,class:`node-shape ${o.root?'journal-paper':'journal-note'}`});
      art+=line(`M${x+14},${y+15}q14,-2 ${o.root?35:19},0`,o.root?4:2.5,.9,accent);
    }else if(kind==='capsule'){
      // Cardinal midpoints stay on the layout box, keeping all five connection directions aligned.
      const d=`M${x},${y+h/2}C${x},${y+7} ${x+w*.22},${y} ${x+w/2},${y}S${x+w},${y+5} ${x+w},${y+h/2}S${x+w*.76},${y+h} ${x+w/2},${y+h}S${x},${y+h-6} ${x},${y+h/2}Z`;
      art+=tag('path',{d,fill:paper,stroke:ink,'stroke-width':1.6,class:'node-shape journal-circle'});
      art+=tag('circle',{cx:x+w-13,cy:y+9,r:2.8,fill:accent,class:'journal-pin'});
    }else if(kind==='marker'){
      art+=tag('path',{d:L.pencilBox(x,y,w,Math.max(5,h),seed),fill:accent,opacity:o.opacity||.16,stroke:'none',class:'journal-highlight'});
    }else if(kind==='tape'){
      art+=tag('path',{d:`M${x},${y+1}l4,-1 4,1 4,-1 4,1 4,-1 4,1 ${w-24},-1v${h}l-4,-1 -4,1 -4,-1 -4,1 -4,-1 -4,1 ${24-w},-1Z`,fill:paper,stroke:accent,'stroke-width':.4,opacity:.85,transform:`rotate(-5 ${x+w/2} ${y+h/2})`});
    }else if(kind==='spark'){
      art+=tag('path',{d:`M${x},${y-5}Q${x+1},${y-1} ${x+5},${y}Q${x+1},${y+1} ${x},${y+5}Q${x-1},${y+1} ${x-5},${y}Q${x-1},${y-1} ${x},${y-5}Z`,fill:accent});
      art+=tag('circle',{cx:x+9,cy:y-7,r:1.2,fill:accent});
    }else if(kind==='speech'){
      // The speech notch stays inside the box; cardinal connection points never move.
      art+=tag('path',{d:`M${x+w/2},${y}Q${x+w},${y-1} ${x+w},${y+12}V${y+h*.6}L${x+w-7},${y+h*.72}L${x+w},${y+h*.85}Q${x+w},${y+h} ${x+w-16},${y+h}H${x+16}Q${x},${y+h} ${x},${y+h/2}Q${x},${y} ${x+16},${y}Z`,fill:paper,stroke:ink,'stroke-width':1.5,class:'node-shape journal-speech'});
      art+=line(`M${x+13},${y+8}q8,-2 15,0`,1.8,.75,accent);
    }else if(kind==='fold-note'){
      const fold=Math.min(13,h*.25);
      art+=tag('path',{d:`M${x+3},${y+1}L${x+w-fold},${y}L${x+w},${y+fold}V${y+h-2}Q${x+w*.5},${y+h+1} ${x},${y+h}L${x+1},${y+3}Z`,fill:paper,stroke:ink,'stroke-width':1.3,class:'node-shape journal-fold-note'});
      art+=tag('path',{d:`M${x+w-fold},${y+1}V${y+fold}H${x+w-1}`,fill:L.mix(paper,accent,.15),stroke:ink,'stroke-width':.85});
      art+=line(`M${x+10},${y+h-6}q7,1 14,-1`,1.4,.65,accent);
    }else if(kind==='ticket'){
      const r=4;
      art+=tag('path',{d:`M${x+5},${y}H${x+w-5}Q${x+w},${y} ${x+w},${y+r}V${y+h*.22}q-5,4 0,8V${y+h*.68}q-5,4 0,8V${y+h-r}Q${x+w},${y+h} ${x+w-5},${y+h}H${x+5}Q${x},${y+h} ${x},${y+h-r}V${y+h*.68+8}q5,-4 0,-8V${y+h*.22+8}q5,-4 0,-8V${y+r}Q${x},${y} ${x+5},${y}Z`,fill:paper,stroke:ink,'stroke-width':1.4,class:'node-shape journal-ticket'});
      art+=tag('path',{d:`M${x+10},${y+9}V${y+h-9}`,fill:'none',stroke:accent,'stroke-width':1,'stroke-dasharray':'2 3',opacity:.65});
    }else if(kind==='torn-note'){
      // The ragged edge is shallow: it cannot intrude into the label or connection ports.
      let edge='';for(let i=12;i>=0;i--)edge+=`L${x+w*i/12},${y+h-(i%2?1.6:0)}`;
      art+=tag('path',{d:`M${x+3},${y}Q${x+w*.5},${y-1} ${x+w-2},${y+1}L${x+w},${y+h-3}${edge}V${y+4}Z`,fill:paper,stroke:ink,'stroke-width':1.4,class:'node-shape journal-torn-note'});
      art+=line(`M${x+11},${y+8}q7,-1 14,0`,1.6,.7,accent);
    }else if(kind==='stitched-note'){
      art+=tag('path',{d:L.pencilBox(x,y,w,h,seed),fill:paper,stroke:ink,'stroke-width':1.3,class:'node-shape journal-stitched-note'});
      art+=tag('path',{d:`M${x+7},${y+9}V${y+h-9}`,fill:'none',stroke:accent,'stroke-width':.9,'stroke-dasharray':'1 4',opacity:.7});
      for(let i=0;i<3;i++)art+=line(`M${x+5},${y+12+i*7}q-6,-3 -3,-5`,.85,.7);
    }else if(kind==='label-note'){
      art+=tag('path',{d:`M${x},${y+h/2}V${y+5}Q${x},${y} ${x+6},${y}H${x+w-11}Q${x+w-2},${y+1} ${x+w-2},${y+9}Q${x+w+3},${y+13} ${x+w},${y+h/2}V${y+h-5}Q${x+w},${y+h} ${x+w-6},${y+h}H${x+6}Q${x},${y+h} ${x},${y+h-5}Z`,fill:paper,stroke:ink,'stroke-width':1.4,class:'node-shape journal-label-note'});
      art+=line(`M${x+w-11},${y+2}q-3,8 7,7`,.9,.7,accent);
    }else if(kind==='stacked-note'){
      art+=tag('path',{d:`M${x+5},${y+h+3}Q${x+w*.5},${y+h+5} ${x+w+3},${y+h+2}L${x+w+3},${y+5}`,fill:'none',stroke:ink,'stroke-width':1,opacity:.4});
      art+=tag('path',{d:L.pencilBox(x,y,w,h,seed),fill:paper,stroke:ink,'stroke-width':1.4,class:'node-shape journal-stacked-note'});
      art+=line(`M${x+11},${y+8}h12m-12,3h7`,1,.65,accent);
    }else if(kind==='double-line'){
      art+=line(`M${x},${y+h*.38}Q${x+w*.4},${y+h*.08} ${x+w},${y+h*.3}M${x+w*.1},${y+h*.74}Q${x+w*.65},${y+h*.9} ${x+w*.88},${y+h*.62}`,1.2,.65,accent);
    }else if(kind==='corner-glint'){
      art+=line(`M${x+w*.28},${y+h*.75}q-1,${-h*.45} ${w*.28},${-h*.5}M${x+w*.65},${y+h*.15}l${w*.09},${-h*.13}M${x+w*.8},${y+h*.4}l${w*.13},${-h*.03}`,1.15,.85,accent);
    }else if(kind==='petal'){
      art+=tag('g',{transform:`translate(${x+w/2} ${y+h/2}) scale(${Math.min(w,h)/30})`},tag('path',{d:'M0,-2C-10,-15 -16,-1 -3,1C-15,10 -1,16 1,3C11,15 16,1 3,-1C15,-11 1,-15 0,-2Z',fill:L.mix(paper,accent,.18),stroke:accent,'stroke-width':1.2})+tag('circle',{cx:0,cy:1,r:1.8,fill:accent}));
    }else if(kind==='confetti'){
      art+=line(`M${x+w*.2},${y+h*.2}l${w*.04},${h*.16}M${x+w*.73},${y+h*.13}l${-w*.06},${h*.13}M${x+w*.8},${y+h*.7}l${w*.09},${h*.02}M${x+w*.4},${y+h*.78}l${-w*.06},${h*.08}`,1.4,.85,accent);
      art+=tag('circle',{cx:x+w*.48,cy:y+h*.4,r:1.2,fill:accent});
    }else if(kind==='emphasis'){
      art+=line(`M${x+w*.18},${y+h*.7}l${-w*.08},${-h*.35}M${x+w*.48},${y+h*.46}l${w*.05},${-h*.4}M${x+w*.73},${y+h*.68}l${w*.2},${-h*.25}`,1.7,1,accent);
    }else if(kind==='orbit'){
      art+=line(`M${x+w*.3},${y+h*.12}C${x-w*.08},${y+h*.18} ${x-w*.02},${y+h*.95} ${x+w*.5},${y+h*.9}S${x+w*1.04},${y+h*.04} ${x+w*.37},${y+h*.08}M${x+w*.18},${y+h*.98}Q${x+w*.7},${y+h*1.15} ${x+w*.97},${y+h*.57}`,1.1,.7,accent);
      art+=tag('circle',{cx:x+w*.96,cy:y+h*.13,r:1.7,fill:accent});
    }else{
      const pose=kind.slice(7),scale=o.scale||1;
      const eyes=pose==='rest'?line('M-3,-30q1,-1 2,0M3,-30q1,-1 2,0',1):pose==='cheer'?line('M-3,-30q1,-3 3,0M3,-30q1,-3 3,0',1):tag('ellipse',{cx:-2,cy:-31,rx:pose==='look'?1.1:.9,ry:1.3,fill:ink})+(pose==='peek'?line('M3,-31l3,1 -3,1',.9):tag('ellipse',{cx:4,cy:-30,rx:.9,ry:1.3,fill:ink}));
      const face=tag('path',{d:'M-9,-31C-12,-45 12,-44 11,-30C12,-19 -7,-18 -9,-31Z',fill:paper,stroke:ink,'stroke-width':1.65})+eyes+line(pose==='cheer'?'M-1,-26q3,4 6,-1':'M-1,-26q2,2 5,0',.85,.85)+line('M-3,-41q-1,-4 3,-5M0,-41q2,-4 5,-3',1.25);
      const body=tag('path',{d:'M-7,-19Q0,-24 8,-18L11,-8Q1,-3 -9,-8Z',fill:accent,stroke:ink,'stroke-width':1.4})+line('M-4,-16q4,2 8,0',.65,.4);
      let gesture='',prop='';
      if(pose==='peek')gesture=line('M-8,-16Q-18,-17 -16,-26M8,-16Q17,-20 19,-14M-5,-6L-7,1M5,-6L8,1',1.5)+tag('circle',{cx:-16,cy:-27,r:1.7,fill:paper,stroke:ink,'stroke-width':1});
      else if(pose==='think')gesture=line('M-7,-16Q-14,-11 -10,-6L0,-5M8,-16L4,-24M-5,-5L-12,0L-6,2M4,-5L12,-3L14,1',1.5)+tag('circle',{cx:16,cy:-39,r:1.6,fill:accent})+tag('circle',{cx:21,cy:-44,r:2.6,fill:'none',stroke:accent,'stroke-width':1});
      else if(pose==='pencil')gesture=line('M8,-16Q17,-20 15,-27M-8,-16L-17,-20M-5,-6L-12,1M5,-6L13,0',1.5)+tag('g',{transform:'translate(-21 -33) rotate(-24)'},tag('path',{d:'M0,0H5V21L2.5,27L0,21Z',fill:paper,stroke:ink,'stroke-width':1.2})+tag('path',{d:'M1,4H4V20H1Z',fill:accent})+line('M0,21H5M2.5,27L1.8,24',.9));
      else if(pose==='aha'){
        gesture=line('M-7,-17Q-16,-21 -18,-30M8,-17Q17,-23 17,-30M-5,-6L-9,1M5,-6L10,0',1.5);
        prop=tag('path',{d:'M19,-43q0,-7 6,-6q6,1 3,7l-3,3h-4Z',fill:L.mix(paper,accent,.25),stroke:ink,'stroke-width':1})+line('M21,-37h4M16,-46l-3,-1M23,-52v-3M31,-48l3,-2',.9,1,accent);
      }else if(pose==='read'){
        gesture=line('M-8,-17L-15,-12M8,-17L15,-12M-5,-6L-10,0M5,-6L9,0',1.5);
        prop=tag('path',{d:'M-16,-18Q-7,-20 0,-15Q8,-20 16,-18L14,-6Q7,-8 0,-4Q-7,-8 -14,-6Z',fill:paper,stroke:ink,'stroke-width':1.3})+line('M0,-15v11M-11,-15l7,2M5,-13l6,-2M-10,-11l6,1',.75,.75,accent);
      }else if(pose==='go'){
        gesture=tag('path',{d:'M-8,-20q-10,-1 -9,9l6,3',fill:paper,stroke:ink,'stroke-width':1.3})+line('M-7,-16L-18,-21M8,-16L18,-20M-5,-6L-14,-2L-19,2M5,-6L13,-1L18,-5M-25,-14h5M-27,-8h5',1.5);
      }else if(pose==='listen'){
        gesture=line('M-8,-17Q-16,-23 -11,-30M8,-16Q17,-12 18,-18M-5,-6L-8,1M5,-6L8,1',1.5);
        prop=line('M-15,-37q-5,4 -1,9M-20,-40q-7,7 -2,15',1,.7,accent);
      }else if(pose==='look'){
        gesture=line('M-8,-16L-17,-24M8,-16L15,-12M-5,-6L-10,1M5,-6L11,0',1.5);
        prop=tag('circle',{cx:-20,cy:-32,r:6,fill:paper,stroke:ink,'stroke-width':1.3})+line('M-16,-27l5,7',2)+line('M-23,-34q2,-3 5,-1',.9,.7,accent);
      }else if(pose==='link'){
        gesture=line('M-8,-16L-18,-22M8,-16L18,-22M-5,-6L-8,1M5,-6L9,0',1.5);
        prop=line('M-20,-23Q-16,-35 -12,-28M12,-27Q16,-35 21,-24',1,.8,accent)+tag('circle',{cx:-20,cy:-24,r:2,fill:paper,stroke:accent,'stroke-width':1.1})+tag('circle',{cx:21,cy:-24,r:2,fill:paper,stroke:accent,'stroke-width':1.1});
      }else if(pose==='water'){
        gesture=line('M-8,-16L-15,-12M8,-16L16,-21M-5,-6L-9,1M5,-6L8,1',1.5);
        prop=tag('path',{d:'M14,-27l8,-2 2,7 -8,2Z M23,-25l5,-4 2,2 -6,6',fill:paper,stroke:ink,'stroke-width':1.1})+line('M16,-27q-4,-5 -2,-7M29,-24l1,2M32,-22l1,2M30,-6v-9q-7,0 -6,-5q6,0 6,5q1,-6 6,-6q1,5 -6,6M26,-5h8',.9,.85,accent);
      }else if(pose==='rest'){
        gesture=line('M-8,-16Q-5,-9 9,-12M8,-16L12,-13M-5,-5L-13,0L-6,1M5,-5L13,0L7,1',1.5);
        prop=tag('path',{d:'M9,-19h9v7q-4,3 -9,0Z M18,-18q7,-1 4,4h-4',fill:paper,stroke:ink,'stroke-width':1})+line('M13,-23q-3,-3 0,-6M17,-24q-2,-3 0,-5',.8,.7,accent);
      }else if(pose==='stretch'){
        gesture=line('M-7,-17Q-19,-29 -15,-41M8,-17Q20,-28 18,-40M-5,-6L-12,1M5,-6L13,1',1.5);
        prop=line('M-20,-44l-3,-3M22,-43l3,-3',1,.7,accent);
      }else if(pose==='cheer'){
        gesture=line('M-8,-17L-20,-29M8,-17L20,-31M-5,-6L-13,0M5,-6L12,1',1.5);
        prop=line('M-22,-38l-2,-4M-15,-48l2,-3M19,-45l3,-3M26,-36l3,1',1.2,.85,accent)+tag('circle',{cx:11,cy:-52,r:1.3,fill:accent})+tag('circle',{cx:-26,cy:-29,r:1.1,fill:accent});
      }else if(pose==='build'){
        gesture=line('M-8,-16L-16,-12M8,-16L15,-10M-5,-6L-9,1M5,-6L9,0',1.5);
        prop=tag('path',{d:'M13,-7h10v8H13Z M24,-7h10v8H24Z M19,-16h10v8H19Z',fill:paper,stroke:ink,'stroke-width':1.1})+line('M21,-13h5M16,-4h4',.8,.7,accent);
      }
      art=tag('g',{transform:`translate(${x} ${y}) scale(${scale})`,class:'doodle-mascot','data-pose':pose},gesture+body+prop+face);
    }
    return tag('g',{'data-doodle-part':kind,'aria-hidden':'true','pointer-events':'none'},art);
  }
  function renderNode(n,t){
    const c=colors(t),x=n.x-n.w/2,y=n.y-n.h/2;let seed=0;for(const ch of n.id)seed=(Math.imul(seed,31)+ch.charCodeAt(0))>>>0;seed%=10007;
    const base={...c,x,y,w:n.w,h:n.h,seed};
    const part=(kind,extra={})=>renderPart(kind,{...base,...extra});
    const actor=(kind,extra={})=>part(kind,{ink:c.looseInk,paper:t.bg,...extra});
    let art='';
    if(!n.depth){
      art+=actor('mascot-peek',{x:x+n.w-39,y:y+5,scale:1.05});
      art+=part('paper',{root:true});
      art+=part('tape',{x:x+15,y:y-4,w:32,h:8,paper:c.tape});
      art+=part('spark',{x:x+n.w+10,y:y+7});
    }else if(n.depth===1){
      const shapes=['capsule','paper','speech','ticket','torn-note','stitched-note','label-note','stacked-note','fold-note'];
      const shape=shapes[n.branch%shapes.length],pose=poses[seed%poses.length];
      if(t.density.rowGap>=28)art+=actor(pose,{x:x+n.w-25,y:y+2,scale:.49});
      art+=part(shape);
      if(shape==='paper')art+=part('tape',{x:n.x-14,y:y-3,w:28,h:7,paper:c.tape});
    }else{
      // One decoration slot per node; never accumulate stickers as a map grows.
      const hasActor=t.density.rowGap>=28&&n.depth===2&&seed%7===0;
      if(hasActor)art+=actor(poses[Math.floor(seed/7)%poses.length],{x:x+n.w-22,y:y+2,scale:.4});
      // Containers signal a topic that can unfold; terminal ideas stay light.
      const framed=n.children.length>0&&seed%4===0;
      if(framed)art+=part(['fold-note','torn-note','stitched-note','label-note','stacked-note'][Math.floor(seed/4)%5]);
      else{
        const lastBaseline=n.y+((n.lines?.length||1)-1)*(n.lineHeight||21)/2;
        art+=part(seed%5===0?'double-line':'marker',{x:x+13,y:lastBaseline+(n.fontSize||14)*.52,w:n.w-26,h:5,accent:t.palette[n.branch%t.palette.length],opacity:.14});
        art+=tag('circle',{cx:x+5,cy:n.y,r:1.8,fill:c.looseInk,opacity:.55});
      }
      if(t.density.rowGap>=18&&!hasActor&&!framed&&seed%3===1){
        const mark=['orbit','emphasis','corner-glint','petal','confetti','spark'][Math.floor(seed/3)%6];
        art+=part(mark,{x:x+n.w-23,y:y+2,w:14,h:10,...(mark==='spark'?{x:x+n.w-16,y:y+8}:{})});
      }
    }
    return tag('g',{class:'journal-art','aria-hidden':'true','pointer-events':'none'},art);
  }
  const api={parts,families,colors,renderPart,renderNode};
  if(typeof module!=='undefined')module.exports=api;else scope.DoodleKit=api;
})(typeof globalThis!=='undefined'?globalThis:this);
