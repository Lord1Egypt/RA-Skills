# Kunwu Builder Skill - 使用示例（2026-03-16 11:50 更新）

## 🔑 关键经验（必须先读！）

### 经验 1：轴向反向原则
**主从关节的轴向必须相反，才能形成夹紧动作！**

| 主动臂轴向 | 从动臂轴向 | 说明 |
|-----------|-----------|------|
| X+ (0) | X- (1) | 相向运动夹紧 |
| Y+ (2) | Y- (3) | 相向运动夹紧 |
| Z+ (4) | Z- (5) | 相向运动夹紧 |

**错误示例** ❌：两个夹爪都沿 X+ 运动 → 同向移动，无法夹紧  
**正确示例** ✅：一个 X+ 一个 X- → 相向移动，夹紧工件

### 经验 2：行程计算原则
**运动行程 = boundingBox 在轴向上长度 × 1/3**

```javascript
// 从层级树获取 boundSize
const boundSize = child.boundSize;  // [sizeX, sizeY, sizeZ]

// 计算行程（保留 1/3 余量）
const travelX = boundSize[0] / 3;  // X 向行程
const travelY = boundSize[1] / 3;  // Y 向行程
const travelZ = boundSize[2] / 3;  // Z 向行程

// 示例：boundSize[1] = 46mm → 行程 = 46/3 ≈ 15mm
```

**为什么是 1/3？**
- 保留余量防止过行程
- 避免夹爪碰撞
- 实际夹持行程通常小于理论最大值

### 经验 3：dependentTargetId 必须配置（⚠️ 最关键！）
**从动关节必须配置 `dependentTargetId` 指向主动关节，否则无法联动！**

```javascript
// ❌ 错误：缺少 dependentTargetId
await callAPI('/behavior/add', {
  id: '夹具/从动臂',
  behavioralType: 3,
  referenceAxis: 1,
  // dependentTargetId: ??? 缺失！
});

// ✅ 正确：使用层级路径指定 dependentTargetId
await callAPI('/behavior/add', {
  id: '夹具/从动臂',
  behavioralType: 3,
  referenceAxis: 1,
  dependentTargetId: '夹具/主动臂',  // ✅ 必须配置！
  dependentTargetUseModeId: false
});
```

**验证要点**：
- 配置后检查 `dependentTargetId` 不为 null
- 应该显示为 UUID 或模型名称

---

## 行为配置示例

### 重要说明

**模型选择：** 使用"方形"模型，不是"纸箱"！

**枚举类型：**
- `BehavioralType` - 行为类型（0-5）
- `ReferenceAxis` - 参考轴（0-5，包含正负方向）
- `RunState` - 运行状态（0-3）

### 1. 创建旋转关节

```javascript
import { createRotaryJoint, ReferenceAxis, RobotJointPresets } from 'kunwu-tool.js';

// 方式 1：使用 ReferenceAxis 枚举（推荐）
await createRotaryJoint(modelId, ReferenceAxis.Z_POSITIVE, -180, 180, 90);

// 方式 2：使用轴名称（更清晰）
await createRotaryJoint(modelId, 'ZPositive', -180, 180, 90, true);

// 方式 3：使用预设配置
await createRotaryJoint(
  modelId,
  RobotJointPresets.BASE_ROTARY.axis,
  RobotJointPresets.BASE_ROTARY.min,
  RobotJointPresets.BASE_ROTARY.max,
  RobotJointPresets.BASE_ROTARY.speed
);

// 方式 4：简化调用（绕 Z 轴）
await createRotaryJoint(modelId, 4, -180, 180, 90);  // 4 = Z_POSITIVE
```

### 2. 创建直线关节

