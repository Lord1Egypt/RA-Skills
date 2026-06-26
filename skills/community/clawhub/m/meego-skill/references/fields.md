# 你的项目名称 工作项字段配置参考

## 项目信息
- **project_key**: `你的project_key`
- **simple_name**: `your_simple_name`
- **名称**: 你的项目名称

## 工作项类型与状态值

### issue（缺陷管理）

**状态选项**（`work_item_status` 字段）：
| option_id | option_name |
|-----------|------------|
| OPEN | 开始 |
| IN PROGRESS | 待确认 |
| REPAIRING | 待修复 |
| IN REPAIRING | 修复中 |
| RESOLVED | 已修复 |
| VERIFYING | 验证中 |
| REOPENED | 重新打开 |
| CLOSED | 已关闭 |
| REJECTED | 拒绝 |
| ABONDONED | 废弃 |
| ugugjneny | 挂起 |
| systemEnded | 已终止 |

**优先级选项**（`priority` 字段）：
| option_id | option_name |
|-----------|------------|
| 0 | 最高 |
| 1 | 高 |
| 2 | 中 |
| 99 | 低 |

**严重程度选项**（`severity` 字段）：
| option_id | option_name |
|-----------|------------|
| 1 | 致命 |
| 2 | 严重 |
| 3 | 一般 |
| 4 | 轻微 |

**发现阶段选项**（`issue_stage` 字段）：
| option_id | option_name |
|-----------|------------|
| stage_verify | UI/UE/PM验收 |
| stage_lr | UI/UE/PM内部LR |
| stage_test | 测试阶段 |
| 79a_7h2yn | UAT阶段 |
| stage_smoke | 冒烟测试 |
| stage_first | 第一轮测试 |
| stage_second | 第二轮测试 |
| stage_regression | 回归阶段 |
| stage_grey | 灰度阶段 |
| stage_online | 线上阶段 |

**缺陷类型选项**（`field_f76015` 字段）：
| option_id | option_name |
|-----------|------------|
| rrq3w4u7s | 代码问题 |
| y07z_i298 | 需求问题 |
| 7nsesnobz | 配置问题 |
| ugiu8978f | 性能问题 |
| nn552_cgn | 操作类问题 |
| c9c12dt5g | 数据问题 |
| lseoub8lq | 安全问题 |
| km3p85d37 | 环境问题 |
| 4fkex5l5z | 数据库问题 |
| l9qsajbsq | UI问题 |
| zbyeffk23 | 代码走查 |
| 223b5dwq_ | 合并代码问题 |
| rx0z7oyct | 其它 |
| in9koxuav | 研发失误 |

**Bug端分类**（`bug_classification` 字段）：
| option_id | option_name |
|-----------|------------|
| ios | iOS |
| android | Android |
| fe | FE |
| server | Server |

**业务线**（`business` 字段）：
| option_id | option_name |
|-----------|------------|
| 6581475ff2298bcc795df352 | 户用业务 |
| 65814766176b6187c076fc48 | 机构业务 |
| 65814774f81e60a43ef5494c | 供应链 |
| 6581477c7d13f1093802588c | 数据产品 |
| 6581478bc02fb4569c5fe09c | 电站运维 |
| 658147abe649df8012042ac0 | 财务 |
| 65977758b8e755d0b84eadaf | 商用业务 |
| 65d5afca1e4903efc37f16ad | 海外业务 |
| 65d5afd560cdebec977251db | 市场 |
| 65d5afe7cd525ff7061056dc | 工程质量 |
| 65d5affd60cdebec977251dc | 人力发展 |
| 65d5b00ce1137915b2dba86a | 技术管理 |

**开发小组**（`field_f0fb17` 字段）：
| option_id | option_name |
|-----------|------------|
| 9wav0lvd6 | 前端 - APP组 |
| 0pd4dntdi | 前端 - Web1组 |
| lshf1woah | 前端 - Web2组 |
| ylslyf59p | 前端 - Web3组 |
| _blbxwp_o | 后端 - 开发1组 |
| w617wcwir | 后端 - 开发2组 |
| v7v2uxie2 | 后端 - 开发3组 |
| s5cxwh3rr | 后端 - 开发4组 |
| u4hiw9ebg | 数据 - 业务支撑1组 |
| txuwdgsz7 | 数据 - 业务支撑2组 |
| wpryu7bl7 | 数据 - 新能力建设组 |
| 9th4smz6n | AI - 工程组 |
| 30yctwsmo | AI - 算法组 |
| 99txilbjp | 共享服务 - 架构组 |

---

### sub_task（任务）

**状态选项**（`work_item_status` 字段）：
| option_id | option_name |
|-----------|------------|
| unfinished | 未完成 |
| done | 已完成 |

---

### 产品需求类型
**类型 key**: `656ec92050c04311fa3f2085`（storybank）

### 技术优化类型
**类型 key**: `65b721a2b0015eeaeec5cbe6`（tech_opt）

---

## 常用工具与字段对应关系

| 想做的事 | 工具 | 关键字段 |
|---------|------|---------|
| 查缺陷状态分布 | `list_workitem_field_config` | `work_item_status` |
| 查优先级高的缺陷 | `list_todo` + 过滤 | `priority` |
| 查某负责人名下缺陷 | `list_todo` | `current_status_operator` |
| 查某阶段缺陷 | `search_by_mql` | `issue_stage` |
| 查某业务线缺陷 | `search_by_mql` | `business` |
| 查超期任务 | `list_todo` | `schedule.end_time` |
| 查某版本关联工作项 | `search_by_mql` | `planning_version` |

---

## 工作项 ID 与 URL 对照

- 工作项 URL 格式：`https://project.feishu.cn/more/more?workitem_id={id}&project_key={project_key}`
- 所有工具均支持只传 `url` 参数，自动解析 project_key 和 work_item_id
