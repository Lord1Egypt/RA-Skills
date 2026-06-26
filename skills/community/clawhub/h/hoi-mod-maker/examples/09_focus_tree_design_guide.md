# 国策树规划设计与布局指南

> **适用场景**：从零开始设计国策树布局，避免图标重合、连线混乱、视觉拥挤等问题。

---

## 目录

1. [坐标系统详解](#坐标系统详解)
2. [节点尺寸与间距](#节点尺寸与间距)
3. [布局规划方法论](#布局规划方法论)
4. [常见问题与解决方案](#常见问题与解决方案)
5. [实战案例](#实战案例)
6. [设计检查清单](#设计检查清单)
7. [视口与导航设计](#视口与导航设计)
8. [动态与条件定位](#动态与条件定位)
9. [真实游戏架构模式](#真实游戏架构模式)
10. [原版国策树数据分析与设计规范](#原版国策树数据分析与设计规范)

---

## 坐标系统详解

### 基础概念

```
y (纵向)
↑
│
│     ● → 国策节点位置 (x, y)
│
│        ● → x轴向右增加
│
└──────────→ x (横向)
```

**坐标系统特点**：
- **x轴**：横向位置，负值向左，正值向右
- **y轴**：纵向层级，向下递增（类似表格行号）
- **原点**：相对位置由 `relative_position_id` 决定
- **图标尺寸**：每个图标是**以坐标 (x,y) 为中心的2×2正方形**。左边界在 x-1，右边界在 x+1，上边界在 y+1，下边界在 y-1。左右相邻（同行）时 x 差必须 ≥ 2，否则重叠；上下相邻时 y 差 ≥ 1 即可。
- **单位**：逻辑单位，非像素（游戏引擎会自动缩放）

### 相对定位系统

```
focus = {
    id = base_focus        # 基准节点
    x = 0
    y = 0
}

focus = {
    id = child_focus
    relative_position_id = base_focus    # 相对于基准节点
    x = -1                                # 基准节点左侧1单位
    y = 1                                 # 下方1层级
}
```

**关键规则**：
- ❗ **y值必须递增**：子节点y值 > 父节点y值（至少+1）
- ✅ **x值可正可负**：负值向左，正值向右
- ✅ **使用 relative_position_id**：避免绝对坐标，便于重构

---

## 节点尺寸与间距

### 视觉空间占用

每个国策节点在视觉上占用一个"单元格"，包含：

```
┌─────────────────┐
│                 │  ← 上方间距
│    ┌─────┐     │
│    │图标 │      │  ← 图标区域 (约140x140像素)
│    └─────┘     │
│    标题文字     │  ← 名称区域
│                 │  ← 下方间距
└─────────────────┘
```

**推荐间距规则**：

| 场景 | x间距 | y间距 | 说明 |
|------|-------|-------|------|
| 紧密布局 | ±2 | +1 | 单分支直线（y+1即可，x必须≥2） |
| 标准布局 | ±3 | +1 | 多分支，避免连线交叉 |
| 宽松布局 | ±4~5 | +2 | 复杂树，视觉清晰 |
| 互斥节点 | ±1 | +1 | 互斥链紧邻排列 |

### 连线占用空间

国策之间的连线会占用额外的视觉空间：

```
       父节点
         │
         │ ← 连线需要清晰可见
         │
       子节点
```

**连线路径规则**：
- 直线连接：父节点中心 → 子节点中心
- 转折连接：自动计算最短路径
- 避免重叠：确保连线不穿过其他节点

---

## 布局规划方法论

### 步骤1：绘制草图（推荐工具）

**工具选择**：
- ✅ **纸张 + 铅笔**：最直观，快速迭代
- ✅ **Draw.io / Excalidraw**：在线协作，支持导出
- ✅ **Excel / Google Sheets**：网格对齐，易于调整
- ✅ **ASCII图**：快速原型，直接在注释中记录

**ASCII草图示例**：

```
          政治基础 (0,0)
             │
      ┌──────┴──────┐
   民主路线       威权路线
   (-2,1)        (2,1)
      │             │
   议会改革      权力集中
   (-2,2)        (2,2)
      │             │
   └─────┬──────────┘
         │
    工业基础 (0,3)
         │
   ┌─────┴─────┐
重工业      轻工业
(-1,4)      (1,4)
```

### 步骤2：确定树形结构类型

**常见树形结构**：

#### 1. 单一主干型

```
起始节点
    │
    ↓
    │
    ↓
终点节点
```

**适用场景**：线性历史进程、单一路线
**x范围**：0（单一x坐标）
**y间距**：+1（标准）

#### 2. 分叉-合并型

```
    基础节点
    ╱     ╲
分支A   分支B
    │       │
子节点   子节点
    ╲     ╱
    合并节点
```

**适用场景**：政治路线选择、工业分支
**x间距**：分支点x值±2~3
**y间距**：+1（分支内标准）

#### 3. 多起点并行型

```
政治线    工业线    军事线
  │         │         │
  ↓         ↓         ↓
  │         │         │
  ↓         ↓         ↓
```

**适用场景**：大国完整国策树、多功能区域
**x间距**：各起点间距≥5（避免视觉干扰）
**y间距**：各分支独立计算

#### 4. 互斥链型

```
选项A ↔ 选项B ↔ 选项C
  │
  ↓
 共同子节点
```

**适用场景**：意识形态选择、外交路线
**x间距**：±1（互斥节点紧邻）
**y间距**：互斥链+1，子节点再+1

### 步骤3：分配坐标（核心算法）

**算法原则**：

```
1. 确定基准节点（树根或主线起点）
   → 坐标 (0, 0)

2. 分配第一层子节点
   → y = 0 + 1 = 1
   → 根据分支数量分配x值：
      - 1个分支：x = 0
      - 2个分支：x = -2, x = 2
      - 3个分支：x = -4, x = 0, x = 4

3. 递归分配下层节点
   → y = 父节点y + 1
   → x = 父节点x + 相对偏移

4. 检查碰撞
   → 同一y层级的x值不能相同
   → 建议x值差距≥2（避免节点重叠）

5. 调整优化
   → 中心对齐主要分支
   → 平衡左右对称性
```

### 步骤4：编写代码（模板）

```
focus_tree = {
    id = TAG_focus
    
    country = {
        factor = 0
        modifier = { add = 10 tag = TAG }
    }
    
    # ========== 核心定位：树的视觉中心 ==========
    initial_show_position = { x = 500 y = 300 }
    
    # ========== 主干 ==========
    focus = {
        id = TAG_political_base
        icon = GFX_goal_generic_political_pressure
        x = 0      # 中心基准点
        y = 0      # 第0层
        cost = 5
        
        completion_reward = {
            add_political_power = 50
        }
    }
    
    # ========== 第一分支：民主路线 ==========
    focus = {
        id = TAG_democracy_path
        prerequisite = { focus = TAG_political_base }
        relative_position_id = TAG_political_base
        x = -2     # 左侧分支
        y = 1      # 第1层
        cost = 10
        
        mutually_exclusive = { focus = TAG_authority_path }
        
        completion_reward = {
            set_politics = {
                ruling_party = democratic
                elections_allowed = yes
            }
        }
    }
    
    # ========== 第一分支：威权路线 ==========
    focus = {
        id = TAG_authority_path
        prerequisite = { focus = TAG_political_base }
        relative_position_id = TAG_political_base
        x = 2      # 右侧分支
        y = 1      # 第1层
        cost = 10
        
        mutually_exclusive = { focus = TAG_democracy_path }
        
        completion_reward = {
            set_politics = {
                ruling_party = neutrality
                elections_allowed = no
            }
        }
    }
    
    # ========== 民主子节点 ==========
    focus = {
        id = TAG_parliament_reform
        prerequisite = { focus = TAG_democracy_path }
        relative_position_id = TAG_democracy_path
        x = 0      # 相对于父节点x=-2，实际x=-2
        y = 1      # 相对于父节点y=1，实际y=2
        cost = 10
        
        completion_reward = {
            add_political_power = 100
        }
    }
    
    # ========== 工业分支（独立起点）==========
    focus = {
        id = TAG_industrial_base
        icon = GFX_goal_generic_construct_civ_factory
        x = 10     # 远离政治分支，x=10
        y = 0      # 独立起点
        cost = 5
        
        completion_reward = {
            random_owned_controlled_state = {
                add_extra_state_shared_building_slots = 1
                add_building_construction = {
                    type = industrial_complex
                    level = 1
                    instant_build = yes
                }
            }
        }
    }
}
```

---

## 常见问题与解决方案

### 问题1：图标重叠

**症状**：
```
节点A和节点B在游戏中位置完全相同
```

**原因分析**：
- 相同的 `(x, y)` 坐标
- 错误的 `relative_position_id` 引用
- 未考虑 `relative_position_id` 的累积效应

**解决方案**：

```
# ❌ 错误示例：两个节点坐标相同
focus = {
    id = focus_A
    x = 0
    y = 0
}

focus = {
    id = focus_B
    x = 0      # ← 与focus_A相同的x值
    y = 0      # ← 与focus_A相同的y值
}

# ✅ 正确示例：确保唯一坐标
focus = {
    id = focus_A
    x = 0
    y = 0
}

focus = {
    id = focus_B
    x = 2      # ← 不同的x值
    y = 0      # 或 y = 1（不同层级）
}
```

**调试技巧**：
```
# 创建一个坐标检查表（CSV格式）
节点ID, 计算后x, 计算后y, 父节点
TAG_political_base, 0, 0, (根节点)
TAG_democracy_path, -2, 1, TAG_political_base
TAG_authority_path, 2, 1, TAG_political_base
TAG_parliament_reform, -2, 2, TAG_democracy_path

# 在Excel中按y排序，检查同一y值的x值是否重复
```

### 问题2：连线交叉混乱

**症状**：
```
政治分支的连线穿过了工业分支的节点
```

**原因分析**：
- 分支之间的x距离不足
- 节点排列顺序不合理
- 连线路径规划不当

**解决方案**：

```
# ❌ 错误示例：分支间距太小
政治分支 (x=0)
工业分支 (x=2)  ← 连线会交叉

# ✅ 正确示例：增大分支间距
政治分支 (x=0)
    ↓ 连线区域
工业分支 (x=10)  ← 充足的间距
```

**布局原则**：
- 主要分支之间x间距 ≥ 6
- 子分支之间x间距 ≥ 4
- 互斥链内部x间距 = 1（紧凑）

### 问题3：树形结构不平衡

**症状**：
```
左侧分支有10个节点，右侧分支只有3个节点
视觉上严重倾斜
```

**原因分析**：
- 未预先规划分支长度
- 直接编写代码，缺少草图设计
- 未考虑最终视觉效果

**解决方案**：

```
# 方法1：添加平衡节点
左侧长分支        右侧短分支 + 装饰性节点
    │                   │
    ↓                   ↓
    │               [小效果节点]
    ↓                   │
    │                   ↓
    │               [小效果节点]
    ↓                   │
[终点]              [终点]

# 方法2：调整横向布局
将短分支移到侧面，长分支居中

# 方法3：合并终点
两侧分支汇聚到共同终点，形成闭环
```

### 问题4：树太浅，缺乏战略深度

**症状**：
```
国策树只有2-3层深，玩家3-4个月就能点完主要国策
缺乏长期战略规划感
```

**原因分析**：
- 机械套用简单模板，没有根据主题扩展
- 只考虑"做什么"，没有考虑"怎么做"
- 缺少中间过程节点

**解决方案**：

```
# ❌ 错误示例：过于简单的链（仅2层）
TAG_industrial_expansion
  → TAG_military_production

# ✅ 正确示例：增加中间节点和分支选择（6层深度）
TAG_industrial_expansion (y=0)
  ├─ TAG_civilian_focus (y=1)        ← 分支选择
  │   → TAG_consumer_goods (y=2)
  │       → TAG_infrastructure (y=3)
  │           → TAG_total_economy (y=4)
  │               → TAG_war_economy (y=5)
  └─ TAG_military_focus (y=1)        ← 分支选择
      → TAG_arms_production (y=2)
          → TAG_industrial_efficiency (y=3)
              → TAG_heavy_industry (y=4)
                  → TAG_war_economy (y=5)  ← 汇聚

# 增加深度的技巧：
# 1. 添加"准备阶段"节点（动员→扩军→实战）
# 2. 添加"选择节点"（民用/军用二选一）
# 3. 添加"汇聚节点"（多条路径最终指向同一目标）
# 4. 添加"条件节点"（需要特定条件才能解锁）
```

**深度规划建议**：
- 政治路线：5-8层（改革→巩固→深化）
- 军事路线：6-10层（动员→扩军→实战→精锐）
- 工业路线：5-8层（基础→扩张→升级→总动员）
- 外交路线：4-7层（接触→谈判→结盟/吞并）

### 问题5：不同板块的国策发生碰撞

**症状**：
```
政治分支和工业分支的节点位置重叠或过于接近
不同主题的国策混在一起，视觉混乱
```

**原因分析**：
- 使用相对坐标时没有考虑整体布局
- 不同分支的根节点x坐标太接近
- 没有为不同板块预留足够的间距

**解决方案**：

```
# ❌ 错误示例：两个分支根节点太近
政治分支根节点 x=0
工业分支根节点 x=3  ← 距离太近，下层节点会碰撞

# ✅ 正确示例：不同板块根节点间隔 >= 6
政治分支根节点 x=0
  └─ 政治相关节点 (x范围: -4 到 +4)
      ↓ 间距 >= 6
工业分支根节点 x=10
  └─ 工业相关节点 (x范围: 6 到 +14)

# ✅ 更好的做法：用 initial_show_position 分开不同树
# 政治国策树 (focus_tree id = TAG_political_focus)
initial_show_position = { x = 500 y = 300 }

# 工业国策树 (focus_tree id = TAG_industrial_focus)  
initial_show_position = { x = 800 y = 300 }  ← 完全分开
```

**板块间距规则**：
- 同一 `focus_tree` 内不同分支：根节点 x 差 >= 6
- 不同 `focus_tree` 文件：使用不同的 `initial_show_position`
- 同一分支内的子节点：x 差 >= 2

### 问题6：孤立节点（不在树上的碎片）

**症状**：
```
某些国策节点没有连线连接到主树
玩家无法通过正常方式解锁这些国策
```

**原因分析**：
- 编写时遗漏了 prerequisite
- prerequisite 引用了不存在的节点
- 节点ID拼写错误导致连接失败

**解决方案**：

```
# ❌ 错误示例：孤立节点
focus = {
    id = TAG_special_operation
    x = 20
    y = 0
    cost = 10
    # 缺少 prerequisite！
}

# ✅ 正确示例：正确连接到主树
focus = {
    id = TAG_special_operation
    prerequisite = { focus = TAG_military_preparation }  ← 连接到主树
    relative_position_id = TAG_military_preparation
    x = 0
    y = 1
    cost = 10
}

# ✅ 检查方法：确保每个节点（除根节点外）都有 prerequisite
# 且 prerequisite 引用的节点在同一文件中存在
```

**完整性检查清单**：
1. 每个非根节点都有 `prerequisite`
2. 每个 `prerequisite` 引用的ID都在同一文件中定义
3. 所有节点形成连通图（从一个根节点可达所有节点）
4. 没有重复的节点ID

### 问题4：互斥链排列错误

**症状**：
```
三个互斥节点排成一排，但连线混乱
中间节点既连左边又连右边
```

**原因分析**：
- 未理解 `mutually_exclusive` 的视觉规则
- 错误的x坐标分配
- 缺少共同的父节点

**解决方案**：

```
# ✅ 标准互斥链布局
focus = {
    id = choice_base        # 共同父节点
    x = 0
    y = 0
}

focus = {
    id = choice_A
    prerequisite = { focus = choice_base }
    relative_position_id = choice_base
    x = -1
    y = 1
    mutually_exclusive = { focus = choice_B focus = choice_C }
}

focus = {
    id = choice_B
    prerequisite = { focus = choice_base }
    relative_position_id = choice_base
    x = 0
    y = 1
    mutually_exclusive = { focus = choice_A focus = choice_C }
}

focus = {
    id = choice_C
    prerequisite = { focus = choice_base }
    relative_position_id = choice_base
    x = 1
    y = 1
    mutually_exclusive = { focus = choice_A focus = choice_B }
}

视觉布局：
      choice_base
       ╱  │  ╲
   A(左) B(中) C(右)
      └──┴──┘
      互斥连接
```

---

## 实战案例

### 案例1：标准政治三分支

**需求**：民主、共产、法西斯三条路线，起点相同

**草图设计**：

```
        国家基石 (0,0)
         ╱│╲
    ┌───┼───┐
民主(左) 共产(中) 法西斯(右)
(-3,1)   (0,1)    (3,1)
    │       │       │
改革A   革命B   夺权C
(-3,2)   (0,2)    (3,2)
    │       │       │
    └───┬───┴───┬───┘
        │       │
    统一国家(中心)
      (-1,3) (1,3)
        └───┬───┘
            │
        工业复兴 (0,4)
```

**代码实现**：

```
focus_tree = {
    id = TAG_political_focus
    
    country = {
        factor = 0
        modifier = { add = 10 tag = TAG }
    }
    
    initial_show_position = { x = 500 y = 300 }
    
    # ========== 根节点 ==========
    focus = {
        id = TAG_national_foundation
        icon = GFX_goal_generic_construct_civ_factory
        x = 0
        y = 0
        cost = 5
    }
    
    # ========== 三条路线 ==========
    focus = {
        id = TAG_democracy_route
        prerequisite = { focus = TAG_national_foundation }
        relative_position_id = TAG_national_foundation
        x = -3
        y = 1
        cost = 10
        
        mutually_exclusive = { 
            focus = TAG_communism_route 
            focus = TAG_fascism_route 
        }
    }
    
    focus = {
        id = TAG_communism_route
        prerequisite = { focus = TAG_national_foundation }
        relative_position_id = TAG_national_foundation
        x = 0
        y = 1
        cost = 10
        
        mutually_exclusive = { 
            focus = TAG_democracy_route 
            focus = TAG_fascism_route 
        }
    }
    
    focus = {
        id = TAG_fascism_route
        prerequisite = { focus = TAG_national_foundation }
        relative_position_id = TAG_national_foundation
        x = 3
        y = 1
        cost = 10
        
        mutually_exclusive = { 
            focus = TAG_democracy_route 
            focus = TAG_communism_route 
        }
    }
    
    # ========== 各路线子节点 ==========
    focus = {
        id = TAG_democracy_reform
        prerequisite = { focus = TAG_democracy_route }
        relative_position_id = TAG_democracy_route
        x = 0
        y = 1
        cost = 10
    }
    
    focus = {
        id = TAG_communism_revolution
        prerequisite = { focus = TAG_communism_route }
        relative_position_id = TAG_communism_route
        x = 0
        y = 1
        cost = 10
    }
    
    focus = {
        id = TAG_fascism_seize_power
        prerequisite = { focus = TAG_fascism_route }
        relative_position_id = TAG_fascism_route
        x = 0
        y = 1
        cost = 10
    }
    
    # ========== 合并节点（双父节点）==========
    focus = {
        id = TAG_unified_left
        prerequisite = { 
            focus = TAG_democracy_reform 
            focus = TAG_communism_revolution 
        }
        relative_position_id = TAG_democracy_reform
        x = 2
        y = 1
        cost = 10
    }
    
    focus = {
        id = TAG_unified_right
        prerequisite = { 
            focus = TAG_communism_revolution 
            focus = TAG_fascism_seize_power 
        }
        relative_position_id = TAG_communism_revolution
        x = 1
        y = 1
        cost = 10
    }
    
    # ========== 最终合并 ==========
    focus = {
        id = TAG_industrial_revival
        prerequisite = { 
            focus = TAG_unified_left 
            focus = TAG_unified_right 
        }
        relative_position_id = TAG_unified_left
        x = 1
        y = 1
        cost = 15
    }
}
```

### 案例2：复杂工业分支（多层分叉）

**需求**：重工业、轻工业两条主线，各有子分支

**布局规划**：

```
工业基础 (0,0)
    │
工业扩张 (0,1)
    │
    └─────────┬─────────┐
    重工业(-3,2)    轻工业(3,2)
        │              │
    ┌───┴───┐      ┌───┴───┐
钢铁(-4,3) 煤炭(-2,3) 纺织(2,3) 食品(4,3)
    │       │       │       │
    └───┬───┘       └───┬───┘
        │               │
    基础设施(-1,4)  消费品(1,4)
            └───────┬───────┘
                    │
            经济繁荣 (0,5)
```

**关键代码片段**：

```
# ========== 重工业子分支 ==========
focus = {
    id = TAG_heavy_industry
    prerequisite = { focus = TAG_industrial_expansion }
    relative_position_id = TAG_industrial_expansion
    x = -3
    y = 1
    cost = 10
}

focus = {
    id = TAG_steel_production
    prerequisite = { focus = TAG_heavy_industry }
    relative_position_id = TAG_heavy_industry
    x = -1    # 相对于父节点，实际x = -4
    y = 1     # 实际y = 3
    cost = 10
}

focus = {
    id = TAG_coal_mining
    prerequisite = { focus = TAG_heavy_industry }
    relative_position_id = TAG_heavy_industry
    x = 1     # 实际x = -2
    y = 1     # 实际y = 3
    cost = 10
}

# ========== 重工业合并 ==========
focus = {
    id = TAG_infrastructure_development
    prerequisite = { 
        focus = TAG_steel_production 
        focus = TAG_coal_mining 
    }
    relative_position_id = TAG_steel_production
    x = 3     # 实际x = -1（居中）
    y = 1     # 实际y = 4
    cost = 10
}
```

---

## 设计检查清单

### 视觉检查项

- [ ] **坐标唯一性**：所有节点的 `(x, y)` 组合唯一
- [ ] **y值递增**：子节点y值 > 父节点y值
- [ ] **分支间距**：主要分支x间距 ≥ 6
- [ ] **子分支间距**：次要分支x间距 ≥ 4
- [ ] **互斥链紧凑**：互斥节点x间距 = 1
- [ ] **连线清晰**：无连线穿过其他节点
- [ ] **中心对齐**：主干或合并节点在视觉中心

### 功能检查项

- [ ] **前置关系**：所有 `prerequisite` 引用的节点在当前文件中存在（不得引用不存在的ID，不得使用其他国家的ID）
- [ ] **互斥关系**：`mutually_exclusive` 双向绑定
- [ ] **定位引用**：`relative_position_id` 引用的节点存在
- [ ] **权重值**：`cost` 值合理（通常5-15）
- [ ] **图标存在**：`icon` 引用的GFX定义存在

### 代码质量检查项

- [ ] **ID唯一**：所有 `id` 在文件内唯一
- [ ] **命名规范**：`TAG_category_subcategory` 格式
- [ ] **缩进一致**：统一使用制表符或空格
- [ ] **注释清晰**：关键布局节点有注释说明
- [ ] **编码正确**：UTF-8 无 BOM

---

## 进阶技巧

### 技巧1：使用相对坐标的累积计算

**问题**：多层嵌套的 `relative_position_id` 如何计算最终坐标？

**方法**：

```
# 递归计算公式
最终坐标 = Σ(各层relative_position_id的坐标) + 当前节点坐标

示例：
根节点: (0, 0)
  └─ 子节点A: relative_position_id=根, x=-2, y=1
       最终坐标 = (0,0) + (-2,1) = (-2, 1)
       
       └─ 孙节点B: relative_position_id=子节点A, x=0, y=1
              最终坐标 = (0,0) + (-2,1) + (0,1) = (-2, 2)
```

**自动化工具建议**：
- 使用Excel/Sheets创建坐标计算表
- 用公式自动计算累积坐标
- 排序检查重复坐标

### 技巧2：利用 offset 实现条件偏移

**场景**：某个节点在特定条件下需要调整位置

```
focus = {
    id = TAG_conditional_position
    
    # 基础位置
    x = 0
    y = 1
    
    # 条件偏移：如果已完成某国策，向右移动
    offset = {
        if = {
            limit = { has_completed_focus = TAG_other_focus }
            x = 2    # 向右偏移2单位
        }
    }
}
```

### 技巧3：大型树的模块化设计

**策略**：将大型国策树拆分为多个逻辑块

```
# ========== 政治模块 (x: -15 ~ -5) ==========
# 所有政治相关节点x值在-15到-5之间

# ========== 工业模块 (x: -5 ~ 5) ==========
# 所有工业相关节点x值在-5到5之间

# ========== 军事模块 (x: 5 ~ 15) ==========
# 所有军事相关节点x值在5到15之间
```

**优势**：
- 各模块独立开发和测试
- 减少模块间的坐标冲突
- 便于后期扩展和维护

---

## 参考资源

### 游戏内调试

- **调试模式**：启动游戏时添加 `-debug` 参数
- **日志文件**：`logs/error.log` 检查坐标错误
- **视觉检查**：在国策树界面缩放查看全貌

### 外部工具

- **HOI4 Modding Tool**：可视化国策树编辑器
- **Focus Tree Manager**：在线布局规划工具
- **Draw.io**：通用流程图绘制，可导出为图片参考

---

**总结**：国策树布局设计需要"先规划，后编码"。使用草图明确结构，遵循坐标规则，定期检查碰撞，最终实现清晰美观的视觉效果。


---

## 视口与导航设计

> 焦点树不仅是节点的集合，更是玩家的**浏览体验**。视口与导航决定了玩家打开国策界面时看到什么、能多快找到想要的分支。

### initial_show_position — 初始视口定位

当玩家打开国策界面时，游戏需要知道把"镜头"对准哪里。这就是 `initial_show_position` 的作用。

**语法有两种模式**：

```
# 模式1：绝对坐标定位（推荐新手使用）
initial_show_position = {
    x = 500
    y = 300
}

# 模式2：焦点锚点定位（推荐有经验的制作者）
initial_show_position = {
    focus = GER_rearmament
}
```

**模式1 — 绝对坐标**：
- `(x, y)` 是**视口中心**在树坐标系中的位置
- 单位与焦点节点的坐标单位相同
- 设置为树的整体视觉中心即可
- **缺点**：树扩展后需要手动调整

**模式2 — 焦点锚点**：
- 自动将视口中心对准指定焦点
- 该焦点会出现在屏幕正中央
- **优点**：树结构变化后无需调整，自动跟随
- **推荐用法**：锚定到树的第一个焦点或政治路线起点

```
# 推荐模式2的理由：
# 当你后期在树的上方添加新节点时，
# 模式1的坐标偏移会导致视口不再居中，
# 模式2则自动对准正确的焦点。

initial_show_position = {
    focus = TAG_first_focus    # 永远指向第一个政治焦点
}
```

**设计原则**：
- 初始视口应展示树的**起始区域**（通常是政治路线的根节点）
- 确保起始焦点周围有足够的上下文（至少能看到第一层分支）
- 不要将视口对准树的边缘或空白区域

### shortcut — 快捷导航按钮

快捷方式在国策界面底部显示为按钮，点击后视口会平滑滚动到指定焦点并自动缩放。

**语法**：

```
shortcut = {
    name = GER_historical_path_shortcut    # 本地化键（按钮文本）
    target = GER_remilitarize_the_rhineland  # 目标焦点ID
    scroll_wheel_factor = 0.469             # 缩放因子（可选）
    trigger = { always = yes }              # 显示条件（可选）
}
```

**各字段详解**：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 本地化键，按钮显示的文本 |
| `target` | ✅ | 视口跳转到的焦点ID |
| `scroll_wheel_factor` | ❌ | 缩放级别。值越小缩放越远（看到更多节点），值越大缩放越近（聚焦细节）。默认值通常在 0.4-0.8 之间 |
| `trigger` | ❌ | 按钮显示条件，不满足时隐藏该按钮 |

**设计方法论**：

```
# 什么时候需要快捷方式？
# 规则：如果玩家从树的起始位置需要超过3秒才能滚动到某个分支，
#       就应该为该分支添加快捷方式。

# 常见的快捷方式分配：
shortcut = {
    name = TAG_political_path          # 政治路线
    target = TAG_political_base
    scroll_wheel_factor = 0.7          # 稍微放大，看清焦点细节
}

shortcut = {
    name = TAG_industrial_path         # 工业路线
    target = TAG_industrial_base
    scroll_wheel_factor = 0.75
}

shortcut = {
    name = TAG_military_path           # 军事路线
    target = TAG_military_base
    scroll_wheel_factor = 0.75
}
```

**条件快捷方式**（同一槽位根据条件显示不同目标）：

```
# 德国示例：根据DLC显示不同的"反对希特勒"入口
shortcut = {
    name = GER_oppose_hitler_shortcut
    target = GER_oppose_hitler           # 基础版本
    scroll_wheel_factor = 0.55
    trigger = {
        NOT = { has_dlc = "Gotterdammerung" }
    }
}

shortcut = {
    name = GER_oppose_hitler_shortcut    # 同一个name！
    target = GER_oppose_hitler_ww        # DLC版本
    scroll_wheel_factor = 0.485
    trigger = {
        has_dlc = "Gotterdammerung"      # DLC启用时覆盖上面的
    }
}
```

> **注意**：使用相同的 `name` 但不同的 `trigger` 时，同一时间只有一个按钮可见。这是实现条件性导航入口的标准做法。

**scroll_wheel_factor 选择指南**：

| 值 | 视野范围 | 适用场景 |
|----|----------|---------|
| 0.3-0.4 | 极广（鸟瞰整棵树） | 超大树的概览按钮 |
| 0.5-0.6 | 广（看清区域结构） | 主要分支入口 |
| 0.7-0.8 | 中（看清焦点细节） | 小型分支入口 |
| 0.9-1.0 | 近（聚焦单个焦点） | 特殊焦点（连续焦点等） |

### continuous_focus_position — 连续焦点定位

连续焦点（Continuous Focus）是完成10个常规焦点后解锁的特殊焦点，显示在树的一个固定位置。

**语法**：

```
focus_tree = {
    id = TAG_focus
    
    # 连续焦点的显示位置
    continuous_focus_position = { x = 500 y = 1300 }
}
```

**设计原则**：
- 连续焦点应放在树的**下方或侧面**，与常规焦点区域分离
- y值应大于所有常规焦点的最大y值（确保不会重叠）
- x值可以与常规焦点的视觉中心对齐

**布局建议**：

```
# 典型布局：连续焦点在树的下方中央

# 常规焦点区域        y = 0 ~ 20
#     │
#     ↓
# （空白间隔）          y = 20 ~ 25
#     │
#     ↓
# 连续焦点区域        y = 25+

continuous_focus_position = { x = 0 y = 25 }    # x与树中心对齐
```

### inlay_window — 嵌入窗口（内圈焦点）

嵌入窗口用于创建特殊的显示区域，最典型的是德国的内圈焦点系统。

**语法**：

```
focus_tree = {
    id = german_focus
    
    # 定义嵌入窗口的位置和尺寸
    inlay_window = {
        id = ger_inner_circle_inlay_window
        position = { x = 4500 y = 1150 }
        size = { width = 400 height = 300 }     # 可选
    }
}
```

**内圈焦点语法**：

```
focus = {
    id = GER_inner_circle_focus_1
    
    inner_circle = yes          # 标记为内圈焦点
    cost = 20                   # 内圈焦点通常cost较低
    
    icon = GFX_focus_ger_inner_circle
    x = 1
    y = 0
    relative_position_id = GER_rearmament    # 相对于中心焦点
    
    completion_reward = { ... }
}
```

**设计要点**：
- `inner_circle = yes` 是关键标记，没有它焦点不会出现在嵌入窗口中
- 内圈焦点的坐标是**相对于嵌入窗口中心焦点**的偏移
- 内圈焦点通常围绕一个中心焦点呈环形或辐射状排列
- cost建议使用常量定义：

```
@inner_circle_time_tier_1 = 20    # 140天
@inner_circle_time_tier_2 = 20    # 140天
@inner_circle_time_tier_3 = 40    # 280天
```

### 完整的视口设计模板

```
focus_tree = {
    id = TAG_focus
    
    country = {
        factor = 0
        modifier = { add = 10 tag = TAG }
    }
    
    # === 视口定位 ===
    initial_show_position = {        # 打开国策界面时的初始位置
        focus = TAG_first_focus      # 锚定到起始焦点
    }
    
    # === 快捷导航 ===
    shortcut = {
        name = TAG_political_shortcut
        target = TAG_political_base
        scroll_wheel_factor = 0.7
    }
    
    shortcut = {
        name = TAG_industrial_shortcut
        target = TAG_industrial_base
        scroll_wheel_factor = 0.75
    }
    
    shortcut = {
        name = TAG_military_shortcut
        target = TAG_military_base
        scroll_wheel_factor = 0.75
    }
    
    # === 连续焦点位置 ===
    continuous_focus_position = { x = 0 y = 25 }
    
    # === 嵌入窗口（如有内圈焦点）===
    # inlay_window = {
    #     id = TAG_inner_circle_window
    #     position = { x = 4500 y = 1150 }
    # }
    
    # === 焦点定义从这里开始 ===
    focus = { ... }
}
```

### 视口设计检查清单

- [ ] `initial_show_position` 锚定到树的起始焦点（推荐模式2）
- [ ] 初始视口能展示第一层分支（玩家能看到选择）
- [ ] 主要分支都有对应的快捷方式按钮
- [ ] 条件分支使用相同 name + 不同 trigger 的模式
- [ ] `scroll_wheel_factor` 值与分支大小匹配
- [ ] `continuous_focus_position` 与常规焦点区域不重叠
- [ ] 快捷方式的本地化文本已添加到 .yml 文件


---

## 动态与条件定位

> 传统布局中，每个焦点的坐标是固定的。但 HOI4 的国策树支持条件驱动的位置偏移，让焦点可以根据游戏状态"移动"到不同位置。这是实现高级布局模式的关键技术。

### offset — 条件偏移

`offset` 是最常用的动态定位机制。它根据条件对焦点的基础坐标施加额外的偏移量。

**基础语法**：

```
focus = {
    id = TAG_conditional_position
    
    # 基础位置
    x = 0
    y = 1
    
    # 条件偏移：满足条件时，在基础位置上额外偏移
    offset = {
        if = {
            limit = { has_completed_focus = TAG_other_focus }
            x = 2    # 向右偏移2个单位
        }
    }
}
```

**计算规则**：
```
最终位置 = 基础坐标 (x, y) + offset 产生的偏移量

上例中：
- 条件不满足：最终位置 = (0, 1)
- 条件满足：最终位置 = (0+2, 1) = (2, 1)
```

### 多条件偏移（链式 if-else）

当一个焦点需要在多种条件下处于不同位置时，使用 `if-else` 链：

```
focus = {
    id = TAG_dynamic_focus
    
    x = 0
    y = 2
    
    offset = {
        if = {
            limit = { has_government = fascism }
            x = -4       # 法西斯路线时偏左
        }
        else_if = {
            limit = { has_government = communism }
            x = 4        # 共产路线时偏右
        }
        else = {
            x = 0        # 默认不偏移
        }
    }
}
```

**注意**：`else_if` 和 `else` 与 HOI4 脚本的标准条件语法一致。

### 纵向偏移

`offset` 也支持 y 轴偏移：

```
focus = {
    id = TAG_late_game_focus
    
    x = 0
    y = 3
    
    offset = {
        if = {
            limit = { has_completed_focus = TAG_early_war }
            y = 2    # 早期开战时，将焦点下移2行（延后视觉位置）
        }
    }
}
```

### xy 同时偏移

```
offset = {
    if = {
        limit = { has_completed_focus = TAG_alternate_start }
        x = -3       # 向左移3
        y = 1        # 向下移1
    }
}
```

### offset 的典型应用场景

#### 场景1：分支折叠 — 隐藏分支变为可见时腾出空间

当一条分支的焦点有 `visible` 条件时，未满足条件的焦点不显示。但它们**仍然占据空间**（防止布局跳动）。当条件满足后，其他焦点可能需要移位来为"新出现的"分支腾出空间。

```
# 场景：有两条路线A和B，路线B默认隐藏
# 当路线B出现时，路线A的子焦点需要向左偏移

# 路线B的起始焦点（条件可见）
focus = {
    id = TAG_route_B_start
    visible = {
        has_completed_focus = TAG_unlock_B    # 完成某焦点后才显示
    }
    x = 0
    y = 1
}

# 路线A的子焦点（条件偏移）
focus = {
    id = TAG_route_A_child
    
    x = -2       # 基础位置
    y = 2
    
    # 当路线B可见时，进一步左移避免重叠
    offset = {
        if = {
            limit = { has_completed_focus = TAG_unlock_B }
            x = -3    # 从x=-2移到x=-5
        }
    }
}
```

#### 场景2：根据已选路线重新排列后续焦点

```
# 选择了不同政治路线后，后续焦点移到对应路线的"领地"

focus = {
    id = TAG_economic_focus
    
    x = 0
    y = 4
    
    offset = {
        if = {
            limit = { has_completed_focus = TAG_democracy_path }
            x = -6       # 民主区域
        }
        else_if = {
            limit = { has_completed_focus = TAG_fascism_path }
            x = 6        # 法西斯区域
        }
        else = {
            x = 0        # 中立位置
        }
    }
}
```

#### 场景3：联合焦点的空间适配

```
# Joint Focus 完成后，后续焦点在视觉上"归队"到主分支

focus = {
    id = TAG_post_joint_focus
    
    x = 0
    y = 6
    
    offset = {
        if = {
            limit = {
                has_completed_focus = TAG_joint_focus
                is_faction_leader = yes
            }
            x = 2    # 阵营领袖的焦点右移
        }
    }
}
```

### visible — 条件可见性

`visible` 控制焦点是否在树上**显示**。与 `available`（灰色不可选但可见）不同，`visible = no` 的焦点完全不出现。

**语法**：

```
focus = {
    id = TAG_hidden_branch
    
    visible = {
        # 满足条件时才显示
        has_completed_focus = TAG_unlock_branch
    }
    
    x = 0
    y = 3
    
    completion_reward = { ... }
}

# 更复杂的条件
focus = {
    id = TAG_war_branch
    
    visible = {
        OR = {
            has_war_with = GER
            has_war_with = SOV
            is_at_war = yes
        }
    }
    
    x = 5
    y = 2
}
```

**visible 与 available 的区别**：

| 属性 | 效果 | 视觉表现 | 适用场景 |
|------|------|---------|---------|
| `visible = no` | 焦点不存在 | 完全不显示 | 备用路线、DLC内容、隐藏分支 |
| `available = no` | 焦点存在但不可选 | 灰色显示，tooltip提示条件 | 需要前置条件、时间锁、政治条件 |

**设计原则**：
- 用 `visible` 控制**分支的显示/隐藏**（结构性变化）
- 用 `available` 控制**单个焦点的可选择性**（功能性限制）
- 不要滥用 `visible`——频繁的出现/消失会影响玩家的空间认知

### 条件布局的空间预留

当使用 `visible` 隐藏分支时，有一个重要的设计决策：**隐藏的焦点是否仍然占据空间？**

**HOI4 的行为**：`visible` 条件不满足时，焦点不渲染、不占空间。这意味着当分支出现时，周围的焦点不会自动移位——它们仍然在原位。这可能导致新出现的焦点与已有焦点**重叠**。

**解决方案**：使用 `offset` 联动

```
# === 被隐藏的分支 ===
focus = {
    id = TAG_alternate_route_start
    visible = { has_completed_focus = TAG_unlock_alt }
    x = 0
    y = 2
}

focus = {
    id = TAG_alternate_route_child
    prerequisite = { focus = TAG_alternate_route_start }
    relative_position_id = TAG_alternate_route_start
    x = 0
    y = 1
    visible = { has_completed_focus = TAG_unlock_alt }
}

# === 已有的主线焦点（需要条件偏移）===
focus = {
    id = TAG_main_route_child
    prerequisite = { focus = TAG_main_route_parent }
    relative_position_id = TAG_main_route_parent
    x = 0
    y = 2
    
    # 当备用分支出现时，向右移位避免重叠
    offset = {
        if = {
            limit = { has_completed_focus = TAG_unlock_alt }
            x = 3
        }
    }
}
```

### 条件布局的设计模式

#### 模式1：平行替换（In-place Swap）

两条互斥路线共享同一空间，通过 `visible` 和 `offset` 实现切换：

```
# 位置A（条件1）
focus = {
    id = TAG_option_A
    visible = { has_government = democracy }
    x = 0
    y = 3
}

# 位置A（条件2）—— 与A完全重叠，但不会同时显示
focus = {
    id = TAG_option_B
    visible = { has_government = fascism }
    x = 0
    y = 3
}
```

> **优势**：空间利用率高，不浪费坐标空间
> **劣势**：玩家切换路线后"看到"的是不同内容，可能困惑

#### 模式2：渐进展开（Progressive Reveal）

分支随游戏进程逐步出现，新内容出现在已有内容的**外围**（不产生重叠）：

```
# 第一阶段（始终可见）
focus = {
    id = TAG_stage_1
    x = 0
    y = 0
}

# 第二阶段（条件后出现，在已有内容的右侧）
focus = {
    id = TAG_stage_2
    visible = { has_completed_focus = TAG_stage_1 }
    x = 5     # 预留了足够的空间
    y = 0
}

# 第三阶段（进一步条件后出现，在更右侧）
focus = {
    id = TAG_stage_3
    visible = { has_completed_focus = TAG_stage_2 }
    x = 10    # 继续向右扩展
    y = 0
}
```

> **优势**：绝不会重叠，玩家感知到树在"生长"
> **劣势**：x值可能变得非常大

#### 模式3：扇形展开（Fan-out）

从一个中心点根据条件向不同方向展开：

```
# 中心锚点（始终可见）
focus = {
    id = TAG_hub
    x = 0
    y = 5
}

# 条件分支1：向左展开
focus = {
    id = TAG_branch_left
    visible = { has_completed_focus = TAG_condition_A }
    relative_position_id = TAG_hub
    x = -5
    y = 1
}

# 条件分支2：向右展开
focus = {
    id = TAG_branch_right
    visible = { has_completed_focus = TAG_condition_B }
    relative_position_id = TAG_hub
    x = 5
    y = 1
}

# 条件分支3：向下展开
focus = {
    id = TAG_branch_down
    visible = { has_completed_focus = TAG_condition_C }
    relative_position_id = TAG_hub
    x = 0
    y = 2
}
```

### 条件布局的常见陷阱

#### 陷阱1：offset 导致连线跳跃

**问题**：当 `offset` 条件在游戏过程中改变时，焦点位置突然跳到远处，导致连线变得很长或穿过其他焦点。

**解决方案**：
- 保持 `offset` 的偏移量较小（≤3个单位）
- 使用 `offset` 的焦点不应有基于绝对位置的子节点
- 被偏移的焦点的子节点应使用 `relative_position_id`（自动跟随）

#### 陷阱2：visible 的"幽灵连线"

**问题**：一个焦点有 `visible` 条件，但它的父节点（prerequisite）是始终可见的。当子节点不可见时，父节点看起来没有后续焦点；当子节点突然出现时，连线凭空出现。

**解决方案**：
- 确保 `visible` 分支有足够的叙事上下文（如"完成XX焦点解锁新路线"的提示）
- 或者让父节点也有条件：`available` 提示"此路线将在满足XX条件后解锁"

#### 陷阱3：多层 offset 累积导致坐标爆炸

**问题**：一个焦点的 `relative_position_id` 指向一个使用了 `offset` 的父节点，导致子节点的最终位置超出预期。

```
# 父节点（有offset）
父基础位置 = (0, 2)，offset = (+3, 0)
父最终位置 = (3, 2)

# 子节点（相对定位，无offset）
子 relative_position_id = 父
子 x = 0, y = 1
子最终位置 = (3+0, 2+1) = (3, 3)    # 自动跟随父的offset
```

> **结论**：`relative_position_id` 的子节点会**自动继承**父节点的 offset。这是正确的行为，不需要手动处理。但如果你不想要这个继承，应避免使用 `relative_position_id`，改用绝对坐标。

### 动态定位决策树

```
你的焦点需要根据条件改变位置吗？
├── 否 → 使用固定坐标即可
└── 是
    ├── 需要在多个位置间切换吗？
    │   ├── 是 → offset + if/else_if/else 链
    │   └── 否（只需偏移一次）→ offset + 单个 if
    ├── 需要完全不显示吗？
    │   ├── 是 → visible 条件（注意空间预留）
    │   └── 否（灰色不可选即可）→ available 条件
    ├── 有子节点需要跟随移动吗？
    │   ├── 是 → 子节点使用 relative_position_id（自动跟随）
    │   └── 否 → 子节点使用绝对坐标（不受影响）
    └── 是否需要与可见性联动？
        └── 是 → visible + offset 配合使用
```

### 条件定位检查清单

- [ ] `offset` 的偏移量 ≤3（避免大跳跃）
- [ ] `offset` 条件变化不会导致与固定位置焦点重叠
- [ ] 使用 `relative_position_id` 的子节点能正确跟随父节点的 `offset`
- [ ] `visible` 分支出现/消失不会产生视觉重叠（检查了所有可能的组合）
- [ ] 多条件 `offset` 链有 `else` 分支（确保始终有明确的最终位置）
- [ ] `visible` 的解锁条件对玩家有清晰的提示


---

## 真实游戏架构模式

> 学习 HOI4 原版国策树的架构模式，是掌握高级布局的最佳途径。本节剖析5种经典模式，每种都包含完整代码骨架和设计要点。

### 模式一：内圈焦点（Inner Circle）— 以德国为蓝本

**概念**：内圈焦点围绕一个中心焦点呈环形排列，形成视觉上的"圆环"。这是德国国策树的核心设计——4条意识形态路线围绕中央历史焦点旋转。

**结构示意**：

```
                [民主路线起点]
                     |
[法西斯路线起点] ── [中心焦点] ── [中立路线起点]
                     |
                [共产路线起点]
```

**完整代码骨架**：

```
focus_tree = {
    id = german_focus

    country = {
        factor = 0
        modifier = {
            add = 10
            tag = GER
        }
    }

    default = no
    reset_on_civilwar = no

    # === 视口设置 ===
    initial_show_position = {
        x = 14
        y = 9
    }

    # === 中心焦点 ===
    focus = {
        id = GER_center
        icon = GFX_goal_generic_national_unity
        x = 14
        y = 10
        cost = 0
        ai_will_do = { factor = 0 }

        completion_reward = {
            add_political_power = 50
        }
    }

    # === 内圈焦点（4个方向）===

    # 上：民主路线起点
    focus = {
        id = GER_democracy_start
        icon = GFX_goal_generic_democratic_drift
        inner_circle = yes
        x = 14
        y = 9
        cost = 10
        prerequisite = { focus = GER_center }

        available = {
            has_government = democracy
            NOT = { has_government = fascism }
        }

        completion_reward = {
            add_popularity = {
                ideology = democracy
                popularity = 0.05
            }
        }
    }

    # 右：中立路线起点
    focus = {
        id = GER_neutrality_start
        icon = GFX_goal_generic_neutrality_focus
        inner_circle = yes
        x = 15
        y = 10
        cost = 10
        prerequisite = { focus = GER_center }

        available = {
            has_government = neutrality
        }

        completion_reward = {
            add_popularity = {
                ideology = neutrality
                popularity = 0.05
            }
        }
    }

    # 下：共产路线起点
    focus = {
        id = GER_communism_start
        icon = GFX_goal_generic_communism_drift
        inner_circle = yes
        x = 14
        y = 11
        cost = 10
        prerequisite = { focus = GER_center }

        available = {
            has_government = communism
        }

        completion_reward = {
            add_popularity = {
                ideology = communism
                popularity = 0.05
            }
        }
    }

    # 左：法西斯路线起点
    focus = {
        id = GER_fascism_start
        icon = GFX_goal_generic_fascism_drift
        inner_circle = yes
        x = 13
        y = 10
        cost = 10
        prerequisite = { focus = GER_center }

        available = {
            has_government = fascism
        }

        completion_reward = {
            add_popularity = {
                ideology = fascism
                popularity = 0.05
            }
        }
    }
}
```

**内圈布局关键参数**：

| 元素 | 推荐值 | 说明 |
|------|--------|------|
| 中心焦点与内圈间距 | 1格 | 标准环形紧凑布局 |
| 内圈焦点数量 | 2-4个 | 超过4个建议用扇形替代 |
| 内圈焦点cost | 10 | 通常与意识形态绑定 |
| 中心焦点cost | 0 | 作为免费锚点使用 |
| `inner_circle = yes` | 必须 | 启用内圈渲染样式 |

**设计要点**：
- 中心焦点设为 `cost = 0`，充当免费视觉锚点
- 内圈焦点标记 `inner_circle = yes` 以启用特殊渲染
- 内圈焦点通常绑定意识形态的 `available` 条件
- 从内圈焦点向外延伸的路线使用正常布局

### 模式二：条件分支网络 — 以日本为蓝本

**概念**：日本国策树是条件分支的教科书——多个焦点通过 `available` 和 `visible` 互锁，形成"选择一条路，其他路关闭"的网络。

**核心结构**：

```
[军国路线] ──┐
             ├── [共同前提] ── [后续分支]
[民主路线] ──┘
```

**完整代码骨架**：

```
focus_tree = {
    id = japanese_focus

    country = {
        factor = 0
        modifier = {
            add = 10
            tag = JAP
        }
    }

    default = no

    initial_show_position = {
        x = 10
        y = 5
    }

    # === 共同起点 ===
    focus = {
        id = JAP_national_philosophy
        icon = GFX_goal_generic_national_unity
        x = 10
        y = 5
        cost = 10

        completion_reward = {
            add_political_power = 100
        }
    }

    # === 军国主义路线（右上）===
    focus = {
        id = JAP_militarism
        icon = GFX_goal_generic_military_sphere
        relative_position_id = JAP_national_philosophy
        x = 3
        y = 1
        cost = 10
        prerequisite = { focus = JAP_national_philosophy }

        # 民主路线完成后此焦点不可选
        available = {
            NOT = { has_completed_focus = JAP_democracy }
        }

        completion_reward = {
            add_ideas = JAP_militarism_idea
        }

        ai_will_do = {
            factor = 5
            modifier = {
                factor = 2
                has_government = fascism
            }
        }
    }

    # 军国后续
    focus = {
        id = JAP_militarism_expansion
        icon = GFX_goal_generic_major_winter_offensive
        relative_position_id = JAP_militarism
        x = 2
        y = 1
        cost = 10
        prerequisite = { focus = JAP_militarism }

        available = {
            has_completed_focus = JAP_militarism
        }

        completion_reward = {
            add_war_support = 0.05
        }
    }

    # === 民主路线（左上）===
    focus = {
        id = JAP_democracy
        icon = GFX_goal_generic_democratic_drift
        relative_position_id = JAP_national_philosophy
        x = -3
        y = 1
        cost = 10
        prerequisite = { focus = JAP_national_philosophy }

        # 军国路线完成后此焦点不可选
        available = {
            NOT = { has_completed_focus = JAP_militarism }
        }

        completion_reward = {
            add_popularity = {
                ideology = democracy
                popularity = 0.10
            }
        }

        ai_will_do = {
            factor = 2
            modifier = {
                factor = 3
                has_government = democracy
            }
        }
    }

    # 民主后续
    focus = {
        id = JAP_democracy_pacifism
        icon = GFX_focus_generic_treaty
        relative_position_id = JAP_democracy
        x = -2
        y = 1
        cost = 10
        prerequisite = { focus = JAP_democracy }

        completion_reward = {
            add_popularity = {
                ideology = democracy
                popularity = 0.10
            }
            add_stability = 0.05
        }
    }

    # === 条件汇聚焦点（两条路线均可到达）===
    focus = {
        id = JAP_national_destiny
        icon = GFX_goal_generic_forceful_treaty
        x = 10
        y = 10
        cost = 10

        # 两条路线的任一后续焦点都可作为前置
        prerequisite = { focus = JAP_militarism_expansion }
        prerequisite = { focus = JAP_democracy_pacifism }

        completion_reward = {
            add_political_power = 200
        }
    }
}
```

**条件互锁设计原则**：

1. **入口互斥**：两条路线的入口焦点通过 `available` 互锁（完成一条路另一条关闭）
2. **非入口不互锁**：路线内部的焦点不需要再检查互斥条件（入口已保证）
3. **汇聚用 OR 前置**：`prerequisite = { focus = A }` + `prerequisite = { focus = B }` 表示 OR 关系（任一即可）
4. **AI 权重分流**：用 `ai_will_do` 的 `modifier` 引导 AI 根据当前意识形态选择路线

### 模式三：环形布局 — 以意大利为蓝本

**概念**：焦点形成环状结构——从顶部出发，沿两侧向下，最终在底部汇合。意大利的"历史路线vs反历史路线"就是经典的环形。

**结构示意**：

```
         [起点焦点]
        ↙          ↘
  [左路线A]      [右路线B]
      ↓              ↓
  [左路线C]      [右路线D]
        ↘          ↙
         [汇聚焦点]
```

**完整代码骨架**：

```
focus_tree = {
    id = italian_focus

    country = {
        factor = 0
        modifier = {
            add = 10
            tag = ITA
        }
    }

    default = no

    initial_show_position = {
        x = 12
        y = 3
    }

    # === 顶部起点 ===
    focus = {
        id = ITA_mediterranean_ambitions
        icon = GFX_goal_generic_naval_arms
        x = 12
        y = 3
        cost = 10

        completion_reward = {
            add_political_power = 50
        }
    }

    # === 左环：历史路线 ===
    focus = {
        id = ITA_ethiopia_focus
        icon = GFX_goal_generic_territory_or_war
        relative_position_id = ITA_mediterranean_ambitions
        x = -5
        y = 1
        cost = 10
        prerequisite = { focus = ITA_mediterranean_ambitions }

        completion_reward = {
            add_offsite_building = {
                type = arms_factory
                level = 1
                province = 12251
            }
        }
    }

    focus = {
        id = ITA_pact_of_steel
        icon = GFX_goal_generic_alliance
        relative_position_id = ITA_ethiopia_focus
        x = -2
        y = 2
        cost = 10
        prerequisite = { focus = ITA_ethiopia_focus }

        completion_reward = {
            add_opinion_modifier = {
                target = GER
                modifier = positive_relationship
            }
        }
    }

    focus = {
        id = ITA_war_effort
        icon = GFX_goal_generic_major_winter_offensive
        relative_position_id = ITA_pact_of_steel
        x = 3
        y = 2
        cost = 10
        prerequisite = { focus = ITA_pact_of_steel }

        completion_reward = {
            add_war_support = 0.10
        }
    }

    # === 右环：反历史路线 ===
    focus = {
        id = ITA_anti_fascism
        icon = GFX_goal_generic_democratic_drift
        relative_position_id = ITA_mediterranean_ambitions
        x = 5
        y = 1
        cost = 10
        prerequisite = { focus = ITA_mediterranean_ambitions }

        available = {
            NOT = { has_government = fascism }
        }

        completion_reward = {
            add_popularity = {
                ideology = democracy
                popularity = 0.10
            }
        }
    }

    focus = {
        id = ITA_democratic_reforms
        icon = GFX_goal_generic_constitution
        relative_position_id = ITA_anti_fascism
        x = 2
        y = 2
        cost = 10
        prerequisite = { focus = ITA_anti_fascism }

        completion_reward = {
            set_politics = {
                ruling_party = democracy
                elections_allowed = yes
            }
        }
    }

    focus = {
        id = ITA_mediterranean_defense
        icon = GFX_goal_generic_naval_supremacy
        relative_position_id = ITA_democratic_reforms
        x = -3
        y = 2
        cost = 10
        prerequisite = { focus = ITA_democratic_reforms }

        completion_reward = {
            add_naval_bonus = {
                bonus = 0.10
                category = screen_ships
            }
        }
    }

    # === 底部汇聚 ===
    focus = {
        id = ITA_new_roman_empire
        icon = GFX_goal_generic_major_alliance
        x = 12
        y = 10
        cost = 10

        # OR 前置：左环或右环均可到达
        prerequisite = { focus = ITA_war_effort }
        prerequisite = { focus = ITA_mediterranean_defense }

        completion_reward = {
            add_political_power = 200
            add_stability = 0.10
        }
    }
}
```

**环形布局要点**：

| 要素 | 建议 |
|------|------|
| 左右间距 | ≥8格（避免两环交叉） |
| 汇聚焦点y值 | 至少比起点低5行 |
| 中间层焦点 | 使用 `relative_position_id` + xy微调实现"向中心收拢" |
| 视觉对称 | 左右环的焦点数量和深度应大致对称 |

### 模式四：嵌入窗口（Inlay Window）— 以波兰为蓝本

**概念**：嵌入窗口在国策树的某个区域创建一个独立子面板，将一组焦点"隔离"在框架内。波兰用此技术将特殊分支包裹在可视边界中。

**完整代码骨架**：

```
focus_tree = {
    id = polish_focus

    country = {
        factor = 0
        modifier = {
            add = 10
            tag = POL
        }
    }

    default = no

    initial_show_position = {
        x = 14
        y = 5
    }

    # === 主树焦点 ===
    focus = {
        id = POL_polish_independence
        icon = GFX_goal_generic_national_unity
        x = 14
        y = 5
        cost = 10

        completion_reward = {
            add_political_power = 100
        }
    }

    # === 嵌入窗口定义 ===
    # 嵌入窗口本身不是焦点，而是一个容器
    # 它为窗口内的焦点提供一个独立的坐标空间

    # 窗口内的起始焦点（需要连接到主树）
    focus = {
        id = POL_interwar_development
        icon = GFX_goal_generic_construct_military
        relative_position_id = POL_polish_independence
        x = -5
        y = 2
        cost = 10
        prerequisite = { focus = POL_polish_independence }

        # 标记为内圈焦点（在窗口内使用环形排列）
        inner_circle = yes

        completion_reward = {
            add_offsite_building = {
                type = industrial_complex
                level = 1
                province = 3269
            }
        }
    }

    # 窗口内的分支焦点
    focus = {
        id = POL_agrarian_reform
        icon = GFX_goal_generic_generic_fascism_6
        relative_position_id = POL_interwar_development
        x = -3
        y = 1
        cost = 10
        prerequisite = { focus = POL_interwar_development }

        completion_reward = {
            add_stability = 0.05
        }
    }

    focus = {
        id = POL_industrial_development
        icon = GFX_goal_generic_construct_civ_factory
        relative_position_id = POL_interwar_development
        x = 3
        y = 1
        cost = 10
        prerequisite = { focus = POL_interwar_development }

        completion_reward = {
            add_extra_state_shared_building_slots = {
                building = industrial_complex
                level = 2
            }
        }
    }

    # 窗口内汇聚
    focus = {
        id = POL_economic_miracle
        icon = GFX_goal_generic_generic_fascism_7
        relative_position_id = POL_interwar_development
        x = 0
        y = 3
        cost = 10
        prerequisite = { focus = POL_agrarian_reform }
        prerequisite = { focus = POL_industrial_development }

        completion_reward = {
            add_political_power = 100
            add_stability = 0.10
        }
    }
}
```

**嵌入窗口设计原则**：

1. **窗口内的坐标系统**：窗口内焦点使用 `relative_position_id` 链式定位，形成自包含子系统
2. **窗口与主树连接**：窗口只有一个"入口"焦点连接到主树（通过 prerequisite）
3. **窗口入口位置**：入口焦点使用 `relative_position_id` 定位在主树某焦点旁边
4. **窗口大小**：控制在 4-8 个焦点以内（太大不好看，太小没意义）

### 模式五：连续焦点线（Continuous Focus Line）

**概念**：连续焦点（Continuous Focus）不会在完成后消失，而是持续提供效果。在布局上，连续焦点线通常与主树分开排列。

**完整代码骨架**：

```
focus_tree = {
    id = soviet_focus

    country = {
        factor = 0
        modifier = {
            add = 10
            tag = SOV
        }
    }

    default = no

    initial_show_position = {
        x = 15
        y = 8
    }

    # === 主树焦点 ===
    focus = {
        id = SOV_stalin_constitution
        icon = GFX_goal_generic_national_unity
        x = 15
        y = 8
        cost = 10

        completion_reward = {
            add_stability = 0.05
        }
    }

    # === 连续焦点线（底部或侧边）===

    # 连续焦点1：军备生产
    focus = {
        id = SOV_arms_production
        icon = GFX_goal_generic_military_sphere
        x = 10        # 位于主树左侧，与主树明显分离
        y = 15        # y值较大，位于底部
        cost = 10
        continuously_allowed = {
            always = yes
        }

        completion_reward = {
            add_military_bonus = {
                bonus = 0.05
                category = infantry
            }
        }

        ai_will_do = {
            factor = 3
        }
    }

    # 连续焦点2：工业化
    focus = {
        id = SOV_industrialization
        icon = GFX_goal_generic_construct_mil_factory
        relative_position_id = SOV_arms_production
        x = 5
        y = 0       # 与前一个连续焦点同行
        cost = 10
        continuously_allowed = {
            always = yes
        }

        available = {
            has_completed_focus = SOV_arms_production
        }

        completion_reward = {
            add_extra_state_shared_building_slots = {
                building = arms_factory
                level = 1
            }
        }

        ai_will_do = {
            factor = 2
        }
    }

    # 连续焦点3：宣传
    focus = {
        id = SOV_propaganda
        icon = GFX_goal_generic_generic_fascism_6
        relative_position_id = SOV_industrialization
        x = 5
        y = 0       # 继续同行排列
        cost = 10
        continuously_allowed = {
            always = yes
        }

        available = {
            has_completed_focus = SOV_industrialization
        }

        completion_reward = {
            add_war_support = 0.02
            add_political_power = 25
        }

        ai_will_do = {
            factor = 1
        }
    }
}
```

**连续焦点布局原则**：

| 要素 | 建议 |
|------|------|
| 与主树间距 | x差 ≥5格，或y差 ≥3行 |
| 排列方向 | 水平行排列（同一y值，x递增） |
| 节点间距 | 使用 `relative_position_id` + `x = 5` |
| `continuously_allowed` | 至少写 `always = yes`，也可加条件 |
| `available` | 前一个连续焦点完成后再解锁下一个 |
| `cost` | 10（与常规焦点一致） |

> **重要限制**：连续焦点不能作为常规焦点的前置条件（`prerequisite`）。它们是独立的"平行轨道"。

### 模式对比与选用指南

| 模式 | 适用场景 | 复杂度 | 焦点数建议 | 视觉特色 |
|------|---------|--------|-----------|---------|
| 内圈 | 多意识形态选择 | ★★★ | 5-8（含中心） | 环形，居中 |
| 条件分支 | 路线互锁/互斥 | ★★★★ | 10-20 | V形/叉形 |
| 环形 | 两条路线汇聚 | ★★★ | 8-15 | O形/U形 |
| 嵌入窗口 | 子系统隔离 | ★★★★ | 4-8（窗口内） | 框架包裹 |
| 连续焦点 | 持续性奖励轨道 | ★★ | 3-6 | 水平线，独立 |

**组合使用**：复杂国策树通常组合多种模式。例如：
- 德国 = 内圈 + 条件分支
- 日本 = 条件分支 + 环形
- 意大利 = 环形 + 嵌入窗口
- 苏联 = 条件分支 + 连续焦点


## 原版国策树数据分析与设计规范

> **数据来源**：德国(440)、苏联(328)、日本(450)、意大利(314)四国原版国策树，共1532个焦点。
>
> **目的**：从 Paradox 官方设计中提炼可量化的设计规范，为 mod 创作者提供**推荐区间**而非死板上限——你可以在区间内自由调整，只要理解每个数值的含义。

---

### 国策成本（cost）统计

国策的 `cost` 字段直接决定完成天数：**实际天数 = cost × 7**。

#### 四国成本分布

| cost | 天数 | 德国 | 苏联 | 日本 | 意大利 | 含义 |
|------|------|------|------|------|--------|------|
| 0 | 0天 | ✓ | - | ✓ | - | 瞬间完成（剧情触发/内圈选择） |
| 2 | 14天 | 13 | - | 4 | - | 快速过渡节点 |
| 3 | 21天 | - | - | 2 | - | 极少见 |
| 5 | 35天 | 230 | 120 | 233 | 171 | **标准节点**（最常见） |
| 10 | 70天 | 169 | 207 | 204 | 143 | **重大节点** |
| 12 | 84天 | - | 1 | - | - | 极罕见（仅苏联转型自然） |

#### 推荐区间

```
📌 成本分配推荐区间：

  普通节点：cost = 5（35天）
    → 占总数 40-60%
    → 适用于大部分「过程型」节点

  重大节点：cost = 10（70天）
    → 占总数 25-40%
    → 适用于阶段性终点、重大决策

  快速过渡：cost = 1-3（7-21天）
    → 占总数 5-15%
    → 适用于路线切换、内圈选择、剧情触发
    → cost=1-3 原版少用但并非禁忌，可以用来制造「小步快跑」的节奏感

  瞬间触发：cost = 0
    → 仅用于内圈选择、自动触发的剧情节点

  超长节点：cost = 12-15（84-105天）
    → 原版极少使用，但 mod 中可用于「终极目标」型节点
    → 建议：整个国策树中此类节点不超过 2-3 个
    → 必须配以足够丰厚的奖励，否则玩家会跳过

💡 原版数据解读：
  原版不用 cost>10 不代表你不能用——原版的设计偏保守。
  只要你有意为之（比如设计一个需要长期投入才能完成的终极国策），
  cost=12-15 完全合理。关键是：越长的国策，奖励要越值得等待。
```

---

### 分支结构统计

#### 根焦点（独立分支）数量

| 国家 | 焦点总数 | 根焦点数 | 说明 |
|------|----------|----------|------|
| 德国 | 440 | 8 | 经济+四年计划+机动战+空军+海军+莱茵兰+反对希特勒×2 |
| 苏联 | 328 | 9 | 基建+重工业+航空+海军+PCDI+动员+马克思主义+战败+集权 |
| 日本 | 450 | 11 | 不可想象+民主+皇道派+冈田演说+尊皇+清洗+小矶×2+工商+国防+？ |
| 意大利 | 314 | 10 | 后勤+公路+陆军+空军+海军+阿比西尼亚+稳步推进+… |

#### 根分支类型与规模

```
典型大国国策树的分支构成：

┌────────────────────────────────────────────────────┐
│ 政治路线分支（1-3个根）                              │
│   深度：7-14层  节点数：40-180  总耗时：2000-9000天   │
│   特征：互斥选择，多条替代路线，外交和领土要求        │
├────────────────────────────────────────────────────┤
│ 工业分支（1-2个根）                                  │
│   深度：5-8层  节点数：20-30  总耗时：1000-1900天     │
│   特征：民用/军用工厂、基础设施、资源                  │
├────────────────────────────────────────────────────┤
│ 陆军分支（1个根）                                    │
│   深度：5-9层  节点数：15-35  总耗时：800-3400天      │
│   特征：学说、装甲、步兵、特殊兵种                    │
├────────────────────────────────────────────────────┤
│ 空军分支（1个根）                                    │
│   深度：5层  节点数：16-20  总耗时：900-1000天        │
│   特征：战斗机、轰炸机、伞兵                         │
├────────────────────────────────────────────────────┤
│ 海军分支（1个根）                                    │
│   深度：5层  节点数：18-22  总耗时：900-1300天        │
│   特征：舰队、潜艇、海军航空                         │
└────────────────────────────────────────────────────┘
```

#### 推荐区间

```
📌 大国（主要国家）的分支规划：
  • 5-10 个独立根分支
  • 政治路线总深度 7-16 层（含所有子分支）
  • 工业/军事路线总深度 5-9 层
  • 最长单链建议不超过 14 层

📌 小国（次要国家）的分支规划：
  • 3-5 个独立根分支
  • 政治路线总深度 5-10 层
  • 工业/军事路线总深度 3-6 层
  • 焦点总数 30-100 个

📌 需要注意的问题：
  • 单根分支超过 20 层深 → 玩家可能等好几年才走完，考虑拆分
  • 所有分支共享同一根 → 缺乏选择感，考虑增加独立入口
  • 分支间完全无汇合点 → 缺乏战略权衡，考虑在关键位置合并
```

---

### 奖励类型与数值推荐

#### 科技加成（add_tech_bonus）

```
原版最常见格式：
add_tech_bonus = {
    name = <国策ID>
    bonus = 1                 # 100%加成
    uses = 1                  # 使用1次
    category = <类别>
}

📌 推荐区间：
  bonus = 1, uses = 1    → 标准科技加成（最常见）
  bonus = 1, uses = 2    → 双科技加成（重要节点）
  bonus = 0.5, uses = 1  → 50%加成（过渡型节点，给一点但不强）

  进阶用法（原版少见但 mod 可用）：
  bonus = 1, uses = 3    → 三次加成——保留给分支的最终大奖
  bonus = 2, uses = 1    → 200%加成——极强但只能用一次，适合终极节点
  bonus = 0.5, uses = 2  → 两次50%——中等偏弱，适合中间过程节点

💡 判断标准：
  问自己「这个节点在整条分支中是什么位置？」
  • 中间过程 → bonus=1 uses=1 或 bonus=0.5 uses=1
  • 阶段终点 → bonus=1 uses=2
  • 分支终极大奖 → bonus=1 uses=3 或 bonus=2 uses=1
```

#### 建筑（add_building_construction）

| 建筑类型 | 常见等级 | 出现频率 | 说明 |
|----------|----------|----------|------|
| 基础设施 | lvl=1 | 134次 | 最常见的建筑奖励 |
| 民用工厂 | lvl=1 | 79次 | 标准工业奖励 |
| 军用工厂 | lvl=1 | 77次 | 标准工业奖励 |
| 军用工厂 | lvl=2 | 52次 | 重要工业节点 |
| 民用工厂 | lvl=2 | 52次 | 重要工业节点 |
| 船坞 | lvl=1 | 45次 | 海军分支标准奖励 |
| 陆上要塞 | lvl=2 | 44次 | 防御焦点 |
| 船坞 | lvl=2 | 38次 | 重要海军节点 |
| 陆上要塞 | lvl=3 | 37次 | 马奇诺/大西洋壁垒级别 |
| 防空 | lvl=1 | 23次 | 后期防御 |

```
📌 建筑奖励推荐区间：

  中间过程节点（cost=5）：
    → 1个建筑 lvl=1
    → 或 1个科技加成（二选一）

  阶段终点节点（cost=10）：
    → 1-2个建筑 lvl=1-2
    → 或 1个建筑 + 1个科技加成

  分支终极大奖：
    → 2-4个建筑 lvl=1-3
    → 可以同时给建筑 + 科技加成 + 少量PP/XP
    → 例：2民用工厂 + 1军用工厂 + 1科技加成 + 25XP

📌 建筑上限参考：
  • 单节点工厂（民用/军用）建议不超过 4 级
  • 基础设施建议不超过 5 级（分散多个省份）
  • 要塞建议不超过 5 级（马奇诺级 = 3-5）
  • 以上是推荐区间，不是硬上限——终极节点可以适当突破
```

#### 政治点数（add_political_power）

| 数值 | 出现次数 | 占比 |
|------|----------|------|
| < 100 | 188 | 82% |
| 100 | 26 | 11% |
| 120 | 8 | 4% |
| 150 | 6 | 3% |
| 200 | 1 | <1% |

```
📌 PP 奖励推荐区间：

  中间过程节点：25-50 PP
  阶段终点节点：50-100 PP
  分支终极大奖：100-200 PP

💡 原版 82% 的节点 PP<100，但这恰恰是因为原版中间节点给得太多、
   终点节点给得不够突出。mod 设计中可以让终点节点给到 150-200 PP，
   同时把中间节点的 PP 压低到 10-25，制造更强的目标感。
```

#### 经验值（army/air/navy_experience）

| 数值 | 陆军 | 空军 | 海军 |
|------|------|------|------|
| 5 | - | 2 | 3 |
| 10 | 2 | - | 3 |
| 15 | 17 | 7 | 14 |
| 25 | 19 | 23 | 28 |
| 50 | 9 | 6 | 12 |
| 75 | 4 | - | - |

```
📌 XP 奖励推荐区间：

  中间过程节点：10-15 XP（低奖励，推动玩家继续往下走）
  阶段终点节点：25-50 XP
  分支终极大奖：50-100 XP

  典型分配：
  • 陆军焦点 → army_experience
  • 海军焦点 → navy_experience
  • 空军焦点 → air_experience
  • 综合军事 → 三种各 10-15

💡 同样，原版中间节点给 25 XP 偏多。mod 中可以把中间节点压到 10-15，
   终点节点给到 50-100，让玩家明显感到「走到终点是值得的」。
```

---

### 🎯 递进奖励设计（Progressive Reward Design）

这是 mod 国策树设计中最容易被忽略、但对玩家体验影响最大的设计原则：

**中间节点少给，终点节点多给，让玩家始终有奔头。**

#### 为什么要递进？

```
平坦奖励（原版常见模式）：

  ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐
  │ 5 │──▶│ 5 │──▶│ 5 │──▶│ 5 │──▶│ 5 │
  └───┘   └───┘   └───┘   └───┘   └───┘
  +1工厂   +1工厂   +1工厂   +1工厂   +1工厂

  问题：每个节点奖励一样，走到哪里都一样。
       玩家没有「冲向终点」的动力。
       走到一半可能觉得「够了，去做别的吧」。

递进奖励（推荐模式）：

  ┌───┐   ┌───┐   ┌────┐   ┌───┐   ┌──────────┐
  │ 5 │──▶│ 5 │──▶│ 10 │──▶│ 5 │──▶│ 10       │
  └───┘   └───┘   └────┘   └───┘   └──────────┘
  +1基建   +1基建  +2工厂   +1基建  +4工厂+科技+50XP
  ↑        ↑       ↑        ↑       ↑
  铺路     铺路    阶段成果  铺路    🏆 终极大奖！

  玩家心理：「再走一个就到大奖励了！」
           中间的小奖励是安慰剂，不是目的地。
```

#### 三层奖励结构

一个设计良好的分支，每个节点可以归入以下三层之一：

```
┌──────────────────────────────────────────────────────┐
│  🏆 终点层（Capstone）                                │
│  分支的最终目标，玩家走这条路的全部理由                │
│                                                      │
│  奖励力度：★★★★★                                    │
│  典型奖励：                                          │
│    • 3-4 个工厂 + 科技加成 + 50-100 XP               │
│    • 或强力民族精神 + 100-200 PP                     │
│    • 或解锁特殊机制/单位/领土要求                     │
│    • 或 add_tech_bonus bonus=2 uses=1                │
│  cost：通常 = 10-15（值得等待）                      │
│  数量：每条分支 1-2 个                                │
├──────────────────────────────────────────────────────┤
│  📦 阶段层（Milestone）                               │
│  分支的中期目标，让玩家感到「阶段性进展」              │
│                                                      │
│  奖励力度：★★★☆☆                                    │
│  典型奖励：                                          │
│    • 1-2 个工厂 + 少量 XP（10-25）                    │
│    • 或 1 个科技加成                                  │
│    • 或中等民族精神 + 50-100 PP                      │
│  cost：通常 = 10（需要投入但不过分）                  │
│  数量：每条分支 2-3 个                                │
├──────────────────────────────────────────────────────┤
│  🪨 过程层（Stepping Stone）                          │
│  通向目标的踏脚石，奖励少但推进了进度                  │
│                                                      │
│  奖励力度：★★☆☆☆                                    │
│  典型奖励：                                          │
│    • 1 个基建 lvl=1                                  │
│    • 或 10-15 XP                                     │
│    • 或 25 PP                                        │
│    • 或一个 tooltip 提示（无实际效果但推进前置链）     │
│  cost：通常 = 5（快速通过）                           │
│  数量：每条分支 3-5 个                                │
│                                                      │
│  💡 关键：过程层奖励要克制，不要和终点层抢戏！         │
│    给太多 → 终点不稀罕了                              │
│    给太少 → 玩家觉得浪费时间                          │
│    最佳状态：刚好够用，但远远不够好                    │
└──────────────────────────────────────────────────────┘
```

#### 完整示例：工业分支的递进奖励

```
focus_tree = {
    id = TAG_industrial_tree

    # ===== 过程层：铺路 =====
    focus = {
        id = TAG_rebuild_infrastructure
        cost = 5
        # 🪨 奖励：1基建 —— 勉强够用，不是目的地
        completion_reward = {
            add_building_construction = {
                type = infrastructure
                level = 1
                province = { 1234 }
            }
        }
    }

    focus = {
        id = TAG_expand_mining
        cost = 5
        prerequisite = { focus = TAG_rebuild_infrastructure }
        # 🪨 奖励：1基建 + 10 PP —— 还是铺路
        completion_reward = {
            add_building_construction = {
                type = infrastructure
                level = 1
                province = { 5678 }
            }
            add_political_power = 10
        }
    }

    # ===== 阶段层：中期成果 =====
    focus = {
        id = TAG_industrial_expansion
        cost = 10
        prerequisite = { focus = TAG_expand_mining }
        # 📦 奖励：2工厂 + 科技加成 —— 有收获了！
        completion_reward = {
            add_building_construction = {
                type = industrial_complex
                level = 2
                province = { 1234 5678 }
            }
            add_tech_bonus = {
                name = TAG_industrial_expansion
                bonus = 1
                uses = 1
                category = industry
            }
        }
    }

    # ===== 过程层：继续铺路 =====
    focus = {
        id = TAG_modernize_production
        cost = 5
        prerequisite = { focus = TAG_industrial_expansion }
        # 🪨 奖励：1基建 + 15 XP —— 比之前稍好，但还不够
        completion_reward = {
            add_building_construction = {
                type = infrastructure
                level = 1
                province = { 9012 }
            }
            army_experience = 15
        }
    }

    # ===== 🏆 终点层：终极目标 =====
    focus = {
        id = TAG_industrial_supremacy
        cost = 15
        prerequisite = { focus = TAG_modernize_production }
        # 🏆 终极大奖：4工厂 + 2军用工厂 + 科技加成 + 50XP + 100PP
        # 玩家走完整条工业线的全部理由！
        completion_reward = {
            add_building_construction = {
                type = industrial_complex
                level = 4
                province = { 1234 5678 9012 3456 }
            }
            add_building_construction = {
                type = arms_factory
                level = 2
                province = { 1234 5678 }
            }
            add_tech_bonus = {
                name = TAG_industrial_supremacy
                bonus = 1
                uses = 2
                category = industry
            }
            army_experience = 50
            add_political_power = 100
        }
    }
}
```

#### 递进奖励的自检方法

```
自检问题1：「如果我跳过中间节点直接到终点，我会觉得遗憾吗？」
  → 如果答案是「不太遗憾」→ 中间奖励给太多了，压低它
  → 如果答案是「非常遗憾」→ 中间奖励刚刚好

自检问题2：「走到终点的时候，我有「终于到了！」的感觉吗？」
  → 如果答案是「和之前差不多」→ 终点奖励不够突出，加大它
  → 如果答案是「值了！」→ 设计成功

自检问题3：「整条分支的奖励总量合理吗？」
  → 把所有节点的奖励加在一起，和同规模的原版分支对比
  → 如果总量远超原版 → 需要整体压低
  → 如果总量接近原版 → 分布合理
  → 💡 关键：递进设计不是让你给更多奖励，
    而是把同样的奖励总额重新分配——中间少给，终点多给
```

---

### 节奏设计：完成时间与玩家体验

#### 单分支节奏曲线

一个设计良好的分支应该有 **节奏感** —— 不是每个节点都一样重或一样轻：

```
递进式节奏（推荐）：

  ┌───┐   ┌───┐   ┌────┐   ┌───┐   ┌────┐   ┌────────┐
  │ 5 │──▶│ 5 │──▶│ 10 │──▶│ 5 │──▶│ 10 │──▶│ 10-15  │
  └───┘   └───┘   └────┘   └───┘   └────┘   └────────┘
  🪨       🪨      📦       🪨      📦       🏆
  35天     35天     70天    35天     70天    70-105天
  铺路     铺路    阶段成果  铺路    阶段成果  终极大奖

节奏模式：轻-轻-重-轻-重-极重
总耗时：245-315天 ≈ 8-10.5个月

💡 和「平坦节奏」对比：

  平坦：5-5-5-5-5-5 → 总计210天，但没有高潮
  递进：5-5-10-5-10-15 → 总计280天，有节奏有目标
  多出来的70天换来的是强烈的目标感——值得
```

#### 全树并行节奏

```
典型大国早期节奏（1936年开始）：

  第1-3月：完成政治路线第一个节点（cost=5-10）
  第3-6月：工业分支前2个节点（🪨 过程层）
  第6-9月：工业分支第一个 📦 阶段成果
  第9-12月：军事分支起步 + 政治路线继续
  第12-24月：多条分支并行，穿插阶段成果
  第24-36月：开始触及各分支的 🏆 终点

关键设计原则：
  • 玩家前3个月必须能看到并做出第一个有意义的选择
  • 任何分支的「第一跳」建议不超过 70天（cost ≤ 10）
  • 每隔 3-5 个月应该有一个 📦 阶段成果让玩家感到进展
  • 🏆 终点节点不应早于第 12 个月出现（太快拿到大奖没意思）
```

#### 节奏警告（而非违规）

```
⚠️ 疲劳带警告：
  连续 4+ 个节点 cost ≥ 10 → 玩家要等 280+ 天
  连续 3 个 cost=10 不是问题，但如果 4 个以上，
  考虑插入一个 cost=5 的过程节点作为「喘息」。

  不是禁止，而是提醒你检查：这些重量级节点是否都有
  配得上等待的奖励？如果中间节点奖励稀薄 + cost高，
  那才是真正的问题。

⚠️ 闪电带警告：
  连续 4+ 个节点 cost ≤ 2 → 玩家几秒点完
  连续 2-3 个快速节点没问题，但 4 个以上会让
  这段路线缺乏分量感。考虑合并为 cost=5 的节点。

💡 允许的例外：
  • 内圈焦点路线：连续 cost=0 是正常的（选人不是做国策）
  • 革命/政变路线：连续快速节点模拟事态飞速发展
  • 只要在设计时有意识地选择，而不是无意间造成的
```

---

### 焦点总数与规模规划

#### 按国家规模的推荐焦点数

| 国家规模 | 焦点总数 | 根分支数 | 最深层数 |
|----------|----------|----------|----------|
| 主要大国（德苏美英） | 300-450 | 7-11 | 10-14 |
| 次要大国（日意法波） | 200-350 | 5-10 | 8-14 |
| 区域强国（匈罗芬捷） | 80-150 | 4-6 | 6-10 |
| 小国（通用焦点为主） | 40-80 | 2-4 | 4-7 |
| 微型国家 | 15-30 | 1-2 | 3-5 |

#### 按类型分配焦点数

```
大国典型分配（以350个焦点为例）：

  政治路线：100-150个（30-40%）—— 包含多条互斥路线
  工业分支：40-60个（12-15%）
  陆军分支：40-50个（12-15%）
  空军分支：20-30个（6-8%）
  海军分支：20-30个（6-8%）
  外交/领土：30-50个（8-12%）
  内圈/特殊：10-20个（3-5%）

  💡 提示：政治路线总是占比最大的，
           因为它包含多条互斥替代路线。
```

---

### 奖励密度与递进分配

「奖励密度」= 焦点完成奖励的感知价值 ÷ 完成耗时。

在递进奖励设计中，不同层的密度是故意不同的：

```
奖励密度与层级的关系：

  🪨 过程层 —— 低密度（故意为之）
    cost=5，仅给 1基建 / 10-15XP / 25PP
    → 密度偏低是正常的！这正是推动玩家继续往下走的动力
    → ⚠️ 但不能低到「完全不值得点」——至少给一点实质性的东西

  📦 阶段层 —— 中等密度
    cost=10，给 1-2工厂 + 科技加成 / 50PP + 25XP
    → 密度适中，让玩家觉得「这段路没白走」

  🏆 终点层 —— 高密度（蓄力释放）
    cost=10-15，给 3-4工厂 + 科技加成 + XP + PP
    → 密度显著高于前两层——这正是递进设计的核心
    → 所有之前克制的奖励都在这里集中释放

  📊 总量守恒原则：
    递进设计 ≠ 给更多奖励。是把**相同总量**重新分配。

    平坦模式：6个节点各给1工厂 = 总共6工厂
    递进模式：4个过程层给1基建，1个阶段层给2工厂，
             1个终点层给4工厂+科技+XP = 总量相当但更有目标感

    如果递进模式的总量明显高于平坦模式 → 整体偏强，需要削减
```

---

### 与现有检查清单的整合

在[设计检查清单](#设计检查清单)基础上，新增以下数据驱动检查项：

#### 数值平衡检查

```
□ 全树 cost=5 和 cost=10 的比例是否在 2:1 到 1:1 之间？
□ cost>10 的节点是否不超过全树的 3%（且都是终点层）？
□ 单节点奖励是否在推荐区间内：
    • 建筑：过程层 ≤1级，阶段层 1-2级，终点层 2-4级
    • PP：过程层 ≤50，阶段层 50-100，终点层 100-200
    • XP：过程层 ≤25，阶段层 25-50，终点层 50-100
    • 科技加成：过程层 ≤1次，阶段层 1-2次，终点层 2-3次
□ 全树焦点总数是否匹配国家规模？
□ 根分支数量是否在推荐范围？
□ 是否存在奖励远超所在层级标准的节点？（检查是否放错了层）
```

#### 递进奖励检查

```
□ 每条分支是否至少有 1 个 🏆 终点层节点？
□ 终点层的奖励是否明显优于同一分支的过程层？
  （至少 2-3 倍的感知价值差异）
□ 是否存在中间节点奖励 > 终点节点的情况？（层次倒挂）
□ 站在玩家角度：走到终点时是否有「终于到了！」的感觉？
□ 整条分支的奖励总量是否与原版同规模分支相当？
  （递进是重新分配，不是加量）
```

#### 节奏检查

```
□ 从游戏开始到第一个有意义的选择，是否 ≤70天？
□ 是否存在连续 4+ 个 cost≥10 的情况？（疲劳带警告）
□ 是否存在连续 4+ 个 cost≤2 的情况？（闪电带警告）
  → 如果存在，是否是刻意设计（内圈/政变路线）？
□ 每 3-5 个月是否有至少一个 📦 阶段成果？
□ 🏆 终点节点是否不在游戏前 12 个月内出现？
```

## 第7章 典型子模块与拼装策略

> 本章介绍可供组合复用的典型国策树子模块，以及如何将它们拼装成一棵完整树。

### 常用典型子模块

#### 1. 经济-政治 双轨并行（推荐）

```
根节点(x=0,y=0)
├─ 经济分支(x=-2,y=1) ─ 分支终点A(x=-4,y=2)
│                    └─ 分支终点B(x=-6,y=2)
│   ...最多3层深...
└─ 政治分支(x=+2,y=1) ─ 分支终点C(x=+4,y=2)
                     └─ 分支终点D(x=+6,y=2)
    ...最多3层深...

# 两分支在第2层重新汇合到共同终点
汇合节点(x=0,y=3)
```

特点：同一时期给玩家两个方向选择，强迫性小，节奏感好。y间距1格，x间距2格。

#### 2. 主干+双侧翼

```
主干垂直向下 (x=0,y=0) -> (x=0,y=1) -> (x=0,y=2) -> (x=0,y=3)
左翼(x=-2)与右翼(x=+2)在各层展开，y间距1格，x间距2格
最大深度：主干20层，左翼最多3层
```

#### 3. 星形汇聚（5个方向）

```
中心节点(x=0,y=0)
├─ 东(x=+2,y=0)
├─ 西(x=-2,y=0)
├─ 东北(x=+2,y=-1)
├─ 西北(x=-2,y=-1)
└─ 下(x=0,y=+1)
```

最多5个子节点，符合子节点上限5的约束。x间距均为2。

#### 4. 政策三角形

```
上(x=0,y=0)
├─ 左下(x=-2,y=1)
└─ 右下(x=+2,y=1)
    然后左下和右下各有一个子节点在(x=0,y=2)处汇合
```

### 拼装流程（4步）

1. **确定主干**：选出3-5个核心焦点作为主干，垂直排列，y间距1或2，最大深度20层
2. **嵌入子模块**：在主干各节点处替换/挂载典型子模块
3. **间距检查**：同层节点x差>=2，同分支连续节点不超过3层，分支间距>=4
4. **子节点数量检查**：任一节点直接子节点<=5，超过则二级分支

### 典型陷阱

- **主线过长**：主干>10层且无分支 -> 拆分为两段，中间用「章节终点」国策分隔
- **子节点爆炸**：一个节点有6+子节点 -> 选中间节点作为「分流枢纽」，将子节点分到两层
- **孤岛节点**：某些节点前置链条全部断在5层以外 -> 删除或合并到临近分支