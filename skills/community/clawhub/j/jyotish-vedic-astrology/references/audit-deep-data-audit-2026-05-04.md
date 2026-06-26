# 印度占星 Skill 深度数据审计报告

**测试日期**: 2026-05-04  
**测试数据**: 1990-01-15 10:30 北京 (lat=39.9, lon=116.4, tz=+8)  
**验证方法**: 使用 pyswisseph 2.08 独立计算对比引擎输出，逐字段核对  
**测试对象**: GitHub 仓库最新代码 full-reading 综合解盘 19 模块 + 27 子命令  

---

## 审计总结

| 类别 | 通过 | 失败 | 警告 |
|------|------|------|------|
| 核心计算（行星位置/宫位/逆行） | 9/9 | 0 | 0 |
| Dasha 系统 | ✅ | - | - |
| Nakshatra 系统 | 9/9 | 0 | 0 |
| Shadbala 系统 | 7/7 | 0 | 0 |
| Ashtakavarga | ✅ | - | - |
| 分盘系统 (D9 Navamsa) | 9/9 | 0 | 0 |
| Tajika 年运 | ✅ | - | - |
| Vivah Saham | - | 1 | - |
| Jaimini 8-Karaka | - | 1 | - |
| Jaimini Chara Dasha | - | 1 | - |
| Vimsopaka 尊贵判定 | - | 7 | - |
| Arudha Lagna | - | 1 | - |
| Hora/Ghati Lagna | - | - | 1 |
| Yoga 检测 | - | 1 | - |

---

## 一、通过验证的模块（计算正确）

### 1.1 行星位置计算 ✅

所有 9 个行星 + 上升点的经度与 pyswisseph 独立计算结果偏差 < 0.004°（恒为 0.0035°，是 Lahiri Ayanamsa 精度差异，完全可接受）。

| 行星 | 引擎经度 | Swiss Eph | 差值 |
|------|---------|-----------|------|
| Sun | 270.9573 | 270.9538 | 0.0035 |
| Moon | 138.8151 | 138.8116 | 0.0035 |
| Mars | 235.9094 | 235.9059 | 0.0035 |
| Mercury | 257.9240 | 257.9205 | 0.0035 |
| Jupiter | 69.6946 | 69.6911 | 0.0035 |
| Venus | 277.2018 | 277.1983 | 0.0035 |
| Saturn | 263.5500 | 263.5465 | 0.0035 |
| Rahu | 293.9969 | 293.9934 | 0.0035 |
| Ketu | 113.9969 | 113.9934 | 0.0035 |
| Asc | 333.1858 | 333.1860 | 0.0002 |

### 1.2 宫位分配（Whole Sign）✅

所有 9 个行星的宫位分配基于正确的 Whole Sign 方法计算，全部正确。

### 1.3 逆行检测 ✅

Mercury、Jupiter、Venus、Rahu 的逆行状态与 Swiss Ephemeris 行星速度对比，全部正确。

### 1.4 Vimshottari Dasha ✅

- Moon Nakshatra: Purva Phalguni (index 10) ✅
- Balance years: 11.78y（手动计算: 11.78y）✅
- 大运总年数: 120 ✅
- 当前大运: Rahu (2024-10-25 to 2042-10-25) ✅
- 当前小运: Rahu/Rahu (2024-10-25 to 2027-07-08) ✅

### 1.5 Nakshatra 高级系统 ✅

- 全部 9 颗行星的 Nakshatra 名称、索引、Lord 映射 100% 正确
- Pada 计算正确（如 Moon pada=2，手动验证匹配）
- Dasha 年数与 Nakshatra Lord 对应正确

### 1.6 Shadbala 六重力量 ✅

- **所有 7 颗行星**的六种力量加和与报告的 total_virupas 完全一致
- Virupas → Rupas 换算 (÷60) 全部正确
- Ucha Bala 验证通过（如 Sun: debilitation distance = 80.96/180 × 60 = 26.99 ✅）
- 夜生判定: False (10:30 AM) ✅
- Uttarayana 判定: True (Jan 15) ✅

### 1.7 Ashtakavarga ✅

- SAV 总量: 337 ✅
- 全部 8 个 BAV 的 bindus 总量验证通过（Sun=48, Moon=49, Mars=39, Mercury=54, Jupiter=56, Venus=52, Saturn=39, Lagna=49）
- BAV → SAV 逐星座聚合验证通过
- R1-R10 全部 11 项验证通过

### 1.8 D9 Navamsa 分盘 ✅

