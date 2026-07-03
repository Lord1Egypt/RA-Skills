# ESP32 主程序详解 (desktop.ino v4.9)

## 文件位置
`/home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop/desktop.ino` (~430 行)

## 配置常量 (用户可改)

```cpp
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASS     = "YOUR_WIFI_PASSWORD";
const char* SERVER_HOST   = "YOUR_SERVER_IP";
const uint16_t SERVER_PORT = 8080;
const unsigned long FETCH_INTERVAL_MS = 5000;   // v4.8: 30s → 5s
const uint8_t BRIGHTNESS  = 70;                 // v5.2: 70 (老王决策, 室内柔和, 见 verify.md Q15)
const char* DASHBOARD_TITLE = "KID POINTS";
```

## 物理参数 (硬件决定, 别动)

```cpp
#define PANEL_RES_X 96
#define PANEL_RES_Y 64
#define PANEL_CHAIN 2        // 2 块 96×64 链成 96×128
#define NUM_ROWS 2           // 垂直拼 2 块
#define NUM_COLS 1           // 1 列
#define SERPENT  false       // 店家伙配置
#define TOPDOWN  false       // 店家伙配置
```

HUB75 pinmap (店家伙默认, 跟 PCB 印刷对应):
```
R1=14  G1=27  B1=26
R2=25  G2=33  B2=32
A=13   B=15   C=2  D=4  E=16
LAT=5  OE=18  CLK=17
```

## 布局常量 (v4.9 5 行紧凑)

```cpp
#define TITLE_Y       3
#define DIVIDER_1_Y   15
#define ROW_1_Y       30     // baseline
#define ROW_2_Y       46
#define ROW_3_Y       62
#define ROW_4_Y       78
#define ROW_5_Y       94
#define DIVIDER_2_Y   108
#define FOOTER_Y      125
#define PAD_X         4
```

行间距 16 px (Chinese 13px + 3px 留白), 5 行 y=30..94, 底栏 y=125 距下边 2 px。

## 数据结构

```cpp
struct DashboardData {
  char title[20];
  int total_balance;
  int today_count;
  int today_net;
  struct {
    char date[8];
    char sign;
    int amount;
    char description[32];
  } recent[5];                // v4.9: 3 → 5
  char last_updated[32];
  bool has_error;
  char error_msg[40];
};
```

3 个全局实例:
- `current_data`: 当前 HTTP 拉到的
- `last_good`: 上次成功拉的 (网络挂时用)
- `static last_rendered`: 智能渲染比对用

## 关键函数

### setup()
1. 串口 115200 (debug 用)
2. WiFi 连接 (10s timeout, 失败不阻塞)
3. `HUB75_I2S_CFG` 创建 DMA 配置 (`mxconfig.gpio.e = 16`)
4. `new MatrixPanel_I2S_DMA(mxconfig)` → 失败 KABOOM 死循环
5. `setBrightness8(BRIGHTNESS)`
6. `new VirtualMatrixPanel(dma, 2, 1, 96, 64, false, false)`
7. `u8g2.begin(*virtualDisp)`
8. 启动时拉 1 次 (`fetch_dashboard()`)

### loop()
```cpp
if (should_refresh || millis() - last_fetch_ms > 5000) {
  fetch_dashboard();
}
if (millis() - last_render_ms > 5000) {
  render_frame();
}
```

### fetch_dashboard() — HTTP GET /api/dashboard
1. WiFi check → 不连 return false
2. `HTTPClient.get(url)`, timeout 5000
3. 非 200 → 失败 return
4. `ArduinoJson` 解析到 `DashboardData d`
5. `_error` 字段 → `has_error = true`
6. `recent[i]` for i<5, copy date/type/amount/description
7. `current_data = d`, `last_good = d`, `has_last_good = true`

### render_frame() — 智能渲染 (v4.8 核心)
```cpp
static DashboardData last_rendered;
static bool first_render = true;
if (!first_render && memcmp(&current_data, &last_rendered, sizeof(...)) == 0) {
  return;  // 数据没变, 静默不重画
}
first_render = false;
last_rendered = current_data;
// ... 完整重画 ...
```

**核心**: 数据没变 → return, 屏保持上 1 帧, 0 闪。
重画耗时 ~50ms, 5s 间隔有 4950ms 闲置, 屏幕刷新率约 0.2 FPS。

### render_frame() 完整渲染 (数据变了)
1. `fillScreen(COLOR_BLACK)`
2. 标题 (7x13_tr, y=TITLE_Y+10=13, baseline)
3. 横线 1 (y=15) + 横线 2 (y=108)
4. 5 行流水:
   - ASCII 数字 (7x13_tr) + 中文 (gb2312b) 混排
   - description 按 "|" 切前半段
   - 无 "|" → 切 6 中文字 (skip ASCII)
5. 底栏 `T+10 ALL:77` (y=125)

### 字体函数

```cpp
// ASCII (数字/英文) - 7x13_tr, 字符 7×13 px, 高匹配 chinese 13
void draw_ascii(VirtualMatrixPanel* d, const char* str, int x, int y, uint16_t color) {
  u8g2.setFont(u8g2_font_7x13_tr);
  u8g2.setFontMode(1);              // 透明背景
  u8g2.setForegroundColor(color);
  u8g2.setCursor(x, y);             // y 是 baseline
  u8g2.print(str);
}

// 中文 - wqy12_t_gb2312b, 字符 12×13 px
void draw_cn(VirtualMatrixPanel* d, const char* str, int x, int y, uint16_t color) {
  u8g2.setFont(u8g2_font_wqy12_t_gb2312b);
  // ... 同 draw_ascii ...
}

// 混排 - 数字 + 中文, baseline 完美对齐
void draw_mixed(VirtualMatrixPanel* d, const char* ascii_part, const char* cn_part,
                int x, int y_cn, uint16_t color) {
  draw_ascii(d, ascii_part, x, y_cn, color);
  int ascii_w = u8g2.getUTF8Width(ascii_part);
  draw_cn(d, cn_part, x + ascii_w + 2, y_cn, color);
}
```

