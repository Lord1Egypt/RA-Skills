#!/usr/bin/env python3
"""Pet Sitter Client Intake Form Generator — v5.

Features:
- YAML config file support for business presets
- Fillable PDF form fields for digital workflows
- Home access section (keys, alarm, wifi)
- Enhanced pet behavior/temperament fields
- Multi-pet page generation
- Service-type templates (boarding, walking, drop-in)
"""

import argparse
import os
from pathlib import Path

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Flowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfform

DEFAULT_CONFIG = {
    "business_name": "Your Business Name",
    "sitter_name": "",
    "services": "Pet Sitting, Dog Walking, Boarding",
    "location": "",
    "contact": "",
    "service_type": "general",  # general, boarding, walking, drop_in
    "num_pets": 1,
    "include_home_access": True,
    "fillable": True,  # Generate fillable PDF fields by default
    "theme": "lavender",  # Color theme name or "custom"
    "colors": {},  # Custom color overrides (when theme is "custom")
    "output": "client_intake_form.pdf",  # Output filename
}


# ── Color Themes ───────────────────────────────────────────────────────────────
THEMES = {
    "lavender": {
        "primary": "#DDD6F3",       # Light lavender - section headers, backgrounds
        "primary_mid": "#B8ABDF",   # Medium lavender - borders, lines
        "primary_dark": "#6B5B9E",  # Dark lavender - headings, checkbox borders
        "accent": "#FAC8A0",        # Peach - decorative elements
        "accent_light": "#FEF0E7",  # Light peach - hero background, highlights
        "text": "#2D2926",          # Near-black - main text
        "text_muted": "#6B6560",    # Warm gray - labels, secondary text
        "text_light": "#B0A9A4",    # Light gray - notes, hints
    },
    "ocean": {
        "primary": "#D4E8F2",       # Light blue
        "primary_mid": "#8BC4E0",   # Medium blue
        "primary_dark": "#2B7A9E",  # Dark teal
        "accent": "#F9D977",        # Sandy yellow
        "accent_light": "#FFF8E7",  # Cream
        "text": "#1A3A4A",          # Dark blue-gray
        "text_muted": "#4A6670",    # Muted teal
        "text_light": "#8A9EA6",    # Light blue-gray
    },
    "forest": {
        "primary": "#D5E8D4",       # Light sage
        "primary_mid": "#97C9A0",   # Medium green
        "primary_dark": "#4A7C59",  # Forest green
        "accent": "#F4D03F",        # Golden yellow
        "accent_light": "#FDF9E7",  # Light cream
        "text": "#2D3A2E",          # Dark green-gray
        "text_muted": "#5A6B5C",    # Muted green
        "text_light": "#9AAA9C",    # Light sage
    },
    "rose": {
        "primary": "#F8E1E8",       # Light pink
        "primary_mid": "#E8B4C4",   # Medium rose
        "primary_dark": "#B85C7A",  # Deep rose
        "accent": "#C9A87C",        # Warm tan
        "accent_light": "#FDF5F0",  # Blush cream
        "text": "#3D2B32",          # Dark burgundy
        "text_muted": "#6B5560",    # Muted mauve
        "text_light": "#A8929A",    # Dusty rose
    },
    "sunset": {
        "primary": "#FFE4D6",       # Light coral
        "primary_mid": "#FFAA85",   # Medium orange
        "primary_dark": "#D4652F",  # Burnt orange
        "accent": "#7EC8E3",        # Sky blue
        "accent_light": "#FFF5EE",  # Seashell
        "text": "#3D2516",          # Dark brown
        "text_muted": "#6B5144",    # Warm brown
        "text_light": "#A89080",    # Tan
    },
    "neutral": {
        "primary": "#E8E8E8",       # Light gray
        "primary_mid": "#CCCCCC",   # Medium gray
        "primary_dark": "#666666",  # Dark gray
        "accent": "#B8D4E8",        # Soft blue
        "accent_light": "#F5F5F5",  # Off-white
        "text": "#333333",          # Charcoal
        "text_muted": "#666666",    # Medium gray
        "text_light": "#999999",    # Light gray
    },
    "midnight": {
        "primary": "#E0E4F0",       # Pale blue-gray
        "primary_mid": "#9BA4C0",   # Slate blue
        "primary_dark": "#4A5578",  # Deep blue-gray
        "accent": "#C5A880",        # Warm gold
        "accent_light": "#F0EDE8",  # Warm white
        "text": "#2A2D35",          # Near-black blue
        "text_muted": "#555A68",    # Muted slate
        "text_light": "#888D9A",    # Light slate
    },
}


def get_theme_colors(config):
    """Get color palette from theme name or custom colors."""
    theme_name = config.get("theme", "lavender")
    custom_colors = config.get("colors", {})
    
    # Start with base theme
    if theme_name == "custom":
        base_colors = THEMES["lavender"].copy()  # Default base for custom
    elif theme_name in THEMES:
        base_colors = THEMES[theme_name].copy()
    else:
        print(f"⚠️  Unknown theme '{theme_name}', using 'lavender'")
        base_colors = THEMES["lavender"].copy()
    
    # Apply custom color overrides
    for key, value in custom_colors.items():
        if key in base_colors:
            base_colors[key] = value
        else:
            print(f"⚠️  Unknown color key '{key}', ignoring")
    
    # Convert hex strings to reportlab colors
    return {k: colors.HexColor(v) for k, v in base_colors.items()}


def list_themes():
    """Print available themes."""
    print("\nAvailable themes:")
    print("-" * 50)
    for name, palette in THEMES.items():
        print(f"  {name:12} - Primary: {palette['primary']}, Accent: {palette['accent']}")
    print()
    print("Use --theme <name> or set 'theme: <name>' in config.yaml")
    print("For custom colors, set 'theme: custom' and define 'colors:' in config.\n")


def load_config(config_path=None):
    """Load config from YAML file, falling back to defaults."""
    config = DEFAULT_CONFIG.copy()
    
    if config_path:
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            print("   Using default settings instead.")
            return config
            
        if not YAML_AVAILABLE:
            print("=" * 60)
            print("❌ ERROR: PyYAML is required to load config files!")
            print("   Install it with: pip install pyyaml")
            print("   ")
            print("   Your config file was NOT loaded. Using defaults.")
            print("=" * 60)
            return config
            
        with open(config_path, "r") as f:
            user_config = yaml.safe_load(f) or {}
            config.update(user_config)
            print(f"📄 Loaded config from: {config_path}")
    
    return config


