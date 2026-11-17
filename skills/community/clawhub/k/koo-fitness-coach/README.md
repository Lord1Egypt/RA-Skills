<div align="center">

# 💪 私人健身教练

**koo-fitness-coach**

一个 WorkBuddy（AI）技能：让 AI 以**专业私人教练**的身份工作 —— 先做风险筛查与能力分级，再按专项（力量 / 增肌 / 减脂 / 体能）给出安全、可执行、个性化的训练方案与饮食方案，并持续跟进调整。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Skill-orange.svg)](https://www.workbuddy.cn/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple.svg)](#安装跨平台)
[![Hermes](https://img.shields.io/badge/Hermes%20Agent-compatible-teal.svg)](#安装跨平台)
[![Codex](https://img.shields.io/badge/Codex%20CLI-compatible-green.svg)](#安装跨平台)
[![References](https://img.shields.io/badge/references-14-blueviolet.svg)](#目录结构)
[![Exercises](https://img.shields.io/badge/exercises-16-brightgreen.svg)](#动作库)

</div>

---

> 💡 **设计原则：先评估、再开方** —— 不收集信息就不给方案。
> 任何训练建议都必须挂在「能力分级」和「安全红线」之下：强度要标注依据（%1RM 或 RPE/RIR），计划要给进阶规则和退阶选项，涉及疼痛先给就医建议而不是负荷处方。

## ✨ 能做什么

- 🩺 **风险筛查与分级**：PAR-Q+ 心血管/健康风险筛查、体测、动作筛查（含 FMS 七动作框架与关节逐段排查），输出新手 / 中级 / 进阶分级
- 🏋️ **专项训练方案**：力量、增肌、减脂、体能四条专项线，各有强度区间、组次参数、分化模板与进阶规则
- 🎯 **动作技术指导**：16 个动作的标准步骤、常见错误、纠错口令与退阶 / 进阶链路
- 🥗 **运动营养方案**：Mifflin-St Jeor 能量计算 → 宏量分配 → 食谱模板（含素食版）→ 连锁外卖点餐清单 → 补液标准
- 🚦 **安全边界管理**：停练信号、力竭边界、疼痛红绿灯、特殊人群（高血压 / 糖尿病 / 孕妇 / 老年 / 青少年）调整
- 🔁 **跟进与调整**：4 周 / 12 周复测节奏、平台期排查、训练日志与数据 schema

## 📌 适用场景

- ✅ 健身新手制定第一份可执行的训练计划
- ✅ 有经验者排查平台期、优化分化与容量安排
- ✅ 动作做不对 —— 深蹲膝盖内扣、硬拉弓背、卧推肩痛等
- ✅ 增肌 / 减脂期的热量与宏量营养素规划
- ✅ 慢病人群能不能练、怎么练的安全边界咨询
- ✅ 私教备课、写训练日志、做会员跟进

> ❌ **不适用**：疾病诊断、疾病营养处方、术后康复方案 —— 这些只会**转介**并建议就医。

## 🚀 安装（跨平台）

本技能兼容主流 AI 编码助手与 Agent 框架。先 clone，再按你用的工具放到对应目录即可：

```bash
git clone https://github.com/fengeail/koo-fitness-coach.git
```

### 各平台安装位置

| 平台 | 安装目录 | 加载方式 | 兼容文件 |
| --- | --- | --- | --- |
| **WorkBuddy** | `~/.workbuddy/skills/koo-fitness-coach/` | 自动识别 `SKILL.md` | `SKILL.md` |
| **Claude Code** | `.claude/skills/koo-fitness-coach/` | 自动识别 `SKILL.md` | `SKILL.md` |
| **Hermes Agent** | `~/.hermes/skills/koo-fitness-coach/` | 自动识别 `SKILL.md`（兼容 agentskills.io） | `SKILL.md` |
| **OpenClaw** | 技能目录 | 兼容 agentskills.io 开放标准 | `SKILL.md` |
| **Codex CLI** | 项目根目录 | 自动读取 `AGENTS.md` | `AGENTS.md` |
| **Cursor** | 项目根 或 `.cursor/skills/` | 读取 `.cursorrules` | `.cursorrules` |

一键复制命令：

```bash
# WorkBuddy
cp -r koo-fitness-coach ~/.workbuddy/skills/

# Claude Code（项目级）
mkdir -p .claude/skills && cp -r koo-fitness-coach .claude/skills/

# Hermes Agent
cp -r koo-fitness-coach ~/.hermes/skills/

# Codex CLI / Cursor —— 直接在项目根使用，无需复制
cd koo-fitness-coach && codex   # Codex 自动读 AGENTS.md
# Cursor 自动读 .cursorrules
```

安装后直接对话即可触发，例如：

> 我想减脂，每周能练 3 次，家里有一对可调哑铃，该怎么安排？

> 深蹲总是膝盖内扣，怎么纠正？

> 高血压的人可以做力量训练吗，要注意什么？

> 卧推卡在 60kg 三个月了，怎么突破？

### 兼容性说明

- 本技能是**纯提示词技能**：不含脚本、不访问网络、不读写文件系统、不调用外部服务，无第三方依赖。
- 各平台的加载入口文件已全部内置（`SKILL.md` / `AGENTS.md` / `.cursorrules`），互不冲突。
- `SKILL.md` 仅约 5.7 KB，详细信息按场景**按需加载** `references/` —— 不会一次性塞满上下文。

## 🧭 工作流（六步闭环）

```
1. 收集信息        → 目标 / 经验 / 伤病史 / 频率时长 / 可用器械
2. 风险筛查        → PAR-Q+（assessment.md）
3. 评估与分级      → 体测 + 动作筛查 → 新手 / 中级 / 进阶
4. 专项方案        → 力量 / 增肌 / 减脂 / 体能，强度标注 %1RM 或 RPE/RIR
5. 动作指导        → 标准步骤 + 纠错口令 + 退阶选项
6. 营养与跟进      → 能量计算 + 食谱；4 周 / 12 周复测，平台期排查
```

## 🗂 文件路由

`SKILL.md` 内置路由表，按用户场景决定加载哪些 references：

| 用户场景 | 必读文件 |
| --- | --- |
| 首次咨询、不知从哪开始 | `assessment.md` → `session-sop.md` |
| 要正式评估 / 量化基线 / 复测对比 | `movement-screen.md` |
| 定训练阶段 / 判断该练什么 | `opt-model.md` + `assessment.md` |
| 出周计划 / 月计划 | `program-design.md` + 对应专项 |
| 教具体动作 | `exercise-library.md` + `coaching-cues.md` |
| 算饮食 / 备餐 / 外食 | `nutrition.md` |
| **提到疼痛 / 伤病 / 术后** | **`rehab.md` + `safety.md`（必须先读再答）** |
| **提到高血压 / 糖尿病 / 孕妇 / 老年 / 青少年** | **`safety.md`** |

场景可叠加，**冲突时安全文件优先**。

## 🏋️ 动作库

`references/exercise-library.md` 收录 **16 个动作**，按 7 大运动模式分组：

| 运动模式 | 动作 |
| --- | --- |
| 蹲 | 高脚杯深蹲、杠铃后蹲、保加利亚分腿蹲 |
| 髋铰链 | 罗马尼亚硬拉、传统硬拉、臀桥 |
| 水平推 | 俯卧撑、哑铃卧推、杠铃卧推 |
| 垂直推 | 站姿推举、哑铃肩推 |
| 水平拉 | 坐姿划船、单臂哑铃划船 |
| 垂直拉 | 引体向上、高位下拉 |
| 核心与孤立 | 平板支撑、农夫行走、面拉 |

每个动作含：目标肌群 / 起始姿势 / 执行步骤 / 常见错误 / 纠错口令 / 退阶 / 进阶。

## 🔬 知识来源与版权边界

本技能的 references 是**方法论的重述与简化**，不是任何书籍或课程的原文摘录：

| 参考来源 | 接入方式 |
| --- | --- |
| NASM OPT 模型 | 保留五阶段递进逻辑与参数框架，做简化落地版（`opt-model.md`） |
| FMS 功能性动作筛查 | 只归纳公开方法框架（7 动作、0-3 分制、取低分、疼痛优先），不含官方评分细则表 |
| 《灵活如豹》 | 重述其关节逐段排查逻辑，非原文引用（`movement-screen.md`） |
| 《Starting Strength》 | 仅在 `strength.md` 标注为**流派选项之一**，并说明其体系性选择 |
| NSCA / ACSM 标准 | 强度区间与补液标准做通用化表述；力量常模明确标注为**粗略经验区间**，非官方常模 |

**有意不收录的内容**：可由模型通用知识覆盖的基础解剖与训练常识、需要认证才能使用的官方评分细则、以及面向运动科学研究而非私教实操的学术理论。

> FMS 是带有认证体系的商标。本技能只使用其公开的方法框架；完整评分细则请参考官方认证课程。
> 《力量训练解剖学》《肌力训练圣经》《运动训练周期》等著作受版权保护，本项目不包含其原文内容。

## ⚠️ 安全边界与免责声明

- 不做医疗诊断，不开疾病营养处方；
- 康复相关只做**转介** + 医疗指导下的回归训练支持；
- 涉及伤病话题时，输出必须以「建议先就医」开头，**不给负荷处方**；
- 特殊人群（高血压 / 糖尿病 / 孕妇 / 老年 / 青少年）默认先读 `safety.md`；
- 所有计划均标注「仅供参考，身体不适请及时就医」。

> 本项目内容为一般性健身指导信息，**不能替代**医生、物理治疗师或注册营养师的专业意见。训练前请评估自身健康状况，如有不适请及时就医。

## 📁 目录结构

```
koo-fitness-coach/
├── SKILL.md                     # 技能入口（WorkBuddy / Claude Code / Hermes / OpenClaw）
├── AGENTS.md                    # Codex CLI 项目指令
├── .cursorrules                 # Cursor 规则
├── README.md
├── LICENSE
└── references/                  # 按需加载的领域资料（14 篇）
    ├── assessment.md            # PAR-Q+ 筛查、体测、动作筛查、分级决策树、专项体测
    ├── movement-screen.md       # 标准化筛查（FMS 七动作评分、关节逐段排查）
    ├── opt-model.md             # NASM OPT 五阶段模型（阶段递进与升降级规则）
    ├── exercise-library.md      # 动作库：16 个动作，按 7 大运动模式分组
    ├── program-design.md        # 通用计划框架（目标×频率矩阵、周期化、进阶规则、计划模板）
    ├── strength.md              # 力量专项（%1RM 区间、RPE/RIR、5×5、5/3/1、力量水平参考区间）
    ├── hypertrophy.md           # 增肌专项（容量、力竭管理、分化模板、容量速查表）
    ├── fat-loss.md              # 减脂专项（热量缺口、有氧/NEAT、训练模板、diet break）
    ├── conditioning.md          # 体能专项（能量系统、心率区间、LISS/HIIT、专项体能模板）
    ├── nutrition.md             # 运动营养（五步流程、能量计算、食谱模板、补液标准、补剂）
    ├── rehab.md                 # 康复协作框架（疼痛红绿灯、转介标准、沟通话术）
    ├── safety.md                # 安全红线（停练信号、力竭边界、特殊人群、CPR/AED、合规）
    ├── coaching-cues.md         # 纠错口令（高频口令速查表、投放原则、保护技术）
    └── session-sop.md           # 课程 SOP（评估课、备课清单、训练日志、数据 schema）
```

## 🛠 定制建议

references 中的通用内容已可直接使用，无需填空。如需按个人风格调整：

- **执教口令 / 口头禅** → 改 `coaching-cues.md` 的口令表
- **常用动作** → 在 `exercise-library.md` 按 7 字段模板追加
- **主力客户类型的计划** → 在 `program-design.md` 第 6 节追加模板
- **执业地区资质要求** → 按 `safety.md` 末节的提示自行核对补充

## 🙏 致谢

- 方法论参考：NASM OPT 模型、FMS 筛查体系、NSCA / ACSM 指南及上述出版物
- 技能运行环境：[WorkBuddy](https://www.workbuddy.cn/)

---

<div align="center">

**⭐ 如果这个技能帮到了你，欢迎 Star 支持一下！**

</div>
