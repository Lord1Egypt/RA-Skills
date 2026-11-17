import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 from html.parser import HTMLParser
 class Parser(HTMLParser):
  def __init__(self):super().__init__(convert_charrefs=True);self.tables=[];self.depth=0;self.row=None;self.cell=None
  def handle_starttag(self,t,a):
   if t=='table':self.depth+=1;self.tables.append([]) if self.depth==1 else None
   if self.depth==1 and t=='tr':self.row=[]
   if self.depth==1 and t in ['td','th']:self.cell=[]
  def handle_data(self,d):
   if self.cell is not None:self.cell.append(d)
  def handle_endtag(self,t):
   if t in ['td','th'] and self.cell is not None:
    if self.row is not None:self.row.append(' '.join(''.join(self.cell).split()))
    self.cell=None
   if t=='tr' and self.row is not None:self.tables[-1].append(self.row);self.row=None
   if t=='table':self.depth=max(0,self.depth-1)
 p=Parser();p.feed(c.read(r['file']));i=int(r.get('table',0));need(0<=i<len(p.tables),'Table index not found');rows=p.tables[i]
 out=io.StringIO();csv.writer(out).writerows(rows);c.emit('table.csv',out.getvalue());return {'rows':len(rows),'tableCount':len(p.tables),'sourceUrl':r.get('sourceUrl'),'liveBrowserUsed':False}
