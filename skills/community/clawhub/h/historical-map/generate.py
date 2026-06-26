"""
Historical Map Generator - OpenClaw Skill
Generate beautiful vintage-style historical maps from GeoJSON data.

Usage:
    python generate.py --year 1914 --region europe --output map.png
    python generate.py --year 1815 --region balkans --events events.json --output balkans.png
    python generate.py --year 1600 --region world --projection mollweide --output world_1600.png

Data source: https://github.com/aourednik/historical-basemaps
"""

import sys
import os
import json
import argparse
import warnings
warnings.filterwarnings('ignore')

def check_deps():
    """Check and report missing dependencies."""
    missing = []
    for mod in ['geopandas', 'matplotlib', 'numpy', 'PIL', 'pyproj', 'shapely']:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install geopandas matplotlib numpy Pillow pyproj shapely")
        sys.exit(1)

check_deps()

import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.font_manager import FontProperties
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from pyproj import Transformer
from shapely.geometry import box, Point
from shapely.ops import transform as shp_transform

# ===== DEFAULTS =====

# Region bounding boxes (lon_min, lat_min, lon_max, lat_max)
REGIONS = {
    'europe': (-25, 34, 45, 72),
    'balkans': (18, 34, 32, 48),
    'world': (-180, -60, 180, 85),
    'asia': (60, 0, 150, 70),
    'china': (70, 15, 140, 55),
    'mediterranean': (-10, 28, 42, 48),
    'middle_east': (25, 12, 65, 42),
    'americas': (-170, -60, -30, 75),
}

# Projection definitions
PROJECTIONS = {
    'laea': {
        'name': 'Lambert Azimuthal Equal Area',
        'proj': '+proj=laea +lat_0={lat_0} +lon_0={lon_0} +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs',
        'default_center': {'europe': (48, 15), 'balkans': (42, 25), 'world': (30, 0),
                          'asia': (35, 100), 'china': (35, 105), 'mediterranean': (38, 16),
                          'middle_east': (28, 44), 'americas': (10, -90)},
    },
    'lcc': {
        'name': 'Lambert Conformal Conic',
        'proj': '+proj=lcc +lat_1={lat_1} +lat_2={lat_2} +lat_0={lat_0} +lon_0={lon_0} +ellps=WGS84 +units=m +no_defs',
        'default_center': {'europe': (48, 15, 40, 55), 'balkans': (42, 25, 36, 48),
                          'china': (35, 105, 25, 47)},
    },
    'platecarree': {
        'name': 'Plate Carrée (Equirectangular)',
        'proj': '+proj=eqc +ellps=WGS84 +units=m +no_defs',
        'default_center': {},
    },
    'mollweide': {
        'name': 'Mollweide',
        'proj': '+proj=moll +lon_0={lon_0} +ellps=WGS84 +units=m +no_defs',
        'default_center': {'world': (30, 0), 'europe': (48, 15)},
    },
}

# HOI4-inspired vintage color palettes
PALETTES = {
    'vintage': {
        'ocean': '#3A5568', 'paper': '#F5ECD7', 'ink': '#2C1810',
        'countries': {
            'central': {'german': '#5A6E3F', 'austrian': '#C4A35A', 'ottoman': '#8B3A3A', 'bulgarian': '#6B7B3A'},
            'allied': {'british': '#8B6914', 'french': '#4169E1', 'russian': '#2E5E2E', 'italian': '#3CB371'},
            'neutral': {'default': '#D0C4A8'},
        },
        'alpha': 0.82,
    },
    'pastel': {
        'ocean': '#C5D5E0', 'paper': '#FAF6F0', 'ink': '#3C2415',
        'countries': {'neutral': {'default': '#E8DCC8'}},
        'alpha': 0.75,
    },
    'dark': {
        'ocean': '#1A1A2E', 'paper': '#0F0F1A', 'ink': '#E0C097',
        'countries': {'neutral': {'default': '#3A3A5A'}},
        'alpha': 0.85,
    },
    'satellite': {
        'ocean': '#2C3E50', 'paper': '#ECF0F1', 'ink': '#2C3E50',
        'countries': {'neutral': {'default': '#BDC3C7'}},
        'alpha': 0.70,
    },
}

