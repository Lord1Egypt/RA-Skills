# HOI4 人物系统完整示例解析

本文档使用真实游戏代码，展示人物系统的所有关键用法。

---

## 📌 示例1：国家领导人（波兰）

**来源**: `common/characters/POL.txt`

```hoi4
characters = {
    # ============================================
    # 国家领导人：安娜斯塔西娅·罗曼诺夫
    # ============================================
    POL_anna_andersson = {
        name = "Anastasia Romanov"    # 显示名称（可直接写或引用本地化键）
        
        # === 头像系统 ===
        portraits = {
            civilian = {    # 文职头像（用于国家领导人）
                large = "GFX_portrait_POL_anna_anderson"    # 大头像
            }
        }
        
        # === 国家领导人角色 ===
        country_leader = {
            ideology = despotism    # 意识形态类型
            traits = { the_last_romanov_maybe }    # 领导人特质（可多个）
            expire = "1965.1.1.1"    # 过期时间（通常设为1965）
            id = -1    # 内部ID（-1表示自动分配）
        }
    }

    # ============================================
    # 国家领导人：卡尔·阿尔布雷希特
    # ============================================
    POL_karl_albrecht = {
        name = POL_karl_albrecht    # 引用本地化键
        
        portraits = {
            civilian = {
                large = "GFX_portrait_POL_karl_albrecht"
            }
        }
        
        country_leader = {
            ideology = despotism
            traits = { patriot_king }    # 爱国者国王特质
            expire = "1965.1.1.1"
            id = -1
        }
    }

    # ============================================
    # 国家领导人：弗里德里希·克里斯蒂安
    # ============================================
    POL_friedrich_christian = {
        name = POL_friedrich_christian
        portraits = {
            civilian = {
                large = "GFX_portrait_POL_friedrich_christian"
            }
        }
        country_leader = {
            ideology = despotism
            expire = "1965.1.1.1"
            id = -1
            traits = { royal_legitimist }    # 皇位合法主义者
        }
    }
}
```

### 💡 关键说明

**`name`字段**:
- 可直接写文本：`name = "Anastasia Romanov"`
- 可引用本地化：`name = POL_karl_albrecht`

**`portraits`系统**:
- `civilian`: 文职头像（国家领导人）
- `army`: 陆军头像（军事指挥官）
- `navy`: 海军头像（海军指挥官）
- `large`: 大头像（对话框、领导人界面）
- `small`: 小头像（顾问槽、将领列表）

**意识形态类型**:
- `nazism`: 纳粹主义
- `fascism`: 法西斯主义
- `despotism`: 专制主义
- `oligarchism`: 寡头政治
- `anarchism`: 无政府主义
- `conservatism`: 保守主义
- `liberalism`: 自由主义
- `socialism`: 社会主义
- `marxism`: 马克思主义
- `leninism`: 列宁主义
- `democratic`: 民主主义（旧版本）

---

## 📌 示例2：军事指挥官（波兰）

**来源**: `common/characters/POL.txt`

```hoi4
characters = {
    # ============================================
    # 军级指挥官 + 国家领导人双角色
    # ============================================
    POL_boleslaw_wieniawa_glugoszowski = {
        name = POL_boleslaw_wieniawa_glugoszowski
        
        portraits = {
            civilian = {
                large = "GFX_portrait_POL_boleslaw_wieniawa_dlugoszowski"
            }
            army = {
                large = "GFX_portrait_POL_boleslaw_wieniawa_dlugoszowski"
                small = "GFX_idea_POL_boleslaw_wieniawa_dlugoszowski"    # 小头像（可选）
            }
        }

        # === 军级指挥官 ===
        corps_commander = {
            traits = { 
                cavalry_officer        # 骑兵军官
                war_hero              # 战争英雄
                politically_connected # 政治关系
            }
            skill = 2              # 总技能等级（1-5）
            attack_skill = 2       # 攻击技能
            defense_skill = 2       # 防御技能
            planning_skill = 2      # 计划技能
            logistics_skill = 1     # 后勤技能
            legacy_id = -1         # 遗留ID（-1表示自动）
        }
        
        # === 国家领导人（同时担任）===
        country_leader = {
            ideology = oligarchism
            traits = { polish_legionary }    # 波兰军团成员
        }
    }

    # ============================================
    # 军级指挥官（条件可见）
    # ============================================
    POL_vladislav_korchits = {
        name = POL_vladislav_korchits
        portraits = {
            army = {
                large = GFX_portrait_POL_vladislav_korchits
                small = GFX_portrait_POL_vladislav_korchits_small
            }
        }
        
        corps_commander = {
            # === 条件可见性 ===
            visible = {
                has_completed_focus = POL_soviet_military_staff
            }
            
            traits = { 
                JAP_communist_sympathizer    # 共产主义同情者
                old_guard                     # 守旧派
            }
            skill = 3
            attack_skill = 2
            defense_skill = 4
            planning_skill = 3
            logistics_skill = 2
        }
    }

    # ============================================
    # 陆军元帅
    # ============================================
    POL_wladyslaw_sikorski = {
        name = POL_wladyslaw_sikorski
        portraits = {
            civilian = {
                large = GFX_portrait_POL_wladyslaw_sikorski
            }
            army = {
                large = GFX_portrait_POL_wladyslaw_sikorski
                small = GFX_portrait_POL_wladyslaw_sikorski_small
            }
        }

        # === 陆军元帅 ===
        field_marshal = {
            traits = { 
                POL_sanation_left_leader    # 国家特有特质
                defensive_doctrine           # 防御学说
            }
            skill = 3
            attack_skill = 2
            defense_skill = 3
            planning_skill = 2
            logistics_skill = 3
            legacy_id = -1
        }
        
        country_leader = {
            ideology = oligarchism
            traits = { patriotic_guerilla }
            expire = "1965.1.1.1"
            id = -1
        }
    }
}
```

