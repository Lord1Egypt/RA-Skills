# exportGroupVideo API

## 描述

导出指定流星轨迹的视频文件。

## 命令

```bash
mma post --method exportGroupVideo --data-file <filePath>
```

## 请求参数

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| id | 字符串 | 是 | 流星结果的ID |

## 示例

```bash
# 导出流星轨迹视频
echo '{"id": "1769618931207054146177863687894316"}' > data.json
mma post --method exportGroupVideo --data-file data.json

# 指定端口
echo '{"id": "1769618931207054146177863687894316"}' > data.json
mma post --method exportGroupVideo --port 9000 --data-file data.json
```

## 响应格式

```json
{
  "data": "success",
  "msg": "导出中...",
  "summary": "已经提交导出任务了，请稍候调用getDataDetail接口来获取导出的状态(outputStatus)并获取导出的路径(outputFilePath)，如果长时间状态一直为0，则可能导出失败了。通常导出的过程不会超过30秒。"
}
```

## 响应字段说明

- `data` (字符串): 固定为"success"，表示导出任务已提交
- `msg` (字符串): 状态消息
- `summary` (字符串): 操作摘要，包含导出状态检查方法和预计时间

## 导出状态检查

导出任务提交后，可以通过调用`getDataDetail`接口来检查导出状态：

1. 调用`getDataDetail`接口，传入相同的`id`
2. 检查返回数据中的`outputStatus`字段：
   - `0`: 导出中
   - `1`: 导出成功
   - 其他值: 导出失败
3. 如果导出成功（outputStatus=1），可以通过`outputFilePath`字段获取导出文件的完整路径

## 注意事项

1. 必须确保MMA不在首页（mode=0）状态，否则会返回错误

2. 导出是异步进行的，提交任务后会立即返回响应

3. 需要通过`getDataDetail`接口来检查导出状态和获取导出文件路径

4. 如果`outputStatus`长时间保持为0，则可能导出失败

5. 通常导出过程不会超过30秒

6. 导出的视频文件会保存在MMA的默认输出目录中，具体路径可以通过`getDataDetail`接口获取

7. 每次只能导出一个流星轨迹的视频
