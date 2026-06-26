#!/usr/bin/env python3
"""
Suggest HS chapters for a product based on its description.
"""

import sys
import json
import re
from typing import List, Dict, Tuple

# Comprehensive product category mapping
PRODUCT_CATEGORIES = {
    # Electronics / Electrical (Chapter 85)
    "phone": ("85", ["mobile", "cellular", "smartphone", "telephone"]),
    "mobile": ("85", ["phone", "cellular", "smart"]),
    "charger": ("85", ["adapter", "power", "charging"]),
    "charger": ("85", ["adapter", "power", "charging"]),
    "battery": ("85", ["lithium", "rechargeable", "cell"]),
    "cable": ("85", ["wire", "cord", "usb", "hdmi"]),
    "wire": ("74", ["copper", "cable", "electric"]),
    "circuit": ("85", ["pcb", "board", "electronic"]),
    "electronic": ("85", ["device", "component", "part"]),
    "electrical": ("85", ["equipment", "machine", "appliance"]),
    "semiconductor": ("85", ["chip", "ic", "integrated", "circuit"]),
    "led": ("85", ["light", "display", "diode"]),
    "display": ("85", ["screen", "monitor", "lcd", "oled"]),
    "screen": ("85", ["display", "monitor", "panel"]),
    "camera": ("85", ["digital", "security", "cctv"]),
    "sensor": ("85", ["detector", "transducer"]),
    "motor": ("85", ["electric", "dc", "ac"]),
    "transformer": ("85", ["power", "converter"]),
    "switch": ("85", ["button", "control"]),
    "connector": ("85", ["plug", "socket", "jack"]),
    "headphone": ("85", ["earphone", "earbud", "headset"]),
    "earphone": ("85", ["headphone", "earbud"]),
    "earbud": ("85", ["headphone", "earphone", "wireless"]),
    "speaker": ("85", ["audio", "sound", "loudspeaker"]),
    "audio": ("85", ["sound", "music", "speaker"]),
    "microphone": ("85", ["mic", "recording"]),
    "bluetooth": ("85", ["wireless", "headphone", "speaker"]),
    "wireless": ("85", ["bluetooth", "wifi", "radio"]),
    "wifi": ("85", ["wireless", "router", "network"]),
    "router": ("85", ["network", "modem", "wifi"]),
    "modem": ("85", ["network", "communication"]),
    "computer": ("84", ["laptop", "desktop", "server", "tablet"]),
    "laptop": ("84", ["computer", "notebook"]),
    "tablet": ("84", ["ipad", "computer"]),
    "keyboard": ("84", ["computer", "input"]),
    "mouse": ("84", ["computer", "input", "peripheral"]),
    "printer": ("84", ["printing", "scanner"]),
    "scanner": ("84", ["printer", "scanning"]),
    "usb": ("85", ["cable", "connector"]),
    "hdmi": ("85", ["cable", "display"]),
    
    # Machinery (Chapter 84)
    "machine": ("84", ["machinery", "equipment", "device"]),
    "machinery": ("84", ["machine", "equipment", "industrial"]),
    "equipment": ("84", ["machine", "device", "apparatus"]),
    "device": ("84", ["equipment", "machine", "apparatus"]),
    "tool": ("82", ["implement", "cutlery", "hand"]),
    "engine": ("84", ["motor", "combustion"]),
    "pump": ("84", ["compressor", "vacuum"]),
    "compressor": ("84", ["pump", "air"]),
    "generator": ("85", ["power", "electric"]),
    "valve": ("84", ["pipe", "fitting"]),
    "bearing": ("84", ["ball", "roller"]),
    "gear": ("84", ["transmission", "mechanical"]),
    "robot": ("84", ["automation", "industrial"]),
    "automation": ("84", ["robot", "automatic"]),
    
    # Vehicles (Chapter 87)
    "car": ("87", ["automobile", "vehicle"]),
    "automobile": ("87", ["car", "vehicle"]),
    "vehicle": ("87", ["car", "truck", "automotive"]),
    "truck": ("87", ["lorry", "vehicle"]),
    "motorcycle": ("87", ["motorbike", "scooter"]),
    "bicycle": ("87", ["bike", "cycle"]),
    "tire": ("40", ["tyre", "rubber"]),
    "tyre": ("40", ["tire", "rubber"]),
    "wheel": ("87", ["rim", "tire"]),
    "brake": ("87", ["braking", "system"]),
    "transmission": ("84", ["gearbox", "transaxle"]),
    "chassis": ("87", ["frame", "body"]),
    
    # Textiles and Clothing (Chapters 61, 62, 63)
    "clothing": ("61", ["apparel", "garment", "wear"]),
    "apparel": ("61", ["clothing", "garment", "wear"]),
    "garment": ("61", ["clothing", "apparel"]),
    "shirt": ("61", ["blouse", "top", "t-shirt"]),
    "dress": ("62", ["skirt", "gown"]),
    "pants": ("61", ["trousers", "jeans", "shorts"]),
    "jacket": ("61", ["coat", "blazer"]),
    "fabric": ("52", ["cloth", "textile", "material"]),
    "textile": ("52", ["fabric", "cloth", "material"]),
    "cotton": ("52", ["fabric", "textile"]),
    "wool": ("51", ["fabric", "textile"]),
    "silk": ("50", ["fabric", "textile"]),
    "polyester": ("54", ["fabric", "synthetic"]),
    "nylon": ("54", ["fabric", "synthetic"]),
    "yarn": ("52", ["thread", "fiber"]),
    "fiber": ("52", ["fibre", "thread"]),
    "fibre": ("52", ["fiber", "thread"]),
    "shoe": ("64", ["footwear", "boot"]),
    "footwear": ("64", ["shoe", "boot", "sandal"]),
    "bag": ("42", ["handbag", "purse", "backpack"]),
    "handbag": ("42", ["bag", "purse"]),
    "backpack": ("42", ["bag", "rucksack"]),
    
    # Plastics (Chapter 39)
    "plastic": ("39", ["polymer", "resin", "pvc", "polyethylene"]),
    "polymer": ("39", ["plastic", "resin"]),
    "resin": ("39", ["plastic", "polymer"]),
    "pvc": ("39", ["plastic", "pipe"]),
    "bottle": ("39", ["container", "packaging"]),
    "container": ("39", ["box", "packaging"]),
    
    # Chemicals (Chapters 28-38)
    "chemical": ("38", ["compound", "substance"]),
    "paint": ("32", ["coating", "varnish"]),
    "coating": ("32", ["paint", "covering"]),
    "adhesive": ("35", ["glue", "sealant"]),
    "glue": ("35", ["adhesive"]),
    "cosmetic": ("33", ["makeup", "beauty"]),
    "detergent": ("34", ["cleaning", "soap"]),
    "soap": ("34", ["detergent", "cleaning"]),
    "fertilizer": ("31", ["plant", "nutrient"]),
    "pesticide": ("38", ["insecticide", "chemical"]),
    "pharmaceutical": ("30", ["medicine", "drug"]),
    "medicine": ("30", ["pharmaceutical", "drug"]),
    "drug": ("30", ["medicine", "pharmaceutical"]),
    
    # Metals (Chapters 72-83)
    "steel": ("72", ["iron", "metal", "stainless"]),
    "iron": ("72", ["steel", "metal"]),
    "metal": ("73", ["steel", "aluminum", "copper"]),
    "aluminum": ("76", ["aluminium", "metal"]),
    "aluminium": ("76", ["aluminum", "metal"]),
    "copper": ("74", ["brass", "bronze", "metal"]),
    "brass": ("74", ["copper", "alloy"]),
    "hardware": ("73", ["screw", "bolt", "nut"]),
    "screw": ("73", ["bolt", "fastener"]),
    "bolt": ("73", ["screw", "fastener"]),
    
    # Wood and Paper (Chapters 44-49)
    "wood": ("44", ["timber", "lumber"]),
    "timber": ("44", ["wood", "lumber"]),
    "lumber": ("44", ["wood", "timber"]),
    "furniture": ("94", ["chair", "table", "desk"]),
    "chair": ("94", ["furniture", "seat"]),
    "table": ("94", ["furniture", "desk"]),
    "desk": ("94", ["table", "furniture"]),
    "paper": ("48", ["cardboard", "printing"]),
    "cardboard": ("48", ["paper", "packaging"]),
    
    # Food (Chapters 1-24)
    "food": ("16", ["edible", "canned", "prepared"]),
    "beverage": ("22", ["drink", "liquid"]),
    "drink": ("22", ["beverage", "liquid"]),
    "fruit": ("08", ["fresh", "dried"]),
    "vegetable": ("07", ["fresh", "frozen"]),
    "meat": ("02", ["beef", "pork", "chicken"]),
    "fish": ("03", ["seafood", "frozen"]),
    "seafood": ("03", ["fish", "shrimp"]),
    "rice": ("10", ["grain", "cereal"]),
    "grain": ("10", ["rice", "wheat", "cereal"]),
    "wheat": ("10", ["grain", "flour"]),
    "flour": ("11", ["wheat", "powder"]),
    "oil": ("15", ["cooking", "vegetable", "olive"]),
    "sugar": ("17", ["sweetener", "candy"]),
    "coffee": ("09", ["bean", "roasted"]),
    "tea": ("09", ["leaf", "beverage"]),
    "spice": ("09", ["seasoning", "herb"]),
    "chocolate": ("18", ["cocoa", "candy"]),
    "candy": ("17", ["sweet", "confectionery"]),
    
    # Minerals and Construction (Chapters 25-27, 68-70)
    "stone": ("25", ["marble", "granite"]),
    "marble": ("25", ["stone", "tile"]),
    "granite": ("25", ["stone", "tile"]),
    "cement": ("25", ["concrete", "building"]),
    "concrete": ("68", ["cement", "building"]),
    "glass": ("70", ["window", "bottle"]),
    "ceramic": ("69", ["tile", "pottery"]),
    "tile": ("69", ["ceramic", "floor"]),
    
    # Rubber and Leather (Chapters 40-43)
    "rubber": ("40", ["silicone", "latex", "eraser"]),
    "silicone": ("40", ["rubber", "sealant"]),
    "leather": ("41", ["hide", "skin"]),
    "hide": ("41", ["leather", "skin"]),
    
    # Medical and Optical (Chapter 90)
    "medical": ("90", ["hospital", "surgical", "instrument"]),
    "surgical": ("90", ["medical", "operation"]),
    "instrument": ("90", ["device", "tool", "medical"]),
    "lens": ("90", ["optical", "glass", "camera"]),
    "optical": ("90", ["lens", "instrument"]),
    "watch": ("91", ["clock", "timepiece", "wrist"]),
    "clock": ("91", ["watch", "timepiece"]),
    
    # Toys and Sports (Chapter 95)
    "toy": ("95", ["game", "play", "doll"]),
    "game": ("95", ["toy", "playing"]),
    "sports": ("95", ["fitness", "exercise", "equipment"]),
    "fitness": ("95", ["sports", "exercise"]),
    "exercise": ("95", ["fitness", "sports"]),
    
    # Appliances
    "dryer": ("85", ["hair", "blower", "drying"]),
    "blower": ("85", ["hair", "dryer"]),
    "appliance": ("85", ["electrical", "household", "domestic"]),
    "fan": ("84", ["ventilator", "cooling"]),
    "heater": ("85", ["heating", "electro-thermic"]),
    "iron": ("85", ["clothes", "steam", "pressing"]),
    "vacuum": ("85", ["cleaner", "hoover"]),
    "cleaner": ("85", ["vacuum", "appliance"]),
    "refrigerator": ("84", ["fridge", "freezer", "cooling"]),
    "fridge": ("84", ["refrigerator", "cooling"]),
    "washing": ("84", ["machine", "laundry", "washer"]),
    "microwave": ("85", ["oven", "cooking"]),
    "oven": ("85", ["microwave", "cooking", "baking"]),
    "toaster": ("85", ["cooking", "appliance"]),
    "coffee": ("85", ["maker", "machine", "brewer"]),
    
    # Miscellaneous (Chapter 96)
    "pen": ("96", ["ballpoint", "writing"]),
    "pencil": ("96", ["writing", "stationery"]),
    "stationery": ("96", ["paper", "pen", "office"]),
    "button": ("96", ["fastener", "clothing"]),
    "zipper": ("96", ["fastener", "clothing"]),
    "umbrella": ("66", ["rain", "sun"]),
    
    # Jewelry (Chapter 71)
    "jewelry": ("71", ["gold", "silver", "necklace"]),
    "gold": ("71", ["jewelry", "precious"]),
    "silver": ("71", ["jewelry", "precious"]),
    "pearl": ("71", ["jewelry", "precious"]),
    "diamond": ("71", ["jewelry", "gem"]),
}


