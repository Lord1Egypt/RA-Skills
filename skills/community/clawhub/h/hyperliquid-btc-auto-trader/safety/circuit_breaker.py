# skills/hyperliquid-btc-auto-trader/safety/circuit_breaker.py
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self):
        self.last_signal = 0.0
        self.last_signal_time = datetime.now()
        self.paused_until = None

    def is_triggered(self):
        if self.paused_until and datetime.now() < self.paused_until:
            return True
        return False

    def check_signal_jump(self, new_signal: float):
        """Pause for 30 minutes if signal changes >50 points in under 1 minute"""
        now = datetime.now()
        if (now - self.last_signal_time).total_seconds() < 60:
            if abs(new_signal - self.last_signal) > 50:
                self.paused_until = now + timedelta(minutes=30)
                print("⚠️ CIRCUIT BREAKER TRIGGERED — Pausing trading for 30 minutes")
        self.last_signal = new_signal
        self.last_signal_time = now