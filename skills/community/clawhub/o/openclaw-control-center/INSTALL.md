# 📦 openclaw-control-center 安装指南

## 快速安装（推荐：复制文件夹）

### Step 1：找到安装目录

打开文件管理器，导航到：

```
C:\Users\你的用户名\.qclaw\workspace\skills\
```

如果目录不存在，手动创建：
- 在 `C:\Users\你的用户名\.qclaw\` 下新建文件夹 `workspace`
- 在 `workspace` 下新建文件夹 `skills`

### Step 2：复制技能文件夹

将 `openclaw-control-center` 文件夹整个复制到：
```
C:\Users\你的用户名\.qclaw\workspace\skills\
```

最终目录结构应该是：
```
C:\Users\你的用户名\.qclaw\workspace\skills\
└── openclaw-control-center\
    ├── SKILL.md        ← 技能定义（必填）
    ├── README.md        ← 使用说明
    ├── INSTALL.md       ← 本安装指南
    ├── metadata.json    ← 技能元数据
    └── control-center\  ← 仪表盘模板（可选）
        └── template.html
```

### Step 3：重启 OpenClaw

重启 QClaw 桌面应用（或重启 Gateway），AI 会自动加载新技能。

### Step 4：验证安装成功

在 OpenClaw 对话框输入：
```
打开控制中心
```

如果浏览器自动打开了仪表盘，说明安装成功！

---

## 通过 OpenClaw AI 自动安装

在 OpenClaw 对话框直接发送：
```
帮我安装 openclaw-control-center 技能，技能在 ~/.qclaw/workspace/skills/openclaw-control-center/
```

AI 会帮你完成所有步骤。

---

## 手动安装（高级）

将文件夹复制到 `~/.qclaw/skills/`（全局共享目录）：
```
C:\Users\你的用户名\.qclaw\skills\
└── openclaw-control-center\
    └── SKILL.md
```

注意：`~/.qclaw/skills/` 的技能对所有 Agent 共享。

---

## 卸载

删除文件夹即可：
```
C:\Users\你的用户名\.qclaw\workspace\skills\openclaw-control-center\
```

无需重启，即时生效。

---

## 常见问题

**Q: 复制后 AI 找不到技能？**
A: 确认文件夹名称是 `openclaw-control-center`（不是 `openclaw-control-center-main`）

**Q: 仪表盘打不开？**
A: 尝试手动在浏览器地址栏输入：`file:///C:/Users/你的用户名/.qclaw/workspace/control-center.html`

**Q: 想修改仪表盘样式？**
A: 直接编辑 `control-center.html`，保存后刷新浏览器即可
