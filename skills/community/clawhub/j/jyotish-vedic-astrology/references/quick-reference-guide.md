# 印度占星 Skill 执行总控指南

> **用途**：本指南是 v6.0.0 升级的**执行总控文件**，承接 SKILL.md 的详细内容。包含：完整引擎命令参数、10大场景执行模板、27大子命令详表、105个参考文件完整索引、强制规范详情。
>
> **使用方式**：SKILL.md 为入口路由，本文件为执行操作手册。CTRL+F 搜索关键词快速定位。

> **来源标签**: 【现代演绎·Skill整合】 — 执行总控指南
>
> **版本**：v6.0.0 | **最后更新**：2026-05-04
---

## 场景一：用户说"帮我看盘"或"分析我的星盘"

**判断类型**：全面综合解盘（Level 2/3）

**执行顺序**：

```
1. 收集出生数据：
   - 阳历出生日期（精确到日）
   - 出生时间（精确到分钟）
   - 出生地点（经纬度或城市名）
   - 时区

2. 调用引擎铸造星盘：
   python3 scripts/jyotish_engine.py full-reading \
     --year YYYY --month MM --day DD \
     --hour HH --minute MM \
     --lat LAT --lon LON --tz TZ

3. 参考文件（按顺序）：
   a) references/vedic-astrology-fundamentals.md（基础知识）
   b) references/yoga-identification-guide.md（Yoga识别）
   c) references/comprehensive-reading-workflow.md（综合解盘工作流）
   d) references/qin_ruisheng_system.md（秦瑞生体系：星曜/宫位/大运/流年）

4. 质量检查（references/deep-analysis-complete-workflow.md）：
   - Shadbala六重力量
   - Ashtakavarga八分法
   - D1+D9双盘验证
   - 三级置信度评分
```

---

## 场景二：用户说"什么时候结婚"或"感情/婚姻应期"

**判断类型**：婚姻专项推运应期（高复杂度）

**执行顺序**：

```
1. 执行四技法交叉验证（必须全部执行）：
   references/marriage-timing-validation-methodology.md
   → Double Transit + DK木星激活 + UL激活 + Dasha支持

2. 补充综合技法：
   references/marriage-timing-comprehensive-techniques.md
   → KN Rao Double Transit + VP Goel功能征象星 + Jaimini DK

3. 配偶多层画像：
   references/spouse-multi-layer-methodology.md
   → DK+7宫主+金星+木星+昼夜区分+Rahu六层确认

4. 婚姻Navamsa深度：
   references/navamsa-marriage-deep-analysis.md
   → D9婚姻五维 + Pushkara + 婚姻8步算法

5. 如果是复合/分阶段：
   references/marriage-timing-comprehensive-techniques.md
   → Ketu期感情特征判断

6. 婚姻计数法（补充）：
   references/bhrigu-pada-dasha-marriage-counting.md
   → 7宫主D1→D9距离计数

7. 引擎调用：
   python3 scripts/jyotish_engine.py dasha \
     --year YYYY --month MM --day DD \
     --hour HH --minute MM --lat LAT --lon LON --tz TZ

   python3 scripts/jyotish_engine.py transit \
     --target-date YYYY-MM-DD \
     --target-planets Jupiter,Venus,Rahu,Ketu \
     --lat LAT --lon LON --tz TZ
```

**注意事项**：
- 7星系统命中率DK 90%/Dasha 70%/UL 40%/DT 20%
- 8星系统命中率DK 100%/UL 60%/DT 40%
- **DK Jaimini激活100%命中率存在虚命中**（11/12星座被相位）→ 作必要条件非充分条件
- 必须转世界时(UT)计算，否则Moon偏移6-8°
- 优先用Double Transit检验7宫/7主/功能DT/UL/DK多个目标组合
- 7星/8星双轨并行，不排他——80%案例两系统给出不同DK

---

## 场景三：用户说"看看事业/财运/学业"（单项分析）

**判断类型**：专项事件分析

**参考路由**：

| 用户意图 | 主参考文件 | 引擎命令 |
|---------|-----------|---------|
| 事业时机 | references/yoga-phala-timing-guide.md | `dasha` + `transit` |
| **→ Actionable Output** | references/transit-actionable-output-guide.md ⭐v4.1.0 | 必须输出时间段+行动+置信度 |
| 财运来源 | references/darakaraka-complete-guide.md（DK财富5模式）| `chart` + `yoga` |
| 学业考试 | references/planetary-dignity-complete-reference.md（D24分析） | `varga -d 24` |
| 健康预后 | references/advanced-techniques.md（8宫+6宫） | `chart` + `shadbala` |
| 职业方向 | references/d10-varga-guide.md（D10事业盘） | `varga -d 10` |

