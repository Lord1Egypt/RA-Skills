# HOI4 本地化系统完整示例

本文档展示本地化系统的所有关键用法，包括格式、变量、颜色代码等。

---

## 📌 基础格式

### YML 文件结构

```yaml
# 文件编码：UTF-8 带 BOM
# 文件名格式：category_l_language.yml
# 例如：focus_l_english.yml

l_english:    # 语言标识（必需）
 
 # === 基础键值对 ===
 key_name:0 "Display Text"
 key_name_desc:0 "Description text..."
 
 # === 带变量的文本 ===
 variable_text:0 "We gained §Y[GetValue('amount')]§! political power."
 
 # === 多行文本 ===
 multiline:0 "First line\nSecond line\nThird line"
```

---

## 📌 语言代码

| 代码 | 语言 |
|------|------|
| `l_english` | 英语（默认） |
| `l_simp_chinese` | 简体中文 |
| `l_french` | 法语 |
| `l_german` | 德语 |
| `l_spanish` | 西班牙语 |
| `l_japanese` | 日语 |
| `l_korean` | 韩语 |
| `l_polish` | 波兰语 |
| `l_russian` | 俄语 |
| `l_braz_port` | 葡萄牙语 |

---

## 📌 颜色代码

### 基础颜色

```yaml
l_english:
 # === 文本颜色 ===
 red_text:0 "§RThis text is red§!"
 green_text:0 "§GThis text is green§!"
 blue_text:0 "§BThis text is blue§!"
 yellow_text:0 "§YThis text is yellow§!"
 highlight_text:0 "§HThis text is highlighted§!"
 orange_text:0 "§OThis text is orange§!"
 white_text:0 "§WThis text is white§!"
 gray_text:0 "§gThis text is gray§!"
 
 # === 用法示例 ===
 bonus_text:0 "Gain §G+10%§! political power gain."
 penalty_text:0 "§R-5%§! stability."
 warning_text:0 "§RWarning:§! This action cannot be undone."
```

### 颜色代码表

| 代码 | 颜色 | 用途 |
|------|------|------|
| §R | 红色 | 负面效果、警告 |
| §G | 绿色 | 正面效果、增益 |
| §B | 蓝色 | 科技、特殊信息 |
| §Y | 黄色 | 重要数值、强调 |
| §H | 高亮 | 提示、焦点 |
| §O | 橙色 | 特殊状态 |
| §W | 白色 | 普通文本（默认） |
| §g | 灰色 | 次要信息 |

---

## 📌 图标代码

### 常用图标

```yaml
l_english:
 # === 资源图标 ===
 oil_icon:0 "£oil  Oil"
 aluminum_icon:0 "£aluminum  Aluminum"
 rubber_icon:0 "£rubber  Rubber"
 tungsten_icon:0 "£tungsten  Tungsten"
 steel_icon:0 "£steel  Steel"
 chromium_icon:0 "£chromium  Chromium"
 
 # === 建筑图标 ===
 civilian_factory:0 "£civilian_factory  Civilian Factory"
 military_factory:0 "£military_factory  Military Factory"
 dockyard:0 "£dockyard  Dockyard"
 infrastructure:0 "£infrastructure  Infrastructure"
 air_base:0 "£air_base  Air Base"
 naval_base:0 "£naval_base  Naval Base"
 
 # === 政治图标 ===
 political_power:0 "£pol_power  Political Power"
 stability:0 "£stability  Stability"
 war_support:0 "£war_support  War Support"
 
 # === 军事图标 ===
 manpower:0 "£manpower  Manpower"
 army_xp:0 "£army_xp  Army Experience"
 navy_xp:0 "£navy_xp  Navy Experience"
 air_xp:0 "£air_xp  Air Experience"
 
 # === 综合示例 ===
 factory_text:0 "Build §Y2§! £civilian_factory Civilian Factories"
 resource_text:0 "Gain §Y+24§! £steel Steel"
 manpower_text:0 "Recruit §Y500K§! £manpower Manpower"
```

---

## 📌 变量插值

### GetValue 函数

