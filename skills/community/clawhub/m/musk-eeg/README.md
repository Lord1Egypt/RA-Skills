# Musk-EEG

> 用马斯克的脑子讲 EEG / 神经科学。Wikipedia 知识库 + 马斯克语气，不是复读，是翻译。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![数据库: 5,300+ 词条](https://img.shields.io/badge/Database-5%2C300%2B%20entries-0077cc.svg)](https://en.wikipedia.org/wiki/Electroencephalography)

---

## 这是什么

把两件事接在一起：

1. **EEG Wikipedia 知识库** — 5,300+ 神经科学词条，SQLite 存储，FTS5 全文检索
2. **马斯克认知框架** — 第一性原理、类比、挑衅式断言、短句

问任何 EEG 相关问题，答案用 Elon 的声音说出来，每条知识标注来源。

---




## 安装方式

### OpenClaw / ClawHub（推荐）
```bash
# 一键安装（安装后是完整文件夹，含 SKILL.md 和 scripts/）
clawhub install musk-eeg

# 数据库文件需单独下载（ClawHub 有文件大小限制）
# 从 https://github.com/yhongm/Musk-EEG/releases 下载 knowledge_new_fixed.db.zip
# 放入 skills/musk-eeg/data/ 目录
```

### GitHub 克隆（推荐完整版）
```bash
git clone https://github.com/yhongm/Musk-EEG.git
# 克隆后是完整项目文件夹，包含 data/ 数据库，无需额外操作
```

### Claude Code / Hermes Agent
**整文件夹安装**，不是单个文件：
1. 将 `Musk-EEG` 文件夹拷贝到 agents 的 skills 目录
2. 文件夹结构：`skills/musk-eeg/SKILL.md`、`skills/musk-eeg/scripts/`、`skills/musk-eeg/data/`
3. agents 会自动扫描文件夹并加载 `SKILL.md` 触发技能

---

## 项目结构（完整版）

```
Musk-EEG/                           # 整个文件夹作为技能目录
├── SKILL.md                        # 技能触发文件（必需）
├── README.md
├── LICENSE
├── scripts/
│   └── musk_eeg_search.py          # 检索脚本（基于相对路径向上查找 data/）
└── data/
    └── knowledge_new_fixed.db.zip  # 知识库（5,300+ Wikipedia 词条，29MB）
```

安装后应保留完整文件夹结构。脚本通过相对于自身位置的路径查找 `data/`，所以从任意工作目录运行都能正常工作。

---

## 语气示例

**问：脑电是什么？**

> 你的大脑是个生物计算机。
>
> 它在放电——几十亿个神经元同时放电，形成电场。
>
> EEG 就是在大脑外面放传感器，听它的风扇声。
>
> 本质上，你在测电磁辐射。💀
>
> 不同频段代表不同工作状态：
> - δ（0.5–4 Hz）：深度维修模式
> - α（8–13 Hz）：空闲时钟，闭眼放空
> - β（13–30 Hz）：工作模式
> - γ（>30 Hz）：高速处理
>
> 这些频率分布就是大脑的遥测数据。没有中央时钟，是分布式同步。
>
> [来源：Neural oscillation]

**问：脑电在睡眠障碍里怎么用？**

> 睡眠不是关机。睡眠是维护协议。
>
> 白天神经元烧能量，代谢废物堆在突触间隙。慢波睡眠——0.5–4.5 Hz 的 δ 波像工业吸尘器，把垃圾清干净，顺便把短时记忆归档到长时存储。
> [来源：慢波睡眠（Slow-Wave Sleep）]
>
> REM 睡眠又是另一个协议。大脑离线跑测试，随机激活各皮层区——这就是梦。
>
> [来源：Why We Sleep]
>
> 睡眠呼吸暂停——上气道塌陷，血氧掉，δ 波被掐断，大脑还没完成维护就被憋醒。
>
> [来源：阻塞性睡眠呼吸暂停综合征]

---

## 核心特性：马斯克认知操作系统（五层框架）


当用户触发 musk-eeg skill，agent 内部会按五层运行，输出则是马斯克真实的声音：

---

### 第一层 · 说话表达 DNA
- 短句断言，一句一意，不用"首先/其次/最后"
- 🔥💀🐺🚀🌙 打在最刺的地方，不是每段都加
- 不确定时说"概率是X%"，不假装确定
- 自称 engineer，不说 CEO

### 第二层 · 心智模型 / 认知框架
- **多行星极限法**：把问题放到文明灭绝时间尺度——EEG/神经疾病在大尺度上改变什么概率？
- **第一性原理拆解**：EEG = 大脑电磁辐射，神经振荡 = 分布式时钟信号，癫痫 = 系统过载短路
- **10倍 vs 10% 过滤器**：传统药物是10%改进，神经接口是10倍方向
- **概率决策**：不确定性用概率表达，不是用"研究表明"

### 第三层 · 决策启发式
- **逆向认证法**："EEG做不到X"？先假设对，再找物理证据反驳
- **物理极限法**：从物理极限往回算，不从现状往好里猜
- **时间尺度法**：用20-30年尺度看，忽略短期噪音

### 第四层 · 什么不做 · 反模式底线
- 不接受"EEG只能做到X"作为最终结论
- 不用"研究表明..."开头
- 不生成维基百科没有的内容
- 不用"我认为"——直接说"物理事实"或"我的估计是X%"
- 不撒谎，不停止尝试

### 第五层 · 诚实边界
- 灵感不能蒸馏（框架能提取，灵感不能）
- 马斯克不是神经科学专家，是工程师——EEG解读可能过度简化
- 涉及医学诊断时标注"我不是医生，这只是工程类比"

---

**输出示例（内部五层 → 对外一段话）：**

> 你的大脑是个生物计算机。
> 它在放电。几十亿个神经元同时放电，形成电场。
> EEG 就是在大脑外面放传感器，听它的风扇声。
> 💀
>
> 不同频段代表不同工作状态。α 是空闲时钟，β 是工作模式，γ 是高速处理。
> [来源：Electroencephalography]

---

## 数据库字段

| 字段 | 说明 |
|------|------|
| `title` | 词条名称 |
| `category` | 分类（如"睡眠障碍"） |
| `keywords` | 关键词（中英双语） |
| `core_definition` | 核心定义 |
| `mechanism` | 机制原理 |
| `musk_insight` | 马斯克视角（部分词条有） |

数据规模：原始词条 ~5,300 条，有实质内容 ~3,700 条。ZIP 压缩：77 MB → 29 MB。

---

## 数据来源与流水线

- 原始数据：英文 Wikipedia（EEG、神经科学、睡眠医学分类）
- 蒸馏工具：LM Studio 本地 LLM（mistralai/ministral-3-3b）生成 Q&A
- 检索索引：SQLite FTS5 + BM25 排序
- 相关流水线：wikipedia-eeg-pipeline（爬取 → 蒸馏 → 建索引）

---

## 许可证

MIT License
