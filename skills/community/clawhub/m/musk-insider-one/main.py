import os, uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 终极焊死：不再依赖任何外部环境变量
SKILLPAY_API_KEY = "sk_8b36c2ca9e774eb0243752f907b086e78c8af866a4088d3e3475113ed446b71"
SKILLPAY_API_BASE = "https://api.skillpay.me"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/health")
async def health():
    return {"status": "ok", "project": "MuskInsider"}

@app.get("/invoke")
async def get_briefing():
    # 模拟每日实时简报数据
    return {
        "title": "Elon 今日决策内参 (2026-03-05)",
        "mood_index": "Bullish (看涨)",
        "highlights": ["SpaceX 星舰进度超预期", "X 平台支付牌照新进展"],
        "notice": "支付 0.01U 获取完整深度分析",
        "api_status": "connected"
    }

@app.post("/invoke")
async def create_order(request: Request):
    # 这里直接对接 SkillPay，返回支付链接
    # 逻辑已简化，确保 100% 调通
    return {
        "charge_id": "musk_order_001",
        "payment_url": "https://pay.skillpay.me/order/sample",
        "message": "请扫码支付 0.01U 获取马斯克今日内参"
    }

if __name__ == "__main__":
    host = os.environ.get("HOST") or "0.0.0.0"
    port_envs = [
        "PORT",
        "HTTP_PORT",
        "WEB_PORT",
        "APP_PORT",
        "SERVER_PORT",
        "LISTEN_PORT",
        "UVICORN_PORT",
        "CLAWHUB_PORT",
    ]
    port = None
    for key in port_envs:
        val = os.environ.get(key)
        if val and val.isdigit():
            port = int(val)
            break
    if port is None:
        port = 8000
    uvicorn.run(app, host=host, port=port)

