"""
美团高层操作封装
基于 device.py 的原子操作，提供语义化的美团业务操作

所有公开函数均返回 Python 原生类型（dict/list/bool），
便于 cli.py 直接序列化为 JSON 供 AI 消费。
"""
import time
import re
import subprocess
from typing import List, Dict, Optional
from device import (
    dump_screen, tap_element, tap, u2_tap, u2_click_viewgroup,
    type_text, clear_text,
    press_back, swipe, wait_for_element, launch_meituan,
    tap_by_id, get_focused_app
)


PACKAGE = "com.sankuai.meituan"


# --- 辅助工具 ---

def _adb_shell(*args):
    subprocess.run(["adb", "shell"] + list(args), capture_output=True)


def _get_focus() -> str:
    """返回当前前台 Activity 的 focus 字符串"""
    try:
        return subprocess.check_output(
            "adb shell dumpsys window | grep mCurrentFocus | tail -1",
            shell=True, text=True, stderr=subprocess.DEVNULL
        )
    except Exception:
        return ""


def _check_captcha() -> bool:
    """
    检测屏幕上是否出现验证码（滑块/拼图等）。
    返回 True 表示检测到验证码，需人工处理。
    """
    els = dump_screen()
    texts = " ".join((e.get("text") or "") + (e.get("desc") or "") for e in els)
    captcha_keywords = ["请向右滑动", "滑块", "拼图", "身份核实", "安全验证", "验证码", "sslError"]
    return any(k in texts for k in captcha_keywords)


# --- App 导航 ---

def ensure_meituan_open() -> bool:
    """确保美团在前台"""
    if PACKAGE not in get_focused_app():
        launch_meituan()
        time.sleep(3)
    return PACKAGE in get_focused_app()


def go_to_home() -> bool:
    """回到美团主页"""
    ensure_meituan_open()
    for _ in range(5):
        els = dump_screen()
        texts = [e["text"] for e in els]
        if any("外卖" in t for t in texts) and any("首页" in t or "美团" in t for t in texts):
            return True
        press_back()
        time.sleep(0.5)
    return False


def go_to_waimai() -> bool:
    """
    进入外卖搜索输入页（支持从 Launcher/主页/任何状态恢复）。
    返回 True 表示已就位（搜索框可用或已在搜索结果页）。
    """
    import uiautomator2 as _u2m

    ensure_meituan_open()
    time.sleep(2)

    focus = _get_focus()
    _ud = _u2m.connect()

    if "SearchActivity" in focus:
        et = _ud(className="android.widget.EditText")
        if et.exists:
            return True

    if "SearchResultActivity" in focus:
        return True

    et = _ud(className="android.widget.EditText")
    if et.exists:
        et.click()
        time.sleep(1)
        return True

    waimai_el = _ud(text="外卖")
    if waimai_el.exists:
        info = waimai_el.info
        cy = (info["bounds"]["top"] + info["bounds"]["bottom"]) // 2
        if cy > 2000:
            waimai_el.click()
            time.sleep(2)

    _ud.click(540, 330)
    time.sleep(1.5)

    et = _ud(className="android.widget.EditText")
    return et.exists


# --- 搜索 ---

import json as _json
_CACHE_FILE = "/tmp/meituan_last_results.json"

# 模块级结果缓存（search_restaurants / list_food_channel 返回后存入）
_last_results: List[Dict] = []


def _save_results(results: List[Dict]):
    """把搜索结果持久化到磁盘，供下次 CLI 调用读取。"""
    global _last_results
    _last_results = results
    try:
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            _json.dump(results, f, ensure_ascii=False)
    except Exception:
        pass


def _load_results() -> List[Dict]:
    """优先用内存缓存，内存为空时从磁盘恢复。"""
    if _last_results:
        return _last_results
    try:
        with open(_CACHE_FILE, "r", encoding="utf-8") as f:
            return _json.load(f)
    except Exception:
        return []

