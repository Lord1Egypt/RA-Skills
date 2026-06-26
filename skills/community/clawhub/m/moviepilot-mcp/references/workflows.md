# MoviePilot 工作流详解

> 所有命令假设已通过 `python3 scripts/setup.py` 完成配置。

## 工作流 1：搜索并订阅

### 搜索影视/动漫/纪录片
```bash
python3 scripts/mp_call.py search_media '{"title":"流浪地球","media_type":"movie"}'
python3 scripts/mp_call.py search_media '{"title":"三体","media_type":"tv","year":"2023"}'
python3 scripts/mp_call.py search_media '{"title":"进击的巨人","media_type":"tv","year":"2013"}'
```

返回字段关注：`tmdb_id`、`title`、`year`、`type`（`movie`/`tv`）、`season`。

### 获取详情
```bash
python3 scripts/mp_call.py query_media_detail '{"tmdb_id":204541,"media_type":"tv"}'
```

### 添加订阅
```bash
# 电影
python3 scripts/mp_call.py add_subscribe '{"title":"流浪地球","year":"2019","media_type":"movie","tmdb_id":535167,"quality":"BluRay|WEB-DL","resolution":"1080p|2160p"}'

# 电视剧 — season 不传默认仅 S1
python3 scripts/mp_call.py add_subscribe '{"title":"三体","year":"2023","media_type":"tv","tmdb_id":204541,"resolution":"1080p|2160p"}'

# 订第 2 季
python3 scripts/mp_call.py add_subscribe '{"title":"三体","year":"2023","media_type":"tv","tmdb_id":204541,"season":2}'

# 带规则组和指定站点
python3 scripts/mp_call.py add_subscribe '{"title":"三体","year":"2023","media_type":"tv","tmdb_id":204541,"filter_groups":["BluRay","WEB-DL"],"sites":[2,3]}'
```

### 注意
- 电视剧多季需逐季调用 `add_subscribe`，每季一次
- `quality`/`resolution`/`effect` 用正则，`|` = "或"
- `filter_groups` 传规则组**名称**数组（来自 `query_rule_groups`），不是 id
- 订阅后建议 `search_subscribe` 立即触发首轮搜索

---

## 工作流 2：查看订阅 → 补缺

```bash
# 全部订阅
python3 scripts/mp_call.py query_subscribes '{}'

# 只看电视剧
python3 scripts/mp_call.py query_subscribes '{"media_type":"tv"}'

# 看电影
python3 scripts/mp_call.py query_subscribes '{"media_type":"movie"}'

# 搜索缺失剧集
python3 scripts/mp_call.py search_subscribe '{"subscribe_id":42}'

# 暂停
python3 scripts/mp_call.py update_subscribe '{"subscribe_id":42,"state":"S"}'
# 恢复
python3 scripts/mp_call.py update_subscribe '{"subscribe_id":42,"state":"R"}'
# 修改过滤
python3 scripts/mp_call.py update_subscribe '{"subscribe_id":42,"resolution":"2160p"}'

# 删除
python3 scripts/mp_call.py delete_subscribe '{"subscribe_id":42}'
```

状态：`R`=启用 `P`=待定 `S`=暂停

---

## 工作流 3：手动搜种 → 下载 → 入库

```bash
# 按 TMDB ID 搜种
python3 scripts/mp_call.py search_torrents '{"tmdb_id":535167,"media_type":"movie"}'

# 限定站点
python3 scripts/mp_call.py search_torrents '{"tmdb_id":535167,"media_type":"movie","sites":[2,3]}'

# 浏览缓存结果（可按 site/resolution/edition 过滤）
python3 scripts/mp_call.py get_search_results '{"site":"hdhome","page":1}'

# 下载
python3 scripts/mp_call.py add_download '{"torrent_url":"https://example.com/torrent.php?id=12345"}'

# 查看进度
python3 scripts/mp_call.py query_download_tasks '{}'
python3 scripts/mp_call.py query_download_tasks '{"status":"downloading"}'

# 暂停/恢复/打标签
python3 scripts/mp_call.py modify_download '{"hash":"abc123","action":"pause"}'
python3 scripts/mp_call.py modify_download '{"hash":"abc123","action":"resume"}'
python3 scripts/mp_call.py modify_download '{"hash":"abc123","action":"tag","tags":"电影"}'

# 删除（delete_files=true 含文件；不传仅删任务记录）
python3 scripts/mp_call.py delete_download '{"hash":"abc123"}'

# 下载完成 → 整理入库
python3 scripts/mp_call.py transfer_file '{"file_path":"/downloads/movie.mkv","media_type":"movie","tmdbid":535167}'
python3 scripts/mp_call.py transfer_file '{"file_path":"/downloads/tv_show","target_path":"/media/tv/国剧","background":true}'
```

