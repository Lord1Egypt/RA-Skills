# IAM 最小权限（RFQ 询价 · 包年包月 + 按需）

目标：以 BSS 询价为中心的最小只读权限集合。覆盖 `references/related-commands.md` 与 `catalog.yml` `primary_operations` 中全部 op；不引入任何写动作。

IAM Action 会随账号类型、站点、服务版本变化。本文给权限设计口径；落地前以
[IAM 权限最佳实践](https://support.huaweicloud.com/bestpractice-iam/iam_0426.html)、
[API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/overview)
和 `hcloud <SERVICE> <Operation> --help` 为准。

## 权限分层

| 层级 | 用途 | 何时需要 |
| --- | --- | --- |
| BSS 询价只读 | 调用 `ListRateOnPeriodDetail`（包年包月）/ `ListOnDemandResourceRatings`（按需）拿报价 | 默认必需 |
| BSS 字典只读 | 翻译 `cloud_service_type` / `resource_type` / `measure_id` | 默认必需 |
| 产品规格只读 | 解析 `resource_spec`（ECS / RDS / DCS / EVS） | 询价目标产品涉及对应云服务时 |
| 身份范围只读 | 解析 `project_id` 与可访问项目 | 当 hcloud profile 未直接配置 `project_id` 时 |

**禁止**：支付、续费、退订、退款、回收、创建、修改、删除、发送验证码、划拨、改余额或资源。

## BSS 询价只读

| KooCLI 操作 | 读取内容 |
| --- | --- |
| `BSS/ListRateOnPeriodDetail` | 包年/包月报价（官网价 / 可选折扣 / 折扣最优） |
| `BSS/ListOnDemandResourceRatings` | 按需报价（官网价 / 折后成交价 / 折扣明细） |

策略骨架（示意，落地以 IAM 控制台/API Explorer 实际 Action 为准）：

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["bss:order:view"],
      "Resource": "*"
    }
  ]
}
```

## BSS 字典只读

| KooCLI 操作 | 读取内容 |
| --- | --- |
| `BSS/ListServiceTypes` | 云服务类型字典 |
| `BSS/ListResourceTypes` | 资源类型字典 |
| `BSS/ListServiceResources` | 服务 → 资源类型映射 |
| `BSS/ListMeasureUnits` | 计量单位字典 |
| `BSS/ListConversions` | 计量单位进制换算 |

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:*:get",
        "bss:*:list"
      ],
      "Resource": "*"
    }
  ]
}
```

如 IAM 不接受通配只读 Action，按上表显式列出 Action。**不要**用写操作补权限。

## 产品规格只读

仅用于解析 `resource_spec`；不读资源详情之外的内容。

| 服务 | KooCLI 操作 | 用途 |
| --- | --- | --- |
| ECS | `ListFlavors` / `NovaListFlavors` / `NovaListFlavorsDetails` | flavor_id 候选 |
| ECS | `NovaListAvailabilityZones` | AZ 候选 |
| RDS | `ListFlavors` / `ListEngineFlavors` | 数据库规格 |
| DCS | `ListFlavors` | 缓存规格 |
| EVS | `CinderListVolumeTypes` | 云硬盘类型码 |

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:cloudServers:list",
        "ecs:flavors:list",
        "ecs:availabilityZones:list",
        "rds:flavor:list",
        "dcs:flavor:list",
        "evs:volumeTypes:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 身份范围只读

| KooCLI 操作 | 用途 |
| --- | --- |
| `IAM/KeystoneListAuthProjects` | 当前认证用户可访问项目 |
| `IAM/KeystoneListProjects` | 按 `domain_id` 等过滤的项目列表 |

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:projects:listProjectsForUser",
        "iam:projects:listProjects"
      ],
      "Resource": "*"
    }
  ]
}
```

## 伙伴代客户询价场景

伙伴解决方案商 / 总经销商代客户询价时：

1. 伙伴账号本身只需上面四层只读权限。
2. 通过伙伴中心创建客户委托 / 客户授权，置换出客户 Token。
3. 用置换后的客户 Token 调用 `KeystoneListAuthProjects` 获取目标 region 的客户 `project_id`。
4. 在 `ListRateOnPeriodDetail` / `ListOnDemandResourceRatings` 请求中带客户 `project_id`。

授权失败时**不要**绕过、不扩大查询；记录操作名 + 失败原因即可。

## 权限失败处理

| 现象 | 处理 |
| --- | --- |
| `403 Forbidden` | 记录操作名、账号范围；建议补对应只读 Action |
| `CBC.99006006 产品未发现` | 不是权限问题，回到 Spec Review / Clarify 重新核对四元组（cloud_service_type / resource_type / region / resource_spec） |
| `CBC.99006055 询价结果超过金额最大限制` | 拆小 product_infos 或缩短 period_num |
| 维度查不到 | 保留原始 code 写到小结，提示用户用 `ListServiceTypes` / `ListResourceTypes` 校对 |

## 范围外

| 类别 | 拒绝原因 |
| --- | --- |
| 支付 / 续费 / 退订 / 回收 | 写操作，超出本只读询价范围 |
| 历史账单 / 余额 / 对账 | 账务事实，非 RFQ 询价 API 范畴；建议费用中心或 BSS 账单只读查询 |
| 非华为云账务 | 仅服务华为云 BSS |