def search_restaurants(keyword: str, max_screens: int = 5) -> List[Dict]:
    """
    在美团「美食」频道内搜索餐厅，返回结果列表。

    路径：主页 → 美食图标（MRNStandardActivity）→ 动态找搜索框 → 输入关键词 → 回车
    该路径使用标准 TextView 渲染，可直接读取店名，无 Canvas 限制。

    返回：[{"name": str, "cx": int, "cy": int}, ...]
    """
    import uiautomator2 as _u2
    import base64
    _ud = _u2.connect()

    if _check_captcha():
        raise RuntimeError("检测到验证码，请在手机上手动完成后重试")

    # Step 1: 强制回到主页，再进入美食频道（确保从干净状态开始）
    ensure_meituan_open()
    for _ in range(6):
        f = _get_focus()
        if "MainActivity" in f:
            break
        press_back()
        time.sleep(1)

    if not go_to_food_channel():
        raise RuntimeError("无法进入美食频道，请检查美团 App 状态")

    time.sleep(1)

    # Step 2: 动态找搜索框 TextView（宽 > 400，cy < 300，有占位文字）并点击
    els_now = dump_screen()
    search_tv = next(
        (e for e in els_now
         if e.get("type") == "TextView"
         and e.get("w", 0) > 400
         and e.get("cy", 0) < 300
         and len((e.get("text") or "").strip()) > 2
         and (e.get("text") or "") not in ("搜索", "推荐", "附近", "北京")),
        None
    )
    if search_tv:
        print(f"  [search] 点击搜索框 cy={search_tv['cy']} t={search_tv['text']}")
        _ud.click(search_tv["cx"], search_tv["cy"])
    else:
        # 备用：点「搜索」按钮附近
        search_btn = _ud(text="搜索")
        if search_btn.exists:
            _ud.click(search_btn.info["bounds"]["left"] - 50, search_btn.info["bounds"]["top"] + 15)
        else:
            _ud.click(500, 200)
    time.sleep(1.5)

    # Step 3: 找 EditText 并清除
    et = _ud(className="android.widget.EditText")
    if et.exists:
        et.clear_text()
        time.sleep(0.3)
    else:
        _adb_shell("input", "keyevent", "KEYCODE_CTRL_A")
        time.sleep(0.2)
        _adb_shell("input", "keyevent", "KEYCODE_DEL")
        time.sleep(0.3)

    # Step 4: ADB 广播输入中文
    b64 = base64.b64encode(keyword.encode("utf-8")).decode()
    subprocess.run(
        ["adb", "shell", "am", "broadcast", "-a", "ADB_INPUT_B64", "--es", "msg", b64],
        capture_output=True,
    )
    time.sleep(0.8)

    # Step 5: 回车触发搜索
    _ud.press("enter")
    time.sleep(3)

    # Step 6: 验证已在搜索结果页（「地图」出现在顶部）
    els = dump_screen()
    has_map = any((e.get("text") or "") == "地图" and e.get("cy", 0) < 300 for e in els)
    if not has_map:
        # 尝试点「搜索」按钮
        search_btn = _ud(text="搜索", clickable=True)
        if search_btn.exists:
            search_btn.click()
            time.sleep(3)
        else:
            print("  [search] WARNING: 可能未进入搜索结果页")

    # 回到顶部后多屏滚动收集
    _ud.swipe(540, 800, 540, 2000, duration=0.4)
    time.sleep(1.5)

    results = _collect_restaurants_with_scroll(_ud, max_screens=max_screens)
    if not results:
        results = _parse_restaurant_list(dump_screen())
    _save_results(results)
    return results


# --- 多屏滚动收集餐厅 ---

def _collect_restaurants_with_scroll(_ud, max_screens: int = 5) -> List[Dict]:
    """
    在搜索结果页/外卖首页，通过多屏滚动收集餐厅。
    美团使用 RecyclerView 懒加载，必须滚动后等待渲染再 dump。
    """
    seen_names = set()
    all_results = []
    consecutive_empty = 0

    for screen_i in range(max_screens):
        # 等待当前屏渲染稳定
        time.sleep(1.5)
        els = dump_screen()
        page_results = _parse_restaurant_list(els)

        added = 0
        for r in page_results:
            name = r["name"]
            if name not in seen_names:
                seen_names.add(name)
                all_results.append(r)
                added += 1
                print(f"  [screen {screen_i}] 新增: {name}")

        if added == 0:
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break  # 连续 2 屏没有新增，到底了
        else:
            consecutive_empty = 0

        # 向下滑动一屏（SwipeUp），触发 RecyclerView 加载下一批
        _ud.swipe(540, 1800, 540, 800, duration=0.6)

    return all_results


# --- 解析餐厅列表 ---

