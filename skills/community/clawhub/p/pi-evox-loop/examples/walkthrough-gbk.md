# 完整示例走查：GBK 文件解码失败 → 经验继承生效

> **EN**: End-to-end walkthrough: GBK decoding failure -> recall -> fix -> hit registration. Commands run from the repo root; see SKILL.md for install and first-run steps.

> 本文件给出「从零到经验继承生效」的**一端到底**对照，弥补 `task-*.txt` 仅作单行陷阱样例的不足。
> 命令均在仓库根目录执行；未安装依赖先见 SKILL.md 的「安装」与「首次运行 3 步就绪」。

---

## 场景

你在处理一批老文件，其中 `report.txt` 实际是 **GBK 编码**（无效 UTF-8 字节），但你的代码默认按 `utf-8` 读，于是报错：

```
Traceback (most recent call last):
  ...
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 10: invalid continuation byte
```

---

## 第一步：任务开始 · 召回已验证修法（流程 A）

先看一下经验库里有没有可借鉴的修法（替换成你的任务一句话）：

```bash
node code/evolver-recall.mjs --query "处理 GBK 编码文件报错" --top 5
```

**若经验库已有相关已审核基因**，输出形如：

```
[pi-evox] 基因总数=3 | 已审核=2 | 守卫通过=2 | 对靶选中=1/3
以下为已验证修法，与本任务相关时优先采用；任务结束时若实际采用，请执行：
  node code/evolver-recall.mjs --register-hit <N> --note "<任务一句话>"

[#1|gene_b3f1a2] [repair] AVOID: assume-default-utf8 FIX: 用 encoding='gbk' 读取文件；不要用默认 utf-8
```

把 `[#1]` 这条当成提醒去修代码即可。

**若经验库为空（首次运行属正常）**，输出会引导你如何沉淀，见第四步。

---

## 第二步：照着修法改代码

把默认 `utf-8` 改成按真实编码读取：

```python
# 修改前（会抛 UnicodeDecodeError）
with open("report.txt", encoding="utf-8") as f:
    text = f.read()

# 修改后（采用经验库修法）
with open("report.txt", encoding="gbk") as f:
    text = f.read()
```

陷阱被避开 → 任务成功跑通。

---

## 第三步：任务结束 · 登记命中（可选但推荐）

这条修法**确实帮到了你**，登记一下，让命中率度量更准确：

```bash
node code/evolver-recall.mjs --register-hit 1 --note "GBK report.txt 解码失败，改用 encoding='gbk' 读通"
```

输出：

```
[pi-evox] 命中已登记 #1 (gene_b3f1a2) → <cwd>/experiments/hits.jsonl
[pi-evox] 当前命中总数: 1
```

---

## 第四步：若你是第一次踩这个坑 · 沉淀入库（流程 B）

如果你**还没有**这条经验（经验库为空或无关），踩坑修复后把它沉淀下来，未来同类任务自动召回：

```bash
# 1) 贴原始报错，自动抽信号 + 预填 AVOID（人只补 FIX）
node code/light-cli.mjs draft --error "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5" --tool read --context "读取 GBK 老文件"

# 2) 确认草稿后补 FIX 落库为待审草稿
node code/light-cli.mjs draft --error "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5" \
    --strategy "FIX: 用 encoding='gbk' 读取文件；不要用默认 utf-8" --commit

# 3) 审核通过（默认内置 light 后端，零依赖）
node code/light-cli.mjs approve <上一步打印的 gene_id>
```

审核通过后，下一次遇到 GBK 类任务，第一步的召回就会命中它 —— 这就是「经验继承」闭环。

---

## 关键纪律（防噪声）

- **守卫**：只有命中修法信号词（`FIX:` / `encoding` / `gbk` …）且**通过叙述守卫**（首段不是会话旁白）的 strategy 才会被注入；纯成功总结不注入（宁缺毋滥）。
- **审核门控**：`approve` 之前基因不注入；`quarantine` 能撤销已批准（last-write-wins）。
- **注入是软提示**：遵从度与模型相关，守卫只保证噪声不入库 / 不出库，不承诺 100% 避坑。
- 完整机制与逐条出处见 `SKILL.md` 与 `docs/experiment-report.md`。
