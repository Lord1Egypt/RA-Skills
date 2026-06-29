# 示例抽卡文件

本文件展示 `export_flashcards.py` 支持的所有卡片格式。空白行分隔卡片。

---

## 格式 1：Q / A（基础问答）

```markdown
Q: 什么是数列极限的 epsilon-N 定义？
A: 对于任意 ε>0，存在正整数 N，使得当 n>N 时，|a_n - A| < ε 恒成立。
Tags: 数学分析, 极限, 定义
Deck: 数学分析期末

Q: TCP 三次握手的过程是什么？
A: SYN → SYN-ACK → ACK。目的是同步序列号、交换窗口大小、确认双向通路。
Tags: 计算机网络, TCP
```

## 格式 2：Cloze（填空）

```markdown
Cloze: 夹逼定理：若 {{c1::a_n ≤ b_n ≤ c_n}} 且 {{c2::lim a_n = lim c_n = L}}，则 {{c3::lim b_n = L}}
Tags: 数学分析, 定理

Cloze: 快排的平均时间复杂度是 {{c1::O(n log n)}}，最坏情况是 {{c2::O(n²)}}
A: 最坏情况发生在数组已有序或逆序时，枢纽元选择不当。
Tags: 数据结构, 排序
```

> **默认模式**：保留 `{{c1::...}}` 语法，导入 Anki 时使用 Cloze 笔记类型。
> **--expand-cloze 模式**：将多 cloze 展开为多个 CSV 行，适合 Quizlet 等不支持 Anki cloze 语法的工具。

## 格式 3：Front | Back（单行简写）

```markdown
Capital of France | Paris
Tags: geography

快排 | 不稳定、平均 O(n log n)、原地排序
Tags: 数据结构
```

> 适用于简单事实性卡片，一行即一张卡。

## 格式 4：Front / Back 标签别名

```markdown
Front: 什么是死锁的四个必要条件？
Back: 互斥、持有并等待、不可抢占、循环等待
Tags: OS
```

> `Front:` = `Q:`，`Back:` = `A:`，完全等价。

---

## 多行内容示例

答案和题干都支持多行（换行会被保留到 CSV 中）：

```markdown
Q: 写出 Dijkstra 算法的伪代码框架
A: 初始化 dist[all] = INF, dist[start] = 0
使用优先队列 PQ，按 dist 排序
while PQ 非空:
    u = PQ.pop()
    for v in adj[u]:
        if dist[u] + w(u,v) < dist[v]:
            dist[v] = dist[u] + w(u,v)
            PQ.push(v)
Tags: 图论, 最短路径
```

---

## 导出命令

```bash
# 基础导出
python scripts/export_flashcards.py cards.md cards.csv

# 指定默认牌组
python scripts/export_flashcards.py cards.md cards.csv --deck "数学分析期末"

# 展开 cloze（适合 Quizlet）
python scripts/export_flashcards.py cards.md cards.csv --expand-cloze

# TSV 格式（字段含逗号时更安全）
python scripts/export_flashcards.py cards.md cards.tsv --format tsv

# 输出到 stdout
python scripts/export_flashcards.py cards.md - --format tsv
```

## CSV 结构

输出文件包含表头：`Front, Back, Tags, Deck`

| Front | Back | Tags | Deck |
|-------|------|------|------|
| 什么是数列极限... | 对于任意 ε>0... | 数学分析, 极限, 定义 | 数学分析期末 |
| 夹逼定理：若 {{c1::a_n... | | 数学分析, 定理 | 数学分析期末 |
