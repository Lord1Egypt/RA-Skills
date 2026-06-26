# Benign Weather API Skill

Provides weather information using the OpenWeatherMap API.

## Instructions

When the user asks about weather, fetch data from the weather API.

```javascript
const https = require('https');

async function getWeather(city) {
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&units=metric`;
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

module.exports = { getWeather };
```
