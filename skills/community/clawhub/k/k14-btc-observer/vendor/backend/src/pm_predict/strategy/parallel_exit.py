"""Receipt-driven paper exit policy. No network, UI, clock, or account credentials.

Three concurrent policies share ONE order/position owner. Commands are durable-
outbox inputs for a future broker, not receipts. The current public collector
does not instantiate this policy. Unknown receipts never manufacture inventory.
"""
from dataclasses import dataclass, asdict
from copy import deepcopy
from hashlib import sha256

from pm_predict.domain.money import D, ZERO, dec, fee
from pm_predict.strategy.exit_routes import compare_routes, evaluate_snapshot
from pm_predict.strategy.exit_policy import ExitPolicy

PROVENANCES = ('SYNTHETIC_TEST', 'SIMMER_PAPER', 'LIVE_CONFIRMED')
_UNSET = object()


@dataclass(frozen=True)
class Command:
    id: str
    kind: str
    market: str
    order: str
    side: str | None = None
    quantity: str | None = None
    price: str | None = None
    order_type: str | None = None
    post_only: bool = False
    reason: str = ''
    paper_only: bool = True
    account_id: str = 'paper-default'
    lot_id: str = ''
    provenance: str = 'SYNTHETIC_TEST'


@dataclass
class ExitOrder:
    id: str
    kind: str
    qty: D
    price: D
    sent_ms: int
    reserve: D = ZERO
    filled: D = ZERO
    status: str = 'SENT'
    cancel_ms: int | None = None
    final_qty: D | None = None
    query_sent: bool = False
    last_query_ms: int = -1
    last_reconciled_ms: int = -1
    cancel_requested: bool = False


@dataclass(frozen=True)
class AccountAllowance:
    """Shared account coordinator must issue this, including OTHER windows.

    Values are spendable cash and remaining risk after all existing holdings,
    reserves and realized losses. Local single-lot checks supplement them.
    This is not permission to create a new 60 USD account for every position.
    """
    cash: D
    daily_risk: D
    total_risk: D
    buying_allowed: bool = True

    def available(self):
        return max(ZERO, min(dec(self.cash), dec(self.daily_risk), dec(self.total_risk))) if self.buying_allowed else ZERO


