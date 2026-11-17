# Life Companion（`life-companion`）

*[English →](README.md)*

> **算出来的是事实，读出来的是镜子。真正做决定的人，永远是你。**

一个「越用越懂你」的私人陪伴 skill——但不是角色扮演那一类。它**真算**（八字、真实星历、
O\*NET 职业数据），然后把结果当镜子递给你，不告诉你会发生什么。

它记得你（一份**只存在你本机**的档案 + 日记，以及会跨会话跟进的开放线索），
从四个角度陪你：**命理命盘 · 每日运势 · 工作匹配 · 恋爱反思**。

贯穿始终的一条底线是**忠实计算，谦逊解读**：算出来的是可复现的事实，解读只是一面镜子，
**不是科学预测**。它不编造数字，不下判决，不给医疗、财务、法律建议。遇到危机会立刻收起
算命那一套，给你真实的求助渠道——而且这些不只是承诺，是**写进代码、由测试守住**的。

---

## 安装

需要 **Python 3.9+**。没有需要手动装的东西——脚本会在首次使用时自动获取 `PyYAML`、
`lunar-python`、`pyswisseph`、`sxtwl`，装不上时（没网络、PEP 668）会打印确切的安装命令。
用 `python3 scripts/companion.py doctor` 一次看全。

**方式一 —— 一行搞定，用 [`npx skills`](https://github.com/vercel-labs/skills)：**

```bash
npx skills add dong845/life-companions
```

它会问你装给哪个 agent、装在哪个范围。加 `-g` 装给所有项目，`-a claude-code`（或
`-a codex`）跳过 agent 选择，`-y` 全程非交互。**仓库根就是这个 skill**，整个目录会被
复制进你的 skills 文件夹。

**方式二 —— 作为 Claude Code 插件**（更新受管）：

```text
/plugin marketplace add dong845/life-companions
/plugin install life-companion@life-companion
/reload-plugins
```

插件形式的 skill 带命名空间，调用是 `/life-companion:life-companion`。两点要注意：
如果你**同时**在 `~/.claude/skills/` 里留了手动副本，这个 skill 会出现两次——没有去重，
删掉一份。另外第三方 marketplace 不会自动更新，要拿新版本得跑
`/plugin marketplace update life-companion`。

**方式三 —— 直接 clone**（想改它就选这个；改动立即生效，插件缓存做不到这点）：

```bash
git clone --depth 1 https://github.com/dong845/life-companions.git ~/.claude/skills/life-companion
```

无论走哪条路，**你的数据都不会跟着走**：档案和日记在 `~/.companion/`，在仓库之外，
既不属于安装内容，也不会被更新覆盖。

---

## 怎么用

像聊天一样说话就行，不用记命令。第一次用会走一段简短的、征得同意的建档。

| 你想要… | 这样说 | 会触发 |
|---|---|---|
| 看命盘 | 「帮我看看八字，1993-04-12 早上 7:35，男，北京」 | 命理命盘 |
| 今天的运势 / 记一天 | 「记一下今天，也看看今天运势」「今天有点丧…」 | 每日运势 + 日记 |
| 想清楚职业方向 | 「我不确定自己适合做什么工作」 | 工作匹配 |
| 理清一段关系 | 「跟对象闹别扭了，怎么办」 | 恋爱反思 |
| 就是想聊聊 | 「帮我梳理一下最近」 | 日记 + 陪伴 |

四个模块相互独立。你问哪个来哪个，不会一次全塞给你。

### 四个模块

**命理命盘 —— 八字 · 西洋星盘 · 紫微斗数 · 合婚**
四柱、日主、五行、十神、大运、流年，全部真算（`lunar-python` 计算，`sxtwl` 独立核验
立春这条年柱边界）。西洋本命盘走真实瑞士星历，出生时刻不明时**宁可不给上升，也不猜**。
紫微斗数按标准安星法起十二宫、命宫身宫、五行局、十四主星和生年四化——但这里**没有第二个
引擎能交叉核验它**，这一点会写在输出里如实告诉你。合婚只算两盘之间传统的地支关系，
**刻意不给「合／不合」的结论、分数或建议**：一句「你俩不合」拆散过本来好好的关系。

解读是**分层**的：一句话画像 → 大白话性格速写 → 分层面（事业／财／感情／健康／家庭／
学业／性格）→ 分阶段的人生时间轴。术语第一次出现就带大白话夹注。

**每日运势 + 日记**
把今天的流年／流月／流日，和你日记里真实写下的东西织在一起，给一段**短**的当天基调，
外加一个温和的宜／忌。不打星级，也不编幸运数字：颜色和数字只作为你八字喜用五行的传统对应出现，
并且标明是这个。顺手可以帮你把今天记下来。

**工作匹配**
一个透明的 21 题兴趣小测，底子是真实的 Holland/RIASEC 模型，对 **188 个真实 O\*NET
职业**（CC BY 4.0）算契合度，给 **低／中／高** 档位加一句置信度说明，**不给假百分比**。
188 个都带 O\*NET 31.0 的数值兴趣分，其中 **173 个**还带工作价值观，所以你补上价值观排序之后，
匹配是真的数据加权。`--find` 负责把你嘴里说的岗位（「核磁共振技师」「高中老师」）对到真实的
职业编码上；不是那份工作本身的，只标成「弱」的近邻，数据里没有的岗位（比如「MRI 重建」）不会被当成
匹配，也不拿最接近的顶替。要写简历会转给 `job-hunt` skill。

**恋爱反思**
拿依恋理论、Gottman、NVC 当镜子：先分开「实际发生了什么」和「你脑补的故事」，两边都站，
命名模式，然后给具体动作——一句修复的话、一个 NVC 句式、一个该直接问对方的问题。
它**按人追踪**，所以「又是这个循环」是站在真实记录上说的，不是凭印象。一次不叫模式。
安全永远优先：识别到胁迫控制或暴力会切成安全模式，绝不 both-sides，直接给专门的求助渠道。

---

## 你的数据在哪、怎么删

全部存在 **`~/.companion/`**（`chmod 700`，POSIX 系统上只有你能读），**从不上传任何地方**：

- `profile.yaml` 档案 · `consent.yaml` 同意记录
- `journal/` 日记（月度 `.md` + 机器可读的 `index.jsonl`）
- `state/` 命盘缓存、工作记忆、按人追踪

**同意分类、可撤销**：生辰、感情、情绪各自单独授权。没授权就不收集、不推断、不存储。

**删除是真删**，对它说就行。删的不只是那一个文件：日记、索引、关系记录、工作记忆、表单留下的
标记里对应的内容会一起清掉（测试会在删完之后把整个目录搜一遍）：

| 你说 | 实际执行 |
|---|---|
| 「删掉我的生辰数据」 | `companion.py forget --birth` |
| 「忘掉六月」 | `companion.py forget --month 2026-06` |
| 「把刚才那条删了」 | `companion.py forget --entry 2026-06-18 --nth 2` |
| 「关于他的都删了」 | `companion.py forget --person 小李 --with-entries` |
| 「不要再记感情的事」 | `companion.py forget --relationships` |
| 「情绪分数都删了」 | `companion.py forget --mood` |
| 「全部清空」 | `companion.py forget --all` |

这样执行只会列出会删掉什么，不动任何文件；你确认之后，它再加上 `--yes` 真正删除。

**撤回同意和删除是两件事。** 说「别再用我的生辰」，所有脚本马上停止读取这一类数据，但文件先留着，
并且告诉你还留着什么、用哪条命令删。误撤回不会丢东西。

所有计算都是**离线**的，八字、星盘、职业匹配都不联网，所以你的数据不会离开这台机器，
也不产生任何 API 费用。

**有一个例外，说清楚**：**第一次**运行时脚本可能联网 `pip install` 那四个依赖。那是下载
软件包，不是你的数据出去——但它确实是一次网络调用，不该躲在"离线"这个词后面。设
`LIFE_COMPANION_NO_AUTOINSTALL=1` 就能禁止它，脚本会改为打印确切的安装命令让你自己装。
此后这个 skill 的任何操作都不碰网络。

---

## 技术备忘（给想改它的你）

```
SKILL.md              路由（始终加载）
AGENTS.md             给非 Claude agent（Codex 等）的入口说明
references/           onboarding · profile-schema · journaling · continuity · forms
                      factcheck · voice · safety（始终生效）
  modules/            destiny · daily-fortune · career · relationships
scripts/              companion.py · bazi.py · astro.py · ziwei.py · synastry.py
                      career_match.py · relationship_patterns.py · safety_scan.py
                      trends.py · form_server.py · selfcheck.py
                      _deps.py · _zh.py · _branches.py · _tz.py
data/content/         bazi-interpretation · bazi-life-arc · relationships
                      （真实框架的内容层，可直接编辑）
data/career/          occupations.json（188 个真实 O*NET，CC BY 4.0）· assessment_items.json
data/zh/              OpenCC 繁→简字表（Apache-2.0）：诚实闸门和危机扫描先把繁体转成简体再匹配
tools/                build_occupations.py：从 O*NET 数据库重建 data/career/occupations.json
                      （维护用，skill 运行时不会调用）
                      run_agent_evals.py：让 codex 在临时项目里逐个跑 evals/evals.json 的场景（维护用）
tests/                回归测试（纯 unittest，全离线）
```

**依赖**：`PyYAML` · `lunar-python`（MIT，八字）· `pyswisseph`（星盘）·
`sxtwl`（BSD，立春交叉核验，可选）。缺失时脚本会尝试自动 pip 安装；装不上的时候
（没网络、PEP 668 externally-managed 的 Python）会打印明确的安装命令和「少了它会怎样」，
而不是甩一段栈。`python3 scripts/companion.py doctor` 一次看全。

**测试**：`python3 tests/test_scripts.py`（几百项，一两分钟，全程不联网）。
另有 `python3 scripts/career_match.py --selftest` 和 `python3 scripts/ziwei.py --selftest`。

**发出去之前过一道闸门**：
`python3 scripts/selfcheck.py --module destiny --file draft.md`

一条命令，两套互不相干的检查：

- **诚实**（会拦，退出码 1）：编造的百分比和星级、宿命句式（包括「大概率保不住」这种
  对冲过的）、对亲人健康的预言、黄历式禁令、预测录用结果、给不在场的一方贴临床标签、
  **编造的求助热线号码**、缺失的免责声明、没夹注的十神、没有来源和时效就抛出的高风险
  事实，以及拿一段解读去替现实决定背书。
- **AI 味**（永不拦）：让回复读起来像一张填好的表的那些**措辞**问题——「不是X，是Y」
  当反射、套话、破折号当默认连接词、句子长度过于均匀、一个断句都没有、填充副词。
  详见 `references/voice.md`，那里同时讲了怎么把中英文都写得通俗易懂。

**解读内容都在 `data/content/`**，想调口吻或加细节，改那里就行，不用动脚本。

**诚实与安全的底线在 `references/safety.md`**，它**优先于任何模块、也优先于任何
「别加免责声明」的要求**。

---

## 许可

代码与文档见 [`LICENSE`](LICENSE)。职业数据来自 O\*NET Resource Center（美国劳工部），
以 **CC BY 4.0** 使用；署名信息就放在 `data/career/occupations.json` 里面，请保留。

---

*算出来的是事实，读出来的是镜子。真正做决定的人，永远是你。*
