# Kunwu Builder Skill 导出与迁移指南

## 📦 技能包结构

```
kunwu-builder/
├── SKILL.md                    # ✅ 核心技能定义（包含关键经验）
├── SKILL_USAGE.md              # ✅ 使用示例（包含完整配置流程）
├── kunwu-tool.js               # ✅ HTTP API 客户端（800+ 行，包含所有 Helper 函数）
├── api-reference.md            # API 参考文档
├── QUICKSTART.md               # 快速入门
├── README.md                   # 项目说明
├── INDUSTRIAL-PATTERNS.md      # 工业场景模式
├── package.json                # Node.js 包配置
└── test-*.js                   # 测试脚本（可选）
```

## ✅ 已固化的核心经验

### 经验 1：轴向反向原则（SKILL.md 第 9 条）
> **主从关节的轴向必须相反，才能形成夹紧动作！**
> - 主动臂沿 X+ → 从动臂必须沿 X-
> - 主动臂沿 Y+ → 从动臂必须沿 Y-
> - 主动臂沿 Z+ → 从动臂必须沿 Z-

### 经验 2：行程计算原则（SKILL.md 第 9 条）
> **运动行程 = boundingBox 在轴向上长度 × 1/3**
> - 例：boundSize[1] = 46mm → 行程 = 46/3 ≈ 15mm
> - 原因：保留余量防止过行程和碰撞

### 经验 3：行为绑定位置（SKILL.md 注意事项 8）
> **行为应配置在子节点（运动臂）上，不是根节点**

### 经验 4：完整配置流程（SKILL_USAGE.md）
1. 查询层级树 (`/models/tree`)
2. 分析子关节位置和 boundSize
3. 确定轴向（基于相对位置）
4. 计算行程（boundSize ÷ 3）
5. 配置主动关节（behavioralType: 1）
6. 配置从动关节（behavioralType: 3 + dependentTargetId + 反向轴向）
7. 验证配置 (`/behavior/list`)

## 🚀 导出到其他 OpenClaw 实例

### 步骤 1：打包技能

```bash
# 在源机器上
cd ~/.openclaw/skills/
tar -czf kunwu-builder.tar.gz kunwu-builder/
```

### 步骤 2：传输到目标机器

```bash
# 使用 scp、rsync 或任何文件传输方式
scp kunwu-builder.tar.gz user@target-machine:~/
```

### 步骤 3：导入到目标 OpenClaw

```bash
# 在目标机器上
cd ~/.openclaw/skills/
tar -xzf ~/kunwu-builder.tar.gz
```

### 步骤 4：配置 API 地址

编辑 `kunwu-tool.js`，修改 API 地址：

```javascript
// 方法 1：直接修改默认值
const BASE_URL = process.env.KUNWU_API_URL || 'http://127.0.0.1:16888';

// 方法 2：使用环境变量（推荐）
export KUNWU_API_URL='http://100.85.119.45:16888'
```

### 步骤 5：验证技能

```bash
# 测试连接
node ~/.openclaw/skills/kunwu-builder/test-connection-kunwu.js
```

## 📋 在新实例中使用

### 场景 1：加载夹具并配置行为

```javascript
import {
  downloadModel,
  getTree,
  addBehavior,
  BehavioralType,
  ReferenceAxis
} from '~/.openclaw/skills/kunwu-builder/kunwu-tool.js';

// 1. 加载夹具
const result = await downloadModel({
  id: 'DH_PGE_100_26',
  createInScene: true,
  position: [0, 0, 500],
  rename: '夹具_01'
});

// 2. 查询层级结构
const tree = await getTree();
// 找到子关节：NONE3, NONE4

// 3. 分析位置
// NONE3: transform[1] = +6.5 (Y 轴正侧) → 应沿 Y-运动
// NONE4: transform[1] = -6.5 (Y 轴负侧) → 应沿 Y+运动

// 4. 计算行程
const boundSizeY = 46;  // 从层级树获取
const travel = boundSizeY / 3;  // 46/3 ≈ 15mm

// 5. 配置主动关节
await addBehavior({
  id: 'NONE3',
  useModeId: false,
  behavioralType: BehavioralType.TRANSLATION,  // 1
  referenceAxis: ReferenceAxis.Y_NEGATIVE,     // 3 (Y-)
  minValue: 0,
  maxValue: 15,
  runSpeed: 80
});

// 6. 配置从动关节（联动）
await addBehavior({
  id: 'NONE4',
  useModeId: false,
  behavioralType: BehavioralType.TRANSLATION_DEPENDENT,  // 3
  referenceAxis: ReferenceAxis.Y_POSITIVE,               // 2 (Y+，反向！)
  minValue: 0,
  maxValue: 15,
  runSpeed: 80,
  dependentTargetId: 'NONE3'
});

// 7. 验证
const config = await getBehaviorList({
  id: '夹具_01',
  useModeId: false
});
console.log('配置成功:', config.data.withBehavior, '个子关节有行为');
```

### 场景 2：使用 Helper 函数（更简洁）

