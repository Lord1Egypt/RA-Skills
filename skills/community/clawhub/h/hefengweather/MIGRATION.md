# OpenClaw Skill 重构说明

## 概述

本次重构将和风天气查询项目转换为符合 **OpenClaw Skill 标准** 的格式,同时保留了原有的 Python 模块功能。

## 主要变更

### 1. 新增符合 OpenClaw 标准的 SKILL.md

- ✅ **Frontmatter 元数据**: 包含技能名称、描述、作者、版本、分类、标签、依赖配置等
- ✅ **三层渐进式披露设计**:
  - 第1层: 元数据(始终在上下文中)
  - 第2层: SKILL.md 主体(使用指南、工作流程、参数说明)
  - 第3层: 捆绑资源(scripts/ 目录)
- ✅ **自然语言触发条件**: 描述了何时触发此技能
- ✅ **完整的功能文档**: 包含所有工具的详细说明和使用示例

### 2. 创建独立的可执行脚本

将原有的 `skill.py` 模块重构为多个独立的可执行脚本:

| 原函数 | 新脚本 | 功能 |
|--------|--------|------|
| `configure()` | `scripts/configure.py` | 配置API认证信息 |
| `get_weather_now()` | `scripts/weather_now.py` | 查询实时天气 |
| `get_weather()` | `scripts/weather.py` | 查询天气预报 |
| `get_hourly_weather()` | `scripts/weather_hourly.py` | 查询逐小时预报 |
| `get_air_quality()` | `scripts/air_quality.py` | 查询空气质量 |
| `get_indices()` | `scripts/indices.py` | 查询生活指数 |
| `get_warning()` | `scripts/warning.py` | 查询气象预警 |
| `get_astronomy_sun()` | `scripts/astronomy_sun.py` | 查询日出日落 |
| `get_astronomy_moon()` | `scripts/astronomy_moon.py` | 查询月相数据 |
| `get_minutely_5m()` | `scripts/minutely_5m.py` | 查询分钟级降水 |
| `get_grid_weather_now()` | `scripts/grid_weather_now.py` | 查询格点天气 |
| `get_top_cities()` | `scripts/top_cities.py` | 查询热门城市 |
| `search_poi()` | `scripts/search_poi.py` | 搜索POI |

### 3. 创建共享的 API 客户端

- **`scripts/qweather_api.py`**: 统一的API客户端类,封装了所有API调用逻辑
- 所有脚本都使用这个共享模块,避免代码重复
- 支持API KEY和JWT两种认证方式

### 4. 保留原有模块

- **`skill.py`**: 保留了原有的Python模块,可以直接导入使用
- 确保向后兼容性,现有代码无需修改

## 目录结构

```
hefeng-weather-skill/
├── SKILL.md                 # ⭐ OpenClaw Skill 核心定义文件
├── README.md                # 项目说明文档
├── MIGRATION.md             # 重构说明文档(本文件)
├── skill.py                 # 原始Python模块(保留)
├── .env.example             # 环境变量示例
├── scripts/                 # ⭐ 可执行脚本目录
│   ├── __init__.py
│   ├── qweather_api.py      # 共享API客户端
│   ├── configure.py         # 配置脚本
│   ├── weather_now.py       # 实时天气
│   ├── weather.py           # 天气预报
│   ├── weather_hourly.py    # 逐小时预报
│   ├── air_quality.py       # 空气质量
│   ├── indices.py           # 生活指数
│   ├── warning.py           # 预警信息
│   ├── astronomy_sun.py     # 日出日落
│   ├── astronomy_moon.py    # 月相数据
│   ├── minutely_5m.py       # 分钟级降水
│   ├── grid_weather_now.py  # 格点天气
│   ├── search_poi.py        # POI搜索
│   └── top_cities.py        # 热门城市
└── [原有文件...]
```

## 使用方式

### 作为 OpenClaw Skill 使用

1. **安装到 OpenClaw**:
   ```bash
   cp SKILL.md ~/.openclaw/skills/hefeng-weather.md
   cp -r scripts ~/.openclaw/skills/hefeng-weather/
   ```

2. **OpenClaw 会自动识别**:
   - 读取 SKILL.md 的元数据
   - 根据用户自然语言输入触发相应功能
   - 执行对应的脚本

### 作为独立脚本使用

```bash
# 配置API
python scripts/configure.py --api-host "your-domain.qweatherapi.com" --api-key "your_key"

# 查询实时天气
python scripts/weather_now.py --city "北京"

# 查询天气预报
python scripts/weather.py --city "上海" --days "7d"
```

### 作为 Python 模块使用

```python
from skill import get_weather_now, get_weather

# 实时天气
result = get_weather_now(city="北京")
print(f"当前温度: {result['now']['temp']}°C")

# 天气预报
result = get_weather(city="上海", days="3d")
```

## 符合 OpenClaw 标准的特性

### ✅ Frontmatter 元数据

```yaml
---
name: 和风天气查询
description: 提供基于和风天气API的全面气象数据查询服务...
author: fengyu
version: 1.0.0
category: weather
tags: [weather, forecast, air-quality, astronomy, qweather]
dependencies: |
  - Python >= 3.11
  - httpx >= 0.25.0
  ...
config:
  env:
    - HEFENG_API_HOST
    - HEFENG_API_KEY
---
```

### ✅ 三层渐进式披露

1. **第1层 - 元数据**: 始终在上下文中,占用最少资源
2. **第2层 - SKILL.md 主体**: 包含使用指南、工作流程、参数说明
3. **第3层 - 捆绑资源**: scripts/ 目录下的可执行脚本

### ✅ 自然语言触发

SKILL.md 中的 `description` 描述了触发条件:
- "当用户需要查询天气信息..."
- "当用户需要查询空气质量..."
- "当用户需要查询气象预警..."

### ✅ 参数化执行

所有脚本都支持命令行参数:
```bash
python scripts/weather_now.py --city "北京" --lang "zh" --unit "m"
```

## 向后兼容性

- ✅ 原有的 `skill.py` 模块完全保留
- ✅ 所有函数签名和行为保持不变
- ✅ 现有代码无需修改即可继续使用

## 下一步

1. **测试脚本**:
   ```bash
   python scripts/configure.py --help
   python scripts/weather_now.py --help
   ```

2. **配置API**:
   ```bash
   python scripts/configure.py --api-host "your-domain.qweatherapi.com" --api-key "your_key"
   ```

3. **查询天气**:
   ```bash
   python scripts/weather_now.py --city "北京"
   ```

4. **集成到 OpenClaw**:
   - 将 SKILL.md 添加到 OpenClaw 技能目录
   - OpenClaw 将自动识别和使用

## 参考资料

- [OpenClaw 官方文档](https://openclaw.dev)
- [OpenClaw Skill 规范](https://openclaw.dev/skills)
- [和风天气 API 文档](https://dev.qweather.com/docs/)

## 总结

本次重构完全符合 **OpenClaw Skill 标准**,同时保持了向后兼容性。项目现在可以:

1. ✅ 作为 OpenClaw Skill 使用
2. ✅ 作为独立脚本使用
3. ✅ 作为 Python 模块导入使用

所有功能均已实现,脚本已添加执行权限,可以立即使用!
