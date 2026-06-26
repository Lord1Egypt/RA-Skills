# Home Design Skill - 房屋装修设计技能

## 功能概述

本技能提供完整的房屋装修设计服务，包括：

- ✅ 户型分析与优化建议
- ✅ 空间布局规划
- ✅ 装修风格推荐
- ✅ 设计大纲生成
- ✅ 施工图纸指导
- ✅ 材料选择建议
- ✅ 预算规划参考

## 使用方法

### 1. 需求收集

首先使用需求收集模板了解用户需求：

```markdown
请提供以下信息：
- 房屋面积和户型
- 居住人口和年龄结构
- 功能需求（书房、儿童房等）
- 风格偏好
- 预算范围
```

或直接使用 `assets/requirements_template.md` 模板。

### 2. 户型分析

使用分析脚本生成户型报告：

```bash
python scripts/analyze_floor_plan.py \
  --area "100㎡" \
  --layout "3 室 2 厅 2 卫" \
  --orientation "南北通透" \
  --output analysis_report.md
```

### 3. 生成设计大纲

根据用户需求生成设计大纲：

```bash
python scripts/generate_design_outline.py \
  --area "100㎡" \
  --rooms "3 室 2 厅 2 卫" \
  --style "现代简约" \
  --residents "3 人" \
  --requirements "书房、儿童房" \
  --budget "30 万" \
  --output design_outline.md
```

### 4. 输出交付物

标准交付物包括：

1. **户型分析报告** - 优劣势分析、动线规划
2. **设计大纲** - 详细的设计方案
3. **平面布置建议** - 家具布局方案
4. **材料清单** - 主材、辅材建议
5. **预算分配** - 各项目预算比例
6. **施工指导** - 工艺流程和验收标准

## 文件结构

```
home-design/
├── SKILL.md                    # 技能主文件
├── scripts/
│   ├── analyze_floor_plan.py   # 户型分析脚本
│   └── generate_design_outline.py  # 设计大纲生成
├── references/
│   ├── style_guide.md          # 装修风格指南
│   ├── ergonomics.md           # 人体工程学尺寸
│   ├── materials.md            # 材料选择指南
│   └── construction.md         # 施工工艺标准
└── assets/
    └── requirements_template.md  # 需求收集模板
```

## 触发场景

以下用户请求应触发本技能：

- "帮我设计一下房子装修"
- "这个户型怎么布局比较好"
- "生成装修效果图"
- "需要施工图纸"
- "如何最大化利用空间"
- "装修风格推荐"
- "装修预算规划"
- "XXX 平米的房子怎么装修"

## 注意事项

1. **结构安全** - 承重墙不可拆除
2. **防水要求** - 卫生间、厨房防水必须到位
3. **环保标准** - 优先选择 E0/ENF 级环保材料
4. **预算控制** - 建议预留 10-15% 的备用金
5. **施工周期** - 一般 2-4 个月，视面积和复杂度而定

## 扩展功能

未来可扩展：

- [ ] 3D 效果图生成（集成 Blender/Three.js）
- [ ] CAD 施工图生成（集成 CAD 库）
- [ ] VR 全景漫游
- [ ] 预算自动计算
- [ ] 材料清单导出 Excel
- [ ] 施工进度管理

## 版本

v1.0 - 基础功能版本
- 户型分析
- 设计大纲生成
- 参考资料库
