# PRD — 测试验收应用（huo15.test.*）

> 所属技能：huo15-huihuo-suite（辉火云企业套件 ERP）  
> 版本：v1.6.0 新增能力 · 2026-07-09  
> 维护：青岛火一五信息科技有限公司

---

## 一、背景与目标

辉火云企业套件（Odoo 19，db=`huo15`）已上线自定义模块「测试验收」，承载公司软件项目的 **缺陷（Bug）生命周期管理 + 迭代（Sprint）进度**。该模块在 Odoo 后台已有菜单（`测试验收` → `Bug 管理 / 全部 Bug / 迭代 / 统计分析 / 配置·标签`）与表单按钮，但此前本技能无法通过自然语言 / API 操作它。

**目标**：让本技能新增第 12 个应用「测试验收」，支持「记一个 Bug、推进它、验收它、统计它」的全流程，与既有项目（project）、工时单（timesheet）、活动（activity）天然打通。

---

## 二、用户故事

### 角色假设
- **测试/产品（呈报人 reporter）**：发现问题、登记 Bug、指明严重程度。
- **开发（解决人 assignee）**：接单、处理、标记已解决。
- **测试/产品（验收人 verifier）**：验收通过 / 验收打回。
- **项目经理**：看迭代进度、按状态/严重度统计、找积压。

### 核心 User Story
1. 作为**呈报人**，我想用一句话登记一个 Bug：「`在域品汇登录页输入任意验证码都能登录，严重，记到域品汇项目`」→ 自动建 Bug、分配 BUG 编号、默认我就是呈报人。
2. 作为**解决人**，我想看到分配给我的 Bug 列表，并把它从「已确认」推进到「已解决」。
3. 作为**验收人**，我想对「已解决」的 Bug 做验收：通过则关闭；不过则打回（记 reopen_count）。
4. 作为**项目经理**，我想：
   - 按「迭代 / 状态 / 严重度 / 负责人」统计 Bug 分布；
   - 把一批 Bug 挂到某个 Sprint；
   - 看某 Sprint 的完成率（progress）。
5. 作为**呈报人**，当 Bug 与既有记录重复时，我想「标记为重复」并指向主 Bug。

---

## 三、数据模型（来自 Odoo 19 实例）

> 通过 `fields_get` + form 视图 arch 反向工程得到，字段中文 string 即 Odoo 实际配置。

### 3.1 `huo15.test.bug`（测试验收 Bug）— 主模型

| 分组 | 字段 | 类型 | 取值 / 说明 |
|---|---|---|---|
| 标识 | `bug_code` | char | 序列 `BUG-#####`（`ir.sequence` prefix=BUG-, padding=5），**自动生成、只读** |
| 标识 | `name` | char | Bug 标题（必填） |
| 定位 | `project_id` | m2o project.project | 所属项目（**create 时必填**） |
| 定位 | `task_id` | m2o project.task | 关联任务 |
| 定位 | `sprint_id` | m2o huo15.test.sprint | 迭代 |
| 定位 | `found_version` | char | 发现版本 |
| 定位 | `tag_ids` | m2m huo15.test.bug.tag | 标签/模块（带 color） |
| 分级 | `severity` | selection | `serious` 严重 / `high` 高 / `medium` 中 / `low` 低 |
| 分级 | `priority` | selection | `p0` / `p1` / `p2` / `p3` |
| 流转 | `state` | selection | `new` 新 → `confirmed` 已确认 → `in_progress` 处理中 → `resolved` 已解决 → `closed` 已关闭 |
| 流转 | `resolution` | selection | `fixed` 已修复 / `wontfix` 不予处理 / `duplicate` 重复 / `cannotreproduce` 无法复现 / `bydesign` 设计如此 |
| 人员 | `reporter_id` | m2o res.users | 呈报人（默认当前用户） |
| 人员 | `report_date` | date | 呈报日期（默认今日） |
| 人员 | `assignee_id` | m2o res.users | 解决人 |
| 人员 | `cc_user_ids` | m2m res.users | 抄送人 |
| 人员 | `verifier_id` | m2o res.users | 验收人（action_verify 写入当前用户） |
| 日期 | `resolve_date` | date | 实际解决日期（action_resolve 写入今日） |
| 日期 | `verify_date` | date | 验收日期（action_verify 写入今日） |
| 计数 | `reopen_count` | integer | 打回次数（action_reopen 每次 +1） |
| 计数 | `effective_hours` | float | 累计工时（聚合 `timesheet_ids` 即 account.analytic.line） |
| 重复 | `duplicate_of_id` | m2o self | 重复于（标记重复前必填） |
| 重复 | `related_bug_ids` | m2m self | 关联 Bug |
| 正文 | `description` | html | Bug 描述（复现步骤/预期/实际） |
| 正文 | `note` | text | 备注 |
| 杂项 | `company_id` / `create_date` / `write_date` | — | 自动 |
| 邮件 | `message_ids` / `activity_ids` / `message_follower_ids` | — | mail.thread / mail.activity mixin 自带 |

