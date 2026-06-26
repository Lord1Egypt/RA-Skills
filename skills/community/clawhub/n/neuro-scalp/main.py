import asyncio
import json
import os
import yaml
import sys
import signal
from loguru import logger
import redis.asyncio as redis

# Import Core Components
from core.data.feed import MarketDataFeed
from core.engine.execution import ExecutionEngine
from features.microstructure import FeatureEngine
from models.agent import AI_Trader

# Load Configuration
def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

class NeuroScalpOrchestrator:
    def __init__(self):
        self.running = True
        self.symbol = CONFIG['exchange']['pairs'][0]  # Trading first pair for now
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
        
        # Initialize Components
        self.feed = MarketDataFeed(self.symbol, self.redis_url)
        self.feature_engine = FeatureEngine(window_size=CONFIG['ml']['lookback_window'])
        self.agent = AI_Trader(model_path="models/checkpoints/latest.pth") # Loads trained model
        
        # Initialize Execution Engine with Env Vars (Security Best Practice)
        self.exec_engine = ExecutionEngine(
            api_key=os.getenv("OKX_API_KEY"),
            secret=os.getenv("OKX_SECRET"),
            password=os.getenv("OKX_PASSPHRASE")
        )
        
        self.redis = redis.from_url(self.redis_url)
        self.pub_sub = self.redis.pubsub()

    async def strategy_loop(self):
        """
        Consumes ticks from Redis, generates features, and executes trades.
        """
        logger.info("🧠 Strategy Engine Starting...")
        
        # Subscribe to the data feed channel
        channel = f"tick_{self.symbol.replace('/', '')}"
        await self.pub_sub.subscribe(channel)

        async for message in self.pub_sub.listen():
            if not self.running:
                break
                
            if message['type'] == 'message':
                try:
                    # 1. Parse Tick
                    data = json.loads(message['data'])
                    
                    # 2. Update Features
                    self.feature_engine.update(data)
                    
                    # 3. Feature Engineering (On every tick? Or resample? doing every tick for HFT)
                    # We need an orderbook snapshot structure
                    ob_snapshot = {
                        'bid': data['bid'], 'ask': data['ask'],
                        'bid_vol': data['bid_vol'], 'ask_vol': data['ask_vol']
                    }
                    features = self.feature_engine.get_features(ob_snapshot)
                    
                    # 4. AI Inference
                    # (Wait for warmup)
                    if len(self.feature_engine.prices) < self.feature_engine.window_size:
                        continue
                        
                    signal_strength = self.agent.predict(features)
                    
                    # 5. Execution Logic
                    # Filter low confidence signals
                    if abs(signal_strength) > 0.5:
                        logger.info(f"🔮 Signal: {signal_strength:.4f} | Price: {data['last_price']}")
                        
                        await self.exec_engine.execute_signal(
                            signal=signal_strength, 
                            price=data['last_price']
                        )
                        
                except Exception as e:
                    logger.error(f"Strategy Loop Error: {e}")
                    # Don't crash the loop, just log
                    await asyncio.sleep(0.1)
                    
    async def publish_metrics(self):
        """
        Calculates and broadcasts metrics to Redis for the Dashboard.
        """
        metrics = {
            "total_pnl": self.exec_engine.daily_pnl,  # Ensure execution.py tracks this
            "sharpe": 1.5,  # Replace with actual calculation
            "win_rate": 0.65, # Replace with actual calculation
            "timestamp": time.time()
        }
        await self.redis.publish("system_metrics", json.dumps(metrics))

    async def publish_trade(self, order):
        """
        Broadcasts trade confirmation.
        """
        payload = {
            "side": order['side'],
            "amount": order['amount'],
            "price": order['price']
        }
        await self.redis.publish("trade_events", json.dumps(payload))

    async def run(self):
        """
        Main Lifecycle Manager
        """
        logger.info("🚀 NeuroScalp System Starting...")
        
        # 1. Start Data Feed (Background Task)
        feed_task = asyncio.create_task(self.feed.start())
        
        # 2. Start Strategy Engine (Background Task)
        strategy_task = asyncio.create_task(self.strategy_loop())
        
        # 3. Keep alive and monitor
        try:
            while self.running:
                await asyncio.sleep(1)
                # Here you could add a 'health check' ping to the dashboard
        except asyncio.CancelledError:
            logger.info("System stopping...")
        finally:
            # Graceful Shutdown
            logger.info("Shutting down components...")
            await self.feed.close()
            await self.redis.close()
            feed_task.cancel()
            strategy_task.cancel()
            logger.success("System Shutdown Complete.")

    def shutdown(self):
        self.running = False

if __name__ == "__main__":
    # Handle Ctrl+C
    orchestrator = NeuroScalpOrchestrator()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    def signal_handler():
        orchestrator.shutdown()
        
    # Register signal handlers for Docker/Kubernetes graceful stop
    # (Note: Windows doesn't support add_signal_handler fully, wrap in try/except if needed)
    try:
        loop.add_signal_handler(signal.SIGINT, signal_handler)
        loop.add_signal_handler(signal.SIGTERM, signal_handler)
    except NotImplementedError:
        pass # Windows
        
    try:
        loop.run_until_complete(orchestrator.run())
    except KeyboardInterrupt:
        pass