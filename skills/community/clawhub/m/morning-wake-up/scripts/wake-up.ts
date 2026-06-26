import { parseArgs } from "node:util";

// ── Types ──────────────────────────────────────────────────────────────
interface Preset {
  wmo_codes: number[];
  favorite: string;
  volume: number;
}

interface Presets {
  [category: string]: Preset;
}

interface WeatherCurrent {
  weather_code: number;
  temp: number;
}

// ── Preset matching ────────────────────────────────────────────────────
async function loadPresets(presetsPath: string): Promise<Presets> {
  const file = Bun.file(presetsPath);
  if (!(await file.exists())) {
    throw new Error(`Presets file not found: ${presetsPath}`);
  }
  return await file.json();
}

function matchCategory(weatherCode: number, presets: Presets): { category: string; preset: Preset } {
  for (const [category, preset] of Object.entries(presets)) {
    if (preset.wmo_codes.includes(weatherCode)) {
      return { category, preset };
    }
  }
  // Default to cloudy if no match (matches SKILL.md spec)
  const fallback = presets["cloudy"] ?? Object.values(presets)[0];
  return { category: "cloudy", preset: fallback };
}

// ── Weather fetch ──────────────────────────────────────────────────────
async function fetchWeather(location: string, units: string): Promise<WeatherCurrent> {
  // Geocode
  const latLonMatch = location.match(/^(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)$/);
  let lat: number, lon: number;

  if (latLonMatch) {
    lat = parseFloat(latLonMatch[1]);
    lon = parseFloat(latLonMatch[2]);
  } else {
    const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`;
    const geoRes = await fetch(geoUrl);
    if (!geoRes.ok) throw new Error(`Geocoding failed: ${geoRes.status}`);
    const geoData = await geoRes.json();
    if (!geoData.results?.length) throw new Error(`Location not found: "${location}"`);
    lat = geoData.results[0].latitude;
    lon = geoData.results[0].longitude;
  }

  const tempUnit = units === "fahrenheit" ? "fahrenheit" : "celsius";
  const params = new URLSearchParams({
    latitude: lat.toString(),
    longitude: lon.toString(),
    current: "temperature_2m,weather_code",
    temperature_unit: tempUnit,
    timezone: "auto",
  });

  const wxUrl = `https://api.open-meteo.com/v1/forecast?${params}`;
  const wxRes = await fetch(wxUrl);
  if (!wxRes.ok) throw new Error(`Weather API failed: ${wxRes.status}`);
  const wxData = await wxRes.json();

  return {
    weather_code: wxData.current.weather_code,
    temp: wxData.current.temperature_2m,
  };
}

// ── Sonos control ──────────────────────────────────────────────────────
async function sonosPlay(speaker: string, favorite: string, volume: number): Promise<void> {
  const setVol = Bun.spawn(["sonos", "volume", "set", String(volume), "--name", speaker]);
  const volExit = await setVol.exited;
  if (volExit !== 0) throw new Error(`Failed to set volume on "${speaker}"`);

  const playFav = Bun.spawn(["sonos", "favorites", "open", favorite, "--name", speaker]);
  const favExit = await playFav.exited;
  if (favExit !== 0) throw new Error(`Failed to open favorite "${favorite}" on "${speaker}"`);
}

// ── Main ───────────────────────────────────────────────────────────────
async function main() {
  const { values } = parseArgs({
    options: {
      location: { type: "string" },
      speaker: { type: "string" },
      volume: { type: "string", default: "" },
      units: { type: "string", default: "celsius" },
    },
    strict: true,
  });

  if (!values.location) {
    console.error("Error: --location is required");
    process.exit(1);
  }
  if (!values.speaker) {
    console.error("Error: --speaker is required");
    process.exit(1);
  }

  const presetsPath = import.meta.dir + "/presets.json";
  const presets = await loadPresets(presetsPath);

  console.error(`Fetching weather for ${values.location}...`);
  const weather = await fetchWeather(values.location, values.units);
  console.error(`Weather code: ${weather.weather_code}, temp: ${weather.temp}`);

  const { category, preset } = matchCategory(weather.weather_code, presets);
  const rawVolume = values.volume ? parseInt(values.volume, 10) : preset.volume;
  const volume = Math.max(0, Math.min(100, rawVolume));

  console.error(`Matched category: ${category} → favorite: "${preset.favorite}", volume: ${volume}`);
  await sonosPlay(values.speaker, preset.favorite, volume);

  const result = {
    status: "ok",
    location: values.location,
    speaker: values.speaker,
    weather_code: weather.weather_code,
    temp: weather.temp,
    category,
    favorite: preset.favorite,
    volume,
  };
  console.log(JSON.stringify(result));
}

main().catch((err) => {
  console.error(err.message);
  console.log(JSON.stringify({ status: "error", error: err.message }));
  process.exit(1);
});
