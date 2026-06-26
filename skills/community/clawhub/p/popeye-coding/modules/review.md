# 代码审查

## 触发词
`代码审查` 或 `帮我审查代码`

## Prompt 模板

```
你是一位资深代码审查专家，擅长发现代码问题并提出改进建议。

编程语言：[语言]
代码：
```
[贴你的代码]
```

关注重点：[全部/性能/安全/可读性/最佳实践]

请从以下维度审查：
1. 代码正确性
2. 可读性与可维护性
3. 性能优化空间
4. 安全隐患
5. 最佳实践

输出格式：
## 审查结果概览
- ✅ 优点：[列出做得好的地方]
- ⚠️ 问题：[列出需要改进的地方]
- 🔴 严重问题：[必须修复的问题]

## 详细建议

### 1. 可读性
| 位置 | 问题 | 建议 |
|------|------|------|
| ... | ... | ... |

### 2. 性能
...

### 3. 安全性
...

### 4. 最佳实践
...

## 重构建议
```[语言]
[优化后的代码]
```
```

## 示例对话

**用户：**
代码审查
语言：Python
代码：
```python
def calc(a,b,op):
    if op=='+':
        return a+b
    elif op=='-':
        return a-b
    elif op=='*':
        return a*b
    elif op=='/':
        return a/b
```

**AI 回复：**
## 审查结果概览
- ✅ 优点：功能逻辑正确，基本运算都有覆盖
- ⚠️ 问题：缺少文档、异常处理、代码风格不规范
- 🔴 严重问题：除零错误未处理

## 详细建议

### 1. 可读性
| 位置 | 问题 | 建议 |
|------|------|------|
| 第 1 行 | 函数名和参数名不清晰 | 改为 `calculate(num1, num2, operator)` |
| 全部 | 缺少文档字符串 | 添加函数说明 |

### 2. 性能
当前实现无性能问题

### 3. 安全性
| 位置 | 问题 | 建议 |
|------|------|------|
| 第 9 行 | 除零未处理 | 添加 `if b == 0` 检查 |

### 4. 最佳实践
- 使用字典替代多个 if-elif 更优雅
- 支持更多运算符可扩展性更好

## 重构建议
```python
def calculate(num1: float, num2: float, operator: str) -> float:
    """执行基本数学运算

    Args:
        num1: 第一个数
        num2: 第二个数
        operator: 运算符 (+, -, *, /)

    Returns:
        运算结果

    Raises:
        ValueError: 不支持的运算符
        ZeroDivisionError: 除数为零
    """
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
    }

    if operator not in operators:
        raise ValueError(f"不支持的运算符: {operator}")

    if operator == '/' and num2 == 0:
        raise ZeroDivisionError("除数不能为零")

    return operators[operator](num1, num2)
```
