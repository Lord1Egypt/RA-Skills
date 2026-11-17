import {assert,text,date,minor,currency,id,integer} from './store.mjs';
import {csv,md,money,exportFiles,readText,parseCsv,digest} from './files.mjs';
export function handle(i,s,c){
 if(i.action==='import-csv'){const raw=readText(c,i.file),rows=parseCsv(raw),staged=[];const seen=new Map(s.records.filter(r=>r.importKey).map(r=>[r.importKey,r]));let duplicates=0;for(const [n,item] of rows.entries()){for(const key of ['kind','date','amount','currency','category'])assert(Object.hasOwn(item,key),'Missing CSV column: '+key);const key=item.sourceId?'source:'+text(item.sourceId,'sourceId',300):'csv:'+digest(raw)+':'+n;const scratch={records:[]};handle({...item,action:'add'},scratch,c);if(seen.has(key)){const prior=seen.get(key);assert(JSON.stringify([prior.kind,prior.date,prior.amountMinor,prior.currency,prior.category,prior.description])===JSON.stringify([scratch.records[0].kind,scratch.records[0].date,scratch.records[0].amountMinor,scratch.records[0].currency,scratch.records[0].category,scratch.records[0].description]),'Conflicting sourceId: '+key);duplicates++;continue;}scratch.records[0].importKey=key;staged.push(scratch.records[0]);seen.set(key,scratch.records[0]);}s.records.push(...staged);return {changed:staged.length>0,result:{imported:staged.length,duplicates,ids:staged.map(r=>r.id)}};}
 if(i.action==='add'){
  assert(['expense','income','refund'].includes(i.kind),'kind: expense, income or refund');const amountMinor=minor(i.amount);assert(amountMinor>0,'Amount must be positive');
  const row={id:id(),kind:i.kind,date:date(i.date),amountMinor,currency:currency(i.currency),category:text(i.category,'category',80),description:text(i.description||i.category),createdAt:c.now};s.records.push(row);return {changed:true,result:{record:row}};
 }
 if(i.action==='void'){
  const row=s.records.find(r=>r.id===i.id&&r.kind!=='budget');assert(row&&!row.voided,'Active entry not found');row.voided=true;row.voidReason=text(i.reason,'reason',500);return {changed:true,result:{record:row}};
 }
 if(i.action==='budget'){
  assert(/^\d{4}-\d{2}$/.test(i.month||''),'Use YYYY-MM month');date(i.month+'-01');const curr=currency(i.currency),cat=text(i.category,'category',80),amountMinor=minor(i.amount);
  let row=s.records.find(r=>r.kind==='budget'&&r.month===i.month&&r.currency===curr&&r.category===cat);
  if(row)row.amountMinor=amountMinor;else{s.records.push(row={id:id(),kind:'budget',month:i.month,currency:curr,category:cat,amountMinor});}return {changed:true,result:{budget:row}};
 }
 assert(['list','summary','export'].includes(i.action),'action: add, void, budget, import-csv, list, summary, export');
 const from=date(i.from),to=date(i.to);assert(from<=to,'from must be on or before to');
 const rows=s.records.filter(r=>r.kind!=='budget'&&!r.voided&&r.date>=from&&r.date<=to),groups={};
 for(const r of rows){const k=r.currency;groups[k]??={currency:k,incomeMinor:0,expenseMinor:0,refundMinor:0,categories:Object.create(null)};const g=groups[k];g[r.kind+'Minor']+=r.amountMinor;assert(Number.isSafeInteger(g[r.kind+'Minor']),'Summary exceeds safe arithmetic');if(r.kind!=='income')g.categories[r.category]=(g.categories[r.category]||0)+(r.kind==='refund'?-1:1)*r.amountMinor;}
 const budgets=s.records.filter(r=>r.kind==='budget'&&r.month+'-01'<=to&&r.month+'-31'>=from).map(b=>({...b,spentMinor:s.records.filter(r=>!r.voided&&r.kind!=='budget'&&r.kind!=='income'&&r.currency===b.currency&&r.category===b.category&&r.date.startsWith(b.month)).reduce((a,r)=>a+(r.kind==='refund'?-1:1)*r.amountMinor,0)}));
 const totals=Object.values(groups).map(g=>({...g,netExpenseMinor:g.expenseMinor-g.refundMinor}));
 if(i.action==='export')return exportFiles('expenses',{'ledger.csv':csv([['id','date','kind','amount','currency','category','description'],...rows.map(r=>[r.id,r.date,r.kind,money(r.amountMinor),r.currency,r.category,r.description])]),'budget-report.md':`# Ledger ${from} – ${to}\n\n`+totals.map(g=>`## ${g.currency}\n\nIncome: ${money(g.incomeMinor)}; expenses: ${money(g.expenseMinor)}; refunds: ${money(g.refundMinor)}; net expenses: ${money(g.netExpenseMinor)}.\n`).join('\n')+'\n## Monthly budgets (whole month)\n\n'+budgets.map(b=>`- ${b.month} ${md(b.category)}: ${b.currency} ${money(b.spentMinor)} / ${money(b.amountMinor)}; remaining ${money(b.amountMinor-b.spentMinor)}`).join('\n')+'\n'},{from,to,count:rows.length,totals,budgets});
 return {result:{from,to,records:i.action==='list'?rows:undefined,totals,budgets}};
}
