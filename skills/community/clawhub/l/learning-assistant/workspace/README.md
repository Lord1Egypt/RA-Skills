# workspace/

此目录用于存放 **Learning Assistant 在运行时自动生成和维护的数据文件**。

> 首次使用时此目录为空，属于正常状态。第一次会话结束后会自动生成对应文件。

## 文件说明

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `USER_PROFILE.md` | 持久化 | 用户画像：技术栈、学习目标、成长历史。首次会话时由初始化问卷生成。 |
| `LEARNING_INDEX.md` | 持久化 | 全局学习索引：文件目录、标签云、艾宾浩斯复习时间表。首次会话结束时自动创建。 |
| `YYYYMMDD_ANCHOR_[主题].md` | 会话锚点 | 会话断点文件，用于跨会话恢复进度。 |
| `YYYYMMDD_PLAN_[主题].md` | 学习产物 | 学习计划 |
| `YYYYMMDD_SUMMARY_[主题].md` | 学习产物 | 知识总结笔记 |
| `YYYYMMDD_CONFUSION_[主题].md` | 学习产物 | 疑惑记录 |
| `YYYYMMDD_MISTAKE_[主题].md` | 学习产物 | 错题本 |
| `YYYYMMDD_FLASH_[主题].md` | 学习产物 | 知识卡片 |
| `YYYYMMDD_INTERVIEW_[主题].md` | 学习产物 | 面试题库 |
| `YYYYMMDD_CODE_[主题].md` | 学习产物 | 代码笔记 |
| `YYYYMMDD_REVIEW_[主题].md` | 学习产物 | 复盘报告 |

## 命名规范

所有生成文件严格遵循：`YYYYMMDD_[类型]_[主题].md`

**请勿手动删除 `USER_PROFILE.md` 和 `LEARNING_INDEX.md`**，否则学习进度和复习计划将全部丢失。
