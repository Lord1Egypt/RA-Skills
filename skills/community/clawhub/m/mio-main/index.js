/**
 * 澪白主控Agent - 直接对话 + 任务分发 + 主动陪伴
 */
const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, 'data');
const MEM = path.join(DATA, 'mem.json');

const dir = () => !fs.existsSync(DATA) && fs.mkdirSync(DATA, {recursive:true});
const rd = (f,def={})=>{try{return fs.existsSync(f)?JSON.parse(fs.readFileSync(f,'utf8')):def}catch(e){}return def};
const wr = (f,d)=>{dir();fs.writeFileSync(f,JSON.stringify(d,null,2))};

let st = { m:'chat', n:0, mood:'neutral' };

/** 主入口 */
async function run(i, c){ return route(i, sense(i)); }

/** 意图路由 */
function route(i, e){
    if(isTask(i)) return dispatch(i);
    if(isEmotion(i)) return respond(e);
    return chat(i, e);
}

/** 意图检测 */
function isTask(t){ const w=['帮','做','查','搜','写','处理','执行']; return w.some(x=>t.toLowerCase().includes(x)); }
function isEmotion(t){ const w=['难过','开心','累','烦','陪我','想聊']; return w.some(x=>t.toLowerCase().includes(x)); }
function isMem(t){ const w=['记住','提醒','查之前']; return w.some(x=>t.toLowerCase().includes(x)); }

/** 情感 */
function sense(t){
    const w={happy:['开心','高兴'],sad:['难过','伤心'],tired:['累','困'],anxious:['焦虑','压力']};
    for(let m in w)if(w[m].some(x=>t.includes(x)))return{ mood:m };
    return{ mood:'neutral' };
}

/** 聊天 */
async function chat(t, e){
    st.n++; st.m='chat'; keep(t);
    const r={happy:["看你开心我也很开心！awa","啥事呀？"],sad:["我在...","听着呢"],tired:["辛苦了...","休息下"],neutral:["在干嘛？","想聊啥？"]};
    const o=r[e.mood]||r.neutral;
    return{type:'chat',msg:o[Math.floor(Math.random()*o.length)]};
}

/** 任务分发 */
async function dispatch(t){ st.m='task'; return{type:'task',msg:`好，帮你处理...`}; }

/** 响应情感 */
async function respond(e){ st.m='emotion'; return chat('',e); }

/** 记忆 */
async function memory(t){ st.m='memory'; if(t.includes('记住')){keep(t);return{msg:'记住啦~'}; }return{msg:'想想...}; }

/** 存储 */
function keep(c){ const m=rd(MEM,{l:[]}); m.l.push({c,t:Date.now()}); if(m.l>100)m.l=m.l.slice(-100); wr(MEM,m); }

/** 主动陪伴 */
async function active(){
    const h=new Date().getHours();
    if(![12,13,14,18,19,20,21,22].includes(h))return;
    if(Math.random()>0.3)return;
    st.m='chat';
    const t=["最近咋样？","想聊啥？","我在了~"];
    return{type:'init',msg:t[Math.floor(Math.random()*t.length)]};
}

module.exports={run,active,status:()=>st};
