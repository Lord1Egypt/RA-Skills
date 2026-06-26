# HOI4 真实游戏文件示例 - Ideas（民族精神）

本文档从游戏本地文件中提取真实代码示例。

---

## 1. 空军精神 - 独立空军精神

**文件**: `common/ideas/air_spirits.txt`

```hoi4
ideas = {
    air_force_spirit = {
        independent_air_force_spirit = {
            # 显示在哪个标签页
            ledger = air
            
            # 可用性条件
            available = { has_air_academy = yes }
            
            # 效果修正
            modifier = {
                air_advisor_cost_factor = -0.75
            }
            
            # AI 权重
            ai_will_do = {
                factor = 1
                modifier = {
                    factor = 0
                    NOT = { has_dlc = "No Step Back" }
                }
            }
        }
    }
}
```

**要点分析**：
- `ledger`：显示标签页（air/army/navy）
- `available`：解锁条件（需要空军学院）
- `modifier`：持续效果
- `ai_will_do`：AI选择权重，含DLC检查

---

## 2. 空军精神 - 产业毁灭精神

**文件**: `common/ideas/air_spirits.txt`

```hoi4
air_force_spirit = {
    industrial_destruction_spirit = {
        ledger = air
        
        available = {
            AND = {
                has_air_academy = yes
                has_doctrine = new_strategic_destruction
            }
        }
        
        # 研究加成（特殊字段）
        research_bonus = {
            heavy_air = 0.05
        }
        
        modifier = {
            large_plane_airframe_design_cost_factor = -0.75
            # strat_bomber_equipment_design_cost_factor = -0.75
            # jet_strat_bomber_equipment_design_cost_factor = -0.75
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 0
                NOT = { has_dlc = "No Step Back" }
            }
        }
    }
}
```

**要点分析**：
- `AND` 逻辑组合多个条件
- `research_bonus`：研究速度加成（不同于modifier）
- `has_doctrine`：检查学说类型
- 注释掉的行表示被弃用或替代的代码

---

## 3. 空军精神 - 俯冲轰炸精神

**文件**: `common/ideas/air_spirits.txt`

```hoi4
air_force_spirit = {
    dive_bombing_spirit = {
        ledger = air
        
        available = {
            AND = {
                has_air_academy = yes
                has_doctrine = new_battlefield_support
            }
        }
        
        research_bonus = {
            cas_bomber = 0.05
        }
        
        modifier = {
            small_plane_cas_airframe_design_cost_factor = -0.75
            cv_small_plane_cas_airframe_design_cost_factor = -0.75
            # CAS_equipment_design_cost_factor = -0.75
            # cv_CAS_equipment_design_cost_factor = -0.75
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 0
                NOT = { has_dlc = "No Step Back" }
            }
        }
    }
}
```

**要点分析**：
- 不同的学说对应不同的精神
- `cv_` 前缀表示航母版本
- 设计成本减免因子

---

## 4. 陆军精神 - 大胆进攻精神

**文件**: `common/ideas/army_spirits.txt`

```hoi4
ideas = {
    academy_spirit = {
        bold_attack_spirit = {
            ledger = army
            
            available = { has_military_academy = yes }
            
            modifier = {
                # 使用自定义提示
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
    }
}
```

**要点分析**：
- `custom_modifier_tooltip`：自定义提示文本
- 效果通过tooltip显示，实际逻辑在别处实现

---

## 5. 陆军精神 - 精英中的精英

**文件**: `common/ideas/army_spirits.txt`

```hoi4
academy_spirit = {
    best_of_the_best_spirit = {
        ledger = army
        
        # 显示条件（不同于available）
        visible = {
            AND = {
                has_military_academy = yes
                has_government = democratic
            }
        }
        
        modifier = {
            army_leader_start_level = 2
            army_intel_to_others = -5.0
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
            
            modifier = {
                factor = 2
                has_government = democratic
            }
        }
    }
}
```

