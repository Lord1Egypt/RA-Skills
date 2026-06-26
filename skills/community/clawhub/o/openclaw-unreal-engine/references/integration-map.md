# Integration map for the evaluated Unreal Engine repo

## Goal

Map OpenClaw capabilities onto the built-in systems confirmed in the evaluated Unreal Engine source repository.

## Editor automation

### Best fit

- `RemoteControl`
- `WebRemoteControl`
- `RemoteControlUI`

### OpenClaw role

- call exposed functions/properties
- manage editor-side task orchestration
- drive preset-based automation

### Why

The repo already includes a webserver-backed Remote Control stack, so OpenClaw should use it rather than rebuild editor RPC from scratch.

## Blueprint-first request/response

### Best fit

- `HttpBlueprint`
- `JsonBlueprintUtilities`

### OpenClaw role

- receive HTTP requests from Blueprint graphs
- return structured JSON results
- support low-code prototypes and designer-driven flows

### Why

These modules already cover the boring plumbing: HTTP request execution and JSON manipulation in Blueprint.

## Python editor tooling

### Best fit

- `PythonScriptPlugin`

### OpenClaw role

- trigger editor scripting workflows
- batch asset/content tasks
- support rapid iteration without bespoke C++ for every editor tool

### Why

The repo includes Python integration and remote-execution internals. This is a strong fit for editor-only task automation.

## Runtime interaction

### Best fit

- custom OpenClaw runtime plugin
- UE `HTTP`
- UE `WebSockets`

### OpenClaw role

- session/auth/task protocol
- runtime-safe messaging
- progress/event streaming
- gameplay-adjacent utility tasks

### Why

Runtime concerns remain project-specific and should live in a custom plugin rather than piggybacking blindly on editor-oriented systems.

## Suggested split of responsibilities

- **Remote Control**: editor-visible object/function/property control
- **HttpBlueprint + JsonBlueprintUtilities**: Blueprint-friendly HTTP + JSON glue
- **PythonScriptPlugin**: editor scripting/content ops
- **OpenClaw plugin**: auth, session model, protocol, runtime helpers, editor UX glue
