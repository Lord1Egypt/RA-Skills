# HOI4 动态修正 (Dynamic Modifiers) 完整示例

**版本**: 1.0
**更新**: 2026-04-24
**学习目标**: 掌握动态修正的定义和应用

---

## 示例一：国家级临时经济修正

### 场景
玩家完成"紧急经济刺激"国策后，获得一个持续180天的经济增益。

### 1.1 定义动态修正

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt
# 建议：一个mod一个文件，用 mod_前缀命名

MY_economic_stimulus = {
    # ===== 显示设置 =====
    icon = GFX_idea_generic_propaganda  # 图标（可选）
    
    # ===== 启用条件 =====
    # enable 块定义了何时启用此修正
    # 这里默认 always = yes，表示立即启用
    enable = {
        always = yes
    }
    
    # ===== 修正内容 =====
    # 这些值会在修正生效期间持续应用
    
    # 消费品工厂需求 -15%（减少民用生产占用）
    consumer_goods_factor = -0.15
    
    # 建筑速度 +20%
    production_speed_buildings_factor = 0.20
    
    # 工厂效率增长 +10%
    production_factory_efficiency_gain_factor = 0.10
}
```

### 1.2 在国策中应用

```paradox
# 文件：common/national_focus/MY_focus.txt

MY_emergency_stimulus = {
    # ===== 国策基础设置 =====
    id = MY_emergency_stimulus              # 唯一ID
    icon = GFX_goal_generic_production        # 图标
    x = 5                                    # X坐标
    y = 0                                    # Y坐标
    cost = 35                                # 耗时（天）
    
    # ===== 前置国策 =====
    prerequisite = {
        focus = MY_economic_reform          # 需要先完成经济改革
    }
    
    # ===== 互斥国策 =====
    mutually_exclusive = {
        focus = MY_austerity_policy          # 与紧缩政策二选一
    }
    
    # ===== 可用条件 =====
    available = {
        has_completed_focus = MY_economic_reform
    }
    
    # ===== 完成奖励 =====
    completion_reward = {
        # 添加动态修正，持续180天
        add_dynamic_modifier = {
            modifier = MY_economic_stimulus  # 引用上面定义的修正
            days = 180                        # 180天后自动移除
        }
        
        # 显示自定义提示
        custom_effect_tooltip = MY_economic_stimulus_tt
    }
}
```

### 1.3 添加本地化

```yaml
# 文件：localisation/english/MY_mod_l_english.yml
l_english:
 # 修正名称（显示在UI上）
 MY_economic_stimulus:0 "紧急经济刺激"
 
 # 修正描述
 MY_economic_stimulus_desc:0 "实施大规模财政刺激政策，促进工业扩张。"
 
 # 国策提示
 MY_economic_stimulus_tt:0 "获得180天的经济刺激效果：\n  • 消费品工厂需求 -15%\n  • 建筑速度 +20%\n  • 工厂效率增长 +10%"
```

---

## 示例二：州级占领惩罚

### 场景
占领敌方领土后，该州获得"抵抗活动"惩罚，持续到顺从度达到50%。

### 2.1 定义占领惩罚

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt

MY_occupation_resistance = {
    # ===== 显示 =====
    icon = GFX_modifiers_generic_occupation_resistance
    
    # ===== 修正内容 =====
    # 抵抗增长 +5%
    resistance_growth = 0.05
    
    # 抵抗目标 30%
    resistance_target = 0.30
    
    # 资源产出 -25%
    state_resources_factor = -0.25
    
    # 建筑速度 -15%
    state_production_speed_buildings_factor = -0.15
    
    # 禁止战略重部署（防止敌人从这里调动部队）
    disable_strategic_redeployment = 1
}
```

### 2.2 在国策中应用到州

```paradox
MY_occupy_territory = {
    id = MY_occupy_territory
    icon = GFX_goal_generic_propaganda
    x = 5
    y = 1
    cost = 35
    
    available = {
        has_war = yes                      # 需要在战争中
    }
    
    completion_reward = {
        # 随机选择一个占领的州
        random_owned_controlled_state = {
            # 限制：必须是核心领土（不是刚占领的）
            limit = {
                is_core_of = PREV
                NOT = { is_fully_controlled_by = ROOT }
            }
            
            # 添加占领抵抗惩罚
            add_dynamic_modifier = {
                modifier = MY_occupation_resistance
                # 不写 days 表示永久，直到 remove_trigger 触发
            }
            
            custom_effect_tooltip = MY_occupy_territory_tt
        }
        
        # 隐藏效果：设置标志
        hidden_effect = {
            set_country_flag = MY_has_occupied_territory
        }
    }
}
```

### 2.3 移除条件示例

```paradox
# 如果想要顺从度达标后自动移除，修改定义：

MY_occupation_resistance = {
    icon = GFX_modifiers_generic_occupation_resistance
    
    # 移除条件：当顺从度 > 50% 时移除
    remove_trigger = {
        compliance > 0.5
    }
    
    resistance_growth = 0.05
    resistance_target = 0.30
    state_resources_factor = -0.25
    state_production_speed_buildings_factor = -0.15
    disable_strategic_redeployment = 1
}
```

