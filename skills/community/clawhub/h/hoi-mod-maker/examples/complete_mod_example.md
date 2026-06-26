# 完整 HOI4 Mod 示例 - 波兰历史扩展

本示例展示如何创建一个完整的 HOI4 mod，包含：
- 国策树
- 民族精神
- 本地化（中英文）
- 事件
- 决议

---

## 文件结构

```
poland_historical_expansion/
├── descriptor.mod
│
├── common/
│   ├── national_focus/
│   │   └── poland_historical.txt
│   │
│   ├── ideas/
│   │   └── poland_historical.txt
│   │
│   ├── decisions/
│   │   └── poland_decisions.txt
│   │
│   └── modifiers/
│       └── poland_modifiers.txt
│
├── events/
│   └── poland_historical_events.txt
│
├── localisation/
│   ├── english/
│   │   └── poland_historical_l_english.yml
│   └── simp_chinese/
│       └── poland_historical_l_simp_chinese.yml
│
└── interface/
    └── poland_gfx.gfx    # 可选：自定义图标
```

---

## 文件内容

### 1. descriptor.mod

```
name = "Poland Historical Expansion"
supported_version = "1.14.*"
tags = {
    "National Focus"
    "Historical"
    "Gameplay"
}
picture = "thumbnail.png"
```

### 2. common/national_focus/poland_historical.txt

见 `examples/poland_historical_focus.txt`

### 3. common/ideas/poland_historical.txt

```
ideas = {
    country = {
        POL_four_year_plan_idea = {
            allowed = {
                original_tag = POL
                always = no
            }
            
            allowed_civil_war = {
                always = no
            }
            
            removal_cost = -1
            
            picture = generic_industrial_concern
            
            modifier = {
                construction_speed_factory_factor = 0.05
                production_speed_infrastructure_factor = 0.10
                
                # 科技加成
                industrial_research_speed = 0.05
            }
        }
        
        POL_mobilization_effort = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = 100
            
            picture = generic_army
            
            modifier = {
                army_org_factor = 0.05
                land_terrain_defense = 0.05
            }
        }
        
        POL_cavalry_charge_idea = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = -1
            
            picture = generic_cavalry
            
            modifier = {
                cavalry_speed_factor = 0.10
                cavalry_attack_factor = 0.05
                cavalry_defence_factor = 0.05
            }
        }
        
        POL_anti_tank_effort_idea = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = -1
            
            picture = generic_anti_tank
            
            modifier = {
                anti_tank_attack_factor = 0.10
                anti_tank_defence_factor = 0.05
            }
        }
        
        POL_authoritarian_regime_idea = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = -1
            
            picture = generic_authoritarian_regime
            
            modifier = {
                political_power_gain = 0.05
                stability_factor = 0.05
                
                # 意识形态压制
                democratic_drift = -0.03
                communism_drift = -0.03
            }
        }
        
        POL_sanacja_totalitarian_idea = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = -1
            
            picture = generic_authoritarian_regime
            
            modifier = {
                political_power_gain = 0.10
                war_support_factor = 0.15
                
                # 意识形态压制
                democratic_drift = -0.05
                communism_drift = -0.05
                fascism_drift = -0.05
            }
        }
        
        POL_september_preparation_idea = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = -1
            
            picture = generic_war
            
            modifier = {
                army_org_factor = 0.10
                army_morale_factor = 0.05
                land_terrain_attack = 0.05
                land_terrain_defense = 0.05
            }
        }
        
        POL_german_cooperation = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = 100
            
            picture = generic_diplomatic
            
            modifier = {
                fascism_drift = 0.05
            }
        }
        
        POL_western_friendship = {
            allowed = {
                original_tag = POL
            }
            
            removal_cost = 100
            
            picture = generic_diplomatic
            
            modifier = {
                democratic_drift = 0.05
            }
        }
        
        # Opinion modifiers
        pol_german_cooperation = {
            research_speed_factor = 0.03
        }
        
        pol_western_friendship = {
            political_power_gain = 0.03
        }
        
        pol_refused_danzig = {
            attack_bonus_against = 0.05
        }
        
        pol_accepted_danzig = {
            production_speed_factory_factor = 0.05
        }
    }
}
```

### 4. common/decisions/poland_decisions.txt

