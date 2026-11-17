"""Only Simmer virtual $SIM: no real venue, signing or wallet endpoints."""
import asyncio,json,os,re,sqlite3,time,uuid
from pathlib import Path
import httpx
from common import atomic_json,redact,dec

BASE='https://api.simmer.markets'
SOURCE='sdk:k14-paper-v020'

class SimmerPaper:
    def __init__(self,state_dir):
        self.root=Path(state_dir);self.root.mkdir(parents=True,exist_ok=True)
        key=os.environ.get('SIMMER_API_KEY','').strip()
        if not key:raise ValueError('SIMMER_API_KEY missing; supply through environment, never publish it')
        self.http=httpx.AsyncClient(base_url=BASE,headers={'Authorization':'Bearer '+key},timeout=30,follow_redirects=False)
        self.db=sqlite3.connect(self.root/'simmer.sqlite')
        self.db.execute('pragma journal_mode=WAL');self.db.execute('pragma synchronous=FULL')
        self.db.execute('create table if not exists requests (id text primary key, body text, status text, response text)')
        self.db.execute('create table if not exists mappings (slug text primary key, market_id text, yes_side text)')
        self.db.execute('create table if not exists mirror_positions (slug text, side text, model_qty text, sim_qty text, primary key(slug,side))')
        self.db.commit();self.last_error=None
    async def close(self):await self.http.aclose();self.db.close()
    async def get(self,path,params=None):
        allowed=('/api/sdk/agents/me','/api/sdk/portfolio','/api/sdk/markets','/api/sdk/markets/check','/api/sdk/positions','/api/sdk/trades')
        if path not in allowed:raise ValueError('GET not allowlisted')
        for attempt in range(3):
            try:
                r=await self.http.get(path,params=params);r.raise_for_status();return r.json()
            except httpx.TransportError:
                if attempt==2:raise
                await asyncio.sleep(.5*(attempt+1))
    async def trade(self,key,market_id,side,action,*,amount=0,shares=0,reason='K14 paper mirror',dry_run=False,source=SOURCE):
        if side not in ('yes','no') or action not in ('buy','sell'):raise ValueError('invalid virtual trade')
        if action=='buy' and not 0<float(amount)<=2.5:raise ValueError('paper buy exceeds per-order cap')
        if action=='sell' and not 0<float(shares)<=100:raise ValueError('invalid owned virtual shares')
        body={'market_id':str(uuid.UUID(market_id)),'side':side,'action':action,'venue':'sim','execute':False,'dry_run':bool(dry_run),'amount':float(amount),'shares':float(shares),'source':source,'skill_slug':'k14-btc-observer','skill_version':'0.2.0','reasoning':reason,'idempotency_key':key,'signal_data':{'mode':'SIMMER_VIRTUAL_MIRROR','execution_equivalent_to_polymarket':False}}
        old=self.db.execute('select status,response,body from requests where id=?',(key,)).fetchone()
        if old:
            if json.loads(old[2])!=body:raise ValueError('idempotency key reused with different virtual request')
            if old[0]=='COMPLETE':return json.loads(old[1])
            raise RuntimeError('prior virtual request unresolved/rejected; no automatic repost: '+key)
        # Persist BEFORE POST. Unknown outcomes must be reconciled, never resent.
        if action=='buy' and not dry_run:
            spent=0
            for body0,status in self.db.execute('select body,status from requests'):
                b=json.loads(body0)
                if not b.get('dry_run') and b.get('action')=='buy' and status in ('SENDING','UNKNOWN','COMPLETE'):
                    spent+=float(b['amount'])
            if spent+float(amount)>6:raise ValueError('virtual test buy budget of 6 SIM exhausted')
        self.db.execute('insert into requests values (?,?,?,?)',(key,json.dumps(body),'SENDING',None));self.db.commit()
        try:
            # venue is hardcoded here, not accepted from callers or configuration.
            if body['venue']!='sim' or body['execute'] is not False:raise RuntimeError('real-money routing forbidden')
            r=await self.http.post('/api/sdk/trade',json=body)
            try:data=r.json()
            except Exception:data={'http_status':r.status_code,'error':'non-json response'}
            data=redact(data)
            status='COMPLETE' if r.status_code==200 and data.get('success') is True else 'REJECTED' if r.status_code<500 else 'UNKNOWN'
            if data.get('venue') not in (None,'sim','simmer','sandbox'):raise RuntimeError('server returned unexpected venue')
            self.db.execute('update requests set status=?,response=? where id=?',(status,json.dumps(data),key));self.db.commit()
            if status!='COMPLETE':self.last_error=data
            return data
        except Exception as ex:
            self.db.execute('update requests set status=? where id=?',('UNKNOWN',key));self.db.commit()
            self.last_error=type(ex).__name__;raise
    async def status(self):
        a=await self.get('/api/sdk/agents/me')
        p=await self.get('/api/sdk/portfolio',{'venue':'sim'})
        t=await self.get('/api/sdk/trades',{'venue':'sim','limit':20})
        result={'agent':{k:a.get(k) for k in ('id','name','status','claimed','limits')},'virtual_portfolio':p,'virtual_trades':t,'requests':self.request_summary(),'real_trade_requests':0,'last_error':self.last_error}
        atomic_json(self.root/'simmer-status.json',redact(result));return result
    def request_summary(self):
        return [{'id':rid,'status':status,'request':json.loads(body),'response':json.loads(resp) if resp else None} for rid,body,status,resp in self.db.execute('select * from requests')]
    async def resolve(self,slug,tokens):
        if not re.fullmatch(r'btc-updown-15m-\d+',slug):raise ValueError('unrecognized BTC 15m market')
        if set(tokens)!=set(('Up','Down')):raise ValueError('verified public outcome tokens required')
        row=self.db.execute('select market_id,yes_side from mappings where slug=?',(slug,)).fetchone()
        if row:return row
        url='https://polymarket.com/event/'+slug
        data=await self.get('/api/sdk/markets/check',{'url':url})
        market=data.get('market') or data
        mid=market.get('market_id') or market.get('id')
        if not data.get('exists') or not mid:
            # Metadata import does not submit an order or spend money.
            r=await self.http.post('/api/sdk/markets/import',json={'polymarket_url':url})
            r.raise_for_status();data=r.json();market=data.get('market') or data;mid=market.get('market_id') or market.get('id')
        if not mid:raise ValueError('market not available in Simmer')
        # Verify the imported source mapping, rather than assuming arbitrary YES means Up.
        lookup=await self.get('/api/sdk/markets',{'ids':mid,'tradeable_only':'false'})
        rows=lookup.get('markets',[])
        if not rows:raise ValueError('imported market lookup absent')
        record=rows[0];question=record.get('question','')
        yes,no=str(record.get('polymarket_token_id')),str(record.get('polymarket_no_token_id'))
        if 'bitcoin' not in question.lower() or 'up or down' not in question.lower() or {yes,no}!={str(tokens['Up']),str(tokens['Down'])}:
            raise ValueError('unverified BTC Up/Down source mapping')
        yes_side='Up' if yes==str(tokens['Up']) else 'Down'
        self.db.execute('insert or replace into mappings values (?,?,?)',(slug,mid,yes_side));self.db.commit();return mid,yes_side
    async def mirror(self,event):
        if event['kind']!='FILL':return
        slug=event['market'];side=event['side'];action=event['action'].lower()
        mid,yes_side=await self.resolve(slug,event.get('market_tokens',{}))
        which='yes' if side==yes_side else 'no'
        modelq=dec(event['quantity']);q0=self.db.execute('select model_qty,sim_qty from mirror_positions where slug=? and side=?',(slug,side)).fetchone()
        mq,sq=(dec(q0[0]),dec(q0[1])) if q0 else (dec(0),dec(0))
        if action=='buy':
            data=await self.trade('k14-'+event['id'],mid,which,'buy',amount=float(modelq*dec(event['price'])),reason='Mirror of hypothetical K14 fill; LMSR price/size differs from Maker model')
            if data.get('success'):
                q=dec(data.get('shares_bought',data.get('shares',0)))
                if q<=0:raise ValueError('virtual buy receipt has no confirmed shares')
                mq+=modelq;sq+=q
        else:
            if modelq>mq or sq<=0:raise ValueError('virtual mirror position differs; no guessed sell')
            q=sq*modelq/mq
            data=await self.trade('k14-'+event['id'],mid,which,'sell',shares=float(q),reason='Proportional close of separately recorded Simmer virtual position')
            if data.get('success'):
                sold=dec(data.get('shares_sold',data.get('shares',0)))
                if sold<=0 or sold>sq:raise ValueError('virtual sell receipt quantity invalid')
                mq-=modelq*(sold/q);sq-=sold
        if data.get('success'):
            self.db.execute('insert or replace into mirror_positions values (?,?,?,?)',(slug,side,str(mq),str(sq)));self.db.commit()
        else:raise RuntimeError('Simmer virtual trade rejected: '+str(data.get('error') or data.get('detail'))[:200])
        atomic_json(self.root/'simmer-requests.json',self.request_summary())

