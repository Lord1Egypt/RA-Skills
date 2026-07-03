# X.com 投资分析方法论复刻 Skill

## 功能概述

完整复刻 **@jukan05**（GF Securities 海外电子分析师，150K+ X 平台粉丝）的投资分析体系，对任意个股、行业或市场生成**「就像 Jukan05 本人撰写」**的结构化分析报告。

### 核心哲学（已修正）
> **「先识别快速成长的趋势，再在趋势中找最受益的环节。」**
> 
> - **趋势识别** = 出发点（这个趋势够大吗？还在早期吗？）
> - **瓶颈定位** = 筛选方法（最受益环节往往是瓶颈环节）
> - **技术验证** = 核心指标（良率/交期/产能/LTA）
> - **信息源评级** = 可信度判断（S/A/B/C/D 五级）
> - **执行风控** = Jukan 式操作（集中但不赌博、公开认错）

---

## 使用方法

### 触发方式
在对话中输入以下任意指令：
```
用 jukan 的方法分析 [标的]
jukan 会怎么看 [标的]？
按照 jukan 的风格分析 [行业/市场]
```

### 执行流程（AI 自动完成）
1. **识别标的** → 加载 Jukan 历史观点（如有）
2. **趋势识别** → 联网搜索回答：趋势够大吗？还在早期吗？
3. **瓶颈定位** → 在趋势中找最受益环节
4. **技术验证** → 获取良率/交期/产能/LTA 最新数据
5. **信息源评级** → 按 S/A/B/C/D 评级引用来源
6. **输出报告** → Jukan 风格（技术细节 + 免责声明）

---

## 参数说明

本 Skill 为**方法论指令集**，无命令行参数。AI 会根据 `SKILL.md` 中的详细指令自动执行分析。

### 支持的标的类型
| 类型 | 示例 | 处理方式是 |
|------|------|-------------|
| **个股（Jukan 分析过）** | SK Hynix、Samsung、NVIDIA | 加载 `references/jukan_views/*.md` 并引用历史观点 |
| **个股（Jukan 未分析）** | Tesla、腾讯、宁德时代 | 用 Jukan 框架推导分析 |
| **行业/主题** | HBM/内存、先进封装、中国国产化 | 按趋势识别 → 瓶颈定位分析 |
| **市场** | 半导体周期、AI 算力需求 | 宏观趋势 + 受益环节分析 |

---

## 输入输出格式

### 输入
- **用户指令**：自然语言（中文/英文均可）
- **数据来源**：实时联网搜索（行情、新闻、研报）+ Jukan 历史观点（如有）

### 输出结构（Jukan 风格）
```
[开场白] FWIW / FYI 风格引入
  ↓
[趋势识别] 这个趋势是什么、够大吗、还在早期吗
  ↓
[瓶颈定位] 为什么这个标的是最受益环节
  ↓
[技术验证] 良率/交期/产能/LTA 数据（精确到数值）
  ↓
[信息源] 按 S/A/B/C/D 评级列出引用来源
  ↓
[标的定位] A/B/C/D 区 + Jukan 式建议
  ↓
[执行建议] 建仓时机、仓位管理、止损信号
  ↓
[免责声明] Not investment advice | DYODD
```

### 输出格式选项
| 格式 | 触发方式 | 说明 |
|------|---------|------|
| **对话回复** | 默认 | 直接在对话中输出 Jukan 风格分析 |
| **Word 文档** | 用户要求「生成报告」「保存为文档」 | 调用 `scripts/analyze.py` 生成 `.docx` |

---

## 依赖项

### Python 依赖（用于生成 Word 报告）
```bash
pip install python-docx
```

### 联网搜索工具（任选其一）
| 工具 | 用途 | 优先级 |
|------|------|--------|
| `web-tools` Skill | Web Search + Fetch | 推荐 |
| `westock-data` Skill | 金融数据查询 | 推荐（如有） |
| `WebSearch` + `WebFetch` | 内置工具（无 Skill 时） | 备选 |

### 可选：Jukan 历史推文数据
- 放置于 `jukan05_data/jukan05_tweets.csv`（2454 条）
- 用于提取历史观点到 `references/jukan_views/*.md`
- **非必须** — 即便没有，Skill 仍可用 Jukan 框架分析任意标的

---

## 注意事项

### 1. 不是投资建议
- Jukan 每次分析都加 `Not investment advice | DYODD`
- **你必须同样做** — 每篇分析结尾必须加免责声明

### 2. 区分事实和观点
- Jukan 的观点：用「他认为」「Jukan 式分析指出」
- 事实：用「数据显示」「财报确认」

### 3. 承认盲区
- 若某数据无法获取（如非上市公司的良率），明确说明「无法验证，需渠道检查」

### 4. 不过度自信
- Jukan 会公开认错（Marvell/LG Innotek 案例）
- 你的分析也应留有修正空间

### 5. 聚焦半导体/AI
- Jukan 90% 内容在此，分析其他行业时需说明：
  > 「Jukan 较少覆盖此领域，以下分析为其方法论的推导应用」

### 6. Cookie 过期处理（如需抓取最新推文）
- X.com Cookie 通常有效期为 **2-3 个月**
- 过期后需重新导出并更新 `jukan05_data/x_cookies.json`
- 参考 `x-scraper-cookie` Skill 的 Cookie 管理流程

---

## 文件结构

```
x-investment-strategy-analyzer/
├── SKILL.md                          # 核心指令文件（五层分析法）
├── README_zh.md                     # 中文说明（本文件）
├── README_en.md                     # English documentation
├── scripts/
│   └── analyze.py                  # 报告生成器（Word 输出）
└── references/
    ├── jukan_framework_universal.md  # 五层分析法详细说明
    ├── jukan_style_guide.md         # Jukan 语言风格指南（Few-shot）
    └── jukan_views/                # Jukan 历史观点库（可选）
        ├── sk_hynix.md
        ├── samsung.md
        ├── nvidia.md
        ├── tsmc.md
        ├── intel.md
        ├── memory_hbm.md
        ├── china_semiconductor.md
        └── foundry.md
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-01 | 初始版本（通用五维框架） |
| v2.0 | 2026-07-01 | 注入 Jukan 知识库 + 风格指南 |
| v3.0 | 2026-07-01 | 通用化改造（支持任意标的） |
| **v4.0** | **2026-07-02** | **修正核心哲学：「趋势识别优先」而非「瓶颈理论」** |

---

## 10 个英文 Tags

```
X.com, Twitter, investment analysis, semiconductor, AI, trend identification, 
supply chain bottleneek, growth stock, Jukan05, financial framework
```
