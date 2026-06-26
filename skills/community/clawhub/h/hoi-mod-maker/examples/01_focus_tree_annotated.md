# HOI4 国策树完整示例解析

本文档使用真实游戏代码，配合详细注释，展示国策树的所有关键用法。

---

## 📌 示例1：基础国策结构（法国）

**来源**: `common/national_focus/france.txt`

```hoi4
focus_tree = {
    id = french_focus
    
    # === 国家权重 ===
    # 决定哪些国家使用此国策树
    country = {
        factor = 0    # 基础权重为0（不使用）
        
        # 修正：法国权重+10，使用此树
        modifier = {
            add = 10
            tag = FRA
        }
    }
    
    # 初始视口位置（可选）
    initial_show_position = {
        x = 0    # 横坐标
        # y = 0  # 纵坐标（可省略）
    }
    
    default = no    # 不是默认树
    
    # ============================================
    # 焦点1：货币贬值（根节点）
    # ============================================
    focus = {
        id = FRA_devalue_the_franc    # 唯一标识符（必需）
        icon = GFX_focus_fra_devalue_the_franc    # 图标GFX
        x = 0        # 横坐标（绝对定位）
        y = 0        # 纵坐标
        
        prerequisite = {}    # 无前置（根节点）
        mutually_exclusive = { }    # 无互斥
        
        cost = 10    # 天数成本（实际天数 = cost × 7）
        
        # AI权重（决定AI是否选择此焦点）
        ai_will_do = {
            factor = 1    # 基础权重
        }
        
        # 可用条件（空=总是可用）
        available = {
            
        }
        
        # 跳过条件（满足条件自动完成）
        bypass = {
            
        }
        
        # 行为标志
        cancel_if_invalid = yes    # 条件失效时取消
        continue_if_invalid = no    # 条件失效时继续
        available_if_capitulated = no    # 投降后不可用
        
        # 搜索过滤器（UI分类）
        search_filters = { FOCUS_FILTER_INDUSTRY }
        
        # 完成效果
        completion_reward = {
            # 添加临时民族精神（365天=1年）
            add_timed_idea = {
                idea = FRA_devalue_the_franc    # 精神ID
                days = 365    # 持续天数
            }
        }
    }
```

### 💡 关键说明

**字段解释**:
- `id`: 全局唯一，用于引用和本地化
- `cost`: 实际天数 = cost × 7（cost=10 = 70天）
- `cancel_if_invalid`: 可用条件失效时是否取消焦点
- `search_filters`: UI筛选器，可多个值

**`add_timed_idea`**:
- 添加临时民族精神
- `days`: 持续天数（-1 = 永久）
- 时间到期后自动移除

---

## 📌 示例2：条件建筑建造（法国）

**来源**: `common/national_focus/france.txt`

```hoi4
    # ============================================
    # 焦点2：高速公路建设
    # ============================================
    focus = {
        id = FRA_autoroutes
        icon = GFX_goal_generic_construct_infrastructure
        x = 2
        y = 1
        
        # 前置条件：必须完成货币贬值
        prerequisite = { focus = FRA_devalue_the_franc }
        
        mutually_exclusive = { }
        
        # 相对定位（相对于前置焦点）
        relative_position_id = FRA_devalue_the_franc
        
        cost = 10
        
        ai_will_do = {
            factor = 1
        }
        
        # 可用条件：存在核心省份基础设施<4
        available = {
            any_owned_state = {
                is_core_of = ROOT
                infrastructure < 4
            }
        }
        
        bypass = { }
        
        cancel_if_invalid = yes
        continue_if_invalid = no
        available_if_capitulated = no
        
        search_filters = { FOCUS_FILTER_INDUSTRY }
        
        completion_reward = {
            # 随机选择4个核心省份建造基础设施
            # 使用多次random_owned_state实现
            
            random_owned_state = {
                limit = { 
                    is_core_of = ROOT    # 是核心
                    infrastructure < 4    # 基础设施<4
                    NOT = { has_state_flag = FRA_autoroutes_target }    # 未被选择
                }
                
                # 建造基础设施
                add_building_construction = {
                    type = infrastructure
                    level = 1
                    instant_build = yes    # 立即建造
                }
                
                # 标记此省份
                set_state_flag = FRA_autoroutes_target
            }
            
            # 重复3次（共4个省份）
            random_owned_state = {
                limit = { 
                    is_core_of = ROOT 
                    infrastructure < 4
                    NOT = { has_state_flag = FRA_autoroutes_target }
                }
                add_building_construction = {
                    type = infrastructure
                    level = 1
                    instant_build = yes
                }
                set_state_flag = FRA_autoroutes_target
            }
            
            # ... 再重复2次
        }
    }
}
```

