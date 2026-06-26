---
name: netdisk-search
category: web-scraping
description: 网盘资源搜索 - 通过网盘搜索API搜索百度/夸克/阿里/115等14种网盘资源，支持多关键词、过滤、链接检测。Docker一键部署。
tags: [search, cloud-storage, resource, api, docker]
triggers: 搜资源/找资源/网盘搜/搜网盘/找网盘/搜片/找片/搜电影/找电影
---

# 网盘资源搜索 Skill

## 功能概述

这是一个高性能网盘资源搜索 API 服务（GitHub: fish2018/pansou, 13.3k stars），提供以下核心能力：

- **多网盘支持**：覆盖 14 种主流网盘类型（百度/夸克/阿里/天翼/UC/115/PikPak/迅雷/123/磁力等）
- **插件生态**：内置 80+ 搜索插件，持续更新
- **智能排序**：按相关度、时间、插件等级等维度综合排序
- **链接检测**：验证网盘链接是否有效，过滤失效资源
- **灵活部署**：Docker 一键部署，支持本地和云端

## 前置条件

| 依赖 | 要求 | 说明 |
|------|------|------|
| Docker | 20.10+ | 部署搜索服务（必需） |
| Python | 3.6+ | 运行脚本（仅标准库，无额外依赖） |

## 安装为 Skill

### 方式一：Hermes Agent 安装

```bash
# 克隆到 skills 目录
git clone https://github.com/godzx001-dot/NDS.git ~/.hermes/skills/netdisk-search
```

然后在 Hermes 对话中说"搜资源"即可触发。

### 方式二：OpenClaw 安装

将仓库克隆到 OpenClaw 的 skills 目录：

```bash
git clone https://github.com/godzx001-dot/NDS.git ~/.openclaw/skills/netdisk-search
```

或在 OpenClaw 配置中添加远程 skill 源。

### 方式三：手动下载

```bash
# 下载并解压
curl -L https://github.com/godzx001-dot/NDS/archive/main.zip -o nds.zip
unzip nds.zip -d ~/.hermes/skills/
mv ~/.hermes/skills/NDS-main ~/.hermes/skills/netdisk-search
rm nds.zip
```

## 首次使用：部署搜索服务

安装 skill 后，需要先部署搜索服务（一次性操作）：

```bash
cd ~/.hermes/skills/netdisk-search
bash scripts/deploy.sh
```

或手动部署：

```bash
docker run -d --name netdisk-search -p 8888:8888 --restart unless-stopped ghcr.io/fish2018/pansou:latest
```

验证部署成功：

```bash
curl http://localhost:8888/api/health
```

## Agent 中的使用方式

安装后，在 Agent 对话中可以用自然语言触发：

### 搜索资源

```
用户: 帮我搜一下 "速度与激情" 的网盘资源
用户: 找一下 Python教程，只要百度和夸克
用户: 搜个唐朝诡事录，要合集不要预告
用户: 帮我找4K电影资源
```

Agent 会自动调用 search.py 执行搜索并格式化展示结果。

### 检测链接

```
用户: 帮我检测一下这个链接还能不能用: https://pan.quark.cn/s/xxx
用户: 验证这几个链接是否有效（附链接列表）
```

Agent 会调用 check_links.py 检测并返回结果。

### 部署服务

```
用户: 帮我部署一下网盘搜索服务
用户: 把网盘搜索部署到 9000 端口
```

Agent 会调用 deploy.sh 完成部署。

## Skill 内部调用流程

当 Agent 收到搜索请求时，执行流程：

```
用户: 搜一下 "Python教程"
  ↓
1. 探测 API 地址（NETDISK_API_URL > localhost:8888）
  ↓
2. 调用 scripts/search.py "Python教程"
  ↓
3. 解析结果，按网盘类型分组展示
  ↓
4. 返回格式化的搜索结果给用户
```

## 快速开始（命令行）

### 搜索资源

```bash
cd ~/.hermes/skills/netdisk-search

# 基础搜索
python3 scripts/search.py "速度与激情"

# 指定网盘类型
python3 scripts/search.py "Python教程" --types baidu,quark

# 过滤结果
python3 scripts/search.py "唐朝诡事录" --include "合集" --exclude "预告"

# JSON 输出
python3 scripts/search.py "机器学习" --format json --limit 10

# 只搜插件（跳过TG频道）
python3 scripts/search.py "资源" --src plugin
```

### 检测链接

```bash
# 单个链接
python3 scripts/check_links.py --url "https://pan.quark.cn/s/xxx"

# 多个链接
python3 scripts/check_links.py --url "https://pan.quark.cn/s/xxx" --url "https://pan.baidu.com/s/yyy"

# 从文件读取
python3 scripts/check_links.py --file links.txt
```

### 部署服务

```bash
# 一键部署
bash scripts/deploy.sh

# 指定端口
bash scripts/deploy.sh --port 9000

# 含前端版本
bash scripts/deploy.sh --web

# 启用认证
bash scripts/deploy.sh --auth admin:mypassword
```

