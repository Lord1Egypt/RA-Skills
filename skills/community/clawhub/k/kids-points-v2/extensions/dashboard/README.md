# 桌面积分看板 📺

> **一个抛砖引玉的桌面硬件 demo。**
> 把 kids-points-v2 的积分数据，投到桌上一块 96×128 的 LED 矩阵屏上。

**这不是产品**——是一个家长（老王）为了让孩子随时在桌面看到自己的积分，临时攒出来的硬件实验。如果你也想做一块，可以把它当参考，但不建议 1:1 照抄。

> 📦 **完整源码**（ESP32 固件 / systemd service 文件 / 烧录说明）在 GitHub 仓库：
> <https://github.com/cowboy231/kids-points-v2/tree/main/extensions/dashboard>
>
> ClawHub 上是**核心 skill 包**，不含 ESP32 `.ino` 固件源码（ClawHub 不接受这种 content type）。
> 用户从 GitHub 取 `extensions/dashboard/code/esp32/` 后自行烧录。

---

## 🎯 它能干什么

```
KID POINTS
━━━━━━━━━━━━
+2  口算题卡全对
+3  跳绳 500 个
+1  整理书桌
+5  帮妈妈刷碗
-5  看动画片超时
━━━━━━━━━━━━
今  +2    总  77
```

- **标题**：`KID POINTS`（顶部居中）
- **流水**：最近 5 条积分变化（带 emoji 符号）
- **底栏**：今日净变化 + 总余额

数据每 5 秒从本地 server 拉一次，不联网，不上传，纯本地。

### 实物图（HUB75E 全彩 RGB LED 屏，128×96）

![dashboard 实物图](docs/dashboard-real-hardware.jpg)

> 这是 ESP32-WROOM-32 控制 HUB75E 全彩 RGB 屏在 128×96 点阵上的实拍图（2026-07-02 22:55）。
> **完整 ESP32 固件 + server 代码在 GitHub 仓库 `extensions/dashboard/`。**
> **100% 由 Hermes Agent 编写**——从 server 到 ESP32 固件全栈。如果你也想做一块桌面积分板，完全可以
> 让 AI agent 参考这组代码和硬件 demo，直接完成属于自己的左侧积分板。
> **文中"买冰棍"等是真实生活交易，仅供 demo 示意。**

---

## 🔧 硬件清单（~140 元）

| 物料 | 型号/规格 | 数量 | 来源 |
|------|-----------|------|------|
| ESP32 主控板 | **ESP32-WROOM-32** | 1 | 淘宝 |
| LED 矩阵屏 | **HUB75E P2 128×96 全彩 RGB（1/16 扫）** | 1 | 淘宝 |
| 信号线 | **HUB75 16P 杜邦线（母对母 30cm）** | 1 | 淘宝 |
| 电源 | **5V 4A DC 适配器（DC 5.5×2.1 母头）** | 1 | 淘宝 |

**为什么是这个组合？**

- **ESP32-WROOM-32**：内置 Wi-Fi，GPIO 数量足够驱动 HUB75E（~12 根输出），成本约 35 元
- **HUB75E P2 128×96 全彩**：128×96 横屏，刚好放下 KID POINTS 标题 + 流水 + 底栏，全彩渲染
- **单屏直驱**：不需要拼接，一根 16P 排线搞定，比双屏方案简单太多

> 💡 **全栈 100% 由 Hermes Agent 编写**——从 server 到 ESP32 固件。如果你想做一块属于自己的桌面积分板，完全可以让 AI agent 参考这组代码和硬件 demo，直接完成。

---

## 🏗️ 架构（3 层）

```
┌─────────────────────────────────────────────────┐
│  Layer 3: ESP32 + LED 矩阵屏                    │
│  (5 秒拉数据 → memcmp 比对 → 智能渲染)           │
├─────────────────────────────────────────────────┤
│  Layer 2: Flask Server (:8080)                  │
│  (in-memory cache, 防 CLI 重复调用)              │
├─────────────────────────────────────────────────┤
│  Layer 1: kids-points-v2 SQLite (cli.py)        │
│  (唯一数据源)                                     │
└─────────────────────────────────────────────────┘
```

---

