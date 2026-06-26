---
name: moviepilot-mcp
description: "MoviePilot 媒体库自动化：搜索影视/动漫/纪录片、订阅追更、管理下载、整理入库、PT站点维护、插件管理。"
user-invocable: true
---

# MoviePilot MCP

通过 MoviePilot 的 MCP 接口操控 NAS 媒体库自动化系统。覆盖电影、电视剧、动漫、纪录片等全部媒体类型。

## 前置配置（对话中完成，不需要终端）

首次使用时如果未配置 `config.json`，AI **在对话中**直接向用户获取两个信息：

1. **先问 MoviePilot 服务器地址** — 格式 `http://IP:端口`，默认端口 3001
2. **再问 API 密钥** — MoviePilot 的 `API_TOKEN`

拿到后写入 `config.json`，然后继续执行用户原本的请求。用户全程无需切换终端。

### 如何引导用户找 API Key

用户找不到时告诉 ta 任一方式：
- MoviePilot Web UI → **系统设定** → 查看 `API_TOKEN`
- Docker：`docker inspect <容器名> | grep API_TOKEN`
- docker-compose.yml 中 `environment.API_TOKEN`
- 容器启动日志：`docker logs <容器名> | grep -i token`
- V1 默认值 `moviepilot`；V2 要求 ≥16 个字符，不满足会自动重新生成

详见 `references/setup-guide.md`。

### 一步到位

如果用户在首次请求时就把信息给了：
> "服务器 192.168.1.100:3001，Key 是 xxx，帮我搜流浪地球"

AI 先写 config.json 再搜片，一步完成。**不要再开话题问配置。**

### 备用：终端配置

```bash
python3 scripts/setup.py                     # 交互式向导
python3 scripts/setup.py '{"base_url":"http://IP:3001","apikey":"***"}'  # 一键写入
```

## 调用方式

```bash
python3 scripts/mp_call.py <tool_name> '<json_args>'

# 例：
python3 scripts/mp_call.py search_media '{"title":"流浪地球","media_type":"movie"}'
python3 scripts/mp_call.py query_subscribes '{}'
```

JSON 参数要点：
- 空参数：`'{}'`
- 字符串：`'{"title":"三体","media_type":"tv"}'`
- 数字/布尔：不加引号 — `{"tmdb_id":535167,"overwrite":true}`
- 数组：`'{"sites":[2,3],"filter_groups":["BluRay","WEB-DL"]}'`
- 结果取 `result.content[0].text`，部分工具返回带分页前缀（如 `第 1/1 页…` + JSON），需跳过前缀提取

## 核心工具速查

