# HOI4 完整 Mod 教程 - 创建自定义国家

本教程将创建一个完整的小型 mod，展示所有核心系统的实际应用。

---

## 📋 项目概述

**目标**: 创建一个虚构的东欧国家 "威塞克斯共和国" (Republic of Wessex, 标签: WEX)

**包含内容**:
- 完整国策树（政治+工业分支）
- 民族精神系统
- 事件链
- 本地化（英文+中文）
- 自定义修正值

---

## 📁 文件结构

```
wex_republic_mod/
├── descriptor.mod
├── thumbnail.png
│
├── common/
│   ├── national_focus/
│   │   └── wex_focus.txt
│   ├── ideas/
│   │   └── wex_ideas.txt
│   └── modifiers/
│       └── wex_modifiers.txt
│
├── events/
│   └── wex_events.txt
│
└── localisation/
    ├── english/
    │   ├── focus_l_english.yml
    │   ├── ideas_l_english.yml
    │   └── events_l_english.yml
    └── simp_chinese/
        ├── focus_l_simp_chinese.yml
        ├── ideas_l_simp_chinese.yml
        └── events_l_simp_chinese.yml
```

---

## 1. descriptor.mod

```
name = "Republic of Wessex"
supported_version = "1.14.*"
tags = {
    "National Focus"
    "Gameplay"
}
picture = "thumbnail.png"

# 可选
replace_path = ""
```

---

## 2. 国策树 (common/national_focus/wex_focus.txt)

