---
        name: promo-calendar-optimizer
        description: Optimize weekly promotion calendar across content, live sessions, and paid pushes under inventory and capacity constraints. Use when the user asks how to schedule promo actions, avoid campaign collisions, or improve consistency of ecommerce momentum.
        ---

        # Promo Calendar Optimizer

        ## Skill Card

        - **Category:** Operations
        - **Core problem:** How should we schedule promos to maximize conversion without operational overload?
        - **Best for:** Cross-channel promo planning
        - **Expected input:** Campaign goals, inventory limits, creator slots, paid budget windows
        - **Expected output:** Weekly promo calendar with channel mix, owner tasks, and risk notes
        - **Creatop handoff:** Use outputs in batch-content-sprint-os and deal ops execution

        ## Workflow

        1. Collect promo constraints (inventory, budget, creator availability, events).
2. Map campaign intents to best-fit channel/time windows.
3. Detect conflicts and overload risk in execution plan.
4. Output balanced promo calendar + fallback options.

        ## Output format

        Return in this order:
        1. Executive summary (max 5 lines)
        2. Priority actions (P0/P1/P2)
        3. Evidence table (signal, confidence, risk)
        4. 7-day execution plan

        ## Quality and safety rules

        - Do not schedule promo intensity beyond team capacity limits.
- Protect inventory-critical SKUs from overexposure.
- Include contingency options for creator/content delays.

        ## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
