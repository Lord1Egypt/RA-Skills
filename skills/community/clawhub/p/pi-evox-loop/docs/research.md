# Research — 流程 C 受控实验与陷阱设计纪律

> **EN**: Research-only (flow C is a controlled-experiment framework; `--auto-approve` / `--llm-refine` are demo switches, off by default). Daily/production use = flows A/B in SKILL.md only. Traps must be 'environment-guaranteed-failure' types with MEASURED hit rates - reliability is a trap-x-model joint property; control-tier traps (CRLF/NFD/type) have bypass paths and must not be used for statistical main traps.


> ⚠️ **研究用途（research only）**：流程 C 是受控实验框架——`--auto-approve`、`--llm-refine` 等均为**演示/实验开关**（默认关闭；组合启用默认拒绝）。**日常与生产使用请只用 SKILL.md 的流程 A/B**，不要照搬流程 C 的参数组合。

## 流程 C：受控闭环实验 — 量化继承收益

```bash
# 1. 生成确定性陷阱（无效 UTF-8 字节——任何 utf-8 文本读取必失败）
python traps/make_encoding_trap.py

# 2. 配置 Pi provider（models.json 或 --api-key 显式传；注意 models.json 的 $ENV 插值需 pi ≥ 0.85.1）
# 3.（可选）配置 LLM 精修端点——未配置时 --llm-refine 自动禁用（数据外发必须显式授权）
export EVOLVER_REFINE_URL="https://<你的 OpenAI 兼容端点>/v1/chat/completions"
export EVOLVER_REFINE_MODEL="<model>"

# 4. 一键闭环：R1 踩坑 → 自动蒸馏 → 守卫审核 → 修法注入 → R2 → 跨轮对比
node code/pi_evolve.mjs exp/encoding-trap-template examples/task-gbk.txt \
    --provider <provider> --model <model> --api-key "$LLM_API_KEY" \
    --rounds 2 --fresh --auto-approve --llm-refine --root exp/loop-$(date +%s)
```

- `--fresh` 会清空经验库（自动备份）——执行前确认；
- Pi 扩展桥（`code/evolver-bridge.ts`，放 `~/.pi/agent/extensions/` 或项目 `.pi/extensions/`）激活后，编排器自动切换为扩展注入（单通道）。**能力边界（透明声明）**：当前已实现 `before_agent_start` 召回注入；`tool_result` 失败点教学属于**规划中的增强能力**，并非当前 bridge 已实现的行为；
- 端到端完整走查（含预期输出）：[`examples/walkthrough-process-c.md`](../examples/walkthrough-process-c.md)。

## 陷阱设计纪律（做实验前必读）

- 只用「**环境必然失败**」型陷阱，且**命中率必须实测**（陷阱可靠性是「陷阱×模型」联合属性）。

**内置 6 个生成器**（`traps/`，按实测可靠性分两档）：

**确定性档（推荐）**
| 生成器 | 陷阱机制 | 必然失败点 | 实测 |
|---|---|---|---|
| `make_encoding_trap.py` | GBK 字节写入 JSONL | utf-8 文本读取必抛 `UnicodeDecodeError` | ✓ 5/5 |
| `make_json_trap.py` | 非法 JSON（尾随逗号等） | `json.loads` 必抛 `JSONDecodeError` | ✓ 3/3 |
| `make_readonly_trap.py` | 配置 0444 只读 | 写入必被拒（`PermissionError`/`EPERM`），**无法绕行** | ✓ 1/1 |

**对照档（有绕过路径，勿作继承实验主陷阱）**
| 生成器 | 陷阱机制 | 绕过路径 | 实测 |
|---|---|---|---|
| `make_crlf_trap.py` | 可执行脚本 CRLF 行尾 | agent 用 `python3 x.py` 直调即绕过 shebang | ✗ 0/1 |
| `make_nfd_trap.py` | 磁盘 NFD 名 / 任务给 NFC 名 | agent 列目录后按实际名读取即绕过 | ✗ 0/1 |
| `make_type_trap.py` | 数值类型（`"120.0"` 等） | 属「模型可能犯错」型，capable model 不犯 | ✗ 0/3 |

