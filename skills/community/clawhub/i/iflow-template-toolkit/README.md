# iFlow Template Toolkit

A simple, dependency-free template and internationalization toolkit for iFlow skills.

## Features

- **Template Engine**: Variable substitution, conditionals, and loops
- **Internationalization**: Multi-language support with JSON-based translations
- **Zero Dependencies**: Uses only Python standard library
- **Easy Integration**: Simple API for quick adoption

## Quick Start

### Template Rendering

```python
from iflow_template_toolkit import render_template

# Simple variable
render_template("Hello {{name}}!", {"name": "World"})
# → "Hello World!"

# Conditionals
template = """
{% if role == "admin" %}
Welcome, Administrator!
{% else %}
Welcome, User!
{% endif %}
"""
render_template(template, {"role": "admin"})
# → "Welcome, Administrator!"

# Loops
template = """
Items:
{% for item in items %}
- {{index1}}. {{item}}
{% endfor %}
"""
render_template(template, {"items": ["Apple", "Banana", "Cherry"]})
```

### Internationalization

```python
from iflow_template_toolkit import init_translator, t

# Initialize
init_translator({
    'en': {'hello': 'Hello', 'bye': 'Goodbye'},
    'zh': {'hello': '你好', 'bye': '再见'}
})

# Use
t('hello')           # → "Hello"
t('hello', lang='zh') # → "你好"
```

## Template Syntax Reference

| Syntax | Description |
|--------|-------------|
| `{{variable}}` | Variable substitution |
| `{% if condition %}` | Conditional block |
| `{% elif condition %}` | Else-if branch |
| `{% else %}` | Else branch |
| `{% endif %}` | End conditional |
| `{% for item in items %}` | Loop |
| `{% endfor %}` | End loop |
| `==` `!=` | Equality operators |
| `in` `not in` | Membership operators |

## License
MIT
