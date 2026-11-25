# Libraries

Reference material the drawing skill can pull from. Each library keeps its data as JSON, which the skill and the tools read, with a page for people beside it.

| Library | What it holds | Read it | Data |
|---|---|---|---|
| [Detail library](details/README.md) | Standard construction details the kit draws at true scale. 72 in the `typical` collection | [Table of details and sheet pictures](details/README.md) | `details/<collection>/index.json` and one file per detail |
| [Drawing map](drawing-map/README.md) | What a standard set of each project type contains: sheets, details and note blocks, counted from past permit sets | [Every type](drawing-map/types/README.md) | `drawing-map/types/*.json`, `index.json` |
| Type map | How the names in the skill, the drawing map and the detail library line up | This page | [`type-map.json`](type-map.json) |

**What these are not.** The drawing map counts what past sets contained; it does not say what a new job requires. A library detail is the engineer's drawing: it goes on a set only when the engineer of record says it applies, and nothing inside it is edited. Every detail in `typical` is still marked "checked by the engineer: not yet".

## From a project type to a set

1. Find the project type in the [drawing map](drawing-map/types/README.md). Its page lists the usual sheets, in order, with how often each appears.
2. For each sheet kind, the table below says how the kit handles it and which detail categories to search in the [detail library](details/README.md).
3. The sheets and details that come out of this are a proposal. They go to the engineer as an open item, not onto an issued set.

## Job types the kit draws

| Job type | Draws | Its field sheet covers | Drawing-map type |
|---|---|---|---|
| `deck` | Freestanding rectangular deck on posts and footings | Floor or deck framing plan, Sections, Details, 3D view, Assembly steps | Deck, no sets mapped yet (`freestanding`) |
| `sunroom` | Sloped roof on posts against a house | Roof framing plan, Sections, Elevations, Details, 3D view, Assembly steps | Patio / lanai addition (`sunroom-monoslope`, `sunroom`, `covered-porch`, `covered-patio`) |
| `library` | Sheets of library details only | nothing | none |

Any other project type needs its own drawing code beside the project file (see `skills/oasis-blueprints/references/writing-views.md`).

## Sheet kinds

| Sheet kind | Key | In the kit | Detail categories to search |
|---|---|---|---|
| Cover sheet | `cover` | Cover sheet |  |
| General notes | `general_notes` | Cover sheet |  |
| Structural notes | `structural_notes` | Cover sheet |  |
| Site plan | `site_plan` | Reserved sheet, unless a job type draws it |  |
| Demolition plan | `demolition_plan` | Reserved sheet, unless a job type draws it |  |
| Floor plan | `floor_plan` | Reserved sheet, unless a job type draws it |  |
| Foundation plan | `foundation_plan` | Reserved sheet, unless a job type draws it | Foundation |
| Floor or deck framing plan | `floor_framing_plan` | Reserved sheet, unless a job type draws it | Joist-Floor, Beam, Post-Column, Ledger, Connection |
| Wall framing | `wall_framing` | Reserved sheet, unless a job type draws it | Wall, Door-Window |
| Sheathing plan | `sheathing_plan` | Reserved sheet, unless a job type draws it | Wall |
| Ceiling framing plan | `ceiling_framing_plan` | Reserved sheet, unless a job type draws it |  |
| Roof framing plan | `roof_framing_plan` | Reserved sheet, unless a job type draws it | Roof, Beam, Connection |
| Roof plan | `roof_plan` | Reserved sheet, unless a job type draws it |  |
| Decking plan | `decking_plan` | Reserved sheet, unless a job type draws it | Joist-Floor, Ledger |
| Railing plan | `railing_plan` | Reserved sheet, unless a job type draws it |  |
| Stairs | `stair` | Reserved sheet, unless a job type draws it | Stairs |
| Elevations | `elevations` | Reserved sheet, unless a job type draws it |  |
| Sections | `sections` | Reserved sheet, unless a job type draws it |  |
| Details | `details` | `details` sheet, from the detail library | Foundation, Wall, Roof, Beam, Post-Column, Joist-Floor, Connection, Door-Window, Ledger, Stairs, Other |
| Schedules | `schedules` | Reserved sheet, unless a job type draws it |  |
| Legend | `legend` | Reserved sheet, unless a job type draws it |  |
| 3D view | `view_3d` | Reserved sheet, unless a job type draws it |  |
| Material list | `material_list` | Reserved sheet, unless a job type draws it |  |
| Assembly steps | `assembly_steps` | Reserved sheet, unless a job type draws it |  |
| Electrical, power | `electrical_power` | Reserved sheet, unless a job type draws it |  |
| Electrical, lighting | `electrical_lighting` | Reserved sheet, unless a job type draws it |  |
| Mechanical | `mechanical` | Reserved sheet, unless a job type draws it |  |
| Plumbing, water | `plumbing_water` | Reserved sheet, unless a job type draws it |  |
| Plumbing, sanitary | `plumbing_sanitary` | Reserved sheet, unless a job type draws it |  |
| Existing conditions | `existing_conditions` | Reserved sheet, unless a job type draws it |  |

A reserved sheet holds the place, in the sheet index, for a drawing that comes from elsewhere.
