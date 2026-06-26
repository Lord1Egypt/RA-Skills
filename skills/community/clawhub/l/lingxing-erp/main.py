import requests
import hashlib
import hmac
import time
import json

class LingxingSkill:
    def __init__(self, config):
        self.access_key = config["ACCESS_KEY"]
        self.secret_key = config["SECRET_KEY"]
        self.base_url = config.get("BASE_URL", "https://openapi.lingxing.com")

    def _generate_sign(self, params, timestamp):
        # 领星签名算法
        sorted_params = sorted(params.items())
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        sign_str = f"{timestamp}{sign_str}"
        return hmac.new(
            self.secret_key.encode(),
            sign_str.encode(),
            hashlib.sha256
        ).hexdigest().upper()

    def get_today_orders(self, page=1, page_size=20):
        timestamp = str(int(time.time()))
        params = {
            "access_key": self.access_key,
            "timestamp": timestamp,
            "page": page,
            "page_size": page_size,
            "start_time": time.strftime("%Y-%m-%d 00:00:00"),
            "end_time": time.strftime("%Y-%m-%d 23:59:59")
        }
        params["sign"] = self._generate_sign(params, timestamp)
        url = f"{self.base_url}/api/v1/orders"
        resp = requests.get(url, params=params)
        return resp.json()

# 技能入口
def run(config, params):
    skill = LingxingSkill(config)
    func = params.get("func", "get_today_orders")
    if func == "get_today_orders":
        return skill.get_today_orders(
            page=params.get("page", 1),
            page_size=params.get("page_size", 20)
        )
    raise ValueError(f"Unknown function: {func}")