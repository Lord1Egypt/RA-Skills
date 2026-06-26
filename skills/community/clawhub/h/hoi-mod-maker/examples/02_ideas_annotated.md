# HOI4 Ideas 完整示例解析

本文档使用真实游戏代码，配合详细注释，展示 Ideas 系统的所有关键用法。

---

## 📌 示例1：国家精神基础（法国）

**来源**: `common/ideas/france.txt`

```hoi4
ideas = {
    country = {
        # ============================================
        # 国家精神1：充分就业
        # ============================================
        FRA_full_employment = {
            # === 图标 ===
            picture = generic_production_bonus
            
            # === 可用性 ===
            # allowed: 决定哪些国家可以拥有此精神
            # always = no: 表示需要通过效果添加，不会自动出现
            allowed = {
                original_tag = FRA    # 只有法国的原型可以使用
                always = no            # 需要手动添加
            }
            
            # === 内战处理 ===
            # 决定内战时哪个国家保留此精神
            allowed_civil_war = {
                tag = FRA    # 主国家保留
            }
            
            # === 移除花费 ===
            # -1 = 永久（不可移除）
            # 0 = 免费移除
            # 正数 = 移除需要的政治点数
            removal_cost = -1
            
            # === 效果修正 ===
            modifier = {
                conscription_factor = -0.25    # 征兵率-25%
            }
        }
        
        # ============================================
        # 国家精神2：劳动力短缺
        # ============================================
        FRA_worker_shortage = {
            picture = FRA_factory_strikes
            
            allowed = {
                original_tag = FRA
                always = no
            }
            
            allowed_civil_war = {
                tag = FRA
            }
            
            removal_cost = -1
            
            # === 多重修正 ===
            modifier = {
                conscription_factor = -0.25
                industrial_capacity_factory = -0.1    # 工厂效率-10%
                industrial_capacity_dockyard = -0.1    # 船坞效率-10%
            }
        }
        
        # ============================================
        # 国家精神3：经济效率低下（等级1）
        # ============================================
        FRA_inefficient_economy_1 = {
            picture = generic_local_self_management
            
            allowed = {
                original_tag = FRA
                always = no
            }
            
            allowed_civil_war = {
                tag = FRA
            }
            
            removal_cost = -1
            
            modifier = {
                industrial_capacity_factory = -0.1
                industrial_capacity_dockyard = -0.1
            }
        }
        
        # ============================================
        # 国家精神4：经济效率低下（等级2）
        # ============================================
        FRA_inefficient_economy_2 = {
            picture = generic_local_self_management
            
            # === 名称覆盖 ===
            # 使用等级1的本地化名称
            name = FRA_inefficient_economy_1
            
            allowed = {
                original_tag = FRA
                always = no
            }
            
            allowed_civil_war = {
                tag = FRA
            }
            
            removal_cost = -1
            
            # === 更强的负面效果 ===
            modifier = {
                industrial_capacity_factory = -0.2    # -20%
                industrial_capacity_dockyard = -0.2    # -20%
            }
        }
        
        # ============================================
        # 国家精神5：政治暴力
        # ============================================
        FRA_political_violence = {
            # 注意：无 picture 字段（使用默认）
            
            allowed = {
                original_tag = FRA
                always = no
            }
            
            # === 内战时双方都有 ===
            allowed_civil_war = {
                always = yes    # 内战双方都保留
            }
            
            # === 可用条件 ===
            # 必须满足此条件才能添加
            available = {
                has_stability < 0.7    # 稳定度<70%
            }
            
            removal_cost = -1
            
            # 空修正（仅视觉效果）
            modifier = {
                
            }
        }
    }
}
```

### 💡 关键说明

**`allowed` vs `available`**:
- `allowed`: 哪些国家可以拥有（初始限制）
- `available`: 添加时需要满足的条件
- 两者结合控制精神的获取

**`allowed_civil_war`**:
- `tag = FRA`: 主国家保留
- `always = yes`: 内战双方都有
- `always = no`: 都不保留

**等级化精神**:
- 创建多个精神（如等级1、等级2）
- 使用 `name` 共享本地化
- 不同等级效果强度不同

