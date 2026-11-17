# Travel Search System - Enhanced Capabilities

## Overview
This enhanced search system provides multiple fallback mechanisms for finding location information when building the travel database.

## Features Implemented ✅

### 1. API Integration
- **LocationAPI** (`location_api.py`) - Supports Amap and Baidu Maps APIs
- Requires API keys configured in `search_config.ini`

### 2. Backup Search Engines  
- **EnhancedSearchManager** (`enhanced_search.py`) - Primary search with fallbacks
- DuckDuckGo as primary source (most reliable)
- Bing as backup when DuckDuckGo fails

### 3. Local Cache System
- **LocationCache** (`location_cache.py`) - Offline access to frequently searched locations
- Automatic cache expiration (30 days by default)
- Reduces API calls and speeds up repeated searches

### 4. Multi-source Verification
- **MultiSourceVerifier** (`multi_source_verify.py`) - Comprehensive verification across platforms
- Supports Dianping, Xiaohongshu, TripAdvisor (when APIs available)
- Provides cross-platform validation of location data

## Quick Start

### Basic Search (No API Keys Required)
```bash
python3 scripts/enhanced_search.py search "文昌码头老爸茶"
```

### With API Keys (Enhanced Results)
1. Set API keys in your local shell or project `.env`, not in `search_config.ini`:
   - `AMAP_API_KEY` (高德地图)
   - `BAIDU_MAPS_API_KEY` (百度地图)
   - `GOOGLE_PLACES_API_KEY`

2. Run enhanced search:
```bash
python3 scripts/enhanced_search.py search "海口老爸茶"
```

## Search Priority Order
1. **Local Cache** (fastest) - Check if location was recently searched
2. **DuckDuckGo** (primary web source) - Most reliable fallback  
3. **Bing Search** (backup) - When DuckDuckGo fails
4. **Location APIs** (enhanced) - If API keys configured
5. **Multi-source Verification** (comprehensive) - Cross-platform validation

## Configuration Options

Edit `search_config.ini` to customize:
- Default search engine preference
- Maximum results per source  
- Cache expiration period
- Enable/disable specific features

## Troubleshooting

### DuckDuckGo Search Failing
```bash
# Check if ddgs command is available  
which ddgs

# If not found, install the package
pip3 install duckduckgo-search

# Add the user-level Python scripts directory to PATH if needed.
```

### API Keys Not Working  
- Ensure keys are set locally in environment variables or the project `.env` (not in chat)
- Verify API quotas haven't been exceeded  
- Check that APIs are enabled for your account

## Future Enhancements
- [ ] Add more search engines (Google, Yahoo)  
- [ ] Implement web scraping for platforms without APIs
- [ ] Add machine learning to rank search results  
- [ ] Create visual map integration with location data
