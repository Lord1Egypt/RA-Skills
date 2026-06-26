# K.N. Rao 婚姻时机 8 参数验证体系

> 来源: 《Astrology and Timing of Marriage (a Scientific Approach)》
> 作者: K.N. Rao 指导的研究团队 (2008年1月班)
> 验证案例: 218个已确认婚姻案例
> 置信度: [A] 顶级验证

---

## 8 参数及命中率

| 参数 | 描述 | 命中率 |
|------|------|--------|
| **P1** | Vimshottari MD/AD lords 与 Lagna/7H/LL/7L(D1+D9) 有PAC连接 | **100%** (218/218) |
| **P2** | Chara Antar Dasha 与 DK/DKN/DP/UP/7L(D1+D9) 有连接 | **96%** (210/218) |
| **P3** | Transit Jupiter 过 Vivah Saham | **77%** (167/218) |
| **P4** | Double Transit: Saturn+Jupiter 激活 Lagna/7H/LL/7L | **85%** (186/218) |
| **P5** | Transit LL 与 7L 产生连接 | **98%** (214/218) |
| **P6** | Transit Jupiter 激活本命 Venus(男)/Mars(女) | **68%** (149/218) |
| **P7** | Sun 和/或多行星聚于 Lagna 或 7H | **70%** (153/218) |
| **P8** | Transit LL 过 7H 或 7L 过 Lagna | **59%** (128/218) |

## 累积命中率

| 同时满足参数数 | 案例比例 | 累积 |
|------------|---------|------|
| 8个全中 | 18.81% | 18.81% |
| 7个以上 | 34.40% | 53.21% |
| 6个以上 | 32.57% | **85.78%** |
| 5个以上 | 8.72% | **94.50%** |
| 4个以上 | 5.50% | 100% |

**关键结论**: 85.78% 的婚姻案例中 6个或更多参数同时命中。

---

## 参数详解

### P1: Vimshottari Dasha PAC 连接 (100%)

MD(Antardasha) 行星的 **Position/Aspect/Conjunction** 与以下之一连接:
- Lagna (上升)
- 7th House (7宫)
- Lagna Lord (上升主)
- 7th Lord (7宫主)
- 以上行星的关联行星
- **必须在 D1 和 D9 中都检查**

### P2: Chara Dasha + Jaimini 指标 (96%)

Chara Antar Dasha 的 Rashi 通过以下方式连接:
- 1-7 轴与 DK/DKN/DP/UP/7L
- Jaimini Drishti
- **Darakaraka (DK)**: 7-Karaka中度数最低的行星
- **DK Navamsa (DKN)**: DK在D9中的位置
- **Dara Pada (DP)**: 7宫 Arudha Pada
- **Upapada Lagna (UP)**: 12宫 Arudha Pada

### P3: Vivah Saham (77%)

Vivah Saham 计算方法: **LL经度 + 7L经度** (取和的星座)
- Transit Jupiter 必须 aspect 这个 Saham 点
- 注意是 Aspect，不是落宫

### P4: Double Transit (85%)

Saturn(10宫主=Karmadhipati) + Jupiter(9宫主=Dharmadhipati) 同时:
- 激活 Lagna
- 激活 7H
- 激活 LL
- 激活 7L
- 通过 PAC 方式

### P5: Transit LL与7L连接 (98%) ⚠️ 最强Transit指标!

**这是 Transit 参数中命中率最高的！**
- Marriage时，Transit 上升主星 和 7宫主星 之间产生PAC连接
- 我们的验证脚本**完全遗漏了这一点**

### P6: Jupiter激活性别征象星 (68%)

- 男性: Transit Jupiter 激活本命 Venus
- 女性: Transit Jupiter 激活本命 Mars

### P7: 行星聚集 (70%)

- Marriage时 Sun 和/或大量行星聚集在 Lagna 或 7H 附近

### P8: LL/7L互换 (59%)

- Transit LL 过 7H
- 或 Transit 7L 过 Lagna

---

## 额外观察 (研究团队成员贡献)

### B. Shobha: PD Lord 的作用
- Pratyantar Dasha lord 在 Transit 中与 Lagna/LL/7H/7L 有PAC: **84.4%** (90/107)
- 另有20例 PD lord 在 2/12宫 或 6/8宫 (接近上升/7宫)

### Arti Malick: Nakshatra Lord 的 Transit PAC
- 7L Nak Lord PAC in D1: 75%, D9: 83.33%
- LL Nak Lord PAC in D1: 52.77%, D9: 55.55%
- VS Nak Lord PAC in D1: 55.55%, D9: 63.88%

### G.K. Joshi: 7L和Venus Transit
- Marriage时 7L或Venus 在 Transit 中位于 LL(D1或D9)所在星座或其三分星座
- 39个验证: 22个完全符合 (56%), 13个几天前刚过 (33%), 4个不符合 (10%)

### Rishi Kapoor: UP与Vimshottari Dasha
- UP (Upapada) 被 Jaimini Aspect 的行星或其定位星 = Marriage时的Dasha行星
- 40个验证: 75% 命中

---

## 与我们验证的差距

| 我们已有 | Rao已验证我们缺失 |
|---------|----------------|
| DK Nakshatra画像 (100%) | Chara Dasha (P2=96%) |
| D9 DK属性 (100%) | Vivah Saham (P3=77%) |
| Venus/DK Dasha (27%) | Transit LL-7L连接 (P5=98%) |
| 7L落宫相遇方式 (75%) | PAC连接方式 (P1=100%) |
| Double Transit (20%) | Jupiter激活性别征象星 (P6=68%) |
| Rahu Antar离婚 (60%) | DP+UP用于Dasha评分 |
| Yogakaraka识别 (61%) | Nak Lord Transit PAC |

---

## 实施优先级

1. **P5 (Transit LL与7L)** — 最容易实现，98%命中率
2. **P1 PAC连接** — 需要实现Aspect计算
3. **P2 Chara Dasha** — 需要实现Jaimini系统
4. **P3 Vivah Saham** — 简单计算
5. **P6 Jupiter激活Venus/Mars** — 中等难度

---

*来源: K.N. Rao (2008) "Astrology and Timing of Marriage (a Scientific Approach)"*
*提取日期: 2026-05-03*
