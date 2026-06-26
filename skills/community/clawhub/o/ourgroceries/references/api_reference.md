# OurGroceries.com API Reference (via unofficial Python wrapper)

## Current Status
This skill uses the unofficial Python wrapper for OurGroceries.com (`ourgroceries` package from PyPI), which works by simulating login to the website and interacting with the backend APIs used by the official apps.

## Available Actions (from the wrapper)
The unofficial wrapper provides access to these core actions:

### List Management
- `getLists` - Get all lists (current web client; legacy wrapper used `getOverview`)
- `ACTION_GET_LIST` - Get a specific list
- `ACTION_LIST_CREATE` - Create a new list
- `ACTION_LIST_DELETE_ALL_CROSSED_OFF` - Delete all checked-off items
- `ACTION_LIST_REMOVE` - Delete a list
- `ACTION_LIST_RENAME` - Rename a list

### Item Management
- `getItemCategory` - Guess category for an item name (`itemName`, `note`, `guess: true`); response includes `categoryId` when resolved. The web UI calls this before `insertItem` when auto-categorize is enabled.
- `ACTION_ITEM_ADD` - Add an item
- `ACTION_ITEM_ADD_ITEMS` - Add multiple items
- `ACTION_ITEM_REMOVE` - Remove an item
- `ACTION_ITEM_RENAME` - Rename an item
- `ACTION_ITEM_CHANGE_VALUE` - Change item quantity/value
- `ACTION_ITEM_CROSSED_OFF` - Check/uncheck an item

### Utilities
- `ACTION_GET_CATEGORY_LIST` - Get category list
- `ACTION_GET_MASTER_LIST` - Get master list
- `ACTION_ITEM_RENAME` - Rename item

## Authentication Method
The wrapper uses email/password authentication:
- `SIGN_IN` endpoint for login
- Session cookies maintained automatically
- No API keys or tokens required

## Installation
The package is already installed:
```bash
pip install ourgroceries
```

## Usage Example
```python
from ourgroceries import OurGroceries

# Initialize with credentials
og = OurGroceries(email, password)

# Get lists
lists = og.get_lists()

# Add item to first list
if lists:
    og.add_item(lists[0].id, "milk")

# Get items from a list
items = og.get_list(list_id)
```

## Limitations
- Relies on website scraping/simulation rather than official API
- May break if OurGroceries.com changes their website structure
- Requires storing email/password credentials
- No official rate limits or guarantees

For official API access, you would need to contact OurGroceries.com directly.