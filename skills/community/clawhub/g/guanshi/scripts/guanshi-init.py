#!/usr/bin/env python3
"""
观势 (GuanShi) 初始化脚本
=========================
安装观势 Skill 后运行此脚本，自动完成：
1. 知识库骨架创建
2. 专业集群依赖检测 & 安装（自举模式）
用法：
    python3 scripts/guanshi-init.py
    python3 scripts/guanshi-init.py --path /custom/kb/path
    python3 scripts/guanshi-init.py --skip-kb       # 只装 Agent，不建知识库
    python3 scripts/guanshi-init.py --skip-agents   # 只建知识库，不装 Agent
"""

import os
import sys
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

DEFAULT_KB_PATH = os.path.expanduser("~/.hermes/strategy-knowledge")


def parse_args():
    parser = argparse.ArgumentParser(description="观势初始化")
    parser.add_argument("--path", default=DEFAULT_KB_PATH, help=f"知识库路径 (默认: {DEFAULT_KB_PATH})")
    parser.add_argument("--company", default="本公司", help="公司名称（用于模板占位符替换）")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    parser.add_argument("--skip-kb", action="store_true", help="跳过知识库初始化")
    parser.add_argument("--skip-agents", action="store_true", help="跳过专业 Agent 检测安装")
    parser.add_argument("--yes", action="store_true", help="非交互模式，自动确认")
    return parser.parse_args()


def create_dir(path):
    os.makedirs(path, exist_ok=True)
    print(f"  ✓ 创建目录: {path}")


def write_file(path, content, force=False):
    if os.path.exists(path) and not force:
        print(f"  ⏭ 跳过 (已存在): {path}")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ 创建文件: {path}")
    return True


# ==================== 知识库骨架 ====================

INDUSTRY_TEMPLATE = """# 行业数据模板

> ⚠️ 请根据目标行业替换以下内容。

## 行业基本信息
- 行业名称：
- 市场规模（当前/3年预测）：
- 年增长率：
- 产业链位置：

## 关键驱动因素
1. 
2. 
3. 

## 主要参与者
| 公司 | 市场份额 | 核心优势 | 战略方向 |
|------|---------|---------|---------|
| | | | |

## 监管环境
- 关键政策：
- 准入门槛：

---
*本模板供观势战略分析使用，请填充真实数据。*
"""

COMPANY_PROFILE_TEMPLATE = """# 公司档案模板

> ⚠️ 请替换为实际公司信息。

## 基本信息
- 公司名称：
- 成立时间：
- 主营业务：
- 营收规模：
- 员工数量：

## 业务组合
| 业务线 | 营收占比 | 增长率 | 市场地位 |
|--------|---------|--------|---------|
| | | | |

## 核心竞争力
1. 
2. 
3. 

## 战略方向（当前）
- 

## 组织架构
- 

---
*本档案供观势内部诊断使用，信息安全请自行把控。*
"""

COMPETITOR_TEMPLATE = """# 竞争对手档案模板

> ⚠️ 请为每个核心竞对创建独立文件。

## 基本信息
- 公司名称：
- 成立时间：
- 融资/上市状态：
- 营收规模（估算）：

## 战略意图
- 

## 资源禀赋
- 技术：
- 品牌：
- 渠道：
- 人才：
- 资本：

## 惯性约束
- 

## 近期动作
1. 
2. 

## 反应模式预判
- 

---
*数据来源：公开信息/行业报告/推断，标注置信度。*
"""

CASE_TEMPLATE = '{"case_id":"CASE-001","problem":"请填入案例问题","context":{"industry":"行业","market":"目标市场"},"analysis":{"method":"六步洞察法","findings":"关键发现"},"options":["选项1","选项2"],"recommendation":"推荐方案","outcome":"最终结果","date":"2025-01-01","tags":["市场进入","竞争分析"]}\n'

