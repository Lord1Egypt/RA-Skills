# 完整示例走查：流程 C 端到端 — 从造陷阱到量化继承收益

> ⚠️ **研究用途**：流程 C 是受控实验框架，默认全关。本走查展示「R1 踩坑 → 自动蒸馏 → 守卫审核 → 修法注入 → R2 → 跨轮对比」的完整闭环与预期输出。日常只用流程 A/B（见 SKILL.md）。
>
> 命令均在仓库根目录执行。前置：Node ≥22 + Python 3 + Pi CLI + 一个 OpenAI 兼容 LLM key（provider 配置见 `docs/providers.md`）。

> **EN**: Research-only end-to-end walkthrough for flow C: deterministic trap -> R1 (no experience) -> auto-distill -> guard review -> fix injection -> R2 -> cross-round comparison. Prereqs: Node >= 22 + Python 3 + Pi CLI + an OpenAI-compatible key. Interpretation discipline: error counting uses authoritative flags only; token deltas must subtract the repeat-execution baseline (~-22%).


## 场景

量化「经验继承」对一个确定性失败的净贡献：先用无效 UTF-8 字节造一个**环境必然失败**的任务（R1 无经验，agent 试错），把修法沉淀入库，再跑 R2（有经验注入），对比两轮的错误数与 token。

## 步骤

### 1. 生成确定性陷阱
```bash
python traps/make_encoding_trap.py
# 预期输出：写入 exp/encoding-trap-template/（GBK 字节的 JSONL，utf-8 读取必抛 UnicodeDecodeError）
```

### 2. 配置 provider
```bash
node code/light-cli.mjs doctor   # 先自检：Node 版本 / 库目录可写 / 埋点目录可达
```

### 3. 一键闭环（R1+R2 对比）
```bash
node code/pi_evolve.mjs exp/encoding-trap-template examples/task-gbk.txt \
    --provider <provider> --model <model> --api-key "$LLM_API_KEY" \
    --rounds 2 --fresh --auto-approve --llm-refine --root exp/loop-$(date +%s)
```
- `--fresh` 清空经验库（自动备份，先确认）；`--auto-approve` 让 R1 沉淀的修法立即可注入（实验开关，生产勿用组合）。

### 4. 预期输出（关键段）
```
[pi-evox] R1 开始（无经验基线）
[pi-evox] R1 结果：错误 N=5，token T1
[pi-evox] 蒸馏候选 1 条 → 守卫通过 → 已入库（gene_manual_xxx）
[pi-evox] R2 开始（注入 1 条已验证修法）
[pi-evox] R2 结果：错误 N=1，token T2
[pi-evox] 对比：错误 5→1；token Δ=-53%（含重复执行效应基线 ≈-22%）
```

### 5. 验证闭环真的发生了
```bash
node code/light-cli.mjs info      # 召回次数 / 命中 / 待审
node code/light-cli.mjs timeline  # 四账本时间线：R1 报错→沉淀→R2 注入→回填
```

## 判读纪律（诚实边界）

- **错误统计只信权威标志**（`isError=true` 的 toolResult），不用字符串计数；
- **token 必须配对解读**：重复执行本身有学习效应（实测 ≈ -22%），基因净贡献 = 对比降幅 − 基线；
- **陷阱可靠性是「陷阱×模型」联合属性**：对照档陷阱（CRLF/NFD/type）有绕过路径，别用来做统计主陷阱（见 `docs/research.md` 陷阱设计纪律）；
- 完整 22 节实验报告（N=5/N=3 统计证据）：`docs/experiment-report.md`。
