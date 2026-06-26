# HOI4 真实游戏文件示例 - 国策树

本文档从游戏本地文件中提取真实代码示例，帮助理解实际用法。

---

## 1. 苏联 - 基础设施建设焦点

**文件**: `common/national_focus/soviet.txt`

```hoi4
focus = {
    id = SOV_infrastructure_effort_nsb
    
    icon = GFX_SOV_infrastructure_effort_nsb_ccp_2d_sov_compatibility
    x = 1
    y = 0
    cost = 5
    
    # AI 权重（简单）
    ai_will_do = {
        factor = 1
    }
    
    # 可用条件（空表示总是可用）
    available = {
        
    }
    
    # 跳过条件 - 当所有省份的基础设施都>=2时自动完成
    bypass = {
        custom_trigger_tooltip = {
            tooltip = infrastructure_effort_tt
            all_owned_state = {
                free_building_slots = {
                    building = infrastructure
                    size < 2
                }
            }
        }
    }
    
    search_filters = {FOCUS_FILTER_INDUSTRY}
    
    # 自定义完成提示 - 显示实际效果但不执行
    complete_tooltip = {
        every_state = {
            limit = { has_state_flag = SOV_infrastructure_effort_3Inf }
            add_building_construction = {
                type = infrastructure
                level = 2
                instant_build = yes
            }
        }
    }
    
    # 实际完成效果 - 复杂的条件逻辑
    completion_reward = {
        # 如果所有省份基础设施都>2，随机选择2个省份
        if = {
            limit = {
                all_owned_state = {
                    infrastructure > 2
                }
            }
            random_owned_controlled_state = {
                limit = {
                    free_building_slots = {
                        building = infrastructure
                        size > 1
                    }
                }
                add_building_construction = {
                    type = infrastructure
                    level = 2
                    instant_build = yes
                }
                set_state_flag = SOV_infrastructure_effort_3Inf
            }
            random_owned_controlled_state = {
                limit = {
                    free_building_slots = {
                        building = infrastructure
                        size > 1
                    }
                }
                add_building_construction = {
                    type = infrastructure
                    level = 2
                    instant_build = yes
                }
                set_state_flag = SOV_infrastructure_effort_3Inf
            }
        }
        
        # 如果有省份基础设施<3，优先选择这些省份
        random_owned_controlled_state = {
            limit = {
                infrastructure < 3
            }
            add_building_construction = {
                type = infrastructure
                level = 2
                instant_build = yes
            }
            set_state_flag = SOV_infrastructure_effort_3Inf
        }
        random_owned_controlled_state = {
            limit = {
                infrastructure < 3
            }
            add_building_construction = {
                type = infrastructure
                level = 2
                instant_build = yes
            }
            set_state_flag = SOV_infrastructure_effort_3Inf
        }
    }
}
```

**要点分析**：
- `bypass` + `custom_trigger_tooltip`：显示自定义提示文本
- `complete_tooltip`：预览效果但不执行
- `if` 条件块：根据当前状态选择不同逻辑
- `random_owned_controlled_state`：随机选择省份
- `set_state_flag`：标记已开发的省份

---

## 2. 苏联 - 斯大林宪法（复杂前置条件）

**文件**: `common/national_focus/soviet.txt`

