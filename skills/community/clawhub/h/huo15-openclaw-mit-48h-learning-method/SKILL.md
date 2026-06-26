---
name: huo15-openclaw-mit-48h-learning-method
displayName: 火一五48小时学习法技能
version: 3.0.0
description: 麻省理工学院48小时学习法技能（青岛火一五信息科技有限公司）。完整还原 Ihtesham Ali 原始三问框架 + 反馈循环 + 完整 48h 三阶段时间线，叠加网上最佳实践（synthesis / contradictions / gaps / Feynman teach-back / weakness analysis / practice exam）和 NotebookLM 2026 原生子命令（flashcards / quiz / mindmap / chat-config / download）。
  核心三问（精确措辞）：
  Q1 心智模型：该领域每位专家共享的 5 个核心心智模型
  Q2 专家分歧：3 个根本不同意的问题及各方最强论证（steelman）
  Q3 暴露性问题：10 个区分真懂和假背的问题
  Q+ 反馈循环：错答时 → 诊断错误 + 给真懂回答 + 生成追击问题
  科学原理：Active Recall（主动回忆）+ Desirable Difficulty（必要难度）+ Conceptual Frameworks First（先框架后细节）
  触发场景：（1）用户要求快速学习某个领域；（2）用户提到 MIT 学习法、48 小时学习、NotebookLM 三问、context stacking；（3）用户需要生成播客/视频/抽认卡/思维导图概览；（4）用户想用 AI 辅助构建知识体系；（5）用户提到 Ihtesham Ali 或他的 viral tweet。
aliases:
  - 火一五48小时学习法技能
  - 火一五MIT学习法技能
  - 火一五学习法技能
  - 火一五三问学习技能
  - 火一五NotebookLM技能
  - MIT学习法
  - 48小时学习
  - NotebookLM三问
  - Ihtesham学习法
  - context-stacking
---

# 火一五 MIT 48 小时学习法 v3.0.0

> "I accidentally discovered how to compress a semester of learning into 48 hours."
> — Ihtesham Ali（X 推文 3M+ views，27K bookmarks）

MIT 研究生发明、Ihtesham Ali 整理传播的 NotebookLM 学习方法：48 小时内从零掌握任意领域，足以通过 qualifying exam。本技能完整还原其原始三问框架 + 反馈循环 + 完整 48h 时间线，并叠加 Ihtesham 全集中的进阶 prompts（synthesis / contradictions / gaps / Feynman / weakness / exam）和 NotebookLM 2026 全部多模态能力。

## 一、为什么这个方法有效（科学原理）

| 原理 | 说明 | 在本技能中的体现 |
|---|---|---|
| **Conceptual Frameworks First** | 先掌握领域结构，再填充细节，比从细节往上拼接快 10 倍 | Phase 1 的 Q1（mental models）+ Q2（disagreements） |
| **Active Recall** | 尝试回答比重读笔记的记忆效果强数倍 | Phase 2 用 6 小时回答 10 个 probing questions |
| **Desirable Difficulty** | 暴露知识缺口的难题比简单复习产生更深的学习 | Q3 暴露性问题 + Q+ 反馈循环 + 模拟考 |

## 二、原始 48h 时间线（Ihtesham 原方案 + 我们的扩展）

```
Hour 0 ─── 1: Phase 1  Context Stacking + 智识地图
            ├ 上传海量资料（原方案：6 教科书 + 15 论文 + 全部 lecture）
            └ 三问 Q1/Q2/Q3 → 拿到 5 心智模型 + 3 分歧 + 10 暴露问题

Hour 1 ─── 7: Phase 2  主动回忆 + 反馈循环
            ├ 用 6 小时认真回答 10 个 probing questions
            └ 每答错 → ask followup → 诊断盲点 → 追击问题

Hour 7 ── 48: Phase 3  综合 + 模拟考 + 多模态巩固
            ├ synthesize / weakness / exam
            ├ flashcards + mindmap + audio overview
            └ export 到本地知识库
```

## 三、前置条件

```bash
# 首次必须认证（浏览器交互登录 Google）
~/.venv/notebooklm/bin/nlm login
```

脚本每次执行前自动检测登录状态，失效会自动重新 `nlm login`。

## 四、命令一览

> 脚本位置：`huo15-openclaw-mit-48h-learning-method/scripts/mit-learn.sh`

### 4.1 笔记本管理

```bash
mit-learn.sh init "强化学习"            # 创建/复用同名笔记本
mit-learn.sh add --url "..." --file ./paper.pdf --youtube "..." --wait
mit-learn.sh status                      # 当前 notebook 详情
mit-learn.sh list                        # 列出所有 notebooks
```

### 4.2 三问框架（核心精髓）

