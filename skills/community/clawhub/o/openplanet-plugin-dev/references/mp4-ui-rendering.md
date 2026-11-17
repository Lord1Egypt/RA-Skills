# Openplanet MP4 UI / UX Rendering Notes

Collected while restyling `maniacalendar-dev` (the "TM News & Calendar" window)
from a plain list of `TextLinkOpenURL` items into a newsletter-style card list
with colored category badges and accent bars.

## Hard limitation: NO image loading in MP4

Openplanet MP4 ManiaScript has **neither `UI::Image` nor an `Images::` namespace**.
Grepping the API doc and all loaded plugins confirms it. You CANNOT load a
picture from a URL into an overlay window.

Consequence: a "thumbnail" must be faked. The clean approach is a thin **colored
accent bar** (a `BeginChild` whose `ChildBg` style color is the category color),
or a colored category "pill" badge. Don't waste time hunting for an image API —
it isn't there.

## Layout primitives that DO work on MP4

- `UI::BeginChild(id, size, border)` / `UI::EndChild()` — nested scroll/clip region.
  Set the card background with `UI::PushStyleColor(UI::Col::ChildBg, vec4(...))`
  around the `BeginChild`.
- `UI::Dummy(vec2(w, h))` — reserves space. Pair with `UI::SameLine()` to build
  a left "column" (accent bar) + right content column.
- `UI::SameLine()` — place next widget on same line (after a Dummy/Child).
- `UI::Button(label, vec2(0, 0))` — **`vec2(0,0)` means auto-size** (fits the
  text). Use this for badge pills instead of hard-coding a size.
- `UI::PushStyleColor(UI::Col::Button / ButtonHovered / ButtonActive / Text, color)`
  then `UI::Button(...)` then `UI::PopStyleColor(n)` — recolor a button to make a
  category badge. Remember to pop the SAME number of pushes.
- `UI::TextWrapped(s)` — wrapped body text (good for summaries/teasers).
- `UI::TextLinkOpenURL(label, url)` — clickable external link (already worked).
- `UI::Separator()`, `UI::TextDisabled(s)` — fine.

## Things that do NOT exist on MP4 (cost me a recompile)

- `UI::GetCursorScreenPos()` / `UI::SetCursorPos()` — NOT in the MP4 API. Do not
  use them for manual layout; rely on `Dummy` + `SameLine` + `BeginChild` instead.
- `UI::IsItemHovered()` — grep of the API doc returns nothing; don't rely on hover
  effects (the plain `BeginChild` card background is static).
- `DrawList` / `nvg` / `GetWindowDrawList()` — not available in the core MP4 API
  (some plugins ship a vendored `nvg.as` but that's a 3rd-party lib, not built-in).

## Reusable patterns

### Category detection from a title (color + label)
```angelscript
void GetNewsCategory(const string &in title, vec4 &out bg, vec4 &out fg, string &out label) {
    string t = title.ToLower();
    if (t.IndexOf("weekly shorts") != -1) { bg = vec4(0.95,0.55,0.20,1); fg = vec4(1,1,1,1); label = "Weekly Shorts"; return; }
    if (t.IndexOf("formula e")   != -1) { bg = vec4(0.95,0.25,0.30,1); fg = vec4(1,1,1,1); label = "Formula E";   return; }
    if (t.IndexOf("tournament")  != -1 || t.IndexOf("ewc") != -1) { bg = vec4(0.95,0.80,0.30,1); fg = vec4(0,0,0,1); label = "Tournament"; return; }
    if (t.IndexOf("season")      != -1) { bg = vec4(0.35,0.65,0.95,1); fg = vec4(1,1,1,1); label = "Season"; return; }
    // ... more rules ...
    // Fallback: stable hue from a title hash
    uint h = 0; for (uint i = 0; i < uint(title.Length); i++) h = h * 31 + uint(title[i]);
    float hue = float(h % 360) / 360.0f;
    bg = vec4(0.6+0.4*Math::Sin(hue*6.2831), 0.6+0.4*Math::Sin((hue+0.33)*6.2831), 0.6+0.4*Math::Sin((hue+0.66)*6.2831), 1.0);
    fg = vec4(0.03,0.03,0.03,1); label = "News";
}
```

### Newsletter card (accent bar + badge + title + teaser)
```angelscript
vec4 catBg, catFg; string catLabel;
GetNewsCategory(item.title, catBg, catFg, catLabel);

UI::PushStyleColor(UI::Col::ChildBg, vec4(0.10,0.10,0.13,0.85));
UI::BeginChild("news" + tostring(i), vec2(0, 104), true);
    // left accent stripe (simulated thumbnail)
    UI::PushStyleColor(UI::Col::ChildBg, catBg);
    UI::BeginChild("accent" + tostring(i), vec2(10, 88), false);
    UI::EndChild();
    UI::PopStyleColor();
    UI::SameLine();
    // category pill
    UI::PushStyleColor(UI::Col::Button, catBg);
    UI::PushStyleColor(UI::Col::ButtonHovered, catBg);
    UI::PushStyleColor(UI::Col::ButtonActive, catBg);
    UI::PushStyleColor(UI::Col::Text, catFg);
    UI::Button(catLabel + " ##cat" + tostring(i), vec2(0, 0));
    UI::PopStyleColor(4);
    UI::SameLine();
    if (item.date.Length > 0) UI::TextDisabled(item.date);
    // title link
    UI::PushStyleColor(UI::Col::Text, vec4(0.35,0.75,1.0,1));
    UI::TextLinkOpenURL(item.title, item.url);
    UI::PopStyleColor();
    // body
    if (item.summary.Length > 0) UI::TextWrapped(item.summary);
    else UI::TextWrapped("Read the full story on trackmania.com  ->");
UI::EndChild();
UI::PopStyleColor();
```

### Extract a summary from fetched HTML (og:description / meta description)
`ParseNewsHtml` often only captures the title + url. To give cards a body, pull
the page's meta description:
```angelscript
string ExtractMetaDescription(const string &in html) {
    string[] patterns = { "property=\"og:description\" content=\"", "name=\"description\" content=\"" };
    for (uint p = 0; p < patterns.Length; p++) {
        int pos = html.IndexOf(patterns[p]);
        if (pos != -1) {
            int v0 = pos + int(patterns[p].Length);
            int v1 = html.SubStr(v0).IndexOf("\"") + v0;
            if (v1 > v0) {
                string d = StripHtmlTags(html.SubStr(v0, v1 - v0)).Trim();
                if (d.Length > 0) return d;
            }
        }
    }
    return "";
}
```
Call it per item: `item.summary = ExtractMetaDescription(html);`

## Pitfalls
- `UI::PushStyleColor` / `PopStyleColor` must be balanced — `PopStyleColor(4)` to
  undo four pushes. A mismatch corrupts later widgets' colors.
- Nested `BeginChild` inside `BeginChild`: the INNER child's `ChildBg` push must be
  popped before the OUTER `EndChild`, or the outer card inherits the inner color.
- `vec2(0,0)` for `UI::Button` is valid (auto-size); do NOT substitute a fixed
  size unless you want a rigid pill.
- If `item.summary` is empty, still render a short teaser — an empty card looks
  broken. Don't leave the body blank.

### Reference: OpenPlanet-API-Reference

