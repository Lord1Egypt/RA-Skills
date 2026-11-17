#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const stable=/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;
function hash(value){return crypto.createHash('sha256').update(value).digest('hex');}
function packageFiles(directory){
 const files={};
 function walk(folder){for(const item of fs.readdirSync(folder,{withFileTypes:true}).sort((a,b)=>a.name<b.name?-1:a.name>b.name?1:0)){
  const file=path.join(folder,item.name),rel=path.relative(directory,file).split(path.sep).join('/');
  if(['package-manifest.json','installation.json'].includes(rel))continue;
  if(item.isDirectory())walk(file);else if(item.isFile())files[rel]=hash(fs.readFileSync(file));else throw new Error('Unexpected package link: '+rel);
 }}walk(directory);return files;
}
function checkFiles(directory,files){
 for(const [name,digest] of Object.entries(files)){
  const file=path.resolve(directory,name);if(!file.startsWith(path.resolve(directory)+path.sep))throw new Error('Invalid package path: '+name);
  if(hash(fs.readFileSync(file))!==digest)throw new Error('Package integrity failed: '+name);
 }
}
function inspect(directory){
 const identity=JSON.parse(fs.readFileSync(path.join(directory,'version.json'),'utf8'));
 if(!stable.test(identity.version))throw new Error('Invalid Skill version');
 if(identity.releaseTag&&identity.releaseTag!=='v'+identity.version)throw new Error('Skill release tag mismatch');
 if(identity.license&&identity.license!=='MIT')throw new Error('Skill license mismatch');
 const runtime=path.join(directory,'assets/runtime'),renderer=JSON.parse(fs.readFileSync(path.join(runtime,'manifest.json'),'utf8'));
 if(renderer.version!==identity.version)throw new Error('Skill/runtime version mismatch');
 if(hash(JSON.stringify(renderer.files))!==renderer.renderer)throw new Error('Runtime manifest fingerprint mismatch');
 const manifestPath=path.join(directory,'package-manifest.json');let digest=renderer.renderer,integrity='legacy-runtime-only';
 if(fs.existsSync(manifestPath)){
  const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
  if(manifest.format!==1||manifest.version!==identity.version||!manifest.files||!Object.keys(manifest.files).length||hash(JSON.stringify(manifest.files))!==manifest.digest)throw new Error('Package manifest mismatch');
  checkFiles(directory,manifest.files);
  for(const [name,digest] of Object.entries(packageFiles(directory)))if(manifest.files[name]!==digest)throw new Error('Untracked package content: '+name);
  digest=manifest.digest;integrity='verified';
 }else checkFiles(runtime,renderer.files);
 let installation=null;const receipt=path.join(directory,'installation.json');if(fs.existsSync(receipt))installation=JSON.parse(fs.readFileSync(receipt,'utf8'));
 return {version:identity.version,license:identity.license||'MIT',renderer:renderer.renderer,package:digest,integrity,installation};
}
async function checkLatest(directory,fetcher=fetch){
 const installed=inspect(directory);
 try{
  const response=await fetcher('https://api.github.com/repos/MarkingYang/mindbox/releases/latest',{headers:{Accept:'application/vnd.github+json','User-Agent':'mindbox-version-check'},signal:AbortSignal.timeout(5000)});
  if(response.status===404)return {installed:installed.version,status:'unpublished',message:'No published stable GitHub release was found.'};
  if(!response.ok)throw new Error('GitHub HTTP '+response.status);
  const release=await response.json(),version=String(release.tag_name||'').replace(/^v/,'');
  if(!stable.test(version)||release.draft||release.prerelease)throw new Error('Invalid stable release metadata');
  const a=version.split('.').map(Number),b=installed.version.split('.').map(Number);let order=0;for(let i=0;i<3&&!order;i++)order=Math.sign(a[i]-b[i]);
  return {installed:installed.version,latest:version,status:order>0?'update-available':order<0?'ahead':'current',release:'https://github.com/MarkingYang/mindbox/releases/tag/v'+version};
 }catch(error){return {installed:installed.version,status:'unavailable',message:error.message};}
}
module.exports={inspect,checkLatest,packageFiles,hash,stable};
if(require.main===module)(async()=>{
 const directory=path.resolve(__dirname,'..'),args=process.argv.slice(2);
 if(args.length!==1||!['--version','--status','--check'].includes(args[0]))throw new Error('Use --version, --status or --check. Updates: npx skills update mindbox -g');
 if(args[0]==='--version')console.log(JSON.parse(fs.readFileSync(path.join(directory,'version.json'),'utf8')).version);
 else console.log(JSON.stringify(args[0]==='--check'?await checkLatest(directory):inspect(directory),null,2));
})().catch(error=>{console.error(error.message);process.exitCode=1;});
