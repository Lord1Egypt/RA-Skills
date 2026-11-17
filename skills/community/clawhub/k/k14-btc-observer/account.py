from dataclasses import dataclass, field, asdict
from common import D, dec, jsonable

@dataclass
class Account:
    principal: str = '50'
    cash: str = '50'
    buy_gross: str = '0'
    sell_gross: str = '0'
    exchange_fees: str = '0'
    settlement_gross: str = '0'
    settlement_fees: str = '0'
    applied: dict = field(default_factory=dict)

    def fill(self,receipt_id,action,quantity,price,fee,*,gross=None):
        q,p,f=dec(quantity),dec(price),dec(fee)
        value={'action':action,'quantity':str(q),'price':str(p),'fee':str(f)}
        if receipt_id in self.applied:
            if self.applied[receipt_id]!=value:raise ValueError('account receipt conflict')
            return
        if action not in ('BUY','SELL') or q<=0 or not 0<p<1 or f<0:raise ValueError('invalid account fill')
        computed=q*p
        gross=computed if gross is None else dec(gross)
        if abs(gross-computed)>D('1e-20'):raise ValueError('cash gross differs from share price evidence')
        self.cash=str(dec(self.cash)+(-gross-f if action=='BUY' else gross-f))
        field_name='buy_gross' if action=='BUY' else 'sell_gross'
        setattr(self,field_name,str(dec(getattr(self,field_name))+gross))
        self.exchange_fees=str(dec(self.exchange_fees)+f);self.applied[receipt_id]=value
        if dec(self.cash)<0:raise ValueError('confirmed cash became negative; investigate external funds/fees')

    def settlement(self,rid,gross,fee):
        g,f=dec(gross),dec(fee);value={'gross':str(g),'fee':str(f)}
        if rid in self.applied:
            if self.applied[rid]!=value:raise ValueError('settlement conflict')
            return
        if g<0 or f<0:raise ValueError('invalid settlement amounts')
        self.cash=str(dec(self.cash)+g-f)
        self.settlement_gross=str(dec(self.settlement_gross)+g)
        self.settlement_fees=str(dec(self.settlement_fees)+f);self.applied[rid]=value

    def allowance(self,session,config,*,buying_allowed=True):
        from pm_predict.strategy.parallel_exit import AccountAllowance
        reserve=sum((o.reserve for o in session.orders.values() if o.final_qty is None),D('0'))
        if session.exit:
            e=session.exit
            reserve+=sum((o.reserve for o in e.orders.values() if o.final_qty is None),D('0'))
            exposure=e.own_cost+e.other_cost
            loss=max(D('0'),-e.realized)
            pending=bool(e.fee_pending)
        else:
            exposure=session.entry_gross+session.entry_fees;loss=D('0');pending=bool(session.fee_pending)
        cash=max(D('0'),dec(self.cash)-reserve)
        return AccountAllowance(cash,max(D('0'),dec(config.daily_risk)-exposure-loss-reserve),
            max(D('0'),dec(config.total_risk)-exposure-loss-reserve),buying_allowed=buying_allowed and not pending)

    def report(self,session=None):
        closed=bool(session and session.exit and session.exit.own==0 and session.exit.other==0 and not session.exit.fee_pending)
        net=dec(self.cash)-dec(self.principal) if closed else None
        total_fees=dec(self.exchange_fees)+dec(self.settlement_fees)
        return {**{k:v for k,v in asdict(self).items() if k!='applied'},'confirmed_receipts':len(self.applied),
            'net_realized_pnl':str(net) if net is not None else None,
            'gross_realized_pnl_before_recorded_fees':str(net+total_fees) if net is not None else None,
            'unrealized_pnl':None,'external_gas_relayer_vps_subscription_costs':None,
            'profit_after_all_costs':None,
            'note':'pUSD ledger only. Settlement fees are confirmed pUSD payout deductions. External costs and rebates are not assumed zero; reconcile separately. Open inventory is not a fabricated fill; funding is not profit.'}

    def checkpoint(self):return asdict(self)
    @classmethod
    def restore(cls,state):return cls(**state)
