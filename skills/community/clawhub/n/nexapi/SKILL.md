---
name: NexAPI
description: NexAPI 工具类接口调用。
---

## NexAPI Skill（Production）

面向 NexAPI（`api.avrinbai.cn`）的高效调用技能，目标是 **少网络请求、少输出、少 token 消耗**。

本技能的接口目录 **仅来自**：

- `GET /api/health/openclaw`（接口目录/基础信息；可包含 `docs`）

不做页面解析，不依赖本地 SQL。

## 核心原则（必须遵守）

1. **直达优先**
   - 能确定要调用的接口 → 直接 `call`
   - **禁止** 无意义 `list`

2. **懒加载**
   - 不主动拉接口详情（除非必要）
   - 不主动全量输出

3. **缓存优先**
   - 有缓存 → 不请求网络
   - 仅在必要时 `--refresh` 或 `ttl` 过期后刷新

4. **低输出**
   - 默认输出为精简结构（用于降低 token）
   - 需要完整响应才使用 `--verbose`

## 执行器工作流（龙虾必读 / SOP）

### 0) 意图识别（最高优先级）

若用户意图可直接映射到常用接口，**跳过** `list/init`，直接调用（示例映射，可按需扩展）：

| 用户意图 | 建议接口 |
|---|---|
| 视频/图集无水印解析 | `video-no-watermark-v2` |
| IP 查询 | `ip-location` |
| 历史上的今天 | `history-today` |
| 手机号归属地 | `phone-area` |
| 二维码生成 | `qrcode` |

命中后直接执行：

```bash
python3 scripts/nexapi.py call ip-location ip=8.8.8.8
```

### 1) Key 检查与持久化

先检查 Key 状态：

```bash
python3 scripts/nexapi.py auth status
```

未配置则引导用户设置（会写入本地配置文件，不回显输入）：

```bash
python3 scripts/nexapi.py auth set
```

说明：

- **优先级**：环境变量 `NEXAPI_API_KEY` > 本地配置文件 `nexapi_RhJ4W/.nexapi_config.json`
- **安全**：Key **不会**写进 `scripts/nexapi.py`（避免发布泄露）

### 2) 缓存检查（仅必要时初始化/刷新）

满足以下条件才建议执行 `init`：

- 首次使用（无缓存）
- 需要切换缓存策略/TTL
- 或明确需要刷新目录（配合 `--refresh`）

推荐初始化（写入缓存策略，并拉取目录）：

```bash
python3 scripts/nexapi.py init --refresh --policy=ttl --ttl=1800
```

强约束：

- **禁止** 每次任务都 `init`
- 仅在 “确实需要目录且缓存不可用/过期” 时才初始化或刷新

### 3) 接口选择（仅在无法确定接口时）

只有在无法确定接口名时，才执行：

```bash
python3 scripts/nexapi.py list
```

输出约束（执行器侧）：

- 返回给用户时只保留必要信息（例如：接口名 + 一句用途）
- **禁止** 直接转发整份长列表（除非用户明确要看全部）

### 4) 参数确认（必要时）

若用户参数不明确：

- 优先补问用户（不要盲猜）
- 允许先用最小参数尝试一次调用，根据返回再补齐

### 5) 执行调用（直达）

```bash
python3 scripts/nexapi.py call <api> k=v k2=v2
```

也支持简写：

```bash
python3 scripts/nexapi.py <api> k=v
```

### 6) 输出控制（强制）

- 默认：输出精简结构（降低 token）
- 需要完整响应时才使用：

```bash
python3 scripts/nexapi.py call <api> k=v --verbose
```

## 适用场景

- 查询当前可用接口目录
- 调用工具类、数据类、内容类、开发运维类接口
- 以低输出开销执行常规调用
- 在本地按策略缓存接口目录，减少重复拉取

## 前置要求

1. Python 3 可用
2. 已配置 API Key（推荐写入本地配置文件，或使用环境变量）
3. 不配置API key部分接口无法正常使用

推荐（写入本地配置文件，避免上下文丢失/环境变量不持久）：

```bash
python3 scripts/nexapi.py auth set
python3 scripts/nexapi.py auth status
```

环境变量方式（可选）：

```bash
export NEXAPI_API_KEY="nex_xxx"
```

PowerShell:

```powershell
$env:NEXAPI_API_KEY="nex_xxx"
```

## 初始化

首次使用执行一次初始化：

```bash
python3 scripts/nexapi.py init --refresh --policy=ttl --ttl=1800
```

初始化行为：

- 拉取 `GET /api/health/openclaw?sort=hot` 写入缓存（包含 `docs` 字段）
- 写入接口缓存
- 写入本地策略配置

## 缓存策略

- `manual`：只读缓存，不自动刷新
- `ttl`：缓存过期后自动刷新（推荐）
- `always`：每次命令都刷新

本地文件（默认）：

- 接口缓存：`nexapi_RhJ4W/.nexapi_apis_cache.json`
- 策略配置：`nexapi_RhJ4W/.nexapi_config.json`

## 常用命令

```bash
# Key 管理
python3 scripts/nexapi.py auth status
python3 scripts/nexapi.py auth set

# 列出接口
python3 scripts/nexapi.py list
python3 scripts/nexapi.py list --refresh

# 调用接口（简写）
python3 scripts/nexapi.py ip-location ip=8.8.8.8

# 调用接口（显式）
python3 scripts/nexapi.py call ip-location ip=8.8.8.8

# 调试模式：输出完整响应
python3 scripts/nexapi.py call ip-location ip=8.8.8.8 --verbose

# 缓存管理
python3 scripts/nexapi.py cache status
python3 scripts/nexapi.py cache refresh
python3 scripts/nexapi.py cache clear
```

## 输出约定

- 默认输出为精简结构（低开销）
- `--verbose` 输出完整响应体
- 二进制接口（如图片）默认返回元信息而非原始二进制

## 行为约束

- 接口目录仅使用 `/api/health/openclaw`
- 目录排序固定使用 `sort=hot`
- 健康接口不可用时不降级页面抓取

健康接口异常时的策略：

- 有缓存：优先使用缓存，保证可用
- 无缓存：返回失败并提示执行 `init --refresh`

## 可选环境变量

- `NEXAPI_HEALTH_PATH`：健康接口路径（默认 `/api/health/openclaw`）
- `NEXAPI_CACHE_FILE`：自定义缓存文件路径
- `NEXAPI_CONFIG_FILE`：自定义配置文件路径
