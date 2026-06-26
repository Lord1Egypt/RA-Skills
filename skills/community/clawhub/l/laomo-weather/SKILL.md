---
name: laomo-weather
slug: laomo-weather
description: "老默天气 - 支持 AQI/花粉/预警/生活建议，中英双语输出，多城市对比。v2.1 完全免费 API。"
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
---

# Weather Skill V2.0 / 天气技能 v2.0

**P0 + P1 Features Complete / P0 + P1 功能已完成**

Get current weather conditions, forecasts, AQI, pollen data, extreme weather alerts, and lifestyle suggestions. **Supports bilingual (Chinese/English) output with full translation of conditions and AQI descriptions.**

获取当前天气状况、预报、空气质量、花粉数据、极端天气预警和生活建议。**支持中英双语输出，天气状况和空气质量完全翻译。**

## When to Use / 使用场景

✅ **USE this skill when: / 使用此技能：**

- "What's the weather?" / "天气怎么样？"
- "Will it rain today/tomorrow?" / "今天/明天会下雨吗？"
- "Temperature in [city]" / "[城市] 的温度"
- "Weather forecast for the week" / "本周天气预报"
- "Air quality in [city]" / "[城市] 的空气质量"
- "Pollen levels" / "花粉指数"
- "Weather alerts" / "天气预警"
- "Lifestyle suggestions" / "生活建议"
- "Compare weather between cities" / "多城市天气对比"
- Travel planning weather checks / 旅行计划天气查询
- Allergy sufferers checking pollen / 过敏患者查询花粉

❌ **DON'T use this skill when: / 不要使用：**

- Historical weather data → use weather archives/APIs / 历史天气数据
- Climate analysis or trends → use specialized data sources / 气候分析或趋势
- Hyper-local microclimate data → use local sensors / 超本地微气候数据
- Aviation/marine weather → use specialized services (METAR, etc.) / 航空/海洋天气

---

## ✅ Feature Highlights / 功能亮点

### P0 Features (基础功能 - 已完成)

| Feature / 功能 | Description / 描述 | Command / 命令 |
|---------------|------------------|---------------|
| 🔄 Dual API Fallback | wttr.in + Open-Meteo fallback for reliability / wttr.in + Open-Meteo 双重 API 确保稳定性 | Automatic / 自动 |
| 📊 Air Quality (AQI) | PM2.5, AQI from Open-Meteo Air Quality API (FREE) / PM2.5、AQI 数据（Open-Meteo 空气质量 API，免费） | `--aqi` |
| 🌸 Pollen Data | Tree/Grass/Ragweed/Mold pollen levels / 树木/草/豚草/霉菌花粉数据 | `--pollen` |
| ⚠️ Extreme Alerts | Rain/Snow/Thunderstorm warnings / 雨/雪/雷暴预警 | `--alerts` |
| 🌍 Bilingual Support | Chinese/English output / 中英文输出 | `--lang zh/en/auto` |
| 💡 Free All APIs | No paid APIs, fully free service / 全部免费 API，无付费服务 | Free / 免费 |

### P1 Features (高级功能 - 已完成)

| Feature / 功能 | Description / 描述 | Command / 命令 |
|---------------|------------------|---------------|
| 💡 Lifestyle Suggestions | Clothing/Exercise/Car Wash/Allergy advice / 穿衣/运动/洗车/过敏建议 | `--advice` |
| 📈 Multi-City Comparison | Compare weather between cities with highlights / 多城市对比天气（带亮点） | `--compare "Beijing,Shanghai"` |
| 🗺️ Smart Location | City name/Airport/Coordinates with automatic geocoding / 城市名/机场/坐标自动地理编码 | Automatic / 自动 |

---

## 📝 Usage Guide / 使用指南

### Basic Commands / 基本命令

```bash
# Current weather / 当前天气
weather Beijing
天气 北京

# With all data / 完整数据
weather Beijing --aqi --pollen --alerts --advice

# Multi-city comparison / 多城市对比
weather --compare "Beijing,Shanghai,Guangzhou"
```

### Full Feature Examples / 完整功能示例

```bash
# Weather with AQI and lifestyle suggestions / 天气+空气质量+建议
weather Beijing --aqi --advice

# Weather with pollen data / 天气+花粉数据
weather Beijing --pollen

# Weather with extreme alerts / 天气+预警
weather Beijing --alerts

# Compare three cities with all data / 三个城市完整对比
weather --compare "Beijing,Shanghai,Guangzhou" --aqi --pollen --alerts --advice
```

