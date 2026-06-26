# JSON Schema Validator

Validates JSON data against JSON Schema definitions.

```javascript
function validate(data, schema) {
  const errors = [];
  if (schema.type && typeof data !== schema.type) {
    errors.push(`Expected ${schema.type}, got ${typeof data}`);
  }
  if (schema.required && Array.isArray(schema.required)) {
    for (const key of schema.required) {
      if (!(key in data)) errors.push(`Missing required: ${key}`);
    }
  }
  if (schema.properties) {
    for (const [key, subSchema] of Object.entries(schema.properties)) {
      if (key in data) {
        errors.push(...validate(data[key], subSchema));
      }
    }
  }
  return errors;
}

module.exports = { validate };
```
