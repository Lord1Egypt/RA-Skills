---
name: grafana-inspector
description: Grafana 自动化巡检技能。支持浏览器截图 + API 数据巡检，多仪表盘批量巡检，自动发现仪表盘。
---

# Grafana 自动化巡检技能

## 快速开始

```bash
# 1. 配置
cd skills/grafana-inspector/scripts
cp config.example.json config.json
# 编辑 config.json

# 2. 执行
python main.py config.json

# 或在 OpenClaw 中输入
执行 Grafana 巡检
```

## 配置说明

```json
{
  "grafana_url": "http://localhost:3000",
  "api_key": "",
  "dashboard_uids": [],
  "auto_discover": true,
  "discover_limit": 10,
  "inspection_mode": "hybrid",
  "screenshot_dir": "./screenshots"
}
```

| 参数 | 说明 | 必填 |
|------|------|------|
| `grafana_url` | Grafana 地址 | ✅ |
| `api_key` | API Key（API 巡检用） | ✅ |
| `dashboard_uids` | 仪表盘 UID 列表 | ❌ |
| `auto_discover` | 自动发现仪表盘 | ❌ |
| `discover_limit` | 最多巡检数量 | ❌ |

## 使用方式

### 方式 1：命令行

```bash
cd skills/grafana-inspector/scripts
python inspect_report.py config.json
```

### 方式 2：OpenClaw

```
执行 Grafana 巡检
```

## 输出

- `inspection_*.json` - JSON 结果
- `inspection_*.md` - Markdown 报告

## 获取 Dashboard UID

1. 打开 Grafana 仪表盘
2. 查看 URL: `https://grafana/d/{UID}/{name}`
3. 复制 UID 部分

## 获取 API Key

1. Grafana → Configuration → API keys
2. 创建 Viewer 权限的 Key
3. 复制到配置

## 文件结构

```
grafana-inspector/
├── scripts/
│   ├── api_inspect.py    # API 巡检
│   ├── main.py        # 主脚本
│   └── config.json       # 配置
├── screenshots/          # 截图
├── SKILL.md             # 技能定义
└── README.md            # 说明文档
```

## 故障排查

### API 连接失败
- 检查 API Key 是否正确
- 验证网络连接
- 确认 Grafana 服务正常
- 检查飞书授权状态
