from helpers import *
import zipfile
from xml.etree import ElementTree as ET

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS={'w':W}
def el(parent,n,attrs=None,value=None):
 e=ET.SubElement(parent,'{'+W+'}'+n,{'{'+W+'}'+k:str(v) for k,v in (attrs or {}).items()})
 if value is not None:e.text=value
 return e
def para(parent,value,style=None):
 p=el(parent,'p')
 if style:el(el(p,'pPr'),'pStyle',{'val':style})
 t=el(el(p,'r'),'t',value=text(value,20000,True));t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');return p
def handle(s,r):
 action=r.get('action')
 if action=='create':
  title=text(r['title'],500);sections=objects(r,'sections',100);root=ET.Element('{'+W+'}document');body=el(root,'body');para(body,title,'Title');tables=0
  for x in sections:
   para(body,text(x['heading'],500),'Heading1')
   for p in strings(x.get('paragraphs',[]),200):para(body,p)
   for item in strings(x.get('bullets',[]),200):para(body,'• '+item)
   if 'table' in x:
    table=x['table'];require(isinstance(table,list) and 0<len(table)<=1000 and all(isinstance(row,list) for row in table),'Invalid table');width=len(table[0]);require(1<=width<=10 and all(len(row)==width for row in table),'Unequal table rows');tbl=el(body,'tbl');props=el(tbl,'tblPr');el(props,'tblStyle',{'val':'TableGrid'});el(props,'tblW',{'w':0,'type':'auto'})
    for row in table:
     tr=el(tbl,'tr')
     for cell in row:para(el(tr,'tc'),text(cell,10000,True))
    tables+=1
  sect=el(body,'sectPr');el(sect,'pgSz',{'w':11906,'h':16838});el(sect,'pgMar',{'top':1440,'right':1440,'bottom':1440,'left':1440,'header':720,'footer':720,'gutter':0})
  styles=ET.Element('{'+W+'}styles')
  for name,size,bold in [('Normal',22,False),('Title',40,True),('Heading1',30,True)]:
   style=el(styles,'style',{'type':'paragraph','styleId':name});el(style,'name',{'val':name});rp=el(style,'rPr');el(rp,'rFonts',{'ascii':'Calibri','hAnsi':'Calibri','eastAsia':'Microsoft YaHei'});el(rp,'sz',{'val':size})
   if bold:el(rp,'b')
  st=el(styles,'style',{'type':'table','styleId':'TableGrid'});el(st,'name',{'val':'Table Grid'});borders=el(el(st,'tblPr'),'tblBorders')
  for side in ['top','left','bottom','right','insideH','insideV']:el(borders,side,{'val':'single','sz':4,'color':'B8C6D8'})
  out=io.BytesIO()
  with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
   z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
   z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
   z.writestr('word/_rels/document.xml.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
   z.writestr('word/document.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True));z.writestr('word/styles.xml',ET.tostring(styles,encoding='utf-8',xml_declaration=True))
  return file_report(s,{'title':title,'sections':len(sections),'tables':tables,'format':'DOCX','layoutRendered':False},'document.docx',out.getvalue())
 if action=='inspect':
  p=local(s.root,r['file'],'file');readbytes(p,16*1024*1024)
  with zipfile.ZipFile(p) as z:
   require(len(z.infolist())<=2000 and sum(x.file_size for x in z.infolist())<=32*1024*1024,'DOCX too large');require(not any('vbaProject' in n for n in z.namelist()),'Macro content unsupported');b=z.read('word/document.xml');require(b'<!DOCTYPE' not in b.upper() and b'<!ENTITY' not in b.upper(),'DTD/entity content unsupported');doc=ET.fromstring(b)
  return s.report({'paragraphs':[''.join(p.itertext()) for p in doc.findall('.//w:p',NS)],'tables':len(doc.findall('.//w:tbl',NS)),'sourceSha256':sha(readbytes(p))})
 raise ValueError('Actions: create, inspect')
