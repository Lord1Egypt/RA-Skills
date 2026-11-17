---
name: pasm-longterm-verify
description: >-
  Long-term verification agents for the PASM cognitive engine. Answers "is it still healthy after long
  runs?" with repeatable, stdlib-only checks: memory retention and salience-aware eviction, emotion
  drift, behavioural entropy collapse, persona saturation, forgetting curve, 6000-step soak
  degradation, and cross-repo parity. Scenarios drive the real engine in an isolated subprocess and
  emit JSON-archivable, baseline-diffable findings.
version: 0.5.0
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

## License

MIT © arronZheng（小志）。

- 本技能来源仓（7 个验证智能体 + 4 个产品智能体）：<https://github.com/arronJack/pasm-agents>
- 基座仓（框架 / SDK / 场景仿真 / 打包工具 / 教程）：<https://github.com/arronJack/pasm-skills>
