# Ashby

Ashby MCP Pack — wraps the Ashby ATS API

## ashby_list_candidates

Search candidates in your ATS. Returns names, emails, and application metadata. Use ashby_get_candid

## ashby_get_candidate

Get full candidate profile by ID. Returns contact info, resume, interview history, and current appli

## ashby_list_jobs

Search open positions. Filter by status (open, closed, draft, archived). Returns job title, departme

## ashby_get_job

Get full job posting by ID. Returns description, requirements, hiring stage, and applicant count.

## ashby_list_applications

Search job applications across positions. Returns candidate name, applied job, application stage, an

```json
{
  "mcpServers": {
    "ashby": {
      "url": "https://gateway.pipeworx.io/ashby/mcp"
    }
  }
}
```
