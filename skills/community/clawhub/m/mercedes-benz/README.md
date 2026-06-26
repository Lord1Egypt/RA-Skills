# MBUSA Dealer & Inventory API / OpenClaw Skill

A multi-purpose Node.js application that serves as an LLM tool (OpenClaw Skill) and a standalone REST API for querying official Mercedes-Benz USA dealership locations and live vehicle inventory (New & Used).

## Project Structure
* `src/tool.js`: Core logic fetching data from MBUSA APIs. Handles strict MBUSA enum mapping, price formatting, and Google Maps URL generation.
* `schema.json`: Function definitions for OpenClaw LLM agent integration.
* `server.js`: Express wrapper exposing the tools as HTTP REST endpoints.

## Installation

1. Ensure you have Node.js (v18+ recommended) installed.
2. Clone this repository and install the Express dependency:

\`\`\`bash
npm install
\`\`\`

## Running the API Server

To start the standalone web server:

\`\`\`bash
npm start
\`\`\`
The server will listen on `http://localhost:3000`.

## API Documentation

### 1. Dealer Locator
Fetches a list of dealerships near a given zip code. Returns contact information and Google Maps links.

**Endpoint:** `GET /api/dealers`

**Parameters:**
* `zip` (string, **required**): 5-digit US zip code.
* `start` / `count` (integer, optional): Pagination settings.

---

### 2. NEW Vehicle Inventory Search
Fetches live new-vehicle inventory from dealerships near a given zip code.

**Endpoint:** `GET /api/inventory`

**Parameters:**
* `zip` (string, **required**): 5-digit US zip code.
* `distance` (integer, optional): Search radius (10, 25, 50, 100, 200, 500, 1000).
* `minPrice` / `maxPrice` (integer, optional): Filter by MSRP.
* `model` / `classId` / `bodyStyle` / `brand` (string, optional): Specific vehicle filters based on MBUSA enums.
* `exteriorColor` / `interiorColor` (string, optional): Filter by color enum (e.g., BLK, BLU).
* `year` (integer, optional): 2024, 2025, or 2026.
* `start` / `count` (integer, optional): Pagination settings.

---

### 3. USED & CPO Vehicle Inventory Search
Fetches live pre-owned and certified pre-owned inventory.

**Endpoint:** `GET /api/used-inventory`

**Parameters:**
* `zip` (string, **required**): 5-digit US zip code.
* `invType` (string, **required**): Must be `cpo` (Certified Pre-Owned) or `pre` (Standard Pre-Owned).
* `mileage` (string, optional): Filter by mileage band (e.g., `0_5000`, `10000_50000`).
* `year` (integer, optional): Extends range from 2020 to 2026.
* *(Inherits all other filtering parameters from the New Inventory API above)*.

**Example Request:**
\`\`\`text
GET http://localhost:3000/api/used-inventory?zip=10019&invType=cpo&classId=E&distance=50&mileage=0_5000
\`\`\`