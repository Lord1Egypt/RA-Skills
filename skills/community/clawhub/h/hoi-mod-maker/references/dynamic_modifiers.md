# HOI4 动态修正 (Dynamic Modifiers) 完整语法参考

**版本**: 1.0
**更新**: 2026-04-24
**来源**: 游戏本体文件 + Paradox Wiki

---

## 一、概述

**动态修正**是一种可以在游戏运行时动态应用和移除的修饰符系统。与普通修正（modifiers）不同，动态修正：

- ✅ 可以通过效果（effect）添加和移除
- ✅ 支持条件启用（`enable`）和条件移除（`remove_trigger`）
- ✅ 可以限定作用域（`scope`）
- ✅ 可以设置持续时间（`days`）
- ✅ 可以应用于：国家、州、指挥官、特殊项目

**典型用途**：
- 国策树的奖励效果
- 事件的临时增益/减益
- 占领政策的负面影响
- 特殊项目的持续效果

---

## 二、文件位置

```
common/
└── dynamic_modifiers/
    ├── 0_dynamic_modifiers.txt          # 基础/通用动态修正
    ├── aat_dynamic_modifiers.txt        # Arms Against Tyranny DLC
    ├── bba_dynamic_modifiers.txt        # By Blood Alone DLC
    ├── GoE_dynamic_modifiers.txt        # Gates of Hell DLC
    ├── HABSBURG_dynamic_modifiers.txt   # 哈布斯堡王朝Mod
    └── ...其他DLC/Mod的动态修正
```

---

## 三、定义语法

### 3.1 完整结构

```paradox
# ============================================
# 动态修正定义语法
# ============================================

dynamic_modifier_id = {
    # ---------- 可选：显示 ----------
    icon = GFX_modifiers_xxx          # UI图标（可选）
    
    # ---------- 启用条件（可选）----------
    # 只有当 enable 块内的条件满足时，修正才会生效
    # 如果不写 enable，默认 always = yes
    enable = {
        always = yes                  # 默认：总是启用
        # 或自定义条件
        tag = GER                     # 示例：仅特定国家
        has_completed_focus = xxx     # 示例：已完成特定国策
    }
    
    # ---------- 移除条件（可选）----------
    # 当 remove_trigger 条件满足时，修正会被移除
    # 示例：占领结束后移除占领惩罚
    remove_trigger = {
        OWNER = {
            original_tag = CAT        # 原来的国家标签
        }
    }
    
    # ---------- 攻击者修正（可选）----------
    # 如果设为 yes，此修正会影响参与战斗的所有人
    # 即使他们不在这个州
    attacker_modifier = no            # 默认 no
    
    # ---------- 修正值列表 ----------
    # 这里写所有要应用的修正值
    # 可以是国家修正、州修正、或指挥官修正
    
    # --- 国家修正示例 ---
    political_power_gain = 0.1       # 政治 power 获取 +10%
    consumer_goods_factor = -0.05     # 消费品工厂需求 -5%
    production_speed_buildings_factor = 0.15  # 建筑速度 +15%
    
    # --- 州修正示例（需要 local_ 前缀）---
    local_building_slots_factor = 0.25        # 建筑槽位 +25%
    local_factories = 2                       # 额外工厂 +2
    state_resources_factor = 0.1             # 资源产出 +10%
    local_manpower = 0.2                      # 本地人力 +20%
    local_production_speed_industrial_complex_factor = 0.2  # 工业复合体速度 +20%
    
    # --- 指挥官修正示例 ---
    armor_value = 0.5                         # 装甲值 +0.5
    defense = 1                               # 防御 +1
    attack = 2                                # 攻击 +2
    organization = 10                         # 组织度 +10
    
    # --- 抵抗/顺从度修正（占领相关）---
    compliance_growth = 0.05                # 顺从度增长 +5%
    resistance_growth = 0.1                  # 抵抗增长 +10%
    resistance_target = 0.2                  # 抵抗目标 +20%
    resistance_decay = 0.05                   # 抵抗衰减 +5%
    
    # --- 资源修正（临时）---
    temporary_state_resource_oil = sabotaged_oil    # 临时资源减少
}
```