```javascript
import { createLinearJoint, ReferenceAxis } from 'kunwu-tool.js';

// X 轴直线运动，±500mm，速度 100mm/s
await createLinearJoint(modelId, ReferenceAxis.X_POSITIVE, -500, 500, 100);

// Y 轴直线运动，±400mm，速度 100mm/s
await createLinearJoint(modelId, ReferenceAxis.Y_POSITIVE, -400, 400, 100);

// Z 轴直线运动，±300mm，速度 80mm/s
await createLinearJoint(modelId, ReferenceAxis.Z_POSITIVE, -300, 300, 80);

// 使用轴名称
await createLinearJoint(modelId, 'XPositive', -500, 500, 100, true);
```

### 3. 创建参数化方形关节（优先使用 /model/create）

```javascript
import { createBoxJoint } from 'kunwu-tool.js';

// 创建关节，位置 [0,0,100]，尺寸 200×100×150mm
// 注意：
// 1. 使用"方形"模型，不是"纸箱"！
// 2. 优先使用 /model/create（检查本地仓库）
// 3. 所有单位是 mm（毫米）
await createBoxJoint('joint1', [0, 0, 100], 200, 100, 150);
```

**单位说明:**
- 位置：mm（毫米）
- 尺寸：mm（毫米）
- 角度：°（度）
- 速度：mm/s 或 °/s

### 4. 并行下载优化（使用"方形"模型）

```javascript
import { downloadModelsParallel, waitForTasks } from 'kunwu-tool.js';

// 同时下载 4 个模型，速度提升 60-70%
// 注意：使用"方形"模型，不是"纸箱"！
const taskIds = await downloadModelsParallel([
  { id: '方形', rename: 'base', position: [0, 0, 0] },
  { id: '方形', rename: 'joint1', position: [0, 0, 100] },
  { id: '方形', rename: 'joint2', position: [0, 0, 250] },
  { id: '方形', rename: 'joint3', position: [0, 0, 350] }
]);

// 等待所有任务完成
const results = await waitForTasks(taskIds);
```

### 5. 完整示例：3 轴机器人（使用"方形"）

```javascript
import {
  createBoxJoint,
  createRotaryJoint,
  setParent,
  downloadModelsParallel,
  waitForTasks,
  ReferenceAxis
} from 'kunwu-tool.js';

// 1. 并行创建所有关节（使用"方形"模型！）
const taskIds = await downloadModelsParallel([
  { id: '方形', rename: 'base', position: [0, 0, 0] },
  { id: '方形', rename: 'joint1', position: [0, 0, 100] },
  { id: '方形', rename: 'joint2', position: [0, 0, 250] },
  { id: '方形', rename: 'joint3', position: [0, 0, 350] }
]);

// 2. 等待完成
const results = await waitForTasks(taskIds);

// 3. 配置层级关系
await setParent({ 
  childId: results[1].resultData.modelId, 
  parentId: results[0].resultData.modelId, 
  useModeId: true 
});
await setParent({ 
  childId: results[2].resultData.modelId, 
  parentId: results[1].resultData.modelId, 
  useModeId: true 
});
await setParent({ 
  childId: results[3].resultData.modelId, 
  parentId: results[2].resultData.modelId, 
  useModeId: true 
});

// 4. 添加旋转行为（使用 ReferenceAxis 枚举）
await createRotaryJoint(results[1].resultData.modelId, ReferenceAxis.Z_POSITIVE, -180, 180, 90);   // J1: 绕 Z 轴
await createRotaryJoint(results[2].resultData.modelId, ReferenceAxis.Y_POSITIVE, -90, 90, 60);     // J2: 绕 Y 轴
await createRotaryJoint(results[3].resultData.modelId, ReferenceAxis.Y_POSITIVE, -90, 90, 60);     // J3: 绕 Y 轴
```

## 常量使用

