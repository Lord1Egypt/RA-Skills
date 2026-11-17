"""Frozen K14 entry -> receipt fence -> ParallelExit, with no transport or I/O.

One instance per account/session/market. The outer single-writer coordinator
owns ALL cash/risk reservations, persists state + commands atomically, and
decides whether sending is authorized. A LIVE provenance is not that consent.
"""
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256

from pm_predict.domain.money import D, ZERO, dec, floor_tick
from pm_predict.strategy.indicators import signal, fair_up
from pm_predict.strategy.exit_routes import evaluate_snapshot
from pm_predict.strategy.parallel_exit import ParallelExit, ExitOrder, ExitPolicy, Command, PROVENANCES


class TrialSession:
    def __init__(self, market, start_ms, thresholds, *, account_id, session_id, provenance, exit_policy=None):
        if not market or not account_id or not session_id or provenance not in PROVENANCES:
            raise ValueError('explicit market/account/session/receipt domain required')
        if start_ms % 900000 or thresholds.get('provisional') is not False:
            raise ValueError('requires aligned M15 window and final frozen thresholds')
        signal(0,thresholds,start_ms//1000)  # Validate month/K14/q without selecting a signal.
        self.market,self.start_ms=market,start_ms
        self.exit_policy=exit_policy or ExitPolicy()
        if not isinstance(self.exit_policy,ExitPolicy):raise ValueError('versioned ExitPolicy required')
        self.thresholds=deepcopy(thresholds)
        self.account_id,self.session_id,self.provenance=account_id,session_id,provenance
        self.lot_id=f'{session_id}:{market}'
        self.scope_id=sha256('\0'.join((provenance,account_id,self.lot_id)).encode()).hexdigest()[:32]
        self.now_ms=start_ms
        self.locked=False
        self.k=None
        self.side=None
        self.orders={}
        self.fills={}
        self.fee_events={}
        self.reconciliations={}
        self.command_seq=0
        self.last_quote_ms=-100000
        self.last_entry_book=None
        self.halted=None
        self.exit=None
        self.latest={}

    def _fail(self,message):
        self.halted=message
        raise ValueError(message)

    def entry_active(self):
        return next((o for o in self.orders.values() if o.final_qty is None),None)

    @property
    def entry_qty(self):return sum((x['qty'] for x in self.fills.values()),ZERO)

    @property
    def entry_gross(self):return sum((x['qty']*x['price'] for x in self.fills.values()),ZERO)

    @property
    def entry_fees(self):return sum((x['fee'] or ZERO for x in self.fills.values()),ZERO)

    @property
    def fee_pending(self):return [key for key,x in self.fills.items() if x['fee'] is None]

    def _cmd(self,kind,order,**kw):
        self.command_seq+=1
        return Command(f'EN-{self.scope_id}-{self.command_seq}',kind,self.market,order,
                       account_id=self.account_id,lot_id=self.lot_id,provenance=self.provenance,
                       paper_only=self.provenance!='LIVE_CONFIRMED',**kw)

    def _cancel(self,o,reason):
        if o.cancel_requested or o.final_qty is not None:return []
        o.cancel_requested=True;o.cancel_ms=self.now_ms;o.status='CANCEL_PENDING'
        return [self._cmd('CANCEL',o.id,reason=reason)]

    def ack(self,order):
        if order not in self.orders:return self.exit.ack(order)
        o=self.orders[order]
        if o.final_qty is None and o.status=='SENT':o.status='LIVE'

    def cancel_ack(self,order):
        if order not in self.orders:return self.exit.cancel_ack(order)
        if self.orders[order].final_qty is None:self.orders[order].status='CANCEL_ACK'

    def uncertain(self,order):
        if order not in self.orders:return self.exit.uncertain(order)
        if self.orders[order].final_qty is None:self.orders[order].status='UNKNOWN'

    def confirmed_fill(self,receipt_id,order,qty,price,paid_fee,*,provenance):
        if order not in self.orders:
            return self.exit.confirmed_fill(receipt_id,order,qty,price,paid_fee,provenance=provenance)
        q,p=dec(qty),dec(price)
        f=None if paid_fee is None else dec(paid_fee)
        data=dict(order=order,qty=q,price=p,fee=f,original_fee=f,provenance=provenance)
        if receipt_id in self.fills:
            old=self.fills[receipt_id]
            if any(old[k]!=data[k] for k in ('order','qty','price','original_fee','provenance')):self._fail('conflicting entry fill')
            return
        o=self.orders[order]
        if not receipt_id or receipt_id in self.fee_events or provenance!=self.provenance or o.final_qty is not None or self.exit:
            self._fail('entry receipt identity/provenance/fence mismatch')
        if q<=0 or not ZERO<p<=o.price or o.filled+q>o.qty or self.entry_qty+q>5 or (f is not None and f<0):
            self._fail('entry fill exceeds quantity/limit or has invalid fee')
        self.fills[receipt_id]=data;o.filled+=q

    def confirmed_fee(self,event_id,reference_receipt,paid_fee,*,provenance):
        if reference_receipt not in self.fills:
            if not self.exit:self._fail('unknown fee reference')
            return self.exit.confirmed_fee(event_id,reference_receipt,paid_fee,provenance=provenance)
        f=dec(paid_fee);payload=(reference_receipt,f,provenance)
        if event_id in self.fee_events:
            if self.fee_events[event_id]!=payload:self._fail('conflicting entry fee event')
            return
        if not event_id or event_id in self.fills or provenance!=self.provenance or f<0:self._fail('invalid entry fee')
        old=self.fills[reference_receipt]['fee']
        if old is not None and old!=f:self._fail('confirmed entry fee changed')
        if old is None and self.exit:self._fail('entry fee changed after handoff')
        self.fills[reference_receipt]['fee']=f
        self.fee_events[event_id]=payload

    def terminal(self,order,final_qty,*,fill_fence,proof_id=None,provenance=None):
        if order not in self.orders:
            return self.exit.terminal(order,final_qty,fill_fence=fill_fence,proof_id=proof_id,provenance=provenance)
        if self.provenance=='LIVE_CONFIRMED' and (not proof_id or provenance!=self.provenance):
            raise ValueError('live entry terminal needs authoritative proof')
        o=self.orders[order];q=dec(final_qty)
        if o.final_qty is not None:
            if o.final_qty!=q:self._fail('entry terminal changed')
            return
        if not fill_fence or q!=o.filled:
            o.status='UNKNOWN';return
        o.status='FINAL';o.final_qty=q;o.reserve=ZERO

    def reconcile_order(self,order,status,confirmed_filled,*,fill_fence,now_ms,proof_id,provenance):
        if order not in self.orders:
            return self.exit.reconcile_order(order,status,confirmed_filled,fill_fence=fill_fence,
                                            now_ms=now_ms,proof_id=proof_id,provenance=provenance)
        o=self.orders[order];q=dec(confirmed_filled);status=status.upper()
        payload=(order,status,q,bool(fill_fence),now_ms,provenance)
        if not proof_id or provenance!=self.provenance or status not in ('LIVE','FINAL','UNKNOWN'):
            self._fail('invalid entry reconciliation')
        if proof_id in self.reconciliations:
            if self.reconciliations[proof_id]!=payload:self._fail('conflicting entry proof')
            return o.final_qty is not None or o.status=='LIVE'
        if now_ms<max(o.last_reconciled_ms,o.sent_ms,o.cancel_ms or -1):return False
        self.reconciliations[proof_id]=payload;o.last_reconciled_ms=now_ms
        if o.final_qty is not None:
            if status!='FINAL' or q!=o.final_qty:self._fail('entry proof contradicts terminal state')
            return True
        if not fill_fence or q!=o.filled or status=='UNKNOWN':
            o.status='UNKNOWN';o.query_sent=False;o.last_query_ms=now_ms;return False
        if status=='FINAL':self.terminal(order,q,fill_fence=True,proof_id=proof_id,provenance=provenance)
        elif q<o.qty:
            o.status='LIVE';o.cancel_requested=False;o.cancel_ms=None;o.query_sent=False
        else:
            o.status='UNKNOWN';o.query_sent=False;o.last_query_ms=now_ms;return False
        return True

    def _handoff(self):
        if self.exit or self.entry_active() or not self.entry_qty or self.fee_pending or self.halted:return
        self.exit=ParallelExit(self.market,self.start_ms,self.side,self.entry_qty,self.entry_gross,
                              entry_receipt=f'ENTRY-{self.scope_id}',entry_terminal=True,provenance=self.provenance,
                              account_id=self.account_id,lot_id=self.lot_id,entry_fee=self.entry_fees,
                              policy=self.exit_policy)

    def step(self,snapshot,allowance,*,source_age_ms=0):
        now=snapshot.get('now_ms',0)
        if now<self.now_ms:self._fail('entry decision time moved backwards')
        self.now_ms=now
        self._handoff()
        if self.exit:return self.exit.step(snapshot,allowance,source_age_ms=source_age_ms)
        age=now-self.start_ms;o=self.entry_active()
        self.latest={'reason':None,'age_ms':age,'entry_qty':str(self.entry_qty),'fee_pending':self.fee_pending}
        if o and (age>=120000 or self.halted or self.fee_pending or not allowance.buying_allowed):
            commands=self._cancel(o,self.halted or 'entry deadline, unknown fee, or account disallows new buys')
            if commands:return commands
        if o and (o.status!='LIVE' or o.filled==o.qty):
            since=o.cancel_ms if o.cancel_ms is not None else o.sent_ms
            if now-since>2000 and (o.last_query_ms<0 or now-o.last_query_ms>2000):
                o.status='UNKNOWN';o.query_sent=True;o.last_query_ms=now
                return [self._cmd('RECONCILE',o.id,reason='entry receipt/fill fence unknown; reserve retained')]
        if age>=120000 or age<0 or self.halted:
            self.latest['reason']=self.halted or 'outside original 120s entry interval';return []
        m=snapshot.get('market') or {}
        signal_input=snapshot.get('paper',{}).get('signal') or {}
        gates=evaluate_snapshot({**snapshot,'paper':{'signal':signal_input}},ExitPolicy().routes(),source_age_ms=source_age_ms)['issues']
        if m.get('slug')!=self.market or m.get('start',-1)*1000!=self.start_ms:gates.append('wrong entry market/window')
        if not gates:
            try:
                value=float(signal_input['k14'])
                selected=signal(value,self.thresholds,self.start_ms//1000)
                if selected!=signal_input.get('side'):raise ValueError('signal side differs from frozen threshold calculation')
                if self.locked and (value!=self.k or selected!=self.side):raise ValueError('locked K14 changed inside window')
                if not self.locked:self.k,self.side,self.locked=value,selected,True
            except (KeyError,ValueError,TypeError) as ex:gates.append(str(ex))
        ptb=snapshot.get('ptb') or {};price=snapshot.get('price') or {};sigma=snapshot.get('sigma')
        if ptb.get('start',-1)*1000!=self.start_ms or ptb.get('source')!='PM_OFFICIAL_WEB_TWAP60':gates.append('official PTB mismatch/unknown')
        fair=None
        try:
            if not 0<=now-price['source_ms']+max(0,source_age_ms)<=2000:raise ValueError('BTC trade stale')
            fair=fair_up(float(price['price']),float(ptb['value']),float(sigma),900-age/1000)
            if fair is None:raise ValueError('fair value unavailable')
        except (KeyError,ValueError,TypeError,OverflowError) as ex:gates.append(str(ex))
        if gates:
            self.latest['reason']='; '.join(gates)
            return self._cancel(o,self.latest['reason']) if o else []
        if self.side is None:
            self.latest['reason']='K14 no signal';return []
        tick,minimum=dec(m['tick']),dec(m['min_qty'])
        if tick<=0 or tick>=1 or minimum<=0:self._fail('invalid market increments')
        own=snapshot['books'][self.side]
        bid=max(dec(p) for p,_ in own['bids']);ask=min(dec(p) for p,_ in own['asks'])
        f=dec(fair if self.side=='Up' else 1-fair)
        p=floor_tick(min(bid+tick,D('.48'),f+D('.02'),ask-tick),tick)
        self.latest.update(fair=str(f),proposal=str(p))
        if o:
            if o.status=='LIVE' and o.filled<o.qty:
                if o.price>f+D('.02'):return self._cancel(o,'fair value moved adversely')
                if len(self.orders)<7 and bid>o.price and p>o.price and now-self.last_quote_ms>=300:
                    return self._cancel(o,'outbid; reconcile before replacement')
            return []
        if self.entry_qty:
            self.latest['reason']='confirmed partial entry awaiting fees/handoff; no repeated entry';return []
        key=tuple((side,snapshot['books'][side].get('source_ms'),snapshot['books'][side].get('local_sequence')) for side in ('Up','Down'))
        if len(self.orders)>=7 or now-self.last_quote_ms<300 or key==self.last_entry_book:return []
        if p<D('.30') or D('5')<minimum or D('5')*p>allowance.available():
            self.latest['reason']='original entry price/minimum/shared account budget gate';return []
        oid=f'EO-{self.scope_id}-{len(self.orders)+1}'
        self.orders[oid]=ExitOrder(oid,'ENTRY',D('5'),p,now,reserve=D('5')*p)
        self.last_quote_ms,self.last_entry_book=now,key
        return [self._cmd('PLACE',oid,side=self.side,quantity='5',price=str(p),order_type='GTC',post_only=True,reason='ENTRY')]

    def merge_receipt(self,*args,**kwargs):return self.exit.merge_receipt(*args,**kwargs)
    def settle_receipt(self,*args,**kwargs):return self.exit.settle_receipt(*args,**kwargs)

    def checkpoint(self):
        return {'version':2,'exit_policy':self.exit_policy.checkpoint(),'market':self.market,'start_ms':self.start_ms,'thresholds':self.thresholds,
                'account_id':self.account_id,'session_id':self.session_id,'provenance':self.provenance,
                'meta':{k:getattr(self,k) for k in ('now_ms','locked','k','side','command_seq','last_quote_ms','last_entry_book','halted')},
                'orders':{k:asdict(v) for k,v in self.orders.items()},'fills':deepcopy(self.fills),
                'fee_events':deepcopy(self.fee_events),'reconciliations':deepcopy(self.reconciliations),
                'exit':self.exit.checkpoint() if self.exit else None}

    @classmethod
    def restore(cls,state):
        if state['version'] not in (1,2):raise ValueError('unsupported trial checkpoint')
        if state['version']==1 and 'exit_policy' in state:raise ValueError('legacy session cannot select a new policy')
        e=cls(state['market'],state['start_ms'],state['thresholds'],account_id=state['account_id'],session_id=state['session_id'],provenance=state['provenance'],
              exit_policy=ExitPolicy.restore(state['exit_policy']) if state['version']==2 else ExitPolicy())
        for k,v in state['meta'].items():
            if k not in ('now_ms','locked','k','side','command_seq','last_quote_ms','last_entry_book','halted'):raise ValueError('unexpected trial checkpoint field')
            if k=='last_entry_book' and v is not None:v=tuple(tuple(x) for x in v)
            setattr(e,k,v)
        for k,v in state['orders'].items():
            v=dict(v)
            for name in ('qty','price','reserve','filled','final_qty'):
                if v[name] is not None:v[name]=dec(v[name])
            e.orders[k]=ExitOrder(**v)
        for k,v in state['fills'].items():
            v=dict(v)
            for name in ('qty','price','fee','original_fee'):
                if v[name] is not None:v[name]=dec(v[name])
            e.fills[k]=v
        for k,v in state['fee_events'].items():v=list(v);v[1]=dec(v[1]);e.fee_events[k]=tuple(v)
        for k,v in state['reconciliations'].items():v=list(v);v[2]=dec(v[2]);e.reconciliations[k]=tuple(v)
        if state['exit']:e.exit=ParallelExit.restore(state['exit'])
        if e.exit and e.exit.policy!=e.exit_policy:raise ValueError('session/exit policy mismatch')
        if e.entry_active():
            e.entry_active().status='UNKNOWN';e.entry_active().query_sent=False;e.entry_active().last_query_ms=-1
        if e.entry_qty>5 or sum(o.final_qty is None for o in e.orders.values())>1 or (e.exit and e.entry_active()):
            raise ValueError('invalid restored entry inventory/ownership')
        return e

    def snapshot(self):
        o=self.entry_active()
        return {'market':self.market,'account_id':self.account_id,'session_id':self.session_id,'lot_id':self.lot_id,
                'exit_policy':self.exit_policy.checkpoint(),
                'provenance':self.provenance,'locked_k14':self.k,'side':self.side,'entry_qty':str(self.entry_qty),
                'entry_gross':str(self.entry_gross),'entry_known_fees':str(self.entry_fees),'fee_pending':self.fee_pending,
                'active_entry':o.id if o else None,'entry_cash_reserved':str(o.reserve if o else ZERO),
                'reason':self.latest,'halted':self.halted,'exit':self.exit.snapshot() if self.exit else None}
