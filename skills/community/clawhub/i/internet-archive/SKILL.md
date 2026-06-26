# Internet Archive Skill

提供与 Internet Archive (archive.org) 交互的能力：搜索、下载、上传和管理存档内容。

## 描述

此技能允许你：
- 搜索 Internet Archive 目录（支持高级查询语法）
- 下载任何公开存档项目的文件
- 上传文件到你的存档账户（需要认证）
- 管理已上传项目的元数据
- 列出项目中的文件
- 自动安装和配置 `ia` CLI 工具

## 触发器

- "搜索 Internet Archive"
- "从 archive.org 下载"
- "上传到 Internet Archive"
- "管理存档元数据"
- "检查 Internet Archive 工具"
- "安装 ia 命令行工具"
- "存档相关"、"archive.org"

## 输入

用户请求与 Internet Archive 相关的操作。

## 输出

执行具体的 archive.org 操作，返回搜索结果、下载状态、上传确认等信息。

## 实现

- 主脚本: `internet-archive.py`
- 参考文档: `references/`

## 使用方式

直接调用 Python 脚本：

```bash
python3 skills/internet-archive/internet-archive.py <intent> [参数]
```

### 支持的 Intents

#### `check` - 检查工具状态
检查 `ia` CLI 是否已安装和配置。

```bash
python3 skills/internet-archive/internet-archive.py check
```

#### `install` - 安装 ia CLI
自动安装 `internetarchive` 包（使用 uv/pipx/pip）。

```bash
python3 skills/internet-archive/internet-archive.py install
```

#### `search` - 搜索存档
搜索 Internet Archive 目录。

```bash
# 基本搜索
python3 skills/internet-archive/internet-archive.py search "collection:nasa mediatype:image"

# 仅返回标识符列表
python3 skills/internet-archive/internet-archive.py search "public domain books" --itemlist

# 全文搜索
python3 skills/internet-archive/internet-archive.py search "climate change" --fts

# 排序和字段过滤
python3 skills/internet-archive/internet-archive.py search "mediatype:movies" --sort="downloads desc" --field=title --field=identifier
```

常用参数：
- `--itemlist` - 仅输出标识符，每行一个
- `--fts` - 全文搜索（在文本内容中搜索，而非仅元数据）
- `--sort="field asc|desc"` - 排序（如 `downloads desc`, `date asc`）
- `--field=<name>` - 只返回指定字段（可重复使用）
- `--parameters="rows=20&page=1"` - 原始查询参数

#### `download` - 下载项目文件
下载 Internet Archive 项目的文件。

```bash
# 下载整个项目
python3 skills/internet-archive/internet-archive.py download <identifier>

# 只下载特定扩展名文件
python3 skills/internet-archive/internet-archive.py download <identifier> --glob="*.pdf"

# 排除某些文件
python3 skills/internet-archive/internet-archive.py download <identifier> --exclude="*low*"

# 下载到指定目录
python3 skills/internet-archive/internet-archive.py download <identifier> --destdir=./downloads

# 预览（不实际下载）
python3 skills/internet-archive/internet-archive.py download <identifier> --dry-run

# 只下载原始文件，跳过衍生物
python3 skills/internet-archive/internet-archive.py download <identifier> --source=original
```

#### `upload` - 上传文件
上传文件到你的 Internet Archive 账户（需要认证）。

```bash
python3 skills/internet-archive/internet-archive.py upload <identifier> file1.pdf file2.jpg \
  --metadata="mediatype:texts" \
  --metadata="title:My Document" \
  --metadata="creator:Your Name"

# 上传并验证
python3 skills/internet-archive/internet-archive.py upload <id> document.pdf \
  --metadata="mediatype:texts" --checksum --verify

# 跳过衍生物生成（更快上传）
python3 skills/internet-archive/internet-archive.py upload <id> video.mp4 \
  --metadata="mediatype:movies" --no-derive
```

必需参数：
- `<identifier>` - 项目标识符（唯一、仅 ASCII 字母数字、连字符）
- `files` - 要上传的文件路径列表
- `--metadata="key:value"` - 元数据（至少需要 `mediatype`）

可选参数：
- `--checksum` - 使用校验和跳过已上传的文件
- `--verify` - 上传后验证数据完整性
- `--no-derive` - 跳过自动衍生物生成
- `--retries=N` - 重试次数（默认 0）

#### `metadata` - 查看/修改元数据
查看或修改项目元数据。

```bash
# 查看完整元数据（JSON 格式）
python3 skills/internet-archive/internet-archive.py metadata <identifier>

# 列出包含的文件格式
python3 skills/internet-archive/internet-archive.py metadata <identifier> --formats

# 修改字段
python3 skills/internet-archive/internet-archive.py metadata <identifier> --modify="title:New Title"

# 添加值到列表字段（如 subjects）
python3 skills/internet-archive/internet-archive.py metadata <identifier> --append-list="subject:new topic"

# 删除字段
python3 skills/internet-archive/internet-archive.py metadata <identifier> --modify="oldfield:REMOVE_TAG"
```

#### `list` - 列出项目文件
列出 Internet Archive 项目中的所有文件。

```bash
# 列出所有文件
python3 skills/internet-archive/internet-archive.py list <identifier>

# 只显示名称和大小
python3 skills/internet-archive/internet-archive.py list <identifier> --columns=name,size

# 显示完整下载 URL
python3 skills/internet-archive/internet-archive.py list <identifier> --location

# 显示所有文件信息（包含格式、校验和等）
python3 skills/internet-archive/internet-archive.py list <identifier> --all --verbose
```

