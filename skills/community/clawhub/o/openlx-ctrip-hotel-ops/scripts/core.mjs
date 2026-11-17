import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import os from 'node:os';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, 'references/catalog.json')));
export const hash = value => crypto.createHash('sha256').update(typeof value === 'string' || Buffer.isBuffer(value) ? value : JSON.stringify(value)).digest('hex');
export const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const now = () => new Date().toISOString();
export const money = fen => Number.isInteger(fen) ? `¥${(fen / 100).toFixed(2)}` : 'UNKNOWN';
export function safeId(id) { if (!/^[\w-]{1,80}$/.test(String(id))) throw Error('ID格式不正确'); return String(id); }
export function writeJson(file, data) { fs.mkdirSync(path.dirname(file), {recursive:true, mode:0o700}); fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n', {mode:0o600}); }
export function redact(value) {
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).filter(([k]) => !/password|secret|cookie|token|guest_name|phone|mobile|id_card|passport|guest_email|order_no/i.test(k)).map(([k,v]) => [k,redact(v)]));
  if (typeof value === 'string') return value.replace(/\b1[3-9]\d{9}\b/g,'[手机号已隐藏]').replace(/\b\d{17}[\dXx]\b/g,'[证件号已隐藏]');
  return value;
}
export function openWorkspace(folder) {
  const base=path.resolve(folder); fs.mkdirSync(base,{recursive:true,mode:0o700});
  const db=new DatabaseSync(path.join(base,'operations.sqlite'));
  db.exec(`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;
    CREATE TABLE IF NOT EXISTS actions(id TEXT PRIMARY KEY, hotel_id TEXT NOT NULL, kind TEXT NOT NULL, object_id TEXT NOT NULL, payload TEXT NOT NULL, content_hash TEXT NOT NULL, status TEXT NOT NULL, approval_hash TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
    CREATE UNIQUE INDEX IF NOT EXISTS action_content ON actions(hotel_id,kind,object_id,content_hash);
    CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, action_id TEXT, environment TEXT, status TEXT, evidence TEXT, created_at TEXT);
    CREATE TABLE IF NOT EXISTS assets(hash TEXT PRIMARY KEY, filepath TEXT, metadata TEXT, status TEXT, updated_at TEXT);
    CREATE TABLE IF NOT EXISTS locks(hotel_id TEXT PRIMARY KEY, owner TEXT, acquired_at TEXT);
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);`);
  return {base,db,close:()=>db.close()};
}
export function validateSnapshot(s, hotelId) {
  if (!s || !s.hotel || !safeId(s.hotel.id)) throw Error('缺少hotel.id');
  if (s.hotel.id!==hotelId) throw Error('HOTEL_MISMATCH');
  if (!s.hotel.name || !s.source?.type || !Number.isFinite(Date.parse(s.observed_at))) throw Error('缺少门店名称、来源类型或有效观察时间');
  if (!['USER_EXPORT','LIVE','MOCK'].includes(s.source.type)) throw Error('SOURCE_TYPE_INVALID');
  if (s.source.type==='LIVE' && (!s.source.account_id || !s.source.reference)) throw Error('真实数据需账户和来源引用');
  for (const key of ['rooms','rates','inventory','orders','reviews','promotions','competitors','events','facts']) if (s[key]!=null && !Array.isArray(s[key])) throw Error(`${key}必须是数组，缺失请用null`);
  for (const r of s.rates||[]) if (!Number.isInteger(r.price_fen)||r.price_fen<0) throw Error('PRICE_MUST_BE_INTEGER_FEN');
  return s;
}
export function classifyReview(r) {
  const text=String(r.text||'').trim();
  if (r.replied) return {classification:'ALREADY_REPLIED',auto:false};
  if (!r.id || !text) return {classification:'UNKNOWN',auto:false};
  const complaint=/但是|不过|可惜|就是|一般|不太|不够|不好|不好意思|没有|没能|吵|噪|差|脏|臭|失望|投诉|索赔|退钱|漏水|异味|蚊|隔音|遗憾|希望|改善|有待|不满意|not|but|however|dirty|noisy|bad|terrible|disappoint/i;
  if (complaint.test(text)||Number(r.rating)<5) return {classification:'REQUIRES_CONFIRMATION',auto:false};
  // A small whitelist is a deliberate no-model fallback, not a semantic classifier.
  const stripped=text.replace(/[\s，。！!,.👍😊❤️～~]/g,'');
  const tokens=['非常满意','很满意','满意','很好','好评','干净整洁','干净','服务很好','服务热情','位置方便','推荐','下次还来','环境很好','五星好评'];
  let rest=stripped; for(const t of tokens.sort((a,b)=>b.length-a.length))rest=rest.split(t).join('');
  return rest===''&&stripped!==''&&Number(r.rating)===5 ? {classification:'CLEAR_POSITIVE',auto:true} : {classification:'REQUIRES_CONFIRMATION',auto:false};
}
export function reviewDraft(r,s) {
  const decision=classifyReview(r);
  if(decision.classification==='ALREADY_REPLIED')return {...decision,reply:null};
  const reply=decision.auto ? `感谢您对${s.hotel.name}的认可！很高兴这次入住为您留下了美好感受。期待与您再次相见，祝您旅途愉快！` : `感谢您分享入住感受。我们重视您反馈的情况，会认真核实具体问题。欢迎通过平台联系${s.hotel.name}，帮助我们进一步了解细节。`;
  return {...decision,reply,known_facts:[s.hotel.name],missing_facts:decision.auto?[]:['核实点评涉及的具体情况及可公开说明的处理进展'],internal_action:decision.auto?'保留获得认可的服务细节':'核实问题、落实责任人与复查时间；未完成不宣称整改'};
}
export function metrics(s) {
  const m=s.metrics;
  if(!m || !m.scope || !Number.isFinite(m.available_room_nights)||!Number.isFinite(m.sold_room_nights)||!Number.isInteger(m.room_revenue_fen)||m.available_room_nights<=0||m.sold_room_nights<0||m.sold_room_nights>m.available_room_nights) return {status:'UNKNOWN',reason:'缺少同口径可售房晚、已售房晚、客房收入和统计范围'};
  if(m.scope==='PROPERTY'&&!m.authoritative_source)return {status:'UNKNOWN',reason:'缺少全店权威数据，不能给出全店入住率'};
  return {status:'KNOWN',scope:m.scope,period:m.period||'未提供',basis:m.basis||'口径待核实',occupancy:m.sold_room_nights/m.available_room_nights,adr_fen:m.sold_room_nights?Math.round(m.room_revenue_fen/m.sold_room_nights):null,revpar_fen:Math.round(m.room_revenue_fen/m.available_room_nights),source:m.authoritative_source||s.source.reference};
}
export function promotionNet(p) {
  if(p.net_settlement_fen!=null)return Number.isInteger(p.net_settlement_fen)?{status:'KNOWN',net_fen:p.net_settlement_fen,basis:'实际净结算金额，未重复扣减费用'}:{status:'UNKNOWN'};
  const keys=['gross_fen','merchant_discount_fen','commission_base_fen','commission_bps','platform_fee_fen','included_cost_fen'];
  if(!keys.every(k=>Number.isInteger(p[k])&&p[k]>=0)||p.rules_verified!==true)return {status:'UNKNOWN',missing:keys.filter(k=>!Number.isInteger(p[k])),reason:'费用承担、佣金基数或叠加规则待核实'};
  return {status:'KNOWN',net_fen:p.gross_fen-p.merchant_discount_fen-Math.round(p.commission_base_fen*p.commission_bps/10000)-p.platform_fee_fen-p.included_cost_fen,basis:'平台承担优惠未作为商家支出扣减'};
}
export function comparable(a,b) {
  const keys=['checkin','checkout','adults','rooms','breakfast','cancellation','currency','tax_basis','member_condition','room_class'];
  const mismatches=keys.filter(k=>a[k]==null||b[k]==null||JSON.stringify(a[k])!==JSON.stringify(b[k]));
  return {comparable:!mismatches.length&&a.status==='AVAILABLE'&&b.status==='AVAILABLE',mismatches,status:b.status||'NOT_OBSERVED',price_fen:b.status==='AVAILABLE'?b.price_fen:null};
}
export const sections=[['hotel','门店资料'],['rooms','房型产品'],['rates','房价与收益'],['competitors','同行比价'],['inventory','房态与库存'],['orders','订单与接待'],['promotions','活动到手价'],['reviews','点评与整改'],['events','需求日历'],['facts','酒店事实'],['content','内容获客']];
export function diagnose(s) {
  const issues=[]; const add=(module,priority,problem,why,action,source,extra={})=>issues.push({module,priority,problem,why,action,evidence:source||s.source.reference||'用户导入',scope:s.hotel.id,automatic:false,confirmation:'门店负责人',status:'PROPOSED',result:'尚未执行',review_at:new Date(Date.now()+86400000).toISOString(),...extra});
  for(const [key,label]of sections)if(s[key]==null)add(label,'UNKNOWN',`${label}数据未提供`,'缺少数据不能判为正常',`补充${label}的当前导出或授权读取`,s.source.reference);
  if(!s.hotel.description)add('门店资料','P2','门店介绍未提供','客人难以理解真实特色','补充位置、客群与已核实的服务卖点');
  if(Date.now()-Date.parse(s.observed_at)>86400000)add('数据时效','P1','快照超过24小时','价格、库存与待回点评可能变化','重新读取后再执行任何写动作');
  for(const r of s.rates||[])if(Number.isInteger(r.floor_fen)&&r.price_fen<r.floor_fen)add('房价与收益','P1',`${r.date} ${r.room_id}低于底价`, '该价可能侵蚀净收益',`核实价格并在授权范围内恢复至至少${money(r.floor_fen)}`,r.source_reference);
  if(!s.inventory_authority)add('房态与库存','P1','全店库存权威来源未配置','携程可售量不等于全店可用库存','配置PMS或可靠全渠道库存；暂不自动开房或承诺库存');
  for(const r of s.inventory||[])if(Number.isFinite(r.available)&&r.available<0)add('房态与库存','P1',`${r.date} ${r.room_id}库存为负`,'存在超卖风险','核对维护房、自用房及渠道配额，联系负责人');
  for(const r of s.reviews||[]){const d=classifyReview(r);if(!r.replied)add('点评与整改',d.auto?'P2':'P1',`点评${r.id}待回复`,d.auto?'及时回应真实好评':'包含投诉或语义尚不能确定',d.auto?'按已开通授权生成商家回复':'核实事实并确认最终回复文案',r.source_reference,{automatic:d.auto,review_id:r.id});}
  for(const p of s.promotions||[]){const n=promotionNet(p);if(n.status==='UNKNOWN')add('活动到手价','UNKNOWN',`${p.name||p.id}无法精算净回款`,'佣金或承担方不明确','补齐佣金基数、商家优惠、平台费用及叠加顺序');else if(n.net_fen<0)add('活动到手价','P1',`${p.name||p.id}测算净回款为负`,'已知费用超过收入','确认是否暂停该优惠组合，保留旧配置');}
  for(const q of s.competitors||[])if(q.status!=='AVAILABLE')add('同行比价','UNKNOWN',`${q.hotel_name||q.hotel_id}：${q.status||'NOT_OBSERVED'}`,'售罄和采集失败都不是零元报价','保持原因、采样时间与条件；等待有效样本后比较');
  for(const ev of s.events||[])if(!ev.source_url||!ev.verified_at||Date.parse(ev.end_date)<Date.now())add('需求日历','UNKNOWN',`${ev.name}待核验或已过期`,'不能独立作为自动涨价依据','核验主办方来源、地点、日期与实际影响');
  if((s.orders||[]).some(o=>o.status==='PENDING'))add('订单与接待','P1','存在待处理订单','需及时核对入住与特殊需求','查看今日接待清单；接单前检查权威库存');
  const checked=sections.filter(([k])=>s[k]!=null).length;
  return {issues,coverage:{checked,total:sections.length,percentage:Math.round(checked/sections.length*100),unknown:sections.filter(([k])=>s[k]==null).map(([,l])=>l)},metrics:metrics(s)};
}
export function verifyLicense(envelope, publicKey, hotelId, time=Date.now()) {
  try{
    if(!envelope?.payload||!envelope.signature||!publicKey)return null;
    const raw=Buffer.from(envelope.payload,'base64url');
    if(!crypto.verify(null,raw,publicKey,Buffer.from(envelope.signature,'base64url')))return null;
    const p=JSON.parse(raw);if(p.product!==catalog.id||p.hotel_id!==hotelId||!['STANDARD','SUPREME'].includes(p.plan)||Date.parse(p.expires_at)<=time||Date.parse(p.offline_valid_until)<=time||!Number.isFinite(Date.parse(p.expires_at))||!Number.isFinite(Date.parse(p.offline_valid_until)))return null;
    return p;
  }catch{return null;}
}
export function entitlement(base,hotelId) {
  try{const p=verifyLicense(JSON.parse(fs.readFileSync(path.join(base,'license.json'))),fs.readFileSync(path.join(ROOT,'assets/license-public.txt'),'utf8'),hotelId);return p&&p.device_id===fs.readFileSync(path.join(os.homedir(),'.openlx-ctrip-device/id'),'utf8').trim()?p:{plan:'FREE'};}catch{return {plan:'FREE'};}
}
function reportDomain(key,value){
  const unknown='UNKNOWN：未提供';
  const rows=key==='orders'?(value||[]).map(o=>({order_ref:o.id?'订单-'+hash(String(o.id)).slice(0,8):unknown,status:o.status,checkin:o.checkin,checkout:o.checkout,room_id:o.room_id,rooms:o.rooms,nights:o.nights,inventory_confirmed:o.inventory_confirmed})):redact(value);
  const fields={rooms:[['name','房型'],['id','房型标识'],['capacity','人数'],['breakfast','早餐'],['cancellation','取消规则']],rates:[['room_id','房型'],['plan_id','价计划'],['date','入住日期'],['price_fen','挂牌价'],['floor_fen','底价']],competitors:[['hotel_name','同行'],['checkin','入住'],['breakfast','早餐'],['cancellation','取消'],['status','采样状态'],['price_fen','报价']],inventory:[['room_id','房型'],['date','日期'],['available','渠道可售量']],orders:[['order_ref','脱敏索引'],['status','状态'],['checkin','入住'],['checkout','离店'],['rooms','间数']],promotions:[['name','活动'],['gross_fen','订单金额'],['net_settlement_fen','实际净结算']],reviews:[['id','点评标识'],['rating','星级'],['text','真实点评'],['replied','已回复']],events:[['name','需求事件'],['start_date','开始'],['end_date','结束'],['source_url','来源'],['verified_at','核验时间']],facts:[['text','酒店事实'],['verified','已核实'],['source_reference','事实来源']]};
  if(!Array.isArray(rows)||!fields[key])return `<pre>${esc(JSON.stringify(rows,null,2))}</pre>`;
  if(!rows.length)return '<p>当前来源未返回记录。空列表仅代表此次读取结果，不代表所有风险已经排除。</p>';
  const table=`<div class="table-wrap"><table><thead><tr>${fields[key].map(([,label])=>`<th>${esc(label)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${fields[key].map(([f])=>`<td>${esc(r[f]==null?unknown:f.endsWith('_fen')?money(r[f]):typeof r[f]==='object'?JSON.stringify(r[f]):String(r[f]))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  return table+`<details><summary>查看本节脱敏证据字段</summary><pre>${esc(JSON.stringify(rows,null,2))}</pre></details>`;
}
export function renderReport(s,license={plan:'FREE'},history=[]) {
  const d=diagnose(s),paid=['STANDARD','SUPREME'].includes(license.plan),e=esc;
  const plain=x=>e(JSON.stringify(redact(x),null,2));
  const rows=d.issues.map(i=>`<article class="issue"><span class="priority">${e(i.priority)} · ${e(i.module)}</span><h3>${e(i.problem)}</h3><p>${e(i.why)}</p><p><b>建议：</b>${e(i.action)}</p><dl><dt>证据 / 范围</dt><dd>${e(i.evidence)} / ${e(i.scope)}</dd><dt>执行</dt><dd>${i.automatic?'满足授权可自动执行':'需确认'} · ${e(i.status)} · ${e(i.result)}</dd><dt>确认 / 复查</dt><dd>${e(i.confirmation)} / ${e(i.review_at)}</dd></dl></article>`).join('');
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${e(s.hotel.name)} · 经营体检报告</title><style>body{font:16px/1.8 "PingFang SC","Microsoft YaHei",sans-serif;color:#172b49;background:#f6f4ee;margin:0}main{max-width:1080px;margin:auto;padding:40px 24px}h1{font-size:34px;line-height:1.35}h2{margin-top:48px;border-top:2px solid #1764d5;padding-top:24px}h3{margin:8px 0}a{color:#155aba}.notice{background:#fff3c8;padding:16px;border-left:4px solid #ac7400}.summary{display:flex;flex-wrap:wrap;gap:20px}.summary article,.issue{background:white;border:1px solid #d3dae5;padding:22px;margin:12px 0;border-radius:8px}.summary article{flex:1;min-width:180px}.priority{color:#6a4b04;font-size:13px}nav{display:flex;flex-wrap:wrap;gap:14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:18px;font-size:13px;max-height:700px;overflow:auto}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;background:#fff;font-size:14px}th,td{padding:12px;text-align:left;border:1px solid #d3dae5;min-width:90px;overflow-wrap:anywhere}th{background:#eaf0fa}details{margin-top:14px}dl{font-size:13px}dt{font-weight:bold}dd{margin:0 0 8px}footer{font-size:13px;margin-top:40px;color:#53627a}@media print{body{background:white}nav{display:none}pre{max-height:none;overflow:visible}.issue{break-inside:avoid}}@media(max-width:500px){h1{font-size:27px}main{padding:24px 16px}}</style></head><body><main><p>经营报告 · ${e(license.plan)} · ${e(now().slice(0,10))}</p><h1>${e(s.hotel.name)}<br>把发现的问题，落实到下一步。</h1>${s.source.type==='MOCK'?'<p class="notice">演示数据：用于说明报告结构，未读取真实门店，未执行后台动作。</p>':''}<p>数据采样：${e(s.observed_at)} · 来源：${e(s.source.type)} / ${e(s.source.reference||'用户导入')}</p><div class="summary"><article><b>数据覆盖</b><h3>${d.coverage.checked}/${d.coverage.total} · ${d.coverage.percentage}%</h3><p>内部运营诊断覆盖率，非平台官方分值。</p></article><article><b>待处理发现</b><h3>${d.issues.length}项</h3><p>全部发现均可见；未知项未视作健康。</p></article><article><b>执行结果</b><h3>未自动执行</h3><p>报告生成不触发改价、接单或发布。</p></article></div><nav><a href="#actions">今日优先动作</a>${sections.map(([k,l])=>`<a href="#${k}">${l}</a>`).join('')}<a href="#sources">来源口径</a></nav><h2 id="actions">今日优先动作与完整问题清单</h2>${rows||'<p>当前已检查数据未触发规则；不代表所有经营风险已经排除。</p>'}<h2>经营指标与口径</h2><pre>${plain(d.metrics)}</pre>${sections.map(([key,label])=>`<section id="${key}"><h2>${e(label)}</h2>${s[key]==null?`<p>UNKNOWN：尚缺${e(label)}数据。补充当前导出或授权读取后复查。</p>`:reportDomain(key,key==='promotions'?(s[key]||[]).map(p=>({...p,calculation:promotionNet(p)})):s[key])}${key==='content'?'<p>选题建议：入住前须知、已核实房型选择、周边出行提示。素材或事实缺失时先补拍补证据。</p>':''}</section>`).join('')}${paid?`<h2>多期趋势与专项复盘</h2>${history.length?`<pre>${plain(history.map(x=>({observed_at:x.observed_at,metrics:metrics(x),coverage:diagnose(x).coverage})))}</pre>`:'<p>暂无可比较历史快照；积累同口径样本后再分析趋势。</p>'}`:''}<h2 id="sources">证据、执行口径与下次复查</h2><p>报告依照本次快照计算；数据范围、日期、权利说明和适用的AI内容标识保留。未观测的入住率、流量或收益归因显示UNKNOWN。写任务以独立动作账本与同对象回读为准。</p><footer>${paid?'':'OpenLX 携程酒店运营助手 · 法匠科技提供技术支持<br>'}数据属于酒店。本文是内部运营诊断与行动建议，不是携程官方评分。离线可阅，报告不包含操作凭证。</footer></main></body></html>`;
}
export function priceProposal(s,rate,policy,prior=[],license={plan:'FREE'}) {
  const errors=[];const next=policy.target_fen;const old=rate.price_fen;
  if(policy.mode==='AUTOMATIC'&&!['STANDARD','SUPREME'].includes(license.plan))errors.push('PAID_LICENSE_REQUIRED');
  if(policy.strategy==='MULTI_SIGNAL'&&license.plan!=='SUPREME')errors.push('SUPREME_REQUIRED');
  if(!Number.isInteger(next)||next<=0||!Number.isInteger(old)||old<=0)errors.push('INVALID_PRICE');
  const required=['floor_fen','ceiling_fen','max_change_bps','daily_change_bps','daily_count','cooldown_minutes','valid_until','dates','room_ids'];
  if(required.some(k=>policy[k]==null))errors.push('POLICY_INCOMPLETE');
  if(!policy.dates?.includes(rate.date)||!policy.room_ids?.includes(rate.room_id))errors.push('OUT_OF_SCOPE');
  if(Date.parse(policy.valid_until)<=Date.now()||!Number.isFinite(Date.parse(policy.valid_until)))errors.push('AUTH_EXPIRED');
  if(next<Math.max(rate.floor_fen||0,policy.floor_fen||0))errors.push('BELOW_FLOOR');
  if(next>policy.ceiling_fen)errors.push('ABOVE_CEILING');
  const delta=Math.abs(next-old)/old*10000;
  if(delta>policy.max_change_bps)errors.push('CHANGE_LIMIT');
  const date=now().slice(0,10);const recent=prior.filter(a=>a.object_id===`${rate.room_id}:${rate.plan_id}:${rate.date}`&&a.updated_at?.slice(0,10)===date&&a.status==='VERIFIED');
  const used=recent.reduce((sum,a)=>{const p=typeof a.payload==='string'?JSON.parse(a.payload):a.payload;return sum+Math.abs(p.after-p.before)/p.before*10000;},0);
  if(used+delta>policy.daily_change_bps)errors.push('DAILY_CHANGE_LIMIT');
  if(recent.length>=policy.daily_count)errors.push('DAILY_COUNT_LIMIT');
  if(recent.some(a=>Date.now()-Date.parse(a.updated_at)<policy.cooldown_minutes*60000))errors.push('COOLDOWN');
  if(Date.now()-Date.parse(s.observed_at)>(policy.max_age_minutes||60)*60000)errors.push('STALE_DATA');
  if(s.price_authority&&s.price_authority!=='CTRIP')errors.push('PMS_AUTHORITY');
  if(policy.net_floor_fen!=null){const net=promotionNet({...policy.settlement,gross_fen:next});if(net.status!=='KNOWN')errors.push('NET_UNKNOWN');else if(net.net_fen<policy.net_floor_fen)errors.push('BELOW_NET_FLOOR');}
  if(policy.strategy==='MULTI_SIGNAL'&&(!policy.verified_signals||policy.verified_signals.length<2||policy.verified_signals.some(x=>!x.source_reference||!Number.isFinite(Date.parse(x.observed_at)))))errors.push('SIGNALS_UNVERIFIED');
  return {kind:'PRICE',hotel_id:s.hotel.id,object_id:`${rate.room_id}:${rate.plan_id}:${rate.date}`,before:old,after:next,rate,policy,mode:policy.mode||'CONFIRMED',environment:s.source.type,account_id:s.source.account_id||null,eligible:errors.length===0,errors};
}
export function enqueue(w,payload) {
  const h=hash(payload); const existing=w.db.prepare('SELECT * FROM actions WHERE hotel_id=? AND kind=? AND object_id=? AND content_hash=?').get(payload.hotel_id,payload.kind,payload.object_id,h);
  if(existing)return existing;
  const id=crypto.randomUUID();const status=payload.eligible===false?'BLOCKED':'AWAITING_APPROVAL';
  w.db.prepare('INSERT INTO actions VALUES(?,?,?,?,?,?,?,?,?,?)').run(id,payload.hotel_id,payload.kind,payload.object_id,JSON.stringify(payload),h,status,null,now(),now());return w.db.prepare('SELECT * FROM actions WHERE id=?').get(id);
}
export function approve(w,id,h) {
  const a=w.db.prepare('SELECT * FROM actions WHERE id=?').get(id);if(!a||a.content_hash!==h)throw Error('CONTENT_CHANGED');
  if(!['AWAITING_APPROVAL','APPROVED'].includes(a.status))throw Error('ACTION_NOT_APPROVABLE');
  w.db.prepare('UPDATE actions SET approval_hash=?,status=?,updated_at=? WHERE id=?').run(h,'APPROVED',now(),id);return {id,status:'APPROVED',content_hash:h};
}
export function recordAttempt(w,a,status,evidence) {
  w.db.prepare('INSERT INTO attempts(action_id,environment,status,evidence,created_at) VALUES(?,?,?,?,?)').run(a.id,JSON.parse(a.payload).environment,status,JSON.stringify(redact(evidence)),now());
  w.db.prepare('UPDATE actions SET status=?,updated_at=? WHERE id=?').run(status,now(),a.id);
}
export function scanAssets(w,folder,manifest) {
  const root=path.resolve(folder),results=[];
  for(const entry of fs.readdirSync(root,{withFileTypes:true})){
    if(!entry.isFile()||! /\.(png|jpe?g|webp)$/i.test(entry.name))continue;
    const file=path.join(root,entry.name),stat=fs.statSync(file),meta=manifest[entry.name]||{};
    if(Date.now()-stat.mtimeMs<5000){results.push({file:entry.name,status:'WAITING_STABLE'});continue;}
    const digest=hash(fs.readFileSync(file));
    const status=meta.hotel_id&&meta.rights_confirmed===true&&meta.channels?.includes('CTRIP')&&meta.scene&&meta.sensitive!==true&&(!meta.has_people||meta.people_authorized===true)?'ELIGIBLE':'NEEDS_RIGHTS_OR_FACTS';
    const exists=w.db.prepare('SELECT hash FROM assets WHERE hash=?').get(digest);
    w.db.prepare('INSERT INTO assets VALUES(?,?,?,?,?) ON CONFLICT(hash) DO UPDATE SET metadata=excluded.metadata,status=excluded.status,updated_at=excluded.updated_at').run(digest,file,JSON.stringify(meta),status,now());
    results.push({file:entry.name,hash:digest,status,duplicate:!!exists});
  }return results;
}
export function validatePersona(p){for(const k of ['positioning','voice','audience','selling_points','forbidden','topics','examples'])if(!p[k])throw Error(`人设缺少${k}`);if(p.topics.length<30||p.examples.length<3)throw Error('需30天选题与3篇示范稿');return p;}
export function distillPersona(s,answers){
  const facts=(s.facts||[]).filter(f=>f.verified===true).map(f=>f.text),themes=['入住前准备','如何选择房型','周边出行提示','店内一天','适合怎样的客人','季节旅行','主理人的服务细节','常见问题','照片背后的空间','安静度过周末'];
  const p={positioning:answers.positioning||`${s.hotel.name}的真实入住与目的地指南`,voice:answers.voice||{style:'平实、具体，以商家身份表达',ending:'出行前欢迎通过平台了解当前房型与政策。'},audience:answers.audience||['准备预订的旅行者'],selling_points:facts,forbidden:answers.forbidden||['全网最低','百分百满房','本人亲测','保证涨价','官方认证'],topics:Array.from({length:30},(_,i)=>`${i+1}. ${themes[i%themes.length]}：${i<10?'真实信息':i<20?'出行答疑':'场景分享'}`),examples:[],facts_hash:hash(facts),source:'HOTEL_QUESTIONNAIRE_AND_VERIFIED_FACTS',created_at:now(),review_status:'AWAITING_OWNER_REVIEW'};
  p.examples=p.topics.slice(0,3).map(topic=>({title:`${s.hotel.name}｜${topic.slice(3)}`,body:`这里是${s.hotel.name}。\n\n${facts.slice(0,4).join('\n\n')}\n\n请按具体入住日期核对当前预订页面。`}));return p;
}
export function operationalProposal(s,input){
  const errors=[],kind=input.kind;
  if(!['INVENTORY','ORDER','PROPERTY','PROMOTION'].includes(kind))errors.push('UNSUPPORTED_ACTION');
  if(!input.object_id||input.before===undefined||input.after===undefined)errors.push('TARGET_AND_DIFF_REQUIRED');
  if(kind==='INVENTORY'){
    if(!Number.isInteger(input.after)||input.after<0)errors.push('INVALID_INVENTORY');
    if(input.mode==='AUTOMATIC'&&!s.inventory_authority)errors.push('AUTHORITATIVE_INVENTORY_REQUIRED');
    if(s.inventory_authority&&s.inventory_authority!=='CTRIP')errors.push('PMS_AUTHORITY');
  }
  if(kind==='ORDER'&&(input.after!=='ACCEPTED'||!input.inventory_confirmed||!s.inventory_authority))errors.push('ORDER_INVENTORY_CONFIRMATION_REQUIRED');
  if(kind==='PROPERTY'&&!input.verified_fact_ids?.length)errors.push('VERIFIED_FACTS_REQUIRED');
  if(kind==='PROPERTY'&&input.verified_fact_ids?.some(id=>!(s.facts||[]).some(f=>f.id===id&&f.verified===true)))errors.push('UNKNOWN_FACT');
  if(kind==='PROMOTION'&&!input.costs_confirmed)errors.push('COST_CONFIRMATION_REQUIRED');
  return {...input,hotel_id:s.hotel.id,environment:s.source.type,account_id:s.source.account_id||null,mode:'CONFIRMED',eligible:!errors.length,errors};
}
export function revenueSuggestion(s,rate,policy){
  const reasons=[],signals=[];let factor=1;
  const m=metrics(s);if(m.status==='KNOWN'){const target=policy.occupancy_target??0.7;const delta=m.occupancy<target?-0.03:0.03;factor+=delta;signals.push({type:'BOOKING_PACE',source_reference:s.source.reference,observed_at:s.observed_at});reasons.push(`同口径预订进度${(m.occupancy*100).toFixed(1)}%，目标${target*100}%`);}
  const quotes=(s.competitors||[]).filter(q=>q.checkin===rate.date&&q.status==='AVAILABLE'&&q.conditions_verified===true&&Number.isInteger(q.price_fen)&&q.source_reference&&Date.now()-Date.parse(q.observed_at)<86400000).sort((a,b)=>a.price_fen-b.price_fen);
  if(quotes.length){const median=quotes[Math.floor(quotes.length/2)].price_fen;factor+=Math.max(-.03,Math.min(.03,(median-rate.price_fen)/rate.price_fen*.25));signals.push({type:'COMPARABLE_COMPETITORS',source_reference:quotes.map(q=>q.source_reference).join(', '),observed_at:quotes[0].observed_at});reasons.push(`已核验条件的同行中位报价${money(median)}，仅作为辅助信号`);}
  const events=(s.events||[]).filter(e=>e.source_url&&e.verified_at&&e.start_date<=rate.date&&e.end_date>=rate.date&&e.impact_confirmed===true);if(events.length){factor+=.02;signals.push({type:'VERIFIED_DEMAND',source_reference:events[0].source_url,observed_at:events[0].verified_at});reasons.push('有经核验且影响已确认的需求事件');}
  const target=Math.max(policy.floor_fen,Math.min(policy.ceiling_fen,Math.round(rate.price_fen*factor)));
  return {target_fen:target,verified_signals:signals,reasons,scenario:'规则情景建议，不是收益保证',eligible_for_multi_signal:signals.length>=2};
}
export function createContent(s,topic,assets,persona=null) {
  const facts=(s.facts||[]).filter(f=>f.verified===true&&f.text&&(!f.valid_until||Date.parse(f.valid_until)>Date.now()));
  const eligible=assets.filter(a=>a.status==='ELIGIBLE'&&JSON.parse(a.metadata).hotel_id===s.hotel.id);
  if(!facts.length||!eligible.length)return {status:'NEEDS_MATERIALS',missing:[...(!facts.length?['补充已核实酒店事实']:[]),...(!eligible.length?['补充带发布权利与场景说明的照片']:[])],publish_status:'NOT_SUBMITTED'};
  const title=`${s.hotel.destination||s.hotel.name}｜${topic}`;
  const intro=persona?.positioning?`${persona.positioning}\n\n`:'';
  const separator=persona?.voice?.layout==='bullets'?'\n• ':'\n\n';
  const ending=persona?.voice?.ending||'具体日期的房型与入住政策，请以预订页面和门店确认为准。';
  const body=`${intro}这里是${s.hotel.name}。关于「${topic}」，我们整理了这些真实信息，供您安排出行时参考。\n\n${facts.map(f=>f.text).join(separator)}\n\n${ending}`;
  if(persona?.forbidden?.some(word=>(title+body).includes(word)))return {status:'AWAITING_REWRITE',reason:'触及人设禁用表达',publish_status:'NOT_SUBMITTED'};
  return {id:crypto.randomUUID(),hotel_id:s.hotel.id,title,body,assets:eligible.slice(0,9).map(a=>({path:a.filepath,hash:a.hash,alt:JSON.parse(a.metadata).scene})),fact_sources:facts.map(f=>f.source_reference||'门店确认'),persona_applied:!!persona,persona_hash:persona?hash(persona):null,seo:{title,description:body.slice(0,120),keywords:[s.hotel.destination,topic,s.hotel.name].filter(Boolean)},status:'DRAFT_READY',publish_status:'NOT_SUBMITTED',created_at:now(),ai_label:'AI辅助生成，请核对事实并按平台要求标识'};
}
