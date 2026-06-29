# 示例会话：苏格拉底式学习与费曼技巧

这个示例展示 `/socratic` 和 `/feynman` 的差异：前者引导学生一步步发现答案，后者检查学生能否把概念讲清楚。

---

## 1. 苏格拉底式证明引导 `/socratic`

**用户**：`/socratic 用定义证明 lim 1/n = 0`

**Skill**：

> Current strategy: Socratic guidance, because this is a mathematical analysis proof and the goal is to build the proof rather than copy it.
>
> Question 1:
> 数列极限的 ε-N 定义里，你最终需要证明的目标不等式是什么？
>
> Hint ladder available: recall -> contrast -> example -> skeleton.

**用户**：要证明当 n 足够大时，`|1/n - 0| < ε`。

**Skill**：

> 对。现在只看这个不等式：
>
> Question 2:
> `1/n < ε` 等价于对 n 提出什么要求？

**用户**：等价于 `n > 1/ε`。

**Skill**：

> 对。现在有一个隐藏条件：
>
> Question 3:
> N 必须是什么类型的数？你能直接取 `N = 1/ε` 吗？

**用户**：N 要是正整数，不能直接取小数。可以取 `N = ceil(1/ε)`。

**Skill**：

> ## Teacher Close
> 理解度：5/5
>
> 关键点已经抓住：从目标不等式反解出 `n > 1/ε`，再把它转成整数 N。
>
> 完整证明可以写成：
>
> ```text
> 任取 ε > 0，取 N = ceil(1/ε)。当 n > N 时，
> |1/n - 0| = 1/n < 1/N <= ε，
> 所以 lim 1/n = 0。
> ```
>
> Repair Card:
> Q: ε-N 证明中为什么不能随便取 `N = 1/ε`？
> A: 因为 N 必须是正整数；应取向上取整或更大的整数，保证 n>N 时目标不等式成立。
> Tags: 数学分析, 极限, socratic

---

## 2. 费曼技巧检查 `/feynman`

**用户**：`/feynman 时间复杂度`

**Skill**：

> 学长/学姐，我是刚学编程的大一新生。你能不用太多术语，给我讲讲"时间复杂度"到底是什么意思吗？比如我说它就是"程序跑得快不快"，这样理解对吗？

**用户**：时间复杂度就是算法执行时间随数据量增长的变化趋势，比如 O(n) 就是数据多一倍时间也差不多多一倍。

**Skill**：

> 我大概懂了，但还有两个地方想确认：
>
> 1. 你说的"变化趋势"为什么不直接用秒数表示？
> 2. 如果一台电脑快、一台电脑慢，同一个算法的时间复杂度会变吗？

**用户**：不用秒数是因为机器不同，秒数不稳定。复杂度主要看输入规模 n 增大时操作次数怎么增长，所以换电脑一般不改变复杂度。

**Skill**：

> ## Feynman Check
> Clarity: 5/5
> Jargon-free level: 4/5
> Analogy accuracy: 4/5
> Edge-case awareness: 3/5
>
> ## Biggest Gap
> 你还没有说明时间复杂度通常关注最坏情况、平均情况或特定输入分布，不能只说一个笼统趋势。
>
> ## Re-teach Prompt
> 请用 3-5 句话重新讲一遍，必须补上：复杂度描述的是输入规模增长下的操作次数增长，并说明常见分析口径是最坏情况或平均情况。
>
> ## Repair Card
> Q: 为什么时间复杂度不用具体秒数表示？
> A: 秒数受机器、语言、实现常数影响；时间复杂度关注输入规模 n 增大时操作次数的增长阶，常见口径包括最坏情况和平均情况。
> Tags: 程序设计, 时间复杂度, feynman-gap
