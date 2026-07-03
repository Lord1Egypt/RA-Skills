---
name: jiebang-file-process
description: 文件处理工具，提供文本哈希计算、Base64编解码、URL编解码功能。当用户提到计算MD5、SHA1、SHA256哈希、Base64编码解码、URL编码解码、文件哈希校验、文本加密哈希、URL编码转换等需求时使用此技能。
---

# 捷帮文件处理

文件处理工具，基于捷帮工具站API，提供文本哈希计算、Base64编解码、URL编解码功能。

## 何时使用

当用户有以下需求时触发本技能：
- 计算文本的MD5/SHA1/SHA256哈希值
- Base64编码或解码文本
- URL编码或解码特殊字符
- 文件内容哈希校验

## 工作流程

1. 确定用户需要的操作类型（hash/base64/url）
2. 调用对应的API接口
3. 返回处理结果

### 1. 哈希计算 (hash)

调用 `main.py` 的 `calc_hash` 函数：
- `data`: 要计算哈希的文本内容
- `algorithm`: 算法类型，可选 md5 / sha1 / sha256

### 2. Base64编解码 (base64)

调用 `main.py` 的 `base64_convert` 函数：
- `data`: 要处理的内容
- `action`: 操作类型，encode（编码）或 decode（解码）

### 3. URL编解码 (url)

调用 `main.py` 的 `url_convert` 函数：
- `data`: 要处理的内容
- `action`: 操作类型，encode（编码）或 decode（解码）

## 输出格式

所有操作返回JSON格式结果，包含处理后的数据和原始输入。
