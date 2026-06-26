# Kunwu Builder API 完整参考

基于坤吾软件官方 API 文档整理

## 基础信息

- **软件名称**: Kunwu Builder (坤吾)
- **API 地址**: `http://127.0.0.1:16888`
- **请求方式**: POST (HTTP)
- **Content-Type**: application/json

## 错误码

| Code | 说明 |
|------|------|
| 200 | 请求成功 |
| 301 | 资源永久转移 |
| 400 | 请求失败/错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 接口列表

### 0. 系统配置

| 接口 | 说明 |
|------|------|
| - | 修改端口：菜单栏 - 编辑 - 偏好设置，需重启生效 |

### 1. 机器人

| 接口 | 说明 |
|------|------|
| MQTT | 机器人状态同步（见 MQTT 接口文档） |

### 2. 物流设备

#### 2.1 内置设备
- **POST** `/motion/IndustrialEquipment`
```json
{
  "id": "conveyer1",
  "type": 0,
  "command": 0,
  "data": {"target": "1-3"}
}
```
**type**: 0=辊床，1=下层辊床，2=上下横移，3=左右移动，4=传送带，5=下层传送带，6=转台，7=曲面传送带
**command**: 0=停止，1=正向运动，2=反向运动，3=自定义运动

#### 2.2 自定义设备
- **POST** `/motion/CustomEquipmentCommand`
- **POST** `/motion/CustomEquipmentQuery`

### 3. 相机设备

#### 3.1 拍照
- **POST** `/sbt/sensor`
```json
{
  "id": "camera1",
  "type": 1
}
```
**type**: 1=原始图，2=深度图，3=原始图 + 深度图，0=线扫相机点云

#### 3.2 相机列表
- **POST** `/sensor/queryCameralist`

### 4. 小件二次物流

| 接口 | 说明 |
|------|------|
| `/logistic/sensor` | 查询传感器状态 |
| `/logistic/steel` | 查询零件到位状态 |
| `/logistic/encoder` | 下发编码器值 |

### 5. 流程图接口

| 接口 | 说明 |
|------|------|
| `/query/robot_pos` | 获取机器人位姿 |
| `/query/robot_id` | 获取机器人 ID |
| `/query/robot_id` (带 id) | 获取机器人轨迹 |

### 6. 物体（模型）

| 接口 | 说明 |
|------|------|
| `/model/create` | 创建模型 |
| `/model/set_pose` | 设置姿态及参数化 |
| `/model/set_render` | 设置渲染颜色 |
| `/model/export` | 导出模型 (STL/OBJ) |

### 7-9. 机器人查询

| 接口 | 说明 |
|------|------|
| `/GetModelInfo` | 获取物体属性 |
| `/GetAllModelInfo` | 获取所有物体属性 |
| `/GetRobotTrackInfo` | 获取机器人点位 |

### 10-20. 场景与控制

| 接口 | 说明 |
|------|------|
| `/ResetScene` | 重置场景 |
| `/ChangeMode` | 切换模式 (0:场景构建 1:行为信号 2:机器人 3:数字孪生) |
| `/GetRobotExtraLink` | 获取机器人附加轴 |
| `/GetSensorStatus` | 获取传感器状态 |
| `/GetConveyorMoveDistance` | 获取传送带运动距离 |
| `/import/cad_2d` | 导入 CAD 图纸 |
| `/GetGroundTrackInfo` | 查询地轨参数 |
| `/UpdateCollider` | 更新碰撞 |
| `/RobotSolveIK` | 机器人多轴逆解 |
| `/GetRobotLink` | 获取机器人姿态 |
| `/SetRobotLink` | 设置机器人姿态 |

### 21-31. 新增接口

| 接口 | 说明 |
|------|------|
| `/scheduling/return_result` | 排产结果回传 |
| `/motion/ConsecutiveWalkPoints` | 连续运动点 |
| `/ShowGenerateSceneProgress` | AI 场景进度 |
| `/view/show_progress` | 通用进度条 |
| `/CreatePoints` | 创建点位 |
| `/SceneTipsShow` | 场景提示 |
| `/batch/execute` | 批量执行 |
| `/scene/get_scene_json` | 获取场景 JSON |
| `/models/tree` | 获取层级树 |
| `/behavior/add` | 添加/更新行为 |
| `/behavior/get` | 获取行为参数 |
