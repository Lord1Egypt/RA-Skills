# 验证方法

## 前提条件

1. 已配置 HUAWEI_AK/HUAWEI_SK 或 HUAWEICLOUD_SDK_AK/HUAWEICLOUD_SDK_SK 环境变量
2. 已安装依赖：`pip install huaweicloudsdkrds huaweicloudsdkces huaweicloudsdkiam`
3. AK/SK 对应的 IAM 用户已授权 rds:instance:list、ces:metrics:list、ces:metricData:list 权限

## 自测步骤

### 1. 检查 --help 输出

```bash
python3 scripts/huawei_cloud_rds_detail.py --help
```

预期输出：显示所有子命令（list / show / metrics / capability-list）的使用说明。

### 2. 查询能力列表

```bash
python3 scripts/huawei_cloud_rds_detail.py capability-list
```

预期输出：包含 skill 名称、版本和所有能力的 JSON。

### 3. 列出 RDS 实例

```bash
python3 scripts/huawei_cloud_rds_detail.py list
```

预期输出：JSON 格式的 RDS 实例列表（可能为空列表）。

### 4. 查询单实例详情

```bash
python3 scripts/huawei_cloud_rds_detail.py show <instance-id>
```

预期输出：JSON 格式的单实例详细信息（含规格、状态、网络信息等）。

### 5. 查询监控指标

```bash
python3 scripts/huawei_cloud_rds_detail.py metrics <instance-id>
```

预期输出：JSON 格式的 CPU/内存/磁盘监控指标数据。

### 6. 验证凭据缺失场景

```bash
# 临时清空 AK/SK 环境变量测试
unset HUAWEICLOUD_SDK_AK HUAWEICLOUD_SDK_SK
python3 scripts/huawei_cloud_rds_detail.py list
# 预期：退出码 3，输出凭据缺失错误信息
```

## 验证标准

| 测试项 | 预期结果 | 重要性 |
|--------|---------|--------|
| --help | 输出帮助信息 | 必须 |
| capability-list | 返回能力列表 JSON | 必须 |
| list | 返回实例列表 JSON（可能为空列表） | 必须 |
| show <id> | 存在时返回实例详情，不存在时返回错误 | 必须 |
| metrics <id> | 返回监控数据 JSON | 建议 |
| 凭据缺失 | 退出码 3 + 错误提示 | 必须 |