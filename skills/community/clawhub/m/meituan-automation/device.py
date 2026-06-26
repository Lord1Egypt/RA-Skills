"""
设备控制层 - 通过 ADB 控制 Android 设备
不依赖截图，使用 UIAutomator XML 读取界面元素
"""
import subprocess
import xml.etree.ElementTree as ET
import json
import time
import re
from typing import Optional, List, Dict, Any


def _adb(*args, timeout=30) -> str:
    result = subprocess.run(
        ["adb", "shell"] + list(args),
        capture_output=True, text=True, timeout=timeout
    )
    return result.stdout.strip()


def _adb_raw(*args, timeout=10) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["adb"] + list(args),
        capture_output=True, text=True, timeout=timeout
    )


# ─── 屏幕信息 ────────────────────────────────────────────────────────────────

def _parse_xml_nodes(xml_str: str) -> List[Dict]:
    """从 XML 字符串解析 UI 节点列表"""
    try:
        root = ET.fromstring(xml_str)
    except Exception as e:
        return [{"error": f"XML parse failed: {e}"}]
    
    elements = []
    for node in root.iter("node"):
        attribs = node.attrib
        text = attribs.get("text", "").strip()
        desc = attribs.get("content-desc", "").strip()
        rid = attribs.get("resource-id", "")
        cls = attribs.get("class", "").split(".")[-1]
        bounds_str = attribs.get("bounds", "")
        clickable = attribs.get("clickable", "false") == "true"
        enabled = attribs.get("enabled", "true") == "true"
        scrollable = attribs.get("scrollable", "false") == "true"
        
        m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
        if not m:
            continue
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if not text and not desc and not scrollable:
            continue
        if x2 - x1 < 5 or y2 - y1 < 5:
            continue
        
        elements.append({
            "text": text, "desc": desc,
            "id": rid.split("/")[-1] if "/" in rid else rid,
            "type": cls, "cx": cx, "cy": cy,
            "w": x2 - x1, "h": y2 - y1,
            "clickable": clickable, "enabled": enabled, "scrollable": scrollable,
        })
    return elements


def dump_screen() -> List[Dict]:
    """
    读取当前屏幕所有 UI 元素，返回结构化列表。
    优先使用 uiautomator2.dump_hierarchy()（可穿透 ANR 弹窗和透明覆盖层）。
    """
    # 方式1：u2 dump（能穿透 ANR 弹窗，直接读当前焦点 Activity）
    try:
        import uiautomator2 as _u2_mod
        _d = _u2_mod.connect()
        xml_str = _d.dump_hierarchy(compressed=True)
        elements = _parse_xml_nodes(xml_str)
        if elements and not any("error" in e for e in elements):
            return elements
    except Exception:
        pass
    
    # 方式2：adb uiautomator dump（备用）
    try:
        _adb("uiautomator", "dump", "--compressed", "/sdcard/ui.xml", timeout=20)
    except subprocess.TimeoutExpired:
        subprocess.run(["adb", "shell", "pkill", "-f", "uiautomator"], capture_output=True)
        time.sleep(0.5)
        try:
            _adb("uiautomator", "dump", "/sdcard/ui.xml", timeout=15)
        except subprocess.TimeoutExpired:
            return [{"error": "uiautomator dump timeout"}]
    
    result = _adb_raw("pull", "/sdcard/ui.xml", "/tmp/mt_ui.xml")
    
    try:
        with open("/tmp/mt_ui.xml", "r", encoding="utf-8") as f:
            xml_str = f.read()
        return _parse_xml_nodes(xml_str)
    except Exception as e:
        return [{"error": f"XML read failed: {e}"}]




def get_focused_app() -> str:
    """获取当前前台 App 包名"""
    out = _adb("dumpsys", "window", "|", "grep", "mCurrentFocus")
    m = re.search(r'([a-z][a-z0-9.]+)/[A-Za-z.]+', out)
    return m.group(1) if m else ""


# ─── 操作命令 ────────────────────────────────────────────────────────────────

def tap(x: int, y: int):
    """点击坐标"""
    _adb("input", "tap", str(x), str(y))
    time.sleep(0.4)


def u2_tap(x: int, y: int):
    """
    用 uiautomator2 点击坐标（比 adb tap 更可靠，能穿透 MGC 渲染的 ViewGroup）。
    如果 u2 不可用，退回到 adb tap。
    """
    try:
        import uiautomator2 as u2
        _d = u2.connect()
        _d.click(x, y)
        time.sleep(0.4)
    except Exception:
        tap(x, y)


def u2_click_viewgroup(index: int = 0) -> bool:
    """
    用 uiautomator2 点击第 index 个可点击的 ViewGroup（搜索结果卡片）。
    返回 True 表示成功点击。
    """
    try:
        import uiautomator2 as u2
        _d = u2.connect()
        els = _d.xpath('//android.view.ViewGroup[@clickable="true"]').all()
        if index < len(els):
            els[index].click()
            time.sleep(0.4)
            return True
        return False
    except Exception as e:
        return False



def tap_element(elements: List[Dict], keyword: str) -> bool:
    """
    按文字找元素并点击。
    keyword 可以是部分匹配的 text 或 desc。
    """
    keyword_lower = keyword.lower()
    # 优先完全匹配
    for el in elements:
        if el["text"].lower() == keyword_lower or el["desc"].lower() == keyword_lower:
            if el["enabled"]:
                tap(el["cx"], el["cy"])
                return True
    # 模糊匹配
    for el in elements:
        if keyword_lower in el["text"].lower() or keyword_lower in el["desc"].lower():
            if el["enabled"]:
                tap(el["cx"], el["cy"])
                return True
    return False