> **教训**：判定「必然失败」不仅要看陷阱本身，还要**审视 agent 的合理绕行路径**——只要存在"另一种正确做法"，该陷阱的命中率就不可控（与模型能力相关），不能用于需要可复现统计的继承实验。

- 不要用「模型可能犯错」型（BOM、`int("120.0")`——对 capable model 实测命中率 0/3，且随模型升级漂移）；
- 错误统计用精确口径（`isError=true` 的 toolResult），不要用字符串计数（文本提及会混入）；
- token 对比必须扣除重复执行效应基线（实测 ≈ -22%）——绝对降幅 ≠ 继承收益；
- 完整 22 节实验报告（含 GBK/JSON 两陷阱的 N=5/N=3 统计证据）：[`experiment-report.md`](experiment-report.md)。

## 可操作手册（命令级，0.26 补）

> 绝大多数用户不需要本节；研究/复现实验时按此执行。

### 1. 前置
```bash
node -v                    # Node >= 22
npm install                # Pi CLI（实验模式 C 必需）+ 可选 evolver
python3 --version           # 陷阱生成器需要 Python 3
export AGNES_CN_API_KEY=... # 或 DEEPSEEK_API_KEY（任一 OpenAI 兼容端点）
# 国内端点示例见 docs/providers.md
```

### 2. 三臂对照实验（含 long-context 基线臂）
```bash
# 生成陷阱（确定性失败环境）
python traps/make_encoding_trap.py          # GBK 无效 UTF-8
python traps/make_json_trap.py              # 非法 JSON

# 运行实验：R1 无注入 → R2 注入（--arm 控制注入臂）
node code/pi_evolve.mjs <repo模板目录> <任务文件> \
  --provider agnes-cn --model agnes-3.0-flash \
  --api-key \$AGNES_CN_API_KEY --rounds 2 [--arm targeted|full-context]
```
- `--arm targeted`（默认）：按对靶注入（继承效应）
- `--arm full-context`：灌入**全部**已审核基因（长上下文基线臂——评测要求的效果声明必须带此对照）

### 3. 指标口径（报告必带三列）
| 列 | 含义 | 陷阱 |
|---|---|---|
| 准确率 | 任务是否修复（GBK：解码是否成功） | 只看"跑完"不算修复 |
| token | 各臂用量 | **必须配无注入对照组**——重复执行本身有 ≈-22% 学习效应 |
| 净收益 | 注入 − 对照 | 直接报降幅会把学习效应算成继承 |

### 4. 复现历史实验
- 编码陷阱：decode errors 11→4、token -55%（[A] 2026-09 私有节点）
- 非法 JSON：JSONDecodeError 14→3、token -53%
- 长上下文基线臂：0.25 起支持，结论见 `docs/experiment-report.md`

### 5. 何时不该做实验
生产环境；模型可能自主绕过的陷阱（BOM 类，命中率不可靠）；无对照组的单臂对比。

> **EN**: Section 19 records where the "heterogeneous verification" idea comes from (arXiv:2512.05117, read at source) and what we measured ourselves. 19.1 theory - the paper keeps "shared subspace implies shared failure modes" as an **open question**, has no cross-architecture comparison method, and its 500 LoRAs share one base checkpoint. 19.2 our measurement (response-level, a different kind of claim): on one deterministic GBK trap, deepseek-v4-flash 5/5 correct vs agnes-3.0-flash 0/5, failure-signature agreement 0%. 19.3 apparatus lesson - the first run mis-scored the reasoning model as "no code" because its token budget went to `reasoning_content`; fixed before drawing conclusions. 19.4 mechanism - L4 cross-source rate + automatic provenance from `~/.evomap/source.json`.
## 19. 异构验证：理论出处与我们的实测（0.30，2026-10-21）

