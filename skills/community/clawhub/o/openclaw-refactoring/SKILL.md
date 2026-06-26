---
name: refactoring
description: Automated refactoring assistant. Performs safe code transformations including rename, extract method, inline variable, and move code. Provides refactoring suggestions and performs batch operations with preview and undo support.
---

# Refactoring

自动化重构助手，执行安全的代码转换，包括重命名、提取方法、内联变量、移动代码等。

**Version**: 1.0  
**Features**: 安全重构、批量操作、预览模式、撤销支持

---

## Quick Start

### 1. 重命名符号

```bash
# 重命名函数
python3 scripts/main.py rename --symbol "old_func" --to "new_func" src/

# 重命名类
python3 scripts/main.py rename --symbol "OldClass" --to "NewClass" --type class src/
```

### 2. 提取方法

```bash
# 提取选中的代码为新函数
python3 scripts/main.py extract --file src/main.py --lines 10-25 --name "new_helper"
```

### 3. 重构建议

```bash
# 获取重构建议
python3 scripts/main.py suggest src/main.py
```

### 4. 批量重构

```bash
# 批量重命名（预览模式）
python3 scripts/main.py batch-rename --pattern "get_(\w+)" --to "fetch_\1" src/ --dry-run

# 确认后执行
python3 scripts/main.py batch-rename --pattern "get_(\w+)" --to "fetch_\1" src/
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `rename` | 重命名符号 | `rename --symbol X --to Y src/` |
| `extract` | 提取方法 | `extract --file X --lines 10-20 --name Y` |
| `inline` | 内联变量/函数 | `inline --symbol X src/` |
| `move` | 移动代码 | `move --symbol X --to file.py` |
| `suggest` | 重构建议 | `suggest src/` |
| `batch-rename` | 批量重命名 | `batch-rename --pattern X --to Y src/` |

---

## Safety Features

### 预览模式 (--dry-run)

所有修改默认预览，不实际执行：

```bash
python3 scripts/main.py rename --symbol "foo" --to "bar" src/ --dry-run
# 显示将要修改的文件和内容

# 确认后执行（去掉 --dry-run）
python3 scripts/main.py rename --symbol "foo" --to "bar" src/
```

### 自动备份

每次重构自动创建备份：

```
.refactoring/backup/2026-04-01_175930/
├── src/main.py.bak
└── src/utils.py.bak
```

### 撤销操作

```bash
# 撤销上一次重构
python3 scripts/main.py undo

# 撤销特定备份
python3 scripts/main.py undo --backup 2026-04-01_175930
```

---

## Refactoring Types

### Rename（重命名）

```bash
# 重命名函数
python3 scripts/main.py rename --symbol "calculate_total" --to "compute_total" src/

# 重命名变量
python3 scripts/main.py rename --symbol "data" --to "user_data" --type var src/

# 重命名类
python3 scripts/main.py rename --symbol "UserManager" --to "UserService" --type class src/
```

支持：
- 智能识别符号类型
- 处理作用域冲突
- 更新所有引用
- 保留原始注释

### Extract Method（提取方法）

```bash
# 提取代码块为新方法
python3 scripts/main.py extract \
  --file src/main.py \
  --lines 45-67 \
  --name "process_payment" \
  --target-class PaymentProcessor
```

支持：
- 自动识别参数
- 处理返回值
- 提取到类或模块级别

### Inline（内联）

```bash
# 内联变量
python3 scripts/main.py inline --symbol "temp_var" src/

# 内联函数
python3 scripts/main.py inline --symbol "helper_func" --type function src/
```

### Move（移动）

```bash
# 移动函数到新文件
python3 scripts/main.py move --symbol "utility_func" --to src/utils/helpers.py

# 移动类方法到另一个类
python3 scripts/main.py move --symbol "method_name" --from-class A --to-class B
```

---

## Suggestions（重构建议）

自动检测代码坏味道并提供重构建议：

```bash
python3 scripts/main.py suggest src/
```

检测的坏味道：
- **Long Method** - 方法过长
- **Large Class** - 类过大
- **Duplicate Code** - 重复代码
- **Long Parameter List** - 参数过多
- **Feature Envy** - 特性依恋
- **Switch Statements** - 复杂条件

输出示例：
```
🔍 Refactoring Suggestions for src/main.py

⚠️  Long Method: "process_order" (85 lines)
   💡 Extract into smaller methods
   📍 Line 45-130

⚠️  Duplicate Code: Similar logic in 3 places
   💡 Extract common functionality
   📍 src/utils.py:23, src/order.py:45, src/payment.py:78

⚠️  Large Class: "OrderManager" (650 lines, 15 methods)
   💡 Split into OrderService, PaymentHandler, ShippingManager
```

---

## Batch Operations（批量操作）

### 批量重命名

```bash
# 将所有 get_* 函数重命名为 fetch_*
python3 scripts/main.py batch-rename \
  --pattern "get_(\w+)" \
  --to "fetch_\1" \
  --type function \
  src/
```

### 批量移动

```bash
# 将所有工具函数移动到 utils 模块
python3 scripts/main.py batch-move \
  --pattern "util_\w+" \
  --to src/utils/helpers.py \
  src/
```

---

## Configuration

`.refactoring.json`:

```json
{
  "backup": true,
  "backup_dir": ".refactoring/backup",
  "preview": true,
  "ignore": [
    "tests/**",
    "vendor/**"
  ],
  "rules": {
    "max_function_lines": 30,
    "max_class_lines": 300,
    "max_parameters": 5
  }
}
```

---

## Git 集成

```bash
# 重构前自动 stash
git stash

# 执行重构
python3 scripts/main.py rename --symbol "X" --to "Y" src/

# 查看变更
git diff

# 提交重构
git add .
git commit -m "refactor: rename X to Y"
```

---

## Supported Languages

| 语言 | 重命名 | 提取方法 | 内联 | 移动 | 建议 |
|------|--------|----------|------|------|------|
| Python | ✅ | ✅ | ⚠️ | ⚠️ | ✅ |
| JavaScript | ⚠️ | ⚠️ | ❌ | ❌ | ⚠️ |

---

## Examples

### 场景 1：清理代码

```bash
# 1. 获取重构建议
python3 scripts/main.py suggest src/

# 2. 重命名不清晰的变量
python3 scripts/main.py rename --symbol "d" --to "user_data" src/

# 3. 提取长方法
python3 scripts/main.py extract --file src/main.py --lines 50-90 --name "validate_input"

# 4. 移除重复代码
python3 scripts/main.py suggest --detect-duplicates src/
```

### 场景 2：API 迁移

```bash
# 批量重命名旧 API
python3 scripts/main.py batch-rename \
  --pattern "legacy_(\w+)" \
  --to "new_\1" \
  src/
```

---

## Files

```
skills/refactoring/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── rename.py               # 重命名引擎
    ├── extract.py              # 提取方法
    ├── suggest.py              # 重构建议
    └── utils.py                # 工具函数
```

---

## Safety First

⚠️ **重要提示**

1. 始终在 Git 仓库中操作
2. 先使用 `--dry-run` 预览
3. 确保测试通过后再提交
4. 大型重构分步执行

---

## Roadmap

- [x] 重命名符号（Python）
- [ ] 提取方法（Python）
- [ ] 内联变量（Python）
- [ ] 移动代码
- [ ] 重构建议
- [ ] JavaScript 支持
- [ ] IDE 集成
