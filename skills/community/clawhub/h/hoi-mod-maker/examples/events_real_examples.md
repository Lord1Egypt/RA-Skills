# HOI4 真实游戏文件示例 - Events（事件）

本文档从游戏本地文件中提取真实代码示例。

---

## 1. 基础国家事件 - 外国政治影响

**文件**: `events/Generic.txt`

```hoi4
###########################
# COUNTRY INFLUENCING OUR POLITICS
###########################

add_namespace = generic

country_event = {
    id = generic.1
    title = generic.1.t
    
    # 多个描述文本（根据条件显示）
    desc = {
        text = generic.1.d_neutral_good
        trigger = {
            has_government = FROM
        }
    }
    desc = {
        text = generic.1.d_bad
        trigger = {
            NOT = { has_government = FROM }
        }
    }
    
    picture = GFX_report_event_generic_read_write
    
    # 仅触发事件（不能随机触发）
    is_triggered_only = yes
    
    # 选项1：意识形态相同
    option = {
        name = generic.1.a
        trigger = {
            has_government = FROM
        }
        
        # 条件效果预览
        if = {
            limit = {
                FROM = {
                    tag = ENG
                    has_completed_focus = uk_china_focus
                }
                tag = event_target:WTT_current_china_leader
            }
            effect_tooltip = {
                add_offsite_building = { type = arms_factory level = 2 }
            }
        }
    }
    
    # 选项2：意识形态不同
    option = {
        name = generic.1.b
        trigger = {
            NOT = { has_government = FROM }
        }
        
        # 条件效果预览
        if = {
            limit = {
                FROM = {
                    tag = ENG
                    has_completed_focus = uk_china_focus
                }
                tag = event_target:WTT_current_china_leader
            }
            effect_tooltip = {
                add_offsite_building = { type = arms_factory level = 2 }
            }
        }
        
        # 芬兰特殊逻辑示例
        if = {
            limit = {
                original_tag = FIN
                FROM = { original_tag = EST }
                has_idea = EST_vaps_organizing_in_FIN
            }
            effect_tooltip = {
                add_ideas = EST_vaps_organizing_in_FIN
            }
            custom_effect_tooltip = DECISION_WILL_BE_REMOVED_IF
            effect_tooltip = {
                activate_decision = ban_fascist_party
            }
        }
    }
}
```

**要点分析**：
- `add_namespace`：命名空间定义
- 多个 `desc` 块：根据条件显示不同文本
- `FROM`：事件发送方
- `is_triggered_only`：只能通过效果触发
- `option` 内的 `trigger`：条件选项（不满足不显示）
- `effect_tooltip`：仅显示效果预览，不执行
- `if` 条件块：条件执行效果

---

## 2. 加入阵营请求事件

**文件**: `events/Generic.txt`

```hoi4
# Generic request to join major Alliance
country_event = {
    id = generic.2
    title = generic.2.t
    
    trigger = {
        country_exists = FROM
    }
    
    desc = {
        text = generic.2.d.a    # FROM和ROOT都是民主
        trigger = {
            AND = {
                FROM = { has_government = democratic }
                has_government = democratic
            }
        }
    }
    desc = {
        text = generic.2.d.b    # FROM和ROOT都是法西斯
        trigger = {
            AND = {
                FROM = { has_government = fascism }
                has_government = fascism
            }
        }
    }
    desc = {
        text = generic.2.d.c    # FROM和ROOT都是共产主义
        trigger = {
            AND = {
                FROM = { has_government = communism }
                has_government = communism
            }
        }
    }
    desc = {
        text = generic.2.d.d    # 其他情况
        trigger = {
            OR = {
                AND = {
                    FROM = { has_government = democratic }
                    has_government = fascism
                }
                AND = {
                    FROM = { has_government = fascism }
                    has_government = democratic
                }
            }
        }
    }
    
    picture = GFX_report_event_usa_ill_will_toward_red_cross
    
    is_triggered_only = yes
    
    option = {
        name = generic.2.a    # 加入阵营
        tooltip = {           # 效果提示
            join_alliance = ROOT
            ROOT = {
                country_event = { id = generic.2.response days = 1 }
            }
        }
    }
    
    option = {
        name = generic.2.b    # 拒绝请求
        ROOT = {
            country_event = { id = generic.2.response_rejected days = 1 }
        }
    }
}
```

**要点分析**：
- 复杂的 `desc` 条件组合
- `tooltip` 块：显示效果但不执行
- `ROOT` 作用域切换
- 嵌套事件链：触发响应事件

---

## 3. 平均触发时间事件

**文件**: `events/Generic.txt`（推断）

