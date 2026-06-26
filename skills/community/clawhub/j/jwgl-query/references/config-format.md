# Config format

## `config.json`

Create a local `config.json` in the skill root.

The structure is split into school URLs, teacher credentials, login selectors, and per-query selectors. When the user provides a new school URL or teacher account/password, save it into the local config for reuse.

```json
{
  "current_school": "某学校",
  "schools": {
    "某学校": {
      "base_url": "https://jwgl.example.edu.cn",
      "login_url": "https://jwgl.example.edu.cn/jsxsd/framework/jsMain.jsp"
    }
  },
  "teachers": {
    "某老师": {
      "username": "teacher_account",
      "password": "REPLACE_ME",
      "school": "某学校"
    }
  },
  "selectors": {
    "login": {
      "username": { "by": "id", "value": "userAccount" },
      "password": { "by": "id", "value": "userPassword" },
      "login_button": { "by": "css", "value": "button.login_btn" }
    },
    "queries": {
      "invigilation": {
        "menu_parent": { "by": "xpath", "value": "..." },
        "menu_child": { "by": "xpath", "value": "..." },
        "query_frame": { "by": "id", "value": "Frame1" },
        "term_select": { "by": "id", "value": "xnxqid" },
        "query_button": { "by": "xpath", "value": "//*[@id='btn_query']" },
        "result_frame": { "by": "id", "value": "fcenter" },
        "table_id": "dataList"
      },
      "course_schedule": {
        "menu_parent": { "by": "xpath", "value": "..." },
        "menu_child": { "by": "xpath", "value": "..." },
        "query_frame": { "by": "id", "value": "..." },
        "term_select": { "by": "id", "value": "..." },
        "query_button": { "by": "xpath", "value": "..." },
        "result_frame": { "by": "id", "value": "..." },
        "table_id": "dataList"
      }
    }
  }
}
```

Notes:

- New configs should use the `schools` map plus `current_school`.
- `teacher.school` is optional but recommended when you manage multiple schools.
- If the user only provides a school base URL, derive `login_url` as `{base_url}/jsxsd/framework/jsMain.jsp`.
- When `config.json` is written or loaded, missing `selectors` / `selectors.queries.*` should be merged from `config.example.json` so the runtime config stays directly usable.
- Legacy root-level `base_url` and `login_url` are still tolerated for backward compatibility, but new writes should treat school URLs as named entries.

## Selector object format

```json
{ "by": "id|xpath|css|name", "value": "..." }
```

## Output model

- Prefer direct query output in chat.
- Use JSON during debugging.
- Add text summarization in OpenClaw orchestration rather than hardcoding messaging into the Python script.