---

## 场景四：用户上传PDF星盘文件

**执行顺序**：

```
1. 使用 PDF Skill 提取PDF文本（见 use_skill tool）

2. 提取数据验证清单（references/pdf-data-extraction-guide.md）：
   □ D1 12宫主星及落宫
   □ D9 Navamsa 关键星曜
   □ D10 Dashamsha 事业格局
   □ Vimshottari Dasha 时间线
   □ Shadbala 六重力量表
   □ Ashtakavarga SAV值
   □ 特殊Lagna（Chalit/OM/Sahaj）
   □ Karaka列表（除标准7个外+Chara Karaka）

3. 完整性门检查（references/comprehensive-reading-workflow.md §1）：
   → 数据完整 → 进入全链路分析
   → 数据缺失 → 降级分析并注明限制

4. 全链路分析：
   references/deep-analysis-complete-workflow.md
   → 12模块系统化分析
```

---

## 场景五：用户说"我没有出生时间"或"只有年月日"

**判断类型**：生时矫正 / 有限数据分析

**执行顺序**：

```
1. 出生时间矫正：
   references/birth-time-rectification-guide.md
   → 收集10-25个生命事件
   → 8大矫正方法自动验证
   → 输出矫正结果+置信度

   引擎命令：
   python3 scripts/jyotish_engine.py cmd_rectify \
     --events "事件描述1 日期1,事件描述2 日期2,..."

2. 如果无法矫正（有限数据模式）：
   references/vedic-astrology-modern-practice-guide.md
   → 使用星宿+星座+行星分布做有限分析
   → 明确注明置信度限制
```

---

## 场景六：用户提出一个具体问题（不提供出生时间）

**判断类型**：Prashna单事件问事（时卦/卜卦）

**执行顺序**：

```
1. 调用引擎铸造即时星盘：
   python3 scripts/jyotish_engine.py prashna \
     --datetime "YYYY-MM-DD HH:MM" \
     --lat LAT --lon LON --mode chart

2. 参考文件：
   references/single-event-inquiry-protocol.md（标准十步断卦模板）
   references/prashna-complete-guide.md（完整方法论）

3. 问题类型路由（references/single-event-inquiry-protocol.md）：
   | 问题类型 | 征象宫位 | 关键行星 |
   |---------|---------|---------|
   | 婚姻/感情 | 7宫+金星 | Jupiter/Saturn |
   | 事业/职业 | 10宫+太阳 | Saturn/Mars |
   | 财务/投资 | 2宫+11宫 | Jupiter/Venus |
   | 健康/疾病 | 6宫+8宫 | Mars/Saturn |
   | 法律/诉讼 | 6宫+8宫+12宫 | Saturn/Ketu |
   | 失物/寻人 | 8宫+2宫 | Mercury/Rahu |

4. 十步断卦执行（references/single-event-inquiry-protocol.md）：
   Step 1: 输入信息收集
   Step 2: 铸造Prashna星盘
   Step 3: 计算AL/Trisphuta
   Step 4: 征象星力量对比
   Step 5: Tajika Yoga检查
   Step 6: Sphuta组合
   Step 7: 阻碍排查
   Step 8: 时间判断
   Step 9: KP Sub-Lord补充
   Step 10: 综合结论

5. 特殊场景补充：
   - 失物：references/prashna-complete-guide.md（Chor Graha+Kunda）
   - 健康：references/prashna-complete-guide.md（Mrityu Chakra）
```

---

## 场景七：用户说"查一下XXX的星盘"或"验证某个名人的盘"

**执行顺序**：

```
1. 名人数据库查询：
   python3 scripts/jyotish_engine.py celebrity \
     --name "姓名"

   数据库统计：
   python3 scripts/jyotish_engine.py db-stats

2. 参考文件：
   references/famous-case-library.md（24个案例索引）
   references/celebrity-cases.md（案例分析）

3. 验前事标准流程：
   references/deep-analysis-complete-workflow.md
   → 用已知事件验证星盘正确性
   → 再做未知事件预测

4. Shatabhisha专项（如果涉及）：
   references/shatabhisha-complete.md
   → 星宿深度解读
```

---

## 场景八：Double Transit 查询（特定行星过境）

**执行顺序**：

