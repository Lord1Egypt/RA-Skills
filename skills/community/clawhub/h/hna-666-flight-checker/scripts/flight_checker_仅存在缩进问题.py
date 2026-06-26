#!/usr/bin/env python3
"""
海航 666Plus 权益往返航班自动查询脚本
用于 skill: hna-666-flight-checker

版本: 2.0 (修复版)
修复内容: 根据实际页面文本修正选择器
  - "出发" -> "出发请选择出发地"
  - "到达" -> "到达请选择到达地"
  - 增加等待机制确保动态元素加载
"""

# ============================================================
# 第一部分：导入依赖
# ============================================================
from playwright.sync_api import sync_playwright  # 浏览器自动化库
import time                                         # 控制等待时间
import argparse                                     # 解析命令行参数
from typing import List, Tuple                      # 类型提示，让代码更清晰


# ============================================================
# 第二部分：定义城市映射
# ============================================================
# 这个字典存储了所有目的地的代码和中文名
# 格式：三字码: 中文名
DESTINATIONS = {
    "HAK": "海口", "YYA": "岳阳", "XNN": "西宁", "INC": "银川",
    "LHW": "兰州", "XIY": "西安", "KMG": "昆明", "CKG": "重庆",
    "CTU": "成都", "WNZ": "温州", "UYN": "榆林", "JHG": "西双版纳",
    "YIH": "宜昌", "ERL": "二连浩特", "AQG": "安庆", "FOC": "福州",
    "XMN": "厦门", "HRB": "哈尔滨", "DLC": "大连"
}

# 拼音首字母映射，用于快速输入（保留备用，但实际使用中文名）
# 格式：中文名: 拼音首字母
CITY_PINYIN = {
    "北京": "BJ", "海口": "HK", "岳阳": "YY", "西宁": "XN",
    "银川": "YC", "兰州": "LZ", "西安": "XA", "昆明": "KM",
    "重庆": "CQ", "成都": "CD", "温州": "WZ", "榆林": "YL",
    "西双版纳": "XSBN", "宜昌": "YC", "二连浩特": "ELHT",
    "安庆": "AQ", "福州": "FZ", "厦门": "XM", "哈尔滨": "HEB", "大连": "DL"
}