```
decisions = {
    category = {
        name = POL_historical_category
        icon = GFX_goal_generic_major_alliance
        priority = 100
    }
    
    POL_historical_category = {
        POL_seize_danzig = {
            icon = GFX_goal_generic_territory_or_war
            cost = 50
            
            available = {
                tag = POL
                9 = { is_owned_by = GER }
                has_war_with = GER = no
            }
            
            complete_effect = {
                transfer_state = {
                    state = 9
                    target = ROOT
                }
                add_political_power = 50
            }
            
            ai_will_do = {
                factor = 5
            }
        }
    }
}
```

### 5. common/modifiers/poland_modifiers.txt

```
pol_german_cooperation = {
    fascism_drift = 0.05
    political_power_gain = 0.03
}

pol_western_friendship = {
    democratic_drift = 0.05
    political_power_gain = 0.03
}

pol_refused_danzig = {
    attack_bonus_against = 0.05
}

pol_accepted_danzig = {
    production_speed_factory_factor = 0.05
}
```

### 6. events/poland_historical_events.txt

```
add_namespace = poland_political

country_event = {
    id = poland_political.1
    title = poland_political.1_title
    desc = poland_political.1_desc
    picture = generic_political
    
    trigger = {
        tag = POL
        has_completed_focus = POL_toward_totalitarianism
    }
    
    is_triggered_only = yes
    
    option = {
        name = poland_political.1_option_a
        add_stability = 0.05
        add_war_support = 0.10
        set_country_flag = poland_totalitarian_flag
    }
}

country_event = {
    id = poland_political.2
    title = poland_political.2_title
    desc = poland_political.2_desc
    picture = generic_political
    
    trigger = {
        tag = POL
        has_completed_focus = POL_reopen_sejm_path
    }
    
    is_triggered_only = yes
    
    option = {
        name = poland_political.2_option_a
        add_political_power = -50
        add_stability = 0.10
        set_country_flag = poland_democratic_flag
    }
}

# 新闻事件：九月战争
news_event = {
    id = news.poland_september_war
    title = news.poland_september_war_title
    desc = news.poland_september_war_desc
    picture = generic_war
    
    major = yes
    
    option = {
        name = news.option_interesting
    }
}
```

### 7. localisation/english/poland_historical_l_english.yml

```yaml
l_english:
 # 焦点名称
 POL_seize_control_of_the_state:0 "Seize Control of the State"
 POL_seize_control_of_the_state_desc:0 "We must consolidate our authority over all branches of government."
 
 POL_rzeczpospolita_militia:0 "Rzeczpospolita Militia"
 POL_rzeczpospolita_militia_desc:0 "Strengthening our military forces is essential."
 
 POL_cavalry_tradition:0 "Cavalry Tradition"
 POL_cavalry_tradition_desc:0 "Poland's cavalry tradition is legendary."
 
 POL_four_year_economic_plan:0 "Four Year Economic Plan"
 POL_four_year_economic_plan_desc:0 "Implementing a comprehensive industrialization plan."
 
 POL_beck_ribbentrop_path:0 "Beck-Ribbentrop Path"
 POL_beck_ribbentrop_path_desc:0 "Seeking accommodation with Germany."
 
 POL_western_alliance_path:0 "Western Alliance Path"
 POL_western_alliance_path_desc:0 "Strengthening ties with France and Britain."
 
 POL_authoritarian_consolidation:0 "Authoritarian Consolidation"
 POL_authoritarian_consolidation_desc:0 "Consolidating authoritarian rule."
 
 POL_toward_totalitarianism:0 "Toward Totalitarianism"
 POL_toward_totalitarianism_desc:0 "Moving toward a totalitarian state."
 
 # 民族精神
 POL_four_year_plan_idea:0 "Four Year Plan"
 POL_four_year_plan_idea_desc:0 "Economic modernization program."
 POL_mobilization_effort:0 "Mobilization Effort"
 POL_cavalry_charge_idea:0 "Cavalry Charge Doctrine"
 POL_anti_tank_effort_idea:0 "Anti-Tank Warfare"
 POL_authoritarian_regime_idea:0 "Authoritarian Regime"
 POL_sanacja_totalitarian_idea:0 "Sanacja Totalitarianism"
 POL_september_preparation_idea:0 "September Campaign Preparation"
 
 # 修正值
 pol_german_cooperation:0 "German-Polish Cooperation"
 pol_western_friendship:0 "Western Friendship"
 pol_refused_danzig:0 "Refused Danzig"
 pol_accepted_danzig:0 "Accepted Danzig"
 
 # 事件
 poland_political.1_title:0 "Totalitarian Reforms"
 poland_political.1_desc:0 "The Sanacja regime moves toward total control."
 poland_political.1_option_a:0 "Excellent"
 
 poland_political.2_title:0 "Democratic Reforms"
 poland_political.2_desc:0 "The Sejm reopens with expanded powers."
 poland_political.2_option_a:0 "A new era"
 
 # 新闻
 news.poland_september_war_title:0 "September War Begins"
 news.poland_september_war_desc:0 "Germany has declared war on Poland!"
 
 # 决议类别
 POL_historical_category:0 "Polish Historical Decisions"
 POL_seize_danzig:0 "Seize Danzig"
 POL_seize_danzig_desc:0 "Reclaim Danzig for Poland."
```

