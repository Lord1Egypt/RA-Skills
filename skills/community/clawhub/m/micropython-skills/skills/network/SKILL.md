---
name: micropython-skills/network
description: MicroPython networking — WiFi STA/AP, HTTP requests, MQTT pub/sub, BLE, NTP time sync, WebSocket.
---

# Network

Code templates for network communication on MicroPython devices.
WiFi and network operations are **Cautious tier** — inform the user before connecting.

WiFi credentials should never be hardcoded in files saved to the device.
Use variables or prompt the user for values.

## WiFi Station Mode (Connect to Router)

```python
import network, time, json
try:
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    ssid = "YOUR_SSID"       # Replace with actual value
    password = "YOUR_PASS"   # Replace with actual value
    sta.connect(ssid, password)

    timeout = 15
    start = time.time()
    while not sta.isconnected():
        if time.time() - start > timeout:
            print("ERROR:WiFi connection timed out after " + str(timeout) + "s")
            raise SystemExit
        time.sleep(0.5)

    ip, mask, gw, dns = sta.ifconfig()
    print("RESULT:" + json.dumps({
        "ip": ip, "mask": mask, "gateway": gw, "dns": dns,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

## WiFi Access Point Mode

Create a WiFi hotspot on the device:

```python
import network, json
try:
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP32-AP", password="12345678", authmode=network.AUTH_WPA2_PSK)

    ip, mask, gw, dns = ap.ifconfig()
    print("RESULT:" + json.dumps({
        "mode": "AP",
        "ssid": "ESP32-AP",
        "ip": ip,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

## HTTP Client (urequests)

GET request:
```python
import urequests, json
try:
    r = urequests.get("http://httpbin.org/get")
    print("RESULT:" + json.dumps({
        "status": r.status_code,
        "body_preview": r.text[:200],
    }))
    r.close()
except Exception as e:
    print("ERROR:" + str(e))
```

POST with JSON:
```python
import urequests, json
try:
    data = {"sensor": "dht22", "temp": 23.5}
    r = urequests.post(
        "http://example.com/api/data",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print("RESULT:" + json.dumps({"status": r.status_code}))
    r.close()
except Exception as e:
    print("ERROR:" + str(e))
```

Note: `urequests` is included in most MicroPython firmware builds. For HTTPS, the device needs sufficient memory (ESP32 usually OK, ESP8266 may struggle).

## MQTT Publish / Subscribe

Using the built-in `umqtt.simple` module:

```python
from umqtt.simple import MQTTClient
import json, time
try:
    client = MQTTClient(
        "esp32_client",       # Client ID
        "broker.hivemq.com",  # Broker address
        port=1883,
    )
    client.connect()
    print("LOG:Connected to MQTT broker")

    # Publish
    topic = "test/esp32"
    payload = json.dumps({"temp": 23.5, "hum": 61})
    client.publish(topic, payload)

    print("RESULT:" + json.dumps({
        "action": "publish",
        "topic": topic,
        "payload": payload,
    }))

    client.disconnect()
except Exception as e:
    print("ERROR:" + str(e))
```

Subscribe with callback:
```python
from umqtt.simple import MQTTClient
import json, time
try:
    received = []

    def on_message(topic, msg):
        received.append({"topic": topic.decode(), "msg": msg.decode()})

    client = MQTTClient("esp32_sub", "broker.hivemq.com", port=1883)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(b"test/commands")
    print("LOG:Subscribed, waiting for messages...")

    # Check for messages with timeout
    deadline = time.time() + 10
    while time.time() < deadline:
        client.check_msg()
        time.sleep(0.1)
        if received:
            break

    client.disconnect()
    print("RESULT:" + json.dumps({"received": received}))
except Exception as e:
    print("ERROR:" + str(e))
```

Note: If `umqtt` is not available, install it: `mpremote mip install umqtt.simple`

## BLE (Bluetooth Low Energy)

ESP32 BLE advertising example:

```python
import bluetooth, json, struct
try:
    ble = bluetooth.BLE()
    ble.active(True)
    name = "ESP32-BLE"

    # Encode advertising payload
    adv_data = bytearray()
    # Flags
    adv_data += struct.pack("BBB", 2, 0x01, 0x06)
    # Complete name
    name_bytes = name.encode()
    adv_data += struct.pack("BB", len(name_bytes) + 1, 0x09) + name_bytes

    ble.gap_advertise(100000, adv_data)  # Advertise every 100ms

    print("RESULT:" + json.dumps({
        "ble_active": True,
        "name": name,
        "advertising": True,
    }))
except Exception as e:
    print("ERROR:" + str(e))
```

BLE scan for nearby devices:
```python
import bluetooth, json, time
try:
    ble = bluetooth.BLE()
    ble.active(True)
    devices = []

    def scan_cb(event, data):
        if event == 5:  # _IRQ_SCAN_RESULT
            addr_type, addr, adv_type, rssi, adv_data = data
            addr_hex = ":".join("{:02x}".format(b) for b in addr)
            devices.append({"addr": addr_hex, "rssi": rssi})

    ble.irq(scan_cb)
    ble.gap_scan(5000, 30000, 30000)  # Scan for 5 seconds
    time.sleep(6)

    # Deduplicate by address
    seen = {}
    for d in devices:
        if d["addr"] not in seen or d["rssi"] > seen[d["addr"]]["rssi"]:
            seen[d["addr"]] = d

    print("RESULT:" + json.dumps({"ble_devices": list(seen.values()), "count": len(seen)}))
except Exception as e:
    print("ERROR:" + str(e))
```

## NTP Time Sync

Synchronize device clock from the internet:

```python
import ntptime, time, json
try:
    ntptime.settime()
    t = time.localtime()
    print("RESULT:" + json.dumps({
        "synced": True,
        "utc": "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(*t[:6]),
    }))
except Exception as e:
    print("ERROR:NTP sync failed: " + str(e))
```

Note: Device must be connected to WiFi first. NTP uses UDP port 123.

## WebSocket (Minimal Server)

Run a simple WebSocket echo server on the device — useful for real-time data streaming to a browser:

```python
import socket, json, hashlib, binascii
try:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 8080))
    s.listen(1)
    print("LOG:WebSocket server on port 8080")
    print("RESULT:" + json.dumps({"server": "started", "port": 8080}))
    # Accept one connection for demo, then close
    # For production, use asyncio-based server
    s.close()
except Exception as e:
    print("ERROR:" + str(e))
```

For full WebSocket support, consider `micropython-async` or `microdot` framework.
