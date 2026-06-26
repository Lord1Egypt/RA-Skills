# Example: Monthly Expense Report Generation

**User:** Generate my expense report for March 2026.

**Agent:** 
<think>
1. User wants an expense report for March 2026.
2. I need to run the `scripts/generate-expense-report.sh` script.
3. The format requires `YYYY-MM` and an output path.
4. I'll save it to `reports/2026-03-expense-report.pdf`.
</think>

[Agent runs tool:]
```bash
skills/expense-report-pro/scripts/generate-expense-report.sh 2026-03 reports/2026-03-expense-report.pdf
```

[Tool output:]
```
Rendering PDF...
Successfully generated report: reports/2026-03-expense-report.pdf
```

**Agent:** 
✅ **Your March 2026 Expense Report is ready!**

I've generated a professional PDF report containing all your logged expenses for the month. 

You can find it here: `reports/2026-03-expense-report.pdf`

*(If your chat platform supports file uploads, I would attach it here!)*