# ============================================================
# 第三部分：核心类 - 航班检查器
# ============================================================
class HNAFlightChecker:
    """海航 666Plus 权益航班检查器"""
    
    def __init__(self, headless: bool = False):
        """
        初始化浏览器
        
        Args:
            headless: True=后台运行（不显示窗口），False=显示浏览器窗口
        """
        # 启动 playwright 并打开浏览器
        self.playwright = sync_playwright().start()
        
        # 启动 Firefox 浏览器（你用的浏览器）
        self.browser = self.playwright.firefox.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']  # 隐藏自动化特征
        )
        
        # 创建浏览器上下文（类似一个独立的浏览器会话）
        self.context = self.browser.new_context(
            viewport={'width': 375, 'height': 667},  # 手机尺寸，适配移动端页面
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        )
        
        # 创建新页面
        self.page = self.context.new_page()
    
    # ============================================================
    # 第四部分：页面操作方法
    # ============================================================
    
    def _select_city(self, city_name: str, is_departure: bool = True):
        """
        在页面上选择城市
        
        页面使用点击文本的方式选择城市，流程：
        1. 点击"出发请选择出发地"或"到达请选择到达地"文字
        2. 在城市选择弹窗中输入城市名
        3. 点击匹配的城市结果
        
        Args:
            city_name: 城市名，如"北京"、"海口"
            is_departure: True=出发地，False=目的地
        """
        # 1. 点击正确的文字（注意：实际页面文本是完整的）
        if is_departure:
            label = "出发请选择出发地"
        else:
            label = "到达请选择到达地"
        
        # 等待文字出现并点击
        self.page.wait_for_selector(f"text={label}", timeout=5000)
        self.page.locator(f"text={label}").first.click()
        print(f"   已点击: {label}")
        time.sleep(0.8)  # 等待弹窗动画
        
        # 2. 找到城市搜索输入框并输入城市名
        # 等待输入框出现（弹窗中的输入框）
        try:
            # 尝试多种可能的输入框选择器
            input_box = self.page.locator("input[type='text']").first
            input_box.wait_for(state="visible", timeout=5000)
        except:
            # 如果找不到，尝试其他选择器
            input_box = self.page.locator("input").first
            input_box.wait_for(state="visible", timeout=5000)
        
        input_box.click()
        time.sleep(0.3)
        
        # 清空并输入城市名
        input_box.fill("")  # 清空
        time.sleep(0.2)
        input_box.fill(city_name)
        print(f"   输入城市: {city_name}")
        time.sleep(0.8)  # 等待搜索结果
        
        # 3. 点击匹配的城市选项
        self.page.locator(f"text={city_name}").first.click()
        print(f"   选择城市: {city_name}")
        time.sleep(0.5)
    
    def _select_date(self, date_str: str):
        """
        选择日期 - 适配横向滚动日历
        
        页面结构：
        - 横向滚动的时间轴，显示连续月份
        - 月份标题格式: "4月 2026年"
        - 日期格子是数字文本
        
        Args:
            date_str: 日期字符串，格式 YYYYMMDD，如 20260401
        """
        # 解析年月日
        target_year = int(date_str[:4])
        target_month = int(date_str[4:6])
        target_day = int(date_str[6:8])
        
        print(f"   目标日期: {target_year}年{target_month}月{target_day}日")
        
        # 1. 点击日期区域打开选择器
        try:
            date_display = self.page.locator("text=/\\d{2}月\\d{2}日/").first
            date_display.click()
            print(f"   已点击日期显示区域")
            time.sleep(1)
        except Exception as e:
            print(f"   点击日期失败: {e}")
            return
        
        # 2. 构建目标月份文本（支持两种格式）
        target_texts = [
            f"{target_month}月 {target_year}年",
            f"{target_month}月{target_year}年",
        ]
        
        month_found = False
        for target_text in target_texts:
            try:
                # 查找月份标题
                month_header = self.page.locator(f"text={target_text}").first
                month_header.wait_for(state="visible", timeout=3000)
                month_found = True
                print(f"   找到目标月份: {target_text}")
                
                # 滚动到目标月份
                month_header.scroll_into_view_if_needed()
                time.sleep(0.5)
                
                # 3. 在月份区域内点击目标日期
                # 获取月份标题的父容器
                month_container = month_header.locator("xpath=ancestor::div[contains(@class, 'month')]")
                if month_container.count() == 0:
                    month_container = month_header.locator("..")
                
                # 直接查找数字并点击（测试成功的方式）
                day_element = month_container.locator(f"text={target_day}").first
                day_element.click()
                print(f"   ✅ 选择日期: {target_month}月{target_day}日")
                time.sleep(0.5)
                return
                
            except Exception as e:
                print(f"   尝试 '{target_text}' 失败: {e}")
                continue
        
        if not month_found:
            print(f"   ❌ 未找到目标月份 {target_month}月 {target_year}年")
        
    
   def _select_666_rights(self):
        """
        勾选 666 权益卡
        
        页面通过点击文本的方式勾选复选框
        """
        # 先关闭可能出现的弹窗（如价格选择、提示等）
        try:
            # 检查是否有遮挡弹窗
            popup = self.page.locator(".hna-pop-wrap-div, [class*='popup'], [class*='modal']").first
            if popup.is_visible(timeout=1000):
                # 尝试点击关闭按钮
                close_btn = popup.locator("text=关闭, text=×, text=取消, text=我知道了").first
                if close_btn.is_visible():
                    close_btn.click()
                    print(f"   已关闭弹窗")
                    time.sleep(0.5)
                else:
                    # 如果没有关闭按钮，点击弹窗外区域
                    self.page.mouse.click(10, 10)
                    time.sleep(0.5)
        except:
            pass
        
        # 点击"666权益卡航班"文字（会自动勾选复选框）
        try:
            self.page.locator("text=666权益卡航班").first.click()
            print(f"   已勾选: 666权益卡航班")
        except:
            # 如果被遮挡，尝试用 JavaScript 强制点击
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
        time.sleep(0.3)
    
    
    def _click_query(self):
        """点击查询按钮"""
        self.page.locator("text=查询航班").first.click()
        print(f"   已点击: 查询航班")
        time.sleep(2)  # 等待结果加载
    
        def _has_flights(self) -> bool:
        """
        判断当前页面是否有航班
        """
        # 等待结果加载
        time.sleep(2)
        
        # 先关闭可能出现的弹窗
        try:
            popup = self.page.locator(".hna-pop-wrap-div, [class*='popup']").first
            if popup.is_visible(timeout=1000):
                close_btn = popup.locator("text=关闭, text=×, text=我知道了").first
                if close_btn.is_visible():
                    close_btn.click()
                    print(f"   已关闭结果弹窗")
                    time.sleep(0.5)
        except:
            pass
        
        # 如果出现"暂无航班"文字，说明没有航班
        if self.page.locator("text=暂无航班").count() > 0:
            return False
        
        # 检查是否有航班列表项
        flight_selectors = [
            ".flight-item",
            "[class*='flight']",
            ".flight-card",
            ".able-flight-item",
            "text=航班号",
            "text=新海航"
        ]
        
        for selector in flight_selectors:
            if self.page.locator(selector).count() > 0:
                return True
        
        return False
    
    # ============================================================
    # 第五部分：核心业务逻辑
    # ============================================================
    
    def check_route(self, orig: str, dest: str, date: str) -> bool:
        """
        检查单条航线是否有 666Plus 权益航班
        
        Args:
            orig: 出发城市名（如"北京"）
            dest: 目的地城市名（如"海口"）
            date: 日期 YYYYMMDD
        
        Returns:
            True: 有航班，False: 无航班
        """
        print(f"\n  --- 查询 {orig} → {dest} ({date[:4]}-{date[4:6]}-{date[6:8]}) ---")
        
        # 1. 访问查询页面
        self.page.goto("https://m.hnair.com/hnams/plusMember/ableAirlineQuery")
        
        # 等待页面加载完成（等待查询按钮出现）
        self.page.wait_for_selector("text=查询航班", timeout=10000)
        time.sleep(1)  # 额外等待 React 渲染
        
        # 2. 选择出发地
        self._select_city(orig, is_departure=True)
        
        # 3. 选择目的地
        self._select_city(dest, is_departure=False)
        
        # 4. 选择日期
        self._select_date(date)
        
        # 5. 勾选 666 权益
        self._select_666_rights()
        
        # 6. 点击查询
        self._click_query()
        
        # 7. 返回是否有航班
        has_flights = self._has_flights()
        print(f"  结果: {'✅ 有航班' if has_flights else '❌ 无航班'}")
        return has_flights
    
    def find_round_trip_cities(self, out_date: str, ret_date: str) -> List[Tuple[str, str]]:
        """
        找出所有可往返的城市
        
        流程：
        1. 遍历所有目的地，检查去程是否有航班
        2. 对去程有航班的目的地，检查返程是否有航班
        3. 收集去程和返程都有航班的目的地
        
        Args:
            out_date: 去程日期 YYYYMMDD
            ret_date: 返程日期 YYYYMMDD
        
        Returns:
            可往返的城市列表，每个元素为 (三字码, 中文名)
        """
        print("\n" + "="*60)
        print(f"🚀 海航 666Plus 权益航班查询")
        print(f"📅 去程日期: {out_date[:4]}-{out_date[4:6]}-{out_date[6:8]}")
        print(f"📅 返程日期: {ret_date[:4]}-{ret_date[4:6]}-{ret_date[6:8]}")
        print(f"📍 目的地数量: {len(DESTINATIONS)} 个")
        print("="*60)
        
        available_cities = []
        
        # 遍历所有目的地
        for idx, (code, name) in enumerate(DESTINATIONS.items(), 1):
            print(f"\n[{idx}/{len(DESTINATIONS)}] 检查 {name} ({code})")
            
            # 检查去程：北京 → 目的地
            has_outbound = self.check_route("北京", name, out_date)
            
            if not has_outbound:
                print(f"  ❌ {name} 去程无航班，跳过")
                continue
            
            print(f"  ✅ {name} 去程有票，继续检查返程...")
            
            # 检查返程：目的地 → 北京
            has_inbound = self.check_route(name, "北京", ret_date)
            
            if has_inbound:
                print(f"  🎉 {name} 往返均有票！")
                available_cities.append((code, name))
            else:
                print(f"  ⚠️ {name} 返程无票")
            
            # 避免请求过快，暂停 2 秒
            time.sleep(2)
        
        return available_cities
    
    def close(self):
        """关闭浏览器，释放资源"""
        print("\n关闭浏览器...")
        self.browser.close()
        self.playwright.stop()
        print("已关闭")


