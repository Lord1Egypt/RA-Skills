# HOI4 脚本触发器 (Scripted Triggers) 完整示例

**版本**: 1.0
**更新**: 2026-04-24
**学习目标**: 掌握脚本触发器的定义和调用

---

## 示例一：国家政体切换检查

### 场景
检查玩家是否可以切换到民主/法西斯/共产主义政体。

### 1.1 定义脚本触发器

```paradox
# 文件：common/scripted_triggers/00_scripted_triggers.txt

# ============================================
# 民主政体切换检查
# 排除所有不能切换到民主的国家
# ============================================

check_has_focus_tree_to_switch_to_democratic = {
    # ===== 排除特殊情况 =====
    
    # 满洲国不能切换
    NOT = { tag = MAN }
    
    # 主要大国不能切换
    NOT = { tag = FRA }
    NOT = { tag = USA }
    NOT = { tag = ENG }
    NOT = { tag = JAP }
    NOT = { tag = GER }
    NOT = { tag = SOV }
    
    # 英联邦国家不能切换
    NOT = { tag = CAN }
    NOT = { tag = SAF }
    NOT = { tag = AST }
    NOT = { tag = NZL }
    NOT = { tag = RAJ }
    NOT = { tag = CZE }
    
    # 特殊DLC处理：匈牙利
    NOT = {
        AND = {
            tag = HUN
            has_dlc = "Death or Dishonor"
        }
    }
}
```

### 1.2 在国策中使用

```paradox
# 文件：common/national_focus/MY_focus.txt

# ===== 民主路线 =====
MY_democratization = {
    id = MY_democratization
    icon = GFX_goal_generic_democracy
    x = 2
    y = 0
    cost = 35
    
    # ===== 可用条件 =====
    available = {
        # 使用脚本触发器
        check_has_focus_tree_to_switch_to_democratic = yes
    }
    
    # ===== 完成效果 =====
    completion_reward = {
        # 切换政体
        set_politics = {
            ruling_party = democratic
            elections_allowed = yes
        }
        
        add_political_power = 50
    }
}
```

---

## 示例二：州发展程度检查

### 场景
检查州是否有足够的基础设施和工厂。

### 2.1 定义

```paradox
# 文件：common/scripted_triggers/MY_scripted_triggers.txt

# ============================================
# 州发展程度检查
# ============================================

# 检查州是否有发展良好的基础设施
has_developed_infrastructure = {
    # 基础设施 > 3
    infrastructure > 3
    # 工业复合体 > 2
    industrial_complex > 2
}

# 检查州是否是核心州
is_core_state = {
    is_core_of = ROOT
}

# 检查州是否完全控制
is_fully_controlled_state = {
    is_fully_controlled_by = ROOT
}

# 组合检查
is_developed_core_state = {
    is_core_state = yes
    is_fully_controlled_state = yes
    has_developed_infrastructure = yes
}
```

### 2.2 在随机选择中使用

```paradox
MY_develop_state = {
    id = MY_develop_state
    icon = GFX_goal_generic_production
    x = 3
    y = 0
    cost = 70
    
    completion_reward = {
        # 随机选择一个符合条件的州
        random_owned_controlled_state = {
            # 限制：必须是发展良好的核心州
            limit = {
                is_developed_core_state = yes
            }
            
            # 添加建筑槽位
            add_extra_state_shared_building_slots = 2
            
            # 建造工业复合体
            add_building_construction = {
                type = industrial_complex
                level = 3
                instant_build = yes
            }
            
            custom_effect_tooltip = MY_develop_state_tt
        }
    }
}
```

---

## 示例三：国家关系检查

### 场景
检查国家之间的关系是否满足条件。

### 3.1 定义

```paradox
# 文件：common/scripted_triggers/MY_scripted_triggers.txt

# ============================================
# 关系检查
# ============================================

# 检查 ROOT 是否可以与 THIS 建立军事同盟
can_form_military_alliance = {
    # 目标存在
    exists = yes
    
    # 不在同一个阵营
    NOT = { is_in_faction_with = ROOT }
    
    # 不是仆从国
    NOT = { is_subject_of = ROOT }
    
    # 关系值 > 50
    opinion > 50
}

# 检查是否是与特定国家的盟友
is_ally_of_tag = {
    OR = {
        tag = target_tag
        is_in_faction_with = target_tag
        is_subject_of = target_tag
    }
}

# 检查是否在战争中
is_enemy_of_root = {
    OR = {
        has_war_with = ROOT
        AND = {
            is_in_faction_with = ROOT
            NOT = { tag = ROOT }
        }
    }
}
```

### 3.2 在国策中使用

