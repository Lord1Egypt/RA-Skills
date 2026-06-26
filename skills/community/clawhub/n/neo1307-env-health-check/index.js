const fs=require('fs'); const path=require('path');
function args(name){const out=[]; for(let i=0;i<process.argv.length;i++) if(process.argv[i]===name && process.argv[i+1]) out.push(process.argv[i+1]); return out;}
const envs=args('--env'); const dirs=args('--dir'); const out=process.argv.includes('--out')?process.argv[process.argv.indexOf('--out')+1]:path.join(process.cwd(),'out','env_health_report.md');
const findings=[];
for(const name of envs){findings.push({type:'env',name,status:process.env[name]?'OK':'WARN'});}
for(const d of dirs){const abs=path.resolve(d); const exists=fs.existsSync(abs); let writable=false; if(exists){ try{ const test=path.join(abs,'.env-health-check.tmp'); fs.writeFileSync(test,'ok','utf8'); fs.unlinkSync(test); writable=true; }catch{} }
findings.push({type:'dir',path:abs,status:!exists?'FAIL':(writable?'OK':'WARN')}); }
const summary=findings.reduce((m,f)=>(m[f.status]=(m[f.status]||0)+1,m),{});
const lines=['# Environment Health Report','',`- OK: ${summary.OK||0}`,`- WARN: ${summary.WARN||0}`,`- FAIL: ${summary.FAIL||0}`,'','## Findings'];
for(const f of findings){ if(f.type==='env') lines.push(`- [${f.status}] env ${f.name}`); else lines.push(`- [${f.status}] dir ${f.path}`); }
fs.mkdirSync(path.dirname(out),{recursive:true}); fs.writeFileSync(path.resolve(out),lines.join('\n'),'utf8');
console.log(JSON.stringify({ok:true,out:path.resolve(out),summary,findings},null,2));
