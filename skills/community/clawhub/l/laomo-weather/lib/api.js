/**
 * Weather API Wrapper
 * Supports: wttr.in, Open-Meteo, WAQI (Air Quality), Pollen.com
 */

// ==================== wttr.in API ====================
const WTTRENV = 'https://wttr.in';

class WttrAPI {
  constructor() {
    this.base = WTTRENV;
  }

  /**
   * Get weather data from wttr.in
   * @param {string} location - City name, airport code, or coordinates
   * @param {object} options - Format options
   * @returns {Promise<object>} Weather data
   */
  async getWeather(location, options = {}) {
    const { format = 'j1' } = options; // JSON format

    try {
      const url = `${this.base}/${encodeURIComponent(location)}?format=${format}`;
      const res = await fetch(url);
      
      if (!res.ok) {
        throw new Error(`wttr.in API error: ${res.status}`);
      }
      
      const data = await res.json();
      return this._parseWeather(data, location);
    } catch (error) {
      console.error('wttr.in error:', error.message);
      return null;
    }
  }

  _parseWeather(data, location, lang = 'en') {
    if (!data || !data.weather) return null;

    const today = data.weather[0];
    const current = data.current_condition[0];

    // Use the original location parameter instead of API response query
    // to preserve the city name in the desired format
    const locationName = location;

    return {
      location: locationName,
      temp: parseInt(current?.temp_C) || today?.avgtempC,
      feelsLike: parseInt(current?.FeelsLikeC) || today?.FeelsLikeC,
      condition: today?.hourly?.[0]?.weatherDesc?.[0]?.value || current?.weatherDesc?.[0]?.value,
      weatherCode: current?.weatherCode || today?.hourly?.[0]?.weatherCode,
      humidity: parseInt(current?.humidity) || today?.avghumidity,
      windSpeed: parseInt(current?.windspeedKmph) || today?.windspeedKmph,
      windDir: current?.winddir16Point || 'N',
      pressure: parseInt(current?.pressure) || 1013,
      visibility: parseInt(current?.visibility) || 10,
      uvIndex: parseInt(current?.uvIndex) || 0,
      precipMM: parseFloat(today?.precipMM?.[0] || '0'),
      clouds: parseInt(current?.cloudcover) || 0,
      Observations: {
        time: current?.observation_time,
        weather: today?.hourly?.[0]?.weatherDesc?.[0]?.value
      },
      forecast: today
    };
  }
}

// ==================== Open-Meteo API ====================
const OPENMETEO_API = 'https://api.open-meteo.com/v1';

class OpenMeteoAPI {
  constructor() {
    this.base = OPENMETEO_API;
  }

  /**
   * Get weather data from Open-Meteo
   * @param {number} lat - Latitude
   * @param {number} lng - Longitude
   * @param {object} options - Request options
   * @returns {Promise<object>} Weather data
   */
  async getWeather(lat, lng, options = {}) {
    const { 
      current = 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
      daily = 'temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max',
      timezone = 'auto',
      lang = 'en'
    } = options;

    try {
      const url = `${this.base}/forecast?latitude=${lat}&longitude=${lng}&current=${current}&daily=${daily}&timezone=${timezone}`;
      const res = await fetch(url);
      
      if (!res.ok) {
        throw new Error(`Open-Meteo API error: ${res.status}`);
      }
      
      const data = await res.json();
      return this._parseWeather(data, lat, lng, lang);
    } catch (error) {
      console.error('Open-Meteo error:', error.message);
      return null;
    }
  }

  async getAlerts(lat, lng) {
    try {
      const url = `${this.base}/alerts?latitude=${lat}&longitude=${lng}`;
      const res = await fetch(url);
      
      if (!res.ok) return null;
      
      const data = await res.json();
      return data;
    } catch (error) {
      console.error('Open-Meteo alerts error:', error.message);
      return null;
    }
  }