```hoi4
country_event = {
    id = generic.political_events
    
    # 平均触发时间（MTTH）
    mean_time_to_happen = {
        days = 100    # 基础天数
        
        # 条件修正
        modifier = {
            add = 50    # 增加天数
            has_stability < 0.5
        }
        
        modifier = {
            add = -30   # 减少天数
            has_government = fascism
        }
        
        modifier = {
            factor = 0.5    # 乘以因子
            has_war = yes
        }
        
        modifier = {
            factor = 2      # 乘以因子
            has_war_with = GER
        }
    }
    
    trigger = {
        tag = POL
        has_government = democracy
        date > 1936.1.1
    }
    
    title = generic.political_events.t
    desc = generic.political_events.d
    picture = GFX_report_event_generic_political
    
    option = {
        name = generic.political_events.a
        add_stability = 0.05
        add_political_power = 50
    }
}
```

**要点分析**：
- `mean_time_to_happen`：平均触发时间
- `days`：基础天数
- `add`：增加天数
- `factor`：乘以因子
- 条件修正可以组合使用

---

## 4. 新闻事件

**文件**: 从游戏文件综合**

```hoi4
news_event = {
    id = news.poland_war
    title = news.poland_war.t
    desc = news.poland_war.d
    picture = GFX_news_event_poland_war
    
    # 重要事件（所有国家看到）
    major = yes
    
    option = {
        name = news.option_interesting
    }
    
    option = {
        name = news.option_worrying
        # 可选的额外效果
    }
}
```

**要点分析**：
- `news_event`：新闻事件类型
- `major = yes`：所有国家可见
- 通常只有一个选项
- 用于世界重大事件通知

---

## 5. 省份事件

**文件**: 从游戏文件综合**

```hoi4
state_event = {
    id = state_events.100
    title = state_events.100.t
    desc = state_events.100.d
    picture = GFX_report_event_local_resistance
    
    # 触发条件
    trigger = {
        is_owned_by = GER
        has_resistance = yes
        resistance > 0.5
    }
    
    mean_time_to_happen = {
        days = 30
    }
    
    # 省份作用域效果
    option = {
        name = state_events.100.a
        owner = {
            add_political_power = -20
        }
        set_state_flag = resistance_spreading
    }
    
    option = {
        name = state_events.100.b
        add_resistance = -0.2
        owner = {
            add_political_power = -10
        }
    }
}
```

**要点分析**：
- `state_event`：省份事件类型
- 省份作用域触发器
- `owner`：切换到所有者国家
- 省份标记 `set_state_flag`

---

## 6. 复杂选项事件

**文件**: 从游戏文件综合**

```hoi4
country_event = {
    id = country.complex_event
    title = country.complex_event.t
    desc = country.complex_event.d
    picture = GFX_report_event_generic_political
    
    is_triggered_only = yes
    
    # 选项1：基础效果
    option = {
        name = country.complex_event.option_a
        
        add_political_power = 100
        add_stability = 0.05
        
        # 隐藏效果
        hidden_effect = {
            set_country_flag = event_100_done
        }
    }
    
    # 选项2：条件选项（仅特定条件显示）
    option = {
        name = country.complex_event.option_b
        trigger = {
            has_government = fascism
            has_political_power > 50
        }
        
        add_political_power = -50
        add_popularity = {
            ideology = fascism
            popularity = 0.10
        }
        
        # 条件子效果
        if = {
            limit = { has_war = no }
            add_stability = 0.10
        }
        
        # 触发后续事件
        country_event = {
            id = country.follow_up_event
            days = 7
            random_days = 3
        }
    }
    
    # 选项3：显示效果提示但不执行
    option = {
        name = country.complex_event.option_c
        
        # 仅显示效果
        tooltip = {
            add_political_power = 200
            add_stability = 0.10
        }
        
        # 实际效果（与tooltip不同）
        hidden_effect = {
            add_political_power = 100
            add_stability = 0.05
        }
    }
}
```

**要点分析**：
- `hidden_effect`：隐藏效果（不显示在提示中）
- `tooltip`：仅显示效果（不执行）
- `trigger` 在 `option` 内：条件选项
- `if` 条件块：条件子效果
- `country_event` 触发后续事件
- `random_days`：随机延迟天数

---

## 7. 带作用域切换的事件

**文件**: 从游戏文件综合**

