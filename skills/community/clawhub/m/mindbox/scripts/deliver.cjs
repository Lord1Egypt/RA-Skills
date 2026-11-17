'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');

// Stage beside the destination, then replace. Roll back a failed second rename.
// This protects against handled I/O failures, not power loss or concurrent writers.
function deliver(entries,{force=false,io=fs}={}) {
  const stamp=crypto.randomUUID(),staged=[],backups=[],committed=[];
  try {
    for(const [file,content] of entries) {
      if(io.existsSync(file)) {
        if(!force) throw new Error('文件已存在：'+file+'。确认需要更新时使用 --force。');
        if(!io.lstatSync(file).isFile()) throw new Error('目标不是普通文件：'+file);
      }
      const candidate=path.join(path.dirname(file),'.'+path.basename(file)+'.'+stamp+'.tmp');
      staged.push([candidate,file]);io.writeFileSync(candidate,content,{flag:'wx'});
      if(!Buffer.from(io.readFileSync(candidate)).equals(Buffer.from(content)))throw new Error('暂存文件回读不一致：'+file);
    }
    for(const [,file] of staged) if(io.existsSync(file)) {
      const backup=file+'.'+stamp+'.bak';io.renameSync(file,backup);backups.push([backup,file]);
    }
    for(const [candidate,file] of staged) {io.renameSync(candidate,file);committed.push(file);}
    for(const [file,content] of entries)if(!Buffer.from(io.readFileSync(file)).equals(Buffer.from(content)))throw new Error('交付文件回读不一致：'+file);
  } catch(error) {
    for(const file of committed) io.rmSync(file,{force:true});
    for(const [backup,file] of backups.reverse()) io.renameSync(backup,file);
    throw error;
  } finally {
    for(const [candidate] of staged) io.rmSync(candidate,{force:true});
  }
  for(const [backup] of backups) io.rmSync(backup,{force:true});
}
module.exports={deliver};
