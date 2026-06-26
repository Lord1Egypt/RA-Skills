"""
Catalog of 54 popular web design templates.

Each template is a dict with standardized fields.
The first 10 are fully described with design tokens;
the remaining 44 are stubs with name + category.
"""

TEMPLATES = [
    # ── FULLY DESCRIBED TEMPLATES ──────────────────────────────────

    {
        "name": "notion",
        "category": "Design & Productivity",
        "tags": ["warm", "minimal", "serif", "docs", "wiki"],
        "description": "Warm minimalism with serif headings, clean cards, and soft surfaces. Notion's design feels like a well-edited magazine — spacious, calm, and inviting.",
        "best_for": "Documentation sites, wikis, personal blogs, knowledge bases, note-taking apps",
        "key_elements": [
            "Serif display headings with compressed letter-spacing",
            "4-layer whisper shadow stack on cards",
            "Warm off-white backgrounds (#f6f5f4 alternation)",
            "Clean sidebar navigation with emoji support",
            "Subtle 1px rgba(0,0,0,0.1) borders"
        ],
        "colors": [
            {"role": "primary", "hex": "#0075de", "name": "Notion Blue"},
            {"role": "text-primary", "hex": "rgba(0,0,0,0.95)", "name": "Primary Text"},
            {"role": "text-secondary", "hex": "rgba(0,0,0,0.5)", "name": "Secondary Text"},
            {"role": "background", "hex": "#ffffff", "name": "Main Background"},
            {"role": "background-warm", "hex": "#f6f5f4", "name": "Warm White Alt"},
            {"role": "hover", "hex": "rgba(0,0,0,0.04)", "name": "Hover Overlay"},
            {"role": "border", "hex": "rgba(0,0,0,0.1)", "name": "Card Border"},
            {"role": "accent-red", "hex": "#e03e2d", "name": "Red Accent"},
            {"role": "accent-yellow", "hex": "#dfab01", "name": "Yellow Accent"},
            {"role": "accent-green", "hex": "#0f7b6c", "name": "Green Accent"},
        ],
        "typography": {
            "font_family": "'Inter', -apple-system, system-ui, sans-serif",
            "display": {"size": "64px", "weight": 700, "letter_spacing": "-2.125px", "line_height": 1.1},
            "h1": {"size": "40px", "weight": 700, "letter_spacing": "-1.25px", "line_height": 1.2},
            "h2": {"size": "28px", "weight": 600, "letter_spacing": "-0.5px", "line_height": 1.3},
            "h3": {"size": "20px", "weight": 600, "letter_spacing": "-0.25px", "line_height": 1.4},
            "body": {"size": "16px", "weight": 400, "letter_spacing": "0", "line_height": 1.6},
            "caption": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "code": {"family": "'SF Mono', 'Source Code Pro', monospace", "size": "14px"},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 24, 32, 48, 64, 96, 128],
            "card_padding": "16px",
            "section_gap": "64px",
            "page_margin": "96px",
        },
        "borders": {
            "radius_sm": "3px",
            "radius_md": "6px",
            "radius_lg": "12px",
            "card_border": "1px solid rgba(0,0,0,0.1)",
            "input_border": "1px solid rgba(0,0,0,0.15)",
        },
        "shadows": {
            "card": "rgba(0,0,0,0.04) 0px 4px 18px, rgba(0,0,0,0.027) 0px 2.025px 7.84688px, rgba(0,0,0,0.02) 0px 0.8px 2.925px, rgba(0,0,0,0.01) 0px 0.175px 1.04062px",
            "modal": "rgba(0,0,0,0.15) 0px 8px 40px",
            "hover_lift": "rgba(0,0,0,0.06) 0px 8px 30px",
        },
    },

    {
        "name": "linear",
        "category": "Developer Tools & Platforms",
        "tags": ["dark", "minimal", "mono", "devtools", "purple"],
        "description": "Ultra-minimal dark-mode design with precise typography. Linear's interface feels engineered — every pixel intentional, zero decoration.",
        "best_for": "Developer tools, project management apps, issue trackers, dashboards, CLI wrappers",
        "key_elements": [
            "Dark canvas (#1a1a1a) with subtle card contrast (#222)",
            "Purple accent (#5e6ad2) for interactive elements",
            "Whisper borders — rgba(255,255,255,0.06)",
            "Geist/Inter typography at -0.01em tracking",
            "Keyboard-first interaction patterns"
        ],
        "colors": [
            {"role": "primary", "hex": "#5e6ad2", "name": "Purple Accent"},
            {"role": "primary-hover", "hex": "#7b83e0", "name": "Purple Hover"},
            {"role": "background", "hex": "#1a1a1a", "name": "Dark Canvas"},
            {"role": "surface", "hex": "#222222", "name": "Card Surface"},
            {"role": "surface-hover", "hex": "#2a2a2a", "name": "Hover Surface"},
            {"role": "text-primary", "hex": "#ffffff", "name": "Primary Text"},
            {"role": "text-secondary", "hex": "#8a8a8a", "name": "Secondary Text"},
            {"role": "border", "hex": "rgba(255,255,255,0.06)", "name": "Whisper Border"},
            {"role": "danger", "hex": "#f85149", "name": "Red"},
            {"role": "success", "hex": "#3fb950", "name": "Green"},
        ],
        "typography": {
            "font_family": "'Geist', 'Inter', -apple-system, system-ui, sans-serif",
            "mono_family": "'Geist Mono', 'SF Mono', monospace",
            "display": {"size": "36px", "weight": 600, "letter_spacing": "-0.02em", "line_height": 1.2},
            "h1": {"size": "28px", "weight": 600, "letter_spacing": "-0.015em", "line_height": 1.3},
            "h2": {"size": "20px", "weight": 500, "letter_spacing": "-0.01em", "line_height": 1.4},
            "body": {"size": "14px", "weight": 400, "letter_spacing": "-0.005em", "line_height": 1.5},
            "caption": {"size": "12px", "weight": 400, "letter_spacing": "0", "line_height": 1.4},
            "code": {"family": "'Geist Mono', monospace", "size": "13px"},
        },
        "spacing": {
            "scale": [2, 4, 8, 12, 16, 20, 24, 32, 40, 48],
            "card_padding": "12px",
            "section_gap": "32px",
            "page_margin": "24px",
            "compact": True,
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "6px",
            "radius_lg": "8px",
            "card_border": "1px solid rgba(255,255,255,0.06)",
            "input_border": "1px solid rgba(255,255,255,0.08)",
        },
        "shadows": {
            "card": "none",
            "popover": "0px 4px 24px rgba(0,0,0,0.4), 0px 0px 0px 1px rgba(255,255,255,0.06)",
            "modal": "0px 16px 48px rgba(0,0,0,0.6)",
        },
    },

    {
        "name": "stripe",
        "category": "Infrastructure & Cloud",
        "tags": ["clean", "gradient", "blue-purple", "saas", "landing"],
        "description": "Signature purple gradients with weight-300 typographic elegance. Stripe's design communicates trust through refinement — every gradient, every transition, every shadow feels intentional.",
        "best_for": "SaaS landing pages, fintech products, API documentation, payment interfaces, enterprise marketing",
        "key_elements": [
            "Blue-purple gradient system (#635bff → #00d4ff)",
            "Source Sans 3 at weight 300-600",
            "Subtle card lift shadows (0 2px 5px rgba(0,0,0,0.05))",
            "Clean white backgrounds with #f6f9fc cool-gray sections",
            "Generous whitespace and large typography"
        ],
        "colors": [
            {"role": "primary", "hex": "#635bff", "name": "Stripe Purple"},
            {"role": "primary-gradient", "hex": "#00d4ff", "name": "Cyan Partner"},
            {"role": "text-dark", "hex": "#0a2540", "name": "Navy Text"},
            {"role": "text-body", "hex": "#425466", "name": "Body Gray"},
            {"role": "background", "hex": "#ffffff", "name": "White BG"},
            {"role": "background-section", "hex": "#f6f9fc", "name": "Cool Gray Section"},
            {"role": "link", "hex": "#635bff", "name": "Link Purple"},
            {"role": "success", "hex": "#0bb56a", "name": "Green"},
            {"role": "warning", "hex": "#ff9800", "name": "Orange"},
            {"role": "danger", "hex": "#df1b41", "name": "Red"},
        ],
        "typography": {
            "font_family": "'Source Sans 3', -apple-system, system-ui, sans-serif",
            "display": {"size": "72px", "weight": 300, "letter_spacing": "-1.5px", "line_height": 1.1},
            "h1": {"size": "48px", "weight": 400, "letter_spacing": "-0.8px", "line_height": 1.15},
            "h2": {"size": "32px", "weight": 400, "letter_spacing": "-0.3px", "line_height": 1.25},
            "h3": {"size": "22px", "weight": 600, "letter_spacing": "-0.2px", "line_height": 1.3},
            "body": {"size": "17px", "weight": 400, "letter_spacing": "-0.3px", "line_height": 1.65},
            "caption": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "code": {"family": "'Source Code Pro', monospace", "size": "14px"},
        },
        "spacing": {
            "scale": [4, 8, 16, 24, 32, 48, 64, 96, 128, 160],
            "card_padding": "24px",
            "section_gap": "120px",
            "page_margin": "auto (max-width: 1080px)",
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "6px",
            "radius_lg": "12px",
            "radius_xl": "24px",
            "card_border": "1px solid rgba(0,0,0,0.06)",
            "input_border": "1px solid rgba(0,0,0,0.15)",
        },
        "shadows": {
            "card": "0 2px 5px rgba(0,0,0,0.05)",
            "card_hover": "0 8px 30px rgba(0,0,0,0.08)",
            "nav": "0 1px 0 rgba(0,0,0,0.06)",
            "modal": "0 20px 60px rgba(0,0,0,0.15)",
        },
    },

    {
        "name": "vercel",
        "category": "Developer Tools & Platforms",
        "tags": ["black-white", "geometric", "geist", "deploy", "minimal"],
        "description": "Black and white precision with the Geist font system. Vercel's design is geometric, compressed, and unmistakably developer-focused — sharp lines, zero decoration.",
        "best_for": "Deployment platforms, developer tools, portfolio sites, documentation, startup landing pages",
        "key_elements": [
            "Geist / Geist Mono font system",
            "Stark black (#000) on white (#fff) palette",
            "Blue (#0070f3) and purple (#7928ca) accents",
            "Hairline borders — rgba(0,0,0,0.08)",
            "Geometric compressed typography"
        ],
        "colors": [
            {"role": "text", "hex": "#000000", "name": "Black Text"},
            {"role": "background", "hex": "#ffffff", "name": "White Background"},
            {"role": "accent-blue", "hex": "#0070f3", "name": "Vercel Blue"},
            {"role": "accent-purple", "hex": "#7928ca", "name": "Purple Partner"},
            {"role": "accent-pink", "hex": "#ff0080", "name": "Pink Accent"},
            {"role": "text-secondary", "hex": "#666666", "name": "Secondary Text"},
            {"role": "surface", "hex": "#fafafa", "name": "Light Surface"},
            {"role": "border", "hex": "rgba(0,0,0,0.08)", "name": "Hairline"},
            {"role": "success", "hex": "#0070f3", "name": "Success Blue"},
            {"role": "error", "hex": "#ee0000", "name": "Error Red"},
        ],
        "typography": {
            "font_family": "'Geist', -apple-system, system-ui, sans-serif",
            "mono_family": "'Geist Mono', 'SF Mono', monospace",
            "display": {"size": "56px", "weight": 700, "letter_spacing": "-0.04em", "line_height": 1.05},
            "h1": {"size": "40px", "weight": 700, "letter_spacing": "-0.03em", "line_height": 1.1},
            "h2": {"size": "28px", "weight": 600, "letter_spacing": "-0.02em", "line_height": 1.2},
            "h3": {"size": "20px", "weight": 600, "letter_spacing": "-0.01em", "line_height": 1.3},
            "body": {"size": "16px", "weight": 400, "letter_spacing": "-0.005em", "line_height": 1.6},
            "caption": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "code": {"family": "'Geist Mono', monospace", "size": "14px"},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 24, 32, 48, 64, 80, 96],
            "card_padding": "24px",
            "section_gap": "80px",
            "page_margin": "24px (max-width: 1200px auto)",
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "6px",
            "radius_lg": "8px",
            "card_border": "1px solid rgba(0,0,0,0.08)",
            "input_border": "1px solid rgba(0,0,0,0.12)",
        },
        "shadows": {
            "card": "0 2px 8px rgba(0,0,0,0.06)",
            "card_hover": "0 8px 24px rgba(0,0,0,0.1)",
            "tooltip": "0 4px 16px rgba(0,0,0,0.12)",
        },
    },

    {
        "name": "github",
        "category": "Developer Tools & Platforms",
        "tags": ["terminal-green", "code", "open-source", "dark", "developer"],
        "description": "GitHub's iconic design language — dark canvas with terminal-green accents. Code-forward, data-dense, and instantly recognizable by developers worldwide.",
        "best_for": "Open source project pages, developer portfolios, code documentation, CLI tools, README generators",
        "key_elements": [
            "Terminal-green (#2da44e) primary accent",
            "Dark mode with #0d1117 background",
            "Monospace code blocks with syntax highlighting",
            "Tab-style navigation with underline indicators",
            "Contribution graph heatmap aesthetic"
        ],
        "colors": [
            {"role": "primary", "hex": "#2da44e", "name": "GitHub Green"},
            {"role": "primary-hover", "hex": "#2c974b", "name": "Green Hover"},
            {"role": "background", "hex": "#0d1117", "name": "Dark Canvas"},
            {"role": "surface", "hex": "#161b22", "name": "Card Surface"},
            {"role": "surface-hover", "hex": "#1c2128", "name": "Hover State"},
            {"role": "text-primary", "hex": "#e6edf3", "name": "Primary Text"},
            {"role": "text-secondary", "hex": "#8b949e", "name": "Secondary Text"},
            {"role": "border", "hex": "#30363d", "name": "Border Gray"},
            {"role": "link", "hex": "#58a6ff", "name": "Link Blue"},
            {"role": "danger", "hex": "#f85149", "name": "Error Red"},
        ],
        "typography": {
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            "mono_family": "'SF Mono', 'Source Code Pro', 'Fira Code', monospace",
            "display": {"size": "32px", "weight": 600, "letter_spacing": "-0.5px", "line_height": 1.25},
            "h1": {"size": "26px", "weight": 600, "letter_spacing": "-0.5px", "line_height": 1.25},
            "h2": {"size": "20px", "weight": 600, "letter_spacing": "-0.25px", "line_height": 1.3},
            "h3": {"size": "16px", "weight": 600, "letter_spacing": "0", "line_height": 1.4},
            "body": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "caption": {"size": "12px", "weight": 400, "letter_spacing": "0", "line_height": 1.4},
            "code": {"family": "'SF Mono', monospace", "size": "13px"},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 24, 32, 40, 48],
            "card_padding": "16px",
            "section_gap": "24px",
            "page_margin": "auto (max-width: 1280px)",
        },
        "borders": {
            "radius_sm": "6px",
            "radius_md": "6px",
            "radius_lg": "12px",
            "card_border": "1px solid #30363d",
            "input_border": "1px solid #30363d",
        },
        "shadows": {
            "card": "none",
            "dropdown": "0 8px 24px rgba(0,0,0,0.4)",
            "overlay": "0 0 0 100vw rgba(0,0,0,0.5)",
        },
    },

    {
        "name": "spotify",
        "category": "Enterprise & Consumer",
        "tags": ["dark", "green", "bold", "music", "album-art"],
        "description": "Vibrant green on dark backgrounds with bold typography. Spotify's design is music-first — album art drives color, gradients pulse with energy, and type demands attention.",
        "best_for": "Music apps, media players, entertainment platforms, podcast sites, creative portfolios",
        "key_elements": [
            "Signature Spotify green (#1ed760) pop",
            "Deep black (#121212) canvas with #181818 cards",
            "Bold, large typography for artist/track names",
            "Dynamic gradient extraction from album art",
            "Rounded pill buttons and circular media controls"
        ],
        "colors": [
            {"role": "primary", "hex": "#1ed760", "name": "Spotify Green"},
            {"role": "primary-glow", "hex": "#1db954", "name": "Green Glow"},
            {"role": "background", "hex": "#121212", "name": "Deep Black"},
            {"role": "surface", "hex": "#181818", "name": "Card Dark"},
            {"role": "surface-hover", "hex": "#282828", "name": "Hover Gray"},
            {"role": "text-primary", "hex": "#ffffff", "name": "White Text"},
            {"role": "text-secondary", "hex": "#a7a7a7", "name": "Subdued Text"},
            {"role": "text-subdued", "hex": "#6a6a6a", "name": "Muted Text"},
            {"role": "gradient-start", "hex": "#450af5", "name": "Purple Gradient"},
            {"role": "gradient-end", "hex": "#c4efd9", "name": "Mint Gradient"},
        ],
        "typography": {
            "font_family": "'Circular', 'Helvetica Neue', -apple-system, system-ui, sans-serif",
            "display": {"size": "48px", "weight": 700, "letter_spacing": "-1px", "line_height": 1.1},
            "h1": {"size": "32px", "weight": 700, "letter_spacing": "-0.5px", "line_height": 1.2},
            "h2": {"size": "24px", "weight": 700, "letter_spacing": "-0.25px", "line_height": 1.3},
            "body": {"size": "16px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "caption": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.4},
            "small": {"size": "12px", "weight": 400, "letter_spacing": "0.1em", "line_height": 1.3},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 24, 32, 40, 48, 64],
            "card_padding": "16px",
            "section_gap": "32px",
            "page_margin": "24px (sidebar: 240px)",
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "8px",
            "radius_lg": "16px",
            "radius_pill": "9999px",
            "card_border": "none",
            "input_border": "1px solid #333333",
        },
        "shadows": {
            "card": "none",
            "card_hover": "0 8px 24px rgba(0,0,0,0.5)",
            "header": "0 1px 0 rgba(255,255,255,0.1)",
        },
    },

    {
        "name": "apple",
        "category": "Enterprise & Consumer",
        "tags": ["premium", "white-space", "sf-pro", "cinematic", "luxury"],
        "description": "Premium white space with cinematic imagery and the SF Pro type system. Apple's design maximizes impact through restraint — vast whitespace, precise typography, and deep photography.",
        "best_for": "Premium product pages, luxury brand sites, hardware showcases, event landing pages, high-end portfolios",
        "key_elements": [
            "SF Pro Display at precise tracking values",
            "Vast whitespace and full-bleed imagery",
            "Apple Blue (#0071e3) accent on pure white",
            "Complex multi-layer subtle shadows",
            "Sticky navigation with backdrop-filter blur"
        ],
        "colors": [
            {"role": "text-primary", "hex": "#1d1d1f", "name": "Almost Black"},
            {"role": "background", "hex": "#ffffff", "name": "Pure White"},
            {"role": "section-bg", "hex": "#f5f5f7", "name": "Light Gray Section"},
            {"role": "accent", "hex": "#0071e3", "name": "Apple Blue"},
            {"role": "accent-light", "hex": "#2997ff", "name": "Light Blue"},
            {"role": "text-secondary", "hex": "#86868b", "name": "Gray Text"},
            {"role": "link", "hex": "#0071e3", "name": "Link Blue"},
            {"role": "product-red", "hex": "#bf4800", "name": "Product Red"},
            {"role": "product-green", "hex": "#68cc45", "name": "Product Green"},
            {"role": "dark-bg", "hex": "#000000", "name": "Dark Section BG"},
        ],
        "typography": {
            "font_family": "'SF Pro Display', 'Inter', -apple-system, system-ui, sans-serif",
            "display": {"size": "56px", "weight": 600, "letter_spacing": "-0.022em", "line_height": 1.05},
            "h1": {"size": "40px", "weight": 600, "letter_spacing": "-0.02em", "line_height": 1.1},
            "h2": {"size": "28px", "weight": 600, "letter_spacing": "-0.015em", "line_height": 1.15},
            "h3": {"size": "21px", "weight": 500, "letter_spacing": "-0.01em", "line_height": 1.2},
            "body": {"size": "17px", "weight": 400, "letter_spacing": "-0.005em", "line_height": 1.5},
            "caption": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.4},
            "small": {"size": "12px", "weight": 400, "letter_spacing": "-0.005em", "line_height": 1.3},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 24, 32, 48, 64, 80, 96, 120],
            "card_padding": "32px",
            "section_gap": "80px",
            "page_margin": "auto (max-width: 1024px)",
        },
        "borders": {
            "radius_sm": "8px",
            "radius_md": "12px",
            "radius_lg": "18px",
            "radius_xl": "24px",
            "card_border": "none",
            "input_border": "1px solid #d2d2d7",
        },
        "shadows": {
            "card": "0 4px 16px rgba(0,0,0,0.04)",
            "card_hover": "0 8px 30px rgba(0,0,0,0.08)",
            "nav": "0 0 0 1px rgba(0,0,0,0.08)",
            "modal": "0 25px 60px rgba(0,0,0,0.15)",
        },
    },

    {
        "name": "figma",
        "category": "Design & Productivity",
        "tags": ["colorful", "playful", "design-tool", "collaboration", "multi-color"],
        "description": "Vibrant multi-color palette with a playful yet professional tone. Figma's design celebrates creativity — bold accent colors, smooth collaboration cues, and a canvas-first mentality.",
        "best_for": "Design tools, creative platforms, collaboration apps, prototyping tools, creative portfolios",
        "key_elements": [
            "Multi-color accent system (5 distinct colors)",
            "Dark sidebar with colorful file icons",
            "Smooth, rounded UI elements",
            "Collaboration cursors with user colors",
            "Canvas-first layout with floating toolbars"
        ],
        "colors": [
            {"role": "primary", "hex": "#0d99ff", "name": "Figma Blue"},
            {"role": "accent-purple", "hex": "#9747ff", "name": "Purple"},
            {"role": "accent-pink", "hex": "#ff2d6d", "name": "Pink"},
            {"role": "accent-green", "hex": "#1bc47d", "name": "Green"},
            {"role": "accent-orange", "hex": "#ffa629", "name": "Orange"},
            {"role": "background", "hex": "#ffffff", "name": "Canvas White"},
            {"role": "surface", "hex": "#f5f5f5", "name": "Panel Gray"},
            {"role": "sidebar", "hex": "#2c2c2c", "name": "Dark Sidebar"},
            {"role": "text-primary", "hex": "#000000", "name": "Primary Text"},
            {"role": "text-secondary", "hex": "#666666", "name": "Secondary Text"},
        ],
        "typography": {
            "font_family": "'Inter', -apple-system, system-ui, sans-serif",
            "display": {"size": "32px", "weight": 700, "letter_spacing": "-0.5px", "line_height": 1.2},
            "h1": {"size": "24px", "weight": 600, "letter_spacing": "-0.25px", "line_height": 1.3},
            "h2": {"size": "18px", "weight": 600, "letter_spacing": "0", "line_height": 1.4},
            "body": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "caption": {"size": "12px", "weight": 400, "letter_spacing": "0", "line_height": 1.4},
            "label": {"size": "11px", "weight": 500, "letter_spacing": "0.02em", "line_height": 1.3},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
            "card_padding": "16px",
            "section_gap": "40px",
            "page_margin": "0 (canvas fills viewport)",
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "6px",
            "radius_lg": "12px",
            "card_border": "1px solid #e5e5e5",
            "input_border": "1px solid #d9d9d9",
        },
        "shadows": {
            "card": "0 1px 4px rgba(0,0,0,0.06)",
            "popover": "0 4px 20px rgba(0,0,0,0.12)",
            "modal": "0 12px 40px rgba(0,0,0,0.15)",
            "toolbar": "0 2px 8px rgba(0,0,0,0.08)",
        },
    },

    {
        "name": "airtable",
        "category": "Design & Productivity",
        "tags": ["colorful", "friendly", "spreadsheet", "database", "structured"],
        "description": "Colorful, friendly, and structured — Airtable makes databases feel like spreadsheets. Bright pastels, cheerful illustrations, and clear data hierarchy define the experience.",
        "best_for": "Database UIs, spreadsheet apps, project management tools, CRM interfaces, no-code platforms",
        "key_elements": [
            "Bright, friendly pastel color palette",
            "Colorful record chips and field type icons",
            "Clean grid layout with subtle zebra striping",
            "Rounded pill-shaped tags and badges",
            "Playful illustrations and iconography"
        ],
        "colors": [
            {"role": "primary", "hex": "#18bfff", "name": "Airtable Blue"},
            {"role": "accent-yellow", "hex": "#fbbf24", "name": "Yellow"},
            {"role": "accent-green", "hex": "#34d399", "name": "Green"},
            {"role": "accent-pink", "hex": "#f472b6", "name": "Pink"},
            {"role": "accent-purple", "hex": "#a78bfa", "name": "Purple"},
            {"role": "accent-red", "hex": "#fb7185", "name": "Red"},
            {"role": "background", "hex": "#ffffff", "name": "White"},
            {"role": "surface", "hex": "#f9fafb", "name": "Light Gray"},
            {"role": "text-primary", "hex": "#1f2937", "name": "Dark Text"},
            {"role": "text-secondary", "hex": "#6b7280", "name": "Gray Text"},
        ],
        "typography": {
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
            "display": {"size": "28px", "weight": 600, "letter_spacing": "-0.25px", "line_height": 1.3},
            "h1": {"size": "22px", "weight": 600, "letter_spacing": "-0.2px", "line_height": 1.3},
            "h2": {"size": "18px", "weight": 500, "letter_spacing": "0", "line_height": 1.4},
            "body": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "caption": {"size": "12px", "weight": 400, "letter_spacing": "0", "line_height": 1.4},
            "mono": {"family": "'SF Mono', monospace", "size": "13px"},
        },
        "spacing": {
            "scale": [2, 4, 8, 12, 16, 20, 24, 32, 40, 48],
            "card_padding": "12px",
            "section_gap": "24px",
            "page_margin": "24px",
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "6px",
            "radius_lg": "12px",
            "radius_pill": "999px",
            "card_border": "1px solid #e5e7eb",
            "input_border": "1px solid #d1d5db",
        },
        "shadows": {
            "card": "0 1px 3px rgba(0,0,0,0.06)",
            "card_hover": "0 4px 12px rgba(0,0,0,0.1)",
            "dropdown": "0 4px 16px rgba(0,0,0,0.12)",
            "modal": "0 12px 40px rgba(0,0,0,0.15)",
        },
    },

    {
        "name": "tailwind",
        "category": "Developer Tools & Platforms",
        "tags": ["utility-first", "blue", "developer", "framework", "modern"],
        "description": "The Tailwind CSS brand design — utility-first aesthetic with a vibrant blue gradient identity. Clean, modern, and developer-focused with excellent typographic hierarchy.",
        "best_for": "Developer tools, framework documentation, tech marketing sites, component libraries, CSS framework pages",
        "key_elements": [
            "Vibrant blue-to-cyan gradient branding (#38bdf8 → #818cf8)",
            "Slate gray text hierarchy on white backgrounds",
            "Clean code blocks with syntax highlighting",
            "Utility-class-inspired minimal decoration",
            "Rounded, friendly component shapes"
        ],
        "colors": [
            {"role": "primary", "hex": "#38bdf8", "name": "Tailwind Sky"},
            {"role": "primary-dark", "hex": "#0ea5e9", "name": "Sky Dark"},
            {"role": "accent-indigo", "hex": "#6366f1", "name": "Indigo"},
            {"role": "text-primary", "hex": "#0f172a", "name": "Slate 900"},
            {"role": "text-secondary", "hex": "#475569", "name": "Slate 600"},
            {"role": "background", "hex": "#ffffff", "name": "White"},
            {"role": "surface", "hex": "#f8fafc", "name": "Slate 50"},
            {"role": "border", "hex": "#e2e8f0", "name": "Slate 200"},
            {"role": "success", "hex": "#10b981", "name": "Emerald"},
            {"role": "code-bg", "hex": "#1e293b", "name": "Slate 800"},
        ],
        "typography": {
            "font_family": "'Inter', -apple-system, system-ui, sans-serif",
            "mono_family": "'Fira Code', 'Source Code Pro', monospace",
            "display": {"size": "48px", "weight": 800, "letter_spacing": "-1.5px", "line_height": 1.05},
            "h1": {"size": "36px", "weight": 700, "letter_spacing": "-1px", "line_height": 1.15},
            "h2": {"size": "24px", "weight": 600, "letter_spacing": "-0.5px", "line_height": 1.25},
            "h3": {"size": "18px", "weight": 600, "letter_spacing": "-0.25px", "line_height": 1.3},
            "body": {"size": "16px", "weight": 400, "letter_spacing": "0", "line_height": 1.7},
            "caption": {"size": "14px", "weight": 400, "letter_spacing": "0", "line_height": 1.5},
            "code": {"family": "'Fira Code', monospace", "size": "14px"},
        },
        "spacing": {
            "scale": [4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80],
            "card_padding": "24px",
            "section_gap": "64px",
            "page_margin": "auto (max-width: 1280px)",
        },
        "borders": {
            "radius_sm": "4px",
            "radius_md": "6px",
            "radius_lg": "8px",
            "radius_xl": "12px",
            "card_border": "1px solid #e2e8f0",
            "input_border": "1px solid #cbd5e1",
        },
        "shadows": {
            "card": "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
            "card_hover": "0 10px 25px rgba(0,0,0,0.08)",
            "nav": "0 1px 3px rgba(0,0,0,0.04)",
            "modal": "0 20px 50px rgba(0,0,0,0.15)",
        },
    },

    # ── STUB TEMPLATES ─────────────────────────────────────────────

    # AI & Machine Learning (11 — claude already listed above conceptually, so 11 stubs)
    {"name": "claude", "category": "AI & Machine Learning"},
    {"name": "cohere", "category": "AI & Machine Learning"},
    {"name": "elevenlabs", "category": "AI & Machine Learning"},
    {"name": "minimax", "category": "AI & Machine Learning"},
    {"name": "mistral-ai", "category": "AI & Machine Learning"},
    {"name": "ollama", "category": "AI & Machine Learning"},
    {"name": "opencode-ai", "category": "AI & Machine Learning"},
    {"name": "replicate", "category": "AI & Machine Learning"},
    {"name": "runwayml", "category": "AI & Machine Learning"},
    {"name": "together-ai", "category": "AI & Machine Learning"},
    {"name": "voltagent", "category": "AI & Machine Learning"},
    {"name": "x-ai", "category": "AI & Machine Learning"},

    # Developer Tools & Platforms (13 stubs — vercel and linear are fully described above)
    {"name": "cursor", "category": "Developer Tools & Platforms"},
    {"name": "expo", "category": "Developer Tools & Platforms"},
    {"name": "lovable", "category": "Developer Tools & Platforms"},
    {"name": "mintlify", "category": "Developer Tools & Platforms"},
    {"name": "posthog", "category": "Developer Tools & Platforms"},
    {"name": "raycast", "category": "Developer Tools & Platforms"},
    {"name": "resend", "category": "Developer Tools & Platforms"},
    {"name": "sentry", "category": "Developer Tools & Platforms"},
    {"name": "supabase", "category": "Developer Tools & Platforms"},
    {"name": "superhuman", "category": "Developer Tools & Platforms"},
    {"name": "warp", "category": "Developer Tools & Platforms"},
    {"name": "zapier", "category": "Developer Tools & Platforms"},
    # github is already fully described; tailwind too

    # Infrastructure & Cloud (5 stubs — stripe is fully described above)
    {"name": "clickhouse", "category": "Infrastructure & Cloud"},
    {"name": "composio", "category": "Infrastructure & Cloud"},
    {"name": "hashicorp", "category": "Infrastructure & Cloud"},
    {"name": "mongodb", "category": "Infrastructure & Cloud"},
    {"name": "sanity", "category": "Infrastructure & Cloud"},

    # Design & Productivity (8 stubs — notion, figma, airtable are fully described above)
    {"name": "cal", "category": "Design & Productivity"},
    {"name": "clay", "category": "Design & Productivity"},
    {"name": "framer", "category": "Design & Productivity"},
    {"name": "intercom", "category": "Design & Productivity"},
    {"name": "miro", "category": "Design & Productivity"},
    {"name": "pinterest", "category": "Design & Productivity"},
    {"name": "webflow", "category": "Design & Productivity"},

    # Fintech & Crypto (4 stubs)
    {"name": "coinbase", "category": "Fintech & Crypto"},
    {"name": "kraken", "category": "Fintech & Crypto"},
    {"name": "revolut", "category": "Fintech & Crypto"},
    {"name": "wise", "category": "Fintech & Crypto"},

    # Enterprise & Consumer (7 stubs — apple and spotify are fully described above)
    {"name": "airbnb", "category": "Enterprise & Consumer"},
    {"name": "bmw", "category": "Enterprise & Consumer"},
    {"name": "ibm", "category": "Enterprise & Consumer"},
    {"name": "nvidia", "category": "Enterprise & Consumer"},
    {"name": "spacex", "category": "Enterprise & Consumer"},
    {"name": "uber", "category": "Enterprise & Consumer"},
]


def get_template(name: str) -> dict | None:
    """Look up a template by name (case-insensitive)."""
    name_lower = name.lower().replace(" ", "-").replace("_", "-")
    for t in TEMPLATES:
        if t["name"] == name_lower:
            return t
    return None


def list_templates(category: str | None = None) -> list[dict]:
    """List all templates, optionally filtered by category."""
    if category:
        return [t for t in TEMPLATES if t.get("category") == category]
    return list(TEMPLATES)


def get_categories() -> list[str]:
    """Return all unique categories in order of first appearance."""
    seen = []
    for t in TEMPLATES:
        cat = t.get("category", "Uncategorized")
        if cat not in seen:
            seen.append(cat)
    return seen
