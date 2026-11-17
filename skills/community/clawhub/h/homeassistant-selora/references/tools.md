# Selora AI MCP — Tool Reference

All 137 tools exposed by the Selora AI integration **v1.0.0** at `/api/selora_ai/mcp`, grouped by area.

🔒 = needs admin access: a Selora Connect user with an admin role or the `mcp:write` scope, or an MCP token with **Admin** permission (or one that lists the tool in its **Custom** allowlist). Some of these tools only *read*, but they are still gated because Home Assistant itself keeps the data admin-only (logs, traces, backups, camera images, config files, HACS, apps).

Every tool returns its own schema through `tools/list`. The descriptions there are authoritative: read them before calling a tool for the first time.

## Home state & entities

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_get_home_snapshot` |  | Return current Home Assistant entity states grouped by area. |
| `selora_get_entity_state` |  | Return current state and key attributes for a single Home Assistant entity. |
| `selora_search_entities` |  | Fuzzy-search entities by name, alias, area, or device brand/model. Filters (domain, device_class, area, state, label) work alone too — e.g. `state=unavailable`. |
| `selora_find_entities_by_area` |  | Return entities located in a given area, optionally filtered by domain. |
| `selora_list_devices` |  | List Home Assistant devices tracked by Selora AI with their area, manufacturer, model, integration, and entity IDs. |
| `selora_get_device` |  | Return full detail for a single Home Assistant device: metadata, all associated entities, and their current states and key attributes. |
| `selora_get_entity_history` |  | Recorder data for up to 10 entities: `source=history` (state changes), `statistics` (long-term mean/min/max/change), or `logbook` (what happened and what caused it). |
| `selora_home_analytics` |  | Get analytics about device usage patterns and state changes. |
| `selora_find_references` |  | List the automations, scripts and scenes that use an entity or a device — as a trigger, condition, target or member. |
| `selora_list_services` |  | List the services Home Assistant can call, and the fields each accepts. |
| `selora_eval_template` | 🔒 | Evaluate a Home Assistant Jinja template using HA's sandbox. |
| `selora_get_camera_image` | 🔒 | A snapshot from a camera, returned as an image you can look at — who is at the door, whether the garage closed, a package on the porch. |

## Device control

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_validate_action` |  | Check a Home Assistant service call WITHOUT running it: whether the service and entities exist, its risk level, and whether selora_execute_command would ask for confirmation first. |
| `selora_execute_command` | 🔒 | Call any Home Assistant service — lights, locks, scripts, notifications, to-do lists, buttons, number and select entities, and the rest. |
| `selora_fire_event` | 🔒 | Fire an event on Home Assistant's bus — for automations triggered by a custom event, Node-RED flows, or testing an automation by simulating the event that starts it. |

## Selora AI chat, patterns & suggestions

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_chat` | 🔒 | Send a natural-language message to Selora's internal LLM in the context of the current home state. |
| `selora_list_sessions` |  | Return recent Selora chat sessions (title, id, timestamp). |
| `selora_list_patterns` |  | List detected behavior patterns derived from Selora suggestions. |
| `selora_get_pattern` |  | Return full detail for one pattern, including linked suggestions. |
| `selora_list_suggestions` |  | List proactive automation suggestions with YAML previews and risk assessment. |
| `selora_accept_suggestion` | 🔒 | Create an automation from a pending suggestion and mark it accepted. |
| `selora_dismiss_suggestion` | 🔒 | Mark a suggestion as dismissed. |
| `selora_trigger_scan` | 🔒 | Trigger an immediate suggestion scan. |

## Automations

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_automations` |  | List all Home Assistant automations (yaml + storage-managed) with their entity_id, status, and source. |
| `selora_get_automation` |  | Return full detail for any HA automation. |
| `selora_validate_automation` |  | Validate and risk-assess a YAML string representing a Home Assistant automation WITHOUT creating or modifying anything. |
| `selora_create_automation` | 🔒 | Create a new Home Assistant automation from a YAML string, or REPLACE an existing one by passing automation_id — any automation saved in automations.yaml, whoever created it. |
| `selora_accept_automation` | 🔒 | Enable or disable any HA automation. |
| `selora_trigger_automation` | 🔒 | Trigger any HA automation immediately via the automation.trigger service. |
| `selora_delete_automation` | 🔒 | Delete any yaml-managed HA automation permanently. |
| `selora_get_device_triggers` |  | Return the ready-to-use `platform: device` trigger blocks that Home Assistant offers for a device — button presses, scene-controller events, etc. |
| `selora_get_automation_traces` | 🔒 | Return the most recent runs of one automation or script: what triggered it, and the step each run stopped at — that step's configuration and its result (a condition that returned false, an action that errored). |

