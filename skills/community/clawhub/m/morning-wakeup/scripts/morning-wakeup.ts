import { execFileSync } from "child_process";
import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

// ── WMO weather code → category ──────────────────────────────────────
const WMO_CATEGORIES: Record<number, string> = {
  0: "clear", 1: "clear",
  2: "cloudy", 3: "cloudy", 45: "cloudy", 48: "cloudy",
  51: "rain", 53: "rain", 55: "rain", 56: "rain", 57: "rain",
  61: "rain", 63: "rain", 65: "rain", 66: "rain", 67: "rain",
  80: "rain", 81: "rain", 82: "rain",
  71: "snow", 73: "snow", 75: "snow", 77: "snow", 85: "snow", 86: "snow",
  95: "storm", 96: "storm", 99: "storm",
};

const WMO_DESCRIPTIONS: Record<number, string> = {
  0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
  45: "Fog", 48: "Depositing rime fog",
  51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
  56: "Light freezing drizzle", 57: "Dense freezing drizzle",
  61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
  66: "Light freezing rain", 67: "Heavy freezing rain",
  71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
  77: "Snow grains",
  80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
  85: "Slight snow showers", 86: "Heavy snow showers",
  95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
};

const DEFAULT_PRESETS: Record<string, string> = {
  clear: "Morning Sunshine", cloudy: "Cloudy Morning",
  rain: "Rainy Day", snow: "Winter Morning", storm: "Stormy Ambient",
};

// ── CLI args ─────────────────────────────────────────────────────────
function parseArgs(): Record<string, string> {
  const args: Record<string, string> = {};
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "";
      args[key] = value;
    }
  }
  return args;
}

// ── Geocode ──────────────────────────────────────────────────────────
interface GeoResult {
  name: string; latitude: number; longitude: number; country: string;
}

async function geocode(location: string): Promise<GeoResult> {
  const latLonMatch = location.match(/^(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)$/);
  if (latLonMatch) {
    return { name: location, latitude: parseFloat(latLonMatch[1]), longitude: parseFloat(latLonMatch[2]), country: "Unknown" };
  }
  const url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Geocoding API error: ${res.status}`);
  const data = await res.json() as any;
  if (!data.results?.length) throw new Error(`Location not found: "${location}"`);
  const r = data.results[0];
  return { name: r.name, latitude: r.latitude, longitude: r.longitude, country: r.country };
}

// ── Fetch weather ────────────────────────────────────────────────────
async function fetchWeather(lat: number, lon: number, units: string) {
  const tempUnit = units === "fahrenheit" ? "fahrenheit" : "celsius";
  const params = new URLSearchParams({
    latitude: lat.toString(), longitude: lon.toString(),
    current: "temperature_2m,weather_code",
    temperature_unit: tempUnit, timezone: "auto", forecast_days: "1",
  });
  const url = `https://api.open-meteo.com/v1/forecast?${params}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Weather API error: ${res.status}`);
  return res.json() as any;
}

// ── Load presets ─────────────────────────────────────────────────────
function loadPresets(): Record<string, string> {
  const presetPath = resolve(dirname(fileURLToPath(import.meta.url)), "presets.json");
  try {
    return { ...DEFAULT_PRESETS, ...JSON.parse(readFileSync(presetPath, "utf-8")) };
  } catch {
    return { ...DEFAULT_PRESETS };
  }
}

// ── Sonos commands (safe: uses execFileSync, no shell interpolation) ─
function sonosExec(args: string[]): string {
  try {
    return execFileSync("sonos", args, { timeout: 15000, encoding: "utf-8" }).trim();
  } catch (err: any) {
    throw new Error(`Sonos command failed: sonos ${args.join(" ")}\n${err.message}`);
  }
}

// ── Main ─────────────────────────────────────────────────────────────
async function main() {
  const args = parseArgs();
  const location = args.location;
  const speaker = args.speaker;
  const volume = Math.max(0, Math.min(100, parseInt(args.volume || "15", 10)));
  const units = args.units || "celsius";

  if (!location) { console.error("Missing --location"); process.exit(1); }
  if (!speaker)  { console.error("Missing --speaker");  process.exit(1); }

  // 1. Fetch weather
  const geo = await geocode(location);
  console.error(`Location: ${geo.name}, ${geo.country}`);
  const weather = await fetchWeather(geo.latitude, geo.longitude, units);
  const weatherCode: number = weather.current.weather_code;
  const temp: number = weather.current.temperature_2m;
  const description = WMO_DESCRIPTIONS[weatherCode] || "Unknown";

  // 2. Map to preset
  const category = WMO_CATEGORIES[weatherCode] || "clear";
  const presets = loadPresets();
  const preset = presets[category] || DEFAULT_PRESETS.clear || "Morning Sunshine";

  console.error(`Weather: ${description} (${temp}°${units === "fahrenheit" ? "F" : "C"}), code=${weatherCode} → category=${category} → preset="${preset}"`);

  // 3. Set volume
  sonosExec(["volume", "set", String(volume), "--name", speaker]);
  console.error(`Volume set to ${volume}`);

  // 4. Play preset
  sonosExec(["favorites", "open", preset, "--name", speaker]);
  console.error(`Playing preset: ${preset}`);

  // 5. Output result
  const result = {
    success: true,
    location: geo.name,
    weather: { description, weather_code: weatherCode, temp, units },
    category,
    preset,
    speaker,
    volume,
  };
  console.log(JSON.stringify(result));
}

main().catch((err) => {
  console.error(err.message);
  console.log(JSON.stringify({ success: false, error: err.message }));
  process.exit(1);
});
