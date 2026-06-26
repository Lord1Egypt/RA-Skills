# Science

A bundle of four live science data feeds: ISS tracking, earthquake monitoring, air quality, and NASA's Astronomy Picture of the Day.

## get_iss_location

Returns the current latitude and longitude of the International Space Station in real time.

## get_earthquakes

Recent earthquakes from the USGS. Filter by lookback window (1-30 days) and minimum magnitude (default 4.0). Results include magnitude, location description, depth, coordinates, and tsunami warning status.

```bash
curl -X POST https://gateway.pipeworx.io/science/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_earthquakes","arguments":{"days":7,"min_magnitude":5.0}}}'
```

## get_air_quality

Air quality measurements near any lat/lon from the OpenAQ network. Returns PM2.5, PM10, ozone, and other pollutant readings from the five closest monitoring stations.

## get_apod

NASA's Astronomy Picture of the Day. Pass a date (YYYY-MM-DD) or omit for today. Returns the image URL, HD URL, title, explanation, and copyright info.

## Connect your client

```json
{
  "mcpServers": {
    "science": {
      "url": "https://gateway.pipeworx.io/science/mcp"
    }
  }
}
```
