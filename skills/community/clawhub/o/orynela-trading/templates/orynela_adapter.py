"""
Orynela Sandbox Adapter — Drop-in module for any AI agent.
Sandbox-only. No real execution. No broker connection.

Usage:
    from orynela_adapter import OrynelaAdapter
    api = OrynelaAdapter()
    api.send_heartbeat()
    candles = api.get_candles("BTCUSDT", "1h", 200)
    signal = api.send_signal("BTCUSDT", "buy", 0.75, "RSI oversold + volume spike")
    if signal.get("risk_status") == "accepted":
        order = api.simulate_order("BTCUSDT", "buy", 0.01, signal["signal_id"])
    portfolio = api.get_portfolio()

Setup:
    No dependencies beyond Python stdlib.
    Set env vars: ORYNELA_API_BASE, ORYNELA_SANDBOX_KEY
"""
import os, json, time, urllib.request, urllib.error


class OrynelaApiError(Exception):
    pass


class OrynelaAdapter:
    """Sandbox-only adapter. real_execution = False permanently."""

    def __init__(self, api_base=None, api_key=None):
        self.base = api_base or os.environ.get(
            "ORYNELA_API_BASE", "https://orynela.ai/api/sandbox")
        self.key = api_key or os.environ.get("ORYNELA_SANDBOX_KEY", "")
        if not self.key:
            raise OrynelaApiError(
                "No API key. Set ORYNELA_SANDBOX_KEY env var or pass api_key.")
        self.environment = "sandbox"
        self.real_execution = False

    def _request(self, method, path, body=None):
        url = self.base + path
        headers = {"Authorization": "Bearer " + self.key,
                   "Content-Type": "application/json"}
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            try:
                raise OrynelaApiError(
                    f"HTTP {e.code}: {json.loads(error_body)}") from e
            except json.JSONDecodeError:
                raise OrynelaApiError(f"HTTP {e.code}: {error_body}") from e

    def send_heartbeat(self, status="online", latency_ms=None, version="0.1.0"):
        return self._request("POST", "/heartbeat",
            {"status": status, "latency_ms": latency_ms, "version": version})

    def send_log(self, level="info", message="", context=None):
        return self._request("POST", "/logs",
            {"level": level, "message": message, "context": context or {}})

    def send_signal(self, symbol, side, confidence, reasoning,
                    timeframe="1h", signal_type="trend_observation"):
        return self._request("POST", "/signals", {
            "symbol": symbol, "side": side, "confidence": confidence,
            "reasoning": reasoning, "timeframe": timeframe,
            "signal_type": signal_type})

    def get_signals(self):
        return self._request("GET", "/signals")

    def simulate_order(self, symbol, side, quantity, signal_id=None):
        body = {"symbol": symbol, "side": side,
                "order_type": "market", "quantity": quantity}
        if signal_id:
            body["signal_id"] = signal_id
        return self._request("POST", "/orders/simulate", body)

    def get_orders(self):
        return self._request("GET", "/orders")

    def get_portfolio(self):
        return self._request("GET", "/portfolio")

    def get_candles(self, symbol, timeframe="1h", limit=200):
        return self._request("GET",
            f"/market/candles?symbol={symbol}&timeframe={timeframe}&limit={limit}")

    @staticmethod
    def get_status():
        req = urllib.request.Request("https://orynela.ai/api/sandbox/status")
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())

    def signal_and_order(self, symbol, side, confidence, reasoning,
                         quantity=1, timeframe="1h",
                         signal_type="trend_observation"):
        """Signal + immediately place order if accepted."""
        sig = self.send_signal(symbol, side, confidence, reasoning,
                               timeframe, signal_type)
        order = None
        if sig.get("ok") and sig.get("risk_status") == "accepted":
            time.sleep(0.3)
            order = self.simulate_order(symbol, side, quantity,
                                        sig.get("signal_id"))
        return sig, order
