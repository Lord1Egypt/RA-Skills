/* Pure SVG rendering shared by the gallery, workbench and standalone exports. */
(function(scope){
  'use strict';
  const K=typeof module!=='undefined'?require('./engine.cjs'):scope.MindmapKit,Lib=K.library,esc=K.escapeXML;
  const tag=(name,attrs,body='')=>`<${name} ${Object.entries(attrs).map(([k,v])=>`${k}="${esc(v)}"`).join(' ')}>${body}</${name}>`;
  const Doodle=typeof module!=='undefined'?require('./doodle.cjs'):scope.DoodleKit;
  const Fusheng=typeof module!=='undefined'?require('./fusheng.cjs'):scope.FushengKit;
  const safeColor=(color,bg,fallback)=>Lib.contrast(color,bg)>=4.5?color:fallback;
  function nodeSeed(n){let value=0;for(const c of n.id)value=(Math.imul(value,31)+c.charCodeAt(0))>>>0;return value%10007;}
  function baseNodeStyle(n,t){
    const color=t.palette[n.branch%t.palette.length],tint=ratio=>Lib.mix(t.bg,color,ratio);
    if(t.family==='fusheng')return{fill:n.depth<2?t.surface:'none',stroke:n.depth<2?t.ink:'none',text:t.ink,radius:5,color};
    if(!n.depth&&t.recipe.tokens.L.id==='outline'&&['text','hierarchy'].includes(t.node))return{fill:t.surface,stroke:Lib.mix(t.surface,t.ink,.12),text:Lib.readableText(t.surface),radius:6,color:t.accent};
    if(['capsule-outline','colorblock','pastel-patch'].includes(t.node)){
      if(t.node==='capsule-outline'){
        const fill=!n.depth?t.surface:tint(t.dark?.055:.018);
        return{fill,stroke:!n.depth?t.accent:Lib.mix(t.bg,color,n.depth===1?.86:.58),text:Lib.readableText(fill),radius:!n.depth?22:n.depth===1?16:11,color};
      }
      const fill=!n.depth?(t.node==='colorblock'?t.accent:t.root):n.depth===1?color:Lib.mix(t.bg,color,t.node==='pastel-patch'?.42:.12);
      return{fill,stroke:!n.depth?Lib.mix(fill,t.ink,.12):Lib.mix(fill,color,n.depth===1?.8:.3),text:Lib.readableText(fill),radius:!n.depth?14:n.depth===1?11:8,color};
    }
    if(t.node==='marker'){const framed=!n.depth||n.depth===1&&n.branch%3!==2,fill=framed?t.surface:t.bg;return{fill:framed?fill:'none',stroke:Lib.readableText(fill),text:Lib.readableText(fill),radius:0,color};}
    if(['pencilbox','bubble'].includes(t.node)){
      const sticky=t.node==='pencilbox'&&t.recipe.tokens.C.code==='C38';
      const fill=tint(sticky?(!n.depth?.15:n.depth===1?.68:.15):t.dark?(!n.depth?.19:n.depth===1?.13:.045):!n.depth?.16:n.depth===1?.18:.035);
      return{fill,stroke:t.dark?Lib.mix(t.ink,color,.3):Lib.mix(t.ink,'#202020',.7),text:Lib.readableText(fill),radius:0,color};
    }
    if(['hierarchy','silk','fine'].includes(t.node)){
      if(!n.depth){const fill=t.root;return{fill,stroke:t.rootStroke,text:Lib.readableText(fill),radius:t.node==='fine'?20:12,color:t.accent};}
      if(t.node==='hierarchy')return{fill:'none',stroke:'none',text:safeColor(t.ink,t.bg,Lib.readableText(t.bg)),radius:0,color};
      const fill=t.node==='fine'?tint(t.dark?.04:.015):tint(n.depth===1?(t.dark?.27:.17):(t.dark?.10:.045));
      return{fill,stroke:Lib.mix(fill,color,t.node==='fine'?.65:n.depth===1?.38:.18),text:Lib.readableText(fill),radius:t.node==='fine'?16:9,color};
    }
    if(['fold','tag','header','frame'].includes(t.node)){
      const fill=t.node==='header'||t.node==='frame'?t.surface:!n.depth?t.surface:tint(t.dark?(n.depth===1?.19:.09):(n.depth===1?.12:.045));
      const stroke=Lib.mix(fill,!n.depth?t.accent:color,t.dark?.42:.36);
      return{fill,stroke,text:!n.depth?t.ink:t.dark?Lib.mix(t.ink,color,.12):Lib.readableText(fill),radius:t.node==='frame'?3:5,color:!n.depth?t.accent:color};
    }
    if(!n.depth){
      if(t.node==='outline')return{fill:t.surface,stroke:t.accent,text:Lib.readableText(t.surface),radius:15,color:t.accent};
      if(t.node==='solid')return{fill:t.surface,stroke:Lib.mix(t.surface,t.accent,.3),text:safeColor(t.accent,t.surface,Lib.readableText(t.surface)),radius:10,color};
      if(t.node==='sketch'){const fill=Lib.mix(t.surface,'#ffffff',.6);return{fill,stroke:'#84918d',text:Lib.readableText(fill),radius:5,color};}
      return{fill:t.root,stroke:t.rootStroke,text:t.rootText,radius:t.node==='pill'?28:10,color};
    }
    if(t.node==='outline')return{fill:tint(t.dark?.08:.025),stroke:color,text:t.ink,radius:13,color};
    if(t.node==='solid')return{fill:color,stroke:'none',text:Lib.readableText(color),radius:8,color};
    if(t.node==='pill'){const fill=tint(t.dark?.73:.2);return{fill,stroke:'none',text:Lib.readableText(fill),radius:n.depth===1?22:11,color};}
    if(t.node==='paper'){const fill=tint(t.dark?.16:.09);return{fill,stroke:n.depth===1?Lib.mix(t.bg,color,.35):'none',text:t.ink,radius:5,color};}
    if(t.node==='sketch')return{fill:color,stroke:Lib.mix(color,t.ink,.3),text:Lib.readableText(color),radius:5,color};
    if(t.node==='index')return{fill:t.surface,stroke:Lib.mix(t.surface,t.ink,.18),text:Lib.readableText(t.surface),radius:4,color};
    return{fill:'none',stroke:'none',text:t.ink,radius:0,color};
  }
  function nodeStyle(n,t){return K.hierarchy.appearance(n,t,baseNodeStyle(n,t));}
  function detailBody(n,t,s){
    const x=n.x-n.w/2,y=n.y-n.h/2,w=n.w,h=n.h,seed=nodeSeed(n),m=K.hierarchy.metrics(n.depth);
    let art='';
    if(s.stroke!=='none'||s.fill!=='none'){
      const sketch=/^(?:sketch|patch)-/.test(s.kind);
      art+=tag(sketch?'path':'rect',{
        ...(sketch?{d:Lib.pencilBox(x,y,w,h,seed)}:{x,y,width:w,height:h,rx:s.radius}),fill:s.fill,stroke:s.stroke,'stroke-width':s.borderWidth,
        ...(s.kind==='patch-detail'?{'stroke-dasharray':'3 3'}:{}),class:'node-shape level-'+s.kind
      });
    }
    if(s.kind==='outline-note'){
      const d=t.recipe.tokens.L.id==='down'?`M${n.x-8},${y}H${n.x+8}`:`M${x},${y+7}V${y+h-6}H${x+10}`;
      art+=tag('path',{d,fill:'none',stroke:s.color,'stroke-width':s.borderWidth,opacity:s.markOpacity,'stroke-linecap':'round',class:'level-outline-corner'});
    }else if(s.kind.startsWith('journal-')){
      art+=Doodle.renderPart('marker',{x:x+13,y:n.y+5,w:w-26,h:n.depth===3?4:2,seed,ink:s.text,accent:s.color,opacity:.08+.1*m.retention});
      art+=tag('path',{d:`M${x+3},${n.y-2}q-1,3 2,5`,fill:'none',stroke:s.text,'stroke-width':s.borderWidth,'stroke-linecap':'round',class:'level-journal-tick'});
    }else if(s.kind==='color-detail'){
      art+=tag('path',{d:`M${x+4},${y+8}V${y+h-8}`,stroke:s.color,'stroke-width':2,opacity:.7,class:'level-color-accent'});
    }else if(['color-note','patch-note','sketch-note'].includes(s.kind)){
      art+=tag('path',{d:/^sketch/.test(s.kind)?Lib.pencilCurve(x+13,y+h-5,x+w-13,y+h-5,false,seed):`M${x+13},${y+h-5}H${x+w-13}`,fill:'none',stroke:s.color,'stroke-width':s.borderWidth,opacity:s.markOpacity,'stroke-linecap':'round',...(s.kind==='patch-note'?{'stroke-dasharray':'2 3'}:{}),class:'level-note-underline'});
      art+=tag('circle',{cx:x+5,cy:n.y,r:1+1.2*m.retention,fill:s.color,class:'level-note-dot'});
    }else if(s.kind==='text-note'||s.kind.startsWith('branch-')){
      art+=tag(n.depth===3?'circle':'path',n.depth===3?{cx:x+4,cy:n.y,r:1.3,fill:s.color,class:'level-text-dot'}:{d:`M${x+3},${n.y-3}v6`,stroke:s.color,'stroke-width':s.borderWidth,opacity:s.markOpacity,class:'level-text-tick'});
    }
    return art;
  }
  const underlined=(n,t)=>n.depth&&['underline','hierarchy'].includes(t.node);
  const nodeY=(n,t)=>n.y+(underlined(n,t)?n.h/2-5:0);
  function roundedElbow(x1,y1,x2,y2,vertical){
    const sx=Math.sign(x2-x1),sy=Math.sign(y2-y1),r=Math.min(13,Math.abs(x2-x1)/4,Math.abs(y2-y1)/4);
    if(r<1)return `M${x1},${y1}L${x2},${y2}`;
    if(vertical){const m=(y1+y2)/2;return `M${x1},${y1}V${m-sy*r}Q${x1},${m} ${x1+sx*r},${m}H${x2-sx*r}Q${x2},${m} ${x2},${m+sy*r}V${y2}`;}
    const m=(x1+x2)/2;return `M${x1},${y1}H${m-sx*r}Q${m},${y1} ${m},${y1+sy*r}V${y2-sy*r}Q${m},${y2} ${m+sx*r},${y2}H${x2}`;
  }
  function canvasPattern(t){
    if(t.canvas.pattern==='grid')return{image:`linear-gradient(${t.dark?'#ffffff09':'#344d4310'} 1px,transparent 1px),linear-gradient(90deg,${t.dark?'#ffffff09':'#344d4310'} 1px,transparent 1px)`,size:'22px 22px'};
    if(t.canvas.pattern==='ruled')return{image:'linear-gradient(transparent 27px,#698baf18 27px,#698baf18 28px)',size:'100% 28px'};
    if(t.canvas.pattern==='dots')return{image:'radial-gradient(#586b5d24 .9px,transparent .9px)',size:'16px 16px'};
    return{image:'none',size:'auto'};
  }
  function svgContent(geo,t,layout,collapsed,interactive){
    if(layout!==t.recipe.tokens.L.id||geo.layout!==layout)throw new Error('布局结果与展开结构不一致，请重新布局。');
    if(!Lib.allowedEdges(layout).includes(t.recipe.tokens.E.code))throw new Error('连线与当前展开结构不兼容。');
    const map=new Map(geo.nodes.map(n=>[n.id,n]));let content='';
    const path=(d,color,width=1.5,opacity=.82,depth=0)=>{const style=depth>2?K.hierarchy.edge(depth):null;return tag('path',{d,stroke:color,'stroke-width':style?width/1.5*style.width:width,opacity:style?opacity*(.85+.15*K.hierarchy.metrics(depth).retention):opacity,fill:'none','stroke-linecap':'round','stroke-dasharray':t.line==='dash'?'3 6':t.line==='dotted'?'1 5':'none',class:'map-link'});};
    if(layout==='brace'){
      const groups=new Map();geo.edges.forEach(e=>{if(!groups.has(e.from))groups.set(e.from,[]);groups.get(e.from).push(map.get(e.to));});
      groups.forEach((kids,id)=>{
        const p=map.get(id),sx=p.x+p.w/2,nx=Math.min(...kids.map(n=>n.x-n.w/2)),bx=(sx+nx)/2,py=nodeY(p,t),color=p.depth?t.palette[p.branch%t.palette.length]:t.palette[0];
        if(kids.length===1){content+=path(`M${sx},${py}H${nx}`,color,1.5,.82,p.depth+1);return;}
        const top=nodeY(kids[0],t),bottom=nodeY(kids[kids.length-1],t);
        content+=path(`M${sx},${py}H${bx-10}`,color,1.5,.82,p.depth+1);
        content+=tag('g',{class:'structural-brace'},path(`M${bx+11},${top}Q${bx},${top} ${bx},${top+11}L${bx},${py-12}Q${bx},${py} ${bx-10},${py}Q${bx},${py} ${bx},${py+12}L${bx},${bottom-11}Q${bx},${bottom} ${bx+11},${bottom}`,color,1.8,.82,p.depth+1));
        kids.forEach(n=>{content+=path(`M${bx+12},${nodeY(n,t)}H${n.x-n.w/2}`,t.palette[n.branch%t.palette.length],1,.55,n.depth);});
      });
    }else if(layout==='down'&&['elbow','rounded'].includes(t.line)){
      // Draw one shared rail per sibling group so overlapping connectors never become heavier.
      const groups=new Map();geo.edges.forEach(e=>{if(!groups.has(e.from))groups.set(e.from,[]);groups.get(e.from).push(map.get(e.to));});
      groups.forEach((kids,id)=>{
        const p=map.get(id),start=p.y+p.h/2,end=Math.min(...kids.map(n=>n.y-n.h/2)),rail=(start+end)/2,left=Math.min(...kids.map(n=>n.x)),right=Math.max(...kids.map(n=>n.x)),color=p.depth?t.palette[p.branch%t.palette.length]:Lib.mix(t.bg,Lib.readableText(t.bg),.65);
        // Shared rails must remain visible when the entire map is scaled into a card.
        if(kids.length===1){content+=path(`M${p.x},${start}V${end}`,t.palette[kids[0].branch%t.palette.length],1.75,.9,p.depth+1);return;}
        content+=path(`M${p.x},${start}V${rail}`,color,1.75,.9,p.depth+1);
        const radius=t.line==='rounded'?Math.min(12,(end-rail)/2,(right-left)/4):0;
        content+=path(`M${left},${end}V${rail+radius}Q${left},${rail} ${left+radius},${rail}H${right-radius}Q${right},${rail} ${right},${rail+radius}V${end}`,color,1.75,.9,p.depth+1);
        kids.forEach(n=>{if(n.x>left&&n.x<right)content+=path(`M${n.x},${rail}V${end}`,color,1.75,.9,p.depth+1);content+=path(`M${n.x},${end-10}V${end}`,t.palette[n.branch%t.palette.length],2,.95,n.depth);});
      });
    }else geo.edges.forEach(e=>{
      const p=map.get(e.from),n=map.get(e.to),color=t.palette[n.branch%t.palette.length];let d;
      const wide=n.depth>2?1.1+(t.node==='hierarchy'?3.9:7.9)/Math.pow(n.depth,.8):Math.max(1.3,(t.node==='hierarchy'?5:9)/Math.pow(n.depth,.8)),thin=n.depth>2?.8+.6*K.hierarchy.metrics(n.depth).retention:Math.max(1.2,wide*.4);
      if(layout==='outline'){
        const x=p.x-p.w/2+9,y=n.y;content+=path(`M${x},${p.y+p.h/2}V${y}H${n.x-n.w/2}`,Lib.mix(t.bg,color,.5),n.depth===1?1:.8,.5,n.depth);return;
      }
      if(layout==='down'){
        const y1=p.y+p.h/2,y2=n.y-n.h/2,m=(y1+y2)/2;
        if(t.line==='organic')d=`M${p.x-wide/2},${y1}C${p.x-wide/2},${m} ${n.x-thin/2},${m} ${n.x-thin/2},${y2}L${n.x+thin/2},${y2}C${n.x+thin/2},${m} ${p.x+wide/2},${m} ${p.x+wide/2},${y1}Z`;
        else d=t.line==='rounded'?roundedElbow(p.x,y1,n.x,y2,true):t.line==='elbow'?`M${p.x},${y1}V${m}H${n.x}V${y2}`:t.line==='straight'?`M${p.x},${y1}L${n.x},${y2}`:`M${p.x},${y1}C${p.x},${m} ${n.x},${m} ${n.x},${y2}`;
      }else{
        const dir=n.direction,x1=p.x+dir*p.w/2,x2=n.x-dir*n.w/2,y1=nodeY(p,t),y2=nodeY(n,t),m=(x1+x2)/2;
        if(t.line==='organic')d=`M${x1},${y1-wide/2}C${m},${y1-wide/2} ${m},${y2-thin/2} ${x2},${y2-thin/2}L${x2},${y2+thin/2}C${m},${y2+thin/2} ${m},${y1+wide/2} ${x1},${y1+wide/2}Z`;
        else d=t.line==='rounded'?roundedElbow(x1,y1,x2,y2,false):t.line==='elbow'?`M${x1},${y1}H${m}V${y2}H${x2}`:t.line==='straight'?`M${x1},${y1}L${x2},${y2}`:`M${x1},${y1}C${m},${y1} ${m},${y2} ${x2},${y2}`;
      }
      if(t.line==='pencil'){
        const vertical=layout==='down',dir=n.direction||1,x1=vertical?p.x:p.x+dir*p.w/2,y1=vertical?p.y+p.h/2:nodeY(p,t),x2=vertical?n.x:n.x-dir*n.w/2,y2=vertical?n.y-n.h/2:nodeY(n,t),seed=nodeSeed(n);
        const ink=color;
        content+=tag('g',{class:'pencil-edge'},[0,1].map(pass=>path(Lib.pencilCurve(x1,y1,x2,y2,vertical,seed,pass),ink,pass?.65:1.35,pass?.25:.76,n.depth)).join(''));

        return;
      }
      if(t.line==='double'){
        const offset=layout==='down'?'translate(2.2 0)':'translate(0 2.2)',opposite=layout==='down'?'translate(-2.2 0)':'translate(0 -2.2)';
        content+=tag('g',{class:'double-edge'},tag('g',{transform:offset},path(d,color,1.3,.8))+tag('g',{transform:opposite},path(d,color,1.3,.8)));
      }else content+=t.line==='organic'?tag('path',{d,fill:color,opacity:.88,class:'organic-link'}):path(d,color,t.line==='roundbranch'?(n.depth===1?3.8:1.65):t.line==='dash'?1.15:1.5,t.line==='roundbranch'?(n.depth===1?.94:.7):t.line==='dash'?.5:n.depth===1?.84:.55,n.depth);
    });
    geo.nodes.forEach(n=>{
      const s=nodeStyle(n,t),x=n.x-n.w/2,y=n.y-n.h/2,foldable=n.children.length>0;
      let body=tag('title',{},esc(n.text))+tag('rect',{x:x-6,y:y-5,width:n.w+12,height:n.h+10,rx:4,fill:'transparent',class:'node-hit'});
      if(t.family==='fusheng'){body+=Fusheng.renderNode(n,t);}
      else if(n.depth>2){body+=detailBody(n,t,s);}
      else if(t.node==='pastel-patch'){
        const seed=nodeSeed(n);
        body+=tag('path',{d:Lib.pencilBox(x,y,n.w,n.h,seed),fill:s.fill,stroke:s.stroke,'stroke-width':n.depth<2?1.5:.8,'stroke-dasharray':n.depth<2?'5 3':'3 3','stroke-linecap':'round',class:'node-shape pastel-patch'});
      }else if(['pencilbox','bubble','marker'].includes(t.node)){
        const seed=nodeSeed(n),rough=(pass)=>Lib.pencilBox(x,y,n.w,n.h,seed,pass);
        if(t.node==='marker'){
          body+=Doodle.renderNode(n,t);
        }else if(t.node==='bubble'){
          const oval=pass=>`M${x+2},${n.y}C${x-3-pass},${y-4} ${x+n.w+2},${y-5+pass} ${x+n.w-1},${n.y}C${x+n.w+4},${y+n.h+5-pass} ${x-4},${y+n.h+3} ${x+2},${n.y}Z`;
          body+=tag('path',{d:oval(0),fill:s.fill,stroke:s.stroke,'stroke-width':1.15,class:'node-shape pencil-bubble'});
          body+=tag('path',{d:oval(1.7),fill:'none',stroke:s.stroke,'stroke-width':.6,opacity:.33,class:'pencil-echo'});
        }else{
          body+=tag('path',{d:rough(0),fill:s.fill,stroke:s.stroke,'stroke-width':1.65,'stroke-linejoin':'round',class:'node-shape pencil-box'});
          let hatch='';for(let i=10;i<n.w-16;i+=9)hatch+=`M${x+i},${y+n.h-7}l5,-5`;
          body+=tag('path',{d:hatch,fill:'none',stroke:s.color,'stroke-width':.85,opacity:.17,class:'pencil-hatch'});
          body+=tag('path',{d:rough(1),fill:'none',stroke:s.stroke,'stroke-width':.65,opacity:.35,class:'pencil-echo'});
          if(t.recipe.tokens.C.code==='C38'&&n.depth===1)body+=tag('rect',{x:n.x-14,y:y-3.5,width:28,height:7,rx:.5,transform:`rotate(-6 ${n.x} ${y})`,fill:t.dark?'#fff3c9':'#e5d9bd',opacity:.72,stroke:Lib.mix(t.bg,t.ink,.2),'stroke-width':.4,class:'note-tape','aria-hidden':'true'});
          if(!n.depth)body+=tag('path',{d:`M${x+13},${y+n.h-8}Q${x+29},${y+n.h-5} ${x+48},${y+n.h-9}`,fill:'none',stroke:t.dark?'#f0ce8c':'#f15b35','stroke-width':3.5,'stroke-linecap':'round',opacity:.9,class:'sketch-accent'});
        }
      }else if(t.node==='fold'){
        const corner=!n.depth?8:n.depth===1?7:5,r=6,right=x+n.w,bottom=y+n.h;
        body+=tag('path',{d:`M${x+r},${y}H${right-corner}L${right},${y+corner}V${bottom-r}Q${right},${bottom} ${right-r},${bottom}H${x+r}Q${x},${bottom} ${x},${bottom-r}V${y+r}Q${x},${y} ${x+r},${y}Z`,fill:s.fill,stroke:s.stroke,'stroke-width':!n.depth?1.2:.7,class:'node-shape fold-node'});
        body+=tag('path',{d:`M${right-corner},${y+.5}V${y+corner}H${right-.5}`,fill:'none',stroke:s.stroke,'stroke-width':.65,opacity:.7,class:'fold-corner'});
        if(n.depth===1)body+=tag('rect',{x:x+11,y:n.y-7,width:2,height:14,rx:1,fill:s.color,opacity:.8,class:'branch-marker'});
      }else if(t.node==='tag'){
        body+=tag('path',{d:`M${x},${y+n.h/2}L${x+13},${y}H${x+n.w}V${y+n.h}H${x+13}Z`,fill:s.fill,stroke:s.stroke,'stroke-width':1.2,class:'node-shape tag-node'});
        body+=tag('circle',{cx:x+13,cy:y+n.h/2,r:2.5,fill:t.bg,stroke:s.stroke,'stroke-width':.7});
      }else if(s.fill!=='none'||s.stroke!=='none')body+=tag('rect',{x,y,width:n.w,height:n.h,rx:s.radius,fill:s.fill,stroke:s.stroke,'stroke-width':t.node==='capsule-outline'?(!n.depth?2.2:n.depth===1?1.35:.9):['hierarchy','silk','fine'].includes(t.node)?(!n.depth?1.3:.85):!n.depth||t.node==='outline'?2:1,'stroke-dasharray':t.node==='sketch'&&n.depth?'7 4':'none',class:'node-shape'});
      if(t.node==='frame')body+=tag('rect',{x:x+5,y:y+4,width:n.w-10,height:n.h-8,rx:1,fill:'none',stroke:s.stroke,'stroke-width':.7,class:'inner-frame'});
      if(t.node==='header')body+=tag('rect',{x:x+1,y:y+1,width:n.w-2,height:5,rx:2,fill:s.color,class:'header-band'});
      if(t.node==='sketch')body+=tag('rect',{x:x+2,y:y-1,width:n.w-3,height:n.h+2,rx:6,fill:'none',stroke:s.stroke,'stroke-width':.8,opacity:.55,class:'sketch-outline'});
      if(t.node==='index'&&n.depth)body+=tag('rect',{x:x+1,y:y+1,width:4,height:n.h-2,rx:2,fill:s.color});
      const reading=layout==='outline'&&['text','hierarchy'].includes(t.node);
      if(reading){
        if(!n.depth)body+=tag('rect',{x:x+1,y:y+11,width:3,height:n.h-22,rx:1.5,fill:t.accent,class:'reading-title-mark'});
        else if(n.depth===1)body+=tag('rect',{x:x+3,y:n.y-7,width:2.5,height:14,rx:1.25,fill:s.color,class:'reading-section-mark'});
        else if(t.node==='hierarchy')body+=path(`M${x+14},${y+n.h-8}H${x+n.w-18}`,s.color,.8,.4,n.depth);
      }else if(underlined(n,t))body+=path(`M${x},${y+n.h-5}H${x+n.w}`,s.color,t.line==='roundbranch'?(n.depth===1?3.8:1.65):t.line==='organic'?Math.max(1.8,5/n.depth):n.depth===1?2:1.2,.82,n.depth);
      if(t.node==='colorblock'&&n.depth<2)body+=tag('rect',{x:x+1,y:y+1,width:n.w-2,height:n.h-2,rx:Math.max(0,s.radius-1),fill:'none',stroke:'#ffffff','stroke-width':.7,opacity:t.dark?.22:.32,'pointer-events':'none',class:'card-inner-edge'});
      const fs=n.fontSize||K.hierarchy.metrics(n.depth).fontSize,lineHeight=n.lineHeight||21,sy=n.y+(t.node==='marker'&&!n.depth?7:0)-(n.lines.length-1)*lineHeight/2+(t.node==='header'?2:0),tx=reading?x+(!n.depth?20:14):n.x+(t.node==='tag'||t.node==='fold'&&n.depth===1?5:t.node==='index'&&n.depth?3:0);
      body+=tag('text',{x:tx,y:sy,'text-anchor':reading?'start':'middle','dominant-baseline':'central',fill:s.text,'font-size':fs,'font-family':t.font,'font-weight':t.recipe.tokens.T.category?.startsWith('趣味')?400:!n.depth?600:n.depth===1?500:400,class:'node-label'},n.lines.map((line,i)=>tag('tspan',{x:tx,dy:i?lineHeight:0},esc(line))).join(''));
      if(foldable&&interactive){
        const hidden=collapsed.has(n.id),bx=layout==='down'?n.x:layout==='outline'?x-12:n.x+(n.direction||1)*(n.w/2+12),by=layout==='down'?n.y+n.h/2+12:layout==='outline'?n.y:nodeY(n,t),color=safeColor(s.color,t.bg,t.ink);
        body+=tag('circle',{cx:bx,cy:by,r:hidden?10:7,fill:t.bg,stroke:Lib.mix(t.bg,color,.45),'stroke-width':.65,class:!hidden?'fold-badge fold-expanded':'fold-badge'});
        body+=tag('text',{x:bx,y:by,'text-anchor':'middle','dominant-baseline':'central','font-size':hidden?10:12,fill:color,class:!hidden?'fold-badge fold-expanded':'fold-badge'},hidden?String(K.descendants(n)):'−');
      }
      const attrs={class:'map-node','data-node-id':n.id,'data-depth':n.depth,'data-level-role':K.hierarchy.metrics(n.depth).role,'data-sketch-seed':nodeSeed(n),'data-node-kind':t.node};
      if(t.node==='pencilbox'&&t.recipe.tokens.C.code==='C38'&&n.depth===1)attrs.transform=`rotate(${(nodeSeed(n)%5-2)*.45} ${n.x} ${n.y})`;
      if(interactive&&foldable)Object.assign(attrs,{role:'button',tabindex:0,'aria-label':`${collapsed.has(n.id)?'展开':'收起'}：${n.text}`,'aria-expanded':String(!collapsed.has(n.id))});
      content+=tag('g',attrs,body);
    });return content;
  }
  function svgAttributes(recipe){return{'data-recipe':recipe.code,'data-layout':recipe.tokens.L.id,...Object.fromEntries(Lib.order.map(axis=>['data-axis-'+axis.toLowerCase(),recipe.tokens[axis].code]))};}
  function staticSVG(root,recipe,maxDepth=2){
    const t=Lib.themeFor(recipe),layout=recipe.tokens.L.id,geo=K.layoutTree(root,layout,new Set(),maxDepth,t.density),b=geo.bounds,pattern=canvasPattern(t);
    return tag('svg',{xmlns:'http://www.w3.org/2000/svg',...svgAttributes(recipe),viewBox:`${b.x} ${b.y} ${b.w} ${b.h}`,'aria-hidden':'true',style:`background-color:${t.bg};background-image:${pattern.image};background-size:${pattern.size}`},svgContent(geo,t,layout,new Set(),false));
  }
  const api={svgContent,staticSVG,canvasPattern,nodeStyle,svgAttributes};
  if(typeof module!=='undefined')module.exports=api;else scope.MindmapRenderer=api;
})(typeof globalThis!=='undefined'?globalThis:this);
