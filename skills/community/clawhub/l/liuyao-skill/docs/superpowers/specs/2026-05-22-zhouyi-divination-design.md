# liuyao-skill（六爻）设计文档

## 概述

基于周易占卜原理，开发一个兼容 agentskills.io 标准的 skill，供 Hermes Agent 和 opencode 使用。支持铜钱法伪随机起卦、蓍草法伪随机起卦和手动输入起卦，解卦覆盖卦辞原文、传统注解和 AI 个性化解读。

## 当前进度（2026-05-22）

- 已完成：Skill 主指令、铜钱法起卦、手动输入起卦、蓍草法起卦、六十四卦结构化数据、卦辞/爻辞资料、解卦指引。
- 已验证：八卦识别按从下往上的爻序计算，本卦/变卦 lookup 由卦象资料派生，核心逻辑已有 `unittest` 覆盖。
- 待扩展：报数起卦、时间起卦、文字笔画起卦，以及更细的传统注解资料。

## 方案选择

采用方案 A：纯 SKILL.md 文档型 Skill。理由：
- Hermes 原生支持 skill 的 scripts/ 目录，agent 可通过 execute_code 直接运行 Python 脚本
- 渐进式加载让六十四卦等大量数据不会一次性灌入上下文
- 开发量适中，部署简单（放到 ~/.hermes/skills/ 或 ~/.config/opencode/skills/）
- 完全兼容 agentskills.io 标准

## 目录结构

```
./
├── SKILL.md                    # 主指令文件
├── scripts/
│   ├── qigua.py               # 起卦脚本（铜钱法伪随机 + 蓍草法伪随机 + 手动输入）
│   └── regenerate_guaci.py    # 卦辞资料再生成脚本
├── references/
│   ├── 64gua-table.md         # 六十四卦速查表
│   ├── guaci-full.md          # 六十四卦卦辞全文
│   ├── yaoci-full.md          # 六十四卦爻辞全文
│   └── jiegu-guide.md         # 解卦方法与注解指引
├── assets/
│   └── gua-data.json          # 卦象结构化数据（供脚本使用）
└── tests/
    └── test_qigua.py          # 起卦逻辑与资料一致性测试
```

## SKILL.md 核心流程

```
用户请求占卜
    ↓
检查"三不占"原则 → 不诚不占、不义不占、不疑不占 → 不符合则拒绝并说明原因
    ↓
选择起卦方式
    ├── 自动铜钱法 → 运行 scripts/qigua.py --method coin
    ├── 蓍草法 → 运行 scripts/qigua.py --method shicao
    └── 手动输入 → 运行 scripts/qigua.py --method manual --input "..."
    ↓
得到本卦 + 变卦（JSON 格式输出）
    ↓
查 references/64gua-table.md 确认卦名
    ↓
读取 references/guaci-full.md 卦辞原文
    ↓
读取 references/yaoci-full.md 动爻爻辞原文
    ↓
读取 references/jiegu-guide.md 传统注解
    ↓
AI 综合解读：结合卦象 + 用户问题 → 给出个性化建议
```

## 起卦脚本 qigua.py 设计

### 命令行接口

- `--method coin`：铜钱法伪随机起卦，自动摇6次，输出本卦和变卦
- `--method manual`：手动输入模式，用户逐爻输入（1背=少阳，2背=少阴，3背=老阳，0背=老阴）
- `--method shicao`：蓍草法伪随机起卦，按经典蓍草法爻值概率建模（6=1/16、7=5/16、8=7/16、9=3/16）

### 输出格式

JSON，键名统一使用英文（便于脚本和 SKILL.md 引用一致）：

```json
{
  "ben_gua": {"name": "天火同人", "upper": "乾", "lower": "离"},
  "bian_gua": {"name": "天雷无妄", "upper": "乾", "lower": "震"},
  "yao_details": [
    {"position": 1, "type": "少阳", "symbol": "—", "moving": false, "label": "初九"},
    {"position": 2, "type": "少阴", "symbol": "--", "moving": false, "label": "六二"},
    {"position": 3, "type": "老阳", "symbol": "—", "moving": true, "label": "九三"},
    {"position": 4, "type": "少阳", "symbol": "—", "moving": false, "label": "九四"},
    {"position": 5, "type": "少阴", "symbol": "--", "moving": false, "label": "六五"},
    {"position": 6, "type": "少阳", "symbol": "—", "moving": false, "label": "上九"}
  ],
  "moving_yao": ["九三"],
  "timestamp": "2026-05-22T14:30:00"
}
```

