# WeatherSkill - v2.0

**P0 + P1 Features Complete / P0 + P1 功能已完成**

## Overview / 概述

WeatherSkill v2.0 is a complete rewrite of the weather skill with:
- P0 features: Dual API fallback, AQI, Pollen, Alerts, Bilingual support
- P1 features: Lifestyle suggestions, Multi-city comparison, Smart location

天气技能 v2.0 是完整的重写，包含：
- P0 功能：双重 API 备份、空气质量、花粉、预警、双语支持
- P1 功能：生活建议、多城市对比、智能定位

## Architecture / 架构

```
WeatherSkill v2.0/
├── lib/
│   ├── api.js          # API wrappers
│   │   ├── WttrAPI     # wttr.in API
│   │   ├── OpenMeteoAPI # Open-Meteo API
│   │   ├── WAQIAPI     # Air Quality API
│   │   ├── PollenAPI   # Pollen API
│   │   └── AlertsAPI   # Weather alerts API
│   │
│   ├── formatter.js    # Output formatters (text/table/json)
│   ├── suggestions.js  # Lifestyle suggestions engine
│   └── client.js       # Main client
│
├── weather.js          # CLI entry point
├── tests/              # Test suite
├── SKILL.md            # Skill definition
├── README.md           # User guide
└── CHANGELOG.md        # Changelog
```

## Features / 功能

### P0 Features / P0 功能

1. **Dual API Fallback** / 双重 API 备份
   - Primary: wttr.in
   - Fallback: Open-Meteo
   - Automatic failover on API failure

2. **Air Quality (AQI)** / 空气质量
   - PM2.5, PM10, O₃, NO₂, SO₂, CO
   - AQI level and category
   - Quality description

3. **Pollen Data** / 花粉数据
   - Tree, Grass, Ragweed, Mold pollen
   - Risk levels (Low/Medium/High/Very High)

4. **Extreme Weather Alerts** / 极端天气预警
   - Warnings, Advisory, Watch
   - Rain/Snow/Thunderstorm alerts

5. **Bilingual Support** / 双语支持
   - Chinese/English output
   - Auto-detection or manual selection

### P1 Features / P1 功能

1. **Lifestyle Suggestions** / 生活建议
   - Clothing recommendation
   - Car wash suggestion
   - Exercise recommendation
   - Allergy advice
   - UV index advice
   - Rain probability advice

2. **Multi-City Comparison** / 多城市对比
   - Compare up to 10 cities
   - Hottest/Coldest/Wettest/Windiest highlights

3. **Smart Location** / 智能定位
   - Chinese city names (北京, 上海)
   - English city names (Beijing, Shanghai)
   - Airport codes (JFK, LAX)
   - Coordinates (39.9042,116.4074)

## Usage / 使用

### CLI / 命令行

```bash
# Basic usage
weather Beijing

# With all data
weather Beijing --aqi --pollen --alerts --advice

# Multi-city comparison
weather --compare "Beijing,Shanghai,Guangzhou"

# Output formats
weather Beijing --format table
weather Beijing --format json

# Language selection
weather Beijing --lang zh
weather Beijing --lang en
```

### API / API

```javascript
const { WeatherClient } = require('weather');

const client = new WeatherClient();

// Get weather for a city
const weather = await client.getWeather('Beijing', {
  aqi: true,
  pollen: true,
  alerts: true
});

// Get multiple cities
const cities = await client.getMultipleWeather(['Beijing', 'Shanghai']);

// Compare cities
const comparison = await client.compareWeather(['Beijing', 'Shanghai', 'Guangzhou']);
```

## Testing / 测试

```bash
cd /opt/homebrew/lib/node_modules/openclaw/skills/weather
npm test
```

Test coverage: 30+ test cases across 9 test suites.

测试覆盖：9 个测试套件，30+ 测试用例。

## Contributing / 贡献

Contributions welcome! Please follow:
- Code style: ESLint + Prettier
- Tests: Vitest
- Documentation: Update SKILL.md and README.md

欢迎贡献！请遵循：
- 代码风格：ESLint + Prettier
- 测试：Vitest
- 文档：更新 SKILL.md 和 README.md

## License / 许可证

MIT
