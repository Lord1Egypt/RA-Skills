# HOI4 脚本效果 (Scripted Effects) 完整示例

**版本**: 1.0
**更新**: 2026-04-24
**学习目标**: 掌握脚本效果的定义和调用

---

## 示例一：工厂转换效果

### 场景
玩家选择"工业动员"国策，将5个民用工厂转为军用工厂。

### 1.1 定义脚本效果

```paradox
# 文件：common/scripted_effects/00_scripted_effects.txt
# 这是游戏内置的工厂转换效果

replace_civ_with_arms_factories = {
    # ===== 第一次转换 =====
    # 随机选择一个满足条件的州
    random_owned_controlled_state = {
        # 限制条件
        limit = {
            # 必须是完全控制
            is_fully_controlled_by = ROOT
            # 必须有民用工厂
            industrial_complex > 0
        }
        
        # 移除民用工厂
        remove_building = {
            type = industrial_complex
            level = 1
        }
        
        # 立即添加军用工厂
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes  # 立即建成，不等待
        }
    }
    
    # ===== 第二次转换（重复4次）=====
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
            industrial_complex > 0
        }
        remove_building = {
            type = industrial_complex
            level = 1
        }
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes
        }
    }
    
    # 重复直到5个工厂转换完成...
}
```

### 1.2 在国策中调用

```paradox
# 文件：common/national_focus/MY_focus.txt

MY_industrial_mobilization = {
    id = MY_industrial_mobilization
    icon = GFX_goal_generic_production
    x = 3
    y = 0
    cost = 35
    
    # ===== 前置条件 =====
    prerequisite = {
        focus = MY_basic_industry
    }
    
    # ===== 完成奖励 =====
    completion_reward = {
        # 调用脚本效果
        replace_civ_with_arms_factories = yes
        
        # 添加提示
        custom_effect_tooltip = MY_industrial_mobilization_tt
    }
}
```

### 1.3 自定义版本

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt
# 创建自定义mod的脚本效果

MY_convert_3_factories = {
    # ===== 转换3个民用工厂为军用工厂 =====
    
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
            industrial_complex > 0
        }
        remove_building = {
            type = industrial_complex
            level = 1
        }
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes
        }
    }
    
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
            industrial_complex > 0
        }
        remove_building = {
            type = industrial_complex
            level = 1
        }
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes
        }
    }
    
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
            industrial_complex > 0
        }
        remove_building = {
            type = industrial_complex
            level = 1
        }
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes
        }
    }
}
```

---

## 示例二：带参数的脚本效果

### 场景
创建一个可配置的科技加成效果。

### 2.1 定义

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt

# ============================================
# 带参数的效果
# 使用 [?] 语法定义参数
# ============================================

MY_grant_tech_bonus = {
    # 参数1：科技类别
    # 参数2：加成大小
    # 参数3：使用次数
    
    add_tech_bonus = {
        name = MY_tech_bonus
        bonus = bonus_amount
        uses = use_count
        category = tech_category
    }
}
```

### 2.2 调用

```paradox
MY_research_effort = {
    id = MY_research_effort
    icon = GFX_goal_generic_science
    x = 2
    y = 0
    cost = 70
    
    completion_reward = {
        # 调用带参数的效果
        MY_grant_tech_bonus = {
            tech_category = industry
            bonus_amount = 0.5
            use_count = 2
        }
        
        # 另一个调用
        MY_grant_tech_bonus = {
            tech_category = electronics
            bonus_amount = 0.25
            use_count = 1
        }
        
        custom_effect_tooltip = MY_research_effort_tt
    }
}
```

---

## 示例三：AI 策略设置

### 场景
当玩家完成特定国策时，更新AI的对外策略。

### 3.1 定义

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt

