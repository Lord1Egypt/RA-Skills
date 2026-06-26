# 国策树完整语法参考

> 本文件从 SKILL.md 拆分而来，包含国策树的完整语法细节。
> 日常使用请直接查阅本文件；SKILL.md 仅保留黄金法则和导航。

---

## Focus Tree 结构

```
focus_tree = {
    id = polish_focus
    
    # === 国家权重 ===
    country = {
        factor = 0
        modifier = {
            add = 10
            tag = POL
        }
    }
    
    # === 默认树 ===
    default = no
    
    # === 初始视口 ===
    initial_show_position = {
        x = 500
        y = 300
    }
    # 或使用焦点锚点：
    initial_show_position = {
        focus = POL_starting_focus
    }
    
    # === 连续焦点位置 ===
    continuous_focus_position = { x = 100 y = 1300 }
    
    # === 内圈窗口（德国特有）===
    inlay_window = {
        id = ger_inner_circle_inlay_window
        position = { x = 4500 y = 1150 }
    }
    
    # === 备选图标（可选）===
    alternate_icon_set = FOCUS_ICON_SET_HISTORICAL_KEY_FOCUS
    
    # === 快捷方式（可选）===
    shortcut = {
        name = POL_historical_path_shortcut
        target = POL_political_base
        scroll_wheel_factor = 0.469
        trigger = { always = yes }
    }
    
    # === 共享焦点引用（可选）===
    shared_focus = baltic_industrial_base
    
    # === 焦点定义 ===
    focus = { ... }
    focus = { ... }
}
```

## Focus 节点完整字段

### 必需字段

```
focus = {
    id = POL_focus_name       # 唯一标识符
    icon = GFX_focus_POL      # 图标 GFX
    x = 2                     # 横坐标（绝对或相对）
    y = 0                     # 纵坐标
    cost = 10                 # 天数成本（实际天数 = cost × 7）
}
```

### 定位方式（默认用相对定位）

> ⚠️ **`relative_position_id` 是默认首选**：除根节点外，**一律优先使用相对定位**。绝对坐标只在没有父节点时才用。相对定位让树可以整体平移、后期插入节点时不影响子节点坐标。

**绝对定位**（仅用于根节点或无父节点的主干焦点）：
```
focus = {
    id = POL_root_focus
    x = 0
    y = 0
    cost = 5
}
```

**相对定位**：
```
focus = {
    id = POL_child_focus
    relative_position_id = POL_root_focus
    x = 0        # 偏移：负=左，正=右
    y = 1        # 偏移：向下
    cost = 10
}
```

### 前置条件

> ⚠️ **必须验证**：所有 `prerequisite` 引用的 focus ID 必须在当前国策树文件中**实际定义**。生成前先确认 ID 存在，绝不凭空捏造。

```
# 单一前置
prerequisite = { focus = POL_parent }

# 多重前置（AND 关系）
prerequisite = { focus = POL_focus1 focus = POL_focus2 }

# 或关系（满足任一组）
prerequisite = { focus = POL_path_a }
prerequisite = { focus = POL_path_b }
```

### 互斥焦点

```
focus = {
    id = POL_democratic_path
    
    mutually_exclusive = { 
        focus = POL_fascist_path 
        focus = POL_communist_path 
    }
}
```

**注意**：互斥需要双向声明！

### 可用条件

```
available = {
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
    num_of_controlled_factories > 50
    
    # 标记
    has_country_flag = pol_flag_name
    has_global_flag = world_war_started
    
    # 意识形态支持度
    get_popularity = {
        ideology = fascism
        value > 0.3
    }
    
    # 逻辑组合
    OR = {
        has_stability > 0.7
        has_war_support > 0.5
    }
    
    NOT = { has_war_with = GER }
    
    AND = {
        controls_state = 123
        controls_state = 124
    }
}
```

### 跳过条件

```
bypass = {
    custom_trigger_tooltip = {
        tooltip = POL_focus_bypass_tt
        has_tech = infantry_equipment_1
    }
}
```

### 完成效果

