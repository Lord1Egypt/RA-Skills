#!/usr/bin/env python3
"""
Styx Descriptor Parser — resolves garbled credit card transaction names into
real business names using prefix dictionaries and regex cleaning.

Usage:
    from styx_parser import parse_descriptor, lookup_mcc

    result = parse_descriptor("ABM-350 MISSION GARAGE")
    # {'raw': 'ABM-350 MISSION GARAGE', 'cleaned': 'Mission Garage',
    #  'prefix': 'ABM', 'suffix': '350', 'confidence': 0.7, 'method': 'prefix_stripped'}
"""

import json
import re
import sqlite3

# ── Prefix dictionary ────────────────────────────────────────────────────────
# Maps known credit card transaction prefixes to their meaning.
# Built from: psrikanthm/expense-report, merchant-cleanup repos,
# and manual curation from real transaction data.

PREFIX_DICT = {
    # Payment processors / aggregators
    "SQ": "Square",
    "TST": "Toast",
    "SP": "Stripe/Shopify",
    "PYPL": "PayPal",
    "DD": "DoorDash",
    "UE": "Uber Eats",
    "GR": "Grubhub",
    "SPOT": "Spotify",
    "APPL": "Apple",
    "GOOG": "Google",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "EBAY": "eBay",
    "FB": "Facebook/Meta",
    "INSTA": "Instagram",
    "TWTR": "Twitter",
    "LINKD": "LinkedIn",
    "NETFLIX": "Netflix",
    "HULU": "Hulu",
    "DISNEY": "Disney+",
    "PARAMOUNT": "Paramount+",
    "HBO": "HBO Max",
    "SQUARE": "Square",
    "STRIPE": "Stripe",
    "SHOPIFY": "Shopify",
    "VENMO": "Venmo",
    "ZELLE": "Zelle",
    "CASHAPP": "Cash App",
    "WISE": "Wise",
    "REMITLY": "Remitly",
    "WU": "Western Union",
    "MG": "MoneyGram",
    # Bank / card prefixes
    "ABM": "",           # ATM/Bank Machine — strip, keep suffix
    "TCB": "",           # Transaction Credit Bank — strip
    "MED": "",           # Medical — strip prefix
    "FSP": "",           # Facility Service Payment — strip
    "ABC": "",           # American Business Card — strip
    "POS": "POS",        # Point of Sale — keep
    "POSH": "Poshmark",  # Poshmark
    "TGT": "Target",     # Target
    "WMT": "Walmart",    # Walmart
    "COSTCO": "Costco",  # Costco
    "SAFEWAY": "Safeway", # Safeway
    "TRADER": "Trader Joe's", # Trader Joe's
    "WHOLE": "Whole Foods",  # Whole Foods
    "UBER": "Uber",      # Uber
    "LYFT": "Lyft",      # Lyft
    "UNITED": "United Airlines",
    "DELTA": "Delta Airlines",
    "AMERICAN": "American Airlines",
    "SOUTHWEST": "Southwest Airlines",
    "ALASKA": "Alaska Airlines",
    "JETBLUE": "JetBlue",
    "SPIRIT": "Spirit Airlines",
    "FRONTIER": "Frontier Airlines",
    "HOTEL": "Hotel",
    "HILTON": "Hilton",
    "MARRIOTT": "Marriott",
    "HYATT": "Hyatt",
    "IHG": "IHG Hotels",
    "WYNDHAM": "Wyndham",
    "AIRBNB": "Airbnb",
    "BOOKING": "Booking.com",
    "EXPEDIA": "Expedia",
    "TRIPADVISOR": "TripAdvisor",
    "YELP": "Yelp",
    "OPENTABLE": "OpenTable",
    "TOCK": "Tock",
    "RESY": "Resy",
    "DOORDASH": "DoorDash",
    "POSTMATES": "Postmates",
    "INSTACART": "Instacart",
    "SHIPT": "Shipt",
    "GRUBHUB": "Grubhub",
    "SEAMLESS": "Seamless",
    "CAVIAR": "Caviar",
    "DELIVEROO": "Deliveroo",
    "JUSTEAT": "Just Eat",
    "TAKEAWAY": "Takeaway",
    "BIRD": "Bird",
    "LIME": "Lime",
    "SPIN": "Spin",
    "WAYMO": "Waymo",
    "CRUISE": "Cruise",
    "TESLA": "Tesla",
    "RIVIAN": "Rivian",
    "LUCID": "Lucid",
    "FORD": "Ford",
    "GM": "GM",
    "TOYOTA": "Toyota",
    "HONDA": "Honda",
    "BMW": "BMW",
    "MERCEDES": "Mercedes",
    "AUDI": "Audi",
    "VOLKSWAGEN": "Volkswagen",
    "PORSCHE": "Porsche",
    "FERRARI": "Ferrari",
    "LAMBO": "Lamborghini",
    "MCLAREN": "McLaren",
    "ASTON": "Aston Martin",
    "ROLLS": "Rolls Royce",
    "BENTLEY": "Bentley",
    "JAGUAR": "Jag",
    "LAND": "Land Rover",
    "RANGE": "Range Rover",
    "MINI": "Mini",
    "SMART": "Smart",
    "FIAT": "Fiat",
    "ALFA": "Alfa Romeo",
    "MASERATI": "Maserati",
    "BUGATTI": "Bugatti",
    "KOENIGSEGG": "Koenigsegg",
    "PAGANI": "Pagani",
    "SPYKER": "Spyker",
    "MAYBACH": "Maybach",
    "GENESIS": "Genesis",
    "INFINITI": "Infiniti",
    "ACURA": "Acura",
    "LEXUS": "Lexus",
    "LINCOLN": "Lincoln",
    "CADILLAC": "Cadillac",
    "CHRYSLER": "Chrysler",
    "DODGE": "Dodge",
    "JEEP": "Jeep",
    "RAM": "Ram",
    "GMC": "GMC",
    "BUICK": "Buick",
    "CHEVROLET": "Chevrolet",
    "CHEVY": "Chevy",
    "CORVETTE": "Corvette",
    "CAMARO": "Camaro",
    "MUSTANG": "Mustang",
    "CHARGER": "Charger",
    "CHALLENGER": "Challenger",
    "VIPER": "Viper",
    "DURANGO": "Durango",
    "F150": "F-150",
    "SILVERADO": "Silverado",
    "SIERRA": "Sierra",
    "CANYON": "Canyon",
    "COLORADO": "Colorado",
    "TACOMA": "Tacoma",
    "TUNDRA": "Tundra",
    "PATHFINDER": "Pathfinder",
    "ROGUE": "Rogue",
    "MURANO": "Murano",
    "MAXIMA": "Maxima",
    "ALTIMA": "Altima",
    "SENTRA": "Sentra",
    "VERSA": "Versa",
    "LEAF": "Leaf",
    "OUTBACK": "Outback",
    "FORESTER": "Forester",
    "CROSSTREK": "Crosstrek",
    "IMPREZA": "Impreza",
    "WRX": "WRX",
    "STI": "STI",
    "LEGACY": "Legacy",
    "BRZ": "BRZ",
    "MIRAGE": "Mirage",
    "LANCER": "Lancer",
    "ECLIPSE": "Eclipse",
    "GALANT": "Galant",
    "MONTERO": "Montero",
    "OUTLANDER": "Outlander",
    "ASX": "ASX",
    "CROSS": "Cross",
    "RAV4": "RAV4",
    "HIGHLANDER": "Highlander",
    "4RUNNER": "4Runner",
    "SEQUOIA": "Sequoia",
    "LANDCRUISER": "Land Cruiser",
    "PRADO": "Prado",
    "FJ": "FJ Cruiser",
    "CX": "CX",
    "MAZDA3": "Mazda3",
    "MAZDA6": "Mazda6",
    "MX5": "MX-5",
    "MIATA": "Miata",
    "RX": "RX",
    "IS": "IS",
    "ES": "ES",
    "GS": "GS",
    "LS": "LS",
    "NX": "NX",
    "GX": "GX",
    "LX": "LX",
    "RC": "RC",
    "LC": "LC",
    "CT": "CT",
    "HS": "HS",
    "SC": "SC",
    "LFA": "LFA",
}

