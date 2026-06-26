---
name: heimaosearch
description: 用于搜索活动策划、方案、资源及案例的工具，与公关、活动有关的内容都可以使用。
---

# 使用场景

当用户想查询以下内容时，必须使用该工具：
- 节日活动（如中秋、春节、开业）
- 活动策划方案
- 执行资源（舞台、灯光、物料等）
- 活动案例

---

# 用户配置（首次使用需填写）

用户需要提供：
- account：黑猫会账号
- open_api_key：黑猫会开放API-Key

---

# 调用逻辑

当用户输入问题时：

1. 将用户输入作为 content
2. 将 account 和 open_api_key 一起提交
3. 调用接口：

POST https://api.heimaohui.com/index/search/recommendOpenClaw

请求参数：

{
  "account": "{{account}}",
  "open_api_key": "{{open_api_key}}",
  "content": "{{input}}"
}

---

# 返回处理规则

## 如果 code != 0：
直接返回 msg

---

## 如果 code == 0：

data 格式：

{
  "scheme":[{"title":"xxx","url":"http://xxx"}],
  "resource":[{"title":"xxx","url":"http://xxx"}],
  "sample":[{"title":"xxx","url":"http://xxx"}],
  "summary":"xxx"
}

---

# 输出格式（必须遵守）

## 🔹 方案推荐
- [title](url)

## 🔹 资源推荐
- [title](url)

## 🔹 案例参考
- [title](url)

## 🔹 分析总结
直接输出 summary 内容

---

# 注意

- 所有 title 必须可点击（markdown链接）
- 没有内容的分类可以省略
- summary 必须完整返回