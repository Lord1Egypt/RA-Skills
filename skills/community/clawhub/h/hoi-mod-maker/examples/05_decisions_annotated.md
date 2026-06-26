# HOI4 决议系统完整示例

本文档展示决议系统的所有关键用法，包括类别、条件、效果等。

---

## 📌 示例1：基础决议结构

```hoi4
# === 决议类别定义 ===
decisions = {
    category = {
        name = POL_industrial_development
        icon = GFX_goal_generic_construct_civ_factory
    }
}

# === 决议类别引用 ===
POL_industrial_development = {
    # === 决议1：建设工厂 ===
    POL_construct_factory = {
        icon = GFX_goal_generic_construct_civ_factory
        
        # === 可用条件 ===
        available = {
            tag = POL
            has_political_power > 50
        }
        
        # === 显示条件 ===
        visible = {
            has_completed_focus = POL_industrial_base
        }
        
        # === 成本 ===
        cost = 50
        
        # === 移除条件 ===
        remove = {
            has_war_with = GER
        }
        
        # === 完成效果 ===
        complete_effect = {
            add_political_power = -50
            
            random_owned_state = {
                limit = {
                    free_building_slots = {
                        building = industrial_complex
                        size > 0
                    }
                }
                add_building_construction = {
                    type = industrial_complex
                    level = 1
                    instant_build = yes
                }
            }
        }
        
        # === AI权重 ===
        ai_will_do = {
            factor = 1
        }
    }
}
```

### 💡 关键说明

**决议类别**:
- `name`: 类别ID（用于引用）
- `icon`: 类别图标

**`available` vs `visible`**:
- `available`: 可执行条件（满足才能点击）
- `visible`: 显示条件（满足才显示）

**`remove`字段**:
- 满足条件时自动移除决议
- 常用于一次性决议

---

## 📌 示例2：带状态的决议

```hoi4
POL_political_decisions = {
    # === 决议：镇压罢工 ===
    POL_suppress_strike = {
        icon = GFX_goal_generic_major_alliance
        
        available = {
            tag = POL
            has_country_flag = POL_peasants_strike_active
            has_political_power > 100
        }
        
        visible = {
            has_country_flag = POL_peasants_strike_active
        }
        
        cost = 100
        
        # === 完成效果 ===
        complete_effect = {
            add_political_power = -100
            add_stability = 0.05
            
            # 移除罢工精神
            remove_ideas = POL_peasants_strike
            
            # 清除标记
            clr_country_flag = POL_peasants_strike_active
            
            # 触发事件
            country_event = {
                id = poland.200
                days = 7
            }
        }
        
        # === 重新可用条件 ===
        activation = {
            has_country_flag = POL_peasants_strike_active
        }
        
        # === 超时移除 ===
        timeout = {
            days = 60
            remove_effect = {
                add_stability = -0.10
                country_event = { id = poland.201 }
            }
        }
        
        ai_will_do = {
            factor = 5
            modifier = {
                factor = 0
                has_war = yes
            }
        }
    }
}
```

### 💡 关键说明

**`activation`字段**:
- 决议重新激活的条件
- 完成后检查此条件决定是否再次可用

**`timeout`字段**:
- 决议超时天数
- `remove_effect`: 超时执行的效果
- 用于紧急决议

---

## 📌 示例3：多选一决议

