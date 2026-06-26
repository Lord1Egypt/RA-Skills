# 黄大仙灵签

> **一签一解，心诚则灵。**

香港黄大仙祠同款灵签，共100支完整签文，带详细解签。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai/skills/huangdaxian-lingqian-skill)
[![Version](https://img.shields.io/badge/version-2.0.0-green)]()

---

## 🎯 一句话说明

装上这个 Skill，问它抽签或解签，它会按传统格式输出：**签号、签题、签诗、典故、整体吉凶、分类详解（事业/姻缘/财运/健康/出行等）**，一签一解，不跳项。

---

## ✨ 核心能力

- **随机抽签**：心诚则灵，随机抽取一支签
- **指定签号**：直接查询第X签
- **分类解签**：事业/姻缘/财运/健康/出行/家宅/学业/流年
- **典故解读**：每支签皆有典故出处

---

## 🚀 安装使用

### OpenClaw CLI 安装
```bash
# 安装 skill
clawhub install huangdaxian-lingqian-skill

# 查看帮助
cat SKILL.md
```

### 直接使用
```
帮我抽一签看看最近的事业运
```
```
我想问事业，抽一签
```
```
我要第25签
```

### CLI 抽签器
```bash
# 随机抽签
python references/huangdaxian.py

# 抽指定签号
python references/huangdaxian.py --number 25

# 查看帮助
python references/huangdaxian.py --help
```

---

## 📋 签文体系

| 类型 | 数量 |
|------|------|
| 上上签 | 3支 |
| 上吉签 | 12支 |
| 中吉签 | 30支 |
| 中平签 | 37支 |
| 下下签 | 18支 |
| **总计** | **100支** |

---

## 📁 文件结构

```
├── SKILL.md              # OpenClaw Skill 定义（输出协议+完整格式）
├── README.md             # 本文件
├── requirements.txt      # Python 依赖
├── .clawhubignore        # ClawHub 忽略规则
└── references/           # 参考资源
    └── huangdaxian.py    # CLI 抽签器（内置100签数据）
```

---

## 📜 License

MIT License - 自由使用、修改和分发

---

<div align="center">

**一签一解，心诚则灵。**

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai/skills/huangdaxian-lingqian-skill)

</div>
