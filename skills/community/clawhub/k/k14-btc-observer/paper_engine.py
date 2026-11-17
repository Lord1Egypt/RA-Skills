"""Complete frozen strategy with an explicitly hypothetical book-fill model.

No HTTP, API keys, wallets, or live order submission in this module.
Maker fills require a fresh later book to trade THROUGH our price, not touch.
This is a model assumption, not proof that a real queued order would fill.
"""
import bootstrap
from copy import deepcopy
from dataclasses import asdict
from types import SimpleNamespace
from common import D,dec,jsonable
from account import Account
from pm_predict.strategy.trial_session import TrialSession
from pm_predict.strategy.exit_policy import ExitPolicy
from pm_predict.strategy.exit_routes import evaluate_snapshot
from pm_predict.domain.money import fee

PROVENANCE='SIMMER_PAPER'
MODEL='LOCAL_HYPOTHETICAL_TRADE_THROUGH_V1'

class PaperEngine:
    def __init__(self,thresholds,state=None):
        self.thresholds=thresholds;self.account=Account();self.sessions={};self.pending={}
        self.events=[];self.seq=0;self.entry_windows=[];self.last_snapshot=None;self.markets={}
        self.day_losses={};self.total_losses=D('0');self.closed={}
        self.cfg=SimpleNamespace(daily_risk='6',total_risk='20')
        if state:
            if state['model']!=MODEL or state['thresholds']!=thresholds:raise ValueError('incompatible checkpoint')
            self.account=Account.restore(state['account'])
            self.sessions={k:TrialSession.restore(v) for k,v in state['sessions'].items()}
            self.pending=state['pending'];self.seq=state['seq'];self.entry_windows=state['entry_windows']
            self.day_losses={k:dec(v) for k,v in state['day_losses'].items()}
            self.total_losses=dec(state['total_losses']);self.closed=state['closed'];self.markets=state.get('markets',{})
            # No uncertain external exchange state exists in this LOCAL model.
            # On restart reconcile each model order against our durable pending map.
            for e in self.sessions.values():
                for o in self.orders(e).values():
                    if o.final_qty is None and o.id in self.pending:
                        e.reconcile_order(o.id,'LIVE',o.filled,fill_fence=True,now_ms=max(e.now_ms,o.sent_ms,o.cancel_ms or 0),proof_id='restore-'+o.id,provenance=PROVENANCE)

    @staticmethod
    def orders(e):return {**e.orders,**(e.exit.orders if e.exit else {})}
    def record(self,kind,**kw):
        self.seq+=1
        event={'id':f'paper-{self.seq:09d}','kind':kind,'receipt_origin':MODEL,**jsonable(kw)}
        self.events.append(event);return event['id']
    def terminal(self,e,oid):
        o=self.orders(e)[oid]
        e.terminal(oid,o.filled,fill_fence=True,proof_id='local-final-'+oid,provenance=PROVENANCE)
        self.pending.pop(oid,None)
    def fill(self,e,c,qty,price,taker,now):
        q,p=dec(qty),dec(price);f=fee(q,p) if taker else D('0')
        action='SELL' if c['reason'] in ('MAKER_SELL','SELL_FOK') else 'BUY'
        rid=self.record('FILL',market=e.market,market_tokens=self.markets.get(e.market,{}).get('tokens',{}),order=c['order'],action=action,side=c['side'],quantity=q,price=p,fee=f,now_ms=now,role='TAKER' if taker else 'MAKER',strategy_reason=c['reason'])
        e.confirmed_fill(rid,c['order'],q,p,f,provenance=PROVENANCE)
        self.account.fill(rid,action,q,p,f)

    def valid_book(self,s):
        return not evaluate_snapshot(s,ExitPolicy.continuous().routes())['issues']

    def match_resting(self,s):
        if not self.valid_book(s):return
        now=s['now_ms'];market=s['market']['slug'];e=self.sessions.get(market)
        if not e:return
        for oid,c in list(self.pending.items()):
            if c['market']!=market or now<c['eligible_ms'] or c['order_type']!='GTC':continue
            # Orders expire at strategy deadlines even if a crossed book arrives later.
            if now>=e.start_ms+(120000 if c['reason']=='ENTRY' else 900000):continue
            b=s['books'][c['side']]
            if b.get('local_sequence')==c.get('book_sequence') or b.get('source_ms',0)<=c['placed_source_ms']:continue
            buy=c['reason']=='ENTRY';p=dec(c['price']);o=self.orders(e)[oid]
            levels=b['asks'] if buy else b['bids']
            eligible_levels=[(str(price),str(q)) for price,q in levels if (dec(price)<p if buy else dec(price)>p)]
            # Unrelated WS ticks must not repeatedly consume the same displayed size.
            if eligible_levels==[tuple(x) for x in c.get('consumed_levels',[])]:continue
            available=sum((dec(q) for price,q in levels if (dec(price)<p if buy else dec(price)>p)),D('0'))
            q=min(o.qty-o.filled,available)
            c['book_sequence']=b.get('local_sequence');c['placed_source_ms']=b.get('source_ms',0)
            if q>0:
                c['consumed_levels']=eligible_levels
                self.fill(e,c,q,p,False,now)
                if o.filled==o.qty:self.terminal(e,oid)

    def execute(self,e,command,s):
        c=jsonable(asdict(command));self.record('COMMAND',now_ms=s['now_ms'],command=c,command_kind=c['kind'],market=e.market)
        oid=c['order'];now=s['now_ms'];o=self.orders(e).get(oid)
        if c['kind'] in ('CANCEL','RECONCILE'):
            if o and o.final_qty is None:
                if c['kind']=='CANCEL':e.cancel_ack(oid);self.terminal(e,oid)
                elif oid in self.pending:
                    e.reconcile_order(oid,'LIVE',o.filled,fill_fence=True,now_ms=now,proof_id=f'local-proof-{self.seq}',provenance=PROVENANCE)
                else:self.terminal(e,oid)
            return
        if c['kind']=='MERGE':
            q=dec(c['quantity']);f=q*D('.00001')
            rid=self.record('MERGE',market=e.market,quantity=q,gross=q,fee=f,now_ms=now)
            e.merge_receipt(rid,oid,success=True,paid_fee=f,provenance=PROVENANCE)
            self.account.settlement(rid,q,f);return
        if c['kind']!='PLACE':raise ValueError('unsupported strategy command '+c['kind'])
        e.ack(oid);b=s['books'][c['side']];p=dec(c['price']);buy=c['reason'] in ('ENTRY','PAIR_FOK')
        if c['post_only']:
            crossing=min(dec(x[0]) for x in b['asks'])<=p if buy else max(dec(x[0]) for x in b['bids'])>=p
            if crossing:
                self.record('REJECT',market=e.market,order=oid,reason='post_only_would_cross',now_ms=now);self.terminal(e,oid);return
            self.pending[oid]={**c,'eligible_ms':now+250,'placed_source_ms':b['source_ms'],'book_sequence':b.get('local_sequence')}
            return
        if c['order_type']!='FOK':raise ValueError('unsupported immediate order type')
        # All-or-none simulation at visible depth. Fee model stays frozen.
        levels=sorted([(dec(p0),dec(q0)) for p0,q0 in (b['asks'] if buy else b['bids'])],reverse=not buy)
        left=dec(c['quantity']);fills=[]
        for p0,q0 in levels:
            if (buy and p0>p) or (not buy and p0<p):continue
            take=min(left,q0);fills.append((take,p0));left-=take
            if not left:break
        if not left:
            for q0,p0 in fills:self.fill(e,c,q0,p0,True,now)
        else:self.record('REJECT',market=e.market,order=oid,reason='fok_not_filled',now_ms=now)
        self.terminal(e,oid)

    def step(self,s,*,timer=False):
        self.events=[];s=deepcopy(s);self.last_snapshot=s
        now=s['now_ms'];m=s.get('market') or {};slug=m.get('slug')
        if slug:self.markets[slug]=m
        if not timer:self.match_resting(s)
        sig=s.get('paper',{}).get('signal') or {}
        if slug not in self.sessions and sig.get('side') in ('Up','Down') and 0<=now-m.get('start',0)*1000<120000 and not timer:
            if len(self.entry_windows)<1:
                self.sessions[slug]=TrialSession(slug,m['start']*1000,self.thresholds,account_id='k14-paper-50-v020',session_id='paper-20261029',provenance=PROVENANCE,exit_policy=ExitPolicy.continuous())
        for market,e in self.sessions.items():
            if now<e.now_ms:continue
            snapshot=s
            if market!=slug or timer:
                # Timers only expire/cancel/reconcile. Never authorize new fills or orders.
                snapshot={**s,'health':{'status':'DEGRADED','reasons':['timer/other window; no new orders']}}
            used=bool(self.entry_windows and market not in self.entry_windows)
            allowance=self.account.allowance(e,self.cfg,buying_allowed=not used and not timer)
            for c in e.step(snapshot,allowance):
                if c.kind=='PLACE' and timer:raise RuntimeError('timer attempted placement')
                if c.reason=='ENTRY' and market not in self.entry_windows:self.entry_windows.append(market)
                self.execute(e,c,snapshot)
            self.mark_closed(e)
        return self.events

    def mark_closed(self,e):
        if e.market in self.closed or not e.exit or e.exit.own or e.exit.other:return
        pnl=e.exit.realized;day=str(e.start_ms//86400000);loss=max(D('0'),-pnl)
        self.closed[e.market]=str(pnl);self.total_losses+=loss;self.day_losses[day]=self.day_losses.get(day,D('0'))+loss
        self.record('LOT_CLOSED',market=e.market,net_pnl=pnl,now_ms=e.now_ms)

    def settle(self,market,winner,now,proof):
        self.events=[];e=self.sessions.get(market)
        if not e or not e.exit or e.exit.settled:return []
        if not proof or proof.get('official') is not True:raise ValueError('official resolution proof required')
        if now<e.start_ms+900000:raise ValueError('cannot settle before expiry')
        e.now_ms=now;e.exit.now_ms=now
        if e.exit.active():return []
        q=e.exit.own if winner==e.side else e.exit.other
        rid=self.record('REDEEM',market=market,winner=winner,gross=q,fee='0',now_ms=now,proof=proof)
        e.settle_receipt(rid,winner,net_payout=q,provenance=PROVENANCE)
        self.account.settlement(rid,q,0);self.mark_closed(e);return self.events

    def checkpoint(self):
        return jsonable({'version':1,'model':MODEL,'thresholds':self.thresholds,'account':self.account.checkpoint(),'sessions':{k:e.checkpoint() for k,e in self.sessions.items()},'pending':self.pending,'seq':self.seq,'entry_windows':self.entry_windows,'closed':self.closed,'day_losses':self.day_losses,'total_losses':self.total_losses,'markets':self.markets})
    def report(self):
        all_closed=bool(self.entry_windows) and all(k in self.closed for k in self.entry_windows)
        return {'mode':'FULL_STRATEGY_PAPER','model':MODEL,'principal':'50','cash':self.account.cash,'buy_gross':self.account.buy_gross,'sell_gross':self.account.sell_gross,'modeled_fees':str(dec(self.account.exchange_fees)+dec(self.account.settlement_fees)),'merge_redeem_gross':self.account.settlement_gross,'net_realized_pnl':str(dec(self.account.cash)-50) if all_closed else None,'real_money_orders':0,'entry_windows':self.entry_windows,'pending_orders':len(self.pending),'sessions':{k:e.snapshot() for k,e in self.sessions.items()},'limitations':['Model fills are hypothetical; public books do not prove real Maker fills.','Fee model and Merge reserve are assumptions, not actual charges.','Simmer LMSR mirror receipts are kept separately from this ledger.'],'event_count':self.seq}
