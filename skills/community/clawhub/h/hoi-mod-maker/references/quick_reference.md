# HOI4 Modding 快速参考卡片

> 最常用的语法和参数，一页速查。

---

## 🎯 国策树核心字段

### Focus Tree 必需字段
```hoi4
focus_tree = {
    id = {tag}_focus                    # 树ID
    country = { factor = 0; modifier = { add = 10 tag = {TAG} } }
    default = no                       # 是否通用树
}
```

### Focus 节点必需字段
```hoi4
focus = {
    id = {TAG}_focus_name              # 唯一ID
    icon = GFX_focus_generic           # 图标
    x = 0                              # 横坐标
    y = 0                              # 纵坐标
    cost = 10                          # 天数成本
}
```

### 常用可选字段
```hoi4
# 前置条件
prerequisite = { focus = {parent_id} }

# 互斥焦点
mutually_exclusive = { focus = {other_id} }

# 可用条件
available = { tag = {TAG} has_stability > 0.5 }

# 完成效果
completion_reward = { add_political_power = 100 }

# 相对定位
relative_position_id = {parent_id}
x = -1  y = 1                         # 左下

# 内圈焦点
inner_circle = yes

# 连续焦点
continuous = yes
```

---

## 💡 Ideas 核心字段

### 国家精神
```hoi4
ideas = {
    country = {
        {TAG}_spirit_name = {
            modifier = {
                political_power_gain = 0.10
                stability_factor = 0.05
            }
            removal_cost = -1          # 永久
        }
    }
}
```

### 顾问
```hoi4
political_advisor = {
    {TAG}_advisor_name = {
        picture = GFX_idea_generic
        cost = 150
        modifier = { neutrality_drift = 0.10 }
        trait = { inspiring_figure }
    }
}
```

---

## 🎲 Events 核心字段

### 国家事件
```hoi4
add_namespace = {tag}_events

country_event = {
    id = {tag}_events.1
    title = {tag}_events.1_title
    desc = {tag}_events.1_desc
    
    is_triggered_only = yes
    
    option = {
        name = {tag}_events.1_option_a
        add_political_power = 50
    }
}
```

### 常用触发器
```hoi4
tag = {TAG}                           # 国家标签
has_stability > 0.5                   # 稳定度
has_war_support > 0.3                 # 战争支持度
has_political_power > 50             # 政治点数
has_government = fascism              # 意识形态
controls_state = 123                  # 控制省份
has_completed_focus = {id}           # 完成焦点
has_country_flag = {flag}            # 国家标记
date > 1936.1.1                      # 日期条件
```

---

## 📝 Localisation 格式

### YML 文件格式
```yaml
l_english:
 {id}:0 "Display Name"
 {id}_desc:0 "Description text..."

l_simp_chinese:
 {id}:0 "显示名称"
 {id}_desc:0 "描述文本..."
```

### 常用颜色代码
```yaml
§R 红色 §!          §G 绿色 §!
§B 蓝色 §!          §Y 黄色 §!
§H 高亮 §!          §! 结束颜色
```

### 常用图标
```yaml
£pol_power 政治点数    £stability 稳定度
£manpower 人力         £civilian_factory 民工
£military_factory 军工 £research_research 科技
```

---

## 🔧 常用效果

### 政治效果
```hoi4
add_political_power = 100
add_stability = 0.05
add_war_support = 0.05
set_politics = { ruling_party = fascism }
```

### 军事效果
```hoi4
army_experience = 25
add_manpower = 50000
create_wargoal = { type = annex_everything target = GER }
```

### 经济效果
```hoi4
add_tech_bonus = { name = bonus_id bonus = 1.0 uses = 1 }
add_resource = { type = steel amount = 24 state = 762 }
```

### 民族精神
```hoi4
add_ideas = {spirit_id}
remove_ideas = {spirit_id}
add_timed_idea = { idea = {id} days = 365 }
```

### 标记操作
```hoi4
set_country_flag = {flag_name}
clr_country_flag = {flag_name}
set_global_flag = {flag_name}
```

---

## 🎨 布局速查

### 推荐间距
| 场景 | x间距 | y间距 |
|------|-------|-------|
| 单分支 | ±1 | +1 |
| 多分支 | ±2 | +1 |
| 互斥链 | ±1 | +1 |
| 复杂树 | ±3~4 | +2 |

### 坐标规则
- ✅ y值必须递增（子节点 > 父节点）
- ✅ x值可正可负（负左正右）
- ✅ 使用relative_position_id便于重构
- ❌ 避免绝对坐标（除根节点外）

---

## ⚠️ 常见错误

### 编码问题
- ❌ 本地化文件必须 UTF-8 带 BOM
- ✅ 其他文件 UTF-8 无 BOM

### ID 命名
- ✅ 使用国家前缀：`{TAG}_focus_name`
- ✅ 语义化命名：`political_reform`, `industrial_expansion`
- ❌ 避免纯数字或特殊字符

### 作用域
- `ROOT` = 效果执行者
- `FROM` = 效果触发者（如事件的发送方）
- `THIS` = 当前上下文对象

---

## 📚 文件位置速查

```
{mod}/
├── common/
│   ├── national_focus/*.txt        # 国策树
│   ├── ideas/*.txt                 # 民族精神
│   ├── characters/*.txt            # 人物
│   └── decisions/*.txt             # 决议
├── events/*.txt                    # 事件
└── localisation/
    ├── english/*_l_english.yml     # 英文
    └── simp_chinese/*_l_simp_chinese.yml  # 中文
```

---

## 🔍 调试命令

```
-debug          # 启用调试模式
debug_yesmen    # AI 接受所有请求
tdebug          # 显示调试信息
error           # 打开错误日志
```

**错误日志位置**：
```
C:\Users\{用户名}\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log
```

---

**完整文档**: `SKILL.md` | **详细示例**: `examples/` | **原版参考**: `references/vanilla_focus_trees/`