```hoi4
# =====================
# 威塞克斯共和国国策树
# =====================

focus_tree = {
    id = wex_focus
    
    # === 国家权重 ===
    country = {
        factor = 0
        modifier = {
            add = 10
            tag = WEX
        }
    }
    
    default = no
    
    initial_show_position = {
        x = 500
        y = 300
    }
    
    continuous_focus_position = { x = 500 y = 1300 }
    
    # ==================== 政治分支 ====================
    
    # 根节点：共和国理想
    focus = {
        id = WEX_republic_ideals
        icon = GFX_focus_generic_democratic_constitution
        x = 0
        y = 0
        cost = 5
        
        search_filters = { FOCUS_FILTER_POLITICAL }
        
        completion_reward = {
            add_political_power = 50
            add_stability = 0.05
            
            add_popularity = {
                ideology = democratic
                popularity = 0.05
            }
        }
    }
    
    # 二选一：军事强化 vs 民主改革
    focus = {
        id = WEX_military_focus
        prerequisite = { focus = WEX_republic_ideals }
        
        mutually_exclusive = { focus = WEX_civilian_focus }
        
        icon = GFX_focus_generic_military
        x = -1
        y = 1
        relative_position_id = WEX_republic_ideals
        cost = 10
        
        available = {
            has_government = democratic
        }
        
        search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_ARMY_XP }
        
        completion_reward = {
            # 军事经验
            army_experience = 50
            
            # 添加临时民族精神
            add_timed_idea = {
                idea = WEX_military_buildup
                days = 730  # 2年
            }
            
            # 条件效果
            if = {
                limit = { has_war = yes }
                army_experience = 25
            }
        }
    }
    
    focus = {
        id = WEX_civilian_focus
        prerequisite = { focus = WEX_republic_ideals }
        
        mutually_exclusive = { focus = WEX_military_focus }
        
        icon = GFX_focus_generic_industry
        x = 1
        y = 1
        relative_position_id = WEX_republic_ideals
        cost = 10
        
        available = {
            has_government = democratic
            has_stability > 0.4
        }
        
        search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_STABILITY }
        
        completion_reward = {
            add_stability = 0.10
            add_political_power = 100
            
            # 所有核心省份效果
            every_core_state = {
                limit = {
                    is_fully_controlled_by = ROOT
                    infrastructure < 5
                }
                random_select_amount = 2
                add_building_construction = {
                    type = infrastructure
                    level = 1
                    instant_build = yes
                }
            }
        }
    }
    
    # ==================== 工业分支 ====================
    
    # 根节点：工业重建
    focus = {
        id = WEX_industrial_rebuild
        icon = GFX_focus_generic_construct_civ_factory
        x = 3
        y = 0
        cost = 5
        
        search_filters = { FOCUS_FILTER_INDUSTRY }
        
        completion_reward = {
            # 初始化变量
            set_variable = {
                var = WEX_industry_progress
                value = 1
            }
            
            # 科技加成
            add_tech_bonus = {
                name = WEX_industrial_bonus
                bonus = 0.5
                uses = 1
                category = industry
            }
        }
    }
    
    # 中级工业
    focus = {
        id = WEX_heavy_industry
        prerequisite = { focus = WEX_industrial_rebuild }
        icon = GFX_focus_generic_arms_factory
        x = 3
        y = 1
        relative_position_id = WEX_industrial_rebuild
        cost = 10
        
        search_filters = { FOCUS_FILTER_INDUSTRY }
        
        available = {
            num_of_owned_factories > 10
        }
        
        completion_reward = {
            # 追踪变量
            add_to_variable = {
                var = WEX_industry_progress
                value = 1
            }
            
            # 在指定省份建造
            random_owned_controlled_state = {
                prioritize = { 100 101 102 }  # 威塞克斯核心省份
                limit = {
                    free_building_slots = {
                        building = arms_factory
                        size > 0
                        include_locked = yes
                    }
                }
                add_extra_state_shared_building_slots = 1
                add_building_construction = {
                    type = arms_factory
                    level = 2
                    instant_build = yes
                }
                set_state_flag = WEX_heavy_industry_built
            }
            
            # 触发事件
            country_event = {
                id = wex.100
                days = 7
            }
            
            # 隐藏效果
            hidden_effect = {
                set_country_flag = WEX_heavy_industry_done
            }
        }
    }
    
    # 高级工业：资源开发
    focus = {
        id = WEX_resource_exploitation
        prerequisite = { focus = WEX_heavy_industry }
        icon = GFX_focus_generic_resource
        x = 3
        y = 2
        relative_position_id = WEX_heavy_industry
        cost = 10
        
        search_filters = { FOCUS_FILTER_INDUSTRY FOCUS_FILTER_INTERNATIONAL_TRADE }
        
        available = {
            check_variable = {
                var = WEX_industry_progress
                value > 1
            }
        }
        
        completion_reward = {
            # 添加资源
            add_resource = {
                type = steel
                amount = 16
                state = 100
            }
            
            add_resource = {
                type = aluminum
                amount = 8
                state = 101
            }
            
            # 铁路建设
            build_railway = {
                level = 1
                path = { 100 101 102 }
            }
            
            # 动态修饰符
            add_dynamic_modifier = {
                modifier = WEX_industrial_boom
                days = 365
            }
        }
    }
    
    # ==================== 连续焦点 ====================
    
    focus = {
        id = WEX_continuous_industry
        icon = GFX_focus_generic_production
        x = 0
        y = 0
        continuous = yes
        
        modifier = {
            production_speed_factory_factor = 0.10
        }
        
        search_filters = { FOCUS_FILTER_INDUSTRY }
    }
}
```

---

## 3. Ideas 系统 (common/ideas/wex_ideas.txt)

