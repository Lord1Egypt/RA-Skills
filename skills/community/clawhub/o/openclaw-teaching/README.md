# OpenClaw 知识教学技能

一个用于 OpenClaw 平台知识管理和教学的技能包。

## 功能特性

- **知识库管理**: 维护和更新 OpenClaw 平台知识
- **PPT 生成**: 将知识内容导出为专业的演示文稿
- **Word 文档生成**: 生成详细的教学文档
- **知识更新**: 支持增量更新和批量导入

## 安装方法

### 方法一：通过 OpenClaw 平台安装

1. 打开 OpenClaw 平台
2. 进入技能市场
3. 搜索 "openclaw-teaching"
4. 点击安装

### 方法二：手动安装

1. 下载 `openclaw-teaching.zip`
2. 解压到 OpenClaw 技能目录
3. 重启 OpenClaw 服务

## 使用说明

### 生成 PPT

```bash
python scripts/generate_docs.py ppt \
    --output "/path/to/output.pptx" \
    --template "modern"
```

### 生成 Word 文档

```bash
python scripts/generate_docs.py docx \
    --output "/path/to/output.docx" \
    --include-toc \
    --include-cover
```

### 更新知识库

```bash
# 添加新知识
python scripts/update_knowledge.py add \
    --category "技能开发" \
    --title "新功能介绍" \
    --content "详细内容..."

# 搜索知识
python scripts/update_knowledge.py search --keyword "API"

# 查看统计
python scripts/update_knowledge.py stats
```

## 目录结构

```
openclaw-teaching/
├── SKILL.md              # 技能配置文件
├── KNOWLEDGE_BASE.md     # 知识库文档
├── LICENSE.txt           # 许可证
├── README.md             # 说明文档
└── scripts/
    ├── generate_docs.py  # 文档生成脚本
    └── update_knowledge.py # 知识更新脚本
```

## 依赖要求

- Python 3.8+
- python-pptx (PPT 生成)
- python-docx (Word 文档生成)

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2024-01-01 | 初始版本发布 |

## 许可证

MIT License - 详见 LICENSE.txt

## 联系方式

- 技术支持: support@openclaw.io
- 问题反馈: https://github.com/openclaw/issues