  _parseWeather(data, lat, lng, lang = 'en') {
    if (!data || !data.current) return null;

    const current = data.current;
    const daily = data.daily;

    // Reverse geocode for location name using the geocoder
    const location = this.geocoder?.reverseGeocode(lat, lng, lang);

    return {
      location: location || `${lat.toFixed(2)},${lng.toFixed(2)}`,
      temp: current.temperature_2m,
      feelsLike: current.temperature_2m, // No feels like in free tier
      condition: this._wmoToCondition(current.weather_code, lang),
      weatherCode: current.weather_code,
      humidity: current.relative_humidity_2m,
      windSpeed: current.wind_speed_10m,
      windDir: this._getWindDirection(current.wind_direction_10m),
      forecast: {
        daily: daily
      }
    };
  }

  _wmoToCondition(code, lang = 'en') {
    const wmoCodes = {
      'en': {
        0: 'Clear sky',
        1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
        45: 'Fog', 48: 'Depositing rime fog',
        51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
        61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
        71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
        95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Thunderstorm with heavy hail'
      },
      'zh': {
        0: '晴',
        1: '晴间多云', 2: '多云', 3: '阴',
        45: '雾', 48: '冻雾',
        51: '小雨', 53: '中雨', 55: '大雨',
        61: '小雨', 63: '中雨', 65: '大雨',
        71: '小雪', 73: '中雪', 75: '大雪',
        95: '雷雨', 96: '雷雨冰雹', 99: '强雷雨冰雹'
      }
    };
    const translated = wmoCodes[lang]?.[code];
    if (translated) return translated;
    const fallback = wmoCodes['en'][code];
    return fallback || 'Unknown';
  }

  _getWindDirection(deg) {
    const dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    return dirs[Math.round(deg / 22.5) % 16];
  }

  _reverseGeoCode(lat, lng) {
    // Simple reverse geocoding - in production, use a proper geocoding API
    return null; // Will be filled by Geocoder class
  }
}

// ==================== Open-Meteo Air Quality API (Free) ====================
const OPENMETEO_AQ_API = 'https://air-quality-api.open-meteo.com/v1/air-quality';

class OpenMeteoAQAPI {
  constructor() {
    this.base = OPENMETEO_AQ_API;
  }

  /**
   * Get air quality data from Open-Meteo (FREE, no API key required)
   * @param {number} lat - Latitude
   * @param {number} lng - Longitude
   * @returns {Promise<object>} Air quality data
   */
  async getAQI(lat, lng) {
    try {
      // Get current AQI
      const aqUrl = `${this.base}?latitude=${lat}&longitude=${lng}&current=us_aqi&timezone=auto`;
      const aqRes = await fetch(aqUrl);
      
      // Get hourly pollutants
      const pollUrl = `${this.base}?latitude=${lat}&longitude=${lng}&hourly=pm2_5,pm10,ozone,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide&timezone=auto&forecast_days=1`;
      const pollRes = await fetch(pollUrl);
      
      if (!aqRes.ok || !pollRes.ok) {
        throw new Error(`Open-Meteo Air Quality API error: ${aqRes.status} / ${pollRes.status}`);
      }
      
      const aqData = await aqRes.json();
      const pollData = await pollRes.json();
      return this._parseAQI(aqData, pollData, lat, lng);
    } catch (error) {
      console.error('Open-Meteo AQ error:', error.message);
      return null;
    }
  }

  _parseAQI(aqData, pollData, lat, lng) {
    if (!aqData || !aqData.current || !aqData.current.us_aqi) return null;

    const current = aqData.current;
    const aqi = current.us_aqi;
    
    // Get latest hourly pollutant values
    const getPollutantValue = (pollutant) => {
      const values = pollData.hourly?.[pollutant];
      return values && values.length > 0 ? values[0] : null;
    };

    return {
      aqi: aqi,
      pm25: getPollutantValue('pm2_5'),
      pm10: getPollutantValue('pm10'),
      o3: getPollutantValue('ozone'),
      no2: getPollutantValue('nitrogen_dioxide'),
      so2: getPollutantValue('sulphur_dioxide'),
      co: getPollutantValue('carbon_monoxide'),
      aqiDesc: this._getAQIDescription(aqi),
      location: `${lat.toFixed(2)},${lng.toFixed(2)}`,
      time: current.time,
      quality: this._getQuality(aqi),
      category: this._getCategory(aqi)
    };
  }

