---
name: laravel-package-search
description: Real-time Laravel package search via Packagist API with local cache. Supports 22 scenes, quality scoring, and cross-references to laravel-docs-reader for official documentation.
---

# Laravel Package Search - Skill Specification

## Overview

**Skill Name**: Laravel Package Search
**Type**: Development Assistant Skill
**Target**: Laravel developers seeking efficient plugin selection
**Engine**: OpenClaw Agent

---

## 1. Core Objectives

- **Real-time Packagist API** — data never stale, always fresh
- Local cache (1 hour TTL) — fast repeat queries
- Score packages by: stars × downloads × activity × Laravel compatibility
- Support **22 scene categories** including AI/LLM, rate-limit, Stripe, SMS
- Cross-reference to **laravel-docs-reader** for official Laravel documentation
- Provide install commands + config snippets

---

## 2. Scene Categories

### Supported Scenes

| Scene | Chinese | Description |
|-------|---------|-------------|
| `auth` | 认证/权限 | Authentication, authorization, roles, permissions |
| `payment` | 支付/订单 | Payment gateways, Stripe, Alipay, WeChat Pay |
| `multitenancy` | 多租户 | Multi-tenant SaaS applications |
| `excel` | Excel/导入导出 | Spreadsheet import/export, data processing |
| `media` | 媒体/文件 | File uploads, media management, CDN |
| `wechat` | 微信 | WeChat SDK, Mini Program |
| `queue` | 队列/任务 | Job queues, Laravel Horizon |
| `admin` | 后台管理 | Admin panels, Filament |
| `search` | 搜索/全文检索 | Full-text search, Algolia, Scout |
| `logging` | 日志/审计 | Logging, audit trails |
| `api` | API/SDK | REST API, GraphQL, Sanctum |
| `testing` | 测试 | Pest, PHPUnit |
| `cache` | 缓存 | Redis, cache management |
| `security` | 安全 | Security headers, CSRF |
| `devtools` | 开发工具 | Debug, Telescope, Debugbar |
| `email` | 邮件 | Mailgun, notifications |
| `storage` | 存储 | S3, cloud storage |
| `ui` | 前端/UI | Vue, React, Inertia, Breeze |
| `ai` | AI/LLM集成 | OpenAI, LLM, chatbot |
| `ratelimit` | 限流 | Rate limiting, throttle |
| `stripe` | Stripe支付 | Stripe subscriptions & payments |
| `sms` | 短信 | Twilio, SMS notifications |

---

## 3. Package Evaluation Criteria

Each package is scored in real-time via Packagist API (live data):

| Criterion | Weight | Source |
|----------|--------|--------|
| GitHub Stars | 15% | Packagist API (github_stars field) |
| Packagist Downloads | 20% | Packagist API (downloads.total) |
| Favorites | 10% | Packagist API (favers) |
| Maintenance Activity | 30% | Last commit time (≤30d=100, ≤1y=40, >2y=0) |
| Laravel Compatibility | 15% | composer.json require (10/11/12) |
| Description Quality | 10% | Non-empty description = 100 |

### Real-time Scoring

```
Score = min(100, stars/500)*0.15 + min(100, log10(downloads)*15)*0.20
      + min(100, favers/200)*0.10 + activityScore*0.30
      + (hasLaravelVersion ? 100 : 0)*0.15 + (hasDescription ? 100 : 0)*0.10
```

> Data fetched live from Packagist API. Cached for 1 hour in `scripts/.cache.json`.

---

## 4. Top 20 Laravel Packages

Run `php search.php top 20` for live rankings

---

## 5. Smart Recommendation Logic

When a user describes their needs:

1. **Parse Intent** → Map to scene category
2. **Match Packages** → Find packages in that scene
3. **Filter** → Remove incompatible versions
4. **Sort** → By recommendation score
5. **Output** → Top 3 recommendations with reasoning

### Output Template

```
## 🎯 Recommended for: [User's Scenario]

**Top Pick**: [Package Name]
- **Why**: [Recommendation Reason]
- **Alternative**: [Alternative Package]
- **Caution**: [Any concerns]
- **Install**: `composer require [package]`
- **Compatibility**: Laravel X / Y / Z

---

**Alternative 1**: [Name] ...
**Alternative 2**: [Name] ...
```

