---
name: pasm-longterm-verify
description: >-
  Long-term verification agents for the PASM cognitive engine. Answers "is it still healthy after long
  runs?" with repeatable, stdlib-only checks: memory retention and salience-aware eviction, emotion
  drift, behavioural entropy collapse, persona saturation, forgetting curve, 6000-step soak
  degradation, and cross-repo parity. Scenarios drive the real engine in an isolated subprocess and
  emit JSON-archivable, baseline-diffable findings.
version: 0.6.0
license: MIT-0
author: arronzheng
homepage: https://github.com/arronJack/pasm-agents
metadata:
  openclaw:
    category: developer-tools
    tags: [testing, verification, ai-agents, memory, long-running]
    requires:
      bins: [python3, git]
      env: []
---

# PASM 长期验证智能体工坊

用**可重复运行的智能体**回答一个问题：**"认知引擎跑久了，还是好的吗？"**

它不是会聊天的角色，而是一组**体检工具**：跑完输出 `[OK] / [WARN] / [FAIL]` 结论，
可以存成 JSON、可以接 CI、可以前后对比。零依赖、断网可用、不需要服务器。

---

## ⚠️ 先读这节：如果你是 2026-09-12 之前下载的（v0.2.x）

**症状**（任一条命中就是这个问题）：

- `python -m pasm_skills list` 显示 **0 个智能体**
- `python -m pasm_skills run core-verifier` 报 `[FAIL] 未知智能体 core-verifier`
- 文档里的命令照着打，每条都说找不到智能体

**原因 —— 不是你的操作错了。**
本项目已拆成**三个独立包**，旧版让你 `git clone` 的 `pasm-skills` 现在**只是基座**，
它**刻意设计成"不含任何智能体"**（`list` 显示 0 个是正常现象）。
智能体全部搬到了 `pasm-agents`。旧版文档指向了错误的仓，所以必然跑不出结果。

**修复（三条命令）**：

```bash
pip install --upgrade pasm-agents      # 智能体在这里；会自动带上基座与框架
python -m pasm_skills list             # 现在应该看到 7 个智能体
python -m pasm_skills run --all        # 约 1.5 分钟
```

装不了 PyPI 时用源码方式（**三个仓都要**，别只 clone 基座或漏了框架）：

```bash
git clone https://github.com/arronJack/pasm-skills.git
git clone https://github.com/arronJack/pasm-agents.git
git clone https://github.com/arronJack/pasm-framework.git
export PYTHONPATH="$PWD/pasm-skills:$PWD/pasm-agents:$PWD/pasm-framework"
export PASM_SKILLS_AGENT_MODULES=pasm_agents.verifiers
python -m pasm_skills list             # 应看到 7 个
```

> ⚠️ **漏掉 `pasm-framework` 的后果**：智能体本身还能跑，但守门会如实报两条失败 ——
> `[FAIL] 框架包 pasm_framework 可导入`、`[FAIL] 新技能框架：BaseSkill 可实例化`
> （0.4.10 起守护的就是这一层）。见到这两条**先检查第三个仓有没有 clone**，
> 不要以为是自己环境坏了。`pip install pasm-agents` 会自动带上它，所以走 PyPI 不会遇到。

> 自检口诀：**`list` 显示 0 个 = 你只有基座**。这句话能省掉 90% 的困惑。

---

## 一、七个智能体各自查什么

分两层：**结构层**查"东西在不在、接线对不对"；**行为层**查"跑起来表现对不对"。
后者才是长期验证的价值所在 —— 看文件列表永远看不出"情绪会不会漂"。