```yaml
l_english:
 # === 基础变量 ===
 variable_example:0 "We gained §Y[GetValue('amount')]§! political power."
 
 # === 多变量 ===
 multi_variable:0 "We have §Y[GetValue('troops')]§! divisions and §Y[GetValue('ships')]§! ships."
 
 # === 计算 ===
 calculation:0 "Total: §Y[GetValue('base') * 1.5]§! units."
```

### 自定义效果提示

```hoi4
# 在效果中使用
custom_effect_tooltip = {
    localization_key = industrial_reward_tt
    VALUE = var:industrial_reward_amount
}
```

```yaml
# 本地化
l_english:
 industrial_reward_tt:0 "We gained §Y[VALUE]§! political power from industrial development."
```

---

## 📌 特殊格式

### 多行文本

```yaml
l_english:
 # === 使用 \n 换行 ===
 multiline_text:0 "First line\nSecond line\nThird line"
 
 # === 段落格式 ===
 paragraph:0 "This is the first paragraph.\n\nThis is the second paragraph."
 
 # === 列表格式 ===
 list_text:0 "Effects:\n§G+§! 10% Political Power\n§G+§! 5% Stability\n§R-§! 2% War Support"
```

### 条件文本

```yaml
l_english:
 # === 使用脚本效果实现 ===
 # 在效果中：
 # if = {
 #     limit = { has_government = fascism }
 #     set_temp_variable = { ideology_name = "Fascist" }
 # }
 # else = {
 #     set_temp_variable = { ideology_name = "Democratic" }
 # }
 
 conditional_text:0 "Our §Y[GetVariable('ideology_name')]§! government has taken power."
```

---

## 📌 实际示例

### 焦点本地化

```yaml
l_english:
 # === 焦点名称和描述 ===
 POL_industrial_base:0 "Polish Industrial Base"
 POL_industrial_base_desc:0 "Poland must industrialize to survive the coming storm. "
 
 POL_four_year_plan:0 "Four Year Plan"
 POL_four_year_plan_desc:0 "A comprehensive economic development plan to transform Poland into an industrial power."
 
 # === 效果提示 ===
 POL_four_year_plan_tt:0 "§YEffects:§!\n"
 POL_four_year_plan_tt:0 "§G+§! §Y2§! £civilian_factory Civilian Factories\n"
 POL_four_year_plan_tt:0 "§G+§! §Y1§! £military_factory Military Factory\n"
 POL_four_year_plan_tt:0 "§Y+10%§! Industrial Research Speed"
```

### 事件本地化

```yaml
l_english:
 # === 事件标题和描述 ===
 poland.1.t:0 "Eastward Expansion"
 poland.1.d:0 "The Soviet Union has demanded the territories of Eastern Poland. "
 poland.1.d:0 "Our military is not ready for a war with the Red Army. "
 poland.1.d:0 "We must decide: submit to their demands or face the consequences."
 
 # === 选项文本 ===
 poland.1.a:0 "We have no choice but to accept."
 poland.1.b:0 "Never! We will defend our homeland!"
 
 # === AI权重提示（调试用） ===
 poland.1.a_ai:0 "§R(AI Weight: 30)§!"
 poland.1.b_ai:0 "§R(AI Weight: 70)§!"
```

### Ideas 本地化

```yaml
l_english:
 # === 国家精神 ===
 POL_authoritarian_regime:0 "Authoritarian Regime"
 POL_authoritarian_regime_desc:0 "The Sanacja regime maintains tight control over Poland. "
 POL_authoritarian_regime_desc:0 "While providing stability, it limits political freedoms."
 
 # === 顾问 ===
 POL_military_advisor:0 "General Sosnkowski"
 POL_military_advisor_desc:0 "A veteran of the Polish-Soviet War, General Sosnkowski brings valuable military experience."
 
 # === 设计商 ===
 POL_arms_company:0 "Państwowe Zakłady Inżynierii"
 POL_arms_company_desc:0 "State Engineering Works - Poland's primary arms manufacturer."
```

---

## 📌 中文本地化

### 简体中文示例

