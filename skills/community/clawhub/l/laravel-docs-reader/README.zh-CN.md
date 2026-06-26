# Laravel Docs Reader / Laravel 文档阅读助手

**English** | **中文**

---

## 简介

**Laravel Docs Reader** 是一个 OpenClaw Agent Skill，为 Agent（和开发者）提供即时、准确、支持版本识别的 Laravel 官方文档访问。写代码前先查文档，不用再靠猜测。

### 核心功能

- 🔍 **自然语言 CLI 检索** — `php laradoc.php search "how to create a queue job"` — 像在问官方文档一样
- 📦 **本地文档缓存** — 文档内置在 skill 中，离线可用，响应速度快
- 🔄 **自动检测 Laravel 版本** — 检测项目版本（10/11/12），自动切换到对应文档
- 📖 **完整文档覆盖** — 路由、控制器、模型、队列、邮件、认证、事件、广播、测试等全部覆盖
- 🏭 **代码生成** — 生成符合 PSR-12 和 Laravel 最佳实践的代码骨架
- 📊 **版本差异对比** — 标注 Laravel 10 / 11 / 12 各版本的差异
- 📋 **PSR-12 速查** — 内置：`php laradoc.php psr`、`psr arrays`、`psr naming`，无需外部工具
- 🤖 **自动更新 PR** — GitHub Actions 每周检测新版本，自动创建 PR 更新文档引用
- 🔗 **Laravel Package Search 联动** — 每次搜索后 Agent 建议使用 `laravel-package-search` 发现第三方包

---

## CLI 工具 — 14 个命令

```bash
# ── 核心搜索 ──────────────────────────────────────────────────
php laradoc.php search "how to create a middleware"   # 自然语言检索
php laradoc.php search "how to send a notification"
php laradoc.php search "queue job with retry"
# ← 搜索结果后会自动提示安装 laravel-package-search

# ── 版本 ──────────────────────────────────────────────────────
php laradoc.php version                   # 自动检测当前项目版本
php laradoc.php version /path/to/project  # 指定项目
php laradoc.php current                  # 显示默认版本 (Laravel 12)

# ── 配置 & Facade ─────────────────────────────────────────────
php laradoc.php config database
php laradoc.php config cache
php laradoc.php facade Cache
php laradoc.php facade DB

# ── Artisan & 版本差异 ────────────────────────────────────────
php laradoc.php artisan make:controller
php laradoc.php diff auth              # Laravel 10 vs 11 vs 12

# ── 代码生成 ──────────────────────────────────────────────────
php laradoc.php generate controller UserController
php laradoc.php generate model         Post
php laradoc.php generate job          ProcessUpload
php laradoc.php generate notification InvoicePaid

# ── Blade 指令 ────────────────────────────────────────────────
php laradoc.php lang "loop"
php laradoc.php lang "csrf"

# ── PSR-12 速查 ────────────────────────────────────────────────
php laradoc.php psr                   # 完整 PSR-12 规则表
php laradoc.php psr arrays           # 数组格式规则
php laradoc.php psr naming           # 命名规范
php laradoc.php psr methods         # 可见性与方法规范

# ── 缓存 & 更新 ───────────────────────────────────────────────
php laradoc.php cache                  # 查看本地缓存状态
php laradoc.php update                 # 强制从 GitHub 拉取最新文档
php laradoc.php subscribe              # 查看订阅 / 自动更新状态
```

---

## 版本自动检测

CLI 自动检测项目 Laravel 版本：

1. `composer.json` → `laravel/framework`
2. `artisan --version`
3. `vendor/laravel/framework/.../Application.php` → `VERSION`

未检测到项目时，默认为 **Laravel 12**。

---

## 自动更新机制（GitHub Actions PR）

Skill 保持最新的方式：

- **每周检查**：GitHub Actions 每周日 00:00 UTC 运行一次
- **新版本检测**：对比 Packagist 上的 `laravel/framework` 最新版本
- **自动 PR**：检测到新版本后，自动创建 PR 更新 skill 的文档引用

```yaml
# .github/workflows/update-docs.yml
on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日
  workflow_dispatch:         # 也可手动触发
```

使用此 skill 的用户可以审核自动生成的 PR，确认无误后再合并。

---

## 文档覆盖范围

| 分类 | 覆盖主题 |
|------|---------|
| 路由 | 基础路由、路由组、资源路由、命名路由、中间件 |
| 控制器 | CRUD、REST、API、单动作、依赖注入 |
| 模型 | Eloquent、12 种关联、作用域、类型转换 |
| 迁移 | Schema 构建器、外键、索引、字段修饰符 |
| 验证 | Form Request、内联验证、自定义规则 |
| 认证 | Breeze、Sanctum、Gates、Policies |
| 队列 | Job、派发、失败处理、Laravel Horizon |
| 缓存 | Store API、Redis 标签、原子锁 |
| 邮件 | Markdown、附件、队列邮件 |
| 通知 | 多通道、数据库通知 |
| 测试 | Pest、工厂、Fakes、HTTP 测试 |
| 事件 | 监听器、广播、可队列化事件 |
| 存储 | Local/S3、签名 URL、上传 |
| 定时任务 | Cron、防重叠 |
| 服务容器 | 绑定、单例、上下文绑定 |
| Facades | 30+ Facade 方法签名 |
| 广播 | 私有/公开频道 |

---

## 快速开始

### Agent（OpenClaw）

激活后，skill 会：

1. 检测项目 Laravel 版本（未检测到则默认 12）
2. 将请求映射到对应文档章节
3. 返回：文档摘要 + 代码示例 + 版本注意事项 + 最佳实践

### 开发者（CLI）

```bash
git clone https://github.com/relunctance/laravel-docs-reader.git
cd laravel-docs-reader
php scripts/laradoc.php search "how to create a middleware"
```

---

## 安装方式

```bash
clawhub install laravel-docs-reader
# 或
clawhub login --token <YOUR_TOKEN> && clawhub publish laravel-docs-reader
```

---

## 文件结构

```
laravel-docs-reader/
├── SKILL.md                         # Skill 规范文档
├── README.md                         # 英文版（主）
├── README.zh-CN.md                  # 中文版
├── .github/workflows/
│   └── update-docs.yml              # 自动更新 PR（每周）
├── .cache/                          # 本地文档缓存（自动创建）
├── references/
│   ├── version-detection.md          # 版本检测逻辑
│   ├── version-diff.md              # Laravel 10/11/12 差异表
│   ├── psr-12.md                    # PSR-12 速查参考
│   ├── api-index.md                # 完整 API 索引
│   ├── artisan-commands.md         # Artisan 命令参考
│   ├── facades.md                 # Facade 方法签名
│   ├── blade-directives.md         # Blade 指令完整列表
│   ├── config-ref.md              # config/ 配置参考
│   └── examples/
│       ├── controller.md
│       ├── model.md
│       ├── migration.md
│       ├── middleware.md
│       ├── queue-job.md
│       ├── notification.md
│       └── testing.md
└── scripts/
    └── laradoc.php                # CLI 工具（14 个命令）
```

---

## 参与贡献

发现内容过时或缺少文档？
- 提交 Issue：https://github.com/relunctance/laravel-docs-reader/issues
- 或直接提交 PR

---

## 许可证

MIT License