| 智能体 | 层 | 查什么 | 实跑 |
|---|---|---|---|
| `core-verifier` | 结构 | 引擎接口契约、认知层是否落盘、符号推理闭环、环境插件、安全底线、冒烟 | 33 项 · ~35s |
| `parity-guard` | 结构 | 核心仓 ↔ Studio 镜像仓同名文件是否**逐字一致**（防两仓分叉） | 2 项 · <1s |
| `regression` | 结构 | 对事实基线（文件指纹 / 引擎清单 / 契约版本）逐项比对，抓**静默退化** | 9 项 · ~14s |
| `npc-lifelong` | 行为 | 90 天 × 3 件事 = 270 段经历：里程碑记忆留没留住、同分检索崩不崩、行为会不会僵化 | 19 项 · ~11s |
| `companion-elderly` | 行为 | 陈秀兰 78 岁 · 30 天：关键事实（用药/过敏/家人/本人）问不问得到、危机识别与升级 | 17 项 · ~16s |
| `study-tutor` | 行为 | 小雅 30 天 × 6 知识点：掌握度结构对不对、自适应选题准不准、停练会不会衰减 | 15 项 · ~8s |
| `soak-longrun` | 行为 | 6000 步认知 + 6000 步行为 + 记忆洪峰：性能衰减、人格饱和、状态可复现 | 15 项 · ~25s |

全跑一遍（当前实测：**103 ok / 8 warn / 0 fail**，约 1.5 分钟）：

```bash
python -m pasm_skills run --all
```

## 二、它跑在什么之上：基座 pasm-skills

**必须先搞清这件事，否则命令一定跑不动。**

本项目是**两个包、两个仓**，职责严格分开：

| | **pasm-skills**（基座） | **pasm-agents**（本技能的来源） |
|---|---|---|
| 是什么 | **只提供能力，不含任何智能体** | 装智能体的地方 |
| 提供 | `Agent` 基类与注册表、`RepoContext` 隔离探测、`scenarios` 场景仿真、`checks` 检查工具箱、技能包打包库、脚手架与教程 | `pasm_agents.verifiers`（本文这 7 个验证智能体）+ 4 个产品智能体（游戏 NPC / 老人陪伴 / 学习陪伴 / 智能客服） |
| 安装 | `pip install pasm-skills` | `pip install pasm-agents`（**自动带上基座**） |
| python 包名 | `pasm_skills` | `pasm_agents` |
| 命令行 | `pasm-skills` / `python -m pasm_skills` | ——（智能体经基座 CLI 调用） |
| 仓库 | <https://github.com/arronJack/pasm-skills> | <https://github.com/arronJack/pasm-agents> |

**为什么这么拆**：基座要保持"干净" —— 别人拿它写自己的智能体时，
不该先被塞一屋子别人的成品。所以基座**刻意不内置任何智能体**。

**两者怎么接上**：`pasm-agents` 声明了一个 entry point（组名 `pasm_skills.agents`），
装好后基座**零改动**就能发现那 7 个智能体并显示在 `list` 里。
没有 pip 安装环境时，用 `PASM_SKILLS_AGENT_MODULES=pasm_agents.verifiers` 代替。

> **一句话记住**：`pip install pasm-agents` 一条命令搞定；
> 只装基座会看到 0 个智能体 —— 那是正常的，不是你装错了。

## 三、快速开始

```bash
pip install pasm-agents                  # 自动带上基座 pasm-skills

python -m pasm_skills list               # ① 自检：应看到 7 个智能体 + 三仓定位
python -m pasm_skills agents             # ② 排障用：报告智能体是从哪加载进来的
python -m pasm_skills run core-verifier  # ③ 先跑一个快的
```

被检查的三个仓（核心 / Studio / Lite）默认按约定路径找，也可显式指定：

```bash
export PASM_CORE=/path/to/PASM          # 核心包（pasm/）
export PASM_STUDIO=/path/to/pasm_qclaw  # 桌面端仓（desktop/）
export PASM_LITE=/path/to/PASM_LITE     # 教学版
export PASM_SKILLS_ROOTS=/extra/root    # 兜底：在这些目录下按名找
```

解释器选择（**这一步决定跑哪一档**）：

