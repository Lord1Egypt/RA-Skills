// weather_aqi_claw.js - PicoClaw/OpenClaw native (no Node deps, pure async fetch)
async function run(location, json = false) {
  const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`;
  const geoRes = await web_fetch(geoUrl);
  if (!geoRes.results?.[0]) throw new Error(`Location "${location}" not found`);

  const r = geoRes.results[0];
  const geo = { name: r.name, country: r.country, lat: r.latitude, lon: r.longitude };

  const [weatherRes, aqiRes] = await Promise.all([
    web_fetch(`https://api.open-meteo.com/v1/forecast?latitude=${geo.lat}&longitude=${geo.lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,windspeed_10m,wind_direction_10m&wind_speed_unit=kmh&timezone=auto`),
    web_fetch(`https://api.waqi.info/feed/geo:${geo.lat};${geo.lon}/?token=${process.env.WAQITOKEN}`)
  ]);

  const c = weatherRes.current;
  const d = aqiRes.data;
  const result = {
    location: geo,
    weather: {
      temperature: `${c.temperature_2m}°C`,
      feels_like: `${c.apparent_temperature}°C`,
      humidity: `${c.relative_humidity_2m}%`,
      wind: `${c.windspeed_10m} km/h (${windDir(c.wind_direction_10m)})`,
      condition: weatherDesc(c.weather_code)
    },
    aqi: {
      value: d.aqi,
      category: aqiCategory(d.aqi),
      color: aqiColor(d.aqi),
      pollutant: d.dominentpol || 'N/A',
      station: d.city?.name || 'Unknown'
    }
  };

  if (json) return JSON.stringify(result, null, 2);
  return formatOutput(result);
}

function windDir(deg) {
  const dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  return dirs[Math.round(deg / 45) % 8];
}

function weatherDesc(code) {
  const map = {
    0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
    45: 'Fog', 48: 'Depositing rime fog', 51: 'Light drizzle', 53: 'Moderate drizzle',
    55: 'Dense drizzle', 61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
    71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow', 80: 'Slight rain showers',
    81: 'Moderate rain showers', 82: 'Violent rain showers', 95: 'Thunderstorm',
    96: 'Thunderstorm with hail', 99: 'Thunderstorm with heavy hail'
  };
  return map[code] || `Code ${code}`;
}

function aqiCategory(aqi) {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Moderate';
  if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
  if (aqi <= 200) return 'Unhealthy';
  if (aqi <= 300) return 'Very Unhealthy';
  return 'Hazardous';
}

function aqiColor(aqi) {
  const colors = ['🟢', '🟡', '🟠', '🔴', '🟣', '⚫'];
  return colors[Math.min(Math.floor(aqi / 50), 5)];
}

function formatOutput(result) {
  return `${result.location.name}, ${result.location.country}
${'='.repeat(40)}
🌡️  Temperature: ${result.weather.temperature} (feels ${result.weather.feels_like})
💧 Humidity: ${result.weather.humidity}
💨 Wind: ${result.weather.wind}
☁️  Condition: ${result.weather.condition}
${'='.repeat(40)}
${result.aqi.color} AQI: ${result.aqi.value} (${result.aqi.category})
🚨 Pollutant: ${result.aqi.pollutant.toUpperCase()}
📍 Station: ${result.aqi.station}`;
}

// Export for Claw agent
module.exports = { run };