```javascript
import { BehavioralType, ReferenceAxis, RunState, RobotJointPresets } from 'kunwu-tool.js';

// 行为类型（0-5）
console.log(BehavioralType.NONE);              // 0 - 无行为
console.log(BehavioralType.TRANSLATION);       // 1 - 平移（直线运动）
console.log(BehavioralType.ROTATE);            // 2 - 旋转
console.log(BehavioralType.TRANSLATION_DEPENDENT);  // 3 - 平移（联动）
console.log(BehavioralType.ROTATE_DEPENDENT);       // 4 - 旋转（联动）
console.log(BehavioralType.LOGISTICS_TRANSLATION);  // 5 - 物流平移

// 参考轴（0-5，包含正负方向）
console.log(ReferenceAxis.X_POSITIVE);   // 0 - X 正方向
console.log(ReferenceAxis.X_NEGATIVE);   // 1 - X 负方向
console.log(ReferenceAxis.Y_POSITIVE);   // 2 - Y 正方向
console.log(ReferenceAxis.Y_NEGATIVE);   // 3 - Y 负方向
console.log(ReferenceAxis.Z_POSITIVE);   // 4 - Z 正方向
console.log(ReferenceAxis.Z_NEGATIVE);   // 5 - Z 负方向

// 运行状态
console.log(RunState.STOP);    // 0
console.log(RunState.START);   // 1
console.log(RunState.REVERSE); // 2
console.log(RunState.RESET);   // 3

// 机器人关节预设
console.log(RobotJointPresets.BASE_ROTARY);
// { axis: 4, min: -180, max: 180, speed: 90 }  4 = Z_POSITIVE

console.log(RobotJointPresets.SHOULDER);
// { axis: 2, min: -90, max: 90, speed: 60 }   2 = Y_POSITIVE
```

## 关键参数说明

### BehavioralType（行为类型）

| 枚举值 | 常量名 | 说明 | 单位 |
|--------|--------|------|------|
| 0 | NONE | 无行为 | - |
| 1 | TRANSLATION | 平移（直线运动） | mm, mm/s |
| 2 | ROTATE | 旋转运动 | °, °/s |
| 3 | TRANSLATION_DEPENDENT | 平移（联动部件） | mm, mm/s |
| 4 | ROTATE_DEPENDENT | 旋转（联动部件） | °, °/s |
| 5 | LOGISTICS_TRANSLATION | 物流平移 | mm, mm/s |

### ReferenceAxis（参考轴）

| 枚举值 | 常量名 | 说明 | 直线运动 | 旋转运动 |
|--------|--------|------|---------|---------|
| 0 | X_POSITIVE | X 正方向 | 沿 X+ 平移 | 绕 X+ 旋转 |
| 1 | X_NEGATIVE | X 负方向 | 沿 X- 平移 | 绕 X- 旋转 |
| 2 | Y_POSITIVE | Y 正方向 | 沿 Y+ 平移 | 绕 Y+ 旋转 |
| 3 | Y_NEGATIVE | Y 负方向 | 沿 Y- 平移 | 绕 Y- 旋转 |
| 4 | Z_POSITIVE | Z 正方向 | 沿 Z+ 平移 | 绕 Z+ 旋转 |
| 5 | Z_NEGATIVE | Z 负方向 | 沿 Z- 平移 | 绕 Z- 旋转 |

### 典型机器人关节配置

| 关节 | behavioralType | referenceAxis | minValue | maxValue | runSpeed |
|------|---------------|---------------|----------|----------|----------|
| 基座旋转 | 2 (ROTATE) | 4 (Z_POSITIVE) | -180 | 180 | 90°/s |
| 肩关节 | 2 (ROTATE) | 2 (Y_POSITIVE) | -90 | 90 | 60°/s |
| 肘关节 | 2 (ROTATE) | 2 (Y_POSITIVE) | -90 | 90 | 60°/s |
| 腕关节旋转 | 2 (ROTATE) | 4 (Z_POSITIVE) | -180 | 180 | 120°/s |
| 腕关节弯曲 | 2 (ROTATE) | 2 (Y_POSITIVE) | -90 | 90 | 90°/s |

