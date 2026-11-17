# 验收清单

对应 Issue #152 的验收标准，逐项给出可复核的检查方法。

## 功能验收

- [ ] **离线单测全绿**（mock hcloud 子进程 + fake SDK）
      `python3 -m unittest discover -s tests -v` → 0 failed。
- [ ] **默认列表冒烟**：`python3 scripts/list_as_groups.py --region cn-north-4`
      → 返回伸缩组列表或 `当前区域无伸缩组（区域: cn-north-4）。`，rc=0
      （无 AS 只读权限时返回明确的 403 提示，rc=1，需补授权后重跑）。
- [ ] **完整组视图**：`--table` 输出组ID / 名称 / 状态 / 期望实例数 / 当前实例数 /
      最小-最大 / VPC / 子网 / 关联ELB / 创建时间 / region 共 11 列。
- [ ] **下钻有效 ID**：`--group-id <有效ID>` → 组内实例列表，rc=0；
      组内无实例时输出 `伸缩组 … 内无实例`，rc=0。
- [ ] **下钻无效 ID**：`--group-id <无效ID>` → `伸缩组不存在或不属于当前区域`
      明确提示，rc≠0，且不是未捕获异常堆栈。
- [ ] **异常组醒目标注**：期望实例数≠当前实例数的组、状态非 INSERVICE 的组，
      在 `--table` 下单独分区置顶并带 `⚠`。
- [ ] **异常实例醒目标注**：生命周期非 INSERVICE 或健康状态非 NORMAL 的实例，
      在 `--table`（`--group-id`）下单独分区置顶并带 `⚠`。
- [ ] **状态过滤**：`--status <状态>` 可只列异常组（`--status abnormal` 等价于
      期望≠当前 或 状态非 INSERVICE）。
- [ ] **原始 JSON**：`--json` 输出可被 `python3 -m json.tool` 解析，含
      `scaling_groups` / `scaling_group_instances`、`total_number`、`region`。
- [ ] **分页**：`--limit 1~100`，按 `total_number` 与累计条数双条件自动翻页，
      不重复、不漏项，`--max-pages` 有安全上限。
- [ ] **写意图拦截**：`--action delete`、`--name create-me`、`--group-id delete-*`、
      `--operation DeleteScalingGroup` 均在**执行前**被拦截，rc=1。
- [ ] **错误提示可执行**：空列表 / 403 权限不足 / 缺凭据 / `[USE_ERROR]` /
      伸缩组不存在，均给出下一步动作。
- [ ] **不写文件、不访问非华为云网络**；凭据只经 KooCLI profile 或 SDK 环境变量。

## 文档与结构

- [ ] `SKILL.md` 含 YAML frontmatter（name 与目录一致、无 version）、Overview、
      Prerequisites、Workflow、Core Commands、Parameter Confirmation、
      KooCLI Command Format Standard、Reference Documents。
- [ ] `references/` 五份文档齐备：IAM 只读策略、CLI 安装指引、验证方法、
      数据流图、验收清单。
- [ ] `scripts/ensure_cli.sh` / `scripts/install_cli.sh` 存在且与创建器一致。
- [ ] `templates/test-vars.json` 存在且为合法 JSON。
- [ ] `SKILL.md` ≤ 500 行；skill 文件数 ≤ 30；总大小 ≤ 40 MB；
      所有文件扩展名在白名单内。
- [ ] `bash -n scripts/*.sh`、`python3 -m py_compile`、
      `python3 -m json.tool templates/test-vars.json` 全部通过。

## 只读安全

- [ ] 全仓库检索无硬编码 AK/SK。
- [ ] 脚本只会构造 `ListScalingGroups` / `ListScalingInstances` 两个 GET 请求。
- [ ] 无跨 skill 直接调用；无虚构的 API 路径或 IAM 授权项。
- [ ] 建/改/删伸缩组、启停、批量加入/移出实例、执行伸缩策略均不在范围内，
      写操作被守卫拦截并提示需要显式用户确认。

## 快速复核命令

```bash
python3 -m py_compile scripts/list_as_groups.py tests/test_list_as_groups.py
bash -n scripts/ensure_cli.sh
bash -n scripts/install_cli.sh
python3 -m json.tool templates/test-vars.json > /dev/null
python3 -m unittest discover -s tests -v
python3 scripts/list_as_groups.py --action delete; echo "rc=$?"
bash validate-skill.sh -s "$(pwd)"
```