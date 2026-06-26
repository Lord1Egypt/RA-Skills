# Nexus2 Pipeline Fix — Sports Prediction Engine

## What This Fixes
Two critical bugs in the Nexus2 sports prediction pipeline that caused phantom predictions and JSON serialization crashes.

### Bug 1: Timestamp Serialization Crash
**File:** `publishing/publisher.py`  
**Problem:** `json.dumps()` failed with `TypeError: Object of type Timestamp is not JSON serializable` when prediction data contained pandas Timestamp objects.  
**Fix:** Added custom `NexusEncoder` class that converts pandas Timestamp and datetime objects to ISO format strings before serialization.

### Bug 2: Stale Fixture Ingestion
**File:** `nexus.py`  
**Problem:** Scraped fixtures were ingested into an isolated local `NexusDataLoader()` instance instead of `self.data_loader`. Predictions ran against stale database data, producing phantom matches that didn't exist on bookmaker sites.  
**Fix:** Changed ingestion to use `self.data_loader.ingest(matches)` directly, ensuring fresh scraped fixtures flow into the prediction pipeline.

## How to Apply
1. Copy the patched files into your Nexus2 installation:
   - `publishing/publisher.py` — adds `NexusEncoder` class
   - `nexus.py` — fixes fixture ingestion in `predict()` method
2. Restart the prediction pipeline: `python nexus.py --predict`
3. Verify output matches live bookmaker fixtures

## Result
- Predictions now match real SportyBet/SofaScore fixtures
- No more JSON serialization crashes
- Fresh fixtures ingested before each prediction run

## Author
TKDigital ( Imperial Court / OpenClaw )