  _getAQIDescription(aqi) {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
  }

  _getQuality(aqi) {
    if (aqi <= 50) return 'Excellent';
    if (aqi <= 100) return 'Good';
    if (aqi <= 150) return 'Lightly Polluted';
    if (aqi <= 200) return 'Moderately Polluted';
    if (aqi <= 300) return 'Heavily Polluted';
    return 'Severely Polluted';
  }

  _getCategory(aqi) {
    if (aqi <= 50) return { level: 1, color: '00e400', text: 'Good' };
    if (aqi <= 100) return { level: 2, color: 'fcff00', text: 'Moderate' };
    if (aqi <= 150) return { level: 3, color: 'ff7e00', text: 'Unhealthy for Sensitive Groups' };
    if (aqi <= 200) return { level: 4, color: 'ff0000', text: 'Unhealthy' };
    if (aqi <= 300) return { level: 5, color: '8f3f97', text: 'Very Unhealthy' };
    return { level: 6, color: '7e0023', text: 'Hazardous' };
  }
}

// ==================== Open-Meteo Pollen API (Free) ====================
const OPENMETEO_POLLEN_API = 'https://pollen-api.open-meteo.com/v1/pollen';

class OpenMeteoPollenAPI {
  constructor() {
    this.base = OPENMETEO_POLLEN_API;
  }

  /**
   * Get pollen data from Open-Meteo (FREE, no API key required)
   * Note: Coverage is primarily Europe/North America
   * @param {number} lat - Latitude
   * @param {number} lng - Longitude
   * @returns {Promise<object>} Pollen data
   */
  async getPollen(lat, lng) {
    try {
      const url = `${this.base}?latitude=${lat}&longitude=${lng}&daily=tree_pollen,grass_pollen,ragweed_pollen,mold_pollen`;
      const res = await fetch(url);
      
      if (!res.ok) {
        throw new Error(`Open-Meteo Pollen API error: ${res.status}`);
      }
      
      const data = await res.json();
      return this._parsePollen(data, lat, lng);
    } catch (error) {
      console.error('Open-Meteo Pollen error:', error.message);
      return null;
    }
  }

  _parsePollen(data, lat, lng) {
    if (!data || !data.daily) return null;

    const daily = data.daily;
    
    // Get today's pollen data
    const todayIndex = 0;
    
    const treePollen = daily.tree_pollen?.[todayIndex] ?? null;
    const grassPollen = daily.grass_pollen?.[todayIndex] ?? null;
    const ragweedPollen = daily.ragweed_pollen?.[todayIndex] ?? null;
    const moldPollen = daily.mold_pollen?.[todayIndex] ?? null;

    return {
      location: `${lat.toFixed(2)},${lng.toFixed(2)}`,
      treePollen: {
        level: treePollen,
        risk: this._getPollenRisk(treePollen)
      },
      grassPollen: {
        level: grassPollen,
        risk: this._getPollenRisk(grassPollen)
      },
      ragweedPollen: {
        level: ragweedPollen,
        risk: this._getPollenRisk(ragweedPollen)
      },
      moldPollen: {
        level: moldPollen,
        risk: this._getPollenRisk(moldPollen)
      },
      overallIndex: this._calculateOverallIndex(treePollen, grassPollen, ragweedPollen, moldPollen),
      disclaimer: 'Data from Open-Meteo Pollen API (Free)'
    };
  }

  _getPollenRisk(index) {
    if (index === null || index === undefined) return 'Unknown';
    if (index <= 2.5) return 'Low';
    if (index <= 7.5) return 'Medium';
    if (index <= 12.5) return 'High';
    return 'Very High';
  }

  _calculateOverallIndex(...values) {
    const valid = values.filter(v => v !== null && v !== undefined);
    if (valid.length === 0) return null;
    return valid.reduce((a, b) => a + b, 0) / valid.length;
  }
}

// ==================== Open-Meteo Weather Alerts API (Free) ====================
const OPENMETEO_ALERTS_API = 'https://api.open-meteo.com/v1/alerts';