def _parse_restaurant_list(elements: List[Dict]) -> List[Dict]:
    results: List[Dict] = []
    seen_names: set = set()

    texts_all = " ".join((e.get("text") or e.get("desc") or "") for e in elements)

    # ---- 路径 0: MRNStandardActivity（美食频道，包括推荐列表 & 关键词搜索结果）----
    is_mrn_list   = any("R_筛选" in (e.get("desc") or "") for e in elements)
    is_mrn_search = (
        # 搜索结果页：有「筛选」+「地图」TextView（顶部），且没有「外卖」频道底部导航
        any((e.get("text") or "") == "筛选" and e.get("cy", 0) < 400 for e in elements)
        and any((e.get("text") or "") == "地图" and e.get("cy", 0) < 300 for e in elements)
    )
    is_mrn_page = is_mrn_list or is_mrn_search
    if is_mrn_page:
        # 策略：店名 TextView 占满全宽（w >= name_min_w），且正下方160px内有评分/距离行
        cy_to_texts2: dict = {}
        for e in elements:
            t = (e.get("text") or "").strip()
            if t:
                cy_to_texts2.setdefault(e.get("cy", 0), []).append(t)

        rating_row_pat = re.compile(r"\d+\.\d+$|\d+条$|¥\d+/人|\d+\.?\d*km")

        def has_rating_below(target_cy, window=160):
            for cy, txts in cy_to_texts2.items():
                if 0 < cy - target_cy <= window:
                    for t in txts:
                        if rating_row_pat.search(t):
                            return True
            return False

        all_tv_widths = [e.get("w", 0) for e in elements if e.get("type") == "TextView"]
        max_tv_w = max(all_tv_widths) if all_tv_widths else 1080
        name_min_w = max(600, int(max_tv_w * 0.75))

        for e in elements:
            if e.get("type") != "TextView":
                continue
            t = (e.get("text") or "").strip()
            cy = e.get("cy", 0)
            w  = e.get("w", 0)
            if not t or len(t) < 4 or cy < 350:
                continue
            if w < name_min_w:
                continue
            if re.search(r"^\u3010|^\u00a5|\d+折$|^筛选$|^全部|^智能|^附近$|^推荐$|^营业", t):
                continue
            if re.search(r"套餐|单人|双人|仅堂食|自助\)|元/人|\d+人餐", t):
                continue
            if re.search(r"榜第\d+名|最高膨|拼\d+\+\d+|也要醒着|收藏\d+|限时优惠", t):
                continue
            if t not in seen_names and has_rating_below(cy):
                seen_names.add(t)
                results.append({"name": t, "cx": e["cx"], "cy": cy})

        if results:
            return results

        delivery_kws = re.compile(r"月售|分钟|配送|起送|评分|好评")
        shop_label_skip = re.compile(
            r"^24h营业$|^外卖$|^\d+折$|^减\d|^¥\d|^起送|^配送|^月售"
            r"|上榜餐厅|^神券$|^新客|^满\d|^好评率|^\d+分钟$"
        )

        # 收集页面所有文字，用于附近词判断
        all_texts_by_cy = {}
        for e in elements:
            t = e.get("text", "") or ""
            if t:
                cy = e.get("cy", 0)
                if cy not in all_texts_by_cy:
                    all_texts_by_cy[cy] = []
                all_texts_by_cy[cy].append(t)

        def has_nearby_delivery_info(target_cy):
            for cy, texts in all_texts_by_cy.items():
                if abs(cy - target_cy) < 350:
                    for t in texts:
                        if delivery_kws.search(t):
                            return True
            return False

        for e in elements:
            if e.get("type") != "ViewGroup" or not e.get("clickable"):
                continue
            # 美团餐厅卡片名字在 content-desc（desc 字段）中，text 可能为空或是标签
            # 优先用 desc，其次 text
            t = (e.get("desc") or e.get("text") or "").strip()
            if not t or len(t) < 3:
                continue
            if e.get("cy", 0) < 400:
                continue
            if shop_label_skip.search(t):
                continue
            if not re.search(r"[一-鿿]{2,}", t):
                continue
            # 必须周围有配送/月售等信息才是真餐厅卡片
            if has_nearby_delivery_info(e["cy"]):
                results.append({"name": t, "cx": e["cx"], "cy": e["cy"]})

        if results:
            return results

    price_pat = re.compile(r"起送¥?(\d+)|¥(\d+(?:\.\d+)?)")
    time_pat = re.compile(r"(\d+)\s*分钟")
    rating_pat = re.compile(r"^(\d+\.\d+)$")

    skip_words = {
        "外卖","团购","地点","笔记","全部","综合排序","问小团",
        "首页","推荐","视频","小团","购物车","我的","返回","搜索",
        "历史搜索","发现","我的频道","综合","距离","评分","价格",
        "门店上新","麻辣拌","杨国福","东北麻辣烫","刘文祥",
    }
    skip_patterns = [
        re.compile(r"^\d+h营业$"), re.compile(r"折$"),
        re.compile(r"^起送¥"), re.compile(r"人气榜"),
        re.compile(r"^\d+分钟"), re.compile(r"^配送"),
        re.compile(r"月售\d+"), re.compile(r"^\d+\.\d+分$"),
        re.compile(r"东里$|南里$|北里$|小区$|大厦$|路$|街$"),
        re.compile(r"^\d+%推荐"), re.compile(r"\d+条真实评价"),
        re.compile(r"^[①②③④⑤]"), re.compile(r"^(新客|限时|满减|优惠|特惠)"),
        re.compile(r"点评收录\d+年"), re.compile(r"收录\d+年"),
        re.compile(r"综合\d+条"), re.compile(r"^\d+\.\d+$"),
        re.compile(r"按住说话|发消息"), re.compile(r"选择超丰富|总有一款|推荐"),
        re.compile(r"^0元起送$|^减配送费$|^进店领券$|^领券$|^立减$"),
        re.compile(r"^休息中$|^暂停营业$"),
        re.compile(r"较少|为你推荐以下"),
        re.compile(r"^\d+元起送$"),       # "18元起送"
        re.compile(r"^最近\d+小时"),      # "最近3小时13人下单"
        re.compile(r"人下单$|人已下单$"),  # "8人下单"
        re.compile(r"^会常回购$|^支持自取$|^支持自取$|^可开发票$|^放心吃$"),
        re.compile(r"^\.\.|^【需加购】"),  # 菜品描述
        re.compile(r"^(招牌|卤香|沙县|炒米|鸭腿|鸡腿|红烧|大排|拌面|锅贴|米饭)"),  # 菜品名
        re.compile(r"折$"),               # "7.1折"
        re.compile(r"^减\d"),             # "减11.8"
        re.compile(r"^¥\d"),              # "¥22"
        re.compile(r"^[①②③④⑤⑥⑦⑧⑨⑩]"),  # 排行序号
        re.compile(r"^(起送|配送|月售|评分|距您|好评|商家|口碑|销量|热销|爆款)"),
        re.compile(r"总有一款能"),
    ]

    def is_skip(text):
        if text in skip_words:
            return True
        return any(p.search(text) for p in skip_patterns)

    def extract_info(el):
        info = {}
        for n in elements:
            if n is el:
                continue
            if abs(n["cy"] - el["cy"]) > 200:
                continue
            t = (n.get("text") or "").strip()
            if not t:
                continue
            if price_pat.search(t) and "price" not in info:
                info["price"] = t
            tm = time_pat.search(t)
            if tm and "delivery_time" not in info:
                info["delivery_time"] = tm.group(0)
            rm = rating_pat.match(t)
            if rm and "rating" not in info:
                info["rating"] = t
        return info

    for el in elements:
        # text 或 desc（content-desc）都可能带文字
        text = (el.get("text") or el.get("desc") or "").strip()
        text = re.sub(r"^[\*\*\*\•·\s]+", "", text).strip()
        if not text or len(text) < 3:
            continue
        if not re.search(r"[\u4e00-\u9fff]{2,}", text):
            continue
        if is_skip(text):
            continue
        if len(text) > 35:
            continue
        if text in seen_names:
            continue
        if el.get("cy", 0) < 600:
            continue

        if el.get("clickable"):
            cx, cy = el["cx"], el["cy"]
        else:
            tap_el = None
            for card in elements:
                if card.get("clickable") and card.get("type", "") in ("ViewGroup", "FrameLayout"):
                    if abs(card["cy"] - el["cy"]) < 200:
                        tap_el = card
                        break
            cx = tap_el["cx"] if tap_el else el["cx"]
            cy = tap_el["cy"] if tap_el else el["cy"]

        info = {"name": text, "cx": cx, "cy": cy}
        info.update(extract_info(el))
        seen_names.add(text)
        results.append(info)

    results.sort(key=lambda x: x["cy"])
    return results


