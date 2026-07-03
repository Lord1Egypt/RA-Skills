# 踩坑史 (Pitfalls) — M1.4 永久 Lesson

> 烧了 24+ 次才搞定的 M1.4 96×128 HUB75 LED 矩阵屏, 6/3 决定方案, 6/19 落地 v4.9。
> 这些坑**任何 ESP32 + LED 矩阵项目**都会再遇到, 留作永久 lesson。

---

## 🔴 Root Cause #1: erase_flash 破坏 NVS (WiFi 密码丢)

### 现象
- 烧完 ESP32, 串口反复打 `WiFi.status()=6` (WL_DISCONNECTED)
- 跑 wifitest scan 能看到 SSID, 但 begin() 失败
- 串口报 `NVS ret=101` 或 `nvs_open failed`

### 根因
- `esptool erase_flash` 把整个 flash (包括 NVS 分区) 抹了
- WiFi 密码存在 NVS, 没了就只剩 SSID, begin() 永连不上
- arduino-cli `upload` 默认也调 `erase_flash` (不调 --no-erase 的版本)

### 解决 (3 选 1)
1. **烧 wifitest.ino 重建 NVS** (推荐, 快)
   ```bash
   arduino-cli compile --fqbn esp32:esp32:esp32 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/wifitest
   esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x10000 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/wifitest/wifitest.ino.bin
   # 烧完按 EN, 串口看 "连上 IP=..."
   ```
2. **Preferences → WiFi 重新配** (ESP32 Arduino 库自带的 WiFi config portal, 慢)
3. **写代码 hardcode 密码** (最暴力, 不依赖 NVS)

### 永久 lesson
> **永远不要 erase_flash**. 如果一定要, 准备 wifitest 重灌脚本。

---

## 🔴 Root Cause #2: AsyncWebServer + I2S DMA 共存 → KABOOM

### 现象
- 烧了 v1.1 + AsyncWebServer + ArduinoOTA
- 启动时 `I2S allocation failed` → `KABOOM!` → 死循环
- 或跑 5 分钟后随机重启 / 花屏

### 根因
- HUB75 LED 矩阵的 I2S DMA driver 需要连续 RAM buffer (一帧 96×128/8 = 1536 bytes × 2 buffer = 3072 bytes, 加上 frame state 实际 ~24KB)
- ESP32 RAM 320KB, 看似够, 但 AsyncWebServer + ArduinoOTA 占 ~36KB 堆 + task stack
- 内存碎片化后 I2S 找不到连续 buffer → 失败

### 解决
- v2.7 决策: **关 AsyncWebServer / ArduinoOTA / AsyncTCP / AsyncWebSocket 全部**
- 编译省 36KB Flash + 2KB RAM
- I2S DMA 稳跑

### 取舍
- 失去 OTA (远程升级) → 接受, 桌面板子 USB 烧录 1 分钟
- 失去 WebServer (ESP32 自带 HTTP 界面) → 接受, server 在 Linux
- 失去 WebSocket push (V2 SQLite 写触发) → 接受, 改 5s 拉 + memcmp 智能渲染

### 永久 lesson
> **ESP32 + HUB75 I2S DMA 项目, 永远先开 I2S, 其他 service (Web/OTA/WS) 慎加**.
> 加之前先用 `Serial.printf("Free heap: %d\n", ESP.getFreeHeap())` 看剩多少。

---

## 🔴 Root Cause #3: 标题字号溢出物理宽

### 现象
- v1.1 标题字号 2 (16×16), 显示 "KID POINTS" 100px → 物理宽 96 px → 溢出右切

### 解决
- 字号 1 (5×7) → "KID POINTS" 50 px → 装得下, 但 5×7 像素字太矮
- v4.0 升 U8g2 7x13_tr → "KID POINTS" 70 px → 装得下, 字符高 13 跟 chinese3 一致

### 永久 lesson
> **HUB75 屏宽 96 px = 12 个 8×8 字符 = 8 个 chinese3 (12 px) = 13 个 ASCII 7×13 (7 px). 布局前先算文本宽度**.

---

## 🟡 Root Cause #4: 库版本错配 (v3.0.14 vs v2.0.7)

### 现象
- 店家 2022 配 **v2.0.7** 库 (默认 R1=14 E=16 跟 PCB 对应)
- 自装 v3.0.14 库 (默认 R1=25 E=-1) → fill_test 显示花屏

### 根因
- v3.0.14 默认 pinmap 跟店家 PCB 不对应
- E pin 默认 -1 (未用), 但店家 PCB 有 E pin (用于 1/32 扫描多路复用)
- 不改 mxconfig.gpio.e → 花屏

