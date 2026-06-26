# Example: Project Breakdown — "Launch Website"

> User says: "I need to launch a website for my hot sauce brand by March 20"

## Agent Response

```
📁 New project: Launch Hot Sauce Website (due Mar 20)

Phase 1: Content & Design (Mar 11-13)
├── 🔲 Write homepage copy — hero, about, product descriptions (Mar 11) · P2 · ~90 min
├── 🔲 Gather product photos — 3 SKUs, lifestyle shots (Mar 11) · P2 · ~60 min
├── 🔲 Design landing page mockup in Figma or similar (Mar 12) · P2 · ~120 min
│   └── ⏳ Depends on: homepage copy, product photos
├── 🔲 Write FAQ and shipping/returns policy (Mar 12) · P3 · ~45 min
└── 🔲 Review and approve design mockup (Mar 13) · P1 · ~30 min
    └── ⏳ Depends on: design mockup

Phase 2: Technical Setup (Mar 13-15)
├── 🔲 Purchase domain if not already owned (Mar 13) · P2 · ~15 min
├── 🔲 Set up hosting — Vercel, Netlify, or Shopify (Mar 13) · P2 · ~30 min
├── 🔲 Configure DNS and SSL certificate (Mar 13) · P2 · ~20 min
│   └── ⏳ Depends on: domain purchase, hosting setup
└── 🔲 Set up email forwarding for contact form (Mar 14) · P3 · ~15 min

Phase 3: Build & Integrate (Mar 14-17)
├── 🔲 Build responsive site from approved mockup (Mar 14-16) · P1 · ~360 min
│   └── ⏳ Depends on: approved mockup, hosting setup
├── 🔲 Integrate payment processing — Stripe or Shopify Payments (Mar 16) · P1 · ~120 min
│   └── ⏳ Depends on: site build
├── 🔲 Add contact form with email notification (Mar 16) · P3 · ~30 min
├── 🔲 Set up Google Analytics and Meta Pixel (Mar 16) · P3 · ~20 min
└── 🔲 Add SEO meta tags, sitemap, robots.txt (Mar 17) · P2 · ~30 min

Phase 4: Test & Launch (Mar 18-20)
├── 🔲 QA test on Chrome, Safari, Firefox + mobile (Mar 18) · P1 · ~90 min
│   └── ⏳ Depends on: site build complete
├── 🔲 Fix any QA issues found (Mar 18-19) · P1 · ~120 min
├── 🔲 Test checkout flow end-to-end with real payment (Mar 19) · P1 · ~30 min
├── 🔲 Submit sitemap to Google Search Console (Mar 19) · P3 · ~10 min
├── 🔲 Go live — point production domain and verify (Mar 20) · P1 · ~20 min
│   └── ⏳ Depends on: QA complete, DNS configured
└── 🔲 Post launch announcement on social media (Mar 20) · P2 · ~30 min

18 tasks created · Estimated: ~20 hours total
Buffer: 2 days built in before deadline
```

## What the Agent Did

1. **Identified the end state:** A live, functional e-commerce website for a hot sauce brand
2. **Worked backwards from March 20** with 2 days of buffer
3. **Grouped into 4 phases:** Content → Technical → Build → Launch
4. **Set dependencies:** Build can't start until mockup is approved; QA can't start until build is done
5. **Estimated time per task** using reasonable baselines for web development work
6. **Assigned priorities:** Launch-critical tasks (build, QA, go-live) are P1; supporting tasks are P2-P3

## User Follow-Up

The user can then:
- "Looks good, but move the social media post to March 21" → agent adjusts due date
- "Add a task to set up Instagram shop integration" → agent adds to Phase 3
- "I already have the domain, mark that as done" → agent marks done, unblocks DNS task
- "Show me just Phase 1" → agent shows filtered view
