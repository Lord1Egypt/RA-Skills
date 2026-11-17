# 验收标准对照 — huawei-cloud-ces-alarm-rules-list

对应 Issue #139。

- [x] 目录结构与其他 skill 一致：`SKILL.md` + `references/` + `scripts/` + `templates/` + `tests/`。
- [x] 主路径 `hcloud CES ListAlarmRules`（`GET /v2/{project_id}/alarms`，实测见
      [api-verification.md](api-verification.md)）；单条详情 =
      `ListAlarmRules --alarm_id` + `ListAlarmRulePolicies` + `ListAlarmRuleResources`。
- [x] hcloud 缺失时回退 `huaweicloudsdkces`（v2 列表/策略/资源，v1 状态）。
- [x] 三种输出形态：默认名称列表 / `--table`（规则ID·名称·资源类型·监控维度·指标·
      阈值与比较符·告警级别·当前状态·是否启用·通知方式）/ `--json`（原始结构）。
- [x] 四类过滤：`--name`（服务端 `name` 透传 + 客户端模糊）、`--alarm-level`、
      `--alarm-state`、`--resource-type`；后三者因 KooCLI 7.3.12 的 `ListAlarmRules`
      无对应 query 参数，翻全量后客户端过滤。
- [x] `--limit` 1~100 + `--offset` 自动翻页，`--max-pages` 上限保护；区域默认 `cn-north-4`。
- [x] 级别中文映射（1 紧急 ~ 4 提示）；状态中文映射（正常 / 告警 / **数据不足** / 无效），
      `insufficient_data` 独立标注「数据不足」，不与「正常」混同。
- [x] 写意图守卫：create / update / delete / enable / disable / batch- / add / remove 等
      意图拒绝，退出码 1，**不执行任何命令**。
- [x] 异常提示：空列表、403（提示 `ces:alarms:list` / `getPolicies` / `getResources`
      最小授权）、缺凭据（带外配置，绝不索要 AK/SK）、KooCLI `[USE_ERROR]`
      （截取原文关键行 + `--help` 核对建议），均不静默成功。
- [x] `python3 -m unittest discover -s tests -v` 全绿（离线 mock，无凭据无网络）。
- [x] 改动仅限新增 skill 目录，不触碰既有文件。

## Out of scope（明确不实现）

- 一切写操作（创建/修改/删除/启停/批量）、告警历史、告警模板、通知掩码、资源分组、一键告警。
- 指标数据点查询（`ShowMetricData` / `ListMetrics` / `BatchListMetricData`）。