### 3.2 简化形式

```paradox
# 如果不需要 enable/remove_trigger，可以用简化形式：
simple_modifier = {
    icon = GFX_idea_xxx
    political_power_gain = 0.1
    production_speed_buildings_factor = 0.15
}

# 等价于：
simple_modifier = {
    enable = { always = yes }
    icon = GFX_idea_xxx
    political_power_gain = 0.1
    production_speed_buildings_factor = 0.15
}
```

### 3.3 条件修正

```paradox
# 带条件的修正：当 enable 条件满足时应用
conditional_modifier = {
    enable = {
        has_completed_focus = GER_four_year_plan  # 仅在完成特定国策后生效
    }
    
    icon = GFX_idea_man_five_year_plan_industry
    
    political_power_gain = 0.05
    production_speed_buildings_factor = 0.15
    industrial_capacity_factory = -0.02
    production_factory_efficiency_gain_factor = BUL_foreign_industry_production_efficiency_modifier
}
```

---

## 四、应用语法

### 4.1 基本用法

```paradox
# 在任何效果块中使用
effect = {
    # 添加动态修正到当前作用域
    add_dynamic_modifier = {
        modifier = my_modifier  # 修正的 ID
    }
}

# 移除动态修正
effect = {
    remove_dynamic_modifier = {
        modifier = my_modifier
    }
}
```

### 4.2 带作用域（scope）

```paradox
# scope 参数：指定修正应用于哪个国家
# 默认为当前效果的作用域
effect = {
    # 示例1：应用于特定国家
    add_dynamic_modifier = {
        modifier = FIN_confederation_of_finno_russian_republics_dm
        scope = ROOT              # 应用于 ROOT（国策树所属国）
    }
    
    # 示例2：应用于事件目标
    add_dynamic_modifier = {
        modifier = my_modifier
        scope = FROM              # 应用于 FROM
    }
    
    # 示例3：应用于特定标签
    add_dynamic_modifier = {
        modifier = ITA_libyan_railway_modifier
        scope = ITA              # 固定应用于意大利
    }
}
```

### 4.3 带持续时间（days）

```paradox
# days 参数：修正在指定天数后自动移除
effect = {
    # 示例1：持续730天（约2年）
    add_dynamic_modifier = {
        modifier = DEN_economic_crisis_dynamic_modifier
        days = 730
    }
    
    # 示例2：持续30天
    add_dynamic_modifier = {
        modifier = temporary_boost
        days = 30
    }
    
    # 示例3：同时指定 scope 和 days
    add_dynamic_modifier = {
        modifier = ITA_libyan_railway_modifier
        days = 730
        scope = ITA
    }
}
```

### 4.4 完整参数

```paradox
effect = {
    add_dynamic_modifier = {
        modifier = xxx                    # 必填：修正ID
        scope = ROOT                     # 可选：作用域（默认当前作用域）
        days = 365                       # 可选：持续天数（不写则永久）
    }
}

effect = {
    remove_dynamic_modifier = {
        modifier = xxx                   # 必填：修正ID
        scope = ROOT                     # 可选：作用域
    }
}
```

---

## 五、真实游戏代码示例

### 5.1 国家级动态修正（民族精神形式）

