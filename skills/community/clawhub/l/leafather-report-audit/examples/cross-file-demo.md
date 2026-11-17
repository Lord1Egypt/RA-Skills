# 多交付件 demo：逮住「只改了一份、其余还是旧数」

> 零依赖：只用 Python 标准库 sqlite3，**不需要 duckdb**。三步，约 30 秒。

## 为什么有这个东西

真实事故长这样：数据补录后「发货单数」从 7 变成 8，你改了 `report_a.md`，
但 `report_b.html` 和给客户的 PPT 还是旧数。人眼扫两遍看不出，客户一眼看穿。

这个 demo 把那种事故**故意造出来**，让你看见审计怎么抓。

## 三步

```bash
# 第 1 步：造数据、账本、两份交付件（输出到当前目录的 rla-demo/）
python3 examples/cross-file-build.py

# 第 2 步：审计
python3 scripts/rla_audit.py --ledger rla-demo/ledger.json \
    --files report_a.md report_b.html \
    --command "python3 scripts/cmd_sqlite.py --db rla-demo/demo.sqlite" \
    --out rla-demo/audit.md

# 第 3 步：看结果
#   终端里读 rla-demo/audit.md
#   浏览器打开 rla-demo/audit.html（断网也能开）
```

Windows 上把 `python3` 换成 `python`。

## 预期结果

**退出码 1（不通过）**，`audit.md` 里会看到：

```
## 一句话结论

**❌ 不通过**　—　覆盖率 60%（追溯 3 / 应审 5），2 条需人工复核

## 拦下的问题（必须改）

1. **来源不明**：7 @ report_b.html L4
```

`audit.html` 里会看到**跨件一致性矩阵**：

| 指标（账本 ID） | report_a.md | report_b.html |
|---|---|---|
| 净发货额（n1） | 85.25 万 | **85.250 万** ❌ |

## 这两处故意做坏的，分别考什么

| 做坏了什么 | 会被判成 | 为什么 |
|---|---|---|
| `report_b.html` 的发货单数还是旧数 7 | **来源不明**（拦下，exit 1） | 账本里没有「7 单」这个数，它没有出处 |
| 两份文件净发货额小数位不同（85.25 / 85.250） | **跨件不一致**（矩阵标红，需人工复核） | 值一样但写法不同，同一指标在两份交付件里没统一 |

## 能力边界（重要，别误解）

**矩阵抓的是「写法不统一」，不是「数值不同」。**

数值一旦不同（比如旧数 7 vs 新数 8），它大概率在账本里找不到出处 ——
那会被判成「**来源不明**」直接拦下，比矩阵更早、更硬。

所以两道防线是接力关系：

1. 数字对不上账本 → **来源不明**（拦）
2. 数字都对得上，但多份文件写法不一 → **跨件不一致**（复核）

## 删掉

```
rm -rf rla-demo/
```