```
1. 多参考点过境分析（必须执行）：
   references/transit-multi-reference-guide.md
   → 4个参考点（上升/月亮/太阳/Dasha Lord）
   → 防回归干扰

2. 引擎调用：
   python3 scripts/jyotish_engine.py transit \
     --target-date YYYY-MM-DD \
     --target-planets "Planet1,Planet2" \
     --reference-points "Lagna,Moon,Sun,DashaLord" \
     --lat LAT --lon LON --tz TZ

3. Sade Sati专项（如涉及土星）：
   references/qin_ruisheng_system.md（§6.3 Sade Sati判断）
   references/navatara-kantaka-shani-guide.md

4. 年度运势（Varshaphala）：
   references/varshaphala-annual-chart-guide.md

5. ⭐ Transit Actionable Output（v4.1.0 强制）：
   references/transit-actionable-output-guide.md
   → 每条 Transit 预测必须输出：时间段 + 具体行动类型 + 置信度 [A/B/C]
   → 动态预测必须先检索案例再给结论

6. ⭐ 案例检索（v4.1.0 强制）：
   `celebrity --config ...` 或 `web_search`
   → 被发现/合作/应期/事件型预测必须三步法：检索→对比D10/D9→整合
```

---

## 场景九：全面深度分析（高精度要求）

**执行顺序**：

```
references/deep-analysis-complete-workflow.md（12模块系统化分析）

Level 1 → Level 2 → Level 3 递进：
  Level 1：基础格局（5分钟）
  Level 2：专项分析（20分钟）
  Level 3：深度多系统（60分钟+）

12模块顺序：
  M1: D1本命盘基础
  M2: 特殊Lagna（Chalit/OM/Sahaj）
  M3: Jaimini Karaka系统
  M4: Shadbala六重力量
  M5: Avastha行星状态
  M6: Bhava Bala宫位力量
  M7: Vimsopaka分盘综合
  M8: 19分盘系统
  M9: Ashtakavarga八分法
  M10: 多Dasha收敛（6系统）
  M11: Navamsa婚姻深度
  M12: 综合结论+置信度
```

---

## 场景十：精准解盘质量控制（最后一步必做）

**所有分析完成后执行**：

```
references/precision-reading-methodology.md

PACDARES 框架：
  P: Planets（行星）
  A: Aspects（相位）
  C: Constellations in Signs（星座中的星群）
  D: Dignity（尊严状态）
  A: Analytical Houses（分析宫位）
  R: Rashis（月亮星座）
  E: Essential Strength（本质力量）
  S: Situational Strength（情境力量）

九层复合方法 + L3矛盾检查 + 三级置信度

references/deep-analysis-complete-workflow.md（质量检查清单）：
  □ 验前事通过？
  □ PACDARES通过？
  □ 多系统收敛？
  □ 三级置信度≥2？
  □ 矛盾检查通过？
  □ 置信度≥3才给出确定结论
```

---

## 引擎子命令完整参数表

```bash
PYTHON=python3
SCRIPT=~/.workbuddy/skills/jyotish-vedic-astrology/scripts/jyotish_engine.py
```

### 核心计算命令

| 子命令 | 功能 | 典型用法 |
|--------|------|---------|
| **`full-reading`** | ⭐全自动综合解盘（13模块一键出） | `full-reading --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `chart` | 完整星盘计算（含Ayanamsa修正）+ `--validate` 附加R1-R10验证 | `chart --validate --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `dasha` | Vimshottari大运时间线+小运展开 | `dasha --moon-lon 326.5 --birthdate 1993-04-17 --today 2026-04-24` |
| `yoga` | Yoga格局识别（5种Yoga） | `yoga --ascendant Leo --planets 'Sun:Aries:9,Moon:Aquarius:7,...'` |
| `predict` | 三层验证法事件预测+ `--past-verify` 验前事模式 | `predict --chart '<JSON>' --event-type marriage` |
| `varga` | 分盘计算（D9 Navamsa/D10 Dasamsa） | `varga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --d9 --d10` |
| `varga-full` | BPHS十六分盘精确计算（D2-D60全部16分盘，精确度数输出） | `varga-full --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --divisions D9,D60` |

### 高级分析命令