---

## 示例三：带变量的动态修正

### 场景
国策效果根据玩家选择增强或减弱修正强度。

### 3.1 定义（使用变量）

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt

MY_national_mobilization = {
    icon = GFX_idea_generic_mobilization
    
    # 建筑速度（从变量读取）
    production_speed_buildings_factor = MY_mobilization_speed_var
    
    # 消费品需求（从变量读取）
    consumer_goods_factor = MY_mobilization_consumer_var
    
    # 人力恢复（从变量读取）
    mobilizable_manpower_factor = MY_mobilization_manpower_var
}
```

### 3.2 国策效果

```paradox
MY_mobilization_focus = {
    id = MY_mobilization_focus
    icon = GFX_goal_generic_mobilization
    x = 3
    y = 0
    cost = 70
    
    # ===== 选择效果分支 =====
    # 方式1：使用 IF/ELSE 分支
    completion_reward = {
        IF = {
            limit = {
                has_completed_focus = MY_mobilization_light
            }
            # 轻度动员变量
            set_variable = {
                MY_mobilization_speed_var = 0.10
                MY_mobilization_consumer_var = -0.05
                MY_mobilization_manpower_var = 0.05
            }
        }
        ELSE_IF = {
            limit = {
                has_completed_focus = MY_mobilization_medium
            }
            # 中度动员变量
            set_variable = {
                MY_mobilization_speed_var = 0.20
                MY_mobilization_consumer_var = -0.10
                MY_mobilization_manpower_var = 0.10
            }
        }
        ELSE = {
            # 全力动员变量
            set_variable = {
                MY_mobilization_speed_var = 0.30
                MY_mobilization_consumer_var = -0.15
                MY_mobilization_manpower_var = 0.15
            }
        }
        
        # 应用动态修正（使用设置好的变量）
        add_dynamic_modifier = {
            modifier = MY_national_mobilization
        }
        
        custom_effect_tooltip = MY_mobilization_tt
    }
}
```

---

## 示例四：跨国家作用域

### 场景
联邦国家的核心国给成员添加修正。

### 4.1 定义

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt

MY_federation_support = {
    icon = GFX_idea_generic_alliance
    
    # 工业产能 +10%
    industrial_capacity_factory = 0.10
    
    # 研究速度 +5%
    research_speed_factor = 0.05
    
    # 军队组织度恢复 +5%
    army_org_factor = 0.05
}
```

### 4.2 联邦核心国国策

```paradox
MY_federation_grant_support = {
    id = MY_federation_grant_support
    icon = GFX_goal_generic_alliance
    x = 5
    y = 2
    cost = 35
    
    # 前置：需要联邦成立
    prerequisite = {
        focus = MY_federation_formed
    }
    
    available = {
        is_in_faction = yes
        any_allied_country = {
            NOT = { tag = ROOT }
            is_faction_leader = no  # 不是其他国家的领袖
        }
    }
    
    completion_reward = {
        # 添加到自己
        add_dynamic_modifier = {
            modifier = MY_federation_support
            scope = ROOT
        }
        
        # 隐藏效果：给所有盟友添加
        hidden_effect = {
            every_allied_country = {
                limit = {
                    NOT = { tag = ROOT }
                }
                add_dynamic_modifier = {
                    modifier = MY_federation_support
                    scope = ROOT  # 每个国家应用到自己
                }
            }
        }
        
        custom_effect_tooltip = MY_federation_support_tt
    }
}
```

---

## 示例五：临时战斗增益

### 场景
宣战后获得临时的战斗加成。

### 5.1 定义

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt

MY_war_morale_boost = {
    icon = GFX_idea_generic_war_propaganda
    
    # 攻击 +15%
    attack_factor = 0.15
    
    # 防御 +10%
    defense_factor = 0.10
    
    # 组织度 +5%
    organization_factor = 0.05
    
    # 移动速度 +10%
    movement_speed_factor = 0.10
}
```

### 5.2 事件触发

```paradox
# 文件：events/MY_war_events.txt