---

## 6. Installation & Configuration

Each package entry includes:

```bash
composer require vendor/package
```

```php
// config/services.php or dedicated config file
'package' => [
    'key' => env('PACKAGE_KEY'),
],
```

```php
// app/Providers/AppServiceProvider.php
public function register(): void
{
    $this->mergeConfigFrom(...);
}
```

---

## 7. Version Compatibility

| Laravel | Compatible Packages |
|---------|-------------------|
| Laravel 12 | Packages updated after 2024-Q4 |
| Laravel 11 | Packages updated after 2023-Q2 |
| Laravel 10 | Packages updated after 2022-Q1 |

Always verify: `composer show vendor/package --tree | grep laravel/framework`

---

## 8. CLI Tool (scripts/search.php)

Real-time Packagist API with local caching. No static data.

### Commands

```bash
php search.php <command> [args]
```

| Command | Args | Description |
|---------|------|-------------|
| `search` | `<scene> [limit]` | Search by scene (auth, payment, ai...) |
| `compare` | `<pkg1> <pkg2>` | Compare two packages |
| `recommend` | `<requirement>` | Natural language recommendation |
| `top` | `[limit]` | Show Top N packages (default 10) |
| `scenes` | — | List all 22 scene categories |

### Examples

```bash
# Search AI packages
php search.php search ai 3

# Compare two auth packages
php search.php compare spatie/laravel-permission laravel/sanctum

# Natural language recommendation
php search.php recommend "I need WeChat Pay for Laravel 11"
php search.php recommend "I need AI chat for Laravel"
php search.php recommend "I need rate limiting"

# Top 20 packages
php search.php top 20

# All scenes
php search.php scenes
```

### Caching

```
Cache file: scripts/.cache.json (auto-created)
TTL: 1 hour
```

### Integration with OpenClaw Agent

When the agent receives a package query, it calls `php search.php` and formats the output.
If the user asks about Laravel official docs, it cross-references `laravel-docs-reader` skill.

---

## 8b. laravel-docs-reader Cross-Reference

This skill automatically cross-references Laravel official documentation for known packages:

```
Package → Official Laravel Docs
spatie/laravel-permission → Authorization docs
laravel/scout → Database Search docs
laravel/horizon → Queues docs
laravel/telescope → Debugging docs
laravel/sanctum → SPA Authentication docs
laravel/cashier → Billing docs
laravel/fortify → Authentication docs
filament/filament → filamentphp.com/docs
maatwebsite/excel → docs.laravel-excel.com
```

For packages not in the map, the output includes:
```
📖 Laravel Docs: Run `laravel-docs-reader` to search official docs for this package
```

### Workflow

1. User asks: "recommend a Laravel auth package"
2. This skill returns ranked packages with install commands
3. Output includes: `📖 Laravel Docs: Run laravel-docs-reader to search official docs`
4. User can then ask: "search laravel-docs-reader for sanctum setup"
5. laravel-docs-reader handles the official documentation query

---


### Activation Keywords

- "帮我找个 Laravel 插件"
- "Laravel package for XXX"
- "推荐 Laravel 认证插件"
- "Laravel auth package recommendation"
- "帮我评估这个包"
- "compare Laravel packages"

### Workflow

1. User describes requirement (Chinese or English)
2. Skill identifies scene category
3. Skill searches Top20 + scene database
4. Skill returns ranked recommendations
5. User selects → Skill provides install + config

---

## 10. Data Sources

- **Packagist API**: `https://packagist.org/api/search.json?q=`
- **GitHub API**: `https://api.github.com/repos/{vendor}/{package}`
- **GitHub Trending**: Community activity
- **Official Laravel Packages**: laravel.com/packages

---

## 11. File Structure

```
laravel-package-search/
├── SKILL.md                          # This file
├── references/
│   └── scene-index.md                # Scene category index
└── scripts/
    └── search.php                    # Real-time Packagist CLI (v3)
```

---

## 12. Publishing to Skills Market

```bash
clawhub login
clawhub publish laravel-package-search
```

Or submit to ClawHub website for review.

---

## 13. Maintenance

- Update Top 20 quarterly
- Add new scenes as Laravel ecosystem evolves
- Track deprecated packages and mark them
- Update compatibility for new Laravel releases