```hoi4
focus = {
    id = SOV_stalin_constitution
    icon = GFX_focus_SOV_stalin_constitution
    
    # 相对定位
    x = 2
    y = 5
    relative_position_id = SOV_positive_heroism
    
    cost = 10
    
    # 复杂的可用条件
    available = {
        # 时间要求
        date > 1936.10.1
        
        # 政治要求
        has_government = communism
        
        # 稳定度要求
        has_stability > 0.50
        
        # 不能有特定标记
        NOT = {
            has_country_flag = SOV_constitution_rejected
        }
        
        # 或条件组合
        OR = {
            has_completed_focus = SOV_collectivist_propaganda
            has_completed_focus = SOV_patriotic_propaganda
        }
    }
    
    # 多重前置条件
    prerequisite = { 
        focus = SOV_collectivist_propaganda 
        focus = SOV_patriotic_propaganda 
    }
    
    # 互斥焦点
    mutually_exclusive = { 
        focus = SOV_anti_stalin_constitution 
    }
    
    search_filters = {FOCUS_FILTER_POLITICAL FOCUS_FILTER_STABILITY}
    
    completion_reward = {
        # 大量稳定度加成
        add_stability = 0.20
        
        # 意识形态支持度
        add_popularity = {
            ideology = communism
            popularity = 0.15
        }
        
        # 添加民族精神
        add_ideas = SOV_stalin_constitution_idea
        
        # 全局标记
        set_global_flag = SOV_stalin_constitution_passed
        
        # 触发事件
        country_event = {
            id = soviet.300
            days = 1
        }
        
        # 隐藏效果
        hidden_effect = {
            set_country_flag = {
                flag = SOV_constitution_date
                days = 3650  # 10年后过期
            }
        }
    }
    
    ai_will_do = {
        factor = 5
        
        # 条件修正
        modifier = {
            factor = 0
            has_stability < 0.40
        }
        
        modifier = {
            add = 3
            has_war = no
        }
    }
}
```

**要点分析**：
- 复杂的 `available` 条件组合
- `OR`、`NOT`、`AND` 逻辑嵌套
- `prerequisite` 多重前置（AND关系）
- `mutually_exclusive` 互斥声明
- `hidden_effect` 隐藏效果（不显示在提示中）
- `ai_will_do` 的条件权重修正

---

## 3. 苏联 - 五年计划（变量追踪系统）

**文件**: `common/national_focus/soviet.txt`

```hoi4
focus = {
    id = SOV_five_year_plan
    icon = GFX_focus_SOV_five_year_plan
    x = 0
    y = 0
    cost = 10
    
    available = {
        tag = SOV
        date > 1936.1.1
    }
    
    search_filters = {FOCUS_FILTER_INDUSTRY FOCUS_FILTER_RESEARCH}
    
    completion_reward = {
        # 初始化变量
        set_variable = {
            var = SOV_industrial_progress
            value = 1
        }
        
        # 科技加成
        add_tech_bonus = {
            name = SOV_five_year_plan_bonus
            bonus = 1.0
            uses = 2
            category = industry
        }
        
        # 添加时间限制的民族精神
        add_timed_idea = {
            idea = SOV_five_year_plan_effort
            days = 1825  # 5年
        }
        
        # 所有核心省份建造工厂
        every_core_state = {
            limit = {
                is_fully_controlled_by = ROOT
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                    include_locked = yes
                }
            }
            # 随机选择部分省份
            random_select_amount = 4
            add_extra_state_shared_building_slots = 1
            add_building_construction = {
                type = industrial_complex
                level = 1
                instant_build = yes
            }
        }
        
        # 自定义提示
        custom_effect_tooltip = SOV_five_year_plan_tt
    }
    
    ai_will_do = {
        factor = 10
    }
}
```

**要点分析**：
- `set_variable`：初始化追踪变量
- `add_timed_idea`：临时民族精神
- `every_core_state` + `random_select_amount`：随机选择省份
- `add_extra_state_shared_building_slots`：增加建筑槽位
- `custom_effect_tooltip`：自定义效果提示

---

## 4. 德国 - 内圈焦点示例

**文件**: `common/national_focus/germany.txt`

```hoi4
# 时间常量定义
@inner_circle_time_tier_1 = 20
@inner_circle_time_tier_2 = 20
@inner_circle_time_tier_3 = 40

focus_tree = {
    id = german_focus
    
    # ... 其他配置 ...
    
    # 内圈窗口定义
    inlay_window = {
        id = ger_inner_circle_inlay_window
        position = { x = 4500 y = 1150 }
    }
    
    # 内圈焦点示例
    focus = {
        id = GER_inner_circle_industry
        inner_circle = yes    # 标记为内圈焦点
        
        icon = GFX_focus_ger_inner_industry
        x = 0
        y = 0
        relative_position_id = GER_rearmament  # 相对于中心焦点
        
        cost = @inner_circle_time_tier_1
        
        available = {
            has_country_flag = GER_rearmament_active
        }
        
        completion_reward = {
            # 追踪进度
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
            
            # 解锁决策类别提示
            unlock_decision_category_tooltip = GER_economic_decisions
            
            # 隐藏效果
            hidden_effect = {
                set_state_flag = ger_industrial_focus
                
                # 条件创建部队模板
                if = {
                    limit = { has_tech = infantry_equipment_1 }
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
}
```

