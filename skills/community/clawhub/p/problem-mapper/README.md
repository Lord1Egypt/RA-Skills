# Problem-Mapper 问题图谱 🗺️

**系统化定义问题、设定成功标准、识别风险的决策前置工具**

---

## 快速开始

### 使用方式

**方式一：直接对话**
```
@ant 使用 problem-mapper 分析这个问题：[你的问题]
```

**方式二：GitHub 获取**
```
git clone git@github.com:lj22503/one-person-ceo-skills.git
cd skills/problem-mapper
```

**方式三：ClawHub 安装**
```
clawhub install problem-mapper
```

---

## 核心架构

### 四阶段框架

```
【阶段 0：问题淬炼】→ 这是真问题吗？
        ↓
【阶段 1：问题定义】→ 边界/范围/利益相关方
        ↓
【阶段 2：成功标准】→ 定性描述 + 量化 KPI
        ↓
【阶段 3：挑战评估】→ 风险地图 + 优先级
        ↓
【阶段 4：方案生成】→ 方案方向 + MVP 验证计划
```

---

## 文件夹结构

```
problem-mapper/
├── SKILL.md                      # 核心技能定义
├── README.md                     # 本文件
├── examples/                     # 示例库
│   └── case-study.md            # 实战案例（蚂蚁投顾/职业转型/产品设计）
├── references/                   # 参考文档
│   ├── five-clarifying-questions.md  # 五大澄清问题详解
│   └── risk-mapping.md          # 三维度风险评估指南
└── templates/                    # 模板文件
    └── problem-map-template.md  # 问题地图模板
```

---

## 使用场景

| 场景 | 推荐使用 | 示例 |
|------|---------|------|
| 重大决策前 | ✅ 强烈推荐 | 投资/职业/战略决策 |
| 战略模糊时 | ✅ 强烈推荐 | 方向不清晰，需要澄清 |
| 复杂问题 | ✅ 推荐 | 多因素交织，难以拆解 |
| 产品规划 | ✅ 推荐 | 从 0 到 1 设计 |
| 面试准备 | ✅ 推荐 | 系统分析目标公司 |
| 简单问题 | ❌ 不推荐 | 过度分析 |

---

## 核心功能

### 五大澄清问题（阶段 0）

| 问题 | 目的 | 示例 |
|------|------|------|
| （证据） | 确保基于事实 | "是否有具体现象作为例证？" |
| （视角） | 明确分析角度 | "从哪个视角审视？用户/行业/时间？" |
| （联系） | 定位价值链环节 | "影响价值链的哪个环节？" |
| （猜想） | 挑战既有假设 | "这是否重新定义获胜关键？" |
| （相关） | 明确最终目的 | "解决这个问题的最终目的是什么？" |

### 三维度风险评估（阶段 3）

| 维度 | 核心风险 | 示例 |
|------|---------|------|
| 用户与市场 | 用户不接受/市场不认可 | 信任建立的悖论、行为改变的惰性 |
| 竞争与商业 | 竞争加剧/商业模式不可持续 | 策略趋同化、利益协调困难 |
| 技术与合规 | 技术不可行/合规不通过 | 合规边界、系统复杂性 |

---

## 实战案例

### 案例 1：蚂蚁投顾面试准备

**输入：**
```
@ant 使用 problem-mapper 分析蚂蚁投顾面临的 4 个核心问题
```

**输出：**
- 每个问题的四阶段分析报告
- 优先级排序（P0/P1/P2）
- MVP 验证计划
- 面试回答框架

**详见：** `examples/case-study.md`

### 案例 2：职业转型决策

**输入：**
```
@ant 使用 problem-mapper 帮我分析是否应该从大厂跳槽到创业公司
```

**输出：**
- 问题淬炼（五大澄清问题）
- 问题定义（利益相关方/边界）
- 成功标准（定性 + 量化）
- 挑战评估（风险地图）
- 方案生成（3 个方案 + 决策建议）

**详见：** `examples/case-study.md`

---

## 与其他 Skill 的组合使用

### 组合 1：Problem-Mapper + Decision-System

```
1. problem-mapper → 诊断问题本质
2. decision-maker → 基于问题树做决策
3. principle-builder → 沉淀决策原则
```

**适用场景：** 重大决策前

### 组合 2：Problem-Mapper + Financial-Product-Workflow

```
1. problem-mapper → 定义产品问题
2. financial-product-workflow → 执行 6 节点工作流
```

**适用场景：** 金融产品从 0 到 1 设计

### 组合 3：Problem-Mapper + JD-Translator

```
1. jd-translator → 分析 JD 背后的问题
2. problem-mapper → 系统分析目标公司/岗位
```

**适用场景：** 面试准备

---

## 常见问题

### Q1：Problem-Mapper 适合什么问题？

**A：** 适合重大决策/战略模糊/复杂问题。简单问题不推荐使用，避免过度分析。

### Q2：四阶段框架必须完整走完吗？

**A：** 建议完整走，但时间紧迫时可以简化：
- 最少：阶段 0（问题淬炼）+ 阶段 2（成功标准）
- 推荐：阶段 0-3（不含方案生成）
- 完整：阶段 0-4

### Q3：如何量化成功标准？

**A：** 从三个维度思考：
- 用户价值：转化率/留存率/NPS
- 商业价值：AUM/收入/LTV
- 行业影响：引用次数/标杆案例

### Q4：优先级排序用什么方法？

**A：** 推荐 RICE 评分法：
- RICE 得分 = (Reach × Impact × Confidence) / Effort
- 🔴 P0：得分>50
- 🟡 P1：得分 20-50
- 🟢 P2：得分<20

---

## 更新日志

- v1.0.0 (2026-03-30): 初始版本
  - 四阶段框架（问题淬炼→问题定义→成功标准→挑战评估→方案生成）
  - 五大澄清问题（证据/视角/联系/猜想/相关）
  - 三维度风险评估（用户/竞争/技术合规）
  - MVP 验证计划（分步推进 + 量化指标）
  - 实战案例（蚂蚁投顾/职业转型/产品设计）

---

## 相关资源

- `references/five-clarifying-questions.md` - 五大澄清问题详解
- `references/risk-mapping.md` - 三维度风险评估指南
- `examples/case-study.md` - 实战案例分析
- `templates/problem-map-template.md` - 问题地图模板

---

*问题图谱不是寻找答案，而是澄清问题。问题清晰了，答案往往自然浮现。*

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

**Copyright (c) 2026 燃冰 (燃冰 & ant)**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**简单来说：**
- ✅ 你可以自由使用、修改、分发、商用
- ✅ 需要保留原作者版权和许可证声明
- ❌ 不提供任何担保，使用风险自负

详见 [LICENSE](LICENSE) 和 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 🔗 相关资源

- `references/five-clarifying-questions.md` - 五大澄清问题详解
- `references/risk-mapping.md` - 三维度风险评估指南
- `examples/case-study.md` - 实战案例分析
- `templates/problem-map-template.md` - 问题地图模板

🔗
