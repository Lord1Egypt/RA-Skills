import json
import asyncio
import os
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

app = FastAPI(title="NeuroScalp Monitor")

# Redis Connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL)

# Setup Templates (for the frontend HTML)
templates = Jinja2Templates(directory="dashboard/templates")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("New Dashboard Connection")
    
    # Subscribe to Redis channels
    pubsub = r.pubsub()
    await pubsub.subscribe("trade_events", "system_metrics", "tick_BTCUSDT-SWAP")
    
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                # Forward Redis message directly to Frontend
                channel = message['channel'].decode('utf-8')
                data = json.loads(message['data'])
                
                payload = {
                    "type": channel,
                    "data": data
                }
                await websocket.send_json(payload)
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
    finally:
        await websocket.close()