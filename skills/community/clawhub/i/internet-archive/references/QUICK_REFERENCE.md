# Internet Archive 快速参考

## 搜索语法速查

### 基础查询
```
collection:nasa                  # 在 NASA 集合中搜索
mediatype:movies                 # 按媒体类型过滤
creator:"Mark Twain"             # 精确匹配创作者
title:"climate change"           # 在标题中搜索
```

### 布尔操作
```
collection:nasa AND mediatype:image
mediatype:texts OR mediatype:audio
"public domain" NOT collection:opensource
```

### 范围查询
```
date:[2020-01-01 TO 2024-12-31]
downloads:[1000 TO null]         # 下载量 >= 1000
item_size:[1000000000 TO null]   # 大小 >= 1GB
```

### 全文搜索
```
ia search -F 'collection:books "exact phrase"'
ia search -F 'author:Smith AND "content text"'
```

## 常用 ia 命令速查

```bash
# 工具
ia --version
ia configure                    # 首次配置
ia configure --whoami           # 查看当前用户

# 搜索
ia search 'query' --itemlist     # 仅标识符
ia search 'query' --sort='downloads desc' -n  # 仅计数

# 下载
ia download <id>                # 全部文件
ia download <id> --glob='*.pdf' # 通配符
ia download <id> --dry-run      # 预览

# 上传
ia upload <id> file.txt \
  --metadata='mediatype:texts' \
  --metadata='title:My File'

# 元数据
ia metadata <id>                # 查看全部
ia metadata <id> --formats      # 列出文件格式
ia metadata <id> --modify='title:New'  # 修改

# 列出
ia list <id> --location         # 显示 URL
ia list <id> --columns=name,size,format

# 批量（配合 GNU Parallel）
cat items.txt | parallel 'ia download {}'
```

## 标识符命名规则

- 仅 ASCII 字母、数字、下划线 `_`、连字符 `-`、句点 `.`
- 必须以字母或数字开头
- 5-100 字符（推荐 5-80）
- **一旦创建不可更改**
- 建议：小写 + 连字符分隔（`my-document-2024`）

## 常用集合（Collection）

```
opensource_movies    # 开源电影（任何人可上传）
opensource_audio    # 开源音频
opensource_media    # 通用开源媒体
community_texts     # 社区文本
community_video     # 社区视频
community_audio     # 社区音频
test_collection     # 测试集合（30 天后自动删除）
```

## 媒体类型（mediatype）

```
texts       # 书籍、文档、PDF
movies      # 视频
audio       # 音频、播客
software    # 程序、游戏
image       # 照片、图形
data        # 数据集、归档
```

## 有用的排序字段

```
downloads        # 总下载量
week/month       # 周/月下载量
publicdate       # 发布日期（降序=最新）
addeddate        # 添加日期
date             # 内容日期
titleSorter      # 标题字母序
creatorSorter    # 创作者字母序
item_size        # 项目大小
files_count      # 文件数量
```

## 环境变量

```bash
export IA_ACCESS_KEY_ID="your-key"
export IA_SECRET_ACCESS_KEY="your-secret"
```

## 配置文件位置

```
~/.config/ia.ini
```

示例配置：
```ini
[general]
user_agent_suffix = OpenClaw/1.0
```

## 安全注意事项

- **永远不要**在日志中记录：
  - 用户搜索词（敏感查询）
  - 歌曲 ID、内部标识符
  - 歌词内容
  - API 密钥
- 使用 `BuildConfig.DEBUG` 保护所有调试日志
- 生产环境避免 `Log.d()` 输出敏感数据

## 常见问题

**Q: 上传失败 "identifier exists"**
A: 标识符已存在且不可更改，选择新标识符。

**Q: 项目搜索不到**
A: 上传后通常在几分钟内索引，最长 24 小时。检查 `ia tasks <id>`。

**Q: 429 错误**
A: 速率限制，等待 Retry-After 秒数。

**Q: 大文件上传中断**
A: 使用 `--checksum` 支持断点续传。

**Q: 如何只下载原文件，不要衍生物？**
A: `ia download <id> --source=original`

## 有用链接

- 开发者文档: https://archive.org/developers/
- 获取 API 密钥: https://archive.org/account/s3.php
- 完整命令参考: 运行 `ia --help` 或查看 https://github.com/jjjake/internetarchive
