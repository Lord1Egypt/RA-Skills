#!/usr/bin/env node
// Node built-ins only. This same file also provides the public first-install entrypoint.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {createHash, randomBytes} from 'node:crypto';
import {inflateRawSync} from 'node:zlib';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {createInterface} from 'node:readline';

const DEFAULT_SITE = 'https://mochilab.bz';
const MAX_ZIP = 25 * 1024 * 1024, MAX_EXPANDED = 100 * 1024 * 1024;
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const ID = /^[a-f0-9]{32}$/, HASH = /^[a-f0-9]{64}$/;
const KEY = /^mls_[A-Za-z0-9_-]{32,150}$/;
const RECEIPT = '.mochilab-install.json';
export const digest = bytes => createHash('sha256').update(bytes).digest('hex');
export class ClientError extends Error {
  constructor(code, message) { super(message); this.code = code; }
}
const fail = (code, message) => { throw new ClientError(code, message); };
const exists = async p => { try { return await fs.lstat(p); } catch (e) { if (e.code === 'ENOENT') return null; throw e; } };
export function siteUrl(value = DEFAULT_SITE) {
  let url; try { url = new URL(value); } catch { fail('site_invalid', 'Use https://mochilab.bz.'); }
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname);
  if (url.username || url.password || url.search || url.hash ||
      (!local && url.origin !== DEFAULT_SITE) || (local && !['http:', 'https:'].includes(url.protocol)))
    fail('site_invalid', 'Use the official MochiLab site or a loopback test fixture.');
  return url.href.replace(/\/$/, '');
}
async function safeDirectory(directory, create = false) {
  const target = path.resolve(directory), parsed = path.parse(target);
  let current = parsed.root;
  for (const part of target.slice(parsed.root.length).split(path.sep).filter(Boolean)) {
    current = path.join(current, part);
    let stat = await exists(current);
    if (!stat && create) { try { await fs.mkdir(current, {mode: 0o700}); } catch (e) { if (e.code !== 'EEXIST') throw e; } stat = await fs.lstat(current); }
    if (!stat || !stat.isDirectory() || stat.isSymbolicLink()) fail('directory_invalid', 'Use an existing directory without symbolic links or junctions.');
  }
  return target;
}
async function privateFile(file) {
  if (process.platform === 'win32') {
    const system = path.join(process.env.SystemRoot || 'C:\\Windows', 'System32');
    const who = execFileSync(path.join(system, 'whoami.exe'), ['/user', '/fo', 'csv', '/nh'], {encoding:'utf8', windowsHide:true});
    const sid = who.match(/S-1-[0-9-]+/g)?.at(-1);
    if (!sid) fail('credential_permissions', 'Could not protect the credential file.');
    execFileSync(path.join(system, 'icacls.exe'), [file, '/inheritance:r', '/grant:r', `*${sid}:(F)`], {stdio:'pipe', windowsHide:true});
  } else await fs.chmod(file, 0o600);
}
function credentialPath(env) { return path.join(path.resolve(env.MOCHILAB_CONFIG_DIR || path.join(os.homedir(), '.mochilab')), 'credentials.json'); }
async function loadKey(site, env) {
  if (env.MOCHILAB_SKILLS_KEY) {
    if (!KEY.test(env.MOCHILAB_SKILLS_KEY)) fail('key_invalid', 'Use a Skills access key beginning with mls_.');
    return env.MOCHILAB_SKILLS_KEY;
  }
  const file = credentialPath(env);
  if (!await exists(path.dirname(file))) fail('connect_required', 'Connect your account with the login command first.');
  await safeDirectory(path.dirname(file));
  const stat = await exists(file);
  if (!stat || !stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1 || stat.size > 4096)
    fail('connect_required', 'Connect your account with the login command first.');
  if (process.platform !== 'win32' && ((stat.mode & 0o077) !== 0 || stat.uid !== process.getuid()))
    fail('credential_permissions', 'The credential file must be private to your account (mode 600).');
  let value; try { value = JSON.parse(await fs.readFile(file, 'utf8')); } catch { fail('key_invalid', 'Connect your account again with login.'); }
  if (value.site !== site || !KEY.test(value.key || '')) fail('connect_required', 'Connect this site with the login command first.');
  return value.key;
}
async function saveKey(site, key, env) {
  const file = credentialPath(env), parent = await safeDirectory(path.dirname(file), true);
  const old = await exists(file);
  if (old && (!old.isFile() || old.isSymbolicLink() || old.nlink !== 1)) fail('credential_path', 'The credential path is not a regular private file.');
  const temporary = path.join(parent, '.credentials-' + randomBytes(12).toString('hex'));
  try {
    await fs.writeFile(temporary, JSON.stringify({site,key})+'\n', {flag:'wx', mode:0o600});
    await privateFile(temporary);
    await fs.rename(temporary, file);
  } finally { if (await exists(temporary)) await fs.unlink(temporary); }
}
function apiMessage(code) {
  return ({sign_in_required:'Your key is invalid, expired or revoked. Connect again.', skills_key_required:'Use a Skills access key, not a publishing key.',
    membership_required:'This Skill requires an active membership. See the membership page.', entitlement_required:'Claim this free Skill before downloading.',
    skill_not_found:'This Skill is not available.', package_not_found:'This version is unavailable. Refresh the Skill details.',
    skill_not_available:'This Skill is not available.', database_not_ready:'The site is not ready.', unknown_action:'Upgrade the website to the version supporting Skills access.',
    csrf_invalid:'The website did not accept this access key.'})[code] || 'The site could not complete this request.';
}
export class Client {
  constructor(site, key = '') { this.site = siteUrl(site); this.key = key; }
  async request(relative, {body, auth=false, binary=false} = {}) {
    const url = new URL(relative, this.site + '/');
    if (url.origin !== new URL(this.site).origin || !url.pathname.startsWith(new URL(this.site+'/').pathname)) fail('url_invalid', 'A download must stay on the configured MochiLab site.');
    if (auth && !KEY.test(this.key)) fail('connect_required', 'Connect your account with login first.');
    const headers = {Accept: binary ? 'application/zip, application/x-zip-compressed' : 'application/json'};
    if (auth) headers.Authorization = 'Bearer ' + this.key;
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    let response;
    try { response = await fetch(url, {method:body === undefined ? 'GET' : 'POST', headers, body:body === undefined ? undefined : JSON.stringify(body), redirect:'manual', signal:AbortSignal.timeout(60000)}); }
    catch { fail('network_error', 'Could not reach MochiLab. Try again when the connection is available.'); }
    if (response.status >= 300 && response.status < 400) { await response.body?.cancel(); fail('redirect_refused', 'The site returned a redirect; no credentials were forwarded.'); }
    const limit = binary && response.ok ? MAX_ZIP : 2*1024*1024;
    if (Number(response.headers.get('content-length')) > limit) { await response.body?.cancel(); fail('response_too_large', 'The response exceeds its size limit.'); }
    const chunks=[]; let length=0;
    if (response.body) for await (const chunk of response.body) { length+=chunk.length; if(length>limit) { fail('response_too_large','The response exceeds its size limit.'); } chunks.push(chunk); }
    const bytes=Buffer.concat(chunks);
    if (binary && response.ok) {
      if (!['application/zip','application/x-zip-compressed'].includes((response.headers.get('content-type') || '').toLowerCase().split(';')[0].trim())) fail('download_invalid', 'Expected a ZIP package.');
      return bytes;
    }
    let value; try { value=JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/,'')); } catch { fail('response_invalid','The site returned an invalid response.'); }
    if (!response.ok || value.ok === false) { const code=typeof value.error?.code === 'string' ? value.error.code : 'request_failed'; fail(code,apiMessage(code)); }
    return value.ok === true ? value.data : value;
  }
  api(action, body, auth=false) { return this.request('Api/Api.ashx?action='+encodeURIComponent(action),{body,auth}); }
}
const CRC_TABLE = Array.from({length:256}, (_,n) => { let c=n; for(let j=0;j<8;j++) c=c&1 ? 0xedb88320^(c>>>1) : c>>>1; return c>>>0; });
export function crc32(bytes) { let c=0xffffffff; for(const b of bytes) c=CRC_TABLE[(c^b)&255]^(c>>>8); return (c^0xffffffff)>>>0; }
function validPart(part) {
  return part && part!=='.' && part!=='..' && !/[\x00-\x1f\x7f<>:"\\|?*]/.test(part) && !/[. ]$/.test(part) && !/^(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\.|$)/i.test(part);
}
export function unpack(bytes, slug) {
  if(!SLUG.test(slug) || bytes.length<22 || bytes.length>MAX_ZIP) fail('zip_invalid','Invalid Skill package.');
  const invalid=()=>fail('zip_invalid','The ZIP package failed validation.');
  let end=-1;
  for(let i=bytes.length-22;i>=Math.max(0,bytes.length-65557);i--) if(bytes.readUInt32LE(i)===0x06054b50 && i+22+bytes.readUInt16LE(i+20)===bytes.length){end=i;break;}
  if(end<0 || bytes.readUInt16LE(end+4)!==0 || bytes.readUInt16LE(end+6)!==0) invalid();
  const count=bytes.readUInt16LE(end+10), size=bytes.readUInt32LE(end+12), offset=bytes.readUInt32LE(end+16);
  if(!count || count>500 || bytes.readUInt16LE(end+8)!==count || offset+size!==end) invalid();
  const entries=[], names=new Set(), regions=[]; let cursor=offset, expanded=0;
  for(let i=0;i<count;i++) {
    if(cursor+46>end || bytes.readUInt32LE(cursor)!==0x02014b50) invalid();
    const flags=bytes.readUInt16LE(cursor+8), method=bytes.readUInt16LE(cursor+10), crc=bytes.readUInt32LE(cursor+16), compressed=bytes.readUInt32LE(cursor+20), length=bytes.readUInt32LE(cursor+24);
    const n=bytes.readUInt16LE(cursor+28), extra=bytes.readUInt16LE(cursor+30), comment=bytes.readUInt16LE(cursor+32), attrs=bytes.readUInt32LE(cursor+38), local=bytes.readUInt32LE(cursor+42), type=(attrs>>>16)&0xf000;
    if((flags&~0x080e)!==0 || (flags&1)!==0 || ![0,8].includes(method) || !n || cursor+46+n+extra+comment>end || bytes.readUInt16LE(cursor+34)!==0 || ![0,0x8000,0x4000].includes(type) || (attrs&0x400)!==0 || [compressed,length,local].includes(0xffffffff)) invalid();
    const nameBytes=bytes.subarray(cursor+46,cursor+46+n);
    let name; try { name=new TextDecoder('utf-8',{fatal:true}).decode(nameBytes); } catch { invalid(); }
    const directory=name.endsWith('/'), parts=(directory?name.slice(0,-1):name).split('/');
    if(name.length>240 || !parts.every(validPart) || (type===0x4000 || (attrs&0x10)!==0) && !directory || names.has(name.toLowerCase())) invalid();
    names.add(name.toLowerCase());
    if(local+30>offset || bytes.readUInt32LE(local)!==0x04034b50 || bytes.readUInt16LE(local+6)!==flags || bytes.readUInt16LE(local+8)!==method || bytes.readUInt16LE(local+26)!==n) invalid();
    const start=local+30+n+bytes.readUInt16LE(local+28), finish=start+compressed;
    if(finish>offset || !nameBytes.equals(bytes.subarray(local+30,local+30+n))) invalid();
    if(!(flags&8) && (bytes.readUInt32LE(local+14)!==crc || bytes.readUInt32LE(local+18)!==compressed || bytes.readUInt32LE(local+22)!==length)) invalid();
    if(regions.some(([a,b])=>local<b && finish>a)) invalid(); regions.push([local,finish]);
    expanded+=length; if(expanded>MAX_EXPANDED || (directory && length!==0)) invalid();
    let data; try { data=method===0?Buffer.from(bytes.subarray(start,finish)):inflateRawSync(bytes.subarray(start,finish),{maxOutputLength:Math.max(1,length)}); } catch { invalid(); }
    if(data.length!==length || crc32(data)!==crc) invalid();
    entries.push({name,directory,data}); cursor+=46+n+extra+comment;
  }
  if(cursor!==end) invalid();
  const files=entries.filter(e=>!e.directory);
  let prefix='';
  if(!files.some(e=>e.name==='SKILL.md')) {
    prefix=slug+'/'; if(!files.some(e=>e.name===prefix+'SKILL.md') || entries.some(e=>e.name!==prefix && !e.name.startsWith(prefix))) invalid();
  }
  const result=new Map();
  for(const entry of files) {
    const name=entry.name.slice(prefix.length);
    if(name===RECEIPT || name.toLowerCase()===RECEIPT || result.has(name.toLowerCase())) invalid();
    result.set(name,entry.data);
  }
  for(const name of result.keys()) for(const other of result.keys()) if(name!==other && other.toLowerCase().startsWith(name.toLowerCase()+'/')) invalid();
  const skill=result.get('SKILL.md')?.toString('utf8');
  if(!skill || skill.length>128*1024 || !skill.startsWith('---\n') && !skill.startsWith('---\r\n')) invalid();
  const front=skill.split(/\r?\n---(?:\r?\n|$)/)[0];
  const declared=front.match(/^name:\s*["']?([a-z0-9-]+)["']?\s*$/m)?.[1];
  if(declared!==slug) fail('skill_name_mismatch','The package Skill name does not match the catalogue.');
  return result;
}
async function actualFiles(folder, relative='', output={}) {
  for(const entry of await fs.readdir(path.join(folder,relative),{withFileTypes:true})) {
    const name=relative?relative+'/'+entry.name:entry.name;
    if(name===RECEIPT) continue;
    const file=path.join(folder,...name.split('/')), stat=await fs.lstat(file);
    if(stat.isSymbolicLink() || !stat.isFile() && !stat.isDirectory()) fail('local_changed','The installed Skill contains a link or special file.');
    if(stat.isDirectory()) await actualFiles(folder,name,output);
    else { if(stat.size>MAX_EXPANDED) fail('local_changed','The installed Skill has changed.'); output[name]=digest(await fs.readFile(file)); }
    if(Object.keys(output).length>500) fail('local_changed','The installed Skill has changed.');
  }
  return output;
}
async function receiptAt(folder) {
  await safeDirectory(folder);
  const file=path.join(folder,RECEIPT), stat=await exists(file);
  if(!stat || !stat.isFile() || stat.isSymbolicLink() || stat.size>200000) fail('unmanaged_install','This folder was not installed by the MochiLab assistant.');
  let receipt; try { receipt=JSON.parse(await fs.readFile(file,'utf8')); } catch { fail('receipt_invalid','The local installation record is invalid.'); }
  return receipt;
}
export async function installFiles(workspace, slug, files, record, update=false) {
  const root=await safeDirectory(workspace), skills=await safeDirectory(path.join(root,'skills'),true), target=path.join(skills,slug);
  if(!SLUG.test(slug) || files.size===0) fail('slug_invalid','Choose a valid Skill.');
  const stat=await exists(target); let backup=null;
  if(stat) {
    if(!update) fail('already_installed','This Skill is already installed. Use update to change its version.');
    const old=await receiptAt(target);
    if(old.site!==record.site || old.slug!==slug || !old.files || typeof old.files!=='object') fail('unmanaged_install','The installed Skill belongs to another source.');
    const actual=await actualFiles(target), original=old.files;
    if(Object.keys(actual).length!==Object.keys(original).length || Object.entries(actual).some(([n,h])=>original[n]!==h))
      fail('local_changed','Local Skill files have been changed. Preserve your changes before updating.');
    if(old.versionId===record.versionId && old.sha256===record.sha256) return {status:'already_current',slug,version:old.version,path:target};
    const backups=await safeDirectory(path.join(root,'.mochilab-backups'),true);
    backup=path.join(backups,slug+'-'+Date.now()+'-'+randomBytes(6).toString('hex'));
  } else if(update) fail('not_installed','Install this Skill before updating it.');
  const stage=await fs.mkdtemp(path.join(skills,'.mochilab-stage-'));
  try {
    const hashes={};
    for(const [name,bytes] of files) {
      if(!name.split('/').every(validPart)) fail('zip_invalid','Invalid package path.');
      const file=path.join(stage,...name.split('/'));
      await fs.mkdir(path.dirname(file),{recursive:true}); await fs.writeFile(file,bytes,{flag:'wx',mode:0o600}); hashes[name]=digest(bytes);
    }
    await fs.writeFile(path.join(stage,RECEIPT),JSON.stringify({...record,formatVersion:1,slug,files:hashes},null,2)+'\n',{flag:'wx',mode:0o600});
    if(backup) await fs.rename(target,backup);
    try { if(await exists(target)) fail('target_changed','The destination changed during installation.'); await fs.rename(stage,target); }
    catch(e) { if(backup && !await exists(target)) await fs.rename(backup,target); throw e; }
  } finally { if(await exists(stage)) await fs.rm(stage,{recursive:true,force:true}); }
  return {status:update?'updated':'installed',slug,version:record.version,path:target,...(backup?{backup}:{}),next:'Start a new OpenClaw conversation, then ask it to use this Skill.'};
}
function summary(skill) {
  return {slug:skill.slug,title:skill.title,summary:skill.summary,access:skill.accessType,version:skill.latestVersion,tags:skill.tags,url:'https://mochilab.bz/Skills/Detail.aspx?id='+encodeURIComponent(skill.id)};
}
function options(args) {
  const result={command:args[0]||'help'};
  for(let i=1;i<args.length;i++) {
    const key=args[i]; if(!['--site','--workspace','--slug','--query','--locale'].includes(key) || result[key.slice(2)]!==undefined || i+1>=args.length) fail('arguments_invalid','Use help to see supported arguments.');
    result[key.slice(2)]=args[++i];
  }
  return result;
}
async function readSecret(input, output) {
  if(!input.isTTY) { let value=''; for await(const chunk of input){value+=chunk; if(value.length>512) fail('key_invalid','The key input is too long.');} return value.trim(); }
  output.write('MochiLab Skills key (mls_): ');
  const terminal=createInterface({input,output,terminal:true});
  terminal._writeToOutput=()=>{};
  return await new Promise(resolve=>{terminal.question('',key=>{terminal.close(); output.write('\n'); resolve(key.trim());});});
}
export async function run(args, {env=process.env,input=process.stdin,errorOutput=process.stderr}={}) {
  const opt=options(args), site=siteUrl(opt.site), client=new Client(site);
  const locale=opt.locale==='en'?'en':'zh-CN';
  if(opt.command==='help') return {commands:['search [--query WORD]','show --slug NAME','login','status','logout','install --slug NAME --workspace PATH','installed --workspace PATH','updates --workspace PATH','update --slug NAME --workspace PATH','bootstrap --workspace PATH'],keyPage:site+'/Member/SkillAccess.aspx',keyInput:'Use login in your own terminal, or configure MOCHILAB_SKILLS_KEY outside the chat.'};
  if(opt.command==='login') {
    const key=await readSecret(input,errorOutput);
    if(!KEY.test(key)) fail('key_invalid','Use a Skills access key beginning with mls_.');
    client.key=key; const state=await client.api('skills.client.status',undefined,true);
    await saveKey(site,key,env); return {connected:true,membership:state.membership};
  }
  if(opt.command==='logout') {
    const file=credentialPath(env); if(!await exists(path.dirname(file))) return {connected:false,removedLocalKey:false,environmentKeyConfigured:!!env.MOCHILAB_SKILLS_KEY};
    await safeDirectory(path.dirname(file));
    const stat=await exists(file); if(stat && (!stat.isFile() || stat.isSymbolicLink())) fail('credential_path','Invalid credential path.');
    if(stat) await fs.unlink(file);
    return {removedLocalKey:!!stat,environmentKeyConfigured:!!env.MOCHILAB_SKILLS_KEY,revokePage:site+'/Member/SkillAccess.aspx'};
  }
  if(opt.command==='status') { client.key=await loadKey(site,env); return await client.api('skills.client.status',undefined,true); }
  if(opt.command==='search') {
    const data=await client.request('Api/Api.ashx?action=public.catalog&locale='+locale);
    if(!Array.isArray(data.items)) fail('response_invalid','The catalogue is invalid.');
    const terms=(opt.query||'').toLowerCase().split(/[\s,，]+/).filter(Boolean);
    const items=data.items.filter(s=>s.status==='published' && SLUG.test(s.slug||'') && terms.every(t=>[s.title,s.summary,s.slug,...(Array.isArray(s.tags)?s.tags:[])].join(' ').toLowerCase().includes(t)));
    return {items:items.slice(0,30).map(summary),total:items.length};
  }
  if(['installed','updates'].includes(opt.command)) {
    if(!opt.workspace) fail('workspace_required','Specify the active OpenClaw workspace with --workspace.');
    const root=await safeDirectory(opt.workspace), directory=path.join(root,'skills'), result=[];
    if(!await exists(directory)) return {items:[]};
    await safeDirectory(directory);
    for(const entry of await fs.readdir(directory,{withFileTypes:true})) if(entry.isDirectory() && SLUG.test(entry.name)) {
      try { const r=await receiptAt(path.join(directory,entry.name)); if(r.slug===entry.name && r.site===site) result.push({slug:r.slug,version:r.version,versionId:r.versionId}); }
      catch(e) { if(!['unmanaged_install','directory_invalid','receipt_invalid'].includes(e.code)) throw e; }
    }
    if(opt.command==='updates') for(const r of result) {
      if(r.slug==='mochilab-skills') { const m=await client.request('Content/Downloads/mochilab-skills.json'); r.availableVersion=m.version; r.updateAvailable=m.versionId!==r.versionId; }
      else { const data=await client.request('Api/Api.ashx?action=public.skill&locale='+locale+'&slug='+encodeURIComponent(r.slug)); r.availableVersion=data.skill.latestVersion; r.updateAvailable=data.skill.activeVersionId!==r.versionId; }
    }
    return {items:result};
  }
  const slug=opt.command==='bootstrap'?'mochilab-skills':opt.slug;
  if(!SLUG.test(slug||'') || slug.length>100) fail('slug_invalid','Specify a Skill slug from the catalogue.');
  if(opt.command==='show') {
    const data=await client.request('Api/Api.ashx?action=public.skill&locale='+locale+'&slug='+encodeURIComponent(slug));
    return {...summary(data.skill),body:data.skill.body,install:data.skill.install,dependencies:data.skill.dependencies};
  }
  if(!['install','update','bootstrap'].includes(opt.command)) fail('arguments_invalid','Use help to see supported commands.');
  if(!opt.workspace) fail('workspace_required','Specify the active OpenClaw workspace with --workspace.');
  const workspace=await safeDirectory(opt.workspace); let record, bytes;
  if(slug==='mochilab-skills') {
    record=await client.request('Content/Downloads/mochilab-skills.json');
    if(record.slug!==slug || !/^Content\/Downloads\/[a-z0-9.-]+\.zip$/.test(record.packagePath||'')) fail('manifest_invalid','The assistant manifest is invalid.');
  } else {
    const data=await client.request('Api/Api.ashx?action=public.skill&locale='+locale+'&slug='+encodeURIComponent(slug)), skill=data.skill;
    if(skill.slug!==slug || skill.status!=='published' || !ID.test(skill.id) || !ID.test(skill.activeVersionId)) fail('manifest_invalid','This Skill has no published package.');
    const version=data.versions?.find(v=>v.id===skill.activeVersionId && v.status==='published');
    if(!version) fail('manifest_invalid','This Skill has no published package.');
    record={skillId:skill.id,version:version.version,versionId:version.id,sha256:version.sha256,bytes:version.bytes,packagePath:'Download.ashx?skill='+skill.id+'&version='+version.id};
    client.key=await loadKey(site,env);
    if(skill.accessType==='free') await client.api('skills.claim',{skillId:skill.id},true);
  }
  if(!HASH.test(record.sha256||'') || !ID.test(record.versionId||'') || !Number.isSafeInteger(record.bytes) || record.bytes<=0 || record.bytes>MAX_ZIP || !/^[0-9A-Za-z.+-]{1,40}$/.test(record.version||'')) fail('manifest_invalid','Invalid package version, size or checksum.');
  bytes=await client.request(record.packagePath,{auth:slug!=='mochilab-skills',binary:true});
  if(bytes.length!==record.bytes || digest(bytes)!==record.sha256) fail('checksum_mismatch','The package checksum does not match. Nothing was installed.');
  return await installFiles(workspace,slug,unpack(bytes,slug),{site,skillId:record.skillId||'',version:record.version,versionId:record.versionId,sha256:record.sha256},opt.command==='update');
}
if(process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  run(process.argv.slice(2)).then(value=>process.stdout.write(JSON.stringify({ok:true,data:value},null,2)+'\n')).catch(error=>{
    const code=error instanceof ClientError?error.code:'local_error';
    const message=error instanceof ClientError?error.message:'The operation could not finish. Check local paths, permissions and available space.';
    process.stderr.write(JSON.stringify({ok:false,error:{code,message}})+'\n'); process.exitCode=1;
  });
}
