# LeafEngines API Reference

## Base URL
`https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/`

## Authentication
All requests require an `x-api-key` header with your API key.

## Rate Limits
Based on your subscription tier:

| Tier | Requests/Month | Rate Limit |
|------|----------------|------------|
| Starter | 50,000 | 10 req/sec |
| Pro | 200,000 | 25 req/sec |
| Enterprise | 1,000,000 | 100 req/sec |

## Endpoints

### Health Check
`GET /api/health`

Check API service status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-26T08:00:00Z",
  "version": "1.0.0"
}
```

### Soil Analysis
`POST /soil-analysis`

Analyze soil composition and provide recommendations.

**Request Body:**
```json
{
  "latitude": 33.7490,
  "longitude": -84.3880,
  "soil_type": "loam",
  "depth_cm": 30,
  "organic_matter_percent": 2.5
}
```

**Response:**
```json
{
  "analysis": {
    "ph_level": 6.8,
    "nitrogen_ppm": 45,
    "phosphorus_ppm": 22,
    "potassium_ppm": 180,
    "organic_matter": 2.5,
    "texture": "loam",
    "moisture_percent": 18.5
  },
  "recommendations": [
    "Add 50 lbs/acre of nitrogen fertilizer",
    "Maintain current phosphorus levels",
    "Consider cover cropping for organic matter"
  ],
  "suitable_crops": ["corn", "soybeans", "wheat", "cotton"]
}
```

### Weather Forecast
`GET /weather-forecast`

Get weather forecast for location.

**Query Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate  
- `days` (optional): Forecast days (1-7, default: 3)

**Example:**
`GET /weather-forecast?latitude=33.7490&longitude=-84.3880&days=5`

**Response:**
```json
{
  "location": {
    "latitude": 33.7490,
    "longitude": -84.3880,
    "name": "Atlanta, GA"
  },
  "forecast": [
    {
      "date": "2026-03-26",
      "high_c": 22,
      "low_c": 12,
      "precipitation_mm": 0,
      "humidity_percent": 65,
      "wind_speed_kmh": 15,
      "conditions": "Sunny"
    }
  ]
}
```

### Crop Recommendation
`POST /crop-recommendation`

Recommend crops based on soil and climate.

**Request Body:**
```json
{
  "latitude": 33.7490,
  "longitude": -84.3880,
  "season": "spring",
  "water_availability": "medium",
  "market_demand": ["vegetables", "grains"]
}
```

**Response:**
```json
{
  "recommended_crops": [
    {
      "name": "Corn",
      "suitability_score": 0.85,
      "planting_window": "April 15 - May 15",
      "expected_yield_kg_ha": 9500,
      "water_requirement_mm": 500,
      "market_price_usd_kg": 0.18
    }
  ],
  "rotation_suggestions": [
    "Corn → Soybeans → Wheat",
    "Cotton → Peanuts → Cover crop"
  ]
}
```

### Pest Detection
`POST /pest-detection`

Identify common pests from symptoms.

**Request Body:**
```json
{
  "crop": "tomato",
  "symptoms": ["yellow leaves", "holes in leaves", "stunted growth"],
  "location": "southeast_us",
  "photos": ["base64_encoded_image_data"]
}
```

**Response:**
```json
{
  "detected_pests": [
    {
      "name": "Tomato Hornworm",
      "confidence": 0.92,
      "treatment": "Apply Bacillus thuringiensis (Bt)",
      "prevention": "Use row covers, handpick larvae"
    }
  ],
  "integrated_pest_management": {
    "biological": "Release Trichogramma wasps",
    "chemical": "Neem oil application",
    "cultural": "Crop rotation with non-solanaceous plants"
  }
}
```

### Irrigation Scheduling
`POST /irrigation-schedule`

Optimize water usage.

**Request Body:**
```json
{
  "crop": "corn",
  "growth_stage": "vegetative",
  "soil_moisture_percent": 45,
  "weather_forecast": "hot_dry",
  "irrigation_system": "drip"
}
```

**Response:**
```json
{
  "schedule": {
    "next_irrigation": "2026-03-27T06:00:00Z",
    "duration_minutes": 120,
    "water_volume_liters": 4500,
    "efficiency_score": 0.88
  },
  "recommendations": [
    "Water in early morning to reduce evaporation",
    "Consider adding mulch to retain soil moisture",
    "Monitor soil moisture daily during hot periods"
  ]
}
```

### Yield Prediction
`POST /yield-prediction`

Predict crop yield.

**Request Body:**
```json
{
  "crop": "wheat",
  "planting_date": "2026-10-15",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "management_practices": ["no-till", "cover_crops", "precision_fert"]
}
```

**Response:**
```json
{
  "predicted_yield": {
    "kg_per_hectare": 4200,
    "confidence_interval": [3950, 4450],
    "comparison_to_average": "+12%"
  },
  "key_factors": [
    {"factor": "Soil quality", "impact": "high", "direction": "positive"},
    {"factor": "Spring rainfall", "impact": "medium", "direction": "unknown"}
  ]
}
```

### Market Prices
`GET /market-prices`

Get agricultural commodity prices.

**Query Parameters:**
- `commodity` (optional): Specific commodity (corn, wheat, soybeans, etc.)
- `location` (optional): Market location
- `date` (optional): Historical date (YYYY-MM-DD)

**Example:**
`GET /market-prices?commodity=corn&location=chicago`

**Response:**
```json
{
  "prices": [
    {
      "commodity": "Corn",
      "market": "Chicago Board of Trade",
      "price_usd_per_bushel": 4.85,
      "change_percent": 1.2,
      "date": "2026-03-26",
      "unit": "bushel"
    }
  ],
  "trend": "upward",
  "seasonal_average": 4.65
}
```

### Sustainability Score
`POST /sustainability-score`

Calculate environmental impact score.

**Request Body:**
```json
{
  "farm_size_ha": 100,
  "crops": ["corn", "soybeans", "wheat"],
  "practices": ["no-till", "cover_crops", "integrated_pest_mgmt"],
  "water_source": "rainfall",
  "energy_source": "solar"
}
```

**Response:**
```json
{
  "score": 78,
  "breakdown": {
    "soil_health": 85,
    "water_use": 72,
    "biodiversity": 65,
    "carbon_footprint": 82,
    "economic_sustainability": 76
  },
  "improvements": [
    "Add buffer strips along waterways (+5 points)",
    "Implement rotational grazing (+8 points)",
    "Install solar panels for irrigation (+6 points)"
  ]
}
```

### Farm Planning
`POST /farm-planning`

Create seasonal farm plan.

**Request Body:**
```json
{
  "farm_size_ha": 50,
  "location": {"latitude": 38.9072, "longitude": -77.0369},
  "goals": ["maximize_yield", "reduce_input_costs", "improve_soil_health"],
  "budget_usd": 50000
}
```

**Response:**
```json
{
  "annual_plan": {
    "spring": ["Plant corn", "Apply fertilizer", "Start irrigation"],
    "summer": ["Monitor pests", "Weed control", "Harvest wheat"],
    "fall": ["Plant cover crops", "Soil testing", "Equipment maintenance"],
    "winter": ["Planning", "Training", "Infrastructure repairs"]
  },
  "budget_allocation": {
    "seeds": 12000,
    "fertilizer": 8000,
    "labor": 15000,
    "equipment": 10000,
    "contingency": 5000
  },
  "expected_outcomes": {
    "revenue_usd": 85000,
    "profit_margin": 0.41,
    "soil_health_improvement": "+15%"
  }
}
```

## Error Responses

All errors return JSON with:

```json
{
  "error": {
    "code": "invalid_api_key",
    "message": "Invalid or missing API key",
    "details": "Please check your x-api-key header"
  }
}
```

**Common Error Codes:**
- `invalid_api_key` - Missing or invalid API key
- `rate_limit_exceeded` - Too many requests
- `invalid_parameters` - Missing or invalid parameters
- `service_unavailable` - API temporarily unavailable
- `insufficient_quota` - Monthly request limit reached

## SDKs and Libraries

### Python
```python
import requests

api_key = "your_api_key_here"
headers = {"x-api-key": api_key}

response = requests.get(
    "https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/api/health",
    headers=headers
)
```

### JavaScript/Node.js
```javascript
const response = await fetch(
  'https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/api/health',
  {
    headers: {
      'x-api-key': 'your_api_key_here'
    }
  }
);
```

### cURL
```bash
curl -H "x-api-key: your_api_key_here" \
  https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/api/health
```

## Support
- GitHub: https://github.com/QWarranto/leafengines-claude-mcp
- Discord: #mcp channel in Claude Discord
- Email: Support via GitHub issues