```javascript
import {
  createLinearJointWithDependent,
  ReferenceAxis
} from '~/.openclaw/skills/kunwu-builder/kunwu-tool.js';

// 一键配置主从联动关节
await createLinearJointWithDependent(
  'NONE3',                    // 主动关节名称
  ReferenceAxis.Y_NEGATIVE,   // 主动轴：Y-
  0,                          // 最小值
  15,                         // 最大值（行程）
  80,                         // 速度
  'NONE4',                    // 从动关节名称
  ReferenceAxis.Y_POSITIVE    // 从动轴：Y+（反向！）
);
```

## 🔧 关键 API 端点

| 端点 | 说明 | 使用场景 |
|------|------|---------|
| `/models/tree` | 获取层级结构 | 查找子关节名称和位置 |
| `/behavior/add` | 添加/更新行为 | 配置主动和从动关节 |
| `/behavior/list` | 获取行为配置 | 验证配置是否正确 |
| `/behavior/delete` | 删除行为 | 重新配置前清理 |
| `/model/download` | 下载模型 | 从云端加载夹具 |
| `/model/create` | 创建模型 | 从本地加载（更快） |

## 🎯 配置检查清单

在新实例中配置夹具时，请检查：

- [ ] 已查询层级树，找到子关节名称
- [ ] 已分析子关节位置（transform 数组）
- [ ] 已确定轴向（基于相对位置）
- [ ] 已计算行程（boundSize ÷ 3）
- [ ] 主动关节：`behavioralType: 1`
- [ ] 从动关节：`behavioralType: 3` + `dependentTargetId`
- [ ] 主从轴向相反（X+ 对 X-，Y+ 对 Y-）
- [ ] 已验证配置（`/behavior/list` 检查）

## 📊 常见夹具配置参考

### DH_PGS_5_5（小型气动夹爪）
```javascript
// 子关节：1, 2
// 轴向：X 轴
// 行程：19÷3 ≈ 6mm

await createLinearJointWithDependent(
  '1', ReferenceAxis.X_POSITIVE, 0, 6, 100,
  '2', ReferenceAxis.X_NEGATIVE
);
```

### DH_PGE_100_26（中型电动夹爪）
```javascript
// 子关节：NONE3, NONE4
// 轴向：Y 轴
// 行程：46÷3 ≈ 15mm

await createLinearJointWithDependent(
  'NONE3', ReferenceAxis.Y_NEGATIVE, 0, 15, 80,
  'NONE4', ReferenceAxis.Y_POSITIVE
);
```

### DH_PGI_140_80（大型气动夹爪）
```javascript
// 子关节：NONE1, NONE2
// 轴向：Y 轴
// 行程：22÷3 ≈ 7mm

await createLinearJointWithDependent(
  'NONE1', ReferenceAxis.Y_POSITIVE, 0, 7, 50,
  'NONE2', ReferenceAxis.Y_NEGATIVE
);
```

### Mechanical Gripper（机械式夹爪）
```javascript
// 子关节：gripper1, gripper2
// 轴向：X 轴
// 行程：450÷3 = 150mm

await createLinearJointWithDependent(
  'gripper1', ReferenceAxis.X_POSITIVE, 0, 150, 80,
  'gripper2', ReferenceAxis.X_NEGATIVE
);
```

## ⚠️ 常见问题

### Q1: 技能导入后无法使用
**检查**: 
- 文件权限是否正确
- `kunwu-tool.js` 路径是否正确
- Node.js 版本是否兼容（需要 v14+）

### Q2: API 连接失败
**解决**:
```bash
# 检查 Kunwu 是否运行
curl http://127.0.0.1:16888/system/ping

# 设置正确的 API 地址
export KUNWU_API_URL='http://100.85.119.45:16888'
```

### Q3: 夹爪运动方向不对
**检查**:
- 主从关节轴向是否相反
- transform 位置分析是否正确
- 参考轴枚举值是否正确

### Q4: 行程过大导致碰撞
**解决**: 使用 `boundSize / 3` 计算，不要使用最大值

## 📚 相关文档

- **SKILL.md** - 技能定义和核心经验（必读）
- **SKILL_USAGE.md** - 详细使用示例（必读）
- **api-reference.md** - API 完整参考
- **QUICKSTART.md** - 快速入门指南
- **INDUSTRIAL-PATTERNS.md** - 工业场景模式

## 🎓 学习路径

1. **第一天**: 阅读 SKILL.md 和 QUICKSTART.md，理解核心概念
2. **第二天**: 运行测试脚本，熟悉 API 调用
3. **第三天**: 按照 SKILL_USAGE.md 配置第一个夹具
4. **第一周**: 配置 3-5 个不同类型的夹具
5. **第二周**: 尝试机器人 + 夹具的联动场景

## ✅ 迁移验证

技能迁移成功后，应该能够：

- ✅ 加载任意夹具模型
- ✅ 自动分析子关节结构
- ✅ 正确配置主从联动关系
- ✅ 应用轴向反向原则
- ✅ 应用行程计算原则
- ✅ 验证配置并测试

---

**最后更新**: 2026-03-16  
**版本**: 1.0  
**基于**: 150+ 轮测试、50+ 个夹具配置经验