# Pre-configured historical events (year -> events)
PRESET_EVENTS = {
    1914: [
        {"year": "1871", "label": "统一", "cn": "德意志统一", "color": "#5A6E3F"},
        {"year": "1878", "label": "战争", "cn": "俄土战争", "color": "#2E5E2E"},
        {"year": "1885", "label": "会议", "cn": "柏林会议", "color": "#8B6914"},
        {"year": "1894", "label": "同盟", "cn": "法俄同盟", "color": "#4169E1"},
        {"year": "1905", "label": "危机", "cn": "摩洛哥危机", "color": "#8B0000"},
        {"year": "1912", "label": "战争", "cn": "巴尔干战争", "color": "#B03020"},
        {"year": "1914", "label": "事件", "cn": "萨拉热窝", "color": "#A02020"},
    ],
}


class HistoricalMapGenerator:
    """Generate vintage-style historical maps."""

    def __init__(self, data_path=None, basemap_path=None, parchment_path=None):
        self.data_path = data_path
        self.basemap_path = basemap_path
        self.parchment_path = parchment_path
        self.palette = PALETTES['vintage']

        # Try to find a Chinese font
        self.font_path = None
        for fp in ['C:\\Windows\\Fonts\\msyh.ttc',
                    'C:\\Windows\\Fonts\\simhei.ttf',
                    'C:\\Windows\\Fonts\\simsun.ttc',
                    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']:
            if os.path.exists(fp):
                self.font_path = fp
                break

    def _get_projection_transformer(self, projection, region):
        """Create a projection transformer."""
        if projection == 'platecarree':
            return None  # No projection needed

        proj_info = PROJECTIONS.get(projection, PROJECTIONS['laea'])
        fmt = proj_info['proj']

        center = proj_info.get('default_center', {}).get(region)
        if projection == 'laea':
            lat_0, lon_0 = center or (0, 0)
            proj_str = fmt.format(lat_0=lat_0, lon_0=lon_0)
        elif projection == 'lcc':
            lat_0, lon_0, lat_1, lat_2 = center or (0, 0, 20, 60)
            proj_str = fmt.format(lat_0=lat_0, lon_0=lon_0, lat_1=lat_1, lat_2=lat_2)
        elif projection == 'mollweide':
            lon_0, lat_0 = (center[1], center[0]) if center else (0, 0)
            proj_str = fmt.format(lon_0=lon_0)
        else:
            proj_str = fmt.format(lon_0=0)

        return Transformer.from_crs("EPSG:4326", proj_str, always_xy=True).transform

    def _project_geom(self, geom, transformer):
        """Project a geometry, or return as-is if no projection."""
        if transformer is None:
            return geom
        return shp_transform(transformer, geom)

    def _project_point(self, lon, lat, transformer):
        """Project a single point."""
        if transformer is None:
            return Point(lon, lat)
        return shp_transform(transformer, Point(lon, lat))

    def generate(self, year, region='europe', projection='laea', events=None,
                 title=None, title_cn=None, quote=None, quote_author=None,
                 color_palette='vintage', dpi=300, figsize=(22, 16),
                 show_timeline=True, show_compass=True, show_scale=True,
                 show_grid=True, show_legend=True, show_rivers=False,
                 show_ocean_labels=True, parchment_overlay=True,
                 add_vignette=True, add_noise=True,
                 color_overrides=None, basemap_alpha=0.30,
                 output_path='output.png'):
        """
        Generate a historical map.

        Args:
            year: Historical year (must match a GeoJSON file from historical-basemaps)
            region: Region key from REGIONS dict, or (lon_min, lat_min, lon_max, lat_max) tuple
            projection: Projection key from PROJECTIONS dict
            events: List of timeline event dicts, or None for presets
            title: Main title (Latin/English)
            title_cn: Chinese subtitle
            quote: Decorative quote string
            quote_author: Quote attribution
            color_palette: Palette key from PALETTES
            dpi: Output DPI
            figsize: Figure size in inches (width, height)
            show_timeline: Show bottom timeline
            show_compass: Show compass rose
            show_scale: Show scale bar
            show_grid: Show lat/lon grid
            show_legend: Show legend
            show_rivers: Show major rivers
            show_ocean_labels: Show ocean/sea name labels
            parchment_overlay: Add parchment texture
            add_vignette: Add vignette darkening effect
            add_noise: Add paper grain noise
            color_overrides: Dict mapping country names to hex colors
            basemap_alpha: Basemap image transparency (0-1)
            output_path: Where to save the output image
        """
        self.palette = PALETTES.get(color_palette, PALETTES['vintage'])
        if color_overrides:
            for name, color in color_overrides.items():
                self._set_color(name, color)

        # Resolve region bbox
        if isinstance(region, str) and region in REGIONS:
            bbox = REGIONS[region]
        elif isinstance(region, (list, tuple)) and len(region) == 4:
            bbox = tuple(region)
        else:
            bbox = REGIONS['europe']

        # Load GeoJSON data
        if self.data_path and os.path.exists(self.data_path):
            print(f"Loading data from {self.data_path}...")
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            gdf = gpd.GeoDataFrame.from_features(data['features'])
        else:
            # Try to find data in historical-basemaps directory
            hb_paths = [
                os.path.expanduser('~/.openclaw/skills/historical-map/data'),
                os.path.expanduser('~/historical-basemaps/historical-basemaps-master/geojson'),
                './data',
            ]
            geojson_file = f'world_{year}.geojson'
            data_path = None
            for p in hb_paths:
                candidate = os.path.join(p, geojson_file)
                if os.path.exists(candidate):
                    data_path = candidate
                    break
            if data_path is None:
                raise FileNotFoundError(
                    f"GeoJSON for year {year} not found. "
                    f"Download from https://github.com/aourednik/historical-basemaps "
                    f"and place {geojson_file} in ./data/ directory.")
            print(f"Loading {data_path}...")
            gdf = gpd.read_file(data_path)

        # Filter to region
        region_box = box(*bbox)
        gdf_region = gdf[gdf.geometry.intersects(region_box)].copy()
        print(f"  {len(gdf_region)} regions in view")

        # Projection
        transformer = self._get_projection_transformer(projection, region if isinstance(region, str) else 'europe')
        if transformer:
            gdf_proj = gdf_region.copy()
            gdf_proj['geometry'] = gdf_proj.geometry.apply(lambda g: self._project_geom(g, transformer))
        else:
            gdf_proj = gdf_region

        # Basemap
        basemap_ok = False
        if self.basemap_path and os.path.exists(self.basemap_path):
            try:
                Image.MAX_IMAGE_PIXELS = 2000000000
                bi = Image.open(self.basemap_path)
                tw, th = bi.size
                x1 = int((bbox[0]+180)/360*tw)
                y1 = int((90-bbox[3])/180*th)
                x2 = int((bbox[2]+180)/360*tw)
                y2 = int((90-bbox[1])/180*th)
                crop = bi.crop((max(0,x1), max(0,y1), min(tw,x2), min(th,y2)))
                crop = ImageEnhance.Brightness(crop).enhance(0.62)
                crop = ImageEnhance.Color(crop).enhance(0.18)
                crop = crop.filter(ImageFilter.GaussianBlur(3))
                basemap_path = output_path + '.basemap.tmp.png'
                crop.save(basemap_path)
                basemap_ok = True
            except Exception as e:
                print(f"  Basemap error: {e}")

        # Create figure
        print("Drawing...")
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        fig.patch.set_facecolor(self.palette['paper'])
        ax.set_facecolor(self.palette['ocean'])

        if transformer:
            proj_bbox = self._project_geom(region_box, transformer)
        else:
            proj_bbox = region_box
        mxx, mxy, mxX, mxY = proj_bbox.bounds
        px, py = (mxX-mxx)*0.03, (mxY-mxy)*0.03
        ax.set_xlim(mxx-px, mxX+px)
        ax.set_ylim(mxy-py, mxY+py)

        if basemap_ok:
            bg = plt.imread(basemap_path)
            ax.imshow(bg, extent=[mxx, mxX, mxy, mxY], aspect='auto',
                     alpha=basemap_alpha, zorder=0)

        # Grid
        if show_grid:
            grid_pe = [pe.withStroke(linewidth=2.5, foreground=self.palette['paper'])]
            for lat in range(int(bbox[1])//5*5, int(bbox[3])+1, 5):
                pts = [self._project_point(lo, lat, transformer) for lo in range(int(bbox[0]), int(bbox[2])+1)]
                if len(pts) > 1:
                    ax.plot([p.x for p in pts], [p.y for p in pts],
                            color='#8B7355', linewidth=0.3, alpha=0.07, linestyle='--', zorder=1)
            for lon in range(int(bbox[0])//10*10, int(bbox[2])+1, 10):
                pts = [self._project_point(lon, la, transformer) for la in range(int(bbox[1]), int(bbox[3])+1)]
                if len(pts) > 1:
                    ax.plot([p.x for p in pts], [p.y for p in pts],
                            color='#8B7355', linewidth=0.3, alpha=0.07, linestyle='--', zorder=1)

        # Draw countries
        for idx, row in gdf_proj.iterrows():
            name = str(row.get("NAME", "")).strip()
            if name in ("nan", ""):
                continue
            color = self._get_country_color(name, row)
            gdf_proj.loc[[idx]].plot(ax=ax, color=color, edgecolor=self.palette['ink'],
                                      linewidth=0.5, alpha=self.palette['alpha'], zorder=2)

        # Ocean labels
        if show_ocean_labels:
            ocean_pe = [pe.withStroke(linewidth=6, foreground=self.palette['ocean'])]
            for lon, lat, text, fs in [
                (-10, 37, "ATLANTIC OCEAN", 13),
                (18, 35.5, "MEDITERRANEAN SEA", 10),
                (3, 58, "NORTH SEA", 9),
                (40, 44, "BLACK SEA", 9),
                (0, 44, "Bay of Biscay", 7),
            ]:
                if bbox[0] <= lon <= bbox[2] and bbox[1] <= lat <= bbox[3]:
                    pt = self._project_point(lon, lat, transformer)
                    ax.text(pt.x, pt.y, text, fontsize=fs, ha='center', va='center',
                            color='#8AA8B8', fontstyle='italic', alpha=0.30,
                            fontweight='bold', zorder=1, path_effects=ocean_pe, fontfamily='serif')

        # Compass
        if show_compass:
            self._draw_compass(ax, mxx, mxy, mxX, mxY)

        # Scale bar
        if show_scale:
            self._draw_scale(ax, mxx, mxy, mxX, mxY)

        # Legend
        if show_legend:
            self._draw_legend(ax)

        # Title
        title = title or f"ANNO DOMINI {self._year_to_roman(year) if year > 0 else f'{abs(year)} BC'}"
        title_cn = title_cn or f"Year {year}"
        deco = "=" * 40
        fig.text(0.5, 0.970, deco, fontsize=6, ha='center', color='#8B7355', alpha=0.5)
        fig.suptitle(title, fontsize=26, fontweight='bold', color=self.palette['ink'],
                    y=0.958, fontfamily='serif')
        if self.font_path:
            fig.text(0.5, 0.940, title_cn,
                     fontproperties=FontProperties(fname=self.font_path, size=15, weight='bold'),
                     ha='center', color='#5C4030')
        if quote:
            fig.text(0.5, 0.920, f'"{quote}"',
                     fontsize=9, ha='center', color='#6B5040', fontstyle='italic', fontfamily='serif')
            if quote_author:
                fig.text(0.5, 0.905, f"- {quote_author}",
                         fontsize=8, ha='center', color='#8B7355', fontfamily='serif')
        fig.text(0.5, 0.152, deco, fontsize=6, ha='center', color='#8B7355', alpha=0.5)

        # Timeline
        if show_timeline and events is not None:
            self._draw_timeline(fig, events)

        # Cleanup
        ax.set_axis_off()
        plt.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.15)

        # Footer
        proj_name = PROJECTIONS.get(projection, {}).get('name', projection)
        fig.text(0.5, 0.01,
                 f"Data: historical-basemaps | Projection: {proj_name} | Generated by Historical Map Skill",
                 fontsize=7, ha='center', color='#A09880')

        # Save raw
        raw_path = output_path + '.raw.tmp.png'
        plt.savefig(raw_path, dpi=dpi, bbox_inches='tight',
                    facecolor=fig.get_facecolor(), pad_inches=0.15)
        plt.close()
        print(f"  Saved raw: {raw_path}")

        # Post-processing
        print("Post-processing...")
        img = Image.open(raw_path)
        w, h = img.size

        if parchment_overlay and self.parchment_path and os.path.exists(self.parchment_path):
            parch = Image.open(self.parchment_path).resize((w, h), Image.LANCZOS).convert('RGBA')
            parch.putalpha(18)
            img = Image.alpha_composite(img.convert('RGBA'), parch).convert('RGB')

        if add_vignette:
            arr = np.array(img, dtype=np.float32)
            cy, cx = h/2, w/2
            md = np.sqrt(cx**2 + cy**2)
            yg, xg = np.mgrid[0:h, 0:w]
            dist = np.sqrt((xg-cx)**2 + (yg-cy)**2) / md
            vig = np.clip(1.0 - dist**1.5 * 0.22, 0, 1)
            for c in range(3):
                arr[:,:,c] *= vig
            img = Image.fromarray(arr.astype(np.uint8))

        if add_noise:
            arr = np.array(img, dtype=np.float32)
            noise = np.random.normal(0, 3, (h, w, 3))
            arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(arr)

        # Slight desaturation for vintage feel
        img = ImageEnhance.Color(img).enhance(0.86)
        img.save(output_path, quality=96)

        # Cleanup temp files
        for tmp in [raw_path, output_path + '.basemap.tmp.png']:
            if os.path.exists(tmp):
                os.remove(tmp)

        print(f"Done: {output_path} ({img.size[0]}x{img.size[1]})")
        return output_path

    def _get_country_color(self, name, row):
        """Get color for a country from palette or defaults."""
        if name in getattr(self, '_color_overrides', {}):
            return self._color_overrides[name]
        subj = str(row.get("SUBJECTO", ""))
        for group_name, group in self.palette.get('countries', {}).items():
            if isinstance(group, dict):
                for key, color in group.items():
                    if key.lower() in name.lower() or key.lower() in subj.lower():
                        return color
        return '#D0C4A8'

    def _set_color(self, name, color):
        """Override a country color."""
        if not hasattr(self, '_color_overrides'):
            self._color_overrides = {}
        self._color_overrides[name] = color

    def _draw_compass(self, ax, mxx, mxy, mxX, mxY):
        """Draw a compass rose."""
        cx = mxx + (mxX-mxx)*0.89
        cy = mxy + (mxY-mxy)*0.87
        cr = (mxX-mxx)*0.045
        ink = self.palette['ink']

        for rf, lw in [(1.0, 1.5), (0.85, 0.8), (0.5, 0.3)]:
            ax.add_patch(plt.Circle((cx, cy), cr*rf, fill=False,
                                     edgecolor='#5C4030', linewidth=lw, zorder=15, alpha=0.5))
        ax.add_patch(plt.Circle((cx, cy), cr*0.12, fill=True,
                                  facecolor='#5C4030', zorder=16, alpha=0.4))

        for angle, label, lf, lw, color in [
            (90,'N',1.0,2.5,'#8B0000'), (0,'E',0.8,1.2,'#5C4030'),
            (270,'S',0.8,1.2,'#5C4030'), (180,'W',0.8,1.2,'#5C4030'),
            (45,'',0.5,0.6,'#5C4030'), (315,'',0.5,0.6,'#5C4030'),
            (225,'',0.5,0.6,'#5C4030'), (135,'',0.5,0.6,'#5C4030'),
        ]:
            rad = np.radians(angle)
            ax.annotate('', xy=(cx+cr*lf*np.cos(rad), cy+cr*lf*np.sin(rad)),
                        xytext=(cx, cy),
                        arrowprops=dict(arrowstyle='->', color=color, lw=lw), zorder=16)
            if label:
                ax.text(cx+cr*1.25*np.cos(rad), cy+cr*1.25*np.sin(rad), label,
                        fontsize=9, fontweight='bold', color=color,
                        ha='center', va='center', zorder=16, fontfamily='serif')

    def _draw_scale(self, ax, mxx, mxy, mxX, mxY):
        """Draw a scale bar."""
        sx = mxx + (mxX-mxx)*0.05
        sy = mxy + (mxY-mxy)*0.08
        bw = (mxX-mxx)*0.08
        seg = bw/4
        ink = self.palette['ink']
        paper = self.palette['paper']
        bar_h = (mxY-mxy)*0.01
        for i in range(4):
            ax.add_patch(mpatches.Rectangle((sx+i*seg, sy-bar_h/2), seg, bar_h,
                         facecolor=ink if i%2==0 else paper,
                         edgecolor='#4A3828', linewidth=0.5, zorder=21))
        ax.text(sx+bw/2, sy+(mxY-mxy)*0.012, "1000 km",
                fontsize=9, fontweight='bold', color=ink, ha='center', va='bottom',
                zorder=21, fontfamily='serif')

    def _draw_legend(self, ax):
        """Draw a legend box."""
        ink = self.palette['ink']
        paper = self.palette['paper']
        handles = [
            mpatches.Patch(facecolor='#D0C4A8', edgecolor=ink, lw=0.5, label="Countries"),
            mpatches.Patch(facecolor='#F5ECD7', edgecolor=ink, lw=0.5, label="Land / 陆地"),
        ]
        ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.01, 0.01),
                  fontsize=9, framealpha=0.88, facecolor=paper, edgecolor='#8B7355')

    def _draw_timeline(self, fig, events):
        """Draw a bottom timeline."""
        if self.font_path:
            fig.text(0.5, 0.14, "Timeline / 时间线",
                     fontproperties=FontProperties(fname=self.font_path, size=13, weight='bold'),
                     ha='center', color='#5C4030')

        n = len(events)
        tw_span = 0.72
        sx0 = 0.5 - tw_span/2
        ly = 0.095
        xpos = [sx0 + tw_span*i/(n-1) for i in range(n)]

        for i, ev in enumerate(events):
            x = xpos[i]
            color = ev.get('color', '#5C4030')
            fig.text(x, ly+0.005, "●", fontsize=9, ha='center', color=color)
            fig.text(x, ly+0.030, ev.get('year', ''), fontsize=9, ha='center',
                     color=color, fontweight='bold')
            fig.text(x, ly+0.018, ev.get('label', ''), fontsize=7, ha='center',
                     color='#6B5B4D', fontfamily='serif', fontstyle='italic')
            cn_text = ev.get('cn', ev.get('text', ''))
            if self.font_path and cn_text:
                fig.text(x, ly-0.015, cn_text,
                         fontproperties=FontProperties(fname=self.font_path, size=10, weight='bold'),
                         ha='center', color=self.palette['ink'])

        fig.text(0.5, 0.035, "=" * 40, fontsize=6, ha='center', color='#8B7355', alpha=0.5)

    def _year_to_roman(self, year):
        """Convert year to Roman numerals."""
        val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
        syms = ['m','cm','d','cd','c','xc','l','xl','x','ix','v','iv','i']
        roman = ''
        i = 0
        while year > 0:
            for _ in range(year // val[i]):
                roman += syms[i]
                year -= val[i]
            i += 1
        return roman.upper()


def main():
    parser = argparse.ArgumentParser(description='Historical Map Generator')
    parser.add_argument('--year', type=int, required=True, help='Historical year')
    parser.add_argument('--region', type=str, default='europe', help='Region preset or lon_min,lat_min,lon_max,lat_max')
    parser.add_argument('--projection', type=str, default='laea', choices=PROJECTIONS.keys(), help='Map projection')
    parser.add_argument('--palette', type=str, default='vintage', choices=PALETTES.keys(), help='Color palette')
    parser.add_argument('--title', type=str, help='Main title')
    parser.add_argument('--title-cn', type=str, help='Chinese subtitle')
    parser.add_argument('--data', type=str, help='Path to GeoJSON file')
    parser.add_argument('--basemap', type=str, help='Path to satellite basemap image')
    parser.add_argument('--parchment', type=str, help='Path to parchment texture image')
    parser.add_argument('--events', type=str, help='Path to events JSON file')
    parser.add_argument('--dpi', type=int, default=300)
    parser.add_argument('--no-timeline', action='store_true')
    parser.add_argument('--no-compass', action='store_true')
    parser.add_argument('--no-postprocess', action='store_true')
    parser.add_argument('--output', type=str, default='historical_map.png')
    args = parser.parse_args()

    # Parse region
    if ',' in args.region and len(args.region.split(',')) == 4:
        region = tuple(float(x) for x in args.region.split(','))
    else:
        region = args.region

    # Events
    events = PRESET_EVENTS.get(args.year)
    if args.events:
        with open(args.events) as f:
            events = json.load(f)

    gen = HistoricalMapGenerator(
        data_path=args.data,
        basemap_path=args.basemap,
        parchment_path=args.parchment,
    )

    gen.generate(
        year=args.year,
        region=region,
        projection=args.projection,
        events=events,
        title=args.title,
        title_cn=args.title_cn,
        color_palette=args.palette,
        dpi=args.dpi,
        show_timeline=not args.no_timeline and events is not None,
        show_compass=not args.no_compass,
        parchment_overlay=not args.no_postprocess,
        add_vignette=not args.no_postprocess,
        add_noise=not args.no_postprocess,
        output_path=args.output,
    )


if __name__ == '__main__':
    main()
