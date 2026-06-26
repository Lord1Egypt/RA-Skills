# HOI4 事件完整示例解析

本文档使用真实游戏代码，配合详细注释，展示事件系统的所有关键用法。

---

## 📌 示例1：基础国家事件（波兰）

**来源**: `events/Poland.txt`

```hoi4
###########################
# Polish Events
###########################

# === 命名空间定义 ===
# 必须在文件顶部，用于组织事件ID
add_namespace = poland

# ============================================
# 事件1：东进扩张（但泽割让）
# ============================================
country_event = {
    id = poland.1    # 格式：命名空间.数字
    title = poland.1.t
    desc = poland.1.d
    picture = GFX_report_event_polish_tanks_01
    
    # 仅通过效果触发（不能随机触发）
    is_triggered_only = yes
    
    # === 选项1：接受法西斯影响 ===
    option = {
        name = poland.1.a
        
        # AI选择权重（可选）
        ai_chance = { factor = 10 }
        
        # 添加民族精神
        add_ideas = fascist_influence
        
        # 添加省份声索
        add_state_claim = 198    # 但泽
        add_state_claim = 199    # 东普鲁士
        add_state_claim = 201    # 其他
    }
    
    # === 选项2：寻求苏联支持 ===
    option = {
        name = poland.1.b
        ai_chance = { factor = 10 }
        
        # 改善与苏联的关系
        add_opinion_modifier = { 
            target = SOV 
            modifier = medium_increase 
        }
    }
}
```

### 💡 关键说明

**命名空间**:
- `add_namespace`: 组织事件ID
- 格式：`命名空间.数字`
- 避免ID冲突

**`is_triggered_only`**:
- `yes`: 只能通过效果触发
- `no`: 可以随机触发（需配置MTTH）

**`ai_chance`**:
- 决定AI选择哪个选项
- `factor`: 基础权重
- 可添加条件修正

---

## 📌 示例2：复杂选项逻辑（波兰）

**来源**: `events/Poland.txt`

```hoi4
# ============================================
# 事件2：苏联要求东方领土
# ============================================
country_event = {
    id = poland.2
    title = poland.2.t
    desc = poland.2.d
    picture = GFX_report_event_polish_tanks_01
    
    is_triggered_only = yes
    
    # === 选项1：接受要求 ===
    option = {
        name = poland.2.a
        
        # === 复杂的AI权重计算 ===
        ai_chance = { 
            factor = 30    # 基础权重30
            
            # 条件修正：有盟友或保证独立时权重为0
            modifier = {
                factor = 0
                OR = {
                    # 有其他主要国家盟友
                    any_other_country = {
                        is_major = yes
                        OR = {
                            is_in_faction_with = POL
                            has_guaranteed = POL
                        }
                    }
                    # 或有反苏协定
                    has_idea = anti_soviet_pact
                }
            }
        }
        
        # === 仅显示效果预览（不执行）===
        effect_tooltip = {
            FROM = {    # 切换到事件发送方（苏联）
                # 如果波兰拥有并控制省份，则转让
                if = {
                    limit = { POL = { owns_state = 96 controls_state = 96 } }
                    transfer_state = 96
                }
                if = {
                    limit = { POL = { owns_state = 95 controls_state = 95 } }
                    transfer_state = 95
                }
                if = {
                    limit = { POL = { owns_state = 94 controls_state = 94 } }
                    transfer_state = 94
                }
                # ... 更多省份
            }
        }
        
        # 触发苏联的响应事件
        FROM = { 
            country_event = { id = poland.3 } 
        }
    }
    
    # === 选项2：拒绝要求 ===
    option = {
        name = poland.2.b
        ai_chance = { factor = 70 }    # 基础权重70
        
        # 显示效果预览：苏联宣战
        effect_tooltip = {
            FROM = {
                create_wargoal = {
                    type = take_state_focus
                    target = POL
                    # 生成战争目标的省份列表
                    generator = { 96 95 94 93 91 89 97 784 }
                }
            }
        }
        
        # 触发苏联的拒绝响应事件
        FROM = { country_event = { id = poland.4 } }
    }
}
```

