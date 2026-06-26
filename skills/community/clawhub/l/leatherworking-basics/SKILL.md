---
name: leatherworking-basics
description: >-
  Use when you need to repair worn leather goods (boots, belts, bags, tool sheaths) or create new durable items from scratch for everyday self-reliance, gig work, or off-grid living where commercial replacements are costly or unavailable. Agent handles material and tool sourcing research, custom pattern generation from user measurements, project planning with timelines, material quantity calculations, maintenance logs, and decision-tree troubleshooting. Human performs all hands-on physical work: cutting, skiving, stitching, riveting, dyeing, and finishing.
metadata:
  category: skills
  tagline: >-
    Build and repair tough leather gear that outlasts supply-chain breakdowns — agent plans every cut and stitch, you shape the hide with your hands.
  display_name: "Leatherworking Basics: Craft & Repair Durable Goods"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install leatherworking-basics"
---
# Leatherworking Basics: Craft & Repair Durable Goods

Turn raw or scrap leather into reliable, long-lasting tools, clothing, and gear that survive unstable times. This skill equips you with professional-grade protocols for repair and creation while the agent manages every logistical and planning detail.

`npx clawhub install leatherworking-basics`

## When to Use This Skill

Use this skill any time commercial leather goods fail, prices spike, or you want custom items built exactly to your needs (knife sheaths to pair with chainsaw-tree-work, reinforced belts for physical labor, repairable boots for outdoor-recreation-skills, or saddlebags for bicycle use). Agent first collects your specific project (repair vs new build), available leather type/quantity, measurements, and tools on hand, then generates a customized project plan with shopping list, timeline, and step-by-step instructions. Ideal for post-AI self-reliance where you keep your own gear running indefinitely.

## Agent vs Human Roles

**Agent Role (all planning, tracking, and bureaucracy):**  
- Researches current suppliers, prices, and alternatives for leather, thread, rivets, and dyes (including local scrap sources).  
- Generates scalable patterns from user measurements or photos.  
- Builds and maintains a project log with photos descriptions, material usage, and lessons learned.  
- Runs decision trees for “repair vs replace vs redesign.”  
- Sets calendar reminders for oiling/conditioning intervals and tool sharpening.  
- Drafts emails or marketplace messages for sourcing bulk scrap leather.  
- Calculates exact material needs and waste minimization.  
- Escalates to advanced techniques or professional tanneries only if safety-critical.  

**Human Role (all physical, embodied work):**  
- Performs every cut, skive, stitch, punch, and finish.  
- Provides real-time tactile feedback on leather stiffness or tool performance.  
- Executes safety checks and test-fits.  
- Decides final aesthetic or functional tweaks during assembly.  

This division keeps the agent in its lane (logic and memory) while the human stays in the irreplaceable zone of hand-eye coordination and craft intuition.

## Tools and Workspace Setup

**Minimum starter kit (agent generates exact shopping list based on your first project):**  
- Cutting mat, sharp utility knife or leather shears  
- Skiving knife or edge beveler  
- Stitching chisels/punches (4-6 prong), awl, needles (glovers and harness)  
- Mallet, rivet setter, hole punch set  
- Edge slicker, burnisher, and sandpaper  
- Leather conditioner (neatsfoot oil or beeswax blend)  
- Thread (waxed polyester or linen), beeswax, contact cement  
- Optional but recommended: rotary punch, strap cutter, dye applicator  

Workspace: clean, flat table with good lighting and ventilation. Secure leather with weights or clamps. Agent reminds you to wear cut-resistant gloves during initial cutting and to work in a well-ventilated area when using dyes or solvents.

## Step-by-Step Protocol

### Phase 0: Project Intake & Planning (Agent-only, 10–20 minutes)
1. Agent asks: project type (repair/new), dimensions/photos, leather type/thickness (2–8 oz), color/finish preference, deadline.  
2. Agent outputs: exact materials list with quantities and links, tool checklist, timeline (e.g., “4 hours total active work over 2 days”), and pattern files (SVG or printable PDF).  
3. Human confirms or adjusts; agent iterates.

### Phase 1: Material Preparation (1–2 hours)
1. Agent directs inspection: check for defects, measure usable area.  
2. Human cuts rough shapes using the agent-generated pattern.  
3. Skive edges to desired thinness (agent provides thickness targets per project type).  
4. Bevel and burnish edges for professional finish.

### Phase 2: Assembly & Stitching (2–6 hours depending on project)
Agent provides real-time coaching via numbered steps tailored to your exact item.

**Example Project 1: Simple Belt Repair/Rebuild (entry-level, 3 hours)**  
- Decision tree: If buckle intact and leather only cracked at holes → patch and reinforce. If entire strap worn → cut new from stock.  
- Human: punch new holes at precise spacing (agent calculates from waist measurement), rivet buckle, add keeper loop.  
- Finish with oil and edge finish.

