# Kunwu Builder 控制技能

控制 Kunwu Builder (坤吾) 工业仿真软件的 HTTP API。

## 基础信息

| 项目 | 值 |
|------|-----|
| **API 地址** | `http://192.168.30.9:16888` |
| **认证** | 无 |
| **请求方式** | POST |
| **Content-Type** | `application/json` |

## 工具

### `kunwu_call`

```bash
kunwu_call endpoint="/model/create" data='{"id":"M900iB_280L","position":[0,0,0],"checkFromCloud":true}'
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `endpoint` | ✅ | API 路径 |
| `method` | ❌ | HTTP 方法，默认 `POST` |
| `data` | ❌ | 请求体 JSON |

---

## 常用 API

### 1. 模型加载机制（核心流程）⚡

**唯一推荐方式：使用 `/model/create` + `checkFromCloud=true`**

```bash
kunwu_call endpoint="/model/create" data='{
  "id": "M900iB_280L",
  "rename": "机器人_右",
  "position": [0, 2500, 515],
  "eulerAngle": [0, 0, 0],
  "checkFromCloud": true
}'
```

**机制说明：**
- `checkFromCloud: true` → 本地有直接加载（快速），本地没有自动从云端下载
- `checkFromCloud: false` → 仅从本地加载，本地没有则失败

**决策树：**
```
需要加载模型？
  ├─ 是 → 用 /model/create + checkFromCloud:true（99% 场景）
  └─ 否 → 不需要任何操作
```

**步骤 1: 直接使用 /model/create 创建模型**
```bash
kunwu_call endpoint="/model/create" data='{
  "id": "辊床_01",
  "position": [0, 0, 0],
  "checkFromCloud": true
}'
```

**批量加载（推荐）：使用 `scripts/model-loader.js`**
```bash
# 准备 models.json
node scripts/model-loader.js models.json

# 环境变量指定 API 地址
KUNWU_API_URL=http://192.168.30.9:16888 node scripts/model-loader.js models.json
```

**步骤 2: 设置模型参数化（如支持）**
```bash
kunwu_call endpoint="/model/set_pose" data='{
  "id": "皮带线_01",
  "position": [-11013.5, -603.5, 0],
  "eulerAngle": [0, 0, -90],
  "parameterizationCfg": [
    {"type": 0, "value": 10000},
    {"type": 1, "value": 1460},
    {"type": 2, "value": 1000}
  ]
}'
```

**ModelName 说明：**
- 使用本地模型库中的 `modelName` 字段值
- 常见模型：`辊床_01`, `M900iB_280L`, `方形底座_02`, `吸盘_10`, `托盘_07`

**参数化模型说明：**
- 部分模型支持参数化（如皮带线、方形等）
- 使用 `/model/set_pose` 设置参数化配置
- `parameterizationCfg` 格式：`[{"type": 0, "value": 值}, ...]`
- type 编号含义：0=长，1=宽，2=高（具体参考模型文档）

### 2. 场景查询

**获取层级树**
```bash
kunwu_call endpoint="/models/tree" data='{"rootId":"scene","useModeId":true}'
```

### 3. 装配（核心）

```bash
kunwu_call endpoint="/model/assemble" data='{
  "childId": "子模型 modelId",
  "parentId": "父模型 modelId",
  "assemblePosIndex": 0,
  "replaceExisting": false
}'
```

**响应码：**
- `200` - 装配成功
- `409` - 装配位被占用（设置 `replaceExisting: true` 替换）

### 4. 销毁模型

```bash
kunwu_call endpoint="/model/destroy" data='{"id":"modelId","useModeId":true}'
```

---

## 夹具行为配置（核心功能）

### 四大原则（必须遵守！）

| 原则 | 说明 | 示例 |
|------|------|------|
| **1. 轴向判断** | 使用 transform 相对位置确定运动轴向 | ΔX 最大 → X 轴开合 |
| **2. 相向夹紧** | 主动臂朝中心运动，从动臂反向 | 主动 X+ → 从动 X- |
| **3. 行程计算** | 行程 = boundSize ÷ 3 | 52mm → 17mm |
| **4. 联动配置** | 从动臂必须配置 `dependentTargetId` | ⚠️ 不配无法联动 |

### 轴向对照表

| 轴向 | 值 | 相反轴向 | 值 | 异或 |
|------|-----|----------|-----|------|
| X+ | 0 | X- | 1 | `0^1=1` |
| Y+ | 2 | Y- | 3 | `2^1=3` |
| Z+ | 4 | Z- | 5 | `4^1=5` |

**快速反向：** `dependentAxis = activeAxis ^ 1`

### 7 步配置流程

```bash
# 步骤 1: 获取层级树
kunwu_call endpoint="/models/tree" data='{"rootId":"scene"}'

