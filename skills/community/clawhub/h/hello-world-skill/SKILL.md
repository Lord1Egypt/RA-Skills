---
name: hello-world
description: 向用户返回Hello World问候，支持自定义名称
version: 1.0.0
metadata:
  openclaw:
    emoji: 👋
    requires:
      bins: [] # 无外部依赖
---
# Hello World Skill
## 触发方式
1. 命令格式：/hello-world [用户名]
2. 自然语言：“说一句Hello World”“跟XX打个招呼”

## 执行逻辑
1. 若用户传入用户名（如/hello-world 小明），返回“Hello 小明！👋”；
2. 若无用户名，返回“Hello World！👋”。

## 示例
- 输入：/hello-world
  输出：Hello World！👋
- 输入：/hello-world 豆包
  输出：Hello 豆包！👋