### 💡 关键说明

**指挥官类型**:
- `corps_commander`: 军级指挥官（指挥24师以下）
- `field_marshal`: 陆军元帅（指挥24-120师）
- `navy_leader`: 海军指挥官

**技能系统**:
- `skill`: 总技能等级（1-5，影响所有子技能）
- 子技能可不填，自动继承 `skill` 值
- 也可单独指定，覆盖总技能值

**`visible`字段**:
- 控制人物是否在将领列表显示
- 常用于DLC锁定、国策解锁的将领

**多角色支持**:
- 同一人可以同时是：
  - 国家领导人（`country_leader`）
  - 军事指挥官（`corps_commander`/`field_marshal`）
  - 顾问（`advisor`）

---

## 📌 示例3：顾问角色（波兰）

**来源**: `common/characters/POL.txt`

```hoi4
characters = {
    # ============================================
    # 政治顾问
    # ============================================
    POL_ignacy_moscicki = {
        name = POL_ignacy_moscicki
        portraits = {
            army = {
                small = GFX_portrait_POL_ignacy_moscicki_small
            }
            civilian = {
                large = "GFX_portrait_POL_ignacy_moscicki"
            }
        }
        
        # === 顾问角色 ===
        advisor = {
            slot = political_advisor    # 顾问槽位
            idea_token = POL_ignacy_moscicki    # Ideas系统标识符
            
            # === 可用条件 ===
            available = {
                OR = {
                    has_completed_focus = POL_ozon 
                    has_completed_focus = POL_dissolve_the_bbwr 
                }
            }
            
            # === 允许条件（生成时检查）===
            allowed = {
                original_tag = POL
                OR = {
                    has_dlc = "No Step Back"
                    has_dlc = "Poland: United and Ready"
                }
            }
            
            # === 特质（可多个）===
            traits = {
                the_king_of_the_castle    # 城堡之王
            }
        }
        
        country_leader = {
            ideology = oligarchism
            expire = "1965.1.1.1"
            id = -1
            traits = { POL_ignacy_moscicki_leader }
        }
    }
}
```

### 💡 关键说明

**`slot`字段**:
- `political_advisor`: 政治顾问
- `army_chief`: 陆军参谋长
- `navy_chief`: 海军参谋长
- `air_chief`: 空军参谋长
- `high_command`: 最高统帅部
- `theorist`: 理论家

**`idea_token`字段**:
- Ideas系统中的唯一标识符
- 用于效果和条件引用
- 可与角色ID相同或不同

**`available` vs `allowed`**:
- `available`: 随时可用的条件（玩家点击时检查）
- `allowed`: 生成时的条件（创建顾问时检查）

---

## 📌 示例4：女性角色（德国）

**来源**: `common/characters/GER.txt`

```hoi4
characters = {
    # ============================================
    # 女性角色：爱娃·布劳恩
    # ============================================
    GER_eva_braun = {
        name = GER_eva_braun
        
        portraits = {
            civilian = {
                large = GFX_portrait_GER_eva_braun
                small = GFX_portrait_GER_eva_braun_small
            }
        }
        
        # === 性别标识 ===
        gender = female    # 女性角色
        
        # 国家领导人（注释掉，保留作为彩蛋）
        #country_leader = {
        #    ideology = nazism
        #    traits = { GER_the_iron_maiden }
        #    expire = "1965.1.1.1"
        #    id = -1
        #}
    }
}
```

### 💡 关键说明

**`gender`字段**:
- `female`: 女性角色
- 不填默认为男性
- 影响本地化中的性别代词

---

## 📌 示例5：隐藏角色（德国）

**来源**: `common/characters/GER.txt`

