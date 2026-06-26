Description

A powerful local AI accounting assistant that helps you record daily income and expenses through natural language, query transactions, and generate statistical reports. All data is securely stored locally — no internet connection required.

Capabilities

1. Natural Language Accounting
- Record income and expenses through conversation
- Automatically detect amount, category, and date
- Smart category suggestions

2. Transaction Queries
- Query by time range (today, this week, this month, this year, etc.)
- Filter by category
- Keyword search
- Support for multi-condition combined filtering

3. Statistical Analysis
- Total income and expense summary
- Category breakdown analysis
- Daily average spending calculation
- Balance auto-calculation

4. Report Generation
- Generate detailed income/expense reports
- Category statistics TOP ranking
- Export support

Usage Examples

Recording Transactions
- "Record expense: lunch 35 yuan"
- "Income: salary received 15000 yuan"
- "Spent 120 on movie tickets, category entertainment"
- "Transport today 20 yuan"

Querying Transactions
- "Show this month's transactions"
- "How much did I spend this week"
- "Query food and dining expenses"
- "Show last month's income"

Statistics
- "Summarize this month's income and expenses"
- "Spending overview for this year"
- "Show my expense categories"

Available Tools

add_transaction
Add a transaction record
- type: expense or income
- amount: amount
- description: description
- category: category (optional)
- tags: tags (optional)

query_transactions
Query transaction records
- period: time range
- type: transaction type filter
- category: category filter
- keyword: keyword search
- limit: result count limit

get_statistics
Get income/expense statistics
- period: statistics time period

generate_report
Generate detailed report
- period: report time period

get_categories
Get all available categories

update_transaction
Update a transaction record
- id: record ID
- other fields to update

delete_transaction
Delete a transaction record
- id: record ID

Category System

Expense Categories
- Food & Dining: meals, takeout, beverages, etc.
- Transport: bus, subway, taxi, fuel, etc.
- Shopping: supermarket, online shopping, daily necessities, etc.
- Entertainment: movies, games, travel, etc.
- Healthcare: doctor visits, medicine, checkups, etc.
- Education: tuition, training, books, etc.
- Housing: rent, mortgage, utilities, etc.
- Utilities: phone bill, internet, etc.
- Other

Income Categories
- Salary: monthly salary, annual salary, etc.
- Bonus: year-end bonus, performance bonus, etc.
- Investment: stocks, funds, wealth management, etc.
- Freelance: side jobs, self-employment, etc.
- Gift: monetary gifts, red envelopes, etc.
- Reimbursement: expense reimbursement, refunds, etc.
- Other

Data Storage

- All data saved in local JSON files
- Path: configured data directory / accounting.json
- Auto backup: retains the last 30 backups
- Open data format, exportable at any time

Quick Commands

- /accounting.help - Show help
- /accounting.stats - Quick view of this month's statistics

Notes

1. The data file is created automatically on first use
2. Use positive numbers for amounts
3. Edit/delete operations require the record ID (obtainable via query)
4. Back up your data file regularly to prevent accidental loss