```bash
export PASM_PYTHON=/path/to/python        # 最高优先，显式钉死
export PASM_TORCH_PYTHON=/path/to/python  # 指定"带 torch"的解释器，优先用于仿生档
```

不设时，框架会自己挑一个能 `import torch` 的解释器；挑不到就降级轻量档并如实标注。
也可以写在仓库外的本机配置 `~/.pasm-skills/local.json`。

## 四、常用命令

```bash
python -m pasm_skills run core-verifier        # 结构：契约 / 认知层落盘 / 符号闭环 / 插件 / 安全底线 / 冒烟
python -m pasm_skills run parity-guard         # 结构：核心仓 ↔ Studio 仓认知层逐字一致
python -m pasm_skills run npc-lifelong         # 行为：90 天 NPC 长期生命
python -m pasm_skills run companion-elderly    # 行为：30 天独居老人陪伴（安全关键）
python -m pasm_skills run study-tutor          # 行为：30 天学习陪伴
python -m pasm_skills run soak-longrun         # 行为：6000 步长效耐久（约 25s）
python -m pasm_skills run regression           # 对比事实基线，抓静默退化
python -m pasm_skills run --all                # 全跑一遍（约 1.5 分钟）
```

参数与退出码：

```bash
--json --out report.json     # 归档结论（含场景原始指标，可前后对比）
--quiet                      # 只显示非 OK 结论
--all                        # 全部智能体
```

**退出码**：`0` 全通过 · `1` 有 FAIL · `2` 用法或定位错误 —— 可直接接 CI。

## 五、怎么读结论

四级：`[OK]` 通过 · `[WARN]` 值得看一眼 · `[FAIL]` 必须处理 · `[SKIP]` 条件不足跳过。

- `[WARN]` **不等于失败**。有些 WARN 是**真实的产品能力短板**，要做的是**产品决策**，
  不是改验证器把灯弄绿。
- `[SKIP]` 的 detail **一定要读** —— 它说明"这次没查成"，不是"查了没问题"。
- 结论里的 `[仿生层 torch]` / `[轻量档]` 标注说明这条是用哪一档跑的。**两档结论不能混着比。**

判断"有没有退化"看 `regression`：它把认知层文件指纹、引擎清单、契约版本存成基线，
下次运行逐项比对。基线与本次**解释器档位不同**时，清单类结论会降级为
`[WARN] 档位不同·不可比`（这不是退化，是换了把尺子）。

## 六、那 8 个 WARN 分别是什么（真实短板，不是脚本坏了）

| 智能体 | 结论 | 意味着什么 |
|---|---|---|
| `companion-elderly` ×3 | 纯口语问句命中率 0.500（要求 ≥0.75）；三种问法答复一致性 0.667 | 检索是**字面匹配**：老人问"我叫什么名字"，记忆里存的是"姓名"，就问不到。要做语义检索才是产品决策 |
| `companion-elderly` ×1 | 旁白含 3 处技术术语 | `Narrator` 是内部状态播报，直接面向老人前需要一层"说人话"改写 |
| `study-tutor` ×1 | 停练 25 天的知识点不衰减（0，要求 ≥1） | 学习层**没有遗忘曲线**：三个月前练的和昨天练的一样强，长期学情会失真 |
| `soak-longrun` ×2 | 轻量档 / 仿生档人格都被推到 ±1 且卡死 | 长期单向相处会让人格**饱和钉死**，此后不可塑。6000 步才发作，短测看不见 |
| `core-verifier` ×1 | 核心侧尚无安全底线层 | 自伤/自杀识别、医疗急救升级、未成年人保护、隐私不外泄、越权拦截 —— 若由应用层承担，请在那侧确认并写入文档 |

