---
version: "1.0"
title: "{{ title }}"
report_type: "{{ report_type }}"
generated_at: "{{ generated_at }}"
query: "{{ query }}"
model: "{{ model }}"
sources: {{ sources }}
related_topics: {{ related_topics }}
tags: {{ tags }}
---

# {{ title }}

> **Abfrage:** {{ query }}

## Zusammenfassung

{{ summary }}

---

## Detailanalyse

{{ content }}

---

## Quellen

{% for source in source_list %}
- {{ source }}
{% endfor %}

---

## Metadaten

- **Erstellt:** {{ generated_at }}
- **Modell:** {{ model }}
- **Typ:** {{ report_type }}
- **Quellen:** {{ sources | length }} Dokumente

---

*Automatisch generiert vom kb-framework LLM-System*