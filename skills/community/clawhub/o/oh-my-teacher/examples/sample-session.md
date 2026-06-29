# 示例会话：数学分析期末复习

下面是一次完整的 `/profile` → `/materials` → `/map` → `/quiz` → `/grade` → `/fix` 流程示例，展示 skill 的典型使用方式。

---

## 1. 建立课程档案 `/profile`

**用户**：我要复习数学分析，还有 14 天期末考试。

**Skill**：

> 你好！我是你的期末复习助教。已为你建立课程档案：
>
> ```markdown
> ## Current Course Snapshot
> - **Course**: 数学分析 / Mathematics
> - **Assessment**: 闭卷笔试
> - **Days left**: 14
> - **Level**: 待评估
> - **Environment**: plain-chat
> - **Materials**: 未上传
> - **LaTeX**: rendered
> - **Weak points**: 待诊断
> - **Completed**: []
> - **Accuracy**: N/A
> - **Last action**: /profile
> - **Next recommended**: 上传课程材料或生成知识地图
> ```
>
> 接下来你可以：
> 1. 上传课件/笔记/往年题，我用 `/materials` 帮你整理
> 2. 直接开始 `/map` 生成知识地图和复习重点

---

## 2. 材料摄取 `/materials`

**用户**：我上传了第三章极限的课件和两套往年题。（粘贴文本）

**Skill**：

> ## Materials Inventory
> - 课件：第三章极限（极限定义、性质、运算法则、两个重要极限）
> - 往年题A：5道极限计算、2道证明、1道概念辨析
> - 往年题B：3道 epsilon-delta 证明、4道数列极限
> - 无不可读文件
>
> ## Exam-Relevant Topics
> - 必背：epsilon-delta 定义、夹逼定理、单调有界原理
> - 高频题型：无穷小比较、递推数列极限、函数极限证明
> - 教师强调：存疑区域——一致连续性（课件提到但未深入）
>
> ## Missing Materials
> - [ ] 第四章连续性课件
> - [ ] 老师划重点的那套模拟题
> - [ ] 往年题无答案，需自行核对
>
> ## Priority Map
> | Topic | Priority | Exam Action | Confidence |
> |-------|----------|-------------|------------|
> | epsilon-delta 证明 | 高 | 证明练习 | 低 |
> | 数列极限 | 高 | 计算+证明 | 中 |
> | 无穷小比较 | 中 | 计算 | 中 |
> | 一致连续性 | 低 | 概念辨析 | 低（材料不足） |
>
> ## Updated Course Snapshot Fields
> - **Materials**: 课件PPT（第三章）、往年题x2套
> - **Weak points**: 待诊断
> - **Next recommended**: `/map` 生成全课程知识地图
>
> ## Next Action
> `/map` 生成全课程知识地图和复习重点

---

## 3. 知识地图 `/map`

**用户**：`/map`

**Skill**：

> **章节知识树**
> ```
> 数学分析期末
> ├── 1. 极限与连续 (40%)
> │   ├── 数列极限 ★★★ 必考
> │   ├── 函数极限 ★★★ 必考
> │   └── 连续性    ★★☆ 中频
> ├── 2. 微分学 (30%)
> │   ├── 导数定义  ★★★
> │   └── 中值定理  ★★★ 压轴题来源
> ├── 3. 积分学 (25%)
> │   └── ...
> └── 4. 级数 (5%)
>     └── 低频，快速扫过
> ```
>
> **常见陷阱**
> - 忘记证明前先写 "任取 ε > 0"
> - 夹逼定理使用时未验证两边极限相等
> - L'Hospital 法则未验证 0/0 或 ∞/∞ 条件
>
> **Next recommended**: `/quiz` 从极限章开始练习

---

## 4. 自适应练习 `/quiz`

**用户**：`/quiz`

**Skill**：

> 当前策略：examiner mode，从极限基础题开始。
>
> ---
> **Q1** [Topic: 数列极限] [Difficulty: 基础] [Est: 3min]
>
> 用定义证明：$\lim_{n \to \infty} \frac{1}{n} = 0$
>
> （请写出完整证明过程）

