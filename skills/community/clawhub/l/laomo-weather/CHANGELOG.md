# Weather Skill - v2.0 Change Log / 天气技能 v2.0 变更日志

## v2.0.0 (2026-03-15) - P0+P1 Complete / 完成

### ✅ P0 Features (基础功能)

| Feature / 功能 | Description / 描述 | Status / 状态 |
|---------------|------------------|---------------|
| Dual API Fallback | wttr.in + Open-Meteo fallback | ✅ Complete |
| Air Quality (WAQI) | PM2.5, AQI from WAQI API | ✅ Complete |
| Pollen Data | Tree/Grass/Ragweed/Mold pollen | ✅ Complete |
| Extreme Alerts | Rain/Snow/Thunderstorm warnings | ✅ Complete |
| Bilingual Support | Chinese/English output | ✅ Complete |

### ✅ P1 Features (高级功能)

| Feature / 功能 | Description / 描述 | Status / 状态 |
|---------------|------------------|---------------|
| Lifestyle Suggestions | Clothing/Exercise/Car Wash advice | ✅ Complete |
| Multi-City Comparison | Compare weather between cities | ✅ Complete |
| Smart Location | Automatic geocoding | ✅ Complete |

### 📁 New Files / 新文件

```
lib/
├── api.js              # API wrappers (wttr, open-meteo, waqi, pollen)
├── formatter.js        # Output formatters (text, table, json)
├── suggestions.js      # Lifestyle suggestions engine
└── client.js           # Main client combining all features

weather.js              # CLI entry point

tests/
├── test-weather.test.js # Test suite (Vite format)
├── fixtures/           # Test fixtures
└── README.md           # Test documentation

package.json
jest.config.js
.prettierrc
.eslintrc.js
```

### 📝 Updated Files / 更新文件

- `SKILL.md` - Complete rewrite with v2.0 features
- `README.md` - Complete user guide

### 🔧 Breaking Changes / 破坏性变更

- API structure changed from simple curl commands to JavaScript modules
- CLI interface changed from `weather <city>` to `node weather.js <city>`
- Output format enhanced with AQI, pollen, alerts, and suggestions

### 🐛 Bug Fixes / 修复

- Fixed location resolution for Chinese cities
- Fixed language detection for mixed input
- Improved error handling for API failures

### 📚 Documentation / 文档

- Complete README with usage examples
- SKILL.md with P0+P1 feature documentation
- Test suite with comprehensive coverage

### 🎯 API Changes / API 变化

#### New Commands / 新命令

```bash
# AQI data
weather Beijing --aqi

# Pollen data  
weather Beijing --pollen

# Weather alerts
weather Beijing --alerts

# Lifestyle suggestions
weather Beijing --advice

# Multi-city comparison
weather --compare "Beijing,Shanghai,Guangzhou"

# Table output
weather Beijing --format table

# JSON output
weather Beijing --format json
```

## v1.0.0 (2024-01-01) - Initial Release

- Basic weather lookup via wttr.in
- Open-Meteo fallback
- Simple bilingual support

---

**Total Changes / 总变更**: 12 files added, 1 file updated, 1 breaking change
**Test Coverage / 测试覆盖**: 9 test suites, 30+ test cases
**Documentation / 文档**: 2 complete guides (SKILL.md + README.md)
