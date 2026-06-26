# 印度占星 Skill 全面测试报告

**测试日期**: 2026-05-04  
**测试方式**: 从 GitHub 仓库 https://github.com/732642856/yinduzhanxing 克隆最新代码，模拟普通用户通过云端 git 仓库调用  
**测试数据**: 1990-01-15 10:30 北京 (lat=39.9, lon=116.4, tz=+8)  
**测试环境**: macOS, Python 3.11.9, pyswisseph 2.08  

---

## 一、总体结论

**引擎核心计算功能基本可用**，27 个子命令全部能正常启动、接受参数、返回 JSON 输出。full-reading 综合解盘 19 个模块全部返回正常数据。SAV=337、R1-R10 验证全通过、Dasha 总年数=120 等关键数学验证均无误。

**主要问题集中在文档与代码不一致**——quick-reference-guide.md 中的多个示例命令无法直接执行，部分功能声称但未实现，版本号管理混乱。

---

## 二、27 个子命令逐项测试结果

| # | 子命令 | 状态 | 测试命令 | 问题 |
|---|--------|------|---------|------|
| 1 | `chart` | ✅ 正常 | `chart --year 1990 --month 1 --day 15 --hour 10 --minute 30 --lat 39.9 --lon 116.4 --tz 8` | 无 |
| 2 | `chart --validate` | ✅ 正常 | 同上 + `--validate` | 无，R1-R10 全通过 |
| 3 | `full-reading` | ✅ 正常 | `full-reading --year 1990 ... --age 35` | 返回 19 模块全 OK |
| 4 | `dasha` | ✅ 正常 | `dasha --birthdate '1990-01-15' --moon-lon 138.8151` | ⚠ 参数接口与文档场景二不一致 |
| 5 | `yoga` | ✅ 运行 | `yoga --ascendant Pisces --planets '...'` | ⚠ 检测到 0 个 Yoga（可能误判）；参数格式不直观 |
| 6 | `predict` | ✅ 运行 | `predict --year ... --event-type career` | ⚠ 输出质量低（key_factors=[], timing_windows=[]） |
| 7 | `predict --past-verify` | ✅ 运行 | `predict --year ... --past-verify` | 输出泛化，仅有 4 个推断期 |
| 8 | `varga` | ✅ 正常 | `varga --year ... --d9` | ⚠ 文档中 `varga -d 24` 参数不存在 |
| 9 | `varga-full` | ✅ 正常 | `varga-full --year ... --divisions 'D2,D9,D10,D60'` | 无 |
| 10 | `transit` | ✅ 运行 | `transit --year 2026 --month 5` | ⚠ 仅接受 --year --month，文档声称有 7 个参数全不存在 |
| 11 | `shadbala` | ✅ 正常 | `shadbala --year ...` | 6 种力量完整输出 |
| 12 | `ashtakavarga` | ✅ 正常 | `ashtakavarga --year ...` | SAV=337，BAV 全部验证通过 |
| 13 | `validate` | ✅ 正常 | `validate --year ...` | 11 项全通过 |
| 14 | `audit` | ✅ 正常 | `audit --year ...` | P1-P12 审计正常输出 |
| 15 | `aspects` | ✅ 正常 | `aspects --year ...` | 度数精确相位正常 |
| 16 | `jaimini` | ✅ 正常 | `jaimini --year ...` | 7 Karaka + 8 Karaka 双输出 |
| 17 | `nakshatra-adv` | ✅ 正常 | `nakshatra-adv --year ...` | 含 Tara Bala + Sub-Lord |
| 18 | `argala` | ✅ 正常 | `argala --year ...` | 含 Virodha 反向门闩 |
| 19 | `tajika` | ✅ 正常 | `tajika --year ... --age 35` | Muntha + YearLord + Mudda Dasha |
| 20 | `synastry` | ✅ 正常 | `synastry --moon1 ... --moon2 ...` | 36 分制 + Mangal Dosha |
| 21 | `prashna` | ✅ 正常 | `prashna --datetime ... --lat ... --lon ...` | 多模式均正常 |
| 22 | `prashna --mode lost-item` | ✅ 正常 | 同上 | 失物查询正常 |
| 23 | `prashna --mode kunda` | ✅ 正常 | 同上 | 仅返回 derived nakshatra（输出过于简单） |
| 24 | `double-transit-pac` | ✅ 正常 | `double-transit-pac --year ... --date 2026-05-04 --house 7` | D1+D9+CL 三层 |
| 25 | `transit-ll7l` | ✅ 正常 | `transit-ll7l --year ... --date 2026-05-04` | 输出较简单 |
| 26 | `planetary-congregation` | ✅ 正常 | `planetary-congregation --year ... --transit-date 2026-05-04` | 本命+过境聚集检测 |
| 27 | `vivah-saham` | ✅ 正常 | `vivah-saham --year ... --transit-date 2026-05-04` | 含 Double Transit 激活判断 |
| 28 | `celebrity` | ✅ 正常 | `celebrity --name Einstein` | 返回 7 条匹配 |
| 29 | `db-stats` | ✅ 正常 | `db-stats` | 15840 案例 |
| 30 | `memory` (store) | ✅ 正常 | `memory --action store --content ...` | 存储成功 |
| 31 | `memory` (search) | ✅ 正常 | `memory --action search --query test` | 检索正常 |
| 32 | `memory` (context) | ✅ 运行 | `memory --action context --query test` | 输出全空（无历史数据属正常） |
| 33 | `report` | ⚠ 报错 | `report /tmp/test_report --name ...` | 需要预生成的 MD 文件夹 |