---

## 📚 完整示例：夹具行为配置（2026-03-16 更新）

### 示例 1：DH_PGI_140_80（大型气动夹具）

**步骤 1: 获取层级结构**
```javascript
const tree = await callAPI('/models/tree', {});
// 找到：
// 夹具_大型气动
//   ├── NONE1 (transform: [620, -17.35, 412.85], boundSize: [52, 22, 16.7])
//   └── NONE2 (transform: [580, 17.35, 412.85], boundSize: [52, 22, 16.7])
```

**步骤 2: 分析轴向**
```javascript
// 计算相对位置
const dy = -17.35 - 17.35;  // = -34.7mm (NONE1 在 Y 负方向)

// 确定轴向：NONE1 沿 Y- 运动，NONE2 沿 Y+ 运动（相向夹紧）
const activeAxis = ReferenceAxis.Y_NEGATIVE;    // Y-
const dependentAxis = ReferenceAxis.Y_POSITIVE; // Y+（反向！）
```

**步骤 3: 计算行程**
```javascript
const boundSizeY = 22;  // Y 方向尺寸
const travel = boundSizeY / 3;  // 22/3 ≈ 7mm（取整为 60mm 更安全）
```

**步骤 4: 配置行为**
```javascript
// 主动关节
await callAPI('/behavior/add', {
  id: 'NONE1',
  useModeId: false,
  behavioralType: 1,      // 直线运动
  referenceAxis: 1,       // Y 轴
  minValue: 0,
  maxValue: 60,
  runSpeed: 50
});

// 从动关节（联动）⚠️ 必须配置 dependentTargetId！
await callAPI('/behavior/add', {
  id: 'NONE2',
  useModeId: false,
  behavioralType: 3,      // 直线联动
  referenceAxis: 1,       // Y 轴
  minValue: 0,
  maxValue: 60,
  runSpeed: 50,
  dependentTargetId: 'NONE1',            // ⚠️ 关键：指向主动关节
  dependentTargetUseModeId: false
});
```

### 示例 2：完整配置流程（2026-03-16 最新实践）

```javascript
import { callAPI, ReferenceAxis } from 'kunwu-tool.js';

// 1. 加载夹具
await callAPI('/model/download', {
  id: 'DH_PGS_5_5',
  createInScene: true,
  position: [0, 0, 500],
  rename: '夹具_01'
});

// 2. 查询层级树
const tree = await callAPI('/models/tree', {});
const gripper = tree.data.models.find(m => m.modelName === '夹具_01');

// 3. 分析子关节位置
const child1 = gripper.children[0];  // 主动臂
const child2 = gripper.children[1];  // 从动臂

// 4. 计算相对位置，确定轴向
const dx = child2.transform[0] - child1.transform[0];
const activeAxis = dx < 0 ? ReferenceAxis.X_POSITIVE : ReferenceAxis.X_NEGATIVE;
const dependentAxis = dx < 0 ? ReferenceAxis.X_NEGATIVE : ReferenceAxis.X_POSITIVE;

// 5. 计算行程
const travel = child1.boundSize[0] / 3;  // X 向尺寸 ÷ 3

// 6. 配置主动关节
await callAPI('/behavior/add', {
  id: '夹具_01/' + child1.modelName,
  useModeId: false,
  behavioralType: 1,
  referenceAxis: activeAxis,
  minValue: 0,
  maxValue: travel,
  runSpeed: 100,
  targetValue: travel / 2
});

// 7. 配置从动关节 ⚠️ 必须配置 dependentTargetId！
await callAPI('/behavior/add', {
  id: '夹具_01/' + child2.modelName,
  useModeId: false,
  behavioralType: 3,
  referenceAxis: dependentAxis,  // 反向轴向！
  minValue: 0,
  maxValue: travel,
  runSpeed: 100,
  targetValue: travel / 2,
  // ⚠️ 关键：dependentTargetId 必须配置！
  dependentTargetId: '夹具_01/' + child1.modelName,
  dependentTargetUseModeId: false
});

// 8. 验证配置
const result = await callAPI('/behavior/list', {
  id: gripper.modelId,
  useModeId: true
});

// 9. 检查 dependentTargetId
const dependentJoint = result.data.items.find(i => i.behavioralType === 3);
if (dependentJoint.dependentTargetId === null) {
  console.error('❌ 错误：从动关节 dependentTargetId 未配置！');
} else {
  console.log('✅ 配置正确：从动关节已绑定到', dependentJoint.dependentTargetModelName);
}
```

