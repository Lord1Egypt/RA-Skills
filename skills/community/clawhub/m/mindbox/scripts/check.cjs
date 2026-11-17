'use strict';
/* Read data only. Never execute scripts from a supplied HTML. */
const crypto=require('node:crypto'),K=require('../assets/runtime/src/engine.cjs'),E=require('../assets/runtime/src/edit.cjs');
const hash=data=>crypto.createHash('sha256').update(data).digest('hex');
function inspectHTML(html){
 const match=html.match(/<script\b[^>]*\bid=(["'])atlas-boot\1[^>]*>\s*window\.ATLAS_BOOT\s*=\s*([\s\S]*?);\s*<\/script>/i);
 if(!match)throw new Error('HTML 缺少 Mindbox 内容数据');let boot;try{boot=JSON.parse(match[2]);}catch{throw new Error('HTML 内容数据不是有效 JSON');}
 if(!boot.player||!boot.standalone)throw new Error('HTML 不是独立脑图阅读器');
 const head=html.match(/<head>([\s\S]*?)<\/head>/i)?.[1]||'';
 if(!head.includes('data:font/woff2;base64,')||/<script\b[^>]*\bsrc\s*=|<link\b[^>]*(?:stylesheet|preload)|url\((?:["']?https?:|fonts\/)/i.test(head)||/<script\b[^>]*\bsrc\s*=/i.test(html))throw new Error('HTML 离线资源检查失败');
 for(const id of ['stage','node-editor','branch-toggle','style-choices','play','export-menu','save-html'])if(!html.includes('id="'+id+'"'))throw new Error('HTML 阅读器缺少控件：'+id);
 const model=E.create(boot),root=model.root(),recipe=K.library.resolveRecipe(boot.recipeCode||boot.preset||'P61'),theme=K.library.themeFor(recipe),geo=K.layoutTree(root,recipe.tokens.L.id,new Set(),Infinity,theme.density);
 if(!geo.nodes.length||Object.values(geo.bounds).some(x=>!Number.isFinite(x))||geo.bounds.w<=0||geo.bounds.h<=0)throw new Error('HTML 布局范围无效');
 for(const n of geo.nodes)if([n.x,n.y,n.w,n.h,n.fontSize].some(x=>!Number.isFinite(x))||n.w<=0||n.h<=0)throw new Error('HTML 节点布局无效');
 const ids=new Set(geo.nodes.map(n=>n.id));if(ids.size!==geo.nodes.length||geo.edges.some(e=>!ids.has(e.from)||!ids.has(e.to)))throw new Error('HTML 节点引用无效');
 for(let i=0;i<geo.nodes.length;i++)for(let j=i+1;j<geo.nodes.length;j++){const a=geo.nodes[i],b=geo.nodes[j];if(Math.abs(a.x-b.x)<(a.w+b.w)/2-.01&&Math.abs(a.y-b.y)<(a.h+b.h)/2-.01)throw new Error('HTML 节点布局重叠');}
 return {pendingMarkdown:typeof boot.markdownDraft==='string',validation:{passed:true,kind:'structural',browserChecked:false},nodes:geo.nodes.length,levels:Math.max(...geo.nodes.map(n=>n.depth))+1,uid:recipe.preset?.uid||null,preset:recipe.preset?.id||null,style:recipe.code,sha256:{html:hash(Buffer.from(html)),content:hash(JSON.stringify(model.document())),source:hash(model.markdown(recipe.code))}};
}
module.exports={inspectHTML,hash};