### 💡 关键说明

**`random_owned_state`**:
- 随机选择一个拥有的省份
- `limit`: 选择条件
- 使用标记避免重复选择

**`add_building_construction`**:
- `type`: 建筑类型
- `level`: 建造等级
- `instant_build`: 是否立即完成

**`set_state_flag`**:
- 设置省份标记
- 用于追踪已处理的省份
- 避免重复选择

---

## 📌 示例3：条件偏移（意大利）

**来源**: `common/national_focus/italy.txt`

```hoi4
    focus = {
        id = ITA_ethiopian_war_logistics_bba
        icon = GFX_goal_generic_position_armies
        
        x = 2
        y = 0
        
        # === 条件偏移 ===
        # 根据条件动态调整位置
        offset = {
            x = 6    # 向右偏移6格
            y = 0
            
            # 偏移条件：意大利内战分支可见
            trigger = {
                ITA_cw_branches_are_visible = yes
            }
        }
        
        cost = 5
        
        bypass = {
            OR = {
                # 不处于第二次意埃战争
                NOT = { has_global_flag = second_italo_ethiopian_war_flag }
                
                # 或埃塞俄比亚省份已被占领
                AND = {
                    550 = { NOT = { is_owned_and_controlled_by = ITA } }
                    559 = { NOT = { is_owned_and_controlled_by = ITA } }
                    844 = { NOT = { is_owned_and_controlled_by = ITA } }
                }
            }
        }
        
        available = {
            # 可用条件（空）
        }
        
        search_filters = {FOCUS_FILTER_INDUSTRY}
        
        completion_reward = {
            # === 条件省份建造 ===
            # 如果省份550被意大利控制
            
            if = { 
                limit = { 550 = { is_owned_and_controlled_by = ITA } }
                550 = {
                    add_building_construction = {
                        type = infrastructure
                        level = 1
                        instant_build = yes
                    }
                    
                    # === 指定省份建造海军基地 ===
                    add_building_construction = {
                        type = naval_base
                        level = 2
                        province = 12766    # 特定省份ID
                        instant_build = yes
                    }
                }
            }
            
            # 如果省份559被意大利控制
            if = { 
                limit = { 559 = { is_owned_and_controlled_by = ITA } }
                559 = {
                    add_building_construction = {
                        type = infrastructure
                        level = 1
                        instant_build = yes
                    }
                    add_building_construction = {
                        type = naval_base
                        level = 2
                        province = 12991
                        instant_build = yes
                    }
                }
            }
            
            # 如果省份844被意大利控制
            if = { 
                limit = { 844 = { is_owned_and_controlled_by = ITA } }
                844 = {
                    add_building_construction = {
                        type = infrastructure
                        level = 1
                        instant_build = yes
                    }
                    add_building_construction = {
                        type = naval_base
                        level = 2
                        province = 12941
                        instant_build = yes
                    }
                }
            }
        }
    }
```

### 💡 关键说明

**`offset`**:
- 条件偏移：根据条件动态调整焦点位置
- `x`: 横向偏移（负=左，正=右）
- `y`: 纵向偏移（正=下）
- `trigger`: 偏移条件

**省份作用域**:
- `550 = { ... }`: 切换到省份550
- `is_owned_and_controlled_by`: 检查省份控制权

**`province`参数**:
- 在多省份州中指定具体省份
- 用于海军基地等需要特定位置的建筑

---

## 📌 示例4：复杂快捷方式（日本）

**来源**: `common/national_focus/japan.txt`