| 子命令 | 功能 | 典型用法 |
|--------|------|---------|
| `aspects` | 度数精确相位系统（tight/moderate/loose + 入相位/出相位） | `aspects --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `jaimini` | Jaimini完整系统（Chara Karaka 7/8 + Chara Dasha + Karakamsha）+ `--antardasha` | `jaimini --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --mode all --antardasha` |
| `nakshatra-adv` | 高级Nakshatra（Tara Bala + Sub-Lord KP + 兼容性） | `nakshatra-adv --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --mode all` |
| `argala` | Argala门闩系统（主/副Argala + Virodha反干预 + 净评分） | `argala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `tajika` | Tajika年运盘（Muntha + YearLord + Mudda Dasha + Tri-Pataka） | `tajika --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --age 33` |
| `synastry` | 合盘分析（Ashta Koota 36分 + Mangal Dosha + Papasamya） | `synastry --moon1 310.89 --moon2 45.5 --mars1 90.43 --mars2 120.3` |

### 评估与验证命令

| 子命令 | 功能 | 典型用法 |
|--------|------|---------|
| `shadbala` | 六重力量计算（Sthana/Dig/Kala/Chesta/Naisargika/Drik Bala） | `shadbala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `ashtakavarga` | 八分法计算（BPHS完整8×8矩阵，SAV=337） | `ashtakavarga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `validate` | R1-R10数学验证（SAV/BAV/延伸角/Rahu-Ketu/逆行/Dasha/完整性/度数/宫位） | `validate --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `audit` | P1-P12行星审计管线（Identity/Health/Resource/SAV/Dignity/Shadbala/Aspects/Nakshatra/Yogas） | `audit --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `memory` | Hermes记忆系统（store/search/context/stats） | `memory --action store --content "..." --tags "chart" --importance 8` |

### Transit与婚姻专项命令

| 子命令 | 功能 | 典型用法 |
|--------|------|---------|
| `transit` | 行星过境查询（2026-2028） | `transit --year 2026 --month 7` |
| `double-transit-pac` | KN Rao Double Transit PAC + D9层（D1/D9双层PAC检查+跨层确认） | `double-transit-pac --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --date 2026-07-01 --house 7` |
| `transit-ll7l` | Transit LL/7L连接+互换（P5 PAC 98%命中率 + P8过宫 + Parivartana互换） | `transit-ll7l --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --date 2026-07-01` |
| `planetary-congregation` | 行星聚集检测（本命Lagna/7H聚集 + Transit慢行星聚集） | `planetary-congregation --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --house 7 --transit-date 2026-07-01` |
| `vivah-saham` | Vivah Saham婚姻敏感点（度数级计算 + Transit Jupiter/Saturn PAC激活） | `vivah-saham --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --transit-date 2026-07-01` |
| `prashna` | Prashna问事占星（提问时刻星盘+Arudha Lagna+Sphuta组合+Sahams+失物查询） | `prashna --datetime "2026-04-25 14:30" --lat 39.9 --lon 116.4 --mode chart` |

### 其他命令

| 子命令 | 功能 | 典型用法 |
|--------|------|---------|
| `celebrity` | 名人案例查询（SQLite + 15,807条CSV） | `celebrity --name Einstein` |
| `db-stats` | 验证数据库统计（15,840条+10种技法） | `db-stats` |
| `report` | MD→HTML报告生成（羊皮纸主题） | `report ./report_folder --name 一楠 --lagna Leo` |

### 外部数据源（引擎自动读取）

- 验证数据库：`~/WorkBuddy/Claw/vedic_astrology_validation.db`（15,840条案例，10种技法准确率）
- 名人CSV：`~/WorkBuddy/Claw/vedastro_data/PersonList-15k.csv`（15,807条AA级数据）
- 过境配置：`~/WorkBuddy/Claw/月运过境配置-2026-2028.json`（36个月行星位置）

---

## 参考资料完整索引

共 **105个文件**，按功能分组。

### AI解盘工作流（2个）
0. **ai-reading-workflow-prompt.md**：AI解盘工作流Prompt工程（7阶段完整执行引擎）
0b. **quick-reference-guide.md**：⭐执行总控指南（本文件）

### 核心方法论（9个）
1. **common-misconceptions.md**：印度占星常见误判与冲突问题集（错题本）⭐⭐⭐⭐⭐
2. **modern-language-guide.md**：现代生活措辞指南
3. **birth-time-rectification-advanced.md**：出生时间矫正高级方法论
4. **birth-time-rectification-cases.md**：出生时间矫正案例集
5. **pdf-chart-reading-guide.md**：PDF星盘读取指南 v3.0
6. **prediction-checklist.md**：预测清单
7. **data-bridge-mapping.md**：数据桥接映射
8. **prediction-boundary-protocol.md**：预测精度边界规范
9. **prediction-output-protocol.md**：预测输出规范