CHAPTER_DESCRIPTIONS = {
    "01": "Live animals",
    "02": "Meat and edible meat offal",
    "03": "Fish and crustaceans",
    "04": "Dairy produce",
    "05": "Products of animal origin",
    "06": "Live trees and other plants",
    "07": "Edible vegetables",
    "08": "Edible fruit and nuts",
    "09": "Coffee, tea, spices",
    "10": "Cereals",
    "11": "Products of the milling industry",
    "12": "Oil seeds and oleaginous fruits",
    "13": "Lac, gums, resins",
    "14": "Vegetable plaiting materials",
    "15": "Animal or vegetable fats and oils",
    "16": "Preparations of meat, fish",
    "17": "Sugars and sugar confectionery",
    "18": "Cocoa and cocoa preparations",
    "19": "Preparations of cereals, flour",
    "20": "Preparations of vegetables, fruit",
    "21": "Miscellaneous edible preparations",
    "22": "Beverages, spirits and vinegar",
    "23": "Residues from food industries",
    "24": "Tobacco and tobacco substitutes",
    "25": "Salt, sulphur, earths and stone",
    "26": "Ores, slag and ash",
    "27": "Mineral fuels, mineral oils",
    "28": "Inorganic chemicals",
    "29": "Organic chemicals",
    "30": "Pharmaceutical products",
    "31": "Fertilizers",
    "32": "Tanning or dyeing extracts",
    "33": "Essential oils and resinoids",
    "34": "Soap, organic surface-active agents",
    "35": "Albuminoidal substances",
    "36": "Explosives, pyrotechnic products",
    "37": "Photographic or cinematographic goods",
    "38": "Miscellaneous chemical products",
    "39": "Plastics and articles thereof",
    "40": "Rubber and articles thereof",
    "41": "Raw hides and skins",
    "42": "Articles of leather",
    "43": "Furskins and artificial fur",
    "44": "Wood and articles of wood",
    "45": "Cork and articles of cork",
    "46": "Manufactures of straw",
    "47": "Pulp of wood",
    "48": "Paper and paperboard",
    "49": "Printed books, newspapers",
    "50": "Silk",
    "51": "Wool, fine or coarse animal hair",
    "52": "Cotton",
    "53": "Other vegetable textile fibres",
    "54": "Man-made filaments",
    "55": "Man-made staple fibres",
    "56": "Wadding, felt and nonwovens",
    "57": "Carpets and other textile floor coverings",
    "58": "Special woven fabrics",
    "59": "Impregnated, coated textile fabrics",
    "60": "Knitted or crocheted fabrics",
    "61": "Articles of apparel, knitted or crocheted",
    "62": "Articles of apparel, not knitted or crocheted",
    "63": "Other made up textile articles",
    "64": "Footwear, gaiters",
    "65": "Headgear and parts thereof",
    "66": "Umbrellas, sun umbrellas",
    "67": "Prepared feathers and down",
    "68": "Articles of stone, plaster, cement",
    "69": "Ceramic products",
    "70": "Glass and glassware",
    "71": "Natural or cultured pearls, precious stones",
    "72": "Iron and steel",
    "73": "Articles of iron or steel",
    "74": "Copper and articles thereof",
    "75": "Nickel and articles thereof",
    "76": "Aluminium and articles thereof",
    "78": "Lead and articles thereof",
    "79": "Zinc and articles thereof",
    "80": "Tin and articles thereof",
    "81": "Other base metals",
    "82": "Tools, implements, cutlery",
    "83": "Miscellaneous articles of base metal",
    "84": "Nuclear reactors, boilers, machinery",
    "85": "Electrical machinery and equipment",
    "86": "Railway or tramway locomotives",
    "87": "Vehicles other than railway",
    "88": "Aircraft, spacecraft",
    "89": "Ships, boats and floating structures",
    "90": "Optical, photographic, cinematographic",
    "91": "Clocks and watches",
    "92": "Musical instruments",
    "93": "Arms and ammunition",
    "94": "Furniture, bedding, mattresses",
    "95": "Toys, games and sports requisites",
    "96": "Miscellaneous manufactured articles",
    "97": "Works of art, collectors' pieces",
}


