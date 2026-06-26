# HOI4 Modding 代码片段库

> 可直接复制使用的常用代码模板集合。

---

## 📂 目录

- [国策树模板](#国策树模板)
- [民族精神模板](#民族精神模板)
- [事件模板](#事件模板)
- [决议模板](#决议模板)
- [本地化模板](#本地化模板)
- [人物模板](#人物模板)
- [效果片段](#效果片段)
- [触发器片段](#触发器片段)

---

## 🎯 国策树模板

### 最小可用国策树
```hoi4
focus_tree = {
    id = {TAG}_focus
    
    country = {
        factor = 0
        modifier = { add = 10 tag = {TAG} }
    }
    
    default = no
    
    focus = {
        id = {TAG}_root
        icon = GFX_focus_generic_political
        x = 0
        y = 0
        cost = 5
        
        completion_reward = {
            add_political_power = 50
        }
    }
}
```

### 政治三分支国策树
```hoi4
focus_tree = {
    id = {TAG}_focus
    
    country = {
        factor = 0
        modifier = { add = 10 tag = {TAG} }
    }
    
    default = no
    
    # 根节点
    focus = {
        id = {TAG}_political_base
        icon = GFX_focus_generic_political_pressure
        x = 0
        y = 0
        cost = 5
        search_filters = { FOCUS_FILTER_POLITICAL }
        
        completion_reward = {
            add_political_power = 50
        }
    }
    
    # 民主分支
    focus = {
        id = {TAG}_democratic_path
        prerequisite = { focus = {TAG}_political_base }
        mutually_exclusive = { 
            focus = {TAG}_fascist_path 
            focus = {TAG}_communist_path 
        }
        icon = GFX_focus_generic_democracy
        relative_position_id = {TAG}_political_base
        x = -2
        y = 1
        cost = 10
        
        completion_reward = {
            set_politics = {
                ruling_party = democratic
                elections_allowed = yes
            }
            add_popularity = {
                ideology = democratic
                popularity = 0.20
            }
        }
    }
    
    # 法西斯分支
    focus = {
        id = {TAG}_fascist_path
        prerequisite = { focus = {TAG}_political_base }
        mutually_exclusive = { 
            focus = {TAG}_democratic_path 
            focus = {TAG}_communist_path 
        }
        icon = GFX_focus_generic_fascism
        relative_position_id = {TAG}_political_base
        x = 0
        y = 1
        cost = 10
        
        completion_reward = {
            set_politics = {
                ruling_party = fascism
                elections_allowed = no
            }
            add_popularity = {
                ideology = fascism
                popularity = 0.20
            }
        }
    }
    
    # 共产分支
    focus = {
        id = {TAG}_communist_path
        prerequisite = { focus = {TAG}_political_base }
        mutually_exclusive = { 
            focus = {TAG}_democratic_path 
            focus = {TAG}_fascist_path 
        }
        icon = GFX_focus_generic_communism
        relative_position_id = {TAG}_political_base
        x = 2
        y = 1
        cost = 10
        
        completion_reward = {
            set_politics = {
                ruling_party = communism
                elections_allowed = no
            }
            add_popularity = {
                ideology = communism
                popularity = 0.20
            }
        }
    }
}
```

### 工业发展分支
```hoi4
# 工业基础
focus = {
    id = {TAG}_industrial_base
    icon = GFX_focus_generic_construct_civ_factory
    x = 0
    y = 5
    cost = 5
    search_filters = { FOCUS_FILTER_INDUSTRY }
    
    completion_reward = {
        random_owned_controlled_state = {
            prioritize = { 123 124 125 }  # 替换为实际省份ID
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

# 重工业分支
focus = {
    id = {TAG}_heavy_industry
    prerequisite = { focus = {TAG}_industrial_base }
    mutually_exclusive = { focus = {TAG}_light_industry }
    icon = GFX_focus_generic_construction
    relative_position_id = {TAG}_industrial_base
    x = -1
    y = 1
    cost = 10
    
    completion_reward = {
        add_tech_bonus = {
            name = {TAG}_heavy_industry_bonus
            bonus = 1.0
            uses = 1
            category = industry
        }
    }
}

# 轻工业分支
focus = {
    id = {TAG}_light_industry
    prerequisite = { focus = {TAG}_industrial_base }
    mutually_exclusive = { focus = {TAG}_heavy_industry }
    icon = GFX_focus_generic_consumer_goods
    relative_position_id = {TAG}_industrial_base
    x = 1
    y = 1
    cost = 10
    
    completion_reward = {
        random_owned_controlled_state = {
            prioritize = { 123 124 }
            limit = {
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                    include_locked = yes
                }
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

### 军事改革分支
```hoi4
focus = {
    id = {TAG}_military_reform
    icon = GFX_focus_generic_army
    x = 0
    y = 10
    cost = 10
    search_filters = { FOCUS_FILTER_ARMY_XP }
    
    available = {
        army_size > 0.5               # 陆军规模 > 50k
    }
    
    completion_reward = {
        army_experience = 50
        add_ideas = {TAG}_military_reform_spirit
        
        # 解锁顾问
        show_ideas_tooltip = {TAG}_military_advisor
    }
}

focus = {
    id = {TAG}_army_expansion
    prerequisite = { focus = {TAG}_military_reform }
    icon = GFX_focus_generic_army_organization
    relative_position_id = {TAG}_military_reform
    x = 0
    y = 1
    cost = 10
    
    completion_reward = {
        add_manpower = 100000
        army_experience = 25
    }
}
```

---

## 💡 民族精神模板

### 基础国家精神
```hoi4
ideas = {
    country = {
        {TAG}_national_spirit = {
            picture = generic_national_spirit
            modifier = {
                political_power_gain = 0.10
                stability_factor = 0.05
                war_support_factor = 0.05
            }
            removal_cost = -1              # 永久
        }
    }
}
```

### 临时国家精神
```hoi4
ideas = {
    country = {
        {TAG}_temporary_boost = {
            picture = generic_industry_boost
            modifier = {
                industrial_capacity = 0.15
            }
            removal_cost = 0               # 可移除
            allowed = {
                original_tag = {TAG}
            }
        }
    }
}

# 在效果中添加定时精神
completion_reward = {
    add_timed_idea = {
        idea = {TAG}_temporary_boost
        days = 365
    }
}
```

### 条件触发的精神
```hoi4
ideas = {
    country = {
        {TAG}_war_economy = {
            picture = generic_war_economy
            
            modifier = {
                consumer_goods = -0.05
                military_factory_max_speed_factor = 0.10
            }
            
            allowed = { original_tag = {TAG} }
            
            visible = {
                has_war = yes
                has_war_support > 0.5
            }
            
            removal_cost = -1
        }
    }
}
```

### 顾问模板
```hoi4
ideas = {
    political_advisor = {
        {TAG}_advisor_name = {
            picture = GFX_idea_generic_political
            cost = 150
            
            trait = { inspiring_figure }
            
            modifier = {
                neutrality_drift = 0.10
                stability_weekly = 0.10
            }
            
            allowed = { original_tag = {TAG} }
        }
    }
    
    army_chief = {
        {TAG}_army_chief = {
            picture = GFX_idea_generic_military
            cost = 150
            
            modifier = {
                army_attack_factor = 0.05
                army_defense_factor = 0.05
            }
            
            allowed = { original_tag = {TAG} }
        }
    }
}
```

---

## 🎲 事件模板

### 简单国家事件
```hoi4
add_namespace = {tag}_events

country_event = {
    id = {tag}_events.1
    title = {tag}_events.1_title
    desc = {tag}_events.1_desc
    picture = generic_event
    
    is_triggered_only = yes
    
    option = {
        name = {tag}_events.1_option_a
        add_political_power = 50
    }
}
```

### 带条件的事件
```hoi4
country_event = {
    id = {tag}_events.2
    title = {tag}_events.2_title
    desc = {tag}_events.2_desc
    picture = generic_political_event
    
    trigger = {
        tag = {TAG}
        date > 1938.1.1
        has_stability > 0.6
    }
    
    mean_time_to_happen = {
        days = 30
        modifier = {
            add = 15
            has_stability < 0.7
        }
    }
    
    option = {
        name = {tag}_events.2_option_a
        trigger = { has_political_power > 100 }
        
        add_political_power = -100
        add_stability = 0.10
        add_ideas = {TAG}_stability_spirit
    }
    
    option = {
        name = {tag}_events.2_option_b
        
        add_political_power = 50
        custom_effect_tooltip = {tag}_events.2_tt
        
        hidden_effect = {
            set_country_flag = {tag}_event_2_flag
        }
    }
}
```

### 事件链
```hoi4
# 第一个事件
country_event = {
    id = {tag}_events.10
    title = {tag}_events.10_title
    desc = {tag}_events.10_desc
    picture = generic_event
    
    is_triggered_only = yes
    
    option = {
        name = {tag}_events.10_option_a
        country_event = {
            id = {tag}_events.11
            days = 7
        }
    }
}

# 第二个事件（7天后触发）
country_event = {
    id = {tag}_events.11
    title = {tag}_events.11_title
    desc = {tag}_events.11_desc
    picture = generic_event
    
    is_triggered_only = yes
    
    option = {
        name = {tag}_events.11_option_a
        add_political_power = 100
        country_event = {
            id = {tag}_events.12
            days = 7
        }
    }
    
    option = {
        name = {tag}_events.11_option_b
        add_stability = 0.10
    }
}

# 第三个事件（结束）
country_event = {
    id = {tag}_events.12
    title = {tag}_events.12_title
    desc = {tag}_events.12_desc
    picture = generic_event
    
    is_triggered_only = yes
    
    option = {
        name = {tag}_events.12_option_a
        set_country_flag = {tag}_event_chain_complete
    }
}
```

---

## 📋 决议模板

### 普通决议
```hoi4
decisions = {
    {TAG}_decisions = {
        icon = GFX_goal_generic_major_alliance
        
        {TAG}_economic_decision = {
            icon = GFX_goal_generic_industry
            
            cost = 50
            political_cost = yes
            
            available = {
                tag = {TAG}
                has_political_power > 50
            }
            
            visible = {
                tag = {TAG}
            }
            
            complete_effect = {
                add_political_power = -50
                random_owned_controlled_state = {
                    prioritize = { 123 }
                    add_extra_state_shared_building_slots = 1
                    add_building_construction = {
                        type = industrial_complex
                        level = 1
                        instant_build = yes
                    }
                }
            }
            
            ai_will_do = {
                factor = 1
            }
        }
    }
}
```

### 省份决议
```hoi4
decisions = {
    {TAG}_state_decisions = {
        icon = GFX_goal_generic_territory_or_war
        allowed = { tag = {TAG} }
        
        {TAG}_develop_state = {
            icon = GFX_goal_generic_construct_civ_factory
            cost_type = state
            
            target_state = {
                123 124 125               # 可用的省份ID列表
            }
            
            cost = 100
            
            available = {
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                    include_locked = yes
                }
            }
            
            visible = {
                123 = { is_owned_by = ROOT }
            }
            
            complete_effect = {
                add_extra_state_shared_building_slots = 2
                add_building_construction = {
                    type = industrial_complex
                    level = 2
                    instant_build = yes
                }
            }
            
            ai_will_do = {
                factor = 1
            }
        }
    }
}
```

---

## 🌐 本地化模板

### 完整本地化文件
```yaml
l_english:
 # 焦点
 {TAG}_political_base:0 "Political Foundation"
 {TAG}_political_base_desc:0 "Establish the political foundation for our nation."
 
 {TAG}_democratic_path:0 "Democratic Path"
 {TAG}_democratic_path_desc:0 "Embrace democracy and hold free elections."
 
 # 民族精神
 {TAG}_national_spirit:0 "National Spirit"
 {TAG}_national_spirit_desc:0 "Our nation stands united."
 
 {TAG}_military_reform:0 "Military Reform"
 {TAG}_military_reform_desc:0 "Modernize our armed forces."
 
 # 事件
 {tag}_events.1_title:0 "Important Decision"
 {tag}_events.1_desc:0 "A crucial decision must be made."
 {tag}_events.1_option_a:0 "Proceed with reform"

l_simp_chinese:
 {TAG}_political_base:0 "政治基础"
 {TAG}_political_base_desc:0 "为我们的国家建立政治基础。"
 
 {TAG}_democratic_path:0 "民主道路"
 {TAG}_democratic_path_desc:0 "拥抱民主，举行自由选举。"
 
 {TAG}_national_spirit:0 "民族精神"
 {TAG}_national_spirit_desc:0 "我们的国家团结一致。"
 
 {TAG}_military_reform:0 "军事改革"
 {TAG}_military_reform_desc:0 "现代化我们的武装力量。"
 
 {tag}_events.1_title:0 "重要决定"
 {tag}_events.1_desc:0 "必须做出关键决定。"
 {tag}_events.1_option_a:0 "推进改革"
```

### 带格式的本地化
```yaml
l_english:
 {TAG}_focus_effect:0 "§YPolitical Power§!: §G+100§!\n§YStability§!: §G+5%§!"
 {TAG}_focus_desc_detailed:0 "This focus provides:\n• §G100§! Political Power\n• §G5%§! Stability\n• Unlocks §Hnew decisions§!"
 
 {TAG}_event_tt:0 "§HThis will trigger an event§! in §Y7 days§!"
```

---

## 👤 人物模板

### 国家领导人
```hoi4
characters = {
    {TAG}_leader_name = {
        name = "Leader Name"
        
        portraits = {
            civilian = {
                large = "GFX_portrait_{TAG}_leader"
            }
        }
        
        country_leader = {
            ideology = neutrality
            traits = { authoritarian }
            expire = "1965.1.1"
            id = -1
        }
    }
}

# 在效果中设置
completion_reward = {
    set_country_leader = {
        ideology = neutrality
        leader = {TAG}_leader_name
    }
}
```

### 多角色人物
```hoi4
characters = {
    {TAG}_general_name = {
        name = "General Name"
        
        portraits = {
            army = {
                large = "GFX_portrait_{TAG}_general"
                small = "GFX_portrait_{TAG}_general_small"
            }
        }
        
        # 陆军元帅
        field_marshal = {
            traits = { brilliant_strategist defensive_doctrine }
            skill = 4
        }
        
        # 政治顾问（可选）
        advisor = {
            slot = political_advisor
            idea_token = {TAG}_general_advisor
            traits = { army_officer }
            cost = 150
        }
    }
}
```

---

## ⚡ 效果片段

### 政治效果
```hoi4
# 加政治点数
add_political_power = 100

# 加稳定度/战争支持度
add_stability = 0.05
add_war_support = 0.05

# 切换意识形态
set_politics = {
    ruling_party = fascism
    elections_allowed = no
}

# 增加意识形态支持度
add_popularity = {
    ideology = fascism
    popularity = 0.10
}

# 触发选举
hold_election = {
    ruling_party_type = democratic
}
```

### 军事效果
```hoi4
# 加经验
army_experience = 25
navy_experience = 25
air_experience = 25

# 加人力
add_manpower = 50000

# 创建战争目标
create_wargoal = {
    type = annex_everything
    target = GER
}

# 创建阵营
create_faction = {TAG}_alliance

# 加入阵营
add_to_faction = GER

# 保证独立
create_guarantee = { target = CZE }
```

### 经济效果
```hoi4
# 科技加成
add_tech_bonus = {
    name = {TAG}_tech_bonus
    bonus = 1.0
    uses = 1
    category = industry
}

# 加研究槽
add_research_slot = 1

# 加资源
add_resource = {
    type = steel
    amount = 24
    state = 762
}

# 建建筑
add_building_construction = {
    type = industrial_complex
    level = 1
    instant_build = yes
}
```

### 外交效果
```hoi4
# 好感度
GER = {
    add_opinion_modifier = {
        target = ROOT
        modifier = pol_german_cooperation
    }
}

# 转移省份
transfer_state = {
    state = 123
    target = GER
}

# 核心领土
123 = {
    add_core_by = ROOT
    add_claim_by = ROOT
}
```

---

## 🔍 触发器片段

### 国家条件
```hoi4
tag = {TAG}                          # 国家标签
has_government = fascism             # 意识形态
has_stability > 0.5                  # 稳定度
has_war_support > 0.3                # 战争支持度
has_political_power > 100           # 政治点数
has_war = yes                        # 是否在战争中
has_capitulated = no                 # 是否投降
```

### 领土条件
```hoi4
controls_state = 123                 # 控制省份
owns_state = 123                     # 拥有省份
123 = { is_owned_by = ROOT }         # 省份归属
123 = { is_controlled_by = ROOT }    # 省份控制
num_of_controlled_states > 10        # 控制省份数
```

### 科技与焦点
```hoi4
has_tech = infantry_equipment_1      # 已研究科技
has_completed_focus = {focus_id}     # 完成焦点
is_in_faction = yes                  # 在阵营中
faction_leader = yes                # 阵营领袖
```

### 时间条件
```hoi4
date > 1936.1.1                     # 日期
date < 1939.1.1
```

### 逻辑组合
```hoi4
OR = {
    has_stability > 0.7
    has_war_support > 0.5
}

AND = {
    controls_state = 123
    controls_state = 124
}

NOT = { has_war_with = GER }

# 复杂组合
OR = {
    AND = {
        has_government = fascism
        has_stability > 0.5
    }
    AND = {
        has_government = communism
        has_war_support > 0.5
    }
}
```

---

**使用提示**：
1. 将 `{TAG}` 替换为实际国家标签（如 GER, SOV, JAP）
2. 将 `{tag}` 替换为小写标签用于事件命名空间（如 ger, sov, jap）
3. 将 `{id}` 替换为实际的 ID 名称
4. 检查省份 ID 是否正确（使用 `tdebug` 命令）
