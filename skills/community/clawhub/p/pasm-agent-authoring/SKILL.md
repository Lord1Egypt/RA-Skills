---
name: pasm-agent-authoring
description: >-
  The base kit for building agents on the PASM cognitive engine. Ships a BaseAgent SDK (observe /
  recall / mood / act / feedback / save with persistent JSON state), an agent framework (registry,
  isolated repo probing, scenario simulation harness, core-contract check toolboxes) and a
  skill-packaging library producing the two archive layouts platforms require. Write an agent by
  subclassing BaseAgent and implementing an action pool plus a reply template; the engine tier (light
  / core / bionic) is always reported, never hidden. Zero LLM dependency, offline-runnable, stdlib
  only.
version: 0.5.2
license: MIT-0
author: arronzheng
homepage: https://github.com/arronJack/pasm-skills
metadata:
  openclaw:
    category: developer-tools
    tags: [pasm, agent-framework, sdk, ai-agents, authoring]
    requires:
      bins: [python3, git]
      env: []
---

# PASM 智能体开发基座（pasm-agent-authoring）

**从零写一个智能体，并打成能发布的技能包。**
零 LLM 依赖、断网可用、只用标准库 —— 装完就有记忆、情绪、行为选择、反馈塑形、状态持久化。

> 这是**基座**：它不提供成品智能体，只提供写智能体的能力。
> 官方成品智能体（游戏 NPC / 老人陪伴 / 学习陪伴 / 长期验证）在独立公开仓 **pasm-agents**。
> 写完智能体后要把它接成**完整应用 / 服务**（HTTP 接口、智能客服、站点嵌入、插件组合），
> 那属于另一层 —— 用独立仓 **pasm-framework**（`pip install pasm-framework`）。

## 什么时候用

- 想给自己的游戏 / 应用加一个**会记忆、有情绪、能被反馈塑形**的智能体；
- 想复用"记忆淘汰 / 情绪衰减 / 行为选择 / 状态落盘"这些通用件，而不是从零搭；
- 想把自己写的智能体**打成技能包**发到平台上；
- 想写**验证智能体**（给自己或别人的核心做长期体检）。

## 0. 铁律

1. **零 LLM 依赖**：聊天走"模板 + 记忆检索 + 情绪渲染"，不调外部大模型；断网、无显卡、无 API key 都能跑。
   （要接 LLM，就在自己的 `_render_reply` 里接 —— 基座不替你做这个决定。）
2. **档位永不隐藏**：优先驱动 PASM 真核心，拿不到就降级，并在 `agent.tier` 如实写明
   `bionic` / `core` / `light`。**不许假装覆盖了。**
3. **重要度参与淘汰**：`observe(..., salience=1..5)`。容量触顶时按「重要度 + 新旧」淘汰，
   `salience=5` 的关键记忆不会被日常琐事挤掉。
4. **反馈必须能指定动作**：`feedback(kind, action=)`。不指定就只能加强"当前最偏好的动作"，
   长期下来行为分布会被推到极端 —— 这是实测压出来的产品级要求。
5. **落盘开箱即用**：`~/.pasm-agents/<agent_id>/`，跨进程自动恢复。
6. **基座不内置智能体**：具体智能体由外部包通过 entry points（组名 `pasm_skills.agents`）
   或 `PASM_SKILLS_PATH` 提供。基座不依赖任何智能体。

## 1. 30 秒上手

```bash
pip install pasm-skills          # 基座（零依赖）
python -m pasm_skills selftest   # 自检：确认 SDK / 框架 / 发现机制都活着
```

写一个最小智能体：

