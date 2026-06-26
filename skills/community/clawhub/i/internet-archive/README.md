# Internet Archive Skill for OpenClaw

将 Internet Archive 的强大功能集成到 OpenClaw 中。上传、下载、搜索和管理 archive.org 上的内容。

## 功能

- 搜索存档目录（支持 Lucene 查询语法和全文搜索）
- 下载任何公开项目的文件（支持通配符、格式过滤）
- 上传文件到你的存档账户（含完整元数据支持）
- 查看和修改项目元数据
- 列出项目文件
- 自动检测和安装 `ia` CLI 工具

## 安装

技能已放置在 OpenClaw 的 `skills/` 目录中。使用前确保：

1. 安装 `internetarchive` Python 包（可选，按需自动安装）：
   ```bash
   uv tool install internetarchive
   # 或
   pipx install internetarchive
   ```

2. 配置认证（仅上传所需）：
   ```bash
   ia configure
   ```
   从 https://archive.org/account/s3.php 获取密钥。

## 使用方法

从 OpenClaw 直接调用，或在命令行测试：

```bash
# 检查工具状态
python3 skills/internet-archive/internet-archive.py check

# 搜索
python3 skills/internet-archive/internet-archive.py search "collection:nasa mediatype:image"

# 下载
python3 skills/internet-archive/internet-archive.py download <identifier> --glob="*.pdf"

# 上传
python3 skills/internet-archive/internet-archive.py upload <id> file.txt \
  --metadata="mediatype:texts" --metadata="title:My File"

# 查看元数据
python3 skills/internet-archive/internet-archive.py metadata <identifier>

# 列出文件
python3 skills/internet-archive/internet-archive.py list <identifier>
```

## 技能结构

```
skills/internet-archive/
├── internet-archive.py    # 主脚本
├── SKILL.md               # 技能定义和文档
├── README.md              # 本文件
├── references/            # 附加参考文档
└── scripts/               # 辅助脚本（如有）
```

## 与原始仓库的对应

这个 OpenClaw 技能基于 [internetarchive/internet-archive-skills](https://github.com/internetarchive/internet-archive-skills) 仓库，将其从 Claude Code 插件格式转换为 OpenClaw 本地技能格式。

差异：
- 使用 Python 脚本直接实现功能，而非依赖 Claude 内置能力
- 适配 OpenClaw 的技能目录结构
- 简化的调用方式（命令行参数而非自然语言触发）
- 保持与 `ia` CLI 的兼容性

## 贡献

如有问题或改进建议，请参考原仓库：
https://github.com/internetarchive/internet-archive-skills

## 许可证

GNU AGPL v3.0 (与原仓库相同)

## 资源

- [Internet Archive](https://archive.org)
- [API 文档](https://archive.org/developers/)
- [ia CLI 工具](https://github.com/jjjake/internetarchive)
