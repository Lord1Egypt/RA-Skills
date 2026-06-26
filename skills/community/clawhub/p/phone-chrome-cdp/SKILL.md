---
name: phone-chrome-cdp
description: "Control Android Chrome via ADB and raw WebSocket CDP. No Playwright needed for navigate, JS injection, cookies, DOM, scroll, click."
triggers:
  - phone browser
  - mobile chrome
  - adb browser
  - phone cdp
  - 手机浏览器
---

# Phone Chrome CDP

通过 ADB 连接手机 Chrome DevTools Protocol，用原始 WebSocket 控制浏览器。

## Step 1: Setup

启动 Chrome 并转发端口：
```bash
adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main
sleep 3
adb forward --remove tcp:9222 2>/dev/null
adb forward tcp:9222 localabstract:chrome_devtools_remote
```

验证：`curl -s http://localhost:9222/json/version`

获取 tab 列表：`curl -s http://localhost:9222/json/list`

## Step 2: CDPClient Class

关键点：手动构造 WebSocket 帧，**不加 Origin 头**（Chrome Android 会拒绝带 Origin 的连接）。

```python
import socket, base64, os, struct, json, time

class CDPClient:
    def __init__(self, host, port, tab_id):
        self.sock = socket.create_connection((host, port), timeout=10)
        key = base64.b64encode(os.urandom(16)).decode()
        path = "/devtools/page/" + str(tab_id)
        req = "GET " + path + " HTTP/1.1\r\nHost: " + host + ":" + str(port) + "\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: " + key + "\r\nSec-WebSocket-Version: 13\r\n\r\n"
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        self._msg_id = 0

    def send(self, method, params=None):
        self._msg_id += 1
        cmd = {"id": self._msg_id, "method": method}
        if params:
            cmd["params"] = params
        data = json.dumps(cmd).encode()
        mask = os.urandom(4)
        frame = bytearray([0x81])
        length = len(data)
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        frame.extend(mask)
        frame.extend(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(bytes(frame))
        return self._msg_id

    def recv_until(self, target_id, timeout=10):
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.sock.settimeout(max(0.1, deadline - time.time()))
            try:
                header = self.sock.recv(2)
                if len(header) < 2:
                    continue
                length = header[1] & 0x7f
                if length == 126:
                    length = struct.unpack(">H", self.sock.recv(2))[0]
                if header[1] & 0x80:
                    self.sock.recv(4)
                data = bytearray()
                while len(data) < length:
                    chunk = self.sock.recv(length - len(data))
                    if not chunk:
                        break
                    data.extend(chunk)
                msg = json.loads(data.decode())
                if msg.get("id") == target_id:
                    return msg
            except socket.timeout:
                continue
        return None

    def drain(self, timeout=1):
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.sock.settimeout(0.1)
            try:
                self.sock.recv(4096)
            except:
                pass

    def eval_js(self, expression):
        msg_id = self.send("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        resp = self.recv_until(msg_id)
        if resp and "result" in resp:
            return resp["result"].get("result", {}).get("value")
        return None

    def navigate(self, url):
        self.send("Page.navigate", {"url": url})
        time.sleep(3)

    def close(self):
        self.sock.close()
```

## Step 3: Usage Examples

```python
cdp = CDPClient("localhost", 9222, tab_id=110)

# 读页面信息
title = cdp.eval_js("document.title")
url = cdp.eval_js("window.location.href")

# 导航
cdp.navigate("https://www.baidu.com")

# 注入 JS 搜索
cdp.eval_js("document.querySelector('#kw').value = '美食'")
cdp.eval_js("document.querySelector('#su').click()")
time.sleep(4)

# 读搜索结果
results_json = cdp.eval_js("JSON.stringify(Array.from(document.querySelectorAll('h3 a')).slice(0,5).map(a=>({title:a.textContent,href:a.href})))")

# 读 Cookie（含 httpOnly）
cdp.send("Network.enable")
cdp.drain(0.5)
msg_id = cdp.send("Network.getAllCookies")
all_cookies = cdp.recv_until(msg_id)
cookie_count = len(all_cookies["result"]["cookies"])

# 写 Cookie
cdp.eval_js("document.cookie = 'test=hello; path=/'")

# 滚动
cdp.eval_js("window.scrollBy(0, 500)")

# 读页面文本
text = cdp.eval_js("document.body.innerText.substring(0, 2000)")

cdp.close()
```

## 截图（非 CDP）

用 adb screencap：
```bash
adb shell input keyevent KEYCODE_WAKEUP
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png ./screen.png
```

## LAN 共享

当前机器当跳板，用端口转发工具把 localhost:9222 暴露给局域网。其他机器连接 your_ip:转发端口。

## 已验证

- 导航 / 读标题URL / 注入JS / 读写Cookie / 点击 / 滚动 / 读DOM
- 截图通过 screencap（非 CDP 原生）

## 坑

1. websocket-client 库连不上（403）：因为自动加 Origin 头。用 CDPClient 手动构造帧
2. /json/list 超时：重启 Chrome
3. screencap 黑屏：先唤醒屏幕
4. Chrome 重启后 tab ID 变：重新查 tab 列表
