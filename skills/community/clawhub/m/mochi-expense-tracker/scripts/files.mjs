import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {assert,text,safePath} from './store.mjs';
export const digest=value=>createHash('sha256').update(value).digest('hex');
export function readText(c,file,max=2*1024*1024){const p=safePath(c.workspace,text(file,'file',1000),true);assert(fs.statSync(p).isFile()&&fs.statSync(p).size<=max,'File is missing, not regular, or too large');const value=new TextDecoder('utf-8',{fatal:true}).decode(fs.readFileSync(p)).replace(/^\uFEFF/,'');assert(!value.includes('\0'),'Binary content is not supported');return value;}
export const money=n=>(n/100).toFixed(2);
export const md=value=>String(value??'').replace(/\r?\n/g,' / ').replace(/[\\`*_{}\[\]<>#|]/g,'\\$&');
export function csv(rows){return '\uFEFF'+rows.map(row=>row.map(value=>{let s=String(value??'');if(typeof value==='string'&&/^[\s]*[=+@-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}).join(',')).join('\r\n')+'\r\n';}
export function parseCsv(value){
 const rows=[];let row=[],cell='',quoted=false,closed=false;
 for(let n=0;n<value.length;n++){const ch=value[n];if(quoted){if(ch==='"'){if(value[n+1]==='"'){cell+='"';n++;}else{quoted=false;closed=true;}}else cell+=ch;}
 else if(ch==='"'){assert(!cell&&!closed,'Unexpected CSV quote');quoted=true;}
 else if(ch===','){row.push(cell);cell='';closed=false;}
 else if(ch==='\r'||ch==='\n'){if(ch==='\r'&&value[n+1]==='\n')n++;row.push(cell);if(row.some(x=>x!==''))rows.push(row);row=[];cell='';closed=false;}
 else{assert(!closed,'Characters after a closing CSV quote');cell+=ch;}
 assert(cell.length<=20000&&row.length<=100&&rows.length<=5000,'CSV exceeds row, column or field limit');}
 assert(!quoted,'Unclosed CSV quote');if(cell||row.length){row.push(cell);if(row.some(x=>x!==''))rows.push(row);}assert(rows.length>1&&rows.length<=5001,'Provide a header and 1..5000 data rows');
 const header=rows.shift().map(x=>x.trim().replace(/^\uFEFF/,''));assert(header.every(Boolean)&&new Set(header).size===header.length,'CSV headers must be nonempty and unique');
 return rows.map((r,n)=>{assert(r.length===header.length,'CSV column count mismatch at row '+(n+2));return Object.fromEntries(header.map((h,k)=>[h,r[k]]));});
}
export function exportFiles(slug,files,result={}){return {changed:true,artifacts:files,result:{...result,exportKind:slug}};}
