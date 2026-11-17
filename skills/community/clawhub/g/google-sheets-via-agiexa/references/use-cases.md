# Google Sheets use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/google-sheets

## Build a Shopify Sales Dashboard

Combine store sales and order information into a spreadsheet dashboard with revenue metrics, trends, and business summaries.

- Apps: Google Sheets, Shopify
- Tools: `GOOGLESHEETS_CREATE_GOOGLE_SHEET1`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_CREATE_CHART`

> Create or update a Google Sheets dashboard for my Shopify store. Organize the available order data by date, order status, product, and sales channel where those fields exist. Calculate revenue totals, order counts, average order value, and daily or monthly trends using clearly defined formulas or summarized data. Create a dedicated dashboard sheet with metric cards represented by formatted cells, summary tables, and appropriate charts. Preserve the source data and existing formulas. Before creating a new spreadsheet or changing an existing one, identify the intended file and review its current structure. Clearly distinguish actual source values from calculated metrics.

## Track Inventory and Low-Stock Products

Maintain an inventory sheet that highlights products below their configured stock thresholds and helps prioritize replenishment.

- Apps: Google Sheets, Shopify
- Tools: `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_MUTATE_CONDITIONAL_FORMAT_RULES`, `GOOGLESHEETS_FORMAT_CELL`

> Review my Shopify product and inventory data and organize it in Google Sheets with product name, SKU, inventory location, available quantity, and reorder threshold where those fields are available. Add a stock status column with values such as Low Stock, Healthy, and Out of Stock based on the configured threshold. Highlight critical stock levels using conditional formatting and create a separate inventory alert summary. Flag missing SKUs, duplicate product identifiers, and incomplete inventory records. Do not invent stock quantities or reorder thresholds. Preserve existing data and ask before overwriting manually maintained values.

## Compare Google Ads Campaign Results

Organize advertising metrics in Google Sheets to compare campaign spend, clicks, conversions, and cost efficiency.

- Apps: Google Sheets, Google Ads, Shopify
- Tools: `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_CREATE_CHART`

> Prepare a Google Sheets report for my Google Ads campaign performance. Organize the available data by date and campaign, including spend, impressions, clicks, conversions, and cost per conversion. Calculate derived metrics only when the required source values are available. Add summary tables that compare campaigns and highlight those needing further investigation. Where Shopify order and revenue data can be reliably matched, include additional sales and revenue comparisons. Do not treat reported advertising conversions as identical to Shopify orders. Add a chart comparing campaign performance, preserve source data, and do not change live advertising campaigns.

## Reconcile Orders and Business Records

Compare Shopify orders with spreadsheet records to identify missing rows, duplicate entries, and inconsistent order information.

- Apps: Google Sheets, Shopify
- Tools: `GOOGLESHEETS_BATCH_GET`, `GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`

> Compare my Shopify order data with the relevant Google Sheets records. Match records using reliable identifiers such as order IDs, and identify missing orders, duplicate rows, and discrepancies in dates, totals, status, or other available fields. Create a reconciliation summary showing the source values, spreadsheet values, and differences. Avoid matching records solely on customer names or similar amounts when a stronger identifier is available. Preserve the original records and write proposed corrections to a separate review section. Do not delete rows or overwrite existing records until I approve the reconciliation results.

## Automate New Row Processing

Detect new spreadsheet rows and prepare them for validation, classification, calculations, or downstream business workflows.

- Apps: Google Sheets, Shopify
- Tools: `GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW`, `GOOGLESHEETS_UPSERT_ROWS`, `GOOGLESHEETS_VALUES_UPDATE`

> Help me create a workflow for processing new rows added to my Google Sheets product or order tracker. When a new row is detected, validate required fields, check for duplicate identifiers, and calculate relevant derived values where possible. For product rows, validate SKU, price, and inventory fields; for order rows, validate order ID, date, amount, and status. Flag incomplete or invalid records instead of silently correcting them. Preserve manually entered values and avoid processing the same row repeatedly. Explain which changes can be triggered by spreadsheet events and which require a separate workflow. Do not delete or overwrite source data automatically.

## Generate Supplier Reorder Reports

Use inventory and sales records to prepare a prioritized list of products that may require replenishment.

- Apps: Google Sheets, Shopify
- Tools: `GOOGLESHEETS_AGGREGATE_COLUMN_DATA`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`

