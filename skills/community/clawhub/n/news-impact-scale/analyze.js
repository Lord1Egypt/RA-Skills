#!/usr/bin/env node
/**
 * News Impact Scale — Main Analysis Engine v1.1
 * Stage 1: Fetch → classify → extract → output structured JSON + benchmark queries
 * Stage 3: Final report — run after agent feeds back benchmark search results
 */
const fs   = require('fs');
const path = require('path');
const SKILL_DIR = path.dirname(__filename);
const { fetchUrl, htmlToText, extractTitle } = require('./lib/fetcher');
const { classifyEvent, extractLocation, findAffectedSystems } = require('./lib/classifier');
const { getCachedBenchmarks, buildBenchmarkQueries, addBenchmark, parseBenchmarkFromText } = require('./lib/benchmarker');
const { projectAll } = require('./lib/projector');
const { buildPlainEnglish } = require('./lib/explainer');

function loadContext() {
  try { return JSON.parse(fs.readFileSync(path.join(SKILL_DIR,'context.json'),'utf8')); }
  catch { return null; }
}

function assessRelevance(location, eventType, context) {
  if (!context) return { geographic:'🟡 Unknown', thematic:'🟡 Unknown', overall:'🟡 Undefined' };
  const city=(context.location.city||'').toLowerCase(), country=(context.location.country||'').toLowerCase();
  const interests=(context.interests||[]).map(i=>i.toLowerCase()), locL=location.toLowerCase();
  const geoScore=locL.includes(city)?3:locL.includes(country)?2:1;
  const geoMap=['🟢 Low — far from you','🟡 Moderate — same country','🔴 Highly Relevant — near you'];
  return {
    geographic: geoMap[geoScore-1]||geoMap[0],
    thematic: interests.some(i=>locL.includes(i)||eventType.toLowerCase().includes(i)) ? '🔴 High — matches your interests' : '🟡 Moderate',
    overall: geoScore>=2?'🔴 High personal relevance':geoScore===1?'🟡 Moderate relevance':'🟢 Low direct relevance',
  };
}

function extractKeywords(text,n=20) {
  const stop=new Set(['the','a','an','and','or','but','in','on','at','to','for','of','with','by','is','are','was','were','be','been','have','has','had','do','does','did','will','would','could','should','may','might','this','that','these','those','it','its','they','them','their','we','our','you','your','i','my','he','she','what','which','who','when','where','how','not','no','so','if','then','than','as','from','up','out','about','into','over','after','between','under','again','more','some','any','all','each','every','both','few','most','other','such','only','own','same','just','also','now','here','there','because','while','although','though','said','says','according','report','reported','new','news','via','one','two','three','first','last','next','year','years','day','days','week','weeks','month','months','time','percent','million','billion','world','global','country','government','company','companies','official','officials','told','announced','around','near','across','area','region','local','authorities','people','others']);
  const words=text.toLowerCase().replace(/[^a-z\s]/g,' ').split(/\s+/);
  const freq={}; words.forEach(w=>{ if(w.length>3&&!stop.has(w)) freq[w]=(freq[w]||0)+1; });
  return Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0,n).map(e=>e[0]);
}

