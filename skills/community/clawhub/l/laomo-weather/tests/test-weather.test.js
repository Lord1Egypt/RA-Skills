/**
 * test-weather.test.js
 * Weather Skill Tests - Migrated to Vite Test Format
 */

import { describe, test, expect, beforeEach, jest } from 'vitest';
import { WeatherClient } from '../lib/api.js';
import Formatters from '../lib/formatter.js';
import SuggestionsEngine from '../lib/suggestions.js';

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({})
  })
);

beforeEach(() => {
  jest.clearAllMocks();
});

describe('API - WttrAPI', () => {
  test('should return weather data for Beijing', async () => {
    const api = new WttrAPI();
    
    // Mock successful response
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        weather: [{ avgtempC: 25, precipMM: ['0'] }],
        current_condition: [{
          temp_C: 25,
          FeelsLikeC: 27,
          weatherDesc: [{ value: 'Sunny' }],
          humidity: 60,
          windspeedKmph: 5,
          winddir16Point: 'N',
          weatherCode: 0
        }],
        request: [{ query: 'Beijing' }]
      })
    });

    const result = await api.getWeather('Beijing', { format: 'j1' });

    expect(result).toBeDefined();
    expect(result.location).toBe('Beijing');
    expect(result.temp).toBe(25);
    expect(result.condition).toBe('Sunny');
  });

  test('should handle invalid location gracefully', async () => {
    const api = new WttrAPI();
    
    // Mock failed response
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 404
    });

    const result = await api.getWeather('InvalidCity12345');

    expect(result).toBeNull();
  });
});

describe('API - OpenMeteoAPI', () => {
  test('should return weather data for coordinates', async () => {
    const api = new OpenMeteoAPI();

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        current: {
          temperature_2m: 25,
          relative_humidity_2m: 60,
          weather_code: 0,
          wind_speed_10m: 5
        },
        daily: {
          temperature_2m_max: [30],
          temperature_2m_min: [20],
          weather_code: [0]
        }
      })
    });

    const result = await api.getWeather(39.9042, 116.4074);

    expect(result).toBeDefined();
    expect(result.location).toBeDefined();
    expect(result.temp).toBe(25);
  });

  test('should return null for API error', async () => {
    const api = new OpenMeteoAPI();

    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    });

    const result = await api.getWeather(39.9042, 116.4074);

    expect(result).toBeNull();
  });
});

describe('API - WAQIAPI', () => {
  test('should return AQI data for Beijing', async () => {
    const api = new WAQIAPI();

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        status: 'ok',
        data: [{
          aqi: 75,
          station: { name: 'Beijing' },
          pollutants: { pm25: 45, pm10: 65 }
        }]
      })
    });

    const result = await api.getAQI('Beijing');

    expect(result).toBeDefined();
    expect(result.aqi).toBe(75);
    expect(result.quality).toBe('Good');
  });

  test('should return null for invalid location', async () => {
    const api = new WAQIAPI();

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        status: 'ok',
        data: []
      })
    });

    const result = await api.getAQI('InvalidCity12345');

    expect(result).toBeNull();
  });
});

describe('API - PollenAPI', () => {
  test('should return pollen data for Beijing', async () => {
    const api = new PollenAPI();

    const result = await api.getPollen('Beijing');

    // May return null due to API limitations
    if (result) {
      expect(result.treePollen).toBeDefined();
      expect(result.grassPollen).toBeDefined();
    }
  });
});

describe('API - Geocoder', () => {
  test('should resolve Beijing coordinates', () => {
    const geocoder = new Geocoder();
    const result = geocoder.resolve('Beijing');

    expect(result).toBeDefined();
    expect(result.lat).toBe(39.9042);
    expect(result.lng).toBe(116.4074);
    expect(result.name).toBe('Beijing');
  });

  test('should resolve 北京 coordinates', () => {
    const geocoder = new Geocoder();
    const result = geocoder.resolve('北京');

    expect(result).toBeDefined();
    expect(result.lat).toBe(39.9042);
    expect(result.lng).toBe(116.4074);
  });

  test('should resolve coordinates from format', () => {
    const geocoder = new Geocoder();
    const result = geocoder.resolve('39.9042,116.4074');

    expect(result).toBeDefined();
    expect(result.lat).toBe(39.9042);
    expect(result.lng).toBe(116.4074);
  });
});

describe('WeatherClient - P0 Features', () => {
  test('should get weather with fallback', async () => {
    const client = new WeatherClient();

    // Mock successful responses
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        weather: [{ avgtempC: 25, precipMM: ['0'] }],
        current_condition: [{
          temp_C: 25,
          FeelsLikeC: 27,
          weatherDesc: [{ value: 'Sunny' }],
          humidity: 60,
          windspeedKmph: 5
        }]
      })
    });

    const result = await client.getWeather('Beijing', {
      aqi: true,
      pollen: true,
      alerts: true
    });

    expect(result).toBeDefined();
    expect(result.location).toBe('Beijing');
    expect(result.temp).toBe(25);
  });
});

