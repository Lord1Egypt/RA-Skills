# HOI4 Modding 验证检查清单

> 在测试前手动检查的常见问题清单。

---

## ✅ 文件基础检查

### 编码检查
- [ ] 本地化文件(.yml)使用 **UTF-8 带 BOM**
- [ ] 其他文件(.txt)使用 **UTF-8 无 BOM**
- [ ] 文件头部无乱码字符

### 文件结构
- [ ] 所有文件在正确目录下
- [ ] 文件名无空格或特殊字符
- [ ] descriptor.mod 存在且格式正确

---

## 📝 语法检查

### 括号匹配
- [ ] 所有 `{` 都有对应 `}`
- [ ] 嵌套层级正确缩进
- [ ] 使用编辑器的括号高亮功能检查

**示例（正确）**：
```hoi4
focus = {
    id = test_focus
    completion_reward = {
        add_political_power = 100
    }
}
```

**示例（错误）**：
```hoi4
focus = {
    id = test_focus
    completion_reward = {
        add_political_power = 100
    }
    # 缺少闭合括号
```

### ID 唯一性
- [ ] 所有 focus ID 唯一
- [ ] 所有 ideas ID 唯一
- [ ] 所有事件 ID 唯一
- [ ] 无重复定义

**检查方法**：
```powershell
# 在 mod 目录下运行
Get-ChildItem -Recurse -Filter "*.txt" | Select-String "id\s*=" | Group-Object
```

### 字段拼写
- [ ] 所有字段名拼写正确
- [ ] 数值参数无拼写错误
- [ ] 布尔值使用 `yes` 或 `no`

---

## 🎯 国策树检查

### 坐标系统
- [ ] 所有焦点有 x 和 y 坐标
- [ ] 根节点使用绝对坐标
- [ ] 子节点使用 relative_position_id
- [ ] **y 值必须递增**（子节点 > 父节点）

### 前置关系
- [ ] 所有前置焦点 ID 存在
- [ ] prerequisite 语法正确
- [ ] 无循环依赖

**正确语法**：
```hoi4
prerequisite = { focus = parent_focus }
prerequisite = { focus = parent_focus1 focus = parent_focus2 }  # AND关系
```

### 互斥关系
- [ ] mutually_exclusive 双向声明
- [ ] 所有互斥焦点 ID 存在

**正确示例**：
```hoi4
# 焦点A
focus = {
    id = focus_a
    mutually_exclusive = { focus = focus_b }
}

# 焦点B
focus = {
    id = focus_b
    mutually_exclusive = { focus = focus_a }  # 双向声明
}
```

### 布局检查
- [ ] 图标不重叠（x间距至少 ±1）
- [ ] 连线不交叉（复杂情况用 x间距 ±2）
- [ ] 分支布局清晰

---

## 💡 Ideas 检查

### 类型定义
- [ ] ideas 类型正确（country/army/navy/air/political_advisor 等）
- [ ] 槽位限制正确（顾问类通常只有 1 个槽位）

### 条件逻辑
- [ ] `allowed` 只在定义时检查
- [ ] `visible` 控制是否显示
- [ ] `available` 控制是否可选
- [ ] 三者逻辑关系正确

**区别**：
```hoi4
allowed = { original_tag = POL }      # 定义时检查
visible = { has_war = yes }           # 显示条件
available = { has_political_power > 100 }  # 可选条件
```

### 图标
- [ ] GFX 引用存在
- [ ] 图片文件在正确位置
- [ ] 图片尺寸正确（通常 56x56）

---

## 🎲 事件检查

### 事件结构
- [ ] add_namespace 声明存在
- [ ] 事件 ID 格式正确（`命名空间.数字`）
- [ ] 所有 option 至少有一个

### 作用域
- [ ] `ROOT` 使用正确（事件接收方）
- [ ] `FROM` 使用正确（事件触发方）
- [ ] 随机作用域逻辑正确

**作用域示例**：
```hoi4
country_event = {
    id = poland_events.1
    
    option = {
        name = poland_events.1_option_a
        
        # ROOT = 波兰（事件接收方）
        add_political_power = 50
        
        # FROM = 德意志（事件触发方）
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = pol_ger_cooperation
            }
        }
    }
}
```

### 触发条件
- [ ] trigger 逻辑正确
- [ ] MTTH 计算合理
- [ ] mean_time_to_happen 配置正确

---

## 🌐 本地化检查

### 编码
- [ ] 文件使用 UTF-8 带 BOM
- [ ] 无乱码字符
- [ ] 引号使用正确

### 键值对
- [ ] 所有本地化键存在对应文本
- [ ] 格式为 `键:0 "文本"`
- [ ] 无重复键定义

