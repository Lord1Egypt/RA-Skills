## Stealth Browser Text Match Length Sensitivity (2026-06-06)

When using `click_element(instance_id, selector, text_match="...")` on elements with long visible text (e.g., Square's `market-row` which contains service name + description), **the match FAILS if the text_match string is too long or includes a partial description suffix**.

**Failure pattern:**
```
text_match="Swedish Massage A soothing"  → "Element not found: market-row"
text_match="Swedish Massage"             → success ✓
```

**Rule: Use the shortest unique prefix for `text_match`.** For Square services, this is typically just the service name (e.g., "Swedish Massage", "Deep Tissue Massage"). For staff options, the full option text is short enough to use as-is (e.g., "Any staff", "Abbie Ab"). For duration options, use the duration label (e.g., "1.5 Hours", "2 Hours").

**Why:** The stealth browser appears to match using `contains()` on the element's text content, but only up to what's rendered/truncated in the element's visible text. If the `text_match` string extends beyond the truncation point, the match fails with "Element not found".