```bash
mit-learn.sh ask mental-models      # Q1: 5 个核心心智模型
mit-learn.sh ask disagreements      # Q2: 3 个根本分歧 + steelman
mit-learn.sh ask probing            # Q3: 10 个暴露性问题
mit-learn.sh ask followup "我的回答…"  # Q+: 反馈循环（错答诊断+追击）
mit-learn.sh ask all                # 完整三问 Q1→Q2→Q3
```

**Q+（反馈循环）是整个方法最容易被忽视的精髓**：每次回答完一个 probing question，立刻把答案传给 `ask followup`，让 NotebookLM 诊断你的盲点并生成更深的追击问题。Ihtesham 原文：*"Every wrong answer triggered: 'Explain why this is wrong and what I'm missing.'"*

### 4.3 进阶分析（Ihtesham 全集 + 网上最佳实践）

```bash
mit-learn.sh synthesize         # 综合所有资料为一个统一思维框架
mit-learn.sh contradictions     # 找出资料之间的矛盾（含隐含矛盾）
mit-learn.sh gaps               # 对照行业标准识别知识缺口（致命/重要/次要）
mit-learn.sh feynman "梯度下降" "我的解释..."   # Feynman 角色反转 teach-back
mit-learn.sh weakness           # 预测学习者最可能的 5 个盲区
mit-learn.sh exam               # 生成 15 题模拟期末考（含评分要点）
```

### 4.4 NotebookLM 多模态产物

```bash
mit-learn.sh audio [deep_dive|brief|critique|debate]
mit-learn.sh video [auto_select|classic|whiteboard|kawaii|anime|...] [explainer|brief|cinematic]
mit-learn.sh flashcards [easy|medium|hard]
mit-learn.sh quiz
mit-learn.sh mindmap
mit-learn.sh chat-config [default|learning_guide|custom]   # 设置 chat persona
mit-learn.sh download audio --id <artifact_id> -o out.m4a  # 下载已生成产物
```

### 4.5 完整流程

```bash
# 快捷：init → add → 三问 → audio
mit-learn.sh full "强化学习" --file ./book.pdf --url "https://..."

# 完整 48h 马拉松：三阶段 + synthesis + weakness + exam + 多模态 + export
mit-learn.sh marathon "强化学习" --file ./book.pdf --youtube "..."
```

### 4.6 知识库整合

```bash
mit-learn.sh export   # 把所有产物导出到 ~/knowledge/huo15/learning/<topic>/
```

每次 `ask` / `synthesize` / 等命令都会自动把 prompt + 响应保存为 markdown 到 `~/knowledge/huo15/learning/<topic>/<日期>-<命令>.md`，符合三层记忆/KB 协调规则的 L3 共享 KB wiki。

## 五、Ihtesham 原始三问 vs 本技能的强化版

| 维度 | Ihtesham 原始措辞 | 本技能强化点 |
|---|---|---|
| Q1 Mental Models | "5 core mental models that every expert in this field shares" | 加入"为什么是核心""跨子领域使用频次""相互嵌套关系"等结构化要求 |
| Q2 Disagreements | "best argument from each side" | 强制要求 steelman、识别分歧根源（本体论/方法论/价值观/证据偏好） |
| Q3 Probing Questions | "expose whether someone deeply understands vs memorized" | 显式约束：≥3 道反直觉题，≥2 道隐含假设题，≥2 道跨领域迁移，≥1 道识别教科书简化 |
| Q+ Followup | "Explain why this is wrong and what I'm missing" | 加入认知盲点诊断 + 生成"追击问题" |

## 六、典型 48h 工作流示例

```bash
# Day 1 早晨（Phase 1，约 1 小时）
mit-learn.sh init "Transformer 架构"
mit-learn.sh add \
  --file ~/papers/attention-is-all-you-need.pdf \
  --file ~/papers/gpt3.pdf \
  --url "https://jalammar.github.io/illustrated-transformer/" \
  --youtube "https://youtu.be/iDulhoQ2pro" \
  --wait
mit-learn.sh ask all   # 拿到智识地图

# Day 1 上午~下午（Phase 2，约 6 小时）
# 用纸笔/语音逐个回答 Q3 的 10 个 probing questions
# 每答完一题：
mit-learn.sh ask followup "我的回答是：multi-head attention 就是把 Q/K/V 分成 8 份并行..."
# 再答下一题、followup …

# Day 2（Phase 3，剩余 24 小时）
mit-learn.sh synthesize    # 综合成统一框架
mit-learn.sh weakness      # 看看自己最可能哪里没学透
mit-learn.sh exam          # 自我测试
mit-learn.sh flashcards hard
mit-learn.sh mindmap
mit-learn.sh audio brief   # 用洗澡/通勤时间反复听
mit-learn.sh export        # 沉淀到知识库
```

## 七、环境变量

