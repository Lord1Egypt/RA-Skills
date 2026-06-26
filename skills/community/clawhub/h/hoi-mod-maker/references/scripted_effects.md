# HOI4 脚本效果 (Scripted Effects) 完整语法参考

**版本**: 1.0
**更新**: 2026-04-24
**来源**: 游戏本体文件 + Paradox Wiki

---

## 一、概述

**脚本效果**是一种可重用的效果块定义，类似于编程语言中的函数或过程。

### 核心特点

- 📦 **可复用**：一次定义，多次使用
- 🔧 **可参数化**：支持输入参数
- 🌍 **作用域控制**：自动处理 ROOT/PREV/FROM 上下文
- 📁 **文件组织**：按国家或通用分类

### 与普通效果的区别

```paradox
# 普通效果：直接写在效果块中
completion_reward = {
    add_political_power = 100
    add_manpower = 5000
}

# 脚本效果：先定义，再调用
# 定义（common/scripted_effects/）
my_reward_effect = {
    add_political_power = 100
    add_manpower = 5000
}

# 调用
completion_reward = {
    my_reward_effect = yes
}
```

---

## 二、文件位置

```
common/
└── scripted_effects/
    ├── 00_scripted_effects.txt          # 通用脚本效果
    ├── GER_scripted_effects.txt          # 德国专用
    ├── FRA_scripted_effects.txt          # 法国专用
    ├── USA_scripted_effects.txt          # 美国专用
    └── ...其他国家的脚本效果
```

**建议**：通用效果放 `00_scripted_effects.txt`，国家特定的放对应文件。

---

## 三、定义语法

### 3.1 基础定义

```paradox
# 文件：common/scripted_effects/00_scripted_effects.txt

# ============================================
# 基础脚本效果
# ============================================

# 效果名称 = { 效果内容 }
my_first_effect = {
    # 这里写任何效果
    add_political_power = 50
    add_war_support = 0.05
}

# 效果可以包含多个步骤
complex_effect = {
    add_political_power = 100
    add_manpower = 5000
    set_country_flag = my_flag
    custom_effect_tooltip = my_effect_tt
}
```

### 3.2 带参数的效果

```paradox
# 文件：common/scripted_effects/00_scripted_effects.txt

# ============================================
# 带参数的效果（使用 [?] 语法）
# ============================================

# 参数名 = 默认值（可选）
add_n_resources = {
    # resource_type 参数，默认为 oil
    add_resource = {
        type = oil
        amount = 10
        state = PREV
    }
}

# 多个参数
grant_technology_bonus = {
    # tech_category 参数
    # bonus_amount 参数
    add_tech_bonus = {
        name = my_tech_bonus
        bonus = bonus_amount
        uses = 2
        category = tech_category
    }
}

# 在使用时传入参数
effect = {
    grant_technology_bonus = {
        tech_category = industry
        bonus_amount = 0.5
    }
}
```

### 3.3 完整示例

```paradox
# ============================================
# 完整示例：工厂转换效果
# ============================================

replace_civ_with_arms_factories = {
    # 随机选择5个有民用工厂的州
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

    # ... 重复5次
}
```

---

## 四、作用域系统

### 4.1 基础作用域

```paradox
# 脚本效果内部的作用域
my_effect = {
    # ROOT = 调用此效果时的当前作用域
    # 示例：在国家效果块中调用，ROOT = 国家
    ROOT = { add_political_power = 100 }
    
    # PREV = 上一个作用域
    # 示例：在州效果块中调用，PREV = 州
    PREV = { add_manpower = 1000 }
    
    # FROM = 触发效果的源头
    FROM = { has_war = yes }
}
```

### 4.2 实际应用

```paradox
# 文件：common/scripted_effects/00_scripted_effects.txt

# 国家 scope 中使用
give_money_and_pop = {
    # ROOT = 国家
    add_political_power = 50
    add_manpower = 5000
    add_civilian_factories = 1
}

# 州 scope 中使用
develop_state = {
    # PREV = 州
    add_extra_state_shared_building_slots = 2
    add_building_construction = {
        type = industrial_complex
        level = 2
        instant_build = yes
    }
}

# 复杂作用域
inherit_wars = {
    hidden_effect = {
        # 对所有与 PREV（当前作用域）处于防御战的国家
        every_country = {
            limit = {
                has_defensive_war_with = PREV
            }
            # ROOT = 这些国家
            ROOT = {
                # 对这些国家宣战
                declare_war_on = { target = PREV type = annex_everything }
            }
        }
        # 对所有与 ROOT 处于进攻战的国家
        every_country = {
            limit = {
                has_offensive_war_with = ROOT
            }
            # 宣战到 ROOT
            declare_war_on = { target = ROOT type = annex_everything }
        }
    }
}
```