```paradox
MY_alliance_offer = {
    id = MY_alliance_offer
    icon = GFX_goal_generic_alliance
    x = 4
    y = 1
    cost = 35
    
    # ===== 寻找可以结盟的国家 =====
    ai_will_do = {
        factor = 0
        modifier = {
            # AI 只在条件满足时执行
            any_country = {
                can_form_military_alliance = yes
            }
            factor = 1
        }
    }
    
    completion_reward = {
        # 找到符合条件的国家
        random_country = {
            limit = {
                can_form_military_alliance = yes
            }
            
            # 邀请加入阵营
            add_to_faction = THIS
            
            custom_effect_tooltip = MY_alliance_offer_tt
        }
    }
}
```

---

## 示例四：战争目标检查

### 场景
检查是否可以向特定国家发动战争。

### 4.1 定义

```paradox
# 文件：common/scripted_triggers/MY_scripted_triggers.txt

# ============================================
# 战争目标检查
# ============================================

# 检查 ROOT 是否可以对 THIS 发动战争目标
can_ROOT_get_wargoal_on_THIS = {
    # 目标存在
    exists = yes
    
    # 不在同一个阵营
    NOT = { is_in_faction_with = ROOT }
    
    # 不是仆从国
    NOT = { is_subject_of = ROOT }
}

# 检查是否在边界冲突中
is_border_conflict_defender_vs_FROM = {
    has_variable = ROOT.defender_state_vs_@FROM
}

# 检查是否已经发起了边境事件
has_not_initiated_border_incident_with_FROM = {
    # 使用 custom_trigger_tooltip 显示提示
    custom_trigger_tooltip = {
        tooltip = not_initiated_border_incident_with_FROM
        
        NOT = {
            any_state = {
                check_variable = {
                    FROM.defender_state_vs_@PREV = id
                }
            }
        }
    }
}
```

### 4.2 在决议中使用

```paradox
MY_border_incident = {
    name = MY_border_incident
    icon = generic_prepare_for_war
    
    available = {
        # 有潜在目标
        any_country = {
            can_ROOT_get_wargoal_on_THIS = yes
            is_on_continent = europe
        }
    }
    
    cost = 50
    
    days_remove = 30
    
    complete_effect = {
        random_country = {
            limit = {
                can_ROOT_get_wargoal_on_THIS = yes
                is_on_continent = europe
                NOT = { has_government = communism }
            }
            
            # 创建边境事件
            add_state_claim = {
                state = 123
                executor = ROOT
            }
            
            set_state_flag = MY_border_incident_target
        }
    }
}
```

---

## 示例五：军事单位检查

### 场景
检查是否在某个州有足够的部队。

### 5.1 定义

```paradox
# 文件：common/scripted_triggers/MY_scripted_triggers.txt

# ============================================
# 军事单位检查
# ============================================

# 检查 ROOT 在当前州是否有至少1个师
has_ROOT_at_least_1_div_in_current_state_scope = {
    custom_trigger_tooltip = {
        tooltip = at_least_one_division_in_state
        
        ROOT = {
            divisions_in_state = {
                state = PREV
                size > 0
            }
        }
    }
}

# 检查是否有足够的师（参数化）
has_n_divisions_in_state = {
    custom_trigger_tooltip = {
        tooltip = has_n_divisions_check
        
        ROOT = {
            divisions_in_state = {
                state = PREV
                size > division_count
            }
        }
    }
}
```

### 5.2 在国策中使用

```paradox
MY_offensive_preparation = {
    id = MY_offensive_preparation
    icon = GFX_goal_generic_army
    x = 3
    y = 0
    cost = 35
    
    available = {
        # 需要在边境州有至少5个师
        any_owned_state = {
            is_border_state = yes
            divisions_in_state = {
                size > 5
            }
        }
    }
    
    completion_reward = {
        # 给边境州增援
        every_owned_state = {
            limit = {
                is_border_state = yes
            }
            
            add_extra_state_shared_building_slots = 1
            add_manpower = 5000
        }
        
        add_war_support = 0.05
    }
}
```

---

## 示例六：组合触发器

### 场景
创建复杂的条件检查。

### 6.1 基础触发器

```paradox
# 文件：common/scripted_triggers/MY_scripted_triggers.txt

# ===== 基础条件 =====
has_sufficient_factories = {
    num_of_controlled_factories > 30
}

has_sufficient_manpower = {
    manpower > 100000
}

has_war_experience = {
    army_experience > 100
}

has_political_stability = {
    stability > 0.5
    war_support < 0.5
}

# ===== 组合条件 =====
can_launch_offensive = {
    has_sufficient_factories = yes
    has_sufficient_manpower = yes
    has_war_experience = yes
}

can_maintain_offensive = {
    has_political_stability = yes
    has_sufficient_factories = yes
}
```

