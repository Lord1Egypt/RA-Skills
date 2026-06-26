# Kunwu Builder 控制工具

通过 HTTP API 控制 Kunwu Builder (坤吾) 工业仿真软件。

## 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "speedbot-builder": {
          "enabled": true,
          "config": {
            "baseUrl": "http://127.0.0.1:16888"
          }
        }
      }
    }
  }
}
```

## 工具函数

使用 `kunwu_call` 工具调用 API：

```json
{
  "tool": "kunwu_call",
  "endpoint": "/GetAllModelInfo",
  "data": {}
}
```

## 常用命令

### 获取所有模型
```
kunwu_call endpoint="/GetAllModelInfo"
```

### 创建模型
```
kunwu_call endpoint="/model/create" data='{"id":"纸箱","position":[0,0,0]}'
```

### 控制辊床
```
kunwu_call endpoint="/motion/IndustrialEquipment" data='{"id":"conveyer1","type":0,"command":1}'
```

### 相机拍照
```
kunwu_call endpoint="/sbt/sensor" data='{"id":"camera1","type":1}'
```

### 获取机器人位姿
```
kunwu_call endpoint="/GetRobotLink" data='{"id":"r1"}'
```

### 重置场景
```
kunwu_call endpoint="/ResetScene"
```

### 批量执行（新增）
```
kunwu_call endpoint="/batch/execute" data='{"atomic":true,"commands":[{"url":"/GetModelInfo","body":{"id":"Cube"}}]}'
```

### 添加行为组件（新增）
```
kunwu_call endpoint="/behavior/add" data='{"id":"model_001","behavioralType":1,"referenceAxis":0,"minValue":-1000,"maxValue":1000}'
```

### 获取层级树（新增）
```
kunwu_call endpoint="/models/tree" data='{"rootId":"scene"}'
```

## 自然语言示例

你可以这样说：

- "在场景里创建一个纸箱，位置在 10,20,30"
- "让 conveyer1 号辊床开始运动"
- "用 camera1 拍张照"
- "查询机器人 r1 的当前位置"
- "把场景重置一下"
- "导出机器人模型到桌面"
- "获取场景里所有模型的层级树"
- "给 model_001 添加一个旋转行为"
- "批量查询 Cube 和 Robot 的信息"
- "显示一个进度条，提示导入中"

## 故障排查

1. **连接失败**: 确认 SpeedBot Builder 正在运行
2. **端口错误**: 默认端口 16888，可在偏好设置中修改
3. **400 错误**: 检查请求参数格式是否正确
