# 🗺️ Historical Map Generator / 历史地图生成器

[English](#english) | [中文](#中文)

---

<a id="english"></a>
## English

Generate beautiful vintage-style historical maps from GeoJSON data. Built for content creators, history bloggers, educators, and AI agents.

### Features

- 🌍 **50+ Historical Periods** — From 10,000 BC to 2010 AD
- 🎨 **4 Color Palettes** — Vintage (HOI4-inspired), Pastel, Dark, Satellite
- 📐 **4 Projections** — Lambert Azimuthal, Lambert Conformal Conic, Mollweide, Plate Carrée
- ✨ **Decorative Elements** — Compass rose, scale bar, timeline, legend, ocean labels
- 🖼️ **Post-Processing** — Parchment overlay, vignette, paper grain noise
- 🐍 **Python API** — Fully parameterized for integration into workflows
- 🤖 **OpenClaw Skill** — Install via ClawHub for AI agent integration

### Quick Start

```bash
# 1. Install dependencies
pip install geopandas matplotlib numpy Pillow pyproj shapely

# 2. Download historical data
git clone https://github.com/aourednik/historical-basemaps.git
cp historical-basemaps/historical-basemaps-master/geojson/world_*.geojson ./data/

# 3. Generate a map
python generate.py --year 1914 --region europe --output europe_1914.png
```

### Examples

| Command | Output |
|---------|--------|
| `--year 1914 --region europe` | Pre-WWI Europe with timeline |
| `--year 1600 --region world --projection mollweide` | Global Mollweide projection |
| `--year 1400 --region china --palette pastel` | Ming Dynasty China |
| `--year 1815 --region balkans --title "CONGRESS"` | Congress of Vienna Balkans |
| `--year 1945 --region world --palette dark` | Post-WWII world map |

### All Parameters

```bash
python generate.py \
  --year 1914 \              # Historical year
  --region europe \          # Region preset or lon_min,lat_min,lon_max,lat_max
  --projection laea \        # laea / lcc / mollweide / platecarree
  --palette vintage \        # vintage / pastel / dark / satellite
  --title "EUROPA MCMXIV" \  # Main title
  --title-cn "1914年欧洲" \   # Chinese subtitle
  --data path/to/data.geojson \
  --basemap textures/satellite.jpg \
  --parchment textures/parchment.jpg \
  --events events.json \     # Custom timeline events
  --dpi 300 \
  --output map.png
```

### Region Presets

`europe` · `balkans` · `world` · `asia` · `china` · `mediterranean` · `middle_east` · `americas`

### Custom Events

Create a JSON file with timeline events:
```json
[
  {"year": "1789", "label": "Revolution", "cn": "法国大革命", "color": "#4169E1"},
  {"year": "1804", "label": "Empire", "cn": "拿破仑称帝", "color": "#2E5E2E"}
]
```

### Python API

```python
from generate import HistoricalMapGenerator

gen = HistoricalMapGenerator()
gen.generate(
    year=1914,
    region='europe',
    projection='laea',
    title='EUROPA ANNO DOMINI MCMXIV',
    title_cn='第一次世界大战前夜的欧洲',
    output_path='my_map.png',
)
```

### Post-Processing Pipeline

1. **Parchment texture** — Semi-transparent overlay for aged paper look
2. **Vignette** — Subtle edge darkening for focal emphasis
3. **Paper grain** — Gaussian noise for authentic texture
4. **Desaturation** — 14% color reduction for vintage feel

### Data Source

[historical-basemaps](https://github.com/aourednik/historical-basemaps) by @aourednik (CC BY 4.0)
50+ GeoJSON time slices from 10,000 BC to 2010 AD.

> **Note**: Border precision varies by region. The `BORDERPRECISION` field indicates accuracy (1=high, 3=approximate). For publication-quality maps, consider manually editing GeoJSON data.

### Requirements

Python 3.9+ · geopandas · matplotlib · numpy · Pillow · pyproj · shapely

### License

MIT

---

<a id="中文"></a>
## 中文

用 GeoJSON 数据生成精美复古风格历史地图。为内容创作者、历史博主、教育工作者和 AI Agent 打造。

### 特性

- 🌍 **50+历史时期** — 公元前10000年到2010年
- 🎨 **4套配色方案** — 复古（HOI4风格）、柔粉、暗黑、卫星
- 📐 **4种投影方式** — 兰伯特等面积、兰伯特正形圆锥、摩尔魏德、等距圆柱
- ✨ **装饰元素** — 指南针玫瑰、比例尺、时间轴、图例、海洋标注
- 🖼️ **后期处理** — 羊皮纸纹理叠加、暗角效果、纸张颗粒噪点
- 🐍 **Python API** — 完全参数化，可集成到工作流中
- 🤖 **OpenClaw技能** — 通过 ClawHub 安装，支持 AI Agent 直接调用

### 快速开始

```bash
# 1. 安装依赖
pip install geopandas matplotlib numpy Pillow pyproj shapely

# 2. 下载历史数据
git clone https://github.com/aourednik/historical-basemaps.git
cp historical-basemaps/historical-basemaps-master/geojson/world_*.geojson ./data/

# 3. 生成地图
python generate.py --year 1914 --region europe --output europe_1914.png
```

### 示例

| 命令 | 输出 |
|------|------|
| `--year 1914 --region europe` | 一战前欧洲（含时间轴） |
| `--year 1600 --region world --projection mollweide` | 全球摩尔魏德投影 |
| `--year 1400 --region china --palette pastel` | 明朝疆域图 |
| `--year 1815 --region balkans --title "CONGRESS"` | 维也纳会议巴尔干地图 |
| `--year 1945 --region world --palette dark` | 二战后世界地图 |

### 完整参数

```bash
python generate.py \
  --year 1914 \              # 历史年份
  --region europe \          # 区域预设 或 经度_min,纬度_min,经度_max,纬度_max
  --projection laea \        # laea / lcc / mollweide / platecarree
  --palette vintage \        # vintage / pastel / dark / satellite
  --title "EUROPA MCMXIV" \  # 主标题
  --title-cn "1914年欧洲" \   # 中文副标题
  --data path/to/data.geojson \
  --basemap textures/satellite.jpg \
  --parchment textures/parchment.jpg \
  --events events.json \     # 自定义时间轴事件
  --dpi 300 \
  --output map.png
```

### 区域预设

`europe`（欧洲）· `balkans`（巴尔干）· `world`（全球）· `asia`（亚洲）· `china`（中国）· `mediterranean`（地中海）· `middle_east`（中东）· `americas`（美洲）

### 自定义事件

创建 JSON 文件定义时间轴事件：
```json
[
  {"year": "1789", "label": "Revolution", "cn": "法国大革命", "color": "#4169E1"},
  {"year": "1804", "label": "Empire", "cn": "拿破仑称帝", "color": "#2E5E2E"}
]
```

### Python API

```python
from generate import HistoricalMapGenerator

gen = HistoricalMapGenerator()
gen.generate(
    year=1914,
    region='europe',
    projection='laea',
    title='EUROPA ANNO DOMINI MCMXIV',
    title_cn='第一次世界大战前夜的欧洲',
    output_path='my_map.png',
)
```

### 后期处理流程

1. **羊皮纸纹理** — 半透明叠加，模拟古纸质感
2. **暗角效果** — 边缘渐暗，突出视觉焦点
3. **纸张颗粒** — 高斯噪点，增加真实纹理
4. **降低饱和度** — 14%降饱和，营造复古氛围

### 数据来源

[historical-basemaps](https://github.com/aourednik/historical-basemaps) by @aourednik（CC BY 4.0 协议）
50+个 GeoJSON 时间切片，覆盖公元前10000年到公元2010年。

> **注意**：边界精度因地区而异。`BORDERPRECISION` 字段标注精度（1=高，3=近似值）。如需出版级精度，建议手动编辑 GeoJSON 数据或使用商业数据。

### 系统要求

Python 3.9+ · geopandas · matplotlib · numpy · Pillow · pyproj · shapely

### 许可证

MIT