---

## 三、发现的问题分类

### 🔴 严重问题（按文档执行必定失败）

#### P1: `transit` 子命令文档与实现完全不一致

**文档声称**（quick-reference-guide.md 多处）:
```bash
transit --target-date YYYY-MM-DD --target-planets "Jupiter,Venus" --reference-points "Lagna,Moon" --lat LAT --lon LON --tz TZ
```

**实际参数**:
```bash
transit --year 2026 --month 5   # 仅有这两个参数
```

引擎从预编译的 JSON 文件读取过境数据，不支持指定目标行星、参考点或出生信息。按文档执行直接报错。

#### P2: `cmd_rectify` 子命令完全不存在

文档 quick-reference-guide.md 第 157-158 行描述了 `cmd_rectify` 命令用于出生时间矫正：
```bash
python3 scripts/jyotish_engine.py cmd_rectify --events "..."
```

**引擎中完全没有这个子命令**。grep 搜索全文，`rectify` 出现次数为零。

#### P3: 版本号体系混乱

| 位置 | 版本 |
|------|------|
| SKILL.md | v6.0.0 |
| quick-reference-guide.md | v6.0.0 |
| jyotish_engine.py 文件头 | v3.7.1 |
| full-reading 输出 | 4.4.0-full-reading |
| ashtakavarga 输出 | 2.0 |
| audit 输出 | 3.5 |
| synastry 输出 | 3.7 |
| predict 输出 | 3.5 |

v6.0.0 是 Skill 文档层面的版本号，但引擎代码从未更新到 6.0.0。用户看到的输出中没有任何 6.0.0 标识。

### 🟡 中等问题（影响使用体验）

#### P4: `dasha` 子命令不使用标准出生信息参数

大部分子命令使用 `--year --month --day --hour --minute --lat --lon --tz`，但 dasha 使用 `--birthdate --moon-lon`。文档场景二的示例用了标准参数格式，直接执行会报错。

#### P5: `yoga` 子命令设计不直观

yoga 是唯一一个不使用标准出生信息参数的子命令，要求手动传 `--ascendant` 和 `--planets` 字符串（如 `'Sun:Aries:9,Moon:Aquarius:7,...'`）。

**问题**：
- 文档未说明如何从 `chart` 输出中提取 yoga 所需格式
- 不传参数时默认 ascendant=Aries、planets 为空，静默返回空结果（yogas_detected=0）而非报错
- 用户需要手动查 chart 输出再拼接字符串，工作流断裂

#### P6: `varga` 子命令文档中 `-d` 参数不存在

文档提到 `varga -d 24` 和 `varga -d 10`，但引擎只支持 `--d9`、`--d10`、`--all` 三个开关。

#### P7: `predict` 子命令输出质量低

predict 的 career 事件预测输出中：
- `key_factors: []` — 空数组
- `timing_windows: []` — 空数组  
- `dasha_signals: []` — 空数组
- `transit_signals: []` — 空数组
- 所有事件类型（包括未请求的 marriage/wealth/health）都输出，概率全部为 30%

这表明 predict 模块的预测逻辑非常粗浅，几乎只是占位输出。

#### P8: `celebrity` 子命令数据库中 latitude/longitude 全为 null

所有 15840 个案例的 `latitude`、`longitude`、`ascendant_sign`、`ascendant_degree`、`lagna_lord` 等字段全部为 null，数据未被完整导入。但 `person_list_matches` 中包含完整坐标信息。

#### P9: `yoga` 检测灵敏度过低

测试用例中 Pisces 上升、Mars 在天蝎座入庙 9 宫、Jupiter 逆行在 Gemini 4 宫（形成 4-9 轴的 Saraswati Yoga 候选），但 yoga 检测到 0 个 Yoga。可能 Yoga 规则库过于保守或有 bug。

### 🟢 轻微问题