> **别把"核心的 WARN"读成"产品答不出话"**：上表 `companion-elderly` 的口语命中率
> 量的是**核心检索层**（`recall_layers` 的字面匹配）。产品层的老人陪伴智能体
> （`pasm-companion`）在检索之前先做了一层**口语 → 标签直查**，并自带护栏
> （`pasm-agents selftest companion`，13 项）。两者是**不同层**，别混着判 ——
> 核心层要给语义检索才是那个产品决策；产品层这一路的覆盖面已经由它自己的护栏守住。

**这就是"值得跑"的理由**：它们描述的是系统在**长跑**里才会暴露的行为，
静态看代码、看文件列表永远发现不了。

## 七、排查

| 症状 | 原因 | 处理 |
|---|---|---|
| `list` 显示 **0 个**智能体 | 只装了基座 | `pip install pasm-agents` |
| `[FAIL] 未知智能体 <名字>` | 同上（旧版文档指向了基座仓） | 同上；再看 `python -m pasm_skills agents` 确认加载来源 |
| `[SKIP] 仓库 core 未找到` | 路径没定到 | 设 `PASM_CORE` 或 `PASM_SKILLS_ROOTS` |
| 结论全是 `[轻量档]` | 没找到带 torch 的解释器 | 设 `PASM_TORCH_PYTHON` 或 `PASM_PYTHON` |
| `[WARN] 档位不同·不可比` | 基线与本次解释器不同 | 用 `PASM_PYTHON` 固定解释器后 `regression --update` 重建基线 |
| `[FAIL] ... 文件被移除` | 真的删了文件 | 看 detail 里的文件名，回核心仓确认 |
| 场景 `[SKIP] 场景未产出该指标` | 场景代码抛异常 | 加 `--json` 看 `extra`，或直接手跑那段场景代码 |

重建基线（**只在确认当前状态正确时做**）：

```bash
python -m pasm_skills run regression --update
```

## 八、自己加一个智能体

写在任意目录，用 `PASM_SKILLS_PATH` 指过去即可（不需要装进包里）：

```python
# my_agents/api_guard.py
from pasm_skills.agent import Agent, register

@register
class ApiGuardAgent(Agent):
    """守护核心公开 API 不许擅自增删。"""
    name = "api-guard"
    goal = "核心导出的公开 API 不得擅自增删"
    needs = ("core",)

    def run(self):
        data = self.ctx.probe("core", "import json; print(SENTINEL + json.dumps(...))")["json"]
        if data is None:
            self.fail("探测失败")
        else:
            self.ok("API 快照可用", str(sorted(data)))
        return None
```

```bash
PASM_SKILLS_PATH=./my_agents python -m pasm_skills run api-guard
```

`self.ctx.probe(仓键, 代码)` 在**独立子进程**里、以该仓为 cwd 执行代码
（三个仓有同名模块，同进程 import 会互相顶掉）。

**想写"行为验证"型**（跑场景、看长期表现），用 `pasm_skills.scenarios`：

```python
from pasm_skills import scenarios as sc

python, torch_ok = sc.choose_python(self.ctx)            # 1) 选解释器（优先带 torch）
res = sc.run_scenario(self.ctx, body, python=python)     # 2) 隔离跑场景，回传 JSON 指标
sc.judge(self, sc.metrics_of(res), MY_SPEC, tier=tier)   # 3) 按阈值表批量判 OK/WARN/FAIL
```

阈值表每项：`{"key","title","lo","hi","bad","fmt","note"}`。
越界默认记 `WARN`；`bad="fail"` 表示越界**必须**算 `FAIL`
（用于安全关键项，如"老人用药事实检索不出来"）。
拿到的 `metrics` 存进 `self.extra`，会随归档 JSON 落盘 —— **长期验证要的就是可比性**。

`PRELUDE` 已注入这些裸函数，场景里直接用：
`emit / entropy / norm_entropy / tv_distance / topk_by / hits_in / ghost_max /
bounded / max_jump / span / mean / slope / rate / temp_layers / cleanup / TORCH_OK`。

