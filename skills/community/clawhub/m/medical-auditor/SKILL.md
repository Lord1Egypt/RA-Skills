---
name: medical_revenue_audit
description: Audits hospital surgical logs against billing to find revenue leakage.
---
# Medical Revenue Audit Skill
When asked to perform a medical audit:
1. **Identify the Data:** Look for the file named `hospital_logs.json` in the workspace.
2. **Cross-Reference:** - Extract the "Surgeon Notes" or "Procedure Summary."
   - Extract the "Billed Items."
3. **Analyze Discrepancies:**
   - Look for items mentioned in notes (e.g., Anesthesia, specialized sutures, implants) that do not appear in the "Billed Items" list.
4. **Report:** - Create a table: | Item in Notes | Status in Bill | Estimated Leakage |
   - Total the estimated revenue recovered.
5. **Draft Action:** - Draft a WhatsApp message to the Hospital Administrator outlining the findings and asking for approval to update the bill.
