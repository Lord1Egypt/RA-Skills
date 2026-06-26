// 动态导入 node-fetch (兼容 ES Module)
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

export default async function ({ location }) {
  if (!location) {
    location = "Beijing";
  }
  
  try {
    // 使用 wttr.in 获取简洁的天气信息
    const url = `https://wttr.in/${encodeURIComponent(location)}?format=j1`;
    
    // 动态导入 node-fetch
    const { default: fetchLib } = await import('node-fetch');
    const response = await fetchLib(url, {
      headers: { 'User-Agent': 'OpenClaw-Weather-Skill' }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // 解析 wttr.in 的 JSON 返回
    const current = data.current_condition[0];
    const area = data.nearest_area[0];
    
    const city = area.areaName[0].value;
    const country = area.country[0].value;
    const tempC = current.temp_C;
    const tempF = current.temp_F;
    const weatherDesc = current.weatherDesc[0].value;
    const humidity = current.humidity;
    const windSpeed = current.windspeedKmph;
    
    return `📍 地点：${city}, ${country}
🌡️ 温度：${tempC}°C (${tempF}°F)
☁️ 天气：${weatherDesc}
💧 湿度：${humidity}%
🍃 风速：${windSpeed} km/h`;

  } catch (error) {
    console.error("Weather skill error:", error);
    return `无法获取 ${location} 的天气信息。错误详情：${error.message}`;
  }
}