### 示例 2：Mechanical Gripper（机械式夹具）

```javascript
// 层级结构
// 夹具_机械式
//   ├── gripper1 (boundSize: [450, 1250, 1802])
//   └── gripper2 (boundSize: [450, 1250, 1802])

// 分析：gripper1 在左侧，gripper2 在右侧 → X 轴向开合
const boundSizeX = 450;
const travel = boundSizeX / 3;  // 450/3 = 150mm（取 400mm 最大行程）

// 主动关节（gripper1 沿 X+）
await callAPI('/behavior/add', {
  id: 'gripper1',
  useModeId: false,
  behavioralType: 1,
  referenceAxis: 0,       // X 轴
  minValue: 0,
  maxValue: 400,
  runSpeed: 80
});

// 从动关节（gripper2 沿 X-，反向！）
await callAPI('/behavior/add', {
  id: 'gripper2',
  useModeId: false,
  behavioralType: 3,
  referenceAxis: 0,       // X 轴
  minValue: 0,
  maxValue: 400,
  runSpeed: 80,
  dependentTargetId: 'gripper1',
  dependentTargetUseModeId: false
});
```

### 验证配置

```javascript
const result = await callAPI('/behavior/list', {
  id: '夹具_大型气动',
  useModeId: false
});

console.log('主动关节:', result.data.items[1].modelName);
console.log('  behavioralType:', result.data.items[1].behavioralType);  // 1
console.log('  referenceAxis:', result.data.items[1].referenceAxis);    // 1 (Y)

console.log('从动关节:', result.data.items[2].modelName);
console.log('  behavioralType:', result.data.items[2].behavioralType);  // 3 (联动)
console.log('  dependentTargetId:', result.data.items[2].dependentTargetId);  // NONE1
```

---

## 🔧 常见问题排查

### Q1: 夹爪不同步运动
**原因**: 从动关节未设置 `dependentTargetId`  
**解决**: 确保 `behavioralType: 3` + `dependentTargetId: '主动关节名称'`

### Q2: 夹爪同向移动，无法夹紧
**原因**: 主从关节轴向相同  
**解决**: 从动关节的 `referenceAxis` 必须与主动关节相反（X+ 对 X-）

### Q3: 行程过大导致碰撞
**原因**: maxValue 设置过大  
**解决**: 使用 `boundSize / 3` 计算安全行程

### Q4: 找不到子关节
**原因**: 子关节名称重复  
**解决**: 使用层级路径如 `'夹具_大型气动/NONE1'`

---

## ✅ 行为配置检查清单（2026-03-16 最终版，必须逐项检查！）

### 配置前检查
- [ ] 已调用 `/models/tree` 获取层级结构
- [ ] 已读取子关节的 `transform` 数组（计算相对位置）
- [ ] 已读取子关节的 `boundSize` 数组（确定最大轴）
- [ ] **已使用 bounding 最大轴方法确定运动轴向** ⚠️

### 配置时检查
- [ ] 主动关节 `behavioralType: 1`（直线）或 `2`（旋转）
- [ ] 从动关节 `behavioralType: 3`（直线联动）或 `4`（旋转联动）
- [ ] **主从关节轴向相反**（如 X+ 对 X-）⚠️
- [ ] **行程 = boundSize[axisIndex] ÷ 3** ⚠️
- [ ] **从动关节 `dependentTargetId` 已配置** ⚠️⚠️
- [ ] **`dependentTargetUseModeId: false`** ⚠️