---

## 五、调用语法

### 5.1 基本调用

```paradox
# 在国策/事件/决议中调用
completion_reward = {
    # 简单调用
    my_effect = yes
}

# 调用带参数的效果
completion_reward = {
    grant_technology_bonus = {
        tech_category = industry
        bonus_amount = 0.5
    }
}
```

### 5.2 在不同位置调用

```paradox
# 国策中调用
my_focus = {
    completion_reward = {
        replace_civ_with_arms_factories = yes
    }
}

# 事件中调用
country_event = {
    id = my_events.1
    option = {
        name = accept
        replace_civ_with_arms_factories = yes
    }
}

# 决议中调用
my_decision = {
    effect = {
        replace_civ_with_arms_factories = yes
    }
}

# 触发器中调用（通过 scripted_effect）
trigger = {
    has_completed_focus = MY_focus
    custom_trigger_tooltip = {
        tooltip = my_effect_tt
        my_scripted_effect = yes
    }
}
```

---

## 六、常用脚本效果库

### 6.1 工厂转换

```paradox
# 民用工厂转军用工厂（5个）
replace_civ_with_arms_factories = {
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
    # 重复5次...
}

# 军用工厂转民用工厂（3个）
replace_arms_with_civ_factories = {
    random_owned_controlled_state = {
        limit = {
            is_fully_controlled_by = ROOT
            arms_factory > 0
        }
        remove_building = {
            type = arms_factory
            level = 1
        }
        add_building_construction = {
            type = industrial_complex
            level = 1
            instant_build = yes
        }
    }
    # 重复3次...
}
```

### 6.2 AI 策略设置

```paradox
# 民主国家AI策略
GER_democratic_nations_ai_strategies = {
    # 减少对苏联的围堵
    add_ai_strategy = {
        type = contain
        id = "SOV"
        value = -800
    }
    # 保护波兰
    add_ai_strategy = {
        type = protect
        id = "POL"
        value = -200
    }
    # 忽视波兰
    add_ai_strategy = {
        type = ignore
        id = "POL"
        value = 200
    }
    # 联盟波兰
    add_ai_strategy = {
        type = alliance
        id = "POL"
        value = -200
    }
}
```

### 6.3 继承战争

```paradox
ROOT_inherit_current_scope_wars_effect = {
    custom_effect_tooltip = ROOT_inherit_current_scope_wars_effect
    hidden_effect = {
        # 防御战：继承方对敌人宣战
        every_country = {
            limit = {
                has_defensive_war_with = PREV
            }
            ROOT = { declare_war_on = { target = PREV type = annex_everything } }
        }
        # 进攻战：敌人对继承方宣战
        every_country = {
            limit = {
                has_offensive_war_with = PREV
            }
            declare_war_on = { target = ROOT type = annex_everything }
        }
    }
}
```

---

## 七、真实游戏代码示例

### 7.1 国策中的脚本效果

```paradox
# 文件：common/national_focus/usa.txt

USA_production_effort = {
    id = USA_production_effort
    icon = GFX_goal_generic_production
    x = 1
    y = 0
    cost = 35
    
    completion_reward = {
        # 调用脚本效果：5个民用工厂转军用工厂
        replace_civ_with_arms_factories = yes
    }
}
```

### 7.2 事件中的脚本效果

```paradox
# 文件：events/usa_events.txt

country_event = {
    id = usa_events.5
    title = USA_industrial_mobilization_title
    desc = USA_industrial_mobilization_desc
    
    is_triggered_only = yes
    
    trigger = {
        tag = USA
        has_completed_focus = USA_production_effort
    }
    
    option = {
        name = USA_mobilize_industry
        
        # 调用工厂转换效果
        replace_civ_with_arms_factories = yes
        
        # 添加额外效果
        add_war_support = 0.05
        add_political_power = 50
    }
}
```

