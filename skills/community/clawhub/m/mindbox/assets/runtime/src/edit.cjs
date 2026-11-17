/* One content model for every preset, the browser editor and HTML continuation. */
(function(scope){
 'use strict';
 const K=typeof module!=='undefined'?require('./engine.cjs'):scope.MindmapKit;
 const copy=value=>JSON.parse(JSON.stringify(value));
 function normalize(root){
  const ids=new Set();
  function visit(n,depth,branch){
   if(depth>20)throw new Error('最多支持 20 层子节点。');
   if(!n||typeof n.id!=='string'||!/^[-a-zA-Z0-9_]{1,80}$/.test(n.id)||ids.has(n.id))throw new Error('节点标识缺失、重复或无效。');
   ids.add(n.id);
   if(typeof n.text!=='string'||!n.text.trim()||n.text.length>500||/[\x00-\x1f]/.test(n.text))throw new Error('节点文字需为 1–500 个字符，不能含换行或控制字符。');
   if(!Array.isArray(n.children))throw new Error('节点缺少有效子节点列表。');
   return{id:n.id,text:n.text,depth,branch,children:n.children.map((child,i)=>visit(child,depth+1,depth===0?i:branch))};
  }
  return visit(root,0,0);
 }
 function pack(n){return{id:n.id,text:n.text,children:n.children.map(pack)};}
 function locate(root,id,parent=null){if(root.id===id)return{node:root,parent};for(const child of root.children){const found=locate(child,id,root);if(found)return found;}return null;}
 function markdown(root,source,recipe){
  let index=0;const lines=['mindmap'];
  function visit(n){
   const text=n.text,quoted=/^(?:%%|::|---)|^[\w-]+(?:\(\(.*\)\)|\(.*\)|\[.*\])$|^".*"$/u.test(text);
   // Only literal labels that collide with Mermaid shorthand need an explicit wrapper.
   lines.push('  '.repeat(n.depth+1)+(quoted?`mindbox_${index}[${JSON.stringify(text)}]`:text));index++;
   n.children.forEach(visit);
  }
  visit(root);
  let out=source.replace(/(^```mermaid\s*\r?\n)[\s\S]*?^```\s*$/m,()=> '```mermaid\n'+lines.join('\n')+'\n```');
  if(recipe){
   const field='style: '+recipe,re=/^---\r?\n([\s\S]*?)\r?\n---/;
   out=re.test(out)?out.replace(re,(_,body)=>{
    const rest=body.split(/\r?\n/).filter(l=>!/^\s*(?:style|preset|layout|theme):/.test(l)).join('\n');
    return `---\n${rest?rest+'\n':''}${field}\n---`;
   }):`---\n${field}\n---\n\n${out}`;
  }
  const parsed=K.parseMindmap(out);
  const textTree=n=>({text:n.text,children:n.children.map(textTree)});
  if(JSON.stringify(textTree(parsed))!==JSON.stringify(textTree(root)))throw new Error('文字无法完整转换为 Markdown，请检查节点。');
  return out;
 }
 function create(boot){
  // Validate the source context even when the HTML has a newer canonical tree.
  let source=boot.source;K.parseMindmap(source);
  if(boot.markdownDraft!==undefined&&(typeof boot.markdownDraft!=='string'||boot.markdownDraft.length>120000))throw new Error('Markdown 草稿需为不超过 120000 字符的文字。');
  if(boot.document&&boot.document.format!==1)throw new Error('不支持的 HTML 文档版本。');
  let tree=normalize(boot.document?boot.document.root:K.parseMindmap(source)),serial=0;
  const past=[],future=[];
  function checked(next){const normalized=normalize(next);markdown(normalized,source);return normalized;}
  tree=checked(tree);
  const snapshot=()=>({tree,source});
  function remember(){past.push(snapshot());if(past.length>50)past.shift();future.length=0;}
  function commit(change){const next=copy(tree),result=change(next),valid=checked(next);if(JSON.stringify(valid)===JSON.stringify(tree))return result;remember();tree=valid;return result;}
  const find=id=>locate(tree,id)?.node||null;
  function get(next,id){const found=locate(next,id);if(!found)throw new Error('找不到该节点。');return found;}
  return{
   root:()=>tree,find,document:()=>({format:1,root:pack(tree)}),markdown:recipe=>markdown(tree,source,recipe),
   rename(id,text){return commit(next=>{get(next,id).node.text=text;});},
   add(id,kind='child',text='新想法'){
    let newId;do{newId='edit_'+serial++;}while(find(newId));
    return commit(next=>{const {node,parent}=get(next,id),child={id:newId,text,children:[]};
     if(kind==='child')node.children.push(child);
     else if(kind==='sibling'&&parent)parent.children.splice(parent.children.indexOf(node)+1,0,child);
     else throw new Error('中心主题没有同级节点；请增加子节点。');
     return newId;
    });
   },
   remove(id){return commit(next=>{const {node,parent}=get(next,id);if(!parent)throw new Error('中心主题不能删除，可双击修改。');parent.children.splice(parent.children.indexOf(node),1);return parent.id;});},
   revise(nextSource){const next=revise({source,document:{format:1,root:pack(tree)}},nextSource,{preserveNotes:false});if(JSON.stringify(next.document.root)===JSON.stringify(pack(tree))&&next.source===markdown(tree,source))return false;remember();source=next.source;tree=normalize(next.document.root);return true;},
   undo(){if(!past.length)return false;future.push(snapshot());({tree,source}=past.pop());return true;},
   redo(){if(!future.length)return false;past.push(snapshot());({tree,source}=future.pop());return true;}
  };
 }
 function revise(boot,nextSource,{preserveNotes=true}={}){
  const original=create(boot).root(),parsed=K.parseMindmap(nextSource),reserved=new Set();let serial=0;
  (function collect(n){reserved.add(n.id);n.children.forEach(collect);})(original);
  const fresh=()=>{let id;do{id='revision_'+serial++;}while(reserved.has(id));reserved.add(id);return id;};
  function match(next,old){
   const pairs=new Map(),remaining=[...(old?.children||[])];
   for(const child of next.children){const at=remaining.findIndex(n=>n.text===child.text);if(at>=0)pairs.set(child,remaining.splice(at,1)[0]);}
   const unmatched=next.children.filter(n=>!pairs.has(n));
   if(unmatched.length===1&&remaining.length===1)pairs.set(unmatched[0],remaining[0]);
   return {id:old?.id||fresh(),text:next.text,children:next.children.map(child=>match(child,pairs.get(child)))};
  }
  const root=normalize(match(parsed,original));
  // CLI fence-only patches retain context; the full browser editor replaces it exactly.
  const outside=nextSource.replace(/^---\r?\n[\s\S]*?\r?\n---\s*/,'').replace(/^```mermaid\s*\r?\n[\s\S]*?^```\s*$/gm,'').trim();
  const source=markdown(root,outside||!preserveNotes?nextSource:boot.source);
  const ids=new Set();(function collect(n){ids.add(n.id);n.children.forEach(collect);})(root);
  return {source,document:{format:1,root:pack(root)},...(boot.view?{view:{...boot.view,collapsed:(boot.view.collapsed||[]).filter(id=>ids.has(id))}}:{})};
 }
 const api={create,normalize,revise};if(typeof module!=='undefined')module.exports=api;else scope.MindmapEdit=api;
})(typeof window!=='undefined'?window:globalThis);
