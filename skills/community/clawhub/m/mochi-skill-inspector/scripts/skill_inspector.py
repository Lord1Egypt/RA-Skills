from helpers import *
import zipfile,posixpath

RULES=[('process-execution',r'\b(subprocess|child_process|os\.system|eval\(|exec\(|shell=True)'),('network-access',r'https?://|\b(requests\.|urllib\.|fetch\(|curl\s|wget\s)'),('secret-reference',r'(?i)api[_-]?key|credentials\.json|\.ssh/|BEGIN .*PRIVATE KEY'),('policy-override-text',r'(?i)ignore (all |previous |prior )?instructions|disable (all )?(security|sandbox)|忽略.*指令'),('persistent-startup',r'(?i)crontab|systemctl.*enable|LaunchAgents|startupfolder')]

def handle(s,r):
 require(r.get('action')=='inspect','Action: inspect');p=local(s.root,r['file'],'file');readbytes(p,16*1024*1024);findings=[];files=[];total=0;seen=set();has_skill=False
 with zipfile.ZipFile(p) as z:
  require(len(z.infolist())<=2000,'Too many archive members')
  for entry in z.infolist():
   n=entry.filename;clean=n.replace('\\','/');parts=clean.split('/');require(not clean.startswith('/') and '..' not in parts and not re.match(r'^[A-Za-z]:',clean) and '\x00' not in n,'Unsafe archive path')
   require(clean.casefold() not in seen,'Duplicate archive member');seen.add(clean.casefold());require(not stat.S_ISLNK(entry.external_attr>>16),'Archive contains symbolic link')
   require(not entry.flag_bits&1,'Encrypted archive unsupported');total+=entry.file_size;require(total<=32*1024*1024 and entry.file_size<=4*1024*1024,'Uncompressed archive exceeds limit')
   require(entry.file_size<=1000*max(1,entry.compress_size),'Excessive compression ratio')
   if entry.is_dir():continue
   data=z.read(entry);has_skill|=posixpath.basename(clean)=='SKILL.md';files.append({'path':clean,'bytes':len(data),'sha256':sha(data)})
   if clean.lower().endswith(('.exe','.dll','.so','.dylib','.bat','.ps1')):findings.append({'file':clean,'rule':'binary-or-platform-executable'})
   if len(data)<1024*1024:
    try:content=data.decode('utf-8')
    except UnicodeDecodeError:continue
    for rule,pattern in RULES:
     for number,line in enumerate(content.splitlines(),1):
      if re.search(pattern,line):findings.append({'file':clean,'line':number,'rule':rule})
   require(len(findings)<=20000,'Too many findings')
 require(has_skill,'No SKILL.md found')
 return s.report({'archiveSha256':sha(readbytes(p)),'files':files,'findings':findings,'reviewRequired':bool(findings),'executed':False,'assurance':'Static indicators only; a clean result is not a safety certification.'})
