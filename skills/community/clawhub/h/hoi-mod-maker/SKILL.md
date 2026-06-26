---
name: hoi4-mod-maker
description: HOI4 mod全流程技能。国策树/民族精神/人物/事件/决议/本地化/变量/调试。触发：HOI4、钢铁雄心、钢4、国策、国策树、民族精神、焦点树、focus tree、national_focus、ideas、spirits、events、decisions、localisation、inner circle、连续焦点、replace_path、modding、Paradox
metadata:
  version: "1.0.3"
  changelog: |
    1.0.0 初版 — 含完整国策树/民族精神/事件/决议/本地化/调试技能；设计指南含坐标系统/动态定位/真实架构/递进奖励；黄金法则7条；templates参考模式；修复BOM/skill加载问题；去除机械拼装误导
---

# HOI4 Complete Mod-Maker Skill

**触发关键词**: HOI4 mod, 钢铁雄心4, 钢4, 国策, 国策树, 民族精神, 焦点树, focus tree, national_focus, ideas, spirits, events, decisions, localisation, inner circle, 连续焦点, replace_path, Paradox modding

---

## ⚠ 国策树布局黄金法则（每次生成前必读）

> AI 在生成国策树时最常见的错误。生成代码前，**必须确认以下七点全部满足**：

1. **图标尺寸**：每个国策图标是一个**以坐标 (x,y) 为中心的 2×2 正方形**。即图标左边界在 `x-1`，右边界在 `x+1`，上边界在 `y+1`，下边界在 `y-1`。**左右相邻（同行）时 x 差必须 >= 2，否则图标重叠**；上下相邻时 y 差 >= 1 即可。同一焦点块内紧凑排列时 x 间距用 2（最小合法值）。

2. **`relative_position_id` 是首选**：除非有充分理由（固定窗口锚点、避免 offset 继承等），一律使用 `relative_position_id = <父节点ID>` + 小的 x/y 偏移量。**绝对坐标只用于树的根节点或没有父节点的主干焦点**。

3. **前置国策必须存在**：每个 `prerequisite = { focus = XXX }` 引用的 `XXX` 必须在同一个国策树文件中实际定义。**不得凭空捏造 focus ID**，也不得使用其他国家的 focus ID 作为前置。生成完成后，对照 `examples/09_focus_tree_design_guide.md` 的检查清单逐条验证。

4. **禁止长线性链**：同一条路径上**连续节点不得超过 3 个**（即 A->B->C 之后必须出现分支或汇合）。超过 3 个连续节点会让玩家感到单调，且视觉上形成难看的长竖线。如需表达「递进过程」，用分支+汇合代替直线延伸。

5. **子节点数量上限**：单个焦点的直接子节点（同一 prerequisite 指向同一父节点）**不得超过 5 个**。超过 5 个时，将部分子节点改为二级分支（先汇到中间节点，再展开）。

6. **树深度要求**：单个国策树的**主路径深度应 >= 5 层**，建议 6-10 层。浅层树（<5层）会让玩家缺乏战略规划感。通过添加中间节点、分支选择、汇聚节点来增加深度。

7. **不同板块间距**：同一 `focus_tree` 内的不同分支（如政治/工业/军事），**根节点 x 坐标差应 >= 6**。不同 `focus_tree` 文件之间，使用不同的 `initial_show_position` 错开显示。**严禁不同板块的国策左右相邻且 x 差 < 2**，这会导致视觉混乱。

---


## Skill Meta

| 属性 | 值 |
|------|----|
| **版本** | 7.2 |
| **更新** | 2026-04-26 |
| **游戏版本** | HOI4 1.14+ |
| **覆盖范围** | 国策树 / 民族精神 / 人物 / 事件 / 决议 / 本地化 / 变量 / 调试 |
| **参考文件** | 74 原版国策树 + 10 语法参考 + 12 注释示例 |
| **特色能力** | 布局设计 / 原版ID查询 / 代码生成 / 递进奖励设计 / 兼容性指导 |

### 典型使用场景 → 推荐路径

