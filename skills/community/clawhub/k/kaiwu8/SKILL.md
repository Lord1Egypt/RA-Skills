---
name: kaiwu8
description: 开悟吧平台型 Skill - 管理并激活已购功能。用户说"开悟吧"时执行 activate.py 脚本。
---

# 开悟吧 kaiwu8

> 用户只需要安装这一个 skill，所有功能从这里激活

## 触发条件

用户说：**"开悟吧"**

## 执行步骤

1. 运行 activate.py
2. 系统自动调 API 检查已购功能
3. 未激活的功能自动执行激活
4. 缺失的 skill 从 ClawHub 下载

## 配置

在 openclaw.json 的 skills.entries.kaiwu8 中配置：

```json
"kaiwu8": {
  "api_endpoint": "https://api.kaiwu8.com",
  "user_api_key": "你的user_api_key"
}
```
