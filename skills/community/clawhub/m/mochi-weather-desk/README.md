# Weather and Outing Desk

[Simplified Chinese guide](README.zh-CN.md)

Fetch a coordinate-based forecast or inspect saved Open-Meteo data for temperature, rain probability and wind.

## What it does

Fetch a coordinate-based forecast or inspect saved Open-Meteo data for temperature, rain probability and wind.

## Examples

After installation, send an example with its required files or parameters.

```text
Check the next three days’ rain probability for my selected city.
```

```text
Compare temperature and wind in this saved weather response.
```

```text
Fetch a week’s forecast for these coordinates and cite the source.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Use a user-selected city or coordinates; do not discover the device location automatically. Explain that a live request sends coordinates to Open-Meteo. Preserve attribution and check service usage terms, including commercial use. Forecasts are not official emergency alerts.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-weather-desk
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