> Analyze my Shopify inventory and sales data stored in Google Sheets. Identify products below their configured reorder thresholds and estimate replenishment needs using available stock, recent sales, and supplier lead times where known. Create a reorder report with product name, SKU, current stock, recent units sold, reorder threshold, supplier, and proposed reorder quantity where the required data exists. Flag missing lead times and uncertain demand rather than inventing values. Sort the report by stock urgency and sales importance. Do not place supplier orders or change inventory levels; prepare the report for review.

## Combine Analytics, Ads, and Sales Data

Consolidate marketing performance and ecommerce results into one spreadsheet to help evaluate traffic, advertising, and sales trends.

- Apps: Google Sheets, Google Analytics, Google Ads, Shopify
- Tools: `GOOGLESHEETS_UPDATE_VALUES_BATCH`, `GOOGLESHEETS_CREATE_CHART`

> Create a consolidated Google Sheets report combining available Google Analytics, Google Ads, and Shopify data. Organize records by date, campaign, traffic source, landing page, and product where reliable identifiers permit matching. Include advertising spend, clicks, sessions, purchases, Shopify orders, and revenue where available. Calculate derived metrics only when their definitions and required inputs are clear. Highlight data gaps, inconsistent reporting windows, and attribution differences. Create comparison tables and charts showing marketing performance alongside store results. Preserve raw source data in separate sheets and do not imply that correlations prove causation.

## Clean and Standardize Spreadsheet Data

Find duplicate rows, inconsistent formatting, missing values, and invalid records while preserving the original data for review.

- Apps: Google Sheets
- Tools: `GOOGLESHEETS_FIND_REPLACE`, `GOOGLESHEETS_GET_DATA_VALIDATION_RULES`, `GOOGLESHEETS_UPDATE_VALUES_BATCH`

> Audit the specified Google Sheets workbook for duplicate records, inconsistent date formats, inconsistent text values, missing required fields, and suspicious numeric entries. Identify the relevant sheet and cell ranges for each issue. Recommend a standardized format for dates, currency, SKUs, product statuses, and other fields that are present. Use a separate review sheet to list proposed corrections and explain the reason for each. Do not remove duplicates, replace values, clear ranges, or alter existing formulas until I approve the changes. After approval, apply only the agreed changes and verify the affected ranges.

## Create Automated Business Charts

Turn spreadsheet data into clear charts for revenue, product performance, inventory, and advertising comparisons.

- Apps: Google Sheets, Google Ads
- Tools: `GOOGLESHEETS_LIST_CHARTS`, `GOOGLESHEETS_CREATE_CHART`, `GOOGLESHEETS_UPDATE_CHART`

> Review my existing Google Sheets workbook and identify useful charts based on its actual data. Recommend charts for sales trends, top-selling products, inventory status, and Google Ads campaign performance where the relevant data exists. Select chart types that suit each comparison and avoid mixing incompatible units on an unclear axis. Create charts with descriptive titles, readable labels, and appropriate date ranges. Place each chart on the most relevant sheet or dashboard, and preserve the underlying data and formulas. If a chart already exists, review it before creating a duplicate. Summarize the charts created and the source ranges used.

## Monitor Important Spreadsheet Changes

Use spreadsheet change events to initiate validation, refresh summaries, and flag business data that needs attention.

- Apps: Google Sheets, Shopify
- Tools: `GOOGLESHEETS_LIST_DRIVE_CHANGES`, `GOOGLESHEETS_VALUES_GET`

> Help me configure a Google Sheets monitoring workflow for my Shopify business workbook. Monitor the specified sheet or cell range for relevant changes, such as new product rows, modified inventory quantities, updated campaign metrics, or changes to important summary values. When a change occurs, validate the affected data, recalculate dependent summaries where appropriate, and flag issues such as low stock, duplicate SKUs, missing fields, or unusually high advertising costs. Avoid repeated processing and preserve manually maintained fields. Explain which trigger best matches the requested change and which downstream actions require a separate workflow. Do not send external messages or modify unrelated records without approval.
