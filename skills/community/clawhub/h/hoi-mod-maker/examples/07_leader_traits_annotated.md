# HOI4 领导人特质系统完整示例解析

本文档使用真实游戏代码，展示领导人特质系统的所有关键用法。

---

## 📌 示例1：基础特质结构

**来源**: `common/unit_leader/00_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 守旧派特质（最基础的特质）
    # ============================================
    old_guard = { 
        type = land                          # 类型：陆军
        trait_type = personality_trait        # 特质类型：个性特质
        
        # === 修正值 ===
        modifier = {
            max_dig_in = 1                   # 最大堑壕+1
        }
        
        # === 非共享修正值（仅影响此将领）===
        non_shared_modifier = {
            experience_gain_factor = -0.25   # 经验获取-25%
        }

        # === 新指挥官权重 ===
        new_commander_weight = {
            factor = 1
            
            modifier = {
                FROM = { has_idea = best_of_the_best_spirit }
                factor = 0                   # 有最佳精神时不生成
            }
            modifier = {
                FROM = { has_idea = academy_scholarships_spirit }
                factor = 0
            }
        }
    }
}
```

### 💡 关键说明

**`type`字段**:
- `land`: 陆军特质
- `navy`: 海军特质
- `all`: 陆海通用
- `{ land navy }`: 多类型（数组）

**`trait_type`字段**:
- `personality_trait`: 个性特质（开局随机）
- `status_trait`: 状态特质（战斗中获得）
- `assignable_trait`: 可分配特质（需手动分配）
- `basic_trait`: 基础特质（默认）
- `terrain_trait`: 地形特质

**`modifier` vs `non_shared_modifier`**:
- `modifier`: 影响部队
- `non_shared_modifier`: 仅影响此将领

---

## 📌 示例2：个性特质（攻击型）

**来源**: `common/unit_leader/00_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 杰出战略家
    # ============================================
    brilliant_strategist = { 
        type = land
        trait_type = personality_trait
        
        # === 技能加成 ===
        attack_skill = 1          # 攻击技能+1
        planning_skill = 1        # 计划技能+1
        
        # === 技能因子 ===
        attack_skill_factor = 1    # 攻击技能升级权重+1
        planning_skill_factor = 1  # 计划技能升级权重+1

        new_commander_weight = {
            factor = 1
            
            modifier = {
                FROM = { has_idea = best_of_the_best_spirit }
                factor = 0
            }
            modifier = {
                FROM = { has_idea = academy_scholarships_spirit }
                factor = 0
            }
        }
    }
    
    # ============================================
    # 顽固战略家（防御型）
    # ============================================
    inflexible_strategist = { 
        type = land
        trait_type = personality_trait
        
        defense_skill = 1
        logistics_skill = 1
        
        defense_skill_factor = 1
        logistics_skill_factor = 1

        new_commander_weight = {
            factor = 1
            
            modifier = {
                is_army_leader = yes
                FROM = { has_idea = best_of_the_best_spirit }
                factor = 0
            }
        }
    }
    
    # ============================================
    # 政治关系
    # ============================================
    politically_connected = { 
        type = land
        trait_type = personality_trait
        
        non_shared_modifier = {
            experience_gain_factor = -0.1      # 经验获取-10%
            promote_cost_factor = -0.5        # 晋升成本-50%
        }
        
        planning_skill_factor = 1
        logistics_skill_factor = 1
        
        new_commander_weight = {
            factor = 1
            
            modifier = {
                is_army_leader = yes
                FROM = { has_idea = best_of_the_best_spirit }
                factor = 0
            }
        }
    }
}
```

### 💡 关键说明

**技能系统**:
- `attack_skill`: 攻击技能固定加成
- `attack_skill_factor`: 攻击技能升级概率权重

**`new_commander_weight`**:
- 控制新指挥官生成时是否有此特质
- `factor = 0` 表示不随机生成
- 可通过条件修正控制

---

## 📌 示例3：状态特质（战斗获得）