FRAMEWORKS_REFERENCE = """# 战略框架速查表

## PESTEL
P-政治 / E-经济 / S-社会 / T-技术 / E-环境 / L-法律

## 波特五力
1.供应商议价力 2.买家议价力 3.新进入者威胁 4.替代品威胁 5.同业竞争强度

## VRIO
V-有价值 R-稀缺 I-难以模仿 O-组织支撑 → 四项全部满足 = 可持续竞争优势

## 安索夫矩阵
现有市场+现有产品=市场渗透 | 现有市场+新产品=产品开发
新市场+现有产品=市场开发 | 新市场+新产品=多元化

## BCG 矩阵
高增长+高份额=明星 | 高增长+低份额=问号
低增长+高份额=金牛 | 低增长+低份额=瘦狗

## 情景规划
选取2个关键不确定性 → 构建2×2情景矩阵 → 推演战略选项
"""

README_TEMPLATE = """# 观势 (GuanShi) 知识库

> 本知识库为观势 AI 战略分析系统的数据源。
> 生成日期：{date}
> 生成工具：guanshi-init.py

## 目录结构

```
strategy-knowledge/
├── README.md                    ← 本文件
├── market_data/                 ← 行业与市场数据
│   └── industry_template.md
├── company_profiles/            ← 公司档案
│   ├── our_company.md
│   └── competitor_template.md
├── cases/                       ← 战略案例库
│   └── strategy_cases.jsonl
├── frameworks/                  ← 战略框架速查
│   └── frameworks_reference.md
└── research_notes/              ← 研究笔记（自由格式）
```

## 快速开始

1. **填充行业数据**：编辑 `market_data/` 下的模板
2. **填充公司档案**：编辑 `company_profiles/our_company.md`
3. **添加竞对档案**：为每个核心竞对创建 `company_profiles/竞对名.md`
4. **添加案例**：在 `cases/strategy_cases.jsonl` 中添加历史案例

## 自定义路径

```bash
export GUANSHI_KB_PATH=/your/custom/path
```
"""

# ==================== 专家集群 ====================

GUANSHI_DEPENDENCIES = [
    {"name": "战略分析专家", "slug": "guanshi-strategy-expert", "required": True,
     "description": "公司战略方向、业务组合优化、增长路径设计、战略执行评估"},
    {"name": "行业研究专家", "slug": "guanshi-industry-expert", "required": True,
     "description": "行业前景判断、市场规模测算、产业链分析、波特五力"},
    {"name": "竞争情报专家", "slug": "guanshi-competition-expert", "required": True,
     "description": "竞争对手深度画像、竞争格局分析、对标分析、博弈推演"},
    {"name": "组织诊断专家", "slug": "guanshi-org-expert", "required": True,
     "description": "组织架构诊断、人才与战略匹配、文化与战略一致性、变革准备度"},
    {"name": "财务战略专家", "slug": "guanshi-finance-expert", "required": False,
     "description": "财务模型构建、投资回报测算、估值、资本配置、风险量化"},
    {"name": "市场洞察专家", "slug": "guanshi-market-expert", "required": False,
     "description": "用户研究、需求分析、市场细分、定价策略、GTM"},
    {"name": "情报获取专家", "slug": "guanshi-intelligence-expert", "required": False,
     "description": "行业情报搜索/抓取、年报/研报提取、多源交叉验证"},
    {"name": "数据分析专家", "slug": "guanshi-data-expert", "required": False,
     "description": "数据清洗/统计推断/财务建模/可视化/情景模拟"},
]