### 💡 关键说明

**`FROM`作用域**:
- 事件发送方（触发此事件的国家）
- 可在 `FROM = { }` 内执行效果

**`effect_tooltip`**:
- 仅显示效果预览，不实际执行
- 用于让玩家了解选择后果
- 实际效果在后续事件中执行

**复杂`ai_chance`**:
- 基础权重 + 条件修正
- 使用 `OR`、`AND`、`NOT` 组合
- 满足条件时权重×修正因子

---

## 📌 示例3：条件执行效果（波兰）

**来源**: `events/Poland.txt`

```hoi4
# ============================================
# 事件3：波兰割让东方领土
# ============================================
country_event = {
    id = poland.3
    title = poland.3.t
    desc = poland.3.d
    picture = GFX_report_event_polish_tanks_01
    
    is_triggered_only = yes
    
    option = {
        name = poland.3.a
        
        # === 多次条件转让 ===
        # 根据波兰是否实际控制省份来决定是否转让
        
        if = {
            limit = { 
                POL = { 
                    owns_state = 96        # 拥有省份
                    controls_state = 96    # 控制省份
                }
            }
            transfer_state = 96    # 转让给ROOT（苏联）
        }
        
        if = {
            limit = { 
                POL = { 
                    owns_state = 95
                    controls_state = 95 
                }
            }
            transfer_state = 95
        }
        
        if = {
            limit = { 
                POL = { 
                    owns_state = 94
                    controls_state = 94 
                }
            }
            transfer_state = 94
        }
        
        # ... 继续其他省份
        
        # 添加关系修正
        POL = {
            add_opinion_modifier = {
                target = ROOT
                modifier = pol_ceded_territory_to_sov
            }
        }
        
        # 触发波兰的确认事件
        POL = {
            country_event = { 
                id = poland.5 
                days = 1 
            }
        }
    }
}
```

### 💡 关键说明

**多次`if`块**:
- 每个条件独立判断
- 满足则执行，不满足则跳过
- 用于处理多个省份的可能情况

**`owns_state` vs `controls_state`**:
- `owns_state`: 省份归属权
- `controls_state`: 省份控制权（占领）
- 需要两者都满足才能转让

**事件链延迟**:
- `days = 1`: 1天后触发
- 避免同一时刻触发多个事件
- 给玩家时间阅读当前事件

---

## 📌 示例4：多描述文本事件（Generic）

**来源**: `events/Generic.txt`

