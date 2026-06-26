# HOI4 本地化完整指南

## 目录

1. [文件结构](#文件结构)
2. [YML 格式规范](#yml-格式规范)
3. [语言代码](#语言代码)
4. [文本格式标记](#文本格式标记)
5. [变量引用](#变量引用)
6. [本地化类型](#本地化类型)
7. [最佳实践](#最佳实践)

---

## 文件结构

```
localisation/
├── english/
│   ├── focus_l_english.yml          # 焦点名称
│   ├── ideas_l_english.yml          # 民族精神
│   ├── events_l_english.yml         # 事件文本
│   ├── decisions_l_english.yml      # 决议名称
│   └── {mod}_l_english.yml          # mod专用
│
├── simp_chinese/
│   ├── focus_l_simp_chinese.yml
│   ├── ideas_l_simp_chinese.yml
│   └── {mod}_l_simp_chinese.yml
│
└── {language}/
    └── {mod}_l_{language}.yml
```

---

## YML 格式规范

### 基础格式

```yaml
l_english:
 key_name:0 "Display Text"
 key_name_desc:0 "Description text goes here..."
```

### 格式要点

1. **冒号后必须有空格**：
   ```yaml
   # 正确
   focus_id:0 "Focus Name"
   
   # 错误
   focus_id:0"Focus Name"
   focus_id:0"Focus Name"
   ```

2. **版本号**：`0` 是标准版本号，也可以使用 `1`、`2` 等
   
3. **引号**：文本必须用双引号包裹

4. **换行**：每个条目独占一行

---

## 语言代码

| 代码 | 语言 | 文件后缀 |
|------|------|----------|
| `l_english` | 英语 | `_l_english.yml` |
| `l_simp_chinese` | 简体中文 | `_l_simp_chinese.yml` |
| `l_french` | 法语 | `_l_french.yml` |
| `l_german` | 德语 | `_l_german.yml` |
| `l_spanish` | 西班牙语 | `_l_spanish.yml` |
| `l_japanese` | 日语 | `_l_japanese.yml` |
| `l_korean` | 韩语 | `_l_korean.yml` |
| `l_polish` | 波兰语 | `_l_polish.yml` |
| `l_russian` | 俄语 | `_l_russian.yml` |
| `l_braz_por` | 巴西葡语 | `_l_braz_por.yml` |

---

## 文本格式标记

### 颜色代码

```yaml
# 红、绿、蓝、黄、白、高亮、灰色、橙色、青色
red_text:0 "§R这是红色文本§!"
green_text:0 "§G这是绿色文本§!"
blue_text:0 "§B这是蓝色文本§!"
yellow_text:0 "§Y这是黄色文本§!"
white_text:0 "§W这是白色文本§!"
highlight:0 "§H这是高亮文本§!"
gray_text:0 "§g这是灰色文本§!"
orange_text:0 "§O这是橙色文本§!"
cyan_text:0 "§C这是青色文本§!"
```

### 常用颜色用途

| 颜色 | 代码 | 用途 |
|------|------|------|
| §G绿色 | §G | 正面效果、增益 |
| §R红色 | §R | 负面效果、惩罚 |
| §Y黄色 | §Y | 数值、重要信息 |
| §H高亮 | §H | 标题、关键词 |
| §B蓝色 | §B | 友方国家 |

### 文本样式

```yaml
# 换行
multiline_text:0 "第一行\n第二行\n第三行"

# 图标（使用效果图标）
with_icon:0 "获得 §Y+5%§! 稳定度\n£stability_texticon"

# Tab缩进（不常用）
tabbed_text:0 "标题:\t内容"
```

### 常用图标代码

```yaml
# 资源图标
£oil        # 石油
£aluminum   # 铝
£rubber     # 橡胶
£tungsten   # 钨
£steel      # 钢铁
£chromium   # 铬

# 政治图标
£pol_power  # 政治点数
£stability  # 稳定度
£war_support # 战争支持度

# 军事图标
£command_power # 指挥点数
£manpower   # 人力
£army_experience # 陆军经验
£navy_experience # 海军经验
£air_experience  # 空军经验

# 建筑图标
£civilian_factory  # 民用工厂
£military_factory  # 军用工厂
£infrastructure    # 基础设施
£air_base          # 空军基地
£naval_base        # 海军基地
```

---

## 变量引用

### 基础变量

```yaml
# 数字变量
gain_pp:0 "获得 §Y$VALUE$§! 政治点数"

# 国家名称
nation_name:0 "[Root.GetName] 完成了改革"

# 特定国家名
other_nation:0 "[GER.GetName] 对我们提出了要求"

# 领导人名称
leader_name:0 "[Root.GetLeader] 发表了演讲"
```

### 在代码中使用

```
# 效果中使用变量
custom_effect_tooltip = {
    text = gain_pp_tt
    add_political_power = var:gain_amount
}
```

```yaml
# 本地化变量
gain_pp_tt:0 "获得 §Y$VALUE$§! 政治点数"
```

### 复杂变量示例

```yaml
# 多变量文本
complex_text:0 "[Root.GetName] 将 §Y$AMOUNT$§! 个师部署到 $STATE$"

# 百分比显示
percentage_text:0 "稳定度: §G$PERCENT|%.1f$§!"
```

---

## 本地化类型

### 焦点 (Focus)

```yaml
l_english:
 # 焦点名称
 POL_seize_control_of_the_state:0 "掌控国家权力"
 
 # 焦点描述
 POL_seize_control_of_the_state_desc:0 "萨纳奇亚政权必须巩固其对国家各部门的控制..."
```

### 民族精神 (Ideas)

```yaml
l_english:
 # 精神名称
 POL_sanacja_regime:0 "萨纳奇亚政权"
 
 # 精神描述
 POL_sanacja_regime_desc:0 "皮尔斯基执政以来的威权统治..."
```

### 事件 (Events)

```yaml
l_english:
 # 事件标题
 poland_crisis.1_title:0 "但泽危机"
 
 # 事件描述
 poland_crisis.1_desc:0 "德国向我们提出了但泽归属问题..."
 
 # 选项文本
 poland_crisis.1_option_a:0 "拒绝他们的要求"
 poland_crisis.1_option_b:0 "接受他们的条件"
```

### 决议 (Decisions)

```yaml
l_english:
 # 决议名称
 POL_danzig_ultimatum:0 "但泽最后通牒"
 
 # 决议描述
 POL_danzig_ultimatum_desc:0 "向波兰发出最后通牒..."
```

### 修正值 (Modifiers)

```yaml
l_english:
 # 修正值名称
 POL_german_cooperation:0 "德波合作"
 
 # 修正值描述（可选）
 POL_german_cooperation_desc:0 "与德国建立了合作关系"
```

### 工具提示 (Tooltips)

```yaml
l_english:
 # 自定义提示
 POL_september_war_tt:0 "§H九月战役§!\n§Y德国将对波兰宣战§!"
```

---

## 最佳实践

### 1. 文件组织

```yaml
# 按功能分文件
focus_l_english.yml      # 焦点
ideas_l_english.yml      # 民族精神
events_l_english.yml     # 事件
decisions_l_english.yml  # 决议
```

### 2. 命名规范

```yaml
# 使用一致的命名前缀
POL_historical_focus      # 国家前缀
poland_crisis.1_title    # 事件命名空间.编号_类型
POL_german_cooperation   # modifier用国家前缀
```

### 3. 描述文本结构

```yaml
# 焦点描述通常包含：
# 1. 历史背景
# 2. 游戏效果说明
# 3. 后续影响提示
POL_seize_control_of_the_state_desc:0 "皮尔斯基执政以来的威权统治必须得到巩固。\n\n§H效果:§!\n§G+10%§! 政治点数增益\n§G+5%§! 稳定度\n§R+5%§! 消费品需求"
```

### 4. 中文本地化要点

```yaml
l_simp_chinese:
 # 使用中文标点
 focus_name:0 "掌控国家"
 
 # 避免全角字母数字
 bad_example:0 "获得１００点数"    # 错误
 good_example:0 "获得100点数"     # 正确
 
 # 保持术语一致性
 # stable → 稳定度
 # war_support → 战争支持度
 # political_power → 政治点数
 # consumer_goods → 消费品
```

### 5. 条件文本

```yaml
# 使用[Scope]处理条件性文本
# 注意：复杂条件文本通常在代码中处理
dynamic_text:0 "[Root.GetName]的改革"
```

---

## 完整示例文件

### focus_l_english.yml

```yaml
l_english:
 # 波兰焦点树
 POL_seize_control_of_the_state:0 "掌控国家权力"
 POL_seize_control_of_the_state_desc:0 "萨纳奇亚政权必须巩固其对国家各部门的控制，确保政权的稳定性。\n\n§H效果:§!\n§G+10%§! 政治点数增益\n§G+5%§! 稳定度\n我们可以创建阵营"
 
 POL_four_year_economic_plan:0 "四年经济计划"
 POL_four_year_economic_plan_desc:0 "实施全面的工业化计划，加强波兰的经济实力。\n\n§H效果:§!\n获得 §Y四年计划§! 民族精神\n§G+1§! 民用工厂"
```

### focus_l_simp_chinese.yml

```yaml
l_simp_chinese:
 # 波兰焦点树
 POL_seize_control_of_the_state:0 "掌控国家权力"
 POL_seize_control_of_the_state_desc:0 "萨纳奇亚政权必须巩固其对国家各部门的控制，确保政权的稳定性。\n\n§H效果:§!\n§G+10%§! 政治点数增益\n§G+5%§! 稳定度\n我们可以创建阵营"
 
 POL_four_year_economic_plan:0 "四年经济计划"
 POL_four_year_economic_plan_desc:0 "实施全面的工业化计划，加强波兰的经济实力。\n\n§H效果:§!\n获得 §Y四年计划§! 民族精神\n§G+1§! 民用工厂"
```

---

## 常见问题

### Q: 修改后不生效？

1. 检查文件编码（必须是 UTF-8 with BOM）
2. 检查冒号后空格
3. 检查引号闭合
4. 重启游戏

### Q: 如何查看已有的key？

- 英文：`localisation/english/`
- 使用文本搜索工具查找key

### Q: 如何处理特殊字符？

```yaml
# 使用转义或避免特殊字符
# YAML支持的转义字符
escape_example:0 "引号: \" 换行: \n"
```