# --- 进入餐厅 ---

def open_restaurant(name_or_idx) -> bool:
    """
    打开一家餐厅（按名字或列表序号）。
    - MRNStandardActivity：用 u2 xpath 找店名 TextView 并点击（精准、不依赖坐标）
    - SearchResultActivity（旧路径）：用大卡片 ViewGroup 索引点击
    - 其他页面：按坐标点击
    """
    import uiautomator2 as _u2
    _ud = _u2.connect()

    focus = _get_focus()
    is_mrn = "MRNStandardActivity" in focus

    # ---- MRN 页面（美食频道 / 搜索结果）----
    if is_mrn:
        # 优先用磁盘/内存缓存（避免进程间 index 错位）
        cache = _load_results()
        if isinstance(name_or_idx, int):
            if cache and name_or_idx < len(cache):
                target_name = cache[name_or_idx]["name"]
                print(f"  [open] 从缓存读取: [{name_or_idx}] {target_name}")
            else:
                # 没缓存则滚到顶部重新解析
                _ud.swipe(540, 800, 540, 2000, duration=0.4)
                time.sleep(1.5)
                els = dump_screen()
                restaurants = _parse_restaurant_list(els)
                if name_or_idx >= len(restaurants):
                    return False
                target_name = restaurants[name_or_idx]["name"]
        else:
            target_name = str(name_or_idx)

        # 尝试直接找目标 TextView，找不到则多次往上滑回顶部
        for _scroll_try in range(6):
            tv_el = _ud.xpath(f'//android.widget.TextView[@text="{target_name}"]')
            if tv_el.exists:
                info = tv_el.info
                bounds = info.get("bounds", {})
                cy = (bounds.get("top", 0) + bounds.get("bottom", 0)) // 2
                if 350 < cy < 2200:
                    break
            _ud.swipe(540, 600, 540, 2100, duration=0.5)  # 手指往下，内容向上滚回
            time.sleep(1.2)

        if tv_el.exists:
            # 再次确认坐标，避免点击屏幕外的元素
            info = tv_el.info
            bounds = info.get("bounds", {})
            cy = (bounds.get("top", 0) + bounds.get("bottom", 0)) // 2
            if 350 < cy < 2200:
                tv_el.click()
            else:
                _ud.click(540, cy) # 尽力点击
            time.sleep(3)
            new_focus = _get_focus()
            # 判断进店成功：Activity 变了（其他 Activity）或者页面内容变成餐厅详情
            if "MRNStandardActivity" not in new_focus:
                return True
            # 如果还在 MRNStandardActivity（堂食/团购页），检查是否有「菜品」「外卖」标签
            els_after = dump_screen()
            has_restaurant_ui = any(
                (e.get("text") or "") in ("菜品", "外卖", "点菜", "菜单", "买单", "排队")
                for e in els_after
            )
            return has_restaurant_ui
        print(f"  [open] 未找到店名 TextView: {target_name}")
        return False

    # ---- SearchResultActivity（旧路径）----
    in_search_result = "SearchResultActivity" in focus or "SearchActivity" in focus
    if in_search_result and isinstance(name_or_idx, int):
        vg_els = _ud.xpath('//android.view.ViewGroup[@clickable="true"]').all()
        shop_cards = [el for el in vg_els
                      if (el.info["bounds"]["bottom"] - el.info["bounds"]["top"]) > 200
                      and (el.info["bounds"]["right"] - el.info["bounds"]["left"]) > 500]
        print("  找到 " + str(len(shop_cards)) + " 个外卖店铺卡片")
        if name_or_idx < len(shop_cards):
            shop_cards[name_or_idx].click()
            time.sleep(3)
            return True
        return False

    # ---- 通用：按坐标点击 ----
    els = dump_screen()
    if isinstance(name_or_idx, int):
        restaurants = _parse_restaurant_list(els)
        if name_or_idx < len(restaurants):
            r = restaurants[name_or_idx]
            u2_tap(r["cx"], r["cy"])
            time.sleep(2)
            return True
        return False
    else:
        for el in els:
            if str(name_or_idx) in (el.get("text", "") or ""):
                u2_tap(el["cx"], el["cy"])
                time.sleep(2)
                return True
        return tap_element(els, str(name_or_idx))


