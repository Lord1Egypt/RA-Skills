import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 steps=r['steps'];by={x['id']:x for x in steps};need(len(by)==len(steps),'Duplicate step ID');done=[];pending=set(by)
 for x in steps:need(set(x.get('needs',[]))<=set(by),'Unknown dependency')
 while pending:
  ready=sorted(k for k in pending if set(by[k].get('needs',[]))<=set(done));need(ready,'Dependency cycle')
  done+=ready;pending-=set(ready)
 return {'executionOrder':done,'mutatingSteps':[x['id'] for x in steps if x.get('mutates')],'scheduled':False,'externalActionsExecuted':False}