```python
from pasm_skills.sdk import BaseAgent

class TeaHouseOwner(BaseAgent):
    def action_pool(self):
        return ["greet", "brew", "gossip", "rest"]

    def _render_reply(self, text, facts, mood):
        tone = "没精打采" if mood < -0.2 else "笑呵呵"
        if facts:
            return f"（{tone}）你还记得{ facts[0]['title'] }呢……"
        return f"（{tone}）来啦，坐。"

    def bootstrap_event(self):
        return [{"title": "我在巷口开了家茶馆", "salience": 3, "tags": ["茶馆"]}]

a = TeaHouseOwner(agent_id="owner", persona={"name": "王掌柜", "temper": 0.6, "energy": 0.3, "play": 0.4})
a.observe("客人夸今年的龙井好", salience=3, tags=["茶"])
print(a.act())            # 'brew' / 'greet' / ...
print(a.chat("生意怎么样"))
print(a.mood)             # 属性，不是方法
a.feedback("praise", action="brew")   # 显式夸"brew"这个动作
a.save()
```

## 2. 三个钩子 —— 子类只需要写这些

| 钩子 | 签名 | 必填 | 作用 |
|---|---|---|---|
| `action_pool()` | `-> List[str]` | ✅ | 当前成长阶段能做的动作（**动作名决定它属于哪类偏好**，见 §4） |
| `_render_reply(text, facts, mood)` | `-> str` | ✅ | 收到用户输入时怎么回。`facts` 是检索到的记忆，`mood` 是当前情绪 |
| `bootstrap_event()` | `-> List[Dict]` | 否 | **首次启动**时注入的初始记忆，默认空 |

`bootstrap_event()` 的每一项会被当作 `observe(**item)`：
键包括 `title` / `brief` / `tags` / `salience` / `category`。

## 3. 记忆：`observe` / `recall`

```python
a.observe("客人夸今年的龙井好",                 # title（必填）
          brief="他说比去年的香",              # 细节（可选）
          tags=["茶", "客人"],                 # 检索用标签
          salience=3,                          # 1 日常 / 3 值得记 / 5 关键
          category="日常")                     # 分类（记忆层会保留）

print(a.recall("龙井", k=3))    # -> [{'title': ..., 'brief': ..., 'tags': [...], 'sal': 3}, ...]
```

容量上限 200 条；触顶时按 `(salience, -索引)` 淘汰 —— **关键记忆优先留下**。
`salience` 不传默认 1（旧行为）。

## 4. 行为：性格基线 + 反馈塑形

`act()` 在两个档位走**同一套语义**：

```
得分(action) = 性格基线(action) + 学习权重(action)   → 采样
```

- **性格基线**由 `persona` 里的 `temper` / `energy` / `play`（0~1）推导。
  默认实现按**动作名里的关键词**软匹配：

  | 关键词 | 受哪个特质影响 |
  |---|---|
  | `wave` `talk` `share` `teach` `give` | `temper`（脾气：主动 vs 沉默） |
  | `hop` `dance` `spin` `ball` `run` | `energy`（精力：爱动 vs 爱歇） |
  | `peek` `play` `joke` `boast` | `play`（玩心：俏皮 vs 正经） |

  想让自己的动作名被识别，要么名字里带这些关键词，**要么直接覆盖 `_fallback_weights(pool)`**。

- **学习权重**来自 `feedback()` 的累积：

  ```python
  a.feedback("praise", action="brew")   # +0.3
  a.feedback("hug",    action="brew")   # +0.15
  a.feedback("poke",   action="brew")   # -0.05
  a.feedback("scold",  action="brew")   # -0.3
  ```

  `action` **强烈建议传**（不传就作用在"当前最偏好的动作"上，长期会极端化）。

实测（`seed=0`，400 次 `act` 采样，60×`praise` + 60×`scold`）：被夸的动作占比 0.26 → 1.00（core 档 0.27 → 0.80），
被凶的 0.26 → 0.00（core 档 → 0.03）。**两个档位都生效**，只是 core 走真 `LearningEngine`、带 ε-贪心探索，
不会压到 0/1 两端。

## 5. 情绪：`mood` / `feel`

```python
print(a.mood)                        # float，[-1, 1]（**属性，不加括号**）
a.feel("茶馆被泼了脏水", valence=-0.6)   # 注入一次情绪事件
```

有 torch 时接真 `EmotionSystem`（人格模块驱动），没有时用轻量累计。`mood` 会被传进
`_render_reply`，所以"同一句话在高兴和生气时说出来的不一样"是自然发生的。

