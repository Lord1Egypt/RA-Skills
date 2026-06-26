# Kunwu Builder API 50 轮测试报告

## 📊 总体统计

| 指标 | 数值 |
|------|------|
| 测试轮数 | 50 轮 |
| 总测试数 | 186 次 |
| 成功 | 104 次 |
| 失败 | 82 次 |
| **成功率** | **55.91%** |

---

## ✅ 高成功率 API (100%)

| API | 调用次数 | 成功率 | 说明 |
|-----|---------|--------|------|
| `/ChangeMode` | 46 | 100% | 切换模式 |
| `/GetAllModelInfo` | 12 | 100% | 获取所有模型 |
| `/sensor/queryCameralist` | 8 | 100% | 查询相机列表 |
| `/models/tree` | 9 | 100% | 获取层级树 |
| `/ResetScene` | 10 | 100% | 重置场景 |
| `/model/create` | 9 | 100% | 创建模型 |

---

## ❌ 失败 API 分析

### 1. 需要前置条件的 API（0% 成功率）

| API | 失败原因 | 解决方案 |
|-----|---------|---------|
| `/GetSensorStatus` | NotAcceptable | 需要场景中存在传感器 |
| `/GetConveyorMoveDistance` | NotAcceptable | 需要场景中存在传送带 |
| `/sbt/sensor` | 相机 id 不存在 | 需要场景中存在相机 |
| `/query/robot_id` | 请先选中一个机器人 | 需要在软件中选中机器人 |
| `/query/robot_pos` | 未选中机器人 | 需要在软件中选中机器人 |
| `/scene/get_scene_json` | Max allowed object depth reached | Unity 序列化 bug，场景复杂时失败 |
| `/batch/execute` | Batch execution failed | 子命令格式问题 |

### 2. 部分成功的 API

| API | 成功率 | 主要问题 |
|-----|--------|---------|
| `/GetModelInfo` | 18.2% | 模型不存在（test_box 被重置清除） |
| `/model/set_pose` | 25.0% | 模型不存在 |
| `/model/set_render` | 45.5% | 模型不存在 |

---

## 🔧 发现的问题

### 问题 1: 批量执行接口格式问题
**现象**: `/batch/execute` 100% 失败
**原因**: 子命令格式可能与文档不一致
**建议**: 需要验证正确的请求格式

### 问题 2: 场景 JSON 导出 bug
**现象**: `Max allowed object depth reached while trying to export from type UnityEngine.Vector3`
**原因**: Unity 序列化深度限制，复杂场景会失败
**建议**: 这是软件 bug，建议简化场景或联系开发商

### 问题 3: 依赖场景内容的 API
**现象**: 传感器、相机、传送带、机器人相关 API 失败
**原因**: 测试场景中缺少这些设备
**建议**: 在测试前确保场景中有对应设备

### 问题 4: 模型生命周期问题
**现象**: 创建模型后，重置场景就消失了
**原因**: `/ResetScene` 会清除所有用户创建的模型
**建议**: 测试时避免频繁重置场景

---

## 📋 缺失的 API（对比官方文档）

根据官方 API 文档，以下 API **尚未在 skill 中实现**：

### 物流设备
- [ ] `/motion/IndustrialEquipment` - 控制辊床/传送带
- [ ] `/motion/CustomEquipmentCommand` - 自定义设备控制
- [ ] `/motion/CustomEquipmentQuery` - 自定义设备查询
- [ ] `/motion/rollbed` - 到位信号
- [ ] `/motion/ConsecutiveWalkPoints` - 连续运动点

### 物流传感器
- [ ] `/logistic/sensor` - 物流传感器查询
- [ ] `/logistic/steel` - 零件到位状态
- [ ] `/logistic/encoder` - 下发编码器值

### 机器人
- [ ] `/GetRobotLink` - 获取机器人姿态
- [ ] `/SetRobotLink` - 设置机器人姿态
- [ ] `/GetRobotTrackInfo` - 获取机器人轨迹
- [ ] `/RobotSolveIK` - 机器人逆解
- [ ] `/GetRobotExtraLink` - 获取附加轴
- [ ] `/GetGroundTrackInfo` - 地轨参数
- [ ] `/UpdateCollider` - 更新碰撞

### 模型管理
- [ ] `/model/export` - 导出模型 (STL/OBJ)

### 场景
- [ ] `/CreatePoints` - 创建点位
- [ ] `/SceneTipsShow` - 场景提示
- [ ] `/import/cad_2d` - 导入 CAD

### 行为
- [ ] `/behavior/get` - 获取行为参数（已实现但未测试）

### 进度显示
- [ ] `/ShowGenerateSceneProgress` - AI 场景进度
- [ ] `/view/show_progress` - 通用进度条

### 排产
- [ ] `/scheduling/return_result` - 排产结果回传

---

## 🎯 建议

### 立即完善
1. **添加缺失的核心 API** - 物流设备、机器人控制
2. **修复批量执行接口** - 验证正确格式
3. **添加前置条件检查** - 在执行前检查设备是否存在

### 文档改进
1. **添加 API 依赖说明** - 哪些 API 需要场景中有特定设备
2. **添加错误码对照表** - 帮助用户理解错误
3. **添加使用示例** - 每个 API 的完整调用示例

### 测试改进
1. **场景预设** - 测试前准备包含各种设备的场景
2. **条件测试** - 根据场景内容动态选择测试用例
3. **错误分类** - 区分"使用错误"和"API 故障"

---

## 📝 测试时间
- 开始：2026-03-12 23:13
- 结束：2026-03-12 23:15
- 总耗时：约 2 分钟

## 💾 详细数据
- 完整日志：`test-results.json`