### 3.2 `huo15.test.sprint`（测试迭代 / Sprint）

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | char | 迭代名称（必填，如 `2026-07 冲刺`） |
| `project_id` | m2o project.project | 所属项目 |
| `date_start` / `date_end` | date | 起止日期 |
| `state` | selection | `planned` 计划 → `active` 进行中 → `done` 已完成 |
| `description` | text | 迭代目标 / 范围 |
| `bug_ids` | one2many → huo15.test.bug | 该迭代下的 Bug |
| `bug_count` / `bug_closed_count` | integer | Bug 总数 / 已关闭（computed） |
| `progress` | float | 完成率 %（computed） |

### 3.3 `huo15.test.bug.tag`（测试验收 Bug 标签）

| 字段 | 说明 |
|---|---|
| `name` | 标签名称 |
| `color` | 颜色索引 |
| `active` | 启用（可归档） |

---

## 四、状态机（核心）

### 4.1 Bug 状态机

```
        action_confirm      action_start       action_resolve      action_verify
 new ─────────────────▶ confirmed ────────▶ in_progress ────────▶ resolved ───────────────▶ closed
                                                                     │
                                                     action_reopen   │  (reopen_count++)
                                                  ┌─────────────────┘
                                                  ▼
                                            in_progress

 任意非 closed ──action_close_wontfix──▶ closed (resolution=wontfix)
 任意(有 duplicate_of_id) ──action_mark_duplicate──▶ closed (resolution=duplicate)
 closed ──action_reset──▶ new   （重新打开）
```

| 方法 | 前置状态 | 后置状态 | 副作用 |
|---|---|---|---|
| `action_confirm` | new | confirmed | — |
| `action_start` | confirmed | in_progress | — |
| `action_resolve` | in_progress | resolved | resolution='fixed'，resolve_date=今日 |
| `action_verify` | resolved | closed | verifier_id=当前用户，verify_date=今日 |
| `action_reopen` | resolved | in_progress | reopen_count+=1 |
| `action_close_wontfix` | ≠closed | closed | resolution='wontfix' |
| `action_mark_duplicate` | ≠closed 且 duplicate_of_id 已设 | closed | resolution='duplicate' |
| `action_reset` | closed | new | — |

### 4.2 Sprint 状态机

```
 planned ──action_start──▶ active ──action_done──▶ done
   ▲                                          │
   └─────────────action_reset─────────────────┘
```

---

## 五、权限模型（关键约束）

通过 `ir.model.access` 反查得到：

| 操作 | 允许的组 |
|---|---|
| 读 / 创建 / 写（create/read/write） | `Role / User`（全员，含普通登录用户） |
| 删除（unlink） | **仅 `测试验收 / 管理员`**（group id=178） |