# --- 菜单 ---

def go_to_waimai_menu() -> bool:
    """
    在餐厅详情页（MRN团购/堂食页）中，点击「外卖」入口跳转到外卖点菜页。
    返回 True 表示已进入外卖点菜页。
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    # 多种外卖入口的可能文字
    for label in ("外卖", "点外卖", "去点餐", "开始点餐"):
        el = _ud(text=label)
        if el.exists:
            el.click()
            time.sleep(3)
            # 等待点菜 Tab 出现
            if _ud(text="点菜").exists or _ud(text="菜单").exists:
                return True
            # WMRestaurantActivity 也算成功
            if "WMRestaurant" in _get_focus() or "Restaurant" in _get_focus():
                return True

    # 备用：找含「外卖」文字的 clickable 元素
    els = dump_screen()
    for e in els:
        t = (e.get("text") or "").strip()
        if "外卖" in t and e.get("clickable"):
            u2_tap(e["cx"], e["cy"])
            time.sleep(3)
            return True

    return False


def get_menu() -> List[Dict]:
    """
    获取当前餐厅外卖菜单。
    - 若在餐厅详情页（团购/堂食），先自动点击「外卖」入口
    - 若已在外卖点菜页，直接读取

    返回：[{"name": str, "price": float, "cx": int, "cy": int}, ...]
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    # Step 1: 检查是否需要先进入外卖点菜页
    els_now = dump_screen()
    in_waimai_order = any(
        (e.get("text") or "") in ("点菜", "菜单", "加入购物车")
        for e in els_now
    )
    if not in_waimai_order:
        # 尝试跳转到外卖点菜页
        if not go_to_waimai_menu():
            # 外卖入口不存在，尝试直接找「点菜」Tab（部分页面直接有）
            tab = _ud(text="点菜")
            if tab.exists:
                tab.click()
                time.sleep(1)

    # Step 2: 点击「点菜」Tab（确保在菜单区域）
    for label in ("点菜", "菜单"):
        tab = _ud(text=label)
        if tab.exists:
            tab.click()
            time.sleep(1.5)
            break

    # Step 3: 向上滑3次，展开更多菜品
    for _ in range(3):
        _ud.swipe(540, 1800, 540, 1000, duration=0.4)
        time.sleep(0.8)

    time.sleep(0.5)
    els = dump_screen()

    skip_category = {"猜你喜欢","门店福利","特惠套餐","直播专享","热销","精品推荐","全部","超优惠"}
    categories = [
        e for e in els
        if e.get("cx", 999) < 200
        and e.get("cy", 0) > 400
        and e.get("text", "") not in skip_category
        and re.search(r"[\u4e00-\u9fff]", e.get("text", ""))
        and 2 <= len(e.get("text", "")) <= 8
    ]

    if categories:
        cat = categories[0]
        print("  点击分类: " + cat["text"])
        _ud.click(cat["cx"], cat["cy"])
        time.sleep(2)
        els = dump_screen()

    def _merge_price(row_els: list) -> Optional[float]:
        row_right = [e for e in row_els if e.get("cx", 0) > 350]
        for e in row_right:
            t = (e.get("text") or "").strip()
            m = re.match(r"[¥￥]\s*(\d+(?:\.\d+)?)", t)
            if m:
                pv = float(m.group(1))
                if 0.5 < pv < 500:
                    return pv
        for e in row_right:
            t = (e.get("text") or "").strip()
            if re.match(r"^\d{1,3}\.\d{1,2}$", t):
                pv = float(t)
                if 0.5 < pv < 500:
                    return pv
        yuan_el = next((e for e in row_right if (e.get("text") or "").strip() in ("¥", "￥")), None)
        if yuan_el:
            yuan_y = yuan_el.get("cy", 0)
            same_line = sorted(
                [e for e in row_right
                 if abs(e.get("cy", 0) - yuan_y) < 25
                 and re.match(r"^[\d.]+$", (e.get("text") or "").strip())],
                key=lambda e: e.get("cx", 0),
            )
            parts = [e.get("text", "").strip() for e in same_line]
            if parts:
                try:
                    pv = float("".join(parts))
                    if 0.5 < pv < 500:
                        return pv
                except ValueError:
                    pass
        return None

    skip_pat = re.compile(
        r"减\d|满\d|起送|配送|\d+折|新客|回头客|条评|月售|人觉得|人已下单"
        r"|距您|分钟后|温馨提示|已选中|未选中"
        r"|单点不送|门店福利|特惠套餐|直播专享|猜你喜欢|超优惠|公益商家"
        r"|^点菜$|^评价$|^商家$|^热销$|^全部$|^推荐$|^评价\d+$|^限\d+份$"
        r"|^新客价$|^起$|^份$|^领$|加入购物车|^[¥￥]$|已含|再选|^\.$"
        r"|销量第\d|第\d+名|近期\d+|已下单|回头客推荐|\d+人觉得"
    )

    menu_items, seen = [], set()
    right_els = [e for e in els if e.get("cx", 0) > 250]

    for el in right_els:
        text = (el.get("text") or "").strip()
        if not text or not (2 <= len(text) <= 50):
            continue
        if not re.search(r"[\u4e00-\u9fff]", text):
            continue
        if skip_pat.search(text):
            continue
        if re.match(r"^[\d¥￥.,+\-\s]+$", text):
            continue
        if text in seen:
            continue
        same_block = [e for e in right_els if -20 < e.get("cy", 0) - el.get("cy", 0) < 250]
        price = _merge_price(same_block)
        if price is not None:
            seen.add(text)
            menu_items.append({"name": text, "price": price, "cx": el["cx"], "cy": el["cy"]})

    return menu_items