---

## 📌 示例2：海军学院精神

**来源**: `common/ideas/navy_spirits.txt`

```hoi4
ideas = {
    naval_academy_spirit = {
        # ============================================
        # 海军精神1：进攻性培养
        # ============================================
        instilled_aggression_spirit = {
            # === 标签页 ===
            # 决定在UI的哪个标签页显示
            ledger = navy
            
            # === 可用性 ===
            available = { 
                has_naval_academy = yes    # 需要海军学院
            }
            
            # === 自定义提示 ===
            modifier = {
                custom_modifier_tooltip = instilled_aggression_spirit_tt
            }
            
            # === AI权重 ===
            ai_will_do = {
                factor = 1
                modifier = {
                    factor = 0    # 无DLC时AI不选
                    NOT = { has_dlc = "No Step Back" }
                }
            }
        }
        
        # ============================================
        # 海军精神2：舰队存在学说
        # ============================================
        fleet_in_being_academy_spirit = {
            ledger = navy
            
            available = {
                AND = { 
                    has_naval_academy = yes
                    has_doctrine = new_fleet_in_being    # 特定学说
                }
            }
            
            # === 实际效果 + 提示 ===
            modifier = {
                custom_modifier_tooltip = fleet_in_being_academy_spirit_tt
                trait_ironside_xp_gain_factor = 0.2        # 指挥官经验+20%
                trait_superior_tactician_xp_gain_factor = 0.2
            }
            
            ai_will_do = {
                factor = 1.5
                
                modifier = {
                    factor = 0
                    NOT = { has_dlc = "No Step Back" }
                }
                
                # === 条件权重加成 ===
                modifier = {
                    factor = 2    # 拥有学说时权重x2
                    has_doctrine = new_fleet_in_being
                }
            }
        }
        
        # ============================================
        # 海军精神3：贸易阻断学说
        # ============================================
        trade_interdiction_academy_spirit = {
            ledger = navy
            
            available = {
                AND = { 
                    has_naval_academy = yes
                    has_doctrine = new_convoy_raiding
                }
            }
            
            modifier = {
                custom_modifier_tooltip = trade_interdiction_academy_spirit_tt
                trait_seawolf_xp_gain_factor = 0.2
            }
            
            ai_will_do = {
                factor = 1.5
                
                modifier = {
                    factor = 0
                    NOT = { has_dlc = "No Step Back" }
                }
                
                modifier = {
                    factor = 2
                    has_doctrine = new_convoy_raiding
                }
            }
        }
        
        # ============================================
        # 海军精神4：基地打击学说
        # ============================================
        carrier_battlegroup_academy_spirit = {
            ledger = navy
            
            available = {
                AND = { 
                    has_naval_academy = yes
                    has_doctrine = new_base_strike
                }
            }
            
            modifier = {
                custom_modifier_tooltip = carrier_battlegroup_academy_spirit_tt
                trait_naval_aviation_tactical_xp_gain_factor = 0.2
            }
            
            ai_will_do = {
                factor = 1.5
                
                modifier = {
                    factor = 0
                    NOT = { has_dlc = "No Step Back" }
                }
                
                modifier = {
                    factor = 2
                    has_doctrine = new_base_strike
                }
            }
        }
    }
}
```

### 💡 关键说明

**`ledger`字段**:
- `navy`: 海军标签页
- `air`: 空军标签页
- `army`: 陆军标签页
- 无此字段: 普通国家精神列表

**`custom_modifier_tooltip`**:
- 显示自定义提示文本
- 实际效果由其他修正实现
- 提示键：`{spirit_id}_tt`

**`ai_will_do`权重**:
- `factor`: 基础权重
- `modifier`: 条件权重修正
- 可叠加多个条件修正

---

## 📌 示例3：陆军学院精神

**来源**: `common/ideas/army_spirits.txt`