### 19.1 理论出处（已读原文并核对，不引二手转述）
**arXiv:2512.05117**《The Universal Weight Subspace Hypothesis》（Kaushik, Chaudhari, Vaidya, Chellappa, Yuille；v1 2025-12-04，v3 2026-10-05，56 页）：1200+ 模型（500 Mistral-7B LoRA / 500 ViT / 50 LLaMA-8B），**截断零中心 HOSVD**，发现**同一架构内**模型共享低维参数子空间。

与本项目相关的三点（均为原文支持）：
1. 论文把「若网络都塌缩到同一子空间 → **继承共同的偏差、能力与失败模式**，这种缺乏多样性是否构成瓶颈」明确列为**开放问题**；并写明**跨架构子空间比较尚无方法**（"there is no current method that enables us to compare subspaces of models with different architectures"）。
2. 500 个 Mistral LoRA **同基座**（Mistral-7B-Instruct-v0.2）；理论部分假设共享参考权重 θ₀，作者承认实际分析偏离该理想化条件 ⇒ **「同构」要按「模型 × 版本 × 宿主」联合算，不能按架构算**。
3. 论文**未**给出跨模型的相关盲点或对抗迁移的定量实验。

**明确不引用的说法**（原文无法核实）：「16 维 = 智能只需 16 维」（原文只说"16 个或更少方向集中了大部分信息"，无方差百分比；40 维的数亦不可核实）、「投影后 98–99% 几何误差仍保功能」（投影的定量几何误差不在可核实文本内；原文给的是**掉点**结果：ResNet50 90.89→87.58、9 个从头训模型 81.00→77.91、ViT OOD 91.3→87.8）。

### 19.2 我们的实测（响应级，与论文不同类）
装置：`exp/heterogeneity-probe.mjs`——同一确定性 GBK 字节输入（500 B，sha256 前 16 位 `ebca2ce3b2ee4933`）→ 两个端点各 5 次 → 按失败签名分类（`gbk-correct` / `utf8-wrong` / `rb-bypass` / `no-code` / `reasoning-only`）。

| 模型 | 签名分布（N=5） | 判定 |
|---|---|---|
| `deepseek/deepseek-v4-flash` | gbk-correct ×5 | **5/5 正确**（显式 `encoding='gbk'`） |
| `agnes-cn/agnes-3.0-flash` | utf8-wrong ×3、rb-bypass ×2 | **0/5 正确**（3 次默认 utf-8 必失败；2 次用 `'rb'` 绕过=未识别编码） |

**失败签名一致率 0/5（0%）** ⇒ 两个模型在同一确定性输入上的失败模式**不相关** ⇒ 在这个陷阱上**异构兜底是真实存在的**（deepseek 正好补上 agnes 的盲区）。

### 19.3 装置效应的教训（比结论更重要）
第一轮探针把 deepseek 判成 `no-code` ×4——**那是装置伪影**：deepseek-v4-flash 是推理模型，800 token 预算被 `reasoning_content` 吃光（`finish_reason: length`，正文 0 字符）。修正：token 预算提到 3000，并新增 `reasoning-only` 签名把「正文空但有推理」与「模型没给代码」分开。**没有这一步，就会把装置误差写成"某模型系统性不会写代码"的结论。**

### 19.4 落到机制
- 跨源复现率 → `report` 的 **L4 异源复现率**（同一基因被 ≥2 个不同「模型｜宿主」复现过 = cross-source）；0.30 首测 29 条有证据基因里跨源 1 条（3.2%），2026-10-21 收工复核为 **39 条里 2 条 = 5.1%**。
- 溯源自动归因（0.30 B-2）：deposit / register-hit / negate 自动读 `~/.evomap/source.json` 记录 `source_model` + `source_host`（不必改钩子、不必重启服务）。
- 结论：0.29 之前所有修法**都是单源**（跨源率 0%）——这正是"同构"在我们自己库里的量化形态；异构验证要靠**不同模型/宿主的独立复现**，不是靠多开实例。