### 7.3 决议中的脚本效果

```paradox
# 文件：common/decisions/usa_decisions.txt

USA_convert_factories = {
    name = USA_convert_factories
    icon = generic_factory
    
    available = {
        has_war = yes
    }
    
    cost = 35
    
    days_remove = 90
    
    modifier = {
        consumer_goods_factor = 0.10
    }
    
    complete_effect = {
        replace_civ_with_arms_factories = yes
    }
}
```

---

## 八、最佳实践

### 8.1 命名规范

```paradox
# 通用效果：以动词或功能命名
replace_civ_with_arms_factories = { ... }
give_money_and_pop = { ... }
setup_ai_strategies = { ... }

# 国家特定效果：以国家标签开头
GER_democratic_nations_ai_strategies = { ... }
FRA_develop_paris = { ... }
USA_manhattan_project = { ... }

# 带参数的效果：动词短语
add_n_factories_to_state = { ... }
grant_technology_bonus = { ... }
set_state_as_core = { ... }
```

### 8.2 作用域处理

```paradox
# ✅ 正确：明确使用 ROOT/PREV/FROM
my_effect = {
    ROOT = { add_political_power = 50 }
    every_owned_state = {
        PREV = { add_manpower = 1000 }
    }
}

# ❌ 避免：隐式作用域可能导致混淆
my_effect = {
    add_political_power = 50  # 作用域不明确
}
```

### 8.3 隐藏效果

```paradox
# 使用 hidden_effect 隐藏复杂的实现细节
my_effect = {
    custom_effect_tooltip = my_effect_tt
    
    hidden_effect = {
        # 复杂的内部逻辑
        set_variable = { my_var = 1 }
        add_to_variable = { my_var = 2 }
        set_country_flag = my_flag
    }
}
```

### 8.4 组合使用

```paradox
# 在脚本效果中调用其他脚本效果
common_upgrade = {
    replace_civ_with_arms_factories = yes
    add_extra_state_shared_building_slots = 1
}

special_upgrade = {
    # 调用基础效果
    common_upgrade = yes
    
    # 添加特殊效果
    add_research_slot = 1
    set_technology = {
        improved_infantry_weapons = 1
        tech_engineers = 1
    }
}
```

---

## 九、调试技巧

### 9.1 常见错误

```paradox
# ❌ 错误1：效果名称拼写错误
completion_reward = {
    my_effect = yes  # 如果 my_effect 未定义，会报错
}

# ❌ 错误2：参数缺失
my_effect = {
    add_resource = {
        type = resource_type  # 必须是具体类型，不是变量名
        amount = 10
        state = PREV
    }
}

# 正确：
add_resource = {
    type = oil
    amount = 10
    state = PREV
}

# ❌ 错误3：作用域引用错误
my_effect = {
    add_manpower = 1000  # 在国家 scope 中可以，但州 scope 中可能错误
}
```

### 9.2 调试方法

```paradox
# 1. 使用 custom_effect_tooltip 显示提示
my_effect = {
    custom_effect_tooltip = my_effect_tt
}

# 2. 使用日志输出
log = "Effect triggered!"

# 3. 分解复杂效果
complex_effect = {
    hidden_effect = {
        set_country_flag = debug_flag_1
    }
    custom_effect_tooltip = step_1_tt
    
    hidden_effect = {
        set_country_flag = debug_flag_2
    }
    custom_effect_tooltip = step_2_tt
}
```

---

## 十、相关文件关联

| 文件类型 | 位置 | 说明 |
|----------|------|------|
| 脚本效果定义 | `common/scripted_effects/*.txt` | 效果块的定义 |
| 国策奖励 | `common/national_focus/*.txt` | 常见的调用位置 |
| 事件效果 | `events/*.txt` | 事件中的调用 |
| 决议效果 | `common/decisions/*.txt` | 决议中的调用 |
| 脚本触发器 | `common/scripted_triggers/*.txt` | 类似的概念 |

---

**文档版本**: 1.0
**更新日期**: 2026-04-24
**维护者**: AI Agent (HOI Mod-Maker Skill)
