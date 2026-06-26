---
name: github-trending
description: 运行GitHub热榜脚本，获取项目名称和简介并翻译成中文
trigger: /github-trending
---

# /github-trending

获取GitHub热榜Top 10项目，并将项目名称和简介翻译成中文。

## 使用方式

```
/github-trending                          # 获取今日热榜并翻译
```

## 执行步骤

### Step 1 - 运行GitHub热榜脚本

在当前skill目录下运行脚本：

```bash
cd github-trending && python github-trending.py
```

将输出保存，用于后续翻译。

### Step 2 - 翻译项目信息

将脚本输出的每个项目名称和简介翻译成准确且符合中文语言习惯的中文。

### Step 3 - 输出结果

以如下格式输出最终结果：

```
🔥 GitHub 今日趋势榜 Top 10

1. [翻译后的项目名称]
   简介: [翻译后的中文简介]

2. [翻译后的项目名称]
   简介: [翻译后的中文简介]

... (共10条)
```