def tap_by_id(elements: List[Dict], resource_id: str) -> bool:
    """按 resource-id 找元素并点击"""
    for el in elements:
        if resource_id in el["id"]:
            if el["enabled"]:
                tap(el["cx"], el["cy"])
                return True
    return False


def type_text(text: str):
    """输入文字（支持中文，需已安装 ADBKeyboard）"""
    import base64
    b64 = base64.b64encode(text.encode('utf-8')).decode()
    subprocess.run(
        ["adb", "shell", "am", "broadcast", "-a", "ADB_INPUT_B64",
         "--es", "msg", b64],
        capture_output=True
    )
    time.sleep(0.4)


def clear_text():
    """清空当前输入框"""
    _adb("input", "keyevent", "KEYCODE_CTRL_A")
    _adb("input", "keyevent", "KEYCODE_DEL")
    time.sleep(0.2)


def press_back():
    """按返回键"""
    _adb("input", "keyevent", "KEYCODE_BACK")
    time.sleep(0.5)


def press_home():
    """按 Home 键"""
    _adb("input", "keyevent", "KEYCODE_HOME")
    time.sleep(0.5)


def swipe(direction: str = "up", distance: int = 500, duration_ms: int = 300):
    """滑动：up/down/left/right"""
    # 获取屏幕尺寸
    size_out = _adb("wm", "size")
    m = re.search(r'(\d+)x(\d+)', size_out)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (1080, 2400)
    cx, cy = w // 2, h // 2
    
    d = {
        "up":    (cx, cy + distance // 2, cx, cy - distance // 2),
        "down":  (cx, cy - distance // 2, cx, cy + distance // 2),
        "left":  (cx + distance // 2, cy, cx - distance // 2, cy),
        "right": (cx - distance // 2, cy, cx + distance // 2, cy),
    }.get(direction, (cx, cy, cx, cy))
    
    _adb("input", "swipe", str(d[0]), str(d[1]), str(d[2]), str(d[3]), str(duration_ms))
    time.sleep(0.5)


def wait_for_element(keyword: str, timeout: float = 10.0, interval: float = 0.5) -> Optional[Dict]:
    """等待某个文字元素出现，返回找到的元素"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        els = dump_screen()
        for el in els:
            if keyword.lower() in el["text"].lower() or keyword.lower() in el["desc"].lower():
                return el
        time.sleep(interval)
    return None


def handle_dialogs(max_attempts: int = 3) -> bool:
    """
    自动处理常见弹窗：安全提示、权限申请、登录引导等。
    返回 True 表示关闭了至少一个弹窗。
    """
    closed = False
    dismiss_keywords = [
        "我知道了", "知道了", "确定", "同意", "确认", "关闭",
        "跳过", "稍后", "取消", "OK", "Allow", "允许",
        "继续使用", "我已了解", "去使用", "暂不",
    ]
    block_keywords = ["请向右滑动", "身份核实", "滑块", "sslError", "无法打开"]
    
    for _ in range(max_attempts):
        els = dump_screen()
        
        # 检测是否有阻塞性弹窗
        screen_texts = " ".join(e.get("text","") + e.get("desc","") for e in els)
        
        if any(k in screen_texts for k in block_keywords):
            return False  # 需要人工处理
        
        found = False
        for keyword in dismiss_keywords:
            for el in els:
                if keyword in el.get("text","") and el.get("clickable"):
                    tap(el["cx"], el["cy"])
                    time.sleep(0.8)
                    found = True
                    closed = True
                    break
            if found:
                break
        
        if not found:
            break
    
    return closed


def wait_for_main_screen(timeout: float = 15.0) -> bool:
    """
    等待美团主界面加载完成（出现「外卖」「首页」等关键元素）
    """
    deadline = time.time() + timeout
    main_keywords = ["外卖", "首页", "团购", "我的"]
    while time.time() < deadline:
        handle_dialogs()
        els = dump_screen()
        texts = " ".join(e.get("text","") for e in els)
        if sum(1 for k in main_keywords if k in texts) >= 2:
            return True
        time.sleep(1)
    return False


def keep_screen_on():
    """
    在自动化期间保持屏幕常亮：
    1. 插电时始终保持屏幕亮（stay_on_while_plugged_in = 3）
    2. 将屏幕超时延长至 10 分钟，防止操作中途熄屏
    """
    _adb("settings", "put", "global", "stay_on_while_plugged_in", "3")
    _adb("settings", "put", "system", "screen_off_timeout", "600000")
    # 如果屏幕已经关闭，唤醒它
    _adb("input", "keyevent", "KEYCODE_WAKEUP")
    time.sleep(0.3)


def launch_meituan():
    """强制冷启动美团 App，确保从干净的主页开始（同时保持屏幕常亮）"""
    keep_screen_on()
    # 先强制停止，清除返回栈，避免恢复到上次中断的页面
    subprocess.run(["adb", "shell", "am", "force-stop", "com.sankuai.meituan"],
                   capture_output=True)
    time.sleep(1)
    subprocess.run([
        "adb", "shell", "am", "start", "-n",
        "com.sankuai.meituan/com.meituan.android.pt.homepage.activity.MainActivity"
    ], capture_output=True)
    time.sleep(4)