> **产品含义**：普通账号（含本次测试账号 645612509@qq.com = 赵博，仅「测试验收 / 用户」级别）**不能删除 Bug**，只能推进状态 / 归档式关闭。脚本需对 `delete` 命令做明确提示，避免误用。

---

## 六、功能清单（CLI 子命令）

脚本入口：`scripts/testing.py`（避开标准库 `test`，但脚本名 `testing.py` 不冲突）。

### 6.1 Bug 管理
- `bug-add` — 登记 Bug（标题 / 项目 / 严重度 / 优先级 / 描述 / 指派 / 标签 / 迭代 / 任务 / 发现版本 / 抄送）
- `bug-list` — 列 Bug（按状态/严重度/项目/指派人/呈报人/迭代/标签/关键词筛，默认我的活跃 Bug）
- `bug-show` — 详情（含状态栏、人员、日期、reopen、关联、最近消息）
- `bug-update` — 修改可写字段（标题/描述/严重度/优先级/指派/标签/迭代/任务/备注）
- `confirm` / `start` / `resolve` / `verify` / `reopen` / `wontfix` / `duplicate` / `reset` — 8 个状态流转
- `bug-delete` — 删除（仅「测试验收/管理员」可用，失败友好提示）

### 6.2 Sprint 管理
- `sprint-list` — 列迭代（按状态/项目筛）
- `sprint-show` — 详情（含 Bug 分布与完成率）
- `sprint-add` — 建迭代（名称/项目/起止/说明）
- `sprint-start` / `sprint-done` / `sprint-reset` — 状态流转
- `sprint-add-bugs` — 把一批 Bug 挂到迭代

### 6.3 标签管理
- `tag-list` — 列标签
- `tag-add` — 建标签（名称 / 颜色）

### 6.4 统计
- `stats` — 按维度（状态/严重度/项目/解决人/迭代/标签）聚合 Bug 计数 + 活跃/积压预警

---

## 七、验收标准

1. 所有「只读」子命令在普通用户凭据下能正常输出（list/show/stats/sprint-list/tag-list）。
2. 写命令（add/update/状态流转）能驱动 Bug 走完 `new→confirmed→in_progress→resolved→closed` 全链路，字段（resolve_date/verify_date/verifier_id/reopen_count/resolution）被后端正确写入。
3. `duplicate` 必须先设置 `duplicate_of_id` 再调用 `action_mark_duplicate`。
4. `bug-delete` 在非管理员账号下报**友好中文提示**（指出需要「测试验收/管理员」组），不暴露 Odoo 原始 fault。
5. 名字代 id：项目/用户/标签/迭代/Sprint 均可用中文名或 `我` 代替数字 id。
6. 全脚本纯 Python 标准库，零第三方依赖；统一支持 `--json` / `--tools-md`。
7. 与现有应用联动：`task_id` 能用项目任务名解析；`briefing.py` 可统计我的活跃 Bug（后续版本）。

---

## 八、非目标 / 后续

- **本期不做**：附件上传、富文本正文 Markdown 渲染、邮件/消息发送、看板拖拽。
- **后续 v1.7+**：把活跃 Bug 接入 `briefing.py`（「我今天有哪些待验收 Bug」）；按项目/迭代出 Bug 趋势图。

---

## 九、附：探查依据

- 模型与字段：`fields_get('huo15.test.bug'/'huo15.test.sprint'/'huo15.test.bug.tag')`
- 状态方法：表单视图 `ir.ui.view` id=6358 的 `<button name="action_*" type="object">`
- 权限：`ir.model.access` line `huo15.test.bug.manager (group=测试验收/管理员, perm_unlink=True)` / `huo15.test.bug.user (perm_unlink=False)`
- 序列：`ir.sequence` id=47 `prefix=BUG- padding=5 number_next=6`
- 菜单：`ir.ui.menu` id=1117 根「测试验收」
- 全链路自测：建 4 个临时 Bug 驱动 8 个 action_* 全部通过（因普通账号无法删除，已关闭并改名「废弃-技能自测残留-可由管理员删除」留待管理员清理）