**用户**：对于任意 ε>0，取 N = [1/ε]，则当 n>N 时...

**Skill**：

> ## Score
> 8/10 - 证明框架完整，N 的取法不够严谨
>
> ## Checks Performed
> ε-N 定义结构、N 的存在性、不等式推导、结论
>
> ## What Is Correct
> 任取 ε>0 的起手、取 N 的思路、n>N 时的不等式放缩方向
>
> ## Lost Points
> - -2：N = [1/ε]（floor）可能使 N < 1/ε，导致 n>N 时 |1/n| < ε 不严格成立
>
> ## Exact Mistake
> N 的取法：`[1/ε]`（向下取整）不保证 N ≥ 1/ε，应使用向上取整 ⌈1/ε⌉ 或 max{1, ⌊1/ε⌋+1}
>
> ## Correct Version
> 任取 ε > 0，取 $N = \left\lceil \frac{1}{\varepsilon} \right\rceil$，则当 $n > N$ 时...
>
> ## Repair Drill
> 用定义证明 $\lim_{n \to \infty} \frac{n}{n+1} = 1$，注意 N 的取法。
>
> ## SRS Update
> 数列极限-εN证明, score 4, streak 1 → next review 2026-06-08（ease 2.50, lapses 0）

---

## 5. 错题修复 `/fix`

**用户**：刚才那类题我总是忘记 N 怎么取。

**Skill**：

> **微课堂：N 的取法**
>
> 核心原则：N 必须是正整数，且满足 $n > N \Rightarrow |a_n - L| < \varepsilon$。
>
> 模板：
> 1. 从 $|a_n - L| < \varepsilon$ 反解出 $n > f(\varepsilon)$
> 2. 取 $N = \max\{1, \lfloor f(\varepsilon) \rfloor\}$ 或向上取整
> 3. 验证 $n > N$ 时原不等式成立
>
> **变式练习**
> - 基础：$\lim \frac{1}{n^2} = 0$ → 取 $N = \lceil 1/\sqrt{\varepsilon} \rceil$
> - 变式：$\lim \frac{2n+1}{3n-1} = \frac{2}{3}$
> - 综合：$\lim \frac{n^2+1}{2n^2-n} = \frac{1}{2}$（注意先放缩再取 N）
>
> **Next recommended**: `/quiz` 继续练习，难度已上调。

---

## 6. 间隔复习检查 `/review-due`

**用户**：`/review-due`

**Skill**：

> 今日到期主题（2026-06-07）：
>
> | Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |
> |-------|-------------|-------|--------|-------------|------------|------|--------|
> | 数列极限-εN证明 | 2026-06-01 | 4 | 1 | 2026-06-02 | medium (中等) | 2.50 | 0 |
>
> 已逾期 5 天。建议：对"数列极限-εN证明"做一次 `/quiz` 复习，巩固 ε-N 证明中 N 的取法。

---

## 7. 抽卡导出 `/flashcards`

**用户**：把今天学的极限定义和定理做成 Anki 卡片。

**Skill**：

> 已生成卡片，请复制以下内容保存为 `cards.md`：
>
> ```markdown
> Q: 数列极限的 epsilon-N 定义
> A: 对于任意 ε>0，存在正整数 N，使得当 n>N 时，|a_n - A| < ε 恒成立。
> Tags: 极限, 定义
> Deck: 数学分析期末
>
> Cloze: 夹逼定理：若 {{c1::a_n ≤ b_n ≤ c_n}} 且 {{c2::lim a_n = lim c_n = L}}，则 {{c3::lim b_n = L}}
> Tags: 极限, 定理
>
> Q: 用定义证明极限时，N 的取法模板是什么？
> A: 1. 反解 n > f(ε) \n2. 取 N = max{1, ⌈f(ε)⌉} \n3. 验证
> Tags: 极限, 技巧
> ```
>
> 运行命令导出：
> ```bash
> python scripts/export_flashcards.py cards.md cards.csv --deck "数学分析期末"
> ```
