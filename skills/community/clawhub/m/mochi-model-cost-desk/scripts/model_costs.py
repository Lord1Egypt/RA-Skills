from helpers import *
from decimal import Decimal,InvalidOperation

def amount(v):
 try:d=Decimal(str(v))
 except (InvalidOperation,ValueError):raise ValueError('Invalid decimal amount')
 require(d.is_finite() and d>=0 and d<=Decimal('1e12'),'Amount outside range');return d

def handle(s,r):
 require(r.get('action')=='estimate','Action: estimate');rate_rows=objects(r,'rates',100);rates={}
 for x in rate_rows:
  model=text(x['model'],200);require(model not in rates,'Duplicate model rate');currency=text(x['currency'],3);require(re.fullmatch('[A-Z]{3}',currency),'Currency needs ISO-style three-letter code');rates[model]={'currency':currency,'input':amount(x['inputPerMillion']),'cached':amount(x['cachedInputPerMillion']),'output':amount(x['outputPerMillion'])}
 fields,rows=csv_rows(local(s.root,r['file'],'file'));require({'model','input_tokens','cached_input_tokens','output_tokens'}<=set(fields),'CSV missing token columns');groups={};allrows=[]
 for n,x in enumerate(rows,2):
  model=x['model'];require(model in rates,'Missing rate for model');a=rates[model];values=[]
  for k in ['input_tokens','cached_input_tokens','output_tokens']:
   require(re.fullmatch(r'\d{1,15}',x[k]),'Token counts must be nonnegative integers');values.append(int(x[k]))
  inp,cached,out=values;require(cached<=inp,'Cached input exceeds total input');cost=((inp-cached)*a['input']+cached*a['cached']+out*a['output'])/Decimal(1000000);group=groups.setdefault(a['currency'],{'cost':Decimal(0),'requests':0});group['cost']+=cost;group['requests']+=1
  allrows.append({'row':n,'model':model,'currency':a['currency'],'estimatedCost':str(cost),'inputTokens':inp,'cachedInputTokens':cached,'outputTokens':out})
 totals=[{'currency':k,'estimatedCost':str(v['cost']),'requests':v['requests']} for k,v in sorted(groups.items())]
 budget=r.get('budget');alerts=[]
 if budget is not None:
  require(isinstance(budget,dict),'Budget must map currency to amount')
  for currency,value in budget.items():
   cap=amount(value)
   if currency in groups:alerts.append({'currency':currency,'budget':str(cap),'exceeded':groups[currency]['cost']>cap})
 return s.report({'ratesAsOf':text(r['ratesAsOf'],100),'totals':totals,'rows':allrows,'budgetChecks':alerts,'billingVerified':False,'note':'User-supplied rates and usage estimate; no automatic provider access or currency conversion.'},table=(['row','model','currency','estimatedCost','inputTokens','cachedInputTokens','outputTokens'],allrows))