## 配置和认证

**上传和修改元数据需要认证**。搜索和下载公开项目不需要。

### 配置步骤

1. **创建 Internet Archive 账户**：https://archive.org/account/signup
2. **获取 S3 兼容 API 密钥**：https://archive.org/account/s3.php
   - 点击 "Create new keys" 或使用现有密钥
   - 复制 `Access Key ID` 和 `Secret Access Key`
3. **运行配置命令**：
   ```bash
   ia configure
   ```
   按提示输入密钥。

或者，设置环境变量：
```bash
export IA_ACCESS_KEY_ID="your-access-key"
export IA_SECRET_ACCESS_KEY="your-secret-key"
```

配置文件保存在 `~/.config/ia.ini`。

验证配置：
```bash
ia configure --whoami  # 应显示你的用户名
```

### User-Agent 要求

**所有请求必须包含明确的 User-Agent**。`ia` CLI 默认包含你的访问密钥。对于自动化工具，建议设置自定义后缀：

```bash
ia --user-agent-suffix "OpenClaw/1.0"
```

或在 `~/.config/ia.ini` 中：
```ini
[general]
user_agent_suffix = OpenClaw/1.0
```

这有助于 Internet Archive 跟踪来源并维护服务质量。

## 自动安装

如果 `ia` 命令未找到，此技能会提示安装。支持的安装方式（按顺序尝试）：
1. `uv tool install internetarchive`（推荐）
2. `pipx install internetarchive`
3. `pip install internetarchive`

你需要 Python 3.9+ 和 pip/uv/pipx 之一。

## 重要概念

### 项目（Item）
archive.org 的基本单位。一个项目是一组相关文件的逻辑集合（一本书、一张专辑、一个数据集等）。每个项目有唯一的标识符。

项目包含：
- 原始上传文件
- 衍生物（系统自动生成的转换版本）
- `<identifier>_meta.xml` - 项目级元数据
- `<identifier>_files.xml` - 文件级元数据

### 集合（Collection）
项目必须属于一个集合。只有 IA 员工可以创建新集合（通常需要至少 50 个项目）。公开上传集合包括：
- `opensource_movies`, `opensource_audio`, `opensource_media`
- `community_texts`, `community_video`, `community_audio`

### 衍生物（Derivatives）
上传后，IA 自动生成衍生物（不同格式和分辨率的转换版本）：
- 视频 → h.264, Ogg, 多种码率
- 音频 → MP3, Ogg Vorbis, FLAC
- 文本/书籍 → OCR, 可搜索 PDF, EPUB, DjVu
- 图片 → 缩略图, JPEG 2000

使用 `--no-derive` 跳过衍生物生成（更快上传，但内容访问性降低）。

### 元数据模式
必需字段：`identifier`, `mediatype`

推荐字段：`title`, `description`, `creator`, `date`, `subject`, `collection`, `language`

标识符要求：
- 仅 ASCII 字母数字、下划线、连字符、句点
- 以字母数字开头
- 5-100 字符（5-80 推荐）
- 一旦设置不可更改

## 最佳实践

1. **上传前测试** - 使用 `test_collection` 验证上传（30 天后自动删除）
2. **使用有意义的标识符** - 小写、连字符分隔、描述性
3. **完整的元数据** - 至少包含 title, creator, description
4. **检查标识符冲突** - `ia metadata <id>` 看是否已存在
5. **大文件分卷** - 大文件集打包成 ZIP 再上传
6. **使用校验和** - `--checksum` 支持断点续传
7. **速率限制** - 批量操作时添加延迟（如 GNU Parallel 的 `--delay 1`）
8. **预览操作** - 使用 `--dry-run` 预览下载/上传
9. **保护敏感日志** - 避免在日志中记录用户搜索词、歌曲 ID、歌词内容等

关于日志保护：
- 使用 `BuildConfig.DEBUG` 保护所有日志输出
- 不在任何日志中记录用户隐私数据
- 开发日志使用 `Log.d()`，生产环境自动静默

## 常见错误及解决

| 错误 | 解决方案 |
|-----|----------|
| "not configured" | 运行 `ia configure` 或设置环境变量 |
| "identifier exists" | 选择其他标识符（不可更改） |
| "permission denied" | 检查 https://archive.org/account/s3.php 的密钥 |
| "network error" | 重试操作，检查网络连接 |
| "429 Too Many Requests" | 速率限制；等待 Retry-After 指定时间 |
| 项目未出现在搜索中 | 通常几分钟内出现；最长 24 小时；检查 `ia tasks <identifier>` |

## 参考资源

- [Internet Archive 开发者文档](https://archive.org/developers/)
- [Items API](https://archive.org/developers/items.html)
- [元数据模式](https://archive.org/developers/metadata-schema/)
- [Metadata Write API](https://archive.org/developers/md-write.html)
- [Tasks API](https://archive.org/developers/tasks.html)
- [Python 库文档](https://github.com/jjjake/internetarchive)

## 注意事项

- 此技能依赖外部 `ia` 命令；确保安装 `internetarchive` Python 包
- 上传和元数据修改需要有效的 Internet Archive 账户和 API 密钥
- 项目标识符一旦创建不可更改，选择时需谨慎
- 大文件上传可能需要较长时间，建议使用 `--checksum` 支持断点续传
- 遵循 Internet Archive 的使用条款和服务政策