async def smoke(root):
    client=SimmerPaper(root)
    try:
        before=await client.status()
        markets=await client.get('/api/sdk/markets',{'q':'Bitcoin','status':'active','limit':100})
        atomic_json(Path(root)/'sim-markets.json',markets)
        rows=[m for m in markets.get('markets',[]) if m.get('sim_tradeable') is True and float(m.get('seconds_to_resolution') or 0)>600]
        if not rows:raise RuntimeError('no currently tradeable Bitcoin SIM market for connectivity check')
        m=rows[0];mid=m.get('id') or m['market_id'];atomic_json(Path(root)/'smoke-market.json',m)
        result=await client.trade('k14-smoke-v020-buy',mid,'yes','buy',amount=1,source='sdk:k14-connection-test',reason='Virtual-only API connectivity test, NOT a K14 strategy signal or performance observation')
        atomic_json(Path(root)/'smoke-buy.json',result)
        if result.get('success'):
            q=float(result.get('shares_bought',result.get('shares',0)))
            if q>0:
                sold=await client.trade('k14-smoke-v020-sell',mid,'yes','sell',shares=q,source='sdk:k14-connection-test',reason='Close virtual-only connectivity test position; excluded from K14 performance')
                atomic_json(Path(root)/'smoke-sell.json',sold)
        after=await client.status()
        summary={'buy_success':result.get('success') is True,'virtual_requests':len(client.request_summary()),'real_money_orders':0,'result_file':str(Path(root)/'simmer-status.json')}
        atomic_json(Path(root)/'smoke-summary.json',summary);return summary
    finally:await client.close()
