# URL Extraction Guide for Job Watch Skill

## Problem
When extracting job URLs from websites, constructed URLs based on job titles often result in 404 errors. The correct URLs contain numeric IDs.

### General Best Practices:
1. **Always verify URLs**: Test a sample of extracted URLs to ensure they work.
2. **Use direct extraction**: Prefer extracting URLs from HTML over constructing them.
3. **Handle special characters**: URLs are often slugified (lowercase, hyphens, no special chars).
4. **Include numeric IDs**: When present, numeric IDs are crucial for URL validity.


### Implementation Notes:
When implementing the job watch skill:
1. Use `web_fetch` to get HTML content
2. Parse HTML to extract actual URLs using regex or HTML parsing
3. Never construct URLs based on job titles alone
4. Always include the report with verified, working URLs