```hoi4
ideas = {
    # ==================== 国家精神 ====================
    country = {
        # 起始精神：共和国传统
        WEX_republican_tradition = {
            allowed = {
                original_tag = WEX
                always = no
            }
            
            allowed_civil_war = { always = no }
            
            removal_cost = -1
            
            picture = generic_democratic_regime
            
            modifier = {
                political_power_gain = 0.05
                stability_factor = 0.05
                
                democratic_drift = 0.02
                fascism_drift = -0.01
                communism_drift = -0.01
            }
        }
        
        # 临时精神：军事建设
        WEX_military_buildup = {
            allowed = {
                original_tag = WEX
            }
            
            removal_cost = 0
            
            picture = generic_military
            
            modifier = {
                army_org_factor = 0.05
                army_attack_factor = 0.05
                
                # 负面效果
                consumer_goods_factor = 0.05
            }
        }
    }
    
    # ==================== 政治顾问 ====================
    political_advisor = {
        WEX_democratic_reformer = {
            allowed = { original_tag = WEX }
            
            picture = GFX_idea_democratic_politician
            
            democratic = yes
            
            modifier = {
                democratic_drift = 0.10
                stability_weekly = 0.05
            }
        }
        
        WEX_military_advisor = {
            allowed = { original_tag = WEX }
            
            picture = GFX_idea_military_advisor
            
            modifier = {
                army_experience_gain_factor = 0.10
                army_leader_start_level = 1
            }
        }
    }
    
    # ==================== 设计商 ====================
    tank_manufacturer = {
        WEX_arms_company = {
            allowed = { original_tag = WEX }
            
            picture = GFX_idea_generic_tank_manufacturer
            
            removal_cost = 200
            
            modifier = {
                tank_reliability_factor = 0.10
                tank_armor_factor = 0.05
                tank_research_speed_factor = 0.10
            }
        }
    }
}
```

---

## 4. 修饰符定义 (common/modifiers/wex_modifiers.txt)

```
# 动态修饰符定义

WEX_industrial_boom = {
    # 生产速度加成
    production_speed_industrial_complex_factor = 0.15
    production_speed_arms_factory_factor = 0.10
    
    # 工厂效率
    industrial_capacity_factory = 0.05
    
    # 研究加成
    industrial_research_speed = 0.10
}
```

---

## 5. 事件系统 (events/wex_events.txt)

```hoi4
# ====================
# 威塞克斯事件
# ====================

add_namespace = wex

# 工业：重工业完成事件
country_event = {
    id = wex.100
    title = wex.100.t
    desc = wex.100.d
    picture = GFX_report_event_generic_industry
    
    is_triggered_only = yes
    
    option = {
        name = wex.100.a
        add_political_power = 25
        army_experience = 10
    }
    
    option = {
        name = wex.100.b
        # 仅战争时显示
        trigger = { has_war = yes }
        
        add_political_power = 50
        army_experience = 20
    }
}

# 政治：共和国危机事件
country_event = {
    id = wex.200
    title = wex.200.t
    desc = wex.200.d
    picture = GFX_report_event_generic_political
    
    mean_time_to_happen = {
        days = 365
        
        modifier = {
            add = 180
            has_stability > 0.7
        }
        
        modifier = {
            add = -180
            has_stability < 0.3
        }
    }
    
    trigger = {
        tag = WEX
        date > 1938.1.1
        has_government = democratic
    }
    
    option = {
        name = wex.200.a
        # 镇压反对派
        add_stability = -0.05
        add_political_power = 100
        
        hidden_effect = {
            set_country_flag = WEX_opposition_suppressed
        }
    }
    
    option = {
        name = wex.200.b
        # 与反对派妥协
        add_stability = 0.05
        add_political_power = -50
        
        add_popularity = {
            ideology = democratic
            popularity = -0.05
        }
        
        # 触发后续事件
        country_event = {
            id = wex.201
            days = 30
        }
    }
}

# 后续事件
country_event = {
    id = wex.201
    title = wex.201.t
    desc = wex.201.d
    picture = GFX_report_event_generic_political
    
    is_triggered_only = yes
    
    option = {
        name = wex.201.a
        add_stability = 0.10
        add_political_power = 75
        
        set_country_flag = WEX_compromise_reached
    }
}

# 新闻事件：威塞克斯宣言
news_event = {
    id = news.wex_declaration
    title = news.wex_declaration.t
    desc = news.wex_declaration.d
    picture = GFX_news_event_generic_political
    
    major = yes
    
    option = {
        name = news.wex_declaration.a
    }
}
```