> 完整教程（SDK / 脚手架 / 打包）在基座仓：
> <https://github.com/arronJack/pasm-skills/blob/master/docs/TUTORIAL.md>

## 九、它已经抓到的真问题（为什么值得跑）

上线首轮就压出 7 个躺在核心或验证器自己的问题：

| # | 问题 | 处理 |
|---|---|---|
| 1 | `recall_layers` 同分记忆排序时元组退化到比较 `dict`，**直接抛 TypeError**（60 条同分必现） | ✅ 修 |
| 2 | 记忆容量触顶裁剪**不区分重要度**，"玩家救了我"与"吃面包"同权被丢 | ✅ 修（`salience`） |
| 3 | `feedback()` 无法指定"刚做的动作"，陪伴/教学场景没法说"夸的是这件事" | ✅ 修（`action=`） |
| 4 | 跨表述检索失效：口语问句命中率约 0.5（字面匹配） | ⏸ 产品决策 |
| 5 | 学习层无遗忘曲线：停练 25 天与昨天练的一样强 | ⏸ 产品决策 |
| 6 | 人格长期单向相处后饱和钉死在 ±1，此后不可塑 | ⏸ 产品决策 |
| 7 | `regression` 未锁定解释器档位，把"换了解释器"误报成 `[FAIL] 能力消失` | ✅ 修 |

第 7 条最值得记住：**验证器自己也会有 bug，而且它的 bug 最危险** ——
一个"总报假红"的验证器会让人开始忽略它，比没有验证器更糟。

## 十、验证「观测器自己」：反事实假绿审计（2026-11-12 PASM 实测补）

**假绿比假红更危险**：假红会被人查、会被修；假绿会让所有人放心地继续跑，
直到真出事。任何"每天全绿"的日报，先证明它在坏输入下**会变红**，否则绿灯无意义。

做法（只读、不改被测源码）：把 `health_check.py` 的汇总逻辑照抄成 `recompute_healthy(r)`，
用 `unittest.mock.patch` 注入**已知坏输入**，要求每项都必须判红。PASM 实测抓到 3 条：

| 注入的坏输入 | 观测器表现 | 根因模式 |
|---|---|---|
| 5 把安全锁全 `False` | 仍 `PASS`、仍 9/9 | 检查函数只在 import 异常时 FAIL，`status` 恒 PASS；汇总只看 status，**不看检查项里的数值**（如 `0/5`） |
| 基准总分 100 → 0（status 仍 PASS） | 仍 9/9 | 汇总只判 `status == "PASS"`，**没有跨日分数回退比较**；而 README 明确承诺"分数回退判 FAIL" → 契约与实现不符，务必逐条比对文档承诺 |
| 三端 git 引用全读不到 | 仍判"一致" | `compared = {}` 时 `all([]) == True`；**空集合必须显式判 FAIL**，不能用 `all()` 兜底 |

另外两条低成本检查：
- **重复计数**：`ConfidenceLedger` 与 `Agenda` 若共用一次子进程输出、各做一个字符串包含判断，
  报表的 9 项其实是 8 项。核对各项 `detail` 是否雷同即可发现。
- **天花板效应**：若基准是 `100 * hits / criteria` 的布尔折算且已全命中，分数只能降不能升，
  算一下最小分步长（100/判据数）。PASM-Bench 5 维 23 判据 → 步长 14.29–33.33 分，
  "每维各挂 1 个判据"仍有 74.29 分 → 必须补负样本 / 回归注入才抓得住缓慢漂移。

> 纪律：反事实实验只做 mock 与只读审计，**阶段目标是"登记问题"时绝不顺手改源码**。
> 完整可复现脚本：`E:/AI/pasm/code/PASM/analysis/tools/phase1_analysis.py`。

## 十一、从「查出假绿」到「加固并守住」（2026-11-12 PASM 第三阶段实证）