### 解决
```bash
# 1. 看店家库版本
cat ~/Arduino/libraries/ESP32_HUB75_LED_MATRIX_PANEL_DMA_Display/library.properties | grep version
# → version=2.0.7

# 2. 装店家版
mv ~/Arduino/libraries/ESP32_HUB75_LED_MATRIX_PANEL_DMA_Display_v3 \
   ~/Arduino/libraries/ESP32_HUB75_LED_MATRIX_PANEL_DMA_Display_v3.bak
cp -r /home/wang/projects/kids-points-v2/extensions/dashboard/refs/ESP32_HUB75_LED_MATRIX_PANEL_DMA_Display-v2.0.7 \
   ~/Arduino/libraries/ESP32_HUB75_LED_MATRIX_PANEL_DMA_Display

# 3. desktop.ino 加一行强制 E=16 (即使库默认是)
mxconfig.gpio.e = 16;
```

### 永久 lesson
> **店家伙 + 自装库** 二选一, 不要混用。店家配的库版本号要写进 ref/ 归档。

---

## 🟡 Root Cause #5: chinese3 574 字字库覆盖不全

### 现象
- 屏显示 "看动片" (实际应是 "看动画片") — 缺 "画" 字
- 缺字显示为方块 / 乱码 / 错位

### 根因
- U8g2 `u8g2_font_wqy12_t_chinese3` 是**简化子集** (574 常用字)
- "画/题/跳/绳/片" 等常用字都不在

### 解决
- v4.7 升到 `u8g2_font_wqy12_t_gb2312b` (5653 字, GB2312 一级字库)
- Flash +107 KB (1049 / 1310 = 80%), RAM 不变

### 取舍
- 7×7 / 8×8 中文字体 GitHub 上有 (Angelic47/FontChinese7x7), 但:
  - 无 ESP32 现成 .h, 需 fontforge 自造
  - < 10 px 中文字形笔画必糊
  - 维护成本 (作者弃坑 + License)
- 12×13 是甜点 (6 中文字 × 12 px = 72 px, 装得下 96 屏)

### 永久 lesson
> **中文屏选 U8g2 字体先看字符数**: chinese3 (574) 不够, gb2312b (5653) 90% 够, gb2312a 全 6763 字占 Flash 太多不值得。

---

## 🟢 Root Cause #6: GFX 5×7 + U8g2 chinese 混排 baseline 必然不齐

### 现象
- v1.1-v3.0 数字用 GFX 5×7 字体, 中文用 U8g2 chinese3
- 同行显示 "+2 口算题" 时数字底部跟中文底部不对齐, 数字"悬"在中文上方

### 根因
- GFX 5×7 字符 baseline 在 y+6, U8g2 chinese3 baseline 在 y+12 (字符底部)
- 同一行 baseline 不同 → 必然不齐

### 解决
- v4.0 **全 U8g2 接管**: 数字用 `u8g2_font_7x13_tr` (字符高 13)
- U8g2 内部统一 baseline 概念 (`setCursor(x, y)` 的 y 就是 baseline)
- 字符高都 13 → 自动对齐, 无需手动算偏移

### 永久 lesson
> **一行混排多种字体, 必须用同一渲染库** (不能 GFX + U8g2 混). 如果非要混, 选字符高度相等的字体, baseline 才会一致。

---

## 🟢 Root Cause #7: GFX `setTextSize(2)` vs 物理宽

### 现象
- `setTextSize(2)` 字号 2 = 5×7 × 2 = 10×14 像素
- "KID POINTS" 10 字 × 10 px = 100 px > 96 px 物理宽 → 溢出

### 解决
- 全 U8g2 接管后, 字号由字体决定 (7x13_tr 是 7×13, 不可缩放), 没有这个问题

### 永久 lesson
> **GFX setTextSize(2) 是把字放大, 不是换字库**. 放大的字像素粗糙, 难读。要大字号 → 选更大的字体 (U8g2 12×20 / 16×26)。

---

## 🟢 Root Cause #8: mmx vision 误识别像素字体

### 现象
- v3.0 拍照 "口算题" mmx vision 读成 "口算天作" / "口算天昨"
- 老王误以为字库缺字, 实际字是对的, 是 mmx vision 误识别

### 根因
- 12×13 像素字体笔画细, mmx vision 在 96×128 分辨率上识别率低
- 像素字体"题"和"天" 笔画差异小, mmx 容易混

### 解决
- **mmx vision 不可信** 用于像素字体验证
- 改用 CH340 USB 串口日志 + 手动描述 + 对比 server 真实数据

### 永久 lesson
> **像素字体 (< 14 px) 截图验证, 别用 vision API**. 用串口日志 + 文本描述 + 跟 server 数据交叉核对。

---

## 🟢 Root Cause #9: CH340 USB 串口死锁

