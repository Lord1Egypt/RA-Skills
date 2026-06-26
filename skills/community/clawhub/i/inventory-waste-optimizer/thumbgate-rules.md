# ThumbGate Prevention Rules – Inventory & Waste

1. **Volume Sanity Check** — Block any restock recommendation that is >50% higher than the 4-week moving average unless manually overridden.
2. **Variance Flag** — Block finalizing inventory reports if (Prep + Beginning Inventory - End Inventory) vs Sales has a variance > 5%.
3. **Price Jump Guard** — Block the creation of POs where a vendor's unit price has increased >20% since the last cycle.
4. **Expiration Warning** — Block standard restocking of items that currently have >30% stock nearing expiration.