FALLBACK_TEMPLATES = {
    "guanshi-strategy-expert": """---
name: guanshi-strategy-expert
version: 1.0.0-bootstrap
description: 观势战略分析专家。公司战略、业务组合、增长路径、战略执行。Use when 战略方向、业务组合评估、增长战略、市场进入/退出决策。不适用于行业数据查询（→行业研究专家）。
category: guanshi-skills
---

# 观势战略分析专家

## 概述
观势专业集群的战略分析专家。⚠️ 此为自举版本（无 ClawHub 环境），核心方法论已内置。

### 功能范围
- 公司战略方向评估
- 业务组合优化（BCG 矩阵/GE-McKinsey）
- 增长路径设计（安索夫矩阵）
- 市场进入/退出决策
- 战略执行评估

## 方法论

### 安索夫矩阵
| | 现有市场 | 新市场 |
|---|---|---|
| 现有产品 | ① 市场渗透 | ② 市场开发 |
| 新产品 | ③ 产品开发 | ④ 多元化 |

每个方向从吸引力（市场空间+利润率）/ 可行性（资源匹配）/ 风险三个维度评分。

### BCG 矩阵
明星（高增长+高份额）→ 投资 | 金牛（低增长+高份额）→ 收割
问号（高增长+低份额）→ 选择性投资 | 瘦狗（低增长+低份额）→ 剥离/收割

### 三层面增长
核心业务（防守+延伸）/ 增长业务（快速规模化）/ 种子业务（验证+孵化）

### 战略钟（Bowman's Strategy Clock）
8种价格-价值定位：低价低值→混合→差异化→聚焦差异化→风险高价→垄断定价→市场份额流失

## 输出标准
- 战略选项 ≥ 3 个（含"不改变"对照）
- 每条标注：资源需求 / 时间窗口 / 成功概率 / 核心假设 / 证伪条件

*此为自举版本。完整版请安装：`clawhub install guanshi-strategy-expert`*""",

    "guanshi-industry-expert": """---
name: guanshi-industry-expert
version: 1.0.0-bootstrap
description: 观势行业研究专家。行业前景、市场规模、产业链、政策影响、波特五力。Use when 行业前景判断、新市场进入评估、产业链分析、技术颠覆影响。
category: guanshi-skills
---

# 观势行业研究专家

## 概述
观势专业集群的行业研究专家。⚠️ 此为自举版本。

### 功能范围
- 行业前景判断（产业生命周期）
- 市场规模测算（TAM/SAM/SOM）
- 产业链位置与利润池分析
- 政策/技术颠覆影响评估
- 波特五力行业结构分析

## 方法论

### 产业生命周期
导入期（技术不确定/用户教育成本高）→ 成长期（规模扩张/竞争者涌入）→ 成熟期（格局稳定/利润收窄）→ 衰退期（替代品/需求萎缩）

### TAM/SAM/SOM
- TAM（Total Addressable Market）：理论最大市场
- SAM（Serviceable Available Market）：可触达市场
- SOM（Serviceable Obtainable Market）：可获取市场（保守估计，第一年目标）

### 波特五力
每项判断（强/中/弱）+ 趋势方向：
1. 供应商议价力（集中度/切换成本/前向整合威胁）
2. 买家议价力（集中度/差异化/切换成本）
3. 新进入者威胁（规模经济/资本需求/渠道/政策壁垒）
4. 替代品威胁（性价比/切换成本/替代意愿）
5. 同业竞争强度（竞争者数量/行业增长率/退出壁垒）

## 输出标准
- 行业规模（当前 + 3年预测）含置信度
- 五力每项判断 + 趋势 + 证据

*此为自举版本。完整版请安装：`clawhub install guanshi-industry-expert`*""",

    "guanshi-competition-expert": """---
name: guanshi-competition-expert
version: 1.0.0-bootstrap
description: 观势竞争情报专家。竞争对手画像、竞争格局、对标分析、博弈推演。Use when 竞对分析、市场份额变化、竞争策略、对手下一步预判。
category: guanshi-skills
---

# 观势竞争情报专家

## 概述
观势专业集群的竞争情报专家。⚠️ 此为自举版本。

### 功能范围
- 竞争对手深度画像
- 竞争格局分析与战略群组
- 对标分析（Benchmarking）
- 博弈推演（对手反应预测）

## 方法论

### 竞对画像四维度
1. **战略意图**：他们要什么？（市场份额/利润/技术领先/生态控制）
2. **资源禀赋**：他们有什么？（技术/品牌/渠道/人才/资本/数据）
3. **惯性约束**：他们被什么限制？（组织惯性/文化/既有客户/监管/技术路径依赖）
4. **反应模式**：他们怎么回应？（激进/保守/模仿/差异化）

### 战略群组图
- 选取 2 个正交竞争维度
- 标出核心玩家 → 圈出战略群组
- 分析群组间迁移壁垒

### 价值曲线对比
- 选取 6-8 个关键价值元素
- 绘制自身 vs 对手表现曲线
- 识别：哪些元素过度竞争？哪些被忽略？

### 博弈推演
- 囚徒困境场景（如价格战）
- 先发优势评估
- 承诺机制（不可逆投资/排他协议）

## 输出标准
- 核心竞对 3-5 家深度画像
- 竞争反应模式预判（对每种战略选项）

*此为自举版本。完整版请安装：`clawhub install guanshi-competition-expert`*""",

    "guanshi-org-expert": """---
name: guanshi-org-expert
version: 1.0.0-bootstrap
description: 观势组织诊断专家。组织架构、人才与战略匹配、文化与战略一致性、变革准备度。Use when 战略落地遇阻、组织能力评估、变革规划。深度HR诊断建议桥接谛听。
category: guanshi-skills
---

# 观势组织诊断专家

## 概述
观势专业集群的组织诊断专家。专注于组织能力与战略的匹配度，不覆盖深度 HR 诊断（薪酬/离职/敬业度 → 建议桥接谛听）。

### 功能范围
- 组织架构与战略匹配
- 人才梯队与战略需求差距
- 文化与战略一致性
- 变革准备度评估（ADKAR）

## 方法论

### 麦肯锡 7S
战略/结构/制度/风格/人员/技能/共同价值观 —— 七要素需相互匹配。

### 组织能力杨三角
组织能力 = 员工思维 × 员工能力 × 员工治理（乘法关系，短板决定上限）

### ADKAR 变革准备度
Awareness → Desire → Knowledge → Ability → Reinforcement
评估每阶段当前水平（1-5分），识别瓶颈。

## 输出标准
- 组织能力与战略匹配度评分（1-5）
- 关键缺口清单 + 补齐优先级

## 桥接谛听
涉及深层 HR 诊断（离职分析/薪酬公平/文化根因/敬业度），建议同步启动 ` /谛听 `

*此为自举版本。完整版请安装：`clawhub install guanshi-org-expert`*""",

    "guanshi-finance-expert": """---
name: guanshi-finance-expert
version: 1.0.0-bootstrap
description: 观势财务战略专家。财务模型、投资回报、估值、资本配置、风险量化。Use when 并购评估、投资决策、战略成本分析、市场进入财务可行性。
category: guanshi-skills
---

# 观势财务战略专家

## 概述
观势专业集群的财务战略专家。⚠️ 此为自举版本。

### 功能范围
- 战略投资财务模型
- NPV/IRR/回收期测算
- 敏感性分析
- 情景财务建模（乐观/基准/悲观）
- 资本配置建议

## 方法论

### NPV/IRR/回收期
- NPV（净现值）：未来现金流折现 - 初始投资。NPV > 0 = 创造价值
- IRR（内部收益率）：NPV=0 时的折现率。IRR > 资本成本 = 可接受
- 回收期：收回初始投资所需年数

### 敏感性分析
关键变量 ±20%，观察 NPV 变化幅度。变化最大的变量 = 需要重点监控的风险点。

### 情景财务建模
乐观/基准/悲观三种情景，每种给出关键假设差异。

## 输出标准
- 财务模型关键假设清单
- ROI 区间（非点估计）+ 敏感性分析

*此为自举版本。完整版请安装：`clawhub install guanshi-finance-expert`*""",

    "guanshi-market-expert": """---
name: guanshi-market-expert
version: 1.0.0-bootstrap
description: 观势市场洞察专家。用户研究、需求分析、市场细分、定价策略、GTM。Use when 用户画像、需求验证、市场细分、定价、渠道策略。
category: guanshi-skills
---

# 观势市场洞察专家

## 概述
观势专业集群的市场洞察专家。⚠️ 此为自举版本。

### 功能范围
- 用户研究与画像
- 需求分析（JTBD）
- 市场细分
- 定价策略设计
- GTM（Go-to-Market）策略

## 方法论

### JTBD（Jobs to be Done）
用户"雇佣"产品是为了完成什么任务？
- 功能性任务（解决什么问题）
- 情感性任务（满足什么感受）
- 社会性任务（表达什么身份）

### 市场细分四维度
地理 / 人口 / 行为 / 需求 → 选取 1-2 个核心维度切分

### 定价三导向
- 成本导向：成本 + 目标利润率
- 竞争导向：对标竞品定价
- 价值导向：客户感知价值定价（上限 = 客户愿意支付的最高价）

### GTM 策略
目标客群 → 价值主张 → 渠道策略 → 定价策略 → 启动节奏

## 输出标准
- 目标客群画像（含 JTBD）
- 定价区间建议 + 理由

*此为自举版本。完整版请安装：`clawhub install guanshi-market-expert`*""",

    "guanshi-intelligence-expert": """---
name: guanshi-intelligence-expert
version: 1.0.0-bootstrap
description: 观势情报获取专家。行业情报搜索/抓取、年报/研报提取、多源交叉验证。Use when 行业数据抓取、竞对营收数据搜索、研报/白皮书提取、情报缺口填充。
category: guanshi-skills
---

# 观势情报获取专家

## 概述
观势专业集群的情报获取专家。⚠️ 此为自举版本。

### 功能范围
- 多引擎行业情报搜索（年报/券商研报/行业白皮书）
- 页面正文抓取与关键数字提取
- PDF/研报下载与文本提取
- 多源交叉验证与置信度标注
- 结构化情报摘要输出

## 方法论

### 搜索-过滤-提取-验证流水线
1. **搜索**：web_search 多关键词（中英双语并行，目标 ≥ 3 源）
2. **过滤**：按来源可信度筛选（年报/研报 > 第三方报告 > 媒体）
3. **提取**：web_fetch 抓取正文，识别关键数字和表格
4. **验证**：多源对比，标注一致/冲突，给出置信度

## 输出标准
- 标准化 JSON 摘要：source/date/key_findings/confidence/raw_text_ref
- 时效性标注：超过2年 "[数据可能过时]"，超过5年 "[历史参考]"
- 无法获取的数据标注 "[情报缺口]"

*此为自举版本。完整版请安装：`clawhub install guanshi-intelligence-expert`*""",

    "guanshi-data-expert": """---
name: guanshi-data-expert
version: 1.0.0-bootstrap
description: 观势数据分析专家。数据清洗/统计推断/财务建模/可视化/情景模拟。Use when 数据处理、统计分析、ROI测算、敏感性分析、数据可视化、情景推演。
category: guanshi-skills
---

# 观势数据分析专家

## 概述
观势专业集群的数据分析专家。⚠️ 此为自举版本。

### 功能范围
- 数据清洗与标准化（缺失值/异常值/单位统一）
- 统计推断（趋势检验/相关性/假设检验）
- 财务建模（NPV/IRR/回收期/盈亏平衡）
- 敏感性分析（±20%关键变量）
- 数据可视化（折线/柱状/散点/饼图/瀑布图）
- 情景模拟（乐观/基准/悲观）

## 方法论

### CRISP-DM
业务理解 → 数据理解 → 数据准备 → 建模 → 评估 → 部署

### 统计显著性标注
*** p<0.001 / ** p<0.01 / * p<0.05 / n.s. 不显著

### 财务建模
NPV = Σ(CFt/(1+r)^t) - I0，折现率建议 8%-12%

## 输出标准
- 图表 PNG 输出到 output 目录，命名含主题+类型+时间戳
- 统计结果标注 p 值和置信区间
- 财务建模标注折现率假设和推导依据

*此为自举版本。完整版请安装：`clawhub install guanshi-data-expert`*""",
}