---

## 6. 本地化 - 英文 (localisation/english/focus_l_english.yml)

```yaml
l_english:
 # === 焦点名称 ===
 WEX_republic_ideals:0 "Republic Ideals"
 WEX_republic_ideals_desc:0 "The Republic of Wessex stands as a beacon of democracy in Eastern Europe."
 
 WEX_military_focus:0 "Military Focus"
 WEX_military_focus_desc:0 "Strengthen our armed forces to defend the republic."
 
 WEX_civilian_focus:0 "Civilian Focus"
 WEX_civilian_focus_desc:0 "Focus on civilian welfare and economic development."
 
 WEX_industrial_rebuild:0 "Industrial Reconstruction"
 WEX_industrial_rebuild_desc:0 "Rebuild our industrial base after years of neglect."
 
 WEX_heavy_industry:0 "Heavy Industry"
 WEX_heavy_industry_desc:0 "Develop heavy industry to support our military needs."
 
 WEX_resource_exploitation:0 "Resource Exploitation"
 WEX_resource_exploitation_desc:0 "Exploit our natural resources to fuel industrial growth."
 
 WEX_continuous_industry:0 "Continuous Industrial Effort"
```

---

## 7. 本地化 - 中文 (localisation/simp_chinese/focus_l_simp_chinese.yml)

```yaml
l_simp_chinese:
 # === 焦点名称 ===
 WEX_republic_ideals:0 "共和国理想"
 WEX_republic_ideals_desc:0 "威塞克斯共和国是东欧民主的灯塔。"
 
 WEX_military_focus:0 "军事优先"
 WEX_military_focus_desc:0 "加强武装力量，保卫共和国。"
 
 WEX_civilian_focus:0 "民生优先"
 WEX_civilian_focus_desc:0 "专注于民生福利和经济发展。"
 
 WEX_industrial_rebuild:0 "工业重建"
 WEX_industrial_rebuild_desc:0 "重建多年被忽视的工业基础。"
 
 WEX_heavy_industry:0 "重工业"
 WEX_heavy_industry_desc:0 "发展重工业以支持军事需求。"
 
 WEX_resource_exploitation:0 "资源开发"
 WEX_resource_exploitation_desc:0 "开发自然资源以推动工业增长。"
 
 WEX_continuous_industry:0 "持续工业建设"
```

---

## 8. Ideas 本地化 - 英文 (localisation/english/ideas_l_english.yml)

```yaml
l_english:
 # === 国家精神 ===
 WEX_republican_tradition:0 "Republican Tradition"
 WEX_republican_tradition_desc:0 "Wessex has a long tradition of democratic governance."
 
 WEX_military_buildup:0 "Military Buildup"
 WEX_military_buildup_desc:0 "The military is expanding rapidly."
 
 # === 顾问 ===
 WEX_democratic_reformer:0 "Democratic Reformer"
 WEX_military_advisor:0 "Military Advisor"
 WEX_arms_company:0 "Wessex Arms Company"
```

---

## 9. Ideas 本地化 - 中文 (localisation/simp_chinese/ideas_l_simp_chinese.yml)

```yaml
l_simp_chinese:
 # === 国家精神 ===
 WEX_republican_tradition:0 "共和国传统"
 WEX_republican_tradition_desc:0 "威塞克斯有悠久的民主治理传统。"
 
 WEX_military_buildup:0 "军事建设"
 WEX_military_buildup_desc:0 "军队正在快速扩张。"
 
 # === 顾问 ===
 WEX_democratic_reformer:0 "民主改革者"
 WEX_military_advisor:0 "军事顾问"
 WEX_arms_company:0 "威塞克斯军备公司"
```

---

## 10. 事件本地化 - 英文 (localisation/english/events_l_english.yml)

