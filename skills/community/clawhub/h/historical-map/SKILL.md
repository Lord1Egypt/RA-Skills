---
name: historical-map
description: Generate beautiful vintage-style historical maps from GeoJSON data. Supports multiple projections, color palettes, timelines, compass roses, parchment overlays, and vignette effects. Perfect for history blogs, videos, articles, and educational content.
metadata:
  {
    "openclaw": {
      "emoji": "🗺️",
      "requires": {
        "pip": ["geopandas>=0.14", "matplotlib>=3.8", "numpy>=1.24", "Pillow>=10.0", "pyproj>=3.6", "shapely>=2.0"]
      },
      "install": [
        {
          "id": "pip-install",
          "kind": "pip",
          "packages": ["geopandas>=0.14", "matplotlib>=3.8", "numpy>=1.24", "Pillow>=10.0", "pyproj>=3.6", "shapely>=2.0"],
          "label": "Install map generation dependencies"
        }
      ]
    }
  }
keywords:
  - map
  - historical
  - geography
  - geojson
  - visualization
  - cartography
---

# Historical Map Generator

Generate beautiful vintage-style historical maps from GeoJSON data.

## Quick Start

```bash
# Install dependencies
pip install geopandas matplotlib numpy Pillow pyproj shapely

# Download historical GeoJSON data
git clone https://github.com/aourednik/historical-basemaps.git
# Copy world_YYYY.geojson files to ./data/

# Generate a map
python generate.py --year 1914 --region europe --output europe_1914.png
```

## What It Does

- **Historical boundaries** from 10,000 BC to 2010 AD (50+ time slices)
- **Multiple projections**: Lambert Azimuthal, Lambert Conformal Conic, Mollweide, Plate Carrée
- **4 color palettes**: Vintage (HOI4-inspired), Pastel, Dark, Satellite
- **Decorative elements**: Compass rose, scale bar, timeline, legend, ocean labels
- **Post-processing**: Parchment overlay, vignette darkening, paper grain noise
- **Customizable**: Override any country color, add custom events, swap basemap textures

## Available Time Slices

Commonly used years from historical-basemaps:
```
world_bc3000.geojson, world_bc1500.geojson, world_100.geojson
world_500.geojson, world_1000.geojson, world_1200.geojson
world_1400.geojson, world_1492.geojson, world_1600.geojson
world_1700.geojson, world_1783.geojson, world_1815.geojson
world_1880.geojson, world_1900.geojson, world_1914.geojson
world_1920.geojson, world_1930.geojson, world_1938.geojson
world_1945.geojson, world_1960.geojson, world_2000.geojson
```

## Usage Examples

### Basic: Europe 1914
```bash
python generate.py --year 1914 --region europe --output europe_1914.png
```

### World map with custom palette
```bash
python generate.py --year 1600 --region world --projection mollweide --palette dark --output world_1600.png
```

### China with custom colors
```bash
python generate.py --year 1400 --region china --palette pastel \
  --title "MING DYNASTY" --title-cn "明朝疆域" --output ming.png
```

### Custom region (Balkans)
```bash
python generate.py --year 1815 --region 18,34,32,48 --output balkans_1815.png
```

### With custom events timeline
Create `my_events.json`:
```json
[
  {"year": "1789", "label": "Revolution", "cn": "法国大革命", "color": "#4169E1"},
  {"year": "1804", "label": "Empire", "cn": "拿破仑称帝", "color": "#2E5E2E"},
  {"year": "1815", "label": "Fall", "cn": "滑铁卢", "color": "#8B0000"}
]
```
```bash
python generate.py --year 1815 --events my_events.json --output napoleon.png
```

### Custom country colors
```bash
python generate.py --year 1945 --region world \
  --title "POST-WAR WORLD" --title-cn "二战后的世界" \
  --palette vintage --output postwar.png
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--year` | required | Historical year (must match a GeoJSON file) |
| `--region` | `europe` | Region preset or `lon_min,lat_min,lon_max,lat_max` |
| `--projection` | `laea` | `laea`, `lcc`, `mollweide`, `platecarree` |
| `--palette` | `vintage` | `vintage`, `pastel`, `dark`, `satellite` |
| `--title` | auto | Main title (Latin/English) |
| `--title-cn` | auto | Chinese subtitle |
| `--data` | auto-detect | Path to GeoJSON file |
| `--basemap` | none | Path to satellite basemap image |
| `--parchment` | none | Path to parchment texture image |
| `--events` | auto-preset | Path to events JSON file |
| `--dpi` | 300 | Output resolution |
| `--no-timeline` | false | Disable bottom timeline |
| `--no-compass` | false | Disable compass rose |
| `--no-postprocess` | false | Skip vignette/noise effects |
| `--output` | `historical_map.png` | Output file path |

## Region Presets

| Key | Coverage |
|-----|----------|
| `europe` | Full European continent |
| `balkans` | Balkan Peninsula |
| `world` | Global view |
| `asia` | Asian continent |
| `china` | China and surroundings |
| `mediterranean` | Mediterranean basin |
| `middle_east` | Middle East |
| `americas` | North + South America |

## Color Palettes

### Vintage (Default)
HOI4-inspired desaturated military colors. Ocean: dark teal. Perfect for war maps.

### Pastel
Light, soft colors on off-white background. Great for educational content.

### Dark
Deep navy background with gold accents. Dramatic, cinematic feel.

### Satellite
Modern cartography style with clean lines. Professional and neutral.

## Post-Processing Pipeline

1. **Parchment overlay** — Semi-transparent parchment texture (alpha=18/255)
2. **Vignette** — Edge darkening for focal point emphasis
3. **Paper grain** — Subtle noise for aged paper texture
4. **Desaturation** — 14% color reduction for vintage feel

## Python API

```python
from generate import HistoricalMapGenerator

gen = HistoricalMapGenerator(
    data_path='data/world_1914.geojson',
    basemap_path='textures/satellite.jpg',
    parchment_path='textures/parchment.jpg',
)

gen.generate(
    year=1914,
    region='europe',
    projection='laea',
    title='EUROPA ANNO DOMINI MCMXIV',
    title_cn='第一次世界大战前夜的欧洲',
    color_palette='vintage',
    dpi=300,
    output_path='my_map.png',
)
```

## Data Source

[historical-basemaps](https://github.com/aourednik/historical-basemaps) by @aourednik.
50+ GeoJSON time slices covering 10,000 BC to 2010 AD.

**Note**: Border precision varies. The `BORDERPRECISION` field indicates accuracy (1=high, 3=approximate). Some regions (especially Balkans) may have minor gaps between neighboring territories. For publication-quality maps, consider manually editing the GeoJSON or using commercial data.

## Requirements

- Python 3.9+
- geopandas >= 0.14
- matplotlib >= 3.8
- numpy >= 1.24
- Pillow >= 10.0
- pyproj >= 3.6
- shapely >= 2.0

## License

MIT

## Credits

Developed by [Lumielle](https://github.com/muxueqingze) / OpenClaw Agent
Data: [historical-basemaps](https://github.com/aourednik/historical-basemaps) (CC BY 4.0)
