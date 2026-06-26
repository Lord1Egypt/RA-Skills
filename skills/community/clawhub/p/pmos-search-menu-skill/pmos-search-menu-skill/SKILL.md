# pmos-search-menu-skill

**版本**: 1.0.0  
**作者**: ClawTech  
**描述**: 自动化爬取甘肃电力交易平台（PMOS）网站的菜单导航路径

## 功能

- 🌐 自动打开 PMOS 网站并等待登录
- 📍 按照指定路径逐级点击菜单
- 🔄 自动处理新标签页的打开和切换
- 📋 支持深度嵌套的菜单结构
- 📸 自动获取页面快照和元素引用

## 触发条件

当用户提到以下关键词时激活此技能：
- "PMOS 菜单导航"
- "甘肃电力交易平台"
- "sgcc.com.cn"
- "信息披露菜单"
- "电力交易菜单点击"

## 使用方法

### 基础用法

```bash
# 使用 PowerShell 脚本
.\scripts\navigate-pmos.ps1 -MenuPath "信息披露","综合查询","市场运营"

# 使用 Node.js 脚本
node scripts/navigate-pmos.js

# 使用 browser 工具手动操作
openclaw browser open https://pmos.gs.sgcc.com.cn/
```

### 完整菜单路径

```
信息披露 
  → 综合查询 (打开新标签页)
    → 市场运营 
      → 交易组织及出清 
        → 现货市场申报、出清信息 
          → 实时各节点出清类信息 
            → 实时市场出清节点电价
```

## 依赖工具

- `browser` - OpenClaw 浏览器控制工具

## 配置

无需特殊配置，但需要：
1. PMOS 网站的有效登录账号
2. OpenClaw browser 工具已启用

## 文件结构

```
pmos-search-menu-skill/
├── SKILL.md                      # 本文件
├── README.md                     # 详细使用说明
├── clawhub.json                  # ClawHub 包配置
├── references/
│   └── NAVIGATION_PATH.md        # 详细导航路径和元素引用
└── scripts/
    ├── navigate-pmos.ps1         # PowerShell 导航脚本
    ├── navigate-pmos.sh          # Bash 导航脚本
    └── navigate-pmos.js          # Node.js 导航脚本
```

## 注意事项

1. **登录状态**: 使用前必须先手动登录 PMOS 网站
2. **新标签页**: 点击"综合查询"会打开新标签页，后续操作都在新标签页进行
3. **动态引用**: 页面元素的 aria-ref 可能会变化，每次操作前建议重新获取快照
4. **等待时间**: 菜单展开和页面加载需要 2-3 秒延迟

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 找不到菜单项引用 | 重新执行 `browser snapshot` 获取最新引用 |
| 点击后无反应 | 检查是否在新标签页操作，使用 `browser focus` 切换 |
| 菜单未展开 | 点击父菜单后等待 2-3 秒再获取快照 |
| 页面加载超时 | 增加脚本中的等待时间配置 |

## 相关文档

- [OpenClaw Browser 工具](https://docs.openclaw.ai/tools/browser)
- [OpenClaw CLI 参考](https://docs.openclaw.ai/cli/browser)

## 许可证

MIT License