# Default colors (will be overridden by theme)
# These are kept as module-level for backward compatibility with Flowable classes
THEME_COLORS = None  # Set by build_form() before rendering

WHITE = colors.white
PAGE_W = 7.0 * inch   # usable width (letter - margins)


def _c(key):
    """Get color from current theme. Helper for cleaner code."""
    return THEME_COLORS[key] if THEME_COLORS else colors.HexColor("#000000")


# ── Custom checkbox row ────────────────────────────────────────────────────────
class CheckboxRow(Flowable):
    """Draws proper open white-filled checkboxes — never unicode blobs."""
    def __init__(self, options, per_row=4, box_size=9, font_size=8.5):
        super().__init__()
        self.options   = options
        self.per_row   = per_row
        self.box_size  = box_size
        self.font_size = font_size
        n_rows = -(-len(options) // per_row)
        self.height = n_rows * (box_size + 16)
        self.width  = 0

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        col_width = self.width / self.per_row
        box = self.box_size
        for i, label in enumerate(self.options):
            row = i // self.per_row
            col = i % self.per_row
            x = col * col_width
            y = self.height - (row + 1) * (box + 16) + 5
            c.setStrokeColor(_c("primary_dark"))
            c.setFillColor(WHITE)
            c.rect(x, y, box, box, stroke=1, fill=1)
            c.setFillColor(_c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(x + box + 6, y + 1.5, label)


# ── Fillable form field helpers ────────────────────────────────────────────────
class FillableTextField(Flowable):
    """A fillable text field for digital forms.
    
    Args:
        name: Unique field name
        width: Field width in points
        height: Field height in points (auto-increased for multiline)
        multiline: If True, allows multiple lines with text wrapping
        maxlen: Maximum character limit (0 = unlimited)
    """
    def __init__(self, name, width, height=18, multiline=False, maxlen=0):
        super().__init__()
        self.field_name = name
        self.field_width = width
        self.multiline = multiline
        self.maxlen = maxlen
        # Multiline fields need more height for usability
        if multiline and height < 36:
            self.field_height = 36
        else:
            self.field_height = height
        self.width = width
        self.height = self.field_height

    def wrap(self, availWidth, availHeight):
        return self.field_width, self.field_height

    def draw(self):
        c = self.canv
        # Convert local (0,0) to absolute page coordinates
        abs_x, abs_y = c.absolutePosition(0, 0)
        form = c.acroForm
        
        # Build field flags
        flags = 'multiline' if self.multiline else ''
        
        form.textfield(
            name=self.field_name,
            x=abs_x,
            y=abs_y,
            width=self.field_width,
            height=self.field_height,
            borderWidth=0.5,
            borderColor=_c("primary_mid"),
            fillColor=WHITE,
            textColor=_c("text"),
            fontSize=9 if not self.multiline else 8,
            fieldFlags=flags,
            maxlen=self.maxlen if self.maxlen > 0 else None,
        )


class FillableCheckbox(Flowable):
    """A fillable checkbox for digital forms."""
    def __init__(self, name, label, box_size=12, font_size=9):
        super().__init__()
        self.field_name = name
        self.label = label
        self.box_size = box_size
        self.font_size = font_size
        self.width = 200
        self.height = box_size + 4

    def wrap(self, availWidth, availHeight):
        return availWidth, self.height

    def draw(self):
        c = self.canv
        # Convert local (0,0) to absolute page coordinates
        abs_x, abs_y = c.absolutePosition(0, 0)
        form = c.acroForm
        form.checkbox(
            name=self.field_name,
            x=abs_x,
            y=abs_y,
            size=self.box_size,
            borderWidth=0.5,
            borderColor=_c("primary_dark"),
            fillColor=WHITE,
            checked=False,
        )
        c.setFillColor(_c("text"))
        c.setFont("Helvetica", self.font_size)
        c.drawString(self.box_size + 6, 2, self.label)


class FillableCheckboxRow(Flowable):
    """Row of fillable checkboxes for digital forms."""
    def __init__(self, field_prefix, options, per_row=4, box_size=12, font_size=9):
        super().__init__()
        self.field_prefix = field_prefix
        self.options = options
        self.per_row = per_row
        self.box_size = box_size
        self.font_size = font_size
        n_rows = -(-len(options) // per_row)
        self.height = n_rows * (box_size + 16)
        self.width = 0

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        form = c.acroForm
        col_width = self.width / self.per_row
        box = self.box_size
        
        for i, label in enumerate(self.options):
            row = i // self.per_row
            col = i % self.per_row
            local_x = col * col_width
            local_y = self.height - (row + 1) * (box + 16) + 5
            
            # Convert local coords to absolute page coordinates
            abs_x, abs_y = c.absolutePosition(local_x, local_y)
            
            safe_label = label.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
            field_name = f"{self.field_prefix}_{safe_label}"
            
            form.checkbox(
                name=field_name,
                x=abs_x,
                y=abs_y,
                size=box,
                borderWidth=0.5,
                borderColor=_c("primary_dark"),
                fillColor=WHITE,
                checked=False,
            )
            c.setFillColor(_c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(local_x + box + 6, local_y + 2, label)


class VaxCheckboxRow(Flowable):
    """Compact inline checkboxes for vaccination status (Yes/No/Exempt or N/A)."""
    def __init__(self, field_prefix, options, box_size=10, font_size=8):
        super().__init__()
        self.field_prefix = field_prefix
        self.options = options
        self.box_size = box_size
        self.font_size = font_size
        self.height = box_size + 6
        self.width = 0

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        form = c.acroForm
        box = self.box_size
        
        # Calculate spacing for options
        num_options = len(self.options)
        spacing = self.width / num_options
        
        for i, label in enumerate(self.options):
            local_x = i * spacing
            local_y = 0
            
            # Convert local coords to absolute page coordinates
            abs_x, abs_y = c.absolutePosition(local_x, local_y)
            
            safe_label = label.replace(" ", "_").replace("/", "_")
            field_name = f"{self.field_prefix}_{safe_label}"
            
            form.checkbox(
                name=field_name,
                x=abs_x,
                y=abs_y,
                size=box,
                borderWidth=0.5,
                borderColor=_c("primary_dark"),
                fillColor=WHITE,
                checked=False,
            )
            c.setFillColor(_c("text"))
            c.setFont("Helvetica", self.font_size)
            c.drawString(local_x + box + 4, local_y + 1, label)


# ── Style helpers ──────────────────────────────────────────────────────────────
def sty():
    """Create paragraph styles using current theme colors."""
    s = {}
    def ps(name, **kw):
        defaults = dict(fontName="Helvetica", fontSize=9, textColor=_c("text"), leading=13,
                        leftIndent=0, firstLineIndent=0, bulletIndent=0)
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    s["title"]    = ps("title",    fontName="Helvetica-Bold", fontSize=22, textColor=_c("primary_dark"), alignment=TA_CENTER, spaceAfter=4, leading=28)
    s["subtitle"] = ps("subtitle", fontSize=11, textColor=_c("text_muted"), alignment=TA_CENTER, spaceAfter=3)
    s["contact"]  = ps("contact",  fontSize=9,  textColor=_c("text_muted"), alignment=TA_CENTER, spaceAfter=2)
    s["svc"]      = ps("svc",      fontSize=8.5, textColor=_c("text_muted"), alignment=TA_CENTER)
    s["sec"]      = ps("sec",      fontName="Helvetica-Bold", fontSize=11, textColor=_c("primary_dark"))
    s["lbl"]      = ps("lbl",      fontName="Helvetica-Bold", fontSize=8.5, textColor=_c("text_muted"), spaceAfter=3, leading=12)
    s["sublbl"]   = ps("sublbl",   fontName="Helvetica-Bold", fontSize=9,   textColor=_c("primary_dark"), spaceAfter=3, leading=13)
    s["note"]     = ps("note",     fontName="Helvetica-Oblique", fontSize=8, textColor=_c("text_light"), spaceAfter=6, leading=11)
    s["body"]     = ps("body",     fontSize=8.5, textColor=_c("text"), spaceAfter=3, leading=13)
    s["foot"]     = ps("foot",     fontSize=7.5, textColor=_c("text_light"), alignment=TA_CENTER)
    s["th"]       = ps("th",       fontName="Helvetica-Bold", fontSize=8.5, textColor=_c("primary_dark"), leading=11)
    s["td"]       = ps("td",       fontSize=8.5, textColor=_c("text_muted"), leading=11)
    s["office"]   = ps("office",   fontName="Helvetica-Oblique", fontSize=7.5, textColor=_c("text_light"), alignment=TA_CENTER)
    return s


def sp(h=0.1):
    return Spacer(1, h * inch)

def hr(color=None, thick=1.0, after=8):
    """Horizontal rule. Uses accent color if none specified."""
    return HRFlowable(width="100%", thickness=thick, color=color or _c("accent"), spaceAfter=after)

def sec_hdr(title, s):
    """Section header band — no emoji dependency, reliable across all PDF viewers."""
    t = Table([[Paragraph(title, s["sec"])]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), _c("primary")),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
    ]))
    return t

def para_row(text, style):
    """Wrap a single Paragraph in a full-width Table so it sits flush left,
    matching the LEFTPADDING=0 behaviour of field/two_col/three_col."""
    t = Table([[Paragraph(text, style)]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t

def field(label, s, extra_space=24, extra_lines=1, fillable=False, field_name=None, multiline=None):
    """Label + one or more write-on underlines (or fillable text fields).
    
    Args:
        label: Field label text
        s: Styles dict
        extra_space: Space after field (for print version)
        extra_lines: Number of lines (for print version); if >1, fillable becomes multiline
        fillable: Whether to generate interactive form field
        field_name: Unique name for fillable field
        multiline: Force multiline mode (auto-detected from extra_lines if None)
    """
    cell = []
    if label:
        cell.append(Paragraph(label, s["lbl"]))
    
    if fillable and field_name:
        # Auto-detect multiline from extra_lines if not explicitly set
        is_multiline = multiline if multiline is not None else (extra_lines > 1)
        
        if is_multiline:
            height = max(40, 22 * extra_lines)  # Taller for multiline
        else:
            height = 20
        
        cell.append(FillableTextField(field_name, PAGE_W - 4, height=height, multiline=is_multiline))
        cell.append(Spacer(1, extra_space - 10 if not is_multiline else 6))
    else:
        for _ in range(extra_lines):
            cell.append(HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=extra_space))
    
    t = Table([[cell]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return [t]

def two_col(left_label, right_label, s, lw=None, rw=None, fillable=False, field_names=None):
    """Two fields side by side. Column widths default to exactly PAGE_W total."""
    gutter = 0.25 * inch
    lw = lw or (PAGE_W - gutter) / 2
    rw = rw or (PAGE_W - gutter) / 2
    
    if fillable and field_names:
        cell_l = [
            Paragraph(left_label, s["lbl"]),
            FillableTextField(field_names[0], lw - 4, height=18),
            Spacer(1, 10),
        ]
        cell_r = [
            Paragraph(right_label, s["lbl"]),
            FillableTextField(field_names[1], rw - 4, height=18),
            Spacer(1, 10),
        ]
    else:
        cell_l = [
            Paragraph(left_label,  s["lbl"]),
            HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=20),
        ]
        cell_r = [
            Paragraph(right_label, s["lbl"]),
            HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=20),
        ]
    
    t = Table([[cell_l, cell_r]], colWidths=[lw, rw + gutter])
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(0,-1),  0),
        ("RIGHTPADDING",  (0,0),(0,-1),  gutter),
        ("LEFTPADDING",   (1,0),(1,-1),  0),
        ("RIGHTPADDING",  (1,0),(1,-1),  0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t

def three_col(labels, s, widths=None, fillable=False, field_names=None):
    """Three fields side by side. widths = content widths; a 0.1*inch gutter is added per column."""
    gutter = 0.1 * inch
    widths = widths or [(PAGE_W - 3 * gutter) / 3] * 3
    cells = []
    
    if fillable and field_names:
        for lbl, w, fname in zip(labels, widths, field_names):
            cells.append([
                Paragraph(lbl, s["lbl"]),
                FillableTextField(fname, w - 4, height=18),
                Spacer(1, 10),
            ])
    else:
        for lbl, w in zip(labels, widths):
            cells.append([
                Paragraph(lbl, s["lbl"]),
                HRFlowable(width="100%", thickness=0.8, color=_c("primary_mid"), spaceAfter=20),
            ])
    
    col_widths = [w + gutter for w in widths]
    t = Table([cells], colWidths=col_widths)
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), gutter),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t

