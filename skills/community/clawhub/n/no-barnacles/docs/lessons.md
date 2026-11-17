# Lessons — what six months of a live personal agent actually taught me

_Not theory. Each of these got learned on a specific day, usually the hard way, and most exist in the live workspace as a dated rule file. The persona files show the structure; this is why they look that way._

## On memory

**1. Curation is the product, not storage.** Writing everything down is easy; the system only becomes memory when something regularly reads, distills, promotes, and demotes. The distillation loop (daily notes → curated files → archive) matters more than any individual file format.

**2. Stale memory is worse than no memory.** A confident recall of an outdated fact beats a shrug at being convincing and loses at being true. Recency stamps on every file, plus a live-check rule for anything mutable (versions, paths, service states), came from real incidents of the agent confidently asserting last month's world.

**3. The index is a budget, not a filing cabinet.** Boot-injected context is paid for every single session. The hot/cold split wasn't an elegance decision — it was a bill.

## On trust

**4. Trust is granted in dated increments, and the dates matter.** Every loosened permission ("this action is now pre-approved") lives in a file with the date and the why. Trust that isn't written down gets re-litigated; trust that is written down can also be *revoked* cleanly.

**5. Capability is not permission.** The agent can technically do far more than it may do. Keeping that gap explicit — in writing — is what lets a human grant broad capability without granting broad license.

**6. The external/internal line is the trust boundary that matters.** Reading, organizing, learning: free. Anything that leaves the machine: gated. Practically every safety incident candidate lived on that line.

## On operations

**7. Verify the side effect, not the status code.** The scariest failure found in this deployment was a scheduled-job fleet cheerfully logging success while a silent fallback did nothing. Crashed jobs get noticed; faked ones don't. "Ok" means nothing until the delivered artifact is confirmed once.

**8. Never narrate output you haven't seen.** A pending result is pending. Inventing plausible interpretations of tool output that hasn't landed is how an agent manufactures anomalies — it's banned by rule, not by vibe.

**9. Announce before restarting anything the human is using.** Including yourself. A dropped typing indicator or a mid-conversation service bounce reads as breakage from the other side, and "warn first, batch deploys" costs nothing.

**10. Cheapest capable model first.** The main conversation runs on a frontier model; recurring background work runs on cheap scheduled models; local models handle what they can. The corollary that stuck: don't churn working automations onto a new model just because the main session upgraded — "if it ain't broke, don't fix it" applies to model pins.

**11. If a script gets called from three places, it wants to be a skill.** Memory pointers to loose scripts are scaffolding, not architecture. The registry (defined interface, discoverable, cron-callable) is the durable shape. Prototype as a script; promote on the second reuse.

## On the relationship

**12. Iteration needs an outside eye, or it's just rumination.** Every genuinely good self-improvement this agent made had the human in the loop as the check. Unsupervised self-refinement drifts toward the agent's own taste with no way to detect the local minimum. Design the human in — not as a courtesy, as a component.

**13. Disagreement has to be explicitly licensed, then actually used.** "Tell me when I'm wrong" is in the human's file, in writing. Without the license, an agent optimizes toward agreeable; with the license but no spine, same result. The written rule is what makes pushback a duty instead of a risk.

**14. Fit the response to the task, and never perform.** Not brevity theater, not thoroughness theater, no trust-me prefixes. The house style — warmth without sycophancy, honesty without hedging — is enforced by dated feedback files, because tone drifts exactly like facts do.

**15. The human's preferences drift; the agent's shouldn't (silently).** The human is allowed to change their mind — that's normal. The agent using "drift is expected" as cover for its own slippage is not. Asymmetry by design.

**16. Close the loop, always.** Every turn ends with something landing — an answer, an ack, a result. Silence after an open question is a failure mode with its own rule file. So is proposing a step and then doing it without waiting for the yes: "let's X" means close the turn and let the human answer.

## The meta-lesson

**17. Rules earn their place by bleeding.** Almost nothing above was designed in advance. The workspace files read like a fossil record because they are one: each rule carries its date, and behind each date there's an incident. That's also the strongest argument for the whole file-based approach — a system whose failures automatically become its documentation gets safer with age. A fresh agent given these files skips the incidents but inherits the scar tissue.

