# HOI4 高级语法参考

本文档整合了从 Wiki 和游戏本地文件提取的高级语法特性。

---

## 目录

1. [Focus Tree 高级特性](#focus-tree-高级特性)
2. [Inner Circle 内圈焦点](#inner-circle-内圈焦点)
3. [Shortcut 快捷方式](#shortcut-快捷方式)
4. [Inlay Window 嵌入窗口](#inlay-window-嵌入窗口)
5. [Continuous Focus 连续焦点](#continuous-focus-连续焦点)
6. [Effect 作用域完整列表](#effect-作用域完整列表)
7. [变量系统](#变量系统)
8. [动态修饰符](#动态修饰符)
9. [高级效果示例](#高级效果示例)

---

## Focus Tree 高级特性

### alternate_icon_set（备选图标集）

```
focus_tree = {
    id = german_focus
    
    # 允许玩家切换到备选图标风格
    alternate_icon_set = FOCUS_ICON_SET_HISTORICAL_KEY_FOCUS
    # 或使用自定义：
    # alternate_icon_set = FOCUS_ALTERNATE_ICONS
    
    # 本地化键：
    # FOCUS_ALTERNATE_ICONS -> 切换按钮文本
    # GFX_FOCUS_ALTERNATE_ICONS -> 切换按钮图标
}
```

### default 树（默认树）

```
focus_tree = {
    id = generic_focus
    
    # 设为默认树，无专属树的国家使用此树
    default = yes
    
    # DLC 检查示例（波兰DLC）
    country = {
        factor = 0
        
        modifier = {
            add = 10
            OR = {
                has_dlc = "No Step Back"
                has_dlc = "Poland: United and Ready"
            }
            original_tag = POL
        }
    }
}
```

---

## Inner Circle 内圈焦点

德国内圈焦点是围绕中心焦点的小型辅助焦点，用于角色政治系统。

### 基础语法

```
focus = {
    id = GER_inner_circle_focus_1
    
    # 标记为内圈焦点
    inner_circle = yes
    
    # 内圈焦点通常 cost 较低
    cost = 20        # 实际天数 = 20 × 7 = 140天
    
    icon = GFX_focus_ger_inner_circle
    
    # 内圈焦点位置相对于中心焦点
    x = 1
    y = 0
    relative_position_id = GER_rearmament
    
    completion_reward = {
        add_political_power = 25
        set_country_flag = ger_inner_circle_1_done
    }
}
```

### 内圈时间常量

```
# 在文件顶部定义常量（实际天数 = 值 × 7）
@inner_circle_time_tier_1 = 20    # 140天
@inner_circle_time_tier_2 = 20    # 140天  
@inner_circle_time_tier_3 = 40    # 280天

focus = {
    id = GER_inner_tier_1
    inner_circle = yes
    cost = @inner_circle_time_tier_1
    # ...
}
```

### 内圈窗口定义

```
focus_tree = {
    id = german_focus
    
    # 内圈焦点显示区域
    inlay_window = {
        id = ger_inner_circle_inlay_window
        position = { x = 4500 y = 1150 }
    }
}
```

---

## Shortcut 快捷方式

快捷方式允许玩家快速定位到特定焦点分支。

### 定义快捷方式

```
focus_tree = {
    id = german_focus
    
    # 快捷方式定义
    shortcut = {
        name = GER_historical_path_shortcut
        target = GER_remilitarize_the_rhineland
        
        # 滚轮缩放因子（可选）
        scroll_wheel_factor = 0.469
        
        # 显示条件（可选）
        trigger = {
            always = yes
        }
    }
    
    shortcut = {
        name = GER_economic_path_shortcut
        target = GER_construct_the_reichsautobahn
        scroll_wheel_factor = 0.75
    }
    
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = GER_oppose_hitler
        scroll_wheel_factor = 0.55
        
        # DLC 条件
        trigger = {
            NOT = { has_dlc = "Gotterdammerung" }
        }
    }
    
    # 多个快捷方式可指向不同目标（根据条件显示）
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = GER_oppose_hitler_ww
        scroll_wheel_factor = 0.485
        trigger = {
            has_dlc = "Gotterdammerung"
        }
    }
}
```

### 本地化

```yaml
# 本地化文件
GER_historical_path_shortcut:0 "历史路线"
GER_economic_path_shortcut:0 "经济建设"
GER_oppose_hitler_shortcut:0 "反对希特勒"
```

---

## Inlay Window 嵌入窗口

嵌入窗口用于在焦点树中创建特殊显示区域（如德国内圈、波兰意志斗争等）。

### 定义嵌入窗口

```
focus_tree = {
    id = polish_focus
    
    # 嵌入窗口定义
    inlay_window = {
        id = pol_will_of_the_people_inlay_window
        position = { x = 1000 y = 800 }
        
        # 可选：定义大小
        size = { width = 400 height = 300 }
    }
}
```

---

## Continuous Focus 连续焦点

连续焦点是一种特殊焦点类型，在完成10个常规焦点后解锁，持续消耗政治点数并提供持续效果。

### 基础结构

```
focus_tree = {
    id = german_focus
    
    # 连续焦点显示位置
    continuous_focus_position = { x = 500 y = 1300 }
    
    # 连续焦点定义
    focus = {
        id = GER_continuous_industrial_effort
        icon = GFX_focus_generic_production
        x = 0
        y = 0
        
        # 标记为连续焦点
        continuous = yes
        
        # 连续焦点不消耗天数，而是每天消耗1政治点数
        # cost 字段对连续焦点无效
        
        completion_reward = {
            # 持续效果
            # 通常使用 modifier
        }
        
        # 连续焦点效果通过 modifier 实现
        modifier = {
            production_speed_factory_factor = 0.10
            production_speed_arms_factory_factor = 0.10
        }
    }
}
```

### 连续焦点完整示例

```
focus_tree = {
    id = generic_focus
    
    continuous_focus_position = { x = 500 y = 1300 }
    
    # 军事经验连续焦点
    focus = {
        id = continuous_army_xp
        icon = GFX_focus_generic_army_xp
        x = 0
        y = 0
        continuous = yes
        
        modifier = {
            army_experience_gain_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_ARMY_XP }
    }
    
    focus = {
        id = continuous_navy_xp
        icon = GFX_focus_generic_navy_xp
        x = 1
        y = 0
        continuous = yes
        
        modifier = {
            navy_experience_gain_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_NAVY_XP }
    }
    
    focus = {
        id = continuous_air_xp
        icon = GFX_focus_generic_air_xp
        x = 2
        y = 0
        continuous = yes
        
        modifier = {
            air_experience_gain_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_AIR_XP }
    }
    
    # 资源连续焦点
    focus = {
        id = continuous_resource_oil
        icon = GFX_focus_generic_oil
        x = 3
        y = 0
        continuous = yes
        
        modifier = {
            oil_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_INTERNATIONAL_TRADE }
    }
}
```

### 连续焦点限制

- 解锁条件：完成10个常规焦点
- 每天消耗：1 政治点数
- 效果：仅在激活时生效
- 数量：同时只能激活一个连续焦点
- 切换：可随时切换，无额外消耗

---

## Effect 作用域完整列表

### 国家作用域

```
# 切换到特定国家
GER = { add_political_power = 100 }

# 所有国家
every_country = {
    limit = { tag = POL }
    # 效果
}

# 随机国家
random_country = {
    limit = { has_stability > 0.5 }
    # 效果
}

# 所有其他国家
every_other_country = {
    limit = { has_war_with = ROOT }
    # 效果
}

# 所有邻国
every_neighbor_country = {
    limit = { is_subject = no }
    # 效果
}

# 所有敌对国家
every_enemy_country = {
    # 效果
}

# 所有占领国（核心被占领）
every_occupied_country = {
    # 效果
}

# 所有附属国
every_subject_country = {
    # 效果
}

# 所有阵营成员
every_faction_member = {
    # 效果
}
```

### 省份作用域

```
# 所有省份
every_state = {
    limit = { is_owned_by = ROOT }
    # 效果
}

# 随机省份
random_state = {
    prioritize = { 123 124 125 }  # 优先选择
    limit = {
        free_building_slots = {
            building = industrial_complex
            size > 0
        }
    }
    # 效果
}

# 所有拥有省份
every_owned_state = {
    limit = { is_core_of = ROOT }
    # 效果
}

# 所有核心省份
every_core_state = {
    limit = { is_owned_by = ROOT }
    # 效果
}

# 所有控制省份
every_controlled_state = {
    # 效果
}

# 随机拥有且控制省份
random_owned_controlled_state = {
    prioritize = { 86 87 88 }
    limit = {
        free_building_slots = {
            building = industrial_complex
            size > 0
            include_locked = yes
        }
    }
    # 效果
}
```

### 单位指挥官作用域

```
# 所有单位指挥官
every_unit_leader = {
    limit = { has_trait = cautious = yes }
    # 效果
}

# 所有陆军指挥官
every_army_leader = {
    # 效果
}

# 所有海军指挥官
every_navy_leader = {
    # 效果
}
```

### 特工作用域

```
# 所有特工
every_operative = {
    limit = { is_active = yes }
    # 效果
}

# 随机特工
random_operative = {
    # 效果
}
```

### 军事工业组织作用域（1.13+）

```
# 所有MIO
every_military_industrial_organization = {
    limit = { has_trait = tank_manufacturer }
    # 效果
}

# 随机MIO
random_military_industrial_organization = {
    # 效果
}
```

---

## 变量系统

### 变量操作效果

```
completion_reward = {
    # 设置变量
    set_variable = {
        var = POL_economy_var
        value = 10
        tooltip = economy_var_tt    # 自定义提示
    }
    
    # 增加变量值
    add_to_variable = {
        var = POL_economy_var
        value = 5
    }
    
    # 减少变量值
    subtract_from_variable = {
        var = POL_economy_var
        value = 3
    }
    
    # 乘法
    multiply_variable = {
        var = POL_economy_var
        value = 2
    }
    
    # 除法
    divide_variable = {
        var = POL_economy_var
        value = 10
    }
    
    # 取模
    modulo_variable = {
        var = POL_economy_var
        value = 100
    }
    
    # 四舍五入
    round_variable = POL_economy_var
    
    # 限制范围
    clamp_variable = {
        var = POL_economy_var
        min = 0
        max = 100
    }
    
    # 设置随机值
    set_variable_to_random = {
        var = random_num
        min = 0
        max = 100
        integer = yes    # 整数
    }
    
    # 清除变量
    clear_variable = POL_economy_var
}
```

### 临时变量

```
completion_reward = {
    # 设置临时变量（事件结束后清除）
    set_temp_variable = {
        temp_var = num_owned_states
        value = num_owned_states
    }
    
    # 临时变量操作
    add_to_temp_variable = {
        temp_var = my_temp
        value = 10
    }
}
```

### 变量作为作用域

```
# 将作用域存储到变量
set_variable = { target_country = THIS }

# 使用变量作为作用域
var:target_country = { add_political_power = 100 }

# 在效果中使用变量
add_to_faction = var:target_country
```

---

## 动态修饰符

### 定义动态修饰符

```
# common/dynamic_modifiers/example_modifiers.txt

POL_war_economy_modifier = {
    # 使用变量的修饰符
    consumer_goods_factor = var:POL_war_economy_var
    
    # 静态值
    production_speed_factory_factor = 0.10
    
    # 条件修饰符
    production_speed_arms_factory_factor = {
        value = 0.10
        triggered_by = {
            has_country_flag = pol_military_buildup
        }
    }
}

GER_economy_of_conquest_modifier = {
    # 触发式修饰符
    production_speed_factory_factor = {
        value = 0.05
        triggered_by = { has_war = yes }
    }
    
    # 对特定国家
    attack_bonus_against = {
        value = 0.10
        triggered_by = {
            FROM = { is_subject_of = ROOT }
        }
    }
}
```

### 添加/移除动态修饰符

```
completion_reward = {
    # 添加动态修饰符
    add_dynamic_modifier = {
        modifier = POL_war_economy_modifier
        scope = ROOT           # 可选，默认为ROOT
        days = 365             # 可选，持续天数
    }
    
    # 移除动态修饰符
    remove_dynamic_modifier = {
        modifier = POL_war_economy_modifier
    }
    
    # 强制更新（变量值变化后立即生效）
    force_update_dynamic_modifier = yes
}
```

---

## 高级效果示例

### 完整的复杂国策效果

```
focus = {
    id = POL_four_year_plan
    icon = GFX_focus_POL_four_year_plan
    x = 0
    y = 0
    cost = 5
    
    search_filters = { FOCUS_FILTER_INDUSTRY FOCUS_FILTER_RESEARCH }
    
    completion_reward = {
        # 科技加成
        add_tech_bonus = {
            name = POL_four_year_plan_bonus
            bonus = 1.0
            uses = 1
            category = construction_tech
        }
        
        # 时间限制的民族精神
        add_timed_idea = {
            idea = POL_four_year_plan_idea
            days = 1460    # 4年
        }
        
        # 设置变量
        set_variable = {
            var = POL_economy_level
            value = 1
        }
        
        # 条件效果
        if = {
            limit = {
                has_tech = construction_tech1
            }
            add_building_construction = {
                type = industrial_complex
                level = 2
                instant_build = yes
                state = 86
            }
        }
        
        # 隐藏效果
        hidden_effect = {
            set_country_flag = pol_four_year_plan_done
            
            # 仅调试日志
            if = {
                limit = { is_debug = yes }
                log = "Poland completed Four Year Plan"
            }
        }
        
        # 自定义提示
        custom_effect_tooltip = POL_four_year_plan_tt
        
        # 循环所有核心省份
        every_core_state = {
            limit = {
                is_fully_controlled_by = ROOT
                free_building_slots = {
                    building = infrastructure
                    size > 2
                }
            }
            random_select_amount = 3    # 随机选择3个
            add_building_construction = {
                type = infrastructure
                level = 1
                instant_build = yes
            }
        }
        
        # 对所有邻国的效果
        every_neighbor_country = {
            limit = {
                NOT = { has_war_with = ROOT }
            }
            add_opinion_modifier = {
                target = ROOT
                modifier = pol_economic_cooperation
            }
        }
    }
    
    # 自定义完成提示
    complete_tooltip = {
        add_political_power = 50
        custom_effect_tooltip = POL_four_year_plan_display_tt
    }
}
```

### 内圈焦点与变量追踪

```
focus = {
    id = GER_inner_circle_industry
    inner_circle = yes
    icon = GFX_focus_ger_inner_industry
    x = 0
    y = 0
    relative_position_id = GER_rearmament
    cost = @inner_circle_time_tier_1
    
    completion_reward = {
        # 增加追踪变量
        add_to_variable = {
            var = GER_inner_circle_progress
            value = 1
        }
        
        # 条件效果
        if = {
            limit = {
                check_variable = {
                    var = GER_inner_circle_progress
                    value > 5
                }
            }
            add_political_power = 100
            custom_effect_tooltip = GER_inner_circle_complete_tt
        }
        
        # 显示顾问提示
        show_ideas_tooltip = GER_hjalmar_schacht
        
        # 解锁决策提示
        unlock_decision_category_tooltip = GER_economic_decisions
        
        # 隐藏效果
        hidden_effect = {
            set_state_flag = ger_industrial_focus
            
            # 条件创建部队模板
            if = {
                limit = {
                    has_tech = infantry_equipment_1
                }
                create_division_template = {
                    name = "Infanterie-Division"
                    is_locked = yes
                    regiments = {
                        infantry = 3
                    }
                }
            }
        }
    }
}
```

### 建筑建造完整示例

```
completion_reward = {
    # 随机省份建造（带优先级）
    random_owned_controlled_state = {
        prioritize = { 762 }    # 上西里西亚
        limit = {
            free_building_slots = {
                building = industrial_complex
                size > 0
                include_locked = yes
            }
        }
        add_extra_state_shared_building_slots = 1
        add_building_construction = {
            type = industrial_complex
            level = 1
            instant_build = yes
        }
        set_state_flag = POL_develop_upper_silesia
    }
    
    # 多个省份建造（随机选择数量）
    every_owned_state = {
        limit = {
            is_core_of = ROOT
            free_building_slots = {
                building = arms_factory
                size > 0
            }
        }
        random_select_amount = 3
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes
        }
    }
    
    # 铁路建设
    build_railway = {
        level = 1
        path = { 9508 6558 3483 }
    }
    
    # 添加资源
    add_resource = {
        type = steel
        amount = 24
        state = 762
    }
}
```

---

## 搜索过滤器完整列表

```
FOCUS_FILTER_POLITICAL           # 政治
FOCUS_FILTER_RESEARCH            # 研究
FOCUS_FILTER_INDUSTRY            # 工业
FOCUS_FILTER_STABILITY           # 稳定度
FOCUS_FILTER_WAR_SUPPORT          # 战争支持度
FOCUS_FILTER_MANPOWER            # 人力
FOCUS_FILTER_ANNEXATION          # 吞并
FOCUS_FILTER_INTERNAL_AFFAIRS    # 内部事务
FOCUS_FILTER_ARMY_XP             # 陆军经验
FOCUS_FILTER_NAVY_XP             # 海军经验
FOCUS_FILTER_AIR_XP              # 空军经验
FOCUS_FILTER_BALANCE_OF_POWER    # 权力平衡
FOCUS_FILTER_POLITICAL_CHARACTER # 政治人物
FOCUS_FILTER_MILITARY_CHARACTER  # 军事人物
FOCUS_FILTER_INTERNATIONAL_TRADE # 国际贸易
FOCUS_FILTER_HISTORICAL          # 历史路线
```

---

**最后更新**: 2026-04-24