```
completion_reward = {
    # ===== 政治效果 =====
    add_political_power = 100
    add_stability = 0.05
    add_war_support = 0.05
    
    # 意识形态
    add_popularity = {
        ideology = fascism
        popularity = 0.10
    }
    
    set_politics = {
        ruling_party = fascism
        elections_allowed = no
    }
    
    # ===== 民族精神 =====
    add_ideas = POL_new_spirit
    remove_ideas = POL_old_spirit
    
    add_timed_idea = {
        idea = POL_temp_boost
        days = 365
    }
    
    # ===== 科技效果 =====
    add_tech_bonus = {
        name = POL_tech_bonus
        bonus = 1.0
        uses = 1
        category = industry
    }
    
    add_research_slot = 1
    
    # ===== 建筑效果（正确写法）=====
    # ❌ 错误写法：random_owned_controlled_state 里用 state = 762
    # ✅ 正确写法：用具体 state ID 作为 scope，在其内部调用 add_building_construction

    # 写法一：指定具体省份/州（推荐）
    # 在 state scope 内调用建筑效果
    123 = {
        add_extra_state_shared_building_slots = 1    # 先扩容（如果槽位已满）
        add_building_construction = {
            type = industrial_complex              # 建筑类型
            level = 1                               # 建造等级
            instant_build = yes                     # 瞬间完成（国策中推荐）
        }
    }

    124 = {
        add_extra_state_shared_building_slots = 2
        add_building_construction = {
            type = arms_factory
            level = 2
            instant_build = yes
        }
    }

    # 写法二：多个州同时建造（遍历）
    every_owned_state = {
        limit = {
            is_capital = no
            free_building_slots = {
                building = industrial_complex
                size > 0
                include_locked = yes
            }
        }
        add_building_construction = {
            type = industrial_complex
            level = 1
            instant_build = yes
        }
    }

    # 写法三：随机选择一个州
    random_owned_controlled_state = {
        prioritize = { 123 124 125 }
        limit = {
            free_building_slots = {
                building = air_base
                size > 5
            }
        }
        add_building_construction = {
            type = air_base
            level = 6
            instant_build = yes
        }
        set_state_flag = GER_expanding_luftwaffe_flag
    }

    # 建筑类型参考：
    # industrial_complex (民用工厂) / arms_factory (军用工厂)
    # dockyard (船坞) / infrastructure (基础设施)
    # air_base (空军基地) / naval_base (海军基地)
    # bunker (陆上要塞) / coastal_bunker (海岸要塞)
    # anti_air_building (防空炮)

    # ===== 资源效果（正确写法）=====
    # ❌ 错误写法：add_resource 里用 state = 762
    # ✅ 正确写法：在 state scope 内调用 add_resource
    762 = {
        add_resource = {
            type = steel
            amount = 24
        }
    }

    # 也可以给首都加资源：
    1 = {
        add_resource = {
            type = chromium
            amount = 12
        }
    }
    
    # ===== 铁路建设 =====
    build_railway = {
        level = 1
        path = { 9508 6558 3483 }
    }
    
    # ===== 军事效果 =====
    army_experience = 25
    navy_experience = 25
    air_experience = 25
    add_manpower = 50000
    
    # ===== 外交效果 =====
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
    
    # ===== 阵营效果 =====
    create_faction = POL_international_block
    add_to_faction = GER
    
    # ===== 领土效果 =====
    transfer_state = {
        state = 123
        target = GER
    }
    
    123 = {
        add_core_by = ROOT
        add_claim_by = ROOT
    }
    
    # ===== 事件效果 =====
    country_event = {
        id = poland_events.1
        days = 7
        random_days = 3
    }
    
    # ===== 标记效果 =====
    set_country_flag = pol_focus_done
    set_country_flag = {
        flag = pol_focus_variant
        days = 365
        value = 1
    }
    set_global_flag = world_event_happened
    
    # ===== 条件效果 =====
    if = {
        limit = { has_government = fascism }
        add_political_power = 150
    }
    else = {
        add_political_power = 50
    }
    
    # ===== 隐藏效果 =====
    hidden_effect = {
        set_country_flag = pol_hidden_flag
    }
    
    # ===== 自定义提示 =====
    custom_effect_tooltip = POL_focus_custom_tt
    
    # ===== 显示顾问提示 =====
    show_ideas_tooltip = GER_hjalmar_schacht
    
    # ===== 解锁决策提示 =====
    unlock_decision_category_tooltip = POL_economic_decisions
}
```

### 内圈焦点（Inner Circle）

```
focus = {
    id = GER_inner_circle_1
    inner_circle = yes
    icon = GFX_focus_ger_inner_circle
    x = 0
    y = 0
    relative_position_id = GER_center_focus
    cost = 20    # 内圈焦点通常 cost 较低
    
    completion_reward = {
        add_political_power = 25
    }
}

# 时间常量定义
@inner_circle_time_tier_1 = 20    # 140天
@inner_circle_time_tier_2 = 40    # 280天
```

### 可持久国策（Persistent Focus / Continuous Focus）

可持久国策分为两种：**Continuous Focus**（连续焦点）和 **Persistent Focus**（持久焦点）。

#### Continuous Focus（连续焦点）