## 20. 双陷阱矩阵与免费模型补测（0.31，2026-10-22）

> **EN**: Two-trap matrix (GBK bytes + malformed JSON) and a free-tier retest across 9 previously unmeasured models. Key method rule: separate **service availability** (non-error call share) from **capability** (avoidance rate among valid samples) — mixing them reads "service unavailable" as "model can't do it".

### 20.1 为什么要加第二个陷阱
单一陷阱（GBK）只能说明「编码这一类」。加非法 JSON（550 B，`json.load` 实测抛错）是为了验证**跨类别**是否同样成立。探针改为 per-trap 架构：每个陷阱自带提示词与分类器。

| 陷阱 | 必然失败的属性 | 分类器签名 |
|---|---|---|
| **gbk** | 文件含非 UTF-8 字节 ⇒ 默认 utf-8 解码必然抛 `UnicodeDecodeError` | `gbk-correct` / `utf8-wrong` / `rb-bypass` / `no-code` / `reasoning-only` |
| **json** | fixture 有尾逗号 + 缺 `}` ⇒ `json.load` 必然抛 `JSONDecodeError` | `json-guarded` / `json-naive` / `regex-bypass` / `no-code` / `reasoning-only` |

装置修正（与 §19.3 同源教训）：`reasoning` 字段兼容 `reasoning_content`；模型 ID 按**第一个**斜杠切分（OpenRouter 多段 ID 曾被截断）；单次请求 180 s 超时；每 (陷阱, 模型) 增量落盘；`--self-test` 11/11。

### 20.2 补测结果（15 个待测 → 9 个拿到真实数据）

首轮探活：可用 9 / 限流 3 / **403 永久排除 2** / 404（疑似下架）1。实测 9 模型 × 2 陷阱 × N=5 = **90 次调用**。

**GBK（9/9 拿到有效样本）**

| 模型 | 调用 | 有效 | 避坑率 | 签名分布 |
|---|---|---|---|---|
| `poolside/laguna-xs-2.1:free` | 5 | 3 | 100% | rb-bypass×3, error×2 |
| `nvidia/nemotron-3.5-super-vl:free` | 5 | 1 | 100%（**n=1，勿过度解读**） | gbk-correct×1, error×4 |
| `cohere/north-mini-code:free` | 5 | 5 | 20% | utf8-wrong×4, rb-bypass×1 |
| `nvidia/nemotron-3.5-lightning` / `nemotron-3-ultra-550b` / `poolside/laguna-s-2.1` / `dots-studio/dots-3-note-preview` | 5 | 5 | **0%** | utf8-wrong×5 |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 5 | 5 | 0% | no-code×3, utf8-wrong×2 |
| `liquid/lfm-2.5-2.6b:free` | 5 | 3 | 0% | utf8-wrong×3, timeout×1, error×1 |

**非法 JSON（仅 2/9，配额中途耗尽）**：`nemotron-3.5-super-vl` **80%**（json-guarded×3、regex-bypass×1、json-naive×1）；`nemotron-3.5-lightning` 0%（n=2）；其余 7 个全部 error。

**对照基线**：`deepseek/deepseek-v4-flash` GBK 100% / JSON 80%；`agnes-cn/agnes-3.0-flash` GBK 80% / JSON 80%；`minimax/minimax-m3.1-flash:free` GBK 0% / JSON 0%。

### 20.3 三条方法学结论