## 6. 档位与降级

| tier | 含义 | 何时启用 |
|---|---|---|
| `bionic` | 完整 PASM 核心 + emotion 模块 | 装有 torch，且能 import `pasm.modules.emotion` |
| `core`   | PASM 核心（`memory_layers` + `learning`） | 能 import `pasm.cognitive`（**不需要 torch**） |
| `light`  | 纯内置（重要度淘汰 + 字面检索 + 性格/反馈加权） | 任何机器 |

```python
print(a.tier)          # 'light' / 'core' / 'bionic'
a = TeaHouseOwner(agent_id="x", persona={...}, use_core=False)   # 强制轻量档（测试用）
```

**接口在三个档位下完全一致**，调用方不需要分支。

## 7. 落盘

```python
a.save()        # -> ~/.pasm-agents/<agent_id>/
a.summary()     # -> {'tier': ..., 'persona': ..., 'total_interactions': ..., 'mood': ...}
```

```
~/.pasm-agents/<agent_id>/
├── agent_state.json       # persona / 交互数 / 反馈历史 / mood / notes
├── episodes.json          # light 档的记忆（core/bionic 档走 pasm.cognitive.memory_layers）
└── action_weights.json    # 动作权重（性格基线 + 反馈累积）
```

`ElderlyCompanion` 那样需要额外结构化状态时，用 `state.notes` 存（它随 state 一起落盘）：

```python
self.state.notes.setdefault("knowledge_state", {})[topic] = 0.8
```

## 8. 常用扩展点（官方智能体就是这么写的）

| 想做的事 | 怎么做 | 官方例子 |
|---|---|---|
| 关键事实永不丢 | 首次启动把 `persona.key_facts` 逐条 `observe(salience=5, tags=[label])`，检索时先按标签直查 | `pasm-companion` |
| 按知识点追踪掌握度 | 状态存 `state.notes`，用 EMA 平滑 `新 = 旧*0.7 + 本次*0.3` | `pasm-tutor` |
| 行为随成长解锁 | `action_pool()` 按 `state.growth_stage` 返回不同池子 | `pasm-npc` |
| 危险内容升级 | 关键词扫一遍 → `observe(salience=5, category="危机")` + `feel(-0.6)` → 返回升级上下文给调用方 | `pasm-companion` |
| 机读导出 | 加一个 `snapshot() -> Dict`，**别让外部读 `state.notes`** | `pasm-tutor` |

## 9. 打成技能包

一个正文 → 两种**归档形态**（按结构命名，不按平台名）：

| 形态 | 归档结构 | 产物 |
|---|---|---|
| `zip-root` | ZIP **根目录直接是 `SKILL.md`** | `dist/zip-root/<name>/SKILL.md` + `<name>-<ver>.zip` |
| `slug-dir` | 以 slug 命名的目录，内含 `SKILL.md` | `dist/slug-dir/<name>/SKILL.md` |

在自己的仓写 `tools/build_skill.py`：

```python
from pasm_skills.build import ProjectMeta, SkillSpec, run_cli

META = ProjectMeta(author="you", homepage="https://github.com/you/your-repo")
SKILLS = [SkillSpec(
    name="my-teahouse-agent",
    body_file="SKILL.teahouse.body.md",     # 放在 skill/ 下
    display_name_zh="茶馆掌柜智能体",
    display_name_en="Tea house owner agent",
    desc_zh="……（中文描述，含触发词）",
    desc_en="……",
    plain_desc="……（英文，最小形态用）",
    plain_category="agents",
    plain_tags=["pasm", "npc"],
)]

if __name__ == "__main__":
    raise SystemExit(run_cli(SKILLS, META))
```

```bash
python tools/build_skill.py --zip --clean     # 打两种形态 + ZIP（内置结构自检）
```