### 配置后验证
- [ ] 调用 `/behavior/list` 验证配置
- [ ] 父模型 `hasBehavior: false`
- [ ] 主动关节 `hasBehavior: true`, `dependentTargetId: null`
- [ ] **从动关节 `hasBehavior: true`, `dependentTargetId` 不为 null** ⚠️⚠️
- [ ] 从动关节 `dependentTargetModelName` 显示主动关节名称
- [ ] 主从轴向相反（验证 referenceAxis）

### 常见错误（避免！）
- ❌ 使用 transform 相对位置判断轴向（可能误判）
- ❌ 忘记配置 `dependentTargetId`
- ❌ `dependentTargetId` 使用 modelId 而不是层级路径
- ❌ 主从关节轴向相同（都沿 X+）
- ❌ 行程设置过大（使用 boundSize 而不是 boundSize/3）
- ❌ 行为配置在父模型上而不是子关节

---

## 📝 配置记录模板（推荐保存）

```markdown
## 夹具行为配置记录

**夹具名称**: [名称]  
**型号**: [型号]  
**配置日期**: 2026-03-16

### 层级结构
```
[夹具名称]
├── [子关节 1] - transform: [x, y, z], boundSize: [sx, sy, sz]
└── [子关节 2] - transform: [x, y, z], boundSize: [sx, sy, sz]
```

### 轴向判断（bounding 最大轴方法）
```javascript
const boundSize = child1.boundSize;  // [sx, sy, sz]
const maxSize = Math.max(...boundSize);  // 最大轴

// 判断结果：[X/Y/Z] 轴是最大轴 → [X/Y/Z] 轴开合
```

### 参数计算
- **相对位置**: dx = ?, dy = ?, dz = ?
- **bounding 最大轴**: [X/Y/Z] 轴 ([size]mm)
- **主动轴向**: [方向] (referenceAxis: ?)
- **从动轴向**: [方向] (referenceAxis: ?) ← 反向！
- **行程**: [size] ÷ 3 ≈ [travel]mm

### 配置结果
```javascript
// 主动关节
{
  id: '[夹具名称]/[主动关节]',
  behavioralType: 1,
  referenceAxis: ?,  // [方向]
  maxValue: [travel]
}

// 从动关节
{
  id: '[夹具名称]/[从动关节]',
  behavioralType: 3,
  referenceAxis: ?,  // [反向！]
  maxValue: [travel],
  dependentTargetId: '[夹具名称]/[主动关节]'  // ✅ 已配置
}
```

### 验证结果
- [x] 父模型 hasBehavior: false
- [x] 主动关节 dependentTargetId: null
- [x] 从动关节 dependentTargetId: "xxx-xxx-xxx" (不为 null)
- [x] 主从轴向相反（[轴+] 对 [轴-]）

### 备注
- [其他注意事项]
```

---

## 📊 实测案例总结（2026-03-16 验证）

### 案例 1：DH_PGS_5_5（小型气动夹具）
```
boundSize: [13, 19, 22.5]
最大轴：X 轴 (13mm) → X 轴开合
行程：13÷3≈4mm
配置：referenceAxis 0 (X+) 和 1 (X-) ✅
```

### 案例 2：DH_PGI_140_80（大型气动夹具）⚠️ 修正案例
```
boundSize: [52, 22, 16.7]
最大轴：X 轴 (52mm) → X 轴开合
行程：52÷3≈17mm

错误配置（已修正）:
- 误用 transform 判断：ΔY=34.7mm → Y 轴开合 ❌
- 正确判断：boundSize 最大轴 X(52mm) → X 轴开合 ✅

配置：referenceAxis 0 (X+) 和 1 (X-) ✅
```