```paradox
# 文件：common/dynamic_modifiers/0_dynamic_modifiers.txt

# ============================================
# 示例1：保加利亚外资工业（作为民族精神使用）
# ============================================
BUL_foreign_industry_dynamic_modifier = {
    enable = { always = yes }
    
    icon = GFX_idea_man_five_year_plan_industry
    
    # 政治 power 获取 +5%
    political_power_gain = 0.05
    
    # 建筑速度（从变量读取）
    production_speed_buildings_factor = BUL_foreign_industry_construction_speed_modifier
    
    # 军工厂产能 -2%
    industrial_capacity_factory = -0.02
    
    # 生产效率增益（从变量读取）
    production_factory_efficiency_gain_factor = BUL_foreign_industry_production_efficiency_modifier
    
    # 最大效率上限（从变量读取）
    production_factory_max_efficiency_factor = BUL_foreign_industry_production_efficiency_modifier
    
    # 消费品工厂需求（从变量读取）
    consumer_goods_factor = BUL_foreign_industry_consumer_goods_modifier
}

# ============================================
# 示例2：自治州状态（占领相关）
# ============================================
autonomous_state = {
    enable = { always = yes }
    
    icon = GFX_modifiers_sabotaged_resource
    
    # 可招募人口 -50%
    recruitable_population_factor = -0.5
    
    # 建筑槽位 -25%
    local_building_slots_factor = -0.25
    
    # 资源产出 -25%
    state_resources_factor = -0.25
    
    # 建筑速度 -25%
    state_production_speed_buildings_factor = -0.25
    
    # 移除条件：原国家为加泰罗尼亚/加利西亚/巴斯克时移除
    remove_trigger = {
        OWNER = {
            OR = {
                original_tag = CAT
                original_tag = GLC
                original_tag = BAS
            }
        }
    }
}
```

### 5.2 州级动态修正（占领惩罚）

```paradox
# ============================================
# 示例3：库尔德斯坦 agitation（抵抗活动）
# ============================================
kurdish_agitation = {
    enable = { always = yes }
    
    icon = GFX_modifiers_tur_kurdish_agitation
    
    # 抵抗增长 +3%
    resistance_growth = 0.03
    
    # 抵抗目标 10%
    resistance_target = 0.1
    
    # 抵抗衰减 -10%（负数=增长）
    resistance_decay = -0.1
    
    # 资源产出 -15%
    state_resources_factor = -0.15
}

# ============================================
# 示例4：库尔德斯坦叛乱（严重）
# ============================================
kurdish_separatism = {
    enable = { always = yes }
    
    icon = GFX_modifiers_tur_kurdish_separatism
    
    # 顺从度增长 -5%
    compliance_growth = -0.05
    
    # 抵抗增长 +5%
    resistance_growth = 0.05
    
    # 抵抗目标 20%
    resistance_target = 0.20
    
    # 抵抗衰减 -20%
    resistance_decay = -0.20
    
    # 资源产出 -33%
    state_resources_factor = -0.33
    
    # 禁止战略重部署
    disable_strategic_redeployment = 1
}

# ============================================
# 示例5：基础设施条件触发
# ============================================
dense_rural_infrastructure = {
    enable = { always = yes }
    
    # 移除条件：基础设施 > 4 时移除
    remove_trigger = {
        ROOT = {
            infrastructure > 4
        }
    }
    
    icon = GFX_modifiers_SOV_civilian_labor_in_defense
    
    # 非核心补给影响 +40%
    local_non_core_supply_impact_factor = 0.4
}
```

### 5.3 国策中的应用

```paradox
# 文件：common/national_focus/italy.txt
# 示例：利比亚铁路建设

ITA_libyan_railway = {
    # ... 国策定义 ...
    
    completion_reward = {
        # 添加动态修正到意大利国家
        # 持续730天，作用域 ITA
        add_dynamic_modifier = {
            modifier = ITA_libyan_railway_modifier
            days = 730
            scope = ITA
        }
        
        custom_effect_tooltip = ITA_libyan_railway_tt
    }
}

# ============================================
# 文件：common/national_focus/denmark.txt
# 示例：经济危机

DEN_economic_crisis = {
    # ... 国策定义 ...
    
    completion_reward = {
        # 添加730天的经济危机修正
        add_dynamic_modifier = {
            modifier = DEN_economic_crisis_dynamic_modifier
            days = 730
        }
    }
}

# ============================================
# 文件：common/national_focus/finland.txt
# 示例：芬诺俄罗斯共和国联邦

FIN_confederation = {
    # ... 国策定义 ...
    
    completion_reward = {
        # 添加到 ROOT（芬兰）
        add_dynamic_modifier = {
            modifier = FIN_confederation_of_finno_russian_republics_dm
            scope = ROOT
        }
        
        # 同时给俄罗斯添加
        hidden_effect = {
            RUS = {
                add_dynamic_modifier = {
                    modifier = FIN_confederation_of_finno_russian_republics_dm
                    scope = ROOT
                }
            }
        }
    }
}
```