# 步骤 2-3: 分析结构，确定轴向
# 读取 transform 计算 ΔX/ΔY/ΔZ，选最大值的轴
# 根据相对位置确定方向（相向夹紧原则）

# 步骤 4: 计算行程
# travel = boundSize[axisIndex] / 3

# 步骤 5: 配置主动臂 (behavioralType: 1)
kunwu_call endpoint="/behavior/add" data='{
  "id": "DH_PGS_5_5/1",
  "useModeId": false,
  "behavioralType": 1,
  "referenceAxis": 0,
  "minValue": 0,
  "maxValue": 4,
  "runSpeed": 80,
  "targetValue": 2
}'

# 步骤 6: 配置从动臂 (behavioralType: 3 + dependentTargetId！)
kunwu_call endpoint="/behavior/add" data='{
  "id": "DH_PGS_5_5/2",
  "useModeId": false,
  "behavioralType": 3,
  "referenceAxis": 1,
  "minValue": 0,
  "maxValue": 4,
  "runSpeed": 80,
  "targetValue": 2,
  "dependentTargetId": "DH_PGS_5_5/1",
  "dependentTargetUseModeId": false
}'

# 步骤 7: 验证配置
kunwu_call endpoint="/behavior/list" data='{"id":"夹具 modelId","useModeId":true}'
```

### 实测案例

| 夹具型号 | ΔX | ΔY | ΔZ | 轴向 | 行程 |
|----------|----|----|----|------|------|
| DH_PGS_5_5 | 16mm | - | - | X 轴 | 4mm |
| DH_PGI_140_80 | 40mm | 34.7mm | - | X 轴 | 17mm |
| DH_PGE_100_26 | - | 46mm | - | Y 轴 | 15mm |
| DH_RGD_5_14 | 40mm | - | - | X 轴 | 13mm |

---

## 完整示例：搭建双机器人工作站（带托盘布局）

**方式 A: 使用批量加载工具（推荐）**
```bash
node scripts/model-loader.js scripts/models-dual-robot-trays.json
```

**方式 B: 手动逐步创建**
```bash
# 步骤 1: 创建模型（使用 checkFromCloud=true，本地有则快，没有自动下载）
# 1.1 输送线
kunwu_call endpoint="/model/create" data='{
  "id": "辊床_01",
  "rename": "输送线",
  "position": [0, 0, 0],
  "checkFromCloud": true
}'

# 1.2 底座×2
kunwu_call endpoint="/model/create" data='{
  "id": "方形底座_02",
  "rename": "底座_右",
  "position": [0, 2500, 0],
  "checkFromCloud": true
}'
kunwu_call endpoint="/model/create" data='{
  "id": "方形底座_02",
  "rename": "底座_左",
  "position": [0, -2500, 0],
  "checkFromCloud": true
}'

# 1.3 机器人×2
kunwu_call endpoint="/model/create" data='{
  "id": "M900iB_280L",
  "rename": "机器人_右",
  "position": [0, 2500, 515],
  "checkFromCloud": true
}'
kunwu_call endpoint="/model/create" data='{
  "id": "M900iB_280L",
  "rename": "机器人_左",
  "position": [0, -2500, 515],
  "checkFromCloud": true
}'

# 1.4 吸盘×2
kunwu_call endpoint="/model/create" data='{
  "id": "吸盘_10",
  "rename": "吸盘_右",
  "position": [0, 2500, 2000],
  "checkFromCloud": true
}'
kunwu_call endpoint="/model/create" data='{
  "id": "吸盘_10",
  "rename": "吸盘_左",
  "position": [0, -2500, 2000],
  "checkFromCloud": true
}'

