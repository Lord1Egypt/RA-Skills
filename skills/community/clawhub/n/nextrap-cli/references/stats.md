# 公共情报统计
<!-- reference-type: business -->

> **范围**：按所需单一维度读取去重对象数或请求量分布；不检索正文，不提供产品管理。条件、日期与分页遵循 [query.md](query.md)。
<!-- slot: 范围 -->

## 命令一览

| 命令 | 作用 |
|---|---|
| `nextrap-cli stats unique-count` | 返回所选维度的去重对象数 |
| `nextrap-cli stats distribution` | 返回所选维度的请求数分布 |
<!-- slot: 命令清单 -->

### nextrap-cli stats unique-count

```bash
nextrap-cli stats unique-count --query 'url="*/api/auth/login*"' \
  --field ip -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| 条件与维度 | `--query` 与 `--field` 必填；`ip/country/product` 每次只调用相应一个接口，不合成三份概览。 |
| `data.count` | 去重对象数，`count_kind=distinct_objects`、`approximate=true`；不是请求总数。产品按上游产品 ID 去重，不按名称合并。 |
| 空值与窗口 | 零是合法结果，缺失/null/负数计数报错；`requested_start/end` 仅是请求窗口，不承诺有效权限窗口或聚合误差。 |
<!-- slot: 参数 -->

### nextrap-cli stats distribution

```bash
nextrap-cli stats distribution --query 'url="*/api/auth/login*"' \
  --by ip --size 5 -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| 条件与维度 | `--query` 与 `--by` 必填；`ip/path/type/product` 仅调用所选接口。没有自定义排序参数，沿用请求数降序。 |
| `value` / `total` | 桶内请求数 / 去重桶种类数，两者都可能近似；当前页求和不是全量，空页仍可能有正数 total。 |
| 分布投影与答复 | `data[].name` 是桶标签，`data[].value` 是桶内请求数；一起保留 `name/value` 和必要的打码解释，不仅报告桶数或数值。 |
| `masked` / `can_filter` | `null` 保持未知；可回填只是值的可用性，不是账号权限。只有明确未脱敏的合法 IP 可用 `filter_value`。 |
| 其他维度回填 | 路径没有等价公共查询字段，类型编号需要正确检索枚举，产品名可能重名；不把这些桶名直接拼成条件，不猜产品 ID。 |
| 产品 | 保留上游字符串 ID，明确脱敏的桶不输出 ID；同名或相同脱敏名称的桶不合并。 |
<!-- slot: 参数 -->

## 注意事项

- [ ] 已按问题选一种计数或分布，没有为了“完整”额外拉取全部维度或所有页。
- [ ] 答复已区分对象数、请求数和桶数，没有把近似值、名称或字段可用性当作精确身份或权限。
- [ ] 是否有查询门槛和消费由后台执行，不以某次余额未变承诺永久免费或绕过准入规则。
<!-- slot: 注意事项 -->
