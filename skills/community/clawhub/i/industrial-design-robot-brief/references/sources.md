# Sources

Use this reference when collecting candidate papers for `industrial-design-robot-brief`.

## Goal

Find recent humanoid-robot papers that are strong candidates for industrial-design, UX, and product-definition translation.

The goal is not to maximize academic completeness.
The goal is to maximize useful product insight for industrial designers working on humanoid robot programs.

## Source Priority And Search Strategy

Source ranking:
1. arXiv
2. Hugging Face Papers or daily paper feeds
3. Organization or lab release pages when directly linked from the paper
4. Public demo videos or project pages
5. Industry reporting or trusted summaries, only as supporting context

Prefer original paper pages over news summaries.

If using API access:
- arXiv API query: `cat:cs.RO AND (humanoid OR bipedal OR whole-body OR dexterous manipulation OR embodied OR legged locomotion OR teleoperation)`
- Semantic Scholar API: filter by `Computer Science`, keyword match, and citation velocity
- Hugging Face daily papers: scan the full daily list and filter by humanoid relevance
- Papers With Code: check robotics trending pages

If using conversational AI without API:
- use user-provided links, lists, screenshots, or browsing results
- verify each paper before ranking it
- do not fabricate candidate papers

In all cases:
- every paper must have a verifiable arXiv ID or DOI
- if a paper cannot be verified, mark it as `⚠️ 待核实` and do not rank it in the top `5`

## Candidate Scope

Collect papers directly related to:
- humanoid robots
- whole-body control and coordination
- locomotion with product or form implications
- manipulation with embodiment or packaging implications
- egocentric or onboard perception systems
- hand, wrist, arm, foot, torso, and head mechanical integration
- social interaction, safety, motion readability, or human trust
- deployable robot hardware with strong design consequences
- sim-to-real transfer with hardware validation
- teleoperation systems that define operator-robot interaction

## Tech-To-Design Mapping

Use this mapping to judge design relevance:

| Paper Topic | Design Relevance Area |
|---|---|
| Egocentric or onboard vision | Head form, sensor window geometry, face or eye design |
| Whole-body locomotion | Standing posture, center of gravity, foot or ankle proportion, stance width |
| Dexterous manipulation | Hand size, finger proportion, wrist diameter, forearm volume |
| Tactile or force sensing | Skin material, surface texture, visible sensor integration areas |
| Human-robot interaction | Approachability, motion legibility, personal space, face expression |
| Safety or compliance | Soft covers, speed limitations, warning signals |
| Battery or thermal management | Back and torso volume, vent placement, weight distribution |
| Modularity or field repair | Panel line placement, access points, swap interface |
| Teleoperation | Operator interface design, wearable form, latency-related UX |
| Audio or speech | Speaker and microphone placement, mouth or jaw area design |

A paper that activates `3+` rows is usually a strong candidate.

## Low-Priority Topics

Down-rank papers mainly about:
- benchmarks or leaderboard comparisons without hardware
- synthetic datasets without embodiment application
- pure simulation without stated real-robot implications
- generic model training without direct humanoid use case
- strong technical novelty but no identifiable product or design impact
- drones, quadrupeds, or non-humanoid platforms unless explicitly transferred to humanoids

## Time Window

Default: `yesterday` in the user's local timezone.

If yesterday has fewer than `5` viable candidates:
- extend to `48 hours`
- then extend to `72 hours` if still needed

Special handling:
- on Monday, include Friday, Saturday, and Sunday preprints if needed
- on low-volume days, note: `今日候选论文较少，已扩展至 72 小时窗口`

Mixing recency with discussion heat:
- a paper from `3-5` days ago is acceptable if it became notably important yesterday
- a paper older than `7` days should only appear with explicit justification
- always note the actual posting date

## Selection Size

- target scanning about `20+` candidate papers when possible
- short-list `8-10` strong candidates
- final output: exactly `5`, ranked by design impact score
- if fewer than `5` strong candidates exist, output all qualified ones and note the shortfall

## Selection Heuristics

Prioritize papers with one or more of these signals:
- real robot hardware validation
- clear body-part design implication
- visible hardware integration constraint or packaging challenge
- human-facing interaction consequence
- published video, figure sequence, or demo
- strong scenario relevance
- practical deployment implication such as cost, weight, power, or maintenance

## Diversity Rule

The final `5` papers should cover at least `3` different design-relevant topic areas from the mapping table.

If one topic dominates the candidate pool:
- select the `1-2` strongest papers from that topic
- use remaining slots to cover other meaningful topic areas
- note this in the daily summary

## Verification Rules

Mandatory verification from the paper text or official source:
- exact English title
- arXiv ID or DOI
- first author name and primary affiliation
- robot platform name if applicable
- key performance numbers only when clearly stated
- publication or posting date

Allowed to summarize or interpret:
- design implications
- scenario relevance
- product positioning
- maturity assessment
- cross-paper trend observations

Handling uncertainty:
- if a metric is vague, quote the original wording instead of inventing a number
- if an institution is ambiguous, use `可能为`
- if the paper is a preprint, note `预印本，未经同行评审`
- if a demo video is reported but not found in the paper, note that explicitly

Hard rules:
- never generate a fake arXiv ID
- never fabricate author names
- never invent performance numbers

## Design Impact Scoring

Rate each paper on four dimensions, each scored `1-5`:

| Dimension | 1 (Low) | 3 (Medium) | 5 (High) |
|---|---|---|---|
| Form Impact | No visible shape consequence | Suggests minor proportion or surface change | Directly changes external geometry or silhouette |
| Layout Impact | No hardware packaging change | Affects one internal zone | Forces rethink of major internal arrangement |
| UX or Trust Impact | No human-facing consequence | Affects interaction at close range | Changes how people perceive or coexist with the robot |
| Product Definition Impact | Incremental improvement | Expands capability within a known category | Suggests a new product role or use case |

Total design impact score = sum of four dimensions, max `20`.

Use total score to rank the final `5`, highest first.

## Output Reminder

The candidate list is only an intermediate step.

Each final paper must help answer:
1. Why does this matter for form?
2. Why does this matter for layout?
3. Why does this matter for UX or trust?
4. What kind of product or scenario does this suggest?

If a paper only connects weakly to these questions, reconsider whether it belongs in the top `5`.