```hoi4
POL_economic_reforms = {
    # === 决议：经济政策选择 ===
    POL_choose_economic_policy = {
        icon = GFX_goal_generic_industry_expansion
        
        available = {
            tag = POL
            has_political_power > 150
        }
        
        visible = {
            NOT = {
                has_country_flag = POL_economic_policy_chosen
            }
        }
        
        cost = 150
        
        complete_effect = {
            # 显示选项事件
            country_event = { id = poland.300 }
        }
        
        ai_will_do = {
            factor = 3
        }
    }
    
    # === 决议：自由市场 ===
    POL_free_market = {
        icon = GFX_goal_generic_free_trade
        
        available = {
            tag = POL
            has_country_flag = POL_free_market_available
            has_political_power > 50
        }
        
        visible = {
            has_country_flag = POL_free_market_available
        }
        
        cost = 50
        
        complete_effect = {
            add_political_power = -50
            
            add_ideas = POL_free_market_economy
            
            clr_country_flag = POL_free_market_available
            set_country_flag = POL_economic_policy_chosen
        }
        
        ai_will_do = {
            factor = 1
        }
    }
    
    # === 决议：计划经济 ===
    POL_planned_economy = {
        icon = GFX_goal_generic_rapid_mobilization
        
        available = {
            tag = POL
            has_country_flag = POL_planned_economy_available
            has_political_power > 50
        }
        
        visible = {
            has_country_flag = POL_planned_economy_available
        }
        
        cost = 50
        
        complete_effect = {
            add_political_power = -50
            
            add_ideas = POL_planned_economy
            
            clr_country_flag = POL_planned_economy_available
            set_country_flag = POL_economic_policy_chosen
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                add = 2
                has_government = communism
            }
        }
    }
}
```

### 💡 关键说明

**决议互斥实现**:
- 使用标记控制可见性
- 完成一个决议后设置标记
- 其他决议检查此标记

**AI权重修正**:
- 根据意识形态调整权重
- 使AI选择符合国家情况的决议

---

## 📌 示例4：省份决议

```hoi4
# === 省份决议类别 ===
POL_state_development = {
    # === 决议：工业投资 ===
    POL_invest_in_state = {
        icon = GFX_goal_generic_construct_civ_factory
        
        # === 省份目标 ===
        targeted = yes    # 标记为省份决议
        
        available = {
            tag = POL
            FROM = {
                is_owned_by = POL
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                    include_locked = yes
                }
            }
            has_political_power > 100
        }
        
        visible = {
            FROM = {
                is_owned_by = POL
                is_core_of = POL
            }
        }
        
        cost = 100
        
        complete_effect = {
            add_political_power = -100
            
            FROM = {
                add_extra_state_shared_building_slots = 1
                add_building_construction = {
                    type = industrial_complex
                    level = 1
                    instant_build = yes
                }
            }
        }
        
        ai_will_do = {
            factor = 2
        }
    }
    
    # === 决议：基础设施投资 ===
    POL_invest_infrastructure = {
        icon = GFX_goal_generic_construct_infrastructure
        
        targeted = yes
        
        available = {
            tag = POL
            FROM = {
                is_owned_by = POL
                infrastructure < 5
            }
            has_political_power > 50
        }
        
        visible = {
            FROM = {
                is_owned_by = POL
            }
        }
        
        cost = 50
        
        complete_effect = {
            add_political_power = -50
            
            FROM = {
                add_building_construction = {
                    type = infrastructure
                    level = 1
                    instant_build = yes
                }
            }
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 2
                FROM = {
                    infrastructure < 3
                }
            }
        }
    }
}
```

### 💡 关键说明

**`targeted = yes`**:
- 标记为省份决议
- 玩家需要先选择目标省份
- `FROM` 指向选中的省份

**`FROM`作用域**:
- 在省份决议中指向目标省份
- 可检查省份状态并执行省份效果

---

## 📌 示例5：外交决议

```hoi4
POL_diplomatic_decisions = {
    # === 决议：加强关系 ===
    POL_strengthen_relations = {
        icon = GFX_goal_generic_diplomatic_talks
        
        targeted = yes    # 国家目标
        
        available = {
            tag = POL
            FROM = {
                NOT = { tag = POL }
                is_major = yes
            }
            has_political_power > 75
        }
        
        visible = {
            FROM = {
                NOT = { has_war_with = POL }
            }
        }
        
        cost = 75
        
        complete_effect = {
            add_political_power = -75
            
            FROM = {
                add_opinion_modifier = {
                    target = POL
                    modifier = improved_relations
                }
            }
            
            # 减少外交影响力消耗
            set_country_flag = {
                flag = POL_good_relations_with_FROM
                days = 365
            }
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 0
                FROM = {
                    has_opinion = {
                        target = POL
                        value > 50
                    }
                }
            }
        }
    }
    
    # === 决议：索取领土 ===
    POL_demand_territory = {
        icon = GFX_goal_generic_territory_or_war
        
        targeted = yes
        
        available = {
            tag = POL
            FROM = {
                is_neighbor_of = POL
                NOT = { is_in_faction = yes }
            }
            has_political_power > 150
            has_war = no
        }
        
        visible = {
            FROM = {
                any_owned_state = {
                    is_claimed_by = POL
                }
            }
        }
        
        cost = 150
        
        complete_effect = {
            # 触发领土要求事件
            FROM = {
                country_event = { id = poland.400 }
            }
        }
        
        ai_will_do = {
            factor = 2
            modifier = {
                add = 2
                FROM = {
                    is_subject_of = POL
                }
            }
        }
    }
}
```

