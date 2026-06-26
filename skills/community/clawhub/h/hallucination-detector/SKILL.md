---
name: hallucination-detector
description: 幻觉检测器 - 原创技能。检测AI生成代码中的幻觉内容，包括不存在的API、错误的参数、虚假引用等。适用于代码审查、AI编程辅助、质量保证等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [hallucination, detection, code-quality, verification, safety]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 检测逻辑完整
- [x] 幻觉类型覆盖全
- [x] 验证流程明确
- [x] 无语法错误

---

# Hallucination Detector - 幻觉检测器

> 原创技能 | 激活词: 检测幻觉 / 验证代码 / 代码审查

## 核心问题

AI生成的代码可能出现"幻觉"：
- 调用不存在的API
- 使用错误的参数
- 引用不存在的文档
- 混淆相似的库名称
- 虚构函数签名

## 幻觉类型分类

### 类型1: API幻觉

```python
# ❌ 幻觉: 不存在的API
response = requests.get_json(url)  # 应该是 response.json()

# ❌ 幻觉: 错误的方法
list.append_many([1,2,3])  # 应该是 extend()

# ❌ 幻觉: 不存在的参数
df.sort('column', ascending=True)  # pandas 2.x 应该用 by= 参数
```

### 类型2: 版本幻觉

```python
# ❌ 幻觉: 版本不兼容
# React 19 不需要 forwardRef 了

# ❌ 幻觉: 过时的API
requests.post(url, data={})  # 应该用 json={}
```

### 类型3: 引用幻觉

```python
# ❌ 幻觉: 不存在的文档
# 参见: https://fake-docs-example.com  (虚构链接)

# ❌ 幻觉: 不存在的库
import super_fake_library  # 未发布的库
```

### 类型4: 类型幻觉

```python
# ❌ 幻觉: 错误的类型假设
def func(x: str) -> str:
    return x.append('a')  # str没有append方法

# ❌ 幻觉: 类型不匹配
result = await promise.json()  # promise是Promise对象���不是Response
```

### 类型5: 逻辑幻觉

```python
# ❌ 幻觉: 不可能的逻辑
if user.is_admin and not user.is_admin:  # 自相矛盾
    return "impossible"

# ❌ 幻觉: 永远为真的条件
if x == x:  # 总是True
    pass
```

## 检测策略

### 1. 静态分析

```python
def static_check(code: str) -> list[Hallucination]:
    issues = []
    
    # 检查不存在的API调用
    for call in extract_api_calls(code):
        if not api_exists(call):
            issues.append(Hallucination(
                type='api',
                location=call.location,
                message=f"API '{call.name}' 不存在"
            ))
    
    # 检查类型错误
    for type_check in extract_type_checks(code):
        if not type_compatible(type_check):
            issues.append(Hallucination(
                type='type',
                location=type_check.location,
                message=f"类型不匹配: {type_check.expected}"
            ))
    
    return issues
```

### 2. 引用验证

```python
def verify_references(code: str) -> list[Hallucination]:
    issues = []
    
    for ref in extract_urls_and_docs(code):
        if not url_exists(ref):
            issues.append(Hallucination(
                type='reference',
                location=ref.location,
                message=f"URL不存在或无法访问: {ref.url}"
            ))
    
    for lib in extract_imports(code):
        if not package_exists(lib):
            issues.append(Hallucination(
                type='package',
                location=lib.location,
                message=f"包 '{lib.name}' 不存在"
            ))
    
    return issues
```

### 3. 逻辑验证

```python
def logical_check(code: str) -> list[Hallucination]:
    issues = []
    
    for expr in extract_conditions(code):
        if is_contradiction(expr):
            issues.append(Hallucination(
                type='logic',
                location=expr.location,
                message="逻辑矛盾或永真条件"
            ))
    
    return issues
```

## 完整检测流程

```
1. 代码输入
      ↓
2. 静态分析 (API/类型检查)
      ↓
3. 引用验证 (URL/包检查)
      ↓
4. 逻辑验证 (矛盾/永���检查)
      ↓
5. 综合报告
      ↓
6. 修复建议
```

## 输出格式

```markdown
## 幻觉检测报告

### 检测结果: 发现 3 处幻觉 ⚠️

### 幻觉 #1 [高危]
- **类型**: API幻觉
- **位置**: line 15
- **代码**: `response.get_json()`
- **问题**: 方法名错误
- **建议**: 改为 `response.json()`

### 幻觉 #2 [中危]
- **类型**: 版本兼容
- **位置**: line 23
- **代码**: `forwardRef(...)`
- **问题**: React 19 已废弃
- **建议**: 直接使用 ref 作为 prop

### 幻觉 #3 [低危]
- **类型**: 引用幻觉
- **位置**: line 45
- **代码**: `https://docs.example.com/fake`
- **问题**: URL可能不存在
- **建议**: 验证链接或移除

### 置信度评估
- 综合置信度: 0.92
- 误报率预估: <5%
```

## 置信度计算

| 检测类型 | 基础置信度 | 调整因素 |
|----------|-----------|----------|
| API检查 | 0.85 | +0.1 静态可验证 |
| 版本检查 | 0.70 | +0.1 版本明确 |
| 引用检查 | 0.80 | +0.1 可实际验证 |
| 逻辑检查 | 0.75 | +0.1 模式明确 |

## 集成建议

配合其他技能使用：

| 配合技能 | 效果 |
|---------|------|
| workflow-verifier | 执行前验证代码 |
| karpathy-principles | 确保代码简洁可验证 |
| entropy-manager | 控制验证流程熵 |

## 原创性声明

本技能为原创，融合了：
- 静态代码分析
- API签名验证
- 引用完整性检查
- 逻辑矛盾检测

---

**作者**: laosi
**创建日期**: 2026-04-28