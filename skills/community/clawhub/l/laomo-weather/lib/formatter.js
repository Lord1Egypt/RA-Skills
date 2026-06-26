/**
 * Formatter for weather output
 * Supports: text, table, json formats
 */

const AQIUtils = {
  getAQIDescription(aqi, lang = 'en') {
    const descriptions = {
      en: {
        good: 'Good',
        moderate: 'Moderate',
        usg: 'Unhealthy for Sensitive Groups',
        unhealthy: 'Unhealthy',
        veryUnhealthy: 'Very Unhealthy',
        hazardous: 'Hazardous'
      },
      zh: {
        good: '优',
        moderate: '良',
        usg: '敏感人群不适宜',
        unhealthy: '不健康',
        veryUnhealthy: '很不健康',
        hazardous: '危险'
      }
    };
    
    if (aqi <= 50) return descriptions[lang].good;
    if (aqi <= 100) return descriptions[lang].moderate;
    if (aqi <= 150) return descriptions[lang].usg;
    if (aqi <= 200) return descriptions[lang].unhealthy;
    if (aqi <= 300) return descriptions[lang].veryUnhealthy;
    return descriptions[lang].hazardous;
  },
  
  getQuality(aqi, lang = 'en') {
    const qualities = {
      en: {
        excellent: 'Excellent',
        good: 'Good',
        lightlyPolluted: 'Lightly Polluted',
        moderatelyPolluted: 'Moderately Polluted',
        heavilyPolluted: 'Heavily Polluted',
        severelyPolluted: 'Severely Polluted'
      },
      zh: {
        excellent: '优秀',
        good: '良好',
        lightlyPolluted: '轻度污染',
        moderatelyPolluted: '中度污染',
        heavilyPolluted: '重度污染',
        severelyPolluted: '严重污染'
      }
    };
    
    if (aqi <= 50) return qualities[lang].excellent;
    if (aqi <= 100) return qualities[lang].good;
    if (aqi <= 150) return qualities[lang].lightlyPolluted;
    if (aqi <= 200) return qualities[lang].moderatelyPolluted;
    if (aqi <= 300) return qualities[lang].heavilyPolluted;
    return qualities[lang].severelyPolluted;
  }
};

// Condition translations
const conditionTranslations = {
  'Clear sky': { en: 'Clear', zh: '晴' },
  'Mainly clear': { en: 'Mainly clear', zh: '主晴' },
  'Partly cloudy': { en: 'Partly cloudy', zh: '多云' },
  'Overcast': { en: 'Overcast', zh: '阴' },
  'Fog': { en: 'Fog', zh: '雾' },
  'Depositing rime fog': { en: 'Rime fog', zh: '冻雾' },
  'Light drizzle': { en: 'Light drizzle', zh: '小雨' },
  'Moderate drizzle': { en: 'Moderate drizzle', zh: '中雨' },
  'Dense drizzle': { en: 'Dense drizzle', zh: '大雨' },
  'Slight rain': { en: 'Slight rain', zh: '小雨' },
  'Moderate rain': { en: 'Moderate rain', zh: '中雨' },
  'Heavy rain': { en: 'Heavy rain', zh: '大雨' },
  'Slight snow': { en: 'Slight snow', zh: '小雪' },
  'Moderate snow': { en: 'Moderate snow', zh: '中雪' },
  'Heavy snow': { en: 'Heavy snow', zh: '大雪' },
  'Thunderstorm': { en: 'Thunderstorm', zh: '雷雨' },
  'Thunderstorm with hail': { en: 'Thunderstorm with hail', zh: '雷雹' },
  'Thunderstorm with heavy hail': { en: 'Thunderstorm with heavy hail', zh: '强雷雹' }
};

