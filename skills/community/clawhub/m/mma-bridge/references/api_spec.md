# MMA Bridge API 规范索引

本文档列出所有可用的 API 方法及其详细文档位置。

## API 方法列表

| 方法名 | 描述 | 详细文档 |
|--------|------|----------|
| getCurrentInfo | 获取 Meteor Master AI 的当前信息（模式、工作状态、视频路径等） | [getCurrentInfo.md](./getCurrentInfo.md) |
| getFilterList | 获取可用的筛选和排序选项列表 | [getFilterList.md](./getFilterList.md) |
| getDataList | 根据筛选和排序条件获取流星检测数据列表 | [getDataList.md](./getDataList.md) |
| getDataDetail | 根据数据ID获取单条流星检测数据的详细信息 | [getDataDetail.md](./getDataDetail.md) |
| exportTrackImg | 导出指定流星轨迹的轨迹图 | [exportTrackImg.md](./exportTrackImg.md) |
| exportGroupVideo | 导出指定流星轨迹的视频文件 | [exportGroupVideo.md](./exportGroupVideo.md) |
| deleteGroup | 删除单条或多条流星检测数据 | [deleteGroup.md](./deleteGroup.md) |
| collect | 收藏单条或多条流星检测数据 | [collect.md](./collect.md) |
| incollect | 取消收藏单条或多条流星检测数据 | [incollect.md](./incollect.md) |
| analyzeVideoFile | 分析单条视频文件 | [analyzeVideoFile.md](./analyzeVideoFile.md) |
| analyzeImageFolder | 分析图片文件夹中的jpg/jpeg图片 | [analyzeImageFolder.md](./analyzeImageFolder.md) |
| analyzeLiveStream | 分析直播流 | [analyzeLiveStream.md](./analyzeLiveStream.md) |
| stopAnalyze | 停止当前直播/摄像头/推流分析 | [stopAnalyze.md](./stopAnalyze.md) |

## 调用格式

所有 API 方法均通过以下统一格式调用：

```bash
mma post --method <methodName> [--port <port>] --data-file <filePath>
```

## 通用参数

- `--method <methodName>`: 必需，指定要调用的 API 方法名称
- `--port <port>`: 可选，指定 API 服务器端口（默认：9000）
- `--data-file <filePath>`: 可选，指定包含 JSON 数据的文件路径。当 API 不需要请求参数时（如 stopAnalyze），此参数可省略；否则需要先将 JSON 数据写入文件，再通过文件路径传递。

## 注意事项

1. 具体可用的方法及其详细参数请查阅上述每个接口的详细文档
2. 随着应用版本的更新，可能会添加新的方法或修改现有方法的参数
3. 发送请求前确保 Meteor Master AI 正在运行
