# 软件依赖 + 版本

## ESP32 端 (Arduino)

### Arduino IDE 配置

```
IDE: arduino-cli (CLI) 或 Arduino IDE 2.x
Board: ESP32 Dev Module (esp32:esp32:esp32)
Upload Speed: 921600 (烧录速度)
CPU Frequency: 240MHz
Flash Frequency: 80MHz
Flash Mode: QIO
Flash Size: 4MB (32Mb)
Partition Scheme: Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)
```

**注意**: Partition Scheme 选 **Default 4MB with spiffs**, app 分区是 0x10000, 烧录时只写这一段。**不要**改 Huge APP, 烧录位置会变。

### 库依赖

```bash
# 必装
arduino-cli lib install "ESP32 HUB75 LED MATRIX PANEL DMA Display"          # v2.0.7 店家伙 (不要 v3.0.14)
arduino-cli lib install "U8g2 for Adafruit GFX"                              # v1.1+ 中文桥接
arduino-cli lib install "ArduinoJson"                                        # v7.x (v6 也兼容)
arduino-cli lib install "Adafruit GFX Library"                               # v1.11+ (GFX 基础)
```

| 库 | 版本 | 来源 | 大小 | 备注 |
|----|------|------|------|------|
| ESP32 HUB75 LED MATRIX PANEL DMA Display | **2.0.7** (店家伙, 不是 v3.0.14) | 店家提供的 .zip | - | 强制 `mxconfig.gpio.e = 16` |
| U8g2 for Adafruit GFX | 1.1+ | 官方库 | - | 中文桥接 |
| U8g2 (字体源) | 最新 | 官方库 | - | 提供 wqy12_t_gb2312b 字体头 |
| ArduinoJson | 7.x | 官方库 | - | JSON 解析 |
| Adafruit GFX Library | 1.11+ | 官方库 | - | 绘图基础 |
| WiFi | (内置) | - | - | ESP32 板自带 |
| HTTPClient | (内置) | - | - | ESP32 板自带 |

### 字体

U8g2 字体头文件在 `~/Arduino/libraries/U8g2_for_Adafruit_GFX/u8g2_fonts.c`, 包含所有 wqy12_t_* 字体。

当前用:
- `u8g2_font_wqy12_t_gb2312b` (中文, 5653 字, 12×13 px)
- `u8g2_font_7x13_tr` (ASCII, 字符 7×13 px)

**字体选择依据**:
- chinese3 (574 字) 覆盖不全 (缺 画/题/跳/绳/片) → 已弃用
- gb2312a (6763 字) 覆盖 100%, 但 Flash 占 130 KB (太大) → 不必要
- gb2312b (5653 字) 覆盖 90%, Flash 占 107 KB → **当前用**

## Server 端 (Python)

### Python 版本
```
Python 3.10+ (system 或 hermes-agent venv 都行)
```

### venv 选择

Dashboard service 用 `~/.hermes/hermes-agent/venv/bin/python` (跟 hermes 共享 venv)。这是 service 文件里写死的。

如果你想用独立 venv:
```bash
mkdir -p /home/wang/projects/kids-points-v2/extensions/dashboard/venv
python3 -m venv /home/wang/projects/kids-points-v2/extensions/dashboard/venv
/home/wang/projects/kids-points-v2/extensions/dashboard/venv/bin/pip install -r /home/wang/projects/kids-points-v2/extensions/dashboard/code/server/requirements.txt
# 改 service 的 ExecStart 指向 /home/wang/projects/kids-points-v2/extensions/dashboard/venv/bin/python
```

### Python 依赖 (requirements.txt)

```
flask>=3.0
watchdog>=4.0  # 监听 V2 SQLite mtime, 标 in-memory cache dirty (v5.4)
```

### V2 CLI 依赖

V2 CLI 在 `/home/wang/桌面/龙虾工作区/StuAgent/New project/kids-points-runtime/`, 独立项目, 自己的 `requirements.txt`。

Dashboard server 通过 subprocess 调 V2 CLI, 不直接 import, 所以 V2 CLI 的依赖必须装在**同一个 venv** 里 (或者 V2 CLI 自己的 venv 里, 用绝对路径调)。

当前: V2 CLI 用系统 Python 跑, dashboard server 用 hermes venv 跑 → **V2 CLI 必须**装在**系统 Python** 里:
```bash
/usr/bin/python3 -m pip install -r "/home/wang/桌面/龙虾工作区/StuAgent/New project/kids-points-runtime/requirements.txt"
```

## 工具链

### arduino-cli

```bash
# 装 (一次性)
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# 加 ESP32 core
arduino-cli core update-index
arduino-cli core install esp32:esp32

# 看板子列表
arduino-cli board list

# 编译
arduino-cli compile --fqbn esp32:esp32:esp32 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop

# 烧录 (❌ 不要用这个, 会破坏 NVS)
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop

# 串口
arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=115200
```

### esptool

```bash
# 装 (用 hermes venv 或 pipx)
pip install esptool

# 烧录 (✅ 用这个)
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x10000 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop/desktop.ino.bin

# 注意: 写完不重启 ESP32, 必须手动按 EN
```

### sqlite3 (CLI 调试)

```bash
# 直接看 kids_points.db 内容
sqlite3 "/home/wang/projects/kids-points-v2/runtime/data/kids_points.db" \
  "SELECT * FROM points ORDER BY date DESC LIMIT 10;"

# 插测试数据 (调试用, 老王决定要不要)
sqlite3 "/home/wang/projects/kids-points-v2/runtime/data/kids_points.db" \
  "INSERT INTO points (date, type, amount, description) VALUES (date('now'), 'income', 5, '测试 +5');"
```

## 版本兼容性

### 已验证可跑

| 工具/库 | 版本 | 验证日期 |
|---------|------|----------|
| ESP32 Arduino core | 2.0.x (老王安装时) | 2026-06-19 |
| ESP32 HUB75 LED Matrix | **v2.0.7** | 2026-06-19 |
| U8g2 for Adafruit GFX | 1.1+ | 2026-06-19 |
| ArduinoJson | 7.x | 2026-06-19 |
| Python | 3.10+ | 2026-06-19 |
| Flask | 3.0+ | 2026-06-19 |
| ~~flask-sock~~ | ~~0.7+~~ | **v5.4 删** (WS 已废弃) |
| watchdog | 4.0+ | 2026-06-19 (**v5.4 用**: 监 V2 SQLite 标 cache dirty) |

### ❌ 不兼容 (老王试过不行)

| 工具/库 | 版本 | 问题 |
|---------|------|------|
| ESP32 HUB75 LED Matrix | **v3.0.14** (自装) | 默认 pinmap 跟店家 PCB 不对应, fill_test 花屏 |
| arduino-cli `upload` 子命令 | - | 默认调 erase_flash, 破坏 NVS |
| erase_flash (esptool) | - | 同上, 清 NVS, WiFi 密码丢 |
| U8g2 chinese3 | 574 字 | 缺 "画/题/跳/绳/片", v4.7 已升 gb2312b |
| GFX 5×7 数字 + U8g2 chinese3 混排 | - | baseline 必然不齐 |

### ⏳ 待验证 (装上未跑)

- ~~flask-sock~~ (**v5.4 删**: WS 已废弃, 改 in-memory cache 模式)
- watchdog (**v5.4 启用**: 监 V2 SQLite mtime 标 cache dirty, 替代原 WS 推)
- AsyncWebServer (故意关掉, 不要恢复)