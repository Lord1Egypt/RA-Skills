#!/usr/bin/env python3
"""
城市选择模块
专门处理城市选择器的操作
"""

from utils import human_delay


class CitySelector:
    """城市选择器"""
    
    def __init__(self, page):
        self.page = page
    
    def select_city(self, city_name: str, is_departure: bool = True):
        """选择城市"""
        label = "出发请选择出发地" if is_departure else "到达请选择到达地"
        
        self.page.wait_for_selector(f"text={label}", timeout=8000)
        self.page.locator(f"text={label}").first.click()
        print(f"   已点击: {label}")
        human_delay(0.8, 1.2)
        
        input_box = self.page.locator("input").first
        input_box.wait_for(state="visible", timeout=5000)
        input_box.click()
        human_delay(0.3, 0.6)
        input_box.fill(city_name)
        print(f"   输入城市: {city_name}")
        human_delay(0.8, 1.2)
        
        self.page.locator(f"text={city_name}").first.click()
        print(f"   选择城市: {city_name}")
        human_delay(0.5, 0.8)
