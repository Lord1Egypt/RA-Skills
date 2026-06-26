/**
 * Suggestions Engine
 * Generates lifestyle recommendations based on weather data
 */

class SuggestionsEngine {
  constructor() {
    this.weather = null;
    this.aqi = null;
    this.pollen = null;
  }

  /**
   * Set weather data
   * @param {object} weather - Weather data from API
   */
  setWeather(weather) {
    this.weather = weather;
    return this;
  }

  /**
   * Set air quality data
   * @param {object} aqi - AQI data
   */
  setAQI(aqi) {
    this.aqi = aqi;
    return this;
  }

  /**
   * Set pollen data
   * @param {object} pollen - Pollen data
   */
  setPollen(pollen) {
    this.pollen = pollen;
    return this;
  }

  /**
   * Get all suggestions
   * @param {string} lang - Language (zh/en)
   * @returns {object} Suggestions object
   */
  getAllSuggestions(lang = 'auto') {
    const t = Translations[lang === 'auto' ? this._detectLanguage() : lang];

    return {
      clothing: this.getClothingSuggestion(t),
      carWash: this.getCarWashSuggestion(t),
      exercise: this.getExerciseSuggestion(t),
      allergy: this.getAllergySuggestion(t),
      uv: this.getUVSuggestion(t),
      rain: this.getRainSuggestion(t)
    };
  }

  /**
   * Get clothing suggestion
   * @param {object} t - Translations
   * @returns {string} Clothing suggestion
   */
  getClothingSuggestion(t) {
    if (!this.weather) return t.invalid;

    const temp = this.weather.temp;
    const condition = (this.weather.condition || '').toLowerCase();
    const rainProb = this.weather.precipProbability || this.weather.forecast?.precipProbability || 0;

    if (temp < 0) {
      return t.clothing.cold;
    }
    if (temp < 5) {
      return t.clothing.cool;
    }
    if (temp < 15) {
      return t.clothing.chilly;
    }
    if (temp < 25) {
      return t.clothing.warm;
    }
    if (temp < 30) {
      return t.clothing.hot;
    }
    return t.clothing.veryHot;
  }

  /**
   * Get car wash suggestion
   * @param {object} t - Translations
   * @returns {string} Car wash suggestion
   */
  getCarWashSuggestion(t) {
    if (!this.weather) return t.invalid;
    if (!this.aqi) return t.invalid;

    const rainProb = this.weather.precipProbability || this.weather.precipMM || 0;
    const aqi = this.aqi.aqi;

    if (rainProb > 50) {
      return t.carWash.rainHigh;
    }
    if (aqi > 150) {
      return t.carWash.pollution;
    }
    if (rainProb > 20) {
      return t.carWash.rainSome;
    }
    return t.carWash.good;
  }

  /**
   * Get exercise suggestion
   * @param {object} t - Translations
   * @returns {string} Exercise suggestion
   */
  getExerciseSuggestion(t) {
    if (!this.weather) return t.invalid;
    if (!this.aqi) return t.invalid;

    const aqi = this.aqi.aqi;
    const condition = (this.weather.condition || '').toLowerCase();

    if (aqi > 200) {
      return t.exercise.aqiBad;
    }
    if (aqi > 150) {
      return t.exercise.aqiModerate;
    }
    if (condition.includes('rain') || condition.includes('snow') || condition.includes('storm')) {
      return t.exercise.weatherBad;
    }
    return t.exercise.good;
  }

  /**
   * Get allergy/pollen suggestion
   * @param {object} t - Translations
   * @returns {string} Allergy suggestion
   */
  getAllergySuggestion(t) {
    if (!this.pollen) {
      return t.allergy.noData;
    }

    const maxRisk = Math.max(
      this._getRiskLevel(this.pollen.treePollen?.risk),
      this._getRiskLevel(this.pollen.grassPollen?.risk),
      this._getRiskLevel(this.pollen.ragweedPollen?.risk),
      this._getRiskLevel(this.pollen.moldPollen?.risk)
    );

    if (maxRisk >= 3) {
      return t.allergy.highRisk;
    }
    if (maxRisk >= 2) {
      return t.allergy.moderateRisk;
    }
    return t.allergy.lowRisk;
  }

  /**
   * Get UV suggestion
   * @param {object} t - Translations
   * @returns {string} UV suggestion
   */
  getUVSuggestion(t) {
    if (!this.weather) return t.invalid;

    const uv = this.weather.uvIndex || 0;

    if (uv >= 11) {
      return t.uv.extreme;
    }
    if (uv >= 8) {
      return t.uv.veryHigh;
    }
    if (uv >= 6) {
      return t.uv.high;
    }
    if (uv >= 3) {
      return t.uv.moderate;
    }
    return t.uv.low;
  }

