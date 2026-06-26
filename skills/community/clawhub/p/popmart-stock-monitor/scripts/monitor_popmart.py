#!/usr/bin/env python3
"""
PopMart Stock Monitor - Main monitoring script
Supports WeChat Mini Programs, Taobao, JD.com, and Tmall
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Platform-specific modules (to be implemented)
from .platforms import wechat, taobao, jd, tmall
from .notifier import send_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PopMartMonitor:
    def __init__(self, config_path: str = "popmart_config.json"):
        """Initialize monitor with configuration"""
        self.config = self.load_config(config_path)
        self.platform_handlers = {
            'wechat': wechat.WeChatHandler(),
            'taobao': taobao.TaobaoHandler(),
            'jd': jd.JDHandler(),
            'tmall': tmall.TmallHandler()
        }
        
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {config_path} not found")
            return self.create_default_config()
            
    def create_default_config(self) -> Dict:
        """Create default configuration"""
        default_config = {
            "products": [],
            "check_interval_minutes": 30,
            "notification": {
                "channel": "console",
                "webhook_url": ""
            },
            "api_keys": {}
        }
        # Save default config
        with open("popmart_config.json", 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        logger.info("Created default config file: popmart_config.json")
        return default_config
        
    def check_product_stock(self, product: Dict) -> List[Dict]:
        """Check stock status for a single product across all platforms"""
        results = []
        platforms = product.get('platforms', ['jd', 'tmall', 'taobao', 'wechat'])
        
        for platform in platforms:
            if platform not in self.platform_handlers:
                logger.warning(f"Unknown platform: {platform}")
                continue
                
            try:
                handler = self.platform_handlers[platform]
                stock_info = handler.check_stock(product)
                if stock_info:
                    results.append(stock_info)
                    logger.info(f"Found stock info for {product['name']} on {platform}")
                    
                    # Send notification if back in stock
                    if stock_info.get('in_stock', False):
                        self.send_stock_alert(product, platform, stock_info)
                        
            except Exception as e:
                logger.error(f"Error checking {platform} for {product['name']}: {e}")
                
        return results
        
    def send_stock_alert(self, product: Dict, platform: str, stock_info: Dict):
        """Send notification when product is back in stock"""
        alert_data = {
            'product_name': product['name'],
            'platform': platform,
            'product_url': stock_info.get('url', ''),
            'price': stock_info.get('price', 'N/A'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        notification_config = self.config.get('notification', {})
        send_notification(alert_data, notification_config)
        
    def run_monitoring_loop(self):
        """Main monitoring loop"""
        products = self.config.get('products', [])
        if not products:
            logger.warning("No products configured for monitoring")
            return
            
        interval = self.config.get('check_interval_minutes', 30) * 60
        
        logger.info(f"Starting PopMart monitoring for {len(products)} products")
        logger.info(f"Check interval: {interval//60} minutes")
        
        while True:
            try:
                logger.info("Starting stock check cycle...")
                for product in products:
                    self.check_product_stock(product)
                    
                logger.info(f"Completed stock check cycle. Sleeping for {interval//60} minutes...")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main entry point"""
    monitor = PopMartMonitor()
    monitor.run_monitoring_loop()

if __name__ == "__main__":
    main()