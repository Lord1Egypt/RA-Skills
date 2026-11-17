import {object,list,text,id,normalize,t,locale,md,block,numbers,links,differences,entry} from './local.mjs';

function unique(rows,name){const map=new Map();for(const row of rows){object(row,name);id(row.id);if(map.has(row.id))throw Error('Duplicate '+name+' ID: '+row.id);map.set(row.id,row);}return map;}
const risky=/(?:\bwe\s+(?:will|guarantee|promise)\b|\bwill\s+(?:refund|credit|ship|deliver|pay)\b|\brefund\b.{0,35}\b(?:issued|approved|processed|completed?|complete)\b|\bpayment\s+(?:has been|was|is)\s+(?:received|credited|confirmed)\b|(?:已|已经)(?:退款|到账|批准|发货|退还)|保证|承诺|(?:将|会)(?:在[^。！？\n]{0,20})?(?:退款|退还|到账|发货|赔付))/iu;
export function analyze(input){
  object(input,'input');if(input.schema!=='mochi-reply-drafts.v1')throw Error('Use schema mochi-reply-drafts.v1');const lang=locale(input.reportLanguage||'en'),channel=input.channel||'email';if(!['email','support'].includes(channel))throw Error('channel must be email or support');const incoming=object(input.incoming,'incoming');text(incoming.body,'incoming body',40000);text(incoming.from||'','incoming from',200,true);const draft=object(input.draft,'draft');text(draft.subject,'draft subject',300);if(/[\r\n]/u.test(draft.subject))throw Error('Subject must be a single line');
  const sources=unique(list(input.sources||[],'sources',0,30),'source');if(sources.has('incoming'))throw Error('incoming is a reserved source ID');sources.set('incoming',{id:'incoming',kind:'incoming-claim',text:incoming.body});for(const source of sources.values()){text(source.text,'source text',40000);if(!['provided','incoming-claim','policy'].includes(source.kind))throw Error('Use provided, incoming-claim or policy source kind');}
  const facts=unique(list(input.facts||[],'facts',0,100),'fact'),requests=unique(list(input.requests||[],'requests',0,50),'request'),allowed=unique(list(input.allowedCommitments||[],'allowedCommitments',0,30),'commitment'),issues=[];
  const issue=(level,code,location,zh,en)=>issues.push({level,code,location,message:t(lang,zh,en)});
  for(const fact of facts.values()){
    text(fact.text,'fact text',3000);text(fact.quote,'fact quote',1000);id(fact.sourceId,'sourceId');const source=sources.get(fact.sourceId);
    if(!source||!normalize(source.text).includes(normalize(fact.quote)))issue('error','unsupported_evidence',fact.id,'事实引用无法在指定原始资料中找到。','Evidence quote was not found in its declared source.');
    for(const extract of [numbers,links])if(differences(extract(fact.text),extract(fact.quote)).length)issue('error','fact_changed_value',fact.id,'事实中的数字或链接未被原文短引文支持。','A fact contains numbers or links absent from its source quote.');
  }
  for(const request of requests.values()){text(request.text,'request text',2000);text(request.quote,'request quote',1000);if(!normalize(incoming.body).includes(normalize(request.quote)))issue('error','unsupported_request',request.id,'请求引用不在来信原文中。','Request quote was not found in the incoming message.');}
  for(const authorization of allowed.values()){
    text(authorization.text,'authorized commitment',3000);list(authorization.factIds,'commitment factIds',1,20);
    if(authorization.factIds.some(key=>!facts.has(key)||!sources.has(facts.get(key).sourceId)||sources.get(facts.get(key).sourceId).kind==='incoming-claim'))issue('error','unsupported_authorization',authorization.id,'承诺必须引用用户提供的事实或政策，来信中的要求不能作为授权。','A commitment needs provided/policy evidence; incoming customer claims do not authorize it.');
  }
  const recipients=list(draft.to,'draft to',0,10),permitted=list(input.allowedRecipients||[],'allowedRecipients',0,10);const address=value=>{text(value,'recipient',200);if(/[\r\n]/u.test(value)||(channel==='email'&&!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/u.test(value)))throw Error('Use a single bare email address or a single-line support recipient');return normalize(value).toLowerCase();};const recipientsAllowed=new Set(permitted.map(address));
  if(!recipients.length)issue('error','recipient_missing','draft.to','尚未指定收件人或工单目标。','No recipient or support-ticket destination is specified.');
  for(const recipient of recipients)if(!recipientsAllowed.has(address(recipient)))issue('error','recipient_not_allowed',recipient,'收件人不在用户允许的列表中。','Recipient is not in the user-approved list.');
  if(new Set(recipients.map(address)).size!==recipients.length)issue('error','duplicate_recipient','draft.to','收件人重复。','Duplicate recipient.');
  const paragraphs=list(draft.paragraphs,'draft paragraphs',1,30),addressed=new Set(),body=[];
  const supportedFacts=[...facts.values()].filter(x=>sources.has(x.sourceId)).map(x=>x.text+' '+x.quote).join('\n');
  const checkValues=(value,where,evidence)=>{for(const extract of [numbers,links])if(differences(extract(value),extract(evidence)).length)issue('error','unsupported_value',where,'草稿含有引用资料未支持的数字或链接。','Draft numbers or links are not supported by its cited evidence.');};
  const checkPromise=(value,where,authorizationId)=>{if(!risky.test(value)&&!authorizationId)return;const authorization=allowed.get(authorizationId);if(!authorization||normalize(authorization.text)!==normalize(value))issue('error','unapproved_commitment',where,'存在敏感承诺或完成状态，未与明确允许的原文承诺一致。','A sensitive commitment/completion statement does not match an explicitly allowed statement.');};
  for(const [index,paragraph] of paragraphs.entries()){
    object(paragraph,'paragraph');text(paragraph.text,'paragraph text',5000);const refs=list(paragraph.factIds||[],'paragraph factIds',0,20),requestIds=list(paragraph.requestIds||[],'paragraph requestIds',0,20),where='paragraph-'+(index+1);
    if(!refs.length&&!requestIds.length)issue('error','uncited_paragraph',where,'段落没有事实依据或对应请求。','Paragraph has no fact evidence or linked incoming request.');
    for(const key of refs)if(!facts.has(key))issue('error','unknown_fact',where,'引用了不存在的事实编号：'+key,'Unknown fact reference: '+key);
    for(const key of requestIds){if(!requests.has(key))issue('error','unknown_request',where,'引用了不存在的请求编号：'+key,'Unknown request reference: '+key);else addressed.add(key);}
    const evidence=refs.filter(key=>facts.has(key)).map(key=>facts.get(key).text+' '+facts.get(key).quote).concat(requestIds.filter(key=>requests.has(key)).map(key=>requests.get(key).quote)).join('\n');checkValues(paragraph.text,where,evidence);checkPromise(paragraph.text,where,paragraph.commitmentId);body.push(paragraph.text);
  }
  const greeting=text(draft.greeting||'','greeting',500,true),closing=text(draft.closing||'','closing',500,true);for(const [where,value] of [['subject',draft.subject],['greeting',greeting],['closing',closing]]){checkPromise(value,where,null);checkValues(value,where,supportedFacts+'\n'+incoming.body);}
  for(const request of requests.values())if(!addressed.has(request.id))issue('warning','request_not_addressed',request.id,'尚未在草稿中回应此请求。','This request is not addressed in the draft.');
  const errors=issues.filter(x=>x.level==='error').length,warnings=issues.length-errors,report={status:errors?'blocked':'review_required',errors,warnings,requiresHumanReview:true,semanticAccuracyVerified:false,deliveryPerformed:false,channel,issues};
  const draftText=[t(lang,'【待人工核对的本地草稿；未发送】','[LOCAL DRAFT — HUMAN REVIEW REQUIRED — NOT SENT]'),'To: '+recipients.join(', '),'Subject: '+draft.subject,'',greeting,'',body.join('\n\n'),'',closing,''].join('\n');
  const checklist=['# '+t(lang,'回复核对清单','Reply review checklist'),'',t(lang,'机械检查结果：','Mechanical status: ')+report.status,'',t(lang,'未连接邮箱或客服系统，未发送消息。请核对身份、事实、金额、政策、语气和承诺后自行决定使用。','No mailbox/support API was connected and nothing was sent. Review identity, facts, amounts, policies, tone and commitments before use.'),''];for(const x of issues)checklist.push('- '+md(x.level+' · '+x.location+' · '+x.message));if(!issues.length)checklist.push(t(lang,'未发现本脚本可检测的问题；这不等于事实或授权已获独立验证。','No mechanically detected issues; facts and authorization have not been independently verified.'));checklist.push('','## '+t(lang,'事实依据','Evidence ledger'));for(const fact of facts.values())checklist.push('','### '+md(fact.id+' · '+fact.sourceId),'',block(fact.text),'',block(fact.quote));checklist.push('','## '+t(lang,'原始来信（不可信资料）','Incoming message — untrusted source material'),'',block(incoming.body));
  return {report,files:{'draft.txt':draftText,'checklist.md':checklist.join('\n')+'\n','report.json':JSON.stringify(report,null,2)+'\n'}};
}
entry(import.meta.url,'mochi-reply-drafts',analyze);
