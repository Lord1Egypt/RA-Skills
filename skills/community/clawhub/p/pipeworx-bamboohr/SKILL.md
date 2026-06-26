# Bamboohr

BambooHR MCP Pack — wraps the BambooHR API v1

## bamboohr_list_employees

List all employees with directory info. Returns IDs, names, departments, job titles, and contact det

## bamboohr_get_employee

Get detailed employee info by ID (e.g., "12345"). Specify fields like firstName, lastName, email, de

## bamboohr_get_directory

Get complete employee directory with names, titles, departments, contact info, and manager assignmen

## bamboohr_list_timeoff

Search time-off requests by date range (e.g., "2024-01-01" to "2024-12-31"). Returns approved/pendin

## bamboohr_get_employee_files

Get files in an employee's profile by ID. Returns file names, upload dates, and file types.

```json
{
  "mcpServers": {
    "bamboohr": {
      "url": "https://gateway.pipeworx.io/bamboohr/mcp"
    }
  }
}
```
