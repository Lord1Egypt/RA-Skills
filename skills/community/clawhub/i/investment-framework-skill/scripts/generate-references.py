#!/usr/bin/env python3
"""
批量生成 references 基础内容
"""

import os

BASE_DIR = '/home/admin/.openclaw/workspace/investment-framework-skill'

# 技能信息
SKILLS_INFO = {
    'stock-picker': {
        'name': '选股专家',
        'theory': '彼得·林奇投资理论',
        'book': '《彼得·林奇的成功投资》',
    },
    'simple-investor': {
        'name': '简单投资者',
        'theory': '邱国鹭投资最简单的事',
        'book': '《投资中最简单的事》',
    },
    'intrinsic-value-calculator': {
        'name': '内在价值计算器',
        'theory': '格雷厄姆 - 多德估值理论',
        'book': '《证券分析》',
    },
    'moat-evaluator': {
        'name': '护城河评估师',
        'theory': '巴菲特护城河理论',
        'book': '《巴菲特致股东的信》',
    },
    'asset-allocator': {
        'name': '资产配置师',
        'theory': '马尔基尔漫步华尔街',
        'book': '《漫步华尔街》',
    },
    'portfolio-designer': {
        'name': '组合设计师',
        'theory': '耶鲁捐赠基金模式',
        'book': '《机构投资者的创新之路》',
    },
    'global-allocator': {
        'name': '全球配置师',
        'theory': '达斯特资产配置艺术',
        'book': '《资产配置的艺术》',
    },
    'industry-analyst': {
        'name': '行业分析师',
        'theory': '肖璟行业分析方法',
        'book': '《如何快速了解一个行业》',
    },
    'cycle-locator': {
        'name': '周期定位师',
        'theory': '达利欧经济机器运行',
        'book': '《经济机器是怎样运行的》',
    },
    'future-forecaster': {
        'name': '未来预测师',
        'theory': '凯文·凯利趋势预测',
        'book': '《必然》《失控》',
    },
    'decision-checklist': {
        'name': '决策清单',
        'theory': '芒格多元思维模型',
        'book': '《穷查理宝典》',
    },
    'bias-detector': {
        'name': '认知偏差检测器',
        'theory': '卡尼曼行为经济学',
        'book': '《思考，快与慢》',
    },
    'second-level-thinker': {
        'name': '二阶思维者',
        'theory': '霍华德·马克斯逆向思维',
        'book': '《投资最重要的事》',
    },
}

def generate_theory(skill_key, info):
    """生成 theory.md 基础内容"""
    return f"""# {info['theory']}

**基于{info['book']}**

---

## 核心概念

### 1. 主要理念

［待补充：核心理念详解］

### 2. 关键原则

［待补充：关键原则列表］

### 3. 应用方法

［待补充：实际应用方法］

---

## 与其他理论的关系

［待补充：相关理论对比］

---

## 参考资料

- {info['book']}
- 相关研究论文
- 行业最佳实践

---

*最后更新：2026-03-20*
"""

def generate_examples(skill_key, info):
    """生成 examples.md 基础内容"""
    return f"""# {info['name']}使用示例

---

## 基础用法

### 示例 1：基础分析

**输入**：
```bash
python3 {skill_key}/scripts/analyze-{skill_key.split('-')[0]}.py 600519.SH
```

**预期输出**：
```
［待补充：实际输出示例］
```

---

## 进阶用法

### 示例 2：批量分析

［待补充：批量处理示例］

---

### 示例 3：与其他技能组合

［待补充：组合使用示例］

---

## 输出解读

### 关键指标

［待补充：指标解释］

### 判断标准

［待补充：判断标准］

---

## 最佳实践

1. ［待补充：最佳实践 1］
2. ［待补充：最佳实践 2］
3. ［待补充：最佳实践 3］

---

*最后更新：2026-03-20*
"""

def generate_faq(skill_key, info):
    """生成 faq.md 基础内容"""
    return f"""# {info['name']}常见问题 (FAQ)

---

## 基础问题

### Q1: 什么是{info['name']}？

**A**: ［待补充：基本定义和用途］

---

### Q2: 何时使用{info['name']}？

**A**: ［待补充：使用场景］

---

## 进阶问题

### Q3: 如何解读分析结果？

**A**: ［待补充：结果解读方法］

---

### Q4: 有什么局限性？

**A**: ［待补充：局限性说明］

---

## 实战问题

### Q5: 实际应用中需要注意什么？

**A**: ［待补充：实战注意事项］

---

## 工具使用

### Q6: 常见问题排查？

**A**: ［待补充：故障排查步骤］

---

*最后更新：2026-03-20*
"""

def main():
    """主函数"""
    for skill_key, info in SKILLS_INFO.items():
        refs_dir = os.path.join(BASE_DIR, skill_key, 'references')
        os.makedirs(refs_dir, exist_ok=True)
        
        # 生成 theory.md
        theory_path = os.path.join(refs_dir, 'theory.md')
        if os.path.exists(theory_path) and os.path.getsize(theory_path) < 100:
            with open(theory_path, 'w', encoding='utf-8') as f:
                f.write(generate_theory(skill_key, info))
            print(f"✅ {skill_key}/theory.md")
        
        # 生成 examples.md
        examples_path = os.path.join(refs_dir, 'examples.md')
        if os.path.exists(examples_path) and os.path.getsize(examples_path) < 100:
            with open(examples_path, 'w', encoding='utf-8') as f:
                f.write(generate_examples(skill_key, info))
            print(f"✅ {skill_key}/examples.md")
        
        # 生成 faq.md
        faq_path = os.path.join(refs_dir, 'faq.md')
        if os.path.exists(faq_path) and os.path.getsize(faq_path) < 100:
            with open(faq_path, 'w', encoding='utf-8') as f:
                f.write(generate_faq(skill_key, info))
            print(f"✅ {skill_key}/faq.md")
    
    print("\n🎉 References 基础内容生成完成")

if __name__ == '__main__':
    main()
