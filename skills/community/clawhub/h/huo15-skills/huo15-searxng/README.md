# huo15-searxng

> SearXNG 自托管搜索引擎一键部署 - Docker Compose + OpenClaw 配置自动化 (v1.1.0)

## 功能特性

- 🔍 **一键部署**：Docker Compose 自动部署 SearXNG 实例
- 🔄 **端口冲突自动处理**：8888 → 8889 → 8890 → 8910 自动检测可用端口
- 🔒 **botdetection 修复**：limiter.toml 解决 SearXNG 403 Forbidden 问题
- ⚙️ **OpenClaw 无缝集成**：自动配置 `SEARXNG_BASE_URL` 环境变量
- ✅ **健康检查**：启动后自动验证服务可用性（含 JSON API）
- 🔄 **幂等性**：已安装时自动检测并显示状态，支持升级

## 前提条件

- Docker Desktop (macOS) / Docker Engine (Linux)
- docker compose v2 (`docker compose` 命令)
- `nc` 命令（macOS/Linux 内置）

## 快速开始

### 安装 Skill

```bash
clawhub install huo15-searxng --dir ~/.openclaw/workspace/skills
```

### 部署 SearXNG

```bash
@贾维斯 安装 SearXNG
```

或手动执行安装脚本：

```bash
bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/install.sh
```

## 工作原理

```
安装脚本流程：
1. 检查 Docker + docker compose v2
2. 检测已安装？ → 显示状态并退出（幂等性）
3. 端口 8888-8910 可用性检测
4. 渲染 docker-compose.yml + settings.yml + limiter.toml
5. docker compose up -d
6. 健康检查 (HTTP 200) + JSON API 验证
7. 配置 SEARXNG_BASE_URL 到 ~/.zshrc
8. 输出完成信息
```

## 目录结构

```
huo15-searxng/
├── SKILL.md              # Skill 定义
├── README.md             # 本文档
├── scripts/
│   ├── install.sh        # 核心安装脚本 (v1.1.0)
│   ├── uninstall.sh      # 卸载脚本 (新增)
│   ├── env.sh           # 环境变量加载
│   └── status.sh        # 状态检查 (v1.1.0)
└── templates/
    └── docker-compose.yml.template
```

## 配置说明

### 环境变量

安装后自动添加以下环境变量到 `~/.zshrc`：

```bash
export SEARXNG_BASE_URL="http://localhost:8888"
```

**立即生效**：

```bash
source ~/.zshrc
```

### OpenClaw 配置

OpenClaw 自动检测 `SEARXNG_BASE_URL` 环境变量，无需手动配置。

如需手动配置，编辑 `~/.openclaw/openclaw.json`：

```json
{
  "plugins": {
    "entries": {
      "searxng": {
        "config": {
          "webSearch": {
            "baseUrl": "http://localhost:8888"
          }
        }
      }
    }
  }
}
```

## 常用命令

| 操作 | 命令 |
|------|------|
| 安装/升级 | `bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/install.sh` |
| 查看状态 | `bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/status.sh` |
| 查看日志 | `docker logs searxng` |
| 重启服务 | `cd ~/docker/searxng && docker compose restart` |
| 停止服务 | `cd ~/docker/searxng && docker compose down` |
| 卸载 | `bash ~/.openclaw/workspace/skills/huo15-searxng/scripts/uninstall.sh` |

## 端口说明

| 端口 | 说明 |
|------|------|
| 8888 | 默认端口 |
| 8889 | 备用端口 1 |
| 8890 | 备用端口 2 |
| 8910 | 最大检测端口 |

脚本会按顺序检测，找到第一个可用端口为止。

## v1.1.0 更新

- ✅ 修复 `grep -oP` (GNU grep) → `grep -oE` (跨平台)
- ✅ 修复 sed 分隔符问题（用 `|` 代替 `/` 避免 URL 冲突）
- ✅ 新增幂等性检测（已安装时显示状态不重复部署）
- ✅ 新增卸载脚本 `uninstall.sh`
- ✅ 新增 `source ~/.zshrc` 生效提示
- ✅ 增强 curl 超时参数（--connect-timeout, --max-time）
- ✅ 停止旧容器逻辑（升级时清理）

## 故障排除

### Docker 未安装

```bash
# macOS
brew install --cask docker

# Linux (Ubuntu)
curl -fsSL https://get.docker.com | sh
```

### 端口全部占用

手动指定端口后重新安装：

```bash
cd ~/docker/searxng
# 编辑 docker-compose.yml 修改端口
docker compose up -d
# 手动设置环境变量
export SEARXNG_BASE_URL="http://localhost:你指定的端口"
```

### SearXNG 启动失败

```bash
# 查看日志
docker logs searxng

# 调试健康检查
curl -v http://localhost:8888/healthz

# 完整日志
cd ~/docker/searxng && docker compose logs
```

### 环境变量未生效

```bash
source ~/.zshrc
echo $SEARXNG_BASE_URL
```

## 技术参考

- [SearXNG 官方文档](https://docs.searxng.org/)
- [OpenClaw SearXNG 配置](https://docs.openclaw.ai/tools/searxng-search)
- [SearXNG GitHub](https://github.com/searxng/searxng)

## License

MIT