**来源**: `common/unit_leader/00_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 勇敢（战斗中获得）
    # ============================================
    brave = {
        type = land
        trait_type = status_trait
        
        modifier = {
            org_loss_at_low_org_factor = -0.1    # 低组织度时组织度损失-10%
        }
        
        # === 不随机生成 ===
        new_commander_weight = {
            factor = 0    # 必须通过战斗获得
        }
        
        defense_skill = 1
        
        # === 获得经验条件 ===
        gain_xp = {
            is_combat_leader = yes        # 必须在战斗中指挥
            OR = {
                average_combat_org < 0.3  # 平均组织度<30%
                enemies_strength_ratio > 2.0  # 敌人强度比>2.0
            }
        }
        
        # === 自定义获得提示 ===
        custom_gain_xp_trigger_tooltip = bravery_tt
    }
    
    # ============================================
    # 沙漠之狐（沙漠战斗获得）
    # ============================================
    trait_desert_fox = {
        type = land
        trait_type = status_trait
        
        modifier = {
            desert_attack = 0.10          # 沙漠攻击+10%
            desert_defense = 0.10         # 沙漠防御+10%
        }
        
        new_commander_weight = {
            factor = 0
        }
        
        # === 在沙漠地形获得经验 ===
        gain_xp = {
            is_combat_leader = yes
            terrain_type = desert         # 必须在沙漠地形战斗
        }
        
        custom_gain_xp_trigger_tooltip = trait_desert_fox_gain_tt
    }
}
```

### 💡 关键说明

**`gain_xp`字段**:
- 定义获得经验的条件
- 满足条件时有概率获得特质
- 可指定地形类型、战斗状态等

**常见战斗状态条件**:
- `is_combat_leader`: 正在指挥战斗
- `average_combat_org`: 平均组织度
- `enemies_strength_ratio`: 敌人强度比
- `terrain_type`: 地形类型

---

## 📌 示例4：地形特质系统

**来源**: `common/unit_leader/00_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 山地专家
    # ============================================
    trait_mountaineer = {
        type = land
        trait_type = terrain_trait
        
        modifier = {
            hills_attack = 0.05
            hills_defense = 0.05
            mountain_attack = 0.10
            mountain_defense = 0.10
        }
        
        new_commander_weight = {
            factor = 0
        }
        
        # === GUI布局 ===
        gui_row = 1
        gui_column = 0
        
        gain_xp = {
            is_combat_leader = yes
            OR = {
                terrain_type = hills
                terrain_type = mountain
            }
        }
    }
    
    # ============================================
    # 林地专家
    # ============================================
    trait_forest_ranger = {
        type = land
        trait_type = terrain_trait
        
        modifier = {
            forest_attack = 0.10
            forest_defense = 0.10
            jungle_attack = 0.05
            jungle_defense = 0.05
        }
        
        new_commander_weight = {
            factor = 0
        }
        
        gui_row = 1
        gui_column = 1
        
        gain_xp = {
            is_combat_leader = yes
            OR = {
                terrain_type = forest
                terrain_type = jungle
            }
        }
    }
    
    # ============================================
    # 冬季专家
    # ============================================
    trait_winter_specialist = {
        type = land
        trait_type = terrain_trait
        
        modifier = {
            winter_attack = 0.10
            winter_defense = 0.10
            snow_attack = 0.05
            snow_defense = 0.05
            frozen_attack = 0.05
            frozen_defense = 0.05
        }
        
        new_commander_weight = {
            factor = 0
        }
        
        gui_row = 1
        gui_column = 2
        
        gain_xp = {
            is_combat_leader = yes
            OR = {
                terrain_type = winter
                terrain_type = snow
                terrain_type = frozen
            }
        }
    }
}
```

### 💡 关键说明

**地形类型**:
- `plains`: 平原
- `forest`: 森林
- `hills`: 丘陵
- `mountain`: 山地
- `desert`: 沙漠
- `jungle`: 丛林
- `marsh`: 沼泽
- `urban`: 城市
- `snow`: 雪地
- `frozen`: 冻土
- `winter`: 冬季

