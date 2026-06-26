# Poe.ninja API Skill

Path of Exile market price query tool using the poe.ninja API.

## Features

- 🔍 **Currency Query** - Check Chaos, Divine, Mirror and other currency rates
- 📦 **Item Query** - Support for 29 item types (equipment, skill gems, maps, etc.)
- 🔎 **Cross-type Search** - Search across all item types at once
- 📊 **Price Trends** - Display price change percentages

## Installation

### Method 1: Install .skill file directly

Download `poe-ninja-api.skill` and place it in your skills directory:

```bash
# macOS
cp poe-ninja-api.skill ~/.qclaw/skills/

# Extract
cd ~/.qclaw/skills
unzip poe-ninja-api.skill
```

### Method 2: Install from source

```bash
git clone https://github.com/qpooqp77/poe-ninja-api.git
cd poe-ninja-api
```

## Usage

### Using in QClaw/OpenClaw

After installation, query using natural language:

- "Check Divine Orb price"
- "How much is Mageblood"
- "Search for Mirror related items"

### Command Line Usage

#### Query currency prices

```bash
python scripts/get_currency.py --league Settlers
python scripts/get_currency.py --league Standard --search "divine"
```

#### Query item prices

```bash
python scripts/get_item.py --league Settlers --type UniqueWeapon
python scripts/get_item.py --league Standard --type SkillGem --search "Enlighten"
```

#### Cross-type search

```bash
python scripts/search_item.py --league Standard --query "Mirror"
python scripts/search_item.py --league Standard --query "Mageblood" --min-price 1000
```

## Supported Item Types

### Currency Types (currencyoverview)

| Type | Description |
|------|-------------|
| Currency | Currency items (Chaos, Divine, Mirror, etc.) |
| Fragment | Fragments |

### Item Types (itemoverview)

| Type | Description |
|------|-------------|
| Oil | Oils |
| Incubator | Incubators |
| Scarab | Scarabs |
| Fossil | Fossils |
| Resonator | Resonators |
| Essence | Essences |
| DivinationCard | Divination Cards |
| SkillGem | Skill Gems |
| BaseType | Base Types |
| HelmetEnchant | Helmet Enchants |
| UniqueMap | Unique Maps |
| Map | Maps |
| UniqueJewel | Unique Jewels |
| UniqueFlask | Unique Flasks |
| UniqueWeapon | Unique Weapons |
| UniqueArmour | Unique Armours |
| UniqueAccessory | Unique Accessories |
| Beast | Beasts |
| Vial | Vials |
| DeliriumOrb | Delirium Orbs |
| Omen | Omens |
| UniqueRelic | Unique Relics |
| ClusterJewel | Cluster Jewels |
| BlightedMap | Blighted Maps |
| BlightRavagedMap | Blight Ravaged Maps |
| Invitation | Invitations |
| Memory | Memories |
| Coffin | Coffins |
| AllflameEmber | Allflame Embers |

## API Source

This tool uses the public API provided by [poe.ninja](https://poe.ninja).

- API Documentation: [ayberkgezer/poe.ninja-API-Document](https://github.com/ayberkgezer/poe.ninja-API-Document)

## Notes

1. **League Name** - League names change each season, use the current league name
2. **Price Updates** - poe.ninja data updates hourly
3. **Low Confidence Data** - Prices may be inaccurate when trading volume is low
4. **Request Rate** - Avoid making too many requests in a short period

## Documentation

- [README.zh-TW.md](README.zh-TW.md) - Traditional Chinese documentation

## License

MIT License

## Author

Created for QClaw/OpenClaw
