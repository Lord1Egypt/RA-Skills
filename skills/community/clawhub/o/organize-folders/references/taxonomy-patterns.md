# 分类模型

分类建模由场景模型、方法模型和生命周期模型组成。

## 场景模型

| 场景 | 适合结构 |
|---|---|
| 个人电脑 | inbox / documents / media / software / archive / backup |
| 学习资料 | projects / resources / knowledge / archive |
| 开发者工作区 | projects / areas / resources / software / archive |
| 家庭/NAS | documents / media / resources / archive / backup |
| 混合磁盘 | inbox / projects / areas / resources / knowledge / documents / media / software / archive / backup |

## 方法模型

### IRK

用来判断内容的价值密度和处理方式：

- Information：过程性材料，跟随任务或项目。
- Resource：可复用资料，进入资源库。
- Knowledge：提炼后的知识，进入知识库。

### PARA

用来判断行动状态：

- Projects：当前项目。
- Areas：长期责任领域。
- Resources：未来可能有用的资源。
- Archives：已完成或不再活跃的内容。

### 时间模型

用来组织归档、凭证、照片、会议资料、学习批次和备份快照。

常用格式：

```text
YYYY
YYYY-MM
YYYY-MM-DD_topic
YYYY-Q1_topic
```

## 生命周期模型

| 状态 | 处理 |
|---|---|
| 收件箱 | 暂存新文件，定期清理 |
| 使用中 | 保留在项目、领域或当前工作目录 |
| 已完成 | 进入归档判断 |
| 归档 | 保留未来查询 |
| 备份 | 作为恢复副本 |
| 删除候选 | 进入待确认清单 |

## 推荐组合

| 使用区域 | 推荐组合 |
|---|---|
| 整个磁盘 | 场景模型 + 生命周期模型 |
| 工作区 | PARA Projects + Archives |
| 笔记库 | IRK Knowledge + PARA Areas |
| 资料库 | IRK Resources + 主题分类 |
| 报销合同 | 时间模型 + documents |
| 照片视频 | 时间模型 + media |
| 备份 | 时间快照 + backup |

