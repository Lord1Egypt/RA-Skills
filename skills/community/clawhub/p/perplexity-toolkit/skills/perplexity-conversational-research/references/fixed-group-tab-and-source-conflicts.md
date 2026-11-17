# Fixed Group/Tab Research and Source-Conflict Notes

## Reusable fixed-tab recipe

Use this when the user wants Perplexity research to remain visually contained in one group and one tab.

1. Pick one task-named WebBridge session. Call `list_tabs` first.
2. If the session has no task tab, call `navigate` once with `newTab:true` and a task-language `group_title`.
3. Save the original Perplexity conversation URL before any model-mode detour.
4. For toolkit calls, inject a `WebBridgeDriver` using the same session and pass `new_tab=False`:

```python
from perplexity_toolkit.config import get_config
from perplexity_toolkit.search import search, model_council
from perplexity_toolkit.drivers.webbridge import WebBridgeDriver

cfg = get_config()
driver = WebBridgeDriver(cfg.webbridge_url, session="<fixed-session>")
answer = search(query, config=cfg, driver=driver, new_tab=False)
# Model variety, same physical tab:
council = model_council(query, config=cfg, driver=driver, new_tab=False)
```

5. Use WebBridge fill + the three-event Enter sequence for a same-thread follow-up. Take a fresh snapshot after navigation or generation; page refs are not durable.
6. After a model-mode detour, navigate back to the saved original URL with `newTab:false`. Verify `list_tabs`: one task tab, expected group title, intended final URL.

## Same tab is not always the same chat

A follow-up submitted in the result page remains in the same Perplexity conversation. Toolkit mode functions navigate to the home page before submitting and may create a new conversation even with `new_tab=False`. If “one exact chat” is a hard requirement, use follow-ups only and do not claim the model changed. If model diversity is required, use a mode as a temporary second conversation in the same physical tab, then restore the original URL and disclose the distinction.

The Perplexity model dropdown is not a reliable automation surface. Supported mode-based diversity (`model_council`, `step_by_step`, and `deep_research`) is preferable to fighting the UI selector.

## Evidence handling for source checks

The HEAD-vs-readback rule and the `toolkit-head` / `page-content` two-state recording are defined once in Step 3 (Verification) of the `perplexity-search` skill. Apply that definition; this file only covers what is specific to multi-turn conflicts below.

When a Perplexity answer contradicts itself or changes across turns, re-read the canonical URL directly through an approved extraction/browser path. Preserve the conflict until resolved, prefer explicit current-page text over answer summaries, and record access date/version requirements. Answer scores, source counts, and model-council agreement are discovery/review signals, not factual verification.

## 2026-09-02 worked evidence pattern

In one run, Perplexity first reported that Claude Code's current Output Styles page did not list `Concise`, then later corrected itself. Direct extraction of `https://code.claude.com/docs/en/output-styles` explicitly listed `Concise` and stated that it requires Claude Code v2.1.237 or later. The durable lesson is the verification sequence, not the volatile feature state: re-read the canonical page before carrying a contradictory Perplexity claim into the final answer.

The same run's Model Council returned official URLs whose HTTP `HEAD` probes included `403`, while direct page extraction succeeded. Treat this as transport/probe behavior and verify each material claim from the page body.
