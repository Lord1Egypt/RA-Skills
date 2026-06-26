MT4 File-Based Bridge Client
Python -> JSON file -> MT4 EA -> Response file -> Python
100% pure file I/O, no DLL imports needed
路径配置（按优先级）:
  1. MT4_BRIDGE_DIR 环境变量
  2. 默认 %APPDATA%\MetaQuotes\Terminal\Common\Files\mt4_bridge
凭证/敏感信息请使用环境变量，不要硬编码在代码中。
import os
import sys
import json
import time
import re
import logging
from ctypes import wintypes
import ctypes
# ---- 日志 ----
logger = logging.getLogger("mt4_client")
# ---- 编码处理 ----
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
# ---- 路径配置 ----
_BRIDGE_DIR = os.environ.get(
    "MT4_BRIDGE_DIR",
    os.path.expandvars(r"%APPDATA%\MetaQuotes\Terminal\Common\Files\mt4_bridge")
)
_GRID_BRIDGE_DIR = os.environ.get(
    "MT4_GRID_BRIDGE_DIR",
    os.path.expandvars(r"%APPDATA%\MetaQuotes\Terminal\Common\Files\grid_bridge")
)
REQUEST_FILE = os.path.join(_BRIDGE_DIR, "request.json")
RESPONSE_FILE = os.path.join(_BRIDGE_DIR, "response.json")
os.makedirs(_BRIDGE_DIR, exist_ok=True)
os.makedirs(_GRID_BRIDGE_DIR, exist_ok=True)
DEFAULT_TIMEOUT = 15
DEFAULT_POLL_INTERVAL = 0.2
class MT4Client:
    MT4 文件桥接客户端。
    Args:
        request_file: 请求文件路径
        response_file: 响应文件路径
        timeout: 默认超时秒数
        poll_interval: 轮询间隔秒数
    def __init__(self, request_file=REQUEST_FILE, response_file=RESPONSE_FILE,
                 timeout=DEFAULT_TIMEOUT, poll_interval=DEFAULT_POLL_INTERVAL):
        self.request_file = request_file
        self.response_file = response_file
        self.timeout = timeout
        self.poll_interval = poll_interval
    def is_ea_running(self):
        try:
            test = self.request_file + ".ping"
            with open(test, "w") as f:
                f.write("ping")
            os.remove(test)
            return True
        except OSError:
            return False
    def wait_for_ea(self, timeout=30):
        logger.info("等待 MT4 EA...（超时: %ds）", timeout)
        start = time.time()
        while time.time() - start < timeout:
            if self.is_ea_running():
                logger.info("MT4 EA 就绪")
                return True
            time.sleep(0.5)
        logger.error("MT4 EA 超时 - 是否已加载 EA？")
        return False
    def _transact(self, request, symbol=None, timeout=None, poll_interval=None):
        发送请求到 EA 并等待响应。
        Args:
            request: 请求字典
            symbol: 交易品种（用于 grid_* 动作的文件路由）
            timeout: 本次超时（秒），None 则使用实例默认值
            poll_interval: 本次轮询间隔（秒），None 则使用实例默认值
        Returns:
            响应字典，超时返回 {"status": "error", "error": "..."}
        timeout = timeout if timeout is not None else self.timeout
        poll_interval = poll_interval if poll_interval is not None else self.poll_interval
        action = request.get("action", "")
        is_grid_action = action.startswith("grid_")
        # ---- 选择文件路径 ----
        if symbol:
            fname = symbol.replace(".", "_").replace("/", "_")
            if is_grid_action:
                req_file = os.path.join(_GRID_BRIDGE_DIR, f"request_{fname}.json")
                resp_file = os.path.join(_GRID_BRIDGE_DIR, f"response_{fname}.json")
            else:
                req_file = os.path.join(_BRIDGE_DIR, f"request_{fname}.json")
                resp_file = os.path.join(_BRIDGE_DIR, f"response_{fname}.json")
        elif is_grid_action:
            return {"status": "error", "error": "grid action requires symbol parameter"}
        else:
            req_file = self.request_file
            resp_file = self.response_file
        # ---- 清理旧响应文件 ----
        _safe_remove(resp_file)
        # ---- 写入请求 ----
        try:
            with open(req_file, "w", encoding="utf-8") as f:
                json.dump(request, f, ensure_ascii=False, separators=(',', ':'))
            logger.debug("写入请求 -> %s", os.path.basename(req_file))
        except Exception as e:
            return {"status": "error", "error": f"写入请求失败: {e}"}
        # ---- 轮询等待响应 ----
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed >= timeout:
                logger.warning("请求超时（%ds）: %s", timeout, action)
                return {"status": "error", "error": f"MT4 超时 ({timeout}s)"}
            if os.path.exists(resp_file):
                try:
                    time.sleep(0.15)
                    response = _read_json_file(resp_file)
                    _safe_remove(resp_file)
                    logger.debug("收到响应（%.2fs）: %s", elapsed, action)
                    return response
                except Exception as e:
                    _safe_remove(resp_file)
                    return {"status": "error", "error": f"读取响应失败: {e}"}
            time.sleep(poll_interval)
            if int(elapsed) % 2 == 0 and elapsed > 1:
                logger.debug("等待中... %.1fs", elapsed)
    def get_price(self, symbol):
        return self._transact({"action": "get_price", "params": {"symbol": symbol}})
    def get_account_info(self):
        return self._transact({"action": "get_account_info", "params": {}})
    def get_auto_trading(self):
        return self._transact({"action": "get_auto_trading", "params": {}})
    def get_positions(self):
        return self._transact({"action": "get_positions", "params": {}})
    def buy(self, symbol, lots=0.01, price=0):
        return self._transact({
            "action": "buy",
            "params": {"symbol": symbol, "lots": str(lots), "price": str(price)}
        })
    def sell(self, symbol, lots=0.01, price=0):
        return self._transact({
            "action": "sell",
            "params": {"symbol": symbol, "lots": str(lots), "price": str(price)}
        })
    def close(self, ticket):
        return self._transact({"action": "close", "params": {"ticket": str(ticket)}})
    def close_all_buy(self):
        return self._transact({"action": "close_all_buy", "params": {}})
    def close_all_sell(self):
        return self._transact({"action": "close_all_sell", "params": {}})
    def close_all(self):
        return self._transact({"action": "close_all", "params": {}})
    def close_profit(self):
        return self._transact({"action": "close_profit", "params": {}})
    def close_loss(self):
        return self._transact({"action": "close_loss", "params": {}})
    def close_by_magic(self, magic, symbol=None):
        params = {"magic": str(magic)}
        if symbol:
            params["symbol"] = symbol
        return self._transact({"action": "close_by_magic", "params": params})
    def safe_close_all(self, symbol):
        安全平掉所有订单：先停网格再平仓，防止边平边开。
        流程：
        1. grid_close_all — 停止网格 + 平掉网格订单
        2. close_all — 平掉剩余所有订单
        即使网格 EA 没运行，第 1 步超时后第 2 步仍会执行。
        result = {"steps": []}
        r1 = self.grid_close_all(symbol=symbol, timeout=8)
        result["steps"].append({"step": "grid_close_all", "result": r1})
        grid_success = r1.get("success") is True
        if grid_success:
            time.sleep(1)
        r2 = self.close_all()
        result["steps"].append({"step": "close_all", "result": r2})
        result["grid_was_running"] = grid_success
        result["status"] = "ok"
        return result
    def get_pending_orders(self):
        return self._transact({"action": "get_pending", "params": {}})
    def cancel_pending(self, ticket):
        return self._transact({"action": "cancel_pending", "params": {"ticket": str(ticket)}})
    def buy_limit(self, symbol, lots, price, sl=0, tp=0):
        return self._transact({
            "action": "buy_limit",
            "params": {"symbol": symbol, "lots": str(lots), "price": str(price),
                       "sl": str(sl), "tp": str(tp)}
        })
    def sell_limit(self, symbol, lots, price, sl=0, tp=0):
        return self._transact({
            "action": "sell_limit",
            "params": {"symbol": symbol, "lots": str(lots), "price": str(price),
                       "sl": str(sl), "tp": str(tp)}
        })
    def buy_stop(self, symbol, lots, price, sl=0, tp=0):
        return self._transact({
            "action": "buy_stop",
            "params": {"symbol": symbol, "lots": str(lots), "price": str(price),
                       "sl": str(sl), "tp": str(tp)}
        })
    def sell_stop(self, symbol, lots, price, sl=0, tp=0):
        return self._transact({
            "action": "sell_stop",
            "params": {"symbol": symbol, "lots": str(lots), "price": str(price),
                       "sl": str(sl), "tp": str(tp)}
        })
    def modify_order(self, ticket, sl=None, tp=None):
        修改现有订单的止损和/或止盈。
        None = 保持当前值，0 = 移除。
        Args:
            ticket: 订单号
            sl: 新止损价（None=保持，0=移除）
            tp: 新止盈价（None=保持，0=移除）
        Example:
            modify_order(123456, sl=78431.86, tp=76431.86)
            modify_order(123456, sl=78000)
            modify_order(123456, tp=80000)
            modify_order(123456, sl=0)
        params = {"ticket": str(ticket)}
        if sl is not None:
            params["sl"] = str(sl)
        if tp is not None:
            params["tp"] = str(tp)
        return self._transact({"action": "modify_order", "params": params})
    def set_sl(self, ticket, sl_price):
        return self._transact({
            "action": "set_sl",
            "params": {"ticket": str(ticket), "sl": str(sl_price)}
        })
    def set_sl_all(self, symbol, sl_price):
        return self._transact({
            "action": "set_sl_all",
            "params": {"symbol": symbol, "sl": str(sl_price)}
        })
    def set_tp(self, ticket, tp_price):
        return self._transact({
            "action": "set_tp",
            "params": {"ticket": str(ticket), "tp": str(tp_price)}
        })
    def set_tp_by_profit(self, profit, sl_profit=None, symbol=None):
        params = {"profit": str(profit)}
        if sl_profit is not None:
            params["sl_profit"] = str(sl_profit)
        if symbol:
            params["symbol"] = symbol
        return self._transact({"action": "set_tp_by_profit", "params": params})
    def set_sl_tp_all(self, symbol, sl=0, tp=0):
        return self._transact({
            "action": "set_sl_tp_all",
            "params": {"symbol": symbol, "sl": str(sl), "tp": str(tp)}
        })
    def partial_close(self, ticket, lots):
        return self._transact({
            "action": "partial_close",
            "params": {"ticket": str(ticket), "lots": str(lots)}
        })
    def auto_sl(self, ticket, risk_percent=2.0):
        return self._transact({
            "action": "auto_sl",
            "params": {"ticket": str(ticket), "risk_percent": str(risk_percent)}
        })
    def trailing_stop(self, ticket, trail_distance=500):
        return self._transact({
            "action": "trailing_stop",
            "params": {"ticket": str(ticket), "trail_distance": str(trail_distance)}
        })
    def atr_sl(self, ticket, atr_period=14, atr_multiplier=2.0):
        return self._transact({
            "action": "atr_sl",
            "params": {"ticket": str(ticket), "atr_period": str(atr_period),
                       "atr_multiplier": str(atr_multiplier)}
        })
    def oco_order(self, symbol, lots, order1, order2):
        params = {
            "symbol": symbol,
            "lots": str(lots),
            "order1": {"type": order1["type"], "price": str(order1["price"])},
            "order2": {"type": order2["type"], "price": str(order2["price"])}
        }
        for key in ("sl", "tp"):
            if key in order1 and order1[key] > 0:
                params["order1"][key] = str(order1[key])
            if key in order2 and order2[key] > 0:
                params["order2"][key] = str(order2[key])
        return self._transact({"action": "oco", "params": params})
    def grid_close_all(self, symbol, timeout=None):
        return self._transact({"action": "grid_close_all"}, symbol=symbol, timeout=timeout)
    def grid_close_all_buy(self, symbol):
        return self._transact({"action": "grid_close_buy"}, symbol=symbol)
    def grid_close_all_sell(self, symbol):
        return self._transact({"action": "grid_close_sell"}, symbol=symbol)
    def grid_stop(self, symbol):
        return self._transact({"action": "grid_stop"}, symbol=symbol)
    def grid_start(self, symbol):
        return self._transact({"action": "grid_start"}, symbol=symbol)
    def grid_start_buy(self, symbol):
        return self._transact({"action": "grid_start_buy"}, symbol=symbol)
    def grid_start_sell(self, symbol):
        return self._transact({"action": "grid_start_sell"}, symbol=symbol)
    def grid_status(self, symbol):
        return self._transact({"action": "grid_status"}, symbol=symbol)
    def grid_set_sl_tp(self, symbol, tp_profit_usd=None, sl_points=None):
        params = {"symbol": symbol}
        if tp_profit_usd is not None:
            params["tp"] = str(tp_profit_usd)
        if sl_points is not None:
            params["sl"] = str(sl_points)
        return self._transact({"action": "grid_set_sl_tp", "params": params}, symbol=symbol)
    def get_history(self, days=7):
        return self._transact({
            "action": "get_history",
            "params": {"days": str(days)}
        })
    def calc_lots(self, symbol, risk_percent=1.0, sl_distance=0):
        return self._transact({
            "action": "calc_lots",
            "params": {"symbol": symbol, "risk_percent": str(risk_percent),
                       "sl_distance": str(sl_distance)}
        })
    def get_klines(self, symbol, timeframe="H1", count=10):
        return self._transact({
            "action": "get_klines",
            "params": {"symbol": symbol, "timeframe": timeframe, "count": str(count)}
        })
    def set_auto_trading(self, enabled=True):
        if enabled == "toggle":
            val = "toggle"
        else:
            val = "true" if enabled else "false"
        return self._transact({"action": "set_auto_trading", "params": {"enabled": val}})
    def toggle_auto_trading_global(self, window_title=None, desired_state=None):
        通过模拟 Ctrl+E 切换 MT4 全局自动交易。
        使用 SendInput API（替代弃用的 keybd_event）+ Alt 键技巧
        绕过前台锁限制，即使 MT4 不是活动窗口也能工作。
        Args:
            window_title: MT4 窗口标题（可选，自动检测）
            desired_state: "ON" 或 "OFF" — 先检查状态，需要时才切换
        Returns:
            {"status": "ok", "message": "..."} 或 {"status": "error", "error": "..."}
        from ctypes import wintypes
        import ctypes
        _u32 = ctypes.windll.user32
        # ---- 自动检测 MT4 窗口 ----
        if not window_title:
            window_title = self._find_mt4_window_title(_u32)
            if not window_title:
                return {"status": "error", "error": "未找到 MT4 终端窗口"}
        try:
            hwnd = _u32.FindWindowW(None, window_title)
            if not hwnd:
                return {"status": "error", "error": f"未找到窗口: {window_title}"}
            # ---- 如指定了目标状态，先检查当前状态 ----
            if desired_state and desired_state.upper() in ("ON", "OFF"):
                check = self._transact(
                    {"action": "get_terminal_auto_trading", "params": {}}
                )
                current = check.get("terminal_auto_trading", "").upper()
                if current == desired_state.upper():
                    return {"status": "ok", "message": f"已是 {desired_state.upper()}，无需切换"}
            # ---- 发送 Ctrl+E ----
            self._send_ctrl_e(_u32, hwnd)
            return {"status": "ok", "message": "Ctrl+E 已发送到 MT4 终端"}
        except Exception as e:
            logger.exception("切换自动交易失败")
            return {"status": "error", "error": str(e)}
    def _find_mt4_window_title(self, _u32):
        WNDENUMPROC = ctypes.WINFUNCTYPE(
            ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
        )
        _found = []
        def _enum_cb(hwnd, _lparam):
            length = _u32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                _u32.GetWindowTextW(hwnd, buf, length + 1)
                t = buf.value
                if "EBCFinancial" in t and "MetaEditor" not in t:
                    _found.append(t)
            return True
        _u32.EnumWindows(WNDENUMPROC(_enum_cb), 0)
        return _found[0] if _found else None
    def _send_ctrl_e(self, _u32, hwnd):
        SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001
        SPIF_SENDCHANGE = 0x0002
        _u32.SystemParametersInfoW(
            SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 0, SPIF_SENDCHANGE
        )
        VK_MENU = 0x12
        KEYEVENTF_KEYUP = 0x0002
        _u32.keybd_event(VK_MENU, 0, 0, 0)
        _u32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)
        _u32.ShowWindow(hwnd, 9)
        _u32.SetForegroundWindow(hwnd)
        _u32.BringWindowToTop(hwnd)
        time.sleep(1.0)
        INPUT_KEYBOARD = 1
        KEYEVENTF_SCANCODE = 0x0008
        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
            ]
        class INPUT_u(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT)]
        class INPUT(ctypes.Structure):
            _fields_ = [
                ("type", ctypes.c_ulong),
                ("u", INPUT_u),
            ]
        ctrl_down = INPUT()
        ctrl_down.type = INPUT_KEYBOARD
        ctrl_down.u.ki.wVk = 0x11
        ctrl_down.u.ki.dwFlags = 0
        e_down = INPUT()
        e_down.type = INPUT_KEYBOARD
        e_down.u.ki.wVk = 0x45
        e_down.u.ki.dwFlags = 0
        e_up = INPUT()
        e_up.type = INPUT_KEYBOARD
        e_up.u.ki.wVk = 0x45
        e_up.u.ki.dwFlags = KEYEVENTF_KEYUP
        ctrl_up = INPUT()
        ctrl_up.type = INPUT_KEYBOARD
        ctrl_up.u.ki.wVk = 0x11
        ctrl_up.u.ki.dwFlags = KEYEVENTF_KEYUP
        inputs = (INPUT * 4)(ctrl_down, e_down, e_up, ctrl_up)
        sent = ctypes.windll.user32.SendInput(4, ctypes.byref(inputs),
                                              ctypes.sizeof(INPUT))
        if sent != 4:
            logger.warning("SendInput 只发送了 %d/4 个输入", sent)
    def get_sr_levels(self, symbol, timeframe=60, strength=5, max_levels=5):
        tf = self._resolve_timeframe(timeframe)
        return self._transact({
            "action": "get_sr_levels",
            "params": {"symbol": symbol, "timeframe": tf,
                       "strength": strength, "max_levels": max_levels}
        })
    def draw_sr_levels(self, symbol, timeframe=60, strength=5, max_levels=5):
        tf = self._resolve_timeframe(timeframe)
        return self._transact({
            "action": "draw_sr_levels",
            "params": {"symbol": symbol, "timeframe": tf,
                       "strength": strength, "max_levels": max_levels}
        })
    @staticmethod
    def _resolve_timeframe(timeframe):
        tf_map = {
            1: 1, 5: 5, 15: 15, 30: 30,
            60: 60, 240: 240, 1440: 1440, 10080: 10080, 43200: 43200
        }
        return tf_map.get(timeframe, 60)
    def add_alert(self, symbol, condition="above", target=0, message=""):
        if not message:
            message = f"{symbol} {condition} {target}"
        return self._transact({
            "action": "add_alert",
            "params": {"symbol": symbol, "condition": condition,
                       "target": str(target), "message": message}
        })
    def list_alerts(self):
        return self._transact({"action": "list_alerts", "params": {}})
    def cancel_alert(self, slot):
        return self._transact({
            "action": "cancel_alert",
            "params": {"slot": str(slot)}
        })
    def get_notifications(self):
        return self._transact({"action": "get_notifications", "params": {}})
    def clear_chart_objects(self, symbol):
        return self._transact({
            "action": "clear_chart_objects",
            "params": {"symbol": symbol}
        })
    def draw_hline(self, symbol, name, price, color='Yellow', width=1, style='solid', label=''):
        在图表上画自定义水平线。
        参数:
            symbol: 品种名
            name: 线的名称（会自动加前缀 "HL_"）
            price: 价格位置
            color: 颜色 (Red/Green/Blue/Orange/Yellow/Cyan/Magenta/Lime/White/Gray)
            width: 线宽 (1-5)
            style: 样式 (solid/dash/dot/dashdot)
            label: 标签文字（显示在图表上）
        return self._transact({
            "action": "draw_hline",
            "params": {
                "symbol": symbol,
                "name": name,
                "price": float(price),
                "color": color,
                "width": int(width),
                "style": style,
                "label": label
            }
        })
    def clear_hline(self, symbol, prefix='HL_'):
        按前缀删除水平线。
        参数:
            symbol: 品种名
            prefix: 前缀（默认 "HL_"，删除所有 HL_ 开头的线）
        return self._transact({
            "action": "clear_hline",
            "params": {"symbol": symbol, "prefix": prefix}
        })