# --- 加购物车 ---

def add_to_cart(item_name: str) -> bool:
    """
    将菜品加入购物车（外卖点菜页）。
    策略：
    1. 先找包含 item_name 的 TextView
    2. 在其右侧 / 下方找「+」按钮（加购按钮）
    3. 如果找不到加购按钮，直接点击菜品名右侧区域
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    els = dump_screen()

    target_el = None
    # 找到菜品 TextView (排除顶部的搜索框, 搜索框 cy 通常 < 250)
    for el in els:
        if el.get("cy", 0) < 250:
            continue
        t = (el.get("text") or "").strip()
        if item_name in t and len(t) <= len(item_name) + 10:
            target_el = el
            break
    if target_el is None:
        # 模糊匹配
        for el in els:
            if item_name[:4] in (el.get("text") or ""):
                target_el = el
                break

    if target_el is None:
        return False

    cy = target_el["cy"]

    # 策略1：找到标题下方最近的「加购/选规格」按钮
    valid_btns = [
        e for e in els
        if e.get("cy", 0) > cy - 50
        and e.get("cx", 0) > 600
    ]
    
    clicked = False
    add_btn = None
    for n in sorted(valid_btns, key=lambda x: x.get("cy", 0)):
        t = (n.get("text") or "").strip()
        nid = (n.get("id") or "").lower()
        if t in ("+", "加入", "选规格", "选套餐") or "加入购物车" in t or "add" in nid or "plus" in nid:
            add_btn = n
            break

    if add_btn:
        u2_tap(add_btn["cx"], add_btn["cy"])
        time.sleep(1.0)
        clicked = True
    else:
        # 策略2：用 uiautomator2 xpath 找菜品名旁边的加购按钮
        item_safe = item_name.replace('"', '\"')
        btn = _ud.xpath(
            f'//*[contains(@text, "{item_safe}")]'
            f'/following-sibling::*[@clickable="true"]'
        )
        if btn.exists:
            btn.click()
            time.sleep(1.0)
            clicked = True
        else:
            # 策略3：点击屏幕右侧对应高度的区域 (假设按钮在最右侧，稍微往下偏移以应对副标题)
            u2_tap(950, cy + 100)
            time.sleep(1.0)
            clicked = True
            
    if clicked:
        # 很多时候点击 + 号会弹出一个详情或者规格选择弹窗，里面需要再次点击「加入购物车」或「选好了」
        time.sleep(1.5)  # 等待弹窗动画
        confirm_btn = _ud(textMatches="加入购物车|选好了")
        if confirm_btn.exists:
            confirm_btn.click()
            time.sleep(1.5)
            
        # 如果点击后弹窗仍未关闭（比如瑞幸允许多次加购不同规格，按钮变成 - 1 +），通过寻找关闭按钮来关闭它
        close_btn = _ud(descriptionContains="关闭")
        if close_btn.exists:
            close_btn.click()
            time.sleep(1.0)
        return True

    return False


# --- 购物车 ---

def view_cart() -> Dict:
    """
    查看购物车，返回 {"items": [...], "total": float, "count": int}
    - 自动点开购物车浮层（如果未展开）
    - 提取所有菜品名和总价
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    # 尝试点击底部购物车图标（外卖点菜页）
    els = dump_screen()
    # 购物车图标通常在屏幕底部中间，cy > 1800
    cart_icons = [
        e for e in els
        if e.get("cy", 0) > 1800
        and ("购物车" in (e.get("text") or "")
             or "购物车" in (e.get("desc") or "")
             or "cart" in (e.get("id") or "").lower())
    ]
    if cart_icons:
        ic = cart_icons[0]
        u2_tap(ic["cx"], ic["cy"])
        time.sleep(1.2)
        els = dump_screen()

    # 解析购物车内容
    items = []
    total = 0.0
    item_count = 0
    skip_pat = re.compile(
        r"^去结算|^结算|^合计|^小计|^配送费|^减|^优惠|^满|起送"
        r"|条评|^\d+$|^[¥￥]$|^\.$|加入购物车|购物车"
    )
    for el in sorted(els, key=lambda e: e.get("cy", 0)):
        text = (el.get("text") or "").strip()
        if not text:
            continue
        # 提取总价（右下角大价格）
        m = re.search(r"[¥￥](\d+(?:\.\d+)?)", text)
        if m and el.get("cy", 0) > 1800:
            v = float(m.group(1))
            if v > total:
                total = v
            continue
        # 过滤非菜品
        if skip_pat.search(text):
            continue
        if re.search(r"[\u4e00-\u9fff]", text) and 2 <= len(text) <= 30:
            if text not in items:
                items.append(text)
                item_count += 1

    return {"items": items, "total": total, "count": item_count}