### 8. localisation/simp_chinese/poland_historical_l_simp_chinese.yml

```yaml
l_simp_chinese:
 # 焦点名称
 POL_seize_control_of_the_state:0 "掌控国家权力"
 POL_seize_control_of_the_state_desc:0 "我们必须巩固对政府各部门的权威。"
 
 POL_rzeczpospolita_militia:0 "共和国民兵"
 POL_rzeczpospolita_militia_desc:0 "加强我们的军事力量至关重要。"
 
 POL_cavalry_tradition:0 "骑兵传统"
 POL_cavalry_tradition_desc:0 "波兰的骑兵传统传奇般的存在。"
 
 POL_four_year_economic_plan:0 "四年经济计划"
 POL_four_year_economic_plan_desc:0 "实施全面的工业化计划。"
 
 POL_beck_ribbentrop_path:0 "贝克-里宾特洛甫路线"
 POL_beck_ribbentrop_path_desc:0 "寻求与德国的妥协。"
 
 POL_western_alliance_path:0 "西方联盟路线"
 POL_western_alliance_path_desc:0 "加强与法国和英国的关系。"
 
 POL_authoritarian_consolidation:0 "威权整合"
 POL_authoritarian_consolidation_desc:0 "巩固威权统治。"
 
 POL_toward_totalitarianism:0 "走向极权"
 POL_toward_totalitarianism_desc:0 "迈向极权国家。"
 
 # 民族精神
 POL_four_year_plan_idea:0 "四年计划"
 POL_four_year_plan_idea_desc:0 "经济现代化计划。"
 POL_mobilization_effort:0 "动员努力"
 POL_cavalry_charge_idea:0 "骑兵冲锋学说"
 POL_anti_tank_effort_idea:0 "反坦克作战"
 POL_authoritarian_regime_idea:0 "威权政权"
 POL_sanacja_totalitarian_idea:0 "萨纳奇极权主义"
 POL_september_preparation_idea:0 "九月战役准备"
 
 # 修正值
 pol_german_cooperation:0 "德波合作"
 pol_western_friendship:0 "西方友谊"
 pol_refused_danzig:0 "拒绝但泽"
 pol_accepted_danzig:0 "接受但泽"
 
 # 事件
 poland_political.1_title:0 "极权改革"
 poland_political.1_desc:0 "萨纳奇政权走向全面控制。"
 poland_political.1_option_a:0 "太好了"
 
 poland_political.2_title:0 "民主改革"
 poland_political.2_desc:0 "议会重新召开，权力扩大。"
 poland_political.2_option_a:0 "新时代"
 
 # 新闻
 news.poland_september_war_title:0 "九月战争爆发"
 news.poland_september_war_desc:0 "德国向波兰宣战！"
 
 # 决议类别
 POL_historical_category:0 "波兰历史决议"
 POL_seize_danzig:0 "夺取但泽"
 POL_seize_danzig_desc:0 "为波兰夺回但泽。"
```

---

## 使用说明

1. 将上述文件结构复制到 HOI4 mod 目录
2. 修改 `descriptor.mod` 中的 mod 名称
3. 在游戏启动器中启用 mod
4. 选择波兰进行测试

## 调试技巧

- 使用 `debug_mode` 控制台命令查看错误
- 检查 `error.log` 文件
- 逐个文件测试，先确保焦点可用
- 本地化编码必须是 UTF-8