SKILL.md 引用方式：从 ben_gua['name'] 取本卦名，从 bian_gua['name'] 取变卦名

### 铜钱法伪随机逻辑

每次摇卦模拟3枚铜钱：
- 每枚铜钱：随机决定正反面，背面=阳（1），正面=阴（0）
- 3枚结果求和：0背=老阴(×)，1背=少阳(—)，2背=少阴(--)，3背=老阳(〇)
- 重复6次，从下往上排列

### 手动输入逻辑

用户输入6个数字（每个0-3），代表每爻的背面数量：
- 0 → 老阴(×)，动爻
- 1 → 少阳(—)，静爻
- 2 → 少阴(--)，静爻
- 3 → 老阳(〇)，动爻

## 数据文件设计

### assets/gua-data.json

结构化数据，包含：
- 八卦基本信息（名称、符号、自然象征、方位、二进制编码）
- 六十四卦映射表（upper_trigram + lower_trigram → 卦名）
- 每卦的上下卦组成
- `_meta.trigram_binary_order` 说明 `trigrams.*.binary` 使用自上而下位序；脚本读取六爻时使用自下而上位序，并在代码注释中说明。
- `lookup` 不在 JSON 中重复存储，由 `scripts/qigua.py` 运行时从 `hexagrams` 派生。

### references/64gua-table.md

六十四卦速查表，按行=外卦/上卦、列=内卦/下卦交叉排列，便于 agent 快速定位卦名。

### references/guaci-full.md

六十四卦卦辞原文，按卦名索引。格式：
```
## 乾为天
卦辞：元亨利贞

## 坤为地
卦辞：元亨，利牝马之贞...
```

### references/yaoci-full.md

六十四卦全部爻辞原文（初爻到上爻），按卦名索引。格式：
```
## 乾为天
- 初九：潜龙勿用
- 九二：见龙在田，利见大人
- 九三：君子终日乾乾，夕惕若厉，无咎
- 九四：或跃在渊，无咎
- 九五：飞龙在天，利见大人
- 上九：亢龙有悔
- 用九：群龙无首，吉

## 坤为地
- 初六：履霜，坚冰至
- 六二：直方大，不习无不利
...
```

### references/jiegu-guide.md

解卦方法指引，包含：
- 卦辞解读原则
- 动爻爻辞的权重
- 变卦分析思路
- 传统注解引用（如《周易本义》等经典解读）
- 不同动爻数量的解卦规则

## 解卦逻辑规则

根据动爻数量，采用不同的解卦侧重：

1. **无动爻**：以本卦卦辞为主
2. **一个动爻**：以该动爻爻辞为主
3. **两个动爻**：以两个爻辞为主，上爻为主
4. **三个动爻**：本卦卦辞为体，变卦卦辞为用
5. **四个动爻**：以变卦中两个不变爻辞为主，下爻为主
6. **五个动爻**：以变卦中一个不变爻辞为主
7. **六个动爻**：
   - 乾卦六爻全动 → 用"用九"爻辞（"群龙无首，吉"）
   - 坤卦六爻全动 → 用"用六"爻辞（"利永贞"）
   - 其他卦六爻全动（游魂卦）→ 以变卦卦辞为主

## 三不占原则

SKILL.md 中明确要求 agent 在占卜前检查：
1. **不诚不占** — 心中无敬意、不真诚者不占
2. **不义不占** — 所问之事不合道义者不占
3. **不疑不占** — 心中无疑问、无困惑者不占

不符合原则时，agent 应拒绝占卜并说明原因。

## 部署方式

- Hermes Agent：放到 `~/.hermes/skills/` 目录（自动发现）
- opencode：放到 `~/.config/opencode/skills/` 目录
- 后续可发布到 Skills Hub（`hermes skills publish`）

## 后续扩展

- 报数起卦（scripts/qigua.py --method number）
- 时间起卦（scripts/qigua.py --method time）
- 文字笔画起卦