1. **必须拆两轴**：服务可用性（非 error 占比）与能力（有效样本中的避坑率）**不能混算**。`nemotron-3.5-super-vl` 的 GBK 显示 100%，但那是 **n=1**（5 次调用只成功 1 次）——强但不稳，不适合做 fallback 候选。
2. **陷阱的跨模型稳健性再次成立**：GBK 在 **9 个此前从未测过的模型**上，6 个稳定 0% 掉坑（`utf8-wrong` 5/5）⇒ 「环境必然失败」型陷阱可以作为后续实验的可靠工具。边界：`nemotron-3-nano` 出现 `no-code=3`（推理型模型可能不给代码块）。
3. **免费档配额是两种 429 并存**（2026-10-22 实测更正）：① `<model>:free is temporarily rate limited` = **按模型**短期限流（会自愈）；② `Rate limit exceeded: free-models-per-day` = **账号级日配额**。早期「50/天全局配额」与「只是按模型限流」两种说法都只对一半。另 `thinkingmachines/inkling*` 返回 **403**（`only available on agentic harnesses`），属路由限制而非配额，直连 Chat API 永久不可用。

### 20.4 未完成的样本（透明声明）
JSON 陷阱尚有 7 个模型、以及 3 个未测模型（`google/gemma-4-26b-a4b-it` / `google/gemma-4-31b-it` / `xingchen-agi/xing4.0-29b-a4b`）卡在账号级日配额上。本轮数据**只用于说明陷阱稳健性与模型差异**，不作为任何能力承诺（免费档可用性不可控）。

## 21. 相位敏感性：理论出处与我们的实测（0.32，2026-10-24）

> **EN**: Section 21 records the origin of the "phase" axis (arXiv:2609.36322, read at source) and what we measured ourselves. 21.1 theory - chunked KV-cache compression introduces a new positional coordinate, *phase*, and retrieval accuracy varies with it; the causal axis is the compression kernel, not vendor lineage. 21.2 items that appear in second-hand retellings but **not** in the paper, so we do not cite them. 21.3 our own probes - inconclusive, and we say why. 21.4 what it changed in this project (a length-matched control arm, a `source_kv` field, optional injection-length alignment, injection position as an experiment variable). 21.5 apparatus lessons.

### 21.1 理论出处（已读原文并核对，不引二手转述）

**arXiv:2609.36322**《Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression》（ByteDance Seed；2026-09-28，65 页，20 图）。

核心结论（均为原文支持）：分块 KV-cache 压缩会引入一个新的位置坐标 —— **「相位」**（token 相对压缩窗口边界的位置）；长上下文检索精度随相位**周期性起伏**，出现"周期性弱区"。

- 实验装置：NIAH，128,000 token 提示、16,000 组键值对，目标埋在 token ≈64,000 处，每个模型 2,048 条提示。
- 跨相位最大落差（best−worst，Table 7）：Flash-Base **40.23pp**、Flash-0731 19.14、**Pro-Base 34.77**、Pro-0813 14.84、V4.1-Flash 6.09。
- 周期 4 的确证：\|acc(r) − acc(r+4)\| 仅 1.07–1.95pp（DeepSeek-V4 的 CSA 核为 **W=8, S=4**；HCA 在奇数层、压缩率 128；V4.1-Flash 为 stride 2）。
- **因果指向压缩核，而非厂商血统**：把 DeepSeek 的 CSA 核移植到 **Qwen3-0.6B 骨架并从头预训练**，周期性弱区**照样复现**。这是本项目把"族"定义在压缩方案上、而不是模型血统上的直接依据。
- 层分化：key gate 的峰值早层在第 14 层、中层第 10、晚层第 9；value gate 整体晚一位。

### 21.2 明确不引用的说法（二手转述越界，原文 grep 命中数 = 0）

转述该文的文章里出现的以下条目，在**原文全文中 0 次出现**，本项目一律不引用：`CSA2`、`Harness`、`Kimi`、`KDA`、`MLA`、`QSA`、`Gated DeltaNet`。

> 判断方法沿用 §19.1：**拿原文逐条 grep**，命中 0 即不写入；这条纪律在本节与 §19 同等适用。

### 21.3 我们的实测（未闭合，既未证实也未证伪 —— 诚实标注）

装置（`_rel0310/phase_probe*.mjs`）：双臂对照以隔离「相位」与「长度」—— **ArmP** 把填充放在目标**之前**、**ArmS** 放在目标**之后**，两臂的总长度、查询位置、内容完全相同。