---

## 工作流 4：检查媒体库

```bash
# 检查是否已存在
python3 scripts/mp_call.py query_library_exists '{"tmdb_id":535167,"media_type":"movie"}'
python3 scripts/mp_call.py query_library_exists '{"douban_id":"1234567","media_type":"movie"}'

# 最近入库
python3 scripts/mp_call.py query_library_latest '{"page":1}'

# 刮削 NFO/海报
python3 scripts/mp_call.py scrape_metadata '{"path":"/media/movies/流浪地球 (2019)"}'
python3 scripts/mp_call.py scrape_metadata '{"path":"/media/movies/流浪地球 (2019)","overwrite":true}'

# 浏览目录
python3 scripts/mp_call.py list_directory '{"path":"/media/movies","sort_by":"mtime"}'

# 查看目录配置
python3 scripts/mp_call.py query_directory_settings '{"directory_type":"movie"}'

# 整理历史
python3 scripts/mp_call.py query_transfer_history '{"page":1}'
```

---

## 工作流 5：PT 站点维护

```bash
# 查看所有站点
python3 scripts/mp_call.py query_sites '{}'
python3 scripts/mp_call.py query_sites '{"status":"active"}'

# 测试连通
python3 scripts/mp_call.py test_site '{"site_identifier":"hdhome"}'

# 刷新 Cookie
python3 scripts/mp_call.py update_site_cookie '{"site_identifier":"hdhome","username":"your_username","password":"***"}'

# 站点数据（上传/下载量）
python3 scripts/mp_call.py query_site_userdata '{"site_id":2}'

# 修改站点配置
python3 scripts/mp_call.py update_site '{"site_id":2,"is_active":true,"timeout":30}'
```

---

## 工作流 6：过滤规则管理

```bash
# 查看
python3 scripts/mp_call.py query_builtin_filter_rules '{}'
python3 scripts/mp_call.py query_custom_filter_rules '{}'
python3 scripts/mp_call.py query_rule_groups '{}'

# 新增自定义规则
python3 scripts/mp_call.py add_custom_filter_rule '{"rule_id":"my_rule","name":"优质资源","include":"BluRay|WEB-DL","exclude":"CAM|TS|TC","size_range":"5-50","seeders":"5"}'

# 新增规则组（组合多个规则）
python3 scripts/mp_call.py add_rule_group '{"name":"我的优质规则","rule_string":"my_rule & !low_quality & 1080p","media_type":"movie"}'

# 编辑/删除
python3 scripts/mp_call.py update_custom_filter_rule '{"current_rule_id":"my_rule","new_rule_id":"my_rule_v2","name":"优质资源v2"}'
python3 scripts/mp_call.py delete_custom_filter_rule '{"rule_id":"my_rule"}'
```

---

## 工作流 7：插件管理

```bash
# 已装插件
python3 scripts/mp_call.py query_installed_plugins '{}'

# 搜索市场
python3 scripts/mp_call.py query_market_plugins '{"query":"自动备份"}'

# 查看配置
python3 scripts/mp_call.py query_plugin_config '{"plugin_id":"AutoBackup"}'

# 安装/卸载
python3 scripts/mp_call.py install_plugin '{"plugin_id":"AutoBackup"}'
python3 scripts/mp_call.py uninstall_plugin '{"plugin_id":"AutoBackup"}'

# 重载/读数据
python3 scripts/mp_call.py reload_plugin '{"plugin_id":"AutoBackup"}'
python3 scripts/mp_call.py query_plugin_data '{"plugin_id":"AutoBackup","key":"history"}'
```

---

## 工作流 8：系统操作

```bash
# 定时任务
python3 scripts/mp_call.py query_schedulers
python3 scripts/mp_call.py run_scheduler '{"job_id":"subscription_search"}'

# 系统设置
python3 scripts/mp_call.py query_system_settings '{"group":"download"}'

# Persona 切换
python3 scripts/mp_call.py query_personas
python3 scripts/mp_call.py switch_persona '{"persona_id":1}'

# 发送通知
python3 scripts/mp_call.py send_message '{"message":"下载完成！","title":"MoviePilot 通知"}'
```

---

## 注意事项

1. **分页响应**：部分工具 text 带分页头（如 `第 1/1 页，当前页 20 条结果…`），解析 JSON 需先跳过该前缀
2. **`transfer_file` 路径**：必须是 MoviePilot 容器内可见的绝对路径
3. **`add_subscribe` 的 `season`**：不传默认仅 S1，订整部剧需逐季调用
4. **`quality`/`resolution`/`effect`**：正则表达式，`|` 分隔，如 `"1080p|2160p"`
5. **下载器名称**：参考 `query_downloaders` 返回的 `name` 字段