## Blueprints

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_blueprints` | 🔒 | Blueprints installed on this home — parameterised automation, script and template blueprints. |
| `selora_get_blueprint` | 🔒 | One blueprint's inputs in full — name, description, selector and default for each, and whether it is required. |
| `selora_import_blueprint` | 🔒 | Import a blueprint from a URL — a Home Assistant community forum post, GitHub, a gist or the HA website (other hosts are refused). |
| `selora_delete_blueprint` | 🔒 | Delete a blueprint (domain and path from list_blueprints). |

## Scenes

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_scenes` |  | List all Home Assistant scenes (yaml + storage-managed) with their entity_id, name, source, and a 'selora_managed' flag. |
| `selora_get_scene` |  | Return full detail for any HA scene. |
| `selora_validate_scene` |  | Validate a scene payload (name + entities) WITHOUT creating anything. |
| `selora_create_scene` | 🔒 | Create a new Selora-managed scene from a name and an entities map. |
| `selora_update_scene` | 🔒 | Change an existing scene in scenes.yaml — Selora's or one made in Home Assistant's editor: its name, the states it sets, or its icon. |
| `selora_activate_scene` | 🔒 | Activate any Home Assistant scene by calling scene.turn_on. |
| `selora_delete_scene` | 🔒 | Delete any yaml-managed HA scene from scenes.yaml. |

## Scripts

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_scripts` |  | List the home's scripts — named, reusable action sequences with no trigger. |
| `selora_get_script` |  | Return one script's full configuration, including its action sequence. |
| `selora_set_script` | 🔒 | Create a script, or replace an existing one entirely. |
| `selora_delete_script` | 🔒 | Delete a script. |

## Helpers & groups

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_helpers` |  | List the home's helper entities — input_boolean, input_number, timer, counter, schedule, zone, person, and the config-entry helpers. |
| `selora_create_helper` | 🔒 | Create any Home Assistant helper, immediately — no YAML, no restart. |
| `selora_update_helper` | 🔒 | Change a UI-created helper (input_*, counter, timer, schedule, zone, person): name, icon, options, range, duration… Pass only what changes. |
| `selora_delete_helper` | 🔒 | Delete a UI-created helper. Automations, scripts and cards using it stop working. |
| `selora_list_groups` |  | List Home Assistant group helpers with their members, live state, and config entry_id. |
| `selora_create_group` | 🔒 | Create a Home Assistant group helper: one entity_id that controls many devices. |
| `selora_update_group` | 🔒 | Change a group helper's members and/or name. |
| `selora_delete_group` | 🔒 | Delete a Home Assistant group helper, identified by entry_id, entity_id, or group_name. |