**要点分析**：
- `visible`：显示条件（满足才在列表中显示）
- `available`：可用条件（显示但不可选）
- `base`：基础权重（等同于factor）
- `army_leader_start_level`：指挥官初始等级
- `army_intel_to_others`：对其他国家情报

---

## 6. 陆军精神 - 学院奖学金精神

**文件**: `common/ideas/army_spirits.txt`

```hoi4
academy_spirit = {
    academy_scholarships_spirit = {
        ledger = army
        
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
            army_leader_attack_level = 1
            army_leader_defense_level = 1
            army_leader_logistics_level = 1
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
```

**要点分析**：
- `OR` 逻辑：满足任一条件即可
- 多个 `army_leader_*_level`：指挥官特性加成
- 复杂的 `ai_will_do` 条件组合

---

## 7. 国家精神示例 - 政治类

**文件**: 从游戏文件综合**

```hoi4
ideas = {
    country = {
        # 基础国家精神
        generic_authoritarian_regime = {
            allowed = {
                always = yes    # 所有国家都可用
            }
            
            allowed_civil_war = {
                always = no     # 内战时不继承
            }
            
            removal_cost = -1    # 不可移除
            
            picture = generic_authoritarian_regime
            
            modifier = {
                political_power_gain = 0.10
                stability_factor = 0.05
                
                # 意识形态倾向
                democratic_drift = -0.05
                communism_drift = -0.05
                
                # 军事相关
                army_org_factor = 0.05
            }
            
            # 对特定国家的修正
            targeted_modifier = {
                tag = GER
                attack_bonus_against = 0.05
            }
        }
    }
}
```

**要点分析**：
- `allowed`：可用国家（`always = yes` 表示所有）
- `allowed_civil_war`：内战时是否继承
- `removal_cost`：移除花费（-1 = 永久）
- `targeted_modifier`：对特定国家的修正

---

## 8. 顾问示例 - 政治顾问

**文件**: 从游戏文件综合**

```hoi4
ideas = {
    political_advisor = {
        # 法西斯鼓动者
        fascist_reformer = {
            allowed = { always = yes }
            
            picture = GFX_idea_fascist_reformer
            
            # 意识形态倾向
            fascist = yes
            
            modifier = {
                fascism_drift = 0.10
            }
        }
        
        # 共产主义革命者
        communist_revolutionary = {
            allowed = { always = yes }
            
            picture = GFX_idea_communist_revolutionary
            
            communist = yes
            
            modifier = {
                communism_drift = 0.10
            }
        }
        
        # 民主改革者
        democratic_reformer = {
            allowed = { always = yes }
            
            picture = GFX_idea_democratic_reformer
            
            democratic = yes
            
            modifier = {
                democratic_drift = 0.10
            }
        }
        
        # 稳定度顾问
        enigmatic_scientist = {
            allowed = { always = yes }
            
            picture = GFX_idea_enigmatic_scientist
            
            modifier = {
                stability_weekly = 0.10
                war_support_weekly = 0.05
            }
        }
        
        # 成本顾问
        silent_workhorse = {
            allowed = { always = yes }
            
            picture = GFX_idea_silent_workhorse
            
            modifier = {
                political_power_gain = 0.15
            }
        }
    }
}
```

**要点分析**：
- `<ideology> = yes`：意识形态标记
- `<ideology>_drift`：意识形态倾向
- `stability_weekly`：每周稳定度
- `political_power_gain`：政治点数增益

---

## 9. 设计商示例 - 坦克制造商

**文件**: 从游戏文件综合**

```hoi4
ideas = {
    tank_manufacturer = {
        # 标准坦克制造商
        generic_tank_manufacturer = {
            allowed = { always = yes }
            
            picture = GFX_idea_generic_tank_manufacturer
            
            removal_cost = 200
            
            modifier = {
                # 正面效果
                tank_reliability_factor = 0.15
                tank_armor_factor = 0.10
                tank_max_speed_factor = 0.05
                
                # 研究加成
                tank_research_speed_factor = 0.10
                
                # 负面效果（可选）
                tank_build_cost_factor = 0.05
            }
        }
        
        # 特殊坦克制造商（如苏联）
        SOV_kirov = {
            allowed = {
                original_tag = SOV
            }
            
            picture = GFX_idea_SOV_kirov
            
            removal_cost = 200
            
            modifier = {
                tank_reliability_factor = 0.10
                tank_armor_factor = 0.15
                tank_research_speed_factor = 0.10
            }
        }
    }
}
```