---

## 六、常用修正字段速查表

### 6.1 国家级修正

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `political_power_gain` | 百分比 | 政治 power 获取 | `0.1` (+10%) |
| `consumer_goods_factor` | 百分比 | 消费品工厂需求 | `-0.05` (-5%) |
| `production_speed_buildings_factor` | 百分比 | 建筑速度 | `0.15` (+15%) |
| `industrial_capacity_factory` | 百分比 | 军工厂产能 | `-0.02` (-2%) |
| `production_factory_efficiency_gain_factor` | 百分比 | 生产效率增长 | `0.1` (+10%) |
| `army_core_attack_factor` | 百分比 | 陆军核心攻击 | `0.1` (+10%) |
| `army_core_defence_factor` | 百分比 | 陆军核心防御 | `0.1` (+10%) |
| `training_time_factor` | 百分比 | 训练时间 | `-0.1` (-10%) |
| `experience_gain_navy_factor` | 百分比 | 海军经验获取 | `0.1` (+10%) |

### 6.2 州级修正（需要 `local_` 前缀）

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `local_building_slots_factor` | 百分比 | 建筑槽位 | `0.25` (+25%) |
| `local_factories` | 数字 | 额外工厂数 | `2` |
| `state_resources_factor` | 百分比 | 资源产出 | `0.1` (+10%) |
| `local_manpower` | 百分比 | 本地人力 | `0.2` (+20%) |
| `local_non_core_manpower` | 百分比 | 非核心人力 | `0.25` (+25%) |
| `local_supply_impact_factor` | 百分比 | 补给影响 | `0.5` (+50%) |
| `local_production_speed_industrial_complex_factor` | 百分比 | 工业复合体速度 | `0.2` (+20%) |
| `local_non_core_supply_impact_factor` | 百分比 | 非核心补给 | `0.4` (+40%) |

### 6.3 占领/抵抗修正

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `compliance_growth` | 百分比 | 顺从度增长 | `0.05` (+5%) |
| `resistance_growth` | 百分比 | 抵抗增长 | `0.1` (+10%) |
| `resistance_target` | 百分比 | 抵抗目标 | `0.2` (20%) |
| `resistance_decay` | 百分比 | 抵抗衰减 | `0.15` (+15%) |
| `disable_strategic_redeployment` | 布尔 | 禁止战略重部署 | `1` |

### 6.4 指挥官修正

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `armor_value` | 数字 | 装甲值 | `0.5` |
| `defense` | 数字 | 防御 | `1` |
| `attack` | 数字 | 攻击 | `2` |
| `organization` | 数字 | 组织度 | `10` |

---

## 七、最佳实践

### 7.1 命名规范

```paradox
# 国家级修正：以国家标签开头
GER_war_economy = { ... }
FRA_five_year_plan = { ... }

# 州级修正：描述性名称
kurdish_separatism = { ... }
occupied_territory_penalty = { ... }

# 功能性修正
temporary_boost = { ... }
research_bonus_modifier = { ... }
```

### 7.2 图标命名

```paradox
# 国家修正（民族精神）：使用 GFX_idea_
icon = GFX_idea_man_five_year_plan_industry

# 州修正（占领相关）：使用 GFX_modifiers_
icon = GFX_modifiers_tur_kurdish_agitation
icon = GFX_modifiers_sabotaged_resource
```

