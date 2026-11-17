# justin-writing-style

> 一种源自 2026 年中文互联网现象级自述长文的**冷叙事自述体**写作 Skill：用会计的方式写爱情，用账单的方式写崩塌。表面流水账，底下是地震仪。

- **版本**：1.1.0
- **类型**：单 prompt / workflow 风格生成器（含 Judge → Critique → Revision 判断回路）
- **许可证**：Custom Non-Commercial（语料已匿名化，仅供风格复刻，不背书原文内容）

---

![justin-writing-style 风格示意图](justin-writing-style.png)

## 一、这是什么

一种"情绪越大、字越少；事实越重、语气越轻"的叙事文体。全部情感藏在**数字、物件和对话的留白**里，叙述者从不解释、从不抒情、从不哭。

核心指纹（实测自约 7000 字语料，详见 `references/style.md`）：

| 指标 | 实测值 |
|------|--------|
| 平均句长 | 14.9 字（±3） |
| 单句成段占比 | ~85% |
| 具体数量词密度 | 每 53 字 1 个 |
| 直接情感形容词 | **0 个** |
| 比喻密度 | 每千字 ≤ 2 个（仅冷喻） |
| 感叹号 | **0 个** |

---

## 二、适用 / 不适用

**适用**：
- 个人自述体长文
- 病毒式传播的社交媒体叙事（X / 微博 / 公众号长文）
- 虚构纪实体、"表面平静实则崩塌"的情感叙事

**不适用**（命中 description 的排斥边界，会被路由排除）：
- 需要煽情的演讲稿
- 营销文案
- 学术论文
- 诗歌

---

## 三、安装

将本目录整体放入宿主平台的 skills 目录（如 `~/.workbuddy/skills/` 或项目级 `.workbuddy/skills/`），重启会话即可。宿主平台读取 `SKILL.md` 的 `name` / `description` / `version` 完成注册与触发路由。

```bash
cp -r justin-writing-style ~/.workbuddy/skills/
```

---

## 四、触发方式

当用户消息命中以下任一信号时由宿主路由到本 skill：

- 显式：`justin style` / `冷叙述写作` / `克制文体` / `病毒文写作` / `蒙太奇文体` / `零度叙事` / `极简叙事体` / `自述体长文` / `viral essay`
- 语义：要求"用克制、零形容词、数字承载情绪的方式写一段故事/自述"

> 触发描述已显式声明"不适用于"边界，避免误触发（AP-10 防护）。

---

## 五、文件结构

```
justin-writing-style/
├── SKILL.md                  # 根文档：角色、工作流、质量维度、文件导航
├── honest-boundaries.md      # 语料溯源、置信度、已知局限、失败模式预告
├── justin-writing-style.png  # 风格示意图
├── references/               # 稳定风格知识（按需加载）
│   ├── style.md              # 风格指纹（量化参数）+ 风格语法
│   ├── principles.md         # 14 条创作原则（含出处）
│   ├── heuristics.md         # 12 条写作瞬间启发法（信号→纠正）
│   ├── anti-patterns.md      # 10 条反模式 + 检测信号 + 纠正方向
│   └── runtime.md            # 判断回路配置（Judge/Critique/Revision）
├── examples/                # 教学配对
│   ├── positive.md           # 5 个正面仿写 + 解析
│   ├── negative.md           # 5 个错误写法 + 纠正
│   └── contrastive.md        # 同一场景 A 版 vs B 版对照
├── templates/
│   └── output.md             # 结构骨架 + 输出契约 + 平台适配
├── tests/                   # 评估基准
│   ├── golden-set.md         # 4 条基准用例（Case 1-4）
│   └── adversarial.md       # 6 条对抗测试（ADT1-6）
├── evals/
│   └── README.md             # 评估入口 + 部署期验证包（Trigger/Anti-Trigger）
├── CHANGELOG.md
└── README.md
```

> 渐进加载：SKILL.md 只做路由 manifest，各 reference / example / test 文件按需加载，无"Read all files"贪婪加载（满足三层渐进加载原则）。

---

## 六、核心工作流（判断回路）

```
用户给题材/素材
  → Step 1  装载风格：读 references/style.md + principles.md
  → Step 2  选结构装置：冷开场 + 时间硬切 + 物件锚 + 回环结尾（templates/output.md）
  → Step 3  初稿生成：严格按指纹参数写作
  → Step 4  Judge：按 runtime.md 五维度打分（克制/具体/节奏/结构/平叙）
  → Step 5  Critique：对照 anti-patterns.md 逐条检测，命中即标记
  → Step 6  Revision：诊断后局部修改，保护已达标段落（禁止全篇重写）
  → Step 7  终检：跑 tests/golden-set.md 基准，输出成品
```

- **质量维度与一票否决线**（详见 `SKILL.md` 与 `references/runtime.md`）：

| 维度 | 权重 | 一票否决线 |
|------|------|-----------|
| 情感克制 | 0.25 | 出现任何直接情感形容词 → FAIL |
| 具体度 | 0.25 | 连续 100 字无具体数字/物件 → FAIL |
| 节奏 | 0.20 | 情感节点句长 >20 字 → FAIL |
| 结构装置 | 0.15 | 无冷开场且无回环结尾 → WARN |
| 平叙荒诞 | 0.15 | 出现感叹号/惊叹语气 → FAIL |

- **Revision 上限**：普通篇幅 max_rounds = 2；>3000 字长文 = 3。修订须先诊断后改写，原段落保护（preserve）。

---

## 七、合规红线（不可协商）

本 skill 的一切输出**必须使用虚构人物与化名**，禁止真实人名及可识别的真实人物/机构/事件。

- 用户提供的素材若含真实人名 → 先替换为化名再创作；
- 用户坚持使用真实人名 → **停止执行**并说明名誉权/隐私权风险；
- 禁止将"代孕/取卵/巨额转账/威胁"等高敏感情节附着于任何真实人物或可被反向识别的身份特征。

> 语料作者、文中人物及相关真实人名均已匿名化；任何后续维护**不得**回填真实姓名、原帖链接或可溯源标识。

---

## 八、已知局限（诚实边界）

1. **单语料过拟合风险**：全部指纹数值来自一篇文本。
2. **题材依赖性强**：原文传播奇迹建立在"极端财富/权力 + 私人情感崩塌"张力上；普通题材用此文体可能只剩"平淡"。
3. **人称未验证**：语料为第一人称，第三人称/书信体/现在时未验证。
4. **文类边界**：为"病毒式个人自述长文"优化，短视频脚本/演讲稿/广告仅可迁移部分特征。
5. **时代印记**：部分手法带有原文特有的叙事装置，直接照搬可能违和。

详见 `honest-boundaries.md`。

---

## 九、评估与验证

评估套件见 `evals/README.md`：
- **基准**：`tests/golden-set.md`（4 用例）
- **对抗**：`tests/adversarial.md`（6 用例，冲击 Style Drift 防御）
- **部署期验证包**：Trigger / Anti-Trigger prompt 集，每 90 天复跑一次。

---

## 十、维护与演进

- 修订遵循 `CHANGELOG.md` 的 semver-light 规则。

- 演进方向（详见 `honest-boundaries.md`）：补充第二语料校准指纹、增加第三人称与题材迁移验证、收集真实否决记录充实 Failure Memory。

- 修改关键指纹数值前，先 `grep` 其在 `references/style.md`、`SKILL.md`、`references/runtime.md` 的所有出现位置，避免跨文件事实不一致（S11）。

  

## 许可证

Custom Non-Commercial。本 Skill 仅供个人学习与非商业创意写作使用。如需商用，请另行授权。