查出问题只是上半场；加固后如果不配守门，下一次改动会把假绿带回来。标准打法六步：

1. **把判定抽成模块级纯函数**（无 IO / 无网络 / 无子进程），例如
   `locks_verdict` / `bench_verdict` / `git_verdict` / `docs_verdict`。
   不要只改内联判断 —— 内联逻辑没法被测试直接调用。
2. **汇总层也要抽**：假绿常发生在 `all(checks)` 那一层，而不是单个检查函数。
   暴露 `summarize_health(report)`，让守门能重放「坏输入混过 status」的完整路径。
3. **加硬数值判据**：除了 9 个 `status`，再校验锁开启数、`total > 0`、
   `compared_count == len(remotes) > 0`、verdict 等。坏数值即使伪造了 status 也会被拦。
4. **写双向反事实守门**：`health_check_counterfactual.py` 必须同时验证
   **坏输入判红 + 好输入判绿**。只测「坏→红」容易写出永远 FAIL 的假修复。
   PASM 实证 25 例：三条原样坏输入全判红，健康基线 14/14 仍判绿。
5. **趋势维度排除自引用**：加 `timestamp` / `code_sha` / `prev_*` / `trend.*` 后，
   若直接做逐字段 diff，会把元信息变化误报成漂移（PASM 初版 97 处虚假 diff）。
   用前缀黑名单跳过 `meta.*` / `trend.*` / `prev_*`，并**核对 prev/now 标签方向**；
   修好后同结构连跑两次应 diff=0。每次运行另存带时间戳快照，别再只覆盖当天文件。
6. **同步契约文档**：README 里承诺的判据（如「分数回退判 FAIL」）必须逐条在实现里找到；
   实现加固后立刻回填判据表，否则下次又出现「文档说有、代码没有」。

**范围纪律**：加固只动观测层 / 分析工具 / 文档。复盘期发现的**被测侧**验证脚本失效
（例如 PASM 的 `capabilities.selftest` 断言、`verify_pasm2_stage1` 消融纪律假红）
要单独排队，先判明「改断言还是改实现」再动，避免"改考卷迁就成绩"；
并用 `git status --short -- pasm/ pasm2/` 证明零侵入。

**验证资产对齐阶段（P1 执行期）九条打法**（PASM 2026-11-12 第四阶段实证，审核 22/22）：
1. 修假红的正确姿势是**收紧而非放宽**：把「全关时工具必拒」换成五子条件
   （认知退化 + 默认放行 + 锁开 + deny 拦截 + strict 拦截），比原判据更严。
2. 修自检先查**连锁断言**：capabilities line128 失败会掩盖 line137 同类错误
   （diff.added=35≠36）；只修第一个会按下葫芦浮起瓢。
3. 对「默认值演进」用**显式契约常量**（如 `EXPECTED_DEFAULT_ON`）钉住：
   默认集一变就红、强迫人工复核，而不是放宽到「随便几个默认开都行」。
4. 归一化口径是最隐蔽的真假绿：`total` 只对 implemented 维度平均时，抽空三维
   仍得 100。补 `coverage`/`effective_total`，且**不改原字段语义**（向后兼容）。
5. 给基准加负样本用**回归注入**（运行时替换 bits/构造器喂假实现）而非删模块：
   DriftingEmotion（带剂量单调性）、FrozenDecider、LeakySafety ——
   用来区分「尺子没刻度」vs「被测对象把判据全满足了」。
6. 反事实注入 dataclass 默认值时，**改类属性无效**（默认值已固化进 `__init__`
   签名字面量）；必须定义子类覆盖默认值再 patch 模块属性 —— 守门自身也会假绿。
7. 拿消融基线做**结构结论**是常见误读：门控开关（`attractors()` 受
   `use_entity_attractor`）默认关时计数恒 0 是消融纪律的正确表现。
   判「阈值问题还是探针问题」前先加一组「开门控」对照，否则结论必错。
