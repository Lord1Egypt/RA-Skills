# OpenClaw Plugin API Reference

## **Overview**
This document provides a reference for OpenClaw's plugin API. Plugins can extend OpenClaw's functionality by adding new tools, commands, or integrations.

## **Plugin Structure**
A plugin consists of:
- An `openclaw.plugin.json` file containing metadata.
- A main JavaScript file (e.g., `index.js`).

### **`openclaw.plugin.json`**
| Field        | Type     | Description                                                                                     |
|--------------|----------|-------------------------------------------------------------------------------------------------|
| `name`       | string   | Name of the plugin (lowercase, hyphens only).                                                   |
| `version`    | string   | Version of the plugin (semver, e.g., `1.0.0`).                                                   |
| `description`| string   | Description of the plugin.                                                                      |
| `main`       | string   | Path to the main JavaScript file (default: `index.js`).                                         |
| `author`     | string   | Author of the plugin (optional).                                                                 |
| `license`    | string   | License (e.g., `MIT`, optional).                                                                  |
| `keywords`   | array    | Keywords for the plugin (optional).                                                              |
| `openclaw`   | object   | OpenClaw-specific configuration (optional).                                                       |

### **OpenClaw Configuration Object**
```json
{
  "openclaw": {
    "minVersion": "1.0.0",
    "permissions": ["network", "filesystem"]
  }
}
```

## **Plugin Lifecycle**

### **Entry Point**
```javascript
module.exports = {
  name: 'my-plugin',
  
  /**
   * Called when the plugin is loaded
   * @param {Object} context - OpenClaw context object
   */
  async onLoad(context) {
    this.context = context;
    // Initialize plugin
  },
  
  /**
   * Called when the plugin is activated
   */
  async onActivate() {
    // Plugin is now active
  },
  
  /**
   * Called when the plugin is deactivated
   */
  async onDeactivate() {
    // Clean up resources
  },
  
  /**
   * Register commands, tools, or handlers
   * @param {Object} registry - OpenClaw registry object
   */
  register(registry) {
    // Register commands, tools, etc.
  }
};
```

## **Context Object**
The `context` object passed to `onLoad` provides access to OpenClaw features:

```javascript
// Available properties depend on OpenClaw version
// Check the OpenClaw documentation for the current API

// Example context structure:
context = {
  version: '1.0.0',
  config: { ... },
  // Additional context properties
};
```

## **Registry Object**
The `registry` object passed to `register` allows registering plugin features:

```javascript
register(registry) {
  // Example: Register a command (check OpenClaw docs for current API)
  // registry.command('mycommand', this.myCommand.bind(this));
  
  // Example: Register a tool (check OpenClaw docs for current API)
  // registry.tool('mytool', this.myTool.bind(this));
}
```

> **Note**: The registry API is subject to change. Check the OpenClaw documentation for the current plugin API.

## **Best Practices**
- **Modularity**: Keep plugins small and focused on a single task.
- **Documentation**: Include a `README.md` explaining your plugin's purpose and usage.
- **Validation**: Run the validation script before installation:
  ```bash
  ~/.openclaw/skills/plugin-integration/scripts/validate-plugin.sh <plugin-dir>
  ```
- **Testing**: Test your plugin in a development environment before deploying.
- **Versioning**: Use semantic versioning (semver) for your plugin versions.

## **Example Plugin**
See `examples/hello-world/` for a complete example plugin.

## **Getting Help**
- OpenClaw Documentation: https://docs.openclaw.ai
- OpenClaw GitHub: https://github.com/openclaw/openclaw
- OpenClaw Discord: https://discord.gg/clawd