```hoi4
###########################
# Generic Events
###########################

add_namespace = generic

# === 外国政治影响事件 ===
country_event = {
    id = generic.1
    title = generic.1.t
    
    # === 多个描述文本（根据条件显示）===
    desc = {
        text = generic.1.d_neutral_good
        trigger = {
            has_government = FROM    # FROM和ROOT意识形态相同
        }
    }
    desc = {
        text = generic.1.d_bad
        trigger = {
            NOT = { has_government = FROM }    # 意识形态不同
        }
    }
    
    picture = GFX_report_event_generic_read_write
    
    is_triggered_only = yes
    
    # === 选项1：意识形态相同 ===
    option = {
        name = generic.1.a
        
        # 条件：意识形态相同才显示
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
                add_offsite_building = { 
                    type = arms_factory 
                    level = 2 
                }
            }
        }
    }
    
    # === 选项2：意识形态不同 ===
    option = {
        name = generic.1.b
        
        # 条件：意识形态不同才显示
        trigger = {
            NOT = { has_government = FROM }
        }
        
        # 特殊逻辑：爱沙尼亚法西斯组织
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

### 💡 关键说明

**多个`desc`块**:
- 可定义多个描述文本
- 根据条件显示不同文本
- 从上到下检查，第一个满足的显示

**条件选项**:
- `option` 内的 `trigger`: 决定选项是否显示
- 不满足条件则选项不可见
- 可用于条件分支

**`event_target`**:
- 事件目标引用
- 在其他事件中设置的临时作用域
- 用于跨事件传递信息

---

## 📌 示例5：平均触发时间事件

**来源**: 从游戏文件综合

```hoi4
# === 政治危机事件 ===
country_event = {
    id = country.political_crisis
    title = country.political_crisis.t
    desc = country.political_crisis.d
    picture = GFX_report_event_generic_political
    
    # === 平均触发时间（MTTH）===
    mean_time_to_happen = {
        days = 365    # 平均365天触发
        
        # === 条件修正 ===
        modifier = {
            add = 180    # 增加180天
            has_stability > 0.7    # 高稳定度降低触发概率
        }
        
        modifier = {
            add = -180    # 减少180天
            has_stability < 0.3    # 低稳定度提高触发概率
        }
        
        modifier = {
            factor = 0.5    # 乘以0.5（减半）
            has_war = yes    # 战争状态下更频繁
        }
        
        modifier = {
            factor = 2.0    # 乘以2.0（加倍）
            is_major = yes    # 主要国家更少触发
        }
    }
    
    # === 触发条件 ===
    trigger = {
        tag = POL
        has_government = democratic
        date > 1938.1.1
        NOT = { has_country_flag = political_crisis_cooldown }
    }
    
    # === 选项1：镇压反对派 ===
    option = {
        name = country.political_crisis.a
        
        add_stability = -0.05
        add_political_power = 100
        
        hidden_effect = {
            set_country_flag = political_crisis_suppressed
            set_country_flag = {
                flag = political_crisis_cooldown
                days = 730    # 2年冷却
            }
        }
    }
    
    # === 选项2：妥协 ===
    option = {
        name = country.political_crisis.b
        
        add_stability = 0.05
        add_political_power = -50
        
        add_popularity = {
            ideology = democratic
            popularity = -0.05
        }
        
        # 触发后续事件
        country_event = {
            id = country.political_crisis_resolution
            days = 30
            random_days = 15    # 随机延迟15天
        }
    }
}
```

### 💡 关键说明

**MTTH计算**:
- 基础天数 + `add` 修正 + `factor` 修正
- 实际触发概率呈指数分布
- 多个修正可以叠加

**`add` vs `factor`**:
- `add`: 增加固定天数（绝对修正）
- `factor`: 乘以因子（相对修正）
- 通常混合使用

**隐藏效果**:
- `hidden_effect`: 不显示在提示中
- 用于设置冷却标记
- 避免事件频繁触发

---

## 📌 示例6：省份事件

**来源**: 从游戏文件综合

```hoi4
# === 抵抗运动事件 ===
state_event = {
    id = state.resistance_spreading
    title = state.resistance_spreading.t
    desc = state.resistance_spreading.d
    picture = GFX_report_event_local_resistance
    
    # === 触发条件 ===
    trigger = {
        is_owned_by = GER        # 德国拥有
        has_resistance = yes    # 有抵抗运动
        resistance > 0.5        # 抵抗>50%
    }
    
    # === 平均触发时间 ===
    mean_time_to_happen = {
        days = 60
        
        modifier = {
            factor = 0.5
            resistance > 0.8    # 高抵抗更频繁
        }
    }
    
    # === 选项1：镇压 ===
    option = {
        name = state.resistance_spreading.a
        
        # 切换到所有者国家作用域
        owner = {
            add_political_power = -30
            command_power = -10
        }
        
        # 省份效果
        add_resistance = -0.15
        set_state_flag = resistance_suppressed
        
        # 创建抵抗部队
        create_resistance_cell = {
            template = "underground_resistance"
            province = {
                # 省份内的特定省份
            }
        }
    }
    
    # === 选项2：忽视 ===
    option = {
        name = state.resistance_spreading.b
        
        owner = {
            add_stability = -0.02
        }
        
        # 增加抵抗
        add_resistance = 0.10
    }
}
```

### 💡 关键说明

**`state_event`**:
- 省份事件类型
- 触发器在省份作用域内检查
- 效果可影响省份和所有者

**`owner`作用域**:
- 切换到省份所有者国家
- 可执行国家级别效果

---

## 📌 示例7：新闻事件

**来源**: 从游戏文件综合

```hoi4
# === 德国入侵波兰新闻 ===
news_event = {
    id = news.germany_invades_poland
    title = news.germany_invades_poland.t
    desc = news.germany_invades_poland.d
    picture = GFX_news_event_german_tanks
    
    # === 重要新闻：所有国家可见 ===
    major = yes
    
    option = {
        name = news.option_interesting
        # 可选：添加效果
    }
}
```

### 💡 关键说明

**`news_event`**:
- 新闻事件类型
- 通常只有一个选项
- 用于重大世界事件通知

**`major`字段**:
- `yes`: 所有国家可见
- `no`: 仅相关国家可见

---

## 📌 示例8：带变量的事件

```hoi4
# === 工业奖励事件 ===
country_event = {
    id = country.industrial_reward
    title = country.industrial_reward.t
    desc = country.industrial_reward.d
    
    is_triggered_only = yes
    
    option = {
        name = country.industrial_reward.a
        
        # 设置随机奖励
        set_variable_to_random = {
            var = industrial_reward_amount
            min = 50
            max = 200
            integer = yes
        }
        
        # 使用变量
        add_political_power = var:industrial_reward_amount
        
        # 自定义提示（带变量）
        custom_effect_tooltip = {
            localization_key = industrial_reward_tt
            VALUE = var:industrial_reward_amount
        }
        
        # 清除变量
        clear_variable = industrial_reward_amount
    }
}
```

---

## 📝 本地化示例

```yaml
l_english:
 # 波兰事件
 poland.1.t:0 "Eastward Expansion"
 poland.1.d:0 "The Soviet Union has demanded the territories of Eastern Poland. We must decide..."
 poland.1.a:0 "Accept the demands"
 poland.1.b:0 "Seek Soviet support"
 
 poland.2.t:0 "Soviet Union Demands the East"
 poland.2.d:0 "The Soviet Union has formally demanded the return of Eastern Poland..."
 poland.2.a:0 "We have no choice"
 poland.2.b:0 "We will never surrender!"
 
 # 提示文本
 poland.3.t:0 "Poland Cedes the East"
 poland.3.d:0 "The Polish government has accepted our demands and ceded the territories..."
 poland.3.a:0 "Excellent"
 
 # 带变量的文本
 industrial_reward_tt:0 "We gained §Y[GetValue('industrial_reward_amount')]§! political power."
```

---

## ✅ 最佳实践总结

### 1. 事件类型选择
| 类型 | 触发方式 | 可见性 |
|------|----------|--------|
| `country_event` | 效果触发或MTTH | 目标国家 |
| `state_event` | MTTH或效果 | 省份所有者 |
| `news_event` | 效果触发 | `major`决定 |

### 2. 字段使用建议
- `is_triggered_only`: 推荐使用（更好控制）
- `mean_time_to_happen`: 配合 `trigger` 使用
- `hidden_effect`: 隐藏实现细节

### 3. 事件链设计
```
事件A（触发）→ 事件B（响应）→ 事件C（结果）
```
- 使用 `FROM` 引用发送方
- 使用 `days` 延迟触发
- 使用 `event_target` 传递信息

### 4. UI优化
- 多个 `desc` 块：根据条件显示不同文本
- `effect_tooltip`: 显示效果预览
- `custom_effect_tooltip`: 自定义提示

---

**恭喜！你已掌握 HOI4 事件系统的核心用法！**