  /**
   * Get rain suggestion
   * @param {object} t - Translations
   * @returns {string} Rain suggestion
   */
  getRainSuggestion(t) {
    if (!this.weather) return t.invalid;

    const rainProb = this.weather.precipProbability || 0;
    const precipMM = this.weather.precipMM || 0;

    if (rainProb > 70 || precipMM > 5) {
      return t.rain.veryLikely;
    }
    if (rainProb > 40 || precipMM > 2) {
      return t.rain.moderatelyLikely;
    }
    if (rainProb > 10) {
      return t.rain.slightlyLikely;
    }
    return t.rain.unlikely;
  }

  _getRiskLevel(risk) {
    if (!risk) return 0;
    const map = {
      'Low': 1,
      'Medium': 2,
      'High': 3,
      'Very High': 4
    };
    return map[risk] || 0;
  }

  _detectLanguage() {
    if (this.weather?.location) {
      if (/[\u4e00-\u9fa5]/.test(this.weather.location)) return 'zh';
    }
    return 'en';
  }
}

// Translations
const Translations = {
  en: {
    invalid: 'Invalid data',
    clothing: {
      cold: 'Wear a down jacket, gloves, and scarf',
      cool: 'Wear a thick coat and sweater',
      chilly: 'Wear a long-sleeve shirt and light coat',
      warm: 'Wear T-shirt and shorts',
      hot: 'Wear short sleeves and shorts',
      veryHot: 'Wear light clothing and hat'
    },
    carWash: {
      rainHigh: 'Not suitable for car wash (high rain probability)',
      pollution: 'Delay car wash (air pollution)',
      rainSome: 'Better to avoid car wash (some rain chance)',
      good: ' suitable for car wash'
    },
    exercise: {
      aqiBad: 'Indoor exercise only (severe air pollution)',
      aqiModerate: 'Limit outdoor exercise time',
      weatherBad: 'Indoor exercise (rain/snow)',
      good: ' suitable for outdoor exercise'
    },
    allergy: {
      noData: 'No pollen data available',
      lowRisk: 'Low allergy risk',
      moderateRisk: 'Moderate allergy risk, sensitive people should be cautious',
      highRisk: 'High allergy risk, stay indoors and keep windows closed'
    },
    uv: {
      low: 'Low UV, minimal protection needed',
      moderate: 'Moderate UV, apply sunscreen',
      high: 'High UV, wear sunscreen and hat',
      veryHigh: 'Very high UV, avoid outdoor activities',
      extreme: 'Extreme UV, stay indoors'
    },
    rain: {
      unlikely: 'Rain unlikely',
      slightlyLikely: 'Slight chance of rain',
      moderatelyLikely: 'Moderate chance of rain',
      veryLikely: 'Very likely to rain, carry umbrella'
    }
  },
  zh: {
    invalid: '数据无效',
    clothing: {
      cold: '穿羽绒服、戴手套、围巾',
      cool: '穿厚外套、毛衣',
      chilly: '穿长袖衬衫、薄外套',
      warm: '穿短袖、短裤',
      hot: '穿短袖、短裤',
      veryHot: '穿轻薄衣物、戴帽子'
    },
    carWash: {
      rainHigh: '不宜洗车 (降雨概率高)',
      pollution: '建议延后洗车 (空气污染)',
      rainSome: '建议延后洗车 (有降雨可能)',
      good: '适合洗车'
    },
    exercise: {
      aqiBad: '室内运动 (空气污染严重)',
      aqiModerate: '减少户外运动时间',
      weatherBad: '室内运动 (雨天/雪天)',
      good: '适合户外运动'
    },
    allergy: {
      noData: '无花粉数据',
      lowRisk: '花粉风险低',
      moderateRisk: '花粉风险中等，敏感人群注意',
      highRisk: '花粉风险高，建议室内停留'
    },
    uv: {
      low: '紫外线弱，无需防护',
      moderate: '紫外线中等，涂抹防晒霜',
      high: '紫外线强，涂抹防晒霜并戴帽子',
      veryHigh: '紫外线很强，避免户外活动',
      extreme: '紫外线极强，建议室内停留'
    },
    rain: {
      unlikely: ' unlikely 下雨',
      slightlyLikely: '有小概率下雨',
      moderatelyLikely: '较大概率下雨',
      veryLikely: ' likely 下雨，记得带伞'
    }
  }
};

module.exports = SuggestionsEngine;
