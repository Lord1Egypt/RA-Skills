# Chapter blueprint contract

Blueprints are planning artifacts, not draft prose. They describe intent,
causality, dependencies, and the expected settlement without writing dialogue or
paragraphs for the writer.

## Minimal JSON

```json
{
  "id": "v01-c001",
  "phase": "scene",
  "viewpoint": {"character": "character.example", "distance": "profile-defined"},
  "scene_types": ["choice"],
  "state": {
    "long_form": true,
    "chapter_boundary": true
  },
  "dependencies": {
    "entities": ["character.example"],
    "hooks": [],
    "relations": [],
    "events": []
  },
  "scenes": [
    {
      "id": "scene-1",
      "location": "location.example",
      "characters": ["character.example"],
      "goal": "",
      "pressure": "",
      "information_change": "",
      "exit_state": ""
    }
  ],
  "settlement": {
    "changes": [],
    "next_question": ""
  }
}
```

## Validation rules

- `id` matches the file name and is path-safe.
- `phase` is a non-empty string; `scene_types` and every dependency collection
  are string lists.
- When `scenes` is present, every scene has an ID, location, character list,
  goal, pressure, information change, and exit state.
- Every dependency file exists before context compilation; no missing item is
  inferred.
- The blueprint contains no direct dialogue, finished prose, or hidden
  dependency list.
- When `settlement` is present, it names expected fact and state changes, even
  when the expected list is empty.

Run `novelforgectl blueprint validate` before `context build`. The script, not this
document, decides whether the chapter may advance.
