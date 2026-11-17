# 发布失败映射表

## 1. 工作流解析失败

常见表现：

- `Invalid workflow file`
- reusable workflow `uses:` 找不到 ref

先看：

- workflow 文件的 `uses:` 引用
- ref 是否真实存在
- 本地 YAML 是否可解析

## 2. 发布命令没跑到

常见表现：

- workflow 成功启动，但 publish job 没执行
- 条件判断导致 job 被 skip

先看：

- `if:` 条件
- 触发分支
- `paths` 是否覆盖 skill 目录

## 3. owner 或 token 问题

常见表现：

- 无法正式发布
- token 没传入 publish 层

先看：

- `CLAWHUB_OWNER`
- `CLAWHUB_TOKEN`
- secrets 是否透传到 reusable workflow

## 4. skill 命名问题

常见表现：

- slug 被拒
- 使用受保护前缀

先看：

- skill 目录名
- `name`
- owner / slug 是否组合合理

## 5. 假失败

常见表现：

- Actions 红灯
- registry 实际已接受或已同步

先看：

- `inspect` 结果
- 公开页
- workflow 是否把 `pending-publication` 或 `unchanged` 当失败