def tokenize(text: str) -> List[str]:
    """Tokenize text into words."""
    # Remove punctuation and split
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w.strip() for w in text.split() if len(w.strip()) > 2]


def suggest_chapters(product_name: str) -> Dict:
    """
    Suggest likely chapters for a product.
    
    Args:
        product_name: Product name or description
        
    Returns:
        Dictionary with suggestions
    """
    words = tokenize(product_name)
    all_words = words + product_name.lower().split()
    
    chapter_scores = {}
    matched_keywords = []
    matched_details = []
    
    # Check each word against product categories
    for word in all_words:
        word = word.strip()
        if word in PRODUCT_CATEGORIES:
            chapter, related = PRODUCT_CATEGORIES[word]
            matched_keywords.append(word)
            matched_details.append(f"{word} -> Ch.{chapter}")
            
            # Base score
            chapter_scores[chapter] = chapter_scores.get(chapter, 0) + 10
            
            # Bonus for multiple related keywords
            for related_word in related:
                if related_word in all_words:
                    chapter_scores[chapter] += 5
    
    # Check for multi-word matches (phrases)
    product_lower = product_name.lower()
    for phrase, (chapter, _) in PRODUCT_CATEGORIES.items():
        if " " in phrase and phrase in product_lower:
            matched_keywords.append(phrase)
            chapter_scores[chapter] = chapter_scores.get(chapter, 0) + 15
    
    # Sort by score
    sorted_chapters = sorted(chapter_scores.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "product": product_name,
        "matched_keywords": list(set(matched_keywords)),
        "matched_details": matched_details,
        "suggestions": [
            {
                "chapter": ch,
                "score": score,
                "description": CHAPTER_DESCRIPTIONS.get(ch, "Unknown category")
            }
            for ch, score in sorted_chapters[:5]
        ]
    }