class OpenMeteoAlertsAPI {
  constructor() {
    this.base = OPENMETEO_ALERTS_API;
  }

  /**
   * Get weather alerts from Open-Meteo (FREE, no API key required)
   * Note: Open-Meteo Alerts API may not be available in all regions
   * @param {number} lat - Latitude
   * @param {number} lng - Longitude
   * @returns {Promise<object>} Alerts
   */
  async getAlerts(lat, lng) {
    try {
      const url = `${this.base}?latitude=${lat}&longitude=${lng}`;
      const res = await fetch(url);
      
      if (!res.ok) {
        // Return null if alerts API not available for this region
        console.warn(`Weather alerts not available for this region (API status: ${res.status})`);
        return null;
      }
      
      const data = await res.json();
      return this._parseAlerts(data);
    } catch (error) {
      console.warn('Open-Meteo Alerts error:', error.message);
      return null;
    }
  }

  _parseAlerts(data) {
    if (!data) return null;

    return {
      warnings: data.warnings || [],
      advisory: data.advisory || [],
      watch: data.watch || [],
      severe: data.severe || [],
      summary: data.summary || '',
      overallSeverity: data.overall_severity || 'None'
    };
  }
}

// ==================== Geocoder ====================
class Geocoder {
  constructor() {
    this.cityCoords = {};
    this.cityMap = {
      // Chinese to English
      '北京': { lat: 39.9042, lng: 116.4074, name: '北京' },
      '上海': { lat: 31.2304, lng: 121.4737, name: '上海' },
      '广州': { lat: 23.1291, lng: 113.2644, name: '广州' },
      '深圳': { lat: 22.5431, lng: 114.0579, name: '深圳' },
      '成都': { lat: 30.5728, lng: 104.0668, name: '成都' },
      '杭州': { lat: 30.2741, lng: 120.1551, name: '杭州' },
      '南京': { lat: 32.0603, lng: 118.7969, name: '南京' },
      '武汉': { lat: 30.5928, lng: 114.3055, name: '武汉' },
      '西安': { lat: 34.3416, lng: 108.9398, name: '西安' },
      '重庆': { lat: 29.5630, lng: 106.5516, name: '重庆' },
      '天津': { lat: 39.3434, lng: 117.3616, name: '天津' },
      '沈阳': { lat: 41.8057, lng: 123.4315, name: '沈阳' },
      '哈尔滨': { lat: 45.8038, lng: 126.5349, name: '哈尔滨' },
      '郑州': { lat: 34.7466, lng: 113.6253, name: '郑州' },
      '济南': { lat: 36.6512, lng: 117.1201, name: '济南' },
      '合肥': { lat: 31.8206, lng: 117.2272, name: '合肥' },
      '福州': { lat: 26.0745, lng: 119.2965, name: '福州' },
      '长沙': { lat: 28.2282, lng: 112.9388, name: '长沙' },
      '昆明': { lat: 24.8801, lng: 102.8329, name: '昆明' },
      '贵阳': { lat: 26.6470, lng: 106.6302, name: '贵阳' },
      '兰州': { lat: 36.0590, lng: 103.8343, name: '兰州' },
      '西宁': { lat: 36.6172, lng: 101.7782, name: '西宁' },
      '乌鲁木齐': { lat: 43.8256, lng: 87.6168, name: '乌鲁木齐' },
      '拉萨': { lat: 29.6500, lng: 91.1400, name: '拉萨' },
      '海口': { lat: 20.0448, lng: 110.1999, name: '海口' },
      '香港': { lat: 22.3193, lng: 114.1694, name: '香港' },
      '澳门': { lat: 22.1987, lng: 113.5439, name: '澳门' },
      '台北': { lat: 25.0330, lng: 121.5654, name: '台北' },
      '高雄': { lat: 22.6273, lng: 120.3013, name: '高雄' },
      
      // English to Chinese
      'Beijing': { lat: 39.9042, lng: 116.4074, name: 'Beijing' },
      'Shanghai': { lat: 31.2304, lng: 121.4737, name: 'Shanghai' },
      'Guangzhou': { lat: 23.1291, lng: 113.2644, name: 'Guangzhou' },
      'Shenzhen': { lat: 22.5431, lng: 114.0579, name: 'Shenzhen' },
      'Chengdu': { lat: 30.5728, lng: 104.0668, name: 'Chengdu' },
      'Hangzhou': { lat: 30.2741, lng: 120.1551, name: 'Hangzhou' },
      'Nanjing': { lat: 32.0603, lng: 118.7969, name: 'Nanjing' },
      'Wuhan': { lat: 30.5928, lng: 114.3055, name: 'Wuhan' },
      'Xian': { lat: 34.3416, lng: 108.9398, name: 'Xian' },
      'Chongqing': { lat: 29.5630, lng: 106.5516, name: 'Chongqing' },
      'Tianjin': { lat: 39.3434, lng: 117.3616, name: 'Tianjin' },
      'Shenyang': { lat: 41.8057, lng: 123.4315, name: 'Shenyang' },
      'Harbin': { lat: 45.8038, lng: 126.5349, name: 'Harbin' },
      'Zhengzhou': { lat: 34.7466, lng: 113.6253, name: 'Zhengzhou' },
      'Jinan': { lat: 36.6512, lng: 117.1201, name: 'Jinan' },
      'Hefei': { lat: 31.8206, lng: 117.2272, name: 'Hefei' },
      'Fuzhou': { lat: 26.0745, lng: 119.2965, name: 'Fuzhou' },
      'Changsha': { lat: 28.2282, lng: 112.9388, name: 'Changsha' },
      'Kunming': { lat: 24.8801, lng: 102.8329, name: 'Kunming' },
      'Guiyang': { lat: 26.6470, lng: 106.6302, name: 'Guiyang' },
      'Lanzhou': { lat: 36.0590, lng: 103.8343, name: 'Lanzhou' },
      'Xining': { lat: 36.6172, lng: 101.7782, name: 'Xining' },
      'Urumqi': { lat: 43.8256, lng: 87.6168, name: 'Urumqi' },
      'Lhasa': { lat: 29.6500, lng: 91.1400, name: 'Lhasa' },
      'Haikou': { lat: 20.0448, lng: 110.1999, name: 'Haikou' },
      'Hong Kong': { lat: 22.3193, lng: 114.1694, name: 'Hong Kong' },
      'Macau': { lat: 22.1987, lng: 113.5439, name: 'Macau' },
      'Taipei': { lat: 25.0330, lng: 121.5654, name: 'Taipei' },
      'Kaohsiung': { lat: 22.6273, lng: 120.3013, name: 'Kaohsiung' },
      
      // International cities
      'London': { lat: 51.5074, lng: -0.1278, name: 'London' },
      'New York': { lat: 40.7128, lng: -74.0060, name: 'New York' },
      'Tokyo': { lat: 35.6762, lng: 139.6503, name: 'Tokyo' },
      'Paris': { lat: 48.8566, lng: 2.3522, name: 'Paris' },
      'Berlin': { lat: 52.5200, lng: 13.4050, name: 'Berlin' },
      'Moscow': { lat: 55.7558, lng: 37.6173, name: 'Moscow' },
      'Sydney': { lat: -33.8688, lng: 151.2093, name: 'Sydney' },
      'Singapore': { lat: 1.3521, lng: 103.8198, name: 'Singapore' },
      'Dubai': { lat: 25.2048, lng: 55.2708, name: 'Dubai' },
      'Bangkok': { lat: 13.7563, lng: 100.5018, name: 'Bangkok' },
      'Kuala Lumpur': { lat: 3.1390, lng: 101.6869, name: 'Kuala Lumpur' },
      'Seoul': { lat: 37.5665, lng: 126.9780, name: 'Seoul' },
      
      // International cities in Chinese (for reverse lookup)
      '伦敦': { lat: 51.5074, lng: -0.1278, name: 'London' },
      '纽约': { lat: 40.7128, lng: -74.0060, name: 'New York' },
      '东京': { lat: 35.6762, lng: 139.6503, name: 'Tokyo' },
      '巴黎': { lat: 48.8566, lng: 2.3522, name: 'Paris' },
      '柏林': { lat: 52.5200, lng: 13.4050, name: 'Berlin' },
      '莫斯科': { lat: 55.7558, lng: 37.6173, name: 'Moscow' },
      '悉尼': { lat: -33.8688, lng: 151.2093, name: 'Sydney' },
      '新加坡': { lat: 1.3521, lng: 103.8198, name: 'Singapore' },
      '迪拜': { lat: 25.2048, lng: 55.2708, name: 'Dubai' },
      '曼谷': { lat: 13.7563, lng: 100.5018, name: 'Bangkok' },
      '吉隆坡': { lat: 3.1390, lng: 101.6869, name: 'Kuala Lumpur' },
      '首尔': { lat: 37.5665, lng: 126.9780, name: 'Seoul' }
    };
  }