MY_update_ai_strategies = {
    # ===== 对苏联的策略 =====
    add_ai_strategy = {
        type = contain
        id = "SOV"
        value = -500  # 减少围堵
    }
    
    add_ai_strategy = {
        type = befriend
        id = "SOV"
        value = 200  # 增加友好
    }
    
    # ===== 对波兰的策略 =====
    add_ai_strategy = {
        type = protect
        id = "POL"
        value = 100
    }
    
    add_ai_strategy = {
        type = alliance
        id = "POL"
        value = 200
    }
}
```

### 3.2 调用

```paradox
MY_peaceful_diplomacy = {
    id = MY_peaceful_diplomacy
    icon = GFX_goal_generic_diplomacy
    x = 4
    y = 0
    cost = 35
    
    completion_reward = {
        # 更新AI策略
        MY_update_ai_strategies = yes
        
        # 额外奖励
        add_political_power = 50
        add_opinion_modifier = {
            target = SOV
            modifier = improved_relations
        }
    }
}
```

---

## 示例四：继承战争效果

### 场景
当国家政权更迭时，继承前任的战争。

### 4.1 定义

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt

MY_inherit_wars_effect = {
    # 显示提示
    custom_effect_tooltip = MY_inherit_wars_effect_tt
    
    # 隐藏的继承逻辑
    hidden_effect = {
        # 处理防御战
        every_country = {
            limit = {
                has_defensive_war_with = PREV
            }
            ROOT = {
                declare_war_on = {
                    target = PREV
                    type = annex_everything
                }
            }
        }
        
        # 处理进攻战
        every_country = {
            limit = {
                has_offensive_war_with = ROOT
            }
            declare_war_on = {
                target = ROOT
                type = annex_everything
            }
        }
    }
}
```

### 4.2 调用

```paradox
MY_revolution = {
    id = MY_revolution
    icon = GFX_goal_generic_propaganda
    x = 5
    y = 1
    cost = 70
    
    # 触发条件
    trigger = {
        NOT = { has_government = democratic }
    }
    
    completion_reward = {
        # 改变政体
        set_politics = {
            ruling_party = communist
            poll_priority = yes
        }
        
        # 继承战争
        MY_inherit_wars_effect = yes
        
        # 其他效果
        add_stability = -0.1
        add_war_support = 0.1
    }
}
```

---

## 示例五：组合脚本效果

### 场景
创建多个可组合的基础效果，然后组合成高级效果。

### 5.1 基础效果

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt

# ===== 基础效果1：增加人力 =====
MY_add_manpower_base = {
    add_manpower = 5000
    add_war_support = 0.02
}

# ===== 基础效果2：增加工业 =====
MY_add_industry_base = {
    add_extra_state_shared_building_slots = 2
    
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
        }
        add_building_construction = {
            type = industrial_complex
            level = 2
            instant_build = yes
        }
    }
}

# ===== 基础效果3：增加科研 =====
MY_add_research_base = {
    add_research_slot = 1
    add_tech_bonus = {
        name = MY_research_bonus
        bonus = 0.5
        uses = 1
        category = industry
    }
}
```

### 5.2 组合效果

```paradox
# ===== 组合效果1：全面增强 =====
MY_military_upgrade = {
    MY_add_manpower_base = yes
    MY_add_industry_base = yes
}

# ===== 组合效果2：科研优先 =====
MY_science_upgrade = {
    MY_add_research_base = yes
    MY_add_manpower_base = yes
}

# ===== 组合效果3：终极强化 =====
MY_ultimate_upgrade = {
    MY_add_manpower_base = yes
    MY_add_industry_base = yes
    MY_add_research_base = yes
    
    # 添加额外效果
    add_political_power = 100
    set_country_flag = MY_ultimate_upgrade_active
}
```

### 5.3 调用

```paradox
MY_national_effort = {
    id = MY_national_effort
    icon = GFX_goal_generic_production
    x = 3
    y = 0
    cost = 140  # 更长的时间
    
    # 选择分支
    completion_reward = {
        IF = {
            limit = {
                has_completed_focus = MY_military_path
            }
            MY_military_upgrade = yes
        }
        ELSE_IF = {
            limit = {
                has_completed_focus = MY_science_path
            }
            MY_science_upgrade = yes
        }
        ELSE = {
            MY_ultimate_upgrade = yes
        }
    }
}
```

---

## 示例六：事件中调用

### 6.1 定义效果

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt

MY_random_event_reward = {
    # 随机奖励
    random_list = {
        33 = {
            add_political_power = 50
            custom_effect_tooltip = MY_reward_political_power
        }
        33 = {
            add_manpower = 5000
            custom_effect_tooltip = MY_reward_manpower
        }
        33 = {
            add_civilian_factories = 1
            custom_effect_tooltip = MY_reward_factories
        }
    }
}
```