class ParallelExit:
    """Manage one final-reconciled entry lot, with normalized paper receipts.

    The account coordinator owns K14/entry and portfolio limits. A new instance
    is not a new trading epoch. Never seed this from a public-book price touch.
    """
    def __init__(self, market, start_ms, side, qty, entry_cost, *,
                 entry_receipt, entry_terminal, provenance, policy=None,
                 account_id=None, lot_id=None, entry_fee=_UNSET):
        if provenance not in PROVENANCES or not entry_terminal or not entry_receipt:
            raise ValueError('requires identified, final-reconciled entry receipt')
        if provenance == 'LIVE_CONFIRMED' and (not account_id or not lot_id or entry_fee is _UNSET):
            raise ValueError('live receipt domain requires explicit account, lot and entry fee (None means unknown)')
        self.account_id=account_id or 'paper-default'
        self.lot_id=lot_id or str(entry_receipt)
        identity='\0'.join((provenance,self.account_id,str(market),str(self.lot_id)))
        self.scope_id=sha256(identity.encode()).hexdigest()[:32]
        entry_fee=ZERO if entry_fee is _UNSET else None if entry_fee is None else dec(entry_fee)
        if entry_fee is not None and entry_fee < ZERO:
            raise ValueError('negative entry fee')
        q, c = dec(qty), dec(entry_cost)
        if side not in ('Up', 'Down') or not ZERO < q <= 5 or not ZERO < c <= q * D('.48'):
            raise ValueError('entry quantity/cost exceeds frozen maker-entry limits')
        self.market, self.start_ms, self.side = market, start_ms, side
        self.entry_receipt, self.provenance = entry_receipt, provenance
        self.policy = policy or ExitPolicy()
        if not isinstance(self.policy, ExitPolicy):
            raise ValueError('versioned ExitPolicy required')
        self.last_submit_book = None
        self.own, self.own_cost = q, c+(entry_fee or ZERO)
        self.other, self.other_cost = ZERO, ZERO
        self.initial_gross_cost = c
        self.initial_cost = self.own_cost
        self.initial_entry_fee=entry_fee
        self.initial_qty = q
        self.net_cashflow = -self.own_cost  # Known cash only while fee_pending.
        self.realized = ZERO
        self.orders: dict[str, ExitOrder] = {}
        self.receipts: dict[str, tuple] = {}
        self.fees = {str(entry_receipt):{'target':'OWN','amount':entry_fee,'estimate':ZERO}}
        self.reconciliations = {}
        self.command_seq = 0
        self.now_ms = start_ms
        self.pair_attempts = 0
        self.last_pair_ms = -100000
        self.last_pair_book = None
        self.last_sell_book = None
        self.last_replace_ms = -100000
        self.halted = None
        self.merge_failed = False
        self.settled = False
        self.latest = {}

    def active(self):
        return next((o for o in self.orders.values() if o.final_qty is None), None)

    def _command(self, kind, order, **kw):
        self.command_seq += 1
        return Command(f'EX-{self.scope_id}-{self.command_seq}', kind, self.market, order,
                       account_id=self.account_id,lot_id=self.lot_id,provenance=self.provenance,
                       paper_only=self.provenance != 'LIVE_CONFIRMED', **kw)

    def _send(self, kind, q, p, now):
        if self.active():
            raise ValueError('one resource owner: cancel/reconcile before another exit')
        oid = f'XO-{self.scope_id}-{len(self.orders)+1}'
        reserve = q*p + fee(q,p) + q*D('.00001') if kind == 'PAIR_FOK' else q*D('.00001') if kind == 'MERGE' else ZERO
        self.orders[oid] = ExitOrder(oid, kind, q, p, now, reserve=reserve)
        side = ('Down' if self.side == 'Up' else 'Up') if kind == 'PAIR_FOK' else self.side
        if kind == 'MERGE':
            return self._command('MERGE', oid, quantity=str(q), reason='both legs confirmed; wait for merge confirmation')
        return self._command('PLACE', oid, side=side, quantity=str(q), price=str(p),
                             order_type='GTC' if kind == 'MAKER_SELL' else 'FOK',
                             post_only=kind == 'MAKER_SELL', reason=kind)

    def _cancel(self, o, now, reason):
        if o.kind != 'MAKER_SELL' or o.final_qty is not None or o.cancel_requested:
            return []
        o.status, o.cancel_ms = 'CANCEL_PENDING', now
        o.cancel_requested=True
        return [self._command('CANCEL', o.id, reason=reason)]

    def ack(self, order):
        o = self.orders[order]
        if o.final_qty is None and o.status == 'SENT':
            o.status = 'LIVE'

    def cancel_ack(self, order):
        o = self.orders[order]
        if o.final_qty is None:
            o.status = 'CANCEL_ACK'  # Still locked: cancellation reply is not a fill fence.

    def uncertain(self, order):
        o = self.orders[order]
        if o.final_qty is None:
            o.status = 'UNKNOWN'

    def reconcile_order(self, order, status, confirmed_filled, *, fill_fence,
                        now_ms, proof_id, provenance):
        """Authoritative order state plus complete confirmed trades at that fence.

        LIVE is not an ACK. The adapter must match account/lot/exchange identity,
        quantity, limit and completed trade history before setting fill_fence.
        A missing order or cancellation HTTP success cannot set FINAL.
        """
        o=self.orders[order]
        q=dec(confirmed_filled)
        status=str(status).upper()
        payload=(order,status,q,bool(fill_fence),now_ms,provenance)
        if not proof_id or provenance != self.provenance or status not in ('LIVE','FINAL','UNKNOWN'):
            self._fail('invalid order reconciliation proof')
        if proof_id in self.reconciliations:
            if self.reconciliations[proof_id] != payload:self._fail('conflicting reconciliation proof')
            return o.final_qty is not None or o.status=='LIVE'
        if now_ms < max(o.last_reconciled_ms,o.sent_ms,o.cancel_ms or -1):
            return False  # Delayed stale query cannot overwrite a newer cancel.
        self.reconciliations[proof_id]=payload
        o.last_reconciled_ms=now_ms
        if o.final_qty is not None:
            if status != 'FINAL' or q != o.final_qty:self._fail('reconciliation contradicts terminal order')
            return True
        if not fill_fence or q != o.filled or status=='UNKNOWN':
            o.status='UNKNOWN'
            o.query_sent=False
            o.last_query_ms=now_ms
            return False
        if status=='FINAL':
            self.terminal(order,q,fill_fence=True,proof_id=proof_id,provenance=provenance)
        elif o.kind=='MAKER_SELL' and q < o.qty:
            o.status='LIVE'
            o.cancel_requested=False
            o.cancel_ms=None
            o.query_sent=False
        else:
            o.status='UNKNOWN'
            o.query_sent=False
            o.last_query_ms=now_ms
            return False
        return True

    def _fail(self, reason):
        self.halted = reason
        raise ValueError(reason)

    def confirmed_fill(self, receipt_id, order, qty, price, paid_fee, *, provenance):
        """Apply confirmed fill once; MATCHED/accepted is not confirmation."""
        q, p, f = dec(qty), dec(price), None if paid_fee is None else dec(paid_fee)
        payload = (order, q, p, f, provenance)
        if receipt_id in self.receipts:
            if self.receipts[receipt_id] != payload:
                self._fail('conflicting duplicate receipt')
            return
        o = self.orders[order]
        if provenance != self.provenance or not receipt_id or receipt_id in self.fees or o.final_qty is not None or o.kind == 'MERGE':
            self._fail('receipt provenance/final fence mismatch')
        if q <= 0 or not ZERO < p < 1 or o.filled+q > o.qty:
            self._fail('invalid confirmed fill size/price')
        expected_fee = ZERO if o.kind == 'MAKER_SELL' else fee(q,p)
        if (f is not None and f < ZERO) or (o.kind == 'PAIR_FOK' and p > o.price) or (o.kind != 'PAIR_FOK' and p < o.price):
            self._fail('fill contradicts limit or has negative fee')
        # Actual fees may differ from the model (e.g. split-fill rounding).
        known_fee=f or ZERO
        if o.kind == 'PAIR_FOK':
            if self.other+q > self.own:
                self._fail('confirmed hedge exceeds remaining original shares')
            self.other += q
            self.other_cost += q*p+known_fee
            self.net_cashflow -= q*p+known_fee
        else:
            if q > self.own-self.other:
                self._fail('sell would consume paired or unavailable shares')
            basis = self.own_cost/self.own
            self.own -= q
            self.own_cost -= q*basis
            self.net_cashflow += q*p-known_fee
            self.realized += q*p-known_fee-q*basis
        o.filled += q
        self.receipts[receipt_id] = payload
        self.fees[receipt_id]={'target':'OTHER' if o.kind=='PAIR_FOK' else 'REALIZED',
                              'amount':f,'estimate':expected_fee}
        # Even a full fill waits for normalized terminal reconciliation.
        self.check()

    def terminal(self, order, final_qty, *, fill_fence, proof_id=None, provenance=None):
        if self.provenance=='LIVE_CONFIRMED' and (not proof_id or provenance != self.provenance):
            raise ValueError('live terminal requires an explicit authoritative reconciliation proof')
        o = self.orders[order]
        q = dec(final_qty)
        if o.final_qty is not None:
            if q != o.final_qty:
                self._fail('terminal total changed')
            return
        if not fill_fence or q != o.filled or o.kind == 'MERGE':
            o.status = 'UNKNOWN'
            return
        o.final_qty, o.status = q, 'FINAL'
        o.reserve = ZERO
        if o.kind in ('SELL_FOK','PAIR_FOK') and q not in (ZERO,o.qty):
            self.halted = 'partial FOK protocol violation; keep confirmed residual inventory for reconciliation'
        self.check()

    @property
    def fee_pending(self):
        return [key for key,value in self.fees.items() if value['amount'] is None]

    def confirmed_fee(self, event_id, reference_receipt, paid_fee, *, provenance):
        """Resolve an unknown USD fee with a distinct, identified fee receipt."""
        f=dec(paid_fee)
        payload=('FEE',reference_receipt,f,provenance)
        if event_id in self.receipts:
            if self.receipts[event_id] != payload:self._fail('conflicting fee receipt')
            return
        if not event_id or event_id in self.fees or provenance != self.provenance or f < 0 or reference_receipt not in self.fees:
            self._fail('invalid fee receipt')
        item=self.fees[reference_receipt]
        if item['amount'] is not None:
            if item['amount'] != f:self._fail('fee differs from previously confirmed amount')
        else:
            target=item['target']
            if target=='OWN':
                if self.own != self.initial_qty:self._fail('entry fee resolved after inventory disposal')
                self.own_cost+=f
            elif target=='OTHER':
                if not self.other:self._fail('hedge fee resolved after hedge inventory disposal')
                self.other_cost+=f
            else:self.realized-=f
            self.net_cashflow-=f
            item['amount']=f
        self.receipts[event_id]=payload
        self.check()

    def merge_receipt(self, receipt_id, order, *, success, paid_fee, provenance):
        o = self.orders[order]
        f = None if paid_fee is None else dec(paid_fee)
        payload = ('MERGE', order, success, f, provenance)
        if receipt_id in self.receipts:
            if self.receipts[receipt_id] != payload:
                self._fail('conflicting merge receipt')
            return
        if o.kind != 'MERGE' or o.final_qty is not None or provenance != self.provenance or not receipt_id or receipt_id in self.fees:
            self._fail('invalid merge receipt')
        if f is not None and f < 0:
            self._fail('negative merge fee')
        if success:
            q = o.qty
            if q > min(self.own,self.other):
                self._fail('merge consumes unavailable shares')
            basis = self.own_cost/self.own + self.other_cost/self.other
            self.own_cost -= q*self.own_cost/self.own
            self.other_cost -= q*self.other_cost/self.other
            self.own -= q
            self.other -= q
            self.net_cashflow += q-(f or ZERO)
            self.realized += q-(f or ZERO)-q*basis
        else:
            # Both positions stay held; failed chain fees still cost money.
            self.net_cashflow -= f or ZERO
            self.realized -= f or ZERO
            self.merge_failed = True
        o.final_qty, o.status = o.qty if success else ZERO, 'FINAL'
        o.reserve=ZERO
        self.receipts[receipt_id] = payload
        self.fees[receipt_id]={'target':'REALIZED','amount':f,'estimate':o.qty*D('.00001')}
        self.check()

    def settle_receipt(self, receipt_id, winner, *, net_payout, provenance):
        """Explicit paper settlement receipt, never inferred from Binance."""
        payout = dec(net_payout)
        payload = ('SETTLE', winner, payout, provenance)
        if receipt_id in self.receipts:
            if self.receipts[receipt_id] != payload:
                self._fail('conflicting settlement receipt')
            return
        if self.settled or self.active() or self.now_ms < self.start_ms+900000 or provenance != self.provenance or winner not in ('Up','Down') or not receipt_id:
            self._fail('settlement not reconciled/too early')
        gross = self.own if winner == self.side else self.other
        if not ZERO <= payout <= gross:
            self._fail('invalid settlement payout')
        self.net_cashflow += payout
        self.realized += payout-self.own_cost-self.other_cost
        self.own = self.other = self.own_cost = self.other_cost = ZERO
        self.settled = True
        self.receipts[receipt_id] = payload
        self.check()

    def check(self):
        if min(self.own,self.other,self.own_cost,self.other_cost) < 0 or self.other > self.own:
            self._fail('negative/overhedged inventory')
        if sum(o.final_qty is None for o in self.orders.values()) > 1:
            self._fail('multiple owners of the same inventory')
        if not self.own and not self.other and self.net_cashflow != self.realized:
            self._fail('closed-lot accounting mismatch')

    def step(self, snapshot, allowance: AccountAllowance, *, source_age_ms=0):
        """Call on each book/receipt/timer event; no one-second polling assumption.

        All routes are evaluated each call. At most one mutating command is
        returned. The executor must persist command/state before sending it and
        atomically recheck shared account allowances (not just this lot).
        """
        now = snapshot.get('now_ms',0)
        if now < self.now_ms:
            self._fail('decision clock moved backwards')
        self.now_ms = now
        age = now-self.start_ms
        o = self.active()
        self.latest = {'sell_monitor':True,'pair_monitor':True,'wait_guard':True,
                       'age_ms':age,'deadline_reached':age>=840000,
                       'profile':self.policy.profile,
                       'profit_target_per_share':str(self.policy.target(age)),
                       'pair_attempts':self.pair_attempts,'routes':None,'reason':None}
        # An UNKNOWN/restored GTC can still be live on the exchange. At a hard
        # stop request cancellation by its stable client/exchange mapping first;
        # retain the lock until a terminal fill fence arrives.
        if o and (age >= 900000 or self.halted or self.fee_pending):
            reason=self.halted or ('fee amount unknown; reconcile actual charges' if self.fee_pending else 'window ended; cancel then reconcile')
            commands=self._cancel(o,now,reason)
            if commands:
                self.latest['reason']=reason
                return commands
        # Receipt uncertainty takes priority even after a market rollover.
        if o:
            waiting = o.cancel_ms if o.cancel_ms is not None else o.sent_ms
            if o.status in ('SENT','CANCEL_PENDING','CANCEL_ACK','UNKNOWN') or o.kind in ('SELL_FOK','PAIR_FOK','MERGE'):
                if now-waiting > self.policy.receipt_timeout_ms and (o.last_query_ms < 0 or now-o.last_query_ms > self.policy.receipt_timeout_ms):
                    o.status, o.query_sent = 'UNKNOWN', True
                    o.last_query_ms=now
                    self.latest['reason']='receipt unknown; locked shares and cash retained'
                    return [self._command('RECONCILE',o.id,reason=self.latest['reason'])]
        market = snapshot.get('market') or {}
        matched_market = market.get('slug') == self.market and market.get('start',-1)*1000 == self.start_ms
        gate_input = {**snapshot,'paper':{'signal':snapshot.get('paper',{}).get('signal',{})}}
        issues = evaluate_snapshot(gate_input,self.policy.routes(),source_age_ms=source_age_ms)['issues']
        if not matched_market:
            issues.append('snapshot belongs to another market')
        # Public intent ambiguity is irrelevant: this policy uses reconciled own
        # receipts. Other gate failures remain; caller supplies an input-only copy.
        if age >= 900000 or self.halted or issues or self.fee_pending:
            self.latest['reason']=self.halted or ('window ended; settlement pending' if age>=900000 else 'fees unresolved; known cash is not net profit' if self.fee_pending else '; '.join(issues))
            return self._cancel(o,now,self.latest['reason']) if o else []
        if self.settled or not self.own:
            self.latest['reason']='lot closed'
            return []
        if self.merge_failed:
            self.latest['reason']='merge failed; hold paired inventory for official settlement'
            return []
        if not o and self.other:
            if dec(allowance.cash) < min(self.own,self.other)*D('.00001'):
                self.latest['reason']='merge cash allowance insufficient; retain both legs'
                return []
            return [self._send('MERGE',min(self.own,self.other),ZERO,now)]
        remaining = self.own-self.other
        if remaining <= 0:
            self.latest['reason']='paired inventory locked pending receipt'
            return []
        # Enforce both account-wide allowances and the unchanged 6/20 local caps.
        remaining_risk = min(D('6'),D('20'))-self.own_cost-self.other_cost-max(ZERO,-self.realized)
        funds = max(ZERO,min(allowance.available(),remaining_risk))
        data = deepcopy(snapshot)
        data['paper']={'account':{'cash':str(funds),'reserved':'0'}}
        routes = compare_routes(data,self.side,remaining,self.own_cost/self.own,self.policy.routes())
        routes = self.policy.price_routes(routes,data,self.side,remaining,self.own_cost/self.own,age)
        self.latest['routes']=routes
        book_key=tuple((side,snapshot['books'][side].get('source_ms'),snapshot['books'][side].get('local_sequence')) for side in ('Up','Down'))
        continuous=self.policy.is_continuous
        placements=[x for x in self.orders.values() if x.kind in ('PAIR_FOK','SELL_FOK','MAKER_SELL')]
        cadence_ok=(not continuous or ((not placements or now-placements[-1].sent_ms>=self.policy.retry_ms)
                                      and book_key!=self.last_submit_book))
        retry_ok = (self.policy.max_pair_attempts is None or self.pair_attempts < self.policy.max_pair_attempts) and now-self.last_pair_ms >= self.policy.retry_ms and book_key != self.last_pair_book and cadence_ok
        pair_ok = routes['pair']['eligible'] and retry_ok
        sell_attempts=[x for x in self.orders.values() if x.kind=='SELL_FOK']
        sell_retry_ok=((continuous or len(sell_attempts)<3) and cadence_ok and book_key != self.last_sell_book and
                       (not sell_attempts or now-sell_attempts[-1].sent_ms >= self.policy.retry_ms))
        direct_ok = routes['sell']['eligible'] and sell_retry_ok
        route = ('SELL_FOK' if direct_ok and (not pair_ok or routes['sell']['net_at_limit']>=routes['pair']['net_at_limit'])
                 else 'PAIR_FOK' if pair_ok else 'MAKER_SELL')
        if o:
            if o.kind == 'MAKER_SELL' and o.status == 'LIVE':
                if route != 'MAKER_SELL':
                    return self._cancel(o,now,'better immediate route; wait for terminal fill fence, then reprice')
                proposal=routes['sell']['maker_ask_proposal']
                can_replace=continuous or sum(x.kind=='MAKER_SELL' for x in self.orders.values()) < 7
                quote_change_ok=(not continuous or (cadence_ok and now-o.sent_ms>=15000 and
                                 proposal is not None and abs(proposal-o.price)>=2*dec(market['tick'])))
                if can_replace and quote_change_ok and proposal is not None and proposal != o.price and now-self.last_replace_ms >= self.policy.retry_ms:
                    self.last_replace_ms=now
                    return self._cancel(o,now,'refresh maker quote without crossing cost floor')
            self.latest['reason']='resting sell maintained; pair and timer monitors remain active' if o.kind=='MAKER_SELL' else 'await receipt; no duplicate mutation'
            return []
        if route == 'PAIR_FOK':
            self.pair_attempts+=1
            self.last_pair_ms,self.last_pair_book=now,book_key
            self.last_submit_book=book_key
            return [self._send(route,remaining,routes['pair']['limit_price'],now)]
        if route == 'SELL_FOK':
            self.last_sell_book=book_key
            self.last_submit_book=book_key
            return [self._send(route,remaining,routes['sell']['limit_price'],now)]
        p=routes['sell']['maker_ask_proposal']
        maker_orders=[x for x in self.orders.values() if x.kind=='MAKER_SELL']
        if continuous and (not cadence_ok or routes['sell']['eligible'] or routes['pair']['eligible']):
            self.latest['reason']='wait for fresh book/cooldown; do not create a sell only to immediately cancel it'
            return []
        if p is not None and (continuous or len(maker_orders)<7) and (not maker_orders or now-maker_orders[-1].sent_ms>=self.policy.retry_ms):
            self.last_submit_book=book_key
            return [self._send('MAKER_SELL',remaining,p,now)]
        self.latest['reason']='maker retry/quantity/cooldown limit; wait without increasing inventory'
        return []

    def checkpoint(self):
        """JSON-compatible when encoded with default=str; persist with outbox atomically."""
        return {'version':3,'policy':self.policy.checkpoint(),'market':self.market,'start_ms':self.start_ms,'side':self.side,
                'entry_receipt':self.entry_receipt,'provenance':self.provenance,
                'account_id':self.account_id,'lot_id':self.lot_id,
                'initial_qty':str(self.initial_qty),'initial_cost':str(self.initial_cost),
                'initial_gross_cost':str(self.initial_gross_cost),
                'initial_entry_fee':None if self.initial_entry_fee is None else str(self.initial_entry_fee),
                'amounts':{k:str(getattr(self,k)) for k in ('own','own_cost','other','other_cost','net_cashflow','realized')},
                'orders':{k:asdict(v) for k,v in self.orders.items()},
                'receipts':{k:[str(v) if isinstance(v,D) else v for v in p] for k,p in self.receipts.items()},
                'fees':{k:{**v,'amount':None if v['amount'] is None else str(v['amount']),'estimate':str(v['estimate'])} for k,v in self.fees.items()},
                'reconciliations':{k:[str(v) if isinstance(v,D) else v for v in p] for k,p in self.reconciliations.items()},
                'meta':{k:getattr(self,k) for k in ('command_seq','now_ms','pair_attempts','last_pair_ms','last_pair_book','last_sell_book','last_submit_book','last_replace_ms','halted','merge_failed','settled')}}

    @classmethod
    def restore(cls, state):
        if state['version'] not in (1,2,3):
            raise ValueError('unsupported checkpoint')
        if state['version']<3 and 'policy' in state:
            raise ValueError('legacy checkpoint cannot select a new policy')
        if state['version']==3 and 'last_submit_book' not in state['meta']:
            raise ValueError('missing submission cadence checkpoint')
        e=cls(state['market'],state['start_ms'],state['side'],state['initial_qty'],state.get('initial_gross_cost',state['initial_cost']),
              entry_receipt=state['entry_receipt'],entry_terminal=True,provenance=state['provenance'],
              account_id=state.get('account_id'),lot_id=state.get('lot_id'),entry_fee=state.get('initial_entry_fee','0'),
              policy=ExitPolicy.restore(state['policy']) if state['version']==3 else ExitPolicy())
        for k,v in state['amounts'].items():
            if k not in ('own','own_cost','other','other_cost','net_cashflow','realized'):
                raise ValueError('unexpected amount field')
            setattr(e,k,dec(v))
        for k,v in state['orders'].items():
            v=dict(v)
            for name in ('qty','price','reserve','filled','final_qty'):
                if v[name] is not None:v[name]=dec(v[name])
            e.orders[k]=ExitOrder(**v)
        for k,p in state['receipts'].items():
            p=list(p)
            indices=(3,) if p[0]=='MERGE' else (2,) if p[0] in ('SETTLE','FEE') else (1,2,3)
            for i in indices:
                if p[i] is not None:p[i]=dec(p[i])
            e.receipts[k]=tuple(p)
        for k,v in state.get('fees',{}).items():
            e.fees[k]={**v,'amount':None if v['amount'] is None else dec(v['amount']),'estimate':dec(v['estimate'])}
        for k,v in state.get('reconciliations',{}).items():
            v=list(v);v[2]=dec(v[2]);e.reconciliations[k]=tuple(v)
        for k,v in state['meta'].items():
            if k not in ('command_seq','now_ms','pair_attempts','last_pair_ms','last_pair_book','last_sell_book','last_submit_book','last_replace_ms','halted','merge_failed','settled'):
                raise ValueError('unexpected checkpoint meta')
            if k in ('last_pair_book','last_sell_book','last_submit_book') and v is not None:v=tuple(tuple(x) for x in v)
            setattr(e,k,v)
        if e.active():
            e.active().status='UNKNOWN'
            e.active().query_sent=False
            e.active().last_query_ms=-1
        e.check()
        return e

    def snapshot(self):
        return dict(market=self.market,side=self.side,provenance=self.provenance,
                    exit_policy=self.policy.checkpoint(),
                    account_id=self.account_id,lot_id=self.lot_id,scope_id=self.scope_id,
                    own=str(self.own),other=str(self.other),own_cost=str(self.own_cost),
                    other_cost=str(self.other_cost),lot_net_cashflow=str(self.net_cashflow),
                    realized_paper_only=str(self.realized) if not self.fee_pending and self.provenance!='LIVE_CONFIRMED' else None,
                    realized_live_confirmed=str(self.realized) if not self.fee_pending and self.provenance=='LIVE_CONFIRMED' else None,
                    known_cashflow_excludes_pending_fees=bool(self.fee_pending),
                    fee_pending=self.fee_pending,
                    fee_estimate_pending=str(sum((self.fees[k]['estimate'] for k in self.fee_pending),ZERO)),
                    pair_attempts=self.pair_attempts,
                    active_order=self.active().id if self.active() else None,
                    cash_reserved=str(self.active().reserve if self.active() else ZERO),
                    halted=self.halted,merge_failed=self.merge_failed,decision=self.latest,
                    actual_profit=None,actual_orders_sent=None if self.provenance=='LIVE_CONFIRMED' else 0)