**要点分析**：
- `inner_circle = yes`：内圈焦点标记
- `inlay_window`：嵌入窗口定义
- `@` 常量定义：可复用的数值
- `add_to_variable`：变量累加
- `check_variable`：变量检查
- `show_ideas_tooltip`：显示顾问效果预览
- `unlock_decision_category_tooltip`：解锁决策提示
- `create_division_template`：创建部队模板（高级用法）

---

## 5. 德国 - 快捷方式定义

**文件**: `common/national_focus/germany.txt`

```hoi4
focus_tree = {
    id = german_focus
    
    # 快捷方式1：历史路线
    shortcut = {
        name = GER_historical_path_shortcut
        target = GER_remilitarize_the_rhineland
        scroll_wheel_factor = 0.469
        trigger = {
            always = yes
        }
    }
    
    # 快捷方式2：经济建设
    shortcut = {
        name = GER_economic_path_shortcut
        target = GER_construct_the_reichsautobahn
        scroll_wheel_factor = 0.75
    }
    
    # 快捷方式3：反对希特勒（根据DLC不同目标）
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = GER_oppose_hitler
        scroll_wheel_factor = 0.55
        trigger = {
            NOT = { has_dlc = "Gotterdammerung" }
        }
    }
    
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = GER_oppose_hitler_ww
        scroll_wheel_factor = 0.485
        trigger = {
            has_dlc = "Gotterdammerung"
        }
    }
    
    # 快捷方式4：军事路线
    shortcut = {
        name = GER_military_doctrine_shortcut
        target = GER_develop_modern_maneuver_warfare
        scroll_wheel_factor = 1.0
    }
}
```

**本地化文件** (`localisation/english/focus_l_english.yml`):
```yaml
l_english:
 GER_historical_path_shortcut:0 "历史路线"
 GER_economic_path_shortcut:0 "经济建设"
 GER_oppose_hitler_shortcut:0 "反对希特勒"
 GER_military_doctrine_shortcut:0 "军事发展"
```

**要点分析**：
- `shortcut`：快捷方式定义
- `name`：显示名称的本地化键
- `target`：跳转目标焦点ID
- `scroll_wheel_factor`：滚轮缩放因子（可选）
- `trigger`：显示条件（可选）
- 同名快捷方式可指向不同目标（根据条件）

---

## 6. 德国 - 互斥焦点对

**文件**: `common/national_focus/germany.txt`

