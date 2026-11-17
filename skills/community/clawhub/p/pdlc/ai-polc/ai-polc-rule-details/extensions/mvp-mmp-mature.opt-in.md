<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: MVP/MMP for Mature Products (Opt-In Prompt)

**Trigger:** User mentions "define next version scope", "next major release", "v2 scope"
**Stage:** 7 (Release & Increment Slicing)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly asks to define next version/major release scope
- Product Maturity = Mature and user requests "what's in the next version"
- User mentions "MMP" (Minimum Marketable Product)

## Activation Prompt

```
I detect you'd benefit from the MVP/MMP Mature extension.

For mature products defining their next major version, this adds:
• MMP scoping framework (what's the minimum for the next version to be marketable?)
• Version increment decision (major vs. minor vs. patch)
• Migration/compatibility epic identification
• Sunset/deprecation planning for replaced features

Core Stage 7 already handles MVP for new products (0→1).
This extension re-activates the same discipline for "1→2" transitions.

Activate MVP/MMP for Mature Products? (yes/no)
```

If yes → load `mvp-mmp-mature.md`
