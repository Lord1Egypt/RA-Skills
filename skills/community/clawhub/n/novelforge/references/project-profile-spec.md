# Project profile

The project profile is the only place where a project chooses its genre,
format, language register, style detectors, and narrative engines. Novel Core
does not assume a genre or author.

```json
{
  "schema": 1,
  "name": "my-project",
  "genre": "修仙+系统流",
  "format": "long_serial",
  "engine": "jin-yong",
  "engines": ["jin-yong"],
  "scale": {
    "tier": "standard",
    "target_words": 1000000,
    "words_per_chapter": 2500,
    "planned_volumes": 5,
    "estimated_chapters": 400
  },
  "narrative_scope": {
    "world_depth": "三界六道/飞升体系",
    "progression_ranks": 7,
    "primary_conflicts": ["正邪宗门存亡", "天道异化危机"]
  },
  "style_detectors": [],
  "policies": {
    "style_detector_mode": "warning"
  }
}
```

The `scale` field establishes deterministic word count and volume boundaries (`short`, `novella`, `standard`, `epic`).
Project policies may promote a detector to `blocking`, but a detector cannot
block engine installation. An omitted `style_detectors` field uses the Core's
advisory detector defaults; an explicit empty list disables those defaults.
Unknown fields are preserved under `custom` and are available to engine
applicability predicates.
