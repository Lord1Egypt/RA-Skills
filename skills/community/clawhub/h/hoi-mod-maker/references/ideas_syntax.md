# HOI4 Ideas 完整语法参考

## 目录

1. [文件结构](#文件结构)
2. [Idea 类型](#idea-类型)
3. [国家精神 (country)](#国家精神-country)
4. [军事精神](#军事精神)
5. [顾问系统](#顾问系统)
6. [设计商系统](#设计商系统)
7. [常用 Modifier 速查表](#常用-modifier-速查表)
8. [示例代码](#示例代码)

---

## 文件结构

```
common/ideas/{filename}.txt

ideas = {
    country = { ... }
    army = { ... }
    navy = { ... }
    air = { ... }
    political_advisor = { ... }
    theorist = { ... }
    chief_of_staff = { ... }
    army_chief = { ... }
    navy_chief = { ... }
    air_chief = { ... }
}
```

---

## Idea 类型

| 类型 | 槽位 | 说明 |
|------|------|------|
| `country` | 无限制 | 国家精神，可同时拥有多个 |
| `army` | 1个 | 陆军精神（需DLC） |
| `navy` | 1个 | 海军精神（需DLC） |
| `air` | 1个 | 空军精神（需DLC） |
| `political_advisor` | 1个 | 政治顾问 |
| `theorist` | 1个 | 理论家 |
| `chief_of_staff` | 1个 | 参谋长 |
| `army_chief` | 1个 | 陆军首脑 |
| `navy_chief` | 1个 | 海军首脑 |
| `air_chief` | 1个 | 空军首脑 |

---

## 国家精神 (country)

### 基础模板

```
{TAG}_{idea_name} = {
    # 可用性限制
    allowed = {
        original_tag = {TAG}
        always = no          # 防止其他国家获取
    }
    
    # 内战时的处理
    allowed_civil_war = {
        always = no          # 内战双方都不继承
    }
    
    # 移除花费（-1 = 不可移除）
    removal_cost = -1
    
    # 图标（使用现有GFX或自定义）
    picture = generic_political_reform
    
    # 效果修正
    modifier = {
        political_power_gain = 0.10
        stability_factor = 0.05
        consumer_goods_factor = 0.05
    }
    
    # 对特定国家的修正
    targeted_modifier = {
        tag = GER
        attack_bonus_against = 0.10
        defense_bonus_against = 0.05
    }
}
```

### allowed 字段详解

```
allowed = {
    # 原始国家标签
    original_tag = POL
    
    # 多国家共享
    OR = {
        original_tag = POL
        original_tag = RSI
        original_tag = RDS
    }
    
    # 条件限制
    has_government = fascism
    is_subject = no
}
```

### removal_cost

```
removal_cost = -1      # 不可移除（永久精神）
removal_cost = 0       # 免费移除
removal_cost = 50      # 需要50政治点数移除
removal_cost = 150     # 需要150政治点数移除
```

### name 字段（引用其他idea名称）

```
# 使用其他idea的名称和描述
POL_economic_crisis_v2 = {
    name = POL_economic_crisis    # 引用 POL_economic_crisis 的名称/描述
    
    allowed = { original_tag = POL }
    
    modifier = {
        consumer_goods_factor = 0.20
        production_speed_buildings_factor = -0.20
    }
}
```

---

## 军事精神

### 陆军精神模板

```
army = {
    {TAG}_army_spirit = {
        allowed = {
            original_tag = {TAG}
        }
        
        picture = generic_army
        
        # 允许移除和更换
        removal_cost = 100
        
        modifier = {
            army_org_factor = 0.05
            army_morale_factor = 0.05
            land_terrain_attack = 0.05
            land_terrain_defense = 0.05
        }
        
        # 对特定国家加成
        targeted_modifier = {
            tag = SOV
            attack_bonus_against = 0.10
        }
    }
}
```

### 海军精神模板

```
navy = {
    {TAG}_navy_spirit = {
        allowed = { original_tag = {TAG} }
        
        picture = generic_navy
        
        modifier = {
            naval_hit_chance_factor = 0.05
            naval_speed_factor = 0.05
            screening_efficiency_factor = 0.05
            mine_laying_efficiency_factor = 0.10
            mine_effectiveness_factor = 0.10
        }
    }
}
```

### 空军精神模板

```
air = {
    {TAG}_air_spirit = {
        allowed = { original_tag = {TAG} }
        
        picture = generic_air
        
        modifier = {
            air_mission_efficiency_factor = 0.05
            air_ace_generation_chance_factor = 0.10
            fighter_air_attack_factor = 0.05
            fighter_air_defence_factor = 0.05
        }
    }
}
```

---

## 顾问系统

### 政治顾问模板

```
political_advisor = {
    {TAG}_{advisor_name} = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{advisor_name}
        
        # 可选：意识形态倾向
        fascist = yes              # 增加法西斯支持度
        # communist = yes
        # democratic = yes
        # neutrality = yes
        
        modifier = {
            fascism_drift = 0.10
            # communism_drift = 0.10
            # democratic_drift = 0.10
            # neutrality_drift = 0.10
            
            # 或稳定度加成
            stability_weekly = 0.10
            war_support_weekly = 0.05
            
            # 或派系加成
            passive_faction_political_cost = -0.15
        }
    }
}
```

### 理论家模板

```
theorist = {
    {TAG}_{theorist_name} = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{theorist_name}
        
        modifier = {
            army_experience_gain_factor = 0.05
            # navy_experience_gain_factor = 0.05
            # air_experience_gain_factor = 0.05
            
            # 或研究加成
            land_doctrine_research_speed = 0.10
            # naval_doctrine_research_speed = 0.10
            # air_doctrine_research_speed = 0.10
        }
    }
}
```

### 参谋长模板

```
chief_of_staff = {
    {TAG}_cos_name = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        modifier = {
            command_capacity = 0.10        # 指挥容量
            staff_planning_max = 0.10      # 参谋计划
            supply_grace = 0.10            # 补给储备
        }
    }
}
```

### 军队首脑模板

```
army_chief = {
    {TAG}_army_chief_name = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        modifier = {
            army_attack_factor = 0.05
            army_defence_factor = 0.05
            army_org_factor = 0.05
            land_terrain_attack = 0.05
            
            # 或特定地形
            land_terrain_plains_attack = 0.10
            land_terrain_forest_attack = 0.10
            land_terrain_hills_attack = 0.10
            land_terrain_mountain_attack = 0.10
            land_terrain_urban_attack = 0.10
        }
    }
}

navy_chief = {
    {TAG}_navy_chief_name = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        modifier = {
            naval_attack_factor = 0.05
            naval_defence_factor = 0.05
            carrier_capacity_factor = 0.10
            naval_speed_factor = 0.05
        }
    }
}

air_chief = {
    {TAG}_air_chief_name = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        modifier = {
            air_attack_factor = 0.05
            air_defence_factor = 0.05
            carrier_traffic_efficiency_factor = 0.10
            air_mission_efficiency_factor = 0.05
        }
    }
}
```

---

## 设计商系统

### 坦克设计商

```
tank_manufacturer = {
    {TAG}_{manufacturer_name} = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        removal_cost = 200           # 设计商更换成本较高
        
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
}
```

### 船舶设计商

```
ship_manufacturer = {
    {TAG}_{manufacturer_name} = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        removal_cost = 200
        
        modifier = {
            # 船体特性
            ship_reliability_factor = 0.10
            ship_max_speed_factor = 0.05
            ship_anti_air_factor = 0.10
            
            # 研究加成
            naval_research_speed_factor = 0.10
        }
    }
}
```

### 飞机设计商

```
aircraft_manufacturer = {
    {TAG}_{manufacturer_name} = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        removal_cost = 200
        
        modifier = {
            # 飞机特性
            fighter_air_attack_factor = 0.10
            fighter_air_defence_factor = 0.05
            
            # 或轰炸机
            bomber_air_attack_factor = 0.10
            
            # 研究加成
            air_research_speed_factor = 0.10
        }
    }
}
```

### 工业设计商

```
industrial_concern = {
    {TAG}_{industrial_name} = {
        allowed = { original_tag = {TAG} }
        
        picture = GFX_{name}
        
        removal_cost = 150
        
        modifier = {
            # 工业研究
            industrial_research_speed = 0.10
            
            # 生产速度
            production_speed_industrial_complex_factor = 0.05
            production_speed_arms_factory_factor = 0.05
            
            # 或资源开采
            oil_factor = 0.10
            steel_factor = 0.10
            aluminum_factor = 0.10
        }
    }
}
```

---

## 常用 Modifier 速查表

### 政治类

| Modifier | 说明 | 范围 |
|----------|------|------|
| `political_power_gain` | 政治点数增益 | 0.1 = +10% |
| `stability_factor` | 稳定度加成 | 0.05 = +5% |
| `war_support_factor` | 战争支持度 | 0.05 = +5% |
| `consumer_goods_factor` | 消费品比例 | 0.05 = +5% |
| `fascism_drift` | 法西斯倾向 | 0.1 = 每日+0.1% |
| `communism_drift` | 共产主义倾向 | 同上 |
| `democratic_drift` | 民主倾向 | 同上 |
| `neutrality_drift` | 中立倾向 | 同上 |

### 工业类

| Modifier | 说明 |
|----------|------|
| `production_speed_buildings_factor` | 建筑速度 |
| `production_speed_industrial_complex_factor` | 民用工厂速度 |
| `production_speed_arms_factory_factor` | 军用工厂速度 |
| `industrial_capacity_factory` | 工厂产出 |
| `industrial_speed_factory` | 工厂效率 |
| `research_speed_factor` | 研究速度 |

### 陆军类

| Modifier | 说明 |
|----------|------|
| `army_org_factor` | 组织度 |
| `army_morale_factor` | 士气（恢复） |
| `army_attack_factor` | 攻击 |
| `army_defence_factor` | 防御 |
| `land_terrain_attack` | 地形攻击（所有） |
| `land_terrain_plains_attack` | 平原攻击 |
| `land_terrain_forest_attack` | 森林攻击 |
| `land_terrain_hills_attack` | 丘陵攻击 |
| `land_terrain_mountain_attack` | 山地攻击 |
| `land_terrain_urban_attack` | 城市攻击 |
| `attack_bonus_against` | 对特定国家攻击 |

### 海军类

| Modifier | 说明 |
|----------|------|
| `naval_hit_chance_factor` | 命中率 |
| `naval_speed_factor` | 速度 |
| `naval_attack_factor` | 攻击 |
| `naval_defence_factor` | 防御 |
| `screening_efficiency_factor` | 屏蔽效率 |
| `carrier_traffic_efficiency_factor` | 航母甲板效率 |
| `mine_laying_efficiency_factor` | 布雷效率 |
| `submarine_visibility_factor` | 潜艇可见度 |

### 空军类

| Modifier | 说明 |
|----------|------|
| `air_mission_efficiency_factor` | 任务效率 |
| `air_ace_generation_chance_factor` | 王牌生成 |
| `fighter_air_attack_factor` | 战斗机攻击 |
| `fighter_air_defence_factor` | 战斗机防御 |
| `bomber_air_attack_factor` | 轰炸机攻击 |

---

## 示例代码

### 完整国家精神示例

```
ideas = {
    country = {
        POL_sanacja_regime = {
            allowed = {
                original_tag = POL
                always = no
            }
            
            allowed_civil_war = {
                always = no
            }
            
            removal_cost = -1
            
            picture = generic_authoritarian_regime
            
            modifier = {
                political_power_gain = 0.10
                stability_factor = 0.05
                war_support_factor = 0.05
                
                # 负面效果
                democratic_drift = -0.05
                communism_drift = -0.05
                
                # 军事相关
                army_org_factor = 0.05
            }
            
            targeted_modifier = {
                tag = GER
                defense_bonus_against = 0.10
            }
        }
    }
}
```

### 完整顾问示例

```
ideas = {
    political_advisor = {
        POL_edward_smigly = {
            allowed = {
                original_tag = POL
            }
            
            picture = GFX_POL_edward_smigly
            
            neutrality = yes
            
            modifier = {
                neutrality_drift = 0.10
                stability_weekly = 0.10
                passive_faction_political_cost = -0.15
            }
        }
    }
}
```

### 完整设计商示例

```
ideas = {
    tank_manufacturer = {
        POL_PZInz = {
            allowed = {
                original_tag = POL
            }
            
            picture = GFX_POL_PZInz
            
            removal_cost = 200
            
            modifier = {
                tank_reliability_factor = 0.15
                tank_armor_factor = 0.10
                tank_max_speed_factor = 0.05
                tank_research_speed_factor = 0.10
                
                # 成本增加
                tank_build_cost_factor = 0.05
            }
        }
    }
}
```
