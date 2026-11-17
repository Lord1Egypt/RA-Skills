# 完整闭环示例：一次真实的 pip 镜像排错 → 沉淀 → 召回 → 回填

> **EN**: End-to-end closed-loop walkthrough with REAL outputs (not mocked): a real pip-mirror failure we hit on 2026-10-25, deposited via the guided draft, approved, recalled in a later task, and fed back two ways. Every command below was actually run; outputs are verbatim.

> 与 `walkthrough-gbk.md`（受控实验 R1/R2 视角）不同，本文件走的是**日常闭环**：流程 B（沉淀）→ 流程 A（召回）→ 回填 → 指标。场景是 2026-10-25 的真实排错（本机装 SkillSpector 时 pip 镜像的坑）。
> **复现方式**：为避免污染真实库，本示例在**隔离库**中运行（`EVO_STORE_DIR` / `EVOX_HITS_DIR` 指向临时目录）。你可以照抄每一条命令，输出应当一致（基因 id 会不同）。

---

## 场景（真实事件）

本机经代理装 SkillSpector，用清华 TUNA 镜像：

```bash
pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple <example-package>  # **EN**: placeholder package name; outputs below remain verbatim historical records
```

报错极具误导性——看起来像"包不存在"：

```
ERROR: Could not find a version that satisfies the requirement boto3>=1.34.0 (from <example-package>) (from versions: none)
ERROR: No matching distribution found for boto3>=1.34.0
```

**真相**：TUNA 对 pip 的 PEP691 Accept 协商请求返回 403（`curl` 直取同一个索引页是 200，浏览器无碍），pip 把"拿不到版本列表"表现成"没有可用版本"。换 **aliyun 镜像**即通。（顺带：`pypi.org` 索引页经本机代理会挂起，但 `files.pythonhosted.org` 通——wheel 也可以先从 PyPI 页面手动下载，再本地 `pip install <wheel>`。）

---

## 第一步：引导式沉淀（流程 B）

非显而易见的坑修完后，趁记忆新鲜用 `draft --error` 起稿：

```bash
node code/light-cli.mjs draft --error "ERROR: Could not find a version that satisfies the requirement boto3>=1.34.0 (from <example-package>) (from versions: none)" --context "在本机代理后 pip install <example-package>，用清华 TUNA 镜像"
```

真实输出（注意它**诚实地暴露了自动抽取的局限**）：

```
【引导草稿】从错误自动生成（预填 AVOID，请补 FIX 后审核）：
  signals_match : manual
  anti_patterns : （空·该信号族无无歧义单 token）
  负经验标签    : repeat-failed-approach
  summary       : unknown 失败（在本机代理后 pip install <example-package>，用清华 TUNA 镜像） [AVOID repeat-failed-approach]: ERROR: Could not find a version that satisfies the requirement boto3>=1.34.0 (fr
  strategy      : AVOID: repeating the first approach after it failed, instead of inspecting the error. FIX: <在此填写可执行修法，例如 use encoding='gbk' / 先 chmod u+w 再写 / 先 ls 确认路径>

未加 --commit：补全 strategy 里的 FIX 后，运行上面等价的 distill 命令（或加 --strategy 与 --commit 直接落库为待审草稿）。
```

**教学点**：基础设施类错误的信号词自动抽取常常只给出 `manual`——这是正常的，草稿的职责是起头，**FIX 必须由人补全**（这正是"引导式"的含义）。也不要直接把原始报错长篇粘进 strategy：提炼成"现象 + 根因 + 可执行修法"。

## 第二步：补全并落库

按草稿提示，用 `distill` 补上 signals 与完整 FIX：

```bash
node code/light-cli.mjs distill --signals "pip,proxy,mirror,pypi" \
  --strategy "AVOID: 用清华 TUNA 镜像给 pip 装包——TUNA 对 pip 的 PEP691 Accept 协商请求返回 403（curl 直取同页 200，浏览器无碍），报错形态是 'Could not find a version ... (from versions: none)'，极易误判成'包不存在'。FIX: pip 换 aliyun 镜像 --index-url https://mirrors.aliyun.com/pypi/simple/；另注意 pypi.org 索引页经本机代理会挂起、files.pythonhosted.org 通，wheel 也可先从 PyPI 页手动下载再本地装。" \
  --summary "pip 装 SkillSpector：TUNA 403 误报 'versions: none'，换 aliyun 镜像即通"
```

真实输出：

```
[pi-evox] drafted UNPROVEN gene gene_manual_ca900220 (sha256:ca90022…) — quarantined

已入库【待审/隔离，不会注入】：gene_manual_ca900220
   审核：node code/light-cli.mjs approve gene_manual_ca900220
```

**注意**：落库状态是 `quarantined`（待审/隔离）——**未经审核的基因不会注入**，这是 fail-closed 的设计（防噪音/防恶意基因直接进 system prompt）。

## 第三步：审核

```bash
node code/light-cli.mjs approve gene_manual_ca900220
```

真实输出（0.22 起的审核取证会自动执行）：

