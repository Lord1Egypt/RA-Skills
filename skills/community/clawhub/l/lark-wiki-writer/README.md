# Lark Wiki Writer

飞书知识库文档写入器 - 支持 Markdown 解析、富文本、标题识别。

## 安装

```bash
# 下载 skill
git clone <repo_url>
cd lark-wiki-writer

# 或使用 clawhub
clawhub install lark-wiki-writer
```

## 快速开始

1. 创建飞书应用并获取凭证
2. 配置环境变量
3. 运行验证命令
4. 开始使用

详细文档请查看 [SKILL.md](SKILL.md)

## 示例

```bash
# 验证配置
python3 lark_wiki_writer.py validate \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --space-id YOUR_SPACE_ID

# 创建文档
python3 lark_wiki_writer.py write_file "我的文档" report.md \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --space-id YOUR_SPACE_ID
```

## 许可证

MIT