| 变量 | 默认值 | 用途 |
|---|---|---|
| `NLM` | `~/.venv/notebooklm/bin/nlm` | nlm CLI 路径 |
| `NOTEBOOKLM_PROFILE` | `default` | 多 Google 账号切换 |
| `MIT_LEARN_LANG` | `zh-CN` | audio/video 输出语言 |
| `MIT_LEARN_KB_DIR` | `~/knowledge/huo15/learning` | 导出目录 |
| `DEBUG` | `0` | 设为 `1` 打印 debug 日志 |

## 八、注意事项

- 当前 notebook ID 保存在 `~/.mit-learn-notebook-id`，所有非 init 命令复用它
- 切换学习项目时重新 `init` 即可
- NotebookLM API 有速率限制，连续请求建议间隔 10s+
- 三问/进阶命令的输出**自动保存**到 `~/knowledge/huo15/learning/<topic>/`，无需手动复制
- 反馈循环（`ask followup`）是这个方法的灵魂——不要省略
- `marathon` 命令会跑完所有阶段产物，约 5-10 分钟（不含你回答 probing 的 6 小时）

## 九、参考资料

- [Ihtesham Ali on X - 原始 viral 推文](https://x.com/ihtesham2005/status/2030214970353602806)
- [Ihtesham Ali on X - 90 分钟 context stacking 进阶](https://x.com/ihtesham2005/status/2041576806810370553)
- [Ihtesham Ali on X - 16 NotebookLM 进阶 prompts](https://x.com/ihtesham2005/status/2031706700139675875)
- [How an MIT Student Compressed a Semester of Learning into 48 Hours with NotebookLM](https://cerebrodigital.net/en/how-an-mit-student-compressed-a-semester-of-learning-into-48-hours-with-notebooklm/)
- [NotebookLM Advanced Guide 2026: Custom Instructions, Deep Research](https://www.shareuhack.com/en/posts/notebooklm-advanced-guide-2026)
- [10 NotebookLM Prompts For Studying (Beat 99% of Students)](https://www.learnwithmeai.com/p/notebooklm-prompts-for-studying)

---

## 更新日志

### v3.0.0 (2026-04-27)

**重大重构：精髓还原 + 进阶能力 + NotebookLM 2026 集成**

#### 精髓修正
- **三问 prompt 用 Ihtesham 原始措辞**（"5 core mental models that every expert in this field shares" 等），叠加结构化输出要求
- **新增 Q+ 反馈循环**（`ask followup`）：实现 Ihtesham 原文 *"Explain why this is wrong and what I'm missing"*——这是原方法最易被忽略的精髓
- **新增完整 48h 时间线**（`marathon` 命令）：Phase 1 智识地图 / Phase 2 主动回忆 / Phase 3 综合巩固

#### 6 个新增进阶命令（基于 Ihtesham 全集 + 网上最佳实践）
- `synthesize` — 综合所有资料为一个统一思维框架（Ihtesham synthesis prompt）
- `contradictions` — 找资料之间的矛盾（含隐含矛盾检测）
- `gaps` — 对照行业标准识别致命/重要/次要知识缺口
- `feynman` — Feynman 角色反转 teach-back（你解释，AI 当 12 岁孩子追问）
- `weakness` — 预测学习者最可能的 5 个知识盲区
- `exam` — 生成 15 题模拟期末考（含评分要点和及格线）

#### NotebookLM 2026 原生子命令集成
- `flashcards` / `quiz` / `mindmap` — 调 nlm 原生命令
- `chat-config` — 设置 notebook-level chat goal（learning_guide/custom）
- `download` — 下载所有产物（audio/video/quiz/flashcards/mindmap/report/...）

#### 知识库整合
- 所有 `ask` / 进阶命令的输出**自动保存**为 markdown 到 `~/knowledge/huo15/learning/<topic>/`
- `export` 命令生成 INDEX.md 汇总学习档案

#### Bug 修复
- 修复脚本主入口调用 `usage` 但未定义导致 command-not-found 的 bug
- 修复 SKILL.md 中错误的脚本路径（原写 `huo15-mit-48h-learning-method` 缺 openclaw 前缀）
- 统一版本号（_meta.json / config.json / SKILL.md / 脚本注释）
- `auto_login` 仅对网络命令运行，help/list 不再触发不必要的网络检查
- 修复空数组传递给 `cmd_add` 时产生空字符串参数的 bug
- 颜色变量 `LANG` 重命名为 `LEARN_LANG`，避免污染 shell 全局 `LANG` 变量

### v2.0.0 (2026-04-06)
- 支持 file:// URL 自动转真实路径
- 音频生成 wait_for_audio 等待确认
- 重复 notebook 检测
- 自动续登录
- 修复 full 命令数组传参 bug

```bash
# 一键体验完整 48h 学习马拉松
mit-learn.sh marathon "你想学的领域" --file ./key-paper.pdf --url "..." --youtube "..."
```