# 1.5 托盘×4（分布在机器人前后两侧）
kunwu_call endpoint="/model/create" data='{
  "id": "托盘_07",
  "rename": "托盘_右前",
  "position": [3000, 4500, 0],
  "checkFromCloud": true
}'
kunwu_call endpoint="/model/create" data='{
  "id": "托盘_07",
  "rename": "托盘_右后",
  "position": [3000, 500, 0],
  "checkFromCloud": true
}'
kunwu_call endpoint="/model/create" data='{
  "id": "托盘_07",
  "rename": "托盘_左前",
  "position": [3000, -500, 0],
  "checkFromCloud": true
}'
kunwu_call endpoint="/model/create" data='{
  "id": "托盘_07",
  "rename": "托盘_左后",
  "position": [3000, -4500, 0],
  "checkFromCloud": true
}'

# 步骤 2: 设置参数化（必须同时传 position + eulerAngle + parameterizationCfg）
kunwu_call endpoint="/model/set_pose" data='{
  "id": "输送线 modelId",
  "useModeId": true,
  "position": [0, 0, 0],
  "eulerAngle": [0, 0, 0],
  "parameterizationCfg": [
    {"type": 0, "value": 7940},
    {"type": 1, "value": 4340},
    {"type": 2, "value": 708}
  ]
}'

kunwu_call endpoint="/model/set_pose" data='{
  "id": "底座_右 modelId",
  "useModeId": true,
  "position": [0, 2500, 0],
  "eulerAngle": [0, 0, 0],
  "parameterizationCfg": [
    {"type": 0, "value": 1000},
    {"type": 1, "value": 1000},
    {"type": 2, "value": 515}
  ]
}'

# 步骤 3: 获取模型 ID 并执行装配
# 吸盘 → 机器人 → 底座
kunwu_call endpoint="/model/assemble" data='{
  "childId": "吸盘 modelId",
  "parentId": "机器人 modelId",
  "assemblePosIndex": 0,
  "useModeId": true
}'
kunwu_call endpoint="/model/assemble" data='{
  "childId": "机器人 modelId",
  "parentId": "底座 modelId",
  "assemblePosIndex": 0,
  "useModeId": true
}'
```

**托盘布局说明：**
```
         Y+
          ↑
    左后  |  右后
    ──────┼──────
    左前  |  右前
          |
──────────┼──────────→ X+
    输送线 (0,0)
    
机器人_右：Y=2500
机器人_左：Y=-2500
托盘_右前：(3000, 4500)   托盘_右后：(3000, 500)
托盘_左前：(3000, -500)   托盘_左后：(3000, -4500)
```

---

## 装配规则

**正确层级：**
```
场景
├── 地轨/底座 → 机器人 → 夹具
├── 桁架 → 自由臂 → 抓手
└── 相机支架 → 相机
```

**错误示例：** ❌ 底座 → 桁架（两者都是支撑结构，不应互相装配）

**多装配位选择规则：**
1. 优先 `assemblePosName`（按名称匹配）
2. 优先 `assemblePosIndex >= 0`（兼容位）
3. 自动选择（先找兼容且空闲位）

---

## 完整 API 参考

### 模型库管理

| 接口 | 说明 | 示例 |
|------|------|------|
| `/model/library/local` | 获取本地模型库 | `{"get":"true"}` |
| `/model/library/remote` | 获取远程模型库 | `{"pageNum":1,"pageSize":10}` |
| `/model/library/categories` | 获取分类列表 | `{}` |
| `/model/library/favorites` | 获取收藏列表 | `{}` |
| `/model/library/favorite` | 收藏模型 | `{"id":"模型名"}` |
| `/model/library/delete` | 删除本地模型 | `{"id":"模型名"}` |

### 模型创建与加载

| 接口 | 说明 | 示例 |
|------|------|------|
| `/model/create` | 创建/加载模型（唯一推荐） | `{"id":"模型名","position":[x,y,z],"checkFromCloud":true}` |
| `/model/set_pose` | 设置位置/参数化 | `{"id":"模型名","position":[x,y,z],"parameterizationCfg":[...]}` |
| `/model/set_render` | 设置渲染颜色 | `{"id":"模型名","color":"#FF0000"}` |
| `/model/export` | 导出模型 | `{"id":"模型名"}` |
| `/model/destroy` | 销毁模型 | `{"id":"modelId","useModeId":true}` |

**重要：** 始终使用 `/model/create` 并设置 `checkFromCloud: true`：
- 本地有模型 → 直接加载（快速）
- 本地没有 → 自动从云端下载（无需额外步骤）

**⚠️ 参数化设置注意事项：**
`/model/set_pose` 设置参数化时**必须同时传位置和角度**，否则返回 406 错误！

```bash
# ✅ 正确 - 三者一起传
kunwu_call endpoint="/model/set_pose" data='{
  "id": "皮带线_01",
  "position": [0, 0, 0],
  "eulerAngle": [0, 0, 0],
  "parameterizationCfg": [
    {"type": 0, "value": 7940},
    {"type": 1, "value": 4340},
    {"type": 2, "value": 708}
  ]
}'

