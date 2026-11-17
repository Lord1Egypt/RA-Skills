import time
from core import *

def open_readonly(s,name):
 p=local(s.root,name,'file');require(p.stat().st_size<=256*1024*1024,'Database exceeds 256 MiB');db=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True,timeout=5);db.enable_load_extension(False);db.execute('PRAGMA query_only=ON');db.execute('PRAGMA busy_timeout=5000');return db
def handle(s,r):
 a=r.get('action')
 if a=='import-csv':
  fields,rows=csv_rows(local(s.root,r['file'],'file'));require(len(fields)<=250,'Too many columns');table=ident(r.get('table','data'));out=s.exports();dest=out/'imported.sqlite';db=sqlite3.connect(dest)
  quote=lambda v:'"'+v.replace('"','""')+'"'
  try:
   with db:
    db.execute('CREATE TABLE '+quote(table)+' ('+','.join(quote(k)+' TEXT' for k in fields)+')')
    db.executemany('INSERT INTO '+quote(table)+' VALUES('+','.join('?' for k in fields)+')',[[row[k] for k in fields] for row in rows])
   require(db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','Imported database integrity check failed')
  finally:db.close()
  return {'database':s.rel(dest),'table':table,'rows':len(rows),'columns':fields,'columnType':'TEXT','sourceModified':False}
 require(a in ('schema','query','integrity'),'Actions: schema, query, import-csv, integrity');db=open_readonly(s,r['database'])
 try:
  if a=='schema':
   tables=[]
   for name,kind in db.execute("SELECT name,type FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY name"):
    require(len(tables)<500,'Too many database objects');q='"'+name.replace('"','""')+'"';tables.append({'name':name,'type':kind,'columns':[{'name':x[1],'type':x[2],'notNull':bool(x[3]),'primaryKey':x[5]} for x in db.execute('PRAGMA table_info('+q+')')]})
   return s.report({'database':r['database'],'objects':tables},'SQLite schema')
  if a=='integrity':
   deadline=time.monotonic()+10;db.set_progress_handler(lambda:int(time.monotonic()>deadline),1000);result=db.execute('PRAGMA integrity_check(100)').fetchmany(100);return {'database':r['database'],'ok':result==[('ok',)],'messages':[x[0] for x in result]}
  sql=r.get('sql','');require(isinstance(sql,str) and 0<len(sql)<=10000,'SQL length must be 1..10000 characters');maximum=limit(r.get('limit',1000),1,10000);deadline=time.monotonic()+limit(r.get('timeoutSeconds',5),1,15);steps=[0]
  def progress():steps[0]+=1000;return int(time.monotonic()>deadline or steps[0]>2000000)
  def authorizer(action,p1,p2,db_name,trigger):
   if action==sqlite3.SQLITE_FUNCTION and str(p2 or p1).lower() in ('load_extension','readfile','writefile','randomblob','zeroblob','printf','format'):return sqlite3.SQLITE_DENY
   return sqlite3.SQLITE_OK if action in (sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION,sqlite3.SQLITE_RECURSIVE) else sqlite3.SQLITE_DENY
  db.set_progress_handler(progress,1000);db.set_authorizer(authorizer)
  try:cursor=db.execute(sql,r.get('parameters',[]));fields=[x[0] for x in cursor.description];require(len(fields)==len(set(fields)),'Use unique aliases for result columns');rows=cursor.fetchmany(maximum+1)
  except sqlite3.Error:raise ValueError('Read-only query rejected or execution limit reached; SELECT/CTE only') from None
  truncated=len(rows)>maximum;rows=rows[:maximum]
  def value(x):return {'blobHex':x.hex()} if isinstance(x,bytes) else x
  mapped=[dict(zip(fields,[value(x) for x in row])) for row in rows];return s.report({'database':r['database'],'columns':fields,'rows':mapped,'returnedRows':len(mapped),'truncated':truncated,'sourceModified':False},'SQLite query', (fields,mapped))
 finally:db.close()
