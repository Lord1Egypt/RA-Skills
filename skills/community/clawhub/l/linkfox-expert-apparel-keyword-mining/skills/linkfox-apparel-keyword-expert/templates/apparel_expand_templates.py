# Apparel-specific expansion templates for Amazon Suggestions mining
# Used by linkfox-apparel-keyword-expert

APPAREL_EXPAND_TEMPLATES = {
    "length": [
        "above the knee",
        "mid thigh",
        "midi",
        "maxi",
        "ankle length",
        "tea length",
        "floor length",
        "mini",
        "knee length",
        "high low",
        "mid-thigh length",
        "above-the-knee",
    ],
    "neckline": [
        "v neck",
        "off shoulder",
        "off the shoulder",
        "one shoulder",
        "halter",
        "square neck",
        "scoop neck",
        "cowl neck",
        "boat neck",
        "sweetheart",
        "collared",
        "v-neck",
        "off-the-shoulder",
    ],
    "sleeve": [
        "sleeveless",
        "short sleeve",
        "long sleeve",
        "3/4 sleeve",
        "cap sleeve",
        "puff sleeve",
        "bell sleeve",
        "flutter sleeve",
        "cold shoulder",
        "short-sleeve",
        "long-sleeve",
    ],
    "silhouette": [
        "a-line",
        "bodycon",
        "wrap",
        "fit and flare",
        "shift",
        "sheath",
        "empire waist",
        "peplum",
        "babydoll",
        "shirt dress",
        "fit & flare",
        "a line",
    ],
    "occasion": [
        "casual",
        "wedding guest",
        "party",
        "cocktail",
        "vacation",
        "beach",
        "work",
        "office",
        "formal",
        "prom",
        "homecoming",
        "date night",
        "wedding",
        "evening",
    ],
    "audience": [
        "for women",
        "for ladies",
        "petite",
        "plus size",
        "maternity",
        "juniors",
        "tall",
        "for her",
    ],
    "style_feature": [
        "floral",
        "solid",
        "striped",
        "with pockets",
        "with belt",
        "ruffle",
        "smocked",
        "tiered",
        "flowy",
        "elegant",
        "boho",
        "sexy",
        "polka dot",
        "geometric",
    ],
}

# Flat list for quick access in expand / gap modes
APPAREL_ALL_MODIFIERS = []
for group in APPAREL_EXPAND_TEMPLATES.values():
    APPAREL_ALL_MODIFIERS.extend(group)

# Default mining modes for apparel
DEFAULT_MODES = ["expand", "az", "numbers", "reverse", "gap"]

# Priority order when applying templates
TEMPLATE_PRIORITY = [
    "length",
    "neckline",
    "sleeve",
    "silhouette",
    "occasion",
    "audience",
    "style_feature",
]