### 7.3 与变量的结合

```paradox
# 保加利亚示例：用变量控制动态修正强度
BUL_foreign_industry_dynamic_modifier = {
    enable = { always = yes }
    icon = GFX_idea_man_five_year_plan_industry
    
    # 从变量读取修正值
    production_speed_buildings_factor = BUL_foreign_industry_construction_speed_modifier
    production_factory_efficiency_gain_factor = BUL_foreign_industry_production_efficiency_modifier
    consumer_goods_factor = BUL_foreign_industry_consumer_goods_modifier
}

# 在国策中设置变量
completion_reward = {
    set_variable = { BUL_foreign_industry_construction_speed_modifier = 0.15 }
    set_variable = { BUL_foreign_industry_production_efficiency_modifier = 0.1 }
    set_variable = { BUL_foreign_industry_consumer_goods_modifier = -0.05 }
    
    add_dynamic_modifier = {
        modifier = BUL_foreign_industry_dynamic_modifier
    }
}
```

### 7.4 条件启用的正确用法

```paradox
# ✅ 正确：使用 enable 条件
conditional_modifier = {
    enable = {
        has_completed_focus = MY_national_focus_id
    }
    production_speed_buildings_factor = 0.1
}

# ✅ 正确：使用 remove_trigger
temporary_penalty = {
    enable = { always = yes }
    
    # 条件满足时移除
    remove_trigger = {
        date > 1939.1.1
    }
    
    political_power_gain = -0.1
}

# ❌ 错误：在 enable 中使用复杂逻辑
# 应该在国策/事件的 available 块中处理
```

---

## 八、调试技巧

### 8.1 修正不生效的常见原因

1. **忘记定义**：修正ID必须在 `common/dynamic_modifiers/` 中定义
2. **enable 条件不满足**：检查 enable 块的条件
3. **remove_trigger 已触发**：检查移除条件
4. **作用域错误**：使用 `scope` 参数指定正确的作用域
5. **已存在相同修正**：移除旧修正后再添加

### 8.2 调试命令

```paradox
# 在控制台查看当前国家的动态修正
# debug_mode 后使用以下命令查看

# 查看国家级动态修正
has_dynamic_modifier = { modifier = xxx }

# 查看特定修正是否激活
has_country_modifier = xxx
```

### 8.3 常见错误

```paradox
# ❌ 错误1：修正ID不存在
add_dynamic_modifier = {
    modifier = NONEXISTENT_modifier  # 会报错！
}

# ✅ 正确：先在 dynamic_modifiers 中定义
# common/dynamic_modifiers/my_modifiers.txt
my_modifier = {
    political_power_gain = 0.1
}

# 然后再使用
add_dynamic_modifier = {
    modifier = my_modifier
}

# ❌ 错误2：days 参数类型错误
add_dynamic_modifier = {
    modifier = my_modifier
    days = "30"  # 错误：字符串类型
}

# ✅ 正确：使用数字
add_dynamic_modifier = {
    modifier = my_modifier
    days = 30
}

# ❌ 错误3：scope 写错
add_dynamic_modifier = {
    modifier = my_modifier
    scope = "ROOT"  # 错误：引号
}

# ✅ 正确：不加引号
add_dynamic_modifier = {
    modifier = my_modifier
    scope = ROOT
}
```

---

## 九、相关文件关联

| 文件类型 | 位置 | 说明 |
|----------|------|------|
| 动态修正定义 | `common/dynamic_modifiers/*.txt` | 修正的完整定义 |
| 国策奖励 | `common/national_focus/*.txt` | 常见的应用位置 |
| 事件效果 | `events/*.txt` | 事件中添加/移除 |
| 决议效果 | `common/decisions/*.txt` | 决议中添加/移除 |

---

**文档版本**: 1.0
**更新日期**: 2026-04-24
**维护者**: AI Agent (HOI Mod-Maker Skill)