  async resolve(location) {
    // Try to parse coordinates first
    const coords = this._parseCoordinates(location);
    if (coords) return { ...coords, name: location };

    // Try Chinese/English city mapping
    const mapped = this._resolveCity(location);
    if (mapped) return mapped;

    // Try Open-Meteo reverse geocoding
    const geo = await this._geocodeOpenMeteo(location);
    if (geo) return geo;

    throw new Error(`无法解析位置: ${location}`);
  }

  _parseCoordinates(loc) {
    const match = loc.match(/(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)/);
    if (match) {
      return { lat: parseFloat(match[1]), lng: parseFloat(match[2]) };
    }
    return null;
  }

  _resolveCity(location) {
    // Normalize location by removing common suffixes for Chinese cities
    const normalized = location
      .replace(/市$/u, '')  // Remove '市' suffix
      .replace(/\s+/g, '');  // Remove spaces
    
    // Use instance variable cityMap
    const cityMap = this.cityMap;
    
    // First try with normalized location
    const result = cityMap[normalized] || cityMap[location] || null;
    
    // If found and it's Chinese city, add '市' suffix back for display
    if (result && /[\u4e00-\u9fa5]/.test(result.name) && !result.name.endsWith('市')) {
      const original = cityMap[location];
      if (original && original.name) {
        result.name = original.name;
      }
    }
    
    return result;
  }

