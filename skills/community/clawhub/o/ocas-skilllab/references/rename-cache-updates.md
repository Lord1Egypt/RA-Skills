# Rename Cache Updates

When to read: during a skill rename, for the exact cache-key rewrite snippets.

   ```python
   import json
   with open(os.path.expanduser("~/.hermes/.skills_prompt_snapshot.json")) as f:
       cache = json.load(f)
   cache["new-name"] = cache.pop("old-name")
   with open(os.path.expanduser("~/.hermes/.skills_prompt_snapshot.json"), "w") as f:
       json.dump(cache, f, indent=2)
   ```

