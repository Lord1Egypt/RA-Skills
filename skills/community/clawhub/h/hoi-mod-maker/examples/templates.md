# HOI4 常用代码模板

> 从 SKILL.md 拆分而来，包含完整的国策树和本地化模板。

---

## 常用模板

### 完整国策树模板

```
focus_tree = {
    id = {country}_focus
    
    country = {
        factor = 0
        modifier = { add = 10 tag = {TAG} }
    }
    
    default = no
    
    initial_show_position = { x = 500 y = 300 }
    
    # 政治分支
    focus = {
        id = {TAG}_political_base
        icon = GFX_goal_generic_political_pressure
        x = 0
        y = 0
        cost = 5
        search_filters = { FOCUS_FILTER_POLITICAL }
        
        completion_reward = {
            add_political_power = 50
        }
    }
    
    focus = {
        id = {TAG}_political_path1
        prerequisite = { focus = {TAG}_political_base }
        icon = GFX_goal_generic_authoritarian
        x = -1
        y = 1
        relative_position_id = {TAG}_political_base
        cost = 10
        
        mutually_exclusive = { focus = {TAG}_political_path2 }
        
        available = { has_government = neutrality }
        
        completion_reward = {
            add_political_power = 100
            add_ideas = {TAG}_authoritarian_spirit
        }
    }
    
    # 工业分支
    focus = {
        id = {TAG}_industrial_base
        icon = GFX_goal_generic_construct_civ_factory
        x = 3
        y = 0
        cost = 5
        search_filters = { FOCUS_FILTER_INDUSTRY }
        
        completion_reward = {
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
            }
        }
    }
}
```

### 本地化文件模板

```yaml
l_english:
 # 焦点
 {TAG}_political_base:0 "Political Foundation"
 {TAG}_political_base_desc:0 "Description..."
 
 {TAG}_political_path1:0 "Authoritarian Path"
 {TAG}_political_path1_desc:0 "Description..."
 
 # 民族精神
 {TAG}_authoritarian_spirit:0 "Authoritarian Regime"
 {TAG}_authoritarian_spirit_desc:0 "Description..."

l_simp_chinese:
 {TAG}_political_base:0 "政治基础"
 {TAG}_political_base_desc:0 "描述..."
```

---

---

---

## ⚠ 重要提示

> 这些模板**仅供参考学习**，展示常见的国策树布局模式。
> 
> **不要机械套用模板！** 每个国家的国策树都应该是独特的，根据其历史背景、战略定位、游戏机制来设计。
> 
> 模板的局限性：
> - 坐标是示例值，需要根据你的整体布局调整
> - 效果代码需要根据你的具体需求修改
> - 层次结构可能过于简单或过于复杂，需要灵活调整
> - 缺乏与其他系统的联动（事件、决议、民族精神等）
> 
> 正确的使用方式：
> 1. 理解模板展示的布局模式（互斥、并行、汇聚等）
> 2. 根据你的国策树整体规划调整坐标
> 3. 为每个节点设计符合主题的效果
> 4. 确保所有节点连接成一个完整的树，无孤立节点

---

## 参考子模块（示例模式，需根据实际需求调整）

> 基于 vanilla 国策树规律提炼，覆盖政治/军事/工业/外交四类场景。每个子模块**自带坐标基准**（根节点在 x=0 y=0），用 
elative_position_id 拼入主树。

### 子模块1：快速政治链（3节点互斥链）

`
focus = {
    id = {TAG}_pol_base
    icon = GFX_goal_generic_political_pressure
    x = 0
    y = 0
    cost = 5
    available = { has_government = neutrality }
    completion_reward = { add_political_power = 50 }
}
focus = {
    id = {TAG}_pol_path_a
    prerequisite = { focus = {TAG}_pol_base }
    relative_position_id = {TAG}_pol_base
    icon = GFX_goal_generic_authoritarian
    x = 1
    y = 0
    cost = 10
    mutually_exclusive = { focus = {TAG}_pol_path_b }
    completion_reward = { add_ideas = {TAG}_authoritarian_spirit }
}
focus = {
    id = {TAG}_pol_path_b
    prerequisite = { focus = {TAG}_pol_base }
    relative_position_id = {TAG}_pol_base
    icon = GFX_goal_generic_demand_territory
    x = -1
    y = 0
    cost = 10
    completion_reward = { add_ideas = {TAG}_democratic_spirit }
}
`

> **参考模式**：互斥选择链。x=±1 使两选项紧邻父节点，y=0 保持同层。

### 子模块2：军事动员链（3节点顺序链）

`
focus = {
    id = {TAG}_mil_base
    icon = GFX_goal_generic_mobilize
    x = 0
    y = 0
    cost = 5
    search_filters = { FOCUS_FILTER_MANPOWER }
    completion_reward = { army_experience = 25 }
}
focus = {
    id = {TAG}_mil_expand
    prerequisite = { focus = {TAG}_mil_base }
    relative_position_id = {TAG}_mil_base
    icon = GFX_goal_generic_army_infrastructure
    x = 2
    y = 0
    cost = 10
    completion_reward = {
        add_manpower = 5000
        add_war_support = 0.05
    }
}
focus = {
    id = {TAG}_mil_focus
    prerequisite = { focus = {TAG}_mil_expand }
    relative_position_id = {TAG}_mil_expand
    icon = GFX_goal_generic_army_design
    x = 2
    y = 0
    cost = 10
    completion_reward = { army_experience = 50 }
}
`

