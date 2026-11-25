# AI Host: Where the Run Happens

The host provides conversation, context, models, tools, permissions, events, and returned results. OpenXSys builds each run on the capability actually present in the current environment.

## Runtime contract

For each run, establish:

- what the current model can understand and generate;
- which user inputs, files, images, and history are truly in context;
- which tools can be called and how results and errors return;
- the boundaries of the file system, network, external applications, and execution environment;
- which actions can happen directly, which require confirmation, and which need another implementation;
- whether the host truly supports events, schedules, background work, or cross-session state.

A tool enters the current capability picture after one smallest real operation succeeds. When changing hosts, re-establish the actual state of authorization, caches, plugins, and background tasks.

## Context and the persistent system

Conversation context is the working surface for one run. The persistent system is jointly carried by user-owned files, works, tools, domain state, and natural-language handoff points. After context compression or a model change, recover from real files, authoritative state, current user corrections, and checkable results.

## Events and waiting

A file change, tool result, due signal, or external request actually delivered by the host is an event. Return-driven hosts inspect change when the user returns; event-driven hosts continue when the signal arrives. During a wait, preserve completed works and state what is pending, who can move it forward, and how the next confirmation will happen.

See the complete [runtime architecture](../runtime/architecture.md).
