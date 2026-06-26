# HOI4 脚本触发器 (Scripted Triggers) 完整语法参考

**版本**: 1.0
**更新**: 2026-04-24
**来源**: 游戏本体文件 + Paradox Wiki

---

## 一、概述

**脚本触发器**是一种可重用的条件判断块，类似于编程语言中的函数或布尔表达式。

### 核心特点

- 🔍 **可复用**：一次定义，多次使用
- 🔧 **可参数化**：支持输入参数
- 🌍 **作用域控制**：自动处理 ROOT/PREV/FROM 上下文
- 📁 **文件组织**：按国家或通用分类

### 与脚本效果的区别

| 特性 | 脚本效果 | 脚本触发器 |
|------|----------|------------|
| **返回值** | 无（执行操作） | 布尔值（true/false） |
| **用途** | 执行一系列效果 | 检查条件是否满足 |
| **使用位置** | 效果块、触发器块 | 触发器块、limit 块 |

### 与普通触发器的区别

```paradox
# 普通触发器：直接写在触发器块中
available = {
    has_completed_focus = MY_focus
    num_of_controlled_factories > 50
}

# 脚本触发器：先定义，再调用
# 定义（common/scripted_triggers/）
my_condition = {
    has_completed_focus = MY_focus
    num_of_controlled_factories > 50
}

# 调用
available = {
    my_condition = yes
}
```

---

## 二、文件位置

```
common/
└── scripted_triggers/
    ├── 00_scripted_triggers.txt          # 通用脚本触发器
    ├── GER_scripted_triggers.txt          # 德国专用
    ├── FRA_scripted_triggers.txt          # 法国专用
    └── ...其他国家的脚本触发器
```

**建议**：通用触发器放 `00_scripted_triggers.txt`，国家特定的放对应文件。

---

## 三、定义语法

### 3.1 基础定义

```paradox
# 文件：common/scripted_triggers/00_scripted_triggers.txt

# ============================================
# 基础脚本触发器
# ============================================

# 触发器名称 = { 条件内容 }
my_first_trigger = {
    # 这里写任何触发器条件
    has_completed_focus = MY_focus
    has_war = no
}

# 触发器可以包含多个条件（AND 关系）
complex_trigger = {
    has_completed_focus = MY_focus
    NOT = { has_country_flag = MY_flag }
    num_of_controlled_factories > 10
}
```

### 3.2 带参数触发器

```paradox
# ============================================
# 带参数的触发器
# ============================================

# 检查国家是否有特定标签
is_tag = {
    tag = target_tag
}

# 检查是否在特定洲
is_on_continent_check = {
    is_on_continent = target_continent
}

# 在使用时传入参数
trigger = {
    is_tag = {
        target_tag = GER
    }
}
```

### 3.3 复杂条件

```paradox
# ============================================
# 复杂条件示例
# ============================================

# 检查是否可以切换到民主政体
check_has_focus_tree_to_switch_to_democratic = {
    # 排除不能切换的国家
    NOT = { tag = MAN }
    NOT = { tag = FRA }
    NOT = { tag = USA }
    NOT = { tag = ENG }
    NOT = { tag = CAN }
    NOT = { tag = SAF }
    NOT = { tag = AST }
    NOT = { tag = NZL }
    NOT = { tag = RAJ }
    NOT = { tag = CZE }
    
    # DLC 相关排除
    NOT = {
        AND = {
            tag = JAP
            has_dlc = "Waking the Tiger"
        }
    }
    NOT = {
        AND = {
            tag = GER
            has_dlc = "Waking the Tiger"
        }
    }
}
```

---

## 四、作用域系统

### 4.1 基础作用域

```paradox
# 脚本触发器内部的作用域
my_trigger = {
    # ROOT = 调用此触发器时的当前作用域
    # 示例：在国家触发器中调用，ROOT = 国家
    ROOT = { has_war = yes }
    
    # THIS = 触发器定义所在的对象
    THIS = { is_controlled_by = ROOT }
    
    # FROM = 触发效果的源头
    FROM = { has_war = yes }
}
```

### 4.2 实际应用

```paradox
# 国家 scope 中使用
can_switch_to_democratic = {
    NOT = { tag = MAN }
    has_completed_focus = MY_democratic_path
}

# 州 scope 中使用
has_developed_infrastructure = {
    infrastructure > 3
    industrial_complex > 2
}

# 限制块中使用
random_owned_controlled_state = {
    limit = {
        # 这里可以使用脚本触发器
        has_developed_infrastructure = yes
    }
}
```