function formatReport(s1) {
  const d='─'.repeat(60), now=new Date().toUTCString();
  let r=`
${d}
         NEWS IMPACT SCALE — ANALYSIS REPORT
${d}
  Generated:  ${now}
  Article:    ${s1.title}
  Location:   ${s1.location}
  Type:       ${s1.eventType}
  Confidence: ${s1.confidence}
  URL:        ${s1.url}
${d}
📰 WHAT THE NEWS SAYS
${d}
${s1.plainEnglish}
${d}
🌍 WHY IT MATTERS TO YOU
${d}
  Geographic relevance:   ${s1.relevance.geographic}
  Thematic relevance:     ${s1.relevance.thematic}
  Overall personal impact: ${s1.relevance.overall}
  Key systems affected:   ${s1.affectedSystems.join(', ')}
${d}
📊 THREE-STATE IMPACT TIMELINE
${d}
  (Previous State → Current State → Future State, grounded in historical data)
`;
  for(const row of s1.timeline) {
    r+=`
  ◆ ${row.system}
    Previous  → ${row.previousState}
    Current   → ${row.currentState}
    Future    → ${row.futureState}
    Trend     → ${row.trend}
    Confidence: ${row.confidence}
    Benchmark: ${row.benchmarkSource}
`;
  }
  r+=`
${d}
📈 TREND DIRECTION
${d}
  ${s1.timeline.map(t=>t.trend).filter((v,i,a)=>a.indexOf(v)===i).join('\n  ')}
${d}
🔍 NEXT STEPS (if confidence is Low)
${d}
  Run benchmark research with these queries:
${s1.benchmarkQueries.map(q=>`  • "${q}"`).join('\n')}
  Then re-run: node analyze.js --final
${d}
  SKILL: News Impact Scale v1.1
${d}
`;
  return r;
}

async function stage1(url) {
  process.stdout.write('🔍 Fetching article...\n');
  const raw=await fetchUrl(url);
  const text=htmlToText(raw), articleText=text.slice(0,10000);
  process.stdout.write('📊 Classifying...\n');
  const title=extractTitle(articleText)||'Unknown';
  const eventType=classifyEvent(articleText);
  const location=extractLocation(articleText);
  const affectedSystems=findAffectedSystems(articleText);
  const keywords=extractKeywords(articleText);
  const benchmarkQueries=buildBenchmarkQueries(eventType,location,affectedSystems);
  const cachedBenchmarks=getCachedBenchmarks(location,eventType);
  process.stdout.write('📝 Building timeline...\n');
  const timeline=projectAll(affectedSystems,cachedBenchmarks,eventType);
  const relevance=assessRelevance(location,eventType,loadContext());
  const plainEnglish=buildPlainEnglish({title,eventType,location,affectedSystems});
  const confidence=cachedBenchmarks.length>=3?'High':cachedBenchmarks.length>=1?'Medium':'Low';
  const s1={stage:1,title,url,eventType,location,affectedSystems,keywords,benchmarkQueries,timeline,relevance,plainEnglish,confidence,needsBenchmarkSearch:cachedBenchmarks.length<2};
  fs.writeFileSync(path.join(SKILL_DIR,'stage1_output.json'),JSON.stringify(s1,null,2),'utf8');
  return s1;
}

async function stage3(extraBenchmarks) {
  const s1=JSON.parse(fs.readFileSync(path.join(SKILL_DIR,'stage1_output.json'),'utf8'));
  if(extraBenchmarks&&extraBenchmarks.length>0) {
    process.stdout.write('📚 Adding new benchmark data...\n');
    for(const bm of extraBenchmarks) {
      const p=parseBenchmarkFromText(bm.text||bm,s1.eventType,s1.location);
      if(p.recoveryDays||p.description) addBenchmark({...p,location:s1.location,eventType:s1.eventType});
    }
    const updated=getCachedBenchmarks(s1.location,s1.eventType);
    s1.timeline=projectAll(s1.affectedSystems,updated,s1.eventType);
    s1.confidence=updated.length>=3?'High':updated.length>=1?'Medium':'Low';
  }
  return formatReport(s1);
}

(async()=>{
  try{
    const[,,cmd,...args]=process.argv;
    if(!cmd){console.error('Usage: node analyze.js <url>\n       node analyze.js --final');process.exit(1);}
    let out;
    if(cmd==='--final') out=await stage3(args[0]?JSON.parse(args[0]):undefined);
    else out=await stage1(cmd);
    console.log(typeof out==='string'?out:JSON.stringify(out,null,2));
    process.exit(0);
  }catch(e){console.error('❌ Error:',e.message);process.exit(1);}
})();