### 6.2 在国策中使用

```paradox
MY_launch_offensive = {
    id = MY_launch_offensive
    icon = GFX_goal_generic_attack
    x = 3
    y = 1
    cost = 70
    
    prerequisite = {
        focus = MY_mobilize_forces
    }
    
    # ===== 可用条件 =====
    available = {
        can_launch_offensive = yes
    }
    
    # ===== 取消条件 =====
    cancel_if_invalid = yes
    continue_if_invalid = yes
    
    # ===== 完成效果 =====
    completion_reward = {
        # 应用进攻增益
        add_war_support = 0.1
        
        # 消耗经验
        army_experience = -100
        
        custom_effect_tooltip = MY_launch_offensive_tt
    }
}
```

---

## 示例七：事件触发条件

### 7.1 定义

```paradox
# 文件：common/scripted_triggers/MY_scripted_triggers.txt

# ============================================
# 事件触发条件
# ============================================

# 检查是否面临多线作战
is_fighting_multiple_wars = {
    custom_trigger_tooltip = {
        tooltip = fighting_multiple_wars
        
        OR = {
            AND = {
                is_in_war = yes
                any_enemy_state = {
                    NOT = { is_owned_by = PREV }
                }
            }
            AND = {
                is_in_war = yes
                is_actually_playing = yes
                check_variable = { MY_enemy_count > 1 }
            }
        }
    }
}

# 检查是否经济困难
is_economic_crisis = {
    custom_trigger_tooltip = {
        tooltip = economic_crisis_check
        
        AND = {
            consumer_goods_factor > 0.2
            stability < 0.6
            NOT = { has_government = fascism }
        }
    }
}
```

### 7.2 事件中使用

```paradox
# 文件：events/MY_events.txt

country_event = {
    id = MY_events.10
    title = MY_economic_crisis_title
    desc = MY_economic_crisis_desc
    picture = GFX_event_generic_protest
    
    # ===== 触发条件 =====
    trigger = {
        tag = MY
        date > 1938.1.1
        is_economic_crisis = yes
        NOT = { has_country_flag = MY_crisis_handled }
    }
    
    # ===== 事件时间 =====
    mean_time_to_happen = {
        months = 6
    }
    
    # ===== 选项 =====
    option = {
        name = MY_austerity_measures
        
        # 紧缩措施
        add_stability = 0.05
        add_war_support = -0.05
        add_political_power = -50
        
        set_country_flag = MY_crisis_handled
    }
    
    option = {
        name = MY_stimulus_measures
        
        # 刺激措施
        add_stability = -0.05
        add_war_support = 0.05
        add_political_power = 50
        
        set_country_flag = MY_crisis_handled
    }
}
```

---

## 常见错误检查

### ❌ 错误1：在触发器中使用效果
```paradox
# 错误：触发器不能有效果
my_trigger = {
    add_political_power = 50  # 错误！
}

# 正确：触发器只能有条件
my_trigger = {
    has_completed_focus = MY_focus
}
```

### ❌ 错误2：忘记参数
```paradox
# 错误：缺少参数
is_tag = {
    # 缺少 target_tag
}

# 正确：提供参数
is_tag = {
    target_tag = GER
}
```

### ❌ 错误3：作用域混淆
```paradox
# 在国家 scope 中使用州级触发器
my_focus = {
    available = {
        has_developed_infrastructure = yes  # 错误：没有州上下文
    }
}

# 正确：需要在州 scope 中使用
random_owned_controlled_state = {
    limit = {
        has_developed_infrastructure = yes  # 正确
    }
}
```

---

## 调试技巧

### 1. 使用 custom_trigger_tooltip
```paradox
my_trigger = {
    custom_trigger_tooltip = {
        tooltip = my_trigger_active
        has_completed_focus = MY_focus
    }
}
```

### 2. 分解复杂条件
```paradox
condition_a = {
    has_completed_focus = MY_focus_a
}

condition_b = {
    has_completed_focus = MY_focus_b
}

combined_condition = {
    OR = {
        condition_a = yes
        condition_b = yes
    }
}
```

### 3. 检查变量
```paradox
my_trigger = {
    custom_trigger_tooltip = {
        tooltip = var_check
        check_variable = { my_var > 10 }
    }
}
```

---

**学习完成**: 你现在应该掌握了脚本触发器的定义、调用和调试。

**下一步**: 继续完善其他模块，或返回主 SKILL.md 查看完整的学习路径。