| 用户意图 | 推荐路径 |
|---------|----------|
| 做国策树 | 09设计指南 → 布局规划 → 代码生成 → 检查清单 |
| 图标重叠 | 09设计指南 → 坐标系统/间距规则 |
| 查原版国策ID | `references/vanilla_focus_trees/` → 搜索对应国家.txt |
| 条件偏移 | 09设计指南(动态与条件定位) → advanced_syntax.md |
| 修改原版树 | 查原版ID → replace_path/同ID追加 |
| 写民族精神 | 02注释示例 → ideas_syntax.md → 08导入详解 |
| 内圈焦点 | 09设计指南(真实架构模式) → germany.txt参考 |
| 完成效果写法 | focus_complete_guide.md / dictionary.md |
| 本地化编码 | 04本地化详解 → UTF-8 BOM |
| mod不生效 | 调试技巧 → error.log |

---

## 快速开始

### Mod 基础文件结构

```
your_mod/
├── descriptor.mod              # Mod 描述符（必需）
├── thumbnail.png               # 封面图（推荐 256x256）
├── common/
│   ├── national_focus/         # 国策树 .txt
│   ├── ideas/                  # 民族精神 .txt
│   ├── characters/             # 人物定义 .txt
│   ├── unit_leader/            # 领导人特质 .txt
│   ├── decisions/              # 决议 .txt
│   └── modifiers/              # 自定义修正值
├── events/                     # 事件 .txt
├── localisation/
│   ├── english/                # 英文本地化 .yml
│   └── simp_chinese/           # 中文本地化 .yml
├── interface/                  # GFX 图标定义
└── gfx/
    └── goals/                  # 国策图标图片
```

### descriptor.mod 模板

```
name = "Your Mod Name"
version = "0.2.0"  # changelog: 扩展黄金法则至7条；去除模板机械拼装；新增孤立节点/碰撞检测；BOM清理修复skill加载
tags = { "National Focus" "Gameplay" }
picture = "thumbnail.png"
```

---

## 代码规范

### 基础语法

```
<attribute> = <argument>    # 数值/字符串/布尔值/代码块
```

### 编码要求

| 文件类型 | 编码 |
|---------|------|
| 脚本文件 (.txt) | UTF-8 无 BOM |
| 本地化文件 (.yml) | UTF-8 带 BOM |

### 缩进规范

- 开闭括号同一缩进层级
- 代码块内部增加一层缩进（Tab 或 4空格）
- 一行不要有多于一个括号

### 注释

```
# 单行注释（无多行注释）
cost = 10  # TODO: 检查平衡性
```

### 常量定义

```
@base_cost = 10
focus = { id = POL_focus  cost = @base_cost }
```

---

## 文件结构

### 加载顺序

```
Base Game → DLCs → User Directory → Mods
```

文件名排序：ASCII 字符顺序，`00_` 前缀先加载，`zz_` 后加载。

---

## 国策树

> 📄 **完整语法**: `references/focus_complete_guide.md` — Focus Tree 结构、节点字段、定位方式、前置条件、互斥、available、bypass、completion_reward 完整效果列表、内圈焦点、连续焦点、Search Filters
>
> 📄 **高级语法**: `references/advanced_syntax.md` — 备选图标、默认树、内圈窗口、快捷方式、嵌入窗口、连续焦点位置
>
> 📄 **形式化语法**: `references/syntax.md` — BNF 语法 + Joint/Shared Focus + 11 个常见陷阱
>
> 📄 **布局设计**: `examples/09_focus_tree_design_guide.md` — 坐标系统、间距、4步方法论、视口导航、动态定位、真实架构模式、递进奖励设计、原版数据分析

### 最小可用模板

```
focus_tree = {
    id = {TAG}_focus
    country = { factor = 0  modifier = { add = 10  tag = {TAG} } }
    default = no
    initial_show_position = { x = 500  y = 300 }
    
    focus = {
        id = {TAG}_root
        icon = GFX_goal_generic_political_pressure
        x = 0  y = 0
        cost = 5
        search_filters = { FOCUS_FILTER_POLITICAL }
        completion_reward = { add_political_power = 50 }
    }
    
    focus = {
        id = {TAG}_child
        prerequisite = { focus = {TAG}_root }
        relative_position_id = {TAG}_root
        x = 0  y = 1
        icon = GFX_goal_generic_authoritarian
        cost = 10
        completion_reward = { add_political_power = 100 }
    }
}
```

