# 验证方法

本 skill 的验证分四层：语法与结构检查 → 离线单测 → 真实只读冒烟 → 只读守卫与
边界检查。

## 1. 语法与结构检查

```bash
# Python 语法
python3 -m py_compile scripts/list_as_groups.py tests/test_list_as_groups.py

# Shell 语法
bash -n scripts/ensure_cli.sh
bash -n scripts/install_cli.sh

# JSON 语法
python3 -m json.tool templates/test-vars.json > /dev/null

# 结构/规范校验（FAIL 必须为 0）
bash validate-skill.sh -s "$(pwd)"
```

## 2. 离线单测（无凭据、无网络）

```bash
python3 -m unittest discover -s tests -v
```

覆盖范围：

| 用例 | 验证点 |
|------|--------|
| 命令构造 | `AS ListScalingGroups` / `AS ListScalingInstances`、region、limit、start_number、name、group-id |
| 默认输出 | 名称 / 组ID / 状态 三列 + 汇总行 + 异常计数 |
| `--table`（组） | 11 列齐全；异常组单独分区置顶并带 `⚠`；正常组独立分区 |
| `--table`（实例） | 6 列齐全；非 INSERVICE / 非 NORMAL 实例单独分区置顶 |
| `--json` | 原始合并响应（scaling_groups / scaling_group_instances / total_number / region） |
| 过滤 | `--name` 精确、`--fuzzy` 模糊、`--status` 状态与 `abnormal` 别名 |
| 下钻 | `--group-id` 只调用 ListScalingInstances；空组提示 rc=0；无效 ID 明确报错 rc=1 |
| 分页 | total_number + 累计条数双条件、短页终止、total=0、limit 整数倍、max-pages 上限、重复项去重 |
| 错误分类 | 403 / 凭据 / `[USE_ERROR]` / 伸缩组不存在 |
| SDK 回退 | hcloud 缺失/瞬时失败时走 fake SDK；403 不回退；请求字段正确 |
| 只读守卫 | `--action delete`、`--name create-me`、`--group-id delete-*`、`--operation DeleteScalingGroup` 均在调用前 rc=1 |
| 参数边界 | `--limit` 0/101、`--max-pages` 0、`--timeout` 0、非法 `--status` 均 rc=1 |
| JSON 解析 | hcloud 在 JSON 前后追加诊断文本时仍能解析 |

## 3. 真实只读冒烟（需要有效 AK/SK 与 AS 只读权限）

```bash
# 主路径（CLI）
skill-quality-cli run --skill-name huawei-cloud-as-group-list -- \
  hcloud AS ListScalingGroups --cli-region=cn-north-4 --limit=1; echo "rc=$?"

python3 scripts/list_as_groups.py --region cn-north-4; echo "rc=$?"

# 完整表格 / 原始 JSON
python3 scripts/list_as_groups.py --table --region cn-north-4; echo "rc=$?"
python3 scripts/list_as_groups.py --json --region cn-north-4; echo "rc=$?"

# 下钻（用上一步返回的有效 group-id）
python3 scripts/list_as_groups.py --group-id <valid_group_id> --table; echo "rc=$?"
```

判定标准：

- 默认列表：rc=0；输出伸缩组列表或 `当前区域无伸缩组（区域: cn-north-4）。`。
- `--table`：异常组单独分区置顶；`期望实例数≠当前实例数` 与非 `INSERVICE` 组带 `⚠`。
- `--json`：可被 `python3 -m json.tool` 解析。
- 下钻有效 ID：rc=0，输出组内实例或 `伸缩组 … 内无实例`。
- 下钻无效 ID：rc≠0，输出 `伸缩组不存在或不属于当前区域`，不崩溃。

> 若当前账号/region 没有 AS 只读权限，真实冒烟会返回 403 与明确的
> `as:scalingGroup:list` / `as:scalingGroup:listInstances` 提示，rc=1。这是
> **权限问题**，不是脚本缺陷；补授权后重跑即可。无权限时以离线单测结论为准，
> 并如实记录 `live_skipped=true`。

## 4. 只读守卫验证（不需要凭据，不产生任何调用）

```bash
python3 scripts/list_as_groups.py --action delete;           echo "rc=$?"   # 期望 rc=1
python3 scripts/list_as_groups.py --name create-me;          echo "rc=$?"   # 期望 rc=1
python3 scripts/list_as_groups.py --group-id delete-1234;    echo "rc=$?"   # 期望 rc=1
python3 scripts/list_as_groups.py --operation DeleteScalingGroup; echo "rc=$?"  # 期望 rc=1
```

以上命令都不应出现任何 hcloud / SDK 调用痕迹（守卫在调用之前返回）。

## 5. 参数边界验证

```bash
python3 scripts/list_as_groups.py --limit 0;      echo "rc=$?"   # rc=1，提示 1~100
python3 scripts/list_as_groups.py --limit 101;    echo "rc=$?"   # rc=1，提示 1~100
python3 scripts/list_as_groups.py --status foo;   echo "rc=$?"   # rc=1，提示可选状态
```

## 6. 验收记录模板

| 检查项 | 结果 | 备注 |
|--------|------|------|
| `py_compile` / `bash -n` / `json.tool` | PASS / FAIL | |
| 离线单测 | N passed, 0 failed | |
| 真实只读冒烟（默认 / `--table` / `--json` / 下钻） | rc + 输出摘要 | 403 时记录 IAM 授权项 |
| 写意图拦截 | rc=1 | |
| references 五件套 | 齐全 | |