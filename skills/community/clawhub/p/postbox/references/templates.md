# Frontend Integration Templates

These are the base templates for integrating Postbox forms into frontends. Replace `{slug}`, `{endpoint}`, and `{FormName}` with actual values from the form creation response (`response.form.endpoint`). Generate real form fields based on the schema. Fields use a rules array: check for `{"op": "required"}` to mark fields as required in HTML. Validation errors are `422` status.

## Rules

1. NEVER use `<form method="POST" action="...">`. Always use `fetch()`.
2. Always handle validation errors from `error.details` (status 422) and display per-field.
3. Always handle success state (reset form, show message).
4. Always handle network errors.
5. Hide honeypot fields (those with `{"op": "honeypot"}` rule) with `position:absolute; left:-9999px; top:-9999px; opacity:0; pointer-events:none;` (not `display:none`).
6. Submit as `Content-Type: application/json` only.

## HTML + JavaScript Template

```html
<form id="{slug}-form">
  <!-- Generate inputs matching the schema:
       string  → <input type="text">
       email   → <input type="email">
       number  → <input type="number">
       boolean → <input type="checkbox">
       date    → <input type="date">
       Mark fields with {"op": "required"} rule using the `required` attribute.
  -->
  <!-- Honeypot (if schema includes a field with {"op": "honeypot"} rule): -->
  <div
    style="position:absolute; left:-9999px; top:-9999px; opacity:0; pointer-events:none;"
  >
    <input
      type="text"
      name="{honeypot_field}"
      tabindex="-1"
      autocomplete="off"
    />
  </div>
  <button type="submit">Submit</button>
  <div id="{slug}-errors" style="display:none; color:red;"></div>
  <div id="{slug}-success" style="display:none; color:green;">
    Submitted successfully!
  </div>
</form>

<script>
  document
    .getElementById("{slug}-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const errorsEl = document.getElementById("{slug}-errors");
      const successEl = document.getElementById("{slug}-success");
      errorsEl.style.display = "none";
      successEl.style.display = "none";

      const data = Object.fromEntries(new FormData(e.target));

      try {
        const res = await fetch("{endpoint}", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        if (res.ok) {
          successEl.style.display = "block";
          e.target.reset();
        } else {
          const body = await res.json();
          if (body.error?.details) {
            const messages = Object.entries(body.error.details)
              .map(([field, errs]) => `${field}: ${errs.join(", ")}`)
              .join("\n");
            errorsEl.textContent = messages;
          } else {
            errorsEl.textContent =
              body.error?.message || "Something went wrong.";
          }
          errorsEl.style.display = "block";
        }
      } catch (err) {
        errorsEl.textContent = "Network error. Please try again.";
        errorsEl.style.display = "block";
      }
    });
</script>
```

## React Template

```jsx
import { useState } from 'react';

export default function {FormName}Form() {
  const [errors, setErrors] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors(null);
    setSuccess(false);

    const data = Object.fromEntries(new FormData(e.target));

    try {
      const res = await fetch('{endpoint}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (res.ok) {
        setSuccess(true);
        e.target.reset();
      } else {
        const body = await res.json();
        if (body.error?.details) {
          setErrors(body.error.details);
        } else {
          setErrors({ _form: [body.error?.message || 'Something went wrong.'] });
        }
      }
    } catch {
      setErrors({ _form: ['Network error. Please try again.'] });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Generate fields from schema:
          string  → <input type="text" name="..." required />
          email   → <input type="email" name="..." required />
          number  → <input type="number" name="..." required />
          boolean → <input type="checkbox" name="..." />
          date    → <input type="date" name="..." required />
          Add `required` for fields with {"op": "required"} rule.
      */}
      {/* Honeypot (if schema includes a field with {"op": "honeypot"} rule): */}
      <div style={{ position: 'absolute', left: '-9999px', top: '-9999px', opacity: 0, pointerEvents: 'none' }}>
        <input type="text" name="{honeypot_field}" tabIndex={-1} autoComplete="off" />
      </div>
      {errors && Object.entries(errors).map(([field, msgs]) => (
        <p key={field} style={{ color: 'red' }}>{field}: {msgs.join(', ')}</p>
      ))}
      {success && <p style={{ color: 'green' }}>Submitted successfully!</p>}
      <button type="submit">Submit</button>
    </form>
  );
}
```
