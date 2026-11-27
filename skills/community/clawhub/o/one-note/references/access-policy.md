# OneNote access policy

An access policy limits which endpoints OneNote connections may call through Maton. OneNote doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/one-note#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for OneNote: its 30 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create one-note --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1.0/me/onenote/notebooks"},
    {"method": "GET", "path": "v1.0/me/onenote/notebooks/{id}"},
    {"method": "POST", "path": "v1.0/me/onenote/notebooks/getNotebookFromWebUrl"},
    {"method": "GET", "path": "v1.0/me/onenote/sectionGroups"},
    {"method": "GET", "path": "v1.0/me/onenote/sectionGroups/{id}"},
    {"method": "GET", "path": "v1.0/me/onenote/notebooks/{id}/sectionGroups"},
    {"method": "GET", "path": "v1.0/me/onenote/sectionGroups/{id}/sectionGroups"},
    {"method": "GET", "path": "v1.0/me/onenote/sectionGroups/{id}/parentNotebook"},
    {"method": "GET", "path": "v1.0/me/onenote/sections"},
    {"method": "GET", "path": "v1.0/me/onenote/sections/{id}"},
    {"method": "GET", "path": "v1.0/me/onenote/notebooks/{id}/sections"},
    {"method": "GET", "path": "v1.0/me/onenote/sectionGroups/{id}/sections"},
    {"method": "GET", "path": "v1.0/me/onenote/sections/{id}/parentNotebook"},
    {"method": "GET", "path": "v1.0/me/onenote/pages"},
    {"method": "GET", "path": "v1.0/me/onenote/pages/{id}"},
    {"method": "GET", "path": "v1.0/me/onenote/pages/{id}/content"},
    {"method": "GET", "path": "v1.0/me/onenote/pages/{id}/preview"},
    {"method": "GET", "path": "v1.0/me/onenote/pages/{id}/parentSection"},
    {"method": "GET", "path": "v1.0/me/onenote/sections/{id}/pages"},
    {"method": "GET", "path": "v1.0/me/onenote/resources/{id}"},
    {"method": "GET", "path": "v1.0/me/onenote/resources/{id}/content"},
    {"method": "GET", "path": "v1.0/me/onenote/resources/{id}/$value"},
    {"method": "GET", "path": "v1.0/me/onenote/operations/{id}"},
    {"method": "GET", "path": "v1.0/me/onenote/**"},
    {"method": "GET", "path": "v1.0/users/{id}/onenote/**"},
    {"method": "POST", "path": "v1.0/users/{id}/onenote/notebooks/getNotebookFromWebUrl"},
    {"method": "GET", "path": "v1.0/groups/{id}/onenote/**"},
    {"method": "POST", "path": "v1.0/groups/{id}/onenote/notebooks/getNotebookFromWebUrl"},
    {"method": "GET", "path": "v1.0/sites/{id}/onenote/**"},
    {"method": "POST", "path": "v1.0/sites/{id}/onenote/notebooks/getNotebookFromWebUrl"}
  ],
  "deny": []
}
```

## Endpoints

The OneNote endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1.0/me/onenote/notebooks | read | notebooks | List notebooks. |
| GET | v1.0/me/onenote/notebooks/{id} | read | notebooks | Get a notebook, or recent notebooks via notebooks/getRecentNotebooks(includePersonalNotebooks=true). |
| POST | v1.0/me/onenote/notebooks/getNotebookFromWebUrl | read | notebooks | Look up a notebook by its web URL (POST only carries the URL). |
| POST | v1.0/me/onenote/notebooks | write | notebooks | Create a notebook. |
| POST | v1.0/me/onenote/notebooks/{id}/copyNotebook | write | notebooks | Copy a notebook. |
| GET | v1.0/me/onenote/sectionGroups | read | section groups | List all section groups. |
| GET | v1.0/me/onenote/sectionGroups/{id} | read | section groups | Get a section group. |
| GET | v1.0/me/onenote/notebooks/{id}/sectionGroups | read | section groups | List the section groups in a notebook. |
| GET | v1.0/me/onenote/sectionGroups/{id}/sectionGroups | read | section groups | List nested section groups. |
| GET | v1.0/me/onenote/sectionGroups/{id}/parentNotebook | read | section groups | Get the notebook that contains a section group. |
| POST | v1.0/me/onenote/notebooks/{id}/sectionGroups | write | section groups | Create a section group in a notebook. |
| POST | v1.0/me/onenote/sectionGroups/{id}/sectionGroups | write | section groups | Create a nested section group. |
| GET | v1.0/me/onenote/sections | read | sections | List all sections. |
| GET | v1.0/me/onenote/sections/{id} | read | sections | Get a section. |
| GET | v1.0/me/onenote/notebooks/{id}/sections | read | sections | List the sections in a notebook. |
| GET | v1.0/me/onenote/sectionGroups/{id}/sections | read | sections | List the sections in a section group. |
| GET | v1.0/me/onenote/sections/{id}/parentNotebook | read | sections | Get the notebook that contains a section. |
| POST | v1.0/me/onenote/notebooks/{id}/sections | write | sections | Create a section in a notebook. |
| POST | v1.0/me/onenote/sectionGroups/{id}/sections | write | sections | Create a section in a section group. |
| POST | v1.0/me/onenote/sections/{id}/copyToNotebook | write | sections | Copy a section to a notebook. |
| POST | v1.0/me/onenote/sections/{id}/copyToSectionGroup | write | sections | Copy a section to a section group. |
| GET | v1.0/me/onenote/pages | read | pages | List all pages. |
| GET | v1.0/me/onenote/pages/{id} | read | pages | Get a page's metadata. |
| GET | v1.0/me/onenote/pages/{id}/content | read | pages | Get a page's HTML content. |
| GET | v1.0/me/onenote/pages/{id}/preview | read | pages | Get a text preview of a page. |
| GET | v1.0/me/onenote/pages/{id}/parentSection | read | pages | Get the section that contains a page. |
| GET | v1.0/me/onenote/sections/{id}/pages | read | pages | List the pages in a section. |
| POST | v1.0/me/onenote/pages | write | pages | Create a page in the default section (or ?sectionName=). |
| POST | v1.0/me/onenote/sections/{id}/pages | write | pages | Create a page in a section. |
| PATCH | v1.0/me/onenote/pages/{id}/content | write | pages | Update a page's content with patch commands. |
| POST | v1.0/me/onenote/pages/{id}/onenotePatchContent | write | pages | Update a page's content (action form). |
| PATCH | v1.0/me/onenote/pages/{id} | write | pages | Update a page's metadata, e.g. its level or order. |
| POST | v1.0/me/onenote/pages/{id}/copyToSection | write | pages | Copy a page to a section. |
| DELETE | v1.0/me/onenote/pages/{id} | write | pages | Delete a page. |
| GET | v1.0/me/onenote/resources/{id} | read | resources | Get an image or file resource embedded in a page. |
| GET | v1.0/me/onenote/resources/{id}/content | read | resources | Download the binary content of a page resource. |
| GET | v1.0/me/onenote/resources/{id}/$value | read | resources | Download the binary content of a page resource ($value form). |
| GET | v1.0/me/onenote/operations/{id} | read | operations | Get the status of a long-running copy operation. |
| GET | `v1.0/me/onenote/**` | read | onenote trees | Any GET under the signed-in user's OneNote: notebooks, section groups, sections, pages, content, resources (all reads). |
| POST | `v1.0/me/onenote/**` | write | onenote trees | Any other POST under the signed-in user's OneNote: create, update, copy or delete. |
| PUT | `v1.0/me/onenote/**` | write | onenote trees | Any other PUT under the signed-in user's OneNote: create, update, copy or delete. |
| PATCH | `v1.0/me/onenote/**` | write | onenote trees | Any other PATCH under the signed-in user's OneNote: create, update, copy or delete. |
| DELETE | `v1.0/me/onenote/**` | write | onenote trees | Any other DELETE under the signed-in user's OneNote: create, update, copy or delete. |
| GET | `v1.0/users/{id}/onenote/**` | read | onenote trees | Any GET under a user's OneNote: notebooks, section groups, sections, pages, content, resources (all reads). |
| POST | v1.0/users/{id}/onenote/notebooks/getNotebookFromWebUrl | read | onenote trees | Look up a notebook by web URL in a user's OneNote. |
| POST | `v1.0/users/{id}/onenote/**` | write | onenote trees | Any other POST under a user's OneNote: create, update, copy or delete. |
| PUT | `v1.0/users/{id}/onenote/**` | write | onenote trees | Any other PUT under a user's OneNote: create, update, copy or delete. |
| PATCH | `v1.0/users/{id}/onenote/**` | write | onenote trees | Any other PATCH under a user's OneNote: create, update, copy or delete. |
| DELETE | `v1.0/users/{id}/onenote/**` | write | onenote trees | Any other DELETE under a user's OneNote: create, update, copy or delete. |
| GET | `v1.0/groups/{id}/onenote/**` | read | onenote trees | Any GET under a group's OneNote: notebooks, section groups, sections, pages, content, resources (all reads). |
| POST | v1.0/groups/{id}/onenote/notebooks/getNotebookFromWebUrl | read | onenote trees | Look up a notebook by web URL in a group's OneNote. |
| POST | `v1.0/groups/{id}/onenote/**` | write | onenote trees | Any other POST under a group's OneNote: create, update, copy or delete. |
| PUT | `v1.0/groups/{id}/onenote/**` | write | onenote trees | Any other PUT under a group's OneNote: create, update, copy or delete. |
| PATCH | `v1.0/groups/{id}/onenote/**` | write | onenote trees | Any other PATCH under a group's OneNote: create, update, copy or delete. |
| DELETE | `v1.0/groups/{id}/onenote/**` | write | onenote trees | Any other DELETE under a group's OneNote: create, update, copy or delete. |
| GET | `v1.0/sites/{id}/onenote/**` | read | onenote trees | Any GET under a site's OneNote: notebooks, section groups, sections, pages, content, resources (all reads). |
| POST | v1.0/sites/{id}/onenote/notebooks/getNotebookFromWebUrl | read | onenote trees | Look up a notebook by web URL in a site's OneNote. |
| POST | `v1.0/sites/{id}/onenote/**` | write | onenote trees | Any other POST under a site's OneNote: create, update, copy or delete. |
| PUT | `v1.0/sites/{id}/onenote/**` | write | onenote trees | Any other PUT under a site's OneNote: create, update, copy or delete. |
| PATCH | `v1.0/sites/{id}/onenote/**` | write | onenote trees | Any other PATCH under a site's OneNote: create, update, copy or delete. |
| DELETE | `v1.0/sites/{id}/onenote/**` | write | onenote trees | Any other DELETE under a site's OneNote: create, update, copy or delete. |
| POST | v1.0/$batch | write | batch | JSON batch of up to 20 Graph requests; can carry writes. |
