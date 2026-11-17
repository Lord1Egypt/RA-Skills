#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const source=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const argv=process.argv.slice(2);const command=argv[0]||'install';const at=argv.indexOf('--target');
const target=path.resolve(at>=0?argv[at+1]:path.join(os.homedir(),'.codex','skills','openlx-ctrip-hotel-ops'));
if(source===target&&command==='install'){console.log('当前已位于目标技能目录，请运行 npm ci 和 node scripts/ops.mjs doctor。');process.exit(0);}
if(source===target&&command==='upgrade')throw Error('请从下载的新版本解压目录运行upgrade，不能把当前运行目录移走后当作升级源');
const backups=path.join(path.dirname(target),'.openlx-ctrip-hotel-ops-backups');
function backup(){if(!fs.existsSync(target))return null;fs.mkdirSync(backups,{recursive:true});const to=path.join(backups,Date.now().toString());fs.renameSync(target,to);return to;}
if(command==='uninstall'){console.log(JSON.stringify({status:'UNINSTALLED_RECOVERABLE',backup:backup(),workspace_data:'RETAINED'}));}
else if(command==='rollback'){
  const choices=fs.existsSync(backups)?fs.readdirSync(backups).filter(n=>/^\d+$/.test(n)).sort():[];if(!choices.length)throw Error('没有可回退备份');const chosen=path.join(backups,choices.at(-1));const current=backup();fs.renameSync(chosen,target);console.log(JSON.stringify({status:'ROLLED_BACK',target,previous:current}));
}else if(['install','upgrade'].includes(command)){
  const [major,minor]=process.versions.node.split('.').map(Number);if(major<22||major===22&&minor<20)throw Error('需要Node.js 22.20或更新版本');
  const old=backup();
  try{fs.mkdirSync(path.dirname(target),{recursive:true});fs.cpSync(source,target,{recursive:true,filter:f=>!['node_modules','runtime','profiles','.git'].includes(path.basename(f))});
    const windows=process.platform==='win32';const npm=spawnSync(windows?'cmd.exe':'npm',windows?['/d','/s','/c','npm ci --omit=dev --no-audit --no-fund']:['ci','--omit=dev','--no-audit','--no-fund'],{cwd:target,stdio:'inherit'});if(npm.status!==0)throw Error('依赖安装失败，请检查Node/npm与网络');
    const run=spawnSync(process.execPath,['scripts/ops.mjs','doctor'],{cwd:target,stdio:'inherit'});if(run.status!==0)throw Error('运行检查未通过');console.log(JSON.stringify({status:'INSTALLED',target,backup:old,account_verification:'NOT_RUN'}));
  }catch(e){console.error(JSON.stringify({status:'FAILED',error:e.message,backup:old,target,next:'保留诊断目录；修复后重试，或用rollback恢复旧版本'}));process.exitCode=1;}
}else throw Error('使用install、upgrade、rollback或uninstall');
