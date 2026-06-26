# HOI4 国策树完整语法参考

本文档整合了官方 Wiki 和游戏本地文件的所有国策树语法细节。

---

## 目录

1. [Focus Tree 结构](#focus-tree-结构)
2. [Focus 节点](#focus-节点)
3. [Joint Focus 联合焦点](#joint-focus-联合焦点)
4. [Shared Focus 共享焦点](#shared-focus-共享焦点)
5. [Effect 效果参考](#effect-效果参考)
6. [Trigger 触发器参考](#trigger-触发器参考)
7. [示例代码](#示例代码)

---

## Focus Tree 结构

### 完整模板

```
focus_tree = {
    # === 树标识 ===
    id = polish_focus              # 树的唯一 ID
    
    # === 国家权重 ===
    country = {
        factor = 0                 # 基础权重（0 = 不使用）
        
        # 权重修正（满足条件时添加）
        modifier = {
            add = 10
            tag = POL
        }
        
        # 多国家共享示例
        modifier = {
            add = 10
            OR = {
                tag = POL
                tag = SLO
            }
        }
        
        # DLC 检查示例
        modifier = {
            add = 10
            tag = POL
            OR = {
                has_dlc = "No Step Back"
                has_dlc = "Poland: United and Ready"
            }
        }
    }
    
    # === 默认树标志 ===
    default = no                   # yes = 无专属树的国家使用此树
    
    # === 初始显示位置 ===
    initial_show_position = {
        x = 500
        y = 300
    }
    # 或使用焦点作为锚点：
    initial_show_position = {
        focus = POL_starting_focus
    }
    
    # === 连续焦点位置（可选）===
    continuous_focus_position = {
        x = 100
        y = 50
    }
    
    # === 引用共享焦点（可选）===
    shared_focus = {shared_focus_id}
    # 可引用多个：
    shared_focus = {shared_focus1}
    shared_focus = {shared_focus2}
    
    # === 焦点定义 ===
    focus = { ... }
    focus = { ... }
    joint_focus = { ... }
}
```

### Country 权重详解

```
country = {
    factor = 0                     # 基础权重
    
    modifier = {
        add = 10                    # 添加的权重值
        tag = POL                   # 国家标签
    }
    
    modifier = {
        add = 10
        original_tag = POL          # 使用原始标签（支持内战双方）
    }
    
    modifier = {
        factor = 5                  # 乘法修正
        has_dlc = "No Step Back"    # DLC 检查
    }
}
```

**权重逻辑**：
- 最终权重 = factor + 所有满足条件的 modifier.add
- 只有最高权重的树会被使用
- 如果权重相同，文件名 ASCII 码靠后的胜出

---

## Focus 节点

### 必需字段

```
focus = {
    id = POL_focus_id              # 唯一标识符（必填）
    icon = GFX_focus_POL_focus     # 图标（必填，可用现有 GFX）
    x = 2                          # 横坐标（必填）
    y = 0                          # 纵坐标（必填）
    cost = 10                      # 完成天数（必填，实际天数 = cost × 7）
}
```

### 定位方式

**方式1：绝对定位**
```
focus = {
    id = POL_focus_1
    icon = GFX_goal_generic_construction
    x = 2          # 树坐标系中的绝对位置
    y = 0
    cost = 5
}
```

**方式2：相对定位**
```
focus = {
    id = POL_focus_2
    icon = GFX_goal_generic_construction
    
    relative_position_id = POL_focus_1    # 锚点焦点
    
    x = 0              # 相对于锚点的偏移（-表示左，+表示右）
    y = 1              # 向下一行
    
    cost = 10
}
```

**相对定位规则**：
- `x` 负值 = 左侧，正值 = 右侧
- `y` 正值 = 下方（通常为正）
- 适用于需要平移整条分支的场景

### 前置条件 (Prerequisite)

**单一前置**：
```
prerequisite = { focus = POL_parent_focus }
```

**多重前置（AND 关系）**：
```
prerequisite = { 
    focus = POL_focus1 
    focus = POL_focus2 
}
```

**或关系（满足任一组）**：
```
prerequisite = { focus = POL_path_a }
prerequisite = { focus = POL_path_b }
```

**组合使用**：
```
# 需要 (A AND B) OR (C AND D)
prerequisite = { focus = POL_focus_a focus = POL_focus_b }
prerequisite = { focus = POL_focus_c focus = POL_focus_d }
```

### 互斥 (Mutually Exclusive)

```
focus = {
    id = POL_path_democratic
    
    mutually_exclusive = { 
        focus = POL_path_fascist 
        focus = POL_path_communist 
    }
}

focus = {
    id = POL_path_fascist
    
    mutually_exclusive = { 
        focus = POL_path_democratic 
        focus = POL_path_communist 
    }
}

focus = {
    id = POL_path_communist
    
    mutually_exclusive = { 
        focus = POL_path_democratic 
        focus = POL_path_fascist 
    }
}
```

**注意**：互斥需要双向声明，每个焦点都要列出其他互斥焦点。

### 可用条件 (Available)

```
available = {
    # 基础条件
    tag = POL
    
    # 时间条件
    date > 1936.1.1
    
    # 政治条件
    has_political_power > 50
    has_government = democracy
    fascism > 0.3
    
    # 稳定度/战争支持度
    has_stability > 0.5
    has_war_support > 0.3
    
    # 领土条件
    controls_state = 123
    owns_state = 123
    123 = { is_owned_by = ROOT }
    
    # 已完成焦点
    has_completed_focus = POL_other_focus
    
    # 已研究科技
    has_tech = infantry_equipment_1
    
    # 工厂数量
    num_of_owned_factories > 50
    
    # 国家标记
    has_country_flag = pol_flag_name
    
    # 全局标记
    has_global_flag = world_war_started
    
    # 意识形态支持度
    get_popularity = {
        ideology = fascism
        value > 0.3
    }
    
    # 或条件
    OR = {
        has_stability > 0.7
        has_war_support > 0.5
    }
    
    # 且条件
    AND = {
        controls_state = 123
        controls_state = 124
    }
    
    # 非条件
    NOT = {
        has_war_with = GER
    }
}
```

### 跳过条件 (Bypass)

```
bypass = {
    # 满足条件时自动完成焦点
    custom_trigger_tooltip = {
        tooltip = POL_focus_bypass_tt
        has_tech = infantry_equipment_1
    }
}

# 本地化
POL_focus_bypass_tt:0 "已研究步兵装备 I"
```

### 完成效果 (Completion Reward)

```
completion_reward = {
    # === 政治效果 ===
    add_political_power = 100
    add_stability = 0.05
    add_war_support = 0.05
    
    # === 意识形态 ===
    add_popularity = {
        ideology = fascism
        popularity = 0.10
    }
    
    set_politics = {
        ruling_party = fascism
        elections_allowed = no
    }
    
    # === 民族精神 ===
    add_ideas = POL_spirit_name
    remove_ideas = POL_old_spirit
    
    add_timed_idea = {
        idea = POL_temporary_boost
        days = 365
    }
    
    # === 建筑效果 ===
    random_owned_controlled_state = {
        prioritize = { 123 124 125 }
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
        set_state_flag = POL_state_developed
    }
    
    # === 资源效果 ===
    add_resource = {
        type = steel
        amount = 24
        state = 762
    }
    
    # === 铁路建设 ===
    build_railway = {
        path = { 9508 6558 3483 }
    }
    
    # === 科技效果 ===
    add_tech_bonus = {
        name = POL_tech_bonus
        bonus = 1.0         # 100% 研究速度
        uses = 1
        category = industry
    }
    
    add_research_slot = 1
    
    # === 军事效果 ===
    army_experience = 25
    navy_experience = 25
    air_experience = 25
    
    add_manpower = 50000
    
    # === 外交效果 ===
    GER = {
        add_opinion_modifier = {
            target = ROOT
            modifier = pol_german_cooperation
        }
    }
    
    create_guarantee = { target = CZE }
    
    create_wargoal = {
        type = annex_everything
        target = GER
    }
    
    # === 阵营效果 ===
    create_faction = POL_international_block
    
    add_to_faction = GER
    
    # === 领土效果 ===
    transfer_state = {
        state = 123
        target = GER
    }
    
    123 = {
        add_core_by = ROOT
        add_claim_by = ROOT
    }
    
    # === 事件效果 ===
    country_event = {
        id = poland_events.1
        days = 7
        random_days = 3
    }
    
    news_event = {
        id = news.poland_war
        days = 1
    }
    
    # === 标记效果 ===
    set_country_flag = pol_focus_done
    
    set_country_flag = {
        flag = pol_focus_variant
        days = 365         # 过期天数（可选）
        value = 1          # 标记值（可选，用于变量）
    }
    
    set_global_flag = world_event_happened
    
    # === 变量效果 ===
    set_variable = {
        var = POL_economy_var
        value = 10
    }
    
    add_to_variable = {
        var = POL_economy_var
        value = 5
    }
    
    # === 条件效果 ===
    if = {
        limit = {
            has_government = fascism
        }
        add_political_power = 150
    }
    else = {
        add_political_power = 50
    }
    
    # === 循环效果 ===
    every_owned_state = {
        limit = {
            is_core_of = ROOT
            free_building_slots = {
                building = infrastructure
                size > 2
            }
        }
        add_building_construction = {
            type = infrastructure
            level = 1
            instant_build = yes
        }
    }
    
    # === 隐藏效果 ===
    hidden_effect = {
        set_country_flag = pol_hidden_flag
    }
    
    # === 自定义提示 ===
    custom_effect_tooltip = POL_focus_custom_tt
}
```

### 行为标志

```
focus = {
    id = POL_focus_name
    
    # 投降后仍可用
    available_if_capitulated = yes
    
    # 可取消（默认 no）
    cancelable = yes
    
    # 条件失效时取消
    cancel_if_invalid = yes
    
    # 条件失效时暂停但保留进度
    continue_if_invalid = yes
    
    # 即使与其他焦点效果冲突也允许
    will_lead_to_war_with = GER
    
    # ...
}
```

### Search Filters

```
search_filters = { 
    FOCUS_FILTER_POLITICAL 
    FOCUS_FILTER_STABILITY 
}

# 可用过滤器：
FOCUS_FILTER_POLITICAL      # 政治
FOCUS_FILTER_INDUSTRY       # 工业
FOCUS_FILTER_RESEARCH       # 研究
FOCUS_FILTER_STABILITY      # 稳定度
FOCUS_FILTER_WAR_SUPPORT    # 战争支持度
FOCUS_FILTER_MANPOWER       # 人力
FOCUS_FILTER_ANNEXATION     # 吞并
FOCUS_FILTER_HISTORICAL     # 历史路线
FOCUS_FILTER_INNER_CIRCLE   # 德国内圈
```

### AI 权重

```
ai_will_do = {
    factor = 10           # 基础权重
    
    modifier = {
        add = 5           # 权重加成
        has_war_with = GER
    }
    
    modifier = {
        factor = 0         # 权重归零（永不选择）
        has_stability < 0.3
    }
    
    modifier = {
        factor = 2        # 权重翻倍
        has_government = fascism
    }
}
```

---

## Joint Focus 联合焦点

联合焦点用于阵营共享机制，阵营领袖发起，成员同时完成。

### 完整模板

```
joint_focus = {
    id = HAB_joint_economy
    icon = GFX_focus_generic_economy
    x = 5
    y = 3
    cost = 10
    
    # === 前置条件 ===
    prerequisite = { focus = HAB_economic_base }
    
    # === 发起者触发条件 ===
    joint_trigger = {
        is_faction_leader = yes
        num_faction_members > 1
        has_dlc = "No Step Back"
    }
    
    # === 成员触发条件 ===
    member_trigger = {
        is_faction_member = yes
        NOT = { is_faction_leader = yes }
    }
    
    # === 发起者完成效果 ===
    completion_reward_joint_originator = {
        add_political_power = 100
        
        every_faction_member = {
            limit = { NOT = { is_faction_leader = yes } }
            add_political_power = 50
        }
        
        add_named_threat = { threat = 2 name = HAB_expansionism }
    }
    
    # === 成员完成效果 ===
    completion_reward_joint_member = {
        add_political_power = 50
    }
    
    # === 可用条件（双方都要满足）===
    available = {
        is_in_faction = yes
    }
    
    # === AI 权重 ===
    ai_will_do = {
        factor = 10
    }
}
```

---

## Shared Focus 共享焦点

共享焦点定义在单独文件中，可被多个焦点树引用。

### 定义共享焦点

```
# 文件: common/national_focus/shared_focuses.txt

shared_focus = {
    id = baltic_industrial_base
    
    icon = GFX_goal_generic_construction
    x = 0
    y = 0
    cost = 5
    
    # 与普通焦点相同的所有字段
    completion_reward = {
        random_owned_controlled_state = {
            add_building_construction = {
                type = industrial_complex
                level = 1
                instant_build = yes
            }
        }
    }
}
```

### 引用共享焦点

```
focus_tree = {
    id = estonian_focus
    
    country = {
        factor = 0
        modifier = {
            add = 10
            tag = EST
        }
    }
    
    # 引用共享焦点
    shared_focus = baltic_industrial_base
    
    # 本土焦点
    focus = {
        id = EST_local_focus
        prerequisite = { focus = baltic_industrial_base }
        # ...
    }
}
```

---

## Effect 效果参考

### 政治效果

| Effect | 说明 | 示例 |
|--------|------|------|
| `add_political_power` | 政治点数 | `100` |
| `add_stability` | 稳定度 | `0.05` (5%) |
| `add_war_support` | 战争支持度 | `0.05` |
| `add_popularity` | 意识形态支持度 | `{ ideology = fascism popularity = 0.10 }` |
| `set_politics` | 设置政体 | `{ ruling_party = fascism elections_allowed = no }` |

### 工业效果

| Effect | 说明 | 示例 |
|--------|------|------|
| `add_building_construction` | 建造建筑 | `{ type = industrial_complex level = 1 instant_build = yes }` |
| `add_resource` | 添加资源 | `{ type = steel amount = 24 state = 762 }` |
| `add_extra_state_shared_building_slots` | 增加建筑槽 | `1` |
| `build_railway` | 建铁路 | `{ path = { 9508 6558 } }` |

### 科技效果

| Effect | 说明 | 示例 |
|--------|------|------|
| `add_tech_bonus` | 科技加成 | `{ name = bonus bonus = 1.0 uses = 1 category = industry }` |
| `add_research_slot` | 研究槽位 | `1` |
| `set_technology` | 解锁科技 | `{ infantry_equipment_1 = 1 }` |

### 军事效果

| Effect | 说明 | 示例 |
|--------|------|------|
| `army_experience` | 陆军经验 | `25` |
| `navy_experience` | 海军经验 | `25` |
| `air_experience` | 空军经验 | `25` |
| `add_manpower` | 人力 | `50000` |
| `add_ideas` | 添加精神 | `POL_spirit_name` |

---

## Trigger 触发器参考

### 国家触发器

| Trigger | 说明 | 示例 |
|---------|------|------|
| `tag` | 国家标签 | `POL` |
| `original_tag` | 原始标签 | `POL` |
| `has_political_power` | 政治点数 | `> 50` |
| `has_stability` | 稳定度 | `> 0.5` |
| `has_war_support` | 战争支持度 | `> 0.3` |
| `has_government` | 意识形态 | `fascism` |
| `has_completed_focus` | 已完成焦点 | `POL_focus_name` |
| `has_tech` | 已研究科技 | `infantry_equipment_1` |
| `num_of_owned_factories` | 工厂数量 | `> 50` |
| `has_country_flag` | 国家标记 | `pol_flag_name` |
| `has_global_flag` | 全局标记 | `world_war_started` |

### 领土触发器

| Trigger | 说明 | 示例 |
|---------|------|------|
| `controls_state` | 控制省份 | `123` |
| `owns_state` | 拥有省份 | `123` |
| `is_owned_by` | 所有者 | `POL` (在省份范围内) |
| `is_on_continent` | 大洲 | `europe` |

---

## 示例代码

### 波兰历史国策树示例

```
focus_tree = {
    id = polish_historical_focus
    
    country = {
        factor = 0
        modifier = {
            add = 10
            tag = POL
        }
    }
    
    default = no
    
    # === 政治分支 ===
    focus = {
        id = POL_seize_control_of_the_state
        icon = GFX_focus_generic_political_pressure
        x = 0
        y = 0
        cost = 5
        
        search_filters = { FOCUS_FILTER_POLITICAL }
        
        completion_reward = {
            add_political_power = 50
            add_stability = 0.05
        }
    }
    
    focus = {
        id = POL_authoritarian_consolidation
        prerequisite = { focus = POL_seize_control_of_the_state }
        icon = GFX_focus_generic_authoritarian_regime
        x = -1
        y = 1
        relative_position_id = POL_seize_control_of_the_state
        cost = 10
        
        mutually_exclusive = { focus = POL_democratic_reform }
        
        available = {
            has_government = neutrality
        }
        
        completion_reward = {
            add_political_power = 100
            add_ideas = POL_authoritarian_regime
        }
    }
    
    focus = {
        id = POL_democratic_reform
        prerequisite = { focus = POL_seize_control_of_the_state }
        icon = GFX_goal_support_democracy
        x = 1
        y = 1
        relative_position_id = POL_seize_control_of_the_state
        cost = 10
        
        mutually_exclusive = { focus = POL_authoritarian_consolidation }
        
        available = {
            NOT = { has_government = fascism }
            NOT = { has_government = communism }
        }
        
        completion_reward = {
            add_stability = 0.10
            add_popularity = {
                ideology = democratic
                popularity = 0.15
            }
            add_ideas = POL_democratic_spirit
        }
    }
    
    # === 工业分支 ===
    focus = {
        id = POL_four_year_plan
        icon = GFX_focus_POL_four_year_plan
        x = 3
        y = 0
        cost = 5
        
        search_filters = { FOCUS_FILTER_INDUSTRY FOCUS_FILTER_RESEARCH }
        
        completion_reward = {
            add_tech_bonus = {
                name = POL_four_year_plan
                bonus = 1.0
                uses = 1
                category = construction_tech
            }
            add_timed_idea = {
                idea = POL_four_year_plan_idea
                days = 1460
            }
        }
    }
    
    focus = {
        id = POL_industrial_expansion
        prerequisite = { focus = POL_four_year_plan }
        icon = GFX_goal_generic_construct_civ_factory
        x = 3
        y = 1
        relative_position_id = POL_four_year_plan
        cost = 10
        
        search_filters = { FOCUS_FILTER_INDUSTRY }
        
        completion_reward = {
            random_owned_controlled_state = {
                prioritize = { 86 87 88 89 90 91 92 807 }
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
            }
        }
    }
}
```

---

**最后更新**: 2026-04-24