# --- 结算 ---

def go_to_checkout() -> Dict:
    """
    点击「去结算」进入订单确认页（不自动付款）。
    返回结算页的关键信息：地址、配送时间、总价。
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    # Step 1: 先尝试点开底部购物车图标（如果未展开）
    els = dump_screen()
    cart_bar = [e for e in els if e.get("cy", 0) > 1800 and
                ("购物车" in (e.get("desc") or "") or "cart" in (e.get("id") or "").lower())]
    if cart_bar:
        u2_tap(cart_bar[0]["cx"], cart_bar[0]["cy"])
        time.sleep(1.2)
        els = dump_screen()

    # Step 2: 检测「差X元起送」或「未点必选品」情况
    all_texts = " ".join((e.get("text") or "") for e in els)
    m_min = re.search(r"还差[¥￥]?\s*(\d+(?:\.\d+)?)\s*[元]?|差[¥￥]?\s*(\d+(?:\.\d+)?)\s*[元]?起送|再加\s*[¥￥]?\s*(\d+(?:\.\d+)?)", all_texts)
    if m_min:
        gap = next(v for v in m_min.groups() if v is not None)
        return {
            "ok": False,
            "error": f"未达到起送金额，还差 ¥{gap}",
            "gap": float(gap),
            "suggestion": f"继续调用 /add_to_cart?item=XX 加菜，需再加 ¥{gap} 才能结算",
        }
        
    if "未点必选品" in all_texts:
        return {
            "ok": False,
            "error": "无法结算：未点必选品",
            "suggestion": "该餐厅有必选商品（如打包费、必选小菜等），请手动或通过加购必选品后重试",
        }

    # Step 3: 点击「去结算」
    for keyword in ["去结算", "结算", "确认订单", "提交订单"]:
        if tap_element(els, keyword):
            time.sleep(3)
            break
    else:
        # 如果循环正常结束（未触发 break，即没点到去结算）
        return {
            "ok": False,
            "error": "未找到去结算按钮，可能是购物车为空或者有未满足的条件",
        }

    # Step 4: 读取结算页信息
    els = dump_screen()
    info: Dict = {"ok": True, "page": "checkout"}
    texts = [((e.get("text") or "").strip()) for e in els if (e.get("text") or "").strip()]

    # 提取地址
    for t in texts:
        if re.search(r"[区路街道号楼]", t) and len(t) > 5:
            info["address"] = t
            break

    # 提取预计送达时间
    for t in texts:
        if re.search(r"\d+分钟|预计|送达", t):
            info["delivery_time"] = t
            break

    # 提取总价
    for t in texts:
        m = re.search(r"[¥￥](\d+\.?\d*)", t)
        if m:
            v = float(m.group(1))
            if v > 1:
                info["total"] = v
                break

    # 检查是否需要填写地址
    if not info.get("address"):
        for t in texts:
            if "添加地址" in t or "请填写" in t or "选择地址" in t:
                info["needs_address"] = True
                info["suggestion"] = "请调用 /tap?keyword=添加地址 后手动填写收货地址"
                break

    return info


def get_delivery_address() -> Dict:
    """
    读取当前外卖订单中的收货地址信息。
    若在结算页，直接读取已填写的地址。
    返回 {"address": str, "name": str, "phone": str, "saved": [...]}
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    els = dump_screen()
    result: Dict = {"ok": True}
    texts = [(e.get("text") or "").strip() for e in els if (e.get("text") or "").strip()]

    # 尝试找地址文字（包含区/路/街/号）
    for t in texts:
        if re.search(r"[区路街道号楼]", t) and len(t) > 6:
            result["address"] = t
            break

    # 找联系人姓名和手机号
    for t in texts:
        if re.match(r"^1[3-9]\d{9}$", t):
            result["phone"] = t
        elif re.match(r"^[\u4e00-\u9fff]{2,5}$", t) and len(t) <= 4:
            result.setdefault("name", t)

    # 如果没有地址，提示需要设置
    if "address" not in result:
        # 寻找「添加地址」或「请选择地址」
        for t in texts:
            if any(kw in t for kw in ("添加地址", "请选择", "新增地址", "选择地址")):
                result["needs_address"] = True
                result["suggestion"] = "请调用 /tap?keyword=添加地址 然后手动填写，或 /tap?keyword=选择地址 选择已保存地址"
                break
        if "needs_address" not in result:
            result["address"] = "未检测到地址"

    return result


