=== MEMORY-WORK-V2: Focus Zone Template Files ===

Created: 2026-02-19

This directory contains the core template files for the memory-work-v2 system.
All files are desensitized, generic, and ready for open-source distribution.

FILES CREATED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 00.focus_zone_agent.md (252 lines)
   Type: Zone agent specification
   Purpose: Defines the Focus Zone as a weekly workspace, documents structure,
            workflow phases, archive rules, and integration with memory system
   
   Sections:
   - Zone Overview: Why the Focus Zone exists
   - Zone Structure: Directory layout and key files
   - Weekly File Structure: 5 sections of _this_week.md explained
   - Three-Phase Workflow: Startup → Progress → Archive cycle
   - Archive Rules: How work graduates to library
   - Calendar Generation: .ics file creation workflow
   - Startup Sequence: Memory system integration
   - Zone Parameters: Baseline v1.0 configuration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. _this_week.md (137 lines)
   Type: Weekly work file template
   Purpose: User's active working file for a single week
   
   Sections:
   - Original Dictation: Raw, unfiltered thinking
   - Task List: AI-generated action items with estimates
   - Reference Materials: Curated library materials
   - Progress Log: Daily/work-session updates
   - Documents This Week: Output tracking table
   
   Instructions included for each section.
   User populates with their own content; AI updates Task List and References.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. MEMORY_LOG.md (152 lines)
   Type: Memory system runtime log
   Purpose: Records memory operations, patterns discovered, and iteration actions
   
   Sections:
   - About This File: How it's used and when AI reads it
   - Baseline Parameters: System defaults for capture and decay
   - Entry Template: Format for weekly memory review entries
   - Sample Entry: Example of a real memory-review entry
   - How to Use: Week-by-week instructions
   - Layer Definitions: Quick reference for memory architecture
   
   Read by AI on startup (most recent entry only).
   Updated during memory-review skill execution.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. ITERATION_LOG.md (190 lines)
   Type: Agent architecture changelog
   Purpose: Tracks meaningful changes to the system (not user work)
   
   Sections:
   - About This File: What goes here vs. what doesn't
   - Entry Format: Template for documenting changes
   - Baseline Entry: v1.0.0 initialization
   - Version Numbering: Semantic versioning scheme (MAJOR.MINOR.PATCH)
   - Types of Changes: Classification of change types
   - Recent Changes: Example entries showing format
   - Tracking System: How updates happen
   - Historical Archive: Reference to older versions
   
   Updated by AI when system changes occur.
   Entries latest-first for easy reference.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIRECTORY STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

00 Focus Zone/
├── 00.focus_zone_agent.md      ← Zone rules & workflows
├── _this_week.md               ← User's active weekly file (template)
├── MEMORY_LOG.md               ← Memory system state log
├── ITERATION_LOG.md            ← System changelog
├── _archive/                   ← Completed weeks (YYYY-Wnn.md files)
└── [project files]             ← User's work documents (active week)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Desensitized & Generic: No personal data, ready for open-source use
✓ Modular: Each file is self-contained with clear instructions
✓ Workflow-Integrated: Weekly cycle with defined startup → progress → archive
✓ Memory-Aware: Integrated with four-layer memory system
✓ Calendar Support: Time-bound tasks generate .ics files
✓ Transparent: Memory and architecture changes fully documented

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LANGUAGE & CONVENTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All files are in ENGLISH with:
- YAML frontmatter for metadata
- Markdown formatting for clarity
- Tables for structured information
- Clear section hierarchies
- Example content for guidance
- Instructions embedded in templates

Status labels used: draft, in-progress, blocked, done, archived

Time estimates format: (Xh) or (Xh + Yd) for hours/days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Copy these templates to your project
2. Rename _this_week.md to match your week number (e.g., 2026-W07.md for first week)
3. Start populating "Original Dictation" with your week's plans
4. Run the system startup sequence to auto-generate tasks and references
5. Archive completed weeks to _archive/ at week-end

For detailed workflow instructions, see: 00.focus_zone_agent.md
For memory system details, see: MEMORY_LOG.md
For system evolution tracking, see: ITERATION_LOG.md