> ⚠️ `zip-root` 形态**必须**把 `SKILL.md` 放在 ZIP 根目录。包成 `skills/<name>/SKILL.md`
> 会被平台拒收（报「压缩包缺少 SKILL.md 文件」）—— 平台不递归找。打包库已内置校验。
> ⚠️ 正文里教用户敲的每条命令，都要在**真 `pip install` 装出来的环境**里跑一遍：
> 开发时能跑 ≠ 装了能跑 —— 比如 `tools/xxx.py` 不进 wheel（`packages.find` 默认只收你的包目录），
> 照正文做的用户手里根本没这个文件。实现放包里（`python -m <包>.<模块>`），`tools/` 只留转发壳。

## 10. 进阶：写验证智能体

基座还提供一套"给自己/别人的核心做长期体检"的框架 —— 与产品智能体是两套东西：

```python
from pasm_skills.agent import Agent, register
from pasm_skills import scenarios as S

@register
class MyVerifier(Agent):
    name = "my-verifier"
    goal = "验证 XXX 跑久了会不会坏"
    needs = ("core",)                 # 声明需要哪些仓（core / lite）

    def run(self):
        m = S.run_scenario(self.ctx, MY_BODY, repo="core")   # 隔离子进程跑场景
        S.judge(self, m["metrics"], SPEC, tier="...")        # 阈值表 → OK/WARN/FAIL
```

- `S.choose_python()`：解释器择优（优先带 torch），档位写进结论；
- `S.run_scenario()`：场景跑在**真实核心组件**上，拿不到就 `SKIP`（**不许写自研替身**）；
- `S.judge()`：阈值表驱动，越界默认 WARN，`bad="fail"` 用于安全关键项；
- `pasm_skills.checks`：核心契约检查工具箱（文件/契约/安全底线）。

放到能 pip 安装的包里，并在 `pyproject.toml` 声明入口，基座就会自动发现它：

```toml
[project.entry-points."pasm_skills.agents"]
my-agents = "my_pkg.agents"
```

### 10.1 自检护栏自己必须"可重复"（三条血泪）

护栏写错比不写更糟：它会把**环境残留**报成**能力缺失**，让人去修根本没坏的代码。三条硬规则：

1. **隔离要清"整族"，不能只删基础目录。** 智能体常有 `<id>_ref` / `<id>_brief` / `<id>_fresh` 等变体目录，
   只删基础 id 会留下变体、改变检索排序 —— 同一份代码在干净机器上满分、在你机器上扣分。
   写法：`for p in (Path.home() / ".pasm-agents").glob(<id> + "*"): shutil.rmtree(p, ignore_errors=True)`
2. **被测实现带随机/抖动时，只钉确定性契约。** 例如选题是"80% 最弱 + 20% 随机"，
   就断言 `snapshot()["weakest"]` 与抖动取值范围，**绝不**断言某一次 `pick_next()` 的具体结果
   （`check(..., reply == pick_next())` 这种必 flaky）。
3. **断言里的中间量要与实现同源。** 别拿 A 接口的抽样结果去断言 B 接口的文本 —— 先取稳定字段
   （`snapshot()`），再让文本里的数字与它自洽（如 `f"{int(mastery[t] * 100)}%" in reply`）。

> 复检口径：**同一个包连跑 3 次、并在一台"脏机器"上再跑一遍，结论必须一致**。
> 只跑一次就绿的护栏，等于没护栏。

## 11. 相关

- **pasm-agents**（独立公开仓）—— 官方成品智能体：游戏 NPC / 老人陪伴 / 学习陪伴 / 长期验证。**读它的源码是最好的教程。**
- **pasm-framework**（独立公开仓）—— **应用框架**：把智能体接成完整应用的那一层
  （插件子系统、HTTP 网关与流式输出、知识库自学、多语言客户端）。用 `from pasm_framework import SimpleApplication, capability` 三行起步。
  见其 `docs/tutorials/`（9 篇，含站点智能客服、游戏 NPC、Web 部署）。
- `docs/BUILD-AGENT.md` —— 手把手从零到发版
- `docs/SKILL-FORMAT.md` —— 技能包格式与两种归档形态
- `templates/` —— 可直接复制的智能体骨架与技能正文模板