### 递进奖励（Progressive Reward）

> 📄 **完整设计指南**: `examples/09_focus_tree_design_guide.md` → 递进奖励设计章节

```
三层奖励结构：
  🪨 过程层 → cost=5, 1基建/10-15XP/25PP（克制，推动继续走）
  📦 阶段层 → cost=10, 1-2工厂+科技加成/50PP+25XP（阶段性成果）
  🏆 终点层 → cost=10-15, 3-4工厂+科技+50-100XP+100PP（终极目标）

核心原则：递进 ≠ 加量，是把相同总量重新分配——中间少给，终点多给
```

### 建筑效果（正确语法）

> 📄 **完整参考**: `references/focus_complete_guide.md` → 建筑效果章节

```
# ❌ 错误写法：random_owned_controlled_state + state = 762
# ✅ 正确写法：在 state scope 内直接调用 add_building_construction

# 指定州建造（推荐）
123 = {
    add_extra_state_shared_building_slots = 1    # 先扩容（如需）
    add_building_construction = {
        type = industrial_complex              # 民用工厂
        level = 1
        instant_build = yes
    }
}
124 = {
    add_extra_state_shared_building_slots = 2
    add_building_construction = { type = arms_factory  level = 2  instant_build = yes }
}

# 遍历所有符合条件的州
# every_owned_state = {
#     limit = { free_building_slots = { building = industrial_complex size > 0 } }
#     add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
# }

# 建筑类型：industrial_complex / arms_factory / dockyard
#           infrastructure / air_base / naval_base / bunker / coastal_bunker
```

### 可持久/连续国策

> 📄 **完整参考**: `references/focus_complete_guide.md` → Continuous Focus 章节

```
# 连续焦点（continuous = yes）：完成10个常规国策后解锁，激活期间持续生效
focus = {
    id = continuous_army_xp
    icon = GFX_focus_generic_army_xp
    x = 0  y = 0
    continuous = yes                  # 关键标记
    cost = 0                         # 连续焦点必须为 0
    search_filters = { FOCUS_FILTER_ARMY_XP }
    # ✅ 用 modifier = {} 提供持续效果（不是 completion_reward）
    modifier = { army_experience_gain_factor = 0.05 }
}

# 可取消的持久国策（带 cancel 块）
focus = {
    id = TAG_mobilization
    cost = 30
    cancel = {                        # ❗ 被取消时触发
        add_stability = -0.05
    }
    cancel_if_invalid = yes            # 条件失效时自动取消
    ai_will_do = { factor = 0 }       # AI 不会自动选（玩家决策）
}

# 可取消属性
cancelable = yes        # 可手动取消（默认）
cancelable = no         # 不可取消（内圈选择等）
```

---

## 民族精神

> 📄 **完整语法**: `references/ideas_syntax.md` | **注释示例**: `examples/02_ideas_annotated.md` | **导入详解**: `examples/08_importing_ideas_annotated.md`

### Ideas 类型

| 类型 | 槽位 | 说明 |
|------|------|------|
| `country` | 无限制 | 国家精神 |
| `army/navy/air` | 各1个 | 军种精神（需DLC） |
| `political_advisor` | 1个 | 政治顾问 |
| `theorist` | 1个 | 理论家 |
| `chief_of_staff/army_chief/navy_chief/air_chief` | 各1个 | 军事首脑 |

### 国家精神模板

```
ideas = {
    country = {
        {TAG}_spirit_name = {
            allowed = { original_tag = {TAG}  always = no }
            allowed_civil_war = { always = no }
            removal_cost = -1
            picture = generic_authoritarian_regime
            modifier = {
                political_power_gain = 0.10
                stability_factor = 0.05
            }
        }
    }
}
```

---

## 人物系统

> 📄 **注释示例**: `examples/06_characters_annotated.md`

### 角色类型

| 角色类型 | 说明 |
|----------|------|
| `country_leader` | 国家领导人 |
| `corps_commander` | 军级指挥官 |
| `field_marshal` | 陆军元帅 |
| `navy_leader` | 海军指挥官 |
| `advisor` | 顾问 |