# ============================================================
# 第六部分：命令行入口
# ============================================================
def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description='海航 666Plus 权益往返航班查询',
        epilog='示例: python flight_checker.py --out 20260401 --ret 20260405'
    )
    parser.add_argument('--out', required=True, help='去程日期 YYYYMMDD')
    parser.add_argument('--ret', required=True, help='返程日期 YYYYMMDD')
    parser.add_argument('--headless', action='store_true', 
                        help='无头模式（不显示浏览器窗口，用于后台运行）')
    
    args = parser.parse_args()
    
    # 验证日期格式
    if len(args.out) != 8 or len(args.ret) != 8:
        print("❌ 日期格式错误，请使用 YYYYMMDD 格式，如 20260401")
        return
    if not (args.out.isdigit() and args.ret.isdigit()):
        print("❌ 日期必须为数字")
        return
    
    print("\n" + "="*60)
    print("🔧 初始化浏览器...")
    if args.headless:
        print("   模式: 无头模式（后台运行）")
    else:
        print("   模式: 有头模式（显示浏览器窗口）")
    
    # 创建检查器实例
    checker = HNAFlightChecker(headless=args.headless)
    
    try:
        # 执行查询
        results = checker.find_round_trip_cities(args.out, args.ret)
        
        # 输出结果汇总
        print("\n" + "="*60)
        print("📊 查询结果汇总")
        print("="*60)
        
        if results:
            print(f"\n✅ 找到 {len(results)} 个可往返的目的地：")
            print("-" * 40)
            for code, name in results:
                print(f"   ✈️  {name} ({code})")
        else:
            print("\n❌ 没有找到可往返的目的地")
            print("\n💡 建议：")
            print("   • 检查日期是否正确")
            print("   • 尝试其他日期")
            print("   • 确认 666Plus 权益是否有效")
            print("   • 可能该时段航班较少，建议提前查询")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("\n💡 调试建议：")
        print("   • 去掉 --headless 参数，观察浏览器操作过程")
        print("   • 如果出现验证码，手动通过后脚本会自动继续")
        print("   • 检查网络连接是否正常")
        input("\n按 Enter 退出...")
        
    finally:
        checker.close()


# 标准入口
if __name__ == "__main__":
    main()
