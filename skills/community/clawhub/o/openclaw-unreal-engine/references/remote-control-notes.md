# Unreal Remote Control notes

## Use cases

Use Unreal Remote Control for editor-time control over exposed properties and functions. It is a good fit for OpenClaw when the agent should orchestrate work in the editor without embedding itself deeply into gameplay systems.

## How to think about it

Remote Control is the external control plane for editor-visible, explicitly exposed targets.

OpenClaw can:

- enumerate or target known presets/objects configured by the project
- set properties
- invoke exposed functions
- subscribe to updates when the chosen integration uses WebSocket/event support

## Best practices

- expose only what is needed
- separate safe read actions from mutating actions
- document which presets/objects the agent is expected to touch
- keep project-specific mapping in a reference file or config, not in the core skill body

## Important limitation

Do not confuse Remote Control with a general solution for every packaged runtime use case. For runtime gameplay and Blueprint UX, keep a project plugin in play.
