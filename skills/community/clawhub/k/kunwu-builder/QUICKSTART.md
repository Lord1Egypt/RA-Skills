# Kunwu Builder Skill - 快速开始

## ✅ 已创建的文件

```
~/.openclaw/skills/kunwu-builder/
├── SKILL.md              # 技能说明文档
├── README.md             # 详细使用指南
├── QUICKSTART.md         # 本文件
├── kunwu-tool.js         # API 工具库
├── test-connection-kunwu.js  # 连接测试脚本
└── package.json          # 项目配置
```

## 🚀 使用步骤

### 1. 启动 Kunwu Builder 软件

确保软件在 Windows 上运行，并且：
- 菜单栏 → 编辑 → 偏好设置 → 端口：**16888**
- 软件处于正常运行状态

### 2. 测试连接

```bash
cd ~/.openclaw/skills/kunwu-builder
node test-connection-kunwu.js
```

成功输出：
```
✅ 连接成功！
📦 场景中有 X 个模型
```

### 3. 开始控制

现在你可以通过自然语言控制软件了！

## 💬 可以这样说

### 场景管理
- "重置场景"
- "切换到机器人模式"
- "获取场景中所有模型"

### 模型操作
- "创建一个纸箱，位置在 10,20,30"
- "把机器人 r1 移动到 100,200,300"
- "导出机器人模型到 C:\Users\Sam\Desktop"
- "把 conveyer1 改成红色"

### 设备控制
- "让 conveyer1 号辊床开始正向运动"
- "停止传送带"
- "查询传感器 sensor1 的状态"

### 机器人
- "获取机器人 r1 的当前位置"
- "查询机器人 r1 的轨迹点"
- "计算机器人 r1 在 100,200,300 的逆解"

### 相机
- "用 camera1 拍张照"
- "查询所有相机"

## 🔧 测试命令

```bash
# 获取所有模型
node speedbot-tool.js /GetAllModelInfo

# 创建模型
node speedbot-tool.js /model/create '{"id":"纸箱","position":[10,20,30]}'

# 重置场景
node speedbot-tool.js /ResetScene
```

## 📝 注意事项

1. **软件必须运行**：SpeedBot Builder 需要在 Windows 上运行
2. **端口配置**：默认 16888，可在偏好设置中修改
3. **本地访问**：API 仅允许本地连接（127.0.0.1）
4. **JSON 格式**：所有请求参数必须是有效的 JSON

## ❓ 故障排查

### 连接失败
```
❌ Connection failed: connect ECONNREFUSED 127.0.0.1:16888
```
**解决**：启动 SpeedBot Builder 软件

### 400 错误
```
❌ API Error 400: Bad Request
```
**解决**：检查请求参数格式，确保 JSON 正确

### 模型找不到
```
❌ Model not found
```
**解决**：使用 `/GetAllModelInfo` 查看场景中的实际模型名称

## 🎯 下一步

1. 启动 SpeedBot Builder
2. 运行 `node test-connection.js` 测试连接
3. 开始用自然语言控制你的仿真软件！

有任何问题随时告诉我！🤖
