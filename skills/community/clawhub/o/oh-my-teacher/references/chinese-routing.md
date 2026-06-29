# Chinese Natural-Language Routing

Use this file before asking the user to remember slash commands. If a phrase maps clearly to a command, route directly and briefly state the interpreted command.

| 用户说法 | Route |
|---|---|
| 老师说这些是重点 | `/teacher-emphasis` |
| 这些是老师划的重点 | `/teacher-emphasis` |
| 帮我看往年题怎么复习 | `/paper-analyze` |
| 分析这套卷子 | `/paper-analyze` |
| 整理错题 | `/wrong-note` |
| 做个错题本 | `/wrong-note` |
| 我这题哪里错了 | `/grade` |
| 给我出几道类似题 | `/fix` or `/quiz` |
| 今天该复习什么 | `/review-due` or `/dashboard` |
| 把知识库资料变成计划 | `/materials -> /source-map -> /plan` |
| 把这些资料变成复习计划 | `/materials -> /source-map -> /plan` |
| 做考前速记 | `/last-page` |
| 最后一页复习 | `/last-page` |
| 生成复习 PPT | `/last-page -> /ppt` |
| 做一个考前速记 PPT | `/last-page -> /ppt` |
| 做阶段复盘报告 | `/dashboard -> /report` |
| 我还有三天考试，救一下 | `/cram` |
| 帮我复习知识库里的这门课 | `/profile -> /materials -> /source-map` |
| 建一个课程主页 | `/profile` with ima-note |

## Routing Rules

- In ima, prefer note and knowledge-base workflows when the user mentions 知识库, 笔记, 课程主页, 错题本, 老师划重点, or 往年题.
- If the phrase implies multiple steps, create a `task_plan` in ima and execute the first useful step.
- If confidence is below 0.7, ask one compact `ask_user` question instead of listing commands.
