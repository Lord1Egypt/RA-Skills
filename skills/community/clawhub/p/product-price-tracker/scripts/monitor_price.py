#!/usr/bin/env python3
"""
价格监控器 - 生产就绪版
结合 kimi_search + browser 实现自动价格监控
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 数据文件路径
DB_FILE = os.environ.get("PRICE_DB_FILE", "/tmp/price_monitor_db.json")
SCREENSHOT_DIR = os.environ.get("PRICE_SCREENSHOT_DIR", "/tmp/price_screenshots")

class PriceMonitor:
    def __init__(self):
        self.db_file = DB_FILE
        self.screenshot_dir = Path(SCREENSHOT_DIR)
        self._ensure_directories()
        self.data = self.load_data()
    
    def _ensure_directories(self):
        """确保数据目录存在"""
        try:
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"⚠️  创建截图目录失败: {e}")
    
    def load_data(self):
        """加载价格数据库"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️  数据库文件损坏: {e}，将创建新数据库")
        except Exception as e:
            print(f"⚠️  读取数据库失败: {e}")
        return {"products": {}, "history": []}
    
    def save_data(self):
        """保存价格数据库"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ 保存数据库失败: {e}")
            return False
        return True
    
    def add_product(self, name, url=None, search_query=None):
        """添加监控产品"""
        try:
            self.data["products"][name] = {
                "url": url,
                "search_query": search_query or f"{name} 价格",
                "added_at": datetime.now().isoformat(),
                "last_price": None,
                "last_check": None
            }
            if self.save_data():
                print(f"✅ 已添加监控: {name}")
                return True
        except Exception as e:
            print(f"❌ 添加产品失败: {e}")
        return False
    
    def search_price(self, product_name):
        """
        搜索产品价格
        
        注：此版本输出搜索建议，供 AI Agent 调用 kimi_search
        实际使用时，由 Agent 调用 kimi_search 并将结果传入 record_price
        """
        try:
            product = self.data["products"].get(product_name)
            if not product:
                print(f"❌ 未找到产品: {product_name}")
                print(f"💡 先添加产品: python3 monitor_price.py --add \"{product_name}\"")
                return None
            
            query = product.get("search_query", f"{product_name} 价格")
            print(f"🔍 搜索: {query}")
            print(f"\n💡 请让 AI Agent 执行: kimi_search(query='{query}', limit=3)")
            
            # 返回搜索参数，供外部调用
            return {
                "action": "kimi_search",
                "query": query,
                "limit": 3,
                "product": product_name
            }
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return None
    
    def record_price(self, product_name, price_data):
        """
        记录价格
        
        Args:
            price_data: dict 包含 price, source 字段
        """
        try:
            if product_name not in self.data["products"]:
                print(f"❌ 产品未添加: {product_name}")
                return False
            
            old_price = self.data["products"][product_name].get("last_price")
            new_price = price_data.get("price")
            
            # 检测价格变化
            change_info = None
            if old_price and old_price != new_price:
                change_type = "📈 上涨" if self._price_increased(old_price, new_price) else "📉 下降"
                change_info = f"{change_type}: {old_price} → {new_price}"
                print(f"{change_info}")
            elif old_price == new_price:
                print(f"➡️  价格无变化: {new_price}")
            else:
                print(f"📝 首次记录: {new_price}")
            
            # 更新数据
            self.data["products"][product_name]["last_price"] = new_price
            self.data["products"][product_name]["last_check"] = datetime.now().isoformat()
            
            # 添加到历史
            history_entry = {
                "product": product_name,
                "price": new_price,
                "source": price_data.get("source", "unknown"),
                "date": datetime.now().isoformat()
            }
            if change_info:
                history_entry["change"] = change_info
            
            self.data["history"].append(history_entry)
            
            if self.save_data():
                print(f"✅ 价格已记录")
                return True
        except Exception as e:
            print(f"❌ 记录价格失败: {e}")
        return False
    
    def _price_increased(self, old, new):
        """判断价格是否上涨（简化版）"""
        try:
            # 提取数字比较
            import re
            old_nums = re.findall(r'\d+\.?\d*', str(old))
            new_nums = re.findall(r'\d+\.?\d*', str(new))
            
            if old_nums and new_nums:
                old_num = float(old_nums[0])
                new_num = float(new_nums[0])
                return new_num > old_num
        except:
            pass
        return False
    
    def generate_report(self):
        """生成价格监控报告"""
        try:
            print("\n" + "="*60)
            print("📊 价格监控报告")
            print("="*60)
            print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-"*60)
            
            if not self.data["products"]:
                print("\n暂无监控产品")
                print(f"💡 添加产品: python3 monitor_price.py --add \"产品名称\" --url \"官网链接\"")
                return
            
            print("\n📦 监控产品列表:")
            for name, info in self.data["products"].items():
                price = info.get("last_price") or "未记录"
                last_check = info.get("last_check")
                if last_check:
                    last_check = last_check[:16].replace("T", " ")
                else:
                    last_check = "从未"
                
                print(f"\n   {name}")
                print(f"   ├─ 当前价格: {price}")
                print(f"   ├─ 最后检查: {last_check}")
                print(f"   └─ 官网: {info.get('url') or '未设置'}")
            
            # 统计
            total = len(self.data["products"])
            checked = sum(1 for p in self.data["products"].values() if p.get("last_price"))
            print(f"\n📈 统计:")
            print(f"   监控产品数: {total}")
            print(f"   已记录价格: {checked}")
            print(f"   历史记录数: {len(self.data['history'])}")
            
            print("="*60)
        except Exception as e:
            print(f"❌ 生成报告失败: {e}")
    
    def list_products(self):
        """列出所有监控产品"""
        try:
            print("\n📋 监控产品列表:")
            if not self.data["products"]:
                print("   (暂无产品)")
                return
            for name in self.data["products"]:
                print(f"   - {name}")
        except Exception as e:
            print(f"❌ 列出产品失败: {e}")
    
    def remove_product(self, name):
        """删除监控产品"""
        try:
            if name in self.data["products"]:
                del self.data["products"][name]
                if self.save_data():
                    print(f"✅ 已删除: {name}")
                    return True
            else:
                print(f"❌ 未找到产品: {name}")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="价格监控器 - 监控产品价格变化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 添加监控产品
  python3 monitor_price.py --add "Cursor Pro" --url "https://cursor.com/pricing"
  
  # 搜索价格（输出搜索建议）
  python3 monitor_price.py --search --product "Cursor Pro"
  
  # 生成报告
  python3 monitor_price.py --report
  
  # 列出所有产品
  python3 monitor_price.py --list
        """
    )
    parser.add_argument("--add", help="添加监控产品")
    parser.add_argument("--url", help="产品官网URL")
    parser.add_argument("--search", action="store_true", help="搜索产品价格建议")
    parser.add_argument("--product", help="指定产品名称")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--list", action="store_true", help="列出产品")
    parser.add_argument("--remove", help="删除监控产品")
    
    args = parser.parse_args()
    
    if not any([args.add, args.search, args.report, args.list, args.remove]):
        parser.print_help()
        sys.exit(0)
    
    try:
        monitor = PriceMonitor()
        
        if args.add:
            monitor.add_product(args.add, args.url)
        elif args.search and args.product:
            monitor.search_price(args.product)
        elif args.report:
            monitor.generate_report()
        elif args.list:
            monitor.list_products()
        elif args.remove:
            monitor.remove_product(args.remove)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