> **参考模式**：顺序链。x间距=2 防止重叠，适合表达线性递进关系。

### 子模块3：工业扩张链（3节点+1分支）

`
focus = {
    id = {TAG}_ind_base
    icon = GFX_goal_generic_construct_civ_factory
    x = 0
    y = 0
    cost = 5
    search_filters = { FOCUS_FILTER_INDUSTRY }
    completion_reward = {
        random_owned_controlled_state = {
            limit = { free_building_slots = { building = industrial_complex size > 0 } }
            add_extra_state_shared_building_slots = 1
        }
    }
}
focus = {
    id = {TAG}_ind_expand
    prerequisite = { focus = {TAG}_ind_base }
    relative_position_id = {TAG}_ind_base
    icon = GFX_goal_generic_propaganda
    x = 2
    y = 0
    cost = 10
    completion_reward = {
        random_owned_controlled_state = {
            limit = { free_building_slots = { building = industrial_complex size > 0 } }
            add_extra_state_shared_building_slots = 1
            add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
        }
    }
}
focus = {
    id = {TAG}_ind_mil
    prerequisite = { focus = {TAG}_ind_base }
    relative_position_id = {TAG}_ind_base
    icon = GFX_goal_generic_propaganda
    x = -2
    y = 0
    cost = 10
    completion_reward = {
        random_owned_controlled_state = {
            limit = { free_building_slots = { building = arms_factory size > 0 } }
            add_extra_state_shared_building_slots = 1
        }
    }
}
focus = {
    id = {TAG}_ind_deep
    prerequisite = { focus = {TAG}_ind_expand }
    relative_position_id = {TAG}_ind_expand
    icon = GFX_goal_generic_military_deal
    x = 2
    y = 0
    cost = 10
    completion_reward = { add_research_slot = 1 }
}
`

> **参考模式**：双分支并行。根节点展开两条对称路径，x=±2 防止分支间碰撞。

### 子模块4：外交吞并链（4节点，含傀儡/吞并）

`
focus = {
    id = {TAG}_dip_base
    icon = GFX_goal_generic_diplomacy
    x = 0
    y = 0
    cost = 5
    search_filters = { FOCUS_FILTER_POLITICAL }
    completion_reward = { add_threat = -5 }
}
focus = {
    id = {TAG}_dip_claim
    prerequisite = { focus = {TAG}_dip_base }
    relative_position_id = {TAG}_dip_base
    icon = GFX_goal_generic_demand_territory
    x = 2
    y = 0
    cost = 10
    completion_reward = { create_wargoal = { target = {TAG}_neighbor type = annex_everything } }
}
focus = {
    id = {TAG}_dip_puppet
    prerequisite = { focus = {TAG}_dip_base }
    relative_position_id = {TAG}_dip_base
    icon = GFX_goal_generic_demand_territory
    x = -2
    y = 0
    cost = 10
    completion_reward = {
        create_wargoal = { target = {TAG}_weak_neighbor type = puppet }
        add_named_threat = { threat = -5 name = dip_puppet_relief }
    }
}
focus = {
    id = {TAG}_dip_war
    prerequisite = { focus = {TAG}_dip_claim }
    relative_position_id = {TAG}_dip_claim
    icon = GFX_goal_generic_military_deal
    x = 2
    y = 0
    cost = 10
    will_lead_to_war_with = {TAG}_neighbor
    completion_reward = { set_rule = { can_create_factions = yes } }
}
`

> **参考模式**：外交双路径。一条吞并路线，一条傀儡路线，玩家二选一。

### 子模块5：科技突破链（5节点，最多5子节点）

`
focus = {
    id = {TAG}_tec_base
    icon = GFX_goal_generic_research
    x = 0
    y = 0
    cost = 5
    search_filters = { FOCUS_FILTER_RESEARCH }
    completion_reward = { add_doctrine_cost_reduction = { cost = 0.1 name = land_docrine_cost_factor } }
}
focus = {
    id = {TAG}_tec_army
    prerequisite = { focus = {TAG}_tec_base }
    relative_position_id = {TAG}_tec_base
    icon = GFX_goal_generic_army_design
    x = 2
    y = 0
    cost = 10
    completion_reward = { army_experience = 25 }
}
focus = {
    id = {TAG}_tec_navy
    prerequisite = { focus = {TAG}_tec_base }
    relative_position_id = {TAG}_tec_base
    icon = GFX_goal_generic_navy_design
    x = 2
    y = 1
    cost = 10
    completion_reward = { navy_experience = 25 }
}
focus = {
    id = {TAG}_tec_air
    prerequisite = { focus = {TAG}_tec_base }
    relative_position_id = {TAG}_tec_base
    icon = GFX_goal_generic_air_design
    x = 2
    y = 2
    cost = 10
    completion_reward = { air_experience = 25 }
}
focus = {
    id = {TAG}_tec_deep
    prerequisite = { focus = {TAG}_tec_army focus = {TAG}_tec_navy focus = {TAG}_tec_air }
    relative_position_id = {TAG}_tec_base
    icon = GFX_goal_generic_propaganda
    x = 0
    y = 1
    cost = 15
    completion_reward = { add_research_slot = 1 }
}
`

> **参考模式**：汇聚型。多个分支最终汇聚到一个核心节点，适合"全面XX"主题。注意：纵向y间距=1是合法的。