### 基础知识体系（7个）
10. **planets.md**：行星详解（九大行星完整属性、关系、征象）⭐⭐⭐⭐⭐
11. **signs-and-houses.md**：星座与宫位基础知识
12. **nakshatra_deities.md**：27星宿神祇详解
13. **nakshatra-chinese-quick-ref.md**：27 Nakshatra中文速查表
14. **vimshottari_dasha_guide.md**：Vimshottari大运系统指南
15. **dasha-transit-method.md**：Dasha+Transit方法论
16. **software-comparison-guide.md**：排盘软件与天文计算完全指南

### Yoga格局体系（5个）
17. **yoga_list.md**：Yoga格局完整列表（300+Yoga分类索引）⭐⭐⭐⭐⭐
18. **yoga-list-chinese.md**：瑜伽格局中文完整列表
19. **yoga-and-dasha.md**：Yoga与Dasha结合分析
20. **yoga-strength-scoring-system.md**：Yoga力量评分系统
21. **neechabhanga-raja-yoga.md**：落陷化解详解

### 宫位与生活场景映射（3个）
22. **house-modern-mapping.md**：宫位现代场景映射
23. **house-domain-planet-mapping.md**：宫位-领域-行星映射表
24. **modern-life-scenarios-complete.md**：现代生活场景完整版

### 占星系统（5个）
25. **jaimini-complete-system.md**：Jaimini占星完整体系 ⭐⭐⭐⭐⭐
26. **kp-astrology-complete-system.md**：KP占星完整体系 ⭐⭐⭐⭐⭐
27. **kp-practical-event-timing.md**：KP实战案例与事件时机
28. **remedies-complete-system.md**：补救措施完整体系
29. **personalized-remedies-system.md**：个性化补救系统

### 分盘与力量评估（7个）
30. **ashtakavarga-complete-system.md**：Ashtakavarga完整体系（SAV=337）
31. **shadbala-complete-methodology.md**：Shadbala完整计算方法论
32. **planetary-strength-quick-ref.md**：行星力量速查表
33. **varga-system-quick-reference.md**：综合九层分盘体系对照手册
34. **varga-divisional-charts-quick-reference.md**：分盘快速参考
35. **navamsa-d9-interpretation-template.md**：D9 Navamsa解读模板
36. **shodasavarga-complete-guide.md**：Shodasavarga十六分盘完全指南

### 过境与推运（9个）
37. **transit-comprehensive-guide.md**：过境综合实战指南
38. **transit-multi-reference-guide.md**：多参考点过境分析强制规范
39. **pratyantar-calculation-guide.md**：Pratyantar精确计算指南
40. **varshaphala-annual-chart-guide.md**：Varshaphala年运盘指南
41. **dasha-calculation-tool.md**：Dasha计算工具
42. **dasa-convergence-methodology.md**：Dasa Convergence多系统大运交叉验证
43. **navatara-kantaka-shani-guide.md**：Navatara九星链+Kantaka Shani
44. **alternative-dasha-systems.md**：替代推运系统完全指南
45. **condition-dasha-complete.md**：条件Dasha系统完全指南

### 关系占星（5个）
46. **relationship-astrology-guide.md**：关系占星/合盘分析指南
47. **spouse-multi-layer-methodology.md**：配偶多层综合分析方法论（6层交叉确认）⭐⭐⭐⭐⭐
48. **planetary-dignity-complete-reference.md**：行星尊严与度数完整参考手册 ⭐⭐⭐⭐⭐
49. **marriage-timing-comprehensive-techniques.md**：婚姻应期技法综合手册

### 综合分析框架（5个）
50. **comprehensive-reading-workflow.md**：综合解盘工作流
51. **tri-system-analysis-template.md**：三系统协同分析模板
52. **yoga-phala-timing-guide.md**：Yoga Phala Timing精确预测
53. **tajika-yoga-complete-guide.md**：Tajika Yoga完整审计指南
54. **promise-assessment-templates.md**：承诺判定模板

### 静态解读最后一环（3个）
55. **retrograde-combustion-war-guide.md**：逆行/燃烧/行星战争深度指南
56. **ketu-dual-nature-guide.md**：Ketu双重属性解读框架
57. **argala-complete-guide.md**：Argala行星干预体系完整指南

### 案例库（13个）
58-70. 名人案例库、普通人咨询案例库、验证案例集（猫王/特朗普/梦露/杰克逊/小李子）等