**baseline 对齐原理**: 7x13_tr 字符高 13, chinese3 字符高 13, baseline 都在字符底部 → `setCursor(x, y)` 同一个 y 就是同一个 baseline → 自动对齐。

## 编译资源占用

| 版本 | Flash | RAM |
|------|-------|-----|
| v4.7 (gb2312b) | 1049 KB / 1310 KB (80%) | 47 KB / 320 KB (14%) |
| v4.9 (智能渲染) | 1049 KB (不变) | ~50 KB (+50 字节 last_rendered) |

## 烧录 (重要!)

### ❌ 不要用 arduino-cli upload
- 会重写分区表 + bootloader + app + NVS
- **NVS 被覆盖 → WiFi 密码丢失 → 连不上 WiFi → 死循环**
- **I2S DMA + AsyncWebServer/OTA 共存 → 内存爆 → KABOOM**

### ✅ 用 esptool 只写 app 分区
```bash
# 1. 编译
arduino-cli compile --fqbn esp32:esp32:esp32 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop

# 2. 只写 app 分区 (0x10000), 不动 NVS
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x10000 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop/desktop.ino.bin

# 3. 按 ESP32 板 EN/RST 按钮手动复位 (esptool 不会自动重启 ESP32)
```

### ✅ NVS 丢失修复 (erase_flash 副作用)
```bash
# 烧 wifitest 重建 NVS (只烧这一个 app, 不动 NVS 分区)
arduino-cli compile --fqbn esp32:esp32:esp32 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/wifitest
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x10000 ~/Arduino/dashboard_kid/wifitest/wifitest.ino.bin

# 烧完按 EN 复位, 看串口确认 WiFi 连上
arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=115200
```

## 调试要点

### 串口日志关键字段
```
[v2.7] WiFi 连上, IP=192.168.50.197    ← WiFi OK
[fetch] OK: balance=77, today_count=3   ← HTTP + JSON OK
[fetch] HTTP 500, 失败                  ← server 错
[fetch] JSON parse 失败: xxx            ← schema 不匹配
[wifi] 断连!                            ← WiFi 挂了
```

### 串口打不开 (CH340 USB 死锁)
- 完全拔 USB 30 秒+
- 换 USB 口
- `sudo chmod 666 /dev/ttyUSB0`

### 编译失败 - 库找不到
```bash
arduino-cli lib list                            # 看装了哪些
arduino-cli lib install "ESP32 HUB75 LED MATRIX PANEL DMA Display"
arduino-cli lib install "U8g2 for Adafruit GFX"
arduino-cli lib install "ArduinoJson"
arduino-cli lib install "Adafruit GFX Library"
```

### 字体缺字 (chinese3 574 字覆盖不全)
- 现象: 某些字显示为方块或乱码
- 解决: 已在 v4.7 升到 gb2312b (5653 字), 见 [pitfalls.md](./pitfalls.md)
- 如果还缺字 (GB2312 一级字库 90% 覆盖, 罕见字在二级), 需自定义字库 (fontforge 转换 TTF)

### 颜色不鲜艳 / 偏色 (v4.0-v5.0 长期 bug, v5.1 修复)
- 现象: 颜色看着不像琥珀, 偏暗绿黄
- 根因: 颜色定义 `0xFF8C00` 是 RGB888 (24-bit), 库 API 是 `uint16_t` (16-bit RGB565)
  - 取低 16 位 = `0x8C00` → R=17 G=32 B=0 = 偏暗绿黄
- 修复: v5.1 改用真 RGB565 `0xFC40` (R=31 G=34 B=0 = 真琥珀)
- 重要: **板子是 RGB 全彩 HUB75**, 之前以为是单色琥珀是误判, v5.1 老王拍板启用全彩
  - + → 绿 (0x07E0)
  - - → 红 (0xF800)
  - 0 → 琥珀 (0xFC40)

### 蓝光护眼硬红线 (v5.2, 老王 2026-06-19 决策)
- **永久禁止任何含蓝光的颜色** (LED 蓝光波长 ~470nm 直接伤眼)
- RGB565 B 通道 = 低 5 bit (`0x001F`)
- 调色板全部 B=0 (零蓝光: 琥珀/红/绿/黑)
- **编译期硬检查**: 任一调色板常量含 B>0 → 编译失败 (`#error`)
  ```cpp
  #define BLUE_BIT_MASK 0x001F
  #define HAS_BLUE(color) ((color) & BLUE_BIT_MASK)
  
  #if HAS_BLUE(COLOR_BLACK) || HAS_BLUE(COLOR_AMBER) || \
      HAS_BLUE(COLOR_AMBER_DIM) || HAS_BLUE(COLOR_GREEN) || \
      HAS_BLUE(COLOR_RED) || HAS_BLUE(COLOR_RED_ERR)
  #error "蓝光护眼红线违反 (老王 2026-06-19 决策): 调色板常量含蓝光 (B>0)..."
  #endif
  ```
- 颜色安全分级:
  - **安全 (B=0)**: 琥珀 / 红 / 绿 / 黑 / 黄 (R+G) / 橙 (R+G 弱 G)
  - **禁用 (B>0)**: 蓝 / 紫 / 粉 / 白 — LED 蓝光直接伤眼, 跟 LCD 一样
- 未来加颜色必须 `HAS_BLUE(color) == 0`, 否则编译报错
- 需要蓝光颜色时必须先跟老王讨论护眼取舍