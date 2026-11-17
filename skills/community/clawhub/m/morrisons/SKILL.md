---
name: morrisons
description: Automated search and insertion of grocery items to your active Morrisons supermarket trolley, viewing basket contents, listing delivery slots, reserving slots, managing shopping lists, and viewing previous orders.
---

# Morrisons Shop Skill

> [!NOTE]
> **Disclaimer**: This skill is an unofficial open-source automation tool for personal productivity. It is not affiliated with, endorsed by, or sponsored by Wm Morrison Supermarkets Limited. All product names, trademarks, and registered trademarks are property of their respective owners. Use responsibly and in accordance with website terms.

Automated search and insertion of grocery items to your active Morrisons supermarket trolley, viewing basket contents, listing delivery slots, reserving slots, managing shopping lists, and viewing previous order history and itemized receipts via Morrisons' GraphQL backend.

## Requirements & Setup

* **Runtime**: [Bun](https://bun.sh) and [Playwright](https://playwright.dev) (`bun install playwright`).
* **Authentication**: Save your session storage state to `~/.openclaw/workspace/morrisons-auth-state.json` (via `morrisons-action.ts auth` or `morrisons-action.ts import-cookies <cookies.json>`).
* **Optional Credentials**: Store `MORRISONS_EMAIL` and `MORRISONS_PASSWORD` in `~/.config/morrisons.env`.

## Arguments

* `$ARGUMENTS[0]` — Command to execute:
  * Orders & History: `orders`, `order`
  * Shopping Lists: `lists`, `list`, `create-list`, `rename-list`, `list-add`, `list-remove`, `delete-list`, `list-to-cart`
  * Trolley & Slots: `search`, `add-exact`, `add`, `cart`, `slots`, `book-slot`, `check-checkout`, `auth`, `import-cookies`
* `$ARGUMENTS[1]` — Primary argument:
  * For `orders`: Number of orders to fetch (e.g. `5` or `10`, default `10`).
  * For `order` / `view-order`: Order reference ID (e.g. `1126176030930`) or `latest`.
  * For `search`: Product search term (e.g. `milk`).
  * For `add-exact`: Exact product title returned by search (e.g. `Morrisons British Semi Skimmed Milk 4 Pint`).
  * For `add`: Comma-separated list of items (e.g. `milk,bananas`).
  * For `book-slot`: Date/Day target (e.g. `Monday`).
  * For `import-cookies`: Path to exported cookies JSON file.
  * For `list` / `view-list`: List name or ID (e.g. `Weekly` or `ee2e3713-0018-4a60-a28e-862d2bb78e0b`).
  * For `create-list`: Name for new list (e.g. `Weekend Brunch`).
  * For `rename-list` / `edit-list`: Existing list name or ID.
  * For `list-add` / `add-to-list`: Target list name or ID.
  * For `list-remove` / `remove-from-list`: Target list name or ID.
  * For `delete-list`: Target list name or ID to delete.
  * For `list-to-cart` / `add-list-to-cart`: Target list name or ID.
* `$ARGUMENTS[2]` — Secondary argument:
  * For `book-slot`: Time window (e.g. `08:00 - 09:00`).
  * For `rename-list`: New name for the list.
  * For `list-add`: Product title, keyword, or product UUID to add.
  * For `list-remove`: Product title or product UUID to remove.

## Execution

### 1. View Previous Orders & Order Details

#### List Previous Orders
View list of past orders with order numbers, delivery dates/time slots, status, and total cost:
```bash
bun morrisons-action.ts orders 5
```

#### View Itemized Order Details
View complete itemized breakdown of a specific order (delivered items, unavailable items, substituted items, unit prices, promotions, savings, and total cost):
```bash
bun morrisons-action.ts order "$ARGUMENTS[1]"
```

### 2. Search Products (Microdecision flow)
Search for items and return a clean serialized JSON array of matching product titles, prices, stock statuses, and cart states.
```bash
bun morrisons-action.ts search "$ARGUMENTS[1]"
```

### 3. Add Exact Product (Microdecision flow)
Add a product by its exact title.
```bash
bun morrisons-action.ts add-exact "$ARGUMENTS[1]"
```

### 4. Add Groceries (Fuzzy batch flow)
Run a batch add using fuzzy terms (falls back to search matching):
```bash
bun morrisons-action.ts add "$ARGUMENTS[1]"
```

### 5. View Cart / Trolley
Lists items currently in your basket and total cost:
```bash
bun morrisons-action.ts cart
```

### 6. Shopping Lists Management

#### List All Shopping Lists
View summary of all shopping lists, item counts, prices, and sample items:
```bash
bun morrisons-action.ts lists
```

#### View Specific Shopping List
View full details and all products in a list by name or UUID:
```bash
bun morrisons-action.ts list "$ARGUMENTS[1]"
```

#### Create New Shopping List
Create a new list with optional initial items:
```bash
bun morrisons-action.ts create-list "$ARGUMENTS[1]"
```

#### Rename / Edit Shopping List Name
Rename an existing list by name or UUID:
```bash
bun morrisons-action.ts rename-list "$ARGUMENTS[1]" "$ARGUMENTS[2]"
```

#### Add Item to List
Search for a product by name or pass a product UUID to add it to a list:
```bash
bun morrisons-action.ts list-add "$ARGUMENTS[1]" "$ARGUMENTS[2]"
```

#### Remove Item from List
Remove an item by name or UUID from a list:
```bash
bun morrisons-action.ts list-remove "$ARGUMENTS[1]" "$ARGUMENTS[2]"
```

#### Delete Shopping List
Delete an entire list by name or UUID:
```bash
bun morrisons-action.ts delete-list "$ARGUMENTS[1]"
```

#### Add Shopping List to Trolley / Cart
Transfer all items from a list directly into your active basket:
```bash
bun morrisons-action.ts list-to-cart "$ARGUMENTS[1]"
```

### 7. List Available Delivery Slots
Lists available time windows and prices:
```bash
bun morrisons-action.ts slots
```

### 8. Book / Reserve a Slot
Reserves a specific delivery slot. On success, it sends a checkout alert and schedules a follow-up check in 45 minutes to warn the user if they haven't completed checkout.
```bash
bun morrisons-action.ts book-slot "$ARGUMENTS[1]" "$ARGUMENTS[2]"
```

### 9. Check Checkout Status
Manually check if the reserved slot is still pending checkout:
```bash
bun morrisons-action.ts check-checkout
```

### 10. Setup / Session authentication
Import cookies:
```bash
bun morrisons-action.ts import-cookies "$ARGUMENTS[1]"
```
Direct Login:
```bash
bun morrisons-action.ts auth $ARGUMENTS[1]
```
