# HOI4 民族精神导入与使用完整示例

本文档详细展示如何在各种场景中导入、添加、移除民族精神。

---

## 📌 示例1：国策奖励中添加民族精神

### 1.1 基础添加

```hoi4
# === 国策：军事改革 ===
focus = {
    id = POL_military_reform
    x = 10
    y = 0
    cost = 10
    
    completion_reward = {
        # 方法1：直接添加
        add_ideas = POL_military_reform_spirit
        
        # 方法2：添加多个
        add_ideas = { 
            POL_military_reform_spirit
            POL_army_modernization
        }
    }
}

# === 民族精神定义（在ideas文件中）===
ideas = {
    POL_military_reform_spirit = {
        name = POL_military_reform_spirit
        picture = GFX_idea_POL_military_reform
        
        modifier = {
            army_org = 0.10              # 陆军组织度+10%
            defense_fact = 0.05          # 防御+5%
        }
    }
}
```

### 💡 关键说明

**`add_ideas`用法**:
- 单个：`add_ideas = idea_id`
- 多个：`add_ideas = { idea1 idea2 }`
- Ideas文件位置：`common/ideas/*.txt`

---

## 📌 示例2：事件中添加民族精神

### 2.1 永久添加

```hoi4
country_event = {
    id = poland.100
    title = poland.100.t
    desc = poland.100.d
    
    is_triggered_only = yes
    
    option = {
        name = poland.100.a
        
        # 永久添加民族精神
        add_ideas = POL_political_crisis
        
        # 添加稳定性修正
        add_stability = -0.10
    }
}
```

### 2.2 临时添加（定时移除）

```hoi4
country_event = {
    id = poland.110
    title = poland.110.t
    desc = poland.110.d
    
    is_triggered_only = yes
    
    option = {
        name = poland.110.a
        
        # 添加临时民族精神
        add_ideas = POL_emergency_measures
        
        # 添加定时移除标记
        set_country_flag = {
            flag = POL_emergency_measures_active
            days = 365    # 365天后移除
        }
        
        # 触发移除事件
        country_event = {
            id = poland.111
            days = 365
        }
    }
}

# === 移除事件 ===
country_event = {
    id = poland.111
    title = poland.111.t
    desc = poland.111.d
    
    is_triggered_only = yes
    
    option = {
        name = poland.111.a
        
        # 移除民族精神
        remove_ideas = POL_emergency_measures
        clr_country_flag = POL_emergency_measures_active
    }
}
```

### 2.3 使用 `add_timed_idea`

```hoi4
country_event = {
    id = poland.120
    title = poland.120.t
    desc = poland.120.d
    
    is_triggered_only = yes
    
    option = {
        name = poland.120.a
        
        # 直接添加定时民族精神
        add_timed_idea = {
            idea = POL_war_economy_temporary
            days = 730    # 730天（2年）
        }
    }
}

# === 定时民族精神定义（在ideas文件中）===
ideas = {
    POL_war_economy_temporary = {
        name = POL_war_economy_temporary
        picture = GFX_idea_war_economy
        
        modifier = {
            industrial_capacity_factory = 0.15
            consumer_goods = 0.05
        }
        
        # 注意：不需要removal_cost，因为会自动移除
    }
}
```

---

## 📌 示例3：条件民族精神

### 3.1 可用条件检查

```hoi4
# === 国策：强化工业 ===
focus = {
    id = POL_strengthen_industry
    x = 15
    y = 0
    cost = 10
    
    completion_reward = {
        # 条件：如果稳定度>50%，添加强化版
        if = {
            limit = { has_stability > 0.5 }
            add_ideas = POL_industrial_boost_strong
        }
        # 否则：添加普通版
        else = {
            add_ideas = POL_industrial_boost_weak
        }
    }
}
```

### 3.2 多级民族精神系统

```hoi4
# === 国策：工业化进程（三步）===

# 第一步
focus = {
    id = POL_industrialization_1
    x = 20
    y = 0
    cost = 10
    
    completion_reward = {
        add_ideas = POL_industrialization_level_1
        set_country_flag = POL_industrial_level_1
    }
}

# 第二步（升级）
focus = {
    id = POL_industrialization_2
    x = 20
    y = 1
    cost = 10
    prerequisite = { focus = POL_industrialization_1 }
    
    completion_reward = {
        # 移除低级版
        remove_ideas = POL_industrialization_level_1
        
        # 添加高级版
        add_ideas = POL_industrialization_level_2
        
        set_country_flag = POL_industrial_level_2
    }
}

# 第三步（最终）
focus = {
    id = POL_industrialization_3
    x = 20
    y = 2
    cost = 10
    prerequisite = { focus = POL_industrialization_2 }
    
    completion_reward = {
        remove_ideas = POL_industrialization_level_2
        add_ideas = POL_industrialization_level_3
        set_country_flag = POL_industrial_level_3
    }
}

# === Ideas定义 ===
ideas = {
    POL_industrialization_level_1 = {
        name = POL_industrialization_level_1
        picture = GFX_idea_generic_industry
        
        modifier = {
            industrial_capacity = 0.10
        }
    }
    
    POL_industrialization_level_2 = {
        name = POL_industrialization_level_2
        picture = GFX_idea_generic_industry
        
        modifier = {
            industrial_capacity = 0.20
            construction_speed = 0.10
        }
    }
    
    POL_industrialization_level_3 = {
        name = POL_industrialization_level_3
        picture = GFX_idea_generic_industry
        
        modifier = {
            industrial_capacity = 0.30
            construction_speed = 0.20
            production_factory_max_efficiency_factor = 0.10
        }
    }
}
```

