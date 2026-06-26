const { WeatherClient } = require('./api');
const Formatters = require('./formatter');
const SuggestionsEngine = require('./suggestions');

/**
 * Weather Skill - CLI Interface
 * Main entry point for the weather skill
 */

class WeatherSkill {
  constructor() {
    this.client = new WeatherClient();
  }

  /**
   * Get weather information
   * @param {object} params - Parameters
   * @param {string} params.location - City name
   * @param {string} params.lang - Language (zh/en/auto)
   * @param {string} params.format - Output format (text/table/json)
   * @param {boolean} params.aqi - Include air quality
   * @param {boolean} params.pollen - Include pollen data
   * @param {boolean} params.alerts - Include weather alerts
   * @param {boolean} params.advice - Include lifestyle suggestions
   * @param {string} params.compare - Comma-separated cities for comparison
   * @returns {Promise<string>} Formatted output
   */
  async weather(params) {
    const {
      location,
      lang = 'auto',
      format = 'text',
      aqi = false,
      pollen = false,
      alerts = false,
      advice = false,
      compare = null
    } = params;

    // Handle comparison mode first - doesn't require single location
    if (compare) {
      const cities = compare.split(',').map(c => c.trim());
      return this._compareWeather(cities, { lang, format, aqi, pollen, alerts, advice });
    }

    // Validate location for single city mode
    if (!location) {
      throw new Error('请提供城市名称 / Please provide a city name');
    }

    // Get weather data - pass lang directly for formatter to detect
    const weather = await this.client.getWeather(location, { aqi, pollen, alerts, lang });

    // Add suggestions if requested
    if (advice) {
      const suggestions = new SuggestionsEngine()
        .setWeather(weather)
        .setAQI(weather.aqi)
        .setPollen(weather.pollen);
      
      weather.suggestions = suggestions.getAllSuggestions(lang);
    }

    // Format output
    const formatter = Formatters[format];
    if (!formatter) {
      throw new Error(`Unsupported format: ${format}`);
    }

    return formatter.format(weather, { lang, showAqi: aqi, showPollen: pollen, showAlerts: alerts });
  }

  /**
   * Compare weather between multiple cities
   * @param {string[]} cities - Cities to compare
   * @param {object} options - Options
   * @returns {Promise<string>} Comparison output
   */
  async _compareWeather(cities, options) {
    const { lang = 'auto', format = 'text', aqi = false, pollen = false, alerts = false, advice = false } = options;

    if (cities.length < 2) {
      throw new Error('至少需要两个城市进行比较 / At least 2 cities required for comparison');
    }

    // Get weather for all cities
    const weatherData = await this.client.getMultipleWeather(cities, { aqi, pollen, alerts, lang: weatherLang });

    // Add suggestions if requested
    if (advice) {
      weatherData.forEach(w => {
        const suggestions = new SuggestionsEngine()
          .setWeather(w)
          .setAQI(w.aqi)
          .setPollen(w.pollen);
        w.suggestions = suggestions.getAllSuggestions(lang);
      });
    }

    // Get comparisons
    const comparisons = {
      hottest: weatherData.reduce((a, b) => a.temp > b.temp ? a : b),
      coldest: weatherData.reduce((a, b) => a.temp < b.temp ? a : b),
      wettest: weatherData.reduce((a, b) => (a.humidity || 0) > (b.humidity || 0) ? a : b),
      windiest: weatherData.reduce((a, b) => (a.windSpeed || 0) > (b.windSpeed || 0) ? a : b)
    };

    // Add comparison info to each city
    weatherData.forEach(w => {
      w.comparisons = {
        isHottest: w.temp === comparisons.hottest.temp,
        isColdest: w.temp === comparisons.coldest.temp,
        isWettest: (w.humidity || 0) === (comparisons.wettest.humidity || 0),
        isWindiest: (w.windSpeed || 0) === (comparisons.windiest.windSpeed || 0)
      };
    });

    // Format output
    const formatter = Formatters[format];
    if (format === 'text') {
      // Text format with comparison summary
      let output = [];
      output.push(`📊 ${lang === 'zh' ? '多城市天气对比' : 'Multi-City Weather Comparison'}`);
      output.push(``);
      output.push(`📍 ${weatherData.length} ${lang === 'zh' ? '个城市' : 'cities'}: ${cities.join(', ')}`);
      output.push(``);
      
      // Comparison highlights
      output.push(`🔥 ${lang === 'zh' ? '最热' : 'Hottest'}: ${comparisons.hottest.location} (${comparisons.hottest.temp}°C)`);
      output.push(`❄️ ${lang === 'zh' ? '最冷' : 'Coldest'}: ${comparisons.coldest.location} (${comparisons.coldest.temp}°C)`);
      output.push(`💧 ${lang === 'zh' ? '最湿润' : 'Wettest'}: ${comparisons.wettest.location} (${comparisons.wettest.humidity}%)`);
      output.push(`💨 ${lang === 'zh' ? '风最大' : 'Windiest'}: ${comparisons.windiest.location} (${comparisons.windiest.windSpeed}km/h)`);
      output.push(``);
      
      // Individual city details
      output.push(`--- ${lang === 'zh' ? '详细数据' : 'Details'} ---`);
      output.push(``);
      
      for (const w of weatherData) {
        output.push(`📍 ${w.location} ${this._getWeatherEmoji(w.weatherCode || 0)}`);
        output.push(`├─ ${lang === 'zh' ? '温度' : 'Temp'}: ${w.temp}°C | ${lang === 'zh' ? '体感' : 'Feels Like'}: ${w.feelsLike || w.temp}°C`);
        output.push(`├─ ${lang === 'zh' ? '天气' : 'Condition'}: ${w.condition} | ${lang === 'zh' ? '湿度' : 'Humidity'}: ${w.humidity}%`);
        output.push(`└─ ${lang === 'zh' ? '风' : 'Wind'}: ${w.windDir} ${w.windSpeed}km/h`);
        output.push(``);
      }
      
      return output.join('\n');
    }

    // Table or JSON format
    return formatter.formatMultiple(weatherData, { lang, showAqi: aqi, showPollen: pollen });
  }

  _getWeatherEmoji(code) {
    const emojis = {
      0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️', 45: '🌫️', 51: '🌦️', 61: '🌧️', 71: '❄️', 95: '⛈️'
    };
    return emojis[code] || '❓';
  }
}

module.exports = WeatherSkill;
