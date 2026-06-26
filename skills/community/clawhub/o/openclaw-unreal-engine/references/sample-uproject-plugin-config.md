# Sample `.uproject` plugin config

Use this when installing `OpenClawUnrealPlugin` as a project plugin.

## Example

```json
{
  "FileVersion": 3,
  "EngineAssociation": "5.4",
  "Category": "",
  "Description": "",
  "Plugins": [
    {
      "Name": "OpenClawUnrealPlugin",
      "Enabled": true
    },
    {
      "Name": "RemoteControl",
      "Enabled": true
    },
    {
      "Name": "HttpBlueprint",
      "Enabled": true
    },
    {
      "Name": "JsonBlueprintUtilities",
      "Enabled": true
    },
    {
      "Name": "PythonScriptPlugin",
      "Enabled": true,
      "TargetAllowList": ["Editor"]
    }
  ]
}
```

## Notes

- Enable `PythonScriptPlugin` only for editor-oriented workflows unless you have a specific reason otherwise.
- `RemoteControl` is best treated as editor-focused even though parts of the stack are runtime-capable.
- If your project does not need Python automation, omit `PythonScriptPlugin`.
- If you want a minimal runtime-only install, keep only `OpenClawUnrealPlugin` and the dependencies it truly uses.
