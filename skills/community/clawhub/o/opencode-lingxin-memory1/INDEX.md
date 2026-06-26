# 灵芯派 OpenCode 记忆 - 索引

## 快速导航

| 主题 | 文件 | 说明 |
|------|------|------|
| **使用说明** | README.md | 技能包使用说明 |
| **长期记忆** | MEMORY.md | 核心持久信息 |
| **今日记忆** | 2026-04-30.md | 当日工作记录 |
| **记忆索引** | INDEX.md | 本文件 |

## 核心信息速查

### 系统配置
- IP: 10.1.1.1 (有线) / 192.168.31.247 (WiFi)
- 用户: zmrobo / 密码: zmrobo
- 系统: Debian 10 + ARM Cortex-A55

### 网络优化
- WiFi卡顿解决: DNS改为本地路由器192.168.31.1
- 命令: `nmcli con mod "XiaFi名称" ipv4.dns "192.168.31.1"`

### Python环境
- 空间仅2GB，不适合venv
- 系统用Python 3.7，AI用Python 3.9

## 同步命令

```bash
~/.opencode-memory/sync.sh
```

## 搜索

```bash
grep -r "关键词" ~/.opencode-memory/
```