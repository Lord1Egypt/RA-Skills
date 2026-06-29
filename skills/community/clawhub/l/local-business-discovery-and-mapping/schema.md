# Local Business Discovery and Mapping Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `local-business-discovery-and-mapping`

x402 availability: not enabled for this product.

## `geocode`

Action slug: `geocode`

Price: `20` credits

Convert a street address or place name into geographic coordinates, place ID, and address components.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | yes | The street address or place name to geocode. |

Sample parameters:

```json
{
  "address": "example address"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "The street address or place name to geocode.",
    "required": true,
    "type": "string"
  }
}
```

## `nearby_search`

Action slug: `nearby-search`

Price: `20` credits

Search for places near a location by category. Requires either an address or latitude/longitude coordinates. Automatically geocodes addresses to coordinates.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Street address or area name to search near. Will be geocoded to coordinates automatically. Required if latitude/longitude are not provided. |
| `excluded_types` | `array` | no | Place category groups to exclude from search results. |
| `included_types` | `array` | no | Place category groups to include in search results. Each group expands to multiple specific place types. |
| `latitude` | `number` | no | Latitude coordinate of search center (-90 to 90). Required if address is not provided. |
| `longitude` | `number` | no | Longitude coordinate of search center (-180 to 180). Required if address is not provided. |
| `max_results` | `integer` | no | Maximum number of results to return. |
| `radius_meters` | `integer` | no | Search radius in meters around the center point. |

Sample parameters:

```json
{
  "address": "example address",
  "excluded_types": [
    "restaurants_and_dining"
  ],
  "included_types": [
    "restaurants_and_dining"
  ],
  "latitude": -90,
  "longitude": -180,
  "max_results": 50,
  "radius_meters": 1000
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Street address or area name to search near. Will be geocoded to coordinates automatically. Required if latitude/longitude are not provided.",
    "required": false,
    "type": "string"
  },
  "excluded_types": {
    "description": "Place category groups to exclude from search results.",
    "items": {
      "enum": [
        "restaurants_and_dining",
        "cafes_and_light_fare",
        "bars_and_nightlife",
        "bakeries_and_sweets",
        "food_retail_and_markets",
        "food_services",
        "lodging_and_accommodation",
        "shopping_general",
        "shopping_specialty_retail",
        "automotive",
        "health_and_medical",
        "beauty_and_personal_care",
        "fitness_and_sports",
        "parks_and_nature",
        "entertainment_and_attractions",
        "arts_and_culture",
        "performing_arts_and_venues",
        "religious_sites",
        "education",
        "government_and_civic",
        "financial_services",
        "professional_services",
        "home_services_and_contractors",
        "transportation",
        "travel_and_tourism",
        "residential",
        "geographic_administrative",
        "outdoor_recreation",
        "community_and_social",
        "miscellaneous_services"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "included_types": {
    "description": "Place category groups to include in search results. Each group expands to multiple specific place types.",
    "items": {
      "enum": [
        "restaurants_and_dining",
        "cafes_and_light_fare",
        "bars_and_nightlife",
        "bakeries_and_sweets",
        "food_retail_and_markets",
        "food_services",
        "lodging_and_accommodation",
        "shopping_general",
        "shopping_specialty_retail",
        "automotive",
        "health_and_medical",
        "beauty_and_personal_care",
        "fitness_and_sports",
        "parks_and_nature",
        "entertainment_and_attractions",
        "arts_and_culture",
        "performing_arts_and_venues",
        "religious_sites",
        "education",
        "government_and_civic",
        "financial_services",
        "professional_services",
        "home_services_and_contractors",
        "transportation",
        "travel_and_tourism",
        "residential",
        "geographic_administrative",
        "outdoor_recreation",
        "community_and_social",
        "miscellaneous_services"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "latitude": {
    "description": "Latitude coordinate of search center (-90 to 90). Required if address is not provided.",
    "maximum": 90,
    "minimum": -90,
    "required": false,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude coordinate of search center (-180 to 180). Required if address is not provided.",
    "maximum": 180,
    "minimum": -180,
    "required": false,
    "type": "number"
  },
  "max_results": {
    "default": 50,
    "description": "Maximum number of results to return.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "radius_meters": {
    "default": 1000,
    "description": "Search radius in meters around the center point.",
    "maximum": 50000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `reverse_geocode`

Action slug: `reverse-geocode`

Price: `20` credits

Convert latitude/longitude coordinates into a human-readable address with place ID and address components.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `latitude` | `number` | yes | Latitude coordinate (-90 to 90). |
| `longitude` | `number` | yes | Longitude coordinate (-180 to 180). |

Sample parameters:

```json
{
  "latitude": -90,
  "longitude": -180
}
```

Generated JSON parameter schema:

```json
{
  "latitude": {
    "description": "Latitude coordinate (-90 to 90).",
    "maximum": 90,
    "minimum": -90,
    "required": true,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude coordinate (-180 to 180).",
    "maximum": 180,
    "minimum": -180,
    "required": true,
    "type": "number"
  }
}
```

## `text_search`

Action slug: `text-search`

Price: `20` credits

Search for places using a free-text query. Optionally bias results toward a specific location.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Bias results toward this address. Optional location context. |
| `latitude` | `number` | no | Latitude to bias results toward (-90 to 90). |
| `longitude` | `number` | no | Longitude to bias results toward (-180 to 180). |
| `max_results` | `integer` | no | Maximum number of results to return. |
| `query` | `string` | yes | Text search query (e.g., 'best pizza in Brooklyn', 'Statue of Liberty'). |
| `radius_meters` | `integer` | no | Bias radius in meters around the location. |

Sample parameters:

```json
{
  "address": "example address",
  "latitude": -90,
  "longitude": -180,
  "max_results": 50,
  "query": "example search query",
  "radius_meters": 1000
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Bias results toward this address. Optional location context.",
    "required": false,
    "type": "string"
  },
  "latitude": {
    "description": "Latitude to bias results toward (-90 to 90).",
    "maximum": 90,
    "minimum": -90,
    "required": false,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude to bias results toward (-180 to 180).",
    "maximum": 180,
    "minimum": -180,
    "required": false,
    "type": "number"
  },
  "max_results": {
    "default": 50,
    "description": "Maximum number of results to return.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Text search query (e.g., 'best pizza in Brooklyn', 'Statue of Liberty').",
    "required": true,
    "type": "string"
  },
  "radius_meters": {
    "default": 1000,
    "description": "Bias radius in meters around the location.",
    "maximum": 50000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```