  async _geocodeOpenMeteo(location) {
    try {
      // Use wttr.in to get coordinates for a city
      const url = `https://wttr.in/${encodeURIComponent(location)}?format=%l`;
      const res = await fetch(url);
      
      if (res.ok) {
        const city = await res.text();
        // Then get coordinates from Open-Meteo
        const geoUrl = `https://geocoding.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`;
        const geoRes = await fetch(geoUrl);
        
        if (geoRes.ok) {
          const geoData = await geoRes.json();
          if (geoData.results && geoData.results.length > 0) {
            return {
              lat: geoData.results[0].latitude,
              lng: geoData.results[0].longitude,
              name: geoData.results[0].name
            };
          }
        }
      }
    } catch (error) {
      // Ignore errors, return null
    }
    
    return null;
  }
  
  reverseGeocode(lat, lng, lang = 'en') {
    // Find city by coordinates in the city map
    // First pass: look for exact English name match if lang is 'en'
    if (lang === 'en') {
      for (const [cityName, data] of Object.entries(this.cityMap)) {
        if (Math.abs(data.lat - lat) < 0.01 && Math.abs(data.lng - lng) < 0.01) {
          // If cityName is English (no Chinese), return data.name
          if (!/[\u4e00-\u9fa5]/.test(cityName)) {
            return data.name;
          }
        }
      }
    }
    
    // Second pass: find any match
    for (const [cityName, data] of Object.entries(this.cityMap)) {
      // Check if coordinates match (with small tolerance)
      if (Math.abs(data.lat - lat) < 0.01 && Math.abs(data.lng - lng) < 0.01) {
        // Return the city name in the requested language
        if (lang === 'zh' && /[\u4e00-\u9fa5]/.test(data.name)) {
          return data.name;
        } else if (lang === 'en') {
          // Return English name if available, otherwise use the key
          return /[\u4e00-\u9fa5]/.test(cityName) ? data.name : cityName;
        }
        return data.name;
      }
    }
    return null;
  }
}