---

## 📌 示例4：动态修饰符系统

### 4.1 添加动态修饰符

```hoi4
# === 国策：战争动员 ===
focus = {
    id = POL_war_mobilization
    x = 25
    y = 0
    cost = 10
    
    completion_reward = {
        # 添加动态修饰符
        add_dynamic_modifier = {
            modifier = POL_war_mobilization_modifier
            days = 365    # 可选：持续天数
        }
    }
}

# === 动态修饰符定义（在modifiers文件中）===
dynamic_modifiers = {
    POL_war_mobilization_modifier = {
        modifier = {
            mobilization_speed = 0.20
            attack_factor = 0.10
        }
        
        # 可选：显示条件
        visible = {
            has_war = yes
        }
    }
}
```

### 4.2 作用域限定动态修饰符

```hoi4
focus = {
    id = POL_state_industrialization
    x = 30
    y = 0
    cost = 10
    
    completion_reward = {
        # 对特定省份添加动态修饰符
        762 = {    # 上西里西亚省
            add_dynamic_modifier = {
                modifier = POL_state_industrial_boost
            }
        }
        
        # 对所有核心省份添加
        every_core_state = {
            limit = {
                is_owned_by = POL
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                }
            }
            add_dynamic_modifier = {
                modifier = POL_industrial_development
            }
        }
    }
}
```

---

## 📌 示例5：从其他Mod导入民族精神

### 5.1 基础导入

```hoi4
# === 在你的国策文件中 ===
focus = {
    id = MYC_focus_import
    x = 0
    y = 0
    cost = 10
    
    completion_reward = {
        # 直接添加其他Mod的idea（必须已加载）
        add_ideas = other_mod_idea_id
        
        # 添加条件检查
        if = {
            limit = { has_dlc = "DLC名称" }
            add_ideas = dlc_specific_idea
        }
    }
}
```

### 5.2 兼容性检查

```hoi4
focus = {
    id = MYC_compatible_focus
    x = 0
    y = 0
    cost = 10
    
    available = {
        # 检查Mod是否加载
        OR = {
            has_country_flag = other_mod_loaded
            has_dlc = "Some DLC"
        }
    }
    
    completion_reward = {
        # 安全添加
        if = {
            limit = { has_country_flag = other_mod_loaded }
            add_ideas = other_mod_idea
        }
    }
}
```

### 5.3 创建桥接文件

```hoi4
# === 创建文件：common/ideas/ZZZ_my_mod_bridge.txt ===
# （ZZZ前缀确保最后加载）

ideas = {
    # 重新定义或包装其他Mod的idea
    MYC_imported_idea = {
        name = MYC_imported_idea
        picture = GFX_idea_generic
        
        # 如果原Mod存在，使用原版
        # 否则使用替代版本
        
        modifier = {
            # 你的修正值
        }
    }
}
```

---

## 📌 示例6：民族精神的条件移除

### 6.1 定时移除（使用标记）

```hoi4
# === 初始添加 ===
country_event = {
    id = my_country.200
    
    option = {
        name = my_country.200.a
        add_ideas = MYC_temporary_boost
        set_country_flag = {
            flag = MYC_temporary_boost_active
            days = 180
        }
    }
}

# === 在on_actions中监听 ===
on_actions = {
    on_startup = {
        # 检查标记并移除
        every_country = {
            limit = {
                has_country_flag = MYC_temporary_boost_active
                NOT = { has_country_flag = { flag = MYC_temporary_boost_active days > 0 } }
            }
            remove_ideas = MYC_temporary_boost
        }
    }
}
```

### 6.2 条件自动移除

```hoi4
# === Ideas文件中定义自动移除 ===
ideas = {
    MYC_war_economy = {
        name = MYC_war_economy
        picture = GFX_idea_war_economy
        
        # === 自动移除条件 ===
        removal = {
            NOT = { has_war = yes }    # 不在战争中时移除
        }
        
        # === 移除效果（可选）===
        on_removal = {
            add_stability = -0.05    # 移除时损失稳定度
        }
        
        modifier = {
            mobilization_speed = 0.30
            consumer_goods = 0.05
        }
    }
}
```