def get_installed_skills(skills_base=None):
    installed = set()
    if skills_base:
        base = Path(skills_base)
        if base.exists():
            for entry in base.iterdir():
                if entry.is_dir() and (entry / "SKILL.md").exists():
                    installed.add(entry.name)
    try:
        result = subprocess.run(["hermes", "skills", "list"], capture_output=True, text=True, timeout=10)
        for line in (result.stdout + result.stderr).split("\n"):
            parts = [p.strip() for p in line.split("│")]
            if len(parts) >= 2 and parts[1]:
                installed.add(parts[1])
    except Exception:
        pass
    try:
        global_skills = Path(os.path.expanduser("~/.hermes/skills"))
        if global_skills.exists():
            for entry in global_skills.iterdir():
                if entry.is_dir() and (entry / "SKILL.md").exists():
                    installed.add(entry.name)
    except Exception:
        pass
    return installed


def is_skill_installed(slug, installed_slugs, skills_base=None):
    if skills_base:
        dir_path = Path(skills_base) / slug
        if dir_path.exists() and (dir_path / "SKILL.md").exists():
            return True
        return False
    if slug in installed_slugs:
        return True
    for installed in installed_slugs:
        installed_clean = installed.rstrip("…")
        if slug.startswith(installed_clean) and len(installed_clean) >= len(slug) - 5:
            return True
    return False


