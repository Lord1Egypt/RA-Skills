# paper-polisher-pro — 论文润色降重一站式工具

> 🎯 **AI痕迹检测 · 去AI味改写 · 智能降重 · 术语标准化 · 综合质量报告**
> 中英双语 · 纯本地运行 · 数据不出本机 · 零配置

## 核心亮点

大多数AI检测器只能识别ChatGPT。**这是唯一能指纹识别中文大模型的开源工具**——DeepSeek V4、GLM-5/5.1、Qwen 3.5/3.6、Kimi K2.5/K2.6、MiniMax M2.5、Step，以及GPT、Claude、Gemini。

**2026旗舰模型实测（长文本学术论文）：**
- 准确率 98.0% · 精确率 96.7% · 召回率 100% · F1 98.3%
- 10个模型测试：GLM-5、GLM-5.1、GLM-4.7、Kimi-K2.6、Kimi-K2.5、MiniMax-M2.5、DeepSeek-V3.2、DeepSeek-R1——全部100%检出
- 100字以上文本零漏检

## 触发词

"润色论文", "降AI检测", "查AI写作", "论文润色", "改写论文", "去AI味", "AI论文检测", "学术写作助手", "AI写作检测", "去除AI痕迹", "人化AI文本", "毕业论文润色", "学位论文降重", "SCI论文编辑", "手稿润色", "AI写作评分"

## 快速开始

### 检测AI痕迹

```bash
python3 {{SKILL_DIR}}/scripts/ai_detector.py your_paper.txt --lang auto
```

输出示例：
```
📄 your_paper.txt
AI Risk Score: 68.5 / 100 🔴 高风险
分析段落数: 12
主要特征: "值得注意的是" (×3), "具有重要作用" (×2)
建议: 改写第2、5、8段
```

### 术语标准化检查

```bash
python3 {{SKILL_DIR}}/scripts/term_check.py your_paper.txt
```

### 综合质量报告

```bash
python3 {{SKILL_DIR}}/scripts/quality_report.py your_paper.txt --format json
```

---

## AI检测引擎（v1.1.0）

### 九层评分系统

| 层级 | 权重 | 检测内容 |
|------|------|----------|
| 模式匹配 | 50 | 1,002条模型专属AI特征（中文663 + 英文339） |
| 突变性 | 20 | 三组件方差分析（人类写作不均匀） |
| TTR词汇丰富度 | 15 | 词汇多样性 |
| 困惑度 | 15 | 统计可预测性 |
| 信息密度 | 15 | 内容密度 vs 填充词比例 |
| 句式模板 | 10 | 公式化句式结构 |
| 开头模式 | 10 | 可预测的段落起始词 |
| 长度分布 | 5 | 不自然的均匀性 |
| RLHF对齐 | +加分 | 讨好型/对齐化表达 |

### 支持的AI模型（2026实测）

**中文大模型（独家指纹识别）：**
DeepSeek V4 · V3.2 · R1 · GLM-5 · GLM-5.1 · GLM-4.7 · Qwen 3.5-397B · Qwen 3.6 · Kimi K2.5 · K2.6 · MiniMax M2.5 · Step

**国际模型：** ChatGPT · Claude · Gemini

### 模式库

| 语言 | 模式数 | 分类数 |
|------|--------|--------|
| 中文 | 663 | 18类（过渡词、结构标记、医学模板、RLHF对齐、Kimi/DeepSeek/GLM指纹等） |
| 英文 | 339 | 9类（学术正式语、填充短语、Markdown痕迹、RLHF对齐等） |

另有：501组同义词库、25条中文句式模板。

---

## 完整工作流

### 第1步：AI检测 → 评分 + 特征分析

```bash
python3 {{SKILL_DIR}}/scripts/ai_detector.py <文件> --lang auto --format json --output report.json
```

返回0–100分AI风险评分、风险等级、每段匹配特征。

### 第2步：去AI改写（评分≥35的段落）

**中文：** 删除填充词（"值得注意的是"、"综上所述"），打破对称结构，用数据替换模糊评价，变化句长，使用内容驱动的过渡。

**英文：** 禁用AI标志词（plays a crucial role, has gained significant attention, delve into, myriad, plethora），使用主动语态，混合5–30词句长。

### 第3步：智能降重（5层策略）

1. 同义词替换（501组，跳过受保护术语）
2. 语态转换（主动 ↔ 被动）
3. 语序调整
4. 抽象 ↔ 展开
5. 视角转换

### 第4步：术语标准化

2,255条权威术语（全国名词委 + MeSH 2026 + 药物术语），标记非标准用法并建议修正。

### 第5步：质量报告

改写前后对比：AI分数变化、段落级改善明细、术语规范率、可读性指标。

---

## 学科适配

- **医学/生物学**：保护临床术语、药名、剂量、统计数据
- **工程/计算机**：保护算法名称、公式、性能指标
- **人文/社科**：允许个性化表达，避免AI式总结
- **商业/经济学**：保护数据和模型名称，替换泛泛评论

## 使用约束

1. 绝不修改数据——数字、统计、引用保持原样
2. 2,255个专业术语在降重时自动保护
3. 语义保真——不增减信息
4. 逐段处理保持逻辑连贯
5. 所有修改需用户确认后生效

---

## 文件结构

```
paper-polisher/
├── SKILL.md                    ← 英文文档（ClawHub）
├── SKILL_ZH.md                 ← 本文件（中文，SkillHub）
├── scripts/
│   ├── ai_detector.py          ← AI检测引擎（v1.1.0，9层，1002条模式）
│   ├── perplexity.py           ← 困惑度评分模块
│   ├── term_check.py           ← 术语标准化（2,255条）
│   ├── ngram_similarity.py     ← N-gram重复分析
│   └── quality_report.py       ← 综合质量报告
├── references/
│   ├── ai_patterns_zh.json     ← 中文AI特征（663条，18类）
│   ├── ai_patterns_en.json     ← 英文AI特征（339条，9类）
│   ├── synonyms_general.json   ← 同义词词典（501组）
│   └── sentence_patterns_zh.json ← 中文句式模板（25条）
├── data/
│   └── terminology.json        ← 标准术语库（2,255条）
└── templates/                  ← 改写提示模板
```

## 版本历史

- **v1.1.0** — 重大升级：9层检测引擎（+困惑度、三组件突变性、句式模板、RLHF对齐），模式库扩展至1,002条（中文663 + 英文339），同义词库501组，10个2026旗舰模型实测F1=98.3%
- **v1.0.1** — 英文SKILL.md，SEO关键词优化
- **v1.0.0** — 初始发布