const Formatters = {
  text: {
    format(weather, options = {}) {
      const {
        lang = 'auto',
        showAqi = false,
        showPollen = false,
        showAlerts = false,
        showSuggestions = false
      } = options;

      const t = Translations[lang === 'auto' ? Formatters.text._detectLanguage(weather.location) : lang];

      let output = [];
      
      // Location header
      output.push(`📍 ${weather.location} ${Formatters.text._getWeatherEmoji(weather.weatherCode || 0)}`);
      
      // Current conditions
      const langForTranslation = lang === 'auto' ? Formatters.text._detectLanguage(weather.location) : lang;
      const conditionTranslated = Formatters.text._translateCondition(weather.condition, langForTranslation);
      output.push(`├─ ${t.temp}: ${weather.temp}°C | ${t.feelsLike}: ${weather.feelsLike || weather.temp}°C`);
      output.push(`├─ ${t.condition}: ${conditionTranslated} | ${t.humidity}: ${weather.humidity}%`);
      output.push(`└─ ${t.wind}: ${weather.windDir} ${weather.windSpeed}km/h`);
      
      // AQI
      if (showAqi && weather.aqi) {
        const aqi = weather.aqi;
        const aqiLang = lang === 'auto' ? Formatters.text._detectLanguage(weather.location) : lang;
        const aqiDesc = AQIUtils.getAQIDescription(aqi.aqi, aqiLang);
        output.push(``);
        output.push(`📊 ${t.aqi}: ${aqiDesc} (${aqi.aqi})`);
        output.push(`   PM2.5: ${aqi.pm25 || 'N/A'} | PM10: ${aqi.pm10 || 'N/A'}`);
        output.push(`   O₃: ${aqi.o3 || 'N/A'} | NO₂: ${aqi.no2 || 'N/A'} | CO: ${aqi.co || 'N/A'}`);
      }
      
      // Pollen
      if (showPollen && weather.pollen) {
        const p = weather.pollen;
        output.push(``);
        output.push(`🌸 ${t.pollen}`);
        output.push(`   🌳 Tree: ${p.treePollen.level || 'N/A'} (${p.treePollen.risk})`);
        output.push(`   🌿 Grass: ${p.grassPollen.level || 'N/A'} (${p.grassPollen.risk})`);
        output.push(`   🌼 Ragweed: ${p.ragweedPollen.level || 'N/A'} (${p.ragweedPollen.risk})`);
        output.push(`   🍄 Mold: ${p.moldPollen.level || 'N/A'} (${p.moldPollen.risk})`);
      }
      
      // Alerts
      if (showAlerts && weather.alerts) {
        const alerts = weather.alerts;
        if (alerts.warnings?.length > 0 || alerts.advisory?.length > 0) {
          output.push(``);
          output.push(`⚠️ ${t.alerts}`);
          alerts.warnings?.forEach(w => output.push(`   ⚠️ ${w}`));
          alerts.advisory?.forEach(a => output.push(`   ℹ️ ${a}`));
        }
      }
      
      return output.join('\n');
    },

    formatMultiple(weatherData, options = {}) {
      const {
        lang = 'auto',
        showAqi = false,
        showPollen = false
      } = options;

      const t = Translations[lang === 'auto' ? Formatters.text._detectLanguage(weatherData[0]?.location) : lang];

      let output = [];
      
      // Header
      output.push(`📍 ${weatherData.length} ${t.cities}`);
      output.push(``);
      
      // Table
      output.push(`┌─────────────────────────────────────────────────────────┐`);
      
      for (const weather of weatherData) {
        output.push(`│ ${Formatters.text._getWeatherEmoji(weather.weatherCode || 0)} ${weather.location}`);
        output.push(`│   ${t.temp}: ${weather.temp}°C | ${t.humidity}: ${weather.humidity}% | ${t.wind}: ${weather.windSpeed}km/h`);
        
        if (showAqi && weather.aqi) {
          const aqi = weather.aqi;
          const aqiLang = lang === 'auto' ? Formatters.text._detectLanguage(weather.location) : lang;
          const aqiDesc = AQIUtils.getAQIDescription(aqi.aqi, aqiLang);
          output.push(`│`);
          output.push(`│ 📊 ${t.aqi}: ${aqiDesc} (${aqi.aqi}) │`);
          output.push(`│   PM2.5: ${aqi.pm25 || 'N/A'} | PM10: ${aqi.pm10 || 'N/A'} │`);
        }
        
        if (showPollen && weather.pollen) {
          const overall = weather.pollen.overallIndex || 5;
          output.push(`│   🌸 Pollen: Level ${overall}`);
        }
        
        output.push(`└─────────────────────────────────────────────────────────┘`);
        output.push(``);
      }
      
      return output.join('\n');
    },

    _getWeatherEmoji(code) {
      const emojis = {
        0: '☀️',  // Clear sky
        1: '🌤️',  // Mainly clear
        2: '⛅',  // Partly cloudy
        3: '☁️',  // Overcast
        45: '🌫️', // Fog
        48: '🌫️', // Rime fog
        51: '🌦️', // Light drizzle
        53: '🌦️', // Moderate drizzle
        55: '🌧️', // Dense drizzle
        56: '🌧️', // Freezing drizzle
        57: '🌧️', // Dense freezing drizzle
        61: '🌧️', // Slight rain
        63: '🌧️', // Moderate rain
        65: '🌧️', // Heavy rain
        66: '🌧️', // Freezing rain
        67: '🌧️', // Heavy freezing rain
        71: '❄️', // Slight snow
        73: '❄️', // Moderate snow
        75: '❄️', // Heavy snow
        77: '❄️', // Snow grains
        80: '🌧️', // Slight rain showers
        81: '🌧️', // Moderate rain showers
        82: '🌧️', // Violent rain showers
        85: '❄️', // Slight snow showers
        86: '❄️', // Heavy snow showers
        95: '⛈️', // Thunderstorm
        96: '⛈️', // Thunderstorm with hail
        99: '⛈️'  // Thunderstorm with heavy hail
      };
      
      if (code === 'undefined' || code === undefined) return '❓';
      return emojis[Math.floor(code / 10) * 10] || '❓';
    },

    _detectLanguage(location) {
      if (/[\u4e00-\u9fa5]/.test(location)) return 'zh';
      return 'en';
    },

    _translateCondition(condition, lang) {
      if (!condition) return condition;
      
      // Trim the condition
      const trimmed = condition.trim();
      
      // If it's already in Chinese (contains Chinese characters), return as is
      if (/[\u4e00-\u9fa5]/.test(trimmed)) {
        return lang === 'zh' ? trimmed : trimmed;
      }
      
      // Translate from English to Chinese if needed
      if (lang === 'zh' && ConditionTranslations[trimmed]) {
        return ConditionTranslations[trimmed].zh;
      }
      
      // If lang is 'en' or translating failed, return English
      return trimmed;
    }
  },

  table: {
    format(weather, options = {}) {
      const {
        lang = 'auto',
        showAqi = false,
        showPollen = false
      } = options;

      const t = Translations[lang === 'auto' ? Formatters.table._detectLanguage(weather.location) : lang];

      let output = [];
      
      // Header
      output.push(`┌──── ${weather.location} ${Formatters.table._getWeatherEmoji(weather.weatherCode || 0)} ────┐`);
      
      const langForTranslation = lang === 'auto' ? Formatters.table._detectLanguage(weather.location) : lang;
      
      // Data rows
      output.push(`│ ${t.temp.padEnd(12)} ${weather.temp}°C | ${weather.feelsLike || weather.temp}°C │`);
      output.push(`│ ${t.humidity.padEnd(12)} ${weather.humidity}% │`);
      output.push(`│ ${t.wind.padEnd(12)} ${weather.windDir} ${weather.windSpeed}km/h │`);
      const conditionTranslated = Formatters.table._translateCondition(weather.condition, langForTranslation);
      output.push(`│ ${t.condition.padEnd(12)} ${conditionTranslated} │`);
      
      // AQI column
      if (showAqi && weather.aqi) {
        const aqi = weather.aqi;
        const aqiDesc = AQIUtils.getAQIDescription(aqi.aqi, langForTranslation);
        output.push(`│`);
        output.push(`│ 📊 ${t.aqi}: ${aqiDesc} (${aqi.aqi}) │`);
        output.push(`│   PM2.5: ${aqi.pm25 || 'N/A'} | PM10: ${aqi.pm10 || 'N/A'} │`);
      }
      
      // Pollen column
      if (showPollen && weather.pollen) {
        const p = weather.pollen;
        output.push(`│`);
        output.push(`│ 🌸 ${t.pollen} │`);
        output.push(`│   🌳 Tree: ${p.treePollen.level || 'N/A'} (${p.treePollen.risk}) │`);
        output.push(`│   🌿 Grass: ${p.grassPollen.level || 'N/A'} (${p.grassPollen.risk}) │`);
      }
      
      output.push(`└─────────────────────────────────────────────────┘`);
      
      return output.join('\n');
    },

    formatMultiple(weatherData, options = {}) {
      const {
        lang = 'auto'
      } = options;

      const t = Translations[lang === 'auto' ? Formatters.text._detectLanguage(weatherData[0]?.location) : lang];

      let output = [];
      
      // Column headers
      output.push(`┌─────┬─────────────────────────────────────────────────┐`);
      output.push(`│ ${t.city.padEnd(10)} │ ${t.temp.padEnd(8)} | ${t.condition.padEnd(12)} | ${t.humidity.padEnd(6)} │`);
      output.push(`├─────┼─────────────────────────────────────────────────┤`);
      
      for (const weather of weatherData) {
        const emoji = Formatters.table._getWeatherEmoji(weather.weatherCode || 0);
        const conditionTranslated = Formatters.text._translateCondition(weather.condition, langForTranslation);
        output.push(`│ ${emoji} ${weather.location.substring(0, 8).padEnd(10)} │ ${weather.temp}°C ${weather.temp >= 0 ? ' ' : ''} | ${conditionTranslated.substring(0, 10).padEnd(10)} | ${weather.humidity}% │`);
      }
      
      output.push(`└─────┴─────────────────────────────────────────────────┘`);
      
      return output.join('\n');
    },

    _getWeatherEmoji(code) {
      const emojis = {
        0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️', 45: '🌫️', 51: '🌦️', 61: '🌧️', 71: '❄️', 95: '⛈️'
      };
      return emojis[code] || '❓';
    },

    _detectLanguage(location) {
      if (/[\u4e00-\u9fa5]/.test(location)) return 'zh';
      return 'en';
    },

    _translateCondition(condition, lang) {
      if (!condition) return '';
      
      // Trim the condition for lookup
      const trimmed = condition.trim();
      const lower = trimmed.toLowerCase();
      
      // Use ConditionTranslations (with capital C) for lookup
      const conditionKey = Object.keys(ConditionTranslations).find(k => k.toLowerCase() === lower);
      if (conditionKey && ConditionTranslations[conditionKey]) {
        return lang === 'zh' ? ConditionTranslations[conditionKey].zh : ConditionTranslations[conditionKey].en;
      }
      
      // Simple direct mapping for Chinese conditions
      if (lang === 'zh') {
        if (lower.includes('晴')) return '晴';
        if (lower.includes('cloud')) return '多云';
        if (lower.includes('阴')) return '阴';
        if (lower.includes('fog')) return '雾';
        if (lower.includes('drizzle')) return '小雨';
        if (lower.includes('rain')) return '雨';
        if (lower.includes('snow')) return '雪';
        if (lower.includes('thunder')) return '雷雨';
      }
      
      // Return trimmed condition
      return trimmed;
    }
  },

  json: {
    format(weather, options = {}) {
      return JSON.stringify(weather, null, 2);
    },
    formatMultiple(weatherData, options = {}) {
      return JSON.stringify(weatherData, null, 2);
    }
  }
};

