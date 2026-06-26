#!/usr/bin/env python3
"""
IPO监控技能 V2 - 主入口
功能：每日自动抓取IPO数据，对比差异，推送飞书

使用方法:
    python main.py              # 运行一次
    python main.py --daemon     # 守护进程模式
    python main.py --test       # 测试模式（不推送）
    python main.py --interval 2 # 指定运行间隔（小时）
    python main.py --browser    # 浏览器模式（需要OpenClaw环境）
"""
import sys
import os
import logging
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from scrapers.csrc_scraper import CSRCScraper
from scrapers.hkex_scraper import HKEXScraper
from scrapers.nyse_scraper import NYSEScraper
from scrapers.nasdaq_scraper import NASDAQScraper
from scrapers.sse_scraper import SSEScraper
from scrapers.szse_scraper import SZSEScraper
from scrapers.bse_scraper import BSEScraper
from scrapers.browser_fetcher import BrowserFetcher
from scrapers.browser_scrapers import (
    SSEBrowserScraper,
    SZSEBrowserScraper,
    BSEBrowserScraper,
    HKEXNewBrowserScraper,
    HKEXAppBrowserScraper,
    NASDAQBrowserScraper,
    NYSEBrowserScraper,
)
from storage.sqlite_storage import SQLiteStorage
from storage.feishu_pusher import FeishuPusher
from utils.deduplicator import Deduplicator
from utils.diff_engine import DiffEngine