### 6.3 国策主动移除

```hoi4
focus = {
    id = MYC_end_war_economy
    x = 35
    y = 0
    cost = 10
    
    available = {
        has_idea = MYC_war_economy
    }
    
    completion_reward = {
        remove_ideas = MYC_war_economy
        add_stability = 0.10    # 恢复稳定度
    }
}
```

---

## 📌 示例7：民族精神的效果提示定制

### 7.1 自定义效果提示

```hoi4
focus = {
    id = MYC_industrial_development
    x = 40
    y = 0
    cost = 10
    
    completion_reward = {
        # 添加民族精神
        add_ideas = MYC_industrial_boost
        
        # 自定义提示
        custom_effect_tooltip = MYC_industrial_boost_tt
        
        # 隐藏实际效果（避免重复显示）
        hidden_effect = {
            add_political_power = 100
            set_country_flag = MYC_industrial_developed
        }
    }
}
```

```yaml
# === 本地化文件 ===
l_english:
 MYC_industrial_boost_tt:0 "§YEffects:§!\n"
 MYC_industrial_boost_tt:0 "§G+10%§! Industrial Capacity\n"
 MYC_industrial_boost_tt:0 "§G+5%§! Construction Speed\n"
 MYC_industrial_boost_tt:0 "Gain §Y100§! Political Power"
```

### 7.2 显示民族精神提示

```hoi4
focus = {
    id = MYC_military_reform
    x = 45
    y = 0
    cost = 10
    
    # === 显示即将添加的民族精神 ===
    completion_reward = {
        show_ideas_tooltip = MYC_military_reform_spirit
        add_ideas = MYC_military_reform_spirit
    }
}
```

---

## 📌 示例8：多国共享民族精神

### 8.1 定义共享精神

```hoi4
# === 创建文件：common/ideas/shared_ideas.txt ===
ideas = {
    # === 可被多国使用的民族精神 ===
    shared_industrial_boom = {
        name = shared_industrial_boom
        picture = GFX_idea_generic_industry
        
        # === 允许所有国家使用 ===
        allowed = {
            always = yes
        }
        
        modifier = {
            industrial_capacity = 0.15
            construction_speed = 0.10
        }
    }
}
```

### 8.2 在不同国家国策中添加

```hoi4
# === 波兰国策 ===
focus = {
    id = POL_shared_industry
    completion_reward = {
        add_ideas = shared_industrial_boom
    }
}

# === 德国国策 ===
focus = {
    id = GER_shared_industry
    completion_reward = {
        add_ideas = shared_industrial_boom
    }
}
```

---

## 📝 完整工作流程示例

### 步骤1：定义民族精神

```hoi4
# 文件：common/ideas/my_country.txt
ideas = {
    MYC_special_spirit = {
        name = MYC_special_spirit
        picture = GFX_idea_my_country_special
        
        modifier = {
            political_power_gain = 0.10
            stability = 0.05
        }
    }
}
```

### 步骤2：添加本地化

```yaml
# 文件：localisation/english/ideas_l_english.yml
l_english:
 MYC_special_spirit:0 "National Spirit"
 MYC_special_spirit_desc:0 "Description of the national spirit."
```

### 步骤3：在国策中添加

```hoi4
# 文件：common/national_focus/my_country.txt
focus_tree = {
    id = my_country_tree
    country = {
        factor = 0
        modifier = {
            add = 100
            tag = MYC
        }
    }
    
    focus = {
        id = MYC_unlock_spirit
        x = 0
        y = 0
        cost = 10
        
        completion_reward = {
            add_ideas = MYC_special_spirit
        }
    }
}
```

---

## ✅ 最佳实践

### 1. 文件组织
```
common/
├── ideas/
│   ├── my_country.txt           # 国家特有精神
│   ├── shared_ideas.txt          # 共享精神
│   └── spirits/                   # 学说精神（可选）
│       ├── army_spirits.txt
│       ├── navy_spirits.txt
│       └── air_spirits.txt
```

### 2. 命名规范
```
{TAG}_{name}              # 国家前缀（永久精神）
{TAG}_{name}_temporary    # 临时后缀（定时移除）
{TAG}_{name}_level1       # 等级后缀（多级系统）
```

### 3. 平衡性建议
- 永久精神：修正值5-15%
- 临时精神：修正值15-30%
- 可移除精神：修正值10-20% + 移除成本

### 4. 性能优化
- 避免过于复杂的 `visible` 条件
- 使用 `removal` 自动移除而非频繁检查
- 临时精神优先使用 `add_timed_idea`

---

**恭喜！你已掌握 HOI4 民族精神导入与使用的核心用法！**
