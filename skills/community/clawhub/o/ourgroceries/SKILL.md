---
name: ourgroceries
description: Skill for interacting with OurGroceries.com to manage shopping lists. Use when you need to add items to grocery lists, check existing lists, or synchronize with OurGroceries.com account. Enables programmatic grocery list management through voice or text commands using the unofficial Python wrapper.
---

# OurGroceries Integration

## Overview

This skill provides integration with OurGroceries.com using an unofficial Python wrapper, allowing you to manage your grocery lists through natural language commands. You can add items to lists, check what's on your lists, and synchronize with your OurGroceries.com account.

## Setup Required

To use this skill, you need to:
1. Have an OurGroceries.com account (email and password)
2. Install **`aiohttp`** (see `requirements.txt`). Scripts load a **vendored client** from `lib/ourgroceries/` (patched for current OurGroceries APIs, including `getItemCategory` + `getLists` / auto-categorize parity with the web app).
3. Configure your credentials securely

## Quick Start

### Adding Items
To add an item to your grocery list, simply say or type:
- "Add milk to my grocery list"
- "I need eggs and bread for shopping"
- "Put apples on OurGroceries"

### Checking Lists
To see what's on your list:
- "What's on my grocery list?"
- "Show me OurGroceries"
- "List items for shopping"

## Available Operations

Once configured with your OurGroceries.com credentials, this skill supports:
- Adding items to specific lists or default list
- Retrieving items from lists
- Removing items from lists
- Marking items as purchased
- Creating new lists
- Deleting lists
- Synchronizing with OurGroceries.com

## Resources

### scripts/
Contains executable scripts for interacting with OurGroceries.com via the unofficial Python wrapper:
- `add_item.py` - Add items to grocery lists
- `get_list.py` - Retrieve current list items
- `remove_item.py` - Remove items from lists
- `devtools_network_monitor.js` - Paste in browser DevTools to log POST JSON (see file header)

### references/
Documentation and usage guides:
- `api_reference.md` - OurGroceries.com API endpoints and authentication (based on unofficial wrapper)
- `authentication.md` - How to obtain and use API credentials (email/password)
- `examples.md` - Common usage patterns and examples

## Configuration

Before using this skill, you'll need to:
1. Visit https://www.ourgroceries.com and note your login email and password
2. Store these credentials securely (we recommend using environment variables or a secure vault)
3. The scripts will look for credentials in environment variables:
   - `OURGROCERIES_EMAIL`: Your OurGroceries.com login email
   - `OURGROCERIES_PASSWORD`: Your OurGroceries.com login password

## Credits
- Based on [py-our-groceries](https://github.com/ljmerza/py-our-groceries) by ljmerza.

If you encounter issues, check the references/ directory for troubleshooting tips and current status.

## Example Usage

After setting environment variables:
```bash
OURGROCERIES_EMAIL="your@email.com" OURGROCERIES_PASSWORD="yourpassword" \
  python3 /path/to/skill/scripts/add_item.py "milk" -l "My Grocery List"
```
(`add_item.py` uses **auto-categorize** via `getItemCategory` + `insertItem`; see `AGENTS.md` in this skill folder.)