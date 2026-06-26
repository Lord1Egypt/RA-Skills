# 和风天气查询 Skill

基于和风天气API的气象数据查询服务,符合 **OpenClaw Skill 标准**。

## 功能特性

- **基础天气**: 实时天气、3-30天预报、逐小时预报、历史天气
- **空气质量**: 实时AQI、逐小时/逐日预报、监测站数据、历史数据
- **生活指数**: 16种指数(运动、洗车、穿衣、感冒、紫外线等)
- **气象预警**: 台风、暴雨、高温等灾害预警
- **天文数据**: 日出日落、月相数据(未来60天)
- **分钟级降水**: 未来2小时5分钟级预报
- **格点天气**: 高分辨率数值模式数据
- **地理信息**: 热门城市、POI搜索

## OpenClaw Skill 标准结构

```
hefeng-weather-skill/
├── SKILL.md              # OpenClaw Skill 核心定义文件
├── README.md             # 项目说明文档
├── skill.py              # 原始Python模块(保留用于直接导入)
├── scripts/              # 可执行脚本目录
│   ├── __init__.py
│   ├── qweather_api.py   # API客户端共享模块
│   ├── configure.py      # 配置脚本
│   ├── weather_now.py    # 实时天气
│   ├── weather.py        # 天气预报
│   ├── weather_hourly.py # 逐小时预报
│   ├── air_quality.py    # 空气质量
│   ├── indices.py        # 生活指数
│   ├── warning.py        # 预警信息
│   ├── astronomy_sun.py  # 日出日落
│   ├── astronomy_moon.py # 月相数据
│   ├── minutely_5m.py    # 分钟级降水
│   ├── grid_weather_now.py # 格点天气
│   ├── search_poi.py     # POI搜索
│   └── top_cities.py     # 热门城市
└── .env.example          # 环境变量示例
```

## 快速开始

### 1. 安装依赖

```bash
pip install httpx pyjwt python-dotenv cryptography
```

### 2. 配置API

**方式一: 使用配置脚本(推荐)**

```bash
python scripts/configure.py --api-host "your-domain.qweatherapi.com" --api-key "your_api_key"
```

**方式二: 手动创建配置文件**

创建 `~/.config/qweather/.env`:

```bash
mkdir -p ~/.config/qweather
cat > ~/.config/qweather/.env << 'EOF'
HEFENG_API_HOST=your-domain.qweatherapi.com
HEFENG_API_KEY=your_api_key_here
EOF
```

**方式三: 环境变量**

```bash
export HEFENG_API_HOST=your-domain.qweatherapi.com
export HEFENG_API_KEY=your_api_key_here
```

### 3. 使用脚本

查询实时天气:
```bash
python scripts/weather_now.py --city "北京"
```

查询天气预报:
```bash
python scripts/weather.py --city "上海" --days "7d"
```

查询空气质量:
```bash
python scripts/air_quality.py --city "广州"
```

查询生活指数:
```bash
python scripts/indices.py --city "深圳" --days "1d"
```

查询日出日落:
```bash
python scripts/astronomy_sun.py --location "北京" --date "20251029"
```

查询气象预警:
```bash
python scripts/warning.py --city "杭州"
```

## 可用脚本列表

### 基础天气

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `weather_now.py` | 实时天气 | `--city`, `--location` |
| `weather.py` | 天气预报(3-30天) | `--city`, `--days` (3d/7d/10d/15d/30d) |
| `weather_hourly.py` | 逐小时预报 | `--city`, `--hours` (24h/72h/168h) |

### 空气质量

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `air_quality.py` | 实时空气质量 | `--city` |

### 生活指数

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `indices.py` | 生活指数预报 | `--city`, `--days`, `--types` |

### 预警信息

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `warning.py` | 气象灾害预警 | `--city` |

### 天文数据

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `astronomy_sun.py` | 日出日落时间 | `--location`, `--date` |
| `astronomy_moon.py` | 月相数据 | `--location`, `--date` |

### 分钟级预报

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `minutely_5m.py` | 5分钟级降水预报 | `--location` |

### 格点天气

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `grid_weather_now.py` | 格点实时天气 | `--location` (经度,纬度) |

### 地理信息

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `top_cities.py` | 热门城市列表 | `--number`, `--city-type` |
| `search_poi.py` | POI搜索 | `--location`, `--keyword`, `--poi-type` |

## 作为 Python 模块使用

如果你想直接在代码中使用,可以导入原始的 `skill.py`:

```python
from skill import (
    get_weather_now,
    get_weather,
    get_air_quality,
    get_indices,
    get_warning
)

# 查询实时天气
result = get_weather_now(city="北京")
print(f"当前温度: {result['now']['temp']}°C")

# 查询3天预报
result = get_weather(city="上海", days="3d")
for day in result['daily']:
    print(f"{day['fxDate']}: {day['textDay']}, {day['tempMin']}~{day['tempMax']}°C")
```

## 获取和风天气API

1. 访问 [和风天气开发者平台](https://dev.qweather.com/)
2. 注册账号并创建项目
3. 获取API KEY或配置JWT认证
4. 获取API主机地址(商业版为自定义域名)

## OpenClaw Skill 集成

此 Skill 完全符合 OpenClaw 标准:

- ✅ **SKILL.md** - 包含完整的 Frontmatter 元数据和使用说明
- ✅ **三层渐进式披露** - 元数据、主体内容、捆绑资源
- ✅ **可执行脚本** - 每个功能都有独立的可执行脚本
- ✅ **自然语言触发** - 支持自然语言描述触发条件
- ✅ **参数化执行** - 所有脚本支持命令行参数

### 安装到 OpenClaw

将此 Skill 安装到 OpenClaw:

```bash
# 复制 SKILL.md 到 OpenClaw 技能目录
cp SKILL.md ~/.openclaw/skills/hefeng-weather.md

# 或者复制整个项目
cp -r . ~/.openclaw/skills/hefeng-weather/
```

## 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `HEFENG_API_HOST` | ✅ | API主机地址 |
| `HEFENG_API_KEY` | ✅ | API KEY(推荐) |
| `HEFENG_PROJECT_ID` | ⚠️ | 项目ID(JWT认证) |
| `HEFENG_KEY_ID` | ⚠️ | 密钥ID(JWT认证) |
| `HEFENG_PRIVATE_KEY_PATH` | ⚠️ | 私钥文件路径(JWT认证) |

## 认证方式

### API KEY 认证(推荐)

```bash
python scripts/configure.py \
  --api-host "your-domain.qweatherapi.com" \
  --api-key "your_api_key"
```

### JWT 数字签名认证

```bash
python scripts/configure.py \
  --api-host "your-domain.qweatherapi.com" \
  --project-id "your_project_id" \
  --key-id "your_key_id" \
  --private-key-path "./ed25519-private.pem"
```

## 依赖

- Python >= 3.11
- httpx >= 0.25.0
- pyjwt >= 2.8.0 (可选,JWT认证)
- cryptography >= 41.0.0 (可选,JWT认证)
- python-dotenv >= 1.0.0

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!

## 参考资料

- [和风天气官方文档](https://dev.qweather.com/docs/)
- [和风天气API参考](https://dev.qweather.com/docs/api/)
- [OpenClaw 技能规范](https://openclaw.dev/skills)
