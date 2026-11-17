"""Pure public-feed normalization. Local receive order is NOT exchange sequence."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
import json
import math
import re


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat().replace('+00:00', 'Z')


def website_reference(html, start):
    """Read the exact BTC/TWAP60 query in the official page's hydration data.

    No JS execution, regex number guessing, or cross-window fallback. Schema changes fail closed.
    """
    chunks = []
    for match in re.finditer(r'self\.__next_f\.push\((\[.*?\])\)</script>', html, re.S):
        try:
            part = json.loads(match.group(1))
            if part[0] == 1 and isinstance(part[1], str):
                chunks.append(part[1])
        except (ValueError, IndexError, TypeError):
            continue
    text = ''.join(chunks)
    decoder = json.JSONDecoder()
    wanted = ['crypto-prices','price','BTC',iso(start),'fifteen',iso(start+900),True,60]
    found = []
    for match in re.finditer(r'\{"dehydratedAt"', text):
        try:
            query, _ = decoder.raw_decode(text[match.start():])
            if query.get('queryKey') != wanted or query['state']['status'] != 'success':
                continue
            data = query['state']['data']
            value = data.get('openPrice')
            if isinstance(value, (int,float)) and math.isfinite(value) and value > 0:
                found.append({'value':value, 'close_value':data.get('closePrice'),
                              'query_key':wanted, 'published_ms':query['state']['dataUpdatedAt'],
                              'source':'PM_OFFICIAL_WEB_TWAP60', 'start':start})
        except (ValueError, KeyError, TypeError):
            continue
    if not found or len({x['value'] for x in found}) != 1:
        raise ValueError('official page has no unambiguous matching BTC 15m TWAP60 reference')
    return found[-1]


def normalize_market(m, start):
    def array(x): return json.loads(x) if isinstance(x,str) else x
    slug = f'btc-updown-15m-{start}'
    if m.get('slug') != slug:
        raise ValueError('wrong market')
    outcomes, tokens = array(m.get('outcomes')), array(m.get('clobTokenIds'))
    if outcomes != ['Up','Down'] or len(tokens) != 2 or tokens[0] == tokens[1]:
        raise ValueError('outcome/token mismatch')
    cfg, fees = m.get('cryptoMarketConfig') or {}, m.get('feeSchedule') or {}
    rules = (cfg.get('asset') == 'btc' and cfg.get('duration') == '15m' and
             cfg.get('twapEnabled') is True and cfg.get('twapLookbackSeconds') == 60 and
             m.get('resolutionSource') == 'https://data.chain.link/streams/btc-usd-twap-60s-streams' and
             m.get('eventStartTime') == iso(start) and m.get('endDate') == iso(start+900))
    fees_ok = (m.get('feesEnabled') is True and fees.get('rate') == .07 and
               fees.get('exponent') == 1 and fees.get('takerOnly') is True)
    return {'start':start,'end':start+900,'slug':slug,'condition':m['conditionId'],
            'tokens':dict(zip(outcomes,tokens)), 'tick':str(m['orderPriceMinTickSize']),
            'min_qty':str(m['orderMinSize']), 'rules_verified':rules,
            'fees_verified':fees_ok,'fee_schedule':fees,'accepting':m.get('acceptingOrders') is True,
            'closed':m.get('closed') is True, 'source':'GAMMA_PUBLIC'}


@dataclass
class PublicBook:
    bids: dict = field(default_factory=dict)
    asks: dict = field(default_factory=dict)
    source_ms: int = 0
    receive_ms: int = 0
    sequence: int = 0
    epoch: str = ''
    valid: bool = False

    @staticmethod
    def level(p,q):
        p,q = Decimal(str(p)),Decimal(str(q))
        if not p.is_finite() or not q.is_finite() or not 0 < p < 1 or q < 0:
            raise ValueError('invalid book level')
        return p,q

    def snapshot(self, event, receive_ms, epoch):
        bids, asks = {}, {}
        for key, target in [('bids',bids),('asks',asks)]:
            for x in event.get(key,[]):
                p,q = self.level(x['price'],x['size'])
                if p in target: raise ValueError('duplicate snapshot level')
                if q: target[p] = q
        self.bids,self.asks,self.epoch = bids,asks,epoch
        self.valid = True
        self.stamp(event['timestamp'],receive_ms)

    def delta(self, change, source_ms, receive_ms, epoch):
        if not self.valid or self.epoch != epoch: raise ValueError('delta before connection snapshot')
        p,q = self.level(change['price'],change['size'])
        if change['side'] not in ('BUY','SELL'): raise ValueError('unknown book side')
        target = self.bids if change['side'] == 'BUY' else self.asks
        if q: target[p] = q
        else: target.pop(p,None)
        self.stamp(source_ms,receive_ms)

    def stamp(self, source_ms, receive_ms):
        source_ms=int(source_ms)
        if source_ms < self.source_ms:
            self.valid=False
            raise ValueError('source timestamp regressed')
        self.source_ms,self.receive_ms=source_ms,receive_ms
        self.sequence+=1

    def public(self, now):
        return {'bids':[[str(p),str(q)] for p,q in sorted(self.bids.items(),reverse=True)[:10]],
                'asks':[[str(p),str(q)] for p,q in sorted(self.asks.items())[:10]],
                'source_ms':self.source_ms,'receive_ms':self.receive_ms,
                'age_ms':now-self.source_ms, 'local_sequence':self.sequence,
                'upstream_sequence':None,'epoch':self.epoch,'valid':self.valid,
                'sequence_note':'接收顺序可核查；官方此通道无全局序号，不能证明上游无遗漏'}
