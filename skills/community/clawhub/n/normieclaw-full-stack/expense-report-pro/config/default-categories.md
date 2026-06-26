# Default Categories & Rules

These are the default categories for Expense Report Pro. You can modify this file (`expenses/categories.md`) to add custom categories or routing rules.

## Standard Categories (IRS/Corporate Friendly)
- Meals & Entertainment
- Travel & Transit
- Lodging
- Office Supplies
- Software & Subscriptions
- Hardware & Equipment
- Professional Services
- Marketing & Advertising
- Utilities
- Miscellaneous

## Auto-Routing Rules
The AI will automatically categorize expenses based on the vendor. Here are some examples of rules it follows:

* If Vendor contains "Uber", "Lyft", "Delta", "United", "Amtrak" -> Travel & Transit
* If Vendor contains "Hilton", "Marriott", "Hyatt", "Airbnb" -> Lodging
* If Vendor contains "Starbucks", "Diner", "Restaurant", "Cafe" -> Meals & Entertainment
* If Vendor contains "AWS", "Google Workspace", "Adobe", "GitHub" -> Software & Subscriptions
* If Vendor contains "Staples", "Office Depot", "Amazon" -> Office Supplies
* If Vendor contains "Apple", "Best Buy" -> Hardware & Equipment

## Tax-Relevant Flags
* If the expense is marked as a business expense, it is considered tax-deductible.
* If the expense is marked as personal, it is not tax-deductible.
* The AI will attempt to determine this based on the context (e.g. "I spent $50 on a team dinner" -> Business; "I bought groceries" -> Personal).
