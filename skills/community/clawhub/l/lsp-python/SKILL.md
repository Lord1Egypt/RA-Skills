---
name: lsp-python
description: "Python code quality checking and LSP integration using pylsp. Provides code diagnostics, completion, hover tips, and style analysis. Use when: checking Python errors/warnings, getting code completions, viewing function signatures, analyzing code quality, or fixing style issues."
---

# LSP Python 技能

使用 Python Language Server Protocol (LSP) 进行代码质量检查和智能分析。

## 快速开始

### 1. 检查代码问题

```bash
# 单个文件
python3 scripts/lsp-service.py check <文件路径>

# 批量检查 (推荐)
python3 scripts/check_python.py <文件或目录>

# 批量检查并自动修复
python3 scripts/check_python.py --auto-fix <文件或目录>
```

示例:
```bash
python3 scripts/lsp-service.py check my_script.py
python3 scripts/check_python.py src/
python3 scripts/check_python.py --auto-fix src/
```

### 2. 获取代码补全

```bash
python3 scripts/lsp-service.py complete <文件> <行号> <字符位置>
```

### 3. 查看符号信息

```bash
python3 scripts/lsp-service.py info <文件> <行号> <字符位置>
```

## 依赖

- **Python 3.x**
- **pylsp**: `pip install python-lsp-server`
- **可选插件**:
  - `pip install python-lsp-server[all]` - 完整插件集
  - `pip install pylsp-mypy` - 类型检查
  - `pip install pylsp-black` - black 格式化

## 核心功能

### 代码诊断 (check)

检查 Python 文件中的错误和警告:

- **pyflakes** - 代码错误检测 (未使用导入、未定义变量等)
- **pycodestyle** - PEP8 风格检查 (格式、行长、空白等)

输出示例:
```
⚠️ 第 3 行 [pyflakes]: 'os' imported but unused
⚠️ 第 6 行 [pycodestyle]: E302 expected 2 blank lines, found 1
✅ 没有发现问题
```

### 代码补全 (complete)

获取指定位置的代码补全建议:

```bash
python3 scripts/lsp-service.py complete script.py 5 10
```

输出:
```
补全建议:
  • json (模块)
  • jsonpatch (模块)
  • requests (模块)
```

### 悬停提示 (info)

查看函数签名、文档字符串等信息:

```bash
python3 scripts/lsp-service.py info script.py 10 5
```

### 跳转定义 (goto)

查找符号的定义位置:

```bash
python3 scripts/lsp-service.py goto script.py 15 10
```

## 自动修复代码问题

### 清理未使用的导入

```bash
pip install autoflake
autoflake --remove-all-unused-imports --in-place --recursive .
```

### 格式化代码

```bash
pip install black
black .
```

### 完整修复流程

```bash
# 1. 备份
cp -r project/ project.backup

# 2. 清理导入
autoflake --remove-all-unused-imports --in-place --recursive project/

# 3. 格式化
black project/

# 4. 验证
python3 scripts/lsp-service.py check project/main.py
```

## 诊断严重性级别

| 级别 | 代码 | 含义 |
|------|------|------|
| ❌ | 1 | Error (错误) |
| ⚠️ | 2 | Warning (警告) |
| ℹ️ | 3 | Information (信息) |
| 💡 | 4 | Hint (提示) |

## 常见问题代码

| 代码 | 含义 | 修复方法 |
|------|------|----------|
| E402 | 导入不在文件顶部 | 移动导入到文件开头 |
| E501 | 行太长 (>79 字符) | 拆分长行或使用括号 |
| W293 | 空行包含空白字符 | 删除行尾空格 |
| E302 | 缺少空行 | 函数/类定义前加 2 个空行 |
| E712 | 布尔比较风格 | `if x is True` → `if x` |

## 在 OpenClaw 中使用

```bash
exec: python3 /path/to/lsp-python/scripts/lsp-service.py check <file>
```

## 批量检查项目

```bash
# 检查所有 Python 文件
find . -name "*.py" -exec python3 scripts/lsp-service.py check {} \;

# 仅显示有问题的文件
for f in $(find . -name "*.py"); do
  result=$(python3 scripts/lsp-service.py check "$f" 2>&1)
  if ! echo "$result" | grep -q "✅ 没有发现问题"; then
    echo "=== $f ==="
    echo "$result"
  fi
done
```

## 参考资料

- **LSP 协议详解**: 见 `references/lsp-protocol.md`
- **pylsp 配置**: 见 `references/pylsp-config.md`
- **代码风格指南**: 见 `references/pep8-guide.md`

## 故障排除

### pylsp 无法启动

```bash
# 检查安装
which pylsp
pylsp --version

# 重新安装
pip install --upgrade python-lsp-server
```

### 检查超时

增加脚本中的 `LSP_TIMEOUT` 值 (默认 10 秒)。

### 中文字符问题

确保文件使用 UTF-8 编码，脚本已设置 `ensure_ascii=False`。
