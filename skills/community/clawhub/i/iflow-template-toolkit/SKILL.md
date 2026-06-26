# iFlow Template Toolkit

## Description
A simple, dependency-free template and internationalization toolkit for iFlow skills. Provides template rendering with variable substitution, conditionals, and loops, plus multi-language support.

## Installation

```bash
# Clone or copy to your skills directory
openclaw skills install iflow-template-toolkit
```

## Usage

### Template Engine

```python
from iflow_template_toolkit import TemplateEngine, render_template

# Quick render from string
result = render_template("Hello {{name}}!", {"name": "World"})
# Output: "Hello World!"

# Using TemplateEngine class
engine = TemplateEngine("./templates")
result = engine.render_file("config.md", {
    "project_name": "my-project",
    "team_size": 5
})
```

### Template Syntax

**Variables:**
```
Hello {{name}}!
Project: {{project_name}}
```

**Conditionals:**
```
{% if status == "active" %}
Status is active
{% elif status == "pending" %}
Status is pending
{% else %}
Status unknown
{% endif %}
```

**Loops:**
```
{% for item in items %}
- {{item}} ({{index1}})
{% endfor %}
```

### Internationalization

```python
from iflow_template_toolkit import Translator, t, init_translator

# Initialize with translations
init_translator({
    'en': {'greeting': 'Hello', 'farewell': 'Goodbye'},
    'zh': {'greeting': '你好', 'farewell': '再见'}
}, default_lang='en')

# Translate
t('greeting')           # "Hello"
t('greeting', lang='zh')  # "你好"

# With interpolation
t('welcome', name='John')  # "Welcome, John!" (if translation is "Welcome, {name}!")
```

## Features

| Feature | Description |
|---------|-------------|
| Variable Substitution | `{{variable}}` syntax |
| Conditionals | `{% if %}...{% elif %}...{% else %}...{% endif %}` |
| Loops | `{% for item in items %}...{% endfor %}` |
| Comparison | `==`, `!=`, `in`, `not in` operators |
| Loop Variables | `index`, `index1`, `first`, `last` |
| Multi-language | JSON-based translation files |
| Fallback | Falls back to default language |

## Requirements
- Python 3.6+
- No external dependencies

## File Structure
```
iflow-template-toolkit/
├── src/
│   ├── __init__.py
│   ├── template_engine.py
│   ├── i18n/
│   │   ├── __init__.py
│   │   ├── translator.py
│   │   └── langs/
│   │       ├── en.json
│   │       └── zh.json
│   └── templates/
├── tests/
├── SKILL.md
└── README.md
```

## Version
1.0.0