### 高级技法与全球方法论（5个）
71. **advanced-techniques.md**：高级技法合集
72. **global-astrologer-practical-methodology.md**：全球占星师实战方法论
73. **global-astrologer-reflections.md**：全球占星师反思笔记
74. **qin_ruisheng_system.md**：秦瑞生印度占星体系完整指南

### 古典文献与专业发展（2个）
75. **classical-texts-translation-guide.md**：古典梵语文献指南
76. **professional-development-guide.md**：专业占星师发展路径

### 深度分析方法论（5个）
77. **shadbala-interpretation-methodology.md**：Shadbala六重力量实战解读方法论
78. **multi-dasha-convergence-protocol.md**：多Dasha收敛协议
79. **navamsa-marriage-deep-analysis.md**：Navamsa婚姻深度分析协议
80. **divisional-chart-deep-reading.md**：分盘深度阅读工作流
81. **deep-analysis-complete-workflow.md**：综合深度分析完整工作流

### Prashna与婚姻验证（3个）
82. **prashna-complete-guide.md**：Prashna问事占星完整指南
83. **single-event-inquiry-protocol.md**：Prashna单事件问事协议模板
84. **marriage-timing-validation-methodology.md**：婚姻应期四技法验证方法论

### BCP自然周期法（1个）
86. **bhrigu-chakra-paddhati.md**：Bhrigu Chakra Paddhati自然周期法

### 关系占星补充（2个）
87. **high-status-spouse-yoga.md**：高地位配偶Yoga判定规则
88. **darakaraka-complete-guide.md**：Darakaraka完整指南

### 多元技法系统（5个）
89. **yogi-avayogi-system.md**：Yogi/Ava Yogi/Duplicate Yogi行星系统
90. **tithi-lord-relationship-system.md**：Tithi Lord关系影响系统
91. **rashi-tulya-navamsa-root-impulse.md**：Rashi Tulya Navamsa与Navamsa根源冲动
92. **bhrigu-pada-dasha-marriage-counting.md**：Bhrigu Pada Dasha与婚姻计数法
93. **pancha-pakshi-nakshatra-systems.md**：Pancha Pakshi五鸟择时术+Nakshatra三体系

### BPHS/Raman/Goel体系（5个）
94. **badhaka-obstacle-planet-guide.md**：Badhaka障碍星系统
95. **raman-house-judgment-methodology.md**：B.V. Raman宫位判断方法论
96. **shasti-hayani-dasha-guide.md**：Shasti Hayani条件Dasha指南
97. **marc-boney-marriage-six-step.md**：Marc Boney婚姻六步法
98. **vp-goel-jaimini-dasha-systems.md**：V.P. Goel Jaimini Dasha系统概览

### 精准解盘方法论（1个）
99. **precision-reading-methodology.md**：精准解盘与推运方法论 ⭐⭐⭐⭐⭐

### MEVG强制验证（1个）
100. **mandatory-verification-gate-protocol.md**：强制外部验证门控协议（MEVG）
| 数学验证 | `python3 scripts/jyotish_engine.py validate ...` |
| 行星审计 | `python3 scripts/jyotish_engine.py audit ...` |
| HTML报告 | `python3 scripts/jyotish_engine.py report ...` |

---

---

## 场景十一：Transit Actionable Output（⭐ v4.1.0 新增）

> **所有涉及 Transit 推运分析的场景（场景三/八/九）都必须执行此步骤。**

**核心文件**：references/transit-actionable-output-guide.md

**三要素输出（强制）**：

| 要素 | 要求 | 禁止 |
|------|------|------|
| 时间段 | 精确到日/周/月 | ❌ "今年内" / "下半年" |
| 具体行动类型 | 发布/跟进/保持在线/推进谈判 | ❌ "保持开放心态" |
| 置信度 | [A]=已验证 / [B]=高概率 / [C]=推断 | ❌ 无标注的绝对断言 |

**案例检索触发词**（自动执行）：
"被发现"、"合作"、"应期"、"时机"、"破圈"、"升职"、"搬迁"

**输出模板**：
```
## [B] 时间段：事件描述
**置信度**：⭐ [B]（依据：维度1+维度2+维度3）
**Actionable Output**：
- 时间段：精确日期
- 行动：具体做什么
- 类型：发现型/主动型/等待型
**案例参照**：真实案例名称+关键特征
**未验证声明**：未经个人历史事件验证，置信度[X]。
```

---

*本文件为 v3.13.1 新增，配合 SKILL.md 主文档使用。v4.1.0 新增场景十一（Transit Actionable Output）。*
*最后更新：2026-04-27*