# ❌ 错误 - 只传参数化会失败（406 NotAcceptable）
kunwu_call endpoint="/model/set_pose" data='{
  "id": "皮带线_01",
  "parameterizationCfg": [...]
}'
```

### 场景查询

| 接口 | 说明 | 示例 |
|------|------|------|
| `/models/tree` | 获取场景层级树 | `{"rootId":"scene","useModeId":true}` |
| `/GetModelInfo` | 获取单个模型信息 | `{"id":"modelId","useModeId":true}` |
| `/GetAllModelInfo` | 获取所有模型信息 | `{}` |
| `/scene/get_scene_json` | 获取场景 JSON | `{}` |

### 层级与装配

| 接口 | 说明 | 示例 |
|------|------|------|
| `/model/assemble` | 装配到指定位置 | `{"childId":"xxx","parentId":"xxx","assemblePosIndex":0}` |
| `/model/set_parent` | 设置父子关系 | `{"childId":"xxx","parentId":"xxx"}` |

### 行为控制

| 接口 | 说明 | 示例 |
|------|------|------|
| `/behavior/add` | 添加行为 | `{"id":"模型/子节点","behavioralType":1,"referenceAxis":0,...}` |
| `/behavior/list` | 获取行为配置列表 | `{"id":"modelId","useModeId":true}` |
| `/behavior/get` | 获取行为参数 | `{"id":"模型/子节点","useModeId":false}` |
| `/behavior/delete` | 删除行为 | `{"id":"模型/子节点","useModeId":false}` |

### 其他功能

| 接口 | 说明 | 示例 |
|------|------|------|
| `/batch/execute` | 批量执行命令 | `{"commands":[{"url":"...","body":{}}]}` |
| `/view/show_progress` | 显示进度条 | `{"progress":50,"message":"处理中..."}` |
| `/ResetScene` | 重置场景 | `{}` |
| `/ChangeMode` | 切换模式 | `{"mode":0}` (0:构建 1:信号 2:机器人 3:孪生) |

---

## 错误码

| Code | 说明 | 处理 |
|------|------|------|
| 200 | 成功 | - |
| 202 | 任务运行中 | 等待后查询 |
| 400 | 请求错误 | 检查参数 |
| 404 | 资源不存在 | 检查 modelId |
| 409 | 装配位被占用 | `replaceExisting: true` |

---

## 快速参考

**参考轴 (referenceAxis)：** `0`=X+, `1`=X-, `2`=Y+, `3`=Y-, `4`=Z+, `5`=Z-

**行为类型 (behavioralType)：** `1`=主动，`3`=从动

**层级路径：** `"DH_PGS_5_5/1"` → 夹具的第一个子关节

---

## 更新日志

- **2026-03-20**: 统一模型加载机制（仅用 `/model/create + checkFromCloud:true`），彻底移除 `/model/download`
- **2026-03-19 (3)**: 补充完整 API 参考表（25+ 接口）
- **2026-03-19 (2)**: 新增参数化设置方法（/model/set_pose）+ 完整场景搭建示例
- **2026-03-16**: 固化四大原则 + 相向夹紧原则 + 7 步流程
- **2026-03-14**: 支持从属运动配置
- **2026-03-13**: 新增模型库管理