```yaml
l_simp_chinese:
 # === 焦点 ===
 POL_industrial_base:0 "波兰工业基础"
 POL_industrial_base_desc:0 "波兰必须实现工业化才能在即将到来的风暴中生存。"
 
 POL_four_year_plan:0 "四年计划"
 POL_four_year_plan_desc:0 "一项全面的经济发展计划，旨在将波兰转变为工业强国。"
 
 # === 效果提示 ===
 POL_four_year_plan_tt:0 "§Y效果：§!\n"
 POL_four_year_plan_tt:0 "§G+§! §Y2§! £civilian_factory 民用工厂\n"
 POL_four_year_plan_tt:0 "§G+§! §Y1§! £military_factory 军用工厂\n"
 POL_four_year_plan_tt:0 "§Y+10%§! 工业研究速度"
 
 # === 事件 ===
 poland.1.t:0 "东方扩张"
 poland.1.d:0 "苏联要求东波兰的领土。我们的军队还没有准备好与红军作战。"
 poland.1.a:0 "我们别无选择，只能接受。"
 poland.1.b:0 "绝不！我们将保卫家园！"
 
 # === 民族精神 ===
 POL_authoritarian_regime:0 "威权政体"
 POL_authoritarian_regime_desc:0 "萨纳齐亚政权对波兰实行严格控制。虽然提供了稳定，但限制了政治自由。"
```

---

## 📌 高级技巧

### 动态数值显示

```hoi4
# 效果代码
set_variable = { var = reward_amount value = 150 }
custom_effect_tooltip = {
    localization_key = dynamic_reward_tt
    AMOUNT = var:reward_amount
}
```

```yaml
# 本地化
l_english:
 dynamic_reward_tt:0 "We received §Y[AMOUNT]§! £pol_power political power."
```

### 条件文本组合

```hoi4
# 效果代码
if = {
    limit = { has_war = yes }
    set_temp_variable = { war_status = "at war" }
}
else = {
    set_temp_variable = { war_status = "at peace" }
}
custom_effect_tooltip = {
    localization_key = war_status_tt
    STATUS = var:war_status
}
```

```yaml
l_english:
 war_status_tt:0 "Our nation is currently §Y[STATUS]§!"
```

---

## 📌 文件组织

### 推荐文件结构

```
localisation/
├── english/
│   ├── focus_l_english.yml          # 焦点
│   ├── ideas_l_english.yml          # 民族精神
│   ├── events_l_english.yml         # 事件
│   ├── decisions_l_english.yml      # 决议
│   ├── modifiers_l_english.yml      # 修正值
│   └── units_l_english.yml          # 单位
│
└── simp_chinese/
    ├── focus_l_simp_chinese.yml
    ├── ideas_l_simp_chinese.yml
    ├── events_l_simp_chinese.yml
    └── ...
```

### 命名规范

```
{category}_l_{language}.yml

示例：
focus_l_english.yml          # 焦点本地化
ideas_l_simp_chinese.yml     # 民族精神本地化
events_l_english.yml         # 事件本地化
```

---

## ✅ 最佳实践

### 1. 文件编码
- ✅ UTF-8 **带 BOM**
- ❌ 不要使用无 BOM 的 UTF-8
- ❌ 不要使用其他编码

### 2. 键命名规范
```
{TAG}_{name}              # 国家前缀（焦点、精神）
{namespace}.{id}.{field}  # 命名空间（事件）
{type}_{name}             # 通用命名
```

### 3. 文本编写
- ✅ 使用颜色代码突出重要数值
- ✅ 使用图标增强可读性
- ✅ 保持文本简洁明了
- ❌ 避免过长的单行文本

### 4. 调试技巧
- 使用 `debug_text` 控制台命令测试
- 检查 `error.log` 中的本地化错误
- 使用 Modding 工具检查语法

---

## 📝 常见错误

### 错误1：缺少冒号
```yaml
# ❌ 错误
key_name "Display Text"

# ✅ 正确
key_name:0 "Display Text"
```

### 错误2：缺少语言标识
```yaml
# ❌ 错误（文件开头缺少）
key_name:0 "Text"

# ✅ 正确
l_english:
 key_name:0 "Text"
```

### 错误3：编码错误
```
❌ UTF-8 无 BOM → 可能导致乱码
✅ UTF-8 带 BOM → 正确显示中文
```

---

**下一步**: 学习决议系统示例 →
