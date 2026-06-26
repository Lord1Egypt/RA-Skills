# md2wechat-skill

将 Markdown 文件转换为微信公众号兼容的内联样式 HTML，并可一键上传到微信草稿箱。

## ✨ 功能特性

- **Markdown → 微信 HTML**：完整解析标题、列表、表格、代码块、引用等，自动转换为微信兼容的内联样式
- **Front Matter 元数据**：支持 YAML Front Matter 定义标题、作者、摘要等
- **图片自动处理**：正文内嵌的本地图片自动上传到微信 CDN
- **封面图上传**：支持指定封面图上传为微信永久素材
- **代码块深色主题**：代码块自动适配深色背景样式
- **超长内容截断**：超过微信 2MB 限制的内容自动安全截断

## 🚀 快速上手

### 安装依赖

```bash
pip install -r requirements.txt
```

### 模式一：仅转换 HTML（无需微信密钥）

```bash
python scripts/md2wechat.py ./article.md --convert-only --output ./preview.html
```

### 模式二：转换并上传到微信草稿箱

```bash
# 1. 配置微信凭据
cp resources/env_template.txt .env
# 编辑 .env 填入 WECHAT_APPID 和 WECHAT_SECRET

# 2. 上传
python scripts/md2wechat.py ./article.md --draft --env-file .env
```

## 📁 目录结构

```
md2wechat-skill-1.0.0/
├── SKILL.md                # 技能定义入口文件
├── _meta.json              # 发布元数据
├── requirements.txt        # Python 依赖清单
├── README.md               # 本文件
├── scripts/
│   ├── md2wechat.py        # CLI 主入口
│   ├── md_converter.py     # Markdown → HTML 转换引擎
│   ├── html_formatter.py   # HTML 内联样式适配器
│   └── wechat_client.py    # 微信公众号 API 客户端
├── examples/
│   └── sample_article.md   # 示例 Markdown 文章
└── resources/
    └── env_template.txt    # 环境变量配置模板
```

## 🔑 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `WECHAT_APPID` | 微信公众号 AppID | 仅 `--draft` 模式 |
| `WECHAT_SECRET` | 微信公众号 AppSecret | 仅 `--draft` 模式 |

获取方式：登录 [微信公众平台](https://mp.weixin.qq.com/) →「开发」→「基本配置」→ 获取 AppID 和 AppSecret。

## 📄 许可证

MIT
