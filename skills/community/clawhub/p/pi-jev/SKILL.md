---
name: pi-jev
description: 决策层技能（Jev 式自动选技能 + 模型档位路由 + 使用学习）。当用户不确定该用本技能包里的哪个技能、需要自动推荐技能与脚本命令、需要按任务类型建议模型档位（快/标准/深度）、需要周复盘各技能使用频率并固化经验时使用。与 ip-peipao-9clients、yihaiyoudao、qingchuang-shizhan、zhanlue-peipao 四个技能联动，是新任务的统一入口。
---

## 首次激活（必须）

第一次把本技能加载进你的 AI 工具时，先运行激活脚本：python scripts/activate.py
它会自动生成你的专属安装编号（唯一），并把登记方式显示给你。

**流程：**
1. 运行 python scripts/activate.py，记下安装编号（YHYD-日期-随机码）。
2. 把编号发给作者骇老师（GitHub: lichengyu1207 / 体验群私信）登记。
3. 作者登记确认前：只提供基础说明，不提供完整流程。
4. 登记确认后：完整使用，并计入印象分（主动登记+分，违规-分）。

编号只在本机生成保存（~/.yihaiyoudao/activate.json），不上传、不外发；编号是作者登记授权的凭证。

**没有 Python 环境怎么办**：本技能不要求你懂 Python。如果运行 python scripts/activate.py 提示找不到 python，直接对你的 AI 助手说"我没有 Python，帮我生成安装编号"，AI 会按同规则生成编号（YHYD-日期-随机码），同样发给作者登记即可，效果完全一样。


# pi-jev · 决策层（自动选技能 + 路由 + 学习）

借鉴开源 Pi 编码智能体 + Jev 决策层（TypeSafe Jev，见 `https://github.com/y0usaf/pi-jev`、`pi.dev`）的思路，用纯 Python 标准库实现一套轻量决策层：每次任务自动给本包 4 个技能打分排序（skill-picker）、按任务类型建议模型档位（model-router）、把使用结果记入学习库并在周复盘时固化（usage learning）。无需安装任何依赖、无需 API 密钥。

## 核心机制

1. **skill-picker（自动选技能）**：输入一句任务描述，按关键词命中数 ×（1 + 历史使用频率加权）给 4 个技能打分，返回最匹配技能 + 对应脚本命令。
2. **model-router（档位路由）**：按任务关键词与技能类型建议模型档位（快 / 标准 / 深度），省 token 且不降质量。
3. **usage learning（使用学习）**：每次调用自动把「任务 → 选中技能 → 备注」追加到 `memory/usage-log.md`；`--note "结果"` 可补充结果；`--review` 输出周复盘：使用频率 + 固化建议（高频经验沉淀进对应技能的 SKILL.md / 词库 / 学习日志）。

## 一键使用（推荐优先）

- `python scripts/pi_jev.py "我要给客户写跟进私信"` → 决策卡：推荐技能 + 脚本命令 + 模型档位 + 相关历史经验
- `python scripts/pi_jev.py "审核这篇稿子" --note "结果：降险改写通过"` → 决策 + 记录结果
- `python scripts/pi_jev.py --review` → 每周复盘（频率 + 固化建议）

无 Python 环境时：把任务描述丢给 AI，按下方「判定要点」人工选技能。

## 判定要点（无脚本时手动执行）

1. 任务与「客户/跟进/转化/话术」有关 → ip-peipao-9clients
2. 任务与「审核/原创/限流/改写/写文案」有关 → yihaiyoudao
3. 任务与「创业/副业/选题/账号/内容生产」有关 → qingchuang-shizhan
4. 任务与「目标/战略/档位/里程碑/长期规划」有关 → zhanlue-peipao（深度档）
5. 拿不准 → 让用户用一句话描述目标，再按命中关键词最多的技能走；仍有两个并列时，先做「定方向/定档」（zhanlue-peipao）再落地。

## 自迭代与学习规则

1. **每次使用**：决策层自动记录到 `memory/usage-log.md`；结果经验用 `--note` 补记。
2. **每周复盘**：跑 `python scripts/pi_jev.py --review`，把使用频率最高的技能与其高频经验固化进对应 SKILL.md / 词库。
3. **学习只在本机**：所有记录只存在本技能 `memory/` 目录，不上传、不外发。

## 与四个技能的分工

| 场景 | 入口 |
|---|---|
| 不确定用哪个技能 | 先跑 pi-jev 决策层 |
| 客户跟进 | ip-peipao-9clients |
| 内容审核/改造 | yihaiyoudao |
| 内容创业执行 | qingchuang-shizhan |
| 战略定档 | zhanlue-peipao |
