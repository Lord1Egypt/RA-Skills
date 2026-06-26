# Expense Tracker

Log daily expenses to Notion via natural language chat. Type something like "chicken rice 5" and it auto-parses the item, amount, category, and payment method — then writes it to your Notion database.

Supports bilingual input (English + Chinese), 10 spending categories, and multiple payment platforms.

## Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Share your expense database with the integration
3. Set environment variables:
   ```
   export NOTION_API_KEY="your_token_here"
   export EXPENSE_DATABASE_ID="your_database_id_here"
   ```

### Required Notion Database Schema

| Property         | Type   | Notes                                                                                         |
|------------------|--------|-----------------------------------------------------------------------------------------------|
| Name             | title  | Expense description                                                                           |
| Amount           | number | Numeric value in SGD, no currency prefix                                                      |
| Bank Name        | select | OCBC, TRUST, DBS, Revolut, 支付宝, 微信, OCBC BUSINESS                                       |
| Category         | select | Food, Transport, shopping, business, Groceries, Leisure, Bills, medical, investment, Education |
| Transaction Date | date   | ISO 8601 (YYYY-MM-DD)                                                                        |

## Usage Examples

| Input                        | Item           | Amount | Category  | Bank   |
|------------------------------|----------------|--------|-----------|--------|
| chicken rice 5               | chicken rice   | 5.00   | Food      | OCBC   |
| grab to school 12.50         | grab to school | 12.50  | Transport | OCBC   |
| 咖啡 3.50 支付宝             | 咖啡           | 3.50   | Food      | 支付宝 |
| notion labs 33 revolut       | notion labs    | 33.00  | business  | Revolut|
| dinner with jy 57 trust      | dinner with jy | 57.00  | Food      | TRUST  |
| driving class 90             | driving class  | 90.00  | Education | OCBC   |

## Commands

- `/today` — List today's expenses with running total
- `/summary` — Current month breakdown by category
- `/month [month]` — View a specific month (e.g., `/month march`)
- `/budget [amount]` — Set monthly budget; shows remaining on each log
- `/bank [name]` — Filter expenses by payment method

## Parsing Rules

- Amount is usually the last number: "2 coffee 9" → item="2 coffee", amount=9
- Strips "$" or "SGD" prefixes
- Supports decimals: "3.50", "12.5"
- Bank detection is case-insensitive: "ocbc" = "OCBC"
- Chinese platforms: "支付宝" / "alipay" → 支付宝, "微信" / "wechat" → 微信
- Default bank: OCBC (when none specified)
- If user specifies category explicitly (e.g., "chicken rice 5 business"), uses that override
- All amounts in SGD, rounded to 2 decimal places

## Troubleshooting

If logging to Notion fails:
1. Verify your `NOTION_API_KEY` environment variable is set and valid
2. Confirm your `EXPENSE_DATABASE_ID` is correct and the database is shared with your integration
3. Ensure database properties match the schema above (exact names, case-sensitive)
4. Check that the integration has write permissions