```hoi4
country_event = {
    id = country.scope_event
    title = country.scope_event.t
    desc = country.scope_event.d
    
    is_triggered_only = yes
    
    option = {
        name = country.scope_event.option_a
        
        # 当前国家效果
        add_political_power = 100
        
        # 切换到FROM（事件发送方）
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = improved_relations
            }
        }
        
        # 切换到随机国家
        random_country = {
            limit = {
                has_war_with = ROOT
            }
            add_opinion_modifier = {
                target = ROOT
                modifier = enemy_of_enemy
            }
        }
        
        # 所有邻国效果
        every_neighbor_country = {
            limit = {
                is_subject_of = ROOT
            }
            add_political_power = 20
        }
        
        # 特定标签国家
        GER = {
            if = {
                limit = { exists = yes }
                add_opinion_modifier = {
                    target = ROOT
                    modifier = diplomatic_action
                }
            }
        }
    }
}
```

**要点分析**：
- 多作用域切换：`FROM`、`ROOT`、`random_country`、`every_neighbor_country`
- `limit`：作用域条件限制
- 嵌套作用域：`FROM = { ... }`
- 标签作用域：`GER = { ... }`

---

## 8. 带变量的事件

**文件**: 从游戏文件综合**

```hoi4
country_event = {
    id = country.variable_event
    title = country.variable_event.t
    desc = country.variable_event.d
    
    is_triggered_only = yes
    
    option = {
        name = country.variable_event.option_a
        
        # 设置变量
        set_variable = {
            var = event_reward_amount
            value = 100
        }
        
        # 条件修改变量
        if = {
            limit = { has_stability > 0.5 }
            add_to_variable = {
                var = event_reward_amount
                value = 50
            }
        }
        
        # 使用变量作为效果参数
        add_political_power = var:event_reward_amount
        
        # 清除临时变量
        clear_variable = event_reward_amount
    }
    
    option = {
        name = country.variable_event.option_b
        
        # 随机变量值
        set_variable_to_random = {
            var = random_reward
            min = 50
            max = 200
            integer = yes
        }
        
        add_political_power = var:random_reward
        
        # 自定义提示
        custom_effect_tooltip = {
            localization_key = random_reward_tt
            VALUE = var:random_reward
        }
        
        clear_variable = random_reward
    }
}
```

**要点分析**：
- `set_variable`：设置变量
- `add_to_variable`：增加变量值
- `var:variable_name`：使用变量作为参数
- `set_variable_to_random`：设置随机值
- `clear_variable`：清除变量
- `custom_effect_tooltip`：自定义提示（带变量）

---

## 9. 带本地化的事件

**事件文件** (`events/Poland.txt`):
```hoi4
country_event = {
    id = poland.focus_event
    title = poland.focus_event.t
    desc = poland.focus_event.d
    picture = GFX_report_event_poland_industry
    
    option = {
        name = poland.focus_event.a
        add_political_power = 100
    }
}
```

**本地化文件** (`localisation/english/poland_l_english.yml`):
```yaml
l_english:
 poland.focus_event.t:0 "波兰工业化"
 poland.focus_event.d:0 "我们的五年计划即将完成，工业产出大幅提升。"
 poland.focus_event.a:0 "太好了！"
 
 # 带变量的本地化
 poland.variable_event.d:0 "我们获得了 £pol_power §Y[GetValue('event_reward_amount')]§! 政治点数。"
```

---

## 10. 事件链示例

```hoi4
# 事件1：触发事件
country_event = {
    id = chain.event_1
    title = chain.event_1.t
    desc = chain.event_1.d
    
    is_triggered_only = yes
    
    option = {
        name = chain.event_1.a
        
        # 效果
        add_political_power = 50
        
        # 触发事件2
        country_event = {
            id = chain.event_2
            days = 7
            random_days = 3
        }
    }
    
    option = {
        name = chain.event_1.b
        
        # 拒绝，不触发事件2
        add_stability = 0.05
    }
}

# 事件2：后续事件
country_event = {
    id = chain.event_2
    title = chain.event_2.t
    desc = chain.event_2.d
    
    is_triggered_only = yes
    
    option = {
        name = chain.event_2.a
        add_political_power = 100
    }
}
```

---

## 总结

事件系统的关键特性：

### 事件类型
- `country_event`：国家事件
- `state_event`：省份事件
- `news_event`：新闻事件

### 触发方式
- `is_triggered_only`：仅效果触发
- `mean_time_to_happen`：平均触发时间
- `trigger`：硬性条件

### 选项特性
- `trigger`：条件选项
- `hidden_effect`：隐藏效果
- `tooltip`：仅显示效果
- `if`：条件子效果

### 作用域
- `ROOT`：事件接收方
- `FROM`：事件发送方
- `PREV`：前一个作用域
- `THIS`：当前作用域

### 推荐学习路径
1. 阅读 `Generic.txt` 理解基础结构
2. 研究具体国家的复杂事件链
3. 注意变量和条件效果的使用
4. 练习编写带本地化的事件