### Output Formats / 输出格式

```bash
# Text format (default) / 文本格式（默认）
weather Beijing

# Table format / 表格格式
weather Beijing --format table

# JSON format / JSON 格式
weather Beijing --format json --aqi
```

### Language Options / 语言选项

```bash
# Auto-detect (default) / 自动检测（默认）
weather Beijing --lang auto

# Force Chinese / 强制中文
weather Beijing --lang zh

# Force English / 强制英文
weather Beijing --lang en
```

---

## 📊 API and Limits / API 和限制

| API / API | Free Limit / 免费限制 | Notes / 说明 |
|----------|---------------------|------------|
| wttr.in | 250/day | Main weather source / 主天气源 |
| Open-Meteo | Unlimited | Complete weather suite / 完整天气服务（免费） |
| Open-Meteo Air Quality | Unlimited | Free air quality API / 免费空气质量 API |
| Open-Meteo Pollen | Unlimited | Free pollen API / 免费花粉 API |
| Open-Meteo Alerts | Unlimited | Free weather alerts / 免费天气预警 |

**Note**: All APIs are completely free with no API key required! / 注意: 所有 API 完全免费且无需 API Key！

---

## 🌍 Supported Cities / 支持城市

We support cities worldwide! Key examples:

我们支持全球城市！主要城市：

- 🇨🇳 China / 中国: Beijing (北京), Shanghai (上海), Guangzhou (广州), Shenzhen (深圳), Chengdu (成都)
- 🇺🇸 USA / 美国: New York (纽约), Los Angeles (洛杉矶), Chicago (芝加哥)
- 🇬🇧 UK / 英国: London (伦敦), Manchester (曼彻斯特)
- 🇯🇵 Japan / 日本: Tokyo (东京), Osaka (大阪)
- 🇫🇷 France / 法国: Paris (巴黎), Lyon (里昂)
- 🇩🇪 Germany / 德国: Berlin (柏林), Munich (慕尼黑)
- And 1000+ more cities! / 还有 1000+ 个城市！

**Add a city? / 添加城市**:
- English name / 英文名称
- Chinese name / 中文名称
- Coordinates / 坐标: "lat,lng" (e.g., "39.9042,116.4074")

---

## 🎯 Best Practices / 最佳实践

### Daily Weather Check / 日常天气查询

```bash
weather Beijing --aqi --advice
```

This gives you: / 这会给你:
- Current weather / 当前天气
- Air quality / 空气质量
- Lifestyle suggestions / 生活建议

### Travel Planning / 旅行规划

```bash
weather --compare "Beijing,Shanghai,Guangzhou" --aqi --advice
```

This helps you: / 这会帮你:
- Compare weather between cities / 比较城市天气
- Check air quality / 检查空气质量
- Get advice for each city / 获取每个城市的建议

### Allergy Sufferers / 过敏患者

```bash
weather Beijing --pollen --advice
```

This shows you: / 这会显示:
- Pollen levels for all types / 所有类型的花粉水平
- Allergy risk / 过敏风险
- Management suggestions / 管理建议

---

## 🔧 Implementation Details / 实现细节

### Architecture / 架构

```
weather-v2.0/
├── lib/
│   ├── api.js          # API wrappers (wttr, open-meteo, waqi, pollen, alerts)
│   ├── formatter.js    # Output formatters (text, table, json)
│   ├── suggestions.js  # Lifestyle suggestions engine
│   └── client.js       # Main client combining all features
├── weather.js          # CLI entry point
└── tests/              # Test suite
```

### Key Components / 核心组件

1. **WttrAPI**: Primary weather source (wttr.in)
2. **OpenMeteoAPI**: Fallback weather API (no key needed)
3. **WAQIAPI**: Air quality data (PM2.5, AQI)
4. **PollenAPI**: Pollen index data
5. **AlertsAPI**: Extreme weather warnings
6. **Geocoder**: Smart location recognition
7. **SuggestionsEngine**: Lifestyle recommendations
8. **Formatter**: Multi-format output (text/table/json)

### Language Detection / 语言检测

1. Check explicit `--lang` parameter first / 首先检查显式 `--lang` 参数
2. Detect query language (Chinese vs Latin characters) / 检测查询语言
3. Fall back to system locale / 回退到系统区域设置
4. Default to English if undetermined / 默认英文

### City Name Mapping / 城市名映射

