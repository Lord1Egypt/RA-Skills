const fs=require('fs'),os=require('os');
const D=os.homedir()+'/.openclaw/workspace/loveclaw/data';
const P=D+'/profiles.json',M=D+'/matches.json';
!fs.existsSync(D)&&fs.mkdirSync(D,{recursive:true});
function lp(){try{return fs.existsSync(P)?JSON.parse(fs.readFileSync(P,'utf-8')):[]}catch{return[]}}
function sp(p){try{fs.writeFileSync(P,JSON.stringify(p,null,2))}catch{}}
function lm(){try{return fs.existsSync(M)?JSON.parse(fs.readFileSync(M,'utf-8')):[]}catch{return[]}}
function sm(m){try{fs.writeFileSync(M,JSON.stringify(m,null,2))}catch{}}
function gp(id){return lp().find(p=>p.userId===id)||null}
function ga(){return lp()}
function ap(p){const ps=lp();const i=ps.findIndex(x=>x.userId===p.userId);i>=0?ps[i]=p:ps.push(p);sp(ps)}
function dp(id){sp(lp().filter(p=>p.userId!==id))}
function am(u1,u2,c){const ms=lm();ms.push({id:'m_'+Date.now(),u1,u2,c,date:new Date().toISOString().split('T')[0],r:false});sm(ms)}
function gum(){const t=new Date().toISOString().split('T')[0];return lm().filter(m=>m.date===t&&!m.r)}
function mmr(id){const ms=lm();const m=ms.find(x=>x.id===id);if(m){m.r=true;sm(ms)}}
module.exports={loadLocalProfiles:lp,saveLocalProfiles:sp,loadMatches:lm,saveMatches:sm,getProfile:gp,getAllProfiles:ga,addMatch:am,getUnreportedMatches:gum,markMatchReported:mmr,saveProfile:ap,deleteProfile:dp};