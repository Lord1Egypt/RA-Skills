# IP 归属与公共活动
<!-- reference-type: business -->

> **范围**：读取单个 IP 的基础归属信息和窗口内公共活动；不管理黑名单、收藏或私有数据。活动窗口遵循 [query.md](query.md)。
<!-- slot: 范围 -->

## 命令一览

| 命令 | 作用 |
|---|---|
| `nextrap-cli ip info` | 查询地理归属、运营商、ASN等基础信息 |
| `nextrap-cli ip activity` | 查询窗口内活动、请求总数、每日趋势及按需分布 |
<!-- slot: 命令清单 -->

### nextrap-cli ip info

```bash
nextrap-cli ip info 8.8.8.8 -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| IP | 一个合法 IPv4/IPv6，不接受网段；使用任务实际 IP 替换示例。不带日期、scope 或 include 参数。 |
| 基础信息 | `source=awdb`，未提供字段为 null；不是实时 WHOIS、风险评分或活动统计。库没有结果时按错误处理，不编造归属。 |
<!-- slot: 参数 -->

### nextrap-cli ip activity

```bash
nextrap-cli ip activity 8.8.8.8 -o json
nextrap-cli ip activity 8.8.8.8 --include types,products -o json
```
<!-- slot: 示例 -->

| 输入或输出 | 约束 |
|---|---|
| 请求规模 | 上面两行是二选一，不连续执行。默认只读首次/末次时间、请求总数、每日趋势 3 个接口；确需分布才用第二行，所选类型与产品各增一个接口，重复选项只调一次。 |
| 活动含义 | `first_active/last_active` 是有效窗口内活动时间，不是全历史；`request_count` 是匹配请求数，不承诺均为恶意请求。无活动是 0、空数组和null时间。 |
| 每日桶 | `days` 按 UTC+08:00 分桶，`active_days` 只数正请求日；不补观测跨度外的零日期。首次/末次保留上游时间戳时区。 |
| 分布 | 未请求 `types/products` 为 null，请求后无桶为 []；可能近似，不保证完整。产品只有标签，`product_id=null`，不猜 ID、不合并同名桶；类型标签不等于检索枚举。 |
| 一致性与准入 | 多接口不是同一快照，任何所选接口失败整条失败；访问权限和 IP 查询余额门槛仍由后台执行。 |
<!-- slot: 参数 -->

## 注意事项

- [ ] 示例 IP 已换成实际目标，没有为了尝试参数对同一 IP 连续执行两个活动示例。
- [ ] 已区分归属、活动与攻击结论；未把窗口内无结果、近似分布或未知字段解释成安全证明。
<!-- slot: 注意事项 -->
