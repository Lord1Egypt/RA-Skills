#!/bin/bash
# P1 剩余技能批量优化脚本
# 为每个技能创建标准化的 scripts/calculators/examples

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
    
    # 创建 scripts 目录
    mkdir -p "$skill/scripts"
    
    # 创建 calculators 目录
    mkdir -p "$skill/calculators"
    
    # 创建示例文件（2 个）
    mkdir -p "$skill/examples"
    
    # 创建 README.md（如果不存在）
    if [ ! -f "$skill/README.md" ]; then
        cat > "$skill/README.md" << 'EOF'
# 技能包

> 基于经典投资理论的核心技能

---

## 📁 目录结构

```
./
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

1. 查看技能定义：`cat SKILL.md`
2. 查看示例：`cat examples/*.md`
3. 使用模板：`cat templates/*.md`
4. 参考理论：`cat references/*.md`
5. 使用工具：`python scripts/*.py`

---

## 📊 技能功能

详见 `SKILL.md`。

---

## 🔗 相关技能

详见 `SKILL.md` 的"related_skills"字段。

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

*详见 SKILL.md 完整文档。*
EOF
    fi
    
    echo "  Created directories for $skill"
done

echo "Done!"