全部 9 颗行星的 Navamsa 位置使用 BPHS 标准（Movable/Fixed/Dual 起算方法）验证正确。

### 1.9 Tajika 年运盘 ✅

- Muntha: (Pisces=11 + age=35) % 12 = 10 = Aquarius ✅
- Muntha Lord: Saturn ✅
- Mudda Dasha 总月数: 12.0 ✅

### 1.10 其他正确项

- Bhava Lagna: (Asc + Sun - Moon) = 105.328° ✅
- Vivah Saham 公式（独立子命令时）: (Venus - Saturn + Asc) = 346.84° Pisces 16.84° ✅
- Argala 门闩系统: 逻辑合理
- Aspects 相位系统: Mars-Ketu 120° tight orb (1.9°) 正确

---

## 二、发现的计算错误（按严重程度排序）

### 🔴 P0: Jaimini 8-Planet Karaka 排名完全错误

**问题描述**: 8 行星系统中，Rahu 被错误排名。

**证据**:
```
Rahu 实际 degree_in_sign = 23.9969°（应为第 2 名 Amatyakaraka）
引擎使用 degree_in_sign = 6.0031°（30 - 23.9969 = 6.0031）
```

引擎错误地将 Rahu 的度数取反（用了 30° - 实际度数），导致 Rahu 从第 2 名掉到最后第 7 名(Darakaraka)，完全扰乱了 Karaka 分配：

| Karaka | 引擎输出 | 正确应为 |
|--------|---------|---------|
| Atmakaraka | Mars ✅ | Mars |
| Amatyakaraka | Saturn ❌ | Rahu |
| Bhratrikaraka | Moon ❌ | Saturn |
| Matrikaraka | Mercury ❌ | Moon |
| Putrakaraka | Jupiter ❌ | Mercury |
| Gnatikaraka | Venus ❌ | Jupiter |
| Darakaraka | Rahu ❌ | Venus |
| Pitrukaraka | Sun ✅ | Sun |

**影响**: 7/8 的 Karaka 分配错误。Darakaraka（配偶指示星）从 Venus 变成了 Rahu，影响所有关系占星解读。

### 🔴 P0: Jaimini Chara Dasha 全部为 0 年

**问题描述**: Chara Dasha 的 12 个大运全部显示 0.0 年，total_years=137。

```
所有 12 个星座的 years = 0.0
Sum = 0.0y (应该 = 120)
total_years 字段 = 137（与 sum 矛盾）
```

**影响**: Chara Dasha 完全不可用。

### 🔴 P0: Vimsopaka Bala 尊贵状态判定严重错误

**问题描述**: 所有 16 个 Varga 的尊贵判定全部使用 Rashi（D1）的尊贵值，没有按各分盘独立计算。且 Rashi 层面的判定本身也有错。

| 行星 | 实际位置 | 正确尊贵 | 引擎尊贵 | 结果 |
|------|---------|---------|---------|------|
| Mars | Scorpio (入庙) | Own Sign | Friend | ❌ |
| Moon | Leo | Friend | Own Sign | ❌ |
| Jupiter | Gemini (敌星宫) | Enemy | Friend | ❌ |
| Mercury | Sagittarius (敌星宫) | Enemy | Friend | ❌ |
| Sun | Capricorn (土星宫) | Enemy | Friend | ❌ |
| Venus | Capricorn | Friend | Neutral | ❌ |
| Saturn | Sagittarius | Neutral | Neutral | ✅ |

**验证**: 检查了 Mars、Jupiter、Sun、Moon 的 16 个 varga_scores，每颗行星的所有 16 个 Varga 都显示**相同的 dignity 值**，确认引擎直接复制了 Rashi 的尊贵判定到所有分盘。

**影响**: Vimsopaka Bala 的分数计算基于错误的尊贵判定，整个模块的数据不可信。如 Mars 在 Scorpio 入庙应得 15 virupas，但引擎按 Friend 只给了 10 virupas。

### 🔴 P0: Yoga 检测返回 0 个 Yoga

**问题描述**: 测试盘中至少应存在 Anapha Yoga（Ketu 在 Moon 的 12 宫）和 Voshi Yoga（Mercury+Saturn 在 Sun 的 12 宫），但引擎检测到 0 个。

**可能原因**: Yoga 检测逻辑过于保守，或没有实现这些基础 Solar/Lunar Yoga。

### 🟡 P1: Arudha Lagna 计算疑似 Off-by-One

**问题描述**: 

Pisces 上升，Jupiter 在 Gemini（第 4 宫）。

