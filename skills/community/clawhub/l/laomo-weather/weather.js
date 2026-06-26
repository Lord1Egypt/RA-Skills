/**
 * Weather Skill - CLI Entry Point
 * Usage: node weather.js [options]
 */

const WeatherSkill = require('./lib/client');

// Parse command line arguments
function parseArgs(args) {
  const params = {
    location: null,
    lang: 'auto',
    format: 'text',
    aqi: false,
    pollen: false,
    alerts: false,
    advice: false,
    compare: null,
    help: false,
    version: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    switch (arg) {
      case '-h':
      case '--help':
        params.help = true;
        break;
      case '-v':
      case '--version':
        params.version = true;
        break;
      case '-l':
      case '--location':
        params.location = args[++i];
        break;
      case '--lang':
        params.lang = args[++i];
        break;
      case '--format':
        params.format = args[++i];
        break;
      case '--aqi':
        params.aqi = true;
        break;
      case '--pollen':
        params.pollen = true;
        break;
      case '--alerts':
        params.alerts = true;
        break;
      case '--advice':
      case '--advice':
        params.advice = true;
        break;
      case '--compare':
        params.compare = args[++i];
        break;
      default:
        // Positional argument is the location
        if (!params.location && !arg.startsWith('-')) {
          params.location = arg;
        }
        break;
    }
  }

  return params;
}

// Show help
function showHelp() {
  const help = `
🎤 weather - Get current weather and forecasts (v2.0)

📍 Usage / 使用方法:
  node weather.js <city> [options]
  node weather.js -l <city> [options]

🔍 Options / 选项:
  -l, --location <city>    City name / 城市名称
  --lang <zh|en|auto>      Language / 语言 (default: auto)
  --format <text|table|json>  Output format / 输出格式 (default: text)
  --aqi                    Include air quality data / 包含空气质量
  --pollen                 Include pollen data / 包含花粉数据
  --alerts                 Include weather alerts / 包含天气预警
  --advice                 Include lifestyle suggestions / 包含生活建议
  --compare <cities>       Compare multiple cities (comma-separated) / 多城市对比
  -h, --help               Show this help / 显示帮助
  -v, --version            Show version / 显示版本

✅ P0 Features (完成):
  ✓ Dual API fallback (wttr.in + Open-Meteo)
  ✓ Air quality (WAQI API)
  ✓ Pollen data (Pollen.com)
  ✓ Extreme weather alerts
  ✓ Bilingual support (Chinese/English)

✅ P1 Features (完成):
  ✓ Lifestyle suggestions engine
  ✓ Multi-city comparison
  ✓ Smart location recognition

📚 Examples / 示例:
  # Current weather / 当前天气
  node weather.js Beijing
  node weather.js 北京

  # Full forecast with all data / 完整预报
  node weather.js Beijing --aqi --pollen --alerts --advice

  # Multi-city comparison / 多城市对比
  node weather.js --compare "Beijing,Shanghai,Guangzhou" --aqi

  # Output in table format / 表格输出
  node weather.js Beijing --format table

  # Output in JSON format / JSON 输出
  node weather.js Beijing --format json --aqi

📝 Notes / 注意:
  - No API key required for most features / 大部分功能无需 API Key
  - Support for Chinese and English cities / 支持中英文城市名
  - Automatic language detection / 自动语言检测

`;
  console.log(help);
}

// Show version
function showVersion() {
  console.log('weather-cli v2.0.0');
}

// Main entry point
async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  // Handle special cases
  if (params.help) {
    showHelp();
    process.exit(0);
  }

  if (params.version) {
    showVersion();
    process.exit(0);
  }

  // Check for location (required unless comparing)
  if (!params.location && !params.compare) {
    console.error('❌ Error / 错误: No city specified / 未指定城市');
    console.error('Usage: node weather.js <city> [--options]');
    console.error('使用方法: node weather.js <城市> [--选项]');
    process.exit(1);
  }

  try {
    const skill = new WeatherSkill();
    const result = await skill.weather(params);
    console.log(result);
  } catch (error) {
    console.error(`❌ Error / 错误: ${error.message}`);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = { WeatherSkill, parseArgs };