// Condition translations
const ConditionTranslations = {
  'Clear': { zh: '晴', en: 'Clear' },
  'Clear sky': { zh: '晴', en: 'Clear sky' },
  'Mainly clear': { zh: '晴间多云', en: 'Mainly clear' },
  'Partly cloudy': { zh: '多云', en: 'Partly cloudy' },
  'Overcast': { zh: '阴', en: 'Overcast' },
  'Fog': { zh: '雾', en: 'Fog' },
  'Depositing rime fog': { zh: '冻雾', en: 'Depositing rime fog' },
  'Light drizzle': { zh: '小雨', en: 'Light drizzle' },
  'Moderate drizzle': { zh: '中雨', en: 'Moderate drizzle' },
  'Dense drizzle': { zh: '大雨', en: 'Dense drizzle' },
  'Slight rain': { zh: '小雨', en: 'Slight rain' },
  'Moderate rain': { zh: '中雨', en: 'Moderate rain' },
  'Heavy rain': { zh: '大雨', en: 'Heavy rain' },
  'Slight snow': { zh: '小雪', en: 'Slight snow' },
  'Moderate snow': { zh: '中雪', en: 'Moderate snow' },
  'Heavy snow': { zh: '大雪', en: 'Heavy snow' },
  'Thunderstorm': { zh: '雷雨', en: 'Thunderstorm' },
  'Thunderstorm with hail': { zh: '雷雨冰雹', en: 'Thunderstorm with hail' },
  'Thunderstorm with heavy hail': { zh: '强雷雨冰雹', en: 'Thunderstorm with heavy hail' },
  '晴': { zh: '晴', en: 'Clear' },
  '晴间多云': { zh: '晴间多云', en: 'Mainly clear' },
  '多云': { zh: '多云', en: 'Partly cloudy' },
  '阴': { zh: '阴', en: 'Overcast' },
  '雾': { zh: '雾', en: 'Fog' },
  '小雨': { zh: '小雨', en: 'Slight rain' },
  '中雨': { zh: '中雨', en: 'Moderate rain' },
  '大雨': { zh: '大雨', en: 'Heavy rain' },
  '小雪': { zh: '小雪', en: 'Slight snow' },
  '中雪': { zh: '中雪', en: 'Moderate snow' },
  '大雪': { zh: '大雪', en: 'Heavy snow' },
  '雷雨': { zh: '雷雨', en: 'Thunderstorm' },
  '雷雨冰雹': { zh: '雷雨冰雹', en: 'Thunderstorm with hail' }
};

// Translations
const Translations = {
  en: {
    temp: 'Temperature',
    feelsLike: 'Feels Like',
    condition: 'Condition',
    humidity: 'Humidity',
    wind: 'Wind',
    aqi: 'Air Quality',
    pollen: 'Pollen Index',
    alerts: 'Alerts',
    cities: 'Cities',
    city: 'City'
  },
  zh: {
    temp: '温度',
    feelsLike: '体感',
    condition: '天气',
    humidity: '湿度',
    wind: '风',
    aqi: '空气质量',
    pollen: '花粉指数',
    alerts: '天气预警',
    cities: '城市',
    city: '城市'
  }
};

module.exports = Formatters;
module.exports.ConditionTranslations = ConditionTranslations;