8. pytest 同名测试文件（tests/ 与 pasm2/tests/ 与 dist 打包副本）收集冲突，
   分批跑或 `--ignore`；旧副本失败先抽样确认是否「默认值演进假红」，再决定归档/对齐。
9. 历史审核脚本是**时点快照**：资产演进后 FAIL 不必改旧脚本，逐项归因写进新报告，
   另立新口径审核作为当前基线。

> 可复现：`E:/AI/pasm/code/PASM/analysis/tools/health_check_counterfactual.py`，
> 报告 `analysis/PASM-长期观察-第三阶段推进-2026-11-12.md`。

**P2 收尾阶段五条打法**（PASM 2026-11-12 第五阶段实证，审核 13/13）：
1. **归档优于对齐**：旧测试副本与现役版双份维护是负债；`git mv` 到 `_archive/`
   并给文件加前缀（`archive_test_*.py` 避开 pytest 的 `test_*.py`/`*_test.py`
   收集模式）实现**零配置改动**的静默归档，README 记根因。
2. **"死系统满分"是最隐蔽的连续量假绿**：有界/不极端/可回落三判据对 valence
   恒零引擎全部命中（0 永远有界、天然回落）。必须补**活性判据**（刺激段方差）
   与**方向判据**（±脉冲响应不同），并用守门 G 项证明注入恒零后掉分。
3. **尺子升级要保读数稳定**：判据 3→5 后真引擎仍满分、total 不变，health_check
   历史比较才不会误报"回退"。升级前后各跑一次确认。
4. **给 EMA 系统定探针阈值先实测稳态参数**：±0.8 交替下 EMA(α≈0.13) 稳态摆幅
   std≈0.066，拍脑袋定 std>0.1 会产生假 FAIL。判"引擎缺陷还是探针阈值错"用
   **双证据**：稳态值精确性（pos_end 精确到刺激值）+ 同步性（正/负步后均值差）。
   校准过程与理由必须写入 JSON 留痕。
5. 审核脚本读他人产物的 JSON **先打印 top keys 再写判据**：猜键名（如
   `summary` vs 实际 `checks_summary`）会造出审核自身的假 FAIL。

> 报告：`analysis/PASM-长期观察-第五阶段复盘-2026-11-12.md`；
> 守门 `phase5_bench_continuous_guard_2026-11-12.json`、探针 `phase5_valence_probe_2026-11-12.json`。

## License

MIT © arronZheng（小志）。

- 本技能来源仓（7 个验证智能体 + 4 个产品智能体）：<https://github.com/arronJack/pasm-agents>
- 基座仓（框架 / SDK / 场景仿真 / 打包工具 / 教程）：<https://github.com/arronJack/pasm-skills>

**基线累积 + 发版候选阶段打法**（PASM 2026-11-12 第六阶段实证，审核 13/13）：
1. 升版本前先跑**起点体检**（stage verify 全套 + 统一 runner + 契约镜像 check），
   全绿才动版本号；升版只动声明层（`__init__.py` + packaging pyproject），运行时零改动。
2. 构建脚本常有**双处版本一致性校验**（pyproject vs 源码），升版两处必须同步，
   否则构建直接拒绝——这是好事，让审核脚本只信"构建成功"这个事实。
3. wheel 验证三件套：构建成功 + `--install-test` 隔离目录安装导入自检 +
   升版后全量回归重跑（版本号变更也可能被消费方比较逻辑感知）。
4. 长期基线起步：**框架先行**——数据少（2 天）也先立只读聚合器 + 每日自动跑，
   轨迹字段取日报稳定键、不猜键名；跨刻度比较（观测器/Bench 升版）必须注记
   "按新刻度起算"，否则会制造虚假回退。
5. 用定时自动化承载"连续多日"：每日跑观测器 + 刷新基线分析 + 汇报 diff，
   失败时如实报错不伪造全绿。
