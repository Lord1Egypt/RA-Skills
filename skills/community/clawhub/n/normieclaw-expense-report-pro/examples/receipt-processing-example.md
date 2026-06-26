# Example: Receipt Photo Processing

**User:** [Sends a photo of a receipt from Joe's Diner for $24.50]

**Agent:** 
<think>
1. User uploaded an image.
2. I need to run vision extraction to pull: Vendor, Date, Subtotal, Tax, Tip, Total.
3. I'll use the `image` tool to read the receipt.
4. I'll determine the category based on `expenses/categories.md` (Joe's Diner -> Meals & Entertainment).
5. I'll append a JSON object to `expenses/expense-log.json`.
6. I'll save the image to `expenses/receipts/2026-03-07-joes-diner.jpg`.
</think>

[Agent runs tools:]
```json
// expense-log.json update
[
  {
    "date": "2026-03-07",
    "vendor": "Joe's Diner",
    "category": "Meals & Entertainment",
    "subtotal": 20.00,
    "tax": 1.50,
    "tip": 3.00,
    "total": 24.50,
    "currency": "USD",
    "line_items": [
      {"description": "Burger", "amount": 15.00},
      {"description": "Fries", "amount": 5.00}
    ],
    "receipt_file": "2026-03-07-joes-diner.jpg"
  }
]
```

**Agent:** 
✅ **Logged $24.50 at Joe's Diner (Meals & Entertainment)**

I've saved the receipt and added the expense to your log. The breakdown is:
* Subtotal: $20.00
* Tax: $1.50
* Tip: $3.00
* Total: $24.50

This brings your total Meals & Entertainment spending for the month to $145.50.
