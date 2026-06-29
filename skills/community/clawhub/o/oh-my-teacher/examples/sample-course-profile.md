# 示例课程快照

以下是一个填写完整的 `Current Course Snapshot` 示例，供用户理解各字段含义。

```markdown
## Current Course Snapshot
- **Course**: 数据结构与算法 / Computer Science
- **Assessment**: 机考（闭卷，2小时，OJ自动评测）
- **Days left**: 7
- **Level**: shaky（基础题能做，综合题经常超时或WA）
- **Environment**: agent-shell
- **Materials**: 课件PPT（12章全）、实验报告x4、往年OJ题库x3套、老师划重点录音（文字稿）
- **LaTeX**: not applicable
- **Weak points**: [图论-Dijkstra堆优化, 动态规划-状态设计, 并查集-路径压缩]
- **Completed**: [线性表, 栈与队列, 二叉树基础遍历, 排序算法]
- **Accuracy**: "8/10 on sorting, 4/10 on graph shortest path, 2/5 on DP"
- **Last action**: /fix on Dijkstra with negative-weight confusion
- **Next recommended**: /quiz on DP state design (interval DP, knapsack variant)
```

## 字段说明

| 字段 | 含义 | 更新时机 |
|------|------|----------|
| **Course** | 课程名 + 学科大类 | `/profile` 或课程切换时 |
| **Assessment** | 考试形式（笔试/机考/口试/实验/开卷/闭卷） | `/profile` 或 `/paper` `/lab` 时 |
| **Days left** | 距离考试天数 | 用户提供或更新 |
| **Level** | 当前水平：beginner / shaky / basic ok / high-score / pass-only（后两项为目标声明） | 用户在 `/profile` 声明 |
| **Environment** | agent-shell / rag-notebook / plain-chat | 自动检测 |
| **Materials** | 已上传/可用的复习资料 | `/materials` 后更新 |
| **LaTeX** | 数学课程的公式渲染模式：rendered / plain-text / not applicable | 数学课程开始时用户指定 |
| **Weak points** | 薄弱知识点标签列表 | `/grade` `/quiz` `/fix` 后更新 |
| **Completed** | 本session已练习/掌握的主题 | 每次练习后追加 |
| **Accuracy** | 近期各主题正确率 | `/grade` 后更新 |
| **Last action** | 上一次执行的命令 | 每次命令后更新 |
| **Next recommended** | 下一步建议（一个具体动作） | 每次任务结束后更新 |

## 多课程 juggling 示例

当用户同时复习多门课时，用 `/plan` 的 multi-course 模式：

```markdown
## Multi-Course Plan
| Course | Days Left | Difficulty | Weakness | Priority |
|--------|-----------|------------|----------|----------|
| 数学分析 | 14 | 高 | 证明题 | P1 |
| 数据结构 | 7 | 中 | DP/图论 | P2 |
| 英语 | 21 | 低 | 听力 | P3 |

今日建议：上午 2h 数据结构 DP 专题，下午 1.5h 数学分析极限证明。
```