**`gui_row`和`gui_column`**:
- 控制特质在UI中的位置
- 从0开始计数
- `-1`或省略表示不显示

---

## 📌 示例5：海军特质

**来源**: `common/unit_leader/00_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 优秀战术家
    # ============================================
    superior_tactician = {
        type = navy
        trait_type = personality_trait
        
        attack_skill = 1
        coordination_skill = 1
        
        attack_skill_factor = 1
        coordination_skill_factor = 1
        
        new_commander_weight = {
            factor = 1
            
            modifier = {
                FROM = { has_idea = best_of_the_best_naval_academy_spirit }
                factor = 0
            }
        }
    }
    
    # ============================================
    # 海狼（潜艇专家）
    # ============================================
    seawolf = {
        type = navy
        trait_type = personality_trait
        
        modifier = {
            submarine_detection = 0.2        # 潜艇探测+20%
            submarine_visibility = -0.2      # 潜艇可见度-20%
        }
        
        maneuvering_skill_factor = 1
        
        new_commander_weight = {
            factor = 0    # 特殊特质，不随机生成
        }
    }
    
    # ============================================
    # 航母打击
    # ============================================
    carrier_bonuses = {
        type = navy
        trait_type = status_trait
        
        modifier = {
            carrier_air_targetting = 0.10     # 航母舰载机目标锁定+10%
            carrier_naval_strike_attack = 0.05  # 航母攻击+5%
        }
        
        new_commander_weight = {
            factor = 0
        }
        
        gain_xp = {
            is_combat_leader = yes
            has_carrier = yes                  # 必须指挥航母
        }
    }
}
```

### 💡 关键说明

**海军技能**:
- `attack_skill`: 攻击技能
- `defense_skill`: 防御技能
- `maneuvering_skill`: 机动技能
- `coordination_skill`: 协调技能

**海军修正值**:
- `submarine_detection`: 潜艇探测
- `submarine_visibility`: 潜艇可见度
- `carrier_naval_strike_attack`: 航母攻击

---

## 📌 示例6：可分配特质

**来源**: `common/unit_leader/00_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 后勤专家（需手动分配）
    # ============================================
    logistic_expert = {
        type = land
        trait_type = assignable_trait
        
        # === 分配成本 ===
        cost = 1000                # 需要1000政治点数
        
        # === 前置条件 ===
        prerequisites = {
            logistics_skill >= 3   # 后勤技能>=3
        }
        
        # === 修正值 ===
        modifier = {
            supply_consumption_factor = -0.10    # 补给消耗-10%
        }
        
        # === 每日效果 ===
        daily_effect = {
            add_army_experience = 0.05    # 每日+0.05陆军经验
        }
        
        # === 互斥特质 ===
        mutually_exclusive = logistic_incompetent
        
        new_commander_weight = {
            factor = 0    # 不随机生成
        }
    }
    
    # ============================================
    # 空中支援协调
    # ============================================
    air_support_coordination = {
        type = land
        trait_type = assignable_trait
        
        cost = 1500
        
        prerequisites = {
            attack_skill >= 3
            planning_skill >= 2
        }
        
        modifier = {
            close_air_support_efficiency_on_unit = 0.10    # 近距空中支援效率+10%
        }
        
        # === 启用能力 ===
        enable_ability = last_stand_ability    # 解锁背水一战能力
        
        new_commander_weight = {
            factor = 0
        }
    }
}
```

### 💡 关键说明

**`assignable_trait`**:
- 需要玩家手动分配
- 消耗政治点数
- 可设置前置条件

**`cost`字段**:
- 分配成本（政治点数）
- 建议范围：500-2000

**`prerequisites`字段**:
- 分配前置条件
- 通常要求技能等级

**`enable_ability`字段**:
- 解锁特殊能力
- 如背水一战、强行军等

---

## 📌 示例7：国家特有特质