**Example Project 2: Custom Knife Sheath (pairs with existing tool skills, 4 hours)**  
- Agent generates pattern from knife dimensions and photos.  
- Human: wet-form leather over knife (safety: blade covered), stitch with saddle stitch (8–10 SPI), add belt loop and retention strap.  
- Dye and finish to match your other gear.

**Example Project 3: Boot or Glove Repair (maintenance mode, 2–4 hours)**  
- Agent decision tree: sole separation vs upper tear vs lining failure.  
- Human: re-stitch seams, patch holes with matching scrap, replace eyelets/rivets, re-oil for waterproofing.

**Example Project 4: Wallet or Small Pouch (gift or daily carry, 5 hours)**  
- Full build from 4–5 oz vegetable-tanned leather.  
- Human: card slots, bill compartment, snap closure — agent supplies exact slot dimensions and folding sequence.

For every project agent maintains a live checklist and pauses for human confirmation before irreversible steps (cutting, dyeing).

### Phase 3: Finishing & Conditioning (30–60 minutes)
- Dye if desired (agent provides color-mixing ratios).  
- Apply conditioner and buff.  
- Human test-fits and reports any binding; agent logs adjustments for next iteration.

## Ready-to-Use Templates & Scripts

**Project Log Template (Agent maintains as markdown file):**
```
Project: [Name] | Date: [YYYY-MM-DD] | Leather used: [qty/thickness] | Hours: [X] | Lessons: [notes] | Next conditioning due: [date]
```

**Sourcing Message Template (Agent customizes and you copy-paste):**
"Looking for scrap vegetable-tanned leather (4–6 oz, 10+ sq ft) or sides from [specific animal]. Prefer natural finish. Will pay fair market or trade [your skill/service]. Located in [your area]."

**Pattern Request to Agent:**
"Generate a pattern for a [item] that fits these measurements: [list]. Include seam allowance and assembly order."

**Maintenance Reminder Script (Agent sends via your preferred channel):**
"Your [item] was last conditioned on [date]. Time to apply neatsfoot oil. Estimated 15 minutes. Reply 'ready' when you start."

## Decision Trees (Agent Runs These Live)

**Repair vs Replace:**  
- If damage <30% surface and structural integrity intact → repair.  
- If stitching failed but leather sound → re-stitch only.  
- If leather dry-rotted or moldy → replace with new.  
Agent outputs recommendation with exact reasoning based on your photos/descriptions.

**Leather Type Selection:**  
- Vegetable-tanned: for tooling, stamping, molding (sheaths, belts).  
- Chrome-tanned: for soft goods, gloves, linings (more flexible).  
- Scrap vs side: agent calculates cost/benefit for your project size.

## Success Metrics

- 100% of repaired items remain functional for minimum 12 months post-repair (agent tracks).  
- At least one new custom item built per quarter.  
- Total leather goods maintenance cost drops >50% vs buying new (agent calculates from your log).  
- Human self-reported confidence in leather projects rises from beginner to intermediate within 3 projects.  
- Zero preventable failures during field use (e.g., sheath holds tool securely, belt does not snap).

## Maintenance & Iteration

Agent reviews your leatherworking log every 90 days and proposes next project based on your gear inventory and usage patterns. Update patterns when your measurements change or new tools arrive. Re-oil all vegetable-tanned items every 6–12 months or after heavy use/wet exposure — agent sets recurring reminders.

## Rules & Safety Notes

- Always cut away from your body; use cutting mat.  
- Test dye on scrap first — agent reminds this step.  
- Keep sharp tools stored safely when not in use.  
- Work in ventilated area when using solvent-based finishes.  
- For items carrying sharp tools (sheaths), ensure retention prevents accidental draw.  
- Never use on critical life-safety gear (e.g., climbing harnesses) without professional certification.  
- Dispose of leather scraps responsibly or repurpose via composting (if vegetable-tanned).

This protocol draws from established leatherworking standards: Al Stohlman’s classic saddle-stitch and edge-finishing techniques, modern Tandy Leather training sequences, and traditional guild methods refined for minimal-tool home use. All measurements and tolerances are industry-standard unless you specify otherwise.

## Disclaimer

Leatherworking involves sharp tools and potential for cuts or eye injury. Follow all safety instructions and stop immediately if you feel uncertain. This skill is for educational and self-reliance purposes only and is not a substitute for professional leather goods manufacturing or repair when structural integrity is critical (e.g., horse tack used daily). Results depend on your leather quality, tool sharpness, and execution. Perform at your own risk and consult local regulations for any commercial use of crafted items.