---

## 五、调用语法

### 5.1 基本调用

```paradox
# 在触发器块中调用
available = {
    my_trigger = yes
}

# 调用带参数的效果
trigger = {
    is_tag = {
        target_tag = GER
    }
}
```

### 5.2 在不同位置调用

```paradox
# 国策可用条件
my_focus = {
    available = {
        my_trigger = yes
    }
}

# 限制块（limit）
random_owned_controlled_state = {
    limit = {
        my_state_trigger = yes
    }
}

# 事件触发条件
country_event = {
    trigger = {
        my_trigger = yes
    }
}

# 决议条件
my_decision = {
    available = {
        my_trigger = yes
    }
}
```

---

## 六、常用脚本触发器库

### 6.1 国策树切换检查

```paradox
# 检查是否可以切换到特定政体
check_has_focus_tree_to_switch_to_democratic = {
    NOT = { tag = MAN }
    NOT = { tag = FRA }
    NOT = { tag = USA }
    NOT = { tag = ENG }
    NOT = { tag = JAP }
    NOT = { tag = GER }
    NOT = { tag = SOV }
    # ... 更多排除
}

check_has_focus_tree_to_switch_to_fascism = {
    NOT = { tag = JAP }
    NOT = { tag = GER }
    NOT = { tag = MAN }
    # ...
}

check_has_focus_tree_to_switch_to_communism = {
    NOT = { tag = PRC }
    NOT = { tag = SIK }
    NOT = { tag = MAN }
    NOT = { tag = SOV }
    # ...
}
```

### 6.2 关系检查

```paradox
# 检查 ROOT 是否可以对 THIS 发动战争目标
can_ROOT_get_wargoal_on_THIS = {
    exists = yes
    NOT = { is_in_faction_with = ROOT }
    NOT = { is_subject_of = ROOT }
}

# 检查是否是与 JAP 的盟友
is_JAP_or_ally_of_JAP = {
    OR = {
        tag = JAP
        is_in_faction_with = JAP
        is_subject_of = JAP
    }
}
```

### 6.3 边界冲突

```paradox
# 检查是否是边界冲突的防御方
is_border_conflict_defender_vs_FROM = {
    has_variable = ROOT.defender_state_vs_@FROM
}

# 检查是否发起了边境事件
has_not_initiated_border_incident_with_FROM = {
    custom_trigger_tooltip = {
        tooltip = not_initiated_border_incident_with_FROM
        NOT = {
            any_state = {
                check_variable = { FROM.defender_state_vs_@PREV = id }
            }
        }
    }
}
```

### 6.4 军事单位检查

```paradox
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
```

---

## 七、真实游戏代码示例

### 7.1 国策中的脚本触发器

```paradox
# 文件：common/national_focus/MY_focus.txt

MY_democratic_path = {
    id = MY_democratic_path
    icon = GFX_goal_generic_democracy
    x = 2
    y = 0
    cost = 35
    
    # 使用脚本触发器检查是否可用
    available = {
        check_has_focus_tree_to_switch_to_democratic = yes
    }
    
    completion_reward = {
        add_political_power = 50
    }
}

MY_fascist_path = {
    id = MY_fascist_path
    icon = GFX_goal_generic_fascism
    x = 4
    y = 0
    cost = 35
    
    available = {
        check_has_focus_tree_to_switch_to_fascism = yes
    }
    
    completion_reward = {
        add_political_power = 50
    }
}
```

### 7.2 限制块中的脚本触发器

```paradox
MY_national_effort = {
    id = MY_national_effort
    icon = GFX_goal_generic_production
    x = 3
    y = 1
    cost = 70
    
    prerequisite = {
        focus = MY_democratic_path
        focus = MY_fascist_path
    }
    
    completion_reward = {
        # 选择发展最好的州进行强化
        random_owned_controlled_state = {
            # 使用脚本触发器作为限制
            limit = {
                has_developed_infrastructure = yes
                is_fully_controlled_by = ROOT
            }
            
            add_extra_state_shared_building_slots = 2
            add_building_construction = {
                type = industrial_complex
                level = 2
                instant_build = yes
            }
        }
    }
}
```