```javascript
{
  "北京": { lat: 39.9042, lng: 116.4074, name: "Beijing" },
  "Shanghai": { lat: 31.2304, lng: 121.4737, name: "上海" },
  // ... 1000+ cities
}
```

### Output Templates / 输出模板

**Chinese Template / 中文模板:**
```
📍 {city}: {emoji} {temp}°C, {condition}, 湿度 {humidity}%
📊 空气质量: {aqi} ({quality})
🌸 花粉指数: {pollen}
 Clothing: {clothing}
Exercise: {exercise}
```

**English Template / 英文模板:**
```
📍 {city}: {emoji} {temp}°C, {condition}, {humidity}% humidity
📊 AQI: {aqi} ({quality})
🌸 Pollen: {pollen}
 Clothing: {clothing}
Exercise: {exercise}
```

---

## 📚 Examples / 示例

### Example 1: Daily Check / 示例 1: 日常查询

```bash
$ weather Beijing --aqi --advice

📍 北京 ☀️
├─ 温度: 25°C | 体感: 27°C
├─ 天气: 晴 | 湿度: 60%
└─ 风: 北 5km/h

📊 空气质量: 75 (良)
   PM2.5: 45 | PM10: 65

👕 穿衣建议: 穿短袖、短裤
🚗 洗车建议: 适合洗车
🏃 运动建议: 适合户外运动
🌸 过敏建议: 花粉风险低
```

### Example 2: Multi-City / 示例 2: 多城市对比

```bash
$ weather --compare "Beijing,Shanghai,Guangzhou" --aqi

📊 多城市天气对比

📍 3 个城市: Beijing, Shanghai, Guangzhou

🔥 最热: Guangzhou (32°C)
❄️ 最冷: Beijing (25°C)
💧 最湿润: Shanghai (85%)
💨 风最大: Beijing (15km/h)

┌─────┬─────────────────────────────────────────────────┐
│ 城市       │ 温度         | AQI     | 湿度       │
├─────┼─────────────────────────────────────────────────┤
│ ☀️ 北京      │ 25°C   | 75 (良) │ 60% │
│ 🌤️ 上海      │ 28°C   | 60 (良) │ 70% │
│ 🌧️ 广州      │ 32°C   | 55 (优) │ 85% │
└─────┴─────────────────────────────────────────────────┘
```

### Example 3: Full Features / 示例 3: 完整功能

```bash
$ weather Beijing --aqi --pollen --alerts --advice --format table

┌─────┬─────────────────────────────────────────────────┐
│ 北京       │ 温度         | AQI     | 湿度       │
├─────┼─────────────────────────────────────────────────┤
│ ☀️ Beijing  │ 25°C   | 75 (良) │ 60% │
└─────┴─────────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting / 故障排除

### City Not Found / 城市未找到

```
❌ Error: City not found: InvalidCity
```

**Solution / 解决方案**:
- Check city spelling / 检查城市拼写
- Try English name / 尝试英文名称
- Try coordinates / 尝试坐标: "39.9042,116.4074"

### AQI/data Unavailable / 空气质量数据不可用

```
📊 空气质量: N/A
```

**Solution / 解决方案**:
- Some APIs may not have data for all cities / 部分 API 可能没有所有城市数据
- Try a larger city / 尝试大城市
- Wait and retry / 稍后重试

### Rate Limiting / 限速

If you see frequent errors / 如果频繁出现错误:

- Wait a few minutes / 等待几分钟
- Reduce request frequency / 减少请求频率
- Check API status / 检查 API 状态

---

## 📖 Documentation / 文档

- **README.md**: Complete user guide / 完整用户指南
- **tests/test-weather.js**: Test suite / 测试用例
- **_meta.json**: Skill metadata / 技能元数据

---

## 🤝 Contributing / 贡献

This skill is maintained by the OpenClaw community / 这个技能由 OpenClaw 社区维护.

- **GitHub**: https://github.com/openclaw
- **Discord**: https://discord.gg/openclaw

Contributions welcome! / 欢迎贡献！

---

## 📄 License / 许可证

MIT License

---

## 🙏 Acknowledgments / 致谢

- **wttr.in** for weather data / 感谢 wttr.in 提供天气数据
- **Open-Meteo** for complete weather suite (weather, AQI, pollen, alerts) / 感谢 Open-Meteo 提供完整的天气套件（天气、空气质量、花粉、预警）
- **All APIs above are completely free with no API key required! / 以上所有 API 完全免费且无需 API Key！

---