```hoi4
characters = {
    # ============================================
    # 空角色：威廉二世（仅定义，不自动成为领导人）
    # ============================================
    GER_wilhelm_ii = {
        name = GER_wilhelm_ii
        portraits = {
            civilian = {
                large = GFX_portrait_ger_wilhelm_ii
            }    
        }
        # 不定义 country_leader，不会自动成为领导人
        # 需要通过效果手动设置：set_country_leader = GER_wilhelm_ii
    }

    # ============================================
    # 条件可见顾问：奥托·施特拉塞尔
    # ============================================
    GER_otto_strasser = {
        name = GER_otto_strasser
        portraits = {
            civilian = {
                large = GFX_portrait_GER_otto_strasser
                small = GFX_portrait_GER_otto_strasser_small
            }
        }

        advisor = {
            slot = political_advisor
            idea_token = GER_otto_strasser
            
            # === 允许条件 ===
            allowed = {
                original_tag = GER
            }
            
            # === 可见性条件（彩蛋）===
            visible = {
                has_completed_focus = GER_expatriate_the_communists_ww
                has_country_flag = GER_strasserism_relevant_in_germany_flag
            }
            
            available = {
                # 可用条件（满足visible后才检查）
            }
            
            traits = {
                GER_revolutionary_nationalist_advisor
            }
        }
    }
}
```

### 💡 关键说明

**空角色模式**:
- 只定义 `name` 和 `portraits`
- 不定义任何角色类型
- 通过效果手动设置：`set_country_leader = GER_wilhelm_ii`

**`visible`字段**:
- 控制顾问是否在列表中显示
- 用于隐藏彩蛋、DLC锁定内容

---

## 📌 示例6：海军指挥官

**来源**: 从游戏文件综合

```hoi4
characters = {
    # ============================================
    # 海军指挥官
    # ============================================
    POL_jozef_unrug = {
        name = POL_jozef_unrug
        portraits = {
            navy = {
                large = GFX_portrait_POL_jozef_unrug
                small = GFX_portrait_POL_jozef_unrug_small
            }
        }
        
        navy_leader = {
            traits = {
                superior_tactician    # 优秀战术家
                seawolf              # 海狼
            }
            skill = 3              # 海军总技能
            attack_skill = 2       # 攻击技能
            defense_skill = 3      # 防御技能
            maneuvering_skill = 3  # 机动技能
            coordination_skill = 2 # 协调技能
        }
    }
}
```

### 💡 关键说明

**海军技能**:
- `maneuvering_skill`: 机动技能
- `coordination_skill`: 协调技能
- 替代陆军的 `planning_skill` 和 `logistics_skill`

---

## 📌 示例7：通过效果设置领导人

```hoi4
# === 在国策或事件中设置领导人 ===
completion_reward = {
    # 方法1：设置国家领导人
    set_country_leader = {
        ideology = despotism
        leader = POL_karl_albrecht
    }
    
    # 方法2：替换领导人
    replace_country_leader = {
        ideology = despotism
        leader = POL_karl_albrecht
    }
    
    # 方法3：通过效果设置
    POL_karl_albrecht = {
        set_country_leader = yes
    }
}
```

---

## 📌 示例8：通过效果生成指挥官

```hoi4
# === 在国策或事件中生成指挥官 ===
completion_reward = {
    # 方法1：创建指定角色
    create_country_leader = {
        name = "New Leader"
        desc = "leader_desc"
        picture = GFX_portrait_new_leader
        ideology = democracy
        traits = { incorruptible }
        skill = 4
        attack_skill = 3
        defense_skill = 3
        planning_skill = 4
        logistics_skill = 2
    }
    
    # 方法2：使用已定义角色
    create_field_marshal = {
        character = POL_boleslaw_wieniawa_glugoszowski
    }
}
```

---

## 📝 本地化示例

```yaml
l_english:
 # 人物名称
 POL_anna_anderson:0 "Anastasia Romanov"
 POL_karl_albrecht:0 "Karl Albrecht I"
 POL_boleslaw_wieniawa_glugoszowski:0 "Bolesław Wieniawa-Długoszowski"
 
 # 领导人特质
 the_last_romanov_maybe:0 "The Last Romanov"
 the_last_romanov_maybe_desc:0 "Some claim she is the surviving daughter of the Tsar."
 
 patriot_king:0 "Patriot King"
 patriot_king_desc:0 "A king who puts his country above all else."
```

---

## ✅ 最佳实践

### 1. 命名规范
```
{TAG}_{name}              # 国家前缀（领导人）
{TAG}_{rank}_{name}       # 军衔前缀（将领）
```

### 2. 头像准备
- 大头像：128x128 或 256x256
- 小头像：48x48 或 64x64
- 格式：PNG 或 DDS

### 3. 多角色使用
```hoi4
# 同一人担任多个角色
character_name = {
    portraits = { ... }
    
    country_leader = { ... }
    corps_commander = { ... }
    advisor = { ... }
}
```

### 4. 条件可见性
- 使用 `visible` 控制显示
- 用于DLC锁定、国策解锁
- 避免过多隐藏角色影响性能

---

**恭喜！你已掌握 HOI4 人物系统的核心用法！**
