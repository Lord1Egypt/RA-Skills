# 验证方法 — huawei-cloud-ces-alarm-rules-list

分四层：**接口事实核对**、**离线单元测试**、**离线 mock 冒烟**、**真实只读冒烟**。
其中真实冒烟只做 GET 读取（不创建、不修改任何云资源），完整功能验证仍由 QA 带外执行。

## 1. 接口事实核对（本机实测，可复现）

```bash
hcloud CES --help | grep -E "ListAlarmRules|ListAlarmRulePolicies|ListAlarmRuleResources|ListAlarms"
hcloud CES ListAlarmRules --help          # 参数清单（无 alarm_level/alarm_state/resource_type）
hcloud CES ListAlarmRulePolicies --help
hcloud CES ListAlarmRuleResources --help
hcloud CES ListAlarms --help              # v1：--start / --limit / --order / --enterprise_project_id

python3 - <<'PY'
import huaweicloudsdkces.v1 as v1, huaweicloudsdkces.v2 as v2
for cls, name in ((v2.CesClient, "_list_alarm_rules_http_info"),
                  (v2.CesClient, "_list_alarm_rule_policies_http_info"),
                  (v2.CesClient, "_list_alarm_rule_resources_http_info"),
                  (v1.CesClient, "_list_alarms_http_info")):
    paths = [c for c in getattr(cls, name).__func__.__code__.co_consts
             if isinstance(c, str) and c.startswith("/")]
    print(name, paths)
PY
# -> /v2/{project_id}/alarms
# -> /v2/{project_id}/alarms/{alarm_id}/policies
# -> /v2/{project_id}/alarms/{alarm_id}/resources
# -> /V1.0/{project_id}/alarms
```

结论固化在 [api-verification.md](api-verification.md)。

## 2. 离线单元测试（无凭据、无网络）

```bash
cd skills/monitoring/huawei-cloud-ces-alarm-rules-list
python3 -m unittest discover -s tests -v
```

覆盖范围（62 个用例）：

| 分组 | 覆盖点 |
|------|--------|
| `GuardTests` | 只读词通过；create/update/delete/enable/disable/batch/add/remove 拦截；操作白名单；只读取值旗标不参与扫描；后续旗标仍被扫描；写意图在**任何命令执行前**退出 1 |
| `CommandBuildTests` | 四个操作的 hcloud 参数构造（含 `--alarm_id` / `--name` / `--namespace` / `--offset` / `--start` / `--order`）；REST 路径常量 |
| `JsonAndEnvelopeTests` | 带噪声的 JSON 提取；空输出；非法输出报错；错误信封识别；容器键提取 |
| `PagingTests` | offset 翻页直到 `count`；短页停止；起始 offset 透传；`--max-pages` 防死循环 |
| `StateMapTests` | v1 状态映射；`insufficient_data` → 「数据不足」且不等于「正常」；按 `start` 翻页去重 |
| `RuleRowTests` | 十列表格字段口径；列顺序；停用/未开启通知；分级阈值；级别中文映射 |
| `FilterTests` | 名称模糊（含 alarm_id）；级别；状态（数据不足独立）；资源类型（namespace / product_name / 维度名）；入参别名与非法值 |
| `DetailTests` | 单条详情三次调用顺序；可读详情三段（阈值策略/关联资源/通知对象）；`--json` 原始结构；规则不存在 |
| `ErrorClassificationTests` | 403 → 文案含 `ces:alarms:list`；`[USE_ERROR]` → 参数错误提示；缺凭据 → 带外配置提示；错误信封（stdout + rc=0）不得当空列表；空列表提示；`--limit` 越界 |
| `MainOutputModesTests` | 名称列表 / 表格 / JSON 三种形态；过滤生效；状态补齐失败在无 `--alarm-state` 时降级「未知」、有该过滤时报错 |
| `SdkFallbackTests` | SDK 查询（列表/状态）；缺 AK/SK；缺 project id；hcloud 缺失回退；**凭据错误不回退** |
| `SkillQualityWrapperTests` | skill-quality-cli 包裹；`SKILL_QUALITY_REPORT=0` 裸跑；显式 mock bin 原样执行 |

## 3. 离线 mock 冒烟（本机已执行，验证输出形态）

用一个本地 mock 充当 hcloud（`export CES_ALARM_HCLOUD_BIN=/path/to/mock-hcloud`），
逐项确认：

- 默认输出：表头 + 每行一个规则名称；
- `--table`：十列按验收顺序输出，`数据不足` 与 `正常` 分开标注；
- `--json`：原始结构（`alarm_id` / `policies` / `resources` 原样）；
- `--alarm-state 数据不足`：只留该状态的规则；
- `--rule-id <id>`：阈值策略 / 关联资源 / 通知对象三段齐全；
- 写意图（`--enable-alarm-rule`）→ 退出 1，未执行命令；
- 错误信封（stdout + rc=0）→ 退出 1 且给 IAM 提示；
- `[USE_ERROR]` → 退出 1 且给 `--help` 核对建议。

## 4. 真实只读冒烟（本机已执行，cn-north-4）

```
python3 scripts/ces_alarm_rules.py --limit 10        # 名称列表 ✓
python3 scripts/ces_alarm_rules.py --limit 3 --table # 10 列表格，状态「正常」✓
python3 scripts/ces_alarm_rules.py --alarm-state 正常 # 状态过滤 ✓
python3 scripts/ces_alarm_rules.py --alarm-state 数据不足  # 空结果提示 ✓
python3 scripts/ces_alarm_rules.py --rule-id <alarm_id>   # 阈值策略/关联资源/通知对象 ✓
```

冒烟过程中修正了三个与真实响应相关的问题（详见
[api-verification.md](api-verification.md) §4.1）：`period` 单位是秒、分级阈值重复打印、
详情接口 `resources` 是二维结构。

## 5. 未覆盖 / 留给 QA

- 真实只读冒烟只覆盖当前账号已有的一条告警规则（分级阈值 + RDS namespace）；
  多资源组、`ok_notifications` 为空、停用规则等组合由 QA 带外覆盖。
- SDK 回退的真实网络调用未在本机执行（本机无 `huaweicloudsdkces` 且无 project id）；
  该分支由注入式 fake loader 的单元测试覆盖。
- 跨区域差异：v1 `ListAlarms` 的 `start` 边界语义按「无新增即停止」兜底，未逐区域实测。