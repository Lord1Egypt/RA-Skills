# Weather

Current conditions and multi-day forecasts for any location on Earth. Temperatures in Fahrenheit, wind in mph.

## get_weather

Pass a latitude and longitude, get back: temperature, feels-like temperature, humidity percentage, weather conditions (clear, cloudy, rain, snow, thunderstorm, etc.), wind speed, and wind direction.

## get_forecast

Up to 16 days of daily forecasts. Each day includes the high, low, total precipitation in mm, and conditions.

## Example: current weather in San Francisco

```bash
curl -X POST https://gateway.pipeworx.io/weather/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_weather","arguments":{"latitude":37.7749,"longitude":-122.4194}}}'
```

## Example: 5-day forecast for London

```bash
curl -X POST https://gateway.pipeworx.io/weather/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_forecast","arguments":{"latitude":51.5074,"longitude":-0.1278,"days":5}}}'
```

Powered by Open-Meteo. No API key needed.

```json
{
  "mcpServers": {
    "weather": {
      "url": "https://gateway.pipeworx.io/weather/mcp"
    }
  }
}
```
