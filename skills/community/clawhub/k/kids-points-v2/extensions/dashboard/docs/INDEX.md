# INDEX — 项目文档入口

> **项目**: Kids Dashboard 家庭儿童积分电子看板
> **位置**: `/home/wang/projects/kids-points-v2/extensions/dashboard/docs/`
> **当前版本**: v4.9 (2026-06-19) — M1.4 完成

## 📚 文档目录

### 入门 (新成员)
1. **[README.md](./README.md)** — 项目介绍 + 快速开始 + 老王决策
2. **[architecture.md](./architecture.md)** — 3 层架构 + 数据流 + JSON Schema
3. **[hardware.md](./hardware.md)** — 硬件清单 + 接线 + 故障排查

### 深入 (开发/修改)
4. **[esp32-code.md](./esp32-code.md)** — ESP32 主程序 v4.9 详解 (430 行)
5. **[server-code.md](./server-code.md)** — Dashboard server + data_source 详解
6. **[dependencies.md](./dependencies.md)** — 软件依赖 + 版本兼容性

### 经验沉淀 (避免重蹈覆辙)
7. **[pitfalls.md](./pitfalls.md)** — M1.4 踩坑史 + 12 root causes + 永久 lesson
8. **[CHANGELOG.md](./CHANGELOG.md)** — v0 → v4.9 完整版本史 + 老王决策时间线

### 运维 (排查/部署)
9. **[verify.md](./verify.md)** — 验证手册 + FAQ + 故障决策树
10. **[roadmap.md](./roadmap.md)** — M1.5+ 后续路线图 + 本周冲刺

---

## 🔍 按场景查

| 我想... | 看 |
|---------|-----|
| 看项目是干嘛的 | [README.md](./README.md) |
| 烧录 / 改代码 | [esp32-code.md](./esp32-code.md) + [pitfalls.md](./pitfalls.md) |
| 加积分 / 看数据 | [verify.md](./verify.md) FAQ + V2 CLI help |
| 排查屏不亮 | [verify.md](./verify.md) 故障决策树 + [pitfalls.md](./pitfalls.md) |
| 修 server | [server-code.md](./server-code.md) |
| 加新功能 | [roadmap.md](./roadmap.md) + [architecture.md](./architecture.md) |
| 知道为什么这么做 | [CHANGELOG.md](./CHANGELOG.md) (老王决策) |
| 知道为啥之前失败 | [pitfalls.md](./pitfalls.md) (12 root causes) |
| 升级 / 换硬件 | [dependencies.md](./dependencies.md) + [hardware.md](./hardware.md) |

---

## 🚦 当前状态 (2026-06-19)

```
M1.4 ✅ 完成
├─ ESP32 v4.9 烧完
├─ 5 行流水 + 智能渲染
├─ 96×128 LED 屏跑通
└─ 老王决策归档

M1.5 ⏳ 待办 (本周冲刺)
├─ systemd 开机自启
├─ 亮度 100
└─ today_net bug 调查

M1.6 ⏳ 体验优化 (2 周)
├─ 按键翻页
├─ 颜色状态
└─ 节假日特效

M2.0 🟢 架构升级 (1 个月)
├─ in-memory cache (v5.4 取代 WS 推) ✅
├─ OTA 远程升级 (不做, USB 烧录 1 分钟)
├─ 多屏支持
└─ Web 控制面板

M3.0+ 🔵 长期 (3 个月+)
├─ 其他场景接入 (体重/血压/番茄钟)
├─ AI 加成 (LLM 评价/语音播报)
└─ 多端协同 (BLE/平板/手环)
```

---

## 📦 关键文件位置

### 代码
| 文件 | 说明 |
|------|------|
| `/home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop/desktop.ino` | ESP32 主程序 v5.3 (~496 行) |
| `/home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/wifitest/wifitest.ino` | NVS 重建脚本 (31 行) |
| `/home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/fill_test/fill_test.ino` | 店家色块测试 |
| `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/server.py` | Flask :8080 主服务, **v5.4 in-memory cache 模式** (~256 行) |
| `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/data_source.py` | V2 CLI 包装 (~131 行) |
| `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/dashboard.service` | systemd unit |

### 数据 (外部依赖)
| 文件 | 说明 |
|------|------|
| `/home/wang/projects/kids-points-v2/runtime/cli.py` | V2 CLI 主入口 |
| `/home/wang/projects/kids-points-v2/runtime/data/kids_points.db` | SQLite DB |

### 库 (Arduino)
| 路径 | 说明 |
|------|------|
| `~/Arduino/libraries/ESP32_HUB75_LED_MATRIX_PANEL_DMA_Display/` | **v2.0.7** 店家伙 |
| `~/Arduino/libraries/U8g2_for_Adafruit_GFX/` | U8g2 中文桥接 |
| `~/Arduino/libraries/Adafruit_GFX_Library/` | GFX 基础 |
| `~/Arduino/libraries/ArduinoJson/` | JSON 解析 |

---

## 🔗 快速命令

```bash
# 烧录 ESP32 (✅ 用 esptool)
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x10000 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop/desktop.ino.bin

# 烧录 ❌ 不要用 (破坏 NVS)
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop

# 重建 NVS (erase_flash 后)
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x10000 /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/wifitest/wifitest.ino.bin

# 看串口
arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=115200

# 看 server 数据
curl http://YOUR_SERVER_IP:8080/api/dashboard | python3 -m json.tool

# 加积分
python3 \
  "/home/wang/projects/kids-points-v2/runtime/cli.py" add \
  --type income --amount 2 --description "口算题"

# 看 SQLite
sqlite3 "/home/wang/projects/kids-points-v2/runtime/data/kids_points.db" \
  "SELECT * FROM points ORDER BY date DESC LIMIT 10;"
```

---

## 📝 文档维护

- **新建**: 老王确认后, 我 (Hermes) 自动写
- **更新**: 每次版本变化 (烧新 v) bump CHANGELOG.md
- **归档**: 文档放 `/home/wang/projects/kids-points-v2/extensions/dashboard/docs/`, **不在 wiki 系统里** (跟 Karpathy LLM Wiki 分开)

**为什么 docs 不在 ~/wiki/?**
- ~/wiki/ 是 LLM Wiki Karpathy 系统 (产品经理知识大脑), 强 frontmatter + Lint
- 本看板 docs 是**项目级技术文档**, 不需要 wiki 系统
- systemd service 文件 `Documentation=/home/wang/projects/kids-points-v2/extensions/dashboard/docs/plan.md` 引用此路径, 自然对齐

---

## 版本

- **v4.9** (2026-06-19) — INDEX 创建 (项目 docs 系统化)
- v4.9-v4.0 各版本变更 → 见 [CHANGELOG.md](./CHANGELOG.md)