// ==================== Main Weather Client ====================
class WeatherClient {
  constructor() {
    this.wttr = new WttrAPI();
    this.openMeteo = new OpenMeteoAPI();
    this.openMeteoAQ = new OpenMeteoAQAPI();
    this.openMeteoPollen = new OpenMeteoPollenAPI();
    this.openMeteoAlerts = new OpenMeteoAlertsAPI();
    this.geocoder = new Geocoder();
  }

  /**
   * Get complete weather data with fallback
   * @param {string} location - City name
   * @param {object} options - Request options
   * @returns {Promise<object>} Complete weather data
   */
  async getWeather(location, options = {}) {
    const {
      aqi = false,
      pollen = false,
      alerts = false,
      lang = 'en'
    } = options;

    // Resolve location to coordinates
    const geo = await this.geocoder.resolve(location);
    
    // Get primary weather (wttr.in)
    let weather = await this.wttr.getWeather(location, { format: 'j1' });
    
    // Fallback to Open-Meteo if wttr.in fails
    if (!weather) {
      weather = await this.openMeteo.getWeather(geo.lat, geo.lng, { lang });
    }
    
    if (!weather) {
      throw new Error(`无法获取天气数据: ${location}`);
    }

    // Add coordinates
    weather.lat = geo.lat;
    weather.lng = geo.lng;
    
    // Set correct location name using reverse geocoding
    const reverseName = this.geocoder.reverseGeocode(geo.lat, geo.lng, lang);
    if (reverseName) {
      weather.location = reverseName;
    }

    // Add AQI if requested (now using Open-Meteo)
    if (aqi) {
      weather.aqi = await this.openMeteoAQ.getAQI(geo.lat, geo.lng);
    }

    // Add pollen if requested (now using Open-Meteo)
    if (pollen) {
      weather.pollen = await this.openMeteoPollen.getPollen(geo.lat, geo.lng);
    }

    // Add alerts if requested (now using Open-Meteo)
    if (alerts) {
      weather.alerts = await this.openMeteoAlerts.getAlerts(geo.lat, geo.lng);
    }

    return weather;
  }

  /**
   * Get weather for multiple cities
   * @param {string[]} cities - Array of city names
   * @param {object} options - Request options
   * @returns {Promise<object[]>} Array of weather data
   */
  async getMultipleWeather(cities, options = {}) {
    const results = await Promise.all(
      cities.map(city => this.getWeather(city, options))
    );
    
    return results;
  }

  /**
   * Compare weather between multiple cities
   * @param {string[]} cities - Array of city names
   * @param {object} options - Request options
   * @returns {Promise<object>} Comparison results
   */
  async compareWeather(cities, options = {}) {
    const weatherData = await this.getMultipleWeather(cities, options);
    
    if (weatherData.length < 2) {
      throw new Error('至少需要两个城市进行比较');
    }

    const comparisons = {
      hottest: weatherData.reduce((a, b) => a.temp > b.temp ? a : b),
      coldest: weatherData.reduce((a, b) => a.temp < b.temp ? a : b),
      wettest: weatherData.reduce((a, b) => (a.humidity || 0) > (b.humidity || 0) ? a : b),
      windiest: weatherData.reduce((a, b) => (a.windSpeed || 0) > (b.windSpeed || 0) ? a : b),
      highestAQI: weatherData.find(a => a.aqi)?.aqi 
        ? weatherData.reduce((a, b) => (a.aqi?.aqi || 0) > (b.aqi?.aqi || 0) ? a : b)
        : null,
      lowestAQI: weatherData.find(a => a.aqi)?.aqi 
        ? weatherData.reduce((a, b) => (a.aqi?.aqi || 0) < (b.aqi?.aqi || 0) ? a : b)
        : null
    };

    return {
      baseInfo: {
        count: weatherData.length,
        cities: cities
      },
      comparisons: comparisons,
      details: weatherData
    };
  }
}

// Export modules
module.exports = {
  WeatherClient,
  WttrAPI,
  OpenMeteoAPI,
  OpenMeteoAQAPI,
  OpenMeteoPollenAPI,
  OpenMeteoAlertsAPI,
  Geocoder
};
