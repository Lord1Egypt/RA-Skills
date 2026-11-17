"""Frozen-engine shadow decisions. Public books cannot identify our queue fills.

No fabricated ACK/MATCH/CONFIRMED events. Ambiguous intent reserves remain held.
The live account is therefore an epistemic shadow, not a hypothetical profit curve.
"""
from decimal import Decimal as D
from pm_predict.engine import PaperEngine
from pm_predict.domain.money import fee
from pm_predict.strategy.indicators import Bar, k14, signal, fair_up


class LiveShadow:
    def __init__(self, thresholds, emit):
        self.engine=PaperEngine();self.thresholds=thresholds;self.emit=emit
        self.current=None;self.signal=None;self.signals=0;self.last_reason=None
        self.opened=set();self.book_seq={};self.sent_books={}
        self.recovery_reason=None;self.previous_account=None
        self.previous_orders=[]
        self.session=None;self.archived_sessions=[]

    def lock(self, start, bars):
        if self.current==start:return
        value=k14([Bar(**x) for x in bars],start)
        if self.thresholds.get('provisional') is not False:
            raise ValueError('provisional thresholds cannot authorize shadow entries')
        side=signal(value,self.thresholds,start)
        self.current=start;self.signal={'start':start,'k14':value,'side':side,'fair_up':None,
            'status':'WAITING','reason':'等待完整官方行情与健康检查','formula':'K14 / q=0.05',
            'fill_status':'NOT_ATTEMPTED','realized_pnl':None,'actual_fee':None,'actual_slippage':None}
        self.signals+=int(side is not None)
        # Retain all uncertain exposure, but evict completed observation-only windows.
        e=self.engine
        for key in list(e.windows):
            if e.windows[key].start < start and not any(o.market==key for o in e.orders.values()):
                del e.windows[key]
        self.opened.intersection_update(e.windows)
        self.book_seq.clear();self.sent_books.clear()
        self.emit('SIGNAL_LOCKED',dict(self.signal))

    def reason(self, text):
        if self.signal:
            self.signal['reason']=text
            if text != self.last_reason:
                self.emit('PAPER_GATE',{'start':self.current,'reason':text});self.last_reason=text

    def disconnect(self, now, reason):
        e=self.engine
        for w in e.windows.values():
            if not w.blocked and w.start+900>now/1000:
                e.health(w.id,max(now,e.now),connected=False)
        self.drain()
        self.reason(reason)

    def step(self, market, ptb, books, price, sigma, clock, now):
        if not self.signal or self.current!=market['start']:return
        s=self.signal;e=self.engine;key=market['slug'];age=now/1000-market['start']
        if self.recovery_reason:
            s['status']='BLOCKED';self.reason(self.recovery_reason);return
        if key in self.opened:
            w=e.windows[key]
            if w.blocked:
                s['status']='BLOCKED';self.reason(w.blocked);return
            if age>=120 or any(o.market==key and o.status=='SENT' and now-o.sent_ms>2000 for o in e.orders.values()):
                e.step(key,now);self.drain()
                if w.blocked:
                    s['status']='BLOCKED';self.reason(w.blocked);return
        if s['side'] is None:
            s['status']='NO_SIGNAL';self.reason('K14 未越过锁定阈值');return
        if age>=900:return
        if not (market['rules_verified'] and market['fees_verified'] and market['accepting']):
            self.reason('市场规则、费率或交易状态未通过原门槛');return
        if not ptb or ptb['start']!=market['start']:
            self.reason('官方待击败价未知');return
        if not price or sigma is None:
            self.reason('逐笔价格或连续分钟波动率未就绪');return
        s['fair_up']=fair_up(float(price['price']),ptb['value'],sigma,900-age)
        if not clock or clock.get('age_ms',120001)>120000 or clock.get('residual_bound_ms',float('inf'))>=50:
            self.reason('时钟误差区间尚不能确认在 50 ms 内');return
        if set(books)!= {'Up','Down'} or not all(b.valid and b.bids and b.asks and 0<=now-b.source_ms<=2000 for b in books.values()):
            self.reason('双边盘口缺失、断流或超过冻结的 2 秒新鲜度');return
        if not 0<=now-price['source_ms']<=2000:
            self.reason('币安价格延迟超过 2 秒');return
        if key not in self.opened:
            if age>=120:
                s['status']='MISSED_ENTRY';self.reason('数据就绪时已超过原 120 秒入场期限，不补做历史交易');return
            e.open_window(key,market['start'],self.bars,self.thresholds,ptb['value'],
                tick=market['tick'],min_qty=market['min_qty'],rule_verified=True,
                ptb_source='CHAINLINK_TWAP60_AT_START',fee_rate='0.07',now=now)
            self.opened.add(key)
        w=e.windows[key]
        if w.blocked:
            s['status']='BLOCKED';self.reason(w.blocked);return
        for side,b in books.items():
            if self.sent_books.get(side)!=b.sequence:
                seq=self.book_seq.get(side,0)+1;self.book_seq[side]=seq;self.sent_books[side]=b.sequence
                e.book(key,side,seq,b.source_ms,now,str(max(b.bids)),
                       [(str(p),str(q)) for p,q in sorted(b.asks.items())],market['tick'])
        e.price(key,price['price'],sigma,price['source_ms'],now)
        e.health(key,now,clock_offset_ms=clock['residual_bound_ms'],reconciled=True,connected=True)
        e.step(key,now)
        orders=[o for o in e.orders.values() if o.market==key]
        if orders:
            s['status']='INTENT_ONLY';s['fill_status']='UNKNOWN_PUBLIC_QUEUE'
            self.reason('仅生成纸面意图；无真实订单回执，成交、实际费用和盈亏未知，预留资金不释放')
            entry=orders[0];other='Down' if entry.side=='Up' else 'Up'
            s['conditional_hedge']=conditional_cost(entry.price,books[other],market['min_qty'])
        else:
            s['status']='OBSERVING';self.reason('行情有效，原挂价 / 风控条件尚未触发')
        self.drain()

    def drain(self):
        e=self.engine
        for item in e.journal:self.emit('FROZEN_ENGINE',item)
        e.state.journal.clear();e.state.intents.clear()

    def public(self):
        e=self.engine
        return {'signal':self.signal,'signals_seen':self.signals,'orders':[
            {'id':o.id,'market':o.market,'side':o.side,'price':str(o.price),'qty':str(o.qty),
             'status':'UNKNOWN_PUBLIC_QUEUE','engine_status':o.status,'sent_ms':o.sent_ms,
             'actual_fee':None,'actual_slippage':None,'actual_filled_qty':None} for o in e.orders.values()]+self.previous_orders,
             'account':self.previous_account or {'cash':str(e.cash),'reserved':str(e.reserve()),'realized_pnl':None,
                        'note':'未提交实际订单；金额为影子意图预算，未假设任何 Maker 成交'},
             'thresholds':self.thresholds,'session':self.session,'archived_sessions':self.archived_sessions}


def conditional_cost(entry_price, opposite_book, min_qty):
    """Quote-based what-if, conditional on a full first leg, never posted as P&L."""
    left=D('5');cost=D('0');fees=D('0');worst=None
    best=min(opposite_book.asks) if opposite_book.asks else None
    for p,q in sorted(opposite_book.asks.items()):
        if p>D('.50'):break
        take=min(left,q);cost+=take*p;fees+=fee(take,p);left-=take;worst=p
        if left==0:break
    filled=D('5')-left
    bound=D('5')*worst+fee(D('5'),worst)+D('.00005') if worst else None
    allowed=not left and D(min_qty)<=5 and entry_price*5+bound<=D('4.75')
    return {'assumption':'仅假设首腿已全成 5 份；实际是否成交未知',
            'depth_qty':str(filled),'missing_qty':str(left),'taker_fee_estimate':str(fees),
            'snapshot_pair_cost':str(entry_price*5+cost+fees) if not left else None,
            'worst_pair_cost':str(entry_price*5+bound) if not left else None,
            'depth_slippage':str(cost-filled*best) if best is not None else None,
            'passes_original_cap':bool(allowed),'actual_fill':None,'actual_latency':None}
