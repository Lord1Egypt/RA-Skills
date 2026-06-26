---
name: package-design
description: 包装设计能力；支持包装方案设计、材料选择、法规审核；当进行产品包装设计或包材选型时使用
dependency:
  python:
    - pandas==1.5.0
  system:
    - mkdir -p data/package
---

# 包装设计

## 任务目标
- 本技能用于：设计产品包装方案和选型包材
- 核心能力：包装结构设计、材料选择、法规审核
- 触发条件：新品包装设计、包材变更、法规符合性评估

## 数据来源

### 包装材料与法规查询

使用 `web_search` 获取相关信息：

```
# 包装材料
web_search(query="食品包装材料 标准 GB")
web_search(query="食品接触材料 法规 要求")
web_search(query="可降解包装 材料 供应商")

# 包装设计
web_search(query="食品包装 设计 规范 要求")
web_search(query="预包装食品 标签 标注 规范")
web_search(query="食品包装 印刷 法规 限制")
```

## 数据存储

包装设计数据保存在工作区 `data/package/` 目录：
- `package_specs.json` - 包装规格
- `material_list.csv` - 材料清单
- `compliance_check.md` - 合规检查

## 操作步骤

### 1. 需求分析
1. 明确产品特性和保护需求
2. 了解销售渠道和展示要求
3. 确定包装规格和数量

### 2. 方案设计
1. 选择包装结构和形式
2. 确定包材类型和规格
3. 设计包装展开图

### 3. 材料选型
1. 评估包材性能（阻隔、强度等）
2. 对比成本和供应商
3. 确认材料合规性

### 4. 法规审核
1. 核对标签标识要求
2. 检查食品接触材料合规
3. 确认广告宣传合规

## 资源索引
- 包装计算脚本：见 [scripts/package_calculator.py](scripts/package_calculator.py)
- 法规检查清单：见 [references/package_regulations.md](references/package_regulations.md)
- 材料选择指南：见 [references/material_selection.md](references/material_selection.md)

## 注意事项
- 确保食品接触材料合规
- 标签信息符合GB 7718要求
- 关注环保和可持续发展趋势
