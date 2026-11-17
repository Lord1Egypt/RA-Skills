# 完整示例走查：JSONL 被当单个 JSON 解析 → 经验继承生效

> **EN**: Walkthrough for the invalid-JSON trap: how the trap is generated, what the agent sees, which fix gets deposited, and how the fix is recalled on the next run. Pairs with `examples/walkthrough-encoding.md` (GBK encoding trap).


> 与 `walkthrough-gbk.md` 平行，这里演示**数据格式类**陷阱（而非编码类）的完整闭环。
> 命令均在仓库根目录执行；未安装依赖先见 SKILL.md 的「首次运行 3 步就绪」。

---

## 场景

你接手一个 `events.jsonl` 数据文件——**每行是一个独立的 JSON 对象**（JSONL / NDJSON，行分隔）。但你的代码按单个 JSON 文档整体解析，于是报错：

```
Traceback (most recent call last):
  ...
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

根因是「文件里有很多 JSON」≠「文件是一个 JSON 数组」——少了 `[` `]` 外层，或该按行读。

---

## 第一步：任务开始 · 召回已验证修法（流程 A）

```bash
node code/evolver-recall.mjs --query "JSONL 每行一个 JSON 解析报错 JSONDecodeError" --top 5
```

**若经验库已有相关已审核基因**，输出形如：

```
[pi-evox] 基因总数=5 | 已审核=3 | 守卫通过=3 | 对靶选中=1/5
以下为已验证修法，与本任务相关时优先采用；任务结束时若实际采用，请执行：
  node code/evolver-recall.mjs --register-hit <N> --note "<任务一句话>"

[#1|gene_c7d9e0] [repair] AVOID: assume-single-json-array FIX: JSONL 按行 json.loads（for line in f），或整体包一层 [...] 再解析；不要对多行 JSONL 直接 json.load
```

**若经验库为空（首次运行属正常）**，输出会引导你如何沉淀，见第四步。

---

## 第二步：照着修法改代码

```python
# 修改前（把 JSONL 当单个 JSON 文档解析 → JSONDecodeError）
import json
with open("events.jsonl", encoding="utf-8") as f:
    events = json.load(f)          # ❌ 多个顶层 JSON 对象，不是合法 JSON 文档

# 修改后（采用经验库修法，二选一）
with open("events.jsonl", encoding="utf-8") as f:
    events = [json.loads(line) for line in f if line.strip()]   # ✅ 按行

# 或者整体包一层数组
with open("events.jsonl", encoding="utf-8") as f:
    events = json.loads("[" + ",".join(l for l in f if l.strip()) + "]")  # ✅ 包数组
```

陷阱被避开 → 任务成功跑通。

---

## 第三步：任务结束 · 登记命中（可选但推荐）

这条修法**确实帮到了你**，登记一下，让命中率度量更准确：

```bash
node code/evolver-recall.mjs --register-hit 1 --note "events.jsonl 按行解析，不再当单 JSON 数组"
```

输出：

```
[pi-evox] 命中已登记 #1 (gene_c7d9e0) → <cwd>/experiments/hits.jsonl
[pi-evox] 当前命中总数: 1
```

---

## 第四步：若你是第一次踩这个坑 · 沉淀入库（流程 B）

```bash
# 1) 贴原始报错，自动抽信号 + 预填 AVOID（人只补 FIX）
node code/light-cli.mjs draft --error "json.decoder.JSONDecodeError: Expecting value: line 1 column 1" --tool read --context "解析 JSONL 行分隔文件"

# 2) 确认草稿后补 FIX，落库为待审草稿
node code/light-cli.mjs draft --error "json.decoder.JSONDecodeError: Expecting value: line 1 column 1" \
    --strategy "AVOID: 把 JSONL 当单个 JSON 数组解析。FIX: 按行 json.loads（for line in f），或整体包一层 [...] 再 json.loads" --commit

# 3) 审核通过（默认内置 light 后端，零依赖）
node code/light-cli.mjs approve <上一步打印的 gene_id>
```

审核通过后，下一次遇到 JSONL 解析类任务，第一步的召回就会命中它 —— 这就是「经验继承」闭环。

---

## 想自己造这个陷阱？用内置生成器

```bash
python traps/make_json_trap.py     # 造一个「非法 JSON」失败环境（需 Python ≥ 3.8）
```

再配合 `examples/task-numeric.txt` 等样例，可搭出完整的流程 C 受控实验（见 [`docs/research.md`](docs/research.md) 与 [`examples/walkthrough-process-c.md`](walkthrough-process-c.md)）。

---

## 关键纪律（防噪声）

- **守卫**：只有命中修法信号词（`FIX:` / `json.loads` / `JSONL` …）且**通过叙述守卫**的 strategy 才会被注入；纯成功总结不注入（宁缺毋滥）。
- **审核门控**：`approve` 之前基因不注入；`quarantine` 能撤销已批准（last-write-wins）。
- **注入是软提示**：遵从度与模型相关，守卫只保证噪声不入库 / 不出库，不承诺 100% 避坑。
- 编码类陷阱的完整走查见 `walkthrough-gbk.md`；机制与逐条出处见 `SKILL.md` 与 `docs/experiment-report.md`。