### 完整人物定义

```
characters = {
    {TAG}_character = {
        name = "Character Name"
        portraits = {
            civilian = { large = "GFX_portrait_{TAG}_char" }
            army = { large = "GFX_portrait_{TAG}_char" }
        }
        country_leader = {
            ideology = despotism
            traits = { trait_name }
            expire = "1965.1.1.1"  id = -1
        }
        corps_commander = {
            traits = { cavalry_officer war_hero }
            skill = 2  attack_skill = 2  defense_skill = 2
            planning_skill = 2  logistics_skill = 1
        }
    }
}
```

---

## 领导人特质

> 📄 **注释示例**: `examples/07_leader_traits_annotated.md`

### 特质类型

| 类型 | 获得方式 |
|------|----------|
| `personality_trait` | 开局随机 |
| `status_trait` | 战斗获得 |
| `assignable_trait` | 手动分配 |
| `terrain_trait` | 地形战斗 |

### 特质定义模板

```
leader_traits = {
    trait_name = {
        type = land
        trait_type = personality_trait
        attack_skill = 1
        modifier = { planning_speed = 0.10 }
    }
}
```

---

## 本地化

> 📄 **详细指南**: `references/localisation_guide.md` | **注释示例**: `examples/04_localisation_annotated.md`

### YML 格式

```yaml
l_english:
 {TAG}_focus_name:0 "Focus Display Name"
 {TAG}_focus_name_desc:0 "Detailed description..."
```

### 编码：本地化文件必须 UTF-8 带 BOM + LF

> ⚠️ **AI 生成 .yml 本地化文件时必须遵守此格式，零例外：**
>
> | 属性 | 值 |
> |------|-----|
> | **编码** | UTF-8 with BOM（文件开头三个隐藏字节 `\xEF\xBB\xBF`） |
> | **换行符** | LF（`\n`，不是 CRLF `\r\n`） |
> | **文件路径示例** | `localisation/simp_chinese/{TAG}_l_simp_chinese.yml` |
>
> **为什么必须带 BOM**：Paradox Launcher 读取 .yml 本地化文件时依赖 BOM 识别 UTF-8。
> 无 BOM 的文件在游戏中直接显示为乱码，无法事后修复。
>
> **生成后自检命令**：
> ```powershell
> $bytes = [System.IO.File]::ReadAllBytes("path\to\file.yml")
> if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
>     Write-Host "✅ BOM 正确"
> } else {
>     Write-Host "❌ 缺少 BOM，请重新生成并确保编辑器保存为 UTF-8 with BOM"
> }
> ```
>
> **常见错误避坑**：
> - ❌ VSCode 保存为「UTF-8」（无 BOM）→ 游戏中文乱码
> - ❌ 记事本 / Notepad 保存为 ANSI/GBK → 中文完全无法显示
> - ❌ LF/CRLF 混用 → 部分游戏版本解析异常
> - ✅ 正确：VSCode 选「UTF-8 with BOM」，底部状态栏 CRLF 改为 LF

### 颜色与图标

```yaml
§R红色§!  §G绿色§!  §B蓝色§!  §Y黄色§!  §H高亮§!
£pol_power  £stability  £civilian_factory
```

---

## 事件

> 📄 **事件参考**: `references/events_guide.md` | **注释示例**: `examples/03_events_annotated.md`

### 国家事件模板

```
add_namespace = {TAG}_events

country_event = {
    id = {TAG}_events.1
    title = {TAG}_events.1_title
    desc = {TAG}_events.1_desc
    picture = generic_event
    is_triggered_only = yes
    
    option = {
        name = {TAG}_events.1_option_a
        add_political_power = 100
    }
}
```

---

## 决议

> 📄 **注释示例**: `examples/05_decisions_annotated.md`

### 决议模板

```
decisions = {
    {TAG}_category = {
        icon = GFX_goal_generic_major_alliance
        
        {TAG}_decision = {
            available = { tag = {TAG} }
            visible = { has_war_with = GER }
            cost = 50
            complete_effect = {
                transfer_state = { state = 123  target = ROOT }
            }
        }
    }
}
```