```hoi4
focus_tree = {
    id = japan_wtt_focus
    
    country = {
        factor = 0
        modifier = {
            add = 20
            tag = JAP
        }
    }
    
    # =========================================
    # 快捷方式定义
    # =========================================
    
    # 快捷方式1：军事学说
    shortcut = {
        name = JAP_military_doctrine_shortcut
        target = JAP_the_imperial_defense_plan
        scroll_wheel_factor = 0.65
    }
    
    # 快捷方式2：经济建设
    shortcut = {
        name = GER_economic_path_shortcut
        target = JAP_ministry_of_commerce_and_industry 
        scroll_wheel_factor = 0.9
    }
    
    # 快捷方式3：历史路线（无条件）
    shortcut = {
        name = GER_historical_path_shortcut
        target = JAP_sea_purge_the_kodoha_faction
        scroll_wheel_factor = 0.6
        trigger = {
            always = yes
        }
    }
    
    # 快捷方式4：反对派路线（条件显示）
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = JAP_strengthen_civilian_government
        scroll_wheel_factor = 0.8
        trigger = {
            NOT = { 
                has_dlc = "No Compromise, No Surrender"
                has_completed_focus = JAP_support_the_kodoha_faction
                has_completed_focus = JAP_the_unthinkable_option
            }
        }
    }
    
    # 快捷方式5：同名称不同目标（根据已完成焦点）
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = JAP_support_the_kodoha_faction
        scroll_wheel_factor = 0.8
        trigger = {
            has_completed_focus = JAP_support_the_kodoha_faction
        }
    }
    
    shortcut = {
        name = GER_oppose_hitler_shortcut
        target = JAP_the_unthinkable_option
        scroll_wheel_factor = 0.8
        trigger = {
            has_completed_focus = JAP_the_unthinkable_option
        }
    }
    
    # =========================================
    # 嵌入窗口定义
    # =========================================
    inlay_window = {
        id = jap_imperial_influence_inlay_window
        
        # 基础位置
        position = { X = 10000 y = 700 }
        
        # === 条件位置覆盖 ===
        # 根据条件动态调整窗口位置
        
        override_position = {
            x = 6800
            y = 700
            trigger = {
                NOT = {
                    has_dlc = "No Compromise, No Surrender"
                }
                NOT = {
                    has_completed_focus = JAP_support_the_kodoha_faction
                    has_completed_focus = JAP_strengthen_civilian_government
                    has_completed_focus = JAP_the_unthinkable_option
                    has_completed_focus = JAP_sea_purge_the_kodoha_faction
                }
            }
        }
        
        override_position = {
            x = 4400
            y = 700
            trigger = {
                has_game_rule = {
                    rule = obsolete_focus_branches_visibility
                    option = HIDE    # 隐藏过时分支
                }
                has_completed_focus = JAP_sea_purge_the_kodoha_faction
            }
        }
        
        override_position = {
            x = 6000
            y = 700
            trigger = {
                has_game_rule = {
                    rule = obsolete_focus_branches_visibility
                    option = HIDE
                }
                has_completed_focus = JAP_revere_the_emperor_destroy_the_traitors
            }
        }
    }
}
```

### 💡 关键说明

**`shortcut`特性**:
- `name`: 显示名称的本地化键
- `target`: 跳转目标焦点ID
- `scroll_wheel_factor`: 滚轮缩放因子（可选）
- `trigger`: 显示条件（可选）

**同名快捷方式**:
- 可定义多个同名快捷方式
- 根据条件显示不同目标
- 用于动态路线导航

**`inlay_window`**:
- 嵌入窗口：创建特殊显示区域
- `position`: 基础位置
- `override_position`: 条件位置覆盖
- `trigger`: 覆盖条件

**用途**:
- 德国内圈焦点
- 日本皇道派影响
- 波兰意志斗争

---

## 📌 示例5：连续焦点（Generic）

**来源**: `common/national_focus/generic.txt`

```hoi4
focus_tree = {
    id = generic
    
    # 连续焦点显示位置
    continuous_focus_position = { x = 500 y = 1300 }
    
    # === 连续焦点：陆军经验 ===
    focus = {
        id = continuous_army_xp
        icon = GFX_focus_generic_army_xp
        x = 0
        y = 0
        
        # 标记为连续焦点
        continuous = yes
        
        # 连续焦点使用 modifier 而非 completion_reward
        modifier = {
            army_experience_gain_factor = 0.05    # 每天获得5%的陆军经验加成
        }
        
        search_filters = { FOCUS_FILTER_ARMY_XP }
    }
    
    # === 连续焦点：海军经验 ===
    focus = {
        id = continuous_navy_xp
        icon = GFX_focus_generic_navy_xp
        x = 1
        y = 0
        continuous = yes
        
        modifier = {
            navy_experience_gain_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_NAVY_XP }
    }
    
    # === 连续焦点：空军经验 ===
    focus = {
        id = continuous_air_xp
        icon = GFX_focus_generic_air_xp
        x = 2
        y = 0
        continuous = yes
        
        modifier = {
            air_experience_gain_factor = 0.05
        }
        
        search_filters = { FOCUS_FILTER_AIR_XP }
    }
    
    # === 连续焦点：政治点数 ===
    focus = {
        id = continuous_pol_power
        icon = GFX_focus_generic_political_advances
        x = 3
        y = 0
        continuous = yes
        
        modifier = {
            political_power_gain = 0.10    # 每天+0.10政治点数
        }
        
        search_filters = { FOCUS_FILTER_POLITICAL }
    }
}
```