| 类别 | 工具 | 说明 |
|------|------|------|
| 🔍 搜索 | `search_media` | TMDB 搜索影视/动漫/纪录片 |
| 🔍 搜索 | `recognize_media` | 从种子标题或文件路径提取媒体信息 |
| 🔍 搜索 | `query_media_detail` | 获取详情：状态/类型/演职员/分季信息 |
| 🔍 搜索 | `get_recommendations` | 热门/新片/口碑推荐 |
| 🔍 搜索 | `search_person` | 搜索演员/导演等影人 |
| 🔍 搜索 | `search_person_credits` | 查询影人参演作品列表 |
| 🔍 搜索 | `query_episode_schedule` | 剧集播出日历/更新进度 |
| 📥 订阅 | `add_subscribe` | 新建订阅，自动追更/下载 |
| 📥 订阅 | `query_subscribes` | 查看全部订阅及状态 |
| 📥 订阅 | `search_subscribe` | 立即搜索缺失剧集 |
| 📥 订阅 | `update_subscribe` | 改状态/过滤/集数/质量 |
| 📥 订阅 | `delete_subscribe` | 删除订阅 |
| 📥 订阅 | `query_subscribe_shares` | 社区分享的订阅推荐 |
| 📥 订阅 | `query_popular_subscribes` | 全站热门订阅排行 |
| 📥 订阅 | `query_subscribe_history` | 订阅搜索历史 |
| ⬇️ 下载 | `search_torrents` | 跨站点搜索种子资源 |
| ⬇️ 下载 | `get_search_results` | 浏览缓存的搜索结果 |
| ⬇️ 下载 | `add_download` | 提交下载任务 |
| ⬇️ 下载 | `query_download_tasks` | 查看下载进度/状态 |
| ⬇️ 下载 | `modify_download` | 暂停/恢复/打标签 |
| ⬇️ 下载 | `delete_download` | 删除下载（可含文件） |
| ⬇️ 下载 | `delete_download_history` | 清理下载历史 |
| ⬇️ 下载 | `query_downloaders` | 查看已配置的下载器 |
| 📂 整理 | `transfer_file` | 整理文件到媒体库 |
| 📂 整理 | `query_library_exists` | 检查是否已在库 |
| 📂 整理 | `query_library_latest` | 最近入库媒体 |
| 📂 整理 | `scrape_metadata` | 刮削 NFO/海报/背景 |
| 📂 整理 | `query_transfer_history` | 整理历史 |
| 📂 整理 | `delete_transfer_history` | 清除整理记录 |
| 📂 整理 | `list_directory` | 浏览文件目录 |
| 📂 整理 | `query_directory_settings` | 查看目录分类设置 |
| 🌐 站点 | `query_sites` | 列出所有 PT 站点 |
| 🌐 站点 | `update_site` | 修改站点配置 |
| 🌐 站点 | `query_site_userdata` | 站点用户数据（上传/下载量等） |
| 🌐 站点 | `test_site` | 测试站点连通性 |
| 🌐 站点 | `update_site_cookie` | 刷新/更新站点登录 |
| 🧩 规则 | `query_custom_filter_rules` | 自定义过滤规则 |
| 🧩 规则 | `query_rule_groups` | 过滤规则组 |
| 🧩 规则 | `query_builtin_filter_rules` | 系统内置规则 |
| 🧩 规则 | `add_custom_filter_rule` | 新增过滤规则 |
| 🧩 规则 | `add_rule_group` | 新建规则组 |
| 🧩 规则 | `update_custom_filter_rule` / `delete_custom_filter_rule` | 编辑/删除规则 |
| 🧩 规则 | `update_rule_group` / `delete_rule_group` | 编辑/删除规则组 |
| 🔌 插件 | `query_installed_plugins` | 已装插件 |
| 🔌 插件 | `query_market_plugins` | 插件市场搜索 |
| 🔌 插件 | `query_plugin_config` / `update_plugin_config` | 查看/修改插件配置 |
| 🔌 插件 | `install_plugin` / `uninstall_plugin` | 安装/卸载插件 |
| 🔌 插件 | `reload_plugin` | 重载插件 |
| 🔌 插件 | `query_plugin_data` | 读取插件数据 |
| 🔌 插件 | `query_plugin_capabilities` | 插件能力查询 |
| ⚙️ 系统 | `query_system_settings` / `update_system_settings` | 系统配置 |
| ⚙️ 系统 | `query_schedulers` / `run_scheduler` | 定时任务 |
| ⚙️ 系统 | `query_workflows` / `run_workflow` | 工作流管理 |
| ⚙️ 系统 | `send_message` / `send_local_file` | 发送通知/本地文件 |
| ⚙️ 系统 | `browse_webpage` | 浏览网页 |
| 👤 人格 | `query_personas` / `switch_persona` / `update_persona_definition` | Persona 管理 |
| ⌨️ 快捷 | `list_slash_commands` / `run_slash_command` | 快捷指令 |
| 🏷️ 标识 | `query_custom_identifiers` / `update_custom_identifiers` | 自定义识别词 |

## 常用工作流

### 1. 搜片 → 订阅

```
search_media（拿到 tmdb_id + year + media_type）
  → add_subscribe
  → query_subscribes 确认 / search_subscribe 立即搜
```
- 电视剧 `year` 必传；`season` 不传默认仅 S1，多季逐季调用
- `media_type`：电影 `"movie"`，剧集 `"tv"`

### 2. 手动搜种 → 下载 → 入库

```
search_torrents → get_search_results → add_download
  → query_download_tasks（看进度）
  → transfer_file（入库）
```

### 3. 管订阅

```
query_subscribes → 找 subscribe_id
  → search_subscribe  补缺
  → update_subscribe  改过滤/状态（R=启用 P=待定 S=暂停）
  → delete_subscribe  删除
```

### 4. 检查媒体库

```
query_library_exists + tmdb_id → 是否已有
query_library_latest → 最近入库
```

### 5. 维护 PT 站点

```
query_sites → 找站点标识
  → test_site 测试连通 / update_site_cookie 更新登录 / update_site 改配置
```

## 注意事项

- `add_subscribe` 的 `filter_groups` 传规则组**名称**数组，不是 id
- `transfer_file` 的 `file_path` 须是 MoviePilot 容器内可见路径
- `quality`/`resolution`/`effect` 过滤用正则，`|` 分隔多选项
- 部分工具 text 带分页前缀，解析 JSON 前须跳过

全部 70 个工具参数 → `references/tools.md`，工作流实例 → `references/workflows.md`。