### 7.3 事件中的脚本触发器

```paradox
# 文件：events/MY_events.txt

country_event = {
    id = MY_events.1
    title = MY_border_conflict_title
    
    # 使用脚本触发器作为触发条件
    trigger = {
        is_border_conflict_defender_vs_FROM = yes
    }
    
    mean_time_to_happen = {
        days = 30
    }
    
    option = {
        name = MY_escalate
        
        # 检查是否可以升级
        if = {
            limit = {
                is_border_conflict_defender_vs_FROM = yes
            }
            add_war_support = 0.05
        }
    }
}
```

---

## 八、最佳实践

### 8.1 命名规范

```paradox
# 通用触发器：描述性动词短语
can_switch_to_democratic = { ... }
has_developed_infrastructure = { ... }
is_border_conflict_defender = { ... }

# 国家特定触发器：以国家标签开头
GER_can_use_naval_treaty = { ... }
FRA_has_parliament_approval = { ... }
USA_can_declare_war = { ... }

# 带参数的触发器：动词短语
is_tag = { ... }
has_completed_focus = { ... }
is_on_continent_check = { ... }
```

### 8.2 组合使用

```paradox
# 使用 OR 组合
can_do_action = {
    OR = {
        my_trigger_1 = yes
        my_trigger_2 = yes
        my_trigger_3 = yes
    }
}

# 使用 AND 组合（默认）
can_do_action = {
    my_trigger_1 = yes
    my_trigger_2 = yes
    my_trigger_3 = yes
}

# 否定
cannot_do_action = {
    NOT = {
        my_trigger = yes
    }
}
```

### 8.3 避免的问题

```paradox
# ❌ 避免：过于复杂的触发器
too_complex = {
    OR = {
        AND = {
            condition1 = yes
            condition2 = yes
        }
        AND = {
            condition3 = yes
            NOT = { condition4 = yes }
        }
    }
}

# ✅ 推荐：分解为多个简单触发器
simple_condition_1 = {
    condition1 = yes
    condition2 = yes
}

simple_condition_2 = {
    condition3 = yes
    NOT = { condition4 = yes }
}

can_do_action = {
    OR = {
        simple_condition_1 = yes
        simple_condition_2 = yes
    }
}
```

### 8.4 性能优化

```paradox
# ❌ 避免：性能开销大的检查
expensive_check = {
    any_state = {
        check_variable = { var = 1 }
    }
}

# ✅ 推荐：使用 custom_trigger_tooltip 包装
has_variable_check = {
    custom_trigger_tooltip = {
        tooltip = has_variable_check_desc
        NOT = {
            any_state = {
                check_variable = { var = 1 }
            }
        }
    }
}
```

---

## 九、调试技巧

### 9.1 常见错误

```paradox
# ❌ 错误1：触发器名称拼写错误
available = {
    my_triger = yes  # 拼写错误！
}

# ❌ 错误2：参数缺失
is_tag = {
    # 缺少 target_tag 参数
}

# ❌ 错误3：作用域错误
my_trigger = {
    add_manpower = 1000  # 错误：触发器不能有效果！
}
```

### 9.2 调试方法

```paradox
# 1. 使用 custom_trigger_tooltip 显示条件
my_debug_trigger = {
    custom_trigger_tooltip = {
        tooltip = my_trigger_desc
        # 实际条件
        has_completed_focus = MY_focus
    }
}

# 2. 分解复杂条件
condition_1 = {
    has_completed_focus = MY_focus
}

condition_2 = {
    num_of_controlled_factories > 10
}

can_do_action = {
    condition_1 = yes
    condition_2 = yes
}
```

---

## 十、相关文件关联

| 文件类型 | 位置 | 说明 |
|----------|------|------|
| 脚本触发器定义 | `common/scripted_triggers/*.txt` | 触发器块的定义 |
| 国策可用条件 | `common/national_focus/*.txt` | 常见的调用位置 |
| 限制块 | `common/national_focus/*.txt` | 随机选择限制 |
| 事件触发 | `events/*.txt` | 事件触发条件 |
| 脚本效果 | `common/scripted_effects/*.txt` | 类似的概念 |

---

**文档版本**: 1.0
**更新日期**: 2026-04-24
**维护者**: AI Agent (HOI Mod-Maker Skill)