### 💡 关键说明

**连续焦点特点**:
- 解锁条件：完成10个常规焦点
- 每天消耗：1 政治点数
- 效果：仅激活时持续生效
- 切换：随时可切换，无额外消耗

**语法差异**:
- `continuous = yes`：标记为连续焦点
- 无 `cost` 字段
- 使用 `modifier` 块（持续效果）
- 不使用 `completion_reward`（一次性效果）

---

## 📌 示例6：内圈焦点（德国）

**来源**: `common/national_focus/germany.txt`（推断）

```hoi4
# 文件顶部定义时间常量
@inner_circle_time_tier_1 = 20    # 140天
@inner_circle_time_tier_2 = 20    # 140天
@inner_circle_time_tier_3 = 40    # 280天

focus_tree = {
    id = german_focus
    
    # 内圈窗口定义
    inlay_window = {
        id = ger_inner_circle_inlay_window
        position = { x = 4500 y = 1150 }
    }
    
    # === 内圈焦点示例 ===
    focus = {
        id = GER_inner_circle_industry
        inner_circle = yes    # 标记为内圈焦点
        
        icon = GFX_focus_ger_inner_industry
        x = 0
        y = 0
        
        # 相对于中心焦点定位
        relative_position_id = GER_rearmament
        
        cost = @inner_circle_time_tier_1
        
        available = {
            has_country_flag = GER_rearmament_active
        }
        
        completion_reward = {
            # 追踪内圈进度
            add_to_variable = {
                var = GER_inner_circle_progress
                value = 1
            }
            
            # 条件奖励
            if = {
                limit = {
                    check_variable = {
                        var = GER_inner_circle_progress
                        value > 5
                    }
                }
                add_political_power = 100
                custom_effect_tooltip = GER_inner_circle_complete_tt
            }
            
            # 显示顾问效果预览
            show_ideas_tooltip = GER_hjalmar_schacht
            
            # 解锁决策类别提示
            unlock_decision_category_tooltip = GER_economic_decisions
            
            # 隐藏效果
            hidden_effect = {
                set_state_flag = ger_industrial_focus
                
                # 条件创建部队模板
                if = {
                    limit = { has_tech = infantry_equipment_1 }
                    create_division_template = {
                        name = "Infanterie-Division"
                        is_locked = yes
                        regiments = {
                            infantry = 3
                        }
                    }
                }
            }
        }
    }
}
```

### 💡 关键说明

**内圈焦点特点**:
- 围绕中心焦点的小型辅助焦点
- 用于角色政治系统（德国DLC）
- 通常 cost 较低（20-40）
- 相对于中心焦点定位

**高级提示**:
- `show_ideas_tooltip`：显示顾问效果预览
- `unlock_decision_category_tooltip`：解锁决策提示
- `custom_effect_tooltip`：自定义文本提示

---

## 📝 本地化示例

**文件**: `localisation/english/focus_l_english.yml`

```yaml
l_english:
 # 法国焦点
 FRA_devalue_the_franc:0 "Devalue the Franc"
 FRA_devalue_the_franc_desc:0 "The Franc has been overvalued for years, hurting our exports. A controlled devaluation will boost the economy."
 
 FRA_autoroutes:0 "Autoroutes"
 FRA_autoroutes_desc:0 "Building a network of highways will improve infrastructure and connect our nation."
 
 # 日本焦点
 JAP_the_imperial_defense_plan:0 "The Imperial Defense Plan"
 JAP_the_imperial_defense_plan_desc:0 "Our empire must be defended against all threats."
 
 JAP_ministry_of_commerce_and_industry:0 "Ministry of Commerce and Industry"
 JAP_ministry_of_commerce_and_industry_desc:0 "Centralized economic planning for the empire."
```

---

## ✅ 最佳实践总结

### 1. 定位选择
- 根节点：绝对定位
- 子节点：相对定位（`relative_position_id`）
- 条件位置：使用 `offset`

### 2. 条件效果
- 使用 `if` 块处理条件逻辑
- `hidden_effect` 用于隐藏实现细节
- `complete_tooltip` 用于显示实际效果

### 3. 建筑建造
- 使用 `random_owned_state` 随机选择
- 使用标记避免重复（`set_state_flag`）
- 指定省份时使用 `province` 参数

### 4. UI优化
- 使用 `shortcut` 提升导航体验
- 使用 `inlay_window` 创建特殊区域
- 使用 `search_filters` 方便筛选

---

**下一步**: 学习 Ideas 系统示例 →
