# 验证方法

## 验证步骤

### 1. 环境准备

确保 hcloud CLI 已安装并配置，AK/SK 环境变量已设置。

### 2. 验证 ECS 实例列表查询

```bash
python3 skills/huawei-cloud-ecs-detail-query/scripts/huawei_cloud_ecs_detail_query.py list --region=cn-north-4 --limit=5
```

预期结果：返回 ECS 实例列表，包含名称、状态、规格、IP 等信息。

### 3. 验证 ECS 实例详情查询

```bash
python3 skills/huawei-cloud-ecs-detail-query/scripts/huawei_cloud_ecs_detail_query.py show --region=cn-north-4 --server-id=<真实实例ID>
```

预期结果：返回指定 ECS 实例的完整详细信息。

### 4. 验证错误处理

```bash
# 无效实例 ID
python3 skills/huawei-cloud-ecs-detail-query/scripts/huawei_cloud_ecs_detail_query.py show --region=cn-north-4 --server-id=00000000-0000-0000-0000-000000000000
```

预期结果：提示未找到实例，退出码 4。