# ── Regex patterns ───────────────────────────────────────────────────────────

# Store/location numbers: "350", "1234", etc. at start of name
STORE_NUMBER_RE = re.compile(r'^\d{2,5}\s+')

# Phone fragments: "<phone>", "<phone>", etc.
PHONE_RE = re.compile(r'[\(\)\-\d]{7,}')

# Trailing state codes: " CA", " NY", " TX", etc.
STATE_CODE_RE = re.compile(r'\s+[A-Z]{2}$')

# Trailing zip codes: " 94105", " 94105-1234"
ZIP_RE = re.compile(r'\s+\d{5}(-\d{4})?$')

# Asterisks (redaction)
ASTERISK_RE = re.compile(r'\*+')

# Multiple spaces
MULTI_SPACE_RE = re.compile(r'\s+')

# ── MCC lookup ───────────────────────────────────────────────────────────────

MCC_CODES = {
    "5411": "Grocery Stores, Supermarkets",
    "5422": "Freezer and Locker Meat Provisioners",
    "5441": "Candy, Nut, Confectionery Stores",
    "5451": "Dairy Products Stores",
    "5461": "Bakeries",
    "5462": "Miscellaneous Food Stores",
    "5499": "Miscellaneous Food Stores",
    "5511": "Car and Truck Dealers",
    "5521": "Car and Truck Dealers",
    "5531": "Auto and Home Supply Stores",
    "5532": "Automotive Tire Stores",
    "5533": "Automotive Parts and Accessories Stores",
    "5541": "Service Stations",
    "5542": "Automated Fuel Dispensers",
    "5551": "Boat Dealers",
    "5561": "Camper, Recreational and Utility Trailer Dealers",
    "5571": "Motorcycle Shops and Dealers",
    "5592": "Motor Homes Dealers",
    "5598": "Snowmobile Dealers",
    "5599": "Miscellaneous Automotive, Aircraft, and Farm Equipment Dealers",
    "5611": "Men's and Boy's Clothing and Accessories Stores",
    "5621": "Women's Ready-to-Wear Stores",
    "5631": "Women's Accessory and Specialty Shops",
    "5641": "Children's and Infant's Wear Stores",
    "5651": "Family Clothing Stores",
    "5655": "Sports and Riding Apparel Stores",
    "5661": "Shoe Stores",
    "5681": "Furriers and Fur Shops",
    "5691": "Men's and Women's Clothing Stores",
    "5697": "Tailors, Seamstress, Mending, and Alterations",
    "5698": "Wig and Toupee Stores",
    "5699": "Miscellaneous Apparel and Accessory Shops",
    "5712": "Furniture, Home Furnishings and Equipment Stores",
    "5713": "Floor Covering Stores",
    "5714": "Drapery, Window Covering, and Upholstery Stores",
    "5718": "Fireplace, Fireplace Screens, and Accessories Stores",
    "5719": "Miscellaneous Home Furnishing Specialty Stores",
    "5722": "Household Appliance Stores",
    "5732": "Electronics Stores",
    "5733": "Music Stores, Musical Instruments, Pianos",
    "5734": "Computer Software Stores",
    "5735": "Record Stores",
    "5811": "Caterers",
    "5812": "Eating Places, Restaurants",
    "5813": "Drinking Places, Alcoholic Beverages",
    "5814": "Fast Food Restaurants",
    "5815": "Digital Goods Media, Books, Movies, Music",
    "5816": "Digital Goods Games",
    "5817": "Digital Goods Applications",
    "5818": "Digital Goods Large Digital Goods Merchant",
    "5912": "Drug Stores and Pharmacies",
    "5921": "Package Stores, Beer, Wine, and Liquor",
    "5931": "Used Merchandise and Secondhand Stores",
    "5932": "Antique Shops",
    "5933": "Pawn Shops",
    "5935": "Wrecking and Salvage Yards",
    "5937": "Antique Reproductions Stores",
    "5940": "Bicycle Shops",
    "5941": "Sporting Goods Stores",
    "5942": "Book Stores",
    "5943": "Stationery Stores, Office and School Supply Stores",
    "5944": "Jewelry Stores, Watches, Clocks, and Silverware Stores",
    "5945": "Hobby, Toy, and Game Shops",
    "5946": "Camera and Photographic Supply Stores",
    "5947": "Gift, Card, Novelty, and Souvenir Shops",
    "5948": "Luggage and Leather Goods Stores",
    "5949": "Sewing, Needlework, Fabric, and Piece Goods Stores",
    "5950": "Glassware, Crystal Stores",
    "5960": "Direct Marketing Insurance Services",
    "5962": "Direct Marketing Travel Related Arrangements",
    "5963": "Door-to-Door Sales",
    "5964": "Direct Marketing Catalog Merchant",
    "5965": "Direct Marketing Combination Catalog and Retail Merchant",
    "5966": "Direct Marketing Outbound Telemarketing Merchant",
    "5967": "Direct Marketing Inbound Telemarketing Merchant",
    "5968": "Direct Marketing Continuity/Subscription Merchant",
    "5969": "Direct Marketing Other",
    "5970": "Artists Supply and Craft Shops",
    "5971": "Art Dealers and Galleries",
    "5972": "Stamp and Coin Stores",
    "5973": "Religious Goods Stores",
    "5975": "Hearing Aids Sales, Service, and Supply Stores",
    "5976": "Orthopedic Goods, Prosthetic Devices",
    "5977": "Cosmetic Stores",
    "5978": "Typewriter Stores",
    "5983": "Fuel Dealers",
    "5992": "Florists",
    "5993": "Cigar Stores and Stands",
    "5994": "News Dealers and Newsstands",
    "5995": "Pet Shops, Pet Food, and Supplies",
    "5996": "Swimming Pools, Sales, Service, and Supplies",
    "5997": "Electric Razor Stores",
    "5998": "Tent and Awning Shops",
    "5999": "Miscellaneous and Specialty Retail Stores",
    "6010": "Financial Institutions, Manual Cash Disbursements",
    "6011": "Financial Institutions, Automated Cash Disbursements",
    "6012": "Financial Institutions, Merchandise and Services",
    "6050": "Quasi Cash, Financial Institutions",
    "6051": "Quasi Cash, Non-Financial Institutions",
    "6211": "Securities, Brokers/Dealers",
    "6300": "Insurance Sales, Underwriting, and Premiums",
    "6513": "Real Estate Agents and Managers, Rentals",
    "6529": "Remote Stored Value Load",
    "6530": "Remove Stored Value Load",
    "6531": "Payment Service Provider, Money Transfer for a Purchase",
    "6532": "Payment Service Provider, Member Financial Institution, Payment Transaction",
    "6533": "Payment Service Provider, Merchant, Payment Transaction",
    "6534": "Money Transfer, Financial Institution, Value Load",
    "6535": "Value Card, Financial Institution, Remote Load",
    "6536": "Money Transfer, Financial Institution, Remote Load",
    "6537": "Money Transfer, Financial Institution, Remote Load",
    "6538": "Money Transfer, Financial Institution, Remote Load",
    "6540": "POI Funding Transactions",
    "6550": "Funding Transactions, Non-Financial Institution",
    "7011": "Lodging, Hotels, Motels, Resorts",
    "7012": "Timeshares",
    "7032": "Sporting and Recreational Camps",
    "7033": "Trailer Parks and Campgrounds",
    "7210": "Laundry, Cleaning, and Garment Services",
    "7211": "Laundry, Family and Commercial",
    "7216": "Dry Cleaners",
    "7217": "Carpet and Upholstery Cleaning",
    "7221": "Photographic Studios",
    "7230": "Beauty and Barber Shops",
    "7251": "Shoe Repair Shops and Hat Cleaning Shops",
    "7261": "Funeral Service and Crematories",
    "7273": "Dating and Escort Services",
    "7276": "Tax Preparation Service",
    "7277": "Counseling Service, Debt, Marriage, Personal",
    "7278": "Buying/Shopping Services, Clubs",
    "7296": "Clothing Rental, Costumes, Formal Wear, Uniforms",
    "7297": "Massage Parlors",
    "7298": "Health and Beauty Spas",
    "7299": "Miscellaneous Personal Services",
    "7311": "Advertising Services",
    "7321": "Consumer Credit Reporting Agencies",
    "7322": "Debt Collection Agencies",
    "7333": "Commercial Photography, Art, and Graphics",
    "7338": "Quick Copy, Reproduction, and Blueprinting Services",
    "7339": "Stenographic and Secretarial Support Services",
    "7342": "Exterminating and Disinfecting Services",
    "7349": "Cleaning, Maintenance, and Janitorial Services",
    "7361": "Employment Agencies, Temporary Help Services",
    "7372": "Computer Programming, Data Processing, and Integrated Systems Design Services",
    "7375": "Information Retrieval Services",
    "7379": "Computer Maintenance, Repair, and Services",
    "7392": "Management, Consulting, and Public Relations Services",
    "7393": "Detective, Protective, and Security Services",
    "7394": "Equipment, Tool, Furniture, and Appliance Rental and Leasing",
    "7395": "Photofinishing Laboratories, Photo Developing",
    "7399": "Miscellaneous Business Services",
    "7511": "Truck Stop",
    "7512": "Car Rental Agencies",
    "7513": "Truck and Utility Trailer Rentals",
    "7519": "Motor Home and Recreational Vehicle Rentals",
    "7523": "Parking Lots and Garages",
    "7531": "Automotive Body Repair Shops",
    "7534": "Tire Retreading and Repair Shops",
    "7535": "Automotive Paint Shops",
    "7538": "Automotive Service Shops",
    "7542": "Car Washes",
    "7549": "Towing Services",
    "7622": "Electronics Repair Shops",
    "7623": "Air Conditioning and Refrigeration Repair Shops",
    "7629": "Electrical and Small Appliance Repair Shops",
    "7631": "Watch, Clock, and Jewelry Repair Shops",
    "7641": "Furniture, Reupholstery, Repair, and Refinishing",
    "7692": "Welding Repair",
    "7699": "Miscellaneous Repair Shops and Related Services",
    "7829": "Motion Picture and Video Tape Production and Distribution",
    "7832": "Motion Picture Theaters",
    "7833": "Drive-In Motion Picture Theaters",
    "7841": "Video Tape Rental Stores",
    "7911": "Dance Halls, Studios, and Schools",
    "7922": "Theatrical Producers and Miscellaneous Services",
    "7929": "Bands, Orchestras, and Miscellaneous Entertainers",
    "7932": "Billiard and Pool Establishments",
    "7933": "Bowling Alleys",
    "7941": "Commercial Sports, Athletic Fields, Professional Sport Clubs",
    "7991": "Tourist Attractions and Exhibits",
    "7992": "Golf Courses, Public",
    "7993": "Video Amusement Game Supplies",
    "7994": "Video Game Arcades and Establishments",
    "7995": "Betting, including Lottery Tickets, Casino Gaming Chips, Off-Track Betting",
    "7996": "Amusement Parks, Carnivals, Circuses, Fortune Tellers",
    "7997": "Membership Clubs, Recreation, Athletic, Country Clubs",
    "7998": "Aquariums, Seaquariums, Dolphinariums, Zoos",
    "7999": "Recreation Services",
    "8011": "Doctors, Physicians",
    "8021": "Dentists, Orthodontists",
    "8031": "Osteopaths",
    "8041": "Chiropractors",
    "8042": "Optometrists, Ophthalmologists",
    "8043": "Opticians, Optical Goods, and Eyeglasses",
    "8049": "Podiatrists, Chiropodists",
    "8050": "Nursing and Personal Care Facilities",
    "8062": "Hospitals",
    "8071": "Medical and Dental Laboratories",
    "8099": "Medical Services and Health Practitioners",
    "8111": "Legal Services, Attorneys",
    "8211": "Elementary and Secondary Schools",
    "8220": "Colleges, Universities, Professional Schools, and Junior Colleges",
    "8241": "Correspondence Schools",
    "8244": "Business and Secretarial Schools",
    "8249": "Vocational and Trade Schools",
    "8299": "Schools and Educational Services",
    "8351": "Child Care Services",
    "8398": "Charitable and Social Service Organizations",
    "8641": "Civic, Social, and Fraternal Associations",
    "8651": "Political Organizations",
    "8661": "Religious Organizations",
    "8675": "Automobile Associations",
    "8699": "Membership Organizations",
    "8734": "Testing Laboratories",
    "8911": "Architectural, Engineering, and Surveying Services",
    "8931": "Accounting, Auditing, and Bookkeeping Services",
    "8999": "Professional Services",
    "9211": "Court Costs, Including Alimony and Child Support",
    "9222": "Fines",
    "9223": "Bail and Bond Payments",
    "9311": "Tax Payments",
    "9399": "Government Services",
    "9401": "Government-Owned Lotteries",
    "9402": "Government-Owned Lotteries",
    "9950": "Intra-Company Purchases",
}