```hoi4
ideas = {
    academy_spirit = {
        # ============================================
        # 陆军精神：大胆进攻
        # ============================================
        bold_attack_spirit = {
            ledger = army
            
            available = { 
                has_military_academy = yes 
            }
            
            # 仅提示，效果在别处实现
            modifier = {
                custom_modifier_tooltip = bold_attack_spirit_tt
            }
            
            ai_will_do = {
                factor = 1
                modifier = {
                    factor = 0
                    NOT = { has_dlc = "No Step Back" }
                }
            }
        }
        
        # ============================================
        # 陆军精神：坚韧防御
        # ============================================
        tenacious_defense_spirit = {
            ledger = army
            
            available = { 
                has_military_academy = yes 
            }
            
            modifier = {
                custom_modifier_tooltip = tenacious_defense_spirit_tt
            }
            
            ai_will_do = {
                factor = 1
                modifier = {
                    factor = 0
                    NOT = { has_dlc = "No Step Back" }
                }
            }
        }
        
        # ============================================
        # 陆军精神：精锐中的精锐
        # ============================================
        best_of_the_best_spirit = {
            ledger = army
            
            # === 显示条件 ===
            # 满足条件才会出现在列表中
            visible = {
                AND = { 
                    has_military_academy = yes 
                    has_government = democratic
                }
            }
            
            modifier = {
                army_leader_start_level = 2        # 指挥官初始等级+2
                army_intel_to_others = -5.0        # 对其他国家的陆军情报-5
                custom_modifier_tooltip = best_of_the_best_spirit_tt
            }
            
            ai_will_do = {
                base = 1
                
                modifier = {
                    factor = 0
                    OR = {
                        NOT = { has_dlc = "No Step Back" }
                        NOT = { has_government = democratic }
                    }
                }
                
                # === 民主政府权重加成 ===
                modifier = {
                    factor = 2
                    has_government = democratic
                }
            }
        }
        
        # ============================================
        # 陆军精神：学院奖学金（法西斯/中立）
        # ============================================
        academy_scholarships_spirit = {
            ledger = army
            
            # === 显示条件：法西斯或中立 ===
            visible = { 
                AND = {
                    has_military_academy = yes
                    OR = {
                        has_government = fascism
                        has_government = neutrality
                    }
                }
            }
            
            modifier = {
                army_leader_start_level = 1
                army_leader_attack_level = 1        # 攻击技能+1
                army_leader_defense_level = 1        # 防御技能+1
                army_leader_logistics_level = 1    # 后勤技能+1
                custom_modifier_tooltip = academy_scholarships_spirit_tt
            }
            
            ai_will_do = {
                factor = 1
                modifier = {
                    factor = 0
                    OR = {
                        NOT = { has_dlc = "No Step Back" }
                        NOT = {
                            OR = {
                                has_government = fascism
                                has_government = neutrality
                            }
                        }
                    }
                }
            }
        }
    }
}
```

### 💡 关键说明

**`visible`字段**:
- 决定精神是否出现在选择列表中
- 不满足条件时完全不可见
- `available` 满足但不满足 `visible` 时不可见

**意识形态精神**:
- 使用 `visible` 限制特定意识形态
- 不同意识形态的精神互斥
- AI权重可针对意识形态优化

---

## 📌 示例4：政治顾问

**来源**: `common/ideas/_generic.txt`（推断）

