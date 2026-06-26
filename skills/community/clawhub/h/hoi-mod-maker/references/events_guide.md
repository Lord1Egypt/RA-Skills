# HOI4 事件系统完整参考

## 目录

1. [文件结构](#文件结构)
2. [命名空间](#命名空间)
3. [国家事件](#国家事件)
4. [新闻事件](#新闻事件)
5. [事件触发](#事件触发)
6. [选项系统](#选项系统)
7. [常用效果](#常用效果)
8. [示例代码](#示例代码)

---

## 文件结构

```
events/{mod_name}_events.txt
events/{mod_name}_news.txt
```

### 文件头

```
# 事件文件 - {Mod名称}
# 添加命名空间声明
add_namespace = {mod_name}
```

---

## 命名空间

### 声明命名空间

```
add_namespace = poland_crisis
```

### 事件ID格式

```
{namespace}.{number}

# 示例
poland_crisis.1      # 命名空间.编号
poland_crisis.2
```

### 命名空间作用

- 防止事件ID冲突
- 便于组织和调试
- 允许其他mod引用

---

## 国家事件

### 基础模板

```
country_event = {
    id = {namespace}.{number}
    title = {event_title_key}
    desc = {event_desc_key}
    picture = {GFX_name}
    
    is_triggered_only = yes
    
    option = {
        name = {option_key}
        {effects}
    }
}
```

### 完整模板

```
country_event = {
    id = poland_crisis.1
    title = poland_crisis.1_title
    desc = poland_crisis.1_desc
    picture = generic_event
    
    # 触发条件（可选）
    trigger = {
        tag = POL
        date > 1939.1.1
        has_completed_focus = POL_beck_ribbentrop_path
    }
    
    # 平均触发时间（可选）
    mean_time_to_happen = {
        days = 30
        
        modifier = {
            add = 15
            has_stability < 0.5
        }
        
        modifier = {
            factor = 0.5
            has_war_with = GER
        }
    }
    
    # 是否仅触发（可选）
    is_triggered_only = yes
    
    # 是否隐藏（可选）
    hidden = no
    
    # 选项
    option = {
        name = poland_crisis.1_option_a
        
        # 效果
        add_political_power = 50
        
        # 隐藏效果
        hidden_effect = {
            set_country_flag = poland_crisis_flag
        }
        
        # 触发其他事件
        country_event = {
            id = poland_crisis.2
            days = 3
        }
    }
    
    option = {
        name = poland_crisis.1_option_b
        add_stability = 0.05
    }
}
```

---

## 新闻事件

### 新闻事件模板

```
news_event = {
    id = news.100
    title = news.100_title
    desc = news.100_desc
    picture = generic_event
    
    # 新闻事件特有字段
    
    # 是否显示主要新闻（可选）
    major = yes
    
    # 发送给谁
    # 默认发送给所有国家
    # 可用限定：
    # - filter = news_poland      # 使用预定义筛选器
    # - tag = GER POL             # 特定国家
    
    option = {
        name = news.100_option_a
    }
}
```

### 新闻事件完整示例

```
news_event = {
    id = news.poland_war
    title = news.poland_war_title
    desc = news.poland_war_desc
    picture = generic_war
    
    major = yes
    
    option = {
        name = news.option_interesting
        trigger = {
            tag = GER
        }
    }
    
    option = {
        name = news.option_interesting
        trigger = {
            tag = SOV
        }
    }
    
    option = {
        name = news.option_interesting
    }
}
```

---

## 事件触发

### 从焦点触发

```
focus = {
    id = POL_danzig_or_war
    
    completion_reward = {
        country_event = {
            id = poland_crisis.1
            days = 1
        }
    }
}
```

### 从效果触发

```
# 立即触发
country_event = { id = poland_crisis.1 }

# 延迟触发
country_event = {
    id = poland_crisis.1
    days = 7
    random_days = 3    # 额外随机天数
}

# 从隐藏效果触发
hidden_effect = {
    country_event = {
        id = poland_crisis.1
        days = 1
    }
}
```

### 从决议触发

```
{decision_id} = {
    complete_effect = {
        country_event = { id = poland_crisis.1 }
    }
}
```

### 从其他事件触发

```
option = {
    name = poland_crisis.1_option_a
    country_event = {
        id = poland_crisis.2
        days = 3
    }
}
```

### 从on_action触发

```
# 在 common/on_actions/ 中定义
on_actions = {
    on_startup = {
        effect = {
            country_event = {
                id = poland_crisis.1
                days = 1
            }
        }
    }
}
```

---

## 选项系统

### 基础选项

```
option = {
    name = {option_key}
    {effects}
}
```

### 带触发条件的选项

```
option = {
    name = poland_crisis.1_option_a
    
    # 只有满足条件的选项才显示
    trigger = {
        political_power > 100
    }
    
    # 执行效果
    add_political_power = -100
}
```

### 带AI权重的选项

```
option = {
    name = poland_crisis.1_option_a
    
    # AI选择权重
    ai_chance = {
        factor = 5
        
        modifier = {
            add = 10
            has_war_with = GER
        }
        
        modifier = {
            factor = 0
            has_stability < 0.3
        }
    }
}
```

### 隐藏选项

```
option = {
    name = poland_crisis.1_hidden_option
    
    # 对玩家隐藏但AI可选（不常用）
    hidden = yes
}
```

---

## 常用效果

### 政治类

```
# 政治点数
add_political_power = 100
add_political_power = -50

# 稳定度/战争支持度
add_stability = 0.05
add_war_support = 0.05
add_stability = -0.10

# 意识形态支持度
add_popularity = {
    ideology = fascism
    popularity = 0.10
}

# 切换意识形态
set_politics = {
    ruling_party = fascism
    elections_allowed = no
}
```

### 民族精神

```
# 添加
add_ideas = POL_sanacja_regime

# 移除
remove_ideas = POL_sanacja_regime

# 临时添加
add_timed_idea = {
    idea = POL_economic_boost
    days = 365
}

# 交换（先移除再添加）
swap_ideas = {
    remove_idea = POL_economic_crisis
    add_idea = POL_economic_recovery
}
```

### 领土操作

```
# 核心领土
{state_id} = {
    add_core_by = ROOT
    add_claim_by = ROOT
}

# 移交领土
transfer_state = {
    target = GER
    state = 9          # 但泽
}

# 获得领土
transfer_state = {
    state = 10
    target = POL
}
```

### 外交关系

```
# 观感修正
GER = {
    add_opinion_modifier = {
        target = ROOT
        modifier = POL_german_cooperation
    }
}

# 保证独立
create_guarantee = { target = CZE }

# 宣战
create_wargoal = {
    type = annex_everything
    target = GER
}

# 加入阵营
add_to_faction = GER

# 创建阵营
create_faction = POL_international_block
```

### 军事类

```
# 经验值
army_experience = 25
navy_experience = 25
air_experience = 25

# 人力
add_manpower = 50000
add_manpower = -10000

# 创建师
create_unit = {
    division = "波兰第一步兵师"
    division_template = "步兵师模板"
    start_province = { x y }
    amount = 1
}
```

### 标记系统

```
# 国家标记
set_country_flag = poland_crisis_flag
clr_country_flag = poland_crisis_flag

# 带过期时间的标记
set_country_flag = {
    flag = poland_crisis_flag
    days = 365
    value = 1    # 可选，用于变量
}

# 全局标记
set_global_flag = world_war_started

# 检查标记（在触发条件中）
has_country_flag = poland_crisis_flag
```

### 科技与研究

```
# 研究加成
add_tech_bonus = {
    name = POL_industrial_bonus
    bonus = 0.5
    uses = 1
    category = industrial
}

# 解锁科技
set_technology = {
    infantry_equipment_1 = 1
    basic_machine_tools = 1
}

# 研究槽位
add_research_slot = 1
```

---

## 示例代码

### 完整事件示例

```
# 命名空间声明
add_namespace = poland_crisis

# 事件1：但泽危机
country_event = {
    id = poland_crisis.1
    title = poland_crisis.1_title
    desc = poland_crisis.1_desc
    picture = generic_diplomatic
    
    trigger = {
        tag = POL
        date > 1939.1.1
        NOT = { has_war_with = GER }
        9 = { is_owned_by = POL }    # 但泽
    }
    
    mean_time_to_happen = {
        days = 30
        modifier = {
            factor = 0.5
            has_war_with = SOV
        }
    }
    
    is_triggered_only = no
    
    option = {
        name = poland_crisis.1_refuse
        
        # 德波关系恶化
        GER = {
            add_opinion_modifier = {
                target = ROOT
                modifier = poland_refused_danzig
            }
        }
        
        # 触发德国反应事件
        hidden_effect = {
            GER = {
                country_event = {
                    id = poland_crisis.2
                    days = 1
                }
            }
        }
        
        # 增加战争支持度
        add_war_support = 0.10
    }
    
    option = {
        name = poland_crisis.1_accept
        
        # 失去但泽
        transfer_state = {
            state = 9
            target = GER
        }
        
        # 政治点数惩罚
        add_political_power = -100
        
        # 稳定度下降
        add_stability = -0.10
        
        # 德波关系改善
        GER = {
            add_opinion_modifier = {
                target = ROOT
                modifier = poland_accepted_danzig
            }
        }
    }
}

# 事件2：德国的反应
country_event = {
    id = poland_crisis.2
    title = poland_crisis.2_title
    desc = poland_crisis.2_desc
    picture = generic_war
    
    is_triggered_only = yes
    
    option = {
        name = poland_crisis.2_war
        
        # 对波兰宣战
        create_wargoal = {
            type = annex_everything
            target = POL
        }
        
        # 创建战争目标后触发战争
        hidden_effect = {
            declare_war_on = {
                target = POL
                type = annex_everything
            }
        }
        
        # 触发新闻事件
        news_event = {
            id = news.poland_war
            days = 1
        }
    }
    
    option = {
        name = poland_crisis.2_wait
        
        # 德波关系进一步恶化
        POL = {
            add_opinion_modifier = {
                target = ROOT
                modifier = german_hostility
            }
        }
    }
}
```

### 对应本地化文件

```yaml
l_english:
 # 事件1
 poland_crisis.1_title:0 "但泽归属问题"
 poland_crisis.1_desc:0 "德国向我们提出了但泽归属问题，声称但泽应当回归德国。我们必须做出决定..."
 poland_crisis.1_refuse:0 "拒绝他们的无理要求！"
 poland_crisis.1_accept:0 "接受他们的条件..."
 
 # 事件2
 poland_crisis.2_title:0 "波兰的拒绝"
 poland_crisis.2_desc:0 "波兰拒绝了我们对但泽的要求！"
 poland_crisis.2_war:0 "那就用战争解决！"
 poland_crisis.2_wait:0 "暂时等待..."
```

---

## 高级技巧

### 链式事件

```
# 事件A触发事件B，事件B触发事件C
country_event = {
    id = chain.1
    
    option = {
        name = chain.1_option
        country_event = { id = chain.2 days = 3 }
    }
}

country_event = {
    id = chain.2
    
    option = {
        name = chain.2_option
        country_event = { id = chain.3 days = 3 }
    }
}
```

### 条件效果

```
option = {
    name = event.1_option
    
    if = {
        limit = { political_power > 100 }
        add_political_power = -100
        add_stability = 0.05
    }
    else = {
        add_stability = -0.05
    }
}
```

### 随机效果

```
option = {
    name = event.1_option
    
    random_effect = {
        chance = 50
        add_political_power = 100
    }
    random_effect = {
        chance = 50
        add_stability = 0.10
    }
}
```

### 对象操作

```
# 对特定国家执行效果
GER = {
    add_opinion_modifier = {
        target = ROOT
        modifier = diplomatic_tension
    }
}

# 获取随机国家
random_country = {
    limit = {
        is_neighbor_of = ROOT
        is_at_war_with = no
    }
    add_opinion_modifier = {
        target = ROOT
        modifier = improved_relations
    }
}
```