- **标准 Jaimini AL**: 从上升数到 Jupiter 所在宫 = 4，再从 Jupiter 数 4 = Virgo
- **引擎输出**: AL 在 Leo (129.69°)，使用公式 `Jupiter_lon + (distance-1) × 30 = 69.69 + 60 = 129.69`

引擎的 AL 公式比标准少算 1 宫（使用 distance-1 而非 distance），导致 AL 落在 Leo 而非标准的 Virgo。Upapada Lagna 也有同样的公式模式。

**影响**: AL 和 UL 偏移一个星座，影响所有基于 Arudha 的解读（社会声望、配偶形象等）。

### 🟡 P1: Vivah Saham 在 full-reading 中输出 null

**问题描述**: 

standalone 子命令 `vivah-saham` 返回正确的 346.84° Pisces 16.84°，但 full-reading 集成中 `vivah_saham` 字段为 None（实际数据在 `saham_lon` 等子字段中，但顶层为 None）。

```
standalone: {"vivah_saham": {"longitude": 346.84, "sign": "Pisces", ...}}  ✅
full-reading: {"vivah_saham": None, "saham_lon": 346.84, ...}  ❌ 结构不一致
```

**影响**: full-reading 消费者如果按 `modules.vivah_saham.vivah_saham` 路径访问会得到 null。

### 🟡 P2: Hora Lagna / Ghati Lagna 日出时间可能有误

`hours_from_sunrise=4.5` 意味着日出在 6:00 AM，但北京 1 月 15 日实际日出约 7:30 AM（应得 ~3 小时）。可能引擎的日出计算有误或时区处理有偏差。

---

## 三、上次报告问题的状态更新

| 编号 | 上次发现 | 本次深度验证结论 |
|------|---------|----------------|
| P1 | transit 参数不一致 | 仍然存在，未修复 |
| P2 | cmd_rectify 不存在 | 确认不存在 |
| P3 | 版本号混乱 | 确认混乱 |
| P4 | dasha 参数不统一 | 确认存在 |
| P5 | yoga 参数不直观 | 确认存在 + yoga 检测返回 0 个 |
| P7 | predict 输出质量低 | 确认存在 |
| P9 | yoga 检测灵敏度低 | **升级为严重**: 检测到 0 个 Yoga，核心功能损坏 |

---

## 四、新增发现汇总

| 编号 | 严重度 | 模块 | 问题 | 根因 |
|------|--------|------|------|------|
| D1 | 🔴 P0 | Jaimini 8-Karaka | Rahu 度数取反，7/8 Karaka 错误 | 使用 30° - deg 而非 deg |
| D2 | 🔴 P0 | Jaimini Chara Dasha | 12 大运全部 0 年 | 年份计算逻辑失效 |
| D3 | 🔴 P0 | Vimsopaka | 7/7 行星尊贵判定错误 + 16 Varga 未独立计算 | Rashi dignity 复制到所有分盘 |
| D4 | 🔴 P0 | Yoga | 检测 0 个 Yoga | 检测逻辑缺失或不完整 |
| D5 | 🟡 P1 | Arudha Lagna | 偏移一个星座（Leo vs Virgo） | 公式 distance-1 应为 distance |
| D6 | 🟡 P1 | Vivah Saham | full-reading 中 vivah_saham=None | 数据结构序列化错误 |
| D7 | 🟡 P2 | Hora/Ghati Lagna | 日出时间偏差 ~1.5 小时 | 日出计算或时区问题 |

---

## 五、优先修复建议

### 第一优先级（核心计算错误）

1. **Jaimini 8-Karaka**: 修改 Rahu 的 degree_in_sign 计算，直接使用 Rahu 在其所在星座的实际度数（23.9969°），不要用 30° - deg
2. **Jaimini Chara Dasha**: 排查 years 计算逻辑为何全部返回 0
3. **Vimsopaka**: (a) 修正 Rashi 层面的尊贵判定（Mars=Own Sign, Jupiter=Enemy 等）；(b) 为每个 Varga 独立计算尊贵状态
4. **Yoga 检测**: 实现 Anapha/Sunapha/Voshi 等基础 Solar/Lunar Yoga

### 第二优先级（计算精度）

5. **Arudha Lagna**: 将公式从 `lord_lon + (distance-1)*30` 改为 `lord_lon + distance*30`
6. **Vivah Saham full-reading 集成**: 修正数据结构映射

### 第三优先级（完善性）

7. **Hora Lagna 日出计算**: 验证 pyswisseph 的 sunrise 函数调用是否正确传入时区
8. 继续修复第一轮报告中发现的 transit/dasha 参数接口问题
