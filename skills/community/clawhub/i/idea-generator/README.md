# 🚀 冲击波创意工作台

AI 驱动的迭代式营销创意生成器。在 OpenClaw 对话框说一句话，AI 自动搜索+生成+评分，实时工作台全程可视化。

---

## 安装（3步）

### 第 1 步：解压并放到技能目录

将 `idea-generator/` 文件夹复制到以下任一位置：

```bash
# 方案A：用户工作区（推荐）
cp -r idea-generator/ ~/openclaw/workspace/skills/

# 方案B：OpenClaw 全局技能目录
cp -r idea-generator/ ~/.openclaw/skills/
```

### 第 2 步：重启 OpenClaw

```bash
openclaw gateway restart
```

### 第 3 步：直接用！

在 OpenClaw 对话框输入：

> 启动创意工作台，帮我为【你的产品/品牌】生成创意

AI 会自动：
1. 启动工作台服务
2. 在浏览器提示打开 `http://localhost:50000/live-dashboard.html`
3. 搜索百度 / B站获取行业洞察
4. 每轮生成 5 个候选创意，≥90分入围
5. 多轮迭代递进优化

---

## 前置要求

| 需求 | 说明 |
|------|------|
| OpenClaw | 已安装并运行（[安装指南](https://github.com/openclaw/openclaw)） |
| Python 3.8+ | 通常系统自带；无需 pip install（纯标准库） |
| 网络 | 可访问百度、B站 |

---

## 触发方式

直接在对话框说（任意一种）：

- `启动创意工作台`
- `帮我想关于XX的创意`
- `为XX产品出个营销方案`
- `头脑风暴：XX`

如果没带主题，AI 会追问你具体需求。

---

## 端口说明

默认端口：**50000**

如需更换：
```bash
echo "51000" > idea-generator/scripts/.server_port
```

---

## 文件结构

```
idea-generator/
├── README.md               # 本文件
├── SKILL.md                # OpenClaw 技能描述（AI 读取）
├── scripts/
│   ├── server.py           # API 服务器（状态管理 + SSE 推送）
│   ├── start.sh            # 手动启动脚本（可选）
│   ├── live-dashboard.html # 实时工作台前端
│   └── requirements.txt    # Python 依赖说明（纯标准库）
└── references/
    ├── creative-standards.md  # 创意生成标准（AI 读取）
    └── scoring-guide.md       # 评分详解（AI 读取）
```

---

## 常见问题

**Q：说「启动创意工作台」没反应？**  
确认 OpenClaw 已重启（`openclaw gateway restart`），技能目录位置正确。

**Q：工作台打不开？**  
检查端口占用：`lsof -i :50000`。换个端口：`echo "51000" > scripts/.server_port`。

**Q：AI 没有开始生成创意？**  
重新对话，明确说出主题，例如：「帮我为XX品牌生成3轮创意」。

**Q：停止后任务还在执行？**  
点击「停止」后等 5-10 秒。强制重置：`bash scripts/start.sh`。