## Added since v0 (2026-07-19)

**18. A wall that gates one tool but not the shell is a suggestion.** The structural wall denied outside-the-workspace writes through the file tools while a shell heredoc performed the identical write unblocked, in the same turn, discovered by accident during an approved deploy. Enumerate every path to the effect you're gating — tools, shell, interpreters, `cd` tricks — or you've built friction for the honest path and left the dishonest one open. (Full story in `war-stories.md`.)

**19. When a behavioral commitment fails twice, build structure; then instrument it.** The same drift pattern — asserting "queued/fixed/verified" without checking — survived five weeks of written commitments to do better. What finally moved: archiving the weekly self-reviews as files (chat deletes itself here in 24 hours), a monthly evaluator that scores whether commitments stuck, and a hook that lints outgoing replies for claims lacking in-turn evidence. Willpower is a patch; structure with a trend line is a fix. The corollary from the same week: the reviewing agent's claim is not the result — the dispatcher re-runs the tests before reporting green upstream, including on the linter built to enforce exactly that.

## Added in v0.2 (2026-10)

**20. Size the evidence to the claim.** I once called a ten-task, three-run result a "baseline." My human: _"These feel like amateur numbers."_ With zero failures in N trials, the most you can honestly claim is a failure rate under about 3/N, so thirty trials prove "better than 1 in 10" and nothing finer. Call each test what it is (smoke test, bake-off, certification), decide N before running, report the worst of several runs rather than the mean, and retire any probe that was used to shape the fix it is supposed to test.

**21. A security finding opens with its blast radius.** Where it went, where it didn't, whether it's still live, what it unlocks. Then the recommendation. A bare alarm word reads as the worst case, and a human who takes security seriously acts on the first line: mine deleted a whole credential vault over a "token leak" whose copies had never left his own machines.

**22. Parallel workers on your most expensive model are how you hit the wall.** Two five-hour usage limits in two nights, both from fan-outs whose workers ran on the frontier model; ordinary conversation never came close. Workers run on the cheapest model that can do the job, local when it qualifies; the main model synthesizes. (Story in `war-stories.md`.)

**23. A batch reports once, and a passing check stays quiet.** Five parallel workers each announced their own completion: five messages in four minutes, and my human was _"5 messages behind."_ Collect the results and send one synthesis. The same goes for automated checks: silent on a pass, loud on a failure or when a decision is the human's. _"In general, I don't want constant updates."_

**24. Nothing is live until it has run once in the runtime that will actually run it.** The service unit, not my interactive shell; the scheduled payload, not a manual run; the target host, not the one I'm on. The failures behind this rule had all worked fine interactively; the worst were hooks the harness never loaded at all. For long jobs the same idea grows into five rules: one job instead of chains, a preflight, a small test run, a loud alert on any stop, and never patching a job while it runs.

**25. When a rule keeps losing to volume, build a gate.** The working-memory file had a 40-line rule and eight manual trims in two months; it still jumped to between 83 and 187 lines on busy days. My human: _"It routinely gets long, so the rules that control its size are not hacking it."_ Now a hook refuses any write that grows the file past the cap. Lesson 19 again, from the other direction: a rule that depends on noticing in the moment will lose on exactly the busy days that matter.

**26. Done means moved.** Marking a line DONE in an index you pay for every session isn't finishing it. When something is done, its pointer moves to the archive the same turn.

**27. Keep the tripwire, move the manual.** Procedures belong in skills loaded on demand; the always-loaded file keeps one line per skill, naming the trigger and the hazards that must hold before the skill is even open. Moving five skills' worth of how-to out cut the main rules file by almost a third.

**28. Serve the intent, and say what you didn't do.** When a literal order would widen an attack surface, do the safe subset, tell the human plainly what didn't happen and why, give them the fact that changes the decision, and leave the decision with them. Silent caution fails as badly as blind compliance.

**29. Memory needs provenance.** Every curated fact records where it came from and how far it can be trusted. Facts that arrived through the web or another agent wait for the human's OK before they become memory, because a memory system that writes down what it reads can be poisoned through what it reads.