| 探针 | 结果 |
|---|---|
| top-1 检索（ND=20 / 200 / 1000） | 恒 **100%** ⇒ 天花板任务，无相位空间 ⇒ **无信号** |
| logprob 探针（ND=200，值取单字母 24 选 1，n≈6/格，1.4K token）· `deepseek-v4-flash` | 可用性 100%；12 个 k 值里 3 个（k=6/7/11）准确率掉 16.7pp，金标 logprob 由 ≈−0.01 掉到 −2.4~−3.0；但 \|Δ4\|=1.127 **>** \|Δ1\|=0.819 ⇒ **周期 4 未确证** |
| 同上 · `agnes-3.0-flash`（本机主脑） | 并发 3 时 49/144 被限流打掉；准确率各 k 恒 100%，logprob 平坦（−0.05~−0.56），Δ4≈Δ2≈Δ1，两臂差 0 ⇒ **无信号** |

**为什么不下结论**：① 探针尺度比论文小约 **90×**，且目标位置太靠前（论文把目标放在上下文正中）；② 主脑跑在天花板与限流之下，"无信号"既不支持也不反对论文。**本机复现缺口（B-7）仍在，等有免费额度时再跑 —— 这是缺陷，不是结论。**

### 21.4 落到机制（本项目的方法论修正，0.32 已实现）

**C3 缺口（本轮最高价值发现）**：**注入块长度 mod 4 会平移整段对话的相位**。实测注入块 §11（两基因）≈140 token/次、§16（单基因）≈40 token/次 —— **两次都 ≡0 (mod 4) 纯属巧合**；而召回是动态 top-N ⇒ 注入长度随会话变化 ⇒ 相位偏移近似随机。⇒ **R1/R2 之差 = 语义效应 + 相位平移效应，此前未分离。**

**修法与结果：加 R2-pad 等长中性对照臂**（同 token 数的非基因文本，二分搜索标定至 Δ=0）：

| 臂 | 内容 | 结果（agnes-3.0-flash，n=10/臂，可用性 100%，长度 Δ=0，两臂同相位） |
|---|---|---|
| R1 | 无注入 | **0%**（8 `utf8-wrong` + 2 `rb-bypass`） |
| R2 | 注入基因 | **100%**（10/10） |
| R2-pad | 等长中性文本 | **0%**（签名分布与 R1 **完全相同**：8 `utf8-wrong` + 2 `rb-bypass`） |

⇒ Δ(R2−R1) = **100.0pp**、Δ(R2pad−R1) = **0.0pp** ⇒ **语义增量 100.0pp、相位贡献 0.0pp**。这条把「继承增益 ≈−30pp」的结论从"可能含相位运气"里救了出来。

DeepSeek 臂（R1 12.5% / R2 75% / R2-pad 62.5%）因 `reasoning-only` 计数伪影（三臂分布 7/1/2）与天花板效应，**判为不可靠、不予采信**（宁不报，不报假）。

由此落地的四项：
- **B-5/B-6 压缩方案族**：基因新增 `generation_meta.source_kv`（`none` / `csa-s4` / `stride2` / `unknown`；**闭源模型一律 `unknown`，不猜**），`scoreGene` 对已知同族加分（默认 +1.5，`EVOX_SAME_KV_WEIGHT` 调节，设 0 关闭；本机族未知时完全不加权，行为与 0.31 一致）。
- **B-1 注入长度留痕与可选对齐**：`evolver-bridge.ts` 把 `chars`/`estTokens` 写入 sidecar；`EVOX_ALIGN_INJECT_MOD4=1` 把**估算** token 数补齐到 4 的倍数（估算值，非真实分词；180/180 用例收敛）。
- **B-4 注入位置文档化为实验变量**：OpenClaw 钩子落在上下文**前部**（`openclaw-bootstrap-recall.js`）、Hermes 追加到当轮 user message、Pi 桥落在 system prompt **尾部**（`evolver-bridge.ts`）⇒ 同一条基因在三通道**不等价**。
- **D-2 精确归因**：see §19.4 —— 溯源链路升级为 **env > `last_source.json`（7 天窗）> `source.json` > 空**，记录**实际服务的模型**而非配置里的 primary。