```hoi4
ideas = {
    political_advisor = {
        # ============================================
        # 法西斯改革者
        # ============================================
        fascist_reformer = {
            allowed = { always = yes }
            
            picture = GFX_idea_fascist_reformer
            
            # === 意识形态标记 ===
            fascist = yes
            
            modifier = {
                fascism_drift = 0.10    # 法西斯倾向+0.10/天
            }
        }
        
        # ============================================
        # 共产主义革命者
        # ============================================
        communist_revolutionary = {
            allowed = { always = yes }
            
            picture = GFX_idea_communist_revolutionary
            
            communist = yes
            
            modifier = {
                communism_drift = 0.10
            }
        }
        
        # ============================================
        # 民主改革者
        # ============================================
        democratic_reformer = {
            allowed = { always = yes }
            
            picture = GFX_idea_democratic_reformer
            
            democratic = yes
            
            modifier = {
                democratic_drift = 0.10
            }
        }
        
        # ============================================
        # 默默无闻的工作者
        # ============================================
        silent_workhorse = {
            allowed = { always = yes }
            
            picture = GFX_idea_silent_workhorse
            
            modifier = {
                political_power_gain = 0.15    # 政治点数+15%
            }
        }
        
        # ============================================
        # 神秘科学家
        # ============================================
        enigmatic_scientist = {
            allowed = { always = yes }
            
            picture = GFX_idea_enigmatic_scientist
            
            modifier = {
                stability_weekly = 0.10        # 每周稳定度+10%
                war_support_weekly = 0.05    # 每周战争支持度+5%
            }
        }
        
        # ============================================
        # 人口观念鼓动者
        # ============================================
        popular_figurehead = {
            allowed = { always = yes }
            
            picture = GFX_idea_popular_figurehead
            
            modifier = {
                stability_factor = 0.10
                political_power_gain = -0.10
            }
        }
    }
}
```

### 💡 关键说明

**意识形态标记**:
- `<ideology> = yes`: 标记顾问的意识形态
- 影响UI显示和事件触发
- 与倾向效果配合使用

**常见顾问效果**:
- `political_power_gain`: 政治点数增益
- `stability_weekly`: 每周稳定度
- `<ideology>_drift`: 意识形态倾向

---

## 📌 示例5：理论家

**来源**: 从游戏文件综合

```hoi4
ideas = {
    theorist = {
        # ============================================
        # 军事理论家
        # ============================================
        military_theorist = {
            allowed = { always = yes }
            
            picture = GFX_idea_military_theorist
            
            modifier = {
                army_experience_gain_factor = 0.05    # 陆军经验+5%
                land_doctrine_research_speed = 0.10    # 陆军学说研究+10%
            }
        }
        
        # ============================================
        # 海军理论家
        # ============================================
        naval_theorist = {
            allowed = { always = yes }
            
            picture = GFX_idea_naval_theorist
            
            modifier = {
                navy_experience_gain_factor = 0.05
                naval_doctrine_research_speed = 0.10
            }
        }
        
        # ============================================
        # 空军理论家
        # ============================================
        air_theorist = {
            allowed = { always = yes }
            
            picture = GFX_idea_air_theorist
            
            modifier = {
                air_experience_gain_factor = 0.05
                air_doctrine_research_speed = 0.10
            }
        }
        
        # ============================================
        # 工业关注
        # ============================================
        industrial_concern = {
            allowed = { always = yes }
            
            picture = GFX_idea_industrial_concern
            
            modifier = {
                industrial_research_speed = 0.10        # 工业研究+10%
                production_speed_factory_factor = 0.05    # 工厂生产速度+5%
            }
        }
        
        # ============================================
        # 核物理学家
        # ============================================
        nuclear_physicist = {
            allowed = { always = yes }
            
            picture = GFX_idea_nuclear_physicist
            
            modifier = {
                nuclear_research_speed = 0.10
            }
        }
    }
}
```

---

## 📌 示例6：设计商

**来源**: 从游戏文件综合