## Areas, floors, labels & categories

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_areas` |  | List every area and floor in the home with how many entities and devices each holds. |
| `selora_create_area` | 🔒 | Create a new area (room). |
| `selora_update_area` | 🔒 | Rename an area, move it to a floor, or change its icon or aliases. |
| `selora_assign_area` | 🔒 | Put one or more entities and/or devices into an area. |
| `selora_delete_area` | 🔒 | Delete an area. |
| `selora_list_floors` |  | Every floor of the home with the areas standing on it, ordered by level. |
| `selora_create_floor` | 🔒 | Create a floor. |
| `selora_update_floor` | 🔒 | Rename a floor or change its level, icon, or aliases. |
| `selora_delete_floor` | 🔒 | Delete a floor. |
| `selora_list_labels` |  | List the home's labels with how many entities, devices, and areas carry each. |
| `selora_create_label` | 🔒 | Create a label, or change one: a name already taken is that label — renamed with new_name, its icon, colour or description set, or removed with clear; assignments are kept. |
| `selora_assign_labels` | 🔒 | Add and/or remove labels on entities, devices, and areas. |
| `selora_delete_label` | 🔒 | Delete a label. |
| `selora_list_categories` |  | Categories file automations, scripts, scenes and helpers into named lists on their Home Assistant pages. |
| `selora_create_category` | 🔒 | Create a category within one list, or change one: a name already taken there is that category — renamed with new_name, its icon set or removed with clear=['icon']; what is in it stays. |
| `selora_assign_category` | 🔒 | File entities under a category within one list, or omit category to take them out of it. |
| `selora_delete_category` | 🔒 | Delete a category. |
| `selora_update_entity` | 🔒 | Change one entity's registry settings: friendly name, Assist aliases, icon, whether it is hidden or disabled, and which voice assistants (Assist, Alexa, Google) can see it. |
| `selora_update_device` | 🔒 | Rename a device, move it to an area, or disable it. |
| `selora_remove_device` | 🔒 | Remove a device with its entities — one that is gone for good. |
| `selora_remove_entity` | 🔒 | Remove an entity its integration no longer provides (Home Assistant shows it as restored / unavailable). |

## Dashboards

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_dashboards` |  | List every Lovelace dashboard. |
| `selora_get_dashboard` |  | Read a dashboard: its views (pages) with card counts, and — when you name a view — the cards on it. |
| `selora_get_dashboard_card` |  | Return one card's complete configuration plus its fingerprint. |
| `selora_create_dashboard` | 🔒 | Create a whole new dashboard, with its own sidebar entry, immediately. |
| `selora_update_dashboard` | 🔒 | Change a whole dashboard's settings: its title (the name in the sidebar), its sidebar icon, whether it shows in the sidebar, and whether it is admin-only. |
| `selora_delete_dashboard` | 🔒 | Delete a whole dashboard and everything on it. |
| `selora_set_dashboard_strategy` | 🔒 | Make a dashboard generated by a Home Assistant strategy (areas, home, map, energy, original-states, iframe, custom:) or change its strategy options. |
| `selora_add_dashboard_view` | 🔒 | Add a view (a PAGE) to a dashboard that already exists. |
| `selora_update_dashboard_view` | 🔒 | Rename a view, change its URL path, icon or options, or switch its layout (cards are carried over; a panel page holds one card). |
| `selora_remove_dashboard_view` | 🔒 | Delete a whole view and every card on it. |
| `selora_insert_dashboard_card` | 🔒 | Add a Lovelace card to a dashboard view. |
| `selora_update_dashboard_card` | 🔒 | Replace one card with a new config. |
| `selora_move_dashboard_card` | 🔒 | Move one card or several — to another position in the same view, to a different page, or to a DIFFERENT DASHBOARD. |
| `selora_group_dashboard_cards` | 🔒 | Move existing cards into a container card so they sit together — this is how cards end up side by side, since a masonry view has no rows. |
| `selora_remove_dashboard_card` | 🔒 | Remove one card from a view. |
| `selora_list_dashboard_resources` |  | List the dashboard resources: the JavaScript and CSS files custom cards (custom:button-card, card-mod, mushroom …) need loaded before they render. |
| `selora_add_dashboard_resource` | 🔒 | Register a dashboard resource so a custom card can load. |
| `selora_update_dashboard_resource` | 🔒 | Point a dashboard resource at a new URL (a card's new version) and/or type, keeping it registered throughout — removing and re-adding breaks every card using it in between. |
| `selora_remove_dashboard_resource` | 🔒 | Unregister a dashboard resource. |

## Calendars, energy & voice

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_calendar_events` |  | A calendar's events between start and end (default next 7 days), with the uid/recurrence_id needed to change or remove them. |
| `selora_set_calendar_event` | 🔒 | Add an event to a calendar, or change one by passing its uid (from list_calendar_events). |
| `selora_delete_calendar_event` | 🔒 | Remove an event (one occurrence, this-and-following, or the whole series) by uid. |
| `selora_get_energy_prefs` |  | Energy dashboard configuration (grid, solar, battery, gas, water, device consumption), its issues, and the `config_hash` needed to change it. |
| `selora_set_energy_prefs` | 🔒 | Change the Energy dashboard's configuration. |
| `selora_list_assist_pipelines` |  | Assist voice pipelines (conversation, STT, TTS, wake word engines and languages) and which is preferred. |
| `selora_set_assist_pipeline` | 🔒 | Create an Assist pipeline, or change one by passing pipeline_id — only the settings you pass change. |
| `selora_delete_assist_pipeline` | 🔒 | Delete an Assist pipeline, IMMEDIATELY. |

## Integrations, HACS & apps

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_list_integrations` |  | Integrations as Settings → Devices & services lists them, with state and the reason when not working. `problems_only=true` lists just the broken ones. |
| `selora_reload_integration` | 🔒 | Reload an integration — the usual fix for one stuck in setup_retry or showing stale devices — and return the state it came back in. |
| `selora_set_integration_enabled` | 🔒 | Enable or disable an integration. |
| `selora_set_integration_options` | 🔒 | Change an integration's options through its own options form. |
| `selora_remove_integration` | 🔒 | Remove an integration with all its devices and entities. |
| `selora_hacs_search` | 🔒 | Search HACS (the Home Assistant Community Store) for dashboard cards (category plugin — button-card, card-mod, mushroom …), themes and integrations, installed ones first. |
| `selora_hacs_info` | 🔒 | One HACS repository's details: versions, releases, whether it is installed, authors. |
| `selora_hacs_install` | 🔒 | Install a HACS repository, or update it (to version, or its latest release). |
| `selora_hacs_add_repository` | 🔒 | Add a custom GitHub repository to HACS so it can be installed — for something not in HACS's default list. |
| `selora_hacs_remove` | 🔒 | Uninstall a HACS repository. |
| `selora_list_apps` | 🔒 | The installed apps (formerly add-ons) — Mosquitto, Z-Wave JS, Node-RED … — each with its slug, state (started, stopped …), version and whether an update is available. |
| `selora_search_app_store` | 🔒 | Find apps (formerly add-ons) in the app store — official and added repositories — by words in their name or description, with whether each is installed. |
| `selora_install_app` | 🔒 | Install an app from the store. |
| `selora_get_app_options` | 🔒 | An installed app's options and the schema they follow. |
| `selora_set_app_options` | 🔒 | Change an installed app's options: pass only what changes — the rest, passwords included, are kept. |
| `selora_get_app_logs` | 🔒 | The last lines an app logged (100 by default, at most 500) — read them when an app will not start or misbehaves. |

## Health, updates & maintenance

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_check_system` | 🔒 | What needs attention, in one call: failing integrations, open repairs, pending updates, backup health, offline Zigbee / Z-Wave / Matter devices. |
| `selora_list_repairs` |  | Home Assistant's open repairs (Settings → Repairs), most severe first: each with its title and description in the home's language, whether it has an automatic fix, and the version it breaks in. |
| `selora_fix_repair` | 🔒 | Run a fixable repair's own fix, step by step. |
| `selora_ignore_repair` | 🔒 | Ignore a repair, as the Repairs page's Ignore does — or show it again with ignore=false. |
| `selora_get_logs` | 🔒 | Return recent errors and warnings from Home Assistant's system log, deduplicated with a repeat count. |
| `selora_get_system_health` | 🔒 | Home Assistant's system information, as Settings → System → Repairs → System information shows it: the core version and install, and each integration's health (recorder database, Supervisor, cloud …). |
| `selora_get_diagnostics` | 🔒 | An integration's diagnostics — what its 'Download diagnostics' gives, redacted — for one entry (entry_id from list_integrations) or one of its devices. |
| `selora_get_network_health` | 🔒 | The home's Zigbee (ZHA or Zigbee2MQTT), Z-Wave and Matter networks: each one's controller, how many devices it has, and which are offline or have a weak signal (LQI, RSSI), with when they were last seen. |
| `selora_list_updates` |  | What can be updated: Home Assistant itself (core, OS, supervisor), apps, HACS repositories, device firmware and the rest — each with its installed and latest version, a short release summary and link. |
| `selora_get_release_notes` | 🔒 | The full release notes of one update (from list_updates), where its integration provides them — read them for breaking changes before installing. |
| `selora_get_backups` | 🔒 | Backups newest first, plus automatic-backup health (last completed/attempted, next scheduled, failure warnings). |
| `selora_restart_home_assistant` | 🔒 | Restart Home Assistant — how YAML edits (set_config_yaml) and newly installed integrations (hacs_install) take effect. |

## Configuration files

| Tool | Admin | Description |
|------|:-----:|-------------|
| `selora_get_config_yaml` | 🔒 | Read Home Assistant's YAML configuration: a file's top-level keys (and, for configuration.yaml, the package and theme files there are), or one key's YAML with yaml_path. |
| `selora_set_config_yaml` | 🔒 | Edit Home Assistant's YAML configuration — LAST RESORT, for what no other tool reaches: YAML-only integrations (rest, command_line, shell_command, notify platforms, template, mqtt, knx …), package files, and themes. Two steps: the first call returns a diff and a `confirm_token` and writes nothing. |
| `selora_list_files` | 🔒 | List one folder's files and subfolders under www/, themes/, custom_templates/, dashboards/ or blueprints/. |
| `selora_read_file` | 🔒 | Read a text file under www/, themes/, custom_templates/, dashboards/ or blueprints/. |
| `selora_write_file` | 🔒 | Create a text file under www/, themes/, custom_templates/ or dashboards/ — card files, theme assets, Jinja macros, YAML dashboards. |
| `selora_delete_file` | 🔒 | Delete a text file under www/, themes/, custom_templates/ or dashboards/. |