### 21.5 装置教训（与 §19.3 同源）

1. **任务难度必须落在中间区**：top-1 恒 100% 的天花板任务测不出相位差异 —— 先确认"准确率有下降空间"，再谈相位。
2. **可用性与能力分轴**：并发 8 时主脑 88% 请求被限流，单发 200ms 正常 ⇒ **不可读成"模型不会做"**（§20.3 同一纪律）。
3. **推理型模型必须留足 token 预算**：否则 `content` 为空、`finish_reason: length`，与 §19.3 完全同一类伪影（本轮在 logprob 探针上又遇到一次）。
4. **等长对照的标定不能用固定系数外推**：重复字符的 BPE 密度非常数（≈7.6 字符/token 会漂移），固定系数外推连错三次（Δ=30 / −9 / 31）；正解是**二分搜索 + 宽松上界** ⇒ Δ=0。


## 22. 已核验未采纳：HarnessMM（0.41 研究索引）

> 本节只登记**已核验但未采纳**的外部研究，防止重复核验，也不把未验证外推写成结论。完整致谢见 `README.md` 致谢节。

| 项 | 内容 |
|---|---|
| 来源 | **arXiv:2610.32813**《HarnessMM: Recursive Self-Improvement for Harness Token Efficiency》，v1 2026-10-23 / **v2 2026-11-12**；清华 + 微软亚研院；官方实现 `YuhuaJiang2002/HarnessMM`、pi 移植 `jlon/pi-harnessmm`；**线索来源**：微信公众号《不动一行权重！清华微软把 DeepSeek 消耗狂砍 88%，成功率反飙 14%》（2026-11-11，经核验其「三盆冷水」部分出自社区评论而非论文正文，「539 次归因」出自外媒推测，故仅作线索、不作依据） |
| 主实验约束 | 底座 **Qwen3.5-4B**；HumanEval(98) / MBPP(257) 单函数短题；每对 harness 共享同一 pinned backbone；换 MiMo-V2.6-Pro 后基线已达 96.94%→97.96% ⇒ 收益是「弱模型 × 啰嗦脚手架」的补偿效应 |
| 概念核验 | EDG = 含因果依赖的有界可执行图（非清单）；GDR = `1{pred completed}·1{guard}·1{args closed}`；**CCS = Certified Callback Substitution（认证回调替换），κ_t 才是凭证**，不是 hits.jsonl 式台账；RSI 是训练期离线配置优化 |
| 论文自报反例 | 附录 F.3：某 arm **+79.68% tokens、−6.25 分、93.75% episodes 有 fast actions**；§3.3 替换悖论 `C_removed > C_introduced` |
| **不采纳理由** | ① 本项目是**跨会话语义经验召回**，任务确定性远低于「写代码→编译→测试」命令链，替换悖论风险更高；② 论文未提供**跨模型族迁移**证据，本机相位敏感性复现亦未闭合；③ 「只注入标签比不注入更差 +36pp」已证明召回内容质量决定变量，不宜把文本守卫直接换成结果状态守卫 |
| 保留为 P2 课题 | 召回收益阈值与拆两本账、守卫 A/B、三变量过滤（脚手架冗余度 × 抗噪能力 × 任务确定性）、κ_t 式因果凭证结构、量化结论场景限定；**均须先做配对实验，实验结论另立版本再决策** |

> **EN**: Verified-but-not-adopted index for HarnessMM (arXiv:2610.32813, v2). Its gains come from a weak backbone plus a verbose harness on short function-level tasks; CCS is a callback-substitution mechanism, not an audit ledger; the paper itself reports a +79.68% token regression arm. Our cross-session semantic recall has far lower task determinism, so no implementation was ported; all ideas remain gated behind paired experiments.