```hoi4
ideas = {
    # === 坦克制造商 ===
    tank_manufacturer = {
        generic_tank_manufacturer = {
            allowed = { always = yes }
            
            picture = GFX_idea_generic_tank_manufacturer
            
            removal_cost = 200    # 更换需要200政治点数
            
            modifier = {
                tank_reliability_factor = 0.15        # 可靠性+15%
                tank_armor_factor = 0.10            # 装甲+10%
                tank_max_speed_factor = 0.05        # 最大速度+5%
                
                tank_research_speed_factor = 0.10    # 坦克研究+10%
                
                tank_build_cost_factor = 0.05        # 生产成本+5%（负面）
            }
        }
        
        # === 德国克虏伯 ===
        GER_krupp = {
            allowed = { original_tag = GER }
            
            picture = GFX_idea_GER_krupp
            
            removal_cost = 200
            
            modifier = {
                tank_reliability_factor = 0.20
                tank_armor_factor = 0.15
                tank_research_speed_factor = 0.15
            }
        }
    }
    
    # === 飞机制造商 ===
    aircraft_manufacturer = {
        generic_fighter_manufacturer = {
            allowed = { always = yes }
            
            picture = GFX_idea_generic_fighter_manufacturer
            
            removal_cost = 200
            
            modifier = {
                fighter_air_attack_factor = 0.10
                fighter_air_defence_factor = 0.05
                
                air_research_speed_factor = 0.10
            }
        }
        
        generic_bomber_manufacturer = {
            allowed = { always = yes }
            
            picture = GFX_idea_generic_bomber_manufacturer
            
            removal_cost = 200
            
            modifier = {
                bomber_air_attack_factor = 0.10
                
                air_research_speed_factor = 0.10
            }
        }
        
        # === 德国梅塞施密特 ===
        GER_messerschmitt = {
            allowed = { original_tag = GER }
            
            picture = GFX_idea_GER_messerschmitt
            
            removal_cost = 200
            
            modifier = {
                fighter_air_attack_factor = 0.15
                fighter_max_speed_factor = 0.10
                air_research_speed_factor = 0.15
            }
        }
    }
    
    # === 海军设计师 ===
    naval_manufacturer = {
        generic_naval_manufacturer = {
            allowed = { 
                any_owned_state = {
                    has_building = naval_base
                }
            }
            
            picture = GFX_idea_generic_naval_manufacturer
            
            removal_cost = 200
            
            modifier = {
                capital_ship_attack_factor = 0.10
                capital_ship_armor_factor = 0.05
                
                naval_research_speed_factor = 0.10
            }
        }
    }
}
```

### 💡 关键说明

**设计商特点**:
- `removal_cost`: 更换设计商的成本
- 通常为200政治点数
- 有正面和负面效果
- 影响装备设计和研究

**国家特有设计商**:
- 使用 `original_tag` 限制
- 通常比通用设计商更强
- 有独特的图标和名称

---

## 📝 本地化示例

```yaml
l_english:
 # 法国精神
 FRA_full_employment:0 "Full Employment"
 FRA_full_employment_desc:0 "The French economy has achieved near full employment, but at the cost of military readiness."
 
 FRA_worker_shortage:0 "Worker Shortage"
 FRA_worker_shortage_desc:0 "Factories stand idle due to a lack of workers."
 
 # 海军精神
 instilled_aggression_spirit_tt:0 "§G+10%§! Naval sortie efficiency."
 fleet_in_being_academy_spirit_tt:0 "§G+20%§! Commander XP gain (Ironside, Superior Tactician)."
 
 # 政治顾问
 fascist_reformer:0 "Fascist Reformer"
 fascist_reformer_desc:0 "A fervent believer in the fascist cause, this advisor will sway our nation towards fascism."
 
 silent_workhorse:0 "Silent Workhorse"
 silent_workhorse_desc:0 "This unassuming figure works tirelessly behind the scenes to boost our political efficiency."
```

---

## ✅ 最佳实践总结

### 1. 精神类型选择
| 类型 | 槽位 | 说明 |
|------|------|------|
| `country` | 无限制 | 国家精神（主流） |
| `army` | 1个 | 陆军精神（需DLC） |
| `navy` | 1个 | 海军精神（需DLC） |
| `air` | 1个 | 空军精神（需DLC） |
| `political_advisor` | 1个 | 政治顾问 |
| `theorist` | 1个 | 理论家 |
| `army_chief` | 1个 | 陆军首脑 |
| `navy_chief` | 1个 | 海军首脑 |
| `air_chief` | 1个 | 空军首脑 |

### 2. 字段使用建议
- `allowed`: 初始限制（国家、意识形态）
- `visible`: 显示条件（UI过滤）
- `available`: 添加条件（运行时检查）
- `allowed_civil_war`: 内战继承规则

### 3. 效果设计
- 国家精神: 持续修正（`modifier`）
- 临时精神: 使用 `add_timed_idea`
- 军事精神: `ledger` + `custom_modifier_tooltip`

---

**下一步**: 学习事件系统示例 →