### 💡 关键说明

**国家目标决议**:
- `targeted = yes` 标记为国家目标
- 玩家需选择目标国家
- `FROM` 指向目标国家

**外交效果**:
- `add_opinion_modifier`: 添加关系修正
- 可触发外交事件

---

## 📌 示例6：可升级决议

```hoi4
POL_military_buildup = {
    # === 决议：军事建设（等级1）===
    POL_military_effort_1 = {
        icon = GFX_goal_generic_military
        
        available = {
            tag = POL
            has_political_power > 50
            NOT = { has_country_flag = POL_military_effort_1 }
        }
        
        visible = {
            tag = POL
        }
        
        cost = 50
        
        complete_effect = {
            add_political_power = -50
            army_experience = 25
            set_country_flag = POL_military_effort_1
        }
        
        ai_will_do = {
            factor = 2
        }
    }
    
    # === 决议：军事建设（等级2）===
    POL_military_effort_2 = {
        icon = GFX_goal_generic_military
        
        available = {
            tag = POL
            has_country_flag = POL_military_effort_1
            has_political_power > 100
            NOT = { has_country_flag = POL_military_effort_2 }
        }
        
        visible = {
            has_country_flag = POL_military_effort_1
        }
        
        cost = 100
        
        complete_effect = {
            add_political_power = -100
            army_experience = 50
            add_ideas = POL_military_advisor
            set_country_flag = POL_military_effort_2
        }
        
        ai_will_do = {
            factor = 2
        }
    }
    
    # === 决议：军事建设（等级3）===
    POL_military_effort_3 = {
        icon = GFX_goal_generic_military
        
        available = {
            tag = POL
            has_country_flag = POL_military_effort_2
            has_political_power > 150
            has_war = yes
        }
        
        visible = {
            has_country_flag = POL_military_effort_2
        }
        
        cost = 150
        
        complete_effect = {
            add_political_power = -150
            army_experience = 100
            add_ideas = POL_military_buildup_complete
            set_country_flag = POL_military_effort_3
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 3
                has_war = yes
            }
        }
    }
}
```

### 💡 关键说明

**升级机制**:
- 完成低级决议设置标记
- 高级决议检查标记作为前置
- 逐步解锁更强效果

**AI逻辑**:
- 低级决议更容易完成
- 高级决议需要条件更严格
- 战争状态下更倾向于军事建设

---

## 📝 本地化示例

```yaml
l_english:
 # === 决议类别 ===
 POL_industrial_development:0 "Polish Industrial Development"
 
 # === 决议名称 ===
 POL_construct_factory:0 "Construct Factory"
 POL_construct_factory_desc:0 "Build a civilian factory in our core territories."
 
 POL_suppress_strike:0 "Suppress the Strike"
 POL_suppress_strike_desc:0 "The peasants' strike must be ended by force if necessary."
 
 # === 效果提示 ===
 POL_military_effort_tt:0 "§YGain Military Experience§!"
```

---

## ✅ 最佳实践

### 1. 决议类型选择
| 类型 | 用途 | 特点 |
|------|------|------|
| 普通决议 | 国家级行动 | 无需选择目标 |
| 省份决议 | 建设开发 | `targeted = yes` |
| 外交决议 | 外交行动 | `targeted = yes` |

### 2. 条件设计
- `available`: 可执行条件（运行时检查）
- `visible`: 显示条件（UI过滤）
- `remove`: 移除条件（自动清理）

### 3. 效果设计
- `complete_effect`: 完成效果
- `remove_effect`: 移除效果
- `timeout`: 超时效果

---

**恭喜！你已掌握决议系统的核心用法！**
