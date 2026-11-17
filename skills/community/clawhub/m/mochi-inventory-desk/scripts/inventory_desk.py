from decimal import Decimal,InvalidOperation,ROUND_HALF_UP,getcontext
from core import *
getcontext().prec=80
def number(v,positive=False):
 require(isinstance(v,(str,int)) and not isinstance(v,bool),'Quantities and money must be decimal strings')
 try:d=Decimal(str(v))
 except InvalidOperation:raise ValueError('Invalid decimal')
 require(d.is_finite() and abs(d)<=Decimal('1e15') and d.as_tuple().exponent>=-6,'Decimal outside supported range')
 require(d>0 if positive else d>=0,'Value must be positive' if positive else 'Value cannot be negative');return d
def balances(s):
 rows={}
 for e in s.all('movement'):
  key=(e['sku'],e['warehouse']);v=rows.setdefault(key,{'quantity':Decimal(0),'value':Decimal(0),'currency':e['currency']});qty=Decimal(e['quantity'])
  require(v['currency']==e['currency'],'Currency mismatch in stock ledger')
  v['quantity']+=qty;v['value']+=Decimal(e['valueDelta'])
 return rows
def handle(s,r):
 a=r.get('action')
 if a=='item.upsert':
  sku=ident(r['sku']);old=s.get('item',sku,{})
  name=r.get('name',old.get('name'));require(isinstance(name,str) and name.strip(),'Item name required');currency=r.get('currency',old.get('currency','CNY')).upper();require(re.fullmatch('[A-Z]{3}',currency),'Use a three-letter currency')
  if old:
   require(currency==old['currency'],'Changing an existing SKU currency is not allowed')
   require(r.get('unit',old['unit'])==old['unit'] or not any(x['sku']==sku for x in s.all('movement')),'Cannot change units after stock movements exist')
  item={'sku':sku,'name':name.strip(),'unit':r.get('unit',old.get('unit','pcs')),'currency':currency,'reorderPoint':str(number(r.get('reorderPoint',old.get('reorderPoint','0')))),'targetStock':str(number(r.get('targetStock',old.get('targetStock','0'))))};return s.put('item',sku,item)
 if a=='move':
  key=ident(r['id']);sku=ident(r['sku']);warehouse=ident(r.get('warehouse','main'));item=s.get('item',sku);require(item is not None,'SKU not found');kind=r.get('kind');require(kind in ('in','out','adjust'),'Kinds: in, out, adjust')
  canonical={k:r.get(k) for k in ('id','sku','warehouse','kind','quantity','unitCost','reason','date')};fingerprint=sha(json.dumps(canonical,sort_keys=True).encode());old=s.get('movement',key)
  if old:require(old['requestHash']==fingerprint,'Movement ID exists with different data');return {'movement':old,'replayed':True}
  b=balances(s).get((sku,warehouse),{'quantity':Decimal(0),'value':Decimal(0)});qty=number(r['quantity'],kind!='adjust');cost=number(r.get('unitCost','0'));reason=r.get('reason','')
  if kind=='adjust':require(reason and 'unitCost' in r,'Stock count adjustment requires reason and unitCost');delta=qty-b['quantity'];value=qty*cost-b['value']
  elif kind=='in':require('unitCost' in r,'Stock-in requires unitCost');delta=qty;value=qty*cost
  else:require(qty<=b['quantity'],'Insufficient stock');delta=-qty;value=-(b['value']/b['quantity']*qty) if qty!=b['quantity'] else -b['value']
  day=r.get('date',dt.date.today().isoformat());dt.date.fromisoformat(day)
  e={'id':key,'sku':sku,'warehouse':warehouse,'kind':kind,'quantity':str(delta),'valueDelta':str(value),'currency':item['currency'],'date':day,'reason':str(reason)[:500],'requestHash':fingerprint,'createdAt':now()};s.put('movement',key,e);return {'movement':e,'replayed':False}
 if a=='ledger':return [x for x in s.all('movement') if (not r.get('sku') or x['sku']==r['sku']) and (not r.get('warehouse') or x['warehouse']==r['warehouse'])]
 if a in ('stock','report'):
  items={i['sku']:i for i in s.all('item')};rows=[];totals={};allbalances=balances(s);entries=dict(allbalances)
  for sku,item in items.items():
   warehouse=r.get('warehouse','main')
   if r.get('warehouse') and (sku,warehouse) not in entries or not any(k[0]==sku for k in entries):entries[(sku,warehouse)]={'quantity':Decimal(0),'value':Decimal(0),'currency':item['currency']}
  for (sku,warehouse),b in sorted(entries.items()):
   if r.get('warehouse') and warehouse!=r['warehouse']:continue
   i=items[sku];reorder=Decimal(i['reorderPoint']);target=max(reorder,Decimal(i['targetStock']));low=b['quantity']<=reorder
   row={**i,'warehouse':warehouse,'quantity':str(b['quantity']),'stockValue':str(b['value'].quantize(Decimal('.01'),rounding=ROUND_HALF_UP)),'lowStock':low,'suggestedReorder':str(max(Decimal(0),target-b['quantity'])) if low else '0'};rows.append(row);totals[i['currency']]=totals.get(i['currency'],Decimal(0))+b['value']
  missing=[i['sku'] for i in items.values() if not any(k[0]==i['sku'] for k in allbalances)]
  data={'stock':rows,'unstockedSKUs':missing,'valueByCurrency':{k:str(v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)) for k,v in totals.items()},'valuation':'moving weighted average; no currency conversion'}
  return s.report(data,'Inventory and reorder report',(['sku','name','warehouse','quantity','unit','currency','stockValue','lowStock','suggestedReorder'],rows)) if a=='report' else data
 raise ValueError('Actions: item.upsert, move, stock, ledger, report')
