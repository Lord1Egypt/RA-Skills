# Juggle 工作流规范

## 概览
本文档记录已设计好的 Juggle 工作流信息，包括工作流的出入参、调用示例等。

---

## 工作流列表

### 1. 同步示例工作流 (sync_example)

#### 基本信息
- **流程版本**: v1
- **流程 Key**: sync_example
- **流程类型**: sync（同步流程）
- **触发地址**: `{BASE_URL}/open/v1/flow/trigger/v1/sync_example`

#### 入参说明

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| userName | String | 必填 | 用户名 |
| password | String | 必填 | 密码 |
| deposit | Integer | 必填 | 存款金额 |

**入参示例**:
```json
{
    "flowData": {
        "userName": "juggle",
        "password": "123456",
        "deposit": 666
    }
}
```

#### 出参说明

| 参数名 | 类型 | 描述 |
|--------|------|------|
| success | Boolean | 是否成功 |
| errorCode | String | 错误码 |
| errorMsg | String | 错误信息 |
| result | Object | 流程执行结果 |
| - flowType | String | 流程类型（sync/async） |
| - flowInstanceId | String | 流程实例 ID |
| - status | String | 流程状态（FINISH/ABORT/RUNNING） |
| - data | Object | 流程返回数据 |
| -- userName | String | 用户名 |
| -- age | String | 年龄 |
| -- orderName | String | 订单名称 |

**出参示例**:
```json
{
    "success": true,
    "errorCode": "0",
    "errorMsg": null,
    "result": {
        "flowType": "sync",
        "flowInstanceId": "sync_fYCVeFNzrvwe4k8Z",
        "status": "FINISH",
        "data": {
            "userName": "juggle",
            "age": "18",
            "orderName": "送10元话费"
        }
    }
}
```

#### 调用示例

**命令行调用**:
```bash
python /workspace/projects/juggle/scripts/flow.py trigger \
  --flow-version "v1" \
  --flow-key "sync_example" \
  --flow-data '{"userName": "juggle", "password": "123456", "deposit": 666}'
```

**预期输出**:
```
[触发流程] 正在触发流程...

[触发结果]
{
  "success": true,
  "errorCode": "0",
  "errorMsg": null,
  "result": {
    "flowType": "sync",
    "flowInstanceId": "sync_fYCVeFNzrvwe4k8Z",
    "status": "FINISH",
    "data": {
      "userName": "juggle",
      "age": "18",
      "orderName": "送10元话费"
    }
  }
}

[同步流程] 执行完成
```

#### 使用场景
- 用户注册流程
- 数据查询流程
- 实时计算流程

#### 注意事项
- 这是一个同步流程，调用后立即返回结果
- 所有入参都为必填项，请确保参数完整性
- 用户名和密码需要符合系统验证规则

---

## 如何添加新的工作流

按照以下模板添加新的工作流信息：

```markdown
### {序号}. {工作流名称} ({flow_key})

#### 基本信息
- **流程版本**: {version}
- **流程 Key**: {flow_key}
- **流程类型**: {sync/async}
- **触发地址**: `{BASE_URL}/open/v1/flow/trigger/{version}/{flow_key}`

#### 入参说明

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| {param1} | {type} | {必填/选填} | {描述} |

**入参示例**:
```json
{
    "flowData": {
        "{param1}": "{value1}",
        "{param2}": "{value2}"
    }
}
```

#### 出参说明

| 参数名 | 类型 | 描述 |
|--------|------|------|
| success | Boolean | 是否成功 |
| errorCode | String | 错误码 |
| errorMsg | String | 错误信息 |
| result | Object | 流程执行结果 |
| - flowType | String | 流程类型 |
| - flowInstanceId | String | 流程实例 ID |
| - status | String | 流程状态 |
| - data | Object | 流程返回数据 |

**出参示例**:
```json
{
    "success": true,
    "errorCode": "0",
    "errorMsg": null,
    "result": {
        "flowType": "{sync/async}",
        "flowInstanceId": "{instance_id}",
        "status": "{FINISH/ABORT/RUNNING}",
        "data": {
            "{key}": "{value}"
        }
    }
}
```

#### 调用示例

**命令行调用**:
```bash
python /workspace/projects/juggle/scripts/flow.py trigger \
  --flow-version "{version}" \
  --flow-key "{flow_key}" \
  --flow-data '{"{param1}": "{value1}"}'
```

#### 使用场景
- {场景1}
- {场景2}

#### 注意事项
- {注意事项1}
- {注意事项2}
```

---

## 工作流状态说明

| 状态 | 描述 |
|------|------|
| FINISH | 流程执行完成 |
| ABORT | 流程执行失败/中止 |
| RUNNING | 流程正在执行中（异步流程） |

## 流程类型说明

| 类型 | 描述 | 执行方式 |
|------|------|----------|
| sync | 同步流程 | 触发后立即返回结果 |
| async | 异步流程 | 触发后返回实例ID，需轮询查询结果 |
