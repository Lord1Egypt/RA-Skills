'use strict';
/** DAVYLAB Knowledge Graph Skill — original standalone implementation, MIT. */
const fail=(message)=>{throw new Error(message)};
const unique = xs => [...new Set(xs)];
function buildGraph(topics, dependencies) {
  if(!Array.isArray(topics)||!Array.isArray(dependencies)) fail('topics and dependencies must be arrays');
  const nodes = new Map();
  for(const t of topics){
    if(!t||typeof t.id!=='string'||!t.id.trim()||typeof t.subject!=='string'||!t.subject.trim()||typeof t.title!=='string'||!t.title.trim()) fail('invalid topic');
    if(nodes.has(t.id)) fail('duplicate topic: '+t.id);
    nodes.set(t.id,{...t});
  }
  const incoming = new Map([...nodes.keys()].map(id=>[id,[]]));
  const outgoing = new Map([...nodes.keys()].map(id=>[id,[]]));
  const seen=new Set();
  for(const d of dependencies){
    if(!d||!nodes.has(d.topicId)||!nodes.has(d.prerequisiteId)) fail('dangling dependency');
    if(d.topicId===d.prerequisiteId) fail('self dependency');
    if(!['hard','soft'].includes(d.strength)) fail('invalid strength');
    // Subject boundaries are explicit; cross-subject relationships belong in a separate reference list.
    if(nodes.get(d.topicId).subject!==nodes.get(d.prerequisiteId).subject) fail('cross-subject prerequisite');
    const key=d.topicId+'\u0000'+d.prerequisiteId;
    if(seen.has(key)) fail('duplicate dependency');seen.add(key);
    incoming.get(d.topicId).push({...d});outgoing.get(d.prerequisiteId).push({...d});
  }
  // Kahn topological sort: prerequisites first.
  const deg=new Map([...incoming].map(([id,edges])=>[id,edges.length]));
  const q=[...nodes.keys()].filter(id=>deg.get(id)===0).sort(), order=[];
  while(q.length){const id=q.shift();order.push(id);for(const e of outgoing.get(id)){const n=deg.get(e.topicId)-1;deg.set(e.topicId,n);if(n===0){q.push(e.topicId);q.sort()}}}
  if(order.length!==nodes.size) fail('dependency cycle detected');
  return {nodes,incoming,outgoing,order};
}
function ancestors(g,id,{includeSoft=true}={}){
  if(!g.nodes.has(id)) fail('unknown topic: '+id);
  const visited=new Set(), todo=[id];
  while(todo.length){const current=todo.pop();for(const e of g.incoming.get(current)){if(!includeSoft&&e.strength==='soft')continue;if(!visited.has(e.prerequisiteId)){visited.add(e.prerequisiteId);todo.push(e.prerequisiteId)}}}
  return g.order.filter(x=>visited.has(x));
}
function learningPath(g,targets,{includeSoft=false}={}){
  const all=new Set(targets);
  for(const id of targets)for(const a of ancestors(g,id,{includeSoft}))all.add(a);
  return g.order.filter(id=>all.has(id));
}
function createSession(g,targets,{confirm=2}={}){
  if(!Array.isArray(targets)||targets.length===0||!Number.isInteger(confirm)||confirm<1||confirm>5)fail('invalid session settings');
  for(const id of targets)if(!g.nodes.has(id))fail('unknown topic: '+id);
  return {version:1,targets:unique(targets),confirm,results:{},history:[]};
}
function applyAnswer(g,session,id,result){
  if(!g.nodes.has(id)||!['correct','wrong','skip'].includes(result))fail('invalid answer');
  const allowed=new Set(learningPath(g,session.targets,{includeSoft:true}));if(!allowed.has(id))fail('answer outside scope');
  const s=JSON.parse(JSON.stringify(session));const prev=s.results[id]||{correctStreak:0,wrongStreak:0,status:'untested'};
  const r={...prev};
  if(result==='correct'){r.correctStreak+=1;r.wrongStreak=0;r.status=r.correctStreak>=s.confirm?'mastered':(prev.status==='weak'?'shaky':'untested')}
  if(result==='wrong'){r.wrongStreak+=1;r.correctStreak=0;r.status=r.wrongStreak>=2?'weak':'shaky'}
  if(result==='skip'){r.status='untested';r.correctStreak=0}
  s.results[id]=r;s.history.push({id,result});return s;
}
function nextTopic(g,s){
  const candidates=learningPath(g,s.targets,{includeSoft:false});
  // First probe targets; after confirmed weakness, probe prerequisite roots, never claim mastery by inference.
  const weak=Object.keys(s.results).filter(id=>s.results[id].status==='weak');
  const priority=unique([...weak.flatMap(id=>ancestors(g,id,{includeSoft:false})),...s.targets,...candidates]);
  return priority.find(id=>!s.results[id]||!['mastered','weak'].includes(s.results[id].status))||null;
}
function summarize(g,s){
  const groups={mastered:[],shaky:[],weak:[],untested:[]};
  for(const id of learningPath(g,s.targets,{includeSoft:false})){
    const status=s.results[id]?.status||'untested';groups[status].push(id);
  }
  const rootCauses=groups.weak.filter(id=>!ancestors(g,id,{includeSoft:false}).some(a=>groups.weak.includes(a)));
  const remediation=learningPath(g,unique([...groups.weak,...groups.shaky]),{includeSoft:false});
  return {groups,rootCauses,remediation,attempts:s.history.length,disclaimer:'Screening hints only; educator review required.'};
}
module.exports={buildGraph,ancestors,learningPath,createSession,applyAnswer,nextTopic,summarize};
