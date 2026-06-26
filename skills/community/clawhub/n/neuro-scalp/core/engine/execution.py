class ExecutionEngine:
    def __init__(self, api_key, secret, password):
        self.exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': secret,
            'password': password,
            'enableRateLimit': True,
            'options': {'defaultType': 'swap'}
        })
        self.current_position = 0
        self.daily_pnl = 0

    async def execute_signal(self, signal, price):
        """
        Signal: -1.0 to 1.0
        """
        if abs(signal) < 0.2:
            return # Weak signal filter

        # RISK CHECK
        if not self.check_risk(signal):
            return

        side = 'buy' if signal > 0 else 'sell'
        size = self.calculate_kelly_size(signal)
        
        try:
            # Post-only limit order to save fees (Scalping requirement)
            order = await self.exchange.create_order(
                symbol="BTC/USDT:USDT",
                type='limit',
                side=side,
                amount=size,
                price=price,
                params={'postOnly': True}
            )
            logger.info(f"Order Placed: {side} {size} @ {price}")
            return order
        except Exception as e:
            logger.error(f"Execution Failed: {e}")

    def check_risk(self, signal):
        # 1. Max Drawdown check
        if self.daily_pnl < -500: # $500 max daily loss
            logger.critical("KILL SWITCH ACTIVATED")
            return False
        return True

    def calculate_kelly_size(self, signal_strength):
        # Dynamic sizing based on model confidence
        base_size = 0.01 # BTC
        return base_size * abs(signal_strength)