def lookup_mcc(mcc_code):
    """Look up a Merchant Category Code."""
    return MCC_CODES.get(mcc_code, None)

# ── Main parser ──────────────────────────────────────────────────────────────

def parse_descriptor(raw_name):
    """Parse a credit card transaction descriptor.

    Returns a dict with:
        - raw: original name
        - cleaned: cleaned name
        - prefix: identified prefix (if any)
        - suffix: store/location number (if any)
        - confidence: 0.0-1.0
        - method: how it was parsed
    """
    if not raw_name:
        return {'raw': '', 'cleaned': '', 'prefix': None, 'suffix': None,
                'confidence': 0.0, 'method': 'empty'}

    result = {
        'raw': raw_name,
        'cleaned': raw_name,
        'prefix': None,
        'suffix': None,
        'confidence': 0.0,
        'method': 'raw',
    }

    # Check if fully redacted
    if ASTERISK_RE.search(raw_name) and len(ASTERISK_RE.findall(raw_name)[0]) > 5:
        # Try to extract base name before asterisks
        base = ASTERISK_RE.split(raw_name)[0].strip()
        if base and len(base) > 2:
            result['cleaned'] = base
            result['confidence'] = 0.3
            result['method'] = 'redacted_base'
        return result

    # Try to identify and strip prefix
    cleaned = raw_name.strip()
    identified_prefix = None

    # Check for known prefixes (case-insensitive)
    for prefix, meaning in PREFIX_DICT.items():
        pattern = re.compile(r'^' + re.escape(prefix) + r'[\s\*\-]', re.IGNORECASE)
        if pattern.match(cleaned):
            identified_prefix = prefix
            cleaned = pattern.sub('', cleaned).strip()
            break

    # Strip store numbers
    store_num_match = STORE_NUMBER_RE.match(cleaned)
    if store_num_match:
        result['suffix'] = store_num_match.group().strip()
        cleaned = STORE_NUMBER_RE.sub('', cleaned).strip()

    # Strip phone fragments
    cleaned = PHONE_RE.sub('', cleaned).strip()

    # Strip trailing state codes
    cleaned = STATE_CODE_RE.sub('', cleaned).strip()

    # Strip trailing zip codes
    cleaned = ZIP_RE.sub('', cleaned).strip()

    # Strip asterisks
    cleaned = ASTERISK_RE.sub('', cleaned).strip()

    # Collapse multiple spaces
    cleaned = MULTI_SPACE_RE.sub(' ', cleaned).strip()

    # Title case for readability
    if cleaned:
        cleaned = cleaned.title()

    result['cleaned'] = cleaned
    result['prefix'] = identified_prefix

    # Confidence based on how much we could clean
    if identified_prefix and cleaned:
        result['confidence'] = 0.7
        result['method'] = 'prefix_stripped'
    elif cleaned and cleaned != raw_name:
        result['confidence'] = 0.5
        result['method'] = 'regex_cleaned'
    elif cleaned:
        result['confidence'] = 0.9
        result['method'] = 'already_clean'

    return result


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Styx Descriptor Parser')
    subparsers = parser.add_subparsers(dest='command')

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse a transaction descriptor')
    parse_parser.add_argument('descriptor', help='Transaction descriptor to parse')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process from Styx DB')
    batch_parser.add_argument('--limit', type=int, default=50, help='Max to process')
    batch_parser.add_argument('--city', default='San Francisco', help='City (for display only)')

    args = parser.parse_args()

    if args.command == 'parse':
        result = parse_descriptor(args.descriptor)
        print(json.dumps(result, indent=2))

    elif args.command == 'batch':
        # Process unresolved transactions from Styx DB
        styx_db = '~/.hermes/data/styx.db'
        txn_db = '~/.hermes/data/transactions.db'
        conn = sqlite3.connect(styx_db)
        conn.execute(f'ATTACH DATABASE "{txn_db}" AS txndb')

        rows = conn.execute('''
            SELECT t.transaction_id, t.name, t.merchant_name, t.amount, t.date,
                   t.personal_finance_category
            FROM txndb.transactions t
            LEFT JOIN transaction_merchants tm ON t.transaction_id = tm.transaction_id
            WHERE tm.id IS NULL
            ORDER BY t.date DESC
            LIMIT ?
        ''', (args.limit,)).fetchall()

        print(f"Processing {len(rows)} unresolved transactions...")
        for txn_id, name, merchant_name, amount, date, pfc in rows:
            raw = name or merchant_name or ''
            result = parse_descriptor(raw)
            status = "✓" if result['confidence'] >= 0.5 else "?"
            print(f"  {status} {raw[:40]:40s} → {result['cleaned'][:30]:30s} "
                  f"(conf: {result['confidence']:.2f}, method: {result['method']})")

        conn.close()

    else:
        parser.print_help()