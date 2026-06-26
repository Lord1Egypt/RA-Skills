const fs = require('fs');
const path = require('path');
function arg(name){const i=process.argv.indexOf(name);return i>=0?process.argv[i+1]:null;}
const input=arg('--input');
const out=arg('--out') || path.join(process.cwd(),'out','log_analysis_report.md');
if(!input){console.error('Usage: node index.js --input <logfile> [--out <report.md>]');process.exit(1);}
const lines=fs.readFileSync(path.resolve(input),'utf8').replace(/^\uFEFF/,'').split(/\r?\n/);
const sev=['CRITICAL','ERROR','WARN'];
const matches=[];
for(const line of lines){const s=sev.find(x=>line.includes(x)); if(s) matches.push({severity:s,line});}
const normalize=s=>s.replace(/\d+/g,'<num>').replace(/[a-f0-9]{8,}/gi,'<id>').replace(/\s+/g,' ').trim();
const groups=new Map();
for(const m of matches){const key=`${m.severity}|${normalize(m.line)}`; if(!groups.has(key)) groups.set(key,{severity:m.severity,count:0,sample:m.line}); groups.get(key).count++;}
const ordered=[...groups.values()].sort((a,b)=>b.count-a.count);
const counts=matches.reduce((m,x)=>(m[x.severity]=(m[x.severity]||0)+1,m),{});
const report=[];
report.push('# Log Analysis Report','',`- Total scanned lines: ${lines.length}`,`- WARN: ${counts.WARN||0}`,`- ERROR: ${counts.ERROR||0}`,`- CRITICAL: ${counts.CRITICAL||0}`,'','## Grouped findings');
if(!ordered.length) report.push('- No WARN/ERROR/CRITICAL lines found.');
else ordered.slice(0,50).forEach((g,i)=>report.push(`- ${i+1}. [${g.severity}] x${g.count} — ${g.sample}`));
report.push('','## Suggested first checks','- Start from CRITICAL groups, then highest-frequency ERROR groups.','- Verify whether repeated warnings are expected noise or precursors to failure.');
fs.mkdirSync(path.dirname(out),{recursive:true}); fs.writeFileSync(path.resolve(out),report.join('\n'),'utf8');
console.log(JSON.stringify({ok:true,out:path.resolve(out),groups:ordered.length,counts},null,2));
