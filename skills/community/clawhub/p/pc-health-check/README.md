# PC Health Check Skill

Windows PC一键健康体检工具，基于OpenClaw Skill规范开发。

## 功能

**快速模式**（--quick，10秒内）：
- 操作系统信息
- CPU状态与负载
- 内存使用情况
- 磁盘空间
- 网络连接

**完整模式**（默认，约30秒）：
- 快速模式全部5项
- 高资源进程Top10
- 设备异常检测
- 24小时系统事件
- 启动项列表
- 监听端口扫描（含高危端口检测）
- 最近安全更新

## 使用

在OpenClaw中直接说：
- "PC体检" — 完整检查
- "快速体检" — 5项核心检查
- "电脑健康检查"

## 安装

```bash
# 复制到OpenClaw skills目录
cp -r pc-health-check ~/.openclaw/skills/

# 或Windows
xcopy /E /I pc-health-check %USERPROFILE%\.openclaw\skills\pc-health-check
```

## 技术栈

- Node.js（零外部依赖）
- Windows WMI（PowerShell命令采集）

## 目录结构

```
pc-health-check/
├── SKILL.md              # Skill配置与说明
├── README.md             # 本文件
└── scripts/
    └── health_check.cjs  # 核心巡检脚本
```

## 脚本使用

```bash
node scripts/health_check.cjs --quick --report    # 快速模式，输出Markdown
node scripts/health_check.cjs --json              # 完整模式，输出JSON
```

## 输出示例

```json
{
  "timestamp": "2026-04-19T18:38:15.123Z",
  "overall": "good",
  "mode": "quick",
  "summary": {
    "totalChecks": 5,
    "ok": 5,
    "warnings": 0,
    "errors": 0
  },
  "results": { ... }
}
```

## 许可

MIT License
