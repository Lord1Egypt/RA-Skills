# 📥 思维模型库 - 安装指南

---

## 🔧 安装方式

### 方式 1: ClawHub CLI 安装（推荐）

```bash
# 1. 安装技能
clawhub install mental-models

# 2. 验证安装
clawhub list

# 3. 查看技能
cd skills/mental-models/
cat README.md
```

### 方式 2: 手动安装

```bash
# 1. 克隆/下载技能
git clone https://github.com/openclaw/openclaw.git
cd openclaw/workspace/docs/mental-models/

# 2. 复制到技能目录
cp -r * ~/.openclaw/workspace/skills/mental-models/

# 3. 验证
ls ~/.openclaw/workspace/skills/mental-models/
```

### 方式 3: 直接使用

无需安装，直接访问：
```
/home/admin/.openclaw/workspace/docs/mental-models/
```

---

## ✅ 验证安装

```bash
# 检查文件是否存在
ls skills/mental-models/README.md
ls skills/mental-models/MODEL-CARDS.md
ls skills/mental-models/CASE-STUDIES.md

# 查看模型数量
ls skills/mental-models/*.md | wc -l
# 应该输出：29（25 个模型 + 4 个文档）
```

---

## 🚀 快速开始

### 第一步：了解整体
```bash
cat skills/mental-models/README.md
```

### 第二步：快速浏览
```bash
cat skills/mental-models/MODEL-CARDS.md
```

### 第三步：学习选择
```bash
cat skills/mental-models/FLOWCHART.md
```

### 第四步：实战应用
```bash
# 选择一个场景组合
cat skills/mental-models/MODEL-COMBOS.md

# 学习经典案例
cat skills/mental-models/CASE-STUDIES.md
```

---

## 📚 文件结构

```
mental-models/
├── README.md                    # 总导航
├── SKILL.md                     # 技能说明
├── INSTALL.md                   # 安装指南（本文件）
├── MODEL-CARDS.md              # 模型索引卡
├── CASE-STUDIES.md             # 实战案例库
├── MODEL-COMBOS.md             # 模型组合包
├── FLOWCHART.md                # 选择流程图
├── first-principles.md         # 第一性原理
├── systems-thinking.md         # 系统思维
├── second-order-effects.md     # 二阶效应
├── pestel-analysis.md          # PESTEL 分析
├── swot-analysis.md            # SWOT 分析
├── porters-five-forces.md      # 波特五力
├── mece-principle.md           # MECE 原则
├── occams-razor.md             # 奥卡姆剃刀
├── hans-razor.md               # 汉隆剃刀
├── inversion.md                # 逆向思维
├── game-theory.md              # 博弈论
├── comparative-advantage.md    # 比较优势
├── opportunity-cost.md         # 机会成本
├── lean-startup.md             # 精益创业
├── cycle-theory.md             # 周期理论
├── power-law.md                # 幂律分布
├── antifragile.md              # 反脆弱
├── critical-mass.md            # 临界质量
├── long-term-thinking.md       # 长期主义
├── probabilistic-thinking.md   # 概率思维
├── bayes-theorem.md            # 贝叶斯定理
├── survivorship-bias.md        # 幸存者偏差
├── network-effects.md          # 网络效应
├── blue-ocean.md               # 蓝海战略
└── hot-topic-classify.md       # 热点分类
```

---

## 🔍 常见问题

### Q: 需要付费吗？
A: 完全免费，开源使用。

### Q: 需要编程基础吗？
A: 不需要，所有模型都是思维框架，无需编程。

### Q: 如何应用到实际工作？
A: 参考 `MODEL-COMBOS.md` 选择场景组合，直接套用。

### Q: 如何贡献新模型？
A: 提交 PR 到 https://github.com/openclaw/openclaw

### Q: 如何更新？
A: `clawhub update mental-models`

---

## 📞 获取帮助

- 查看文档：`cat README.md`
- 查看案例：`cat CASE-STUDIES.md`
- GitHub Issues: https://github.com/openclaw/openclaw/issues

---

**祝学习愉快！** 🎯