```
[gene-share] 审核取证（approve 前自动执行，0.22）：
[gene-share] 审核取证：gene_manual_ca900220
  账本来源: ./experiments                    # 相对本机库目录（此处已按可移植写法脱敏）
  信号词: pip, proxy, mirror, pypi, SkillSpector, TUNA, 'versions, none', aliyun, 镜像即通
```

## 第四步：召回（流程 A，模拟"下一次任务"）

几天后你又在代理环境装包，任务开始时先召回（这是 `session open` 或宿主钩子自动做的事，这里手动演示）：

```bash
node code/evolver-recall.mjs --query "pip install 装包报 versions none 代理镜像" --top 5
```

真实输出（节选）：

```
[pi-evox] 基因总数=1 | 已审核=1 | 守卫通过=1 | 对靶选中=1/1
以下为已验证修法，与本任务相关时优先采用；任务结束时请回填效果：
  采用了 → node evolver-recall.mjs --register-hit --gene <asset_id或gene_id> --note "<任务一句话>"（0.18 起推荐：按 id 寻址，多会话并发不漂移）
  没采用/仍踩坑 → node evolver-recall.mjs --negate --gene <asset_id或gene_id> --note "<为什么没起作用>"
  （位置写法 --register-hit <N> 仍兼容，但多会话并行时 N 可能漂移——见 0.18 变更说明）
  （回填才能量化"注入→有效"转化率；不回的注入不计入效果统计）

[#1|gene_manual_ca900220] [repair] AVOID: 用清华 TUNA 镜像给 pip 装包——TUNA 对 pip 的 PEP691 Accept 协商请求返回 403（curl 直取同页 200，浏览器无碍），报错形态是 'Could not find a version ... (from versions: none)'，极易误判成'包不存在'。FIX: pip 换 aliyun 镜像 --index-url https://mirrors.aliyun.com/pypi/simple/；另注意 pypi.org 索引页经本机代理会挂起、files.pythonhosted.org 通，wheel 也可先从 PyPI 页手动下载再本地装。
```

坑没再踩第二次——**这就是经验继承的价值瞬间**。

## 第五步：回填（两种，语义不同）

**① 任务级反馈**（采用了 / 没奏效）：

```bash
node code/evolver-recall.mjs --register-hit --gene gene_manual_ca900220 --note "换 aliyun 镜像后 pip install 成功"
```

```
[pi-evox] 命中已登记 (gene_manual_ca900220) → …/experiments/hits.jsonl
[pi-evox] 当前命中总数: 1
```

**② 验证结论**（隔离测试/复核结论，进 L2 回填率口径）：

```bash
node code/evolver-recall.mjs --query "pip install 装包报 versions none 代理镜像" --record "aliyun 镜像一次通过，SkillSpector 2.13.1 安装成功"
```

```
[pi-evox] 验证结论已回填生产账本（verifications.jsonl）：aliyun 镜像一次通过，SkillSpector 2.13.1 安装成功
```

**教学点（口径，别看错数）**：`--register-hit/--negate` 记 `hits.jsonl`（任务级反馈，`info` 的"命中登记"读它）；`--record` 记 `verifications.jsonl`（验证结论，`report` 的 **L2 回填率 = 验证记录 / 注入数**读它）。两者互补，不是一回事。

## 第六步：看闭环健康度

```bash
node code/light-cli.mjs info
node code/light-cli.mjs report
```

真实输出：

```
库路径      : ./assets                       # 相对本机库目录（此处已按可移植写法脱敏）
基因总数    : 1
台账记录    : 2
已审核(可注入): 1

── 闭环健康度 ──
  召回次数    : 1
  命中登记    : 1
  待审(未决定): 0
  已隔离      : 0
  状态        : 闭环运行中
```

```
[gene-share] 效果周报（近 7 天，账本: …/c5_demo/experiments）
  L1 活性：召回 2 次（对靶 2）｜注入 2 条次｜沉淀 1 条（repair×1）
  L2 相关性：注入待回填 2｜验证记录 1｜回填率 50%
  L3 错误家族（本窗）: 无
  L4 异源复现：有证据基因 1 条｜跨源 1｜单源 0｜跨源率 1｜negate 根因分布 {}
```

**读数指南**：L1 看活性（有没有在用）；L2 看相关性（注入了有没有验证）；L4 的跨源率是「单作危机」指标——同一条修法被 ≥2 个（模型｜宿主）复现过才算跨源，单源占比高说明换环境可能失效。**冷启动时这些数字都小，是正常的**——价值随使用复利增长。

---

## 一页流程回顾

```
踩坑（非显而易见） ──draft/distill──▶ 待审基因 ──approve──▶ 可注入
                                                              │
下次同类任务 ──recall（钩子自动 / session open）◀──────────────┘
   │
   ├─ 采用了   → --register-hit   （hits.jsonl，info 命中登记）
   ├─ 没奏效   → --negate --because model-diff|env-diff|scene-mismatch|fix-wrong
   └─ 复核结论 → --record         （verifications.jsonl，report L2）
```

**相关文档**：`quickstart.md`（5 分钟上手）、`walkthrough-gbk.md`（受控实验视角）、`sample-run-log.md`（真实运行日志）、SKILL.md 流程 A/B/C。
