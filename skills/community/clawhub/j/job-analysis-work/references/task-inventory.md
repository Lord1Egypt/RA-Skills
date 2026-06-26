# Task Inventory

## 一句话

> **Task inventory** = 一张列有"岗位可能做的所有任务"的大问卷，让在岗员工 + 主管对每条任务按若干尺度（做没做、做多久、多重要、多难学、多频繁…）打分。

FJA 里一个 job 通常列 5–10 条任务；**task inventory 里一个 job 往往有 100+ 条**更细粒度的任务。习惯做法：按 **duty**（职责/目标）分组，组内任务按字母序以便检索。

## 两大代表系统

| 系统 | 来源 | 时间 |
|---|---|---|
| **CODAP (Comprehensive Occupational Data Analysis Program)** | U.S. Air Force（USAF），Christal & Weissmuller, 1977 | 1950s–60s 研发 |
| **WPSS (Work Performance Survey System)** | AT&T，Gael, 1983（文献） | 1970s 发展，直接源于 CODAP/USAF |

USAF 动机：要一套能量化、能上大小样本、**直接用在 incumbent** 而非仅靠 analyst、能电脑化的方法。Terry & Evans (1973) 追溯任务清单到 **1919 年**用于技能行业培训。

## 任务清单结构示例

### Table 2.8 — Telephone Line Installation Supervisors
电话线安装主管，按 **difficulty**（难度 = 完成任务所需技能）7 级量表评分：
1 Very much below average – 7 Very much above average。任务举例：
- Assign personnel to installation or repair projects.
- Brief personnel on unit security or safety rules.
- Complete manhour accounting forms for work crews.
- Conduct supervisory orientation of newly assigned personnel.

### Table 2.9 — Drug Clerk in a Pharmacy（"Customer Service" duty 部分节选）
对每条任务给三种答案：
- "X" if Done（是否做）
- Time Spent（1=small amount … 5=large amount）
- Difficulty to Learn（1=one of the easiest … 5=one of the hardest）

任务举例：Answer customer questions about products and services; Call patient about scrip not picked up after 7 days; Make refunds; Recommend products to customers; Refer medical questions to pharmacist; Ring up merchandise and prescriptions on register.

## 设计步骤

### 1. Background Information（写问卷前的准备）

分析师常用多种方法先积累素材：
- **Observation** — 现场观察（兼得工作情境，如噪音、光照、时段）。
- **Background materials** — 岗位说明书、培训材料、组织图、研究文献、O\*NET 等。
- **Interviews** — 访谈 incumbent / supervisor / 培训专家。

### 2. Structure of Tasks（写任务句）

结构宽松遵循 FJA：**动词开头 + 直接宾语**，必要时加说明短语（"何时、何处、为何"）。

- 最精简示范："Make refunds."（Table 2.9）
- 中等具体："Call patient about scrip not picked up after 7 days." — 交代了原因（未取药）和触发条件（7 天）。

### 3. Determining the Appropriate Level of Specificity（specificity 级别）

Gael (1983, p. 9) 定义 task：*"a discrete organized unit of work, with a definite beginning and end, performed by an individual to accomplish the goals of a job."*

- **过粗**（只谈目标）：例 "Takes care of customers." ❌
- **过细**（降到动作序列）：例 "picks up the phone, dials the numbers, …" ❌
- **刚好**：例 "Call customers to notify them that merchandise has arrived." ✓

**Specificity 取决于 purpose**（继续课本一贯主题）：
- 绩效评估 → 可写得较粗。
- 设计培训教材 → 得更具体，甚至带上工具（"挖洞—用铁锹还是挖土机？"）。

### 4. Selecting Response Options（响应选项）

WPSS 常问的四种经典尺度（Gael, 1983, p. 94）：
1. **Importance / Significance** — 对岗位多重要？
2. **Time spent** — 花多少时间？
3. **Frequency** — 做得多频繁？
4. **Difficulty** — 做起来多难？

