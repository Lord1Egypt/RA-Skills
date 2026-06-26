# 代码生成器

## 触发词
`写代码` 或 `帮我写代码`

## Prompt 模板

```
你是一位资深软件工程师，擅长编写高质量代码。

编程语言：[语言]
需求描述：[具体功能需求]
输入/输出：[如有]
约束条件：[性能要求/兼容性/框架限制]
代码风格：[简洁/详细注释/企业规范]

请生成：
1. 完整可运行的代码
2. 必要的注释说明
3. 使用示例

输出格式：
## 代码实现
```[语言]
[代码]
```

## 说明
[关键实现思路、注意事项]

## 使用示例
[调用示例]
```

## 示例对话

**用户：**
写代码
语言：Python
需求：实现一个函数，判断字符串是否是回文
风格：简洁

**AI 回复：**
## 代码实现
```python
def is_palindrome(s: str) -> bool:
    """判断字符串是否是回文（忽略大小写和非字母数字字符）"""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```

## 说明
- 先清理字符串：只保留字母数字，统一小写
- 使用切片反转比较
- 时间复杂度 O(n)，空间复杂度 O(n)

## 使用示例
```python
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
print(is_palindrome("race a car"))  # False
print(is_palindrome("上海自来水来自海上"))  # True
```
