# 待实现/验证的 API

## 📋 用户提出的新 API 需求

以下 API 是用户提出需要添加的，但测试发现软件可能尚未实现：

### 1. 设置层级关系
- **期望端点**: `/model/set_parent`
- **测试结果**: ❌ Bad Request: Bad target URL
- **状态**: 需要确认正确的 API 路径
- **建议**: 检查软件是否支持该功能，或联系开发商确认 API

### 2. 销毁物体
- **期望端点**: `/model/destroy`
- **测试结果**: ❌ Bad Request: Bad target URL
- **状态**: 需要确认正确的 API 路径
- **替代方案**: 可能在场景管理中使用其他端点

### 3. 销毁组件
- **期望端点**: `/model/destroy_component`
- **测试结果**: ❌ 未测试（端点可能不存在）
- **状态**: 需要确认

### 4. 获取本地模型库信息
- **期望端点**: `/model/library/local`
- **测试结果**: ❌ Bad Request: Bad target URL
- **状态**: 需要确认正确的 API 路径

### 5. 获取远程模型库信息
- **期望端点**: `/model/library/remote`
- **测试结果**: ❌ Bad Request: Bad target URL
- **状态**: 需要确认

### 6. 下载模型至本地
- **期望端点**: `/model/library/download`
- **测试结果**: ❌ 未测试
- **状态**: 需要确认

### 7. 装配
- **期望端点**: `/model/assemble`
- **测试结果**: ❌ 未测试
- **状态**: 需要确认

---

## 🔍 已确认存在的 API（测试通过）

以下 API 已经测试通过，可以正常使用：

### 场景与模型
- ✅ `/GetAllModelInfo` - 获取所有模型
- ✅ `/models/tree` - 获取层级树
- ✅ `/model/create` - 创建模型
- ✅ `/model/set_pose` - 设置姿态
- ✅ `/model/set_render` - 设置颜色
- ✅ `/ResetScene` - 重置场景
- ✅ `/ChangeMode` - 切换模式
- ✅ `/scene/get_scene_json` - 获取场景 JSON（复杂场景可能失败）

### 行为控制
- ✅ `/behavior/add` - 添加行为
- ✅ `/behavior/get` - 获取行为参数

### 相机
- ✅ `/sensor/queryCameralist` - 查询相机列表
- ❌ `/sbt/sensor` - 相机拍照（需要场景中有相机）

### 机器人
- ❌ `/query/robot_id` - 需要先选中机器人
- ❌ `/query/robot_pos` - 需要先选中机器人

---

## 💡 下一步行动

### 1. 确认 API 端点
联系坤吾软件开发商或查阅最新 API 文档，确认以下功能的正确端点：
- 层级关系管理
- 物体销毁
- 组件管理
- 模型库管理
- 装配功能

### 2. 可能的替代方案

**层级关系**: 可能在 `/GetAllModelInfo` 返回的数据中已经包含层级信息，可以通过 `children` 字段查看

**销毁物体**: 可能通过 `/ResetScene` 重置场景，或者在软件 UI 中手动操作

**模型库**: 可能是本地文件系统操作，不涉及 HTTP API

### 3. 建议的 API 命名（如果软件后续支持）

```javascript
// 层级关系
/model/set_parent        // 设置父节点
/model/get_parent        // 获取父节点
/model/get_children      // 获取子节点

// 销毁
/model/destroy           // 销毁物体
/model/destroy_component // 销毁组件

// 模型库
/model/library/local     // 本地模型库
/model/library/remote    // 远程模型库
/model/library/download  // 下载模型
/model/library/upload    // 上传模型

// 装配
/model/assemble          // 装配
/model/disassemble       // 拆卸
```

---

## 📝 当前 Skill 状态

### 已实现函数：51 个
- 模型管理：12 个
- 机器人控制：8 个
- 物流设备：5 个
- 传感器与物流：5 个
- 相机设备：2 个
- 场景管理：6 个
- 行为控制：2 个
- 进度与提示：2 个
- 批量与排产：2 个
- 模型库管理：7 个（已实现但未验证）

### 可正常使用的 API：约 20 个
主要集中在这几个领域：
- 场景管理
- 模型创建与查询
- 行为控制
- 模式切换

### 需要前置条件的 API：约 10 个
需要场景中有特定设备：
- 传感器
- 相机
- 传送带
- 机器人（需选中）

### 待确认的 API：约 7 个
用户提出但测试失败的端点

---

**更新时间**: 2026-03-12 23:25
**测试版本**: Kunwu Builder (坤吾)