其他备选：
- **Criticality** — 做错的后果有多严重？（法定合规常用）
- **Difficulty to learn** — 学会要多久？
- **Ability of others to cover** — 别人顶替难吗？
- **Satisfaction with the task** — 做起来满意吗？

> 哪些量表该用仍有争议。参见 Fine (1988) 与 Christal & Weissmuller (1988)。

**信度**（Dierdorff & Wilson, 2003，元分析 100+ 研究）：
- 任务量表 ~.77；一般工作活动 ~.61。
- Frequency / Importance（~.70、.77）比 Difficulty / Time spent（~.63、.66）信度更高。
- 结论：大样本能得可靠估计；小样本做 task inventory 不经济。
- Ash, Levine, Higbee, & Sistrunk (1982)：**小而有经验**的 SME 面板可以给出与大样本 incumbent 近似的评分。

**Task importance 的两种度量法**（合规场景尤重要）：
- Sanchez & Levine (1989)：用 *criticality × difficulty-to-learn* 合成最可靠。
- Sanchez & Fraser (1992)：单一 "overall importance" 评分信度等同合成，**一题可能就够**。
- 结论：取决于目的——培训设计则要知道做的频率、犯错后果、学习难度；绩效评估则需要知道重要性、临界性。

### 5. Matching Questions and Purposes（Table 2.10）

不同用途要问不同尺度。记忆钩：

| Purpose | If Done | Importance | Criticality | Difficulty | Time | Frequency |
|---|---|---|---|---|---|---|
| Describe jobs | X | X | X |  | X | X |
| Design / redesign jobs | X | X | X | X | X | X |
| Match skill & job requirements | X |  |  | X |  |  |
| Develop staffing / span of control | X |  |  |  | X | X |
| Establish training requirements | X | X | X | X | X | X |
| Operations review (actual vs desired) | X |  |  |  | X |  |
| Compare jobs' similarities | X | X | X |  | X |  |
| Develop task-by-task performance evaluation | X | X | X |  |  |  |

### 6. Demographic Data（人口学问题）

通常附带 incumbent 背景：工龄、岗位地点、年龄、性别等。
- Spector et al. (1989)：demo 因素总体影响**小**。
- Cornelius & Lyness, 1980（education）、Smith & Hakel, 1979（job level）显示一些影响（level 可能与 education 相关）。
- Conley & Sackett, 1987；Cornelius & Lyness, 1980；Schmitt & Cohen, 1989 — incumbent 绩效/任期基本**不**影响评分。
- Moore (1976, in Gael 1983)：incumbent vs supervisor **来源**确实影响评分。

### 7. Data Analysis

CODAP 和 WPSS 本身就电脑化；现代任何统计包（SPSS, R, Python）都能替代。典型输出：

**Table 2.11（电话杆维护主管任务样本）**：每条任务一行；列按总公司 + 子区间（C&P、Illinois）展开；每行给 PROP（做此任务的 incumbent 比例）、MEAN（7 点尺度上 Importance 平均）、SD。便于检查不同区域/经验/性别的任务响应是否存在差异。

其他用途：
- 生成绩效评估用的任务子集。
- 比较两个岗位的任务重叠度。
- 作为聚类分析输入，划 job families。

## Task Inventory 的法定与组织意义

- U.S. 法下公司/公共机构若不给任务重要性度量，**法律风险高**（Kleiman & Faley, 1985；Sanchez & Fraser, 1992）。
- 常用于支撑招聘测验、MQ、绩效评估的岗位相关性证据（job-relatedness）。

## 速查

- CODAP / WPSS
- Christal, 1971；Christal & Weissmuller, 1977, 1988
- Gael, 1983（WPSS 文献）；Morsh, Madden, & Christal, 1961（CODAP 早期）
- Sanchez & Levine, 1989；Sanchez & Fraser, 1992；Sanchez & Levine, 2012
- Dierdorff & Wilson, 2003（信度元分析）
- Ash, Levine, Higbee, & Sistrunk, 1982（小 SME 面板）
- Spector, Brannick, & Coovert, 1989（按 duty 分组任务）
