import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 versions=r['artifacts'];issues=[]
 for x in versions:
  if not re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?',x['version']):issues.append({'name':x['name'],'issue':'invalid-version'})
  if not re.fullmatch(r'[a-f0-9]{64}',x.get('sha256','')):issues.append({'name':x['name'],'issue':'missing-or-invalid-sha256'})
  if x.get('testStatus')!='passed':issues.append({'name':x['name'],'issue':'tests-not-passed'})
 return {'readyForReview':not issues,'issues':issues,'artifacts':len(versions),'filesOrRemoteDownloadsVerified':False,'publicationPerformed':False}