**来源**: `common/unit_leader/JAP_traits.txt`

```hoi4
leader_traits = {
    # ============================================
    # 日本特有：神风突击
    # ============================================
    JAP_kamikaze = {
        type = navy
        trait_type = assignable_trait
        
        cost = 0    # 免费分配
        
        prerequisites = {
            has_country_flag = JAP_kamikaze_unlocked
        }
        
        modifier = {
            ship_attack_factor = 0.30      # 舰船攻击+30%
            ship_sunk_damage_chance = 0.5  # 沉船概率+50%
        }
        
        on_add = {
            # 分配时触发效果
            country_event = { id = japan.kamikaze.100 }
        }
        
        new_commander_weight = {
            factor = 0
        }
    }
}
```

### 💡 关键说明

**`on_add`效果**:
- 分配特质时触发
- 可触发事件、设置标记等

**国家特有特质**:
- 放在单独文件中（如JAP_traits.txt）
- 使用国家前缀命名
- 通常有特殊解锁条件

---

## 📌 示例8：高级修正值系统

```hoi4
leader_traits = {
    # ============================================
    # 装甲指挥官
    # ============================================
    armor_commander = {
        type = land
        trait_type = assignable_trait
        
        cost = 2000
        
        # === 单位修正值 ===
        sub_unit_modifiers = {
            armor = {
                units = {
                    # 对装甲单位生效
                    super_heavy_tank_bat
                    heavy_tank_bat
                    medium_tank_bat
                    light_tank_bat
                }
                # 修正值
                attack = 0.10
                defense = 0.05
                breakthrough = 0.10
            }
        }
        
        prerequisites = {
            attack_skill >= 4
        }
        
        new_commander_weight = {
            factor = 0
        }
    }
    
    # ============================================
    # 经验加成特质
    # ============================================
    veteran_instructor = {
        type = land
        trait_type = assignable_trait
        
        cost = 1000
        
        # === 特质经验因子 ===
        trait_xp_factor = {
            brave = 1.5              # 勇敢特质获得经验+50%
            trait_desert_fox = 2.0   # 沙漠之狐获得经验+100%
        }
        
        modifier = {
            division_attack = 0.05
        }
        
        new_commander_weight = {
            factor = 0
        }
    }
}
```

### 💡 关键说明

**`sub_unit_modifiers`**:
- 对特定单位类型生效
- 支持多个单位定义
- 可设置攻击、防御、突破等

**`trait_xp_factor`**:
- 影响其他特质的获得速度
- 用于教学型特质

---

## 📝 本地化示例

```yaml
l_english:
 # 特质名称
 old_guard:0 "Old Guard"
 old_guard_desc:0 "This commander is resistant to new ideas and tactics."
 
 brilliant_strategist:0 "Brilliant Strategist"
 brilliant_strategist_desc:0 "A master of grand strategy and operational planning."
 
 # 获得提示
 trait_desert_fox_gain_tt:0 "Fighting in §HDesert§! terrain."
 bravery_tt:0 "Leading troops in desperate situations with low organization."
 
 # 效果提示
 logistic_expert_tt:0 "§G-10%§! Supply Consumption."
```

---

## ✅ 最佳实践

### 1. 特质类型选择
| 类型 | 获得方式 | 用途 |
|------|----------|------|
| `personality_trait` | 开局随机 | 基础个性 |
| `status_trait` | 战斗获得 | 地形专家、勇敢 |
| `assignable_trait` | 手动分配 | 后勤、战术 |
| `terrain_trait` | 特殊地形 | 山地、丛林 |

### 2. 平衡性建议
- 个性特质：小加成（5-10%）
- 状态特质：中加成（10-15%）
- 可分配特质：大加成（15-25%）
- 成本与效果匹配

### 3. GUI布局
- 同类特质放在同一行
- 地形特质按地形类型排列
- 留出扩展空间

---

**恭喜！你已掌握 HOI4 领导人特质系统的核心用法！**