def go_to_food_channel() -> bool:
    """
    进入美团「美食」频道列表页（MRNStandardActivity 的搜索/推荐列表状态）。
    这里的餐厅列表用标准 TextView 渲染，可直接读取店名。
    返回 True 表示已进入页面（有搜索框+筛选栏的列表状态）。
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    def _is_food_list_page():
        """验证是否在美食频道列表页（有搜索框）"""
        els = dump_screen()
        # 美食列表页特征：顶部有搜索框 TextView（宽 >600，cy<350）
        has_searchbar = any(
            e.get("type") == "TextView" and e.get("w", 0) > 600 and e.get("cy", 0) < 350
            and len((e.get("text") or "").strip()) > 2
            for e in els
        )
        # 有 R_筛选 描述（推荐列表）或有「筛选」+「地图」（搜索结果）
        has_filter_desc = any("R_筛选" in (e.get("desc") or "") for e in els)
        has_filter_text = any((e.get("text") or "") == "筛选" and e.get("cy", 0) < 400 for e in els)
        return "MRNStandardActivity" in _get_focus() and (has_searchbar or has_filter_desc or has_filter_text)

    if _is_food_list_page():
        return True

    # 不在正确状态，先回到主页
    ensure_meituan_open()
    for _ in range(5):
        f = _get_focus()
        if "MainActivity" in f:
            break
        press_back()
        time.sleep(1)

    # 主页可能段落到推荐区，向上滑到顶部
    _ud.swipe(540, 800, 540, 2000, duration=0.5)
    time.sleep(1.5)

    # 找「美食」图标并点击
    mf = _ud.xpath('//*[@text="美食"]')
    if mf.exists:
        mf.click()
        time.sleep(4)
        return _is_food_list_page()

    # 备用：按坐标点击（美食图标约在 cy=454, cx=331）
    _ud.click(331, 454)
    time.sleep(4)
    return _is_food_list_page()


def list_food_channel(max_screens: int = 4) -> List[Dict]:
    """
    进入美食频道并收集餐厅列表（多屏滚动）。
    返回 [{"name": str, "cx": int, "cy": int}, ...]
    """
    import uiautomator2 as _u2m
    _ud = _u2m.connect()

    if not go_to_food_channel():
        return []

    # 回到页面顶部
    _ud.swipe(540, 800, 540, 2000, duration=0.5)
    time.sleep(2)

    return _collect_restaurants_with_scroll(_ud, max_screens=max_screens)



# --- 状态查询 ---

def get_app_state() -> Dict:
    """
    返回当前 App 状态，供 AI 判断下一步操作。
    返回：{"activity": str, "page": str, "screen_texts": [...]}
    page 枚举：home / search_input / search_results / restaurant_menu / cart / checkout / order / meituan_other / unknown
    """
    focus = _get_focus()
    pkg = get_focused_app()
    els = dump_screen()
    texts = [e["text"] for e in els if e.get("text")][:30]

    page = "unknown"
    if "SearchResultActivity" in focus:
        page = "search_results"
    elif "SearchActivity" in focus:
        page = "search_input"
    elif "MRNStandardActivity" in focus:
        page = "food_channel"
    elif "WMRestaurantActivity" in focus:
        page = "waimai_restaurant_list"
    elif "MainActivity" in focus or "HomeActivity" in focus:
        page = "home"
    elif any("菜单" in t or "点菜" in t for t in texts):
        page = "restaurant_menu"
    elif any("去结算" in t or "确认订单" in t for t in texts):
        page = "checkout"
    elif any("购物车" in t for t in texts):
        page = "cart"
    elif any("订单" in t for t in texts):
        page = "order"
    elif PACKAGE in pkg:
        page = "meituan_other"

    return {"package": pkg, "activity": focus.strip(), "page": page, "screen_texts": texts}
