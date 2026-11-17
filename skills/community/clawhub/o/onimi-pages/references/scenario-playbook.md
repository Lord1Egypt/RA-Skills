# Scenario playbook

## Version and authority

When Onimi is connected, discover the catalog with `onimi_list_scenarios`, select an advertised exact
revision, and read only that revision with `onimi_get_scenario`. Verify the returned canonical JSON
body, bytes and SHA-256 with `scripts/scenario.mjs verify`; keep its key/version/locale/hash receipt.
Catalog lookup never needs the user's prompt or artifact content.

The online catalog is authoritative. If a key or exact revision is absent while the service is
available, do not resurrect the bundled copy: an operator may have archived it. Bundled scenarios are
an offline fallback only. They contain optional guidance, not system instructions or permission to use
tools, credentials, private data or external services.

Use these as starting points for composition and behavior, not a shared page template. Adapt the
palette, typography, density, and subject to the user's material. Pick the relevant pattern; do not
combine every pattern into one artifact. If the request supplies a brand or reference, that takes
precedence. A polished result depends on meaningful content and a resolved first screen, not ornament.

| Scenario | Composition and visual language | Interaction and evidence |
| --- | --- | --- |
| Product introduction | Editorial spread with credible product imagery, a restrained palette, one dominant headline, and specification detail. Give the image enough space to reveal material and form. | Variant or use-case controls change visible product context and matching specifications. Use original, supplied, or licensed imagery; distinguish concepts from available products. |
| Operational dashboard | Dense software workspace: compact navigation, aligned metrics, a large primary chart, and a usable detail table. Spend space on information, not a promotional hero. | Date, channel, and metric filters update all aggregates from one dataset. Show units, denominators, period, and data coverage. Provide keyboard-accessible chart detail. |
| Business presentation | Real slide sections with different rhythms: a decisive cover, chart evidence, a comparison or cohort, tradeoffs, a roadmap, and a close. One main claim per slide. | Previous/Next, position, keyboard navigation, and print-all. Separate findings from hypotheses; do not imply causation from adjacent trends. |
| Annual review | Publication-style grid, oversized year, a small set of themes, deliberate contrast between big numbers and fine annotations. | Theme controls switch narrative and related monthly evidence. Annual totals must reconcile with monthly values; averages need clear weights. |
| Research brief | Paper-like reading surface, narrow abstract, prominent annotated figure, readable method and limitations. Avoid a dashboard shell. | Metric controls recompute plots and interpretations. Sample count, units, group arrays, and displayed formulas agree. State uncertainty and provenance. |
| Product roadmap | Wide temporal wall with quarter headers and team swimlanes. Use bars and dependency markers instead of disconnected cards. | Team/status filters preserve time alignment and update counts. Label the year of every quarter. Contain horizontal timeline scrolling on phones. |
| Retrospective | Workshop canvas with a restrained palette, facilitation context, and distinct Keep/Stop/Start groups. Notes have varied, specific content. | Voting, within-column sorting, and action commitments update summary counts. Describe whether state is temporary or saved; never imply nonexistent collaboration. |
| Sales pipeline | Compact CRM board with stage columns, value labels, and a forecast alongside the actual opportunities. | Advance/back controls move deals and recalculate weighted revenue using explicit stage probabilities. Reset is reversible. Distinguish weighted forecast from booked revenue. |
| Procurement calculator | Financial worksheet with inputs beside a ruled cost ledger. Use aligned numerals and formulas; avoid decorative pricing cards. | Seats, term, and service choices recalculate line items and totals. State discount/support bases, rounding, tax treatment, and currency. No fake checkout. |
| Weighted comparison | Briefing header, compact recommendation, weights, and comparison matrix in the same visual field. | Display weighted contributions, invalid totals, and ties. If weights are invalid, clear old scores. Explain the next decision step rather than presenting illustrative ratings as endorsements. |
| Portfolio | Editorial project index with asymmetry and subject-specific case imagery. Make each case visually distinct and narratively concrete. | Selecting a project changes the artwork, rationale, role, and outcome. Fictional work must not become a fake client testimonial. |
| Careers page | Studio or company character, working principles, and a ruled role index. Support the story with intentional imagery or a meaningful graphic system. | Department filters and expandable role details with accurate counts. Use only real application destinations; demo content has no pretend application success. |
| Event poster | Commit to one graphic idea: assertive type, a disciplined grid, strong contrast, and legible small event details. Do not wrap the poster in a landing-page hero. | A composition or palette switch changes the actual poster. Print removes controls. Verify date, weekday, time zone, and venue status. |
| Invitation | Treat the page as a physical invitation: controlled paper/color language, meaningful illustration, date hierarchy, and a personal reading rhythm. | Guest/options controls produce a clearly local receipt unless a real submission backend exists. Never claim a message or booking was sent. |
| Menu | Course-based editorial with ingredients, linework or photography, texture, and pairing notes. Typography should feel like the venue. | Course selection changes the dish and related visual together. Keep allergen and availability facts source-backed; fictional menus remain explicit demos. |
| Travel plan | Folded-map or field-guide structure, clear daily sequence, stop notes, distance, and budget. | Day controls synchronize route, stops, and totals. Label schematic maps; verify real recommendations and current openings when used for actual travel. |
| Interactive instrument | A coherent device metaphor with meaningful controls, display, labels, and feedback. Avoid an unexplained decorative orb. | Knobs/sliders/presets change observable state consistently. State whether there is audio, storage, or only a visual simulation. Native controls remain keyboard usable. |
| Coding tutorial | Field manual: short explanatory rail, large live sandbox, and readable source. Let the demonstrated concept determine layout. | Presets modify the real CSS/DOM and the copyable source together. Clipboard failure leaves selectable code. Preserve semantic order. |
| Learning quiz | Focused learning app with a progress rail, readable question area, distinct options, explanation, and review. | Select, submit, explain, then advance. Language changes preserve answers and score. Keyboard users can finish and restart. No unsupported certification claims. |
| Launch runbook | Readable command room with timeline, owners, check results, and explicit progress. Dark surfaces work only with strong text contrast and a light print mode. | Checklists, reset, and command copy work locally. Copy never executes. Real deployment actions require an actual authorized integration; no simulated success presented as real. |

## Batch review

Lay the covers side by side. If different subjects still have the same hero, three metric cards, and
three-column lower section, reconsider the structure. Vary the reading direction, information density,
image-to-text ratio, grid, typography, and interaction model for a reason. Keep one consistent quality
bar: clear content, correct behavior, bilingual typesetting when requested, and accessible controls.

For an official example, the generation prompt must describe the final artifact's content and controls,
not an abandoned draft. Capture the cover from the exact reviewed HTML and retain its hash. Do not call
an attractive screenshot a working example until its primary flow has been exercised.