## 🚀 5 分钟上手

### 1. 启动 Server

```bash
cd extensions/dashboard/code/server
pip install flask watchdog
python3 server.py
```

验证：
```bash
curl http://localhost:8080/api/health
curl http://localhost:8080/api/dashboard | python3 -m json.tool
```

### 2. 烧录 ESP32

```bash
# 安装库
arduino-cli lib install "ESP32 HUB75 LED MATRIX PANEL DMA Display"
arduino-cli lib install "U8g2 for Adafruit GFX"
arduino-cli lib install "ArduinoJson"
arduino-cli lib install "Adafruit GFX Library"

# 编译
arduino-cli compile --fqbn esp32:esp32:esp32 code/esp32/desktop/

# 烧录（⚠️ 用 esptool，不要用 arduino-cli upload）
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x10000 code/esp32/desktop/desktop.ino.bin

# 烧完按 ESP32 板上的 EN 按钮复位
```

### 3. 接线（HUB75E 全彩 RGB ↔ ESP32）

| HUB75 | ESP32 | HUB75 | ESP32 |
|-------|-------|-------|-------|
| R1 | 14 | A | 13 |
| G1 | 27 | B | 15 |
| B1 | 26 | C | 2 |
| GND | GND | D | 4 |
| R2 | 25 | E | (悬空, 1/16 扫不用) |
| G2 | 33 | CLK | 17 |
| B2 | 32 | LAT | 5 |
| GND | GND | OE | 18 |

共 15 根信号线（E pin 悬空）。

**⚠️ 电源**：ESP32 USB 单独供电，HUB75 必须接 5V 4A 独立电源（USB 500mA 不够，峰值 2A）。共地。

---

## ❓ FAQ

### Q: ESP32 和 LED 屏之间要接多少根线？
A: 15 根（全彩 RGB：R1/G1/B1 + R2/G2/B2 + A/B/C/D + CLK/LAT/OE + 共地）。1/16 扫不需要 E pin，悬空即可。

### Q: 烧录后用 `arduino-cli upload` 还是 `esptool`？
A: **用 `esptool`**。`arduino-cli upload` 会擦除 NVS（WiFi 密码存储区），导致 ESP32 忘密码。`esptool` 只写 0x10000 位置，不动 NVS。

### Q: 屏不亮怎么办？
A: 90% 是电源问题。检查：5V 4A 接 HUB75 了吗？USB 单独给 ESP32 了吗？共地了吗？如果电源没问题，按 EN 按钮复位试试。

### Q: 花屏/乱码怎么办？
A: 先跑 `fill_test.ino` 看色块位置是否和物理屏一致。如果不对，检查 `mxconfig.gpio` 配置（1/16 扫不需要 E pin，悬空即可）。

### Q: 中文字符显示成方块？
A: 字库要选 `gb2312b`（v4.7+），不要 `chinese3`。GB2312 一级字库覆盖 ~90% 日常中文。

### Q: 没有 LED 屏怎么预览？
A: `code/sim/desktop_sim.py` 是 pygame 仿真，可以调字号、排版、看效果，不通硬件。

---

## 📁 目录结构

```
extensions/dashboard/
├── README.md              # ← 你在这里
├── code/
│   ├── esp32/             # ESP32 固件
│   │   ├── desktop/       # 主程序（v5.3, ~496 行）
│   │   ├── wifitest/      # NVS 重建脚本
│   │   └── fill_test/     # 店家色块测试
│   ├── server/            # Flask Server
│   │   ├── server.py      # 主服务 (:8080, in-memory cache)
│   │   └── data_source.py # V2 CLI 包装
│   └── sim/               # pygame 仿真（无硬件预览）
└── docs/                  # 设计/架构/硬件/验证文档
```

---

## ⚠️ 注意事项

1. **烧录用 esptool 不要用 arduino-cli upload**——后者会擦除 NVS（WiFi 密码存储区）。
2. **烧完必须按 EN 按钮复位**——esptool 不会自动重启 ESP32。
3. **亮度可调**：改 `const uint8_t BRIGHTNESS = 50;`（0=全暗，255=拍照级，50=夜间柔和）。

---

_一块屏，让孩子每天看见自己的进步。_ 🌟