### 现象
- 烧完 ESP32, `arduino-cli monitor` 打不开 / 串口乱码 / 卡住
- `/dev/ttyUSB0` busy

### 根因
- CH340 USB-Serial 芯片固件 bug, 长时间高 baudrate 通信后死锁
- esptool 烧完后未正常释放串口

### 解决
```bash
# 完全拔 USB 30 秒+ (最稳)
# 或换 USB 口
# 或降 baudrate
esptool --chip esp32 --port /dev/ttyUSB0 --baud 115200 write_flash ...

# 串口权限
sudo chmod 666 /dev/ttyUSB0
```

### 永久 lesson
> **CH340 USB 死锁 = 完全拔 30s+**. 不要 try soft reset (没用)。

---

## 🟢 Root Cause #10: 烧完必须手动 EN 复位

### 现象
- 烧完 bin, 串口没日志, 屏没反应

### 根因
- esptool `write_flash` 写完不重启 ESP32 (只写 flash)
- ESP32 默认从上次状态继续跑, 不重跑 bootloader

### 解决
- 烧完按 ESP32 板上的 **EN** 按钮 (reset)
- 或短接 EN 到 GND 1 秒

### 永久 lesson
> **esptool 烧完 ≠ ESP32 重启**. 必须手动 EN 或 rst。

---

## 🟢 Root Cause #11: server description 拆分

### 现象
- server 返 `description: "口算题 | 今天做了20道题"`
- v4.5 之前, ESP32 端用 UTF-8 字节截断, 拿到 "口算题 | 今天做了20道" → 12 中文字 (72 + 84 = 156 px) → 溢出 96 屏

### 解决
- v4.5: ESP32 端按 "|" ASCII 分隔符切, 只取前半段 → "口算题"
- 加 fallback: 无 "|" → 切 6 中文字 (skip ASCII)

### 永久 lesson
> **窄屏 + 长 description, 要么 server 端拆, 要么 client 按规则拆**. 让 server 拆是干净的做法 (未来 ESP32 端不用关心), 但本项目 server 是中间层, 不希望它知道屏宽。

---

## 🟢 Root Cause #12: 30s 拉 + 数据没变也重画 → 屏闪

### 现象
- v4.7 之前 FETCH_INTERVAL_MS=30s, 但 ESP32 loop render 间隔 5s
- 每 30s fetch 一次, 拉完 5s 内必然 render → 屏必然闪 (哪怕数据没变)

### 解决
- v4.8: FETCH_INTERVAL_MS=5000 (5s) + render_frame() 头部 memcmp 比对
- 数据没变 → return → 屏保持
- 数据变 → 重画一次

### 取舍 (vs WebSocket push)
- B 方案 (memcmp): CPU < 2%, 5s 内数据变更可见, 零新库
- D 方案 (WS): < 1s 数据变更可见, 但需 flask-sock + WSClient (~50 KB Flash, RAM 风险)
- 选 B: 5s 对家庭场景足够, 不冒险

### v5.4 后续 (2026-06-20, 老王决策)
- B 方案保留, **Server 端加 in-memory cache 模式**取代 WS 推
- watchdog 监听 V2 SQLite 变化 → 标 cache dirty → 下次 GET fetch
- 99% 请求走 cache (0 subprocess, 1ms), V2 挂掉时屏显示最后正常数据
- 详见 CHANGELOG.md v5.4

### 永久 lesson
> **拉频繁没关系, 渲染频繁才伤屏**. memcmp 是廉价优化, 适合静态显示。

---

## 终极 Root Cause 总结

**24+ 次 fill_test 失败**: 库版本错配 (v3.0.14 vs v2.0.7) → 默认 pinmap 不对应店家 PCB → 强制 `mxconfig.gpio.e = 16` + 用 v2.0.7 → 1 次成功。

**6+ 次烧录失败**: erase_flash 破坏 NVS → 必须 wifitest 重建 + 只写 app 分区 (esptool 0x10000) → 永久 OK。

**多次 KABOOM**: AsyncWebServer + I2S DMA 共存 RAM 爆 → 删 36KB 服务 → 永久稳跑。

---

## 永久 Rule (未来 ESP32 + HUB75 项目)

1. **永远不要 erase_flash** (除非准备 wifitest 重灌)
2. **永远 esptool write_flash 0x10000 只写 app**, 不动 NVS
3. **永远先开 I2S**, Web/OTA/WS 慎加
4. **店家伙 vs 自装库二选一**, 不要混
5. **中文屏选 gb2312b** (5653 字覆盖 90%, Flash 可接受)
6. **一行混排多字体必须用同一渲染库**
7. **烧完必须手动 EN 复位**
8. **CH340 死锁 = 完全拔 30s+**