def pg_hdr(name, label, s):
    return [
        Paragraph(name, s["title"]),
        Paragraph(f"Client &amp; Pet Intake Form  \u00b7  {label}", s["subtitle"]),
        hr(None, 1.5, 12),  # Uses accent color
    ]

def auth_block(title, body, s):
    """Full-width left-aligned authorization block."""
    content = [
        Paragraph(f"<b>{title}</b>", s["sublbl"]),
        Paragraph(body, s["body"]),
    ]
    t = Table([[content]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), _c("accent_light")),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    return t


# ── Section builders ───────────────────────────────────────────────────────────
def build_home_access_section(s, fillable=False):
    """Home access section for in-home pet sitting."""
    elements = []
    elements += [sec_hdr("HOME ACCESS & PROPERTY INFORMATION", s), sp(0.2)]
    
    elements.append(para_row("Key / Entry Information", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Entry method:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow("entry_method", 
            ["Key provided", "Lockbox", "Garage code", "Door code", "Hidden key", "Other"],
            per_row=3
        ))
    else:
        elements.append(CheckboxRow(
            ["Key provided", "Lockbox", "Garage code", "Door code", "Hidden key", "Other"],
            per_row=3
        ))
    elements.append(sp(0.1))
    
    elements += field("Lockbox / key location", s, fillable=fillable, field_name="key_location")
    elements += field("Entry code(s)", s, fillable=fillable, field_name="entry_codes")
    elements += field("Alarm code & disarm instructions", s, fillable=fillable, field_name="alarm_code", multiline=True)
    elements.append(sp(0.12))
    
    elements.append(para_row("Property Details", s["sublbl"]))
    elements.append(sp(0.1))
    elements += field("WiFi network & password", s, fillable=fillable, field_name="wifi_info")
    elements += field("Parking instructions", s, fillable=fillable, field_name="parking", multiline=True)
    elements += field("Thermostat / HVAC notes", s, fillable=fillable, field_name="thermostat", multiline=True)
    elements += field("Off-limits rooms or areas", s, fillable=fillable, field_name="off_limits")
    elements += field("Other house rules (TV on for pet, mail, plants, etc.)", s, extra_lines=2, 
                      fillable=fillable, field_name="house_rules")
    
    return elements


def build_pet_behavior_section(s, pet_num=1, fillable=False):
    """Enhanced pet behavior and temperament section."""
    prefix = f"pet{pet_num}_" if pet_num > 1 else ""
    elements = []
    
    elements += [sec_hdr("BEHAVIOR & TEMPERAMENT", s), sp(0.2)]
    
    elements.append(para_row("Good with:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}good_with",
            ["Strangers", "Children", "Other dogs", "Cats", "Small animals"],
            per_row=5
        ))
    else:
        elements.append(CheckboxRow(
            ["Strangers", "Children", "Other dogs", "Cats", "Small animals"],
            per_row=5
        ))
    elements.append(sp(0.1))
    
    elements.append(para_row("Known fears / triggers:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}fears",
            ["Thunderstorms", "Fireworks", "Vacuum", "Doorbell", "Men", "Hats/uniforms", "None known"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["Thunderstorms", "Fireworks", "Vacuum", "Doorbell", "Men", "Hats/uniforms", "None known"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Other triggers or sensitivities", s, fillable=fillable, 
                      field_name=f"{prefix}other_triggers", multiline=True)
    
    elements.append(para_row("Separation anxiety:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}separation",
            ["None", "Mild (whines)", "Moderate (barks/paces)", "Severe (destructive)"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["None", "Mild (whines)", "Moderate (barks/paces)", "Severe (destructive)"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements.append(para_row("Escape artist?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}escape",
            ["No", "Yes — door dasher", "Yes — fence jumper/digger", "Yes — gate opener"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["No", "Yes — door dasher", "Yes — fence jumper/digger", "Yes — gate opener"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Commands pet knows (sit, stay, come, etc.)", s, fillable=fillable,
                      field_name=f"{prefix}commands")
    elements += field("Recall reliability off-leash (1-10, or N/A)", s, fillable=fillable,
                      field_name=f"{prefix}recall")
    
    return elements


def build_potty_section(s, pet_num=1, fillable=False):
    """Potty and house-training section."""
    prefix = f"pet{pet_num}_" if pet_num > 1 else ""
    elements = []
    
    elements.append(para_row("Potty / House Training", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Potty trained?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}potty_trained",
            ["Fully trained", "Mostly (occasional accidents)", "In progress", "Uses pads/litter"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["Fully trained", "Mostly (occasional accidents)", "In progress", "Uses pads/litter"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Potty schedule / signals they give when needing to go", s, fillable=fillable,
                      field_name=f"{prefix}potty_schedule", multiline=True)
    elements += field("Preferred potty area (backyard spot, specific walk route, etc.)", s, 
                      fillable=fillable, field_name=f"{prefix}potty_area", multiline=True)
    
    return elements


def build_sleep_crate_section(s, pet_num=1, fillable=False):
    """Sleep and crate training section."""
    prefix = f"pet{pet_num}_" if pet_num > 1 else ""
    elements = []
    
    elements.append(para_row("Sleep & Crate", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Where does pet sleep?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}sleep_location",
            ["Own bed", "Crate", "Owner's bed", "Couch", "Anywhere"],
            per_row=5
        ))
    else:
        elements.append(CheckboxRow(
            ["Own bed", "Crate", "Owner's bed", "Couch", "Anywhere"],
            per_row=5
        ))
    elements.append(sp(0.1))
    
    elements.append(para_row("Crate trained?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}crate_trained",
            ["Yes — loves it", "Yes — tolerates it", "No — do not crate", "N/A"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["Yes — loves it", "Yes — tolerates it", "No — do not crate", "N/A"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Crate location / bedtime routine", s, fillable=fillable,
                      field_name=f"{prefix}bedtime_routine", multiline=True)
    
    return elements


def build_service_specific_section(s, service_type, fillable=False):
    """Service-specific fields based on service type."""
    elements = []
    
    if service_type == "walking":
        elements += [sec_hdr("DOG WALKING DETAILS", s), sp(0.2)]
        elements += field("Leash & harness location", s, fillable=fillable, field_name="leash_location")
        elements += field("Poop bag location", s, fillable=fillable, field_name="poop_bags")
        
        elements.append(para_row("Leash behavior:", s["lbl"]))
        if fillable:
            elements.append(FillableCheckboxRow("leash_behavior",
                ["Loose leash", "Pulls — needs management", "Reactive on leash", "Heel trained"],
                per_row=4
            ))
        else:
            elements.append(CheckboxRow(
                ["Loose leash", "Pulls — needs management", "Reactive on leash", "Heel trained"],
                per_row=4
            ))
        elements.append(sp(0.1))
        
        elements += field("Preferred walking route / areas to avoid", s, fillable=fillable,
                          field_name="walk_route", multiline=True)
        elements += field("Walk duration preference", s, fillable=fillable, field_name="walk_duration")
        
    elif service_type == "boarding":
        elements += [sec_hdr("BOARDING DETAILS", s), sp(0.2)]
        
        elements.append(para_row("Items to bring:", s["lbl"]))
        if fillable:
            elements.append(FillableCheckboxRow("boarding_items",
                ["Food", "Bed/blanket", "Favorite toys", "Medications", "Crate", "Treats"],
                per_row=3
            ))
        else:
            elements.append(CheckboxRow(
                ["Food", "Bed/blanket", "Favorite toys", "Medications", "Crate", "Treats"],
                per_row=3
            ))
        elements.append(sp(0.1))
        
        elements += field("Drop-off date & time", s, fillable=fillable, field_name="dropoff_datetime")
        elements += field("Pick-up date & time", s, fillable=fillable, field_name="pickup_datetime")
        elements += field("Special items or comfort objects", s, fillable=fillable, 
                          field_name="comfort_items")
        
    elif service_type == "drop_in":
        elements += [sec_hdr("DROP-IN VISIT DETAILS", s), sp(0.2)]
        
        elements.append(para_row("Tasks per visit (check all that apply):", s["lbl"]))
        if fillable:
            elements.append(FillableCheckboxRow("dropin_tasks",
                ["Feed", "Fresh water", "Potty break/walk", "Playtime", "Medication", 
                 "Scoop litter", "Bring in mail", "Water plants", "Rotate lights"],
                per_row=3
            ))
        else:
            elements.append(CheckboxRow(
                ["Feed", "Fresh water", "Potty break/walk", "Playtime", "Medication", 
                 "Scoop litter", "Bring in mail", "Water plants", "Rotate lights"],
                per_row=3
            ))
        elements.append(sp(0.1))
        
        elements += field("Visit time preference", s, fillable=fillable, field_name="visit_time")
        elements += field("Visit duration needed", s, fillable=fillable, field_name="visit_duration")
    
    return elements


# ── Main builder ───────────────────────────────────────────────────────────────
def build_form(config, output_path):
    """Build the intake form PDF from config dict."""
    global THEME_COLORS
    
    # Initialize theme colors before anything else
    THEME_COLORS = get_theme_colors(config)
    
    business_name = config.get("business_name", DEFAULT_CONFIG["business_name"])
    sitter_name = config.get("sitter_name", DEFAULT_CONFIG["sitter_name"])
    services = config.get("services", DEFAULT_CONFIG["services"])
    location = config.get("location", DEFAULT_CONFIG["location"])
    contact = config.get("contact", DEFAULT_CONFIG["contact"])
    service_type = config.get("service_type", DEFAULT_CONFIG["service_type"])
    num_pets = config.get("num_pets", DEFAULT_CONFIG["num_pets"])
    include_home_access = config.get("include_home_access", DEFAULT_CONFIG["include_home_access"])
    fillable = config.get("fillable", DEFAULT_CONFIG["fillable"])
    
    s = sty()
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.6*inch,  bottomMargin=0.6*inch)
    story = []

    # Calculate total pages
    base_pages = 4
    if include_home_access:
        base_pages += 1
    extra_pet_pages = max(0, num_pets - 1) * 2  # 2 pages per additional pet
    total_pages = base_pages + extra_pet_pages

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 1 — PET OWNER INFORMATION
    # ══════════════════════════════════════════════════════════════════════
    hero_rows = [
        [Paragraph(business_name, s["title"])],
        [Paragraph("Client &amp; Pet Intake Form", s["subtitle"])],
        [Paragraph(f"{location}  \u00b7  {contact}", s["contact"])],
        [Paragraph(f"<b>Services:</b>  {services}", s["svc"])],
    ]
    hero = Table(hero_rows, colWidths=[PAGE_W])
    hero.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), _c("accent_light")),
        ("TOPPADDING",    (0,0),(-1,0),  18),
        ("TOPPADDING",    (0,1),(-1,-1), 3),
        ("BOTTOMPADDING", (0,-1),(-1,-1), 16),
        ("BOTTOMPADDING", (0,0),(-1,-2), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
    ]))
    story += [hero, sp(0.22)]

    story += [sec_hdr("SECTION 1  —  PET OWNER INFORMATION", s), sp(0.25)]

    story += field("Owner Full Name", s, extra_space=26, fillable=fillable, field_name="owner_name")
    story.append(two_col("Home Phone", "Cell Phone", s, fillable=fillable, 
                         field_names=["home_phone", "cell_phone"]))
    story += field("Email Address", s, extra_space=26, fillable=fillable, field_name="email")
    story.append(sp(0.08))
    story += field("Street Address", s, extra_space=26, fillable=fillable, field_name="street_address", multiline=True)
    story.append(three_col(
        ["City", "State / Province", "Zip / Postal Code"], s,
        widths=[2.8*inch, 2.0*inch, 1.9*inch],
        fillable=fillable,
        field_names=["city", "state_province", "zip_postal"]
    ))
    story.append(sp(0.3))

    story.append(para_row("Emergency Contact  <i>(someone other than you)</i>", s["sublbl"]))
    story.append(sp(0.1))
    story.append(two_col("Emergency Contact Name", "Relationship", s, fillable=fillable,
                         field_names=["emergency_name", "emergency_relationship"]))
    story.append(two_col("Phone", "Alt Phone", s, fillable=fillable,
                         field_names=["emergency_phone", "emergency_alt_phone"]))
    story.append(sp(0.3))

    story.append(para_row("Veterinarian Information", s["sublbl"]))
    story.append(sp(0.1))
    story.append(two_col("Veterinary Clinic Name", "Clinic Phone", s, fillable=fillable,
                         field_names=["vet_clinic", "vet_phone"]))
    story += field("Clinic Address", s, extra_space=26, fillable=fillable, field_name="vet_address", multiline=True)
    story.append(sp(0.15))
    
    story.append(para_row("24-Hour Emergency Vet  <i>(if different from above)</i>", s["sublbl"]))
    story.append(sp(0.1))
    story.append(two_col("Emergency Vet Name", "Emergency Vet Phone", s, fillable=fillable,
                         field_names=["emergency_vet_name", "emergency_vet_phone"]))
    story.append(sp(0.2))

    story += field("Person(s) Authorized to Pick Up My Pet", s, extra_space=26, fillable=fillable,
                   field_name="authorized_pickup")
    
    story.append(sp(0.15))
    story.append(para_row("Communication Preferences", s["sublbl"]))
    story.append(sp(0.1))
    story.append(para_row("How often would you like updates?", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("update_frequency",
            ["Daily", "Twice daily", "Only if needed", "Other"],
            per_row=4
        ))
    else:
        story.append(CheckboxRow(
            ["Daily", "Twice daily", "Only if needed", "Other"],
            per_row=4
        ))
    story.append(para_row("Preferred contact method:", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("contact_method",
            ["Text", "Email", "Phone call", "App (specify below)"],
            per_row=4
        ))
    else:
        story.append(CheckboxRow(
            ["Text", "Email", "Phone call", "App (specify below)"],
            per_row=4
        ))

    # ══════════════════════════════════════════════════════════════════════
    # HOME ACCESS SECTION (if enabled)
    # ══════════════════════════════════════════════════════════════════════
    current_page = 1
    if include_home_access:
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s)
        story += build_home_access_section(s, fillable=fillable)

    # ══════════════════════════════════════════════════════════════════════
    # PET PROFILE PAGES (one set per pet)
    # ══════════════════════════════════════════════════════════════════════
    for pet_num in range(1, num_pets + 1):
        prefix = f"pet{pet_num}_" if num_pets > 1 else ""
        pet_label = f" #{pet_num}" if num_pets > 1 else ""
        
        # PAGE — PET PROFILE + VACCINATIONS
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s)
        story += [sec_hdr(f"PET PROFILE{pet_label}", s), sp(0.2)]
        
        if num_pets > 1:
            story.append(para_row(f"<b>Pet {pet_num} of {num_pets}</b>", s["note"]))
        
        story.append(two_col("Pet Name", "Species  (Dog / Cat / Other)", s, fillable=fillable,
                             field_names=[f"{prefix}name", f"{prefix}species"]))
        story.append(two_col("Breed", "Mix?   Yes  /  No", s, fillable=fillable,
                             field_names=[f"{prefix}breed", f"{prefix}mix"]))
        story.append(three_col(
            ["Age", "Weight (lbs)", "Color / Markings"], s,
            widths=[1.7*inch, 1.7*inch, 3.3*inch],
            fillable=fillable,
            field_names=[f"{prefix}age", f"{prefix}weight", f"{prefix}color_markings"]
        ))

        story.append(para_row("Sex:", s["lbl"]))
        if fillable:
            story.append(FillableCheckboxRow(f"{prefix}sex",
                ["Male (intact)", "Male (neutered)", "Female (intact)", "Female (spayed)"],
                per_row=4
            ))
        else:
            story.append(CheckboxRow(
                ["Male (intact)", "Male (neutered)", "Female (intact)", "Female (spayed)"],
                per_row=4
            ))
        story.append(sp(0.12))
        story.append(two_col("Microchip #", "License / Tag #", s, fillable=fillable,
                             field_names=[f"{prefix}microchip", f"{prefix}license"]))
        story.append(sp(0.15))
        
        # Flea/tick prevention
        story.append(para_row("Flea/Tick Prevention", s["sublbl"]))
        story.append(sp(0.1))
        story.append(two_col("Prevention product used", "Last applied date", s, fillable=fillable,
                             field_names=[f"{prefix}flea_product", f"{prefix}flea_date"]))
        story.append(sp(0.15))

        # VACCINATIONS
        story += [sec_hdr("VACCINATIONS", s), sp(0.14)]
        story.append(para_row(
            "Proof of current vaccinations may be required. Please attach vet records if available.",
            s["note"]
        ))

        vax_col_widths = [2.8*inch, 2.6*inch, 1.6*inch]
        vax_data = [[
            Paragraph("Vaccine", s["th"]),
            Paragraph("Up to Date?", s["th"]),
            Paragraph("Expiration Date", s["th"]),
        ]]
        
        vaccines = [
            ("Rabies", "rabies", ["Yes", "No", "Exempt"]),
            ("DHPP / DA2PP", "dhpp", ["Yes", "No", "N/A"]),
            ("Bordetella (Kennel Cough)", "bordetella", ["Yes", "No", "N/A"]),
            ("Feline FVRCP", "fvrcp", ["Yes", "No", "N/A"]),
            ("Feline Leukemia", "felv", ["Yes", "No", "N/A"]),
            ("Canine Influenza", "canine_flu", ["Yes", "No", "N/A"]),
            ("Other", "other_vax", ["Yes", "No"]),
        ]
        
        if fillable:
            for vax_name, vax_key, options in vaccines:
                field_base = f"{prefix}vax_{vax_key}"
                
                # Create inline checkboxes for Yes/No/Exempt|N/A
                checkbox_row = VaxCheckboxRow(field_base, options)
                
                # Expiration date text field
                exp_field = FillableTextField(f"{field_base}_exp", vax_col_widths[2] - 16, height=18)
                
                # For "Other" vaccine, make name fillable too
                if vax_key == "other_vax":
                    name_cell = [
                        Paragraph("Other: ", s["td"]),
                        FillableTextField(f"{prefix}vax_other_name", vax_col_widths[0] - 50, height=16),
                    ]
                    name_table = Table([name_cell], colWidths=[0.5*inch, vax_col_widths[0] - 50])
                    name_table.setStyle(TableStyle([
                        ("LEFTPADDING", (0,0), (-1,-1), 0),
                        ("RIGHTPADDING", (0,0), (-1,-1), 0),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                    ]))
                    vax_data.append([name_table, checkbox_row, exp_field])
                else:
                    vax_data.append([Paragraph(vax_name, s["td"]), checkbox_row, exp_field])
        else:
            for vax_name, vax_key, options in vaccines:
                opts_str = "   /   ".join(options)
                display_name = vax_name if vax_key != "other_vax" else "Other: _______________"
                vax_data.append([
                    Paragraph(display_name, s["td"]), 
                    Paragraph(opts_str, s["td"]), 
                    Paragraph("", s["td"])
                ])

        vt = Table(vax_data, colWidths=vax_col_widths)
        vt.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0),  _c("primary")),
            ("GRID",          (0,0), (-1,-1), 0.4, _c("primary_mid")),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [_c("accent_light"), WHITE]),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(vt)
        if not fillable:
            story.append(para_row("Circle the appropriate response in each row.", s["note"]))

        # PAGE — HEALTH, BEHAVIOR & CARE
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s)
        story += [sec_hdr(f"HEALTH & MEDICATIONS{pet_label}", s), sp(0.2)]

        story += field("Known Allergies or Sensitivities", s, extra_space=26, fillable=fillable,
                       field_name=f"{prefix}allergies", multiline=True)
        story += field("Medical Conditions / Diagnoses", s, extra_space=26, fillable=fillable,
                       field_name=f"{prefix}conditions", multiline=True)
        story.append(sp(0.1))
        story.append(para_row("Current Medications  <i>(name, dose, frequency, food instructions)</i>", s["lbl"]))
        story.append(sp(0.1))

        med_col_widths = [2.2*inch, 1.2*inch, 1.3*inch, 2.3*inch]
        med_data = [[
            Paragraph("Medication Name", s["th"]),
            Paragraph("Dosage", s["th"]),
            Paragraph("Frequency", s["th"]),
            Paragraph("Special Instructions", s["th"]),
        ]]
        
        if fillable:
            med_fields = ["med_name", "med_dosage", "med_frequency", "med_instructions"]
            for row_idx in range(3):
                row = []
                for col_idx, (fname, width) in enumerate(zip(med_fields, med_col_widths)):
                    field_name = f"{prefix}{fname}_{row_idx+1}"
                    row.append(FillableTextField(field_name, width - 16, height=20))
                med_data.append(row)
        else:
            for _ in range(3):
                med_data.append([Paragraph("", s["td"])] * 4)
        
        mt = Table(med_data, colWidths=med_col_widths)
        mt.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0),  _c("primary")),
            ("GRID",          (0,0), (-1,-1), 0.4, _c("primary_mid")),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [_c("accent_light"), WHITE, _c("accent_light")]),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("TOPPADDING",    (0,0), (-1,-1), 14),
            ("BOTTOMPADDING", (0,0), (-1,-1), 14),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(mt)
        story.append(sp(0.2))

        # Behavior & temperament
        story += build_pet_behavior_section(s, pet_num, fillable=fillable)
        story.append(sp(0.15))
        
        # Potty section
        story += build_potty_section(s, pet_num, fillable=fillable)
        story.append(sp(0.15))
        
        # Sleep & crate section
        story += build_sleep_crate_section(s, pet_num, fillable=fillable)
        story.append(sp(0.2))

        # FEEDING & DAILY CARE
        story += [sec_hdr(f"FEEDING & DAILY CARE{pet_label}", s), sp(0.2)]
        story.append(two_col("Food Brand / Type", "Amount per Meal", s, fillable=fillable,
                             field_names=[f"{prefix}food_brand", f"{prefix}food_amount"]))
        story += field("Where is food stored?", s, extra_space=22, fillable=fillable,
                       field_name=f"{prefix}food_location")

        story.append(para_row("Feeding Schedule:", s["lbl"]))
        if fillable:
            story.append(FillableCheckboxRow(f"{prefix}feeding_schedule",
                ["Once daily", "Twice daily", "Three times daily", "Free-fed"], per_row=4))
        else:
            story.append(CheckboxRow(["Once daily", "Twice daily", "Three times daily", "Free-fed"], per_row=4))
        story.append(sp(0.16))

        story.append(para_row("Treats:", s["lbl"]))
        if fillable:
            story.append(FillableCheckboxRow(f"{prefix}treats",
                ["Yes — allowed", "No — not allowed"], per_row=2))
        else:
            story.append(CheckboxRow(["Yes — allowed", "No — not allowed"], per_row=2))
        story.append(sp(0.1))

        story += field("If yes, treat brand / type & where stored:", s, extra_space=22, fillable=fillable,
                       field_name=f"{prefix}treat_info")
        story += field("Exercise needs (walk duration, activity level)", s, extra_space=22, fillable=fillable,
                       field_name=f"{prefix}exercise", multiline=True)
        story += field("Any other special care instructions", s, extra_lines=2, fillable=fillable,
                       field_name=f"{prefix}special_instructions")

    # ══════════════════════════════════════════════════════════════════════
    # SERVICE-SPECIFIC SECTION (if not general)
    # ══════════════════════════════════════════════════════════════════════
    if service_type != "general":
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s)
        story += build_service_specific_section(s, service_type, fillable=fillable)

    # ══════════════════════════════════════════════════════════════════════
    # AUTHORIZATION & SIGNATURE PAGE
    # ══════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    current_page += 1
    story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s)
    story += [sec_hdr("AUTHORIZATION & AGREEMENT", s), sp(0.18)]

    sitter = sitter_name if sitter_name else business_name
    for title, body in [
        ("Emergency Veterinary Care",
         f"I authorize <b>{sitter}</b> to seek emergency veterinary care for my pet(s) if I cannot "
         f"be reached and the situation requires immediate attention. I understand I am responsible "
         f"for all veterinary fees incurred."),
        ("Transport Authorization",
         f"I authorize <b>{sitter}</b> to transport my pet(s) in their vehicle if necessary for "
         f"veterinary care or other emergency situations."),
        ("Photo &amp; Social Media Release",
         f"I give permission for photos and videos of my pet(s) to be shared on social media or "
         f"used for marketing by <b>{sitter}</b>."),
        ("Cancellation Policy",
         "Please refer to our separate service agreement for cancellation and refund terms. By "
         "signing below, I acknowledge I have read and agree to all stated terms."),
        ("Liability",
         "I confirm my pet(s) is/are current on required vaccinations, has/have not shown "
         "aggression toward people or other animals without prior written disclosure, and I accept "
         "full liability for any damage or injury caused by my pet(s)."),
    ]:
        story.append(auth_block(title, body, s))
        story.append(sp(0.08))

    story.append(sp(0.06))
    story.append(para_row("Photo / video permission:", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("photo_permission",
            ["Yes, I give permission", "No, please do not share"], per_row=2))
    else:
        story.append(CheckboxRow(["Yes, I give permission", "No, please do not share"], per_row=2))
    story.append(sp(0.06))
    
    story.append(para_row("Transport authorization:", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("transport_permission",
            ["Yes, I authorize transport", "No, do not transport"], per_row=2))
    else:
        story.append(CheckboxRow(["Yes, I authorize transport", "No, do not transport"], per_row=2))
    story.append(sp(0.2))

    # Signature lines
    story.append(two_col("Client Signature", "Date", s, fillable=fillable,
                         field_names=["signature", "signature_date"]))
    story.append(sp(0.1))
    story += field("Printed Name", s, fillable=fillable, field_name="printed_name")
    story.append(sp(0.2))

    # Office use section
    ot = Table([[Paragraph(
        "For office use only  \u00b7  Client ID: _________________   Date on file: _________________   "
        "Last updated: _________________",
        s["office"]
    )]], colWidths=[PAGE_W])
    ot.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), _c("primary")),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
    ]))
    story.append(ot)
    story.append(sp(0.15))
    story.append(hr(None, 0.8, 6))  # Uses accent color
    story.append(Paragraph(f"{business_name}  \u00b7  {location}  \u00b7  {contact}", s["foot"]))
    story.append(Paragraph("Thank you for trusting us with your furry family member!", s["foot"]))

    doc.build(story)
    theme_name = config.get("theme", "lavender")
    print(f"✅  Form saved to: {output_path}")
    print(f"   Pages: {total_pages}, Pets: {num_pets}, Service type: {service_type}, Theme: {theme_name}")
    if fillable:
        print("   📝 Fillable PDF fields enabled")


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Generate professional pet sitter client intake forms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --business-name "Pawsitive Care" --contact "555-1234"
  %(prog)s --config my_business.yaml --fillable
  %(prog)s --pets 2 --service-type boarding
  %(prog)s --config config.yaml --pets 3 --output multi_pet_form.pdf
        """
    )
    
    # Config file (highest priority for defaults)
    p.add_argument("--config", "-c", metavar="FILE",
                   help="YAML config file for business presets")
    
    # Business info (override config)
    p.add_argument("--business-name", metavar="NAME",
                   help="Business name for header")
    p.add_argument("--sitter-name", metavar="NAME",
                   help="Individual sitter name (for authorization text)")
    p.add_argument("--services", metavar="LIST",
                   help="Comma-separated services offered")
    p.add_argument("--location", metavar="LOC",
                   help="Business location/city")
    p.add_argument("--contact", metavar="INFO",
                   help="Contact info (phone, email, website)")
    
    # Form options
    p.add_argument("--service-type", choices=["general", "boarding", "walking", "drop_in"],
                   help="Service type for specialized sections")
    p.add_argument("--pets", type=int, metavar="N",
                   help="Number of pet profile pages to generate (default: 1)")
    
    # Theme options
    theme_names = list(THEMES.keys())
    p.add_argument("--theme", choices=theme_names + ["custom"], metavar="NAME",
                   help=f"Color theme: {', '.join(theme_names)}, or 'custom'")
    p.add_argument("--list-themes", action="store_true",
                   help="Show available color themes and exit")
    
    p.add_argument("--fillable", action="store_true", default=None,
                   help="Generate fillable PDF form fields (default: enabled)")
    p.add_argument("--no-fillable", action="store_true",
                   help="Generate print-only form (static lines instead of fields)")
    p.add_argument("--no-home-access", action="store_true",
                   help="Omit home access section")
    
    # Output
    p.add_argument("--output", "-o", default="client_intake_form.pdf", metavar="FILE",
                   help="Output PDF filename (default: client_intake_form.pdf)")
    
    args = p.parse_args()
    
    # Handle --list-themes
    if args.list_themes:
        list_themes()
        exit(0)
    
    # Load config file first, then override with CLI args
    config = load_config(args.config)
    
    # CLI args override config file
    if args.theme:
        config["theme"] = args.theme
    if args.business_name:
        config["business_name"] = args.business_name
    if args.sitter_name:
        config["sitter_name"] = args.sitter_name
    if args.services:
        config["services"] = args.services
    if args.location:
        config["location"] = args.location
    if args.contact:
        config["contact"] = args.contact
    if args.service_type:
        config["service_type"] = args.service_type
    if args.pets:
        config["num_pets"] = args.pets
    if args.no_fillable:
        config["fillable"] = False
    elif args.fillable:
        config["fillable"] = True
    if args.no_home_access:
        config["include_home_access"] = False
    
    # Determine output path: CLI arg > config file > default
    # Only override config output if user explicitly passed --output
    # (check if it differs from the argparse default)
    if args.output != "client_intake_form.pdf":
        output_path = args.output
    else:
        output_path = config.get("output", "client_intake_form.pdf")
    
    build_form(config, output_path)
