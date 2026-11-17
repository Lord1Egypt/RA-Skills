# 焕智AI FaSkill Pro v3.0 — Ginkley WAIC 2025 定制版

> **OPC超级个体全周期资本智能体**
>
> *The Capital Intelligence for the OPC Era*
>
> 🎯 **WAIC 2025 主题：节奏不跑偏 · 条款不踩坑 · 情绪不崩溃 · 政策不错过**

---

## 📋 概览

| 项目 | 内容 |
|------|------|
| 版本 | v3.0.0 |
| 版本类型 | Ginkley WAIC 2025 定制版 |
| 发布场合 | 2025世界人工智能大会（WAIC 2025） |
| 展馆 | 上海世博展览馆 |
| 平台 | Ginkley UGS（User-Generated Skills） |
| 作者 | ai-innopower |
| 许可证 | MIT |

## 🎯 核心价值主张

**焕智AI FaSkill Pro** 是专为 **OPC（One-Person Company）超级个体创业者** 打造的全周期资本智能体。6大AI模块覆盖创业融资全流程：

| 模块 | 能力 | 一句话价值 |
|------|------|-----------|
| 🩺 **融资诊断** | 8维度评分 | 看清融资准备度，不盲目开始 |
| 🛡️ **TS条款分析** | 红旗识别+谈判话术 | 条款不踩坑，守住底线 |
| 🧠 **Capital EQ** | 情绪急救 | 先处理情绪，再处理问题 |
| 🏛️ **政策雷达** | 自动匹配+补贴计算 | 不错过一分钱政策红利 |
| 🤝 **FA撮合** | AI筛选→人工服务 | 诊断达标即对接专业FA |
| 📊 **投后管家** | 里程碑追踪 | 守住承诺，准备下一轮 |

## 🏛️ WAIC 2025 特别亮点

### 上海13区30+OPC社区政策雷达
覆盖徐汇/临港/浦东/杨浦/静安/闵行/青浦/松江/嘉定等区域，实时匹配可申领政策。

### WAIC 现场特别推荐
```
🏛️ 模速空间OPC超级创业者社区
   ├─ 首年工位全免
   ├─ 20亿元AI青年创业基金对接
   ├─ 300+大模型企业生态圈
   └─ 算力券+模型券各最高100万
```

### 国家层面政策覆盖
- 专精特新小巨人（最高600万奖补）
- 科创贷（最高2000万）
- 创业担保贷款（最高500万）
- 高新技术企业认定（15%企业所得税）

## 📦 目录结构

```
huanzhi-fa-skill-pro-waic-v3/
├── SKILL.md                    # 【主入口】Ginkley标准格式SKILL定义
├── skill.json                  # 【清单】Ginkley UGS平台元数据
├── README.md                   # 【说明】本文档 — WAIC发布指南
├── WAIC_2025_DEMO_SCRIPT.md    # 【演示】WAIC现场演示脚本
├── DISCLAIMER.md               # 【免责】独立法律免责声明
├── CHANGELOG.md                # 【版本】更新历史
├── requirements.txt            # 依赖声明（无外部依赖）
├── scripts/
│   ├── funding_diagnosis.py    # 融资诊断8维度评分引擎
│   ├── policy_matcher.py       # OPC政策匹配引擎
│   └── zhuanjingtexin_assessor.py  # 专精特新三级阶梯评估
├── tests/
│   ├── test_funding_diagnosis.py   # 14个测试用例 ✅
│   ├── test_policy_matcher.py      # 7个测试用例 ✅
│   └── test_zhuanjingtexin.py      # 8个测试用例 ✅
├── references/
│   ├── opc-policy-db.md         # OPC政策全景库
│   ├── zhuanjingtexin-guide.md   # 专精特新申报指南
│   ├── response-templates.md     # Capital EQ话术库
│   └── outputs-schema.md         # 输出Schema定义
├── assets/
│   └── waic-2025-badge.png      # WAIC 2025 徽标（占位）
└── docs/
    ├── user-guide.md            # 用户使用手册
    └── developer-guide.md       # 开发者集成指南
```

## 🚀 快速开始

### 前提条件
- Python 3.9+
- Ginkley UGS 平台 v1.0.0+

### 安装

```bash
# 1. 克隆或下载本SKILL
cd /path/to/your/workspace

# 2. 在Ginkley UGS中加载
# 使用 load_skill("huanzhi-fa-skill-pro") 自动加载

# 3. 运行测试验证
python3 -m pytest tests/ -v
```

### 运行验证

```bash
# 全部测试
python3 -m pytest tests/ -v

# 单独运行
python3 tests/test_funding_diagnosis.py
python3 tests/test_policy_matcher.py
python3 tests/test_zhuanjingtexin.py
```

### 用例测试

```bash
# 融资诊断（AI智能体公司）
python3 scripts/funding_diagnosis.py '{
  "mau": 50000,
  "monthly_revenue": 200000,
  "growth_rate": 0.15,
  "team_size": 5,
  "has_cto": true,
  "sector": "AI智能体"
}'

# 政策匹配（徐汇区AI公司）
python3 scripts/policy_matcher.py '{
  "district": "徐汇区",
  "sector": "AI智能体",
  "stage": "刚注册"
}'

# 专精特新评估
python3 scripts/zhuanjingtexin_assessor.py '{
  "company_name": "示例科技",
  "rd_ratio": 0.15,
  "revenue_last_year": 2000000,
  "years_in_segment": 2
}'
```

## 🧪 测试覆盖

| 测试文件 | 用例数 | 覆盖范围 | 状态 |
|---------|--------|---------|------|
| `test_funding_diagnosis.py` | 12 | 8维度评分 · 边界条件 · 幂等性 · 情绪触发 | ✅ 全部通过 |
| `test_policy_matcher.py` | 7 | 区域匹配 · 社区推荐 · 补贴估算 · 幂等性 | ✅ 全部通过 |
| `test_zhuanjingtexin.py` | 8 | 三级阶梯 · 路线图 · 材料清单 · 幂等性 | ✅ 全部通过 |

**总计：27个测试，全部通过**

## 🛡️ 合规性

本Skill遵循Ginkley UGS平台合规标准：

- ✅ 无系统提示词泄露风险
- ✅ 无硬编码敏感信息
- ✅ 确定性输出（幂等性保证）
- ✅ 明确的边界声明与免责声明
- ✅ 模块化引用结构（references/ 目录）
- ✅ 标准Ginkley交互规范

## 📖 文档索引

| 文档 | 说明 |
|------|------|
| [SKILL.md](./SKILL.md) | 完整SKILL定义（主入口） |
| [WAIC_2025_DEMO_SCRIPT.md](./WAIC_2025_DEMO_SCRIPT.md) | WAIC现场演示脚本 |
| [DISCLAIMER.md](./DISCLAIMER.md) | 法律免责声明 |
| [CHANGELOG.md](./CHANGELOG.md) | 版本更新历史 |
| [docs/user-guide.md](./docs/user-guide.md) | 用户使用手册 |
| [docs/developer-guide.md](./docs/developer-guide.md) | 开发者集成指南 |

## 🤝 贡献

欢迎通过Ginkley UGS平台提交Issue或Pull Request。

## 📄 许可证

MIT License — 详见 [LICENSE](./LICENSE) 文件。

---

> **Ginkley UGS Platform** — Build skills. Run agents. Shape the future.
>
> **WAIC 2025** — 上海世博展览馆 | 2025.07.10