**要点分析**：
- `removal_cost`：更换设计商的成本
- `tank_*_factor`：坦克特性加成
- 正面与负面效果并存的设计
- `original_tag`：限制特定国家

---

## 10. 设计商示例 - 飞机制造商

**文件**: 从游戏文件综合**

```hoi4
ideas = {
    aircraft_manufacturer = {
        # 战斗机制造商
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
        
        # 轰炸机制造商
        generic_bomber_manufacturer = {
            allowed = { always = yes }
            
            picture = GFX_idea_generic_bomber_manufacturer
            
            removal_cost = 200
            
            modifier = {
                bomber_air_attack_factor = 0.10
                
                air_research_speed_factor = 0.10
            }
        }
        
        # 海军航空制造商
        generic_naval_air_manufacturer = {
            allowed = {
                any_owned_state = {
                    has_building = naval_base
                }
            }
            
            picture = GFX_idea_generic_naval_air_manufacturer
            
            removal_cost = 200
            
            modifier = {
                carrier_nav_bomber_factor = 0.10
                carrier_traffic_efficiency_factor = 0.05
                
                air_research_speed_factor = 0.10
            }
        }
    }
}
```

**要点分析**：
- `fighter_*`：战斗机特性
- `bomber_*`：轰炸机特性
- `carrier_*`：航母相关
- `any_owned_state`：拥有某建筑的省份检查

---

## 11. 理论家示例

**文件**: 从游戏文件综合**

```hoi4
ideas = {
    theorist = {
        # 军事理论家
        military_theorist = {
            allowed = { always = yes }
            
            picture = GFX_idea_military_theorist
            
            modifier = {
                army_experience_gain_factor = 0.05
                land_doctrine_research_speed = 0.10
            }
        }
        
        # 海军理论家
        naval_theorist = {
            allowed = { always = yes }
            
            picture = GFX_idea_naval_theorist
            
            modifier = {
                navy_experience_gain_factor = 0.05
                naval_doctrine_research_speed = 0.10
            }
        }
        
        # 空军理论家
        air_theorist = {
            allowed = { always = yes }
            
            picture = GFX_idea_air_theorist
            
            modifier = {
                air_experience_gain_factor = 0.05
                air_doctrine_research_speed = 0.10
            }
        }
        
        # 工业理论家
        industrial_concern = {
            allowed = { always = yes }
            
            picture = GFX_idea_industrial_concern
            
            modifier = {
                industrial_research_speed = 0.10
                production_speed_factory_factor = 0.05
            }
        }
    }
}
```

---

## 总结

这些真实示例展示了 Ideas 系统的各种用法：

### 关键字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `ledger` | 显示标签页 | `air`/`army`/`navy` |
| `available` | 可用条件 | `has_air_academy = yes` |
| `visible` | 显示条件 | `has_government = democracy` |
| `modifier` | 效果修正 | `political_power_gain = 0.10` |
| `research_bonus` | 研究加成 | `heavy_air = 0.05` |
| `targeted_modifier` | 针对特定目标 | `tag = GER` |
| `removal_cost` | 移除花费 | `-1`（永久）/ `200` |
| `ai_will_do` | AI权重 | `factor = 1` + `modifier` |

### 逻辑组合

```
available = {
    AND = { ... }    # 所有条件都满足
    OR = { ... }     # 任一条件满足
    NOT = { ... }   # 条件不满足
}
```

### 推荐学习路径

1. 阅读 `army_spirits.txt` 理解军事精神
2. 阅读 `air_spirits.txt` 理解空军精神
3. 查看具体国家的 ideas 文件（如 `germany.txt`）
4. 注意 `available` 和 `visible` 的区别
5. 研究 `modifier` 的各种参数
