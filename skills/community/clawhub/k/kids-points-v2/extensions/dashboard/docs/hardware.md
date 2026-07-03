# 硬件清单 + 接线

## 总成本估算 (~150 RMB)

| 物料 | 单价 | 数量 | 小计 | 来源 |
|------|------|------|------|------|
| ESP32 DevKit v1 (CH340) | 30 | 1 | 30 | 淘宝 |
| HUB75 LED 矩阵屏 P2 96×64 1/32 扫 | 50 | 2 | 100 | 淘宝 |
| HUB75 16P 杜邦线 (母对母 30cm) | 5 | 2 | 10 | 淘宝 |
| 5V 4A 电源 (DC 5.5×2.1) | 20 | 1 | 20 | 淘宝 |
| ESP32 板载 AMS1117-3.3 降压 | - | - | 0 | 板自带 |
| **总计** | | | **~160 RMB** | |

## ESP32 DevKit v1 板载 (CH340 USB-Serial)

- 30 pin 双列直插, 宽 25.4 mm
- CH340 USB-Serial (老王实测有死锁问题, 见 pitfalls.md #9)
- 板载 3.3V LDO (AMS1117)
- **关键**: 烧录后必须 EN 按钮复位 (见 pitfalls.md #10)

## HUB75 LED 矩阵屏 P2 96×64

- **像素**: 2 mm 点间距, 96×64 = 6144 像素/块
- **扫描**: 1/32 扫 (店家 HUB75E.txt 配置)
- **接口**: HUB75 16P (2×8 pin, 2.54 mm 间距)
- **颜色**: 单色 (老王买的琥珀色/橙色, RGB 引脚只接 R)
- **链**: 2 块垂直拼成 96×128

### 16P HUB75 引脚定义

```
Pin 1  R1    Pin 2  G1    Pin 3  B1    Pin 4  GND
Pin 5  R2    Pin 6  G2    Pin 7  B2    Pin 8  GND
Pin 9  A     Pin 10 B     Pin 11 C     Pin 12 D
Pin 13 CLK   Pin 14 LAT   Pin 15 OE    Pin 16 E
```

**注意**:
- 1/32 扫需要 E pin (店家 PCB 用, 默认库 v3.0.14 E=-1 会花屏)
- 1/16 扫的屏**不需要 E pin**, 接线省 Pin 16
- 颜色: 单色屏只接 R1 (Pin 1), G1/B1 悬空

## 接线 (ESP32 ↔ HUB75)

### 店家 v2.0.7 库默认 pinmap

```
HUB75    ESP32 GPIO
R1  ─── 14
G1  ─── 27
B1  ─── 26
GND ─── GND
R2  ─── 25
G2  ─── 33
B2  ─── 32
GND ─── GND
A   ─── 13
B   ─── 15
C   ─── 2
D   ─── 4
E   ─── 16    ← 1/32 扫必须有
CLK ─── 17
LAT ─── 5
OE  ─── 18
```

### 单色屏精简接线

如果只用单色 (琥珀), 只接 R1/R2 + 控制线:
```
HUB75    ESP32 GPIO
R1  ─── 14
GND ─── GND
R2  ─── 25
GND ─── GND
A   ─── 13
B   ─── 15
C   ─── 2
D   ─── 4
E   ─── 16
CLK ─── 17
LAT ─── 5
OE  ─── 18
```

**省线**: G1/B1/G2/B2 全部悬空, 软件不驱动。12 根线, 不是 16 根。

### 电源

```
5V 4A DC 适配器 (DC 5.5×2.1 母头)
   ↓
   ├── HUB75 VCC (单独供电, 大电流)
   └── ESP32 Vin (USB 不接时, 用 5V 给 ESP32)
```

**注意**:
- ESP32 USB 供电 (500 mA) 不够 HUB75 (峰值 2 A), 必须独立 5V 4A
- 5V 和 GND 用粗线 (≥ 22 AWG), 信号线可用杜邦线 (24 AWG)
- 大屏 (>128×128) 需要更强电源

## 拼装 (2 块链)

### 物理拼
- 2 块 96×64 屏, 垂直拼接 (上 1 块 + 下 1 块)
- 板对板 HUB75 16P 同序对接 (Ribbon cable 或 16P 排线)
- 用亚克力板 + 铜柱固定 (店家一般送)

### 软件配
```cpp
#define PANEL_RES_X 96
#define PANEL_RES_Y 64
#define PANEL_CHAIN 2       // 2 块链
#define NUM_ROWS 2          // 垂直拼 (上下)
#define NUM_COLS 1          // 1 列
#define SERPENT  false      // 店家伙配置, 不蛇形
#define TOPDOWN  false      // 店家伙配置, 不上下颠倒
```

**链方向调试**:
- 上下颠倒 → `TOPDOWN = true`
- 左右镜像 → `SERPENT = true` 或 `mxconfig.gpio.e` 改 pin
- 调试时先开 fill_test.ino, 看色块是否对得上物理位置

## 散热

- 静态显示功耗 ~1 A (峰值 2 A), 板载 LED 驱动芯片发热
- 桌面板子**不需要风扇** (老王决策: 静态散热, 价格敏感)
- 但要留 5 cm 空间在屏背后通风
- **不要**用全封闭外壳, 会热死机

## 常见硬件故障

| 现象 | 可能原因 | 排查 |
|------|----------|------|
| 烧录失败 | USB 线坏 / CH340 死锁 / 端口错 | 换线 / 完全拔 30s+ / `ls /dev/ttyUSB*` |
| 上电花屏 | 库版本错配 / pinmap 错 / E pin 漏接 | 强 `mxconfig.gpio.e = 16` |
| 上电全黑 | 电源功率不够 / HUB75 排线松 | 用 5V 4A / 重插排线 |
| 屏闪 | 电源不稳 / 信号线干扰 | 加 1000μF 电容到 5V / 远离 WiFi 路由 |
| 一行不亮 | HUB75 PCB 坏 / 信号线断 | 换板 / 万用表量 pin 通断 |
| WiFi 连不上 | NVS 丢了 / 密码错 / 2.4G vs 5G | 烧 wifitest / 核对密码 / 用 2.4G |
| 颜色不对 | RGB 顺序反 / 库版本错 | 改 `mxconfig.gpio.r1/g1/b1` 顺序 |
| 字符乱码 | 字库缺字 / UTF-8 编码错 | 升 gb2312b / 看 server description 是不是 UTF-8 |

## 接线检查清单 (烧录前)

- [ ] 5V 4A 接 HUB75 VCC (不是 ESP32 Vin)
- [ ] ESP32 USB 接电脑 (单独供电)
- [ ] HUB75 GND ↔ ESP32 GND (共地)
- [ ] 12/16 根信号线按上面 pinmap 接好
- [ ] ESP32 板 GPIO 5/16/17 等不是 input-only pin (能用 output)
- [ ] 烧录前跑 `arduino-cli compile` 看有没有 pinmap 警告
- [ ] 烧完按 EN 按钮复位

## 不需要买的物料 (店家/老王已有)

- USB 数据线 (Type-C 或 Micro-USB, 看 ESP32 板型)
- 面包板 / 杜邦线 (接线用)
- 万用表 (查 pin 通断)
- 烙铁 (如果 pin 头松, 重焊)