### 案例 3：DH_PGE_100_26（电动中型夹具）
```
boundSize: [18.5, 46, 19.5]
最大轴：Y 轴 (46mm) → Y 轴开合
行程：46÷3≈15mm
配置：referenceAxis 3 (Y-) 和 2 (Y+) ✅
```

### 案例 4：DH_RGD_5_14（旋转型夹具）
```
boundSize: [40, 18.5, 19.5]
最大轴：X 轴 (40mm) → X 轴开合（直线运动）
行程：40÷3≈13mm
配置：referenceAxis 0 (X+) 和 1 (X-) ✅
```

### 关键经验
1. ✅ **bounding 最大轴方法最可靠** - 避免 transform 误判
2. ✅ **dependentTargetId 必须配置** - 否则无法联动
3. ✅ **行程 = boundSize ÷ 3** - 保留余量防碰撞
4. ✅ **轴向必须相反** - 才能形成夹紧动作
```

配置完成后，请按以下清单逐项检查：

### 配置前检查
- [ ] 已调用 `/models/tree` 获取层级结构
- [ ] 已读取子关节的 `transform` 数组
- [ ] 已读取子关节的 `boundSize` 数组
- [ ] 已计算相对位置（dx, dy, dz）

### 配置时检查
- [ ] 主动关节 `behavioralType: 1`（直线）或 `2`（旋转）
- [ ] 从动关节 `behavioralType: 3`（直线联动）或 `4`（旋转联动）
- [ ] 主从关节轴向相反（如 X+ 对 X-）
- [ ] 行程 = boundSize ÷ 3
- [ ] **从动关节 `dependentTargetId` 已配置** ⚠️
- [ ] **`dependentTargetUseModeId: false`** ⚠️

### 配置后验证
- [ ] 调用 `/behavior/list` 验证配置
- [ ] 父模型 `hasBehavior: false`
- [ ] 主动关节 `hasBehavior: true`, `dependentTargetId: null`
- [ ] **从动关节 `hasBehavior: true`, `dependentTargetId` 不为 null** ⚠️
- [ ] 从动关节 `dependentTargetModelName` 显示主动关节名称

### 常见错误
- ❌ 忘记配置 `dependentTargetId`
- ❌ `dependentTargetId` 使用 modelId 而不是层级路径
- ❌ 主从关节轴向相同（都沿 X+）
- ❌ 行程设置过大（使用 boundSize 而不是 boundSize/3）
- ❌ 行为配置在父模型上而不是子关节

---

## 📝 配置记录模板

```markdown
## 夹具行为配置记录

**夹具名称**: 夹具_01  
**型号**: DH_PGS_5_5  
**配置日期**: 2026-03-16

### 层级结构
```
夹具_01
├── 1 (主动臂) - transform[0]: -8, boundSize[0]: 13
└── 2 (从动臂) - transform[0]: +8, boundSize[0]: 13
```

### 参数计算
- **相对位置**: dx = 8 - (-8) = 16mm (>0，主动臂在左侧)
- **主动轴向**: X+ (referenceAxis: 0)
- **从动轴向**: X- (referenceAxis: 1) ← 反向！
- **行程**: 13 ÷ 3 ≈ 4mm

### 配置结果
```javascript
// 主动关节
{
  id: '夹具_01/1',
  behavioralType: 1,
  referenceAxis: 0,
  maxValue: 4
}

// 从动关节
{
  id: '夹具_01/2',
  behavioralType: 3,
  referenceAxis: 1,  // 反向！
  maxValue: 4,
  dependentTargetId: '夹具_01/1'  // ✅ 已配置
}
```

### 验证结果
- [x] 父模型 hasBehavior: false
- [x] 主动关节 dependentTargetId: null
- [x] 从动关节 dependentTargetId: "xxx-xxx-xxx" (不为 null)
- [x] 主从轴向相反（X+ 对 X-）
```