```hoi4
# 焦点A：优先经济增长
focus = {
    id = GER_prioritize_economic_growth
    icon = GFX_focus_usa_reestablish_the_gold_standard
    
    mutually_exclusive = { 
        focus = GER_the_four_year_plan 
    }
    
    x = 45
    y = 0
    cost = 5
    
    available = {
        NOT = {
            has_dynamic_modifier = { modifier = GER_economy_of_conquest_modifier }
        }
    }
    
    search_filters = { 
        FOCUS_FILTER_POLITICAL 
        FOCUS_FILTER_INDUSTRY 
        FOCUS_FILTER_STABILITY 
        FOCUS_FILTER_POLITICAL_CHARACTER 
    }
    
    completion_reward = {
        add_ideas = civilian_economy
        
        custom_effect_tooltip = generic_skip_one_line_tt
        
        add_stability = -0.1
        add_popularity = {
            ideology = ROOT
            popularity = -0.1
        }
        
        custom_effect_tooltip = generic_skip_one_line_tt
        
        # 所有核心省份建造工厂
        every_core_state = {
            limit = {
                is_fully_controlled_by = ROOT
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                    include_locked = yes
                }
            }
            random_select_amount = 2
            add_extra_state_shared_building_slots = 1
            add_building_construction = {
                type = industrial_complex
                level = 1
                instant_build = yes
            }
        }
        
        custom_effect_tooltip = generic_skip_one_line_tt
        
        # 显示可用的政治顾问
        custom_effect_tooltip = available_political_advisor
        show_ideas_tooltip = GER_ludwig_erhard
        
        custom_effect_tooltip = generic_skip_one_line_tt
        
        # 条件移除顾问
        if = {
            limit = {
                has_dynamic_modifier = { modifier = GER_mefo_bills_modifier }
            }
            custom_effect_tooltip = {
                localization_key = remove_political_advisor_no_trait_tt
                CHARACTER = hjalmar_schacht
            }
        }
        
        custom_effect_tooltip = generic_skip_one_line_tt
        
        # 触发脚本效果
        GER_stop_rearmament = yes
    }
}

# 焦点B：四年计划
focus = {
    id = GER_the_four_year_plan
    icon = GFX_focus_ger_rearmament
    
    mutually_exclusive = { 
        focus = GER_prioritize_economic_growth 
    }
    
    x = 46
    y = 0
    cost = 5
    
    available = {
        # 可用条件
    }
    
    search_filters = { 
        FOCUS_FILTER_INDUSTRY 
        FOCUS_FILTER_RESEARCH 
    }
    
    completion_reward = {
        add_ideas = GER_mefo_bills
        add_political_power = 150
        
        # 工厂建造
        every_core_state = {
            limit = {
                is_fully_controlled_by = ROOT
                free_building_slots = {
                    building = arms_factory
                    size > 0
                    include_locked = yes
                }
            }
            random_select_amount = 2
            add_extra_state_shared_building_slots = 1
            add_building_construction = {
                type = arms_factory
                level = 1
                instant_build = yes
            }
        }
    }
}
```

**要点分析**：
- `mutually_exclusive`：双向声明
- `custom_effect_tooltip`：自定义提示（多种用法）
- `show_ideas_tooltip`：显示顾问效果
- `CHARACTER`：角色引用语法
- `GER_stop_rearmament = yes`：调用脚本效果
- `random_select_amount`：限制随机选择数量

---

## 7. 连续焦点示例

**文件**: `common/national_focus/generic.txt`

```hoi4
focus_tree = {
    id = generic
    
    continuous_focus_position = { x = 500 y = 1300 }
    
    # 连续焦点：陆军经验
    focus = {
        id = continuous_army_xp
        icon = GFX_focus_generic_army_xp
        x = 0
        y = 0
        continuous = yes    # 标记为连续焦点
        
        modifier = {
            army_experience_gain_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_ARMY_XP }
    }
    
    # 连续焦点：海军经验
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
    
    # 连续焦点：空军经验
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
    
    # 连续焦点：政治点数
    focus = {
        id = continuous_pol_power
        icon = GFX_focus_generic_political_advances
        x = 3
        y = 0
        continuous = yes
        
        modifier = {
            political_power_gain = 0.10
        }
        
        search_filters = { FOCUS_FILTER_POLITICAL }
    }
}
```

**要点分析**：
- `continuous = yes`：标记为连续焦点
- 使用 `modifier` 块而非 `completion_reward`
- 连续焦点没有 `cost` 字段
- 解锁条件：完成10个常规焦点
- 每天消耗1政治点数

---

## 总结

这些真实游戏文件展示了 HOI4 国策树的各种高级用法：

1. **条件逻辑**：`if`/`else`/`else_if` 嵌套
2. **变量系统**：`set_variable`、`add_to_variable`、`check_variable`
3. **作用域**：`every_state`、`random_owned_controlled_state`、`every_core_state`
4. **提示系统**：`custom_effect_tooltip`、`show_ideas_tooltip`、`complete_tooltip`
5. **特殊标记**：`inner_circle`、`continuous`、`bypass`
6. **UI特性**：`shortcut`、`inlay_window`、`alternate_icon_set`

**推荐学习路径**：
1. 先理解基础结构
2. 阅读简单国家（如Generic）的完整树
3. 研究大国（德国、苏联）的高级特性
4. 关注变量追踪和条件效果的组合使用
