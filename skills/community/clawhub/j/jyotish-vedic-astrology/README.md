# 🪐 Jyotish Vedic Astrology Engine

**印度占星（Jyotish）专业解盘与推运系统 v6.0.0**

基于 Swiss Ephemeris 天文计算库的完整吠陀占星引擎，覆盖从排盘计算到精确推运应期预测的全链路能力。可作为 [WorkBuddy](https://www.codebuddy.cn/) Skill 安装，也可以作为独立 Python CLI 工具使用。

## ✨ 核心特性

- **🧮 统一计算引擎**：22 个 CLI 子命令，一条命令完成全链路分析
- **🔮 全自动综合解盘**：`full-reading` 一键串联 13 个计算模块
- **📐 BPHS 十六分盘**：D2-D60 全部 16 种分盘精确计算
- **👁️ 精确相位系统**：度数级 Drishti 相位分析（tight/moderate/loose）
- **📿 Jaimini 完整系统**：Chara Karaka 7/8 + Chara Dasha + Karakamsha(AK)
- **🌟 高级 Nakshatra**：Tara Bala + Sub-Lord KP 系统 + Nakshatra三计数体系
- **🚪 Argala 门闩系统**：行星干预 + Virodha 反干预
- **🎂 Tajika 年运盘**：Muntha + YearLord + Mudda Dasha + Tri-Pataka三旗
- **💑 合盘分析**：Ashta Koota 36 分制 + Mangal Dosha + Papasamya
- **💪 Shadbala 六重力量**：完整的 Parashara 系统（2026-05-03 Kendra/Ojayugma修正）
- **🎯 Ashtakavarga 八分法**：BPHS 完整表（SAV=337）
- **✅ R1-R10 数学验证** + **P1-P12 行星审计管线**
- **🔒 MEVG 强制外部验证**：v4.2.0 新增，所有解读结论必须外部验证（禁止仅凭AI训练记忆）
- **📊 Transit Actionable Output**：v4.1.0 新增，明确时间段+行动类型+置信度
- **🔮 Prashna 问事占星**：BCP自然周期+Arudha Lagna+Trisphuta+Gulika+Chor Graha
- **⏰ 多Dasha系统**：Vimshottari + Chara + Narayana + Yogini + Moola + Ashtottari等8种

## 📋 系统要求

- **Python**: 3.11+
- **核心依赖**: `pyswisseph`（Swiss Ephemeris 天文计算库）
- **可选依赖**: `requests`（名人数据查询）、`pandas`（批量数据处理）

## 🚀 快速安装

### 1. 克隆仓库

```bash
# HTTPS（推荐，无需配置 SSH key）
git clone https://github.com/732642856/yinduzhanxing.git
cd yinduzhanxing

# 或 SSH
git clone git@github.com:732642856/yinduzhanxing.git
cd yinduzhanxing
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 验证安装

```bash
python3 scripts/jyotish_engine.py chart --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
```

如果输出包含行星位置 JSON，说明安装成功。

## 🎯 使用方法

### 三种输入路径

| 路径 | 适用场景 | 操作 |
|------|---------|------|
| **路径 A** | 有精确出生信息（日期+时间+地点） | 直接调用 `full-reading` |
| **路径 B** | 有 PDF/文字星盘报告 | 提取数据后分析（无需重新排盘） |
| **路径 C** | 出生时间不明确 | 互动式矫正 → 确认后走路径 A |

### 路径 A：精准出生信息（推荐）

```bash
# 一键全链路计算（13 模块自动串行）
python3 scripts/jyotish_engine.py full-reading \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# 输出包含：
# chart + dasha + yoga + varga_full + aspects + jaimini +
# nakshatra_adv + argala + tajika + shadbala + ashtakavarga +
# validation + audit
```

### 单模块调用

```bash
# 基础星盘计算
python3 scripts/jyotish_engine.py chart \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8 --validate

# Vimshottari 大运时间线
python3 scripts/jyotish_engine.py dasha \
  --moon-lon 326.5 --birthdate 1993-04-17 --today 2026-04-25

# Yoga 格局识别
python3 scripts/jyotish_engine.py yoga \
  --ascendant Leo --planets 'Sun:Aries:9,Moon:Aquarius:7,...'

# 十六分盘计算
python3 scripts/jyotish_engine.py varga-full \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8 --divisions D9,D60

# 精确相位分析
python3 scripts/jyotish_engine.py aspects \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# Jaimini 系统（Chara Karaka + Chara Dasha + Karakamsha）
python3 scripts/jyotish_engine.py jaimini \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8 --mode all

# 高级 Nakshatra（Tara Bala + Sub-Lord）
python3 scripts/jyotish_engine.py nakshatra-adv \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8 --mode all

# Argala 门闩分析
python3 scripts/jyotish_engine.py argala \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# Tajika 年运盘
python3 scripts/jyotish_engine.py tajika \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8 --age 33

# Shadbala 六重力量
python3 scripts/jyotish_engine.py shadbala \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# Ashtakavarga 八分法
python3 scripts/jyotish_engine.py ashtakavarga \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# 合盘分析（Ashta Koota 36 分制）
python3 scripts/jyotish_engine.py synastry \
  --moon1 310.89 --moon2 45.5 --mars1 90.43 --mars2 120.3

# 事件预测
python3 scripts/jyotish_engine.py predict \
  --chart '<JSON>' --event-type marriage

# 名人案例查询
python3 scripts/jyotish_engine.py celebrity --name Einstein

# R1-R10 数学验证
python3 scripts/jyotish_engine.py validate \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# P1-P12 行星审计
python3 scripts/jyotish_engine.py audit \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# 行星过境查询
python3 scripts/jyotish_engine.py transit --year 2026 --month 7

# MD → HTML 报告生成（羊皮纸主题）
python3 scripts/jyotish_engine.py report ./report_folder \
  --name "名字" --lagna "Leo" --lang cn
```

### 全部 22 个子命令速查

| 子命令 | 功能 | 核心参数 |
|--------|------|----------|
| **`full-reading`** | ⭐ 全自动综合解盘（13 模块） | `--year/month/day/hour/minute/lat/lon/tz` |
| `chart` | 完整星盘计算 | `--year/month/day/hour/minute/lat/lon/tz` |
| `dasha` | Vimshottari 大运时间线 | `--moon-lon --birthdate --today` |
| `yoga` | Yoga 格局识别 | `--ascendant --planets` |
| `predict` | 三层验证法事件预测 | `--chart --event-type` |
| `varga` | 分盘计算（D9/D10） | `--year/month/day/hour/minute/lat/lon/tz` |
| `varga-full` | BPHS 十六分盘（D2-D60） | `--divisions D9,D60` |
| `aspects` | 度数精确相位（Drishti） | 出生信息 |
| `jaimini` | Jaimini 完整系统 | `--mode all` |
| `nakshatra-adv` | 高级 Nakshatra 分析 | `--mode all` |
| `argala` | Argala 门闩系统 | 出生信息 |
| `tajika` | Tajika 年运盘 | `--age 33` |
| `synastry` | 合盘分析 | `--moon1/2 --mars1/2` |
| `shadbala` | 六重力量计算 | 出生信息 |
| `ashtakavarga` | 八分法（SAV=337） | 出生信息 |
| `validate` | R1-R10 数学验证 | 出生信息 |
| `audit` | P1-P12 行星审计 | 出生信息 |
| `celebrity` | 名人案例查询 | `--name` |
| `db-stats` | 数据库统计 | 无 |
| `transit` | 行星过境查询 | `--year --month` |
| `memory` | Hermes 记忆系统 | `--action store/search` |
| `report` | MD→HTML 报告 | 文件夹路径 |

## 📁 目录结构

```
yinduzhanxing/
├── README.md                    # 本文件
├── CHANGELOG.md                 # 版本更新日志
├── SKILL.md                     # WorkBuddy Skill 配置文件
├── requirements.txt             # Python 依赖
├── .gitignore                   # Git 忽略规则
│
├── scripts/                     # 计算引擎（19 个 Python 文件）
│   ├── jyotish_engine.py        # ⭐ 统一 CLI 入口（22 子命令）
│   ├── varga.py                 # BPHS 十六分盘
│   ├── aspects.py               # 精确相位系统
│   ├── jaimini.py               # Jaimini 系统
│   ├── nakshatra_advanced.py    # 高级 Nakshatra
│   ├── argala.py                # Argala 门闩
│   ├── tajika.py                # Tajika 年运盘
│   ├── synastry.py              # 合盘分析
│   ├── shadbala.py              # Shadbala 六重力量
│   ├── ashtakavarga.py          # Ashtakavarga 八分法
│   ├── event_prediction_model.py # 事件预测规则引擎
│   ├── validate.py              # R1-R10 数学验证
│   ├── dasha_calculator.py      # Dasha 计算
│   ├── dasha_calculator_enhanced.py # 增强版 Dasha
│   ├── dasha_analyzer.py        # Dasha 分析器
│   ├── hermes_bridge.py         # Hermes 桥接层
│   ├── hermes_memory_core.py    # Hermes 记忆核心
│   ├── report_builder.py        # MD→HTML 报告生成
│   └── example.py               # 示例脚本
│
├── references/                  # 知识库（74 个 Markdown 文件）
│   ├── ai-reading-workflow-prompt.md  # ⭐ AI 解盘工作流 v3.0
│   ├── pdf-chart-reading-guide.md     # PDF 星盘读取指南
│   ├── birth-time-rectification-advanced.md  # 出生时间矫正
│   ├── jaimini-complete-system.md     # Jaimini 完整体系
│   ├── kp-astrology-complete-system.md # KP 占星体系
│   ├── ... (详见 SKILL.md 参考资料)
│
└── assets/                      # 模板文件
    ├── birth_time_rectification_template.md  # 矫正信息收集模板
    ├── chart_analysis_template.md            # 星盘分析模板
    ├── event_timing_template.md              # 事件时机模板
    └── timing-prediction-template.md         # 推运应期模板
```

## 🔧 作为 WorkBuddy Skill 使用

本项目是一个标准的 WorkBuddy Skill，安装后在 WorkBuddy 对话中用自然语言即可触发，无需手动输入 CLI 命令。

### 方法 1：手动安装（推荐）

```bash
# HTTPS（推荐，无需配置 SSH key）
git clone https://github.com/732642856/yinduzhanxing.git \
  ~/.workbuddy/skills/jyotish-vedic-astrology

# 或 SSH
git clone git@github.com:732642856/yinduzhanxing.git \
  ~/.workbuddy/skills/jyotish-vedic-astrology
```

安装后，在 WorkBuddy 对话中提到任何印度占星相关关键词（如"印度占星"、"Jyotish"、"解盘"、"推运"等），Skill 即自动激活。

### 方法 2：下载 ZIP（无需 git）

如果电脑没有 git，可以直接下载：

1. 打开 https://github.com/732642856/yinduzhanxing
2. 点击绿色 **Code** 按钮 → **Download ZIP**
3. 解压到 `~/.workbuddy/skills/jyotish-vedic-astrology/` 目录
4. 确保目录下有 `SKILL.md` 文件

### 方法 3：Skill 市场一键安装

> **状态**：待上架。欢迎 WorkBuddy 团队审核后收录到官方市场（`codebuddy-plugins-official`）。
>
> 上架后，用户可在 WorkBuddy 技能市场搜索 `jyotish-vedic-astrology` 一键安装。

**WorkBuddy 团队上架参考**：

| 项目 | 说明 |
|------|------|
| Skill 名称 | `jyotish-vedic-astrology` |
| 仓库 | https://github.com/732642856/yinduzhanxing |
| 入口文件 | `SKILL.md`（根目录） |
| 计算引擎 | `scripts/jyotish_engine.py`（Python 3.11+，依赖 `pyswisseph`） |
| 知识库 | `references/`（100+ Markdown 文件） |
| 系统要求 | macOS / Linux / Windows，Python 3.11+，`pip install -r requirements.txt` |
| 自动安装依赖 | 引擎首次运行时检测 `pyswisseph`，缺失则提示安装 |
| 语言 | 中文为主，技术术语英文 |
| 授权 | 学习与研究用途 |

### Skill 触发词

以下关键词可触发 Skill：
- 印度占星、吠陀占星、Jyotish、印占
- 解盘、推运、星盘分析、排盘、计算星盘
- Dasha、Transit、Nakshatra、Yoga
- 出生时间矫正、生时矫正
- Shadbala、Ashtakavarga、Drishti、Jaimini
- 合盘、婚姻匹配、年运盘
- 以及更多（详见 SKILL.md）

## 🧪 验证与测试

```bash
# 运行 full-reading 验证（一楠星盘）
python3 scripts/jyotish_engine.py full-reading \
  --year 1993 --month 4 --day 17 --hour 14 --minute 45 \
  --lat 36.6 --lon 114.5 --tz 8

# 预期输出：12 modules computed, 0 errors
```

## 📊 数据源

引擎自动读取以下外部数据（如存在）：

| 数据源 | 路径 | 说明 |
|--------|------|------|
| 验证数据库 | `~/WorkBuddy/Claw/vedic_astrology_validation.db` | 15,840 条案例 |
| 名人 CSV | `~/WorkBuddy/Claw/vedastro_data/PersonList-15k.csv` | 15,807 条 AA 级数据 |
| 过境配置 | `~/WorkBuddy/Claw/月运过境配置-2026-2028.json` | 36 个月行星位置 |

> 💡 数据源为可选依赖，不影响基础星盘计算功能。

## 🛠️ 技术架构

```
输入层：出生信息 / PDF星盘 / 互动矫正
    ↓
路由层：自动识别三条路径（A/B/C）
    ↓
计算层：Swiss Ephemeris + Lahiri Ayanamsa 恒星黄道
    ├── chart（星盘计算）
    ├── dasha（大运时间线）
    ├── yoga（格局识别）
    ├── varga-full（十六分盘）
    ├── aspects（精确相位）
    ├── jaimini（Jaimini 系统）
    ├── nakshatra-adv（高级 Nakshatra）
    ├── argala（门闩分析）
    ├── tajika（年运盘）
    ├── shadbala（六重力量）
    ├── ashtakavarga（八分法）
    ├── validate（数学验证）
    └── audit（行星审计）
    ↓
输出层：JSON 数据 → AI 解读 → HTML 报告
```

## 📜 版本历史

详见 [CHANGELOG.md](./CHANGELOG.md)。

- **v6.0.0** (2026-05-05)：反教条主义实战经验整合 + 全球占星师误区总结 + 中文技法论文洞察
- **v5.0.0** (2026-05-04)：27 子命令 + full-reading 19 模块 + 深度数据审计（修复5个P0级Bug）
- **v4.2.0** (2026-04-28)：MEVG 强制外部验证 + Transit Actionable Output
- **v3.7.1** (2026-04-25)：`full-reading` 全自动综合解盘 + 三条入口路径路由
- **v3.7.0** (2026-04-25)：7 大新模块（分盘/相位/Jaimini/Nakshatra/Argala/Tajika/合盘）
- **v3.6.0** (2026-04-24)：报告生成器 + R2b 校验 + P3/P8/冲突仲裁
- **v3.5.0** (2026-04-24)：BPHS 完整表校准 + R1-R10 验证 + P1-P12 审计

## 📄 许可证

本项目仅供学习与研究使用。

## 🙏 致谢

- [Swiss Ephemeris](https://www.astro.com/swisseph/) — 天文计算核心
- KN Rao 学派框架 — 方法论参考
- CNWU16/vedic-astro-skills — 报告生成器灵感
- BPHS（Brihat Parashara Hora Shastra）— 经典理论来源
