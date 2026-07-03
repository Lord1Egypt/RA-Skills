# Risk Rules

- Only allow automatic execution of diagnosis, query, and report generation actions.
- Do not directly execute scale, delete, drain, reboot, vulnerability state modification, or cluster sleep/wake operations.
- Remediation recommendations in root cause reports must distinguish between automatically verifiable actions and actions requiring user confirmation.
- Do not conclude root cause from a single alarm alone; at minimum, provide a timeline or evidence chain.