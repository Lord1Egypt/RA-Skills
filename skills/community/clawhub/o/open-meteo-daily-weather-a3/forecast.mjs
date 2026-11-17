import { pathToFileURL } from 'node:url';

export async function forecastForLocation(location, fetchImpl = fetch) {
  if (typeof location !== 'string' || location.trim().length < 2 || location.length > 100) {
    throw new Error('Provide a city, region, or postal code');
  }
  const geoUrl = new URL('https://geocoding-api.open-meteo.com/v1/search');
  geoUrl.search = new URLSearchParams({ name: location.trim(), count: '1' }).toString();
  const geoResponse = await fetchImpl(geoUrl, { signal: AbortSignal.timeout(8000) });
  if (!geoResponse.ok) throw new Error(`Location lookup unavailable: HTTP ${geoResponse.status}`);
  const place = (await geoResponse.json()).results?.[0];
  if (!place || !Number.isFinite(place.latitude) || !Number.isFinite(place.longitude) || !place.timezone) {
    throw new Error('Location not found');
  }

  const forecastUrl = new URL('https://api.open-meteo.com/v1/forecast');
  forecastUrl.search = new URLSearchParams({
    latitude: String(place.latitude), longitude: String(place.longitude),
    daily: 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
    temperature_unit: 'fahrenheit', timezone: place.timezone, forecast_days: '1',
  }).toString();
  const forecastResponse = await fetchImpl(forecastUrl, { signal: AbortSignal.timeout(8000) });
  if (!forecastResponse.ok) throw new Error(`Forecast unavailable: HTTP ${forecastResponse.status}`);
  const daily = (await forecastResponse.json()).daily ?? {};
  const highF = daily.temperature_2m_max?.[0];
  const lowF = daily.temperature_2m_min?.[0];
  const rainChancePercent = daily.precipitation_probability_max?.[0];
  if (![highF, lowF, rainChancePercent].every(Number.isFinite) || !daily.time?.[0]) {
    throw new Error('Forecast incomplete');
  }
  return { date: daily.time[0], location: [place.name, place.admin1, place.country_code].filter(Boolean).join(', '),
    highF, lowF, rainChancePercent, source: 'Open-Meteo', sourceUrl: forecastUrl.toString() };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(await forecastForLocation(process.argv[2] ?? process.env.WEATHER_LOCATION))); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