## API 端点

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/search` | POST/GET | 可选 | 搜索资源 |
| `/api/check/links` | POST | 可选 | 检测链接有效性 |
| `/api/health` | GET | 不需要 | 健康检查 |
| `/api/auth/login` | POST | 不需要 | 登录获取 Token |

### 搜索 API 示例

```bash
# 基础搜索
curl -X POST http://localhost:8888/api/search \
  -H "Content-Type: application/json" \
  -d '{"kw": "速度与激情"}'

# 带过滤
curl -X POST http://localhost:8888/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "kw": "唐朝诡事录",
    "cloud_types": ["baidu", "quark"],
    "filter": {"include": ["合集"], "exclude": ["预告"]}
  }'
```

详细 API 文档见 [references/api-reference.md](references/api-reference.md)

## 搜索参数详解

### search.py

| 参数 | 说明 | 示例 |
|------|------|------|
| `kw` | 搜索关键词（必填） | `"速度与激情"` |
| `--types` | 网盘类型过滤 | `--types baidu,quark` |
| `--include` | 结果必须包含的词 | `--include "合集,全集"` |
| `--exclude` | 结果排除的词 | `--exclude "预告"` |
| `--src` | 数据来源: all/tg/plugin | `--src plugin` |
| `--plugins` | 指定插件 | `--plugins labi,zhizhen` |
| `--refresh` | 强制刷新缓存 | `--refresh` |
| `--format` | 输出格式 | `--format json` |
| `--limit` | 最大结果数 | `--limit 50` |
| `--api` | API 地址 | `--api http://1.2.3.4:8888` |

### check_links.py

| 参数 | 说明 | 示例 |
|------|------|------|
| `--url` | 待检测链接（可多次） | `--url "https://..."` |
| `--file` | 从文件读取链接 | `--file links.txt` |
| `--type` | 网盘类型 | `--type quark` |
| `--password` | 提取码 | `--password 1234` |
| `--proxy` | 代理地址 | `--proxy socks5://127.0.0.1:1080` |
| `--format` | 输出格式 | `--format json` |

## 支持的网盘类型

| 网盘 | 标识 | 可检测 | | 网盘 | 标识 | 可检测 |
|------|------|--------|-|------|------|--------|
| 百度网盘 | `baidu` | ✅ | | 115网盘 | `115` | ✅ |
| 阿里云盘 | `aliyun` | ✅ | | PikPak | `pikpak` | ❌ |
| 夸克网盘 | `quark` | ✅ | | 迅雷网盘 | `xunlei` | ✅ |
| 天翼云盘 | `tianyi` | ✅ | | 123网盘 | `123` | ✅ |
| UC网盘 | `uc` | ✅ | | 磁力链接 | `magnet` | ❌ |
| 移动云盘 | `mobile` | ✅ | | 电驴链接 | `ed2k` | ❌ |

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `NETDISK_API_URL` | API 服务地址 | 自动探测 |

**API 地址探测优先级：**
1. 命令行 `--api` 参数
2. 环境变量 `NETDISK_API_URL`
3. `http://localhost:8888`（本地默认）

## 故障排查

**Q: 连接被拒绝**
```bash
docker ps | grep netdisk-search          # 检查容器是否运行
docker logs netdisk-search               # 查看日志
docker restart netdisk-search            # 重启
```

**Q: 搜索结果为空**
- 确认关键词是否正确，尝试更简短的词
- 检查网络连接，TG 搜索可能需要代理
- 尝试只搜插件：`--src plugin`

**Q: 链接检测超时**
- 检查网络连接
- 使用代理：`--proxy socks5://127.0.0.1:1080`
- 减少同时检测数量

## 与其他 Skill 的关系

| Skill | 定位 | 适用场景 |
|-------|------|---------|
| **netdisk-search** | 底层通用搜索 | 快速搜索、链接检测、API 集成 |
| **pansou-resource-scraper** | 业务应用 | 资源分类、网站生成、批量采集 |

- 需要快速搜索资源 → 使用 netdisk-search
- 需要构建资源库/生成网站 → 使用 pansou-resource-scraper

## 最佳实践

1. **关键词优化**：使用 2-4 个关键词，避免过于宽泛
2. **类型过滤**：明确指定网盘类型可提高搜索速度和精度
3. **缓存利用**：默认启用缓存，避免重复请求；需要最新结果时加 `--refresh`
4. **资源验证**：重要资源建议先检测链接有效性再使用
5. **代理配置**：国内服务器搜 TG 频道需配置代理，插件搜索一般不需要

## 文件结构

```
netdisk-search/
├── SKILL.md                    # 本文件（Skill 主文档）
├── README.md                   # GitHub 项目文档
├── .gitignore
├── scripts/
│   ├── search.py               # 搜索脚本（终端/JSON/Markdown 输出）
│   ├── check_links.py          # 链接有效性检测脚本
│   └── deploy.sh               # Docker 一键部署脚本
├── references/
│   └── api-reference.md        # API 完整参考文档
└── templates/                  # 预留模板目录
```

## 相关链接

- 本项目: https://github.com/godzx001-dot/NDS
- 上游项目: https://github.com/fish2018/pansou
- 上游文档: https://github.com/fish2018/pansou#readme
- 问题反馈: https://github.com/godzx001-dot/NDS/issues
