/* One depth policy for layout, SVG, gallery and offline exports. No per-document styling. */
(function(scope){
 'use strict';
 const L=typeof module!=='undefined'?require('./library.cjs'):scope.StyleLibrary;
 function metrics(depth){
  if(depth<=2)return{fontSize:depth===0?19:depth===1?16:14,lineHeight:21,paddingX:42,paddingY:24,scale:1,retention:1,role:depth===0?'title':depth===1?'section':'topic'};
  const retention=1/(1+(depth-2)*.45);
  return{fontSize:12+2*retention,lineHeight:17+4*retention,paddingX:22+20*retention,paddingY:12+12*retention,scale:.78+.22*retention,retention,role:depth===3?'detail':'annotation'};
 }
 function visibleAccent(color,bg){
  let c=color;for(let i=0;i<8&&L.contrast(c,bg)<2.5;i++)c=L.mix(c,L.readableText(bg),.14);return c;
 }
 function appearance(n,t,base){
  if(n.depth<=2)return base;
  const m=metrics(n.depth),detail=n.depth===3,color=visibleAccent(base.color,t.bg),r=m.retention;
  let fill='none',stroke='none',radius=0,kind='text-note';
  if(t.node==='capsule-outline'){
   kind=detail?'outline-detail':'outline-note';fill=detail?L.mix(t.bg,base.color,t.dark?.07:.018):'none';stroke=detail?L.mix(t.bg,color,.48+.34*r):'none';radius=3+7*r;
  }else if(t.node==='colorblock'){
   kind=detail?'color-detail':'color-note';fill=detail?L.mix(t.bg,base.color,t.dark?.12:.045):'none';stroke=detail?L.mix(t.bg,color,.62):'none';radius=3+4*r;
  }else if(t.node==='pastel-patch'){
   kind=detail?'patch-detail':'patch-note';fill=L.mix(t.bg,base.color,(t.dark?.24:.085)*r);stroke=detail?L.mix(t.bg,color,.65):'none';radius=3;
  }else if(['pencilbox','bubble'].includes(t.node)){
   kind=detail?'sketch-detail':'sketch-note';fill=detail?L.mix(t.bg,base.color,(t.dark?.12:.035)*r):'none';stroke=detail?L.mix(t.bg,base.stroke,.8):'none';
  }else if(t.node==='marker')kind=detail?'journal-detail':'journal-note';
  else if(t.node==='hierarchy')kind=detail?'branch-detail':'branch-note';
  else if(!['text','underline'].includes(t.node)){
   kind=detail?'outline-detail':'outline-note';fill=detail?L.mix(t.bg,base.color,.04*r):'none';stroke=L.mix(t.bg,color,.6);radius=3+4*r;
  }
  const bg=fill==='none'?t.bg:fill;
  return{...base,fill,stroke,radius,color,text:L.readableText(bg),kind,role:m.role,borderWidth:.6+.5*r,markOpacity:.42+.35*r};
 }
 function edge(depth){const r=metrics(depth).retention;return{width:1+.65*r,opacity:.65+.15*r};}
 const api={metrics,appearance,edge};
 if(typeof module!=='undefined')module.exports=api;else scope.MindmapHierarchy=api;
})(typeof globalThis!=='undefined'?globalThis:this);