class IPOMonitorV2:
    """IPO监控主类"""
    
    def __init__(self, config_path: str = None):
        # 加载配置
        if config_path:
            self.config = Config(config_path)
        else:
            self.config = Config()
        
        # 设置日志
        self.logger = self._setup_logging()
        
        # 初始化存储
        self.storage = SQLiteStorage(self.config.db_path)
        
        # 初始化飞书推送
        self.pusher = FeishuPusher(self.config)
        
        # 差异计算引擎
        self.diff_engine = DiffEngine()
        
        # 去重器
        self.deduplicator = Deduplicator()
        
        # 初始化各交易所抓取器
        self._init_scrapers()
        
        # 绑定告警回调
        self._setup_alert_callbacks()
    
    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        # 确保日志目录存在
        log_file = Path(self.config.log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        logger = logging.getLogger('ipo_monitor')
        logger.setLevel(getattr(logging, self.config.log_level))
        
        # 文件处理器
        file_handler = logging.FileHandler(
            self.config.log_file,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _init_scrapers(self):
        """初始化抓取器"""
        self.scrapers = {}
        self.browser_scrapers = {}  # 浏览器抓取器
        self.browser_fetcher = None  # 浏览器抓取辅助类
        
        for exchange_config in self.config.enabled_exchanges:
            name = exchange_config['name']
            source = exchange_config['source']
            url = exchange_config.get('url', '')
            
            if source == 'csrc':
                # 根据名称判断板块
                board = '科创板' if '科创' in name else '主板'
                self.scrapers[name] = CSRCScraper(self.config, board)
            elif source == 'hkex':
                self.scrapers[name] = HKEXScraper(self.config)
            elif source == 'nyse':
                self.scrapers[name] = NYSEScraper(self.config, name)
            elif source == 'nasdaq':
                # 纳斯达克抓取器
                self.scrapers[name] = NASDAQScraper(self.config)
            elif source == 'sse':
                # 上交所抓取器
                self.scrapers[name] = SSEScraper(self.config)
            elif source == 'szse':
                # 深交所抓取器
                self.scrapers[name] = SZSEScraper(self.config)
            elif source == 'bse':
                # 北交所抓取器
                self.scrapers[name] = BSEScraper(self.config)
        
        # 初始化BrowserFetcher（用于浏览器模式）
        self.browser_fetcher = BrowserFetcher(self.config)
        
        # 初始化BrowserScraper子类（A股）
        self.browser_scrapers = {
            '上交所': SSEBrowserScraper(self.config),
            '深交所': SZSEBrowserScraper(self.config),
            '北交所': BSEBrowserScraper(self.config),
        }
        
        # 添加港股和美股BrowserScraper
        self.browser_scrapers['港股新上市'] = HKEXNewBrowserScraper(self.config)
        self.browser_scrapers['港股申请'] = HKEXAppBrowserScraper(self.config)
        self.browser_scrapers['纳斯达克'] = NASDAQBrowserScraper(self.config)
        self.browser_scrapers['纽交所'] = NYSEBrowserScraper(self.config)
    
    def _setup_alert_callbacks(self):
        """设置告警回调"""
        def alert_callback(exchange: str, error: str, failure_count: int):
            """告警回调函数"""
            self._send_alert(exchange, error, failure_count)
        
        # 为所有抓取器设置告警回调
        for name, scraper in self.scrapers.items():
            if hasattr(scraper, 'set_alert_callback'):
                scraper.set_alert_callback(alert_callback)
        
        # 为BrowserScraper设置告警回调
        for name, scraper in self.browser_scrapers.items():
            if hasattr(scraper, 'set_alert_callback'):
                scraper.set_alert_callback(alert_callback)
    
    def _send_alert(self, exchange: str, error: str, failure_count: int):
        """发送告警消息"""
        alert_webhook = self.config.feishu_alert_webhook
        if not alert_webhook or alert_webhook == "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_ALERT_WEBHOOK_HERE":
            self.logger.warning(f"未配置告警webhook: {exchange}")
            return
        
        try:
            import requests
            message = {
                "msg_type": "text",
                "content": {
                    "text": f"🚨 IPO监控告警\n\n交易所: {exchange}\n连续失败: {failure_count} 次\n错误: {error}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }
            response = requests.post(alert_webhook, json=message, timeout=10)
            if response.status_code == 200:
                self.logger.info(f"告警发送成功: {exchange}")
            else:
                self.logger.error(f"告警发送失败: {response.text}")
        except Exception as e:
            self.logger.error(f"发送告警异常: {e}")
    
    def run(self, test_mode: bool = False):
        """运行监控"""
        self.logger.info("=" * 50)
        self.logger.info(f"IPO监控 V2 启动 - {datetime.now()}")
        
        all_new_data: Dict[str, list] = {}
        
        # 1. 遍历各交易所抓取数据
        for name, scraper in self.scrapers.items():
            try:
                self.logger.info(f"正在抓取: {name}")
                data = scraper.fetch()
                
                # 去重
                data = self.deduplicator.deduplicate(data)
                
                all_new_data[name] = data
                self.logger.info(f"{name} - 获取 {len(data)} 条记录")
                
            except Exception as e:
                self.logger.exception(f"{name} 抓取失败: {e}")
                all_new_data[name] = []
        
        # 2. 获取上次数据，进行对比
        self.logger.info("对比数据...")
        old_data = self.storage.load_all()
        
        # 3. 计算差异
        changes = self.diff_engine.compute_diff(old_data, all_new_data)
        
        # 4. 保存新数据
        self.storage.save_all(all_new_data)
        
        # 5. 推送变化
        if test_mode:
            self.logger.info("测试模式 - 不推送")
            self._print_changes(changes)
        elif changes['has_changes']:
            self.pusher.send_daily_report(changes)
            self.logger.info("推送成功")
        else:
            self.logger.info("无新变化，跳过推送")
        
        self.logger.info(f"IPO监控 V2 完成 - {datetime.now()}")
        self.logger.info("=" * 50)
    
    def _print_changes(self, changes: Dict):
        """打印变化（测试模式）"""
        print("\n" + "=" * 50)
        print("变化内容预览:")
        print("=" * 50)
        
        if changes['added']:
            print(f"\n新增 {len(changes['added'])} 条:")
            for item in changes['added'][:5]:  # 只显示前5条
                data = item['data']
                print(f"  - {data.get('company_name')} ({data.get('stock_code')})")
        
        if changes['updated']:
            print(f"\n更新 {len(changes['updated'])} 条:")
            for item in changes['updated'][:5]:
                data = item['data']
                print(f"  - {data.get('company_name')}: {data.get('old_status')} -> {data.get('application_status')}")
        
        print("=" * 50 + "\n")
    
    def run_browser(self, browser, test_mode: bool = False):
        """使用浏览器抓取数据（需要OpenClaw browser工具）
        
        Args:
            browser: OpenClaw浏览器实例
            test_mode: 是否测试模式
        """
        self.logger.info("=" * 50)
        self.logger.info(f"IPO监控 V2 (浏览器模式) 启动 - {datetime.now()}")
        
        all_new_data: Dict[str, list] = {}
        
        # 使用BrowserFetcher抓取所有支持的交易所
        # A股交易所
        for exchange in ["上交所", "深交所", "北交所"]:
            try:
                self.logger.info(f"正在抓取(浏览器): {exchange}")
                data = self.browser_fetcher.fetch(browser, exchange)
                
                # 去重
                data = self.deduplicator.deduplicate(data)
                
                all_new_data[exchange] = data
                self.logger.info(f"{exchange} - 获取 {len(data)} 条记录")
                
            except Exception as e:
                self.logger.exception(f"{exchange} 抓取失败: {e}")
                all_new_data[exchange] = []
        
        # 港股和美股（使用BrowserScraper）
        for name, scraper in self.browser_scrapers.items():
            try:
                self.logger.info(f"正在抓取(浏览器): {name}")
                # 设置browser实例
                scraper.browser = browser
                data = scraper.fetch(browser)
                
                # 去重
                data = self.deduplicator.deduplicate(data)
                
                all_new_data[name] = data
                self.logger.info(f"{name} - 获取 {len(data)} 条记录")
                
            except Exception as e:
                self.logger.exception(f"{name} 抓取失败: {e}")
                all_new_data[name] = []
        
        # 2. 获取上次数据，进行对比
        self.logger.info("对比数据...")
        old_data = self.storage.load_all()
        
        # 3. 计算差异
        changes = self.diff_engine.compute_diff(old_data, all_new_data)
        
        # 4. 保存新数据
        self.storage.save_all(all_new_data)
        
        # 5. 推送变化
        if test_mode:
            self.logger.info("测试模式 - 不推送")
            self._print_changes(changes)
        elif changes['has_changes']:
            self.pusher.send_daily_report(changes)
            self.logger.info("推送成功")
        else:
            self.logger.info("无新变化，跳过推送")
        
        self.logger.info(f"IPO监控 V2 (浏览器模式) 完成 - {datetime.now()}")
        self.logger.info("=" * 50)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='IPO监控 V2')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--test', '-t', action='store_true', help='测试模式（不推送）')
    parser.add_argument('--daemon', '-d', action='store_true', help='守护进程模式')
    parser.add_argument('--interval', '-i', type=int, default=None, help='运行间隔（小时）')
    parser.add_argument('--browser', '-b', action='store_true', 
                       help='使用浏览器模式抓取（需要在OpenClaw环境中）')
    
    args = parser.parse_args()
    
    # 创建监控实例
    monitor = IPOMonitorV2(config_path=args.config)
    
    # 浏览器模式 - 需要检查args.browser
    if args.browser:
        # 获取browser实例（从全局变量或环境获取）
        try:
            import __main__
            if hasattr(__main__, 'browser'):
                browser = __main__.browser
            else:
                raise AttributeError("未找到browser实例")
            
            monitor.run_browser(browser, test_mode=args.test)
        except Exception as e:
            print(f"获取browser实例失败: {e}")
            print("请在OpenClaw环境中运行，并确保browser已初始化")
    else:
        # 普通模式
        if args.daemon:
            # 获取运行间隔
            interval = args.interval if args.interval else monitor.config.scheduler_interval_hours
            interval_seconds = interval * 3600
            
            monitor.logger.info(f"守护进程模式启动，每 {interval} 小时运行一次")
            
            while True:
                try:
                    monitor.run(test_mode=args.test)
                except Exception as e:
                    monitor.logger.exception(f"运行异常: {e}")
                
                monitor.logger.info(f"等待 {interval} 小时后继续...")
                time.sleep(interval_seconds)
        else:
            # 单次运行
            monitor.run(test_mode=args.test)


if __name__ == '__main__':
    main()
