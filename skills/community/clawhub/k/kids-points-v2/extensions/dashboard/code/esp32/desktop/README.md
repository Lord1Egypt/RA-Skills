# 桌面 dashboard ESP32 (M1.3 v1)

> P2 128×96 LED 矩阵 + Flymara ESP32-HUB75E, 业务层 1:1 复用 `code/sim/desktop_sim.py`

## 📋 状态

- **M1.3 v1 完成**: HUB75 + WiFi + 30s 拉 + WS 收 + 4 区渲染 + 关蓝 + OTA + 自动重连 ✓
- **编译验证**: ⚠️ 待 M1.4 烧录时用 Arduino IDE 编译 (本机无 arduino-cli)
- **烧录**: 📋 阻塞 Q4.1 (板到货)

## 🛠️ 库依赖 (Arduino IDE Library Manager 装)

| 库 | 版本 | 用途 |
|---|---|---|
| **ESP32-HUB75-MatrixPanel-DMA** (mrcodetastic) | latest | HUB75 DMA 驱动, 1/32 扫, 关蓝 |
| **ArduinoJson** (Benoit Blanchon) | 6.x | JSON 解析 (跟 server.py schema 一致) |
| **ESPAsyncWebServer** (ESP32Async) | latest | 异步 HTTP + WebSocket (80 端口) |
| **AsyncTCP** (ESP32Async) | latest | ESPAsyncWebServer 依赖 |
| U8g2 (olikraus) | latest | CJK 像素字体 (chinese1 12x13 ~14KB Flash, 1000 chars) |
| **U8g2_for_Adafruit_GFX** (olikraus) | latest | U8g2 字体桥接到 Adafruit_GFX (HUB75 库用 GFX API) |
| ArduinoOTA | (内置) | Wi-Fi 推更新, 0 线 |

> **板支持**: ESP32 Dev Module (Flymara ESP32-HUB75E 用 ESP32-WROOM-32)

## ⚙️ 编译配置

- **Board**: ESP32 Dev Module
- **Flash Size**: 4MB (32Mb)
- **Partition Scheme**: Default 4MB with spiffs
- **Upload Speed**: 921600
- **CPU Frequency**: 240MHz

## 🚀 烧录步骤 (M1.4 实施)

- 打开 Arduino IDE / arduino-cli, 装 6 个库
- 打开 `desktop.ino` (跟目录同名, arduino-cli 编译要求)
- **DONE**: 其它 config 都已写好 (WIFI_PASS=[YOUR_WIFI_PASSWORD], SERVER_HOST=YOUR_SERVER_IP, DASHBOARD_TITLE, BRIGHTNESS=80)
- 板插 USB-C, 选对应 COM 端口
- 点 "Upload" (IDE) 或 `arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 .` 烧录
- 串口监视器 (115200 baud) 看启动日志:
   ```
   === desktop-dashboard M1.3 v1 (2026-06-15) ===
   [wifi] 连 YOUR_WIFI_SSID...
   [wifi] 连上, IP=192.168.x.x
   [ws] 服务起, /ws /setup /refresh /health
   [ota] ArduinoOTA 起, 主机名 dashboard-esp32
   [fetch] OK: balance=20, today_count=0, today_net=0, recent=0
   ```

## 🌐 调试接口 (Wi-Fi 连上后)

| 路径 | 用途 |
|---|---|
| `http://<ESP32-IP>/health` | 返 `{"ok":true,"ip":"..."}` 健康检查 |
| `http://<ESP32-IP>/refresh` | 触发立即拉 1 次 /api/dashboard |
| `http://<ESP32-IP>/setup?brightness=128` | 调亮度 (0-255, 调试用) |
| `ws://<ESP32-IP>/ws` | WebSocket, 服务器推 `{"type":"refresh"}` 时板立即拉 |

## 📺 4 区布局 (跟 sim 横版 1:1)

```
物理 128×96 像素:
┌──────────────────────────────┐ y=0
│ KID POINTS                   │ TITLE_Y=4 (1 字符 6 物理 px)
├──────────────────────────────┤ DIVIDER_1_Y=22
│ +1 06-14 [zh 2]              │ ROW_1_Y=28
│ -5 06-12 吃萨莉亚 → [zh 4]   │ ROW_2_Y=44
│ +3 06-10 ABC Reading         │ ROW_3_Y=60
├──────────────────────────────┤ DIVIDER_2_Y=78
│ TODAY +1   TOTAL 20          │ FOOTER_Y=82
└──────────────────────────────┘ y=96
```

## ⚠️ v1 已知限制 (M1.3 之后迭代)

1. **中文 description 显示为 `[zh N]` 占位**:
   - 原因: v1 只用 Adafruit GFX 5x7 内置字体, 不支持 CJK
   - 占位提示老王: "这行有 N 个中文字符" (隐式提示"看仿真去")
   - v1.1 改进: 加 u8g2 12x12 中文字体 (高频 200 字 PROGMEM, ~10KB Flash, ESP32 4MB 装得下)
2. **字号偏小** (5x7 物理 1px):
   - 仿真用 36/24/20 屏像素, ESP32 端用 5x7 GFX 物理 1px
   - 实际上 ESP32 端可用 setTextSize(2) 把 GFX 字体放大 1 档
   - v1.1 改进: 字号对齐 sim (setTextSize 2 / 1 / 1)
3. **Wi-Fi 密码硬编码**:
   - v1 用 const char*, 烧录时改
   - v1.1 改进: WiFiManager (配网页, 不重烧)
4. **无 NTP 时间同步**:
   - 板不显示真实时间, last_updated 是字符串
   - v1.1 改进: 加 NTPClient 显示"最近更新: 12:30"

## 🔄 跟 sim 的对应关系

| 业务逻辑 | sim (`desktop_sim.py`) | ESP32 (`.ino`) |
|---|---|---|
| 4 区 y 坐标 | `ORIENTATION_CONFIGS["horizontal"]` | `#define TITLE_Y/ROW_*_Y/DIVIDER_*_Y/FOOTER_Y` |
| 数据获取 | `cli_call` (subprocess) + `fetch_data` | `fetch_dashboard` (HTTP GET /api/dashboard) |
| 渲染 | `pygame.draw.rect/line/blit` | `dma_display->fillScreen/drawFastHLine/print` |
| 30s 拉 | `RELOAD_INTERVAL = 30` | `FETCH_INTERVAL_MS = 30000` |
| 错误状态 | 标题 + 错误 + "TODAY --" 底栏 | 同 |
| 占位 | 暗琥珀 `COLOR_AMBER_DIM` | 同 |

## 📚 参考

- `docs/plan.md` § 5 显示布局 (横/竖 2 套)
- `code/sim/desktop_sim.py` 业务层 1:1
- `code/server/server.py` 数据源 / 推信号格式
- `code/server/data_source.py` V2 CLI 包装层
- 飞书云文档: https://test-dgrzdllex625.feishu.cn/docx/UcvcdCRK1oKW2zxwEFQcChlzn6e
