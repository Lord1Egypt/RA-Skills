# bias-detector 技能包

> 基于《思考，快与慢》- 丹尼尔·卡尼曼的认知偏差识别技能

---

## 📁 目录结构

```
bias-detector/
├── SKILL.md                      # 技能定义（核心）
├── README.md                     # 本文件（目录导航）
├── examples/                     # 示例集合
│   └── loss-decision-example.md  # 损失厌恶决策示例
├── references/                   # 参考资料
│   └── cognitive-biases.md       # 认知偏差详解
├── templates/                    # 模板文件
│   └── decision-checklist.md     # 决策检查清单
├── scripts/                      # 计算脚本（待创建）
│   └── bias-scorer.py            # 偏差评分脚本
└── calculators/                  # 计算工具（待创建）
    └── bias-impact.md            # 偏差影响计算
```

---

## 🚀 快速开始

### 1. 查看技能定义
```bash
cat SKILL.md
```

### 2. 查看示例
```bash
cat examples/loss-decision-example.md
```

### 3. 使用模板
```bash
cat templates/decision-checklist.md
```

### 4. 参考理论
```bash
cat references/cognitive-biases.md
```

---

## 📊 技能功能

**核心功能**：识别 8 种核心认知偏差

**8 大偏差**：
1. 损失厌恶
2. 锚定效应
3. 确认偏误
4. 处置效应
5. 从众心理
6. 过度自信
7. 代表性偏差
8. 可得性偏差

**输入**：
- 投资想法
- 决策理由
- 当前仓位

**输出**：
- 偏差识别
- 风险等级
- 改善建议

---

## 🔗 相关技能

- **decision-checklist**: 决策清单（综合检查）
- **second-level-thinker**: 第二层思维（逆向思考）
- **moat-evaluator**: 护城河评估（客观分析）
- **value-analyzer**: 价值分析（基本面）

---

## 🧪 使用示例

**输入**：
```
我想买入 XX 股票，因为：
1. 最近涨得很好
2. 朋友推荐
3. 新闻说前景好
```

**输出**：
```
【认知偏差检查】

识别出的偏差：
1. 从众心理（中风险）- 朋友推荐
2. 可得性偏差（中风险）- 新闻影响
3. 代表性偏差（低风险）- 近期表现

建议：
1. 独立思考，不盲从
2. 减少媒体暴露
3. 深入基本面分析
```

---

## ⚠️ 常见错误

1. **不承认自己有偏差**：认为自己理性
2. **只在亏损时检查**：盈利时不反思
3. **知道但做不到**：知行不一
4. **过度依赖单一偏差**：忽视其他
5. **忽视环境因素**：被市场情绪影响
6. **缺乏持续练习**：不形成习惯

详见 `SKILL.md` 的"⚠️ 常见错误"章节。

---

## 📚 学习路径

1. 阅读 `SKILL.md` 了解 8 大偏差
2. 查看 `examples/` 学习实战
3. 使用 `templates/` 进行检查
4. 参考 `references/` 深入理论
5. 使用 `scripts/` 和 `calculators/` 评分

---

## 🛠️ 工具脚本

### bias-scorer.py
```bash
# 偏差评分
python scripts/bias-scorer.py --biases "loss_aversion,confirmation" --severity "high,medium"
```

### bias-impact.md
```markdown
# 偏差影响计算
偏差数量 × 风险等级 = 决策风险
0-2 个：低风险
3-5 个：中风险
6-8 个：高风险
```

---

## 📊 版本历史

- v2.0.0 (2026-03-19): 按 SKILL-STANDARD-v2.md 重构
- v1.0.0 (2026-03-13): 初始版本

---

*认知偏差是投资的最大敌人。承认偏差，持续检查，理性决策。* 🧠