**检查缺失键**：
```powershell
# 查找代码中的本地化键
Get-ChildItem -Recurse -Filter "*.txt" | Select-String "\w+_\w+" | ForEach-Object {
    $key = $_ -replace '.*?(\w+_\w+).*', '$1'
    $key
} | Sort-Object -Unique
```

### 颜色与图标
- [ ] 所有颜色代码正确闭合 `§!`
- [ ] 图标代码正确 `£icon`
- [ ] 格式化符号正确 `\n`

---

## 🔧 作用域检查

### 国家作用域
- [ ] `ROOT` - 效果执行者
- [ ] `FROM` - 效果触发者
- [ ] `THIS` - 当前上下文
- [ ] `PREV` - 上一个作用域

### 省份作用域
- [ ] 使用 `123 = { }` 格式
- [ ] 省份 ID 正确
- [ ] 效果适用正确（省份效果 vs 国家效果）

**常见错误**：
```hoi4
# 错误：省份效果用在国家作用域
add_political_power = 100
add_infrastructure = 1  # 这是省份效果

# 正确：先进入省份作用域
123 = {
    add_infrastructure = 1
}
add_political_power = 100  # 国家效果
```

---

## 📁 文件组织检查

### 目录结构
```
{mod}/
├── descriptor.mod              ✓
├── thumbnail.png               ✓ (推荐)
├── common/
│   ├── national_focus/         ✓
│   ├── ideas/                  ✓
│   ├── characters/             ✓
│   └── decisions/              ✓
├── events/                     ✓
└── localisation/
    ├── english/                ✓
    └── simp_chinese/           ✓
```

### 文件命名
- [ ] 使用小写字母和下划线
- [ ] 避免空格
- [ ] 有意义的名称

**推荐**：`{tag}_focus.txt`, `{tag}_ideas.txt`

---

## 🔍 错误日志检查

### 启用调试模式
1. Steam 启动选项添加：`-debug`
2. 游戏内按 `~` 打开控制台
3. 输入 `error` 查看错误日志

### 常见错误类型

| 错误信息 | 原因 | 解决 |
|---------|------|------|
| `Unknown effect: add_political_powr` | 拼写错误 | 修正为 `add_political_power` |
| `Missing }` | 括号不匹配 | 检查括号配对 |
| `Invalid focus ID: ger_focus_` | ID 不存在 | 检查 ID 拼写 |
| `Could not open file` | 编码错误 | 使用 UTF-8 |
| `Unknown trigger: taggg` | 拼写错误 | 修正为 `tag` |

### 错误日志位置
```
C:\Users\{用户名}\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log
```

---

## 📋 最终检查清单

在发布前检查：

### 功能性
- [ ] 所有焦点可完成
- [ ] 所有效果正确触发
- [ ] 事件链正常工作
- [ ] 决议可用
- [ ] 本地化显示正确

### 兼容性
- [ ] 无重复 ID（与原版或其他 mod）
- [ ] 不覆盖原版关键文件（除非有意）
- [ ] DLC 检查正确

### 平衡性
- [ ] 焦点成本合理
- [ ] 效果不过度强化
- [ ] 前置条件合理

### 用户体验
- [ ] 描述文本清晰
- [ ] 图标无重叠
- [ ] 无误导性提示

---

## 🛠️ 常用检查命令

### PowerShell 快速检查
```powershell
# 检查重复 ID
Get-ChildItem -Recurse -Filter "*.txt" | Select-String "id\s*=" | Group-Object | Where-Object { $_.Count -gt 1 }

# 检查括号匹配
Get-ChildItem -Recurse -Filter "*.txt" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $open = ($content.ToCharArray() | Where-Object { $_ -eq '{' }).Count
    $close = ($content.ToCharArray() | Where-Object { $_ -eq '}' }).Count
    if ($open -ne $close) {
        Write-Host "Bracket mismatch in: $($_.Name)"
    }
}

# 查找缺失的本地化键
$keys = Get-ChildItem -Recurse -Filter "*.txt" | Select-String "\w+_\w+" | ForEach-Object {
    $_ -replace '.*?(\w+_\w+).*', '$1'
} | Sort-Object -Unique

$localized = Get-ChildItem -Recurse -Filter "*.yml" | Get-Content

$keys | ForEach-Object {
    if ($localized -notmatch $_) {
        Write-Host "Missing localization: $_"
    }
}
```

---

## 📚 参考资源

- **完整文档**: `SKILL.md`
- **详细示例**: `examples/` 目录
- **原版参考**: `references/vanilla_focus_trees/`
- **快速参考**: `references/quick_reference.md`
- **代码片段**: `examples/snippet_library.md`

---

**提示**：保存此清单，每次创建新 mod 时逐项检查！
