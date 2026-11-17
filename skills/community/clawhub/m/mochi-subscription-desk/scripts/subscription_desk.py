"""Recurring subscriptions, cancellation deadlines and exact currency forecasts."""
import calendar,datetime as dt,re
from decimal import Decimal,InvalidOperation
from core import *
def validate(p):
    p=dict(p); ident(p['id']); iso_date(p['start'])
    if p.get('unit','month') not in ('day','month','year'): raise ValueError('Billing unit day, month or year')
    bounded(p.get('interval',1),1,120)
    amount=Decimal(str(p['amount']))
    if not amount.is_finite() or amount<0 or amount>Decimal('1000000000') or amount.as_tuple().exponent < -4: raise ValueError('Amount must be a positive decimal with <=4 decimals')
    if not re.fullmatch('[A-Z]{3}',p['currency']): raise ValueError('Explicit three-letter currency code required')
    p['amount']=str(amount); bounded(p.get('cancelLeadDays',0),0,365)
    if p.get('end'): iso_date(p['end'])
    return p
def due(p,n):
    a=iso_date(p['start']); step=int(p.get('interval',1))*n; unit=p.get('unit','month')
    if unit=='day': return a+dt.timedelta(days=step)
    months=a.year*12+a.month-1+(step*12 if unit=='year' else step); y,m=divmod(months,12); m+=1
    return dt.date(y,m,min(a.day,calendar.monthrange(y,m)[1]))
def forecast(p,start,end):
    base=iso_date(p['start']); unit=p.get('unit','month'); step=int(p.get('interval',1))
    diff=(start-base).days if unit=='day' else (start.year-base.year)*12+start.month-base.month
    if unit=='year': diff//=12
    n=max(0,diff//step-1); result=[]
    while True:
        d=due(p,n); n+=1
        if d>end or (p.get('end') and d>iso_date(p['end'])): break
        if d>=start: result.append(d)
        if len(result)>10000: raise ValueError('Forecast too large')
    return result
def handle(st,r):
    action=r['action']
    if action=='put':
        p=validate(r['subscription']); old=st.get('subscription',p['id'])
        changed=not old or {k:v for k,v in old.items() if k!='revision'}!={k:v for k,v in p.items() if k!='revision'}
        p['revision']=(old.get('revision',1)+1 if old else 1) if changed else old.get('revision',1)
        if changed:
            for n in st.pending():
                if n['noticeId'].startswith(p['id']+':'): st.ack([n['noticeId']])
        return st.put('subscription',p['id'],p)
    if action=='list': return st.all('subscription')
    if action=='remove':
        st.delete('subscription',r['id'])
        for n in st.pending():
            if n['noticeId'].startswith(r['id']+':'): st.ack([n['noticeId']])
        return {'removed':r['id']}
    if action=='ack': return st.ack(r['noticeIds'])
    if action=='forecast':
        a=iso_date(r['from']); b=iso_date(r['to'])
        if not 0<=(b-a).days<=3660: raise ValueError('Forecast range <=10 years')
        rows=[]; totals={}
        for p in st.all('subscription'):
            if p.get('enabled',True) is False: continue
            for d in forecast(p,a,b):
                rows.append({'subscriptionId':p['id'],'title':p['title'],'date':str(d),'amount':p['amount'],'currency':p['currency'],'cancelBefore':str(d-dt.timedelta(days=p.get('cancelLeadDays',0)))})
                totals[p['currency']]=totals.get(p['currency'],Decimal(0))+Decimal(p['amount'])
        return {'charges':sorted(rows,key=lambda x:x['date']),'totals':{k:str(v) for k,v in totals.items()}}
    if action=='poll':
        today=iso_date(r['date']); days=bounded(r.get('advanceDays',7),0,365)
        for p in st.all('subscription'):
            if p.get('enabled',True) is False: continue
            for d in forecast(p,today,today+dt.timedelta(days=days+p.get('cancelLeadDays',0))):
                cancel=d-dt.timedelta(days=p.get('cancelLeadDays',0))
                for kind,date in (('renewal',d),('cancel-deadline',cancel)):
                    if today<=date<=today+dt.timedelta(days=days): st.notice(p['id']+':'+str(p.get('revision',1))+':'+str(d)+':'+kind,{'type':kind,'title':p['title'],'date':str(date),'chargeDate':str(d),'amount':p['amount'],'currency':p['currency']})
        return {'notifications':st.pending()}
    raise ValueError('Unknown subscription action')
if __name__=='__main__': runmain(handle,'subscription-desk')
