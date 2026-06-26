/**
 * Weather Skill - README.md
 * Complete user guide for weather-cli v2.0
 */

const README = `# 🌤️ Weather Skill - 天气技能

Get current weather and forecasts (v2.0)
获取当前天气状况和预报

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

```bash
# The skill is pre-installed with OpenClaw
# 技能已随 OpenClaw 预装
```

### Basic Usage / 基本用法

```bash
# Get current weather / 获取当前天气
weather Beijing
天气 北京

# Multiple cities / 多城市
weather --compare "Beijing,Shanghai,Guangzhou"
```

### Full Features / 完整功能

```bash
# Weather with AQI and suggestions / 天气+空气质量+建议
weather Beijing --aqi --advice

# Weather with pollen data / 天气+花粉数据
weather Beijing --pollen

# Weather with alerts / 天气+预警
weather Beijing --alerts

# Full forecast / 完整预报
weather Beijing --aqi --pollen --alerts --advice
```

---

## 📋 Feature List / 功能列表

### ✅ P0 Features (基础功能 - 完成)

| Feature / 功能 | Description / 描述 | Command / 命令 |
|---------------|------------------|---------------|
| Dual API Fallback | wttr.in + Open-Meteo fallback | Automatic |
| Air Quality (AQI) | PM2.5, AQI from Open-Meteo Air Quality API (FREE) | `--aqi` |
| Pollen Data | Tree/Grass/Ragweed pollen from Open-Meteo | `--pollen` |
| Extreme Weather Alerts | Rain/Snow/Thunderstorm warnings from Open-Meteo | `--alerts` |
| Bilingual Support | Chinese/English output | `--lang zh/en/auto` |

### ✅ P1 Features (高级功能 - 完成)

| Feature / 功能 | Description / 描述 | Command / 命令 |
|---------------|------------------|---------------|
| Lifestyle Suggestions | Clothing/Exercise/Car Wash advice | `--advice` |
| Multi-City Comparison | Compare weather between cities | `--compare "Beijing,Shanghai"` |
| Smart Location Recognition | City name/Airport/Coordinates | Automatic |

**Note**: All APIs are completely free! No paid APIs, no API keys required! / 注意：所有 API 完全免费！无付费 API，无需 API Key！

---

## 📖 Usage Guide / 使用指南

### Single City Query / 单城市查询

```bash
# English city name / 英文城市名
weather London

# Chinese city name / 中文城市名
weather 北京

# Airport code / 机场代码
weather JFK

# Coordinates / 坐标
weather "39.9042,116.4074"
```

### Multiple Cities Comparison / 多城市对比

```bash
# Three cities / 三个城市
weather --compare "Beijing,Shanghai,Guangzhou"

# With AQI / 带空气质量
weather --compare "Beijing,Shanghai" --aqi

# With advice / 带建议
weather --compare "Beijing,Shanghai,Shenzhen" --advice
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

### All Data / 完整数据

```bash
weather Beijing --aqi --pollen --alerts --advice
```

---

## 🌟 Feature Details / 功能详解

### 📊 Air Quality (AQI) / 空气质量

Get real-time air quality data including PM2.5, PM10, O₃, NO₂, SO₂, CO.

获取实时空气质量数据，包括 PM2.5、PM10、O₃、NO₂、SO₂、CO。

```bash
weather Beijing --aqi
```

Output example / 输出示例:
```
📊 空气质量: 75 (良)
   PM2.5: 45 | PM10: 65
   O₃: 85 | NO₂: 35
```

### 🌸 Pollen Index / 花粉指数

Track tree, grass, ragweed, and mold pollen levels.

追踪树木、草、豚草和霉菌花粉水平。

```bash
weather Beijing --pollen
```

Output example / 输出示例:
```
🌸 花粉指数
   🌳 Tree: 4.5 (High)
   🌿 Grass: 3.2 (Medium)
   🌼 Ragweed: 2.8 (Medium)
   🍄 Mold: 1.5 (Low)
```

### ⚠️ Extreme Weather Alerts / 极端天气预警

Get warnings for severe weather conditions.

获取恶劣天气预警。

```bash
weather Beijing --alerts
```

Output example / 输出示例:
```
⚠️ 天气预警
   ⚠️ Heavy Rain Warning
   ℹ️ Heat Advisory
```

### 💡 Lifestyle Suggestions / 生活建议

Smart recommendations for clothing, exercise, car wash, and allergies.

智能推荐穿衣、运动、洗车和过敏建议。

```bash
weather Beijing --advice
```

Output example / 输出示例:
```
👕 穿衣建议: 穿短袖、短裤
🚗 洗车建议: 适合洗车
🏃 运动建议: 适合户外运动
🌸 过敏建议: 花粉风险中等，敏感人群注意
```

### 📈 Multi-City Comparison / 多城市对比

Compare weather between multiple cities with highlights.

多城市对比天气，包含亮点信息。

```bash
weather --compare "Beijing,Shanghai,Guangzhou"
```

Output example / 输出示例:
```
📊 多城市天气对比

📍 3 个城市: Beijing, Shanghai, Guangzhou

🔥 最热: Guangzhou (32°C)
❄️ 最冷: Beijing (25°C)
💧 最湿润: Shanghai (85%)
💨 风最大: Beijing (15km/h)
```

---

## 🎨 Output Examples / 输出示例

### Text Format (default) / 文本格式（默认）

```
📍 北京 ☀️
├─ 温度: 25°C | 体感: 27°C
├─ 天气: 晴 | 湿度: 60%
└─ 风: 北 5km/h
```

