# Managing Agents

Agents are reusable video editing workflows (graphs of nodes/tiles).

## List agents

```
GET /agents
```

Returns all agents in your organization. [Docs](https://docs.mosaic.so/api/agents/get-agents)

## Get agent details

```
GET /agent/{agent_id}
```

Returns the full node graph. Use the `agent_node_id` values from the response to build `update_params` and `video_inputs`. [Docs](https://docs.mosaic.so/api/agents/get-agent)

## Create an agent

```
POST /agent/create
```

[Docs](https://docs.mosaic.so/api/agents/post-agent-create)

## Update an agent

```
POST /agent/{agent_id}/update
```

[Docs](https://docs.mosaic.so/api/agents/post-agent-update)

## Duplicate an agent

```
POST /agent/{agent_id}/duplicate
```

Creates a copy of an existing agent. [Docs](https://docs.mosaic.so/api/agents/post-agent-duplicate)

## Delete an agent

```
POST /agent/{agent_id}/delete
```

[Docs](https://docs.mosaic.so/api/agents/post-agent-delete)
