#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {openWorkspace,now,writeJson} from './core.mjs';
import {runOnce} from './scheduler.mjs';
const index=process.argv.indexOf('--workspace');if(index<0||!process.argv[index+1])throw Error('缺少--workspace');
const w=openWorkspace(process.argv[index+1]),lock=path.join(w.base,'daemon.pid');
if(fs.existsSync(lock)){const pid=Number(fs.readFileSync(lock));let active=false;try{process.kill(pid,0);active=true;}catch{}if(active)throw Error('DAEMON_ALREADY_RUNNING');fs.unlinkSync(lock);}
fs.writeFileSync(lock,String(process.pid),{flag:'wx',mode:0o600});let stopping=false;
process.on('SIGTERM',()=>{stopping=true;});process.on('SIGINT',()=>{stopping=true;});
try{do{try{const result=await runOnce(w);writeJson(path.join(w.base,'daemon-status.json'),{pid:process.pid,heartbeat_at:now(),result});}catch(e){writeJson(path.join(w.base,'daemon-status.json'),{pid:process.pid,heartbeat_at:now(),error:e.message});}
  if(process.argv.includes('--once'))break;
  for(let i=0;i<30&&!stopping;i++)await new Promise(r=>setTimeout(r,1000));
}while(!stopping);}finally{if(fs.existsSync(lock)&&Number(fs.readFileSync(lock))===process.pid)fs.unlinkSync(lock);w.close();}