#### P10: `report` 子命令依赖预生成的 MD 文件夹

report 需要一个包含 p1_data.md、p2a_planets.md 等预生成文件的文件夹。普通用户不知道如何生成这些文件，文档也未说明。

#### P11: `prashna --mode kunda` 输出过于简单

仅返回 `{"derived_nakshatra": "Rohini", "index": 3}`，缺少解读内容。

#### P12: `full-reading` 模块数与文档不一致

SKILL.md 说"13模块一键出"，实际返回 19 个模块。文档需要更新。

#### P13: `celebrity --config` 参数不存在

文档提到 `celebrity --config`，但引擎中只有 `--name` 和 `--limit`。

#### P14: full-reading 的 `--age` 参数文档未说明

引擎支持 `--age` 可选参数，但 quick-reference-guide.md 未提及。

#### P15: prashna 的 7 种 mode 文档不完整

引擎支持 chart/arudha/sphutas/sahams/lost-item/life/kunda 共 7 种模式，文档仅列了部分。

---

## 四、编码问题

**中文输出全部为乱码**（在终端 JSON 输出中显示为 `逐逐逐` 等不可读字符）。这是因为 JSON 输出中中文被 escape 为 `\uXXXX` 格式，但终端编码处理异常。实际在 Python 中解析后中文是正确的，但**直接阅读 JSON 输出时不可读**。

这个问题对 AI 调用者（程序化解析 JSON）影响不大，但对人类用户直接查看输出很痛苦。

---

## 五、AI 调用工作流中的关键断裂点

从普通用户/AI 的角度，以下工作流路径存在断裂：

### 路径 A（精准出生信息）断裂点：
1. **chart → yoga**：chart 输出的行星数据无法直接喂给 yoga，需要手动拼接字符串
2. **chart → dasha**：chart 输出月亮经度后需要手动传给 dasha，且 dasha 不接受标准参数
3. **chart → predict**：predict 的 `--chart` 参数需要整个 chart 的 JSON 字符串，但传参方式不直观
4. **full-reading 已解决大部分断裂**：full-reading 内部自动串联了大部分模块

### 路径 B（PDF/文字星盘）断裂点：
1. 引擎没有任何 PDF 读取能力，完全依赖 AI 手动提取后拼凑参数
2. `yoga` 需要手动传参，对 AI 来说需要额外转换逻辑

### 路径 C（出生时间矫正）断裂点：
1. `cmd_rectify` 子命令完全不存在
2. 矫正功能纯靠 AI 文档推理，无引擎支持

---

## 六、建议优先级

| 优先级 | 问题编号 | 建议操作 |
|--------|---------|---------|
| **P0** | P1, P2 | 修正 quick-reference-guide.md 中 transit 和 cmd_rectify 的文档，或实现对应功能 |
| **P1** | P3 | 统一版本号，或在 SKILL.md 中明确区分"Skill文档版本"与"引擎版本" |
| **P1** | P4, P5 | 为 dasha 和 yoga 增加标准出生信息参数支持（`_add_chart_args`） |
| **P2** | P6 | 修正 varga 文档中的 `-d` 参数说明 |
| **P2** | P7 | 增强 predict 模块的实际预测逻辑，填充 key_factors 和 timing_windows |
| **P2** | P9 | 排查 Yoga 检测灵敏度过低的问题 |
| **P3** | P8, P10-P15 | 修补文档细节、补充 report 使用说明、完善 celebrity 数据导入 |

---

## 七、测试通过确认的功能

以下核心计算能力验证通过：
- ✅ 行星位置计算（Swiss Ephemeris，Lahiri Ayanamsa）
- ✅ 宫位系统（Whole Sign）
- ✅ 行星尊贵状态（入庙/旺相/落陷等）
- ✅ 逆行检测
- ✅ Nakshatra + Pada 计算
- ✅ Vimshottari Dasha 大运/小运时间线
- ✅ SAV = 337（Ashtakavarga 总量验证）
- ✅ BAV 各行星 12 宫 bindus 总量验证
- ✅ Rahu-Ketu 180° 对冲验证
- ✅ R1-R10 数学验证全通过
- ✅ Shadbala 六种力量计算
- ✅ Jaimini Chara Karaka 7/8 双系统
- ✅ Tajika Muntha + YearLord + Mudda Dasha
- ✅ Synastry Ashta Koota 36 分制
- ✅ Prashna Arudha + Sphutas + Sahams
- ✅ Double Transit PAC 三层检测
- ✅ Vivah Saham 婚姻敏感点 + 双激活检测
- ✅ Argala 门闩 + Virodha 反门闩
- ✅ 名人数据库 15840 案例
- ✅ Hermes 记忆系统 store/search
