---
source: "config/model.yaml"
core_kind: "business_material"
file_type: "yaml"
generated: "2026-06-14T19:16:07"
tags:
  - core-file
  - business-material
  - yaml
---
<!-- CORE_FILE_NOTE_V1 -->
# model.yaml

- Source file: [[config/model.yaml|model.yaml]]
- Folder index: [[config/资料索引|资料索引]]
- Core kind: `business_material`
- Size: 218 B
- Modified: 2026-06-13T11:32:09

## Summary
- YAML sample: 8 lines, 218 chars.
- Opening: provider: openai_compatible
- Keywords: deepseek, provider, openai_compatible, base_url, https, chat_completions_path, chat, completions, model, api_key_env

## Related files
- [[config/model.yaml.core|model.yaml.core.md]] - same folder
- [[config/evaluation.yaml.core|evaluation.yaml.core.md]] - same folder
- [[config/evaluation.yaml.core|evaluation.yaml]] - same folder

## Graph tags
- #core-file/business-material
- #file-type/yaml

## Content preview
```text
provider: openai_compatible
base_url: "https://api.deepseek.com"
chat_completions_path: "/chat/completions"
model: "deepseek-v4-pro"
api_key_env: "DEEPSEEK_API_KEY"
timeout_seconds: 120
max_retries: 2
temperature: 0.1
```

## Processing notes
- encoding=utf-8-sig
