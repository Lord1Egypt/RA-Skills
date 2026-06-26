# PMOS Search Menu Skill

自动化爬取甘肃电力交易平台（PMOS）网站的菜单导航路径。

## 功能

- 🌐 自动打开 PMOS 网站
- 🔐 支持手动登录后继续操作
- 📍 按照指定路径逐级点击菜单
- 🔄 自动处理新标签页的打开和切换
- 📋 支持深度嵌套的菜单结构

## 安装

本 skill 已位于本地工作区：
```
C:\openclaw-workspace\skills\pmos-search-menu-skill
```

## 使用方法

### 方式 1: 手动执行 browser 命令

按照 `references/NAVIGATION_PATH.md` 中的步骤手动执行每个菜单点击操作。

### 方式 2: 使用 PowerShell 脚本

```powershell
cd C:\openclaw-workspace\skills\pmos-search-menu-skill
.\scripts\navigate-pmos.ps1 -MenuPath "信息披露","综合查询","市场运营","交易组织及出清","现货市场申报、出清信息","实时各节点出清类信息","实时市场出清节点电价"
```

### 方式 3: 使用 Node.js 脚本

```bash
node scripts/navigate-pmos.js
```

### 方式 4: 使用 Bash 脚本

```bash
./scripts/navigate-pmos.sh "信息披露" "综合查询" "市场运营"
```

## 完整菜单路径

```
信息披露 
  → 综合查询 (打开新标签页)
    → 市场运营 
      → 交易组织及出清 
        → 现货市场申报、出清信息 
          → 实时各节点出清类信息 
            → 实时市场出清节点电价
```

## 文件结构

```
pmos-search-menu-skill/
├── SKILL.md                      # Skill 描述文件
├── clawhub.json                  # ClawHub 配置
├── README.md                     # 使用说明
├── references/
│   └── NAVIGATION_PATH.md        # 详细导航路径记录
└── scripts/
    ├── navigate-pmos.ps1         # PowerShell 脚本
    ├── navigate-pmos.sh          # Bash 脚本
    └── navigate-pmos.js          # Node.js 脚本
```

## 注意事项

1. **登录状态**: 使用前必须先手动登录 PMOS 网站
2. **新标签页**: 点击"综合查询"会打开新标签页，后续操作都在新标签页进行
3. **动态引用**: 页面元素的 aria-ref 可能会变化，每次操作前建议重新获取快照
4. **iframe 内容**: 部分页面内容可能在 iframe 内，需要特殊处理
5. **等待时间**: 菜单展开和页面加载需要时间，建议操作间添加适当延迟

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 找不到菜单项引用 | 重新执行 `browser snapshot` 获取最新引用 |
| 点击后无反应 | 检查是否在新标签页操作，使用 `browser focus` 切换 |
| 菜单未展开 | 点击父菜单后等待 2-3 秒再获取快照 |

## 相关资源

- [OpenClaw Browser 工具文档](https://docs.openclaw.ai/tools/browser)
- [OpenClaw CLI 参考](https://docs.openclaw.ai/cli/browser)

## 许可证

MIT License
