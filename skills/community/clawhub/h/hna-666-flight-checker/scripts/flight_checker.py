#!/usr/bin/env python3
"""
核心查询类：海航 666Plus 权益航班检查器
"""

from playwright.sync_api import sync_playwright
from config import DESTINATIONS, QUERY_URL
from utils import human_delay, close_popups
from date_selector import DateSelector
from city_selector import CitySelector
from debug import info, error, set_debug

class HNAFlightChecker:
    """海航 666Plus 权益航班检查器"""
    
    def __init__(self, headless: bool = False,debug: bool = False):
        if debug:
            set_debug(True)
            info("调试模式已开启")
        
        info("初始化浏览器...")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            viewport={'width': 375, 'height': 667},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        )
        self.page = self.context.new_page()
        self.destinations = DESTINATIONS
        
        # 初始化子模块
        self.date_selector = DateSelector(self.page)
        self.city_selector = CitySelector(self.page)
        
        info("浏览器初始化完成")
    
    def _select_city(self, city_name: str, is_departure: bool = True):
        """选择城市"""
        info(f"选择城市: {city_name}, {'出发' if is_departure else '到达'}")
        self.city_selector.select_city(city_name, is_departure)
    
    def _select_date(self, date_str: str):
        """选择日期"""
        print(f"   [DEBUG] 调用 select_date, date={date_str}")
        success = self.date_selector.select_date(date_str)
        if not success:
            print(f"   [DEBUG] 日期选择失败！")
        return success
    
    def _select_666_rights(self):
        """勾选 666 权益卡"""
        close_popups(self.page)
        human_delay(0.3, 0.6)
        
        self.page.evaluate("window.scrollTo(0, 0)")
        human_delay(0.5, 0.8)
        
        try:
            is_checked = self.page.evaluate("""() => {
                const spans = document.querySelectorAll('span');
                for (let span of spans) {
                    if (span.innerText === '666权益卡航班') {
                        const checkbox = span.parentElement?.querySelector('input');
                        if (checkbox) return checkbox.checked;
                    }
                }
                return false;
            }""")
            if is_checked:
                print(f"   666权益卡航班 已勾选")
                return
        except:
            pass
        
        try:
            btn = self.page.locator("text=666权益卡航班").first
            btn.wait_for(state="visible", timeout=8000)
            btn.scroll_into_view_if_needed()
            human_delay(0.3, 0.6)
            btn.click()
            print(f"   已勾选: 666权益卡航班")
            human_delay(0.5, 0.8)
        except:
            print(f"   点击失败，尝试强制勾选")
            self.page.evaluate("""() => {
                const elements = document.querySelectorAll('*');
                for (let el of elements) {
                    if (el.innerText === '666权益卡航班') {
                        el.click();
                        break;
                    }
                }
            }""")
            print(f"   已强制勾选: 666权益卡航班")
            human_delay(0.5, 0.8)
    
    def _click_query(self):
        """点击查询按钮"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        human_delay(0.5, 0.8)
        
        close_popups(self.page)
        human_delay(0.3, 0.6)
        
        try:
            btn = self.page.locator("text=查询航班").first
            btn.wait_for(state="visible", timeout=10000)
            btn.scroll_into_view_if_needed()
            human_delay(0.3, 0.6)
            btn.click()
            print(f"   已点击: 查询航班")
            human_delay(2.5, 3.5)
        except:
            print(f"   点击失败，尝试强制点击")
            self.page.evaluate("""() => {
                const btns = document.querySelectorAll('*');
                for (let btn of btns) {
                    if (btn.innerText === '查询航班') {
                        btn.click();
                        break;
                    }
                }
            }""")
            print(f"   已强制点击查询按钮")
            human_delay(2.5, 3.5)
    
    def _has_flights(self) -> bool:
        """判断是否有航班"""
        human_delay(2.0, 3.0)
        close_popups(self.page)
        
        if self.page.locator("text=暂无航班").count() > 0:
            return False
        
        flight_selectors = [
            ".flight-item", "[class*='flight']", ".flight-card",
            "text=航班号", "text=新海航", "text=海南航空"
        ]
        
        for selector in flight_selectors:
            if self.page.locator(selector).count() > 0:
                return True
        
        return False
    
    def check_route(self, orig: str, dest: str, date: str) -> bool:
        """检查单条航线"""
        print(f"\n  --- 查询 {orig} → {dest} ({date[:4]}-{date[4:6]}-{date[6:8]}) ---")
        
        self.page.goto(QUERY_URL)
        human_delay(1.5, 2.0)
        self.page.wait_for_selector("text=查询航班", timeout=15000)
        human_delay(0.5, 1.0)
        
        self._select_city(orig, is_departure=True)
        self._select_city(dest, is_departure=False)
        
        # 在选择日期前，打印当前页面日期
        current = self.page.locator("text=/\\d{2}月\\d{2}日/").first.inner_text()
        print(f"   [DEBUG] 选择日期前: {current}")
        
        self._select_date(date)
        
        # 选择日期后，打印日期是否更新
        after = self.page.locator("text=/\\d{2}月\\d{2}日/").first.inner_text()
        print(f"   [DEBUG] 选择日期后: {after}")
        
        human_delay(1.0, 1.5)
        close_popups(self.page)
        
        self._select_666_rights()
        self._click_query()
        
        human_delay(1.0, 1.5)
        close_popups(self.page)
        
        has_flights = self._has_flights()
        print(f"  结果: {'✅ 有航班' if has_flights else '❌ 无航班'}")
        return has_flights
    
    def find_round_trip_cities(self, out_date: str, ret_date: str):
        """找出所有可往返的城市"""
        print("\n" + "="*60)
        print(f"🚀 海航 666Plus 权益航班查询")
        print(f"📅 去程日期: {out_date[:4]}-{out_date[4:6]}-{out_date[6:8]}")
        print(f"📅 返程日期: {ret_date[:4]}-{ret_date[4:6]}-{ret_date[6:8]}")
        print(f"📍 目的地数量: {len(self.destinations)} 个")
        print("="*60)
        
        available_cities = []
        
        for idx, (code, name) in enumerate(self.destinations.items(), 1):
            print(f"\n[{idx}/{len(self.destinations)}] 检查 {name} ({code})")
            
            has_outbound = self.check_route("北京", name, out_date)
            if not has_outbound:
                print(f"  ❌ {name} 去程无航班，跳过")
                continue
            
            print(f"  ✅ {name} 去程有票，继续检查返程...")
            human_delay(2.0, 3.0)
            
            has_inbound = self.check_route(name, "北京", ret_date)
            if has_inbound:
                print(f"  🎉 {name} 往返均有票！")
                available_cities.append((code, name))
            else:
                print(f"  ⚠️ {name} 返程无票")
            
            human_delay(2.5, 4.0)
        
        return available_cities
    
    def close(self):
        """关闭浏览器"""
        print("\n关闭浏览器...")
        try:
            self.browser.close()
        except:
            pass
        self.playwright.stop()
        print("已关闭")
