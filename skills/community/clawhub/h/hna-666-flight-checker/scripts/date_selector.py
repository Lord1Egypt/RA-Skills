#!/usr/bin/env python3
"""
日期选择模块 - 精确匹配月份内的日期
"""

import time


class DateSelector:
    def __init__(self, page):
        self.page = page
    
    def _highlight(self, element, color="red"):
        try:
            element.evaluate(f"el => el.style.border = '3px solid {color}'")
            element.evaluate(f"el => el.style.backgroundColor = 'yellow'")
        except:
            pass
    
    def select_date(self, date_str: str) -> bool:
        target_year = int(date_str[:4])
        target_month = int(date_str[4:6])
        target_day = int(date_str[6:8])
        
        print(f"   目标日期: {target_year}年{target_month}月{target_day}日")
        
        # 1. 打开日期选择器
        date_display = self.page.locator("text=/\\d{2}月\\d{2}日/").first
        date_display.click()
        print(f"   已打开日期选择器")
        time.sleep(1)
        
        # 2. 找到目标月份标题
        month_title = self.page.locator(f"text={target_month}月").first
        month_title.scroll_into_view_if_needed()
        print(f"   已滚动到 {target_month}月")
        time.sleep(0.5)
        
        # 3. 在月份标题的父容器中查找日期
        # 方法：找到包含月份标题的整个月份区块
        month_block = month_title.locator("xpath=ancestor::div[contains(@class, 'month')]")
        if month_block.count() == 0:
            month_block = month_title.locator("..")
        
        # 4. 在月份区块内，查找文本等于目标日期的元素
        # 使用精确匹配，避免点到其他月份的相同数字
        all_days = month_block.locator(".date, [class*='day'], div").all()
        
        target_element = None
        for elem in all_days:
            try:
                text = elem.inner_text().strip()
                if text == str(target_day):
                    target_element = elem
                    break
            except:
                pass
        
        if not target_element:
            print(f"   ❌ 未找到 {target_month}月{target_day}日")
            return False
        
        # 5. 滚动到目标元素并点击
        target_element.scroll_into_view_if_needed()
        self._highlight(target_element, "red")
        print(f"   ✅ 找到并高亮 {target_month}月{target_day}日")
        time.sleep(0.5)
        
        target_element.click()
        print(f"   ✅ 已点击")
        time.sleep(1)
        
        # 6. 验证
        new_date = self.page.locator("text=/\\d{2}月\\d{2}日/").first.inner_text()
        expected = f"{target_month:02d}月{target_day:02d}日"
        
        if expected in new_date:
            print(f"   ✅ 成功: {new_date}")
            return True
        else:
            print(f"   ❌ 失败: 实际 {new_date}")
            return False
    
    def get_current_date(self) -> str:
        try:
            return self.page.locator("text=/\\d{2}月\\d{2}日/").first.inner_text()
        except:
            return "未知"
