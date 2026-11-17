# 验证方法

## 验证 skill 输出正确性

### 1. 指标列表查询验证

```bash
# 设置 AK/SK 环境变量
export HUAWEICLOUD_SDK_AK="您的AK"
export HUAWEICLOUD_SDK_SK="您的SK"

# 执行列表查询
python3 scripts/huawei-cloud-ces-list.py list --region cn-north-4
```

**预期输出**：

```json
{
  "count": 2,
  "total": 207,
  "marker": "...",
  "metrics": [
    {
      "namespace": "SYS.OBS",
      "dimensions": [{"name": "bucket_name", "value": "demo-aac"}],
      "metric_name": "capacity_archive",
      "unit": "Byte"
    }
  ]
}
```

- 有指标时 `count > 0`，`metrics` 数组含指标对象
- 无指标时 `count=0`，`metrics` 为空数组（非报错）

### 2. 过滤查询验证

```bash
python3 scripts/huawei-cloud-ces-list.py list --region cn-north-4 --namespace SYS.ECS --metric-name cpu_util
```

**验证**：返回结果中指标 namespace 均为 SYS.ECS，metric_name 均为 cpu_util。

### 3. 指标数据查询验证

```bash
# 获取最近1小时的毫秒时间戳
FROM=$(python3 -c "import time; print(int((time.time()-3600)*1000))")
TO=$(python3 -c "import time; print(int(time.time()*1000))")

# 查询指标数据
python3 scripts/huawei-cloud-ces-list.py show \
  --namespace SYS.OBS \
  --metric-name capacity_archive \
  --dim.0 bucket_name,demo-aac \
  --filter average \
  --period 3600 \
  --from $FROM \
  --to $TO
```

**预期输出**：`{"metric_name": "...", "datapoints": [...]}`，含数据点数组。

### 4. 错误处理验证

```bash
# AK/SK 缺失
unset HUAWEICLOUD_SDK_AK HUAWEICLOUD_SDK_SK
python3 scripts/huawei-cloud-ces-list.py list
# 预期：stderr 输出 {"error": "AK/SK credentials missing..."}，退出码 3

# 维度格式错误
python3 scripts/huawei-cloud-ces-list.py list --dim.0 invalid_no_comma
# 预期：stderr 输出维度格式错误，退出码 2
```

### 5. 退出码验证

| 场景 | 退出码 |
|------|--------|
| 查询成功 | 0 |
| 参数/维度格式无效 | 2 |
| AK/SK 缺失/无效 | 3 |
| API 调用失败 | 4 |

```bash
python3 scripts/huawei-cloud-ces-list.py list; echo "exit: $?"
```

### 6. 与控制台交叉验证

将 skill 输出的指标列表与华为云控制台 → 云监控服务 → 指标列表对比，确认指标数量、namespace、metric_name、维度一致。
