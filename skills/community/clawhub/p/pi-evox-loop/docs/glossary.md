# 术语表（Glossary）

> **EN**: One-page glossary for the advanced concepts. Each entry: what it is, why it exists, one minimal example. Read this when a term in `SKILL.md` / `info` output is unclear.
> 定位：**一页纸**，只解释「文档里出现但一眼看不懂」的词。不替代 `SKILL.md` 的流程说明。

## 基因相关

| 术语 | 是什么 | 最小例子 |
|---|---|---|
| **Gene（基因）** | 一条**经验记录**：某个坑的触发信号 + 可执行修法。`genes.jsonl` 里一行一条 | `{"summary":"GBK 解码失败","strategy":["FIX: 用 encoding='gbk' 读取"],"signals_match":["gbk","UnicodeDecodeError"]}` |
| **asset_id** | 基因的**内容哈希** ID（`sha256:` 开头）。同内容在不同机器上算出同一个 ID ⇒ 跨机天然去重 | `sha256:9f2c...` |
| **gene_id / id** | 库内的**短 ID**（用于命令行寻址）。0.18 起全部按 gene_id 寻址，不再用「第几条」的位置序号 | `G0031` |
| **signals_match** | 基因的**对靶信号词**。召回时拿任务文本/报错原文与它做交集，交集越大越相关 | `["gbk","UnicodeDecodeError","codec"]` |
| **anti_patterns** | **负经验 token**：「不要这么做」的单 token 字面量。用于冲突判定（见 geneConflicts） | `["utf-8","default"]` |
| **strategy** | 修法正文（数组）。约定用 `FIX:` 开头写**该怎么做**，`AVOID:` 开头写**别怎么做**——注入守卫靠这两个标记区分语境 | `["AVOID: 不要按默认 utf-8 解码","FIX: 先探测真实编码"]` |

## 审核与状态

| 术语 | 是什么 | 要点 |
|---|---|---|
| **LWW（last-write-wins）** | 审核台账 `review.jsonl` 是**追加式**的，所以一个基因的当前状态 = 它的**最后一条**记录。quarantine 必须能撤销 approve | 读「历史上是否 approved 过」是**错的**（会让已隔离的基因继续被注入） |
| **approved / quarantined** | 已审核生效 / 待审（不生效）。0.31 起判定**精确比对**这两个值 | `unapproved`、`disapproved`、`revoked` 一律**不算** approved |
| **depositionGate** | **沉淀质检闸**：在**入库时**（而非召回时）就拒收无修法的"成功总结"。前移的原因：质检放在召回侧会让半成品基因先污染库 | 命中 → 拒绝落库并给出怎么改 |
| **shareable** | 是否允许进**共享池**。本地库是工作区（待审也在里面），池只装已审核通过的 | 改动 shareable 会自动重签 |
| **tier（official / community）** | 池的信任档位。`official` = 自建策展池（导入自动通过），`community`（默认）= 导入后待审 | 见 `gene-pull-trust` |

## 签名与 provenance

| 术语 | 是什么 | 要点 |
|---|---|---|
| **keyid** | 本机 Ed25519 身份的短标识（公钥 sha256 前 16 位）。私钥 0600，**绝不出本机** | `light-cli identity` 查看 |
| **sig_v（0.31）** | 签名规范化版本。**v1** 的签名域不含嵌套字段（历史遗留），**v2** 递归规范化、嵌套内容全部覆盖 | 新签名一律 v2；存量 v1 仍有效，`light-cli resign --yes` 可升级 |
| **provenance（溯源）** | 基因来自哪台机器、哪个模型。deposit/register-hit 时自动从 `~/.evomap/source.json` 读取 | 不必改钩子、不必重启 |

## 冲突与打分

| 术语 | 是什么 | 要点 |
|---|---|---|
| **geneConflicts** | 基因之间的**主张冲突**（如 A 说"按真实编码读" vs B 说"直接用 utf-8"） | 判定 = anti_pattern **整串** ∈ 对方 token 集；kebab 标签是单个不透明 token，匹配不到 |
| **负载均衡偏置** | 长期被高频命中（热门坑）的基因会**轻微降权**，避免每次都只提醒同一条 | 幅度 ±0.4·min(偏离,5)；全 0 命中时恒为 0（小库无副作用） |
| **L4 跨源率** | 一条经验在**别的模型/机器**上也能复现的比例。用来度量「单作危机」（只在自家环境成立的经验） | 分母 = 有证据的基因数 |

## 实验相关（流程 C）

| 术语 | 是什么 |
|---|---|
| **陷阱（trap）** | 确定性、环境**必然失败**的输入（如 GBK 字节文件、非法 JSON）。用来量化"注入经验有没有用" |
| **臂（arm）** | 实验的对照组。`full-context` = 灌入全部已审核基因的长上下文对照臂 |
| **配对解读** | token 变化必须**配对**看：重复执行本身就有约 −22% 的学习效应，基因净贡献 ≈ −30pp |

> **EN**: Related: `docs/overview.md` (boundaries & non-goals), `docs/common-mistakes.md` (anti-patterns with [A] evidence), `docs/advanced.md` (gate details).