### Table Format / 表格格式

```
┌─────┬─────────────────────────────────────────────────┐
│ 城市       │ 温度         | 天气             | 湿度       │
├─────┼─────────────────────────────────────────────────┤
│ ☀️ 北京      │ 25°C   | 晴            | 60% │
│ 🌤️ 上海      │ 28°C   | 多云          | 70% │
└─────┴─────────────────────────────────────────────────┘
```

### JSON Format / JSON 格式

```json
{
  "location": "Beijing",
  "temp": 25,
  "feelsLike": 27,
  "condition": "Sunny",
  "humidity": 60,
  "windSpeed": 5,
  "windDir": "N",
  "aqi": {
    "aqi": 75,
    "quality": "Good"
  },
  "suggestions": {
    "clothing": "Wear short sleeves and shorts",
    "carWash": " suitable for car wash",
    "exercise": " suitable for outdoor exercise"
  }
}
```

---

## 📝 Command Reference / 命令参考

### Options / 选项

| Option / 选项 | Description / 描述 | Default / 默认值 |
|--------------|------------------|----------------|
| `-l, --location <city>` | City name / 城市名称 | - |
| `--lang <zh\|en\|auto>` | Language / 语言 | auto |
| `--format <text\|table\|json>` | Output format / 输出格式 | text |
| `--aqi` | Include air quality / 包含空气质量 | false |
| `--pollen` | Include pollen data / 包含花粉数据 | false |
| `--alerts` | Include weather alerts / 包含天气预警 | false |
| `--advice` | Include lifestyle suggestions / 包含生活建议 | false |
| `--compare <cities>` | Compare multiple cities / 多城市对比 | - |
| `-h, --help` | Show help / 显示帮助 | - |
| `-v, --version` | Show version / 显示版本 | - |

---

## 🔧 Troubleshooting / 故障排除

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

## 📊 API and Limits / API 和限制

| API / API | Free Limit / 免费限制 | Notes / 说明 |
|----------|---------------------|------------|
| wttr.in | 250/day | Main weather source / 主天气源 |
| Open-Meteo | 10,000/day | Fallback weather / 备用天气 |
| WAQI (AQI) | 1,000/day | Air quality / 空气质量 |
| Pollen.com | Unlimited | Pollen data / 花粉数据 |

**Note**: No API key required for most features! / 注意: 大部分功能无需 API Key!

---

## 🌍 Supported Cities / 支持城市

We support cities worldwide! This includes:

我们支持全球城市！包括:

- 🇨🇳 China: Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu, etc. / 中国: 北京、上海、广州、深圳、成都等
- 🇺🇸 USA: New York, Los Angeles, Chicago, etc. / 美国: 纽约、洛杉矶、芝加哥等
- 🇬🇧 UK: London, Manchester, etc. / 英国: 伦敦、曼彻斯特等
- 🇯🇵 Japan: Tokyo, Osaka, etc. / 日本: 东京、大阪等
- 🇫🇷 France: Paris, Lyon, etc. / 法国: 巴黎、里昂等
- 🇩🇪 Germany: Berlin, Munich, etc. / 德国: 柏林、慕尼黑等
- And 1000+ more cities! / 还有 1000+ 个城市！

**Add a city?** / 添加城市?
If a city is missing, try / 如果缺少城市，请尝试:
- English name / 英文名称
- Coordinates / 坐标: "lat,lng"

---

## 🎯 Best Practices / 最佳实践

### For Daily Weather Check / 日常天气查询

```bash
weather Beijing --aqi --advice
```

This gives you / 这会给你:
- Current weather / 当前天气
- Air quality / 空气质量
- Lifestyle suggestions / 生活建议

### For Travel Planning / 旅行规划

```bash
weather --compare "Beijing,Shanghai,Guangzhou" --aqi --advice
```

This helps you / 这会帮你:
- Compare weather between cities / 比较城市天气
- Check air quality / 检查空气质量
- Get advice for each city / 获取每个城市的建议

### For Allergy Sufferers / 过敏患者

```bash
weather Beijing --pollen --advice
```

This shows you / 这会显示:
- Pollen levels for all types / 所有类型的花粉水平
- Allergy risk / 过敏风险
- Management suggestions / 管理建议

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

### Example 2: Multi-City / 示例 2: 多城市

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
| 🌤️ 上海      │ 28°C   | 60 (良) │ 70% │
│ 🌧️ 广州      │ 32°C   | 55 (优) │ 85% │
└─────┴─────────────────────────────────────────────────┘
```

### Example 3: Compare with All Data / 示例 3: 完整数据对比

```bash
$ weather --compare "Beijing,Shanghai" --aqi --pollen --alerts --advice

📊 多城市天气对比

📍 2 个城市: Beijing, Shanghai

... (comparison highlights) ...

✅ Beijing:🌞 ℃ | 📊 AQI: 75(良) | 🌸 Pollen: Medium | ✅)!
✅ Shanghai:🌤️ ℃ | 📊 AQI: 60(良) | 🌸 Pollen: Low | ✅)!
```

---

## 🤝 Contributing / 贡献

This skill is maintained by / 这个技能由 OpenClaw 社区维护.

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
- **All APIs above are completely free with no API key required!** / 以上所有 API 完全免费且无需 API Key！

---

**Made with ❤️ by OpenClaw Community** / 由 OpenClaw 社区用 ❤️ 制作

`;

module.exports = README;