---

## 变量与动态修饰符

> 📄 **动态修饰符**: `references/dynamic_modifiers.md` | **脚本效果**: `references/scripted_effects.md` | **脚本触发器**: `references/scripted_triggers.md`

### 变量操作

```
set_variable = { var = {TAG}_var  value = 10 }
add_to_variable = { var = {TAG}_var  value = 5 }
subtract_from_variable = { var = {TAG}_var  value = 3 }
clamp_variable = { var = {TAG}_var  min = 0  max = 100 }
```

### 动态修饰符

```
add_dynamic_modifier = { modifier = {TAG}_modifier  days = 365 }
remove_dynamic_modifier = { modifier = {TAG}_old_modifier }
```

---

## 调试技巧

### 启用调试模式

Steam 启动选项加 `-debug`

### 控制台命令

```
debug_yesmen       # AI 总是接受
debug_events       # 显示事件 ID
tdebug             # 显示调试信息
error              # 打开错误日志
```

### 错误日志

```
Windows: C:\Users\<用户名>\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log
```

---

## 参考文档

### 语法参考

| 文件 | 内容 |
|------|------|
| `references/focus_complete_guide.md` | **国策树完整语法**（结构/字段/效果/内圈/连续焦点） |
| `references/focus_syntax_complete.md` | 国策树语法（含Joint/Shared/波兰示例） |
| `references/advanced_syntax.md` | 高级语法（备选图标/默认树/内圈窗口/快捷方式/嵌入窗口/连续焦点位置） |
| `references/syntax.md` | 形式化语法 + BNF + 11个常见陷阱 |
| `references/dictionary.md` | 效果/触发器语义字典（169效果 + 79触发器 + 作用域） |
| `references/ideas_syntax.md` | Ideas 完整语法 |
| `references/localisation_guide.md` | 本地化详细指南 |
| `references/events_guide.md` | 事件系统参考 |
| `references/dynamic_modifiers.md` | 动态修正完整语法 |
| `references/scripted_effects.md` | 脚本效果完整语法 |
| `references/scripted_triggers.md` | 脚本触发器完整语法 |

### 示例与模板

| 文件 | 内容 |
|------|------|
| `examples/09_focus_tree_design_guide.md` | **布局设计指南**（坐标/间距/视口/动态定位/真实架构/递进奖励/原版数据分析） |
| \examples/templates.md\ | **基础模板+经典子模块** 国策+民族精神+建筑效果+5个可组装子模块 |
| `examples/snippet_library.md` | 代码片段库 |
| `examples/01_focus_tree_annotated.md` | 国策树注释示例 |
| `examples/02_ideas_annotated.md` | 民族精神注释示例 |
| `examples/03_events_annotated.md` | 事件注释示例 |
| `examples/04_localisation_annotated.md` | 本地化注释示例 |
| `examples/05_decisions_annotated.md` | 决议注释示例 |
| `examples/06_characters_annotated.md` | 人物系统注释示例 |
| `examples/07_leader_traits_annotated.md` | 领导人特质注释示例 |
| `examples/08_importing_ideas_annotated.md` | Ideas 导入详解 |
| `examples/10_dynamic_modifiers_annotated.md` | 动态修饰符注释示例 |
| `examples/complete_mod_example.md` | 完整 mod 示例 |
| `examples/complete_tutorial.md` | 完整教程 |
| `examples/focus_real_examples.md` | 原版国策真实示例 |
| `examples/ideas_real_examples.md` | 原版精神真实示例 |
| `examples/events_real_examples.md` | 原版事件真实示例 |

### 原版参考

| 文件 | 内容 |
|------|------|
| `references/vanilla_focus_trees/` | **74个原版国策树文本** |
| `references/vanilla_focus_trees/README.md` | 原版国策树索引表 |
| `tools/validator.md` | 验证清单 |

### 官方参考

- Wiki: https://hoi4.paradoxwikis.com/Modding
- 本地文件: `Hearts of Iron IV/common/`

### 推荐工具

- VS Code + CWTools 扩展
- Notepad++
- WinMerge

---

**版本**: 7.2 | **更新**: 2026-04-26