def _safe_remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass
def _read_json_file(filepath):
    读取 JSON 文件，自动尝试多种编码。
    EA 的 FileWriteString 输出可能为 GBK/ANSI。
    raw = None
    for enc in ['utf-8', 'gbk', 'latin-1']:
        try:
            with open(filepath, "r", encoding=enc) as f:
                raw = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if raw is None:
        raise ValueError("无法解码响应文件（尝试了 utf-8/gbk/latin-1）")
    raw = _fix_ea_json_quoting(raw)
    return json.loads(raw)
def _fix_ea_json_quoting(raw):
    修复 EA MQL4 生成的 JSON 中的双层引号问题。
    EA 端可能生成: {""status"": ""ok""} 而不是 {"status": "ok"}
    使用正则精确修复，避免破坏字符串值中的合法双引号。
    raw = re.sub(r'""(\w+)"":', r'"\1":', raw)
    raw = re.sub(r':""([^"]*?)""', r':"\1"', raw)
    raw = re.sub(r'\[""', r'["', raw)
    raw = re.sub(r'""\]', r'"]', raw)
    raw = re.sub(r',""', r',"', raw)
    raw = re.sub(r'"",', r'",', raw)
    return raw
def main():
    logger.info("=" * 50)
    logger.info("MT4 File Bridge - Python Client 测试")
    logger.info("=" * 50)
    logger.info("桥接目录: %s", _BRIDGE_DIR)
    logger.info("请求文件: %s", REQUEST_FILE)
    logger.info("响应文件: %s", RESPONSE_FILE)
    print()
    client = MT4Client()
    if not client.wait_for_ea():
        logger.error("提示: 请先在 MT4 图表上加载 mt4_bridge EA")
        return
    logger.info("[TEST] get_price(XAUUSD)...")
    r = client.get_price(symbol="XAUUSD.s")
    print(json.dumps(r, indent=2, ensure_ascii=False))
    logger.info("[TEST] get_positions()...")
    r = client.get_positions()
    print(json.dumps(r, indent=2, ensure_ascii=False))
    logger.info("[DONE]")
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        datefmt="%H:%M:%S"
    )
    main()
