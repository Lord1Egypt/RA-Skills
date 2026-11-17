from .money import D, ZERO

class EngineState:

    def __init__(self):
        self.initial = self.cash = D('60')
        self.realized = ZERO
        self.daily = {}
        self.windows, self.orders, self.fills = ({}, {}, {})
        self.journal, self.intents = ([], [])
        self.halted = None
        self.loss_streak = 0
        self.pause_until = 0
        self.now = 0

    def _log(self, event, **values):
        self.journal.append({'time_ms': self.now, 'event': event, **values})

    def _intent(self, action, **values):
        item = {'time_ms': self.now, 'action': action, 'mode': 'OFFLINE_PAPER', **values}
        self.intents.append(item)
        self._log('INTENT', **item)

    def _time(self, now):
        if now < self.now:
            raise ValueError('receive time regressed')
        self.now = now