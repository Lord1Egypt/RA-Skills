# Examples

## Geocode
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts geocode --address "Tokyo Tower"
```

## Reverse Geocode
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts reverse-geocode --latlng 35.6585805,139.7454329
```

## Directions (driving, default)
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts directions \
  --origin "Shibuya Station" \
  --dest "Tokyo Tower"
```

## Directions (transit)
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts directions \
  --origin "Shibuya Station" \
  --dest "Tokyo Tower" \
  --mode TRANSIT
```

## Places Text Search
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts places-search --query "ramen near Shinjuku"
```

## Places Text Search (with location bias)
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts places-search \
  --query "coffee" \
  --location 35.6585,139.7454 \
  --radius 1000
```

## Places Nearby
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts places-nearby \
  --location 35.6585,139.7454 \
  --radius 500 \
  --type restaurant
```

## Place Detail
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts place-detail \
  --place-id ChIJCewJkL2LGGAR2HQ6PeTfivU
```

## Elevation
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts elevation \
  --locations "35.6585,139.7454|34.0522,-118.2437"
```

## Timezone
```bash
GOOGLE_MAPS_API_KEY=your_key bun scripts/gmaps.ts timezone \
  --location 35.6585,139.7454 \
  --timestamp 1672531200
```
