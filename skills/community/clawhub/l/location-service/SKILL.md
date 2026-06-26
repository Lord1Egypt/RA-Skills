---
name: location-service
description: Location-based services including geocoding (coordinates to address and address to coordinates), distance calculation, and integration with weather data. Use when you need to process geographic coordinates, get location information from coordinates, calculate distances between points, or get weather for specific geographic locations. Also supports parsing Google Maps URLs to extract coordinates.
---

# Location Service

## Overview

This skill provides tools for working with geographic locations. It can convert between coordinates and addresses, calculate distances between points, and retrieve weather information for specific locations using the OpenStreetMap Nominatim service for geocoding and integrating with the existing weather skill.

**New:** you can now paste a Google Maps URL directly (both desktop and short `maps.app.goo.gl` links) and the service will automatically extract the coordinates, then proceed with the same pipeline as if you had typed them manually.

## Quick Start

### Get address from coordinates
Send coordinates in format `lat,lon` (e.g., `40.7128,-74.0060`) to get the corresponding address.

### Get coordinates from address
Send an address or place name to get its latitude and longitude coordinates.

### Calculate distance
Provide two sets of coordinates to calculate the distance between them.

### Get weather for location
Provide coordinates or address to get current weather information.

### **[NEW] Paste a Google Maps link**
Paste any Google Maps URL — the service extracts the coordinates automatically and then behaves exactly like the `lat,lon` input flow described above.

Supported URL formats:
- `https://www.google.com/maps?q=41.9028,12.4964`
- `https://www.google.com/maps/place/Rome/@41.9028,12.4964,15z`
- `https://maps.google.com/?ll=41.9028,12.4964`
- `https://maps.app.goo.gl/XXXXXXX` (short link — resolved automatically)

## Geocoding Functions

### Reverse Geocoding (Coordinates → Address)
Takes latitude and longitude coordinates and returns a human-readable address.

### Forward Geocoding (Address → Coordinates)
Takes an address, place name, or landmark and returns latitude/longitude coordinates.

### Distance Calculation
Calculates the distance between two geographic points using the Haversine formula.

### Google Maps URL Parsing
Extracts latitude and longitude from a Google Maps URL (including short links resolved via HTTP redirect).

## Weather Integration
Leverages the existing weather skill to provide meteorological data for any set of coordinates.

## Usage Examples

- `41.9028,12.4964` → Returns address for Rome, Italy coordinates
- `Colosseum, Rome` → Returns coordinates for the Colosseum
- `41.9028,12.4964 to 40.7128,-74.0060` → Calculates distance between Rome and New York
- `weather for 41.9028,12.4964` → Gets weather for Rome coordinates
- `https://maps.app.goo.gl/XXXXXXX` → **Extracts coordinates from the Google Maps link**, then returns address
- `https://www.google.com/maps/place/Colosseum/@41.8902,12.4922,17z` → Extracts `41.8902,12.4922` → returns address

## Technical Details

- Uses Nominatim (OpenStreetMap) for geocoding services
- Supports both decimal degrees and degree/minute/second formats
- Distance calculations use the Haversine formula for accuracy
- Integrates with existing weather skill for meteorological data
- Google Maps URL parsing uses regex on the URL string; short `maps.app.goo.gl` links are resolved by following the HTTP redirect (no API key required)
- All services are free and don't require API keys for basic usage

## Resources

### scripts/
Contains executable Python scripts for geocoding and distance calculations:

- `geocode_reverse.py` - Convert coordinates to address
- `geocode_forward.py` - Convert address to coordinates
- `distance_calc.py` - Calculate distance between two points
- `weather_integration.py` - Helper for getting weather data
- **`parse_google_maps_url.py`** - **[NEW] Extract lat/lon from a Google Maps URL**

### references/
Documentation about geocoding services and usage guidelines:

- `nominatim_api.md` - Details about the OpenStreetMap Nominatim API
- *examples.md* - Common use cases and example workflows

### assets/
(Currently unused - reserved for future map templates or location icons)