def print_suggestions(result: Dict):
    """Print suggestions in a formatted way."""
    print(f"\nProduct: {result['product']}")
    
    if result['matched_keywords']:
        print(f"Matched keywords: {', '.join(result['matched_keywords'])}")
    
    if not result['suggestions']:
        print("\n⚠️  Could not automatically determine category.")
        print("Common categories:")
        print("  - Electronics: Chapter 85")
        print("  - Machinery: Chapter 84")
        print("  - Clothing: Chapter 61/62")
        print("  - Textiles: Chapter 52-60")
        print("  - Plastics: Chapter 39")
        return
    
    print("\nSuggested chapters:")
    for i, s in enumerate(result['suggestions'], 1):
        print(f"  {i}. Chapter {s['chapter']}: {s['description']}")
    
    best = result['suggestions'][0]
    print(f"\n✓ Best match: Chapter {best['chapter']} - {best['description']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: suggest_chapter.py <product_name>")
        print("\nExamples:")
        print('  python3 suggest_chapter.py "mobile phone charger"')
        print('  python3 suggest_chapter.py "cotton t-shirt"')
        print('  python3 suggest_chapter.py "plastic water bottle"')
        sys.exit(1)
    
    product_name = " ".join(sys.argv[1:])
    result = suggest_chapters(product_name)
    
    # Output as JSON if requested
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_suggestions(result)