def bootstrap_agent(slug, name, description, skills_base):
    agent_dir = Path(skills_base) / slug
    agent_dir.mkdir(parents=True, exist_ok=True)
    skill_content = FALLBACK_TEMPLATES.get(slug, "")
    if not skill_content:
        return False
    with open(agent_dir / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_content)
    meta = {"source": "bootstrap", "slug": slug, "version": "1.0.0",
            "bootstrapped_at": datetime.now().isoformat(),
            "note": "自举创建的本地版本，请用 clawhub install 替换为官方版本"}
    with open(agent_dir / "_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return True


def check_and_install_agents(skills_base, force_install=False, no_input=False):
    print("\n" + "=" * 50)
    print("🔍 观势专业集群依赖检测")
    print("=" * 50)

    installed_slugs = get_installed_skills(skills_base)
    missing = []
    installed = []
    failed = []

    for dep in GUANSHI_DEPENDENCIES:
        slug = dep["slug"]
        name = dep["name"]
        if is_skill_installed(slug, installed_slugs, skills_base):
            print(f"  ✅ {name} ({slug}) 已安装")
            installed.append(slug)
        else:
            status = "必需" if dep["required"] else "可选"
            print(f"  ⚠️ {name} ({slug}) 未安装 [{status}]")
            missing.append(dep)

    if not missing:
        print("\n🎉 所有专业 Agent 已就绪！观势专业集群运行正常。")
        return {"installed": installed, "missing": [], "failed": []}

    required_missing = [d for d in missing if d["required"]]
    if required_missing:
        print(f"\n📦 发现 {len(required_missing)} 个必需 Agent 未安装")

    should_install = force_install or no_input
    if not should_install:
        print(f"\n是否需要自动安装全部 Agent？")
        try:
            resp = input("输入 Y 安装 / N 跳过 [Y/n]: ").strip().lower()
            if resp == "n":
                print("⏭ 跳过安装。观势将以降级模式运行。")
                return {"installed": installed, "missing": [d["slug"] for d in missing], "failed": []}
        except EOFError:
            pass

    to_install = missing
    print(f"\n📥 开始安装 {len(to_install)} 个 Agent（自举模式）...")
    print("-" * 40)

    for dep in to_install:
        slug = dep["slug"]
        name = dep["name"]
        print(f"  → 安装 {name} ({slug})...", end=" ", flush=True)

        # Try ClawHub API first
        installed_ok = False
        try:
            import urllib.request, zipfile, io
            url = f"https://clawhub.ai/api/v1/download?slug={slug}"
            req = urllib.request.Request(url, headers={"User-Agent": "GuanShi-Init/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                zip_data = resp.read()
            if zip_data and len(zip_data) > 100:
                target_dir = Path(skills_base) / slug
                target_dir.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
                    zf.extractall(target_dir)
                subdirs = [d for d in target_dir.iterdir() if d.is_dir()]
                if len(subdirs) == 1 and subdirs[0].name == slug:
                    nested = subdirs[0]
                    for item in nested.iterdir():
                        dest = target_dir / item.name
                        if dest.exists():
                            import shutil
                            shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
                        item.rename(dest)
                    nested.rmdir()
                if (target_dir / "SKILL.md").exists():
                    print("✅ 成功（从 ClawHub 下载）")
                    installed.append(slug)
                    installed_ok = True
        except Exception:
            pass

        # Fallback to bootstrap
        if not installed_ok:
            if bootstrap_agent(slug, name, dep.get("description", ""), skills_base):
                print("✅ 自举创建成功")
                installed.append(slug)
            else:
                print("❌ 自举失败")
                failed.append(slug)

    print("\n" + "=" * 50)
    if failed:
        print(f"⚠️ 专业集群部分就绪：✅ {len(installed)} 个 / ❌ {len(failed)} 个")
    else:
        print(f"🎉 专业集群就绪！{len(installed)} 个专业 Agent 可用。")
    print("=" * 50)
    return {"installed": installed, "missing": [], "failed": failed}


# ==================== 知识库初始化 ====================

def init_knowledge_base(kb_path, company_name="本公司", force=False):
    kb_path = Path(kb_path)
    print(f"\n🚀 初始化观势知识库: {kb_path}")
    print(f"   公司名称: {company_name}\n")

    print("📁 创建目录结构...")
    dirs = ["market_data", "company_profiles", "cases", "frameworks", "research_notes"]
    for d in dirs:
        create_dir(kb_path / d)

    print("\n📝 创建模板文件...")
    files = {
        "market_data/industry_template.md": INDUSTRY_TEMPLATE,
        "company_profiles/our_company.md": COMPANY_PROFILE_TEMPLATE,
        "company_profiles/competitor_template.md": COMPETITOR_TEMPLATE,
        "frameworks/frameworks_reference.md": FRAMEWORKS_REFERENCE,
        "cases/strategy_cases.jsonl": CASE_TEMPLATE.strip(),
        "README.md": README_TEMPLATE.format(date=datetime.now().strftime("%Y-%m-%d")),
    }

    created = 0
    for rel_path, content in files.items():
        if write_file(kb_path / rel_path, content, force):
            created += 1

    print(f"\n✅ 知识库初始化完成！")
    print(f"   路径: {kb_path}")
    print(f"   创建: {created} 个文件\n")
    print("📋 下一步：")
    print("   1. 编辑 market_data/industry_template.md → 填入目标行业数据")
    print("   2. 编辑 company_profiles/our_company.md → 填入公司信息")
    print("   3. 为每个核心竞对创建 company_profiles/竞对名.md")
    print("   4. 在 cases/strategy_cases.jsonl 中添加历史案例")
    print(f"\n💡 自定义路径：export GUANSHI_KB_PATH=/your/path")


# ==================== 主流程 ====================

if __name__ == "__main__":
    args = parse_args()

    _script_dir = Path(__file__).resolve().parent.parent  # guanshi/
    skills_base = str(_script_dir.parent)  # skills root

    if not args.skip_kb:
        init_knowledge_base(args.path, args.company, args.force)

    if not args.skip_agents:
        check_and_install_agents(skills_base, force_install=args.force, no_input=args.yes)

    print("\n" + "=" * 50)
    print("🎉 观势初始化完成！")
    print("=" * 50)