country_event = {
    id = MY_war_events.1
    title = MY_war_morale_boost_title
    desc = MY_war_morale_boost_desc
    picture = GFX_event_war
    
    is_triggered_only = yes
    
    trigger = {
        tag = MY
        has_war = yes
        NOT = { has_country_flag = MY_war_morale_flag }
    }
    
    option = {
        name = MY_war_morale_boost_accept
        
        # 获得临时战斗增益
        add_dynamic_modifier = {
            modifier = MY_war_morale_boost
            days = 90  # 90天后消失
        }
        
        # 设置标志（防止重复触发）
        set_country_flag = MY_war_morale_flag
        
        # 战争支持度 +10%
        add_war_support = 0.10
    }
}
```

---

## 示例六：完整国家修正系统

### 场景
创建一个完整的"战争经济"系统，包含多个动态修正和切换逻辑。

### 6.1 修正定义

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt

# ===== 平时经济 =====
MY_peace_economy = {
    icon = GFX_idea_generic_economic
    enable = { always = yes }
    
    consumer_goods_factor = -0.10
    production_speed_buildings_factor = 0.05
    research_speed_factor = 0.05
}

# ===== 动员经济 =====
MY_mobilization_economy = {
    icon = GFX_idea_generic_mobilization
    enable = { always = yes }
    
    consumer_goods_factor = -0.20
    production_speed_buildings_factor = 0.15
    research_speed_factor = -0.05
    
    army_org_factor = 0.10
}

# ===== 全面战争经济 =====
MY_total_war_economy = {
    icon = GFX_idea_generic_war_propaganda
    enable = { always = yes }
    
    consumer_goods_factor = -0.30
    production_speed_buildings_factor = 0.25
    research_speed_factor = -0.10
    
    army_org_factor = 0.15
    army_morale_factor = 0.10
}
```

### 6.2 国策切换

```paradox
# 文件：common/national_focus/MY_economy_focus.txt

MY_switch_to_mobilization = {
    id = MY_switch_to_mobilization
    icon = GFX_goal_generic_mobilization
    x = 2
    y = 0
    cost = 35
    
    available = {
        NOT = { has_country_flag = MY_mobilization_economy_active }
    }
    
    completion_reward = {
        # 移除旧的经济修正
        remove_dynamic_modifier = {
            modifier = MY_peace_economy
        }
        remove_dynamic_modifier = {
            modifier = MY_total_war_economy
        }
        
        # 添加新的经济修正
        add_dynamic_modifier = {
            modifier = MY_mobilization_economy
        }
        
        # 设置标志
        set_country_flag = MY_mobilization_economy_active
        clr_country_flag = MY_peace_economy_active
        clr_country_flag = MY_total_war_economy_active
        
        custom_effect_tooltip = MY_switched_to_mobilization_tt
    }
}

MY_switch_to_total_war = {
    id = MY_switch_to_total_war
    icon = GFX_goal_generic_war_propaganda
    x = 4
    y = 0
    cost = 70
    
    prerequisite = {
        focus = MY_switch_to_mobilization
    }
    
    available = {
        has_country_flag = MY_mobilization_economy_active
        NOT = { has_country_flag = MY_total_war_economy_active }
        has_war = yes
    }
    
    completion_reward = {
        # 移除旧的经济修正
        remove_dynamic_modifier = {
            modifier = MY_mobilization_economy
        }
        
        # 添加全面战争经济
        add_dynamic_modifier = {
            modifier = MY_total_war_economy
        }
        
        # 更新标志
        set_country_flag = MY_total_war_economy_active
        clr_country_flag = MY_mobilization_economy_active
        
        custom_effect_tooltip = MY_switched_to_total_war_tt
    }
}
```

---

## 示例七：指挥官动态修正

### 场景
将领获得特殊状态加成。

### 7.1 定义

```paradox
# 文件：common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt

MY_commander_inspired = {
    icon = GFX_idea_generic_military_command
    
    # 攻击 +0.5
    attack = 0.5
    
    # 防御 +0.5
    defense = 0.5
    
    # 组织度 +5
    organization = 5
    
    # 经验获取 +20%
    experience_gain_factor = 0.2
}
```

### 7.2 应用到指挥官

```paradox
# 通常在事件或决议中应用
effect = {
    # 随机选择一个将领
    random_unit_leader = {
        limit = {
            has_trait = clever
            unit_owner = { tag = ROOT }
        }
        
        # 添加动态修正到指挥官
        add_dynamic_modifier = {
            modifier = MY_commander_inspired
            days = 90
        }
        
        # 增加经验
        add_unit_leader_trait = {
            trait = MY_inspiring_leader
        }
    }
}
```

---

## 常见错误检查

### ❌ 错误1：忘记定义修正
```paradox
# 错误：修正未定义
add_dynamic_modifier = {
    modifier = MY_nonexistent_modifier
}

# 正确：先定义
# common/dynamic_modifiers/MY_MOD_dynamic_modifiers.txt
MY_nonexistent_modifier = {
    political_power_gain = 0.1
}
```

### ❌ 错误2：days 参数类型
```paradox
# 错误：字符串
days = "30"

# 正确：数字
days = 30
```

### ❌ 错误3：作用域拼写
```paradox
# 错误：引号
scope = "ROOT"

# 正确：无引号
scope = ROOT
```

### ❌ 错误4：修正冲突
```paradox
# 同一时间只能有一个同ID的动态修正
# 如果需要重新应用，先移除
remove_dynamic_modifier = { modifier = MY_modifier }
add_dynamic_modifier = { modifier = MY_modifier }
```

---

**学习完成**: 你现在应该掌握了动态修正的定义和应用。

**下一步**: 学习脚本效果 (Scripted Effects)，了解如何创建可复用的效果块。
