# NDS - NetDisk Search

网盘资源搜索工具，基于 [fish2018/pansou](https://github.com/fish2018/pansou) 开源 API，支持 **14 种网盘类型**、**80+ 搜索插件**，Docker 一键部署。

---

## 目录

- [特性](#特性)
- [环境要求](#环境要求)
- [部署指南](#部署指南)
  - [Docker 部署（推荐）](#docker-部署推荐)
  - [Docker Compose 部署](#docker-compose-部署)
  - [部署含前端版本](#部署含前端版本)
  - [启用认证](#启用认证)
  - [配置代理](#配置代理)
- [作为 Skill 使用（Hermes/OpenClaw）](#作为-skill-使用hermesopenclaw)
- [使用指南](#使用指南)
  - [搜索资源](#搜索资源)
  - [检测链接](#检测链接)
  - [API 直接调用](#api-直接调用)
- [脚本参数详解](#脚本参数详解)
- [支持的网盘类型](#支持的网盘类型)
- [环境变量](#环境变量)
- [API 文档](#api-文档)
- [故障排查](#故障排查)
- [文件结构](#文件结构)
- [许可证](#许可证)

---

## 特性

- **多网盘搜索**：百度、夸克、阿里、天翼、UC、移动、115、PikPak、迅雷、123、磁力、电驴等 14 种网盘
- **80+ 搜索插件**：覆盖主流资源站，数据源持续更新
- **智能排序**：按时间新鲜度、相关度、插件等级综合排序
- **链接检测**：批量验证网盘链接是否有效，支持 9 种网盘
- **灵活过滤**：按网盘类型、关键词包含/排除过滤结果
- **三种输出**：终端友好格式、JSON 结构化数据、Markdown 表格
- **Docker 一键部署**：开箱即用，支持纯 API 和前后端集成两种模式
- **认证保护**：可选 JWT Token 认证，保护你的搜索服务

---

## 环境要求

| 组件 | 要求 | 用途 |
|------|------|------|
| Docker | 20.10+ | 部署搜索服务 |
| Python | 3.6+ | 运行搜索/检测脚本（仅标准库，无额外依赖） |
| 磁盘空间 | 500MB+ | Docker 镜像 + 缓存 |
| 内存 | 512MB+ | 基础运行 |

> **注意**：Python 脚本只使用标准库（urllib, json, argparse），无需 pip install 任何包。

---

## 部署指南

### Docker 部署（推荐）

**方式一：使用部署脚本**

```bash
# 克隆仓库
git clone https://github.com/godzx001-dot/NDS.git
cd NDS

# 一键部署
bash scripts/deploy.sh
```

脚本会自动：
1. 检查 Docker 是否安装并运行
2. 拉取官方镜像
3. 启动容器
4. 执行健康检查
5. 输出使用说明

**方式二：手动 Docker 命令**

```bash
# 纯 API 版（推荐，端口 8888）
docker run -d \
  --name netdisk-search \
  -p 8888:8888 \
  --restart unless-stopped \
  ghcr.io/fish2018/pansou:latest

# 验证是否启动成功
curl http://localhost:8888/api/health
```

成功响应：
```json
{
  "status": "ok",
  "plugins_enabled": true,
  "plugin_count": 80,
  "channels": ["tgsearchers3"]
}
```

### Docker Compose 部署

创建 `docker-compose.yml`：

```yaml
version: "3.8"
services:
  netdisk-search:
    image: ghcr.io/fish2018/pansou:latest
    container_name: netdisk-search
    ports:
      - "8888:8888"
    environment:
      # 可选：TG 频道列表
      CHANNELS: "tgsearchers3"
      # 可选：启用插件
      ENABLED_PLUGINS: "labi,zhizhen,shandian,duoduo,muou"
      # 可选：启用认证
      # AUTH_ENABLED: "true"
      # AUTH_USERS: "admin:your-password"
    volumes:
      - ./cache:/app/cache
    restart: unless-stopped
```

启动：
```bash
docker-compose up -d
docker-compose logs -f    # 查看日志
```

### 部署含前端版本

如果需要 Web 搜索界面（不仅仅是 API）：

```bash
# 使用部署脚本
bash scripts/deploy.sh --web --port 80

# 或手动部署
docker run -d \
  --name netdisk-search-web \
  -p 80:80 \
  --restart unless-stopped \
  ghcr.io/fish2018/pansou-web:latest
```

部署后访问 `http://你的IP` 即可使用 Web 搜索界面。

### 启用认证

保护你的搜索服务不被他人滥用：

```bash
# 使用部署脚本
bash scripts/deploy.sh --auth admin:mypassword123

# 或手动部署
docker run -d \
  --name netdisk-search \
  -p 8888:8888 \
  -e AUTH_ENABLED=true \
  -e AUTH_USERS="admin:mypassword123" \
  --restart unless-stopped \
  ghcr.io/fish2018/pansou:latest
```

获取 Token：
```bash
curl -X POST http://localhost:8888/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"mypassword123"}'
```

后续请求带上 Token：
```bash
curl -X POST http://localhost:8888/api/search \
  -H "Authorization: Bearer <你的Token>" \
  -H "Content-Type: application/json" \
  -d '{"kw":"测试"}'
```

### 配置代理

如果服务器无法直接访问 Telegram（如国内服务器），需要配置 SOCKS5 代理：

```bash
docker run -d \
  --name netdisk-search \
  -p 8888:8888 \
  -e PROXY="socks5://127.0.0.1:1080" \
  --restart unless-stopped \
  --network host \
  ghcr.io/fish2018/pansou:latest
```

> **提示**：仅 TG 频道搜索需要代理，插件搜索一般不需要。

---

## 作为 Skill 使用（Hermes/OpenClaw）

本项目可以作为 AI Agent 的 Skill 使用，让 Agent 具备网盘资源搜索能力。

### 安装 Skill

```bash
# 方式一：git clone（推荐）
git clone https://github.com/godzx001-dot/NDS.git ~/.hermes/skills/netdisk-search

# 方式二：下载 zip
curl -L https://github.com/godzx001-dot/NDS/archive/main.zip -o /tmp/nds.zip
unzip /tmp/nds.zip -d ~/.hermes/skills/
mv ~/.hermes/skills/NDS-main ~/.hermes/skills/netdisk-search
rm /tmp/nds.zip
```

OpenClaw 用户安装到 `~/.openclaw/skills/netdisk-search`。

### 首次使用

安装后先部署搜索服务（一次性）：

```bash
cd ~/.hermes/skills/netdisk-search
bash scripts/deploy.sh
```

### Agent 中的自然语言使用

安装后，Agent 对话中可以直接用自然语言触发：

```
用户: 帮我搜一下 "速度与激情" 的网盘资源
用户: 找一下 Python教程，只要百度和夸克
用户: 搜个唐朝诡事录，要合集不要预告
用户: 帮我检测一下这个链接: https://pan.quark.cn/s/xxx
用户: 帮我部署一下网盘搜索服务
```

Agent 会自动：
1. 识别搜索意图，调用对应脚本
2. 解析搜索结果，按网盘类型分组
3. 格式化展示（链接、提取码、来源、时间）
4. 检测链接有效性并返回状态

### 触发词

以下词汇会触发此 Skill：

| 触发词 | 动作 |
|--------|------|
| 搜资源、找资源、网盘搜、搜网盘 | 搜索资源 |
| 搜片、找片、搜电影、找电影 | 搜索影视资源 |
| 检测链接、验证链接 | 链接有效性检测 |
| 部署搜索 | 部署搜索服务 |

### 调用流程

```
用户: 搜一下 "Python教程"
  ↓
1. 探测 API 地址（NETDISK_API_URL > localhost:8888）
  ↓
2. 调用 scripts/search.py "Python教程"
  ↓
3. 解析 JSON 结果，按网盘类型分组
  ↓
4. 格式化输出：标题 + 提取码 + 链接 + 来源 + 时间
  ↓
返回给用户
```

---

## 使用指南

### 搜索资源

```bash
# 基础搜索
python3 scripts/search.py "速度与激情"

# 指定网盘类型（只搜百度和夸克）
python3 scripts/search.py "Python教程" --types baidu,quark

# 关键词过滤（包含"合集"，排除"预告"）
python3 scripts/search.py "唐朝诡事录" --include "合集,全集" --exclude "预告,花絮"

# 只搜插件（跳过 TG 频道）
python3 scripts/search.py "机器学习" --src plugin

# 指定插件
python3 scripts/search.py "电影" --plugins labi,zhizhen

# 强制刷新缓存
python3 scripts/search.py "最新资源" --refresh

# 限制结果数量
python3 scripts/search.py "教程" --limit 5

# 输出 JSON 格式
python3 scripts/search.py "资源" --format json

# 输出 Markdown 格式
python3 scripts/search.py "资源" --format markdown

# 指定 API 地址
python3 scripts/search.py "测试" --api http://192.168.1.100:8888
```

**终端输出示例：**

```
🔍 搜索: 速度与激情
📊 找到 15 个资源

📁 百度网盘 (5)
  1. 速度与激情全集1-10 | 提取码: 1234
     https://pan.baidu.com/s/1abcdef
     来源: tg:tgsearchers3 | 2024-06-10

  2. 速度与激情10 4K | 提取码: abcd
     https://pan.baidu.com/s/2ghijkl
     来源: plugin:labi | 2024-06-08

📁 夸克网盘 (3)
  1. 速度与激情系列合集
     https://pan.quark.cn/s/xxxxx
     来源: plugin:zhizhen | 2024-06-09
```

### 检测链接

```bash
# 检测单个链接（自动识别网盘类型）
python3 scripts/check_links.py --url "https://pan.quark.cn/s/xxx"

# 检测多个链接
python3 scripts/check_links.py \
  --url "https://pan.quark.cn/s/xxx" \
  --url "https://pan.baidu.com/s/yyy" \
  --url "https://www.alipan.com/s/zzz"

# 从文件读取（每行一个链接，# 开头为注释）
python3 scripts/check_links.py --file links.txt

# 指定提取码
python3 scripts/check_links.py --url "https://pan.baidu.com/s/xxx" --password 1234

# JSON 输出
python3 scripts/check_links.py --url "https://pan.quark.cn/s/xxx" --format json

# 使用代理检测
python3 scripts/check_links.py --url "https://pan.quark.cn/s/xxx" --proxy socks5://127.0.0.1:1080
```

**终端输出示例：**

```
🔗 检测 3 个链接... (API: http://localhost:8888)
✅ [夸克网盘] https://pan.quark.cn/s/xxx
   链接有效
❌ [百度网盘] https://pan.baidu.com/s/yyy
   链接失效
🔒 [百度网盘] https://pan.baidu.com/s/zzz
   需要提取码

📊 结果: 1/3 个链接有效
```

**链接状态说明：**

| 图标 | 状态 | 含义 |
|------|------|------|
| ✅ | ok | 链接有效 |
| ❌ | bad | 链接已失效 |
| 🔒 | locked | 需要提取码或密码错误 |
| ⚠️ | unsupported | 暂不支持检测该网盘 |
| ❓ | uncertain | 检测失败，结果不确定 |

**links.txt 文件格式：**

```
# 一行一个链接，# 开头为注释
https://pan.quark.cn/s/abc123
https://pan.baidu.com/s/def456
https://www.alipan.com/s/ghi789
```

### API 直接调用

不使用脚本，直接调用 REST API：

**搜索：**

```bash
# 基础搜索
curl -X POST http://localhost:8888/api/search \
  -H "Content-Type: application/json" \
  -d '{"kw": "速度与激情"}'

# 带过滤条件
curl -X POST http://localhost:8888/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "kw": "唐朝诡事录",
    "cloud_types": ["baidu", "quark"],
    "filter": {"include": ["合集"], "exclude": ["预告"]},
    "src": "all",
    "refresh": false
  }'

# GET 方式
curl "http://localhost:8888/api/search?kw=速度与激情&res=merge"
```

**链接检测：**

```bash
curl -X POST http://localhost:8888/api/check/links \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"disk_type": "quark", "url": "https://pan.quark.cn/s/xxx"},
      {"disk_type": "baidu", "url": "https://pan.baidu.com/s/yyy", "password": "1234"}
    ]
  }'
```

**健康检查：**

```bash
curl http://localhost:8888/api/health
```

---

## 脚本参数详解

### search.py 参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `kw` | - | 搜索关键词（必填） | `"速度与激情"` |
| `--types` | - | 网盘类型过滤，逗号分隔 | `--types baidu,quark` |
| `--include` | - | 结果必须包含的关键词 | `--include "合集,全集"` |
| `--exclude` | - | 结果排除的关键词 | `--exclude "预告"` |
| `--src` | - | 数据来源: all/tg/plugin | `--src plugin` |
| `--plugins` | - | 指定插件列表 | `--plugins labi,zhizhen` |
| `--refresh` | - | 强制刷新缓存 | `--refresh` |
| `--format` | - | 输出格式: terminal/json/markdown | `--format json` |
| `--api` | - | API 地址 | `--api http://1.2.3.4:8888` |
| `--limit` | - | 最大结果数（默认 20） | `--limit 50` |

### check_links.py 参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--url` | - | 待检测链接（可多次指定） | `--url "https://..."` |
| `--file` | - | 从文件读取链接 | `--file links.txt` |
| `--type` | - | 网盘类型（不指定则自动识别） | `--type quark` |
| `--password` | - | 提取码 | `--password 1234` |
| `--proxy` | - | 代理地址 | `--proxy socks5://127.0.0.1:1080` |
| `--api` | - | API 地址 | `--api http://1.2.3.4:8888` |
| `--format` | - | 输出格式: terminal/json | `--format json` |

### deploy.sh 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--port` | 服务端口（默认 8888） | `--port 9000` |
| `--web` | 部署含前端版本 | `--web` |
| `--auth` | 启用认证 | `--auth admin:pass123` |
| `--channels` | TG 频道列表 | `--channels ch1,ch2` |
| `--plugins` | 启用插件列表 | `--plugins labi,zhizhen` |
| `--name` | 容器名称 | `--name my-search` |

---

## 支持的网盘类型

| 网盘 | 标识 | 可检测 | 说明 |
|------|------|--------|------|
| 百度网盘 | `baidu` | ✅ | 最大中文网盘 |
| 阿里云盘 | `aliyun` | ✅ | 高速不限速 |
| 夸克网盘 | `quark` | ✅ | 资源丰富 |
| 天翼云盘 | `tianyi` | ✅ | 中国电信 |
| UC网盘 | `uc` | ✅ | 阿里系 |
| 移动云盘 | `mobile` | ✅ | 中国移动 |
| 115网盘 | `115` | ✅ | 老牌网盘 |
| PikPak | `pikpak` | ❌ | 离线下载 |
| 迅雷网盘 | `xunlei` | ✅ | 迅雷出品 |
| 123网盘 | `123` | ✅ | 新兴网盘 |
| 磁力链接 | `magnet` | ❌ | BT 下载 |
| 电驴链接 | `ed2k` | ❌ | eMule 下载 |

---

## 环境变量

### 本工具环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `NETDISK_API_URL` | API 服务地址 | 自动探测 |

**API 地址探测优先级：**
1. 命令行 `--api` 参数
2. 环境变量 `NETDISK_API_URL`
3. `http://localhost:8888`（本地默认）

### Docker 容器环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PORT` | 服务端口 | `8888` |
| `PROXY` | SOCKS5 代理 | - |
| `CHANNELS` | TG 频道列表 | `tgsearchers3` |
| `ENABLED_PLUGINS` | 启用插件 | - |
| `AUTH_ENABLED` | 启用认证 | `false` |
| `AUTH_USERS` | 用户配置 | - |
| `CACHE_TTL` | 缓存有效期（分钟） | `60` |
| `PLUGIN_TIMEOUT` | 插件超时（秒） | `30` |

---

## API 文档

详细 API 文档见 [references/api-reference.md](references/api-reference.md)

### 端点一览

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/search` | POST/GET | 可选 | 搜索资源 |
| `/api/check/links` | POST | 可选 | 检测链接有效性 |
| `/api/health` | GET | 不需要 | 健康检查 |
| `/api/auth/login` | POST | 不需要 | 登录获取 Token |

### 搜索响应格式

```json
{
  "total": 15,
  "results": [
    {
      "unique_id": "channel-12345",
      "title": "资源标题",
      "datetime": "2024-06-10T14:23:45Z",
      "links": [
        {
          "type": "baidu",
          "url": "https://pan.baidu.com/s/xxx",
          "password": "1234"
        }
      ]
    }
  ],
  "merged_by_type": {
    "baidu": [
      {
        "url": "https://pan.baidu.com/s/xxx",
        "password": "1234",
        "note": "资源标题",
        "source": "tg:tgsearchers3"
      }
    ]
  }
}
```

---

## 故障排查

### Q: 连接被拒绝

```bash
# 检查容器是否运行
docker ps | grep netdisk-search

# 检查端口
netstat -tlnp | grep 8888

# 查看日志
docker logs netdisk-search

# 重启容器
docker restart netdisk-search
```

### Q: 搜索结果为空

- 确认关键词是否正确，尝试更简短的词
- 检查网络连接，TG 搜索可能需要代理
- 尝试只搜插件：`--src plugin`
- 强制刷新缓存：`--refresh`

### Q: 链接检测全部超时

- 检查网络连接
- 减少同时检测的链接数量
- 配置代理：`--proxy socks5://127.0.0.1:1080`

### Q: 认证失败

```bash
# 检查认证配置
docker exec netdisk-search env | grep AUTH

# 重新获取 Token
curl -X POST http://localhost:8888/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'
```

### Q: Python 脚本报错

```bash
# 确认 Python 版本
python3 --version   # 需要 3.6+

# 检查是否能访问 API
curl http://localhost:8888/api/health

# 手动指定 API 地址
python3 scripts/search.py "测试" --api http://127.0.0.1:8888
```

---

## 文件结构

```
NDS/
├── README.md                   # 本文档
├── SKILL.md                    # Skill 集成文档
├── .gitignore
├── scripts/
│   ├── search.py               # 搜索脚本（334行）
│   ├── check_links.py          # 链接检测脚本（160行）
│   └── deploy.sh               # Docker 部署脚本（165行）
├── references/
│   └── api-reference.md        # API 完整参考文档
└── templates/                  # 预留模板目录
```

---

## 使用场景示例

### 场景一：找电影资源

```bash
# 搜索 4K 电影，只要夸克和阿里
python3 scripts/search.py "流浪地球2 4K" --types quark,aliyun --include "4K"

# 验证找到的链接是否有效
python3 scripts/check_links.py --url "https://pan.quark.cn/s/xxx"
```

### 场景二：找学习资料

```bash
# 搜索 Python 教程，排除广告
python3 scripts/search.py "Python教程" --include "合集,全套" --exclude "广告,推广"

# JSON 输出方便程序处理
python3 scripts/search.py "机器学习" --format json --limit 10 > results.json
```

### 场景三：批量验证链接

```bash
# 把所有链接写入文件
cat > links.txt << 'EOF'
https://pan.quark.cn/s/abc123
https://pan.baidu.com/s/def456
https://www.alipan.com/s/ghi789
EOF

# 批量检测
python3 scripts/check_links.py --file links.txt --format json > check_results.json
```

### 场景四：集成到自己的工具

```python
import urllib.request
import json

def search_netdisk(keyword, cloud_types=None):
    payload = {"kw": keyword, "res": "merge"}
    if cloud_types:
        payload["cloud_types"] = cloud_types
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        "http://localhost:8888/api/search",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

# 使用
results = search_netdisk("Python教程", ["baidu", "quark"])
for disk_type, links in results.get("merged_by_type", {}).items():
    print(f"\n{disk_type}:")
    for link in links[:3]:
        print(f"  {link['note']}: {link['url']}")
```

---

## 许可证

MIT License

## 致谢

- [fish2018/pansou](https://github.com/fish2018/pansou) - 高性能网盘搜索 API 服务
- 所有插件贡献者