### 6.2 事件调用

```paradox
# 文件：events/MY_events.txt

country_event = {
    id = MY_events.1
    title = MY_national_crisis_title
    desc = MY_national_crisis_desc
    picture = GFX_event_generic_protest
    
    is_triggered_only = yes
    
    trigger = {
        tag = MY
        date > 1938.1.1
        NOT = { has_country_flag = MY_crisis_resolved }
    }
    
    option = {
        name = MY_resolve_by_military
        
        # 调用脚本效果
        MY_add_manpower_base = yes
        
        set_country_flag = MY_crisis_resolved
    }
    
    option = {
        name = MY_resolve_by_economy
        
        # 调用另一个脚本效果
        MY_add_industry_base = yes
        
        set_country_flag = MY_crisis_resolved
    }
}
```

---

## 示例七：决议中调用

### 7.1 定义效果

```paradox
# 文件：common/scripted_effects/MY_scripted_effects.txt

MY_emergency_measures = {
    # 临时效果
    add_war_support = 0.05
    
    # 消耗资源
    add_resource = {
        type = oil
        amount = -10
        state = 1
    }
    
    # 随机选择州进行建设
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
            NOT = { has_building = arms_factory }
        }
        add_building_construction = {
            type = arms_factory
            level = 1
            instant_build = yes
        }
    }
}
```

### 7.2 决议调用

```paradox
# 文件：common/decisions/MY_decisions.txt

MY_emergency_measures_decision = {
    name = MY_emergency_measures
    icon = generic_factory
    
    available = {
        has_war = yes
        has_resource = {
            type = oil
            amount > 10
            state = 1
        }
    }
    
    cost = 30
    days_remove = 60
    
    modifier = {
        consumer_goods_factor = 0.05
    }
    
    complete_effect = {
        MY_emergency_measures = yes
    }
}
```

---

## 常见错误检查

### ❌ 错误1：效果未定义
```paradox
# 错误：undefined_effect 未定义
completion_reward = {
    undefined_effect = yes
}

# 正确：先定义
undefined_effect = {
    add_political_power = 50
}
```

### ❌ 错误2：参数类型错误
```paradox
# 错误：category 必须是具体类别，不是变量
MY_grant_tech_bonus = {
    add_tech_bonus = {
        bonus = 0.5
        category = "tech_category"  # 引号是错误的
    }
}

# 正确：
add_tech_bonus = {
    bonus = 0.5
    category = industry
}
```

### ❌ 错误3：作用域混淆
```paradox
# 在国家 scope 中使用 random_owned_controlled_state
# ROOT 是国家，random 选择的是州
MY_effect = {
    random_owned_controlled_state = {
        # 这里 PREV = 州, ROOT = 国家
        add_manpower = 1000  # 错误：州没有人力概念
    }
}

# 正确：
MY_effect = {
    random_owned_controlled_state = {
        add_extra_state_shared_building_slots = 1  # 正确
    }
}
```

---

## 调试技巧

### 1. 分解复杂效果
```paradox
MY_debug_effect = {
    custom_effect_tooltip = MY_step_1
    hidden_effect = {
        set_country_flag = MY_step_1_done
    }
    
    custom_effect_tooltip = MY_step_2
    hidden_effect = {
        set_country_flag = MY_step_2_done
    }
}
```

### 2. 使用日志
```paradox
MY_logged_effect = {
    log = "MY_effect triggered!"
    add_political_power = 50
    log = "Added 50 political power"
}
```

### 3. 检查标志
```paradox
MY_conditional_effect = {
    if = {
        limit = {
            has_country_flag = MY_debug_flag
        }
        log = "Debug mode active!"
    }
    
    # 主要逻辑
    add_political_power = 50
}
```

---

**学习完成**: 你现在应该掌握了脚本效果的定义、调用和调试。

**下一步**: 学习脚本触发器 (Scripted Triggers)，了解可复用的条件判断。
