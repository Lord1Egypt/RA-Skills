---
version: "1.0"
title: "{{ title }}"
source_hash: "{{ source_hash }}"
source_path: "{{ source_path }}"
extracted_at: "{{ extracted_at }}"
model: "{{ model }}"
type: essence
tags: {{ tags }}
---

# {{ title }}

## Zusammenfassung

{{ summary }}

## Kernpunkte

{% for point in key_points %}
- {{ point }}
{% endfor %}

## Entitäten

{% for entity in entities %}
- {{ entity }}
{% endfor %}

## Beziehungen

{% for rel in relationships %}
- **{{ rel.from }}** → {{ rel.type }} → **{{ rel.to }}**
{% endfor %}

## Keywords

{{ keywords | join(", ") }}

---

*Extracted: {{ extracted_at }} | Model: {{ model }}*