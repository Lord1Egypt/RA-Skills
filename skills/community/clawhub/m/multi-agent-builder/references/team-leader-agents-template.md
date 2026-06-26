# AGENTS.md - {{LEADER_ID}}

## 团队成员
{{TEAM_DIRECTORY}}

## 通信与协作
- 控制平面：sessions_send / sessions_spawn
- 状态：accepted / blocked / done
- 回传闭环：所有子任务完成后必须回传给 {{LEADER_ID}}

## 输出规范
- 仅发送摘要 + 交付路径
- 大体量原始内容写入 shared 目录
- team-leader 接单后先创建英文任务目录：`shared/<task-slug-en>/`
- 所有中间与最终产物写入对应任务目录
- 修改文件前先备份到：`shared/<task-slug-en>/_backup/<UTC时间戳>/`

## 固定职责提醒
- {{LEADER_ID}} 只负责沟通、调度、汇总，不做 specialist 实现
