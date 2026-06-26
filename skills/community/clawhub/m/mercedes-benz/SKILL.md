# MBUSA Dealer & Inventory Skill

This OpenClaw skill enables AI agents to query Mercedes-Benz USA (MBUSA.com) data. This is not officially from MBUSA. It allows the agent to find local dealerships in USA and search for live vehicle inventory across New, Pre-Owned, and Certified Pre-Owned (CPO) categories.

## Tools Included

### 1. `get_mbusa_dealers`
Allows the agent to find official Mercedes-Benz dealerships using a US zip code.
* **Primary Use Case:** "Find a Mercedes dealer near 10019" or "Give me the service department number for the dealer in Bayside, NY."
* **Data Returned:** Dealership name, primary address, distance, main phone, service phone, website URL, and service scheduling URL.

### 2. `get_mbusa_inventory`
Allows the agent to search for new vehicle inventory on dealership lots near a specific zip code.
* **Primary Use Case:** "Are there any new EQS sedans under $100,000 near me?" or "Find a 2026 GLC within 50 miles of 30097."
* **Capabilities:** Supports strict enum-based filtering by model, class, body style, brand, interior/exterior colors, fuel type, passenger capacity, highway fuel economy, price range, year, and search radius.
* **Data Returned:** VIN, Stock ID, year, model name, MSRP, engine type, exterior/interior colors, the holding dealership's name, distance, and direct actionable URLs for images and dealer websites.

### 3. `get_mbusa_used_inventory`
Allows the agent to search for **CERTIFIED PRE-OWNED** and **USED** vehicle inventory.
* **Primary Use Case:** "Show me CPO C-Class sedans near 30097 with under 50,000 miles."
* **Capabilities:** Inherits all filters from the New search, but adds a required `invType` parameter (`cpo` or `pre`), expands the `year` search back to 2020, and supports strict enum filtering by `mileage`.

## Configuration & Output
Ensure the `schema.json` file is loaded into your agent's context window. The agent has been explicitly instructed to format the actionable URLs (Image, Dealer Website, Service Scheduling) as clickable Markdown links when responding to the user.




# MBUSA Dealer & Inventory Skill

This OpenClaw skill enables AI agents to query official Mercedes-Benz USA (MBUSA) data. It allows the agent to find local dealerships and search for live vehicle inventory across New, Pre-Owned, and Certified Pre-Owned (CPO) categories.

## Tools Included

### 1. `get_mbusa_dealers`
Allows the agent to find official Mercedes-Benz dealerships using a US zip code.
* **Primary Use Case:** "Find a Mercedes dealer near 10019" or "Give me the service department number for the dealer in Bayside, NY."
* **Data Returned:** Dealership name, primary address, distance, main phone, service phone, website URL, service scheduling URL, and a direct Google Maps URL.

### 2. `get_mbusa_inventory`
Allows the agent to search for **NEW** vehicle inventory on dealership lots near a specific zip code.
* **Primary Use Case:** "Are there any new EQS sedans under $100,000 near me?"
* **Capabilities:** Supports strict enum-based filtering by model, class, body style, brand, interior/exterior colors, fuel type, passenger capacity, highway fuel economy, price range, year (2024-2026), and search radius.
* **Data Returned:** VIN, Stock ID, year, model name, MSRP, engine type, colors, holding dealership's name, distance, and direct URLs for images, dealer websites, and Google Maps.

### 3. `get_mbusa_used_inventory`
Allows the agent to search for **CERTIFIED PRE-OWNED** and **USED** vehicle inventory.
* **Primary Use Case:** "Show me CPO C-Class sedans near 30097 with under 50,000 miles."
* **Capabilities:** Inherits all filters from the New search, but adds a required `invType` parameter (`cpo` or `pre`), expands the `year` search back to 2020, and supports strict enum filtering by `mileage`.

## Configuration & Output
Ensure the `schema.json` file is loaded into your agent's context window. The agent has been explicitly instructed to format the actionable URLs (Image, Dealer Website, Service Scheduling, Google Maps) as clickable Markdown links.
