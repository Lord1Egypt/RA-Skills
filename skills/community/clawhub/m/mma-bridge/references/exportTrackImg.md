# exportTrackImg API

## 描述

导出指定流星轨迹的轨迹图。

## 命令

```bash
mma post --method exportTrackImg --data-file <filePath>
```

## 请求参数

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| id | 字符串 | 是 | 流星结果的ID |
| filePath | 字符串 | 是 | 导出的目录路径或JPG文件路径，支持中文路径，无需转义 |
| addRedRectToImg | 布尔值 | 否 | 是否在轨迹图上添加红色矩形框（默认值：从设置中读取） |

## 示例

```bash
# 导出到指定目录
echo '{"id": "1769618931207054146177863687894316", "filePath": "C:/Users/username/output"}' > data.json
mma post --method exportTrackImg --data-file data.json

# 导出到指定文件路径
echo '{"id": "1769618931207054146177863687894316", "filePath": "C:/Users/username/output/track.jpg", "addRedRectToImg": true}' > data.json
mma post --method exportTrackImg --data-file data.json

# 指定端口
echo '{"id": "1769618931207054146177863687894316", "filePath": "C:/Users/username/output"}' > data.json
mma post --method exportTrackImg --port 9000 --data-file data.json
```

## 响应格式

```json
{
  "finalFilePath": "C:\Users\username\output\流星轨迹_2026-03-15.jpg",
  "data": "success",
  "msg": "导出中...",
  "summary": "已经提交导出任务了，请稍候前往C:\Users\username\output\流星轨迹_2026-03-15.jpg查看，通常导出轨迹图不会超过5秒"
}
```

## 响应字段说明

- `finalFilePath` (字符串): 最终导出的文件完整路径
  - 如果filePath是目录，则自动生成文件名为"流星轨迹_yyyy-MM-dd.jpg"
  - 如果filePath是JPG文件路径，则使用该路径作为最终文件路径
- `data` (字符串): 固定为"success"，表示导出任务已提交
- `msg` (字符串): 状态消息
- `summary` (字符串): 操作摘要，包含导出路径和预计时间

## 注意事项

1. 如果filePath是目录，系统会自动生成文件名，格式为：`流星轨迹_yyyy-MM-dd.jpg`或`Meteor_yyyy-MM-dd.jpg`

2. 如果filePath是JPG文件路径，则直接使用该路径作为导出路径

3. 导出轨迹图通常不会超过5秒

4. addRedRectToImg参数为可选，如果不提供则使用系统设置中的默认值

5. 必须确保MMA不在首页（mode=0）状态，否则会返回错误

6. 导出完成后，可以通过finalFilePath字段获取导出文件的完整路径
