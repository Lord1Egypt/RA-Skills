"""Monotonic server-time estimate; preserves raw host time outside this class.

RTT/2 is a conservative network asymmetry interval, not proof of UTC accuracy.
The 50 ppm drift allowance is an instrumentation assumption, not a tuned signal.
"""
class ReferenceClock:
    def __init__(self):
        self.anchor=None;self.last=None

    def update(self,sample,mono_ns):
        self.anchor={**sample,'mono_ns':mono_ns,'utc_ms':sample['at_ms']+sample['offset_ms']}

    def now(self,mono_ns):
        if not self.anchor:return None
        current=self.anchor['utc_ms']+(mono_ns-self.anchor['mono_ns'])/1e6
        self.last=max(current,self.last or current)
        return int(self.last)

    def uncertainty(self,mono_ns):
        if not self.anchor:return None
        projected=self.anchor['utc_ms']+(mono_ns-self.anchor['mono_ns'])/1e6
        clamp=max(0,(self.last or projected)-projected)
        return self.anchor['uncertainty_ms']+abs(mono_ns-self.anchor['mono_ns'])/1e6*.00005+1+clamp

    def public(self,mono_ns):
        if not self.anchor:return None
        return {'at_ms':int(self.anchor['utc_ms']),'host_at_ms':self.anchor['at_ms'],
            'offset_ms':self.anchor['offset_ms'],'residual_bound_ms':self.uncertainty(mono_ns),
            'uncertainty_ms':self.uncertainty(mono_ns),'rtt_ms':self.anchor['rtt_ms'],
            'source':'Binance serverTime / monotonic elapsed / RTT uncertainty',
            'drift_assumption_ppm':50,'age_ms':(mono_ns-self.anchor['mono_ns'])/1e6}