```yaml
l_english:
 # === 事件 wex.100 ===
 wex.100.t:0 "Heavy Industry Complete"
 wex.100.d:0 "Our heavy industry expansion is now complete. Production capacity has increased significantly."
 wex.100.a:0 "Excellent work!"
 wex.100.b:0 "This will help the war effort."
 
 # === 事件 wex.200 ===
 wex.200.t:0 "Political Crisis"
 wex.200.d:0 "Opposition forces are demanding reforms. How should we respond?"
 wex.200.a:0 "Suppress the opposition"
 wex.200.b:0 "Negotiate a compromise"
 
 # === 事件 wex.201 ===
 wex.201.t:0 "Compromise Reached"
 wex.201.d:0 "The opposition has agreed to our terms. Stability has been restored."
 wex.201.a:0 "Democracy prevails"
 
 # === 新闻事件 ===
 news.wex_declaration.t:0 "Wessex Declares Neutrality"
 news.wex_declaration.d:0 "The Republic of Wessex has declared its neutrality in the coming conflict."
 news.wex_declaration.a:0 "Interesting development"
```

---

## 11. 事件本地化 - 中文 (localisation/simp_chinese/events_l_simp_chinese.yml)

```yaml
l_simp_chinese:
 # === 事件 wex.100 ===
 wex.100.t:0 "重工业建设完成"
 wex.100.d:0 "我们的重工业扩张已经完成，产能显著提升。"
 wex.100.a:0 "干得好！"
 wex.100.b:0 "这将有助于战争。"
 
 # === 事件 wex.200 ===
 wex.200.t:0 "政治危机"
 wex.200.d:0 "反对派要求改革。我们该如何回应？"
 wex.200.a:0 "镇压反对派"
 wex.200.b:0 "妥协谈判"
 
 # === 事件 wex.201 ===
 wex.201.t:0 "达成妥协"
 wex.201.d:0 "反对派接受了我们的条件，稳定已恢复。"
 wex.201.a:0 "民主胜利"
 
 # === 新闻事件 ===
 news.wex_declaration.t:0 "威塞克斯宣布中立"
 news.wex_declaration.d:0 "威塞克斯共和国宣布在即将到来的冲突中保持中立。"
 news.wex_declaration.a:0 "有趣的动向"
```

---

## 📝 关键学习点

### 国策树要点
1. **权重系统**: `country` 块决定哪个国家使用此树
2. **相对定位**: 使用 `relative_position_id` 简化布局
3. **互斥焦点**: 需要**双向声明** `mutually_exclusive`
4. **变量追踪**: 使用 `set_variable` 和 `add_to_variable`
5. **条件效果**: `if` 块根据条件执行不同效果
6. **隐藏效果**: `hidden_effect` 不显示在提示中

### Ideas 要点
1. **allowed vs allowed_civil_war**: 区分初始可用和内战继承
2. **removal_cost**: `-1` = 永久，`0` = 免费
3. **ledger**: 军事精神需要指定标签页
4. **visible vs available**: 显示条件和可用条件

### 事件要点
1. **事件类型**: `country_event`/`state_event`/`news_event`
2. **触发方式**: `is_triggered_only` vs `mean_time_to_happen`
3. **条件选项**: `option` 内的 `trigger`
4. **作用域切换**: `ROOT`/`FROM`/`PREV`
5. **事件链**: 通过 `country_event` 触发后续事件

### 本地化要点
1. **编码**: UTF-8 带 BOM
2. **格式**: `key:0 "value"`
3. **命名规范**: `{TAG}_{name}` 避免冲突
4. **描述后缀**: `_desc` 自动关联

---

## ✅ 下一步

1. 将文件放入游戏 mod 目录
2. 使用 `-debug` 模式测试
3. 检查 `error.log` 中的错误
4. 调整数值平衡
5. 扩展更多分支和事件

---

**恭喜！你现在有了一个完整的 HOI4 mod 框架！**
