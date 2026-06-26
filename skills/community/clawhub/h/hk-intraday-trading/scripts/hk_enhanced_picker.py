#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股增强版选股器 - 使用Tushare API获取实时价格，计算买入/卖出/止损价格
"""
import os
import json
import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tushare API 配置
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")
TUSHARE_URL = "http://api.tushare.pro"


def call_tushare(api_name: str, params: dict = None, fields: str = "") -> dict:
    """调用Tushare API"""
    try:
        resp = requests.post(
            TUSHARE_URL,
            json={
                "api_name": api_name,
                "token": TUSHARE_TOKEN,
                "params": params or {},
                "fields": fields
            },
            timeout=15
        )
        result = resp.json()
        if result.get("code") != 0:
            logger.warning(f"Tushare API error: {result.get('msg')}")
            return None
        return result.get("data", {})
    except Exception as e:
        logger.error(f"API调用失败: {e}")
        return None


def get_hk_price_yahoo(stock_code: str) -> dict:
    """使用Yahoo Finance获取港股价格"""
    try:
        # Yahoo Finance 港股代码格式: 09988.HK
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_code}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, params={'interval': '1d', 'range': '5d'}, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                meta = result[0].get("meta", {})
                price = meta.get("regularMarketPrice")
                prev_close = meta.get("previousClose")
                pct_chg = 0
                if prev_close and price:
                    pct_chg = (price - prev_close) / prev_close * 100
                
                # 获取最近收盘价
                quotes = result[0].get("indicators", {}).get("quote", [{}])[0]
                if quotes and quotes.get("close"):
                    closes = [c for c in quotes["close"] if c is not None]
                    if closes:
                        price = closes[-1]
                        if len(closes) > 1:
                            prev_close = closes[-2]
                            pct_chg = (price - prev_close) / prev_close * 100 if prev_close else 0
                
                return {
                    "success": True,
                    "price": price,
                    "prev_close": prev_close,
                    "pct_chg": pct_chg,
                    "source": "yahoo"
                }
    except Exception as e:
        logger.warning(f"Yahoo获取{stock_code}失败: {e}")
    return {"success": False}


def get_hk_daily_price(stock_code: str, trade_date: str = None) -> dict:
    """获取港股价格 - 优先Tushare，失败则用Yahoo备用"""
    
    # 先尝试Tushare（如果有额度）
    try:
        if trade_date is None:
            trade_date = datetime.now().strftime("%Y%m%d")
        
        data = call_tushare(
            "hk_daily",
            params={"ts_code": stock_code, "trade_date": trade_date},
            fields="ts_code,trade_date,open,high,low,close,pre_close,pct_chg,vol"
        )
        
        if data and data.get("items"):
            item = data["items"][0]
            fields = data.get("fields", [])
            result = dict(zip(fields, item))
            return {
                "success": True,
                "price": result.get("close", 0),
                "open": result.get("open", 0),
                "high": result.get("high", 0),
                "low": result.get("low", 0),
                "pre_close": result.get("pre_close", 0),
                "pct_chg": result.get("pct_chg", 0),
                "vol": result.get("vol", 0),
                "source": "tushare"
            }
    except:
        pass
    
    # 备用：使用Yahoo Finance
    return get_hk_price_yahoo(stock_code)


def calculate_trade_prices(current_price: float, config: dict) -> dict:
    """计算买入价、卖出价、止损价"""
    buy_discount = config.get("buy_discount", 0.005)
    target_gain = config.get("target_gain_pct", 1.0)
    stop_loss = config.get("stop_loss_pct", 1.5)
    
    target_buy = current_price * (1 - buy_discount / 100)
    target_sell = target_buy * (1 + target_gain / 100)
    stop_price = target_buy * (1 - stop_loss / 100)
    
    risk = stop_loss
    reward = target_gain
    risk_reward = reward / risk if risk > 0 else 0
    
    return {
        "target_buy": round(target_buy, 2),
        "target_sell": round(target_sell, 2),
        "stop_loss": round(stop_price, 2),
        "target_gain_pct": target_gain,
        "stop_loss_pct": stop_loss,
        "risk_reward_ratio": round(risk_reward, 2)
    }


class HKEnhancedPicker:
    """港股增强版选股器"""
    
    def __init__(self):
        self.skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.skill_root, "data")
        self.output_dir = os.path.join(self.skill_root, "output/picks")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 加载配置
        self.strategy_config = self._load_json("strategy_config.json")
        self.performance_data = self._load_json("performance_tracking.json")
        self.stock_pool = [s for s in self.strategy_config["selection_criteria"]["stock_pool"] if s.get("enabled", True)]
        self.trade_settings = self.strategy_config.get("trade_settings", {})
        
        logger.info(f"Loaded {len(self.stock_pool)} stocks from config")
    
    def _load_json(self, filename: str) -> dict:
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_history_data(self) -> dict:
        history = {}
        for code, data in self.performance_data.get("stock_performance", {}).items():
            history[code] = {
                "win_rate": data.get("win_rate", 0),
                "total_trades": data.get("total_picks", 0),
            }
        return history
    
    def calculate_score(self, stock_code: str) -> int:
        """计算选股评分"""
        history = self._get_history_data()
        if stock_code not in history:
            return 60
        
        data = history[stock_code]
        trades = data.get("total_trades", 0)
        if trades < 3:
            return 60 + trades * 5
        
        return min(100, int(data.get("win_rate", 0) * 100))
    
    def run(self):
        """运行选股"""
        logger.info("=" * 50)
        logger.info("港股盘前选股开始（增强版 - Tushare）")
        logger.info("=" * 50)
        
        suggestions = []
        min_score = 50  # 放宽评分限制，只要有一只满足就选
        
        for stock in self.stock_pool:
            code = stock["code"]
            name = stock["name"]
            
            score = self.calculate_score(code)
            # 评分低于55的才跳过（给新股更多机会）
            if score < 55:
                logger.info(f"跳过 {name}: 评分{score} < 55")
                continue
            
            # 获取实时价格（优先Tushare，失败则用Yahoo）
            price_data = get_hk_daily_price(code)
            
            # 如果Tushare失败，尝试Yahoo
            if not price_data.get("success"):
                logger.info(f"Tushare获取{code}失败，尝试Yahoo...")
                price_data = get_hk_price_yahoo(code)
            
            if not price_data.get("success"):
                logger.warning(f"无法获取 {name} 价格")
                continue
            
            current_price = price_data["price"]
            pct_chg = price_data.get("pct_chg", 0)
            
            # 计算交易价格
            trade_prices = calculate_trade_prices(current_price, self.trade_settings)
            
            suggestion = {
                "stock_code": code,
                "stock_name": name,
                "score": score,
                "current_price": current_price,
                "pct_chg": round(pct_chg, 2),
                **trade_prices,
                "action": "推荐买入" if score >= 70 else "考虑买入",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            suggestions.append(suggestion)
            
            logger.info(f"✅ {name}: 现价 HK${current_price} ({pct_chg:+.2f}%)")
            logger.info(f"   买入: {trade_prices['target_buy']} | 卖出: {trade_prices['target_sell']} | 止损: {trade_prices['stop_loss']}")
        
        # 只选评分最高的1只股票
        if suggestions:
            suggestions = [max(suggestions, key=lambda x: x["score"])]
            logger.info(f"已选择评分最高的1只股票: {suggestions[0]['stock_name']}")
        
        self.save_results(suggestions)
        logger.info(f"选股完成，共选出 {len(suggestions)} 只股票")
        return suggestions
    
    def save_results(self, suggestions: list):
        """保存结果"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        result_data = {
            "date": date_str,
            "generated_at": datetime.now().isoformat(),
            "total_picks": len(suggestions),
            "suggestions": suggestions,
            "trade_settings": self.trade_settings
        }
        
        # JSON
        json_file = os.path.join(self.output_dir, f"picks_{date_str}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        # Markdown
        md_file = os.path.join(self.output_dir, f"picks_report_{date_str}.md")
        self._generate_markdown(md_file, result_data)
        
        # 飞书通知
        self._send_feishu_notification(result_data)
        
        logger.info(f"结果已保存: {json_file}")
    
    def _generate_markdown(self, filepath: str, data: dict):
        """生成Markdown报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 🍇 港股盘前选股报告\n\n")
            f.write(f"📅 选股日期: {data['date']}\n")
            f.write(f"⏰ 生成时间: {datetime.now().strftime('%H:%M:%S')}\n\n")
            
            f.write("## 🎯 今日选股结果\n\n")
            
            if not data["suggestions"]:
                f.write("**今日无符合条件的股票**\n\n")
            else:
                f.write(f"**共选出 {data['total_picks']} 只股票**\n\n")
                
                for i, s in enumerate(data["suggestions"], 1):
                    f.write(f"### {i}. {s['stock_name']} ({s['stock_code']})\n\n")
                    f.write(f"**操作建议**: {s['action']} | 评分: {s['score']}/100\n\n")
                    f.write("| 指标 | 数值 |\n")
                    f.write("|------|------|\n")
                    f.write(f"| 当前价格 | HK${s['current_price']} ({s['pct_chg']:+.2f}%) |\n")
                    f.write(f"| **目标买入** | **HK${s['target_buy']}** |\n")
                    f.write(f"| **目标卖出** | **HK${s['target_sell']} (+{s['target_gain_pct']}%)** |\n")
                    f.write(f"| **止损价格** | **HK${s['stop_loss']} (-{s['stop_loss_pct']}%)** |\n")
                    f.write(f"| 风险收益比 | {s['risk_reward_ratio']}:1 |\n\n")
            
            f.write(f"---\n")
            f.write(f"🎯 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def _send_feishu_notification(self, data: dict):
        """发送飞书通知 - 使用OpenClaw CLI"""
        try:
            import subprocess
            import shlex
            
            date_str = data["date"]
            suggestions = data["suggestions"]
            
            message_text = f"🍇 **{date_str} 港股选股结果**\n\n"
            
            if not suggestions:
                message_text += "今日无符合条件的股票"
            else:
                for s in suggestions:
                    message_text += f"**{s['stock_name']}** ({s['stock_code']})\n"
                    message_text += f"  当前: HK${s['current_price']} ({s['pct_chg']:+.2f}%)\n"
                    message_text += f"  🟢 买入: HK${s['target_buy']}\n"
                    message_text += f"  🔴 卖出: HK${s['target_sell']} (+{s['target_gain_pct']}%)\n"
                    message_text += f"  🛡️ 止损: HK${s['stop_loss']} (-{s['stop_loss_pct']}%)\n"
                    message_text += f"  评分: {s['score']}/100 | 建议: {s['action']}\n\n"
            
            # 使用OpenClaw CLI发送到飞书
            feishu_user_id = os.getenv("FEISHU_USER_ID", "ou_eb6695d143b4010149cbf8de7f0e39bd")
            cmd = f"openclaw message send --channel feishu --target {feishu_user_id} --message {shlex.quote(message_text)}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info("飞书通知已发送")
            else:
                # 尝试用--json处理多行消息
                logger.warning(f"飞书通知需要特殊处理: {result.stderr}")
            
        except Exception as e:
            logger.warning(f"飞书通知失败: {e}")


def main():
    picker = HKEnhancedPicker()
    suggestions = picker.run()
    
    if suggestions:
        print(f"\n✅ 选出 {len(suggestions)} 只股票:")
        for s in suggestions:
            print(f"  {s['stock_name']}: 买入{s['target_buy']}, 卖出{s['target_sell']}, 止损{s['stop_loss']}")
    else:
        print("\n⚠️ 今日无符合条件的股票")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())