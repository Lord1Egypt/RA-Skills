# CLAUDE.md

**项目：huo15-furniture-mfg** — 家具制造业智能体技能（和栖家居）v1.4.0

> **加新能力时的分层原则**：详细 CLI 命令写进 `references/commands.md`，SKILL.md 只更新「命令速查」表 + 「字段坑速查」表，保持 SKILL.md 嵌入体积小（< 20KB，ClawHub 8192 token 硬限）。

## 项目定位

家具制造业（首个客户：和栖家居 HeySleep 床垫厂）的对话式查询智能体。后端 test.heysleep.cn（db=`test`，辉火云企业套件 v19 企业版，295 模块 + 28 个 hey_smart_addons 定制模块）。纯 Python 标准库 XML-RPC，零第三方依赖。**P0 全只读**。

策划案：`~/workspace/projects/openclaw/hey_smart_addons/docs/2026-06-13-家具制造业智能体策划案-内部版.md`

## 品牌口径（对外文档必守）

- **对外**（README 主体/汇报/客户培训）：辉火云企业套件 / 辉火云管家 / 和栖家居制造系统。
- **对内**（本文件 / SKILL.md / references / 代码注释）：可用 odoo 等真实技术标识符（API 协议文档性质，全局 §11.8 豁免）。
- 自查：`grep -iE "odoo|openclaw|龙虾" README.md` 只允许命中技术实现小节。

## 环境与红线

- **只许连 test**：`https://test.heysleep.cn` / db=`test`。生产环境地址即使拿到也不连，等发布流程审批（用户 2026-06-13 明确：只在 test 测试）。
- **写操作确认制**（P1 起）：写调用集中在 `actions.py / quote.py / quality.py 写命令段`，默认 dry-run，`--yes` 才执行；查询脚本保持零写入。新增写能力必须沿用两段式 + 可撤回设计。**开发测试时也不许擅自 --yes 打扰真实用户**——用零打扰靶（mt_note 备注 / 提醒建给 Administrator 自己 / 改后还原），或把命令交用户自己跑。
- **操作类功能演进**：新增任何写操作前先读 [../docs/operations-roadmap.md](../docs/operations-roadmap.md)（仓库级 docs，分期 P4-P6 + 评估区红线 + 每命令实现 checklist + 向导处理难点）。评估区动作（开票/收款/取消/批量）默认不做，需客户授权单独立项。该规划含 test 库数据量与内部判断，刻意放仓库级、不进 ClawHub 包。
- 凭据只进 `~/.huo15/tools.md`（标记块 `huo15-furniture-mfg:start/end`，与 huihuo-odoo 技能共存互不覆盖）；secret 走 stdin；绝不进 commit/log/对话输出。

## 目录结构

```
huo15-furniture-mfg/
├── SKILL.md            # 技能主文档（触发词 / 命令速查 / 业务底色 / 字段坑）
├── README.md           # 对外文档（模板：logo + 标语 + 机构表 + 正文 + 页脚）
├── CLAUDE.md           # 本文件
├── _meta.json          # ClawHub 元数据（slug / version）
├── scripts/
│   ├── odoo_client.py  # 核心：凭据(tools.md 标记块) + XML-RPC/JSON-RPC + 只读 ORM 封装
│   ├── odoo_utils.py   # 时区(UTC↔本地/day_range) / m2o / 金额数量格式化 / 中文对齐表格 / 状态中文标签
│   ├── login.py        # 配置并验证凭据（init/set/show/test）
│   ├── order.py        # 订单：status 全链路穿透（SO→明细→MO→picking→QC）/ list
│   ├── mfg.py          # 生产：wip / late / shortage（列表+单据组件展开）
│   ├── inventory.py    # 库存：find 四字段模糊（含型号 x_studio_xinghao）
│   ├── quality.py      # 质检：todo / recent / fail / stats（按 title 分组）
│   ├── purchase.py     # 采购：incoming / overdue
│   ├── partner.py      # 客户：show（档案+应收+成交汇总+最近订单）
│   └── overview.py     # 总览：today / yesterday（晨报数据源 + 风险快照）
└── references/
    ├── commands.md             # 完整命令 + 对话→命令映射
    └── heysleep-mfg-api.md     # test 库实测 API 坑 / selection 取值 / 定制字段 / 链路模型
```

## 开发规范

1. 所有修改在本仓库（`furniture_agents/huo15-furniture-mfg/`），禁止改 ClawHub / OpenClaw workspace 安装副本。
2. 不新增第三方依赖。
3. **改/写 ORM 调用前必读 `references/heysleep-mfg-api.md`**——六个坑全是实测踩出来的，别凭记忆。
4. 入口分层：业务脚本 → `odoo_client.Odoo` 便捷方法 → execute_kw；共用逻辑进 `odoo_utils.py`。
5. 新增命令后：references/commands.md 加细节 → SKILL.md 速查表加一行 → 实测 test 库 → 更新版本号。

## 字段坑速查（详见 references/heysleep-mfg-api.md）

| 坑 | 正确做法 |
|---|---|
| 质检状态 | `quality_state`（无 `state` 字段） |
| name_search | Odoo 19 参数是 `domain=`（`args=` 报 TypeError） |
| 库存量排序 | qty_available 非存储，不能 SQL order，本地 sort |
| move 实收 | Odoo 19 是 `quantity`（无 quantity_done） |
| SO→MO | `origin = so.name`（92% 覆盖）；SO→picking 优先 `sale_id` |
| 本库特性 | MO 不挂 BOM（组件行全库 8 条）；QC 94% 无 product_id（按 title 分组） |
| 时区 | Datetime 全 UTC；当天统计用 `day_range_utc` 否则早 8 点前的单落昨天 |

## 测试

```bash
cd scripts
python3 login.py test                      # 连接
python3 overview.py today                  # 总览（聚合最全，相当于冒烟测试）
python3 order.py status SO-260531-758      # 穿透（已知有 MO+DO+QC 的样本单）
python3 mfg.py shortage MO-260426-374      # 组件展开（已知有组件行的样本单）
```

## 发布流程

```bash
cd ~/workspace/projects/openclaw/furniture_manufacturing/furniture_agents
git add huo15-furniture-mfg/
git commit -m "feat(furniture-mfg): vX.Y.Z 说明"
git push origin main        # cnb.cool 主仓库

# ClawHub（用户要求后才发；绝对路径 + 显式 --version，六坑见全局 ~/CLAUDE.md §7）
# CLAWHUB_TOKEN=... clawhub publish "$(pwd)/huo15-furniture-mfg" --version X.Y.Z
# 发布后手动 bump _meta.json + 单独 chore commit
```

## 版本号规则

- 新增能力域（如 P1 写操作）→ 次版本（1.0 → 1.1）
- 新增命令/参数 → 次版本
- 修 bug / 字段坑 / 文案 → 补丁号
- 每次发版同步 `_meta.json` 与 SKILL.md frontmatter `version` 两处一致