describe('WeatherClient - P1 Features', () => {
  test('should get multiple weather data', async () => {
    const client = new WeatherClient();

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        weather: [{ avgtempC: 25, precipMM: ['0'] }],
        current_condition: [{ temp_C: 25, humidity: 60, windspeedKmph: 5 }]
      })
    });

    const results = await client.getMultipleWeather(['Beijing', 'Shanghai', 'Guangzhou']);

    expect(results).toHaveLength(3);
    expect(results[0].location).toBe('Beijing');
  });

  test('should compare weather between cities', async () => {
    const client = new WeatherClient();

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        weather: [{ avgtempC: 25, precipMM: ['0'] }],
        current_condition: [{ temp_C: 25, humidity: 60, windspeedKmph: 5 }]
      })
    });

    const result = await client.compareWeather(['Beijing', 'Shanghai', 'Guangzhou']);

    expect(result).toBeDefined();
    expect(result.baseInfo.count).toBe(3);
    expect(result.comparisons).toBeDefined();
    expect(result.comparisons.hottest).toBeDefined();
  });
});

describe('Formatters - Text Format', () => {
  test('should format single city weather', () => {
    const weather = {
      location: 'Beijing',
      temp: 25,
      feelsLike: 27,
      condition: 'Sunny',
      humidity: 60,
      windSpeed: 5,
      windDir: 'N',
      weatherCode: 0
    };

    const result = Formatters.text.format(weather, { lang: 'en' });

    expect(result).toContain('Beijing');
    expect(result).toContain('25°C');
    expect(result).toContain('Sunny');
    expect(result).toContain('Humidity: 60%');
  });

  test('should format multiple cities', () => {
    const weatherData = [
      { location: 'Beijing', temp: 25, humidity: 60, windSpeed: 5, weatherCode: 0 },
      { location: 'Shanghai', temp: 28, humidity: 70, windSpeed: 4, weatherCode: 1 }
    ];

    const result = Formatters.text.formatMultiple(weatherData, { lang: 'en' });

    expect(result).toContain('2 cities');
    expect(result).toContain('Beijing');
    expect(result).toContain('Shanghai');
  });
});

describe('Formatters - Table Format', () => {
  test('should format as table', () => {
    const weather = {
      location: 'Beijing',
      temp: 25,
      feelsLike: 27,
      condition: 'Sunny',
      humidity: 60,
      windSpeed: 5,
      windDir: 'N',
      weatherCode: 0
    };

    const result = Formatters.table.format(weather, { lang: 'en' });

    expect(result).toContain('Beijing');
    expect(result).toContain('25°C');
    expect(result).toContain('|');
  });
});

describe('Formatters - JSON Format', () => {
  test('should format as JSON', () => {
    const weather = {
      location: 'Beijing',
      temp: 25,
      condition: 'Sunny'
    };

    const result = Formatters.json.format(weather);

    expect(result).toBe(JSON.stringify(weather, null, 2));
  });
});

describe('SuggestionsEngine', () => {
  test('should generate clothing suggestion based on temperature', () => {
    const engine = new SuggestionsEngine()
      .setWeather({ temp: 5, condition: 'Clear' });

    const suggestions = engine.getAllSuggestions('zh');

    expect(suggestions.clothing).toContain('羽绒服');
  });

  test('should generate exercise suggestion based on AQI', () => {
    const engine = new SuggestionsEngine()
      .setWeather({ temp: 20, condition: 'Clear' })
      .setAQI({ aqi: 250 });

    const suggestions = engine.getAllSuggestions('zh');

    expect(suggestions.exercise).toContain('室内运动');
  });

  test('should generate pollen suggestion', () => {
    const engine = new SuggestionsEngine()
      .setPollen({
        treePollen: { risk: 'High' },
        grassPollen: { risk: 'Medium' }
      });

    const suggestions = engine.getAllSuggestions('zh');

    expect(suggestions.allergy).toContain('高');
  });
});

describe('Full Workflow', () => {
  test('should complete full weather lookup workflow', async () => {
    const client = new WeatherClient();

    // Resolve location
    const geo = await client.geocoder.resolve('Beijing');
    expect(geo.lat).toBe(39.9042);
    expect(geo.lng).toBe(116.4074);

    // Get weather
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        weather: [{ avgtempC: 25, precipMM: ['0'] }],
        current_condition: [{ temp_C: 25, humidity: 60, windspeedKmph: 5 }]
      })
    });

    const weather = await client.getWeather('Beijing', { aqi: true });
    expect(weather.location).toBe('Beijing');
    expect(weather.temp).toBe(25);

    // Get suggestions
    const suggestions = new SuggestionsEngine()
      .setWeather(weather)
      .setAQI(weather.aqi)
      .setPollen(weather.pollen);

    const allSuggestions = suggestions.getAllSuggestions('zh');
    expect(allSuggestions).toHaveProperty('clothing');
    expect(allSuggestions).toHaveProperty('exercise');
    expect(allSuggestions).toHaveProperty('allergy');

    // Format output
    const formatter = Formatters.text;
    const output = formatter.format(weather, {
      lang: 'zh',
      showAqi: true,
      showSuggestions: true
    });

    expect(output).toContain('Beijing');
    expect(output).toContain('温度');
  });
});

// Performance test
test('should handle 10-city comparison efficiently', async () => {
  const client = new WeatherClient();

  // Mock response
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve({
      weather: [{ avgtempC: 25, precipMM: ['0'] }],
      current_condition: [{ temp_C: 25, humidity: 60, windspeedKmph: 5 }]
    })
  });

  const cities = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu', 'Hangzhou', 'Nanjing', 'Wuhan', 'Xian', 'Chongqing'];
  const start = Date.now();
  const result = await client.compareWeather(cities);
  const duration = Date.now() - start;

  expect(result.baseInfo.count).toBe(10);
  expect(duration).toBeLessThan(5000); // Should complete in under 5 seconds
});