连续焦点在完成10个常规国策后解锁，效果在激活期间**持续生效**，每天消耗1政治点数。

```
focus_tree = {
    continuous_focus_position = { x = 500 y = 1300 }  # 连续焦点在地图上的位置

    focus = {
        id = continuous_army_xp
        icon = GFX_focus_generic_army_xp
        x = 0
        y = 0
        continuous = yes                               # 标记为连续焦点

        cost = 0                                       # 连续焦点 cost 必须为 0
        cancelable = no                               # 不可取消（可选，默认 no）
        available_if_capitulated = yes                 # 投降后可用（可选）

        ai_will_do = {                                 # AI 行为配置
            factor = 1
            modifier = {
                add = 10
                tag = GER
            }
        }

        search_filters = {                             # 搜索过滤器（重要！）
            FOCUS_FILTER_ARMY_XP                       # 必须对应焦点效果类型
            FOCUS_FILTER_MANPOWER
        }

        # ✅ 连续焦点使用 modifier = {} 提供持续效果
        # ❌ 不要用 completion_reward，它只生效一次
        modifier = {
            army_experience_gain_factor = 0.05
            mobilization_speed = 0.10
        }
    }
}
```

**Continuous Focus 的特殊规则**：
- `cost` 必须为 0（continuous focus 本身不消耗时间）
- 使用 `modifier = {}` 提供持续效果，而非 `completion_reward`
- 必须指定 `search_filters`（影响显示分类和 AI 选卡逻辑）
- `continuous = yes` 与 `relative_position_id` 不兼容

#### Persistent Focus（持久焦点，可被取消型）

另一种可持久国策：国策开始后持续执行（期间消耗政治点数），但可以被取消，取消时触发 `cancel` 效果。

```
focus = {
    id = TAG_mobilization_focus
    icon = GFX_goal_generic_mobilization
    cost = 30                                    # 持续 210 天

    # 国策进行中的效果（每天生效）
    completion_reward = {
        add_war_support = 0.05
        army_experience = 25
    }

    # 完成后的一次性效果
    # （如果需要额外效果）

    cancel = {                                    # ❗ 被取消时触发的效果
        add_stability = -0.05
        custom_effect_tooltip = TAG_mobilization_cancelled_tt
    }

    cancel_if_invalid = yes                       # 条件不满足时自动取消（可选）
    will_lead_to_war_with = TAG                   # 完成后对某国宣战（可选）

    ai_will_do = {
        factor = 0                                  # AI 不会自动选择（如果需要玩家决策）
        modifier = {
            add = 10
            has_war = yes
        }
    }
}
```

**cancel 块的典型用途**：
- 退还部分资源（用标记追踪）
- 触发负面事件
- 显示提示信息

**cancel_if_invalid 用法**：
- 当国策的 available 条件不再满足时，是否自动取消
- `cancel_if_invalid = yes`：自动取消，触发 `cancel` 效果
- `cancel_if_invalid = no`：国策暂停，直到条件恢复

#### cancelable 字段（可取消属性）

控制国策是否可以被玩家手动取消：

```
cancelable = yes        # 可取消（玩家可随时停止）
cancelable = no         # 不可取消（必须完成或条件失效）
```

默认 `cancelable = yes`。设置为 `no` 用于强制完成的国策（如内圈选择）。

**ai_will_do 完整语法**：

```
ai_will_do = {
    factor = 1                              # 基础权重因子

    modifier = {                            # 修正器（可叠加）
        add = 10                            # 加法修正
        multiply = 2                        # 乘法修正（2x 权重）
        tag = GER                           # 仅对特定国家生效
        NOT = { has_completed_focus = XXX } # 取反
        has_war = yes                       # 战争时权重修正
        has_government = fascism             # 特定政体时生效
        date > 1940.1.1                     # 特定日期后生效
    }
}
```

**常见 ai_will_do 组合**：

```
# AI 总是选择（factor = 0 但 modifier add 修正为正）
ai_will_do = {
    factor = 0
    modifier = { add = 100 }
}

# AI 从不选择
ai_will_do = {
    factor = 0
}

# 战时才选
ai_will_do = {
    factor = 1
    modifier = {
        add = 10
        has_war = yes
        NOT = { has_war = yes }
        add = -100
    }
}
```

### Search Filters 完整列表

```
FOCUS_FILTER_POLITICAL           # 政治
FOCUS_FILTER_RESEARCH            # 研究
FOCUS_FILTER_INDUSTRY            # 工业
FOCUS_FILTER_STABILITY           # 稳定度
FOCUS_FILTER_WAR_SUPPORT         # 战争支持度
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
FOCUS_FILTER_INNER_CIRCLE        # 德国内圈
```
