#!/bin/bash
# P1 技能批量优化脚本
# 为每个 P1 技能创建标准化的 README.md 和目录结构

SKILLS=(
    "cycle-locator"
    "decision-checklist"
    "future-forecaster"
    "global-allocator"
    "industry-analyst"
    "intrinsic-value-calculator"
    "moat-evaluator"
    "portfolio-designer"
    "second-level-thinker"
    "simple-investor"
    "stock-picker"
    "value-analyzer"
)

for skill in "${SKILLS[@]}"; do
    echo "Processing $skill..."
    
    # 创建 README.md 模板
    cat > "$skill/README.md" << 'EOF'
# {{SKILL_NAME}} 技能包

> 基于{{BOOK}}的{{DESCRIPTION}}

---

## 📁 目录结构

```
{{SKILL}}/
├── SKILL.md                      # 技能定义（核心）
├── README.md                     # 本文件（目录导航）
├── examples/                     # 示例集合
├── references/                   # 参考资料
├── templates/                    # 模板文件
├── scripts/                      # 计算脚本
└── calculators/                  # 计算工具
```

---

## 🚀 快速开始

### 1. 查看技能定义
```bash
cat SKILL.md
```

### 2. 查看示例
```bash
cat examples/*.md
```

### 3. 使用模板
```bash
cat templates/*.md
```

### 4. 参考理论
```bash
cat references/*.md
```

---

## 📊 技能功能

**核心功能**：{{CORE_FUNCTION}}

**输入**：
- {{INPUT_1}}
- {{INPUT_2}}

**输出**：
- {{OUTPUT_1}}
- {{OUTPUT_2}}

---

## 🔗 相关技能

- **related-skill-1**: 说明
- **related-skill-2**: 说明

---

## ⚠️ 常见错误

详见 `SKILL.md` 的"⚠️ 常见错误"章节。

---

## 📚 学习路径

1. 阅读 `SKILL.md` 了解功能
2. 查看 `examples/` 学习实战
3. 使用 `templates/` 制定方案
4. 参考 `references/` 深入理论
5. 使用 `scripts/` 和 `calculators/` 计算

---

## 📊 版本历史

- v2.0.0 (2026-03-19): 按 SKILL-STANDARD-v2.md 重构
- v1.0.0 (2026-03-13): 初始版本

---

*{{QUOTE}}*
EOF
    
    echo "  Created README.md for $skill"
done

echo "Done!"
