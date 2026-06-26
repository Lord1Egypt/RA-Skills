# Mosaic API Endpoint Map

Canonical docs:
- [Docs home](https://docs.mosaic.so)
- [API reference index](https://docs.mosaic.so/api/introduction)

## Agents

- [`POST /agent/create`](https://docs.mosaic.so/api/agents/post-agent-create)
- [`POST /agent/{agent_id}/update`](https://docs.mosaic.so/api/agents/post-agent-update)
- [`POST /agent/{agent_id}/delete`](https://docs.mosaic.so/api/agents/post-agent-delete)
- [`POST /agent/{agent_id}/duplicate`](https://docs.mosaic.so/api/agents/post-agent-duplicate)
- [`GET /agents`](https://docs.mosaic.so/api/agents/get-agents)
- [`GET /agent/{agent_id}`](https://docs.mosaic.so/api/agents/get-agent)

## Runs

- [`GET /agent/{agent_id}/runs`](https://docs.mosaic.so/api/agent-runs/get-agent-runs)
- [`GET /agent_runs`](https://docs.mosaic.so/api/agent-runs/get-all-agent-runs)
- [`GET /trigger/{trigger_id}/runs`](https://docs.mosaic.so/api/agent-runs/get-trigger-runs)
- [`POST /agent/{agent_id}/run`](https://docs.mosaic.so/api/agent-runs/post-agent-run)
- [`GET /agent_run/{run_id}`](https://docs.mosaic.so/api/agent-runs/get-agent-run)
- [`GET /agent_run/{run_id}/nodes`](https://docs.mosaic.so/api/agent-runs/get-agent-run-nodes)
- [`POST /agent_run/{run_id}/resume`](https://docs.mosaic.so/api/agent-runs/post-agent-run-resume)
- [`POST /agent_run/{run_id}/cancel`](https://docs.mosaic.so/api/agent-runs/post-agent-run-cancel)

## Node discovery

- [`GET /node_types`](https://docs.mosaic.so/api/agent-nodes/get-agent-nodes)
- [`GET /node_type/{node_type_id}`](https://docs.mosaic.so/api/node-types/get-node-type)
- [`GET /agent_nodes/{agent_node_id}`](https://docs.mosaic.so/api/agent-nodes/get-agent-node)

## Triggers

- [`GET /agent/{agent_id}/triggers`](https://docs.mosaic.so/api/triggers/get-agent-triggers)
- [`POST /agent/{agent_id}/triggers/add_youtube_channels`](https://docs.mosaic.so/api/triggers/post-add-youtube-channels)
- [`POST /agent/{agent_id}/triggers/remove_youtube_channels`](https://docs.mosaic.so/api/triggers/post-remove-youtube-channels)

## Credits & billing

- [`GET /credits`](https://docs.mosaic.so/api/credits/get-credits)
- [`GET /credits/usage`](https://docs.mosaic.so/api/credits/get-credits-usage)
- [`POST /credits/settings`](https://docs.mosaic.so/api/credits/post-credits-settings)
- [`GET /plan`](https://docs.mosaic.so/api/plan/get-plan)
- [`GET /plan/list`](https://docs.mosaic.so/api/plan/get-plan-list)
- [`POST /plan/upgrade`](https://docs.mosaic.so/api/plan/post-plan-upgrade)

## Social publishing

- [`POST /social/{platform}/connect`](https://docs.mosaic.so/api/social/post-social-platform-connect)
- [`GET /social/{platform}/status`](https://docs.mosaic.so/api/social/get-social-platform-status)
- [`DELETE /social/{platform}/remove`](https://docs.mosaic.so/api/social/delete-social-platform-remove)
- [`POST /social/post`](https://docs.mosaic.so/api/social/post-social-post)
- [`GET /social/post/{post_id}`](https://docs.mosaic.so/api/social/get-social-post)
- [`GET /social/post/track/{tracking_id}`](https://docs.mosaic.so/api/social/get-social-post-track)
- [`PATCH /social/post/{post_id}`](https://docs.mosaic.so/api/social/patch-social-post)
- [`DELETE /social/post/{post_id}`](https://docs.mosaic.so/api/social/delete-social-post)

## Asset management

- [`POST /uploads/video/get_upload_url`](https://docs.mosaic.so/api/asset-management/post-uploads-video-get-upload-url)
- [`POST /uploads/video/finalize_upload`](https://docs.mosaic.so/api/asset-management/post-uploads-video-finalize-upload)
- [`POST /uploads/audio/get_upload_url`](https://docs.mosaic.so/api/asset-management/post-uploads-audio-get-upload-url)
- [`POST /uploads/audio/finalize_upload`](https://docs.mosaic.so/api/asset-management/post-uploads-audio-finalize-upload)
- [`POST /uploads/image/get_upload_url`](https://docs.mosaic.so/api/asset-management/post-uploads-image-get-upload-url)
- [`POST /uploads/image/finalize_upload`](https://docs.mosaic.so/api/asset-management/post-uploads-image-finalize-upload)
- [`POST /uploads/get_view_url`](https://docs.mosaic.so/api/asset-management/post-uploads-get-view-url)

## Webhooks

- [Webhook events](https://docs.mosaic.so/api/webhooks/events)
