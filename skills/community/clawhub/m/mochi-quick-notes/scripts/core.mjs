import {assert,text,date,id} from './store.mjs';
import {csv,md,exportFiles} from './files.mjs';
export function handle(i,s,c){
 if(i.action==='update'||i.action==='reopen'){
  const row=s.records.find(r=>r.id===i.id);assert(row,'Record not found');row.history??=[];row.history.push({text:row.text,tags:[...row.tags],due:row.due,status:row.status,changedAt:c.now});
  if(i.action==='reopen'){assert(row.kind==='task','Only tasks can be reopened');row.status='open';}
  else{assert(['text','tags','due'].some(k=>Object.hasOwn(i,k)),'Provide a field to update');if(i.text!==undefined)row.text=text(i.text);if(i.tags!==undefined){assert(Array.isArray(i.tags)&&i.tags.length<=3,'Use up to 3 tags');row.tags=i.tags.map(t=>text(t,'tag',40));}if(Object.hasOwn(i,'due')){if(i.due===null)delete row.due;else row.due=date(i.due);}}
  row.updatedAt=c.now;return {changed:true,result:{record:row}};
 }
 if(i.action==='add'){
  assert(['note','task','idea'].includes(i.kind),'kind: note, task or idea');
  const tags=i.tags||[];assert(Array.isArray(tags)&&tags.length<=3,'Use up to 3 tags');tags.forEach(t=>text(t,'tag',40));
  const row={id:id(),kind:i.kind,text:text(i.text),tags,status:'open',createdAt:c.now};if(i.due)row.due=date(i.due);
  s.records.push(row);return {changed:true,result:{record:row}};
 }
 if(i.action==='complete'||i.action==='archive'){
  const row=s.records.find(r=>r.id===i.id);assert(row,'Record not found');assert(i.action!=='complete'||row.kind==='task','Only tasks can be completed');row.status=i.action==='complete'?'done':'archived';row.updatedAt=c.now;return {changed:true,result:{record:row}};
 }
 assert(['list','search','export'].includes(i.action),'action: add, list, search, update, reopen, complete, archive, export');
 if(i.dueFrom)date(i.dueFrom);if(i.dueTo)date(i.dueTo);if(i.dueFrom&&i.dueTo)assert(i.dueFrom<=i.dueTo,'Invalid due interval');
 const q=i.query?text(i.query).normalize('NFKC').toLowerCase():'';assert(i.action!=='search'||q,'Search needs query');
 const rows=s.records.filter(r=>(i.status?r.status===i.status:r.status!=='archived')&&(!i.kind||r.kind===i.kind)&&(!i.tag||r.tags.includes(i.tag))&&(!i.dueFrom||(r.due&&r.due>=i.dueFrom))&&(!i.dueTo||(r.due&&r.due<=i.dueTo))&&(!q||(r.text+' '+r.tags.join(' ')).normalize('NFKC').toLowerCase().includes(q)));
 if(i.action==='export')return exportFiles('notes',{'notes.md':'# Notes and tasks\n\n'+rows.map(r=>`- [${r.status==='done'?'x':' '}] ${md(r.text)}\n  - ${r.kind}; ${r.status}; due: ${r.due||'not set'}; tags: ${r.tags.map(md).join(', ')}; id: ${r.id}`).join('\n')+'\n','notes.csv':csv([['id','kind','status','text','tags','due'],...rows.map(r=>[r.id,r.kind,r.status,r.text,r.tags.join(';'),r.due||''])])},{count:rows.length});
 return {result:{records:rows}};
}
