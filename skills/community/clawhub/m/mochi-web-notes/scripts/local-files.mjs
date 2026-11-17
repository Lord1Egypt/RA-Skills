import fs from 'node:fs/promises';
import path from 'node:path';
import {constants} from 'node:fs';
export async function noLinks(target){let p=path.resolve(target);for(;;){try{if((await fs.lstat(p)).isSymbolicLink())throw Error('Symlink/junction paths are not supported');}catch(e){if(e.code!=='ENOENT')throw e;}const parent=path.dirname(p);if(parent===p)break;p=parent;}}
export async function workspaceFolder(workspace,leaf){const root=path.resolve(workspace);await noLinks(root);if(!(await fs.stat(root)).isDirectory())throw Error('Workspace must be an existing directory');const folder=path.join(root,leaf);await noLinks(folder);await fs.mkdir(folder,{recursive:true});await noLinks(folder);return folder;}
export async function readLocal(workspace,file,max=131072){
 const root=path.resolve(workspace),target=path.resolve(file);if(target===root||!target.startsWith(root+path.sep))throw Error('Input must be inside this workspace');
 await noLinks(target);const handle=await fs.open(target,constants.O_RDONLY|(constants.O_NOFOLLOW||0));
 try{
  const before=await handle.stat();if(!before.isFile()||before.size>max)throw Error('Input is not a bounded regular file');
  await noLinks(target);const named=await fs.lstat(target);if(named.dev!==before.dev||named.ino!==before.ino||named.isSymbolicLink())throw Error('Input changed while opening');
  const buffer=Buffer.alloc(max+1);let used=0;while(used<buffer.length){const {bytesRead}=await handle.read(buffer,used,buffer.length-used,used);if(!bytesRead)break;used+=bytesRead;}
  const after=await handle.stat();await noLinks(target);const current=await fs.lstat(target);
  if(used>max||after.size>max||after.size!==before.size||after.mtimeMs!==before.mtimeMs||current.dev!==before.dev||current.ino!==before.ino||current.isSymbolicLink())throw Error('Input grew or changed while reading');
  return new TextDecoder('utf-8',{fatal:true}).decode(buffer.subarray(0,used)).replace(/^\ufeff/,'');
 }finally{await handle.close();}
}
export async function writeNew(file,text){await noLinks(file);const handle=await fs.open(file,constants.O_WRONLY|constants.O_CREAT|constants.O_EXCL|(constants.O_NOFOLLOW||0),0o600);try{await handle.writeFile(text,'utf8');}finally{await handle.close();}}
export function options(args,allowed){const out={};for(let i=0;i<args.length;i+=2){const key=args[i],value=args[i+1];if(!allowed.includes(key)||!value||Object.hasOwn(out,key))throw Error('Unknown, missing or duplicate option');out[key]=value;}return out;}
export function md(value){return String(value).replace(/[\\`*_[\]<>|]/g,'\\$&').replace(/[\r\n]/g,' ');}
export function language(value='en'){if(!['en','zh-CN'].includes(value))throw Error('Language must be en or zh-CN');return value;}
